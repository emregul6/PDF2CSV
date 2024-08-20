import os
import pdfplumber
import csv
import re

# Static Questions
questions = [
    "PDF Reference",
    "Location Code",
    "Is subcategory?",
    "Element code?",
    "Brand",
    "Type",
    "Condition",
    "Serial number",
    "Indicative replacement cost",
    "Any remarks",
    "Power/capacity",
    "Installation date",
    "Characteristics1",
    "Characteristics2",
    "Pictures"
]


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


# Step 2: Extract answers
def extract_answers(text: str) -> list:
    answers = []
    lines = text.split('\n')
    current_answer = []
    pictures = []
    question_started = False
    pictures_started = False

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if re.match(r"^\d{1,2}b?\.", line):
            if question_started:
                full_answer = ' '.join(current_answer).replace(' - ', '-').strip()
                if pictures_started:
                    # Extract the last picture number
                    picture_numbers = re.findall(r'\d+', full_answer)
                    if picture_numbers:
                        full_answer = picture_numbers[-1]
                    else:
                        full_answer = ""
                answers.append(full_answer)
                current_answer = []
                pictures_started = False
            question_started = True
        elif question_started:
            if "pictures" in line.lower():
                pictures_started = True
            current_answer.append(line)

    if question_started and current_answer:
        full_answer = ' '.join(current_answer).replace(' - ', '-').strip()
        if pictures_started:
            # Extract the last picture number
            picture_numbers = re.findall(r'\d+', full_answer)
            if picture_numbers:
                full_answer = picture_numbers[-1]
            else:
                full_answer = "No picture"
        answers.append(full_answer)

    return answers


# Step 3: Process all PDFs and compile answers into a CSV
def process_pdfs_into_csv(input_dir, output_csv_path):
    all_answers = []

    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_dir, filename)
            text = extract_text_from_pdf(pdf_path)
            answers = extract_answers(text)

            if  len(answers) < 14 or len(answers) > 14:
                print(f"There is an odd one {filename}")
                print(text)


            all_answers.append([filename] + answers)
            print(f"Extracted answers from {filename}")

    # Save to CSV
    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(questions)
        writer.writerows(all_answers)

