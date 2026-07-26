# 🆕 FastAPI server (exposes your python functions via HTTP)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from properties import ALIGNMENT_OPTIONS, CLASSES_OPTIONS, GENDER_OPTIONS, LOCATIONS_OPTIONS
from api.models import CharacterLoreCreationRequest, CharacterLoreCreationResponse

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

@app.get("/")
def read_root():
    return {"message": "Character Lore Generator API is running!"}

# GET/api/options
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
    response_model=CharacterLoreCreationResponse)
async def generate_lore(request: CharacterLoreCreationRequest):
    return CharacterLoreCreationResponse()

# POST /api/generate-pdf
@app.post("/api/generate-pdf")
async def generate_pdf():
    return {
        "message": "PDF generated successfully!"
    }