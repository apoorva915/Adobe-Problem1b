#!/usr/bin/env python3
"""
Script to create test PDF files from text content for the test cases.
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import os

def create_pdf_from_text(text_content, output_path):
    """Create a PDF file from text content."""
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    # Set font and size
    c.setFont("Helvetica", 12)
    
    # Starting position
    y = height - 1 * inch
    line_height = 14
    
    # Split text into lines
    lines = text_content.split('\n')
    
    for line in lines:
        if y < 1 * inch:  # Start new page if near bottom
            c.showPage()
            c.setFont("Helvetica", 12)
            y = height - 1 * inch
        
        # Handle different line types
        if line.strip().startswith('Tech Company') or line.strip().startswith('Executive Summary:') or line.strip().startswith('Abstract:'):
            c.setFont("Helvetica-Bold", 14)
            c.drawString(1 * inch, y, line.strip())
            y -= line_height + 5
            c.setFont("Helvetica", 12)
        elif line.strip().startswith('-') or line.strip().startswith('•'):
            c.drawString(1.2 * inch, y, line.strip())
            y -= line_height
        elif line.strip().startswith('1.') or line.strip().startswith('2.') or line.strip().startswith('3.') or line.strip().startswith('4.') or line.strip().startswith('5.'):
            c.setFont("Helvetica-Bold", 12)
            c.drawString(1 * inch, y, line.strip())
            y -= line_height
            c.setFont("Helvetica", 12)
        else:
            c.drawString(1 * inch, y, line.strip())
            y -= line_height
    
    c.save()
    print(f"Created PDF: {output_path}")

def main():
    """Create PDF files for all test cases."""
    
    # Test Case 1 - Academic Research
    test_case_1_dir = "input/Test Case 1 - Academic Research/PDFs"
    
    # GNN Drug Discovery Methodology
    gnn_content = """Graph Neural Networks for Drug Discovery: Novel Methodologies

Abstract:
This paper presents novel graph neural network architectures specifically designed for molecular property prediction in drug discovery applications. We introduce a hierarchical attention mechanism that captures both local and global molecular features, achieving state-of-the-art performance on benchmark datasets.

Introduction:
Drug discovery is a complex process that requires understanding of molecular structures and their interactions. Graph Neural Networks (GNNs) have emerged as powerful tools for learning molecular representations due to their ability to capture structural information.

Methodology:
Our approach combines:
• Graph Convolutional Networks (GCN) for local feature extraction
• Attention mechanisms for global molecular understanding
• Hierarchical pooling for multi-scale feature aggregation

Results:
• 15% improvement over baseline GNN models
• 92% accuracy on molecular property prediction
• Reduced computational complexity by 40%

Conclusion:
The proposed methodology demonstrates significant improvements in drug discovery applications, providing a robust framework for molecular property prediction."""
    
    create_pdf_from_text(gnn_content, os.path.join(test_case_1_dir, "GNN_Drug_Discovery_Methodology_2023.pdf"))
    
    # Datasets Study
    datasets_content = """Comparative Analysis of Drug Discovery Datasets

Abstract:
This study provides a comprehensive comparison of datasets commonly used in drug discovery research, evaluating their characteristics, limitations, and suitability for different machine learning approaches.

Introduction:
The quality and characteristics of datasets significantly impact the performance of machine learning models in drug discovery. Understanding dataset properties is crucial for developing robust models.

Dataset Analysis:

1. ChEMBL Database:
   • 2.3 million compounds
   • 13,000 targets
   • High-quality bioactivity data
   • Standardized molecular representations

2. PubChem Database:
   • 111 million compounds
   • Diverse chemical space
   • Multiple bioactivity assays
   • Rich metadata

3. BindingDB:
   • 1.6 million binding data points
   • Protein-ligand interactions
   • High-resolution structures
   • Kinetic parameters

Evaluation Metrics:
• Data quality: Completeness and accuracy
• Chemical diversity: Structural variety
• Biological relevance: Target coverage
• Standardization: Format consistency

Conclusion:
ChEMBL provides the best balance of quality and size for most drug discovery applications, while PubChem offers the broadest chemical space coverage."""
    
    create_pdf_from_text(datasets_content, os.path.join(test_case_1_dir, "Drug_Discovery_Datasets_Comparative_Study.pdf"))
    
    # Performance Benchmarks
    benchmarks_content = """Performance Benchmarks for GNN Models in Drug Discovery

Abstract:
This paper presents comprehensive performance benchmarks comparing different Graph Neural Network architectures on standard drug discovery tasks, providing insights into model selection and optimization strategies.

