import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_testcases(code_snippet, language="python"):
    prompt = f"Analyze the following {language} code snippet. Generate a set of comprehensive unit test cases for it."
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt],
        config={"temperature": 0.5}
    ) 
    test_cases = response.text.strip()
    return test_cases

if __name__ == "__main__":
    pass