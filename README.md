# AI Excel Interviewer

An API for conducting structured Excel mock interviews using AI. The system manages introductions, asks dynamic questions, evaluates answers, and provides constructive feedback.

## Features

* Structured interview flow with increasing question difficulty
* Dynamic question generation and probing for incomplete answers
* Evaluation of candidate responses
* Final feedback report summarizing strengths and areas for improvement
* REST API endpoints for integration
* Ready for deployment with Docker and Render

## Project Structure

```
.env
.gitignore
config.py
main.py
requirements.txt
Dockerfile
core/
    interviewer_agents.py
models/
    request_models.py
    response_models.py
tools/
    chat_tool.py
    evaluation_tool.py
    feedback_tool.py
    question_tool.py
```

## System Architecture

```
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
```

## Getting Started

### Prerequisites

* Python 3.9+
* [pip](https://pip.pypa.io/en/stable/)
* OpenAI API key

### Installation (Local)

1. Clone the repository:

   ```sh
   git clone <your-repo-url>
   cd ai-excel-interviewer
   ```

2. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Set up your `.env` file with API keys:

   ```
   OPENAI_API_KEY="your-openai-key"
   LOG_LEVEL=DEBUG
   ```

4. Start the FastAPI server:

   ```sh
   uvicorn main:app --reload
   ```

   The API will be available at `http://localhost:8000`.

---

## Docker Setup

1. Build the Docker image:

   ```sh
   docker build -t ai-excel-interviewer .
   ```

2. Run the container:

   ```sh
   docker run -d -p 8000:8000 --env-file .env ai-excel-interviewer
   ```

   The API will be available at `http://localhost:8000`.

---

## Deployment on Render

1. Push your code to GitHub/GitLab.

2. In [Render](https://render.com), create a **New Web Service**.

3. Connect your repo and configure:

   * **Environment**: Docker
   * **Build Command**: `docker build -t ai-excel-interviewer .`
   * **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 8000`
   * **Port**: `8000`
   * Add environment variables (like `OPENAI_API_KEY`).

4. Deploy 🎉

---

## API Endpoints

### `POST /v1/query`

* **Description:** Main entry point for interacting with the AI Interviewer.
* **Request Body:**

```json
{
  "query": "Hello, yes i am ready",
  "history": [
    {
            "role": "assistant",
            "content": "hi, im your excel interviewer. are you ready for the interview?"
    }
]
}
```

* **Response:**

```json
{
  "response": "good! Let's start the interviewe. Here's question 1: In excel what..."
}
```

---

### `POST /feedback-report`

* **Description:** Generate a final performance summary report.
* **Request Body:**

```json
{
  "query": "Give me feedback report",
  "history": [
    {"role": "assistant", "content": "Hello, I am your Excel interviewer..."},
    {"role": "user", "content": "Hello, yeah"},
  ]
}
```

* **Response:**

```json
{
  "response": "Interview Summary: ..."
}
```

---

## Testing with Postman

Since the backend is deployed independently, you can test endpoints using **Postman**:

1. Open Postman and create a new **POST** request.

2. Use your API URL (local or deployed):

   * Local: `http://127.0.0.1:8000/v1/query`
   * Render: `https://<your-service>.onrender.com/v1/query`

3. Go to the **Body** tab → Select **raw** → Choose **JSON**.

4. Enter a sample request body:

   ```json
   {
      "query": "Hello, yes i am ready",
      "history": [
            {
                "role": "assistant",
                "content": "hi, im your excel interviewer. are you ready for the interview?"
            }
        ]
    }
   ```

5. Hit **Send** and check the response.

6. For feedback testing:

   * Endpoint: `POST /feedback-report`
   * Request body:

   ```json
   {
     "query": "Give me feedback report",
     "history": [
       {"role": "assistant", "content": "Hello, I am your Excel interviewer..."},
       {"role": "user", "content": "yes"},
     ]
   }
   ```

   * Response:

   ```json
   {
     "response": "Interview Summary: You communicated clearly..."
   }
   ```

---

## Customization

* Interview logic and flow are orchestrated in [`core/interviewer_agents.py`](core/interviewer_agents.py).
* Modify or extend tools in [`tools/`](tools/) for custom interview logic.

---

## License

MIT

---

## Author

* [Aashima Sharma](mailto:aashima127s@gmail.com)
