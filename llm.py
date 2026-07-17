from dotenv import load_dotenv
from logger import logger
import os

from langchain_openai import ChatOpenAI

load_dotenv("/usr/local/nagios/agenticai/.env")

llm = ChatOpenAI(
    model=os.getenv("OPENROUTER_MODEL"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0
)
