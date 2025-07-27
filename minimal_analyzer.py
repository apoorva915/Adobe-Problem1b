#!/usr/bin/env python3
"""
Minimal PDF Analysis System
Uses only PyPDF2 to avoid dependency issues
"""

import os
import json
import re
from typing import List, Dict, Optional
from datetime import datetime
import PyPDF2


class MinimalPDFProcessor:
    def __init__(self):
        # Simple stopwords for text processing
        self.stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 
            'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'will', 'with',
            'i', 'you', 'your', 'we', 'they', 'them', 'this', 'these', 'those', 'but', 'or',
            'if', 'then', 'else', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each',
            'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
            'same', 'so', 'than', 'too', 'very', 'can', 'will', 'just', 'should', 'now'
        }
    
    def extract_text_from_pdf(self, pdf_path: str) -> Dict[int, str]:
        """Extract text from PDF with page numbers using PyPDF2."""
        text_by_page = {}
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    text = page.extract_text()
                    if text and text.strip():
                        text_by_page[page_num] = text.strip()
        except Exception as e:
            print(f"PyPDF2 failed for {pdf_path}: {e}")
                
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
    
    def extract_task_keywords(self, task: str) -> List[str]:
        """Extract relevant keywords from the task description."""
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
    
    def calculate_importance_score(self, section_content: str, task_keywords: List[str]) -> float:
        """Calculate importance score based on task relevance."""
        if not section_content or not task_keywords:
            return 0.0
        
        # Preprocess content
        processed_content = re.sub(r'[^a-zA-Z0-9\s]', ' ', section_content.lower())
        content_words = processed_content.split()
        
        # Count keyword matches
        keyword_matches = 0
        for keyword in task_keywords:
            keyword_lower = keyword.lower()
            for word in content_words:
                if keyword_lower in word or word in keyword_lower:
                    keyword_matches += 1
        
        # Calculate score
        if content_words:
            tf_score = keyword_matches / len(content_words)
            length_bonus = min(len(content_words) / 100, 0.5)
            return tf_score + length_bonus
        
        return 0.0
    
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
            sentences = re.split(r'[.!?]+', text)
            if sentences:
                refined_text = ""
                for sentence in sentences:
                    if len(refined_text + sentence) <= max_length:
                        refined_text += sentence + " "
                    else:
                        break
                return refined_text.strip()
        
        return text


class MinimalPDFAnalyzer:
    def __init__(self, output_dir: str = "output"):
        self.pdf_processor = MinimalPDFProcessor()
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
    
    def load_input_data(self, input_file_path: str) -> Dict:
        """Load input data from JSON file."""
        try:
            with open(input_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Failed to load input data from {input_file_path}: {e}")
            raise
    
    def process_collection(self, collection_path: str, input_file: str = "challenge1b_input.json") -> Dict:
        """Process a complete collection of PDFs and generate analysis output."""
        print(f"Processing collection: {collection_path}")
        
        # Load input data
        input_path = os.path.join(collection_path, input_file)
        challenge_input = self.load_input_data(input_path)
        
        # Extract task keywords
        task_keywords = self.pdf_processor.extract_task_keywords(challenge_input['job_to_be_done']['task'])
        print(f"Extracted task keywords: {task_keywords}")
        
        # Process all documents
        all_sections = []
        all_subsection_analyses = []
        
        pdfs_dir = os.path.join(collection_path, "PDFs")
        
        for doc in challenge_input['documents']:
            pdf_path = os.path.join(pdfs_dir, doc['filename'])
            
            if not os.path.exists(pdf_path):
                print(f"PDF file not found: {pdf_path}")
                continue
            
            print(f"Processing: {doc['filename']}")
            
            # Extract text from PDF
            text_by_page = self.pdf_processor.extract_text_from_pdf(pdf_path)
            
            if not text_by_page:
                print(f"No text extracted from: {pdf_path}")
                continue
            
            # Process each page
            for page_num, page_text in text_by_page.items():
                # Extract sections from page
                sections = self.pdf_processor.extract_sections(page_text)
                
                # Rank sections by importance
                ranked_sections = self.pdf_processor.rank_sections(sections, task_keywords)
                
                # Add document and page information
                for section in ranked_sections:
                    section['document'] = doc['filename']
                    section['page_number'] = page_num
                
                all_sections.extend(ranked_sections)
                
                # Create subsection analyses for top sections
                for section in ranked_sections[:3]:  # Top 3 sections per page
                    refined_text = self.pdf_processor.refine_text_for_analysis(section['content'])
                    if refined_text:
                        all_subsection_analyses.append({
                            'document': doc['filename'],
                            'refined_text': refined_text,
                            'page_number': page_num
                        })
        
        # Sort all sections by importance score and take top ones
        all_sections.sort(key=lambda x: x.get('importance_score', 0), reverse=True)
        top_sections = all_sections[:10]  # Top 10 sections overall
        
        # Create extracted sections
        extracted_sections = []
        for i, section in enumerate(top_sections, 1):
            extracted_sections.append({
                "document": section['document'],
                "section_title": section['title'],
                "importance_rank": i,
                "page_number": section['page_number']
            })
        
        # Create metadata
        metadata = {
            "input_documents": [doc['filename'] for doc in challenge_input['documents']],
            "persona": challenge_input['persona']['role'],
            "job_to_be_done": challenge_input['job_to_be_done']['task'],
            "processing_timestamp": datetime.now().isoformat()
        }
        
        # Create subsection analyses (limit to top 5)
        subsection_analyses = []
        for analysis in all_subsection_analyses[:5]:
            subsection_analyses.append({
                "document": analysis['document'],
                "refined_text": analysis['refined_text'],
                "page_number": analysis['page_number']
            })
        
        # Create output
        output = {
            "metadata": metadata,
            "extracted_sections": extracted_sections,
            "subsection_analysis": subsection_analyses
        }
        
        print(f"Analysis complete. Found {len(extracted_sections)} sections and {len(subsection_analyses)} analyses.")
        return output
    
    def save_output(self, output: Dict, collection_name: str, output_file: str = "challenge1b_output.json"):
        """Save analysis output to JSON file in the output directory."""
        try:
            # Create collection-specific output directory
            collection_output_dir = os.path.join(self.output_dir, collection_name)
            os.makedirs(collection_output_dir, exist_ok=True)
            
            output_path = os.path.join(collection_output_dir, output_file)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=4, ensure_ascii=False, default=str)
            
            print(f"Output saved to: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Failed to save output to {output_path}: {e}")
            raise
    
    def analyze_collection(self, collection_path: str, input_file: str = "challenge1b_input.json", 
                          output_file: str = "challenge1b_output.json") -> str:
        """Complete analysis pipeline for a collection."""
        try:
            # Get collection name from path
            collection_name = os.path.basename(collection_path)
            
            # Process collection
            output = self.process_collection(collection_path, input_file)
            
            # Save output
            output_path = self.save_output(output, collection_name, output_file)
            
            return output_path
            
        except Exception as e:
            print(f"Analysis failed for collection {collection_path}: {e}")
            raise


