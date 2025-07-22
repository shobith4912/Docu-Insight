import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any
import fitz  # PyMuPDF

# Import transformers with fallback
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logging.warning("Transformers library not available. Using fallback analysis.")

def analyze_documents(input_dir: str, persona: str, job: str, output_path: str) -> None:
    """
    Round 1B: Analyze multiple PDFs for persona-driven insights using DistilBERT
    
    Uses zero-shot classification to rank content relevance with 0.7 threshold
    
    Args:
        input_dir: Directory containing PDF files
        persona: User persona (e.g., "PhD Researcher")
        job: Job to be done (e.g., "Prepare a literature review")
        output_path: Path to save analysis results
    """
    try:
        # Initialize classifier if transformers is available
        classifier = None
        if TRANSFORMERS_AVAILABLE:
            try:
                classifier = pipeline(
                    "zero-shot-classification",
                    model="facebook/bart-large-mnli",
                    device=-1  # Use CPU for compatibility
                )
                logging.info("DistilBERT classifier initialized successfully")
            except Exception as e:
                logging.warning(f"Failed to initialize classifier: {str(e)}")
                classifier = None
        else:
            classifier = None
        
        # Initialize results structure
        results = {
            "metadata": {
                "documents": [],
                "persona": persona,
                "job": job,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "analysis_method": "DistilBERT zero-shot classification" if classifier else "Fallback keyword matching",
                "relevance_threshold": 0.7
            },
            "sections": [],
            "subsections": []
        }
        
        # Get PDF files from input directory
        pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            raise Exception("No PDF files found in input directory")
        
        # Process each PDF
        for filename in pdf_files:
            try:
                pdf_path = os.path.join(input_dir, filename)
                doc = fitz.open(pdf_path)
                results["metadata"]["documents"].append(filename)
                
                logging.info(f"Analyzing {filename} ({doc.page_count} pages)")
                
                # Process each page
                for page_num in range(doc.page_count):
                    page = doc[page_num]
                    text = page.get_text("text").strip()
                    
                    if len(text) < 50:  # Skip pages with minimal content
                        continue
                    
                    # Analyze relevance
                    relevance_score = 0.0
                    
                    if classifier:
                        # Use DistilBERT for zero-shot classification
                        try:
                            scores = classifier(text[:1000], candidate_labels=[job, "irrelevant"])
                            relevance_score = scores["scores"][0] if scores["labels"][0] == job else 0.0
                        except Exception as e:
                            logging.warning(f"Classifier error on page {page_num + 1}: {str(e)}")
                            relevance_score = _fallback_relevance_score(text, job)
                    else:
                        # Fallback to keyword-based relevance
                        relevance_score = _fallback_relevance_score(text, job)
                    
                    # Include sections above threshold
                    if relevance_score > 0.7:
                        # Extract section title (first meaningful line)
                        section_title = _extract_section_title(text)
                        
                        results["sections"].append({
                            "document": filename,
                            "page_number": page_num + 1,
                            "section_title": section_title,
                            "importance_rank": round(relevance_score, 3),
                            "text_length": len(text)
                        })
                        
                        # Add subsection with refined text
                        results["subsections"].append({
                            "document": filename,
                            "page_number": page_num + 1,
                            "refined_text": text[:500] + "..." if len(text) > 500 else text,
                            "relevance_score": round(relevance_score, 3)
                        })
                
                doc.close()
                
            except Exception as e:
                logging.error(f"Error processing {filename}: {str(e)}")
                continue
        
        # Sort sections by importance rank (descending)
        results["sections"].sort(key=lambda x: x["importance_rank"], reverse=True)
        results["subsections"].sort(key=lambda x: x["relevance_score"], reverse=True)
        
        # Add summary statistics
        results["metadata"]["total_sections"] = len(results["sections"])
        results["metadata"]["total_subsections"] = len(results["subsections"])
        results["metadata"]["avg_relevance"] = (
            sum(s["importance_rank"] for s in results["sections"]) / len(results["sections"])
            if results["sections"] else 0.0
        )
        
        # Save results
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logging.info(f"Analysis complete. Found {len(results['sections'])} relevant sections.")
        
    except Exception as e:
        logging.error(f"Document analysis failed: {str(e)}")
        raise Exception(f"Document analysis failed: {str(e)}")

def _fallback_relevance_score(text: str, job: str) -> float:
    """
    Fallback relevance scoring using keyword matching
    Used when DistilBERT is not available
    """
    text_lower = text.lower()
    job_lower = job.lower()
    
    # Extract keywords from job description
    job_keywords = [word for word in job_lower.split() if len(word) > 3]
    
    # Count keyword matches
    matches = sum(1 for keyword in job_keywords if keyword in text_lower)
    
    # Calculate score based on keyword density
    if not job_keywords:
        return 0.0
    
    keyword_ratio = matches / len(job_keywords)
    
    # Additional scoring for research-related terms
    research_terms = ["research", "study", "analysis", "method", "result", "conclusion", 
                     "literature", "review", "survey", "experiment", "data", "finding"]
    research_matches = sum(1 for term in research_terms if term in text_lower)
    
    # Combine scores
    base_score = min(keyword_ratio * 0.8, 0.8)
    research_bonus = min(research_matches * 0.05, 0.2)
    
    return min(base_score + research_bonus, 1.0)

def _extract_section_title(text: str) -> str:
    """
    Extract a meaningful section title from text
    """
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if len(line) > 5 and len(line) < 100:
            # Check if it looks like a title (not too long, has meaningful content)
            if not line.startswith(('Figure', 'Table', 'Page', 'Copyright')):
                return line
    
    # Fallback to first 50 characters
    return text[:50].strip() + "..." if len(text) > 50 else text.strip()

if __name__ == "__main__":
    # Test the analysis function
    test_input = "input"
    test_output = "output/test_analysis.json"
    test_persona = "PhD Researcher"
    test_job = "Prepare a literature review"
    
    if os.path.exists(test_input):
        analyze_documents(test_input, test_persona, test_job, test_output)
        print(f"Analysis results saved to {test_output}")
    else:
        print(f"Input directory {test_input} does not exist")
