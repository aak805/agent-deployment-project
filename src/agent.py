"""Modlule containing the agent structure and tools."""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState, StateGraph, END
import os
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT
from langgraph.types import interrupt
from langgraph.types import Command
import logging

logger = logging.getLogger()

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0,
    google_api_key=GEMINI_API_KEY
)

builder = StateGraph(MessagesState)

def ask_a_basic_czech_question(state: MessagesState):
    """Generates a basic Czech question."""
    messages = state.get("messages", [])
    if not messages:
        messages = [HumanMessage(content="Ask me a Czech question")]
    
    response = llm.invoke(
        [SystemMessage(content=SYSTEM_PROMPT)] + messages
    )
    logger.info("Generating a Czech question...")
    # response = AIMessage(content='My first question for you is:\n\n**Co máte rádi k jídlu?** (What do you like to eat?)')
    return {"messages": [response]}

def get_user_answer(state: MessagesState):
    """A node that uses interrupt to get human input."""
    user_input = interrupt(state["messages"][-1].content)
    logger.info("Getting user response.")
    return Command(
        resume=user_input,
        update={
            "messages": [HumanMessage(content=user_input)]
        }
    )

def evaluate_the_answer(state: MessagesState):
    """Evaluates the student's answer."""
    evaluation_prompt = (
        "Evaluate the student's answer to the previous question. "
        "Provide feedback and a corrected version (only if necessary), "
        "but do it in English as the student is still a beginner in Czech."
    )
    response = llm.invoke(
        [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=evaluation_prompt)] + state["messages"]
    )
    logger.info("Evaluating user response.")
    return {"messages": [response]}

builder = StateGraph(MessagesState)

builder.add_node("ask_a_basic_czech_question", ask_a_basic_czech_question)
builder.add_node("get_user_answer", get_user_answer)
builder.add_node("evaluate_the_answer", evaluate_the_answer)

builder.set_entry_point("ask_a_basic_czech_question")

builder.add_edge("ask_a_basic_czech_question", "get_user_answer")
builder.add_edge("get_user_answer", "evaluate_the_answer")
builder.add_edge("evaluate_the_answer", END)

memory = MemorySaver()
agent = builder.compile(checkpointer=memory)
