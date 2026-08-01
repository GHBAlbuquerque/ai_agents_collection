import random
import logging
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.runnables import RunnableParallel, RunnableSerializable
from langchain_core.prompts import ChatPromptTemplate
from api.models import CharacterLoreCreationRequest, CharacterLoreCreationData
from core.ouput_parser import parse_lore_output
from langchain_core.documents import Document
from typing import Any
from core.properties import MODEL_NAME
from core.prompts import SYSTEM_PROMPT, build_human_prompt

from core.ingestion import create_retriever

from dotenv import load_dotenv
load_dotenv()

# -------------------- // --------------------
# 1. Auxiliary methods

def get_destiny_roll(age_input: str = "") -> str:
    if age_input:
        logging.info(f"Age input: {age_input}")
        try:
            if int(age_input) > 300:
                return "Special"
        except ValueError:
            pass 

    roll = random.randint(1, 50)
    logging.info(f"Destiny Roll: {roll}")
    return "Special" if roll > 45 else "Standard"


def format_docs_output(documents: list[Document]):
    return "\n\n".join(document.page_content for document in documents)

# -------------------- // --------------------
# 2. Config Chat Chain

MODEL = ChatOpenAI(model=MODEL_NAME, temperature=0.5)
PARSER = StrOutputParser()

def config_lore_chain(retriever: VectorStoreRetriever) -> RunnableSerializable[Any, str]:

    prompt = ChatPromptTemplate.from_messages(
        [("system", SYSTEM_PROMPT),
         ("human", "{character_request}")]
    )
    
    inputs = {"character_request": lambda character_params: build_human_prompt(character_params),
              "context": lambda _: format_docs_output(retriever.invoke("Ragnarok Online general world lore history and factions")),
              "destiny_roll": lambda character_params: get_destiny_roll(character_params.character_age)}
    
    chain = (RunnableParallel(inputs) | 
            prompt | 
            MODEL | 
            PARSER)
    
    logging.info("Successfully created chain.")
    
    return chain


# -------------------- // --------------------
# 3. High-level Execution Helper

_lore_chain = None

def get_lore_chain():
    global _lore_chain
    if _lore_chain is None:
        retriever = create_retriever()
        _lore_chain = config_lore_chain(retriever)
    return _lore_chain


def get_character_lore(request: CharacterLoreCreationRequest) -> CharacterLoreCreationData:
    """
    Executes the lore generation chain with the given request data 
    and returns a structured CharacterLoreCreationData.
    """
    chain = get_lore_chain()
    raw_output = chain.invoke(request)
    return parse_lore_output(raw_output)