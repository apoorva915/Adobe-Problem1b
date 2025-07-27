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
async def list_collections(base_path: str = "Challenge_1b"):
    """List available collections."""
    try:
        collections = []
        
        if os.path.exists(base_path):
            for item in os.listdir(base_path):
                item_path = os.path.join(base_path, item)
                if os.path.isdir(item_path) and item.startswith("Collection"):
                    # Check if it has required structure
                    input_file = os.path.join(item_path, "challenge1b_input.json")
                    pdfs_dir = os.path.join(item_path, "PDFs")
                    
                    if os.path.exists(input_file) and os.path.exists(pdfs_dir):
                        collections.append({
                            "name": item,
                            "path": item_path,
                            "has_input": True,
                            "has_pdfs": True
                        })
        
        return {
            "collections": collections,
            "total": len(collections)
        }
        
    except Exception as e:
        logger.error(f"Failed to list collections: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/collection/{collection_name}")
async def get_collection_info(collection_name: str, base_path: str = "Challenge_1b"):
    """Get detailed information about a specific collection."""
    try:
        collection_path = os.path.join(base_path, collection_name)
        
        if not os.path.exists(collection_path):
            raise HTTPException(status_code=404, detail="Collection not found")
        
        # Load input data
        input_file = os.path.join(collection_path, "challenge1b_input.json")
        if os.path.exists(input_file):
            with open(input_file, 'r') as f:
                import json
                input_data = json.load(f)
        else:
            input_data = None
        
        # Count PDF files
        pdfs_dir = os.path.join(collection_path, "PDFs")
        pdf_count = 0
        if os.path.exists(pdfs_dir):
            pdf_count = len([f for f in os.listdir(pdfs_dir) if f.endswith('.pdf')])
        
        return {
            "name": collection_name,
            "path": collection_path,
            "input_data": input_data,
            "pdf_count": pdf_count,
            "has_output": os.path.exists(os.path.join(collection_path, "challenge1b_output.json"))
        }
        
    except Exception as e:
        logger.error(f"Failed to get collection info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/results/{collection_name}")
async def get_analysis_results(collection_name: str, base_path: str = "output"):
    """Get analysis results for a specific collection."""
    try:
        # Check in output directory first
        output_file = os.path.join(base_path, collection_name, "challenge1b_output.json")
        
        if not os.path.exists(output_file):
            # Fallback to collection directory
            output_file = os.path.join("Challenge_1b", collection_name, "challenge1b_output.json")
        
        if not os.path.exists(output_file):
            raise HTTPException(status_code=404, detail="Analysis results not found")
        
        with open(output_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        return {
            "collection": collection_name,
            "results": results,
            "output_file": output_file
        }
        
    except Exception as e:
        logger.error(f"Failed to get analysis results: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 