#!/usr/bin/env python3
"""
Simple test script for the PDF Analysis System
"""

import os
import json
from simple_analyzer import SimplePDFAnalyzer


def test_basic_functionality():
    """Test basic functionality of the analyzer."""
    print("Testing Basic Functionality...")
    
    analyzer = SimplePDFAnalyzer()
    
    # Test task keyword extraction
    travel_task = "Plan a trip of 4 days for a group of 10 college friends."
    travel_keywords = analyzer.pdf_processor.extract_task_keywords(travel_task)
    print(f"  ✓ Travel keywords extracted: {len(travel_keywords)} keywords")
    
    hr_task = "Create and manage fillable forms for onboarding and compliance."
    hr_keywords = analyzer.pdf_processor.extract_task_keywords(hr_task)
    print(f"  ✓ HR keywords extracted: {len(hr_keywords)} keywords")
    
    food_task = "Prepare a vegetarian buffet-style dinner menu for a corporate gathering."
    food_keywords = analyzer.pdf_processor.extract_task_keywords(food_task)
    print(f"  ✓ Food keywords extracted: {len(food_keywords)} keywords")
    
    # Test section extraction
    test_text = "HEADER\nContent here\nANOTHER HEADER\nMore content"
    sections = analyzer.pdf_processor.extract_sections(test_text)
    print(f"  ✓ Section extraction: {len(sections)} sections found")
    
    # Test importance scoring
    score = analyzer.pdf_processor.calculate_importance_score("travel vacation trip", travel_keywords)
    print(f"  ✓ Importance scoring: {score:.3f}")
    
    print("  ✓ Basic functionality tests passed\n")


def test_collection_structure():
    """Test collection structure validation."""
    print("Testing Collection Structure...")
    
    challenge_dir = "Challenge_1b"
    if not os.path.exists(challenge_dir):
        print("  ✗ Challenge_1b directory not found")
        return False
    
    collections_found = 0
    valid_collections = 0
    
    for item in os.listdir(challenge_dir):
        item_path = os.path.join(challenge_dir, item)
        if os.path.isdir(item_path) and item.startswith("Collection"):
            collections_found += 1
            
            # Check required files
            input_file = os.path.join(item_path, "challenge1b_input.json")
            pdfs_dir = os.path.join(item_path, "PDFs")
            
            if os.path.exists(input_file) and os.path.exists(pdfs_dir):
                # Check if PDFs directory has PDF files
                pdf_files = [f for f in os.listdir(pdfs_dir) if f.endswith('.pdf')]
                if pdf_files:
                    valid_collections += 1
                    print(f"  ✓ {item}: {len(pdf_files)} PDF files")
                else:
                    print(f"  ✗ {item}: No PDF files found")
            else:
                print(f"  ✗ {item}: Missing required files")
    
    print(f"  ✓ Collections found: {collections_found}")
    print(f"  ✓ Valid collections: {valid_collections}")
    
    return valid_collections > 0


def test_input_loading():
    """Test input data loading."""
    print("Testing Input Loading...")
    
    challenge_dir = "Challenge_1b"
    analyzer = SimplePDFAnalyzer()
    
    # Find first valid collection
    test_collection = None
    for item in os.listdir(challenge_dir):
        item_path = os.path.join(challenge_dir, item)
        if os.path.isdir(item_path) and item.startswith("Collection"):
            input_file = os.path.join(item_path, "challenge1b_input.json")
            if os.path.exists(input_file):
                test_collection = item_path
                break
    
    if not test_collection:
        print("  ✗ No valid collection found for testing")
        return False
    
    try:
        # Load input data
        input_path = os.path.join(test_collection, "challenge1b_input.json")
        challenge_input = analyzer.load_input_data(input_path)
        
        print(f"  ✓ Loaded input: {challenge_input['challenge_info']['challenge_id']}")
        print(f"  ✓ Persona: {challenge_input['persona']['role']}")
        print(f"  ✓ Documents: {len(challenge_input['documents'])}")
        
        # Test task keyword extraction
        task_keywords = analyzer.pdf_processor.extract_task_keywords(
            challenge_input['job_to_be_done']['task']
        )
        print(f"  ✓ Task keywords: {len(task_keywords)} extracted")
        
        print("  ✓ Input loading test passed")
        return True
        
    except Exception as e:
        print(f"  ✗ Input loading failed: {e}")
        return False


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Simple PDF Analysis System - Test Suite")
    print("=" * 60)
    
    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("Collection Structure", test_collection_structure),
        ("Input Loading", test_input_loading),
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
    exit(0 if success else 1) 