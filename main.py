import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="AI Image Generator - Puter",
    page_icon="",
    layout="centered"
)

st.markdown("""
<style>
    .main { padding: 1rem; }
    h1 {
        text-align: center;
        background: linear-gradient(135deg, #6c5ce7, #a855f7, #ff6b6b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem !important;
    }
    .subtitle {
        text-align: center;
        color: #888;
        margin-bottom: 1rem;
    }
    .info-box {
        background: #1e1e2e;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid #6c5ce7;
        color: #e0e0e0;
    }
    .info-box strong {
        color: #a855f7;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# AI Image Generator")
st.markdown('<p class="subtitle">Powered by Puter.js - No API keys needed</p>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <strong> How it works:</strong> You pay for your own AI usage through your Puter account.
    New users get free credits to start!
</div>
""", unsafe_allow_html=True)

# The entire Puter.js app embedded in an iframe
components.html("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://js.puter.com/v2/"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: transparent;
            color: #e0e0e0;
            padding: 0.5rem;
        }
        
        .container {
            max-width: 100%;
            margin: 0 auto;
        }
        
        .input-group {
            margin: 0.75rem 0;
        }
        
        label {
            display: block;
            font-weight: 600;
            margin-bottom: 0.25rem;
            color: #ccc;
            font-size: 0.9rem;
        }
        
        textarea {
            width: 100%;
            padding: 0.75rem;
            border-radius: 12px;
            background: #1e1e2e;
            color: #e0e0e0;
            border: 2px solid #333;
            font-size: 1rem;
            font-family: inherit;
            resize: vertical;
            min-height: 80px;
            transition: border-color 0.3s;
        }
        
        textarea:focus {
            outline: none;
            border-color: #6c5ce7;
            box-shadow: 0 0 0 3px rgba(108, 92, 231, 0.2);
        }
        
        select {
            width: 100%;
            padding: 0.75rem;
            border-radius: 12px;
            background: #1e1e2e;
            color: #e0e0e0;
            border: 2px solid #333;
            font-size: 1rem;
            font-family: inherit;
            cursor: pointer;
            transition: border-color 0.3s;
        }
        
        select:focus {
            outline: none;
            border-color: #6c5ce7;
            box-shadow: 0 0 0 3px rgba(108, 92, 231, 0.2);
        }
        
        select option {
            background: #1e1e2e;
        }
        
        .row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.75rem;
        }
        
        input[type="number"] {
            width: 100%;
            padding: 0.75rem;
            border-radius: 12px;
            background: #1e1e2e;
            color: #e0e0e0;
            border: 2px solid #333;
            font-size: 1rem;
            font-family: inherit;
            transition: border-color 0.3s;
        }
        
        input[type="number"]:focus {
            outline: none;
            border-color: #6c5ce7;
            box-shadow: 0 0 0 3px rgba(108, 92, 231, 0.2);
        }
        
        .btn-generate {
            width: 100%;
            padding: 0.875rem;
            background: linear-gradient(135deg, #6c5ce7, #a855f7);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1.2rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            margin: 0.75rem 0;
        }
        
        .btn-generate:hover {
            transform: scale(1.02);
            box-shadow: 0 4px 20px rgba(108, 92, 231, 0.4);
        }
        
        .btn-generate:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .btn-generate:disabled:hover {
            transform: none;
            box-shadow: none;
        }
        
        #result {
            margin-top: 1rem;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        #result img {
            max-width: 100%;
            border-radius: 15px;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
        }
        
        .status {
            text-align: center;
            color: #888;
            padding: 0.5rem;
            font-size: 0.9rem;
        }
        
        .status.loading {
            color: #a855f7;
        }
        
        .status.error {
            color: #ff6b6b;
        }
        
        .status.success {
            color: #51cf66;
        }
        
        .model-info {
            background: #1a1a2e;
            padding: 0.5rem 0.75rem;
            border-radius: 8px;
            margin-top: 0.5rem;
            font-size: 0.8rem;
            color: #888;
            text-align: center;
            border: 1px solid #2a2a4e;
        }
        
        .model-info strong {
            color: #a855f7;
        }
        
        .download-btn {
            width: 100%;
            padding: 0.75rem;
            background: #2a2a4e;
            color: #e0e0e0;
            border: 2px solid #6c5ce7;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            margin-top: 0.5rem;
        }
        
        .download-btn:hover {
            background: #6c5ce7;
            color: white;
        }
        
        .badge {
            display: inline-block;
            background: #6c5ce7;
            color: white;
            padding: 0.15rem 0.6rem;
            border-radius: 20px;
            font-size: 0.7rem;
            font-weight: bold;
            margin-left: 0.5rem;
        }
        
        @media (max-width: 600px) {
            .row {
                grid-template-columns: 1fr;
            }
            body {
                padding: 0.25rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="input-group">
            <label for="prompt">Describe your image</label>
            <textarea id="prompt" placeholder="A beautiful sunset over mountains, with a lake reflecting the golden light...">A beautiful sunset over mountains with a lake reflecting golden light</textarea>
        </div>
        
        <div class="input-group">
            <label for="modelSelect">Select Model</label>
            <select id="modelSelect">
                <option value="black-forest-labs/flux-2-dev">FLUX.2 Dev (Best Quality)</option>
                <option value="black-forest-labs/flux-1.1-pro">FLUX 1.1 Pro (Fast)</option>
                <option value="gpt-image-2">GPT Image 2</option>
                <option value="gemini-3.1-flash-image-preview" selected>Gemini 3.1 Flash (Nano Banana)</option>
                <option value="google/imagen-4.0-ultra">Imagen 4 Ultra</option>
                <option value="black-forest-labs/flux-schnell">FLUX Schnell (Fastest)</option>
            </select>
        </div>
        
        <div class="row">
            <div class="input-group">
                <label for="width">Width</label>
                <input type="number" id="width" value="512" min="256" max="1024" step="64">
            </div>
            <div class="input-group">
                <label for="height">Height</label>
                <input type="number" id="height" value="512" min="256" max="1024" step="64">
            </div>
        </div>
        
        <div class="input-group">
            <label for="negativePrompt">Negative Prompt (what to avoid)</label>
            <textarea id="negativePrompt" placeholder="blurry, low quality, deformed, ugly" style="min-height: 50px;">blurry, low quality, deformed, ugly, bad anatomy</textarea>
        </div>
        
        <button class="btn-generate" id="generateBtn" onclick="generateImage()">
            Generate Image
        </button>
        
        <div id="status" class="status">Ready to generate</div>
        
        <div id="result"></div>
        
        <div class="model-info">
            Powered by <strong>Puter.js</strong> - You pay for your own AI usage
        </div>
    </div>
    
    <script>
        let currentImageBlob = null;
        let currentFilename = null;
        
        async function generateImage() {
            const prompt = document.getElementById('prompt').value.trim();
            const model = document.getElementById('modelSelect').value;
            const width = parseInt(document.getElementById('width').value) || 512;
            const height = parseInt(document.getElementById('height').value) || 512;
            const negativePrompt = document.getElementById('negativePrompt').value.trim();
            
            const status = document.getElementById('status');
            const result = document.getElementById('result');
            const btn = document.getElementById('generateBtn');
            
            if (!prompt) {
                status.textContent = 'Please enter a prompt!';
                status.className = 'status error';
                return;
            }
            
            btn.disabled = true;
            btn.textContent = 'Generating...';
            status.textContent = 'Creating your masterpiece...';
            status.className = 'status loading';
            result.innerHTML = '';
            
            try {
                const params = {
                    model: model,
                    width: width,
                    height: height
                };
                
                if (negativePrompt) {
                    params.negative_prompt = negativePrompt;
                }
                
                const image = await puter.ai.txt2img(prompt, params);
                
                result.innerHTML = '';
                result.appendChild(image);
                
                const imgElement = result.querySelector('img');
                if (imgElement) {
                    imgElement.style.maxWidth = '100%';
                    imgElement.style.borderRadius = '15px';
                    imgElement.style.boxShadow = '0 8px 30px rgba(0,0,0,0.5)';
                    
                    const response = await fetch(imgElement.src);
                    currentImageBlob = await response.blob();
                    
                    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
                    currentFilename = `generated_image_${timestamp}.png`;
                    
                    const downloadBtn = document.createElement('button');
                    downloadBtn.className = 'download-btn';
                    downloadBtn.textContent = 'Download Image';
                    downloadBtn.onclick = downloadImage;
                    result.appendChild(downloadBtn);
                }
                
                status.textContent = 'Image generated successfully!';
                status.className = 'status success';
                
            } catch (error) {
                console.error('Error:', error);
                status.textContent = 'Error: ' + error.message;
                status.className = 'status error';
                
                if (error.message.includes('insufficient credits')) {
                    status.textContent = 'Insufficient credits! Please add credits to your Puter account.';
                }
            } finally {
                btn.disabled = false;
                btn.textContent = 'Generate Image';
            }
        }
        
        function downloadImage() {
            if (currentImageBlob) {
                const url = URL.createObjectURL(currentImageBlob);
                const a = document.createElement('a');
                a.href = url;
                a.download = currentFilename || 'generated_image.png';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            }
        }
        
        document.getElementById('prompt').addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && e.ctrlKey) {
                generateImage();
            }
        });
    </script>
</body>
</html>
""", height=900, scrolling=True)

st.markdown("""
<div style="text-align:center;color:#666;font-size:0.8rem;margin-top:1rem;padding:1rem 0;border-top:1px solid #222;">
    <p>Powered by <strong>Puter.js</strong> - No API keys required</p>
    <p style="font-size:0.7rem;color:#444;">Users pay for their own AI usage through their Puter account</p>
</div>
""", unsafe_allow_html=True)
