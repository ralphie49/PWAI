import subprocess
import os 
import tempfile
<<<<<<< HEAD
import shutil
import sys 

# --- CRITICAL FIX: Defined MAVEN_EXECUTABLE_PATH outside the function ---
# Your system path is already defined here:
MAVEN_EXECUTABLE_PATH = r"C:\Program Files\Apache\Maven\apache-maven-3.9.11\bin\mvn.cmd"

# --- Multi-File Writer Tool (No changes needed) ---
def create_project_directory(files: list[dict]):
    temp_dir = tempfile.mkdtemp()
    print(f"\n[FileManager]: Created temp project directory: {temp_dir}")
    
    for file_data in files:
        file_name = file_data.get('file_name')
        content = file_data.get('content')
        
        if not file_name or content is None:
            print(f"[FileManager] Skipping invalid file data: {file_data}")
            continue
            
        file_path = os.path.join(temp_dir, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"[FileManager] Wrote file: {file_name}")
        except Exception as e:
            print(f"[FileManager] Error writing {file_name}: {e}")
            
    return temp_dir

def run_subprocess(command, temp_dir, timeout=15):
    """Helper function to run any subprocess command and return structured output."""
    try:
        # CRITICAL FIX 1: Convert list to string if shell=True is used
        if isinstance(command, list):
            command_str = ' '.join(command)
        else:
            command_str = command
            
        result = subprocess.run(
            command_str, # Use the string command
            cwd=temp_dir,
            capture_output=True,
            text=True,
            timeout=timeout, 
            check=False,
            env=os.environ,
            # CRITICAL FIX 2: Force execution through the system shell (fixes Maven/Path issue)
            shell=True 
        )
        return result
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return f"EXECUTION_ERROR: {e}" 

# --- Maven Project Testing (Requires JDK/Maven installed) ---
def test_maven_project(temp_dir):
    """Compiles and tests a Maven project (Exit Code 0 is success)."""
    print("[Tool]: Running Maven clean and test...")
    
    # CRITICAL FIX 3: Wrap the executable path in double quotes (")
    # This prevents the shell from breaking the path at the space in "Program Files".
    # The f-string adds the quotes: '"C:\Program Files\..."'
    quoted_executable = f'"{MAVEN_EXECUTABLE_PATH}"'
    
    # Passes list [quoted_executable, "clean", "test"], which run_subprocess converts to string
    # E.g., '"C:\Program Files\...\mvn.cmd" clean test'
    result = run_subprocess([quoted_executable, "clean", "test"], temp_dir, timeout=120)
    
    if result == "TIMEOUT":
        return "Execution Error: Maven build timed out (120 seconds)."
    elif isinstance(result, str) and result.startswith("EXECUTION_ERROR"):
        return result

    if result.returncode != 0:
        error_output = '\n'.join(result.stdout.strip().splitlines()[-100:] + result.stderr.strip().splitlines()[-100:])
        return f"Maven Build/Test Error (Exit Code {result.returncode}):\n{error_output}"
        
    return f"Maven Project built and unit tests passed successfully.\nOutput (Last 10 lines):\n{'\n'.join(result.stdout.strip().splitlines()[-10:])}"

# --- Python Project Testing ---
def test_python_project(temp_dir):
    """Installs dependencies and executes a Python project."""
    
    # 1. Dependency Installation
    requirements_path = os.path.join(temp_dir, "requirements.txt")
    if os.path.exists(requirements_path):
        print("[Tool]: Installing dependencies from requirements.txt...")
        # The command for installing pip dependencies
        install_command = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        install_result = run_subprocess(install_command, temp_dir, timeout=30)
        
        if install_result == "TIMEOUT" or isinstance(install_result, str) and install_result.startswith("EXECUTION_ERROR"):
            return f"Installation Error: {install_result}"
        if install_result.returncode != 0:
            return f"Installation Error (Exit Code {install_result.returncode}):\n{install_result.stderr}"
        print("[Tool]: Dependencies installed successfully.")

    # 2. Execution (Finds main file: app.py, main.py, or the single .py file)
    main_file = next((f for f in os.listdir(temp_dir) if f.endswith('.py') and f != '__init__.py'), None)
    
    if not main_file:
        return "Execution Error: Could not find main entry point (.py file)."
        
    print(f"[Tool]: Running project entry point: {main_file}")
    
    # The command for running the Python file
    run_command = [sys.executable, main_file]
    result = run_subprocess(run_command, temp_dir, timeout=15)
    
    if result == "TIMEOUT":
        return "Execution Error: Python project timed out (15 seconds)."
    elif isinstance(result, str) and result.startswith("EXECUTION_ERROR"):
        return result

    if result.returncode != 0:
        return f"Runtime Error (Exit Code {result.returncode}):\n{result.stderr}\nOutput:\n{result.stdout}"
    
    # Success Check
    if result.stdout.strip():
         return f"Python Project executed successfully.\nOutput:\n{result.stdout.strip()}"
    else:
         return "Python Project executed, but produced no standard output. The agent must include a print() statement for verification."

# --- Polymorphic Test Wrapper ---
def test_project(temp_dir, language, build_tool):
    """The unified function called by the orchestrator to decide the testing method."""
    
    if build_tool == "maven":
        return test_maven_project(temp_dir)
    elif language == "python":
        return test_python_project(temp_dir)
    elif language == "java" and build_tool == "javac":
        return "Testing single-file Java via javac is not fully implemented in this hybrid agent yet. Try a Python single file or a Maven multi-file project."
    else:
        return f"Test Error: Unsupported build tool/language combination: {language}/{build_tool}."

def cleanup_directory(temp_dir):
    """Removes the temporary directory and all its contents."""
    try:
        shutil.rmtree(temp_dir)
        print(f"\n[FileManager]: Cleaned up directory: {temp_dir}")
    except Exception as e:
        print(f"[FileManager] Error cleaning up {temp_dir}: {e}")
=======
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
>>>>>>> 24fe9b65d74d5ca10cbb9799e58dd22819d4b058
