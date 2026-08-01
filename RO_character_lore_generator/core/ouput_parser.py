import re
from api.models import CharacterLoreCreationData

def parse_lore_output(raw_text: str) -> CharacterLoreCreationData:
    parsed = {}
    
    parsed["name"] = re.search(r"Character Name:\s*(.*)", raw_text)
    parsed["class"] = re.search(r"Character Class:\s*(.*)", raw_text)
    parsed["gender"] = re.search(r"Gender:\s*(.*)", raw_text)
    parsed["place_of_birth"] = re.search(r"Place of Birth:\s*(.*)", raw_text)
    
    # UPDATE 1: Metadata is now higher up. It should stop at "Role:"
    parsed["metadata"] = re.search(r"Metadata:\s*(.*?)(?=Role:|$)", raw_text, re.DOTALL)
    
    parsed["role"] = re.search(r"Role:\s*(.*)", raw_text)
    parsed["description"] = re.search(r"Detailed Description:\s*(.*?)(?=Character Lore:|$)", raw_text, re.DOTALL)
    
    parsed["act_1"] = re.search(r"Act I:\s*(.*?)(?=Act II:|$)", raw_text, re.DOTALL)
    parsed["act_2"] = re.search(r"Act II:\s*(.*?)(?=Act III:|$)", raw_text, re.DOTALL)
    parsed["act_3"] = re.search(r"Act III:\s*(.*?)(?=Act IV:|$)", raw_text, re.DOTALL)
    
    # UPDATE 2: Act IV is now the end of the document, so it just runs to the end ($)
    parsed["act_4"] = re.search(r"Act IV:\s*(.*?)$", raw_text, re.DOTALL)

    cleaned = {}
    for k, v in parsed.items():
        if v:
            text = v.group(1).strip()
            text = text.replace("**", "").strip()
            cleaned[k] = text
        else:
            cleaned[k] = ""
            
    return CharacterLoreCreationData(**cleaned)