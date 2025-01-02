# Medical Report Analyzer

This is a Streamlit-based web application designed to analyze medical reports in PDF format. The app extracts the content, cleans it by removing personal information and irrelevant data, and provides health tips based on the analysis of the report.

## Features

- **PDF Upload:** Upload your medical report in PDF format.
- **Text Extraction:** Extracts and processes the text from each page of the medical report.
- **Named Entity Recognition (NER):** Removes sensitive information like personal names, addresses, dates, etc.
- **Health Tips:** Analyzes the report and provides health tips based on the content.
- **Summarization:** Provides a summarized version of the report for quick insights.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-repository/medical-report-analyzer.git
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Requirements

- Python 3.x
- Streamlit
- PyPDF2
- spaCy (with `en_core_web_sm` model)
- Transformers (Hugging Face)
- langchain-anthropic

## Usage

1. Launch the app:

```bash
streamlit run app.py
```

2. Upload your medical report (PDF format).
3. The app will process the text, clean sensitive information, and analyze the content.
4. It will display page-wise analysis and provide a summarized report at the end.

## Functionality

- **Text Cleaning:** The app removes dates, times, personal names, and addresses to ensure that only relevant content is analyzed.
- **Named Entity Recognition (NER):** Uses spaCy to recognize and remove named entities (person names, organizations, etc.).
- **Summarization:** Each chunk of text is summarized using Hugging Face's BART model to provide a concise summary.
- **Health Tips:** The app interacts with the Anthropic API to provide health advice based on the content.

## API Integration

- **Anthropic API:** Uses the ChatAnthropic API for advanced medical report analysis.
- **Hugging Face:** For text summarization using the BART model.

## Example
![WhatsApp Image 2025-01-03 at 01 29 34_996148a7](https://github.com/user-attachments/assets/a6c49284-acb6-4c58-b9fd-19f404cbe195)
![WhatsApp Image 2025-01-03 at 01 30 11_38f918cd](https://github.com/user-attachments/assets/c50e82f1-6da5-4e34-80ea-921681bb2663)
![WhatsApp Image 2025-01-03 at 01 31 37_cabd4089](https://github.com/user-attachments/assets/883cfe46-17f5-429e-88e6-6db637189028)



