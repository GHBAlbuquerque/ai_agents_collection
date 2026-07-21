
from pypdf import PdfReader
from langchain_core.documents import Document
from configs import FILES_FOLDER
from dotenv import load_dotenv

load_dotenv()

# -------------------- // --------------------
# 1. Load pdfs

def document_loading():
    documents = []
    
    for file in FILES_FOLDER.glob('*.pdf'):
        reader = PdfReader(file)
        
        file_pages = [Document(page_content=page.extract_text(), 
                             metadata={"source": file.name, "page": i}) 
                    for i, page in enumerate(reader.pages)]
        
        documents.extend(file_pages)
        
    print(f'Loaded documents: {len(documents)}')
    return documents

# -------------------- // --------------------
# 2. Chunkerization

# TODO


# -------------------- // --------------------


if __name__ == "__main__":
    document_loading()