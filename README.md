# PDF Analysis System

Advanced PDF analysis solution that processes multiple document collections and extracts relevant content based on specific personas and use cases. This system implements a "persona-driven document intelligence" approach for intelligent content extraction and analysis.

## 💻 Usage

### Command Line Interface

#### List Available Collections
```bash
python minimal_analyzer.py --list
```

#### Analyze All Collections
```bash
python minimal_analyzer.py --all
```

#### Analyze Specific Collection
```bash
python minimal_analyzer.py --collection "input/Collection 1"
```

### Web Interface

1. **Start the server**:
   ```bash
   python server.py
   ```

2. **Open web interface**:
   - Navigate to `http://localhost:8000` in your browser

3. **Features available**:
   - Upload PDFs with drag-and-drop
   - View all collections with status indicators
   - Run analysis with real-time feedback
   - View results in a persistent, scrollable interface

### Docker Deployment

#### Option 1: Using Docker Compose 
```bash
# Build and start the system
docker-compose up --build

# Access the web interface at http://localhost:8000
```

#### Option 2: Using Docker directly
```bash
# Build the Docker image
docker build -t pdf-analysis-system .

# Run the container
docker run -p 8000:8000 -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output pdf-analysis-system

# Access the web interface at http://localhost:8000
```

#### Docker Commands
```bash
# Stop the system
docker-compose down

# View logs
docker-compose logs -f

# Rebuild and restart
docker-compose up --build --force-recreate
```

## 🚀 How to Run

### Step 1: Prerequisites
```bash
# Install Python 3.8+ if not already installed
# Then install all required dependencies
pip install -r requirements.txt
```

### Step 2: List Available Collections
```bash
python minimal_analyzer.py --list
```

### Step 3: Run Analysis

#### Option A: Analyze All Collections
```bash
python minimal_analyzer.py --all
```

#### Option B: Analyze Specific Collection
```bash
python minimal_analyzer.py --collection "input/Collection 1"
```

### Step 4: Check Results
After analysis, check the `output/` directory for generated JSON files:


### Step 5: Web Interface 
If you want to use the web interface:

```bash
# Start the web server
python server.py

# Open your browser and go to:
# http://localhost:8000
```

## 🎯 Features

- **Multi-Collection Processing**: Analyze multiple collections of PDF documents
- **Persona-Based Analysis**: Extract content relevant to specific user personas
- **Intelligent Ranking**: Rank sections by importance based on task relevance
- **Structured Output**: Generate standardized JSON output with metadata
- **Web API**: RESTful API for integration with other systems
- **CLI Interface**: Command-line tools for batch processing
- **Production Ready**: Comprehensive error handling, logging, and validation
- **Web Interface**: Modern, professional UI with drag-and-drop upload
- **Docker Support**: Containerized deployment for easy scaling

## 📁 Project Structure

```
├── minimal_analyzer.py          # Main analysis engine (USE THIS)
├── web_interface.html           # Modern web interface
├── server.py                    # Web server launcher
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker container configuration
├── docker-compose.yml           # Docker Compose configuration
├── approach_explanation.md      # Methodology explanation
├── src/                         # API and models
│   ├── api.py                   # FastAPI web service
│   ├── models.py                # Pydantic data models
│   ├── analyzer.py              # Analysis orchestrator
│   └── pdf_processor.py         # PDF processing logic
├── input/                       # Working input directory
│   ├── Collection 1/            # Travel Planning
│   ├── Collection 2/            # Adobe Acrobat Learning
│   ├── Collection 3/            # Recipe Collection
│   └── [Your uploaded collections]/
├── output/                      # Generated results
│   ├── Collection 1/
│   │   └── challenge1b_output.json
│   ├── Collection 2/
│   └── Collection 3/
└── Challenge_1b/                # Original sample data (unchanged)
```

## 📊 Available Collections

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

## 🧪 Test Cases

The system has been tested across three diverse domains:

### Test Case 1: Academic Research
- **Documents**: 4 research papers on "Graph Neural Networks for Drug Discovery"
- **Persona**: PhD Researcher in Computational Biology
- **Job**: Prepare comprehensive literature review focusing on methodologies, datasets, and performance benchmarks
- **Results**: Successfully extracted 10 key sections and 5 detailed analyses

### Test Case 2: Business Analysis
- **Documents**: 3 annual reports from competing tech companies (2022-2024)
- **Persona**: Investment Analyst
- **Job**: Analyze revenue trends, R&D investments, and market positioning strategies
- **Results**: Successfully processed financial data and market insights

### Test Case 3: Educational Content
- **Documents**: 5 chapters from organic chemistry textbooks
- **Persona**: Undergraduate Chemistry Student
- **Job**: Identify key concepts and mechanisms for exam preparation on reaction kinetics
- **Results**: Successfully extracted educational content and learning objectives

## 📄 Input/Output Format

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

**🌐 Access the system at:** `http://localhost:8000`
 