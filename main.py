import os
import sys
import requests
import json
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Configuration - Read from environment variable or use default
APIDOT_API_KEY = os.environ.get('APIDOT_API_KEY', 'sk-y4UT6Rzf8vuUdPQLOp2hVo8wTTtfV0tv6oh7q96zGBXSGOAaMKe6IawC4n1cZE')
APIDOT_API_URL = "https://api.apidot.ai/api/generate/submit"

# Complete HTML with embedded CSS
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>APIDOT · Image Generator</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background: linear-gradient(135deg, #f0f4f8 0%, #d9e2ec 100%);
            font-family: 'Inter', -apple-system, system-ui, sans-serif;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem 1.5rem;
            color: #1e293b;
        }
        
        .container {
            max-width: 720px;
            width: 100%;
        }
        
        .card {
            background: #ffffff;
            border-radius: 2rem;
            box-shadow: 0 20px 40px -12px rgba(0,0,0,0.15), 0 8px 24px -6px rgba(0,0,0,0.08);
            padding: 2.5rem 2.5rem 3rem;
            transition: box-shadow 0.3s ease;
        }
        
        .card:hover {
            box-shadow: 0 24px 48px -12px rgba(0,0,0,0.2);
        }
        
        header {
            margin-bottom: 2rem;
            text-align: center;
        }
        
        h1 {
            font-size: 2rem;
            font-weight: 600;
            letter-spacing: -0.02em;
            color: #0f172a;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }
        
        .subhead {
            color: #64748b;
            font-size: 0.95rem;
            margin-top: 0.3rem;
            font-weight: 400;
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        label {
            display: block;
            font-weight: 500;
            font-size: 0.875rem;
            letter-spacing: 0.01em;
            color: #334155;
            margin-bottom: 0.5rem;
        }
        
        .required {
            color: #ef4444;
            margin-left: 0.2rem;
        }
        
        textarea, input, select {
            width: 100%;
            padding: 0.75rem 1rem;
            background: #f8fafc;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            font-family: 'Inter', sans-serif;
            font-size: 0.95rem;
            transition: all 0.2s ease;
            color: #0f172a;
        }
        
        textarea {
            resize: vertical;
            min-height: 100px;
        }
        
        textarea:focus, input:focus, select:focus {
            outline: none;
            border-color: #3b82f6;
            background: #ffffff;
            box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
        }
        
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 1rem;
        }
        
        select {
            appearance: none;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%2364748b' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 1rem center;
            padding-right: 2.5rem;
            cursor: pointer;
        }
        
        select:hover {
            background-color: #f1f5f9;
        }
        
        .btn {
            width: 100%;
            padding: 0.9rem;
            background: #0f172a;
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
            margin-top: 0.5rem;
            position: relative;
        }
        
        .btn:hover {
            background: #1e293b;
            transform: translateY(-2px);
            box-shadow: 0 8px 16px -4px rgba(15, 23, 42, 0.2);
        }
        
        .btn:active {
            transform: translateY(0);
        }
        
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .btn .spinner {
            display: none;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,0.3);
            border-top-color: #ffffff;
            border-radius: 50%;
            animation: spin 0.6s linear infinite;
            margin: 0 auto;
        }
        
        .btn.loading .spinner {
            display: block;
        }
        
        .btn.loading .btn-text {
            display: none;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        #result {
            margin-top: 2rem;
            display: none;
        }
        
        #result.show {
            display: block;
            animation: fadeIn 0.5s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .result-card {
            background: #f8fafc;
            border-radius: 16px;
            padding: 1.5rem;
            border: 2px solid #e2e8f0;
        }
        
        .result-card.success {
            border-color: #22c55e;
            background: #f0fdf4;
        }
        
        .result-card.error {
            border-color: #ef4444;
            background: #fef2f2;
        }
        
        .result-title {
            font-weight: 600;
            font-size: 1rem;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .result-title .icon {
            font-size: 1.2rem;
        }
        
        .result-message {
            color: #475569;
            font-size: 0.95rem;
            line-height: 1.6;
            word-break: break-word;
        }
        
        .result-data {
            margin-top: 1rem;
            background: #ffffff;
            border-radius: 8px;
            padding: 1rem;
            font-family: 'Courier New', monospace;
            font-size: 0.85rem;
            overflow-x: auto;
            border: 1px solid #e2e8f0;
            max-height: 300px;
            overflow-y: auto;
        }
        
        .callback-info {
            margin-top: 1.5rem;
            padding-top: 1.5rem;
            border-top: 2px dashed #e2e8f0;
        }
        
        .callback-info label {
            margin-bottom: 0.3rem;
        }
        
        .callback-info input {
            background: #f1f5f9;
        }
        
        .api-warning {
            background: #fef3c7;
            border: 2px solid #f59e0b;
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1.5rem;
            color: #92400e;
        }
        
        .api-warning strong {
            display: block;
            margin-bottom: 0.3rem;
        }
        
        @media (max-width: 640px) {
            .card {
                padding: 1.5rem;
            }
            
            .form-row {
                grid-template-columns: 1fr;
                gap: 0;
            }
            
            h1 {
                font-size: 1.5rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <header>
                <h1>🎨 Image Generator</h1>
                <p class="subhead">Powered by APIDOT · GPT-Image-2</p>
            </header>

            {% if not api_key_set %}
            <div class="api-warning">
                <strong>⚠️ API Key Not Set</strong>
                Please set the APIDOT_API_KEY environment variable in Railway.
            </div>
            {% endif %}

            <form id="generateForm">
                <div class="form-group">
                    <label for="prompt">Prompt <span class="required">*</span></label>
                    <textarea 
                        id="prompt" 
                        name="prompt" 
                        rows="3" 
                        placeholder="Describe the image you want to generate..."
                        required
                    >A premium product photo of a silver espresso machine on a clean white studio background, realistic lighting, high detail</textarea>
                </div>

                <div class="form-row">
                    <div class="form-group">
                        <label for="quality">Quality</label>
                        <select id="quality" name="quality">
                            <option value="low" selected>Low</option>
                            <option value="medium">Medium</option>
                            <option value="high">High</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="size">Size</label>
                        <select id="size" name="size">
                            <option value="1:1" selected>1:1</option>
                            <option value="16:9">16:9</option>
                            <option value="9:16">9:16</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="resolution">Resolution</label>
                        <select id="resolution" name="resolution">
                            <option value="1K" selected>1K</option>
                            <option value="2K">2K</option>
                            <option value="4K">4K</option>
                        </select>
                    </div>
                </div>

                <div class="callback-info">
                    <div class="form-group">
                        <label for="callback_url">Callback URL</label>
                        <input 
                            type="url" 
                            id="callback_url" 
                            name="callback_url" 
                            placeholder="https://your-domain.com/callback"
                            value="https://test-production-917a.up.railway.app/callback"
                        >
                    </div>
                </div>

                <button type="submit" class="btn" id="submitBtn" {% if not api_key_set %}disabled{% endif %}>
                    <span class="btn-text">🚀 Generate Image</span>
                    <div class="spinner"></div>
                </button>
            </form>

            <div id="result">
                <div class="result-card" id="resultCard">
                    <div class="result-title">
                        <span class="icon" id="resultIcon">✅</span>
                        <span id="resultTitle">Success</span>
                    </div>
                    <div class="result-message" id="resultMessage"></div>
                    <div class="result-data" id="resultData"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('generateForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const submitBtn = document.getElementById('submitBtn');
            const resultDiv = document.getElementById('result');
            const resultCard = document.getElementById('resultCard');
            const resultMessage = document.getElementById('resultMessage');
            const resultData = document.getElementById('resultData');
            const resultTitle = document.getElementById('resultTitle');
            const resultIcon = document.getElementById('resultIcon');
            
            // Show loading state
            submitBtn.classList.add('loading');
            submitBtn.disabled = true;
            resultDiv.classList.remove('show');
            
            // Collect form data
            const formData = {
                prompt: document.getElementById('prompt').value,
                quality: document.getElementById('quality').value,
                size: document.getElementById('size').value,
                resolution: document.getElementById('resolution').value,
                callback_url: document.getElementById('callback_url').value || 'https://test-production-917a.up.railway.app/callback'
            };
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });
                
                const data = await response.json();
                
                // Show result
                resultDiv.classList.add('show');
                
                if (data.success) {
                    resultCard.className = 'result-card success';
                    resultIcon.textContent = '✅';
                    resultTitle.textContent = 'Success';
                    resultMessage.textContent = data.message || 'Image generation submitted successfully!';
                    resultData.textContent = JSON.stringify(data.data, null, 2);
                } else {
                    resultCard.className = 'result-card error';
                    resultIcon.textContent = '❌';
                    resultTitle.textContent = 'Error';
                    resultMessage.textContent = data.error || 'Something went wrong';
                    resultData.textContent = data.details || JSON.stringify(data, null, 2);
                }
            } catch (error) {
                resultDiv.classList.add('show');
                resultCard.className = 'result-card error';
                resultIcon.textContent = '❌';
                resultTitle.textContent = 'Error';
                resultMessage.textContent = 'Failed to connect to server';
                resultData.textContent = error.message;
            } finally {
                // Remove loading state
                submitBtn.classList.remove('loading');
                submitBtn.disabled = false;
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Render the main page"""
    api_key_set = bool(APIDOT_API_KEY and APIDOT_API_KEY != 'YOUR_API_KEY_HERE')
    return render_template_string(HTML_TEMPLATE, api_key_set=api_key_set)

@app.route('/generate', methods=['POST'])
def generate_image():
    """
    Handle image generation request
    Expects JSON with: prompt, quality, size, resolution, callback_url
    """
    try:
        # Check if API key is set
        if not APIDOT_API_KEY or APIDOT_API_KEY == 'YOUR_API_KEY_HERE':
            return jsonify({
                'success': False,
                'error': 'API key not configured. Please set APIDOT_API_KEY environment variable.'
            }), 500
        
        # Get form data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        prompt = data.get('prompt')
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Prepare the request payload
        payload = {
            "model": "gpt-image-2",
            "callback_url": data.get('callback_url', 'https://test-production-917a.up.railway.app/callback'),
            "input": {
                "prompt": prompt,
                "quality": data.get('quality', 'low'),
                "size": data.get('size', '1:1'),
                "resolution": data.get('resolution', '1K')
            }
        }
        
        # Prepare headers
        headers = {
            'Authorization': f'Bearer {APIDOT_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        # Make API request
        response = requests.post(
            APIDOT_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        # Check if request was successful
        if response.status_code == 200:
            result = response.json()
            return jsonify({
                'success': True,
                'data': result,
                'message': 'Image generation submitted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'API Error: {response.status_code}',
                'details': response.text
            }), response.status_code
            
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timed out'}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Connection error'}), 503
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'api_key_set': bool(APIDOT_API_KEY and APIDOT_API_KEY != 'YOUR_API_KEY_HERE')
    })

@app.route('/callback', methods=['POST'])
def callback():
    """Callback endpoint for APIDOT"""
    try:
        data = request.get_json()
        print(f"Callback received: {json.dumps(data, indent=2)}")
        return jsonify({'status': 'received'}), 200
    except Exception as e:
        print(f"Callback error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    # Get port from environment or use 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Print startup info
    print(f"🚀 Starting server on port {port}")
    print(f"🔑 API Key {'✓ Set' if APIDOT_API_KEY and APIDOT_API_KEY != 'YOUR_API_KEY_HERE' else '✗ Not Set'}")
    print(f"🌐 Visit: http://localhost:{port}")
    
    # Run the app
    app.run(host='0.0.0.0', port=port)
