import fitz 
import faiss
import numpy as np
from transformers import DPRQuestionEncoder, DPRQuestionEncoderTokenizer, AutoModelForCausalLM, AutoTokenizer

# Function to extract text from the PDF
def extract_text_from_pdf(file_path, start_page, end_page):
    document = fitz.open(file_path)
    text = ''
    for page_number in range(start_page, end_page + 1):
        page = document.load_page(page_number)
        text += page.get_text()
    return text

# Function to initialize and return FAISS indexer
def initialize_faiss_index(embedding_dim):
    index = faiss.IndexFlatL2(embedding_dim)
    return index

# Function to encode and index text using FAISS and a DPR encoder
def encode_and_index_text(text, encoder_tokenizer, encoder_model, indexer):
    sentences = text.split('.')
    embeddings = []
    for sentence in sentences:
        inputs = encoder_tokenizer(sentence, return_tensors="pt", padding=True, truncation=True, max_length=512)
        outputs = encoder_model(**inputs)
        embeddings.append(outputs.pooler_output.detach().numpy().squeeze())
    embeddings = np.array(embeddings)
    indexer.add(embeddings)  # Adding all embeddings to the FAISS index
    return sentences, embeddings

# Function to search FAISS index and retrieve contexts
def search_index(query, question_encoder, question_tokenizer, indexer, sentences, k=5):
    question_embedding = question_encoder(**question_tokenizer(query, return_tensors="pt", padding=True, truncation=True)).pooler_output.detach().numpy()
    _, idxs = indexer.search(question_embedding, k)
    return [sentences[i] for i in idxs[0]]

# Function to generate answer from contexts
def generate_answer(contexts, answer_model, answer_tokenizer, max_length=300, num_return_sequences=1):
    input_text = " ".join(contexts)
    inputs = answer_tokenizer.encode(input_text, return_tensors="pt")
    # Ensure the model input does not exceed the max_length limit
    inputs = inputs[:, :max_length-1]  # Limit input size
    output_sequences = answer_model.generate(
        input_ids=inputs,
        max_length=max_length,
        num_return_sequences=num_return_sequences,
        no_repeat_ngram_size=2,  # Helps in reducing repeated phrases
    )
    return [answer_tokenizer.decode(seq, skip_special_tokens=True) for seq in output_sequences]

# Main execution function
def main():
    pdf_path = '1.pdf'
    start_page = 19  # Adjust to your specific start page
    end_page = 63  # Adjust to your specific end page

    # Extract text from PDF
    chapter_text = extract_text_from_pdf(pdf_path, start_page, end_page)

    # Initialize the DPR context encoder for embeddings
    encoder_tokenizer = DPRQuestionEncoderTokenizer.from_pretrained("facebook/dpr-question_encoder-single-nq-base")
    encoder_model = DPRQuestionEncoder.from_pretrained("facebook/dpr-question_encoder-single-nq-base")
    embedding_dim = encoder_model.config.hidden_size
    indexer = initialize_faiss_index(embedding_dim)

    # Encode and index text
    sentences, embeddings = encode_and_index_text(chapter_text, encoder_tokenizer, encoder_model, indexer)

    # Initialize the answer generation model
    answer_tokenizer = AutoTokenizer.from_pretrained("gpt2")
    answer_model = AutoModelForCausalLM.from_pretrained("gpt2")

    # Example question
    question = "what is the smallest unit of biological structure that meets the functional requirements of living ?"
    contexts = search_index(question, encoder_model, encoder_tokenizer, indexer, sentences)
    answer = generate_answer(contexts, answer_model, answer_tokenizer)
    print("Answer:", answer)

if __name__ == "__main__":
    main()
