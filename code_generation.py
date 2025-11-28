import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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