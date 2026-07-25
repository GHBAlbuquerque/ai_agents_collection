import random
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableSerializable
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.documents import Document
from narwhals import Unknown
from configs import MODEL_NAME
from prompt import SYSTEM_PROMPT

from ingestion import create_retriever

from dotenv import load_dotenv
load_dotenv()

# -------------------- // --------------------
# 1. Auxiliary methods

def get_destiny_roll():
    roll = random.randint(1,50)
    return "Special" if roll == 50 else "Standard"


def format_docs_output(documents: list[Document]):
    return "\n\n".join(document.page_content for document in documents)

# -------------------- // --------------------
# 2. Config Chat Chain

MODEL = ChatOpenAI(model=MODEL_NAME)
PARSER = StrOutputParser()

def config_chat_chain(retriever: VectorStoreRetriever, memory: InMemoryChatMessageHistory) -> RunnableSerializable[Unknown, str]:
    prompt = ChatPromptTemplate.from_messages(
        [("system", SYSTEM_PROMPT),
         MessagesPlaceholder("history"),
         ("human", "{question}")]
    )
    
    inputs = {"context": retriever | format_docs_output,
              "question": RunnablePassthrough(),
              "history": lambda _: memory.messages}
    
    chain = (RunnableParallel(inputs) | 
            prompt | 
            MODEL | 
            PARSER)
    
    return chain

# -------------------- // --------------------
# 3. Create Chat Chain and Memory

def create_chain_and_memory(retriever: VectorStoreRetriever) -> tuple[RunnableSerializable[Unknown, str], InMemoryChatMessageHistory]:
    memory = InMemoryChatMessageHistory()
    chain = config_chat_chain(retriever, memory)
    
    return chain, memory

if __name__ == "__main__":
    retriever = create_retriever()
    chain, memory = create_chain_and_memory(retriever)
    print(chain.config_schema)