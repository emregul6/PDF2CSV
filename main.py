import os
from pdf2csv import process_pdfs_into_csv

# Directories
input_directory = 'PDF_Box'
output_directory = 'CSV_Box'
output_csv = 'All_answers.csv'

if __name__ == '__main__':
    # if not os.path.exists(output_directory):
    #     os.makedirs(output_directory)
    process_pdfs_into_csv(input_directory, os.path.join(output_directory, output_csv))