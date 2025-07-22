import fitz  # PyMuPDF
import json
import os
import logging
from typing import Dict, List, Any

def extract_outline(pdf_path: str) -> Dict[str, Any]:
    """
    Round 1A: Extract structured outline from PDF using font-based heuristics
    
    Font size analysis:
    - >14pt + bold = H1
    - >12pt = H2  
    - >10pt = H3
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Dictionary with title and outline structure
    """
    try:
        doc = fitz.open(pdf_path)
        
        # Extract title from metadata or use filename
        title = doc.metadata.get("title", "")
        if not title:
            title = os.path.basename(pdf_path).replace(".pdf", "")
        
        outline = []
        
        # Process each page
        for page_num in range(doc.page_count):
            page = doc[page_num]
            blocks = page.get_text("dict")["blocks"]
            
            for block in blocks:
                if "lines" not in block:
                    continue
                
                for line in block["lines"]:
                    if not line["spans"]:
                        continue
                    
                    # Get text and font properties from first span
                    span = line["spans"][0]
                    text = span["text"].strip()
                    font_size = span["size"]
                    flags = span["flags"]
                    
                    # Skip empty text or very short text
                    if len(text) < 3:
                        continue
                    
                    # Determine heading level based on font size and style
                    level = None
                    is_bold = flags & 16  # Bold flag
                    
                    if font_size > 14 and is_bold:
                        level = "H1"
                    elif font_size > 12:
                        level = "H2"
                    elif font_size > 10:
                        level = "H3"
                    
                    if level:
                        outline.append({
                            "level": level,
                            "text": text,
                            "page": page_num + 1,
                            "font_size": round(font_size, 2),
                            "is_bold": bool(is_bold)
                        })
        
        doc.close()
        
        # Remove duplicates while preserving order
        seen = set()
        unique_outline = []
        for item in outline:
            key = (item["level"], item["text"], item["page"])
            if key not in seen:
                seen.add(key)
                unique_outline.append(item)
        
        result = {
            "title": title,
            "outline": unique_outline,
            "total_pages": doc.page_count,
            "metadata": {
                "extraction_method": "font_based_heuristics",
                "font_thresholds": {
                    "H1": ">14pt + bold",
                    "H2": ">12pt",
                    "H3": ">10pt"
                }
            }
        }
        
        logging.info(f"Extracted {len(unique_outline)} headings from {doc.page_count} pages")
        return result
        
    except Exception as e:
        logging.error(f"Error extracting outline from {pdf_path}: {str(e)}")
        raise Exception(f"PDF outline extraction failed: {str(e)}")

def process_pdfs(input_dir: str, output_dir: str) -> None:
    """
    Process multiple PDFs in a directory and save outlines as JSON files
    
    Args:
        input_dir: Directory containing PDF files
        output_dir: Directory to save JSON outline files
    """
    os.makedirs(output_dir, exist_ok=True)
    
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        logging.warning(f"No PDF files found in {input_dir}")
        return
    
    for filename in pdf_files:
        try:
            pdf_path = os.path.join(input_dir, filename)
            result = extract_outline(pdf_path)
            
            # Save outline as JSON
            output_filename = filename.replace(".pdf", "_outline.json")
            output_path = os.path.join(output_dir, output_filename)
            
            with open(output_path, "w", encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            logging.info(f"Processed {filename} -> {output_filename}")
            
        except Exception as e:
            logging.error(f"Failed to process {filename}: {str(e)}")
            continue

if __name__ == "__main__":
    # Test the extraction function
    test_input = "input"
    test_output = "output"
    
    if os.path.exists(test_input):
        process_pdfs(test_input, test_output)
    else:
        print(f"Input directory {test_input} does not exist")
