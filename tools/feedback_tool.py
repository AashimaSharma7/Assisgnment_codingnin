import json
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
from pydantic import BaseModel  
from typing import List, Dict
class FeedbackResult(BaseModel):
    Strengths: str
    Weaknesses: str
    AreasForImprovement: str
    OverallScore: int
    Recommendation: str

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class FeedbackTool:
    def __init__(self):
        pass

    def generate_feedback(self, query, history):
        """
        Collects per-answer evaluations from history and generates a final structured summary.
        query: the last request (usually "generate final report")
        history: full conversation history with evaluations included
        """

        # Extract evaluations from history
        evaluations = [
            m["content"].replace("Evaluation: ", "").strip()
            for m in history
            if m["role"] == "assistant" and m["content"].startswith("Evaluation:")
        ]

        if not evaluations:
            return "No evaluations found in history. Cannot generate feedback."

        # Build summary prompt for LLM
        eval_text = "\n\n".join([f"Answer {i+1} Evaluation:\n{e}" for i, e in enumerate(evaluations)])

        feedback_prompt = f"""
You are an interview feedback generator.

The following are evaluations of the candidate's answers:
{eval_text}

Task:
1. Summarize overall strengths and weaknesses.
2. Highlight areas for improvement.
3. Provide an overall score (1–5).
4. Suggest whether the candidate should move to the next round.

Return in this JSON format:

  "Strengths": "...",
  "Weaknesses": "...",
  "AreasForImprovement": "...",
  "OverallScore": 0,
  "Recommendation": "..."

"""

        # Call LLM
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # can switch to gpt-4o or gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "You are an expert HR evaluator."},
                {"role": "user", "content": feedback_prompt},
            ],
            temperature=0.3,
            max_tokens=1024,
            response_format=FeedbackResult
        )

        raw_output = response.choices[0].message.content.strip()

        # Try parsing JSON
        try:
            parsed_output = json.loads(raw_output)
        except json.JSONDecodeError:
            parsed_output = {"error": "Failed to parse JSON", "raw_output": raw_output}

        return parsed_output
