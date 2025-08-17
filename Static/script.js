let currentResumeText = '';

document.getElementById('resumeFile').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        document.getElementById('fileName').textContent = `Selected: ${file.name}`;
        uploadResume(file);
    }
});

async function uploadResume(file) {
    const formData = new FormData();
    formData.append('file', file);

    try {
        showLoading(true);
        const response = await fetch('/upload-resume', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        
        if (response.ok) {
            currentResumeText = result.text;
            enableButtons();
            showMessage('Resume uploaded successfully!', 'success');
        } else {
            showMessage(result.detail, 'error');
        }
    } catch (error) {
        showMessage('Error uploading resume: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

function enableButtons() {
    const buttons = ['btn1', 'btn2', 'btn3', 'btn4', 'btn5'];
    buttons.forEach(id => {
        document.getElementById(id).disabled = false;
    });
}

async function analyzeResume(type) {
    if (!currentResumeText) {
        showMessage('Please upload a resume first!', 'error');
        return;
    }

    const jobDesc = document.getElementById('jobDesc').value.trim();
    
    // Check if job description is required for certain analysis types
    if ((type === 'keywords' || type === 'percentage') && !jobDesc) {
        showMessage('Job description is required for this analysis type!', 'error');
        return;
    }
    
    try {
        showLoading(true);
        hideResults();
        
        const response = await fetch('/analyze-resume', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                resume_text: currentResumeText,
                job_description: jobDesc,
                analysis_type: type
            })
        });

        const result = await response.json();
        
        if (response.ok) {
            showResults(getTitle(type), result.analysis);
        } else {
            showMessage(result.detail, 'error');
        }
    } catch (error) {
        showMessage('Error analyzing resume: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

async function submitCustomQuery() {
    const query = document.getElementById('customQuery').value.trim();
    
    if (!query) {
        showMessage('Please enter a query!', 'error');
        return;
    }

    if (!currentResumeText) {
        showMessage('Please upload a resume first!', 'error');
        return;
    }

    try {
        showLoading(true);
        hideResults();
        
        const response = await fetch('/custom-query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                resume_text: currentResumeText
            })
        });

        const result = await response.json();
        
        if (response.ok) {
            showResults('Custom Query Response', result.response);
            document.getElementById('customQuery').value = '';
        } else {
            showMessage(result.detail, 'error');
        }
    } catch (error) {
        showMessage('Error processing query: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

function getTitle(type) {
    const titles = {
        'about': 'Resume Summary',
        'improve': 'Skill Improvement Suggestions',
        'keywords': 'Missing Keywords Analysis',
        'percentage': 'Match Percentage Analysis'
    };
    return titles[type] || 'Analysis Results';
}

function showResults(title, content) {
    document.getElementById('resultsTitle').textContent = title;
    
    // Convert markdown-style formatting to HTML
    let formattedContent = content
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')  // Bold text
        .replace(/\*(.*?)\*/g, '<em>$1</em>')              // Italic text
        .replace(/•/g, '▪️')                               // Better bullet points
        .replace(/(\d+\.)/g, '<strong>$1</strong>')        // Bold numbers
        .replace(/MATCH SCORE:/g, '<strong style="color: #059669; font-size: 1.3rem;">MATCH SCORE:</strong>')
        .replace(/BREAKDOWN:/g, '<strong style="color: #4f46e5; font-size: 1.2rem;">BREAKDOWN:</strong>')
        .replace(/(\d+%)/g, '<span style="color: #dc2626; font-weight: 600;">$1</span>'); // Highlight percentages
    
    document.getElementById('resultsContent').innerHTML = formattedContent;
    document.getElementById('results').style.display = 'block';
    document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
}

function hideResults() {
    document.getElementById('results').style.display = 'none';
}

function showLoading(show) {
    document.getElementById('loading').style.display = show ? 'block' : 'none';
}

function showMessage(message, type) {
    const existingMessage = document.querySelector('.error, .success');
    if (existingMessage) {
        existingMessage.remove();
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = type;
    messageDiv.textContent = message;
    document.querySelector('.main-content').insertBefore(messageDiv, document.querySelector('.upload-section'));
    
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}