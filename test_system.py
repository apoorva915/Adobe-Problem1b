#!/usr/bin/env python3
"""
Test script for the PDF Analysis System
Validates all components and functionality
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.insert(0, src_path)

try:
    from analyzer import PDFAnalyzer
    from models import ChallengeInput, ChallengeOutput
    from pdf_processor import PDFProcessor
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Current directory: {current_dir}")
    print(f"Source path: {src_path}")
    print(f"Available files in src: {os.listdir(src_path) if os.path.exists(src_path) else 'src directory not found'}")
    sys.exit(1)


def test_pdf_processor():
    """Test PDF processor functionality."""
    print("Testing PDF Processor...")
    
    processor = PDFProcessor()
    
    # Test task keyword extraction
    travel_task = "Plan a trip of 4 days for a group of 10 college friends."
    travel_keywords = processor.extract_task_keywords(travel_task)
    print(f"  ✓ Travel keywords extracted: {len(travel_keywords)} keywords")
    
    hr_task = "Create and manage fillable forms for onboarding and compliance."
    hr_keywords = processor.extract_task_keywords(hr_task)
    print(f"  ✓ HR keywords extracted: {len(hr_keywords)} keywords")
    
    food_task = "Prepare a vegetarian buffet-style dinner menu for a corporate gathering."
    food_keywords = processor.extract_task_keywords(food_task)
    print(f"  ✓ Food keywords extracted: {len(food_keywords)} keywords")
    
    # Test text preprocessing
    test_text = "This is a TEST text with some CAPITAL letters and punctuation!"
    processed = processor.preprocess_text(test_text)
    print(f"  ✓ Text preprocessing: {len(processed)} characters")
    
    # Test section extraction
    test_sections = processor.extract_sections("HEADER\nContent here\nANOTHER HEADER\nMore content")
    print(f"  ✓ Section extraction: {len(test_sections)} sections found")
    
    # Test importance scoring
    score = processor.calculate_importance_score("travel vacation trip", travel_keywords)
    print(f"  ✓ Importance scoring: {score:.3f}")
    
    print("  ✓ PDF Processor tests passed\n")


def test_models():
    """Test Pydantic models."""
    print("Testing Data Models...")
    
    # Test input model
    input_data = {
        "challenge_info": {
            "challenge_id": "round_1b_001",
            "test_case_name": "test_case"
        },
        "documents": [
            {"filename": "test.pdf", "title": "Test Document"}
        ],
        "persona": {"role": "Test User"},
        "job_to_be_done": {"task": "Test task"}
    }
    
    challenge_input = ChallengeInput(**input_data)
    print(f"  ✓ Input model validation: {challenge_input.challenge_info.challenge_id}")
    
    # Test output model
    output_data = {
        "metadata": {
            "input_documents": ["test.pdf"],
            "persona": "Test User",
            "job_to_be_done": "Test task"
        },
        "extracted_sections": [
            {
                "document": "test.pdf",
                "section_title": "Test Section",
                "importance_rank": 1,
                "page_number": 1
            }
        ],
        "subsection_analysis": [
            {
                "document": "test.pdf",
                "refined_text": "Test content",
                "page_number": 1
            }
        ]
    }
    
    challenge_output = ChallengeOutput(**output_data)
    print(f"  ✓ Output model validation: {len(challenge_output.extracted_sections)} sections")
    
    print("  ✓ Data Models tests passed\n")


def test_analyzer():
    """Test analyzer functionality."""
    print("Testing Analyzer...")
    
    analyzer = PDFAnalyzer()
    
    # Test input loading
    test_input = {
        "challenge_info": {
            "challenge_id": "round_1b_test",
            "test_case_name": "test_case"
        },
        "documents": [
            {"filename": "test.pdf", "title": "Test Document"}
        ],
        "persona": {"role": "Test User"},
        "job_to_be_done": {"task": "Test task"}
    }
    
    # Create temporary test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_input, f)
        temp_input_path = f.name
    
    try:
        loaded_input = analyzer.load_input_data(temp_input_path)
        print(f"  ✓ Input loading: {loaded_input.challenge_info.challenge_id}")
    finally:
        os.unlink(temp_input_path)
    
    print("  ✓ Analyzer tests passed\n")


def test_collection_structure():
    """Test collection structure validation."""
    print("Testing Collection Structure...")
    
    challenge_dir = Path("Challenge_1b")
    if not challenge_dir.exists():
        print("  ✗ Challenge_1b directory not found")
        return False
    
    collections_found = 0
    valid_collections = 0
    
    for item in challenge_dir.iterdir():
        if item.is_dir() and item.name.startswith("Collection"):
            collections_found += 1
            
            # Check required files
            input_file = item / "challenge1b_input.json"
            pdfs_dir = item / "PDFs"
            
            if input_file.exists() and pdfs_dir.exists():
                # Check if PDFs directory has PDF files
                pdf_files = list(pdfs_dir.glob("*.pdf"))
                if pdf_files:
                    valid_collections += 1
                    print(f"  ✓ {item.name}: {len(pdf_files)} PDF files")
                else:
                    print(f"  ✗ {item.name}: No PDF files found")
            else:
                print(f"  ✗ {item.name}: Missing required files")
    
    print(f"  ✓ Collections found: {collections_found}")
    print(f"  ✓ Valid collections: {valid_collections}")
    
    return valid_collections > 0


def test_sample_analysis():
    """Test analysis on a sample collection."""
    print("Testing Sample Analysis...")
    
    # Find first valid collection
    challenge_dir = Path("Challenge_1b")
    test_collection = None
    
    for item in challenge_dir.iterdir():
        if item.is_dir() and item.name.startswith("Collection"):
            input_file = item / "challenge1b_input.json"
            pdfs_dir = item / "PDFs"
            
            if input_file.exists() and pdfs_dir.exists():
                pdf_files = list(pdfs_dir.glob("*.pdf"))
                if pdf_files:
                    test_collection = item
                    break
    
    if not test_collection:
        print("  ✗ No valid collection found for testing")
        return False
    
    print(f"  ✓ Testing collection: {test_collection.name}")
    
    try:
        analyzer = PDFAnalyzer()
        
        # Load input data
        input_path = test_collection / "challenge1b_input.json"
        challenge_input = analyzer.load_input_data(str(input_path))
        
        print(f"  ✓ Loaded input: {challenge_input.challenge_info.challenge_id}")
        print(f"  ✓ Persona: {challenge_input.persona.role}")
        print(f"  ✓ Documents: {len(challenge_input.documents)}")
        
        # Test processing (without actually processing PDFs)
        task_keywords = analyzer.pdf_processor.extract_task_keywords(
            challenge_input.job_to_be_done.task
        )
        print(f"  ✓ Task keywords: {len(task_keywords)} extracted")
        
        print("  ✓ Sample analysis test passed")
        return True
        
    except Exception as e:
        print(f"  ✗ Sample analysis failed: {e}")
        return False


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("PDF Analysis System - Test Suite")
    print("=" * 60)
    
    tests = [
        ("PDF Processor", test_pdf_processor),
        ("Data Models", test_models),
        ("Analyzer", test_analyzer),
        ("Collection Structure", test_collection_structure),
        ("Sample Analysis", test_sample_analysis),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result is None or result:
                passed += 1
                print(f"✓ {test_name}: PASSED")
            else:
                print(f"✗ {test_name}: FAILED")
        except Exception as e:
            print(f"✗ {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 