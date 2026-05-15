# Creator Intelligence Agent 🤖🎥

An AI-powered research and content ideation engine. This project automates the process of downloading/processing videos from your favorite creators, transcribing them using **Groq Whisper**, and using an **Agno (Phidata) Agent** to brainstorm new content ideas based on their transcripts.


## 🚀 Workflow

1. **Extract:** Automatically pulls high-quality audio from video files using `ffmpeg`.
2. **Transcribe:** Uses the lightning-fast `whisper-large-v3` model via **Groq** to turn speech into text.
3. **Organize:** Stores transcriptions in a structured JSON database categorized by creator name.
4. **Ideate:** A GPT-powered Agent browses your "transcription library" to help you write scripts, find patterns, or brainstorm new video ideas.


## 🛠 Prerequisites

### System Requirements

* **FFmpeg**: This tool is required for audio extraction.
* *macOS:* `brew install ffmpeg`
* *Ubuntu:* `sudo apt install ffmpeg`
* *Windows:* Download from [ffmpeg.org](https://ffmpeg.org/download.html)

### Environment Variables

Create a `.env` file in the root directory and add your API keys:

```env
GROQ_API_KEY=your_groq_key_here
OPENAI_API_KEY=your_openai_key_here
TAVILY_API_KEY=your_tavily_key_here
```

## 📁 Before You Start: Folder Structure

The script relies on a specific directory structure to identify creators. Organize your raw videos like this:

```text
.
├── videos/
│   ├── jeff_nippard/
│   │   ├── full_day_of_eating.mp4
│   │   └── hypertrophy_tips.mkv
│   └── kallaway/
│       └── apple_vision_pro_review.mp4
├── transcriptions/      # (Auto-generated)
└── agent.py

```

## 🏃 How to Run

### 1. Upload your videos on the /videos folder

To get the most of this agent, you must upload videos of your favorite content creators as references


### 2. Transcribe the Videos

First, run the transcriber to process any new videos in your `videos/` folder:

```bash
uv run video_transcriber.py
```

Check inside the `transcriptions/` folder if the .json files with transcriptions were correctly generated.

### 3. Launch the AI Agent

Start the AgentOS server:

```bash
uv run agent.py
```

By default, the server runs on **port 7777**.

### 4. Using a UI

If you prefer a graphical interface, you can use **AgentUI**.

* Follow the [Agno AgentUI Documentation](https://www.google.com/search?q=https://docs.agno.com/ui/introduction) to connect the UI to your running instance at `localhost:7777`.


## 💡 How to Use

The main focus of the conversation with your agent is gathering creative ideas and writing hooks/scripts for content creation.

When you make a request, **the AI will dynamically look up your database and ask you which creator you want to use as a style reference** to shape the final script.

### Sample Prompts to Try:

* *"Hi! Can you create a reels about how cats know by instinct to use the litter box?"*
* *"Write a reels about minimum body fat in women."*
* *"I want to create a reels about egg freezing..."*


## 📦 Dependencies

* [Agno (formerly Phidata)](https://github.com/agno-agi/agno): For the Agentic Framework.
* [Groq](https://groq.com/): For high-speed Whisper transcriptions.
* [FFmpeg](https://ffmpeg.org/): For media processing.
* [Tavily](https://tavily.com/): For real-time web search capabilities.

---

*Developed with ❤️  by [GHBAlbuquerque](https://github.com/GHBAlbuquerque)*