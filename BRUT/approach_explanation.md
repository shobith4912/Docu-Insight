# Approach Explanation for Round 1B

## Overview

Our solution for Round 1B builds a comprehensive persona-driven document analysis system that extracts and ranks relevant sections from a collection of PDFs. The system leverages PyMuPDF for robust text extraction and DistilBERT (via Hugging Face Transformers) for sophisticated zero-shot classification to evaluate section relevance against user-defined personas and jobs-to-be-done.

## Methodology

### 1. PDF Text Extraction
- **Library**: PyMuPDF (fitz) for high-performance PDF parsing
- **Process**: Extract clean text from each page while preserving document structure
- **Optimization**: Batch processing of multiple documents with memory-efficient streaming
- **Error Handling**: Robust parsing that handles diverse PDF formats and encodings

### 2. Relevance Scoring with DistilBERT
- **Model**: facebook/bart-large-mnli for zero-shot classification
- **Approach**: Score page text against job description using natural language inference
- **Threshold**: 0.7 relevance threshold for section inclusion (tuned for precision)
- **Fallback**: Keyword-based scoring when transformer models unavailable

### 3. Section Title Extraction
- **Heuristics**: Intelligent extraction of meaningful section titles from text
- **Filtering**: Remove headers, footers, and metadata noise
- **Validation**: Length and content validation to ensure quality titles

### 4. Output Formatting and Ranking
- **Structure**: Comprehensive JSON output with metadata, sections, and subsections
- **Ranking**: Sections sorted by importance rank (relevance score)
- **Metadata**: Complete analysis provenance including timestamps and model information

## Technical Implementation

### Zero-Shot Classification Pipeline
```python
classifier = pipeline("zero-shot-classification", 
                     model="facebook/bart-large-mnli")
scores = classifier(text, candidate_labels=[job, "irrelevant"])
relevance_score = scores["scores"][0] if scores["labels"][0] == job else 0.0
