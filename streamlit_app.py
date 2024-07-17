import os
import streamlit as st
from mistralai.client import MistralClient

# Set the API key directly for testing purposes
os.environ["MISTRAL_API_KEY"] = "Mdv0nFKHxWOtJYnTA0YVZGLHeBlzMLly"

# Retrieve the API key from the environment variable
api_key = os.getenv("MISTRAL_API_KEY")

if not api_key:
    st.error("API key is not set. Please set the MISTRAL_API_KEY environment variable.")
else:
    client = MistralClient(api_key=api_key)

    def refactor_code(code, language):
        prompt = f"Refactor the following {language} code to improve readability and performance:\n\n{code}"
        response = client.completion(
            model="codestral-latest",
            prompt=prompt,
            max_tokens=512,
        )
        return response.choices[0].message.content

    def analyze_code(code, language):
        prompt = f"Analyze the following {language} code and provide detailed refactoring suggestions:\n\n{code}"
        response = client.completion(
            model="codestral-latest",
            prompt=prompt,
            max_tokens=512,
        )
        return response.choices[0].message.content

    def save_report(language, original_code, analysis, refactored_code):
        report_content = (
            f"Language: {language}\n\n"
            f"Original Code:\n{original_code}\n\n"
            f"Analysis and Refactoring Suggestions:\n{analysis}\n\n"
            f"Refactored Code:\n{refactored_code}"
        )
        with open("refactoring_report.txt", "w") as file:
            file.write(report_content)
        return "refactoring_report.txt"

    # Streamlit interface
    st.title("CODE SCULPTOR")
    st.subheader("An AI-Driven Code Refactoring Tool")

    language = st.text_input("Enter the programming language:")
    if st.button("Select Language"):
        if not language:
            st.warning("Please enter a programming language.")
    
    code = st.text_area("Enter your code here:", height=400)


    if st.button("Analyze Code"):
        if code and language:
            analysis = analyze_code(code, language)
            st.subheader("Analysis and Refactoring Suggestions")
            st.markdown(analysis.replace('\n', '  \n'))  # Use Markdown to handle line breaks
        else:
            st.warning("Please enter code and select a programming language to analyze.")

    if st.button("Refactor Code"):
        if code and language:
            refactored_code = refactor_code(code, language)
            st.subheader("Original Code")
            st.code(code)
            st.subheader("Refactored Code")
            st.code(refactored_code)
        else:
            st.warning("Please enter code and select a programming language to refactor.")

    if st.button("Download Refactored Code"):
        if code and language:
            refactored_code = refactor_code(code, language)
            st.download_button(label="Download Refactored Code", data=refactored_code, file_name="refactored_code.py")
        else:
            st.warning("Please enter code and select a programming language to download refactored code.")

    if st.button("Save Report"):
        if code and language:
            analysis = analyze_code(code, language)
            refactored_code = refactor_code(code, language)
            report_path = save_report(language, code, analysis, refactored_code)
            with open(report_path, "r") as file:
                st.download_button(label="Download Report", data=file.read(), file_name="refactoring_report.txt")
        else:
            st.warning("Please enter code and select a programming language to save the report.")
