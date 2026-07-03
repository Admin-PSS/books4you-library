import sys
from pathlib import Path

import fitz  # PyMuPDF


def _cluster_image_region(page, tol: float = 2.0):
    """Find the image (or group of adjacent tiled images) on a page and
    return its combined placement rect plus the zoom needed to render it
    at (at least) the native resolution of its highest-res tile.
    """
    items = []
    for im in page.get_images(full=True):
        xref = im[0]
        rects = page.get_image_rects(xref)
        if not rects:
            continue
        base = page.parent.extract_image(xref)
        for r in rects:
            items.append([r, base["width"], base["height"]])

    if not items:
        return None

    def touches(a, b):
        expanded = fitz.Rect(a.x0 - tol, a.y0 - tol, a.x1 + tol, a.y1 + tol)
        return expanded.intersects(b)

    clusters = [[it] for it in items]
    merged = True
    while merged:
        merged = False
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                if any(touches(a[0], b[0]) for a in clusters[i] for b in clusters[j]):
                    clusters[i].extend(clusters[j])
                    del clusters[j]
                    merged = True
                    break
            if merged:
                break

    def bbox(cluster):
        rect = cluster[0][0]
        for it in cluster[1:]:
            rect |= it[0]
        return rect

    best = max(clusters, key=lambda c: bbox(c).get_area())
    rect = bbox(best)
    zoom = max(max(it[1] / it[0].width, it[2] / it[0].height) for it in best)
    return rect, zoom


def extract_first_image(pdf_path: str, output_dir: str = ".") -> tuple[Path, int, int] | None:
    doc = fitz.open(pdf_path)
    for page in doc:
        region = _cluster_image_region(page)
        if region is None:
            continue
        rect, zoom = region
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=rect)
        out_path = Path(output_dir) / f"{Path(pdf_path).stem}_first_image.png"
        pix.save(out_path)
        return out_path, pix.width, pix.height
    return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_first_image.py <pdf_path> [output_dir]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."

    result = extract_first_image(pdf_path, output_dir)
    if result:
        out_path, width, height = result
        print(f"Saved: {out_path}")
        print(f"Size: {width} x {height} px")
    else:
        print("No images found in this PDF.")
