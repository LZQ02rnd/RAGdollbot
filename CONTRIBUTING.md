# Contributing to RAGdollBot

Thank you for your interest in contributing to RAGdollBot! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Your environment (OS, Python version, etc.)
- Relevant logs or error messages

### Suggesting Enhancements

For feature requests or enhancements:
- Open an issue with a clear description
- Explain the use case and benefits
- Provide examples if possible

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/LZQ02rnd/RAGdollbot.git
   cd RAGdollbot
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clean, readable code
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   ```bash
   python test_setup.py
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

6. **Push and create a PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## Development Setup

1. **Clone and setup**
   ```bash
   git clone https://github.com/LZQ02rnd/RAGdollbot.git
   cd RAGdollbot
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your test credentials
   ```

3. **Run tests**
   ```bash
   python test_setup.py
   ```

## Code Style Guidelines

### Python Style
- Follow PEP 8 style guide
- Use descriptive variable names
- Add docstrings to functions and classes
- Keep functions focused and single-purpose

### Example:
```python
def process_document(file_path: str) -> List[Document]:
    """
    Process a document file and return chunks.
    
    Args:
        file_path: Path to the document file
        
    Returns:
        List of document chunks
    """
    # Implementation
    pass
```

### Documentation
- Update README.md for user-facing changes
- Update QUICKSTART.md if setup process changes
- Add inline comments for complex logic
- Update docstrings when changing function signatures

### Commit Messages
Use clear, descriptive commit messages:
- ✅ "Add support for .docx files in knowledge base"
- ✅ "Fix: Handle empty responses from OpenAI API"
- ✅ "Docs: Update installation instructions"
- ❌ "fix bug"
- ❌ "update"

## Project Structure

```
RAGdollbot/
├── bot.py              # Main bot implementation
├── rag_engine.py       # RAG processing logic
├── config.py           # Configuration management
├── setup.py            # Setup verification script
├── test_setup.py       # Component tests
├── requirements.txt    # Dependencies
├── knowledge_base/     # Documents for the bot
└── .env.example       # Example environment variables
```

## Areas for Contribution

### Priority Areas
1. **Additional document formats** (Word, Markdown, etc.)
2. **Improved error handling** and user feedback
3. **Performance optimizations** for large knowledge bases
4. **Additional commands** and features
5. **Better logging** and monitoring
6. **Unit and integration tests**

### Advanced Features (Ideas)
- Web interface for knowledge base management
- Support for multiple vector stores
- Fine-tuned model support
- Conversation memory/context
- Role-based access control
- Analytics dashboard

## Testing

Before submitting a PR:

1. Run the test suite:
   ```bash
   python test_setup.py
   ```

2. Test manually with a test Discord server

3. Verify documentation is up to date

## Questions?

- Open an issue for questions
- Check existing issues and PRs
- Review the documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to RAGdollBot! 🤖
