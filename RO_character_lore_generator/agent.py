import random
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableSerializable
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.documents import Document
from narwhals import Unknown
from properties import MODEL_NAME
from prompt import SYSTEM_PROMPT, build_human_prompt

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

def config_lore_chain(retriever: VectorStoreRetriever) -> RunnableSerializable[Unknown, str]:
    prompt = ChatPromptTemplate.from_messages(
        [("system", SYSTEM_PROMPT),
         ("human", "{character_request}")]
    )
    
    inputs = {"character_request": lambda character_params: build_human_prompt(character_params),
              "context": lambda _: format_docs_output(retriever.invoke("Ragnarok Online general world lore history and factions")),
              "destiny_roll": lambda _: get_destiny_roll()}
    
    chain = (RunnableParallel(inputs) | 
            prompt | 
            MODEL | 
            PARSER)
    
    return chain