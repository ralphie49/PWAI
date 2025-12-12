from code_generation import generate_project_plan
from code_testing import create_project_directory, test_project, cleanup_directory

def get_framework_blueprint(prompt):
    """Detects the required language, framework, and architectural constraints."""
    prompt_lower = prompt.lower()
    
    if 'spring boot' in prompt_lower or 'java api' in prompt_lower or 'maven' in prompt_lower:
        return "java", "maven", "Spring Boot: Enforce Controller/Service/Model structure. Generate a JUnit test file to ensure the Maven 'test' goal passes (Exit Code 0) without running the full server."
    elif 'fastapi' in prompt_lower or 'python api' in prompt_lower:
        return "python", "pip", "Modular FastAPI: Enforce /api (routers), /schemas (Pydantic), and /crud structure. Ensure the test client in main.py prints the final verified output."
    elif 'java' in prompt_lower and not any(kw in prompt_lower for kw in ['api', 'maven', 'multiple files']):
        return "java", "javac", "Single-File Java: The primary file (e.g., Main.java) must use a main method and print the final result to stdout for verification."
    elif 'python' in prompt_lower or ('function' in prompt_lower and not 'api' in prompt_lower):
        return "python", "pip", "Single-File Python: The primary file (e.g., main.py) must include a test block that calls the main function and uses 'print()' to output the final result for verification."

    return "python", "pip", "Single-File Python: The primary file (e.g., main.py) must include a test block that calls the main function and uses 'print()' to output the final result for verification."


def orchestrate_multi_file(prompt, max_retries=5):
    language, build_tool, blueprint = get_framework_blueprint(prompt)
    
    initial_prompt = prompt
    retries = 0
    test_result = ""
    
    MAVEN_SUCCESS_STRING = "Maven Project built and unit tests passed successfully."
    PYTHON_SUCCESS_STRING = "Python Project executed successfully."
    
    while retries < max_retries:
        print(f"\n*** Attempt {retries+1}/{max_retries} to Generate and Test Project ({language.upper()}/{build_tool.upper()}) ***")
        
        current_instruction = initial_prompt
        project_context = ""
        
        if retries > 0 and test_result:
            project_context = (
                f"PREVIOUS ATTEMPT FAILED. The full test result was: {test_result}. "
                "ANALYZE the error and FIX the project. You must ensure ALL required files "
                "are correct. CRITICAL: The code must be runnable via the specified build tool "
                "and must print the final verified result to stdout, or pass unit tests (for Java/Maven)."
            )
        
        full_instruction = f"FRAMEWORK INSTRUCTION: {blueprint}\n\nORIGINAL PROJECT REQUEST: {current_instruction}"
        
        project_files = generate_project_plan(full_instruction, language, project_context)
        
        if not project_files:
            print("Generation failed to produce valid file plan (JSON). Retrying...")
            retries += 1
            test_result = "ERROR: Agent failed to produce valid structured JSON output."
            continue

        temp_dir = None
        try:
            temp_dir = create_project_directory(project_files)
            test_result = test_project(temp_dir, language, build_tool)
            
            print(f"\nTest Result:\n{test_result}")
            
            is_maven_success = MAVEN_SUCCESS_STRING in test_result
            is_python_success = PYTHON_SUCCESS_STRING in test_result
            
            is_success = is_maven_success or is_python_success

            if is_success:
                print("\n✅ PROJECT PASSED ALL TESTS SUCCESSFULLY!")
                return project_files
            else:
                print(f"\n❌ Project failed. Error feedback will be used for retry {retries+2}...")
                retries += 1
                
        except Exception as e:
            test_result = f"ORCHESTRATION FAILED: {e}"
            print(test_result)
            retries += 1
        finally:
            if temp_dir:
                cleanup_directory(temp_dir)

    print("\n--- MAX RETRIES REACHED. PROJECT FAILED. ---")
    return None

if __name__ == "__main__":
    test_prompt_python = "Create a single Python file with a function that calculates the Nth Fibonacci number and print the 10th result."
    test_prompt_java = "Create a multi-file Spring Boot application using Java. Use a Service class to define a greeting function, and a Controller to expose it via REST."
    
    orchestrate_multi_file(test_prompt_java)