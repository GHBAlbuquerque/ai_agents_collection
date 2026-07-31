
import os
import logging
from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from core.properties import FILES_FOLDER, EMBEDDING_MODEL, VECTOR_DB_FOLDER, COLLECTION_NAME
from dotenv import load_dotenv

load_dotenv()

# -------------------- // --------------------
# 1. Load pdfs

def create_documents():
    documents = []
    
    for file in FILES_FOLDER.glob('*.pdf'):
        logging.info(f"Reading file: {file.name}")
        reader = PdfReader(file)
        
        file_pages = [Document(page_content=page.extract_text(), 
                             metadata={"source": file.name, "page": i}) 
                    for i, page in enumerate(reader.pages)]
        
        documents.extend(file_pages)
        
    logging.info(f'Loaded documents: {len(documents)}')
    return documents

# -------------------- // --------------------
# 2. Chunkerization

def split_documents(documents : list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100, length_function=len)
    
    chunks = splitter.split_documents(documents=documents)
    logging.info(f"Created chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks):
        chunk.metadata['source'] = chunk.metadata['source'].split('/')
        chunk.metadata['id'] = i
        
    return chunks

# -------------------- // --------------------
# 3. Create Vector Store (Chroma)

def initialize_vector_store(documents: list[Document]) -> Chroma:
    try:
        embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
        
        if os.environ.get("ENVIRONMENT") == "prod":
            db_directory = "/tmp/vector_db"
        else:
            db_directory = str(VECTOR_DB_FOLDER)

        vector_store = Chroma(
            persist_directory=db_directory,
            embedding_function=embeddings,
            collection_name=COLLECTION_NAME
        )
        
        if vector_store._collection.count() > 0:
            logging.info("Data is already loaded in vector store.")
        else:
            logging.info("Collection is empty. Generating embeddings...")
            vector_store.add_documents(documents=documents)
            
        logging.info("Successfully initialized Chroma vector store.")
        return vector_store
    
    except Exception as e:
        logging.error(f"Failure initializing vector store: {e}")
        raise e

# -------------------- // --------------------
# 4. Create Retriever

def create_retriever() -> VectorStoreRetriever:
    try:
        docs = create_documents()
        split_docs = split_documents(docs)
        vector_store = initialize_vector_store(split_docs)
        
        return vector_store.as_retriever(
            search_kwargs={"k": 4},
            search_type="similarity"
        )
    except Exception as e:
        logging.error(f"Error initializing vector store retriever: {e}", exc_info=True)
        raise e