import os
import json
from openai import OpenAI
from pydantic import BaseModel
from typing import List, Dict
from dotenv import load_dotenv
load_dotenv()

class EvaluationResult(BaseModel):
    Relevance: Dict[str, str]
    Clarity: Dict[str, str]
    Depth: Dict[str, str]
    Accuracy: Dict[str, str]
    Communication: Dict[str, str]
    OverallFeedback: str

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class EvaluationTool:
    def __init__(self):
        self.criteria = ["Relevance", "Clarity", "Depth", "Accuracy", "Communication"]

    def evaluate(self, query, history):
        """
        Evaluates candidate answers using LLM instead of simple keyword checks.
        query: latest candidate response
        history: full conversation history (list of {role, content})
        """

        # Get the last assistant message (the question asked)
        last_question = next(
            (m["content"] for m in reversed(history) if m["role"] == "assistant"),
            "Unknown Question"
        )

        # Build evaluation prompt
        evaluation_prompt = f"""
You are an interview evaluator. Your task is to evaluate the candidate's answer
based on the following criteria:

1. Relevance – Did the answer address the question?
2. Clarity – Was the answer clear and well-structured?
3. Depth – Did they provide reasoning, examples, or just surface-level info?
4. Accuracy – Are the facts technically correct (especially for Excel/technical Qs)?
5. Communication – How professional, concise, and understandable was the answer?

Question: {last_question}
Candidate's Answer: {query}

Instructions:
- Give a score from 1 (poor) to 5 (excellent) for each criterion.
- Provide a one-line explanation for each score.
- Provide an overall impression in 2-3 sentences.
- Return the result strictly in JSON format like this:

  "Relevance": <"score": 0, "explanation": "...">,
  "Clarity": <"score": 0, "explanation": "...">,
  "Depth": <"score": 0, "explanation": "...">,
  "Accuracy": <"score": 0, "explanation": "...">,
  "Communication": <"score": 0, "explanation": "...">,
  "OverallFeedback": "..."

"""

        # Call LLM
        response = client.chat.completions.create(
            model="gpt-4o-mini",   
            messages=[{"role": "system", "content": "You are a strict but fair interview evaluator."},
                      {"role": "user", "content": evaluation_prompt}],
            temperature=0.3,
            max_tokens=1024,
            response_format=EvaluationResult
        )

        raw_output = response.choices[0].message.content.strip()

        # Try parsing into JSON
        try:
            parsed_output = json.loads(raw_output)
        except json.JSONDecodeError:
            parsed_output = {"error": "Failed to parse JSON", "raw_output": raw_output}

        return parsed_output
