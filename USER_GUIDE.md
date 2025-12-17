# AI Knowledge Application - User Guide

## Getting Started

### Prerequisites
Before you begin, make sure you have:
- Docker installed (version 20.10 or higher)
- Docker Compose installed (version 2.0 or higher)
- At least 8GB of RAM available
- At least 5GB of free disk space

### Installation

1. **Clone the repository** (if you haven't already)
   ```bash
   git clone <repository-url>
   cd ai-knowledge
   ```

2. **Make scripts executable**
   ```bash
   chmod +x setup.sh test.sh
   ```

3. **Test the installation** (optional)
   ```bash
   ./test.sh
   ```

4. **Start the application**
   ```bash
   ./setup.sh
   ```

   The setup script will:
   - Start all Docker containers
   - Pull the Llama2 model (this may take 10-15 minutes on first run)
   - Make the application available at http://localhost:8501

### First-Time Setup

When you first start the application:

1. Wait for all services to start (you'll see "✅ Ollama Connected" in the sidebar when ready)
2. The Llama2 model download is automatic but may take time depending on your internet speed
3. Once ready, you can start uploading documents

## Using the Application

### Step 1: Upload PDF Documents

1. Open http://localhost:8501 in your web browser
2. Look at the left sidebar
3. Click on "Browse files" under "Document Upload"
4. Select one or more PDF files from your computer
5. Click "Process Documents"
6. Wait for the processing to complete (you'll see ✅ marks for each document)

**Tips:**
- You can upload multiple PDFs at once
- Supported file types: PDF only
- Make sure PDFs are not password-protected
- Larger PDFs will take longer to process

### Step 2: Ask Questions

Once your documents are processed:

1. Type your question in the chat input at the bottom
2. Press Enter or click the send button
3. Wait for the AI to process your question (usually 10-30 seconds)
4. View the answer in the chat interface

**Example Questions:**
- "What is the main topic of this document?"
- "Summarize the key points from the documents"
- "What does the document say about [specific topic]?"
- "Find information about [specific term or concept]"

### Step 3: View Source Documents

After receiving an answer:
1. Click on "📑 Source Documents" below the answer
2. View the relevant text chunks that were used to generate the answer
3. This helps verify the accuracy of the AI's response

### Managing Your Session

- **Clear Chat History**: Click the "Clear Chat History" button in the sidebar to start fresh
- **Upload More Documents**: You can upload and process additional PDFs at any time
- **Processing**: Processing new documents will add them to the existing knowledge base

## Common Tasks

### Stopping the Application

```bash
docker-compose down
```

### Restarting the Application

```bash
docker-compose restart
```

### Viewing Logs

To see what's happening behind the scenes:

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f webui    # Web interface logs
docker-compose logs -f ollama   # LLM service logs
```

### Removing All Data

To completely remove all data and start fresh:

```bash
# Stop and remove containers
docker-compose down

# Remove uploaded files and database
rm -rf uploads/ chroma_db/

# Remove Docker volumes
docker-compose down -v
```

## Troubleshooting

### Problem: "❌ Ollama Not Connected"

**Solutions:**
1. Wait 1-2 minutes - Ollama takes time to start
2. Check if the Ollama container is running:
   ```bash
   docker ps | grep ollama
   ```
3. View Ollama logs:
   ```bash
   docker logs ai-knowledge-ollama
   ```
4. Restart the Ollama service:
   ```bash
   docker-compose restart ollama
   ```

### Problem: Slow Response Times

**Possible causes:**
1. Large document set - more documents mean longer search time
2. Limited RAM - LLM needs sufficient memory
3. Complex questions - some questions take longer to process

**Solutions:**
1. Upload fewer documents initially
2. Ensure at least 8GB RAM is available
3. Try simpler, more specific questions first

### Problem: "Out of Memory" Error

**Solutions:**
1. Close other applications to free up RAM
2. Process fewer documents at once
3. Consider using a smaller LLM model (requires code modification)

### Problem: PDF Processing Fails

**Common causes:**
1. PDF is password-protected
2. PDF is corrupted or malformed
3. PDF contains only images (no extractable text)

**Solutions:**
1. Remove password protection from PDF
2. Try a different PDF file
3. For image-based PDFs, consider using OCR preprocessing

### Problem: Port Already in Use

If you see an error about port 8501 or 11434 being in use:

**Solution:**
Edit `docker-compose.yml` and change the port mappings:
```yaml
ports:
  - "8502:8501"  # Changed from 8501
```

## Advanced Configuration

### Using Different LLM Models

Ollama supports multiple models. To use a different one:

1. Pull the desired model:
   ```bash
   docker exec ai-knowledge-ollama ollama pull mistral
   ```

2. Edit `app.py` and change the model name:
   ```python
   llm = Ollama(
       base_url=OLLAMA_HOST,
       model="mistral"  # Changed from "llama2"
   )
   ```

3. Restart the webui container:
   ```bash
   docker-compose restart webui
   ```

Available models include:
- `llama2` (default, 7B parameters)
- `mistral` (7B parameters, faster)
- `codellama` (optimized for code)
- `neural-chat` (conversational)

### Adjusting Chunk Size

For better or worse retrieval results, you can modify the text chunking:

Edit `app.py` in the `create_vector_store` function:
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,   # Increase for more context
    chunk_overlap=200,  # Increase for better continuity
    length_function=len
)
```

### Changing the Number of Retrieved Documents

To retrieve more or fewer document chunks for answering:

Edit `app.py` in the `setup_qa_chain` function:
```python
retriever=vectorstore.as_retriever(search_kwargs={"k": 3})  # Change 3 to desired number
```

## Tips for Best Results

1. **Use High-Quality PDFs**: Text-based PDFs work best
2. **Ask Specific Questions**: More specific questions get better answers
3. **Upload Related Documents**: Group related documents together
4. **Check Source Documents**: Always verify the AI's sources
5. **Start Small**: Test with 1-2 documents before uploading many
6. **Be Patient**: First-time model loading takes several minutes
7. **Use Clear Language**: Simple, direct questions work best

## Security and Privacy

- **All data stays local**: No information is sent to external servers
- **Offline capable**: Once models are downloaded, works without internet
- **Private conversations**: Your chats are not stored or monitored
- **Document security**: Uploaded files remain on your machine

## Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Review the logs: `docker-compose logs -f`
3. Ensure prerequisites are met (Docker, RAM, disk space)
4. Try restarting services: `docker-compose restart`
5. Check GitHub issues for similar problems
6. Open a new issue with error logs and system information

## System Requirements

**Minimum:**
- CPU: 4 cores
- RAM: 8GB
- Disk: 10GB free space
- OS: Linux, macOS, or Windows with WSL2

**Recommended:**
- CPU: 8+ cores
- RAM: 16GB+
- Disk: 20GB+ free space
- SSD storage for better performance

## Performance Tips

1. **Use SSD storage** for faster document processing
2. **Close unnecessary applications** to free up RAM
3. **Process documents in batches** if you have many files
4. **Use a wired network connection** for initial model download
5. **Consider GPU support** for faster inference (requires additional setup)

## Updating the Application

To update to the latest version:

```bash
# Pull latest changes
git pull

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Backup and Restore

### Backup your data:
```bash
# Create backup directory
mkdir -p backups

# Backup uploaded files and database
tar -czf backups/ai-knowledge-backup-$(date +%Y%m%d).tar.gz uploads/ chroma_db/
```

### Restore from backup:
```bash
# Extract backup
tar -xzf backups/ai-knowledge-backup-YYYYMMDD.tar.gz
```

## Uninstallation

To completely remove the application:

```bash
# Stop and remove containers
docker-compose down -v

# Remove images
docker rmi ai-knowledge-webui ollama/ollama

# Remove data directories
rm -rf uploads/ chroma_db/

# Remove downloaded models (optional)
docker volume rm ai-knowledge_ollama_data
```

---

**Need more help?** Check the README.md file or open an issue on GitHub.
