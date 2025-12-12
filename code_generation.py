import os
<<<<<<< HEAD
import json
=======
>>>>>>> 24fe9b65d74d5ca10cbb9799e58dd22819d4b058
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

<<<<<<< HEAD
def generate_project_plan(prompt, language="python", project_context=""):
    """
    Generates a structured plan and code for a multi-file project.
    The output MUST be a strict JSON array with full relative file paths.
    """
    
    # 1. Define the system instruction for structured output
    system_instruction = (
        "You are an expert software architect and developer. Your primary goal is to strictly follow the "
        "FRAMEWORK INSTRUCTION provided by the user prompt and respond ONLY with a valid JSON array. "
        "This array must contain one object for every file required for the project, using full relative paths (e.g., 'src/main/java/file.java'). "
        "CRITICAL: Always generate the necessary build files (requirements.txt or pom.xml) and include logic that prints the final result for automated testing."
        f"\n\nJSON Schema Example:\n"
        f"[\n"
        f"  {{'file_name': 'main.{language}', 'content': 'The complete code for this file.'}},\n"
        f"  {{'file_name': 'requirements.txt', 'content': 'flask'}}\n"
        f"]"
    )
    
    # 2. Construct the prompt with context
    user_prompt = f"{prompt}\n\n"
    if project_context:
        user_prompt += f"EXISTING PROJECT CONTEXT/ERROR FEEDBACK:\n{project_context}\n\n"
        user_prompt += "ANALYZE the context and error, then provide a NEW, complete JSON array for the entire project, fixing any errors found. Ensure ALL required files are present and correct."
    else:
        user_prompt += "Generate the initial project structure and complete code."

    # 3. Call the API
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[system_instruction, user_prompt],
            config={"temperature": 0.3}
        )
    except Exception as e:
        print(f"API Call Failed: {e}")
        return None
    
    # 4. Handle JSON extraction and parsing
    raw_text = response.text.strip()
    try:
        if raw_text.startswith('```json'):
            raw_text = raw_text[raw_text.find('```json') + len('```json'):]
            raw_text = raw_text[:raw_text.rfind('```')]
        
        project_files = json.loads(raw_text.strip())
        
        if not isinstance(project_files, list) or not all(isinstance(f, dict) and 'file_name' in f and 'content' in f for f in project_files):
             raise ValueError("Parsed JSON is not a valid list of file dictionaries.")
             
        return project_files
        
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON output from generator: JSON DECODE ERROR. Raw output was: {raw_text[:200]}...")
        return None
    except Exception as e:
        print(f"Error processing project files: {e}")
        return None
=======
def generate_code(prompt, language="python"):
    if language == "python":
        model_name = "gemini-2.5-flash"
        system_instruction = "You are a highly skilled Python code generator. Only respond with the requested, complete, and runnable Python code. Do not include any extra text, explanations, or markdown formatting (e.g., ```python)."
    elif language == "java":
        model_name = "gemini-2.5-flash" 
        system_instruction = "You are a highly skilled Java code generator. Only respond with the requested, complete, and runnable Java code. Do not include any extra text, explanations, or markdown formatting (e.g., ```java)."
    else:
        raise ValueError("Unsupported language: Choose either 'python' or 'java'.")
    
    config = {
        "system_instruction": system_instruction,
        "max_output_tokens": 8000,
        "temperature": 0.5,
    }

    response = client.models.generate_content(
        model=model_name,
        contents=[prompt],
        config=config,
    )
    
    code = response.text.strip()
    return code

if __name__ == "__main__":
    user_prompt = input("Enter your code generation prompt: ")
    language = input("Enter the programming language (python/java): ").lower()
    generated_code = generate_code(user_prompt, language)
    print("Generated Code:\n", generated_code)
>>>>>>> 24fe9b65d74d5ca10cbb9799e58dd22819d4b058
