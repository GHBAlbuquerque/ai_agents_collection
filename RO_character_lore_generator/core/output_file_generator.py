import io
import os
import logging
from core.properties import OUTPUT_FOLDER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_pdf_from_string(generated_lore: str) -> bytes:
    """
    Takes the generated lore text/data, builds a PDF in-memory, 
    and returns the raw bytes for download button.
    """
    buffer = io.BytesIO()
    
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    full_content = []
    
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    
    custom_style = ParagraphStyle(
        'CustomStyle',
        parent=normal_style,
        fontSize=12,
        leading=16,          # Line spacing
        spaceAfter=10
    )
    
    for paragraph in generated_lore.split('\n'):
        if paragraph.strip() == '':
            full_content.append(Spacer(1,10))
        else:
            formatted_paragraph = Paragraph(paragraph, custom_style)
            full_content.append(formatted_paragraph)
            
    doc.build(full_content)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes


def save_txt_to_system(generated_lore: str, file_name: str):
    env = os.environ.get("ENVIRONMENT")
    logging.info(env)
    
    if env == "prod":
        logging.info("Skipping local system file save.")
        return
    
    file_name = file_name + ".txt"
    txt_path = OUTPUT_FOLDER / file_name
    
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    txt_path.write_text(generated_lore, encoding="utf-8")


def format_lore_data_to_text(data) -> str:
    """
    Formats a CharacterLoreCreationData or dictionary into a structured readable string for PDF creation.
    """
    lines = [
        f"Character Name: {data.get('name', 'Unknown')}",
        f"Character Class: {data.get('class', '')}",
        f"Gender: {data.get('gender', '')}",
        f"Place of Birth: {data.get('place_of_birth', '')}",
        f"Role: {data.get('role', '')}",
        "",
        "Detailed Description:",
        f"{data.get('description', '')}",
        "",
        "Character Lore:",
        f"Act I: {data.get('act_1', '')}",
        "",
        f"Act II: {data.get('act_2', '')}",
        "",
        f"Act III: {data.get('act_3', '')}",
        "",
        f"Act IV: {data.get('act_4', '')}",
        "",
        f"Metadata: {data.get('metadata', '')}"
    ]
    return "\n".join(lines)