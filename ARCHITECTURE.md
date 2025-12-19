# System Architecture

## Overview

The AI Knowledge application is built with a microservices architecture using Docker containers. All components run locally and communicate through a Docker network.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         User's Browser                           │
│                    http://localhost:8501                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Docker Network                              │
│  (ai-knowledge-network)                                          │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Web UI Container (webui)                     │  │
│  │                                                            │  │
│  │  ┌─────────────────────────────────────────────┐         │  │
│  │  │         Streamlit Application                │         │  │
│  │  │           (app.py)                           │         │  │
│  │  │                                              │         │  │
│  │  │  • File Upload UI                            │         │  │
│  │  │  • Document Processing                       │         │  │
│  │  │  • Chat Interface                            │         │  │
│  │  │  • Session Management                        │         │  │
│  │  └──────────┬────────────────┬──────────────────┘         │  │
│  │             │                │                             │  │
│  │             │ PyPDF2         │ LangChain                   │  │
│  │             ▼                ▼                             │  │
│  │  ┌──────────────┐  ┌──────────────────┐                  │  │
│  │  │ PDF Text     │  │ RAG Pipeline     │                  │  │
│  │  │ Extraction   │  │ • Text Splitting │                  │  │
│  │  │              │  │ • Embeddings     │                  │  │
│  │  │              │  │ • Retrieval      │                  │  │
│  │  └──────────────┘  └──────────────────┘                  │  │
│  │                                                            │  │
│  │  Volumes:                                                  │  │
│  │  • ./uploads → /app/uploads                               │  │
│  │  • ./chroma_db → /app/chroma_db                           │  │
│  └──────────────┬────────────────┬──────────────────────────┘  │
│                 │                │                              │
│                 │                │                              │
│        ┌────────▼────────┐  ┌────▼──────────┐                 │
│        │                 │  │               │                 │
│        │  local OllamaLLM│  │   ChromaDB    │                 │
│        │  Container      │  │   (Local)     │                 │
│        │                 │  │               │                 │
│        │ • gpt-oss:20b   │  │ • Embeddings  │                 │
│        │ • Inference     │  │ • Vectors     │                 │
│        │ • API: :11434   │  │ • Search      │                 │
│        │                 │  │               │                 │
│        │                 │  │               │                 │
│        │                 │  │               │                 │
│        └─────────────────┘  └───────────────┘                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Web UI Container (Streamlit)

**Technology**: Python 3.11, Streamlit
**Port**: 8501
**Purpose**: User interface and application logic

**Responsibilities**:
- Serve web interface
- Handle file uploads
- Process PDF documents
- Manage chat sessions
- Coordinate RAG pipeline
- Display results

**Key Libraries**:
- `streamlit`: Web UI framework
- `PyPDF2`: PDF text extraction
- `langchain`: RAG orchestration
- `sentence-transformers`: Text embeddings
- `chromadb`: Vector database client

### 2. Ollama Container (LLM)

**Technology**: Ollama runtime
**Port**: 11434
**Purpose**: Large Language Model inference

**Responsibilities**:
- Run Llama2 model locally
- Provide text generation API
- Answer questions based on context
- No external API calls

**Model**: Llama2 (7B parameters)
**Storage**: Docker volume `ollama_data`

### 3. ChromaDB (Vector Store)

**Technology**: ChromaDB (embedded)
**Purpose**: Vector database for semantic search

**Responsibilities**:
- Store document embeddings
- Perform similarity search
- Return relevant chunks
- Persist vector data

**Storage**: Local directory `./chroma_db`

## Data Flow

### Document Processing Flow

```
1. User uploads PDF
        ↓
2. PDF saved to ./uploads/
        ↓
3. Extract text with PyPDF2
        ↓
4. Split into chunks (1000 chars)
        ↓
5. Generate embeddings (Sentence Transformers)
        ↓
6. Store in ChromaDB
        ↓
7. Ready for queries
```

### Query Processing Flow

```
1. User asks question
        ↓
2. Generate question embedding
        ↓
3. Search ChromaDB for similar chunks (k=3)
        ↓
4. Retrieve relevant text chunks
        ↓
5. Combine chunks + question → prompt
        ↓
6. Send to Ollama (Llama2)
        ↓
7. LLM generates answer
        ↓
8. Display answer + sources
```

## Network Architecture

### Docker Network
- **Name**: `ai-knowledge-network`
- **Type**: Bridge network
- **Isolation**: Containers communicate internally
- **External Access**: Only webui exposed on host

