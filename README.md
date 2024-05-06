## Introduction
------------
The PDF Chat Assistant is an innovative Python application designed to enhance your interaction with PDF documents. This application leverages a powerful language model to allow users to ask questions in natural language about any loaded PDF document. It intelligently scans the content of the PDF to provide precise answers, making it easier to find information quickly without needing to manually search through the document. 

## How It Works
------------

The application follows these steps to provide responses to your questions:

1. PDF Loading: The app reads PDF documents and extracts their text content.

2. Text Chunking: The extracted text is divided into smaller chunks that can be processed effectively.

3. Language Model: The application utilizes a language model to generate vector representations (embeddings) of the text chunks.

4. Similarity Matching: When you ask a question, the app compares it with the text chunks and identifies the most semantically similar ones.

5. Response Generation: The selected chunks are passed to the language model, which generates a response based on the relevant content of the PDFs.

## Run using Docker
Build the Docker Image:

docker build -t pdf-chat-assistant .

Run the Docker Container:

docker run -p 8501:8501 pdf-chat-assistant

## Output
![Screenshot from 2024-05-06 18-42-51](https://github.com/Grv02/Custom_RAG_pipeline/assets/37537513/c5aa2129-f2e0-43d6-9402-b369bb823f6f)
![Screenshot from 2024-05-06 18-42-37](https://github.com/Grv02/Custom_RAG_pipeline/assets/37537513/49de26f8-fd20-44ec-b376-b44fb7c4872d)

