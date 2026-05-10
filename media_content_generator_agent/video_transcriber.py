import os
import json
import subprocess
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def extract_audio_from_video(video_path: Path) -> Path:
    """Extracts audio from video and returns the path to the temporary audio file."""
    audio_path = video_path.with_suffix(".mp3")
    print(f"    Extracting audio: {video_path.name} -> {audio_path.name}")
    
    # Construct the FFmpeg command
    command = [
        "ffmpeg",
        "-i", str(video_path),     # Input file
        "-vn",                     # Disable video processing
        "-acodec", "libmp3lame",   # Use MP3 codec
        "-q:a", "2",               # High quality audio
        str(audio_path),           # Output file
        "-y"                       # Overwrite if file already exists
    ]
    
    try:
        # Run the command and suppress output to keep terminal clean
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        raise ValueError(f"Failed to extract audio. Does '{video_path.name}' have an audio track? Ensure FFmpeg is installed.")

    return audio_path

def transcribe_with_groq(client: Groq, audio_path: Path) -> str:
    """Sends audio to Groq Whisper for transcription."""
    print(f"    Transcribing with Groq Whisper...")
    with open(audio_path, "rb") as audio_file:
        # Using whisper-large-v3 for high quality results
        transcription = client.audio.transcriptions.create(
            file=(audio_path.name, audio_file.read()),
            model="whisper-large-v3",
        )
    return transcription.text

def process_videos_by_creator():
    client = Groq()
    
    # Target the 'videos' directory in the current working directory
    videos_dir = Path("videos")
    
    if not videos_dir.exists():
        print(f"Error: Directory '{videos_dir}' not found.")
        return

    video_extensions = {".mp4", ".mkv", ".mov", ".avi", ".webm"}

    # Iterate through each folder (representing a creator)
    for creator_folder in videos_dir.iterdir():
        if not creator_folder.is_dir():
            continue
            
        creator_name = creator_folder.name
        print(f"\n>>> Processing Creator: {creator_name}")
        
        transcriptions = []
        
        # Find all videos within the creator's folder
        for file_path in creator_folder.iterdir():
            if file_path.suffix.lower() in video_extensions:
                print(f"  Processing: {file_path.name}")
                
                temp_audio = None
                try:
                    temp_audio = extract_audio_from_video(file_path)
                    text = transcribe_with_groq(client, temp_audio)
                    transcriptions.append({
                        "video": file_path.name,
                        "transcription": text
                    })
                except Exception as e:
                    print(f"    [Error] {file_path.name}: {e}")
                finally:
                    # Cleanup temporary audio file to save space
                    if temp_audio and temp_audio.exists():
                        temp_audio.unlink()
        
        # Save transcriptions to creator_name.json
        if transcriptions:
            output_json = Path(f"transcriptions/{creator_name}.json")
            with open(output_json, "w", encoding="utf-8") as f:
                json.dump(transcriptions, f, indent=4, ensure_ascii=False)
            print(f"SUCCESS: Saved results to {output_json}")

if __name__ == "__main__":
    process_videos_by_creator()
