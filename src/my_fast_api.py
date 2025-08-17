from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

from langgraph.types import Command
from agent import agent

app = FastAPI(title="LangGraph Agent API")

import logging

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()]) 

class ChatRequest(BaseModel):
    message: Optional[str] = None 
    thread_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    thread_id: str
    status: str 

@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(chat_request: ChatRequest):
    """
    Endpoint to interact with the LangGraph agent.
    Handles both first run and human-in-the-loop resumes.
    """
    thread_id = chat_request.thread_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    if chat_request.thread_id and chat_request.message:
        inputs = Command(resume=chat_request.message)
    else:
        inputs = {}
    try:
        for step in agent.stream(inputs, config=config):
            logging.info(f"Step:\n {step}")
            if "__interrupt__" in step:
                interrupt_data = step["__interrupt__"][0].value
                logging.info(interrupt_data)
                return ChatResponse(
                    response=interrupt_data if isinstance(interrupt_data, str) else str(interrupt_data),
                    thread_id=thread_id,
                    status="awaiting_input"
                )

        final_state = agent.get_state(config)
        final_message = final_state.values["messages"][-1].content

        return ChatResponse(
            response=final_message,
            thread_id=thread_id,
            status="complete"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
