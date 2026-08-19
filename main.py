import os
import requests
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Configuration
APIDOT_API_KEY = os.environ.get('APIDOT_API_KEY', 'sk-y4UT6Rzf8vuUdPQLOp2hVo8wTTtfV0tv6oh7q96zGBXSGOAaMKe6IawC4n1cZE')
APIDOT_API_URL = "https://api.apidot.ai/api/generate/submit"

@app.route('/')
def index():
    """Render the main page"""
    api_key_set = bool(APIDOT_API_KEY and APIDOT_API_KEY != '')
    return render_template('index.html', api_key_set=api_key_set)

@app.route('/generate', methods=['POST'])
def generate_image():
    """
    Handle image generation request
    Expects JSON with: prompt, quality, size, resolution, callback_url
    """
    try:
        # Check if API key is set
        if not APIDOT_API_KEY:
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
        'api_key_set': bool(APIDOT_API_KEY)
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
    print(f"🔑 API Key {'✓ Set' if APIDOT_API_KEY else '✗ Not Set'}")
    print(f"🌐 Visit: http://localhost:{port}")
    
    # Run the app
    app.run(host='0.0.0.0', port=port, debug=True)
