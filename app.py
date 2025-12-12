<<<<<<< HEAD
from orchestrator import orchestrate_multi_file
import streamlit as st

def main():
    st.set_page_config(page_title="Hybrid Code Agent", layout="wide")
    st.title("🤖 Hybrid Self-Correcting Code Generation Agent")
    st.markdown("---")
    
    st.markdown("""
        Enter a request. The agent automatically detects if it should generate a **Single-File Python** script, a **Modular FastAPI** project, or a **Spring Boot/Maven** project. It will test and self-correct the code until it runs successfully.
    """)
    
    prompt = st.text_area("Enter your project generation prompt:", height=150)

    if st.button("Generate & Test Project"):
        if prompt:
            with st.spinner('Generating, writing, and testing project...'):
                project_files = orchestrate_multi_file(prompt)
            
            st.markdown("---")
            
            if project_files:
                st.balloons()
                st.success("🎉 Project Generated and Passed Execution Test!")
                st.subheader("Generated Project Files:")
                
                # Display files in expandable sections
                for file_data in project_files:
                    file_name = file_data['file_name']
                    content = file_data['content']
                    
                    # Determine language for highlighting
                    lang_map = {'py': 'python', 'java': 'java', 'xml': 'xml', 'txt': 'text'}
                    file_extension = file_name.split('.')[-1]
                    code_lang = lang_map.get(file_extension, 'text')
                    
                    # Clean up potential markdown tags
                    clean_content = content.replace("```python", "").replace("```java", "").replace("```xml", "").replace("```", "").strip()
                    
                    with st.expander(f"📁 **{file_name}**"):
                        st.code(clean_content, language=code_lang)
                        
            else:
                st.error("🚨 Failed to generate a valid, runnable project after multiple attempts.")
        else:
            st.warning("Please enter a prompt to start generation.") 
=======
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
>>>>>>> 24fe9b65d74d5ca10cbb9799e58dd22819d4b058

if __name__ == "__main__":
    main()