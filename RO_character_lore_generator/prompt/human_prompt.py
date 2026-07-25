def build_human_prompt(data: dict) -> str:
    return ""
    pass


# def build_human_prompt(data: dict) -> str:
#     # Start with the required fields
#     prompt_parts = [
#         f"Generate a character with these details:",
#         f"- Class: {data['class']}",
#         f"- Gender: {data['gender']}"
#     ]
    
#     # Conditionally add optional fields only if they have values
#     if data.get('name'):
#         prompt_parts.append(f"- Character Name: {data['name']}")
#     if data.get('location'):
#         prompt_parts.append(f"- Birth Location: {data['location']}")
#     if data.get('age'):
#         prompt_parts.append(f"- Age: {data['age']}")
#     if data.get('alignment'):
#         prompt_parts.append(f"- Alignment: {data['alignment']}")
#     if data.get('description'):
#         prompt_parts.append(f"- Brief Description: {data['description']}")
#     else:
#         prompt_parts.append(f"- Brief Description: None provided. Invent a fitting background.")

#     return "\n".join(prompt_parts)