def main():
    """Main function to run the analysis."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Minimal PDF Analysis System")
    parser.add_argument("--collection", type=str, help="Path to collection directory")
    parser.add_argument("--all", action="store_true", help="Analyze all collections")
    parser.add_argument("--list", action="store_true", help="List available collections")
    parser.add_argument("--output-dir", type=str, default="output", help="Output directory for results")
    
    args = parser.parse_args()
    
    analyzer = MinimalPDFAnalyzer(output_dir=args.output_dir)
    
    if args.list:
        # List collections
        challenge_dir = "Challenge_1b"
        if os.path.exists(challenge_dir):
            print(f"\nAvailable collections in '{challenge_dir}':")
            print("-" * 50)
            
            for item in os.listdir(challenge_dir):
                item_path = os.path.join(challenge_dir, item)
                if os.path.isdir(item_path) and item.startswith("Collection"):
                    input_file = os.path.join(item_path, "challenge1b_input.json")
                    pdfs_dir = os.path.join(item_path, "PDFs")
                    
                    status = "✓" if os.path.exists(input_file) and os.path.exists(pdfs_dir) else "✗"
                    print(f"{status} {item}")
                    
                    if os.path.exists(pdfs_dir):
                        pdf_count = len([f for f in os.listdir(pdfs_dir) if f.endswith('.pdf')])
                        print(f"    PDFs: {pdf_count} files")
                    print()
        else:
            print(f"Challenge directory not found: {challenge_dir}")
    
    elif args.all:
        # Analyze all collections
        challenge_dir = "Challenge_1b"
        if not os.path.exists(challenge_dir):
            print(f"Challenge directory not found: {challenge_dir}")
            return
        
        collections = []
        for item in os.listdir(challenge_dir):
            item_path = os.path.join(challenge_dir, item)
            if os.path.isdir(item_path) and item.startswith("Collection"):
                input_file = os.path.join(item_path, "challenge1b_input.json")
                pdfs_dir = os.path.join(item_path, "PDFs")
                
                if os.path.exists(input_file) and os.path.exists(pdfs_dir):
                    collections.append(item_path)
        
        print(f"Found {len(collections)} collections to process")
        print(f"Output will be saved to: {args.output_dir}/")
        
        for collection_path in collections:
            try:
                print(f"\nProcessing: {os.path.basename(collection_path)}")
                output_path = analyzer.analyze_collection(collection_path)
                print(f"✓ Completed: {output_path}")
            except Exception as e:
                print(f"✗ Failed: {e}")
    
    elif args.collection:
        # Analyze specific collection
        try:
            output_path = analyzer.analyze_collection(args.collection)
            print(f"Analysis completed: {output_path}")
        except Exception as e:
            print(f"Analysis failed: {e}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main() 