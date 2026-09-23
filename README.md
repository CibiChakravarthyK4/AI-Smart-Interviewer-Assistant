# 🧪 AI Manual Testing Interviewer

An AI-powered **Manual Testing / QA Technical Interviewer** built using **Python, Streamlit, AutoGen, and OpenAI**.

The application conducts a **5-question technical interview** for a Junior Manual Testing / QA position. It evaluates each candidate's answer using an AI agent and provides brief feedback before moving to the next question.

## 🚀 Features

* 🤖 AI-powered Manual Testing interviewer
* 📝 5-question technical interview
* 🧠 AI-based answer evaluation
* 💬 Interactive Streamlit chat interface
* 💡 Instant feedback for each answer
* 🔄 Automatic progression to the next question
* 🎉 Interview completion message
* 🔐 Secure API key management using `.env`

## 🛠️ Technologies & Concepts Used

* **Python** – Application development
* **Streamlit** – Web UI and chat interface
* **AutoGen AgentChat** – AI agent framework
* **AssistantAgent** – AI interviewer agent
* **OpenAIChatCompletionClient** – Connects AutoGen with OpenAI
* **GPT-4o-mini** – LLM used for answer evaluation
* **System Message** – Defines the AI interviewer's role and behavior
* **Prompt / Task** – Sends the interview question and candidate answer to the agent
* **AsyncIO** – Handles asynchronous AI agent execution
* **python-dotenv** – Loads API keys from environment variables
* **Session State** – Maintains interview questions and chat history
* **HTML/CSS** – Customizes the Streamlit UI

## 🔄 How It Works

```text
Candidate
   ↓
Streamlit Chat Interface
   ↓
Interview Question
   ↓
Candidate Answer
   ↓
AutoGen AssistantAgent
   ↓
OpenAI GPT-4o-mini
   ↓
AI Feedback
   ↓
Next Question
   ↓
Interview Completed 🎉
```

## 📂 Project Structure

```text
AI-Manual-Testing-Interviewer/
│
├── main.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## ⚙️ Installation

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd AI-Manual-Testing-Interviewer
python -m venv venv
```

### Activate Virtual Environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## 🔑 Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
```

Add `.env` to `.gitignore` and never upload your API key to GitHub.

## ▶️ Run the Application

```bash
streamlit run main.py
```

## 🎯 Purpose

This project demonstrates how **Generative AI and AutoGen agents** can be integrated with a Streamlit application to create an interactive **AI-powered QA interview assistant**.

## 👨‍💻 Author

**CB Chakravarthy K**

GenAI & AI | QA Automation | Manual Testing
