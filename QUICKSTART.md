# Quick Start Guide - PDF Analysis System

## Prerequisites

Make sure you have Python 3.8+ installed and the required packages:

```bash
pip install PyPDF2 pdfplumber loguru pydantic fastapi uvicorn
```

## Quick Test

1. **Test the system**:
   ```bash
   python test_simple.py
   ```

2. **List available collections**:
   ```bash
   python simple_analyzer.py --list
   ```

3. **Analyze a specific collection**:
   ```bash
   python simple_analyzer.py --collection "Challenge_1b/Collection 1"
   ```

4. **Analyze all collections**:
   ```bash
   python simple_analyzer.py --all
   ```

## Expected Output

### Test Results
```
============================================================
Simple PDF Analysis System - Test Suite
============================================================
Testing Basic Functionality...
  ✓ Travel keywords extracted: 15 keywords
  ✓ HR keywords extracted: 12 keywords
  ✓ Food keywords extracted: 12 keywords
  ✓ Section extraction: 2 sections found
  ✓ Importance scoring: 0.333
  ✓ Basic functionality tests passed

Testing Collection Structure...
  ✓ Collection 1: 7 PDF files
  ✓ Collection 2: 15 PDF files
  ✓ Collection 3: 9 PDF files
  ✓ Collections found: 3
  ✓ Valid collections: 3

Testing Input Loading...
  ✓ Loaded input: round_1b_002
  ✓ Persona: Travel Planner
  ✓ Documents: 7
  ✓ Task keywords: 15 extracted
  ✓ Input loading test passed

✓ Basic Functionality: PASSED
✓ Collection Structure: PASSED
✓ Input Loading: PASSED

============================================================
Test Results: 3/3 tests passed
🎉 All tests passed! System is ready to use.
```

### Collection Analysis Output
```
Processing collection: Challenge_1b/Collection 1
Extracted task keywords: ['visit', 'tour', 'vacation', 'arrange', 'restaurant', 'culture', 'prepare', 'trip', 'organize', 'city', 'plan', 'travel', 'explore', 'hotel', 'attraction', 'manage', 'holiday', 'activity', 'create']
Processing: South of France - Cities.pdf
Processing: South of France - Cuisine.pdf
Processing: South of France - History.pdf
Processing: South of France - Restaurants and Hotels.pdf
Processing: South of France - Things to Do.pdf
Processing: South of France - Tips and Tricks.pdf
Processing: South of France - Traditions and Culture.pdf
Analysis complete. Found 10 sections and 5 analyses.
Output saved to: output\Collection 1\challenge1b_output.json
Analysis completed: output\Collection 1\challenge1b_output.json
```

## Output Files

After analysis, you'll find `challenge1b_output.json` files in the `output/` directory, organized by collection name. The system preserves the original sample data and saves all results separately.

```json
{
    "metadata": {
        "input_documents": ["file1.pdf", "file2.pdf"],
        "persona": "Travel Planner",
        "job_to_be_done": "Plan a trip of 4 days for a group of 10 college friends.",
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

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure all required packages are installed
   ```bash
   pip install PyPDF2 pdfplumber loguru pydantic fastapi uvicorn
   ```

2. **PDF extraction fails**: Some PDFs might be image-based or password-protected
   - The system will try pdfplumber first, then fall back to PyPDF2
   - Check if PDFs are readable in a PDF viewer

3. **No collections found**: Ensure the `Challenge_1b` directory exists with proper structure
   ```
   Challenge_1b/
   ├── Collection 1/
   │   ├── challenge1b_input.json
   │   └── PDFs/
   │       ├── file1.pdf
   │       └── file2.pdf
   ```

### Performance

- **Processing speed**: ~1-2 seconds per PDF page
- **Memory usage**: Efficient for most PDF sizes
- **Output size**: Typically 10-50KB per collection

## Advanced Usage

### Web API (Optional)

If you want to use the web interface:

1. **Start the server**:
   ```bash
   python server.py
   ```

2. **Open web interface**:
   - Navigate to `http://localhost:8000` in your browser
   - Or open `web_interface.html` directly

3. **API endpoints**:
   - `GET /collections` - List collections
   - `POST /analyze` - Analyze a collection
   - `GET /health` - Health check

### Docker (Optional)

For containerized deployment:

```bash
# Build and run with Docker
docker-compose up --build

# Or build manually
docker build -t pdf-analysis-system .
docker run -p 8000:8000 pdf-analysis-system
```

## Next Steps

1. **Customize analysis**: Modify `simple_analyzer.py` to adjust:
   - Number of extracted sections (default: 10)
   - Number of subsection analyses (default: 5)
   - Text refinement length (default: 500 characters)

2. **Add new collections**: Create new directories in `Challenge_1b/` with:
   - `challenge1b_input.json` file
   - `PDFs/` directory containing PDF files

3. **Extend functionality**: The modular design allows easy extension of:
   - PDF processing methods
   - Analysis algorithms
   - Output formats

## Support

For issues:
1. Check the troubleshooting section above
2. Run `python test_simple.py` to verify system health
3. Check console output for detailed error messages 