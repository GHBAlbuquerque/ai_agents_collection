
```
RO_character_lore_generator/
├── agent.py                 # Core LangChain agent logic (unchanged)
├── ingestion.py             # Vector database retriever (unchanged)
├── properties.py            # Classes, alignments, locations, model name (unchanged)
├── ouput_parser.py          # Output parsing logic (unchanged)
├── output_file_generator.py # PDF generation logic (unchanged)
├── server.py                # 🆕 FastAPI server (exposes your python functions via HTTP)
├── web/                     # 🆕 Ragnarok Online Custom Web Interface
│   ├── index.html           # Main RO character creation & lore UI
│   ├── css/
│   │   └── ro-theme.css     # Classic RO window borders, pixel fonts, parchment scrolls
│   ├── js/
│   │   └── app.js           # Handles form submissions, sprite updates & API calls
│   └── assets/              # Sprites (Classes/Genders), RO fanarts, button click SFX
├── vector_db/               # Existing vector DB files
├── pyproject.toml           # Added fastapi & uvicorn dependencies
└── README.md
```

## ⚙️ How to Run

1. **Environment Setup:** Make sure you have your `.env` file configured in the project directory with your API keys (e.g., `OPENAI_API_KEY`, OMDb keys).
2. **Start the Server:**
   Run
   ```bash
   dotenv run python main.py
   ```
    OR 
   ```bash
   python main.py
   ```
