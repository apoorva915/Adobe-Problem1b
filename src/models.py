from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ChallengeInfo(BaseModel):
    challenge_id: str
    test_case_name: str
    description: Optional[str] = None


class Document(BaseModel):
    filename: str
    title: str


class Persona(BaseModel):
    role: str


class JobToBeDone(BaseModel):
    task: str


class ChallengeInput(BaseModel):
    challenge_info: ChallengeInfo
    documents: List[Document]
    persona: Persona
    job_to_be_done: JobToBeDone


class ExtractedSection(BaseModel):
    document: str
    section_title: str
    importance_rank: int
    page_number: int


class SubsectionAnalysis(BaseModel):
    document: str
    refined_text: str
    page_number: int


class Metadata(BaseModel):
    input_documents: List[str]
    persona: str
    job_to_be_done: str
    processing_timestamp: datetime = Field(default_factory=datetime.now)


class ChallengeOutput(BaseModel):
    metadata: Metadata
    extracted_sections: List[ExtractedSection]
    subsection_analysis: List[SubsectionAnalysis]


class AnalysisRequest(BaseModel):
    collection_path: str
    input_file: str = "challenge1b_input.json"
    output_file: str = "challenge1b_output.json"


class AnalysisResponse(BaseModel):
    success: bool
    message: str
    output_path: Optional[str] = None
    error: Optional[str] = None 