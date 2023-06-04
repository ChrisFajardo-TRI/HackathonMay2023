from dataclasses import dataclass
import pathlib
import textwrap

from langchain.memory import ConversationBufferWindowMemory
from langchain import OpenAI, LLMChain, PromptTemplate


@dataclass
class LLMSpec:
    model_name: str
    human_prefix: str
    ai_prefix: str


red_pajama_llm_spec = LLMSpec(
    model_name="togethercomputer/RedPajama-INCITE-Chat-7B-v0.1",
    human_prefix="<human>",
    ai_prefix="<bot>"
)

fastchat_llm_spec = LLMSpec(
    model_name="lmsys/fastchat-t5-3b-v1.0",
    human_prefix="Human",
    ai_prefix="Chatbot"
)




def create_llmchain(
    llm_spec: LLMSpec, 
    human_template="{question}", 
    system_template="", 
    verbose=False, 
    memory=True
):
    template = system_template
    conversation_memory = None
    input_variables = ["question"]

    if memory:
        template += textwrap.dedent("""
        Current conversation:
        {chat_history}
        """)
        conversation_memory = ConversationBufferWindowMemory(
            human_prefix=llm_spec.human_prefix,
            ai_prefix=llm_spec.ai_prefix,
            memory_key="chat_history",
            k=2
        )
        input_variables.insert(0, "chat_history")

    template += textwrap.dedent(f"""
    <human>: {human_template}
    <bot>:""")

    return LLMChain(
        llm=OpenAI(
            model=pathlib.Path(llm_spec.model_name).name,
            openai_api_base="http://localhost:8000/v1",
            openai_api_key="EMPTY"
        ),
        memory=conversation_memory,
        prompt=PromptTemplate(input_variables=input_variables, template=template),
        verbose=verbose
    )


def create_red_pajama_llmchain(
    human_template="{question}", 
    system_template="", 
    verbose=False, 
    memory=True
):
    return create_llmchain(
        llm_spec=red_pajama_llm_spec,
        human_template=human_template,
        system_template=system_template,
        verbose=verbose,
        memory=memory
    )