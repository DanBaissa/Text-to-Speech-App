import os
import tkinter as tk
from tkinter import filedialog, ttk
import pdfplumber
from gtts import gTTS
import threading

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

    return text

def text_to_speech(text, output_path, language='en'):
    tts = gTTS(text=text, lang=language)
    tts.save(output_path)

def browse_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        pdf_path_var.set(file_path)

def convert_to_mp3():
    pdf_path = pdf_path_var.get()
    if not pdf_path:
        return

    output_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
    if not output_path:
        return

    progress_bar["maximum"] = 100
    progress_bar["value"] = 0
    result_var.set("Converting...")

    def conversion_thread():
        text = extract_text_from_pdf(pdf_path)
        text_to_speech(text, output_path)

        progress_bar["value"] = 100
        result_var.set(f"MP3 file saved at {output_path}")

    threading.Thread(target=conversion_thread, daemon=True).start()

app = tk.Tk()
app.title("PDF to MP3 Converter")

pdf_path_var = tk.StringVar()
result_var = tk.StringVar()

frame = tk.Frame(app, padx=10, pady=10)
frame.pack()

pdf_label = tk.Label(frame, text="PDF File:")
pdf_label.grid(row=0, column=0, sticky="e")

pdf_entry = tk.Entry(frame, width=40, textvariable=pdf_path_var)
pdf_entry.grid(row=0, column=1)

pdf_button = tk.Button(frame, text="Browse", command=browse_pdf)
pdf_button.grid(row=0, column=2)

convert_button = tk.Button(frame, text="Convert to MP3", command=convert_to_mp3)
convert_button.grid(row=1, column=1, pady=10)

progress_bar = ttk.Progressbar(frame, length=300)
progress_bar.grid(row=2, column=0, columnspan=3, pady=10)

result_label = tk.Label(frame, textvariable=result_var)
result_label.grid(row=3, column=0, columnspan=3)

app.mainloop()
