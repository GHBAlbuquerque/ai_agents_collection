
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
        print(f"Reading file: {file.name}")
        reader = PdfReader(file)
        
        file_pages = [Document(page_content=page.extract_text(), 
                             metadata={"source": file.name, "page": i}) 
                    for i, page in enumerate(reader.pages)]
        
        documents.extend(file_pages)
        
    print(f'Loaded documents: {len(documents)}')
    return documents

# -------------------- // --------------------
# 2. Chunkerization

def split_documents(documents : list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100, length_function=len)
    
    chunks = splitter.split_documents(documents=documents)
    print(f"Created chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks):
        chunk.metadata['source'] = chunk.metadata['source'].split('/')
        chunk.metadata['id'] = i
        
    return chunks

# -------------------- // --------------------
# 3. Create Vector Store (Chroma)

def initialize_vector_store(documents: list[Document]) -> Chroma:
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    vector_store = Chroma(persist_directory=str(VECTOR_DB_FOLDER),
                          embedding_function=embeddings,
                         collection_name=COLLECTION_NAME)
    
    if vector_store._collection.count() > 0:
        print("Data is already loaded.")
    else:
        print("Collection is empty. Generating embbedings...")
        vector_store.add_documents(documents=documents)
        
    print("Succesfully initilialized Chroma vector store.")
    return vector_store

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
        print(e)
        return vector_store.as_retriever(
            search_kwargs = {"k":4, "fetch_k":20},
            search_type="mmr"
        )