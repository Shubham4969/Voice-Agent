# 🎙️ AI Voice Agent

An AI-powered Voice Agent built using Python, FastAPI, and OpenAI APIs. This project enables users to interact with an AI assistant through voice, using speech-to-text for transcription and text-to-speech for natural audio responses.

## 🚀 Features

- 🎤 **Speech-to-Text:** Convert user voice into text using OpenAI transcription.
- 🤖 **AI Assistant:** Generate intelligent responses using OpenAI models.
- 🔊 **Text-to-Speech:** Convert AI-generated responses into natural speech.
- ⚡ **FastAPI Backend:** Fast and efficient API-based architecture.
- 🔄 **Voice Interaction:** Supports voice-based interaction workflows.
- 📚 **Document Integration:** Supports document-based processing and retrieval workflows.

## 🛠️ Tech Stack

- **Language:** Python
- **Backend:** FastAPI
- **AI:** OpenAI API
- **Speech Recognition:** OpenAI `gpt-4o-mini-transcribe`
- **Text-to-Speech:** OpenAI `gpt-4o-mini-tts`
- **Server:** Uvicorn
- **Containerization:** Docker

## 📂 Project Structure

```text
Voice-Agent/
│
├── Big_project.py
├── Big_indexing.py
├── Big_retraval.py
├── docker-compose.yml
├── Employee-Handbook.pdf
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Shubham4969/Voice-Agent.git
cd Voice-Agent
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

Activate it:

**Windows:**
```powershell
.venv\Scripts\activate
```

**Linux / macOS:**
```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
```

Never share your API key publicly.

### 5. Run the Application

```bash
uvicorn main:app --reload
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

## 🔑 Environment Variables

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | OpenAI API authentication key |

## 🎯 Project Objective

The objective of this project is to develop an intelligent voice-based assistant that enables natural human-AI interaction using modern Generative AI and speech technologies.

## 👨‍💻 Author

**Shubham Kumar Singh**

- GitHub: [Shubham4969](https://github.com/Shubham4969)

---

⭐ If you find this project interesting, consider giving it a star!
