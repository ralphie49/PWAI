This project is a multi-agent, self-improving code-generation system powered by Google Gemini 2.5 Flash.
It can:

Generate runnable Python or Java code

Compile & run the generated code

Test execution

Automatically re-generate and fix code

Loop until a correct solution is produced

Display and final output using Streamlit UI


The system consists of four agents:

1️⃣ Code Generation Agent (Gemini)

Creates complete runnable code files based on user instructions.

2️⃣ Build & Run Agent

Compiles Java or runs Python scripts in a sandbox temp directory.

3️⃣ Testing Agent

Executes the generated program and returns exit code, stdout, stderr.

4️⃣ Orchestrator Agent

Runs a loop:
Generate → Test → Fix → Regenerate
until success or max attempts reached.

📂 Project Structure
.
├── app.py
├── code_generation.py
├── code_testing.py
├── orchestrator.py
├── requirements.txt
└── README.md

⚙️ Installation & Setup

Follow these steps to run the project.

1️⃣ Clone the Repository
git clone https://github.com/ralphie49/PWAI.git
cd PWAI

2️⃣ Create and Activate Virtual Environment
Windows (PowerShell)
python -m venv venv
.\venv\Scripts\activate

Mac / Linux
python3 -m venv venv
source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Set Up Gemini API Key

Create an API key here:

🔗 https://aistudio.google.com/app/apikey

Then set the API key in your environment.

Windows (PowerShell)
setx GEMINI_API_KEY "your_api_key_here"


Restart terminal, activate venv again:

.\venv\Scripts\activate

Mac / Linux
export GEMINI_API_KEY="your_api_key_here"


5️⃣ Run the Streamlit App
streamlit run app.py


Your browser will open:

👉 http://localhost:8501

🖥️ How to Use the App

Enter any task, e.g.:

Select output language (python or java)

Click Run

The system will:

Generate code using Gemini 2.5 Flash

Run and test the code

Automatically fix issues

Loop until success

Show final runnable file

 
 
Requirements: 

Python 3.8+

Java JDK 11+ 

Streamlit

Google google-genai library

Internet connection for model inference

⚡ Technology Stack
Component	Technology
LLM	Gemini 2.5 Flash
UI	Streamlit
Code Execution	Python subprocess sandbox
Languages Supported	Python, Java
Agents	Custom multi-agent architecture

