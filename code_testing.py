import subprocess
import os 
import tempfile
import shutil
import sys 

MAVEN_EXECUTABLE_PATH = r"C:\Program Files\Apache\Maven\apache-maven-3.9.11\bin\mvn.cmd"

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
        if isinstance(command, list):
            command_str = ' '.join(command)
        else:
            command_str = command
            
        result = subprocess.run(
            command_str,
            cwd=temp_dir,
            capture_output=True,
            text=True,
            timeout=timeout, 
            check=False,
            env=os.environ,
            shell=True 
        )
        return result
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return f"EXECUTION_ERROR: {e}" 

def test_maven_project(temp_dir):
    """Compiles and tests a Maven project (Exit Code 0 is success)."""
    print("[Tool]: Running Maven clean and test...")
    
    quoted_executable = f'"{MAVEN_EXECUTABLE_PATH}"'
    result = run_subprocess([quoted_executable, "clean", "test"], temp_dir, timeout=120)
    
    if result == "TIMEOUT":
        return "Execution Error: Maven build timed out (120 seconds)."
    elif isinstance(result, str) and result.startswith("EXECUTION_ERROR"):
        return result

    if result.returncode != 0:
        error_output = '\n'.join(result.stdout.strip().splitlines()[-100:] + result.stderr.strip().splitlines()[-100:])
        return f"Maven Build/Test Error (Exit Code {result.returncode}):\n{error_output}"
        
    return f"Maven Project built and unit tests passed successfully.\nOutput (Last 10 lines):\n{'\n'.join(result.stdout.strip().splitlines()[-10:])}"

def test_javac_project(temp_dir):
    """Compiles a single Java file using javac and executes it using java."""
    
    main_java_file_path = None
    for root, _, files in os.walk(temp_dir):
        for name in files:
            if name.endswith('.java'):
                main_java_file_path = os.path.join(root, name) 
                break
        if main_java_file_path:
            break

    if not main_java_file_path:
        return "Execution Error: Could not find any Java file (.java) to compile in the project structure."

    main_file_name = os.path.basename(main_java_file_path)
    main_class = main_file_name.replace('.java', '')
    
    print(f"[Tool]: Compiling single Java file: {main_file_name}...")

    compile_command = ["javac", main_java_file_path]
    compile_result = run_subprocess(compile_command, temp_dir, timeout=10) 

    if compile_result.returncode != 0:
        return f"Compilation Error (Exit Code {compile_result.returncode}):\n{compile_result.stderr}"

    print("[Tool]: Compilation successful. Running Java program...")

    run_command = ["java", "-cp", temp_dir, main_class]
    run_result = run_subprocess(run_command, temp_dir, timeout=10)
        
    if run_result.returncode != 0:
        return f"Runtime Error (Exit Code {run_result.returncode}):\n{run_result.stderr}\nOutput:\n{run_result.stdout}"

    if run_result.stdout.strip():
        return f"Python Project executed successfully.\nOutput:\n{run_result.stdout.strip()}"
    else:
        return "Java Program executed, but produced no standard output. The agent must include a print() statement for verification."

def test_python_project(temp_dir):
    """Installs dependencies and executes a Python project."""
    
    requirements_path = os.path.join(temp_dir, "requirements.txt")
    if os.path.exists(requirements_path):
        print("[Tool]: Installing dependencies from requirements.txt...")
        install_command = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        install_result = run_subprocess(install_command, temp_dir, timeout=30)
        
        if install_result == "TIMEOUT" or isinstance(install_result, str) and install_result.startswith("EXECUTION_ERROR"):
            return f"Installation Error: {install_result}"
        if install_result.returncode != 0:
            return f"Installation Error (Exit Code {install_result.returncode}):\n{install_result.stderr}"
        print("[Tool]: Dependencies installed successfully.")

    main_file = next((f for f in os.listdir(temp_dir) if f.endswith('.py') and f != '__init__.py'), None)
    
    if not main_file:
        return "Execution Error: Could not find main entry point (.py file)."
        
    print(f"[Tool]: Running project entry point: {main_file}")
    
    run_command = [sys.executable, main_file]
    result = run_subprocess(run_command, temp_dir, timeout=15)
    
    if result == "TIMEOUT":
        return "Execution Error: Python project timed out (15 seconds)."
    elif isinstance(result, str) and result.startswith("EXECUTION_ERROR"):
        return result

    if result.returncode != 0:
        return f"Runtime Error (Exit Code {result.returncode}):\n{result.stderr}\nOutput:\n{result.stdout}"
    
    if result.stdout.strip():
        return f"Python Project executed successfully.\nOutput:\n{result.stdout.strip()}"
    else:
        return "Python Project executed, but produced no standard output. The agent must include a print() statement for verification."

def test_project(temp_dir, language, build_tool):
    """The unified function called by the orchestrator to decide the testing method."""
    
    if build_tool == "maven":
        return test_maven_project(temp_dir)
    elif language == "python":
        return test_python_project(temp_dir)
    elif language == "java" and build_tool == "javac":
        return test_javac_project(temp_dir)
    else:
        return f"Test Error: Unsupported build tool/language combination: {language}/{build_tool}."

def cleanup_directory(temp_dir):
    """Removes the temporary directory and all its contents."""
    try:
        shutil.rmtree(temp_dir)
        print(f"\n[FileManager]: Cleaned up directory: {temp_dir}")
    except Exception as e:
        print(f"[FileManager] Error cleaning up {temp_dir}: {e}")