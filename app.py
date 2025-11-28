from orchestrator import orchestrate
import streamlit as st

def main():
    st.title("Programming with AI")
    prompt = st.text_area("Enter your code generation prompt:")
    language = st.selectbox("Select Programming Language", ["python", "java"])  # Dropdown to select language

    if st.button("Generate Code"):
        if prompt:
            with st.spinner('Generating and testing code...'):
                result = orchestrate(prompt, language)  # Call orchestrator with selected language
            if result:
                st.success("Code generated!")
                clean_result = result.replace("```python", "").replace("```", "").strip()
                st.code(clean_result, language=language)  # Display code with appropriate syntax highlighting
            else:
                st.error("Failed to generate valid code after multiple attempts.")
        else:
            st.warning("Please enter a prompt to generate code.") 

if __name__ == "__main__":
    main()