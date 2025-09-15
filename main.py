

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from models.response_models import TextResponse
from models.request_models import QueryRequest

from core.interviewer_agents import process_query, generate_feedback_report  

app = FastAPI(title="AI Interviewer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/v1/query", response_model=TextResponse)
async def query_interviewer(query: QueryRequest):
    """
    Main entry point for interacting with the AI Interviewer.
    - Manages structured interview flow.
    - Evaluates answers.
    - Provides constructive feedback at the end.
    """
    try:
        logger.info(f"Received interview query: {query}")
        response_text = await process_query(query.query, query.history)
        return TextResponse(response=response_text)
    except Exception as e:
        logger.exception(f"Exception in /query route: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the interview query.")


@app.post("/feedback-report", response_model=TextResponse)
async def feedback_report(query: QueryRequest):
    """
    Generate a final performance summary report based on the interview history.
    Optionally accepts a custom prompt to style the feedback.
    """
    try:
        logger.info(f"Generating feedback report for query: {query}")
        response_text = await generate_feedback_report(query.history, query.query)
        return TextResponse(response=response_text)
    except Exception as e:
        logger.exception(f"Exception in /feedback-report route: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while generating the feedback report.")
