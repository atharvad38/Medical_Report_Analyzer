import streamlit as st
import PyPDF2
import re
import spacy
from transformers import pipeline
from langchain_anthropic import ChatAnthropic
from langchain.schema import AIMessage, SystemMessage, HumanMessage

# Load the spaCy model for Named Entity Recognition (NER)
nlp = spacy.load("en_core_web_sm")

# Hugging Face summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Anthropic API setup
api_key = 'Your API KEY'
model = ChatAnthropic(model='claude-3-sonnet-20240229',api_key=api_key)

# Function to clean the medical report
def clean_medical_report(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "GPE", "ORG"]:
            text = text.replace(ent.text, "")
    text = re.sub(r"(Name|Address|Phone|Age/Gender|Received|Reported)\\s*[:\\-]?\\s*.*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\\b(?:\\d{1,2}[/-]\\d{1,2}[/-]\\d{2,4}|\\d{4}-\\d{2}-\\d{2})\\b", "", text)  # Dates
    text = re.sub(r"\\b(?:\\d{1,2}:\\d{2}(?:\\s*[APMapm]{2})?)\\b", "", text)  # Times
    text = re.sub(r"Dr\\.?\\s+[A-Za-z]+\\s+[A-Za-z]+", "", text, flags=re.IGNORECASE)  # Doctor names
    text = re.sub(r"\\n\\s*\\n", "\\n", text)  # Collapse multiple newlines
    text = text.strip()
    return text

# Streamlit UI
st.title("Medical Report Analyzer")
st.write("Upload your medical report PDF to analyze and get health tips.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

def chunk_text(text, max_length=500):
    sentences = text.split('.')
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_length = len(sentence.split())
        if current_length + sentence_length <= max_length:
            current_chunk.append(sentence)
            current_length += sentence_length
        else:
            chunks.append('. '.join(current_chunk))
            current_chunk = [sentence]
            current_length = sentence_length
    if current_chunk:
        chunks.append('. '.join(current_chunk))
    return chunks


import re

def remove_irrelevant_line(report_text):
    # Regex to match the sentence containing "This page does not contain..." or "This page contains no..."
    cleaned_report = re.sub(r'(?i)this page (does not contain|contains no)[^.]*\.', '', report_text)
    return cleaned_report

if uploaded_file is not None:
    # Load the PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    num_of_pages = len(pdf_reader.pages)

    chat_history = []
    system_message = SystemMessage(
        content="You are a medical report analyzer. I will send you text from a medical report one page at a time. Analyze the report and provide health tips. Ignore irrelevant information like names and addresses. Thanks."
    )
    chat_history.append(system_message)

    complete_report_analysis = ""
    st.write("### Analyzing Report...")
    progress = st.progress(0)

    for i in range(num_of_pages):
        raw_text = pdf_reader.pages[i].extract_text()
        cleaned_text = clean_medical_report(raw_text)

        chat_history.append(HumanMessage(content=cleaned_text))  # Add user's input
        response = model.invoke(chat_history)  # Invoke the model
        complete_report_analysis += response.content  # Append the analysis
        chat_history.append(AIMessage(content=response.content))  # Add AI's response

        st.write(f"### Page {i + 1} Analysis:")
        st.write(response.content)
        progress.progress((i + 1) / num_of_pages)

    # Chunk the complete analysis
    cleaned_report = remove_irrelevant_line(complete_report_analysis)
    text_chunks = chunk_text(cleaned_report)


    # Summarize each chunk
    summaries = []
    for chunk in text_chunks:
        summary = summarizer(chunk, max_length=150, min_length=50, do_sample=False)
        summaries.append(summary[0]['summary_text'])

    # Combine summaries
    final_summary = ' '.join(summaries)



    # Summarize the complete report
    st.write("### Summarized Report")
    st.write(final_summary)

