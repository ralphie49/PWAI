import os
import json
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_project_plan(prompt, language="python", project_context=""):
    """
    Generates a structured plan and code for a multi-file project.
    The output MUST be a strict JSON array with full relative file paths.
    """
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
    
    user_prompt = f"{prompt}\n\n"
    if project_context:
        user_prompt += f"EXISTING PROJECT CONTEXT/ERROR FEEDBACK:\n{project_context}\n\n"
        user_prompt += "ANALYZE the context and error, then provide a NEW, complete JSON array for the entire project, fixing any errors found. Ensure ALL required files are present and correct."
    else:
        user_prompt += "Generate the initial project structure and complete code."

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[system_instruction, user_prompt],
            config={"temperature": 0.3}
        )
    except Exception as e:
        print(f"API Call Failed: {e}")
        return None
    
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