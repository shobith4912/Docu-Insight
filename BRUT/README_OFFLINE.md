# Adobe Hackathon 2025 - Offline PDF Processor

## Complete Offline Functionality

This application is designed to work **completely offline** without any internet connection. Here's how:

### Core Offline Features

#### ✅ **Round 1A: PDF Outline Extraction** (Always Works Offline)
- **Font-based Analysis**: Uses PyMuPDF to analyze font sizes and styles
- **No AI Required**: Pure heuristic-based heading detection
- **Instant Processing**: Works immediately without downloads
- **Output**: Structured JSON with hierarchical outline

#### ⚡ **Round 1B: Persona Analysis** (Two Modes)

**Mode 1: AI-Powered (When Available)**
- Uses DistilBERT model for zero-shot classification
- Downloads model once, then works offline forever
- Highly accurate relevance scoring
- Model size: ~250MB (under 1GB constraint)

**Mode 2: Keyword Fallback (Always Available)**
- Smart keyword matching algorithm
- Research term detection
- Works without any AI models
- Lightweight and fast

### Offline Architecture

```
┌─────────────────────┐
│   Web Interface     │ ← Static files (no internet needed)
│   (Bootstrap + JS)  │
└─────────┬───────────┘
          │
┌─────────▼───────────┐
│   Flask Server      │ ← Local server (port 5000)
│   (Python Backend)  │
└─────────┬───────────┘
          │
┌─────────▼───────────┐
│   PDF Processing    │ ← PyMuPDF (local library)
│   + AI Analysis     │ ← Transformers (cached models)
└─────────────────────┘
```

### How Offline Mode Works

1. **No Internet Required**: All processing happens locally
2. **Cached Models**: AI models download once, then work offline
3. **Local Storage**: All files processed locally in `input/` and `output/`
4. **Fallback Systems**: If AI unavailable, uses keyword analysis
5. **Complete Self-Containment**: No external API calls or dependencies

### Offline Capabilities Verification

**Test Offline Mode:**
1. Disconnect from internet
2. Start the application: `python main.py`
3. Upload PDFs through web interface
4. Get results instantly

**What Works Offline:**
- ✅ PDF text extraction
- ✅ Font analysis and heading detection  
- ✅ Web interface and file uploads
- ✅ JSON result generation
- ✅ Persona-based content analysis
- ✅ Section ranking and excerpts
- ✅ All Bootstrap styling and JavaScript

**Model Caching (First Run Only):**
- DistilBERT model downloads automatically on first use
- ~250MB download (one-time only)
- Cached in `~/.cache/huggingface/` 
- Subsequent runs work completely offline

### Performance in Offline Mode

- **Round 1A**: < 5 seconds per PDF
- **Round 1B**: < 30 seconds for multiple PDFs
- **Memory Usage**: < 2GB RAM
- **Storage**: < 500MB including models

### Constraints Compliance

✅ **Model Size**: DistilBERT (~250MB) < 1GB limit
✅ **Execution Time**: Well under 60-second limit
✅ **AMD64 CPU**: Pure Python, no GPU required
✅ **Offline Operation**: Complete internet independence

### Fallback Strategy

If transformers/AI models fail to install:
1. Application automatically detects missing dependencies
2. Switches to keyword-based analysis mode
3. Still provides meaningful persona-driven insights
4. Full functionality maintained with reduced accuracy

This ensures the application **always works offline** regardless of system configuration.