import os
import json
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pdf_processor import extract_outline
from doc_analyzer import analyze_documents

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, static_folder='static')
app.secret_key = os.environ.get("SESSION_SECRET", "adobe-hackathon-2025-secret")
CORS(app)

# Ensure directories exist
os.makedirs("input", exist_ok=True)
os.makedirs("output", exist_ok=True)

@app.route("/")
def index():
    """Serve the main application page"""
    return send_from_directory('static', 'index.html')

@app.route("/upload", methods=["POST"])
def upload_pdf():
    """
    Round 1A: Extract structured outline from uploaded PDF
    Analyzes font sizes and styles to identify headings (H1, H2, H3)
    """
    try:
        if 'pdf' not in request.files:
            return jsonify({"error": "No PDF file provided"}), 400
        
        file = request.files['pdf']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not (file.filename and file.filename.lower().endswith('.pdf')):
            return jsonify({"error": "File must be a PDF"}), 400
        
        # Save uploaded file
        filename = file.filename or "unknown.pdf"
        file_path = os.path.join("input", filename)
        file.save(file_path)
        
        # Extract outline using Round 1A logic
        result = extract_outline(file_path)
        
        app.logger.info(f"Successfully processed PDF: {filename}")
        return jsonify(result)
        
    except Exception as e:
        app.logger.error(f"Error processing PDF upload: {str(e)}")
        return jsonify({"error": f"PDF processing failed: {str(e)}"}), 500

@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Round 1B: Analyze multiple PDFs for persona-driven insights
    Uses DistilBERT for zero-shot classification to rank content relevance
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        persona = data.get("persona", "").strip()
        job = data.get("job", "").strip()
        
        if not persona or not job:
            return jsonify({"error": "Both persona and job fields are required"}), 400
        
        # Check if input directory has PDFs
        pdf_files = [f for f in os.listdir("input") if f.lower().endswith('.pdf')]
        if not pdf_files:
            return jsonify({"error": "No PDF files found in input directory. Please upload PDFs first."}), 400
        
        output_path = os.path.join("output", "analysis_output.json")
        
        # Perform Round 1B analysis
        analyze_documents("input", persona, job, output_path)
        
        # Return analysis results
        with open(output_path, "r") as f:
            results = json.load(f)
        
        app.logger.info(f"Successfully analyzed {len(pdf_files)} PDFs for persona: {persona}")
        return jsonify(results)
        
    except Exception as e:
        app.logger.error(f"Error during document analysis: {str(e)}")
        return jsonify({"error": f"Document analysis failed: {str(e)}"}), 500

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy", 
        "service": "Adobe Hackathon 2025 PDF Processor",
        "rounds": ["1A: Outline Extraction", "1B: Persona Analysis"]
    })

@app.route("/clear", methods=["POST"])
def clear_files():
    """Clear input and output directories"""
    try:
        # Clear input directory
        for filename in os.listdir("input"):
            if filename != ".gitkeep":
                os.remove(os.path.join("input", filename))
        
        # Clear output directory
        for filename in os.listdir("output"):
            if filename != ".gitkeep":
                os.remove(os.path.join("output", filename))
        
        return jsonify({"message": "Files cleared successfully"})
    except Exception as e:
        app.logger.error(f"Error clearing files: {str(e)}")
        return jsonify({"error": f"Failed to clear files: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
