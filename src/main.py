from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import uuid
import uvicorn
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import os
from fastapi.middleware.cors import CORSMiddleware
from prompts import SYSTEM_PROMPT
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0,
    google_api_key=GEMINI_API_KEY
)

chat_histories: Dict[str, List[Dict[str, str]]] = {}

app = FastAPI(title="Simple LLM Chat API")

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: Optional[str] = None
    thread_id: Optional[str] = None

class ChatResponse(BaseModel):
    messages: List[Dict[str, str]]
    thread_id: str

@app.post("/chat", response_model=ChatResponse)
async def chat_with_llm(chat_request: ChatRequest):
    """
    Endpoint to interact with the LLM in a simple request-response cycle.
    Each call sends the full chat history to the LLM.
    """
    thread_id = chat_request.thread_id or str(uuid.uuid4())
    
    if thread_id not in chat_histories:
        chat_histories[thread_id] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "assistant", "content": "Dobrý den! My first question for you is: **Co máte rádi k jídlu?** (What do you like to eat?)"}
        ]

    if chat_request.message:
        chat_histories[thread_id].append({"role": "user", "content": chat_request.message})

    llm_messages = []
    for msg in chat_histories[thread_id]:
        if msg["role"] == "user":
            llm_messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            llm_messages.append(AIMessage(content=msg["content"]))
        elif msg["role"] == "system":
            llm_messages.append(SystemMessage(content=msg["content"]))

    try:
        ai_response = llm.invoke(llm_messages)
        
        chat_histories[thread_id].append({"role": "assistant", "content": ai_response.content})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return ChatResponse(
        messages=chat_histories[thread_id],
        thread_id=thread_id
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)