### Port Mappings

| Service | Internal Port | External Port | Purpose |
|---------|---------------|---------------|---------|
| webui   | 8501         | 8501          | Web UI access |
| ollama  | 11434        | 11434         | LLM API (optional) |

## Storage Architecture

### Volume Mounts

| Path          | Type   | Purpose                    | Persistence |
|---------------|--------|----------------------------|-------------|
| uploads/      | Bind   | Uploaded PDF files         | Host        |
| chroma_db/    | Bind   | Vector database            | Host        |
| ollama_data   | Volume | LLM models and cache       | Docker      |

### Data Persistence

- **Uploaded Files**: Persist on host in `./uploads/`
- **Vector DB**: Persist on host in `./chroma_db/`
- **LLM Models**: Persist in Docker volume
- **Chat History**: Session state (not persisted)

## Security Architecture

### Network Security
- **Isolation**: Services in private Docker network
- **No External Calls**: All processing is local
- **No Authentication**: Single-user local application

### Data Security
- **Local Only**: No data leaves the machine
- **No Telemetry**: No tracking or analytics
- **File Access**: Restricted to mounted volumes
- **Model Privacy**: LLM runs locally, no API calls

## Scalability Considerations

### Current Limitations
- **Single User**: Not designed for multi-user
- **In-Memory State**: Chat history not persisted
- **Sequential Processing**: One query at a time
- **Local Compute**: Limited by host resources

### Potential Improvements
- Add user authentication
- Persist chat history in database
- Add job queue for concurrent processing
- Distributed vector storage
- GPU acceleration for LLM

## Technology Stack

### Backend
- **Python 3.11**: Core language
- **LangChain**: RAG framework
- **Ollama**: LLM runtime
- **ChromaDB**: Vector database

### Frontend
- **Streamlit**: Web framework
- **HTML/CSS**: UI rendering

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Orchestration

### AI/ML
- **Llama2**: Language model
- **Sentence Transformers**: Embeddings
- **all-MiniLM-L6-v2**: Embedding model

## Resource Requirements

### Minimum
- **CPU**: 4 cores
- **RAM**: 8GB
- **Disk**: 10GB
- **Network**: Internet (for initial setup)

### Recommended
- **CPU**: 8+ cores
- **RAM**: 16GB+
- **Disk**: 20GB+ (SSD preferred)
- **GPU**: Optional (future enhancement)

## Development Considerations

### Adding New Features

**To add new file types**:
1. Add parser library to requirements.txt
2. Implement extraction function
3. Update file_uploader types
4. Add processing logic

**To add new LLM models**:
1. Pull model: `ollama pull <model>`
2. Update model name in app.py
3. Adjust prompt templates if needed

**To add new UI features**:
1. Modify app.py Streamlit components
2. Update session state as needed
3. Test UI responsiveness

### Testing Strategy

**Component Testing**:
- Test PDF extraction with various PDFs
- Test embedding generation
- Test vector search accuracy
- Test LLM responses

**Integration Testing**:
- Test full RAG pipeline
- Test error handling
- Test edge cases

**System Testing**:
- Test with Docker Compose
- Test resource usage
- Test concurrent uploads

## Deployment

### Local Deployment
```bash
docker compose up -d
```

### Production Considerations
- Add authentication
- Add HTTPS/TLS
- Set up monitoring
- Configure backups
- Scale resources

## Monitoring

### Logs
```bash
docker compose logs -f
```

### Health Checks
- Ollama: `curl http://localhost:11434/api/tags`
- Web UI: Access http://localhost:8501

### Metrics
- Container resource usage: `docker stats`
- Disk usage: `du -sh uploads/ chroma_db/`

## Backup and Recovery

### Backup
```bash
tar -czf backup.tar.gz uploads/ chroma_db/
```

### Restore
```bash
tar -xzf backup.tar.gz
```

### Disaster Recovery
1. Backup volumes regularly
2. Store backups externally
3. Document restoration process
4. Test recovery procedures

## Future Architecture

### Potential Enhancements
- Multi-user support with authentication
- Persistent chat history database
- API endpoints (REST/GraphQL)
- Real-time collaboration
- Advanced analytics dashboard
- Integration with cloud storage
- Mobile app support

---

For implementation details, see:
- [README.md](README.md) - Setup and usage
- [CONTRIBUTING.md](CONTRIBUTING.md) - Development guide
- [USER_GUIDE.md](USER_GUIDE.md) - User documentation
