
import litellm
from loguru import logger

class QuestionTool:
    @staticmethod
    def ask_question(query: str, history: list) -> str:
        """
        Dynamically generate an Excel interview question.
        - Adapts difficulty based on past answers.
        - Avoids repeating previous questions.
        - Probes if user gives incomplete answers.
        """
        system_prompt = ("""
            You are an Excel mock interviewer conducting a structured interview. 
        Based on the previous conversation history, ask a new question or follow up if the last answer was incomplete.
                         
        Keep the tone friendly and conversational, like a real interviewer.
        Increase difficulty if the candidate is answering well.
        Keep track to not repeat questions already asked.
        If the interview has reached 5 questions, say 'Thank you. The interview is complete.'
        Previous conversation history: {history}
        Current user input: {query}"""
        )

        
        formatted_history = "\n".join(
            [f"{msg['role'].capitalize()}: {msg['content']}" for msg in (history or [])]
        )

        user_content = (
            f"Conversation so far:\n{formatted_history}\n\n"
            f"Candidate's latest input: {query}"
        )

        try:
            response = litellm.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                ],
                max_tokens=256,
                temperature=0.7,
            )
            question = response.choices[0].message["content"]
            logger.info(f"Generated Question: {question}")
            return question
        except Exception as e:
            logger.error(f"Error generating question: {e}")
            return "It seems there was an error in generating the question. Let's try again."

