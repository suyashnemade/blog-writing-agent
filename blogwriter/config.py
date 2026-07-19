from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import ChatHuggingFace
from langchain_groq import ChatGroq
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
load_dotenv()
import os

### leave variable as it is
llmhf= HuggingFaceEndpoint(
    repo_id="openai/gpt-oss-120b",
    task="text-generation",
    huggingfacehub_api_token= os.getenv("HUGGINGFACE_API_KEY")
)


llmorchestrator =ChatGroq(model="llama-3.3-70b-versatile")

llmresearcher =ChatGroq(model="llama-3.3-70b-versatile")

# llmworker = ChatHuggingFace(llm=llmhf)
llmworker = ChatGoogleGenerativeAI(model="gemini-3.5-flash")

llmrouter = ChatGroq(model="llama-3.3-70b-versatile")


# llm = llmgeminipro25