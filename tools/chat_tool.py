

from loguru import logger
from openai import AsyncOpenAI
from config import Config

class ChatTool:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=Config.OPENAI_API_KEY)
        logger.info("Initialized ChatTool with OpenAI client")

    async def process(self, query: str, history: list = None) -> str:
        try:
            history = history or []

            
            is_first_interaction = all("Question" not in m.get("content", "") for m in history)

            if is_first_interaction:
                # Greeting phase
                system_prompt = """You are an AI Excel mock interviewer.
Greet the candidate and explain the interview process in 2-3 sentences:
- This is a structured Excel interview
- You will ask multiple questions increasing in difficulty
- You will probe partially answered questions
- At the end, you will provide a feedback report
Then ask the candidate: 'Are you ready to begin?'"""
                
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ]
            else:
                # Normal chat phase (after greeting)
                messages = [{"role": "system", "content": "You are an AI Excel mock interviewer."}]
                messages.extend(history)
                messages.append({"role": "user", "content": query})

            logger.debug(f"Processing chat query: {query}")
            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.7,
                max_tokens=300
            )
            result = response.choices[0].message.content
            logger.success("Chat query processed successfully")
            return result

        except Exception as e:
            logger.exception(f"Error processing chat query: {e}")
            raise
