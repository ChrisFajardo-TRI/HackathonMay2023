import os
from langchain import PromptTemplate, OpenAI, LLMChain
import chainlit as cl

fastchat_model = OpenAI(
    model="fastchat-t5-3b-v1.0",
    openai_api_base="http://localhost:8000/v1",
    openai_api_key="EMPTY"
)

template = """Question: {question}

Answer: Let's think step by step."""

@cl.langchain_factory
def factory():
    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=fastchat_model, verbose=True)
    return llm_chain
