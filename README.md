# Agentic Study Planner 🧠📅

An AI-powered web application that automatically generates optimized study schedules and syncs them directly to your Google Calendar. Built with **CrewAI** and **Flask**, this tool takes the hassle out of exam preparation by calculating subjects, days, and hours to create a balanced routine.

![Study Planner Demo](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web_App-black?logo=flask)
![CrewAI](https://img.shields.io/badge/CrewAI-Agentic_Framework-orange)

## ✨ Features
* **Intelligent Allocation**: Uses CrewAI to dynamically calculate how many hours you should spend on each subject based on your exam timeline.
* **Google Calendar Integration**: Automatically creates non-overlapping events in your Google Calendar for every study block.
* **Modern Interface**: A sleek, glassmorphism web interface to input your study details easily.
* **Multi-LLM Support**: Configured to work beautifully out-of-the-box with Gemini via `langchain-google-genai` or OpenAI.

---

## 🚀 Quick Start & Installation

### 1. Prerequisites
- Python 3.10+
- A Google Cloud Project with the **Google Calendar API** enabled.
- Your project's `credentials.json` file downloaded from Google Cloud.

### 2. Clone the Repository
```bash
git clone https://github.com/Vish-2101/study-planner-v1.git
cd study-planner-v1
```

### 3. Setup Virtual Environment
```bash
python -m venv myenv
source myenv/bin/activate  # On Windows use: myenv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Environment Variables & Google Auth
1. **Google Auth**: Place your `credentials.json` in the root of the project directory. 
2. **API Keys**: Make a copy of `.env.example`, rename it to `.env`, and add your chosen LLM Key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   # Or use OPENAI_API_KEY=your_openai_key
   
   # Optional: Stop CrewAI telemetry
   CREWAI_TELEMETRY_OPT_OUT=true
   CREWAI_TRACING_ENABLED=false
   ```

### 6. Run the Application
Start the Flask server:
```bash
python app.py
```
* Open your browser and go to `http://127.0.0.1:5001`.
* During your first run, your terminal will prompt you to authorize Google Calendar in your browser. This generates a `token.json` file for future uses.

---

## 🛠 Project Structure
* `app.py`: The Flask Web Server.
* `main.py`: The underlying logic containing the CrewAI Agent and Tasks.
* `planner_tools.py`: Custom CrewAI tool that calculates study hour distribution.
* `calendar_tool.py`: Custom CrewAI tool that interfaces with the Google Calendar v3 API.
* `templates/` & `static/`: HTML, CSS, and JS files for the sleek user interface.

## 🤝 Contributing
Feel free to fork this project, submit pull requests, or open an issue if you encounter any bugs!

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).
