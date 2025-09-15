# AI Excel Interviewer

An AI-powered API for conducting **structured Excel mock interviews**. This system simulates a realistic interview process by managing introductions, asking dynamically generated questions with increasing difficulty, evaluating candidate answers, and providing a comprehensive feedback report.

The project leverages **FastAPI**, **OpenAI GPT-4o**, and modular tools for chat, questions, evaluation, and feedback. It is fully containerized for easy deployment with Docker and can be hosted on platforms like **Render**.

---

## Features

* **Structured Interview Flow**: Introduction → Dynamic Questions → Evaluation → Feedback.
* **Dynamic Question Generation**: AI adapts questions based on previous answers.
* **Evaluation of Responses**: Highlights strengths and areas for improvement.
* **Feedback Report**: Generates a final performance summary at the end of the interview.
* **REST API Endpoints**: Easily integrate with web or mobile applications.
* **Dockerized Deployment**: Run locally or deploy on cloud platforms (Render, AWS, Azure, etc.).

---

## Project Structure

```
ai-excel-interviewer/
│
├── main.py                     # FastAPI entry point
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker setup
├── docker-compose.yml          # Local dev setup with Docker
├── .env                        # Environment variables (API keys)
├── config.py                   # Configuration for API keys and settings
├── README.md                   # Project documentation
│
├── core/
│   └── interviewer_agents.py   # Orchestrator for interview flow and feedback
│
├── models/
│   ├── request_models.py       # Request models for API
│   └── response_models.py      # Response models for API
│
├── tools/
│   ├── chat_tool.py            # Handles greetings and chat responses
│   ├── question_tool.py        # Generates dynamic interview questions
│   ├── evaluation_tool.py      # Evaluates candidate responses
│   └── feedback_tool.py        # Generates final feedback report
│
└── agents/                     # Local AI orchestration module
    ├── __init__.py
    ├── run.py
    └── models/
```

---
## Architecture Diagram

+-------------------+       +-------------------+
|   User/Client     |       |   FastAPI Server  |
| (e.g., Web/App)   | <---> | - /v1/query       |
+-------------------+       | - /feedback-report|
                            +-------------------+
                                      |
                                      v
                            +-------------------+
                            |   Orchestrator    |
                            | (process_query)   |
                            +-------------------+
                                      |
                                      | (Based on question count)
                                      v
    +---------------+    +---------------+    +---------------+    +---------------+
    |  Chat Agent  |    | Question Agent|    |Evaluation Agent|    | Feedback Agent|
    +---------------+    +---------------+    +---------------+    +---------------+
          |                       |                    |                    |
          v                       v                    v                    v
    +---------------+    +---------------+    +---------------+    +---------------+
    |  Chat Tool   |    | Question Tool |    |Evaluation Tool|    | Feedback Tool |
    | (GPT-4o)     |    | (LiteLLM/GPT) |    | (Simple Logic)|    | (Static Text) |
    +---------------+    +---------------+    +---------------+    +---------------+

## Getting Started

### Prerequisites

* Python 3.8+
* [pip](https://pip.pypa.io/en/stable/)
* Docker (for containerized deployment)
* Render account (optional, for cloud deployment)

---

### Installation (Local)

1. Clone the repository:

```bash
git clone <your-repo-url>
cd ai-excel-interviewer
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your API keys:

```
OPENAI_API_KEY="your-openai-api-key"
LOG_LEVEL=DEBUG
```

4. Start the FastAPI server:

```bash
uvicorn main:app --reload
```

API will be available at `http://localhost:8000`.

---

## API Endpoints

### `POST /v1/query`

**Description:** Main entry point for the AI interview. Handles structured interview flow.

**Request Body Example:**

```json
{
  "query": "Hello",
  "history": []
}
```

**Response Example:**

```json
{
  "response": "Hello, I am your Excel mock interviewer. Are you ready to begin?"
}
```

---

### `POST /feedback-report`

**Description:** Generate a final interview feedback report. Can optionally provide a custom prompt.

**Request Body Example:**

```json
{
  "query": "Please summarize my performance",
  "history": [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi! Are you ready for the Excel interview?"}
  ]
}
```

**Response Example:**

```json
{
  "response": "Interview Summary:\n- You communicated clearly in most answers.\n- Strengths: Teamwork, clarity of thought.\n- Areas for improvement: Provide more structured examples.\nOverall, you performed well in this mock interview."
}
```

---

## Docker Deployment

### 1. Dockerfile

```dockerfile
# Base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Docker Compose (for local development with auto-reload)

```yaml
version: '3.8'
services:
  ai-interviewer:
    build: .
    container_name: ai_excel_interviewer
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - .:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Build and Run Docker Container

```bash
docker-compose up --build
```

API will be available at `http://localhost:8000` with hot-reload.

---

## Deploying on Render

Render supports Docker deployments. Steps:

1. Push your repository to GitHub.
2. Create a new **Web Service** on Render.
3. Choose **Docker** as the environment.
4. Set the **Build Command** (optional; Dockerfile handles it).
5. Add environment variables (`OPENAI_API_KEY`) in the Render dashboard.
6. Deploy! Your service will be accessible via a public URL.

---

## Customization

* **Interview flow:** Modify `core/interviewer_agents.py` for question limits, evaluation, and feedback logic.
* **Chat behavior:** Adjust `tools/chat_tool.py` for greetings or interaction style.
* **Question generation:** Change prompts or difficulty logic in `tools/question_tool.py`.
* **Feedback report:** Update `tools/feedback_tool.py` for more detailed summaries.

---

## Environment Variables

| Key              | Description                           |
| ---------------- | ------------------------------------- |
| OPENAI\_API\_KEY | OpenAI API key for GPT models         |
| LOG\_LEVEL       | Logging level (`DEBUG`, `INFO`, etc.) |

---

## License

MIT License

---

## Authors

* **Aashima Sharma** – [aashima127s@gmail.com](mailto:aashima127s@gmail.com)
