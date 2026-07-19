from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.vectorstores import VectorStoreRetriever
from prompts import SYSTEM_PROMPT, HUMAN_PROMPT

from dotenv import load_dotenv
load_dotenv() 

"""
Creates and returns both chain and its memory using the Vector DB retriever for context.
"""

MODEL = ChatOpenAI(model="gpt-5.4-mini")
PARSER = StrOutputParser()

# -------------------- // --------------------
# 1. Config Chat Chain and Memory

def format_docs_output(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def config_chat_chain(retriever : VectorStoreRetriever, memory: InMemoryChatMessageHistory):
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", HUMAN_PROMPT)
    ])
    inputs = {"context": retriever | format_docs_output, "question": RunnablePassthrough(), "history": lambda _: memory.messages}
    # context should come from the retriever
    # RunnablePassthrough -> pass what was used on `invoke` through unchanged
    # question should be whatever text is passed into the chain
    # history is the message history in the memory
    
    # a chain is the sequence of: dict of inputs + prompt + model + parser
    chat_chain = (
        RunnableParallel(inputs) |
        prompt |
        MODEL |
        PARSER
        )
    
    return chat_chain

# -------------------- // --------------------
# 2. Create Chat Chain
 
def create_chain_and_memory(retriever : VectorStoreRetriever):
    memory = InMemoryChatMessageHistory()
    chain = config_chat_chain(retriever=retriever, memory=memory)
    
    return chain, memory

    