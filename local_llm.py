
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory
from langchain import OpenAI, LLMChain, PromptTemplate



def create_red_pajama_llmchain(human_template="{question}", system_template="", verbose = False, memory=True):
    template = system_template + f"""
{"{chat_history}" if memory else ""}
<human>: {human_template}
<bot>:"""


    return LLMChain(
        llm=OpenAI(
            model="RedPajama-INCITE-Chat-7B-v0.1",
            openai_api_base="http://localhost:8000/v1",
            openai_api_key="EMPTY"
        ),
        memory=ConversationBufferWindowMemory(
            human_prefix="<human>",
            ai_prefix="<bot>",
            memory_key="chat_history",
            k=2
        ) if memory else None,
        prompt=PromptTemplate(
            input_variables=["chat_history", "question"] if memory else ["question"], 
            template=template
        ),
        verbose=verbose
    )


def create_fastchat_llmchain(human_template="{question}", system_template="", verbose = False, memory=True):
    template = system_template + f"""
{"{chat_history}" if memory else ""}
Human: {human_template}
Chatbot:"""

    return LLMChain(
        llm=OpenAI(
            model="fastchat-t5-3b-v1.0",
            openai_api_base="http://localhost:8000/v1",
            openai_api_key="EMPTY"
        ),
        memory=ConversationBufferMemory(
            human_prefix="Human",
            ai_prefix="Chatbot",
            memory_key="chat_history"
        ) if memory else None,
        prompt=PromptTemplate(
            input_variables=["chat_history", "question"] if memory else ["question"], 
            template=template
        ),
        verbose=verbose
    )



