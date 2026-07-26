from api.models import CharacterLoreCreationRequest

def build_human_prompt(data: CharacterLoreCreationRequest) -> str:
    prompt_parts = [
        "Generate a character with these details:",
        f"- Class: {data.character_class}",
        f"- Gender: {data.gender}"
    ]
    
    # Conditionally add optional fields only if they have values
    if data.character_name:
        prompt_parts.append(f"- Character Name: {data.character_name}")
    if data.birth_location:
        prompt_parts.append(f"- Birth Location: {data.birth_location}")
    if data.character_age:
        prompt_parts.append(f"- Age: {data.character_age}")
    if data.character_alignment:
        prompt_parts.append(f"- Alignment: {data.character_alignment}")
    if data.description:
        prompt_parts.append(f"- Brief Description: {data.description}")
    else:
        prompt_parts.append("- Brief Description: None provided. Invent a fitting background.")

    return "\n".join(prompt_parts)