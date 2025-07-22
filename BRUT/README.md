# Adobe India Hackathon 2025: Connecting the Dots

## Overview

This project addresses Rounds 1A and 1B of the Adobe India Hackathon 2025, building an intelligent PDF processing system. The solution includes a Flask backend for PDF processing and analysis, and a responsive web frontend for user interaction.

### Features

- **Round 1A**: Extract structured outlines (title, H1, H2, H3 headings) from PDFs using font-based heuristics
- **Round 1B**: Analyze multiple PDFs to extract and rank sections based on persona-driven insights using DistilBERT
- **Web Interface**: Responsive React-style frontend with Bootstrap styling
- **Offline Capability**: Complete offline execution with pre-cached models
- **Real-time Processing**: Live feedback and progress indicators

## Architecture

### Backend (Flask)
- **PDF Processing**: PyMuPDF for text extraction and font analysis
- **NLP Analysis**: DistilBERT (facebook/bart-large-mnli) for zero-shot classification
- **API Endpoints**:
  - `POST /upload` - Upload PDF and extract outline (Round 1A)
  - `POST /analyze` - Analyze documents for persona insights (Round 1B)
  - `POST /clear` - Clear uploaded files
  - `GET /health` - Health check

### Frontend (Static Web App)
- **Modern UI**: Bootstrap 5 with dark theme support
- **Interactive Elements**: File upload, form validation, real-time results
- **Responsive Design**: Mobile-friendly interface
- **Progress Feedback**: Loading indicators and status messages

## Technical Approach

### Round 1A: Font-Based Outline Extraction
- Analyzes font size and style properties from PDF text blocks
- Heading classification: H1 (>14pt + bold), H2 (>12pt), H3 (>10pt)
- Extracts document metadata and page information
- Outputs structured JSON with title and hierarchical outline

### Round 1B: Persona-Driven Analysis
- Uses DistilBERT for zero-shot classification of document relevance
- Scores text sections against user-defined job descriptions
- Applies 0.7 relevance threshold for section inclusion
- Ranks sections by importance and extracts meaningful excerpts
- Fallback keyword matching when transformers unavailable

## Installation & Usage

### Prerequisites
```bash
# Using pip
pip install flask flask-cors pymupdf transformers torch requests

# Or using uv (recommended)
uv sync
```

### Quick Start

1. **Clone the repository**
```bash
git clone <repository-url>
cd adobe-hackathon-2025-pdf-processor
```

2. **Install dependencies**
```bash
uv sync  # Recommended
# OR
pip install -r requirements.txt
```

3. **Start the application**
```bash
python main.py
```

4. **Open in browser**
Navigate to `http://localhost:5000`

## Usage

### Round 1A: Single PDF Outline Extraction
1. Select a PDF file in the "Round 1A" section
2. Click "Extract Outline" 
3. View the structured outline with heading hierarchy

### Round 1B: Multiple PDF Analysis
1. Select multiple PDF files in the "Round 1B" section  
2. Click "Upload PDFs for Analysis"
3. Enter persona (e.g., "PhD Researcher") and job description
4. Click "Analyze Documents" to get relevance-ranked results

## Offline Operation

This system works completely offline:
- ✅ PDF processing with PyMuPDF
- ✅ Font-based outline extraction  
- ✅ Keyword-based content analysis (fallback)
- ✅ DistilBERT analysis (when available)
- ✅ Web interface with Bootstrap styling

## Project Structure

```
/
├── app.py              # Flask API server
├── pdf_processor.py    # Round 1A implementation
├── doc_analyzer.py     # Round 1B implementation  
├── main.py            # Application entry point
├── static/            # Frontend files
│   ├── index.html     # Web interface
│   ├── app.js         # JavaScript functionality
│   └── style.css      # Custom styling
├── input/             # Uploaded PDFs
├── output/            # Analysis results
├── pyproject.toml     # Python dependencies
└── README.md          # This file
```

## API Endpoints

- `GET /` - Web interface
- `POST /upload` - Upload PDF for outline extraction
- `POST /analyze` - Analyze uploaded PDFs with persona
- `POST /clear` - Clear uploaded files
- `GET /health` - Health check

## Technology Stack

- **Backend**: Flask, PyMuPDF, Transformers (optional)
- **Frontend**: Vanilla JavaScript, Bootstrap 5
- **Analysis**: Font-based heuristics + DistilBERT/keyword fallback
- **Deployment**: Gunicorn WSGI server

## Contributing

This project was built for Adobe India Hackathon 2025. Feel free to fork and extend for your own use cases.

## License

MIT License - see LICENSE file for details.
