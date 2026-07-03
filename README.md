# Books4You Library

A small library browser for a personal collection of Burmese ebook PDFs stored on OneDrive.

## Live demo

See the "Environments" / GitHub Pages link on the repo page, or `https://<your-username>.github.io/books4you-library/` once Pages is enabled.

## What it does

- `index.html` — a static, searchable web app: a left-hand author list plus a grid of book covers. Click a book to open it on OneDrive.
- `books_data.json` — metadata for each book (title, author, OneDrive link) plus a path to its cover thumbnail, generated from `Book4You.xlsx`.
- `thumbnails/` — a small cover image per book, fetched from Microsoft Graph's own pre-rendered OneDrive thumbnails (no need to download the actual PDFs).

## Scripts

- `extract_first_image.py` / `extract_first_image_gui.py` — given a local PDF, extract its cover image (handles PDFs whose cover is split into multiple tiled sub-images) at full resolution. CLI and Tkinter GUI versions.
- `fetch_thumbnails.py` — one-time build step that reads `Book4You.xlsx` and pulls a cover thumbnail per book via the Microsoft Graph API (OAuth device-code sign-in, no client secret needed). See the docstring at the top of the file for the Azure app registration steps.

## Regenerating the data

```
python fetch_thumbnails.py <YOUR_AZURE_APP_CLIENT_ID>
```

This resumes safely if interrupted — it skips thumbnails already present in `thumbnails/`.

