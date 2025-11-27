import subprocess
import os 
import tempfile
import re

def test_python_code(code):
    try:
        exec_scope = {}
        exec(code, exec_scope)
        return "Python code executed successfully."
    except Exception as e:
        return f"Error during execution: {e}"

def test_java_code(code):
    match = re.search(r'public\s+class\s+([A-Za-z0-9_]+)', code)
    if not match:
        return "Java Error: Could not find 'public class' definition."
        
    class_name = match.group(1)
    file_name = f"{class_name}.java"

    with tempfile.TemporaryDirectory() as temp_dir:
        java_file_path = os.path.join(temp_dir, file_name)
        
        try:
            with open(java_file_path, "w") as file:
                file.write(code)
            compile_result = subprocess.run(
                ["javac", file_name], 
                cwd=temp_dir,
                capture_output=True, 
                text=True, 
                check=False
            )
            if compile_result.returncode != 0:
                return f"Java Compilation Error:\n{compile_result.stderr}"
            run_result = subprocess.run(
                ["java", "-cp", temp_dir, class_name], 
                capture_output=True, 
                text=True,
                check=False,
                timeout=5
            )

            if run_result.returncode != 0:
                return f"Java Runtime Error (Exit Code {run_result.returncode}):\n{run_result.stderr}\nOutput:\n{run_result.stdout}"

            return f"Java Code executed successfully:\n{run_result.stdout}"

        except FileNotFoundError:
            return "Error: 'javac' or 'java' command not found. Ensure Java JDK is in your PATH."
        except subprocess.TimeoutExpired:
            return "Error: Java code execution timed out (5 seconds)."
        except Exception as e:
            return f"Error during Java execution process: {e}"

if __name__ == "__main__":
    code_input = input("Enter the code snippet to test: ")
    language = input("Enter the programming language (python/java): ").lower()
    
    if language == "python":
        result = test_python_code(code_input)
    elif language == "java":
        result = test_java_code(code_input)
    else:
        result = "Unsupported language."
    
    print(result)