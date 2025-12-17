# Contributing to AI Knowledge Application

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/ai-knowledge.git
   cd ai-knowledge
   ```
3. **Create a branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Prerequisites
- Python 3.11+
- Docker and Docker Compose
- Git

### Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Ollama separately** (or use Docker):
   ```bash
   # Option 1: Use Docker Compose
   docker compose up ollama -d
   
   # Option 2: Install Ollama locally
   # Visit https://ollama.ai for installation
   ollama pull llama2
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## Code Style

- Follow PEP 8 style guide for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Comment complex logic

## Making Changes

### Code Changes

1. Make your changes in your feature branch
2. Test your changes thoroughly
3. Ensure the Docker build still works:
   ```bash
   docker compose build
   ```
4. Update documentation if needed

### Adding Features

When adding new features:
- Update the README.md with feature description
- Add usage examples to EXAMPLES.md if applicable
- Update USER_GUIDE.md with any new instructions
- Ensure backward compatibility when possible

### Bug Fixes

When fixing bugs:
- Describe the bug in your commit message
- Include steps to reproduce in the PR description
- Test the fix thoroughly
- Consider adding checks to prevent similar bugs

## Testing

### Manual Testing Checklist

Before submitting a PR, test:

- [ ] Docker build completes successfully
- [ ] All services start with `docker compose up`
- [ ] Web UI is accessible at http://localhost:8501
- [ ] PDF upload works correctly
- [ ] Document processing completes without errors
- [ ] Chat functionality returns relevant answers
- [ ] Error handling works properly
- [ ] Logs don't show unexpected errors

### Testing the Build

```bash
# Test the build
./test.sh

# Or manually
docker compose build --no-cache
docker compose up -d
docker compose logs -f
```

## Commit Guidelines

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat: Add support for DOCX files

Add functionality to process DOCX documents in addition 
to PDFs. Includes text extraction and chunking.

Closes #123
```

```
fix: Resolve Ollama connection timeout

Increase connection timeout and add retry logic for 
Ollama service initialization.

Fixes #456
```

## Pull Request Process

1. **Update documentation**: Ensure README and guides are updated
2. **Test thoroughly**: Test all affected functionality
3. **Create PR**: Submit a pull request with a clear description
4. **Describe changes**: Explain what changed and why
5. **Link issues**: Reference related issues
6. **Wait for review**: Address any feedback

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How was this tested?

## Checklist
- [ ] Code follows project style
- [ ] Documentation updated
- [ ] Changes tested locally
- [ ] Docker build works
- [ ] No breaking changes (or documented)
```

## Areas for Contribution

We welcome contributions in these areas:

### High Priority
- [ ] Support for additional file formats (DOCX, TXT, etc.)
- [ ] Improved error handling and user feedback
- [ ] Performance optimizations
- [ ] Better documentation
- [ ] Unit and integration tests

### Medium Priority
- [ ] Additional LLM model support
- [ ] Custom prompt templates
- [ ] Export chat history
- [ ] Multi-language support
- [ ] Mobile-responsive UI improvements

### Nice to Have
- [ ] User authentication
- [ ] Multi-user support
- [ ] Advanced search filters
- [ ] Document organization/folders
- [ ] Batch document processing
- [ ] API endpoints

## Architecture Overview

Understanding the architecture helps with contributions:

```
app.py
├── PDF Processing
│   ├── Text extraction (PyPDF2)
│   └── Text chunking (LangChain)
├── Vector Store
│   ├── Embeddings (Sentence Transformers)
│   └── Storage (ChromaDB)
├── LLM Integration
│   ├── Ollama connection
│   └── QA Chain (LangChain)
└── UI
    ├── Streamlit interface
    ├── File upload
    └── Chat interface
```

## Code Structure

```python
# Main sections in app.py:

1. Configuration & Imports
2. Session State Initialization
3. Helper Functions
   - check_ollama_connection()
   - extract_text_from_pdf()
   - create_vector_store()
   - setup_qa_chain()
4. Main UI Function
   - Sidebar (document upload)
   - Chat interface
   - Message history
```

## Adding New Features

### Example: Adding DOCX Support

1. **Add dependency** to `requirements.txt`:
   ```
   python-docx==0.8.11
   ```

2. **Add extraction function** in `app.py`:
   ```python
   from docx import Document
   
   def extract_text_from_docx(docx_file):
       doc = Document(docx_file)
       text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
       return text
   ```

3. **Update file uploader**:
   ```python
   uploaded_files = st.file_uploader(
       "Upload files",
       type=['pdf', 'docx'],  # Add 'docx'
       accept_multiple_files=True
   )
   ```

4. **Update processing logic**:
   ```python
   if file_path.suffix == '.pdf':
       text = extract_text_from_pdf(uploaded_file)
   elif file_path.suffix == '.docx':
       text = extract_text_from_docx(uploaded_file)
   ```

5. **Test thoroughly**
6. **Update documentation**
7. **Submit PR**

## Documentation

When contributing, update relevant documentation:

- **README.md**: Project overview, features, setup
- **USER_GUIDE.md**: User-facing instructions
- **QUICKSTART.md**: Quick start guide
- **EXAMPLES.md**: Usage examples
- **CONTRIBUTING.md**: This file

## Questions?

- Open an issue for bugs or feature requests
- Start a discussion for questions or ideas
- Check existing issues before creating new ones

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Assume good intentions
- Help others learn

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- GitHub contributors page

Thank you for contributing! 🎉
