from pypdf import PdfReader
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline


def get_pdf_content_lines(pdf_file_path):
    with open(pdf_file_path, 'rb') as f:
        pdf_reader = PdfReader(f)
        for page in pdf_reader.pages:
            for line in page.extract_text().splitlines():
                yield line


def create_pipeline(name: str) -> pipeline:
    # Load the models (takes ca. 1 min per model) - This only happens the first time the models are called
    tokenizer = AutoTokenizer.from_pretrained(name)
    model = AutoModelForSequenceClassification.from_pretrained(name)
    return pipeline("text-classification", model=model, tokenizer=tokenizer)


def read_pdf() -> None:
    pipelines = [
        # These models aren't very fast - start by running one model, e.g. finbert-esg
        # create_pipeline("ESGBERT/EnvironmentalBERT-environmental"),
        # create_pipeline("ESGBERT/SocialBERT-social"),
        # create_pipeline("ESGBERT/GovernanceBERT-governance"),
        create_pipeline("yiyanghkust/finbert-esg"),
        # create_pipeline("yiyanghkust/finbert-esg-9-categories"),
        # create_pipeline("nbroad/ESG-BERT"),
    ]
    results = []
    for line in get_pdf_content_lines('../../../data/pdf/IBM_SR_2023.pdf'):
        for pipe in pipelines:
            results.append(f"{pipe(line)[0]['label']}: {line}")
    print(results)


def main():
    read_pdf()


if __name__ == "__main__":
    main()

