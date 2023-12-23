import os

from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage
# import openai
import gradio as gr

os.environ["OPENAI_API_BASE"] = "http://192.168.31.12:8000/v1"  # Replace with your base url
os.environ["OPENAI_API_KEY"] = "sk-123456"  # Replace with your api key

llm = ChatOpenAI(temperature=1.0, model='gpt-3.5-turbo')


def predict(message, history):
    history_langchain_format = []
    for human, ai in history:
        history_langchain_format.append(HumanMessage(content=human))
        history_langchain_format.append(AIMessage(content=ai))
    history_langchain_format.append(HumanMessage(content=message))
    gpt_response = llm(history_langchain_format)
    return gpt_response.content


gr.ChatInterface(predict).launch()
