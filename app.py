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

if __name__ == "__main__":
    main()