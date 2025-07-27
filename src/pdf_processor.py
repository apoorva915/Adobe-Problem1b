import os
import json
import re
from typing import List, Dict, Tuple, Optional
from pathlib import Path
import PyPDF2
import pdfplumber
from loguru import logger

# Simple text processing functions (no NLTK dependency)
def simple_sent_tokenize(text: str) -> List[str]:
    """Simple sentence tokenization using regex."""
    sentences = re.split(r'[.!?]+', text)
    return [s.strip() for s in sentences if s.strip()]

def simple_word_tokenize(text: str) -> List[str]:
    """Simple word tokenization using regex."""
    words = re.findall(r'\b\w+\b', text.lower())
    return words

# Simple stopwords list
SIMPLE_STOPWORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 
    'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'will', 'with',
    'i', 'you', 'your', 'we', 'they', 'them', 'this', 'these', 'those', 'but', 'or',
    'if', 'then', 'else', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each',
    'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
    'same', 'so', 'than', 'too', 'very', 'can', 'will', 'just', 'should', 'now'
}


class PDFProcessor:
    def __init__(self):
        self.stop_words = SIMPLE_STOPWORDS
        
    def extract_text_from_pdf(self, pdf_path: str) -> Dict[int, str]:
        """Extract text from PDF with page numbers."""
        text_by_page = {}
        
        try:
            # Try pdfplumber first for better text extraction
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text and text.strip():
                        text_by_page[page_num] = text.strip()
                        
        except Exception as e:
            logger.warning(f"pdfplumber failed for {pdf_path}: {e}")
            # Fallback to PyPDF2
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page_num, page in enumerate(pdf_reader.pages, 1):
                        text = page.extract_text()
                        if text and text.strip():
                            text_by_page[page_num] = text.strip()
            except Exception as e2:
                logger.error(f"PyPDF2 also failed for {pdf_path}: {e2}")
                
        return text_by_page
    
    def extract_sections(self, text: str) -> List[Dict[str, str]]:
        """Extract sections from text based on headers and structure."""
        sections = []
        
        # Common section patterns
        section_patterns = [
            r'^([A-Z][A-Z\s&]+)$',  # ALL CAPS headers
            r'^(\d+\.\s+[A-Z][^.]*)$',  # Numbered sections
            r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)$',  # Title Case headers
            r'^([A-Z][^.]*:)$',  # Headers ending with colon
        ]
        
        lines = text.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if line is a section header
            is_header = False
            for pattern in section_patterns:
                if re.match(pattern, line):
                    # Save previous section if exists
                    if current_section and current_content:
                        sections.append({
                            'title': current_section,
                            'content': '\n'.join(current_content)
                        })
                    
                    current_section = line
                    current_content = []
                    is_header = True
                    break
            
            if not is_header and current_section:
                current_content.append(line)
        
        # Add the last section
        if current_section and current_content:
            sections.append({
                'title': current_section,
                'content': '\n'.join(current_content)
            })
        
        return sections
    
    def preprocess_text(self, text: str) -> str:
        """Preprocess text for analysis."""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def calculate_importance_score(self, section_content: str, task_keywords: List[str]) -> float:
        """Calculate importance score based on task relevance."""
        if not section_content or not task_keywords:
            return 0.0
        
        # Preprocess content
        processed_content = self.preprocess_text(section_content)
        
        # Count keyword matches
        keyword_matches = 0
        content_words = processed_content.split()
        
        for keyword in task_keywords:
            keyword_lower = keyword.lower()
            # Check for exact matches and partial matches
            for word in content_words:
                if keyword_lower in word or word in keyword_lower:
                    keyword_matches += 1
        
        # Calculate TF-IDF based score
        if content_words:
            tf_score = keyword_matches / len(content_words)
            # Add bonus for longer, more detailed sections
            length_bonus = min(len(content_words) / 100, 0.5)
            return tf_score + length_bonus
        
        return 0.0
    
    def extract_task_keywords(self, task: str) -> List[str]:
        """Extract relevant keywords from the task description."""
        # Remove common words and extract meaningful terms
        task_lower = task.lower()
        
        # Define task-specific keyword patterns
        travel_keywords = ['travel', 'trip', 'visit', 'explore', 'tour', 'vacation', 'holiday', 
                          'city', 'restaurant', 'hotel', 'activity', 'attraction', 'culture']
        hr_keywords = ['form', 'fillable', 'onboarding', 'compliance', 'document', 'signature',
                      'pdf', 'acrobat', 'create', 'manage', 'workflow']
        food_keywords = ['menu', 'recipe', 'cooking', 'food', 'meal', 'dinner', 'buffet',
                        'vegetarian', 'gluten-free', 'corporate', 'gathering']
        
        # Determine task type and extract relevant keywords
        keywords = []
        if any(word in task_lower for word in travel_keywords):
            keywords.extend(travel_keywords)
        if any(word in task_lower for word in hr_keywords):
            keywords.extend(hr_keywords)
        if any(word in task_lower for word in food_keywords):
            keywords.extend(food_keywords)
        
        # Add general task words
        general_keywords = ['plan', 'prepare', 'create', 'manage', 'organize', 'arrange']
        keywords.extend(general_keywords)
        
        return list(set(keywords))
    
    def rank_sections(self, sections: List[Dict], task_keywords: List[str]) -> List[Dict]:
        """Rank sections by importance score."""
        for section in sections:
            section['importance_score'] = self.calculate_importance_score(
                section['content'], task_keywords
            )
        
        # Sort by importance score (descending)
        ranked_sections = sorted(sections, key=lambda x: x['importance_score'], reverse=True)
        
        # Add importance rank
        for i, section in enumerate(ranked_sections, 1):
            section['importance_rank'] = i
        
        return ranked_sections
    
    def refine_text_for_analysis(self, text: str, max_length: int = 500) -> str:
        """Refine and summarize text for subsection analysis."""
        if not text:
            return ""
        
        # Clean up the text
        text = re.sub(r'\s+', ' ', text).strip()
        
        # If text is too long, try to extract the most relevant part
        if len(text) > max_length:
            sentences = simple_sent_tokenize(text)
            if sentences:
                # Take the first few sentences that fit within max_length
                refined_text = ""
                for sentence in sentences:
                    if len(refined_text + sentence) <= max_length:
                        refined_text += sentence + " "
                    else:
                        break
                return refined_text.strip()
        
        return text 