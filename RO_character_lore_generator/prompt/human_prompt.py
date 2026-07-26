def build_human_prompt(data: dict) -> str:
    prompt_parts = [
        f"Generate a character with these details:",
        f"- Class: {data['character_class']}",
        f"- Gender: {data['gender']}"
    ]
    
    #Conditionally add optional fields only if they have values
    if data.get('character_name'):
        prompt_parts.append(f"- Character Name: {data['character_name']}")
    if data.get('birth_location'):
        prompt_parts.append(f"- Birth Location: {data['birth_location']}")
    if data.get('character_age'):
        prompt_parts.append(f"- Age: {data['character_age']}")
    if data.get('character_alignment'):
        prompt_parts.append(f"- Alignment: {data['character_alignment']}")
    if data.get('description'):
        prompt_parts.append(f"- Brief Description: {data['description']}")
    else:
        prompt_parts.append(f"- Brief Description: None provided. Invent a fitting background.")

    return "\n".join(prompt_parts)