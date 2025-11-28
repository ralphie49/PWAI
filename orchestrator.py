from code_generation import generate_code
from code_testcases import generate_testcases
from code_testing import test_python_code, test_java_code

def orchestrate(prompt, language="python", max_retries=3):
    retries = 0
    flag = False    
    while retries < max_retries and not flag:
        print(f"Attempt {retries+1} to generate and test code.")
        generated_code = generate_code(prompt, language)
        print("\nGenerated Code:\n", generated_code)
        
        test_cases = generate_testcases(generated_code, language)
        print("\nGenerated Test Cases:\n", test_cases)        
        
        if language == "python":
            test_result = test_python_code(generated_code) 
        elif language == "java":
            test_result = test_java_code(generated_code)
        else:
            test_result = "Unsupported language."
        
        print("\nTest Result:\n", test_result)
        
        if "Error" not in test_result:
            flag = True
            print("Code passed initial execution test successfully.")
            return generated_code
        else:
            print("Code failed the execution test. Retrying...")
            retries += 1

    if not flag:
        print("Max retries reached. Code generation failed.")
        return None

if __name__ == "__main__":
    test_prompt = input("Enter the prompt for the orchestrator: ")
    language = input("Enter the programming language (python/java): ").lower()
    final_code = orchestrate(test_prompt, language)
    
    if final_code:
        print("\n--- FINAL WORKING CODE ---")
        print(final_code)
    else:
        print("\n--- FINAL RESULT: FAILED ---")