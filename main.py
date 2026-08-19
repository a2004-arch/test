import streamlit as st
import requests
import json
import time
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image
import os

st.set_page_config(
    page_title="AI Image Generator",
    page_icon="",
    layout="wide"
)

# Custom CSS for ChatGPT-style UI
st.markdown("""
<style>
    /* Global styles */
    .main {
        background-color: #0a0a0f;
        padding: 0rem 1rem;
    }
    
    /* Chat container */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 1rem 0;
    }
    
    /* Message bubbles */
    .user-message {
        background: linear-gradient(135deg, #1e1e2e, #2a2a3e);
        padding: 1rem 1.2rem;
        border-radius: 18px 18px 4px 18px;
        margin: 0.5rem 0 1.5rem auto;
        max-width: 85%;
        float: right;
        clear: both;
        border: 1px solid #333;
        color: #e0e0e0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #1a1a2e, #2a1a3e);
        padding: 1rem 1.2rem;
        border-radius: 18px 18px 18px 4px;
        margin: 0.5rem 0 1.5rem auto;
        max-width: 85%;
        float: left;
        clear: both;
        border: 1px solid #4a2a6e;
        color: #e0e0e0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    .assistant-message .model-badge {
        display: inline-block;
        background: #7b2ffc;
        color: white;
        padding: 0.15rem 0.6rem;
        border-radius: 12px;
        font-size: 0.6rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .message-time {
        font-size: 0.6rem;
        color: #666;
        margin-top: 0.3rem;
        text-align: right;
    }
    
    /* Image in chat */
    .chat-image {
        border-radius: 12px;
        max-width: 100%;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        margin: 0.5rem 0;
    }
    
    /* Input area */
    .input-area {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #0a0a0f;
        padding: 1rem;
        border-top: 1px solid #222;
        backdrop-filter: blur(10px);
        z-index: 100;
    }
    
    .input-container {
        max-width: 800px;
        margin: 0 auto;
        display: flex;
        gap: 0.5rem;
        align-items: flex-end;
    }
    
    .input-container textarea {
        flex: 1;
        background: #1e1e2e;
        border: 1px solid #333;
        border-radius: 12px;
        color: #e0e0e0;
        padding: 0.75rem;
        font-size: 1rem;
        resize: none;
        min-height: 50px;
        max-height: 150px;
        font-family: inherit;
    }
    
    .input-container textarea:focus {
        outline: none;
        border-color: #7b2ffc;
        box-shadow: 0 0 0 2px rgba(123, 47, 252, 0.2);
    }
    
    .input-container button {
        background: linear-gradient(135deg, #7b2ffc, #00d4ff);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
        white-space: nowrap;
        height: 50px;
    }
    
    .input-container button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 20px rgba(123, 47, 252, 0.4);
    }
    
    .input-container button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
        transform: none;
    }
    
    /* Sidebar styles */
    .sidebar-section {
        background: #1a1a2e;
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border: 1px solid #2a2a4e;
    }
    
    .sidebar-section h3 {
        color: #a855f7;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    /* Clear chat button */
    .clear-btn {
        background: transparent;
        color: #666;
        border: 1px solid #333;
        padding: 0.3rem 1rem;
        border-radius: 8px;
        cursor: pointer;
        font-size: 0.8rem;
        transition: all 0.3s;
    }
    
    .clear-btn:hover {
        background: #ff4444;
        color: white;
        border-color: #ff4444;
    }
    
    /* Loading animation */
    .typing-indicator {
        display: inline-block;
        padding: 0.5rem 1rem;
        background: #1a1a2e;
        border-radius: 12px;
        color: #888;
        font-style: italic;
    }
    
    .typing-indicator span {
        display: inline-block;
        animation: pulse 1.4s infinite;
        animation-fill-mode: both;
    }
    
    .typing-indicator span:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .typing-indicator span:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes pulse {
        0%, 80%, 100% { opacity: 0; }
        40% { opacity: 1; }
    }
    
    /* Scrollable chat */
    .chat-scroll {
        height: calc(100vh - 180px);
        overflow-y: auto;
        padding-bottom: 80px;
    }
    
    .chat-scroll::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-scroll::-webkit-scrollbar-track {
        background: #0a0a0f;
    }
    
    .chat-scroll::-webkit-scrollbar-thumb {
        background: #333;
        border-radius: 3px;
    }
    
    .chat-scroll::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
    
    /* Status indicators */
    .status-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.6rem;
        font-weight: bold;
        margin-left: 0.5rem;
    }
    
    .status-processing {
        background: #ffa500;
        color: black;
    }
    
    .status-completed {
        background: #00ff00;
        color: black;
    }
    
    .status-error {
        background: #ff4444;
        color: white;
    }
    
    /* Responsive */
    @media (max-width: 600px) {
        .user-message, .assistant-message {
            max-width: 95%;
            font-size: 0.9rem;
        }
        .input-container textarea {
            font-size: 0.9rem;
        }
        .input-container button {
            padding: 0.5rem 1rem;
            font-size: 0.9rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I'm your AI image generator. Describe what you'd like to create, and I'll generate it for you. Feel free to be as detailed as you like!",
            "time": datetime.now().strftime("%H:%M")
        }
    ]

if "generating" not in st.session_state:
    st.session_state.generating = False

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# Sidebar
with st.sidebar:
    st.markdown("## Settings")
    
    # API Key Input
    api_key = st.text_input(
        "API Key",
        type="password",
        placeholder="Enter your Apidot API key",
        value=st.session_state.api_key
    )
    if api_key:
        st.session_state.api_key = api_key
    
    st.markdown("---")
    
    # Model Selection
    st.markdown("### Model")
    model = st.selectbox(
        "Select Model",
        ["gpt-image-2", "gpt-image-2-pro"],
        index=0,
        help="gpt-image-2 is faster, gpt-image-2-pro has better quality"
    )
    
    st.markdown("---")
    
    # Image Settings
    st.markdown("### Image Settings")
    
    quality = st.selectbox(
        "Quality",
        ["low", "medium", "high"],
        index=1
    )
    
    size = st.selectbox(
        "Aspect Ratio",
        ["1:1", "3:2", "4:3", "16:9"],
        index=0
    )
    
    resolution = st.selectbox(
        "Resolution",
        ["1K", "2K", "4K"],
        index=0
    )
    
    st.markdown("---")
    
    # Callback URL (optional)
    callback_url = st.text_input(
        "Callback URL (optional)",
        placeholder="https://test-production-917a.up.railway.app/callback",
        help="Leave empty for synchronous generation"
    )
    
    st.markdown("---")
    
    # Clear chat button
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Chat cleared. Ready for your next image request!",
                "time": datetime.now().strftime("%H:%M")
            }
        ]
        st.rerun()
    
    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.7rem;color:#666;">
        <p>Powered by <strong>Apidot API</strong></p>
        <p>Get your API key at <a href="https://apidoo.ai" target="_blank" style="color:#7b2ffc;">apidoo.ai</a></p>
    </div>
    """, unsafe_allow_html=True)

