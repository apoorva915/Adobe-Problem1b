"""
Configuration settings for the PDF Analysis System
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
CHALLENGE_DIR = BASE_DIR / "Challenge_1b"

# Processing settings
MAX_SECTIONS_PER_PAGE = 3
MAX_TOTAL_SECTIONS = 10
MAX_SUBSECTION_ANALYSES = 5
MAX_TEXT_LENGTH = 500

# PDF processing settings
PDF_EXTRACTION_TIMEOUT = 30  # seconds
FALLBACK_TO_PYPDF2 = True

# Analysis settings
TFIDF_MAX_FEATURES = 1000
TFIDF_NGRAM_RANGE = (1, 2)
IMPORTANCE_SCORE_LENGTH_BONUS_MAX = 0.5

# Logging settings
LOG_LEVEL = "INFO"
LOG_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

# API settings
API_HOST = "0.0.0.0"
API_PORT = 8000
API_RELOAD = True

# Task-specific keywords for better analysis
TASK_KEYWORDS = {
    "travel": [
        "travel", "trip", "visit", "explore", "tour", "vacation", "holiday",
        "city", "restaurant", "hotel", "activity", "attraction", "culture",
        "beach", "coast", "adventure", "nightlife", "entertainment"
    ],
    "hr": [
        "form", "fillable", "onboarding", "compliance", "document", "signature",
        "pdf", "acrobat", "create", "manage", "workflow", "hr", "human resources",
        "employee", "process", "automation"
    ],
    "food": [
        "menu", "recipe", "cooking", "food", "meal", "dinner", "buffet",
        "vegetarian", "gluten-free", "corporate", "gathering", "ingredient",
        "preparation", "serving", "nutrition"
    ]
}

# Section extraction patterns
SECTION_PATTERNS = [
    r'^([A-Z][A-Z\s&]+)$',  # ALL CAPS headers
    r'^(\d+\.\s+[A-Z][^.]*)$',  # Numbered sections
    r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)$',  # Title Case headers
    r'^([A-Z][^.]*:)$',  # Headers ending with colon
    r'^([A-Z][A-Za-z\s]+)$',  # Mixed case headers
]

# File patterns
INPUT_FILE_PATTERN = "challenge1b_input.json"
OUTPUT_FILE_PATTERN = "challenge1b_output.json"
PDF_DIR_PATTERN = "PDFs"
COLLECTION_PATTERN = "Collection*"

# Validation settings
REQUIRED_INPUT_FIELDS = [
    "challenge_info",
    "documents", 
    "persona",
    "job_to_be_done"
]

REQUIRED_CHALLENGE_INFO_FIELDS = [
    "challenge_id",
    "test_case_name"
]

REQUIRED_DOCUMENT_FIELDS = [
    "filename",
    "title"
] 