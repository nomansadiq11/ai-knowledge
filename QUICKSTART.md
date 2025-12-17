# Quick Start Guide

## What This Application Does

This AI Knowledge application allows you to:
- Upload PDF documents
- Ask questions about the content in natural language
- Get AI-powered answers based on your documents
- All running locally on your machine with open-source tools

## Requirements

- **Docker** and **Docker Compose** installed
- **8GB RAM** minimum (16GB recommended)
- **10GB free disk space** (for models and data)

## Quick Start (3 Steps)

### 1. Start the Application

```bash
# Make the script executable (first time only)
chmod +x setup.sh

# Run the setup script
./setup.sh
```

This will:
- Start all Docker containers
- Download the Llama2 AI model (takes 5-15 minutes first time)
- Make the app available at http://localhost:8501

### 2. Upload Your PDFs

1. Open http://localhost:8501 in your browser
2. Click "Browse files" in the left sidebar
3. Select one or more PDF files
4. Click "Process Documents"
5. Wait for processing to complete

### 3. Start Chatting

- Type your question in the chat box at the bottom
- Press Enter
- Wait for the AI to respond (10-30 seconds)
- View source documents to verify the answer

## Example Questions

- "What is this document about?"
- "Summarize the main points"
- "Find information about [specific topic]"
- "What does it say about [specific term]?"

## Stopping the Application

```bash
docker compose down
```

## Need Help?

See the detailed [USER_GUIDE.md](USER_GUIDE.md) for:
- Troubleshooting
- Advanced configuration
- Tips and best practices
- Security and privacy information

## Architecture Overview

```
┌─────────────┐
│  Web UI     │  ← Your browser (http://localhost:8501)
│ (Streamlit) │
└──────┬──────┘
       │
       ├─────┐
       │     │
┌──────▼──┐  │  ┌──────────┐
│ Ollama  │  └──►  ChromaDB │
│  (LLM)  │     │ (Vectors) │
└─────────┘     └──────────┘
```

- **Streamlit**: Web interface
- **Ollama**: Local LLM (Llama2)
- **ChromaDB**: Vector database for document search

## Key Features

✅ **100% Local** - No data leaves your machine
✅ **Open Source** - All components are open-source
✅ **Easy Setup** - One command to start everything
✅ **PDF Support** - Upload and chat with multiple PDFs
✅ **RAG Pipeline** - Retrieval Augmented Generation for accurate answers
✅ **Docker-based** - Easy installation and updates

## Common Issues

**"Ollama Not Connected"**
- Wait 1-2 minutes, it takes time to start
- Check: `docker ps | grep ollama`

**Slow responses**
- Normal - LLM inference takes time locally
- First query is always slower

**Build fails**
- Ensure Docker has internet access
- Check: `docker pull python:3.11-slim`

For more issues, see [USER_GUIDE.md](USER_GUIDE.md#troubleshooting)

## What's Inside

```
ai-knowledge/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── Dockerfile         # Container definition
├── docker-compose.yml # Service orchestration
├── setup.sh          # Quick start script
├── test.sh           # Testing script
├── README.md         # Detailed documentation
├── USER_GUIDE.md     # User guide
└── QUICKSTART.md     # This file
```

## Next Steps

1. **Start the app**: `./setup.sh`
2. **Upload PDFs**: Use the sidebar
3. **Ask questions**: Use the chat interface
4. **Explore**: Try different questions and documents

That's it! You're ready to use your local AI knowledge base.

---

**Have questions?** Check [README.md](README.md) for detailed information or [USER_GUIDE.md](USER_GUIDE.md) for comprehensive user documentation.