Introduction:
With the proliferation of GNN architectures, systematic benchmarking is essential for guiding model selection in drug discovery applications.

Benchmark Tasks:

1. Molecular Property Prediction:
   • Solubility prediction
   • Toxicity classification
   • Bioactivity prediction
   • ADMET properties

2. Model Architectures Tested:
   • Graph Convolutional Networks (GCN)
   • Graph Attention Networks (GAT)
   • GraphSAGE
   • Graph Transformer Networks

Performance Results:

GCN Performance:
• Solubility: 0.89 AUC
• Toxicity: 0.92 AUC
• Bioactivity: 0.87 AUC

GAT Performance:
• Solubility: 0.91 AUC
• Toxicity: 0.94 AUC
• Bioactivity: 0.89 AUC

GraphSAGE Performance:
• Solubility: 0.88 AUC
• Toxicity: 0.91 AUC
• Bioactivity: 0.86 AUC

Key Findings:
• GAT consistently outperforms other architectures
• Attention mechanisms improve performance by 2-3%
• Computational cost scales with attention complexity
• Ensemble methods provide additional 1-2% improvement

Conclusion:
GAT models provide the best performance-cost trade-off for most drug discovery applications, with attention mechanisms being crucial for capturing complex molecular interactions."""
    
    create_pdf_from_text(benchmarks_content, os.path.join(test_case_1_dir, "GNN_Performance_Benchmarks_2024.pdf"))
    
    # Molecular Representation Review
    representation_content = """Molecular Representation Methods in Graph Neural Networks: A Comprehensive Review

Abstract:
This review provides a systematic analysis of molecular representation methods used in Graph Neural Networks, covering traditional approaches and recent advances in molecular encoding strategies.

Introduction:
Molecular representation is fundamental to the success of machine learning approaches in drug discovery. The choice of representation method significantly impacts model performance and interpretability.

Representation Methods:

1. SMILES Strings:
   • Linear text representation
   • Widely used in cheminformatics
   • Limited structural information
   • Sequence-based processing

2. Molecular Fingerprints:
   • Binary feature vectors
   • Capture structural patterns
   • Fast similarity calculations
   • Limited interpretability

3. Graph Representations:
   • Atoms as nodes, bonds as edges
   • Preserves structural information
   • Natural for GNN processing
   • Rich feature encoding

4. 3D Conformational Representations:
   • Spatial atomic coordinates
   • Captures molecular geometry
   • Computationally expensive
   • High information content

Advanced Methods:

1. Learned Representations:
   • Autoencoder-based encoding
   • Task-specific optimization
   • Continuous vector spaces
   • Transfer learning capabilities

2. Multi-modal Representations:
   • Combining multiple encodings
   • Complementary information
   • Improved robustness
   • Higher computational cost

Evaluation Criteria:
• Representation completeness
• Computational efficiency
• Interpretability
• Transfer learning potential

Conclusion:
Graph-based representations provide the best balance of structural information and computational efficiency for GNN applications in drug discovery, with learned representations showing promise for specific tasks."""
    
    create_pdf_from_text(representation_content, os.path.join(test_case_1_dir, "Molecular_Representation_GNN_Review.pdf"))
    
    print("Created all PDF files for Test Case 1 - Academic Research")
    
    # Test Case 2 - Business Analysis
    test_case_2_dir = "input/Test Case 2 - Business Analysis/PDFs"
    
    # Tech Company A Annual Report 2022
    company_a_content = """Tech Company A - Annual Report 2022

Executive Summary:
Tech Company A achieved strong financial performance in 2022, with revenue growth of 18% year-over-year and significant investments in research and development to maintain competitive advantage in the technology sector.

Financial Performance:

Revenue Analysis:
• Total Revenue: $12.5 billion (18% increase from 2021)
• Cloud Services: $4.2 billion (25% growth)
• Software Licenses: $3.8 billion (12% growth)
• Consulting Services: $2.1 billion (15% growth)
• Hardware Sales: $2.4 billion (8% growth)

R&D Investments:
• Total R&D Spending: $2.1 billion (16% of revenue)
• AI/ML Research: $800 million
• Cloud Infrastructure: $600 million
• Cybersecurity: $400 million
• Emerging Technologies: $300 million

Market Positioning:
• Market Share: 12% in enterprise software
• Customer Base: 15,000+ enterprise clients
• Geographic Presence: 45 countries
• Industry Focus: Financial services, healthcare, manufacturing

