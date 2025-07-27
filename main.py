#!/usr/bin/env python3
"""
PDF Analysis System - Main CLI Application
Advanced PDF analysis solution for multi-collection document processing
"""

import os
import sys
import argparse
import json
from pathlib import Path
from loguru import logger
from typing import List

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.analyzer import PDFAnalyzer
from src.models import AnalysisRequest


def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    log_level = "DEBUG" if verbose else "INFO"
    logger.remove()
    logger.add(
        sys.stderr,
        level=log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )


def analyze_single_collection(collection_path: str, verbose: bool = False) -> bool:
    """Analyze a single collection."""
    try:
        setup_logging(verbose)
        logger.info(f"Starting analysis of collection: {collection_path}")
        
        analyzer = PDFAnalyzer()
        output_path = analyzer.analyze_collection(collection_path)
        
        logger.success(f"Analysis completed successfully!")
        logger.info(f"Output saved to: {output_path}")
        
        return True
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        return False


def analyze_all_collections(base_path: str = "Challenge_1b", verbose: bool = False) -> dict:
    """Analyze all collections in the base path."""
    setup_logging(verbose)
    logger.info(f"Starting batch analysis of all collections in: {base_path}")
    
    if not os.path.exists(base_path):
        logger.error(f"Base path not found: {base_path}")
        return {"success": False, "error": "Base path not found"}
    
    analyzer = PDFAnalyzer()
    results = {
        "total_collections": 0,
        "successful": 0,
        "failed": 0,
        "results": []
    }
    
    # Find all collection directories
    collections = []
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        if os.path.isdir(item_path) and item.startswith("Collection"):
            input_file = os.path.join(item_path, "challenge1b_input.json")
            pdfs_dir = os.path.join(item_path, "PDFs")
            
            if os.path.exists(input_file) and os.path.exists(pdfs_dir):
                collections.append(item_path)
    
    results["total_collections"] = len(collections)
    logger.info(f"Found {len(collections)} collections to process")
    
    # Process each collection
    for collection_path in collections:
        try:
            logger.info(f"Processing: {os.path.basename(collection_path)}")
            
            output_path = analyzer.analyze_collection(collection_path)
            
            results["successful"] += 1
            results["results"].append({
                "collection": os.path.basename(collection_path),
                "success": True,
                "output_path": output_path
            })
            
            logger.success(f"✓ {os.path.basename(collection_path)} completed")
            
        except Exception as e:
            results["failed"] += 1
            results["results"].append({
                "collection": os.path.basename(collection_path),
                "success": False,
                "error": str(e)
            })
            
            logger.error(f"✗ {os.path.basename(collection_path)} failed: {e}")
    
    # Summary
    logger.info(f"Batch analysis complete!")
    logger.info(f"Total: {results['total_collections']}")
    logger.info(f"Successful: {results['successful']}")
    logger.info(f"Failed: {results['failed']}")
    
    return results


def list_collections(base_path: str = "Challenge_1b"):
    """List all available collections."""
    if not os.path.exists(base_path):
        print(f"Base path not found: {base_path}")
        return
    
    print(f"\nAvailable collections in '{base_path}':")
    print("-" * 50)
    
    collections_found = False
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        if os.path.isdir(item_path) and item.startswith("Collection"):
            input_file = os.path.join(item_path, "challenge1b_input.json")
            pdfs_dir = os.path.join(item_path, "PDFs")
            
            status = "✓" if os.path.exists(input_file) and os.path.exists(pdfs_dir) else "✗"
            print(f"{status} {item}")
            
            if os.path.exists(input_file):
                try:
                    with open(input_file, 'r') as f:
                        data = json.load(f)
                        challenge_id = data.get('challenge_info', {}).get('challenge_id', 'N/A')
                        persona = data.get('persona', {}).get('role', 'N/A')
                        print(f"    Challenge ID: {challenge_id}")
                        print(f"    Persona: {persona}")
                except:
                    pass
            
            if os.path.exists(pdfs_dir):
                pdf_count = len([f for f in os.listdir(pdfs_dir) if f.endswith('.pdf')])
                print(f"    PDFs: {pdf_count} files")
            
            print()
            collections_found = True
    
    if not collections_found:
        print("No collections found.")


def validate_collection(collection_path: str) -> bool:
    """Validate that a collection has the required structure."""
    if not os.path.exists(collection_path):
        print(f"Collection path not found: {collection_path}")
        return False
    
    input_file = os.path.join(collection_path, "challenge1b_input.json")
    pdfs_dir = os.path.join(collection_path, "PDFs")
    
    if not os.path.exists(input_file):
        print(f"Input file not found: {input_file}")
        return False
    
    if not os.path.exists(pdfs_dir):
        print(f"PDFs directory not found: {pdfs_dir}")
        return False
    
    # Check if there are PDF files
    pdf_files = [f for f in os.listdir(pdfs_dir) if f.endswith('.pdf')]
    if not pdf_files:
        print(f"No PDF files found in: {pdfs_dir}")
        return False
    
    print(f"✓ Collection validated successfully")
    print(f"  - Input file: {input_file}")
    print(f"  - PDFs directory: {pdfs_dir}")
    print(f"  - PDF files: {len(pdf_files)}")
    
    return True


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="PDF Analysis System - Advanced PDF analysis for multi-collection document processing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze all collections
  python main.py --all

  # Analyze a specific collection
  python main.py --collection "Challenge_1b/Collection 1"

  # List available collections
  python main.py --list

  # Validate a collection structure
  python main.py --validate "Challenge_1b/Collection 1"

  # Run with verbose logging
  python main.py --all --verbose
        """
    )
    
    parser.add_argument(
        "--all", 
        action="store_true",
        help="Analyze all collections in Challenge_1b directory"
    )
    
    parser.add_argument(
        "--collection", 
        type=str,
        help="Analyze a specific collection by path"
    )
    
    parser.add_argument(
        "--list", 
        action="store_true",
        help="List all available collections"
    )
    
    parser.add_argument(
        "--validate", 
        type=str,
        help="Validate a collection structure"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--base-path",
        type=str,
        default="Challenge_1b",
        help="Base path for collections (default: Challenge_1b)"
    )
    
    args = parser.parse_args()
    
    # Handle different commands
    if args.list:
        list_collections(args.base_path)
        return
    
    if args.validate:
        validate_collection(args.validate)
        return
    
    if args.all:
        results = analyze_all_collections(args.base_path, args.verbose)
        if not results.get("success", True):
            sys.exit(1)
        return
    
    if args.collection:
        success = analyze_single_collection(args.collection, args.verbose)
        if not success:
            sys.exit(1)
        return
    
    # If no specific command, show help
    parser.print_help()


if __name__ == "__main__":
    main() 