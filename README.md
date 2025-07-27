# PDF Analysis System

Advanced PDF analysis solution that processes multiple document collections and extracts relevant content based on specific personas and use cases.

## Features

- **Multi-Collection Processing**: Analyze multiple collections of PDF documents
- **Persona-Based Analysis**: Extract content relevant to specific user personas
- **Intelligent Ranking**: Rank sections by importance based on task relevance
- **Structured Output**: Generate standardized JSON output with metadata
- **Web API**: RESTful API for integration with other systems
- **CLI Interface**: Command-line tools for batch processing
- **Production Ready**: Comprehensive error handling, logging, and validation

## Project Structure

```
├── src/
│   ├── __init__.py
│   ├── models.py          # Pydantic data models
│   ├── pdf_processor.py   # Core PDF processing logic
│   ├── analyzer.py        # Main analysis orchestrator
│   └── api.py            # FastAPI web service
├── Challenge_1b/         # Sample collections
│   ├── Collection 1/     # Travel Planning
│   ├── Collection 2/     # Adobe Acrobat Learning
│   └── Collection 3/     # Recipe Collection
├── main.py              # CLI application
├── server.py            # Web server launcher
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Problem-1b
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python main.py --list
   ```

## Usage

### Command Line Interface

#### List Available Collections
```bash
python main.py --list
```

#### Analyze All Collections
```bash
python main.py --all
```

#### Analyze Specific Collection
```bash
python main.py --collection "Challenge_1b/Collection 1"
```

#### Validate Collection Structure
```bash
python main.py --validate "Challenge_1b/Collection 1"
```

#### Verbose Logging
```bash
python main.py --all --verbose
```

### Web API

#### Start the Server
```bash
python server.py
```

The API will be available at `http://localhost:8000`

#### API Endpoints

- `GET /` - System information
- `GET /health` - Health check
- `GET /collections` - List available collections
- `GET /collection/{name}` - Get collection details
- `POST /analyze` - Analyze a single collection
- `POST /analyze-batch` - Analyze multiple collections

#### Example API Usage

```bash
# List collections
curl http://localhost:8000/collections

# Analyze a collection
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"collection_path": "Challenge_1b/Collection 1"}'
```

## Collections

### Collection 1: Travel Planning
- **Challenge ID**: round_1b_002
- **Persona**: Travel Planner
- **Task**: Plan a 4-day trip for 10 college friends to South of France
- **Documents**: 7 travel guides

### Collection 2: Adobe Acrobat Learning
- **Challenge ID**: round_1b_003
- **Persona**: HR Professional
- **Task**: Create and manage fillable forms for onboarding and compliance
- **Documents**: 15 Acrobat guides

### Collection 3: Recipe Collection
- **Challenge ID**: round_1b_001
- **Persona**: Food Contractor
- **Task**: Prepare vegetarian buffet-style dinner menu for corporate gathering
- **Documents**: 9 cooking guides

## Input/Output Format

### Input JSON Structure
```json
{
  "challenge_info": {
    "challenge_id": "round_1b_XXX",
    "test_case_name": "specific_test_case"
  },
  "documents": [{"filename": "doc.pdf", "title": "Title"}],
  "persona": {"role": "User Persona"},
  "job_to_be_done": {"task": "Use case description"}
}
```

### Output JSON Structure
```json
{
  "metadata": {
    "input_documents": ["list"],
    "persona": "User Persona",
    "job_to_be_done": "Task description",
    "processing_timestamp": "2025-01-XX..."
  },
  "extracted_sections": [
    {
      "document": "source.pdf",
      "section_title": "Title",
      "importance_rank": 1,
      "page_number": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "source.pdf",
      "refined_text": "Content",
      "page_number": 1
    }
  ]
}
```

## Technical Details

### PDF Processing
- Uses `pdfplumber` for primary text extraction
- Falls back to `PyPDF2` for compatibility
- Extracts text with page numbers for precise location tracking

### Content Analysis
- **Section Extraction**: Identifies headers and sections using regex patterns
- **Keyword Matching**: Task-specific keyword extraction and matching
- **Importance Scoring**: TF-IDF based scoring with length bonuses
- **Text Refinement**: Intelligent text summarization for analysis

### Machine Learning Features
- **TF-IDF Vectorization**: For content similarity and importance scoring
- **NLTK Integration**: For text preprocessing and tokenization
- **Cosine Similarity**: For content relevance calculations

### Error Handling
- Comprehensive exception handling at all levels
- Graceful fallbacks for PDF processing failures
- Detailed logging with configurable verbosity
- Input validation using Pydantic models

## Development

### Adding New Collections
1. Create a new directory in `Challenge_1b/`
2. Add `challenge1b_input.json` with proper structure
3. Create `PDFs/` subdirectory with PDF files
4. Run validation: `python main.py --validate "path/to/collection"`

### Extending Analysis
- Modify `pdf_processor.py` for new extraction methods
- Update `analyzer.py` for new analysis algorithms
- Add new endpoints in `api.py` for additional functionality

### Testing
```bash
# Test single collection
python main.py --collection "Challenge_1b/Collection 1" --verbose

# Test all collections
python main.py --all --verbose

# Test API
python server.py
# Then visit http://localhost:8000/docs for interactive API docs
```

## Performance

- **Processing Speed**: ~1-2 seconds per PDF page
- **Memory Usage**: Efficient streaming for large documents
- **Scalability**: Designed for batch processing of multiple collections
- **Concurrency**: FastAPI supports async processing for web requests

## Troubleshooting

### Common Issues

1. **PDF Text Extraction Fails**
   - Check if PDF is image-based (OCR may be needed)
   - Verify PDF is not password-protected
   - Try different PDF processing libraries

2. **Missing Dependencies**
   - Run `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

3. **Collection Validation Fails**
   - Verify directory structure matches expected format
   - Check file permissions
   - Ensure PDF files are readable

### Logs
- Use `--verbose` flag for detailed logging
- Check console output for error messages
- Logs include timestamps and function names for debugging

## License

This project is part of the Challenge 1b solution for advanced PDF analysis.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review logs with `--verbose` flag
3. Validate collection structure
4. Check API documentation at `/docs` when server is running 