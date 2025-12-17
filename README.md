# AI Knowledge Base Application

A local AI-powered knowledge base application that allows you to upload PDF documents and chat with them using open-source tools. All components run locally using Docker.

## Features

- 📄 **PDF Processing**: Upload and process multiple PDF documents
- 💬 **Chat Interface**: Ask questions about your documents in natural language
- 🤖 **Local LLM**: Uses Ollama with Llama2 model (runs completely offline)
- 🗄️ **Vector Storage**: ChromaDB for efficient document retrieval
- 🔍 **RAG Pipeline**: Retrieval Augmented Generation for accurate answers
- 🎨 **Modern UI**: Clean Streamlit-based web interface
- 🐳 **Docker Compose**: Easy setup with all services containerized

## Architecture

The application consists of three main components:

1. **Web UI (Streamlit)**: User interface for uploading PDFs and chatting
2. **Ollama**: Local LLM service running Llama2 model
3. **Vector Database**: Local ChromaDB for storing document embeddings

## Prerequisites

- Docker and Docker Compose installed
- At least 8GB of RAM (for running the LLM)
- At least 5GB of free disk space (for the Llama2 model)

## Quick Start

### Option 1: Using the setup script (Linux/Mac)

```bash
# Make the setup script executable
chmod +x setup.sh

# Run the setup script
./setup.sh
```

### Option 2: Manual setup

```bash
# Start all services
docker-compose up -d

# Wait for services to start
sleep 10

# Pull the Llama2 model (first time only)
docker exec ai-knowledge-ollama ollama pull llama2

# Access the application
# Open your browser to http://localhost:8501
```

## Usage

1. **Start the Application**
   - Run `./setup.sh` or `docker-compose up -d`
   - Wait for all services to start (may take a minute)

2. **Upload Documents**
   - Open http://localhost:8501 in your browser
   - Use the sidebar to upload one or more PDF files
   - Click "Process Documents" to index them

3. **Chat with Your Documents**
   - Type your questions in the chat interface
   - The AI will answer based on the content of your PDFs
   - View source documents to see where answers came from

4. **Stop the Application**
   ```bash
   docker-compose down
   ```

## Project Structure

```
ai-knowledge/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container for web UI
├── docker-compose.yml    # Service orchestration
├── setup.sh             # Setup script
├── README.md            # This file
├── uploads/             # Uploaded PDF files (created at runtime)
└── chroma_db/           # Vector database storage (created at runtime)
```

## Technologies Used

- **Python**: Main programming language
- **Streamlit**: Web UI framework
- **LangChain**: RAG pipeline and LLM integration (v0.3.27 - security patched)
- **LangChain Community**: Community integrations (v0.3.27 - security patched)
- **Ollama**: Local LLM inference
- **ChromaDB**: Vector database for embeddings
- **Sentence Transformers**: Text embeddings
- **PyPDF2**: PDF text extraction
- **Docker**: Containerization

## Configuration

Environment variables can be configured in `docker-compose.yml`:

- `OLLAMA_HOST`: Ollama service URL (default: `http://ollama:11434`)
- Port `8501`: Web UI access port
- Port `11434`: Ollama API port

## Troubleshooting

### Ollama not connecting
- Wait a few minutes after starting services
- Check if Ollama container is running: `docker ps`
- View Ollama logs: `docker logs ai-knowledge-ollama`

### Out of memory errors
- Ensure you have at least 8GB RAM available
- Try using a smaller model (edit the model name in `app.py`)

### PDF processing fails
- Ensure PDFs are not encrypted or password-protected
- Try processing one PDF at a time

### Port conflicts
- If ports 8501 or 11434 are in use, modify the ports in `docker-compose.yml`

## Advanced Usage

### Using Different LLM Models

To use a different Ollama model, edit `app.py` and change the model name:

```python
llm = Ollama(
    base_url=OLLAMA_HOST,
    model="mistral"  # or "codellama", "neural-chat", etc.
)
```

Then pull the model:
```bash
docker exec ai-knowledge-ollama ollama pull mistral
```

### Viewing Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f webui
docker-compose logs -f ollama
```

### Persistent Storage

Document embeddings and uploaded files are stored in:
- `./uploads/` - Uploaded PDF files
- `./chroma_db/` - Vector database

These directories persist between container restarts.

## Development

To run the application locally without Docker:

```bash
# Install dependencies
pip install -r requirements.txt

# Start Ollama separately
# Download from https://ollama.ai

# Pull the model
ollama pull llama2

# Run the application
streamlit run app.py
```

## License

This project is open source and available for educational and personal use.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## Security Note

This application runs entirely locally and does not send any data to external services. Your documents and conversations remain private on your machine.
