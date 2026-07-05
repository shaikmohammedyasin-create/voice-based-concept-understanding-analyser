<div align="center">

# 🧠 VBCUA — Voice-Based Concept Understanding Analyser

**AI-Powered Formative Knowledge Evaluation via Spoken Explanations**

[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B?style=flat-square&logo=streamlit)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-4285F4?style=flat-square&logo=google)](https://ai.google.dev)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python)](https://python.org)

</div>

---

## Overview

VBCUA is an AI-powered educational assessment platform that evaluates a student's conceptual understanding from spoken explanations. The system uses Google Gemini to transcribe audio, perform semantic analysis, identify covered and missed keywords, and generate structured feedback with a similarity score.

### Key Features

- **Audio Input** — Upload or record audio explanations directly in the browser
- **AI Transcription** — Automatic speech-to-text via Gemini 2.5 Flash
- **Semantic Evaluation** — Concept accuracy, keyword coverage, and gap analysis
- **Structured Reports** — Score, strengths, weaknesses, and personalized study advice
- **Session History** — Review and compare past evaluations within a session

---

## Tech Stack

| Layer       | Technology                           |
|-------------|--------------------------------------|
| Frontend    | Streamlit (Python)                   |
| AI Engine   | Google Gemini 2.5 Flash              |
| Validation  | Pydantic structured JSON schema      |
| Environment | python-dotenv                        |

---

## Getting Started

### Prerequisites

- Python 3.9 or later
- A Google Gemini API key ([get one here](https://aistudio.google.com/apikey))

### Installation

```bash
# 1. Clone the repository
git clone <repository-url>
cd vocalsense-ai/SOURCEFILES

# 2. Create and activate a virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env.local
# Edit .env.local and add your GEMINI_API_KEY

# 5. Run the application
streamlit run app.py
```

The application will open at **http://localhost:8501**.

---

## Project Structure

```
vocalsense-ai/
├── SOURCEFILES/
│   ├── app.py              # Main Streamlit application
│   ├── requirements.txt    # Python dependencies
│   ├── .env.example        # Environment variable template
│   ├── data/
│   │   ├── concepts.json   # Educational concepts database
│   │   └── metadata.json   # AI Studio deployment metadata
│   ├── backend/
│   │   ├── ai/
│   │   │   ├── gemini_client.py  # Gemini API integration
│   │   │   └── prompts.py        # AI prompts and system instructions
│   │   ├── config/
│   │   │   └── settings.py       # Application configuration
│   │   ├── models/
│   │   │   └── response.py       # Pydantic response schemas
│   │   ├── services/
│   │   │   └── __init__.py       # Services module
│   │   └── utils/
│   │       └── helpers.py        # Utility functions
│   └── assets/
│       └── styles.py       # Custom CSS styling
└── .gitignore
```

---

## Environment Variables

| Variable         | Required | Description                  |
|------------------|----------|------------------------------|
| `GEMINI_API_KEY` | Yes      | Google Gemini API key        |

---

## Usage

1. Fill in candidate details in the sidebar
2. Select a subject category and assessment topic
3. Upload an audio file **or** record audio directly
4. Click **Evaluate Explanation**
5. Review the detailed assessment report

---

## Deployment

The application is compatible with:

- **Streamlit Community Cloud** — Connect your GitHub repo and set `GEMINI_API_KEY` in Secrets
- **Google AI Studio** — Deploy via the AI Studio app builder
- **Docker** — Use `streamlit run app.py` as the container entrypoint
- **Render / Railway** — Set Python buildpack and `GEMINI_API_KEY` environment variable

---

## Screenshots

![Sidebar Settings](docs/screenshots/sidebar.png)
*Sidebar configuration for candidate details*

![Topic Selection](docs/screenshots/topic-selection.png)
*Select category and assessment topic*

![Upload & Record](docs/screenshots/audio-input.png)
*Upload audio file or record directly*

![Assessment Report](docs/screenshots/report.png)
*Generated assessment report with scores and feedback*

---

## License

This project was created for the SmartBridge internship program.
