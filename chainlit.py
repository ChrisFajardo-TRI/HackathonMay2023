
import chainlit as cl

from llm_lib import create_red_pajama_llmchain

@cl.langchain_factory
def factory():
    return create_red_pajama_llmchain(verbose=True, memory=False)
