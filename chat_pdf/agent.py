from pathlib import Path
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableParallel
from langchain_core.runnables import RunnableLambda 
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv
load_dotenv() 

FILES_FOLDER = Path(__file__).parent / 'files'
SPLITTER = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)
MODEL = ChatOpenAI(model="openai:gpt-5.4-mini")
PARSER = StrOutputParser()

# -------------------- // --------------------
# 1. Load pdfs


def document_loading():
    documents = []
    
    for file in FILES_FOLDER.glob('*.pdf'):
        loader = PyPDFLoader(str(file))
        documents.extend(loader.load())
     
    print(f"Loaded documents: {len(documents)}")    
    return documents

# -------------------- // --------------------
# 2. Chunkerization


def split_docs(documents : list):
    split_documents = SPLITTER.split_documents(documents=documents)
    
    print (f"Created chunks: {len(split_documents)}")
    for i, document in enumerate(split_documents):
        document.metadata['source'] = document.metadata['source'].split('/')
        document.metadata['id'] = i
    
    return split_documents


# -------------------- // --------------------
# 3. Vector Store

embedding_model = OpenAIEmbeddings()

def build_vector_store(documents : list):
   vector_store = FAISS.from_documents(
                        documents=documents,
                        embedding=embedding_model,)
   
   return vector_store

# -------------------- // --------------------
# 4. Create Chat Chain

def create_chat_chain(vector_store : FAISS, question: str):
    memory = InMemoryChatMessageHistory()
    retriever = vector_store.as_retriever()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer using the retrieved context"),
        ("human", "History: {history}\nQuestion: {question}")
    ])
    inputs = {"context": retriever, "question": RunnablePassthrough(), "history": lambda _: memory.messages}
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
    
if __name__ == '__main__':
    documents = document_loading()
    split_documents = split_docs(documents)
    vector_store = build_vector_store(documents)
    chain = create_chat_chain(vector_store=vector_store, question="What is the Lunar Base?")
    print(chain.model_dump_json)