Strategic Initiatives:
1. Cloud-first transformation strategy
2. AI-powered product development
3. International market expansion
4. Strategic partnerships and acquisitions

Risk Factors:
• Intense competition from larger tech companies
• Rapid technological changes
• Regulatory compliance requirements
• Talent acquisition challenges

Outlook:
Company expects 15-20% revenue growth in 2023, driven by cloud services expansion and AI product launches."""
    
    create_pdf_from_text(company_a_content, os.path.join(test_case_2_dir, "Tech_Company_A_Annual_Report_2022.pdf"))
    
    # Tech Company B Annual Report 2023
    company_b_content = """Tech Company B - Annual Report 2023

Executive Summary:
Tech Company B demonstrated exceptional growth in 2023, achieving 22% revenue increase and expanding market presence through strategic acquisitions and innovative product development in the competitive technology landscape.

Financial Performance:

Revenue Analysis:
• Total Revenue: $18.7 billion (22% increase from 2022)
• SaaS Subscriptions: $8.5 billion (30% growth)
• Platform Services: $5.2 billion (18% growth)
• Professional Services: $3.1 billion (12% growth)
• Hardware & IoT: $1.9 billion (8% growth)

R&D Investments:
• Total R&D Spending: $3.2 billion (17% of revenue)
• Platform Development: $1.2 billion
• AI/ML Innovation: $900 million
• Security & Compliance: $600 million
• Edge Computing: $500 million

Market Positioning:
• Market Share: 18% in SaaS platforms
• Customer Base: 25,000+ organizations
• Geographic Reach: 60+ countries
• Industry Leadership: Retail, logistics, healthcare

Strategic Achievements:
1. Successful acquisition of three complementary startups
2. Launch of next-generation AI platform
3. Expansion into emerging markets
4. Strategic partnership with major cloud providers

Competitive Advantages:
• First-mover advantage in AI-powered analytics
• Strong customer retention (95% renewal rate)
• Scalable platform architecture
• Comprehensive security framework

Market Trends:
• Growing demand for AI-powered solutions
• Increased focus on data privacy and security
• Shift toward subscription-based models
• Rising importance of edge computing

Financial Outlook:
Projected revenue growth of 20-25% in 2024, supported by AI platform expansion and international market penetration."""
    
    create_pdf_from_text(company_b_content, os.path.join(test_case_2_dir, "Tech_Company_B_Annual_Report_2023.pdf"))
    
    # Tech Company C Annual Report 2024
    company_c_content = """Tech Company C - Annual Report 2024

Executive Summary:
Tech Company C achieved record-breaking performance in 2024, with 28% revenue growth and breakthrough innovations in quantum computing and advanced AI technologies, positioning the company as a leader in next-generation computing solutions.

Financial Performance:

Revenue Analysis:
• Total Revenue: $25.3 billion (28% increase from 2023)
• Quantum Computing Services: $6.8 billion (45% growth)
• Advanced AI Solutions: $8.2 billion (32% growth)
• Enterprise Software: $6.5 billion (18% growth)
• Research Services: $3.8 billion (15% growth)

R&D Investments:
• Total R&D Spending: $5.1 billion (20% of revenue)
• Quantum Computing Research: $2.1 billion
• AI/ML Development: $1.5 billion
• Advanced Algorithms: $800 million
• Hardware Innovation: $700 million

Market Positioning:
• Market Share: 25% in quantum computing services
• Customer Base: 35,000+ enterprises
• Global Presence: 80+ countries
• Industry Domination: Financial services, pharmaceuticals, aerospace

Innovation Highlights:
1. World's first commercial quantum computer
2. Breakthrough in quantum machine learning
3. Advanced AI language models
4. Revolutionary chip architecture

Strategic Investments:
• $2.5 billion in quantum computing infrastructure
• $1.8 billion in AI research facilities
• $1.2 billion in talent acquisition
• $800 million in strategic partnerships

Competitive Landscape:
• Leading quantum computing market
• Strong AI research capabilities
• Extensive patent portfolio (2,500+ patents)
• Strategic partnerships with universities

Market Opportunities:
• Growing demand for quantum computing
• AI integration across industries
• Edge computing expansion
• Cybersecurity solutions

Financial Projections:
Expected revenue growth of 30-35% in 2025, driven by quantum computing commercialization and AI platform expansion."""
    
    create_pdf_from_text(company_c_content, os.path.join(test_case_2_dir, "Tech_Company_C_Annual_Report_2024.pdf"))
    
    print("Created all PDF files for Test Case 2 - Business Analysis")

if __name__ == "__main__":
    main() 