# Adobe Hackathon 2025: PDF Processing System

## Overview

This is a complete offline PDF processing system built for the Adobe India Hackathon 2025. The application provides two main capabilities:
- **Round 1A**: Extract structured outlines from PDFs using font-based analysis (FULLY OFFLINE)
- **Round 1B**: Analyze multiple PDFs for persona-driven insights using AI classification or keyword fallback (FULLY OFFLINE)

The system works completely offline with Flask backend and static web frontend. Current status: FULLY FUNCTIONAL with keyword-based analysis fallback.

## User Preferences

Preferred communication style: Simple, everyday language.
Priority: Complete offline functionality without internet dependency.

## System Architecture

### Backend Architecture
- **Framework**: Flask web application with CORS enabled
- **PDF Processing**: PyMuPDF (fitz) for text extraction and font analysis
- **AI Analysis**: DistilBERT (facebook/bart-large-mnli) for zero-shot classification with fallback to keyword matching
- **File Handling**: Local file system with input/output directories
- **API Design**: RESTful endpoints for upload, analysis, and utility functions

### Frontend Architecture
- **Type**: Static web application (vanilla JavaScript + Bootstrap)
- **UI Framework**: Bootstrap 5 with dark theme
- **Styling**: Custom CSS with Font Awesome icons
- **Interaction**: Event-driven JavaScript for file handling and API communication

## Key Components

### PDF Processing Engine (`pdf_processor.py`)
- **Purpose**: Implements Round 1A outline extraction
- **Method**: Font-based heuristics (>14pt+bold=H1, >12pt=H2, >10pt=H3)
- **Output**: Structured JSON with hierarchical outline

### Document Analyzer (`doc_analyzer.py`)
- **Purpose**: Implements Round 1B persona-driven analysis
- **AI Model**: DistilBERT for zero-shot classification
- **Threshold**: 0.7 relevance score for section inclusion
- **Fallback**: Keyword-based matching when transformers unavailable

### Flask API (`app.py`)
- **Endpoints**:
  - `POST /upload` - PDF outline extraction
  - `POST /analyze` - Multi-document persona analysis
  - `POST /clear` - File cleanup
  - `GET /health` - Health check
- **Security**: Session management and CORS configuration

### Web Interface (`static/`)
- **Main Page**: `index.html` with responsive Bootstrap layout
- **JavaScript**: `app.js` handles file uploads and API interactions
- **Styling**: `style.css` provides custom outline visualization

## Data Flow

### Round 1A Flow
1. User uploads PDF via web interface
2. File saved to `input/` directory
3. `extract_outline()` processes PDF using font analysis
4. Structured outline returned as JSON
5. Frontend displays hierarchical outline with visual indicators

### Round 1B Flow
1. User uploads multiple PDFs and provides persona/job description
2. Files processed through `analyze_documents()`
3. DistilBERT classifies content relevance against job description
4. Sections ranked by importance with 0.7+ threshold
5. Comprehensive analysis results returned with metadata

## External Dependencies

### Python Backend
- **PyMuPDF**: PDF text extraction and font analysis
- **Transformers**: Hugging Face library for DistilBERT model
- **Flask**: Web framework with CORS support
- **Standard Libraries**: os, json, logging, datetime

### Frontend
- **Bootstrap 5**: UI framework with dark theme
- **Font Awesome**: Icon library
- **Vanilla JavaScript**: No framework dependencies

### AI Model
- **facebook/bart-large-mnli**: Pre-trained model for zero-shot classification
- **Offline Capability**: Models cached for offline execution

## Deployment Strategy

### Local Development
- Flask development server on default port
- Static files served from `static/` directory
- Input/output directories auto-created

### Container Support
- Dockerfile provided for AMD64 architecture
- Requirements.txt for Python dependencies
- Environment variable configuration for secrets

### File Structure
```
/
├── app.py              # Flask API server
├── pdf_processor.py    # Round 1A implementation
├── doc_analyzer.py     # Round 1B implementation
├── static/             # Frontend files
│   ├── index.html
│   ├── app.js
│   └── style.css
├── input/              # Uploaded PDFs
├── output/             # Analysis results
└── requirements.txt    # Python dependencies
```

### Error Handling
- Graceful fallback when AI models unavailable
- File validation and sanitization
- Comprehensive logging and status feedback
- User-friendly error messages in web interface