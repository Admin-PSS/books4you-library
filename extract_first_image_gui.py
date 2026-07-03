import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from extract_first_image import extract_first_image


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Extract First Image from PDF")
        self.resizable(False, False)

        self.pdf_path = tk.StringVar()
        self.output_dir = tk.StringVar()

        pad = {"padx": 10, "pady": 6}

        tk.Label(self, text="PDF file:").grid(row=0, column=0, sticky="w", **pad)
        tk.Entry(self, textvariable=self.pdf_path, width=50).grid(row=0, column=1, **pad)
        tk.Button(self, text="Browse...", command=self.choose_pdf).grid(row=0, column=2, **pad)

        tk.Label(self, text="Output folder:").grid(row=1, column=0, sticky="w", **pad)
        tk.Entry(self, textvariable=self.output_dir, width=50).grid(row=1, column=1, **pad)
        tk.Button(self, text="Browse...", command=self.choose_output_dir).grid(row=1, column=2, **pad)

        tk.Button(self, text="Extract Image", command=self.run_extract, width=20).grid(
            row=2, column=0, columnspan=3, pady=12
        )

    def choose_pdf(self):
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if path:
            self.pdf_path.set(path)
            if not self.output_dir.get():
                self.output_dir.set(str(Path(path).parent))

    def choose_output_dir(self):
        path = filedialog.askdirectory()
        if path:
            self.output_dir.set(path)

    def run_extract(self):
        pdf_path = self.pdf_path.get().strip()
        output_dir = self.output_dir.get().strip()

        if not pdf_path:
            messagebox.showerror("Error", "Please select a PDF file.")
            return
        if not output_dir:
            messagebox.showerror("Error", "Please select an output folder.")
            return

        try:
            result = extract_first_image(pdf_path, output_dir)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract image:\n{e}")
            return

        if result:
            out_path, width, height = result
            messagebox.showinfo(
                "Success", f"Image saved to:\n{out_path}\n\nSize: {width} x {height} px"
            )
        else:
            messagebox.showwarning("No image found", "This PDF has no embedded images.")


if __name__ == "__main__":
    App().mainloop()
