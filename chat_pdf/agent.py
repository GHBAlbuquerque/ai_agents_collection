from pathlib import Path
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

FILES_FOLDER = Path(__file__).parent / 'files'
SPLITTER = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)
MODEL = ChatOpenAI(model="openai:gpt-5.4-mini")

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
collection = 'user_documents'

def build_vector_store(documents : list):
   vector_store = FAISS.from_documents(
                        documents=documents,
                        embedding=embedding_model, 
                        collection= collection)
   
   return vector_store

# -------------------- // --------------------
# 4. Create Chat Chain

def create_chat_chain(vector_store : FAISS):
    memory = InMemoryChatMessageHistory()
    chat_chain = ''
    # TODO
    pass