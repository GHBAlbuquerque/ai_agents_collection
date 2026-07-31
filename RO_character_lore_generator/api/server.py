# 🆕 FastAPI server (exposes your python functions via HTTP)
import os
import logging
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from core.properties import ALIGNMENT_OPTIONS, CLASSES_OPTIONS, GENDER_OPTIONS, LOCATIONS_OPTIONS
from api.models import CharacterLoreCreationRequest, CharacterLoreCreationData
from core.agent import get_character_lore
from core.output_file_generator import create_pdf_from_string, format_lore_data_to_text
from fastapi.staticfiles import StaticFiles

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api.server")

app = FastAPI(
    title="RO Character Lore Generator",
    description="Generate character lore for Ragnarok Online characters using AI.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===================
# ENDPOINTS
# ===================

# GET /api/options
@app.get("/api/options",
    tags=["options"],
    summary="Returns Lore Generator Options",
    description="Returns all the options available for the lore generator.")
async def get_options():
    return {
        "alignments": ALIGNMENT_OPTIONS,
        "classes": CLASSES_OPTIONS,
        "genders": GENDER_OPTIONS,
        "locations": LOCATIONS_OPTIONS,
    }

# POST /api/generate-lore
@app.post("/api/generate-lore",
    tags=["lore", "post", "character"],
    summary="Generate a new character lore",
    description="Generate a new character lore for Ragnarok Online characters using AI.",
    response_model=CharacterLoreCreationData)
async def generate_lore(request: CharacterLoreCreationRequest):
    try:
        logger.info(f"Generating lore for request: {request.name}")
        return get_character_lore(request)
    except Exception as e:
        logger.error(f"Error generating lore: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error trying to generate lore: {str(e)}"
        )

# POST /api/generate-pdf
@app.post("/api/generate-pdf",
    tags=["pdf"],
    summary="Generate a PDF file for character lore",
    description="Builds and returns a PDF document based on character lore data.")
async def generate_pdf(request: CharacterLoreCreationData):
    try:
        formatted_text = format_lore_data_to_text(request)
        pdf_bytes = create_pdf_from_string(formatted_text)
        
        filename = f"{request.name or 'Character'}_Lore.pdf"
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error trying to generate PDF: {str(e)}"
        )
        
web_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "web"))
if os.path.exists(web_dir):
    app.mount("/", StaticFiles(directory=web_dir, html=True), name="static")
else:
    logging.warning(f"Web directory not found at {web_dir}")