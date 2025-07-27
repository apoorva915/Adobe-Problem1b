import os
import json
from typing import List, Dict, Optional
from pathlib import Path
from loguru import logger

from .models import ChallengeInput, ChallengeOutput, Metadata, ExtractedSection, SubsectionAnalysis
from .pdf_processor import PDFProcessor


class PDFAnalyzer:
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        
    def load_input_data(self, input_file_path: str) -> ChallengeInput:
        """Load and validate input data from JSON file."""
        try:
            with open(input_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return ChallengeInput(**data)
        except Exception as e:
            logger.error(f"Failed to load input data from {input_file_path}: {e}")
            raise
    
    def process_collection(self, collection_path: str, input_file: str = "challenge1b_input.json") -> ChallengeOutput:
        """Process a complete collection of PDFs and generate analysis output."""
        logger.info(f"Processing collection: {collection_path}")
        
        # Load input data
        input_path = os.path.join(collection_path, input_file)
        challenge_input = self.load_input_data(input_path)
        
        # Extract task keywords
        task_keywords = self.pdf_processor.extract_task_keywords(challenge_input.job_to_be_done.task)
        logger.info(f"Extracted task keywords: {task_keywords}")
        
        # Process all documents
        all_sections = []
        all_subsection_analyses = []
        
        pdfs_dir = os.path.join(collection_path, "PDFs")
        
        for doc in challenge_input.documents:
            pdf_path = os.path.join(pdfs_dir, doc.filename)
            
            if not os.path.exists(pdf_path):
                logger.warning(f"PDF file not found: {pdf_path}")
                continue
            
            # Extract text from PDF
            text_by_page = self.pdf_processor.extract_text_from_pdf(pdf_path)
            
            if not text_by_page:
                logger.warning(f"No text extracted from: {pdf_path}")
                continue
            
            # Process each page
            for page_num, page_text in text_by_page.items():
                # Extract sections from page
                sections = self.pdf_processor.extract_sections(page_text)
                
                # Rank sections by importance
                ranked_sections = self.pdf_processor.rank_sections(sections, task_keywords)
                
                # Add document and page information
                for section in ranked_sections:
                    section['document'] = doc.filename
                    section['page_number'] = page_num
                
                all_sections.extend(ranked_sections)
                
                # Create subsection analyses for top sections
                for section in ranked_sections[:3]:  # Top 3 sections per page
                    refined_text = self.pdf_processor.refine_text_for_analysis(section['content'])
                    if refined_text:
                        all_subsection_analyses.append({
                            'document': doc.filename,
                            'refined_text': refined_text,
                            'page_number': page_num
                        })
        
        # Sort all sections by importance score and take top ones
        all_sections.sort(key=lambda x: x.get('importance_score', 0), reverse=True)
        top_sections = all_sections[:10]  # Top 10 sections overall
        
        # Create extracted sections
        extracted_sections = []
        for i, section in enumerate(top_sections, 1):
            extracted_sections.append(ExtractedSection(
                document=section['document'],
                section_title=section['title'],
                importance_rank=i,
                page_number=section['page_number']
            ))
        
        # Create metadata
        metadata = Metadata(
            input_documents=[doc.filename for doc in challenge_input.documents],
            persona=challenge_input.persona.role,
            job_to_be_done=challenge_input.job_to_be_done.task
        )
        
        # Create subsection analyses (limit to top 5)
        subsection_analyses = []
        for analysis in all_subsection_analyses[:5]:
            subsection_analyses.append(SubsectionAnalysis(
                document=analysis['document'],
                refined_text=analysis['refined_text'],
                page_number=analysis['page_number']
            ))
        
        # Create output
        output = ChallengeOutput(
            metadata=metadata,
            extracted_sections=extracted_sections,
            subsection_analysis=subsection_analyses
        )
        
        logger.info(f"Analysis complete. Found {len(extracted_sections)} sections and {len(subsection_analyses)} analyses.")
        return output
    
    def save_output(self, output: ChallengeOutput, output_path: str):
        """Save analysis output to JSON file."""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Convert to dict and save
            output_dict = output.model_dump()
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_dict, f, indent=4, ensure_ascii=False, default=str)
            
            logger.info(f"Output saved to: {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to save output to {output_path}: {e}")
            raise
    
    def analyze_collection(self, collection_path: str, input_file: str = "challenge1b_input.json", 
                          output_file: str = "challenge1b_output.json") -> str:
        """Complete analysis pipeline for a collection."""
        try:
            # Process collection
            output = self.process_collection(collection_path, input_file)
            
            # Save output
            output_path = os.path.join(collection_path, output_file)
            self.save_output(output, output_path)
            
            return output_path
            
        except Exception as e:
            logger.error(f"Analysis failed for collection {collection_path}: {e}")
            raise 