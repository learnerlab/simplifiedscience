import os
import openai
import streamlit as st
import fitz  # PyMuPDF
import io

# Attempt to load the OpenAI API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key is None:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
else:
    openai.api_key = openai_api_key

def process_question(question, document_content=None):
    if openai.api_key is None:
        return "Error: OpenAI API key is not set."

    # Craft the prompt to align with the Simplified Science behavior
    prompt = (
        "The following is a question about a scientific topic. "
        "Provide a clear and simple explanation suitable for a general audience: "
        f"{question}"
    )
    
    # If a document is uploaded, append its content to the prompt
    if document_content:
        prompt += (
            "\n\nAttached is a scientific paper. Summarize the key points and conclusions in simple terms:\n"
            f"{document_content}"
        )
    
    # Call the OpenAI API with the crafted prompt
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500
    )
    
    # Extract the text from the response
    return response.choices[0].text.strip()

def read_pdf(file_data):
    # Open the PDF file from the uploaded BytesIO object
    pdf = fitz.open(stream=file_data, filetype="pdf")
    text = ""
    # Extract text from each page of the PDF
    for page in pdf:
        text += page.get_text()
    pdf.close()
    return text

def main():
    st.title('Simplified Science GPT App')
    user_question = st.text_input('Enter your question about science here:')
    
    # File uploader for PDF documents
    uploaded_file = st.file_uploader("Upload a scientific paper (optional):", type=['pdf'])

    document_content = None
    if uploaded_file is not None:
        # Convert the uploaded file to a BytesIO object
        file_bytes = io.BytesIO(uploaded_file.read())
        # Check the uploaded file type and process accordingly
        if uploaded_file.type == "application/pdf":
            document_content = read_pdf(file_bytes)
        else:
            st.error("Unsupported file type. Please upload a PDF.")
    
    if st.button('Submit'):
        # Use a spinner while generating the response
        with st.spinner('Generating response...'):
            answer = process_question(user_question, document_content)
            st.write(answer)

if __name__ == '__main__':
    main()
