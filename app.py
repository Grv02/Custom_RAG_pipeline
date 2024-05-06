import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering
import torch

def get_pdf_text(pdf_docs, start_page, end_page):
    """
    Extract text from PDF files within a specified range of pages.

    Args:
        pdf_docs (list): List of uploaded PDF files.
        start_page (int): Starting page number.
        end_page (int): Ending page number.

    Returns:
        str: Concatenated text extracted from the specified range of pages in the PDFs.
    """
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        num_pages = len(pdf_reader.pages)
        # Adjust the end_page if it exceeds the number of pages in the document
        end_page = min(end_page, num_pages)
        # Process only the specified range of pages
        for page_number in range(start_page - 1, end_page):  # adjust for zero-indexing
            text += pdf_reader.pages[page_number].extract_text()
    return text

def get_answer(question, context):
     """
    Get an answer to a question based on a given context using DistilBERT model.

    Args:
        question (str): The question to be answered.
        context (str): The context (document text) in which to search for the answer.

    Returns:
        str: The answer to the question found in the context.
    """
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased-distilled-squad')
    model = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-uncased-distilled-squad')
    inputs = tokenizer.encode_plus(question, context, add_special_tokens=True, return_tensors="pt", truncation=True, max_length=512)
    outputs = model(**inputs)
    answer_start_scores, answer_end_scores = outputs.start_logits, outputs.end_logits
    answer_start = torch.argmax(answer_start_scores)
    answer_end = torch.argmax(answer_end_scores) + 1
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][answer_start:answer_end]))
    return answer

def main():
    load_dotenv()
    st.set_page_config(page_title="QA with PDF", page_icon=":book:")
    st.header("Question Answering with PDFs :book:")
    
    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here:", accept_multiple_files=True)
        start_page = st.number_input("Start Page", min_value=1, value=1)
        end_page = st.number_input("End Page", min_value=1, value=1)
        
        if st.button("Process PDFs") and pdf_docs:
            with st.spinner("Extracting text from PDF"):
                raw_text = get_pdf_text(pdf_docs, start_page, end_page)
            st.session_state.context = raw_text

    user_question = st.text_input("Ask a question based on your documents:")
    if user_question and 'context' in st.session_state:
        with st.spinner("Finding answers"):
            answer = get_answer(user_question, st.session_state.context)
            st.write("Answer:", answer)

if __name__ == '__main__':
    main()

