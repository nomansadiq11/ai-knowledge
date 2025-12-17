# Changelog

All notable changes to the AI Knowledge application will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2025-12-17

### Security
- **CRITICAL**: Updated langchain from 0.1.0 to 0.3.27 to fix security vulnerabilities
- **CRITICAL**: Updated langchain-community from 0.0.10 to 0.3.27 to fix:
  - XML External Entity (XXE) Attack vulnerability (CVE affecting versions < 0.3.27)
  - SSRF vulnerability in RequestsToolkit component (CVE affecting versions < 0.0.28)
  - Pickle deserialization of untrusted data vulnerability (CVE affecting versions < 0.2.4)

### Changed
- Updated dependencies to latest secure versions
- All functionality remains compatible with new versions

## [1.0.0] - 2025-12-17

### Added
- Initial release of AI Knowledge application
- PDF document upload and processing functionality
- RAG (Retrieval Augmented Generation) pipeline
- Chat interface for querying documents
- Local LLM integration using Ollama and Llama2
- Vector database using ChromaDB for semantic search
- Streamlit-based web UI
- Docker Compose configuration for easy deployment
- Comprehensive documentation:
  - README.md - Main documentation
  - QUICKSTART.md - Quick start guide
  - USER_GUIDE.md - Comprehensive user guide
  - EXAMPLES.md - Usage examples
  - CONTRIBUTING.md - Contribution guidelines
  - ARCHITECTURE.md - System architecture
- Setup and test scripts (setup.sh, test.sh)
- Environment configuration template (.env.example)
- Support for multiple PDF processing
- Source document display for answer verification
- Chat history management
- Session state persistence

### Features
- 100% local execution - no external API calls
- Open-source components only
- Privacy-focused design
- Docker containerization
- Persistent storage for documents and embeddings
- Real-time document processing
- Context-aware question answering
- Multiple document support

### Technical Stack
- Python 3.11
- Streamlit 1.29.0
- LangChain 0.3.27
- LangChain Community 0.3.27
- ChromaDB 0.4.22
- Ollama (Llama2 model)
- Sentence Transformers
- PyPDF2
- Docker & Docker Compose

### Infrastructure
- Multi-container Docker architecture
- Persistent volumes for data storage
- Bridge network for service communication
- Health checks for Ollama service
- Automatic model download on first run

## [Unreleased]

### Planned Features
- Support for additional file formats (DOCX, TXT, etc.)
- Export chat history functionality
- Advanced search filters
- Document organization/folders
- Multi-language support
- Improved error handling
- Performance optimizations
- GPU acceleration support
- User authentication (for multi-user scenarios)
- REST API endpoints
- Unit and integration tests

### Under Consideration
- Support for other LLM models
- Cloud deployment guides
- Kubernetes configuration
- Advanced RAG techniques
- Fine-tuning capabilities
- Document comparison features
- Batch processing
- OCR support for scanned documents

## Version History

### Version 1.0.0 (2025-12-17)
- First stable release
- Complete RAG pipeline
- Full Docker support
- Comprehensive documentation

---

## Release Notes Format

Each release includes:
- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security improvements

## How to Update

To update to the latest version:

```bash
# Pull latest changes
git pull origin main

# Rebuild containers
docker compose down
docker compose build --no-cache
docker compose up -d
```

## Support

For issues or questions about specific versions:
- Check the documentation for that version
- Search existing GitHub issues
- Create a new issue with version information

---

**Current Version**: 1.0.0
**Release Date**: December 17, 2025
**Status**: Stable
