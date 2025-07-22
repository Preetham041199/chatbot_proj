from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os
from pydantic import BaseModel
from tools import invoke_tool, tool_map
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str


genai.configure(api_key=os.getenv("Api_key"))
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    user_input = request.message.strip()
    classification_prompt = f"""
You are a tool classification engine.
Given a user's message, determine if it matches one of the following tools: weather, product_price, stock_price, calculator, code_helper, google_search, tech_news, historical_fact.
If it does, reply with ONLY the tool name.
If none match, reply with "none".

User: {user_input}
Tool:
"""
    classification = model.generate_content(classification_prompt)
    tool_name = classification.text.strip().lower()
 
    if tool_name in tool_map:
        result = invoke_tool(tool_name, user_input)
        return {
            "response": result,
            "source": f"{tool_name} tool"
        }
    response = model.generate_content(user_input)
    return {
        "response": response.text,
        "source": "gemini"
    }



@app.get("/")
def read_root():
    return {"message": "Backend is working ✅"}
