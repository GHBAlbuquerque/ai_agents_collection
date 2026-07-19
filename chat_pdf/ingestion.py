from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.documents import Document
from configs import FILES_FOLDER, RETRIEVAL_ARGS, RETRIEVAL_SEARCH_TYPE

from dotenv import load_dotenv
load_dotenv() 

"""
Does document ingestion, chunkerization, creates Vector Database and retriever.
"""

SPLITTER = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)

# -------------------- // --------------------
# 1. Load pdfs


def document_loading() -> list:
    documents = []
    
    for file in FILES_FOLDER.glob('*.pdf'):
        loader = PyPDFLoader(str(file))
        documents.extend(loader.load())
     
    print(f"Loaded documents: {len(documents)}")    
    return documents

# -------------------- // --------------------
# 2. Chunkerization


def split_docs(documents : list) -> list[Document]:
    split_documents = SPLITTER.split_documents(documents=documents)
    
    print (f"Created chunks: {len(split_documents)}")
    for i, document in enumerate(split_documents):
        document.metadata['source'] = document.metadata['source'].split('/')
        document.metadata['id'] = i
    
    return split_documents


# -------------------- // --------------------
# 3. Vector Store

embedding_model = OpenAIEmbeddings()

def build_vector_store(documents : list) -> FAISS:
   vector_store = FAISS.from_documents(
                        documents=documents,
                        embedding=embedding_model,)
   
   return vector_store


# -------------------- // --------------------
# 4. Create Retriever
    
def create_retriever() -> VectorStoreRetriever:
    documents = document_loading()
    chunks = split_docs(documents)
    vector_store = build_vector_store(chunks)
    
    return vector_store.as_retriever(
        search_kwargs=RETRIEVAL_ARGS, 
        search_type=RETRIEVAL_SEARCH_TYPE
        )
    