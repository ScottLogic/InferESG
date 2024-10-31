import os
import sys
import re
from pypdf import PdfReader
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline


def get_pdf_content_lines(pdf_file_path):
    with open(pdf_file_path, 'rb') as f:
        pdf_reader = PdfReader(f)
        for page in pdf_reader.pages:
            for line in page.extract_text().splitlines():
                yield line


def format_text(lines):

    # Join all lines with a space
    text = ' '.join(lines)

    # Trim leading and trailing whitespace
    text = text.strip()

    return text


def create_pipeline(name: str) -> pipeline:
    # Load the models (takes ca. 1 min per model) - This only happens the first time the models are called
    tokenizer = AutoTokenizer.from_pretrained(name)
    model = AutoModelForSequenceClassification.from_pretrained(name)
    return pipeline("text-classification", model=model, tokenizer=tokenizer)


def read_pdf(pdf_file_path) -> None:
    pipelines = [
        # These models aren't very fast - start by running one model, e.g. finbert-esg
        # create_pipeline("ESGBERT/EnvironmentalBERT-environmental"),
        # create_pipeline("ESGBERT/SocialBERT-social"),
        # create_pipeline("ESGBERT/GovernanceBERT-governance"),
        # create_pipeline("yiyanghkust/finbert-esg"),
        # create_pipeline("yiyanghkust/finbert-esg-9-categories"),
        create_pipeline("nbroad/ESG-BERT"),
    ]
    results = []
    for line in get_pdf_content_lines(pdf_file_path):
        for pipe in pipelines:
            # results.append(f"{pipe(line)[0]['label']}: {line}")
            print(f"{pipe(line)[0]['label']}: {line}")
    # print(results)


def save_pdf_text(pdf_file_path, output_folder='../../../data/pdf_to_text'):
    # Create data folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Generate output filename based on input PDF name
    pdf_name = os.path.splitext(os.path.basename(pdf_file_path))[0]
    output_file = os.path.join(output_folder, f"{pdf_name}_text.txt")

    # Extract and format text
    lines = list(get_pdf_content_lines(pdf_file_path))
    formatted_text = format_text(lines)

    # Write formatted content to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(formatted_text)

    return output_file

"""
Usage: python -m pdf_upload <method> <pdf_file_path>
 Available methods:
   extract - just extract and print the text
   save - extract and save the text to a file

pdf_file_path input example:
    '../../../data/pdf/IBM_SR_2023.pdf'

the save method will output the text file to ../../../data/pdf_to_text/
"""

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <method> <pdf_file_path>")
        print("Available methods:")
        print("  extract - just extract and print the text")
        print("  save - extract and save the text to a file")
        return

    method = sys.argv[1]
    pdf_file_path = sys.argv[2]

    if not os.path.exists(pdf_file_path):
        print(f"Error: PDF file '{pdf_file_path}' not found.")
        return

    if method == "extract":
        read_pdf(pdf_file_path)
    elif method == "save":
        output_file = save_pdf_text(pdf_file_path)
        print(f"Text saved to: {output_file}")
    else:
        print(f"Error: Unknown method '{method}'")
        print("Available methods: extract, save")


if __name__ == "__main__":
    main()

