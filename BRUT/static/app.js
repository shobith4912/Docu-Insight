// Adobe Hackathon 2025 PDF Processor Frontend
class PDFProcessor {
    constructor() {
        this.initializeEventListeners();
        this.baseURL = window.location.origin;
    }

    initializeEventListeners() {
        // Single file input change
        document.getElementById('pdfFile').addEventListener('change', (e) => {
            this.handleFileSelection(e);
        });

        // Multiple files input change
        document.getElementById('multiPdfFiles').addEventListener('change', (e) => {
            this.handleMultiFileSelection(e);
        });

        // Upload button (Round 1A)
        document.getElementById('uploadBtn').addEventListener('click', () => {
            this.handleUpload();
        });

        // Upload multiple files button (Round 1B)
        document.getElementById('uploadMultiBtn').addEventListener('click', () => {
            this.handleMultiUpload();
        });

        // Clear button
        document.getElementById('clearBtn').addEventListener('click', () => {
            this.handleClear();
        });

        // Analyze button
        document.getElementById('analyzeBtn').addEventListener('click', () => {
            this.handleAnalyze();
        });

        // Enter key support for analysis inputs
        ['persona', 'job'].forEach(id => {
            document.getElementById(id).addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.handleAnalyze();
                }
            });
        });
    }

    handleFileSelection(event) {
        const file = event.target.files[0];
        const uploadBtn = document.getElementById('uploadBtn');
        
        if (file && file.type === 'application/pdf') {
            uploadBtn.disabled = false;
            this.showStatus('PDF file selected: ' + file.name, 'info');
        } else {
            uploadBtn.disabled = true;
            if (file) {
                this.showStatus('Please select a valid PDF file', 'warning');
            }
        }
    }

    handleMultiFileSelection(event) {
        const files = Array.from(event.target.files);
        const uploadBtn = document.getElementById('uploadMultiBtn');
        const fileListDiv = document.getElementById('uploadedFilesList');
        const fileListContent = document.getElementById('fileListContent');
        
        // Filter for PDF files only
        const pdfFiles = files.filter(file => file.type === 'application/pdf');
        
        if (pdfFiles.length > 0) {
            uploadBtn.disabled = false;
            
            // Show file list
            fileListDiv.classList.remove('d-none');
            fileListContent.innerHTML = pdfFiles.map((file, index) => 
                `<div><i class="fas fa-file-pdf text-danger me-2"></i>${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)</div>`
            ).join('');
            
            this.showStatus(`${pdfFiles.length} PDF files selected for analysis`, 'info');
            
            if (files.length > pdfFiles.length) {
                this.showStatus(`Note: ${files.length - pdfFiles.length} non-PDF files were ignored`, 'warning');
            }
        } else {
            uploadBtn.disabled = true;
            fileListDiv.classList.add('d-none');
            if (files.length > 0) {
                this.showStatus('Please select valid PDF files', 'warning');
            }
        }
    }

    async handleUpload() {
        const fileInput = document.getElementById('pdfFile');
        const file = fileInput.files[0];

        if (!file) {
            this.showStatus('Please select a PDF file first', 'warning');
            return;
        }

        this.showLoading(true);
        this.hideResults();

        try {
            const formData = new FormData();
            formData.append('pdf', file);

            const response = await fetch(`${this.baseURL}/upload`, {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'Upload failed');
            }

            this.displayOutlineResults(result);
            this.showStatus('PDF outline extracted successfully!', 'success');

        } catch (error) {
            console.error('Upload error:', error);
            this.showStatus('Error: ' + error.message, 'danger');
        } finally {
            this.showLoading(false);
        }
    }

    async handleAnalyze() {
        const persona = document.getElementById('persona').value.trim();
        const job = document.getElementById('job').value.trim();

        if (!persona || !job) {
            this.showStatus('Please fill in both persona and job fields', 'warning');
            return;
        }

        this.showLoading(true);
        this.hideAnalysisResults();

        try {
            const response = await fetch(`${this.baseURL}/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ persona, job })
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'Analysis failed');
            }

            this.displayAnalysisResults(result);
            this.showStatus('Document analysis completed!', 'success');

        } catch (error) {
            console.error('Analysis error:', error);
            this.showStatus('Error: ' + error.message, 'danger');
        } finally {
            this.showLoading(false);
        }
    }

    async handleMultiUpload() {
        const fileInput = document.getElementById('multiPdfFiles');
        const files = Array.from(fileInput.files);
        const pdfFiles = files.filter(file => file.type === 'application/pdf');

        if (pdfFiles.length === 0) {
            this.showStatus('Please select PDF files first', 'warning');
            return;
        }

        this.showLoading(true);

        try {
            // Upload each PDF file
            for (let i = 0; i < pdfFiles.length; i++) {
                const file = pdfFiles[i];
                const formData = new FormData();
                formData.append('pdf', file);

                const response = await fetch(`${this.baseURL}/upload`, {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    const result = await response.json();
                    throw new Error(`Failed to upload ${file.name}: ${result.error}`);
                }
            }

            this.showStatus(`Successfully uploaded ${pdfFiles.length} PDF files for analysis!`, 'success');
            
            // Enable analysis section
            document.getElementById('persona').focus();
            
        } catch (error) {
            console.error('Multi-upload error:', error);
            this.showStatus('Error: ' + error.message, 'danger');
        } finally {
            this.showLoading(false);
        }
    }

    async handleClear() {
        if (!confirm('Are you sure you want to clear all uploaded files?')) {
            return;
        }

        try {
            const response = await fetch(`${this.baseURL}/clear`, {
                method: 'POST'
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'Clear failed');
            }

            // Reset UI
            document.getElementById('pdfFile').value = '';
            document.getElementById('multiPdfFiles').value = '';
            document.getElementById('uploadBtn').disabled = true;
            document.getElementById('uploadMultiBtn').disabled = true;
            document.getElementById('uploadedFilesList').classList.add('d-none');
            this.hideResults();
            this.hideAnalysisResults();
            this.showStatus('Files cleared successfully', 'success');

        } catch (error) {
            console.error('Clear error:', error);
            this.showStatus('Error: ' + error.message, 'danger');
        }
    }

    displayOutlineResults(data) {
        const container = document.getElementById('outlineContent');
        const resultsDiv = document.getElementById('outlineResults');

        let html = `
            <div class="mb-3">
                <h6><i class="fas fa-file-pdf me-2"></i>Title: ${this.escapeHtml(data.title)}</h6>
                <small class="text-muted">Total Pages: ${data.total_pages || 'Unknown'}</small>
            </div>
        `;

        if (data.outline && data.outline.length > 0) {
            html += '<div class="outline-tree">';
            
            data.outline.forEach((item, index) => {
                const levelClass = `level-${item.level.toLowerCase()}`;
                const indentLevel = item.level === 'H1' ? 0 : item.level === 'H2' ? 1 : 2;
                
                html += `
                    <div class="outline-item ${levelClass}" style="margin-left: ${indentLevel * 20}px;">
                        <div class="d-flex justify-content-between align-items-start">
                            <div>
                                <span class="badge bg-${this.getLevelColor(item.level)} me-2">${item.level}</span>
                                <strong>${this.escapeHtml(item.text)}</strong>
                            </div>
                            <div class="text-end">
                                <small class="text-muted">Page ${item.page}</small>
                                ${item.font_size ? `<br><small class="text-muted">${item.font_size}pt</small>` : ''}
                            </div>
                        </div>
                    </div>
                `;
            });
            
            html += '</div>';
        } else {
            html += '<div class="alert alert-info">No structured headings found in this PDF.</div>';
        }

        if (data.metadata) {
            html += `
                <div class="mt-3 p-3 bg-body-secondary rounded">
                    <small class="text-muted">
                        <strong>Extraction Method:</strong> ${data.metadata.extraction_method || 'Font-based heuristics'}<br>
                        <strong>Font Thresholds:</strong> H1 (>14pt + bold), H2 (>12pt), H3 (>10pt)
                    </small>
                </div>
            `;
        }

        container.innerHTML = html;
        resultsDiv.classList.remove('d-none');
    }

    displayAnalysisResults(data) {
        const container = document.getElementById('analysisContent');
        const resultsDiv = document.getElementById('analysisResults');

        let html = `
            <div class="row mb-4">
                <div class="col-md-6">
                    <h6><i class="fas fa-user me-2"></i>Persona: ${this.escapeHtml(data.metadata.persona)}</h6>
                    <h6><i class="fas fa-tasks me-2"></i>Job: ${this.escapeHtml(data.metadata.job)}</h6>
                </div>
                <div class="col-md-6 text-md-end">
                    <small class="text-muted">
                        Analysis Method: ${data.metadata.analysis_method || 'DistilBERT'}<br>
                        Processed: ${data.metadata.documents ? data.metadata.documents.length : 0} documents<br>
                        Threshold: ${data.metadata.relevance_threshold || 0.7}
                    </small>
                </div>
            </div>
        `;

        // Summary Statistics
        if (data.metadata) {
            html += `
                <div class="row mb-4">
                    <div class="col-md-4">
                        <div class="text-center p-3 bg-primary bg-opacity-10 rounded">
                            <h4 class="text-primary">${data.metadata.total_sections || 0}</h4>
                            <small>Relevant Sections</small>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="text-center p-3 bg-success bg-opacity-10 rounded">
                            <h4 class="text-success">${data.metadata.total_subsections || 0}</h4>
                            <small>Subsections</small>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="text-center p-3 bg-info bg-opacity-10 rounded">
                            <h4 class="text-info">${(data.metadata.avg_relevance || 0).toFixed(2)}</h4>
                            <small>Avg. Relevance</small>
                        </div>
                    </div>
                </div>
            `;
        }

        // Relevant Sections
        if (data.sections && data.sections.length > 0) {
            html += '<h6><i class="fas fa-star me-2"></i>Most Relevant Sections</h6>';
            html += '<div class="list-group mb-4">';
            
            data.sections.slice(0, 10).forEach((section, index) => {
                const relevancePercent = Math.round(section.importance_rank * 100);
                html += `
                    <div class="list-group-item">
                        <div class="d-flex justify-content-between align-items-start">
                            <div class="flex-grow-1">
                                <h6 class="mb-1">${this.escapeHtml(section.section_title)}</h6>
                                <p class="mb-1 text-muted">
                                    <i class="fas fa-file me-1"></i>${this.escapeHtml(section.document)} 
                                    (Page ${section.page_number})
                                </p>
                            </div>
                            <div class="text-end">
                                <span class="badge bg-${this.getRelevanceColor(section.importance_rank)}">${relevancePercent}%</span>
                            </div>
                        </div>
                        <div class="progress mt-2" style="height: 4px;">
                            <div class="progress-bar bg-${this.getRelevanceColor(section.importance_rank)}" 
                                 style="width: ${relevancePercent}%"></div>
                        </div>
                    </div>
                `;
            });
            
            html += '</div>';
        } else {
            html += '<div class="alert alert-warning">No sections found above the relevance threshold (0.7).</div>';
        }

        // Sample Text Excerpts
        if (data.subsections && data.subsections.length > 0) {
            html += '<h6><i class="fas fa-text-height me-2"></i>Text Excerpts</h6>';
            html += '<div class="accordion" id="textAccordion">';
            
            data.subsections.slice(0, 5).forEach((subsection, index) => {
                html += `
                    <div class="accordion-item">
                        <h2 class="accordion-header">
                            <button class="accordion-button collapsed" type="button" 
                                    data-bs-toggle="collapse" data-bs-target="#collapse${index}">
                                ${this.escapeHtml(subsection.document)} - Page ${subsection.page_number}
                                <span class="badge bg-info ms-2">${Math.round(subsection.relevance_score * 100)}%</span>
                            </button>
                        </h2>
                        <div id="collapse${index}" class="accordion-collapse collapse" 
                             data-bs-parent="#textAccordion">
                            <div class="accordion-body">
                                <div class="text-muted small">
                                    ${this.escapeHtml(subsection.refined_text)}
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            });
            
            html += '</div>';
        }

        container.innerHTML = html;
        resultsDiv.classList.remove('d-none');
    }

    getLevelColor(level) {
        switch (level) {
            case 'H1': return 'danger';
            case 'H2': return 'warning';
            case 'H3': return 'info';
            default: return 'secondary';
        }
    }

    getRelevanceColor(score) {
        if (score >= 0.9) return 'success';
        if (score >= 0.8) return 'info';
        if (score >= 0.7) return 'warning';
        return 'secondary';
    }

    showStatus(message, type) {
        const statusDiv = document.getElementById('statusMessage');
        statusDiv.className = `alert alert-${type} alert-dismissible fade show`;
        statusDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        statusDiv.classList.remove('d-none');
    }

    showLoading(show) {
        const spinner = document.getElementById('loadingSpinner');
        if (show) {
            spinner.classList.remove('d-none');
        } else {
            spinner.classList.add('d-none');
        }
    }

    hideResults() {
        document.getElementById('outlineResults').classList.add('d-none');
    }

    hideAnalysisResults() {
        document.getElementById('analysisResults').classList.add('d-none');
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    new PDFProcessor();
});