# Main chat area
st.markdown('<div class="chat-scroll" id="chat-scroll">', unsafe_allow_html=True)

# Display messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="user-message">
            {msg["content"]}
            <div class="message-time">{msg["time"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Check if message contains an image
        if "image" in msg:
            st.markdown(f"""
            <div class="assistant-message">
                <div class="model-badge">GPT Image 2</div>
                <div>{msg["content"]}</div>
                <img src="data:image/png;base64,{msg['image']}" class="chat-image" />
                <div class="message-time">{msg["time"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="assistant-message">
                <div class="model-badge">AI</div>
                <div>{msg["content"]}</div>
                <div class="message-time">{msg["time"]}</div>
            </div>
            """, unsafe_allow_html=True)

# Show typing indicator if generating
if st.session_state.generating:
    st.markdown("""
    <div class="assistant-message">
        <div class="model-badge">AI</div>
        <div class="typing-indicator">
            <span>●</span><span>●</span><span>●</span> Generating...
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Input area (fixed at bottom)
with st.container():
    st.markdown("""
    <div class="input-area">
        <div class="input-container">
            <textarea id="user-input" placeholder="Describe the image you want..." rows="2"></textarea>
            <button id="send-btn">Generate</button>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Use Streamlit components for the input
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_area(
            "Message",
            placeholder="Describe the image you want...",
            key="user_input",
            label_visibility="collapsed",
            height=50
        )
    with col2:
        send_button = st.button(
            "Generate",
            use_container_width=True,
            disabled=st.session_state.generating or not user_input or not st.session_state.api_key
        )

# Handle input
if send_button and user_input and st.session_state.api_key:
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "time": datetime.now().strftime("%H:%M")
    })
    
    # Set generating state
    st.session_state.generating = True
    
    # Prepare API request
    api_key = st.session_state.api_key
    model = model
    quality = quality
    size = size
    resolution = resolution
    callback_url = callback_url if callback_url else None
    
    # Make API request
    url = "https://api.apidot.ai/api/generate/submit"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "input": {
            "prompt": user_input,
            "quality": quality,
            "size": size,
            "resolution": resolution
        }
    }
    
    if callback_url:
        payload["callback_url"] = callback_url
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            # Check if we got a direct image or need to poll
            if "data" in result and "image" in result["data"]:
                # Direct image response
                image_data = result["data"]["image"]
                
                # Handle base64 or URL
                if image_data.startswith("data:image"):
                    # Extract base64 part
                    image_data = image_data.split(",")[1]
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Here's your image based on: \"{user_input}\"",
                    "image": image_data,
                    "time": datetime.now().strftime("%H:%M")
                })
            elif "job_id" in result:
                # Job submitted, need to poll
                job_id = result["job_id"]
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Job submitted (ID: {job_id}). Generating your image...",
                    "time": datetime.now().strftime("%H:%M")
                })
                
                # Poll for result
                status_url = f"https://api.apidot.ai/api/generate/status/{job_id}"
                max_attempts = 30
                attempts = 0
                
                while attempts < max_attempts:
                    time.sleep(2)
                    status_response = requests.get(
                        status_url,
                        headers={"Authorization": f"Bearer {api_key}"}
                    )
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        status = status_data.get("status")
                        
                        if status == "completed":
                            image_data = status_data.get("data", {}).get("image")
                            if image_data:
                                if image_data.startswith("data:image"):
                                    image_data = image_data.split(",")[1]
                                st.session_state.messages.append({
                                    "role": "assistant",
                                    "content": f"Here's your image based on: \"{user_input}\"",
                                    "image": image_data,
                                    "time": datetime.now().strftime("%H:%M")
                                })
                            break
                        elif status == "failed":
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": f"Generation failed: {status_data.get('error', 'Unknown error')}",
                                "time": datetime.now().strftime("%H:%M")
                            })
                            break
                    
                    attempts += 1
                else:
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "Generation timed out. Please try again.",
                        "time": datetime.now().strftime("%H:%M")
                    })
            else:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Unexpected response: {json.dumps(result, indent=2)}",
                    "time": datetime.now().strftime("%H:%M")
                })
        else:
            error_msg = f"API Error: {response.status_code} - {response.text}"
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg,
                "time": datetime.now().strftime("%H:%M")
            })
            
    except requests.exceptions.Timeout:
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Request timed out. Please try again.",
            "time": datetime.now().strftime("%H:%M")
        })
    except Exception as e:
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Error: {str(e)}",
            "time": datetime.now().strftime("%H:%M")
        })
    
    st.session_state.generating = False
    st.rerun()

# Auto-scroll script
st.markdown("""
<script>
    // Auto-scroll to bottom of chat
    function scrollToBottom() {
        const chatScroll = document.getElementById('chat-scroll');
        if (chatScroll) {
            chatScroll.scrollTop = chatScroll.scrollHeight;
        }
    }
    
    // Scroll on load and when new messages appear
    window.onload = scrollToBottom;
    setTimeout(scrollToBottom, 100);
    
    // Enter key to send
    document.addEventListener('DOMContentLoaded', function() {
        const textarea = document.querySelector('textarea');
        const button = document.querySelector('.input-container button');
        
        if (textarea && button) {
            textarea.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    button.click();
                }
            });
        }
    });
</script>
""", unsafe_allow_html=True)
