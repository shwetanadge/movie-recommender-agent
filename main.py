from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

#load env file
load_dotenv()

#Initialize LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("YOUR_GROQ_API_KEY")
)