import os
import tkinter as tk
from tkinter import filedialog, ttk
import pdfplumber
from gtts import gTTS
import threading
import glob

def extract_text_from_pdf(pdf_path, progress_callback=None):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        total_pages = len(pdf.pages)
        for i, page in enumerate(pdf.pages):
            current_text = page.extract_text() or ""
            tables = page.extract_tables()
            figures = page.images

            if tables or figures:
                current_text += " See PDF for tables and figures."

            text += current_text

            if progress_callback:
                progress_callback(i+1, total_pages)

    return text

def text_to_speech(text, output_path, language='en'):
    tts = gTTS(text=text, lang=language)
    tts.save(output_path)

def browse_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        pdf_path_var.set(file_path)

def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_path_var.set(folder_path)

def convert_to_mp3():
    pdf_path = pdf_path_var.get()
    if not pdf_path:
        return

    output_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
    if not output_path:
        return

    result_var.set("Working...")

    def conversion_thread():
        try:
            text = extract_text_from_pdf(pdf_path)
            text_to_speech(text, output_path)
            result_var.set("Complete")
        except Exception as e:
            result_var.set("Conversion Failed")

    threading.Thread(target=conversion_thread, daemon=True).start()

def convert_folder_to_mp3s():
    folder_path = folder_path_var.get()
    if not folder_path:
        return

    result_var.set("Working...")

    def conversion_thread():
        try:
            pdf_files = glob.glob(os.path.join(folder_path, '*.pdf'))
            for pdf_path in pdf_files:
                output_path = os.path.splitext(pdf_path)[0] + '.mp3'
                text = extract_text_from_pdf(pdf_path)
                text_to_speech(text, output_path)
            result_var.set("Complete")
        except Exception as e:
            result_var.set("Conversion Failed")

    threading.Thread(target=conversion_thread, daemon=True).start()

app = tk.Tk()
app.title("PDF to MP3 Converter")

pdf_path_var = tk.StringVar()
folder_path_var = tk.StringVar()
result_var = tk.StringVar()

frame = tk.Frame(app, padx=10, pady=10)
frame.pack()

pdf_label = tk.Label(frame, text="PDF File:")
pdf_label.grid(row=0, column=0, sticky="e")

pdf_entry = tk.Entry(frame, width=40, textvariable=pdf_path_var)
pdf_entry.grid(row=0, column=1)

pdf_button = tk.Button(frame, text="Browse", command=browse_pdf)
pdf_button.grid(row=0, column=2)

folder_label = tk.Label(frame, text="Folder:")
folder_label.grid(row=1, column=0, sticky="e")

folder_entry = tk.Entry(frame, width=40, textvariable=folder_path_var)
folder_entry.grid(row=1, column=1)

folder_button = tk.Button(frame, text="Browse", command=browse_folder)
folder_button.grid(row=1, column=2)

convert_button = tk.Button(frame, text="Convert PDF to MP3", command=convert_to_mp3)
convert_button.grid(row=2, column=1, pady=10)

convert_folder_button = tk.Button(frame, text="Convert Folder to MP3s", command=convert_folder_to_mp3s)
convert_folder_button.grid(row=3, column=1, pady=10)

result_label = tk.Label(frame, textvariable=result_var)
result_label.grid(row=4, column=0, columnspan=3)

app.mainloop()

