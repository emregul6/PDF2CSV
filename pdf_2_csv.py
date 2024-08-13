import os
import pdfplumber
import pandas as pd
import csv

# Directories
input_directory = 'PDF_Box'
output_directory = 'CSV_Box'

#Step 1 : Extract pdfs
def extract_text_from_pdf(pdf_path):
    text = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")

    return '\n\n'.join(text)

#Step 2: format content
def format_text(text):
    text = text.strip()
    text = '\n'.join(line.strip() for line in text.split('\n') if line.strip())
    return text

#Step 3: save them to csv
def save_text_to_csv(text, output_csv_path):
    df = pd.DataFrame({'Content': [text]})
    df.to_csv(output_csv_path, index=False, quoting=csv.QUOTE_NONNUMERIC)

#Step 4: process pdfs
def process_pdfs(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_dir, filename)
            text = extract_text_from_pdf(pdf_path)
            formatted_text = format_text(text)
            csv_filename = f"{os.path.splitext(filename)[0]}.csv"
            csv_path = os.path.join(output_dir, csv_filename)
            save_text_to_csv(formatted_text, csv_path)
            print(f"Converted {filename} to {csv_filename}")

