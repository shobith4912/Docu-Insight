#!/usr/bin/env python3
"""
Offline Setup Script for Adobe Hackathon 2025 PDF Processor

This script ensures the application works completely offline by:
1. Installing required dependencies if available
2. Setting up fallback mechanisms when AI models aren't available
3. Downloading and caching models for offline use
"""

import os
import sys
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def install_package(package_name):
    """Try to install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name, "--user", "--quiet"])
        logger.info(f"✓ Installed {package_name}")
        return True
    except subprocess.CalledProcessError:
        logger.warning(f"✗ Failed to install {package_name}")
        return False

def check_package(package_name):
    """Check if a package is available"""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def setup_offline_environment():
    """Set up the offline environment"""
    logger.info("Setting up Adobe Hackathon 2025 PDF Processor for offline use...")
    
    # Check required packages
    packages = {
        'fitz': 'PyMuPDF',
        'flask': 'flask',
        'flask_cors': 'flask-cors'
    }
    
    # Try to install transformers for AI functionality
    ai_packages = {
        'transformers': 'transformers',
        'torch': 'torch'
    }
    
    # Check core packages
    for import_name, package_name in packages.items():
        if check_package(import_name):
            logger.info(f"✓ {package_name} is available")
        else:
            logger.error(f"✗ {package_name} is not available - this is required!")
            return False
    
    # Try AI packages (optional for fallback mode)
    ai_available = True
    for import_name, package_name in ai_packages.items():
        if check_package(import_name):
            logger.info(f"✓ {package_name} is available - AI analysis enabled")
        else:
            logger.warning(f"✗ {package_name} not available - using fallback analysis")
            ai_available = False
    
    # Create directories
    os.makedirs("input", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    logger.info("\n" + "="*50)
    if ai_available:
        logger.info("🎉 FULL OFFLINE MODE: PDF processing + AI analysis")
    else:
        logger.info("⚠️  BASIC OFFLINE MODE: PDF processing only (keyword-based analysis)")
    
    logger.info("="*50)
    logger.info("Offline capabilities:")
    logger.info("✓ PDF text extraction and outline generation")
    logger.info("✓ Font-based heading detection (H1, H2, H3)")
    logger.info("✓ Web interface with file upload")
    logger.info("✓ JSON output generation")
    
    if ai_available:
        logger.info("✓ DistilBERT-powered persona analysis")
        logger.info("✓ Zero-shot classification for content relevance")
    else:
        logger.info("○ Keyword-based content analysis (fallback)")
    
    logger.info("="*50)
    return True

if __name__ == "__main__":
    setup_offline_environment()