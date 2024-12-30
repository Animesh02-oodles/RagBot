import streamlit as st
import google.generativeai as genai
import base64
from pypdf import PdfReader, PdfWriter
import os


def page_setup():
    st.header("Chat with different types of media/files!", anchor=False, divider="blue")

    hide_menu_style = """
            <style>
            #MainMenu {visibility: hidden;}
            </style>
            """
    st.markdown(hide_menu_style, unsafe_allow_html=True)


def get_typeofpdf():
    st.sidebar.header("Select type of Media", divider='orange')
    typepdf = st.sidebar.radio("Choose one:",
                               ("PDF files",
                                "Images",
                                "Video, mp4 file",
                                "Audio files"))
    return typepdf


def get_llminfo():
    st.sidebar.header("Options", divider='rainbow')
    tip1 = "Select a model you want to use."
    model = st.sidebar.radio("Choose LLM:",
                             ("gemini-1.5-flash",
                              "gemini-1.5-pro",
                              ), help=tip1)
    tip2 = "Lower temperatures are good for prompts that require a less open-ended or creative response, while higher temperatures can lead to more diverse or creative results. A temperature of 0 means that the highest probability tokens are always selected."
    temp = st.sidebar.slider("Temperature:", min_value=0.0,
                              max_value=2.0, value=1.0, step=0.25, help=tip2)
    tip3 = "Used for nucleus sampling. Specify a lower value for less random responses and a higher value for more random responses."
    topp = st.sidebar.slider("Top P:", min_value=0.0,
                              max_value=1.0, value=0.94, step=0.01, help=tip3)
    tip4 = "Number of response tokens, 8194 is limit."
    maxtokens = st.sidebar.slider("Maximum Tokens:", min_value=100,
                                   max_value=5000, value=2000, step=100, help=tip4)
    return model, temp, topp, maxtokens


def merge_pdfs(uploaded_files, output_path):
    writer = PdfWriter()
    for file in uploaded_files:
        file_name = file.name
        with open(file_name, "wb") as f:
            f.write(file.read())
        with open(file_name, "rb") as pdf_file:
            reader = PdfReader(pdf_file)
            for page in reader.pages:
                writer.add_page(page)
    # Save the merged PDF
    with open(output_path, "wb") as merged_pdf:
        writer.write(merged_pdf)


def main():
    page_setup()
    typepdf = get_typeofpdf()
    model, temperature, top_p, max_tokens = get_llminfo()

    if typepdf == "PDF files":
        uploaded_files = st.file_uploader("Choose 1 or more files", accept_multiple_files=True)

        if uploaded_files:
            output_path = "merged_all_pages.pdf"
            merge_pdfs(uploaded_files, output_path)

            st.write(f"Merged PDF saved at: {output_path}")
            with open(output_path, "rb") as pdf_file:
                pdf_data = pdf_file.read()

            # Convert the PDF data to base64
            encoded_pdf = base64.b64encode(pdf_data).decode("utf-8")

            question = st.text_input("Enter your question and hit return.")
            if question:
                response = genai.generate_text(
                    prompt=f"Analyze this PDF content and answer the question: {question}",
                    temperature=temperature,
                    top_p=top_p,
                    max_output_tokens=max_tokens
                )
                st.markdown(response.result)

    # Handling for Images, Video, and Audio files remains unchanged
    elif typepdf == "Images":
        image_file_name = st.file_uploader("Upload your image file.")
        if image_file_name:
            st.write("Image handling logic here...")
            # Logic for image handling can go here

    elif typepdf == "Video, mp4 file":
        video_file_name = st.file_uploader("Upload your video")
        if video_file_name:
            st.write("Video handling logic here...")
            # Logic for video handling can go here

    elif typepdf == "Audio files":
        audio_file_name = st.file_uploader("Upload your audio")
        if audio_file_name:
            st.write("Audio handling logic here...")
            # Logic for audio handling can go here


if __name__ == '__main__':
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    genai.configure(api_key=GOOGLE_API_KEY)  # Use API key directly
    main()