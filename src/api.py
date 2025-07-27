from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import tempfile
import shutil
import json
from pathlib import Path
from loguru import logger

# Import the working minimal analyzer instead
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from minimal_analyzer import MinimalPDFAnalyzer

# Simple models for API
from pydantic import BaseModel
from typing import Optional

class AnalysisRequest(BaseModel):
    collection_path: str
    input_file: str = "challenge1b_input.json"
    output_file: str = "challenge1b_output.json"

class AnalysisResponse(BaseModel):
    success: bool
    message: str
    output_path: Optional[str] = None
    error: Optional[str] = None

app = FastAPI(
    title="PDF Analysis System",
    description="Advanced PDF analysis solution for multi-collection document processing",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize analyzer
analyzer = MinimalPDFAnalyzer()

# Mount static files for web interface
try:
    app.mount("/static", StaticFiles(directory="."), name="static")
except Exception as e:
    logger.warning(f"Could not mount static files: {e}")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the web interface."""
    try:
        with open("web_interface.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="""
        <html>
        <head><title>PDF Analysis System</title></head>
        <body>
            <h1>PDF Analysis System API</h1>
            <p>Web interface not found. Use API endpoints directly:</p>
            <ul>
                <li><a href="/health">Health Check</a></li>
                <li><a href="/collections">List Collections</a></li>
                <li><a href="/docs">API Documentation</a></li>
            </ul>
        </body>
        </html>
        """)


@app.get("/api")
async def api_info():
    """API information endpoint."""
    return {
        "message": "PDF Analysis System API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "collections": "/collections",
            "analyze": "/analyze",
            "analyze-batch": "/analyze-batch",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "pdf-analysis-system"}


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_collection(request: AnalysisRequest):
    """Analyze a collection of PDFs."""
    try:
        logger.info(f"Starting analysis for collection: {request.collection_path}")
        
        # Validate collection path exists
        if not os.path.exists(request.collection_path):
            raise HTTPException(
                status_code=404, 
                detail=f"Collection path not found: {request.collection_path}"
            )
        
        # Check if input file exists
        input_file_path = os.path.join(request.collection_path, request.input_file)
        if not os.path.exists(input_file_path):
            raise HTTPException(
                status_code=404,
                detail=f"Input file not found: {input_file_path}"
            )
        
        # Perform analysis
        output_path = analyzer.analyze_collection(
            collection_path=request.collection_path,
            input_file=request.input_file,
            output_file=request.output_file
        )
        
        return AnalysisResponse(
            success=True,
            message="Analysis completed successfully",
            output_path=output_path
        )
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        return AnalysisResponse(
            success=False,
            message="Analysis failed",
            error=str(e)
        )


@app.post("/analyze-batch")
async def analyze_batch_collections(collections: list[str]):
    """Analyze multiple collections in batch."""
    results = []
    
    for collection_path in collections:
        try:
            logger.info(f"Processing batch collection: {collection_path}")
            
            output_path = analyzer.analyze_collection(collection_path)
            
            results.append({
                "collection": collection_path,
                "success": True,
                "output_path": output_path
            })
            
        except Exception as e:
            logger.error(f"Batch analysis failed for {collection_path}: {e}")
            results.append({
                "collection": collection_path,
                "success": False,
                "error": str(e)
            })
    
    return {
        "batch_results": results,
        "total_collections": len(collections),
        "successful": len([r for r in results if r["success"]]),
        "failed": len([r for r in results if not r["success"]])
    }


@app.get("/collections")
async def list_collections(base_path: str = "input"):
    """List available collections."""
    try:
        collections = []
        
        if os.path.exists(base_path):
            for item in os.listdir(base_path):
                item_path = os.path.join(base_path, item)
                if os.path.isdir(item_path):
                    # Check if it has required structure
                    input_file = os.path.join(item_path, "challenge1b_input.json")
                    pdfs_dir = os.path.join(item_path, "PDFs")
                    
                    # Count PDF files
                    pdf_count = 0
                    if os.path.exists(pdfs_dir):
                        pdf_count = len([f for f in os.listdir(pdfs_dir) if f.endswith('.pdf')])
                    
                    # Check if collection has any content
                    has_input = os.path.exists(input_file)
                    has_pdfs = pdf_count > 0
                    
                    if has_input or has_pdfs:  # Include collections with either input or PDFs
                        collections.append({
                            "name": item,
                            "path": item_path,
                            "has_input": has_input,
                            "has_pdfs": has_pdfs,
                            "pdf_count": pdf_count,
                            "is_ready": has_input and has_pdfs
                        })
        
        # Sort collections: ready ones first, then by name
        collections.sort(key=lambda x: (not x["is_ready"], x["name"]))
        
        return {
            "collections": collections,
            "total": len(collections),
            "ready": len([c for c in collections if c["is_ready"]]),
            "incomplete": len([c for c in collections if not c["is_ready"]])
        }
        
    except Exception as e:
        logger.error(f"Failed to list collections: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/collection/{collection_name}")
async def get_collection_info(collection_name: str, base_path: str = "input"):
    """Get detailed information about a specific collection."""
    try:
        collection_path = os.path.join(base_path, collection_name)
        
        if not os.path.exists(collection_path):
            raise HTTPException(status_code=404, detail="Collection not found")
        
        # Load input data
        input_file = os.path.join(collection_path, "challenge1b_input.json")
        input_data = None
        if os.path.exists(input_file):
            with open(input_file, 'r') as f:
                input_data = json.load(f)
        
        # Count PDF files and get list
        pdfs_dir = os.path.join(collection_path, "PDFs")
        pdf_files = []
        pdf_count = 0
        if os.path.exists(pdfs_dir):
            pdf_files = [f for f in os.listdir(pdfs_dir) if f.endswith('.pdf')]
            pdf_count = len(pdf_files)
        
        # Check if output exists
        output_file = os.path.join("output", collection_name, "challenge1b_output.json")
        has_output = os.path.exists(output_file)
        
        return {
            "name": collection_name,
            "path": collection_path,
            "input_data": input_data,
            "pdf_files": pdf_files,
            "pdf_count": pdf_count,
            "has_output": has_output,
            "output_path": output_file if has_output else None,
            "is_ready": input_data is not None and pdf_count > 0
        }
        
    except Exception as e:
        logger.error(f"Failed to get collection info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...), collection_name: str = "New Collection"):
    """Upload a PDF file to a collection."""
    try:
        # Create collection directory if it doesn't exist
        collection_path = os.path.join("input", collection_name)
        pdfs_dir = os.path.join(collection_path, "PDFs")
        
        os.makedirs(pdfs_dir, exist_ok=True)
        
        # Save the uploaded file
        file_path = os.path.join(pdfs_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Create or update input file if it doesn't exist
        input_file = os.path.join(collection_path, "challenge1b_input.json")
        if not os.path.exists(input_file):
            # Get list of all PDF files in the collection
            pdf_files = []
            if os.path.exists(pdfs_dir):
                pdf_files = [f for f in os.listdir(pdfs_dir) if f.endswith('.pdf')]
            
            # Create sample input file
            sample_input = {
                "persona": {
                    "role": "Document Analyst",
                    "description": "Professional who analyzes documents for insights"
                },
                "job_to_be_done": {
                    "task": f"Analyze documents in {collection_name}",
                    "context": f"Collection of {len(pdf_files)} PDF documents"
                },
                "documents": [{"filename": pdf} for pdf in pdf_files]
            }
            
            with open(input_file, 'w') as f:
                json.dump(sample_input, f, indent=4)
        
        return {
            "success": True,
            "message": f"PDF uploaded successfully to {collection_name}",
            "file_path": file_path,
            "collection": collection_name,
            "input_created": not os.path.exists(input_file)
        }
        
    except Exception as e:
        logger.error(f"Failed to upload PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/create-collection")
async def create_collection(collection_name: str, description: str = ""):
    """Create a new collection directory."""
    try:
        collection_path = os.path.join("input", collection_name)
        
        if os.path.exists(collection_path):
            raise HTTPException(status_code=400, detail="Collection already exists")
        
        # Create collection structure
        os.makedirs(collection_path, exist_ok=True)
        os.makedirs(os.path.join(collection_path, "PDFs"), exist_ok=True)
        
        # Create sample input file
        sample_input = {
            "persona": {
                "role": "Document Analyst",
                "description": "Professional who analyzes documents for insights"
            },
            "job_to_be_done": {
                "task": f"Analyze documents in {collection_name}",
                "context": description
            },
            "documents": []
        }
        
        input_file = os.path.join(collection_path, "challenge1b_input.json")
        with open(input_file, 'w') as f:
            json.dump(sample_input, f, indent=4)
        
        return {
            "success": True,
            "message": f"Collection '{collection_name}' created successfully",
            "collection_path": collection_path
        }
        
    except Exception as e:
        logger.error(f"Failed to create collection: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/results/{collection_name}")
async def get_analysis_results(collection_name: str, base_path: str = "output"):
    """Get analysis results for a specific collection."""
    try:
        # Clean collection name (remove path prefixes)
        clean_name = collection_name
        if '\\' in collection_name:
            clean_name = collection_name.split('\\')[-1]
        elif '/' in collection_name:
            clean_name = collection_name.split('/')[-1]
        
        # Check in output directory first
        output_file = os.path.join(base_path, clean_name, "challenge1b_output.json")
        
        if not os.path.exists(output_file):
            # Fallback to collection directory
            output_file = os.path.join("Challenge_1b", clean_name, "challenge1b_output.json")
        
        if not os.path.exists(output_file):
            raise HTTPException(status_code=404, detail=f"Analysis results not found for {clean_name}")
        
        with open(output_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        return {
            "collection": clean_name,
            "results": results,
            "output_file": output_file
        }
        
    except Exception as e:
        logger.error(f"Failed to get analysis results: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 