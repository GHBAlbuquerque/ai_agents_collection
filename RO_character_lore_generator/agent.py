import random
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.runnables import RunnableSerializable
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.documents import Document
from narwhals import Unknown
from configs import MODEL_NAME

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

def config_chat_chain():
    # TODO
    pass

# -------------------- // --------------------
# 3. Create Chat Chain and Memory

def create_chain_and_memory(retriever: VectorStoreRetriever): #-> RunnableSerializable[Unknown, str], InMemoryChatMessageHistory
    #TODO
    pass