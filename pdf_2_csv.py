import os
import pdfplumber
import pandas as pd
import csv

# Directories
input_directory = 'PDF_Box'
output_directory = 'CSV_Box'


# Step 1: Extract PDFs
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


# Step 2: Format content
def format_text(text):
    questions_answers = []
    lines = text.split('\n')
    current_question = None
    current_answer = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check if the line looks like a question
        if line[0].isdigit() and ('.' in line or 'b.' in line):
            if current_question:
                questions_answers.append((current_question, '\n'.join(current_answer)))
            # Start a new question
            current_question = line
            current_answer = []
        else:
            # Collect answers; this might handle cases where answers span multiple lines
            current_answer.append(line)

    # Add the last question-answer pair
    if current_question:
        questions_answers.append((current_question, '\n'.join(current_answer)))

    return questions_answers


# Step 3: Save to CSV
def save_text_to_csv(questions_answers, output_csv_path):
    df = pd.DataFrame(questions_answers, columns=['Question', 'Answer'])
    df.to_csv(output_csv_path, index=False, quoting=csv.QUOTE_NONNUMERIC)


# Step 4: Process PDFs
def process_pdfs(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_dir, filename)
            text = extract_text_from_pdf(pdf_path)
            questions_answers = format_text(text)
            csv_filename = f"{os.path.splitext(filename)[0]}.csv"
            csv_path = os.path.join(output_dir, csv_filename)
            save_text_to_csv(questions_answers, csv_path)
            print(f"Converted {filename} to {csv_filename}")
