
from agents import Agent, Runner, function_tool
from loguru import logger
from tools.chat_tool import ChatTool
from tools.question_tool import QuestionTool
from tools.evaluation_tool import EvaluationTool
from tools.feedback_tool import FeedbackTool
from models.request_models import QueryPayload

# Instantiate tools
chat_tool_instance = ChatTool()
question_tool_instance = QuestionTool()
evaluation_tool_instance = EvaluationTool()
feedback_tool_instance = FeedbackTool()

# Tracking question count globally
QUESTION_LIMIT = 5


@function_tool
def chat_tool(input_data: QueryPayload) -> str:
    query = input_data.get("query")
    history = input_data.get("history", [])
    logger.info(" ChatTool called")
    return chat_tool_instance.process(query, history)


@function_tool
def question_tool(input_data: QueryPayload) -> str:
    query = input_data.get("query")
    history = input_data.get("history", [])
    logger.info(" QuestionTool called")
    return question_tool_instance.ask_question(query, history)


@function_tool
def evaluation_tool(input_data: QueryPayload) -> str:
    query = input_data.get("query")
    history = input_data.get("history", [])
    logger.info(" EvaluationTool called")
    return evaluation_tool_instance.evaluate(query, history)


@function_tool
def feedback_tool(input_data: QueryPayload) -> str:
    query = input_data.get("query")
    history = input_data.get("history", [])
    logger.info(" FeedbackTool called")
    return feedback_tool_instance.generate_feedback(query, history)


# Agents
chat_agent = Agent(
    name="ChatAgent",
    instructions="Manage introductions, clarifications, and small talk in the interview.",
    tools=[chat_tool]
)

question_agent = Agent(
    name="QuestionAgent",
    instructions="Ask structured interview questions dynamically without repeating and with difficulty progression.",
    tools=[question_tool]
)

evaluation_agent = Agent(
    name="EvaluationAgent",
    instructions="Evaluate responses critically, note strengths and weaknesses.",
    tools=[evaluation_tool]
)

feedback_agent = Agent(
    name="FeedbackAgent",
    instructions="Generate a structured feedback report at the end of the interview.",
    tools=[feedback_tool]
)


# Orchestrator 
async def process_query(query: str, history: list = None) -> str:
    """
    Orchestrates the flow:
    1. Greeting/Intro handled by ChatAgent
    2. Ask up to 5 dynamic Excel questions via QuestionAgent
    3. After 5 Qs, run evaluation + feedback
    """
    messages = (history or []) + [{"role": "user", "content": query}]
    logger.info(f"Processing query with {len(messages)} messages")

    
    asked_questions = [m for m in messages if m["role"] == "assistant" and "Question" in m["content"]]
    question_count = len(asked_questions)
    logger.info(f" Questions asked so far: {question_count}")

    
    if question_count == 0:
        
        logger.info(" Handing off to ChatAgent (greeting phase)")
        result = await Runner.run(chat_agent, messages)
        return result.final_output

    elif question_count < QUESTION_LIMIT:
        
        logger.info(" Handing off to QuestionAgent (QnA phase)")
        result = await Runner.run(question_agent, messages)
        return result.final_output

    else:
        # Interview complete - Evaluate + Feedback
        logger.info(" Handing off to EvaluationAgent + FeedbackAgent (final phase)")
        eval_result = await Runner.run(evaluation_agent, messages)
        feedback_result = await Runner.run(feedback_agent, messages + [
            {"role": "assistant", "content": eval_result.final_output}
        ])
        return feedback_result.final_output



async def generate_feedback_report(history: list = None, custom_prompt: str = None) -> str:
    """
    Explicit feedback endpoint that works like process_query.
    """
    
    messages = (history or []) + [{"role": "user", "content": custom_prompt or "Generate a final interview performance summary."}]
    logger.info(f"Generating feedback report with {len(messages)} messages")

    
    result = await Runner.run(feedback_agent, messages)
    return result.final_output


