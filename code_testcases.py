import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_testcases(code_snippet, language="python"):
<<<<<<< HEAD
    # (Simplified for completeness, assuming original logic is kept)
    prompt = f"Analyze the following {language} code snippet. Generate a set of comprehensive unit test cases for it."
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt],
        config={"temperature": 0.5}
    ) 
=======
    if language == "python":
        prompt = f"Analyze the following Python function or code snippet. Generate a set of comprehensive unit test cases for it using the standard 'unittest' or basic assertion format. Focus on edge cases, typical inputs, and error conditions.\n\nCode:\n{code_snippet}"
    elif language == "java":
        prompt = f"Analyze the following Java function or code snippet. Generate a set of comprehensive unit test cases using JUnit. Focus on edge cases, typical inputs, and error conditions.\n\nCode:\n{code_snippet}"
    else:
        raise ValueError("Unsupported language: Choose either 'python' or 'java'.")

    config = {
        "temperature": 0.5,
        "max_output_tokens": 8000,
    }

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt],
        config=config,
    )    
>>>>>>> 24fe9b65d74d5ca10cbb9799e58dd22819d4b058
    test_cases = response.text.strip()
    return test_cases

if __name__ == "__main__":
<<<<<<< HEAD
    pass
=======
    code_input = input("Enter the code snippet to generate test cases for: ")
    language = input("Enter the programming language (python/java): ").lower()
    generated_test_cases = generate_testcases(code_input, language)
    print("Generated Test Cases:\n", generated_test_cases)
>>>>>>> 24fe9b65d74d5ca10cbb9799e58dd22819d4b058
