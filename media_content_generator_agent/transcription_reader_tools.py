import json
from pathlib import Path

def list_available_creators() -> str:
    """
    Lists all content creators currently available in the transcription database.

    Returns:
        str: A list of creator names found in the transcriptions folder.
    """
    transcriptions_dir = Path("transcriptions")
    if not transcriptions_dir.exists():
        return "The 'transcriptions' directory does not exist. Please run the video_transcriber.py script first."

    creators = [f.stem for f in transcriptions_dir.glob("*.json")] #extract filename without formar
    if not creators:
        return "No creator transcription files found in the 'transcriptions' directory."

    return "Available creators: " + ", ".join(creators)

def get_creator_transcriptions(creator_name: str) -> str:
    """
    Reads the transcriptions for a given creator from a JSON file and returns them in Markdown format.

    Args:
        creator_name (str): The name of the content creator (e.g., 'jeffnippard', 'kallaway').

    Returns:
        str: All transcriptions found for the creator, formatted as a Markdown string.
    """
    # Normalize the creator name to match filenames (lowercase, stripped)
    filename = creator_name.lower().strip()
    file_path = Path("transcriptions") / f"{filename}.json"

    if not file_path.exists():
        return f"Error: No transcription data found for '{creator_name}'."

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not data:
            return f"The transcription file for '{creator_name}' is empty."

        formatted_transcripts = []
        for i, entry in enumerate(data, 1): # makes items in a list a key-value pair where the key is the index for counting and the value is the entry itself
            transcript_text = entry.get("transcription", "No transcription available.").strip() # get transcription or default "no transcription"
            formatted_transcripts.append(f"Transcript {i}\n{transcript_text}")

        return "\n\n".join(formatted_transcripts)
    except Exception as e:
        return f"Error reading transcriptions for '{creator_name}': {str(e)}"