import streamlit as st
import os
import gc
import sys
from huggingface_hub import InferenceClient
from PIL import Image
import io
from datetime import datetime

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

st.set_page_config(
    page_title="AI Image Generator",
    page_icon="",
    layout="centered"
)

st.markdown("""
<style>
    .main { padding: 1rem; }
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #FF4B4B, #FF6B6B);
        color: white;
        font-size: 1.2rem;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 12px;
        border: none;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 20px rgba(255,75,75,0.4);
    }
    .stTextInput > div > div > input {
        font-size: 1.1rem;
        padding: 0.75rem;
        border-radius: 12px;
        border: 2px solid #ddd;
    }
    .stTextInput > div > div > input:focus {
        border-color: #FF4B4B;
        box-shadow: 0 0 0 2px rgba(255,75,75,0.2);
    }
    .generated-image {
        border-radius: 15px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.3);
        margin: 1rem 0;
    }
    .info-box {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    .stSelectbox > div > div { border-radius: 12px; }
    h1 {
        text-align: center;
        background: linear-gradient(135deg, #FF4B4B, #FF8A8A);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem !important;
    }
    .free-badge {
        background: #00ff00;
        color: black;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: bold;
        margin-left: 5px;
    }
    .limit-badge {
        background: #ffaa00;
        color: black;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: bold;
        margin-left: 5px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# AI Image Generator")
st.markdown("### Turn your imagination into art")

model_options = {
    "FLUX.1 Schnell (Fastest)": {
        "id": "black-forest-labs/FLUX.1-schnell",
        "source": "https://huggingface.co/black-forest-labs/FLUX.1-schnell",
        "limit": "Free (~1000/day)"
    },
    "Qwen Image 2512 (New)": {
        "id": "Qwen/Qwen-Image-2512", 
        "source": "https://huggingface.co/Qwen/Qwen-Image-2512",
        "limit": "Free (~1000/day)"
    },
    "Stable Diffusion 3.5 (Best Quality)": {
        "id": "stabilityai/stable-diffusion-3.5-large",
        "source": "https://huggingface.co/stabilityai/stable-diffusion-3.5-large",
        "limit": "Free (~1000/day)"
    },
    "Stable Diffusion XL (Fast)": {
        "id": "stabilityai/stable-diffusion-xl-base-1.0",
        "source": "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0",
        "limit": "Free (~1000/day)"
    },
    "Stable Diffusion 2.1 (Balanced)": {
        "id": "stabilityai/stable-diffusion-2-1",
        "source": "https://huggingface.co/stabilityai/stable-diffusion-2-1",
        "limit": "Free (~1000/day)"
    },
    "DreamShaper (Artistic)": {
        "id": "Lykon/dreamshaper-xl-1-0",
        "source": "https://huggingface.co/Lykon/dreamshaper-xl-1-0",
        "limit": "Free (~1000/day)"
    },
    "OpenJourney (Midjourney Style)": {
        "id": "prompthero/openjourney-v4",
        "source": "https://huggingface.co/prompthero/openjourney-v4",
        "limit": "Free (~1000/day)"
    },
    "Craiyon (DALL-E Mini)": {
        "id": "craiyon/craiyon-v1",
        "source": "https://huggingface.co/craiyon/craiyon-v1",
        "limit": "Free (unlimited demo)"
    },
    "ArtFlow (Mobile Optimized)": {
        "id": "ArtFlow/ArtFlow",
        "source": "https://huggingface.co/ArtFlow/ArtFlow",
        "limit": "Free (~1000/day)"
    },
    "Playground v2.5 (Creative)": {
        "id": "playgroundai/playground-v2.5-1024px-aesthetic",
        "source": "https://huggingface.co/playgroundai/playground-v2.5-1024px-aesthetic",
        "limit": "Free (~1000/day)"
    }
}

with st.sidebar:
    st.markdown("## Settings")
    
    hf_token = st.text_input(
        "Hugging Face Token",
        type="password",
        placeholder="Enter your token here"
    )
    
    st.markdown("---")
    
    selected_model_name = st.selectbox(
        "Select Model",
        list(model_options.keys()),
        index=0
    )
    selected_model = model_options[selected_model_name]
    
    st.markdown(f"""
    **Model Info:**
    - **Model:** {selected_model_name}
    - **Rate Limit:** {selected_model['limit']}
    - **[Source]({selected_model['source']})**
    """)
    
    st.markdown("---")
    
    width = st.slider("Image Width", 256, 1024, 512, step=64)
    height = st.slider("Image Height", 256, 1024, 512, step=64)
    guidance_scale = st.slider("Guidance Scale", 1.0, 20.0, 7.5, step=0.5)
    num_inference_steps = st.slider("Steps", 10, 50, 25, step=5)
    
    st.markdown("---")
    st.markdown("""
    ### Tips
    - Better quality: Use more steps (25-50)
    - Faster generation: Use fewer steps (10-20)
    - More creative: Lower guidance scale (5-7)
    - More accurate: Higher guidance scale (8-12)
    - FLUX models work best with 512x512
    """)
    
    st.markdown("---")
    st.markdown("""
    ### Free Model Sources
    - [FLUX.1 Schnell](https://huggingface.co/black-forest-labs/FLUX.1-schnell)
    - [Qwen Image 2512](https://huggingface.co/Qwen/Qwen-Image-2512)
    - [Stable Diffusion 3.5](https://huggingface.co/stabilityai/stable-diffusion-3.5-large)
    - [DreamShaper XL](https://huggingface.co/Lykon/dreamshaper-xl-1-0)
    - [Craiyon Demo](https://huggingface.co/spaces/craiyon/craiyon)
    """)

prompt = st.text_area(
    "Describe your image",
    placeholder="A beautiful sunset over mountains, with a lake reflecting the golden light...",
    height=100
)

with st.expander("Advanced Options"):
    negative_prompt = st.text_input(
        "Negative Prompt (what to avoid)",
        placeholder="blurry, low quality, deformed, ugly",
        value="blurry, low quality, deformed, ugly, bad anatomy"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        seed = st.number_input("Seed ( -1 for random)", value=-1, step=1)
    with col2:
        enhance_prompt = st.checkbox("Enhance prompt automatically", value=False)

if st.button("Generate Image", use_container_width=True):
    if not hf_token:
        st.error("Please enter your Hugging Face token in the sidebar!")
        st.info("Get your free token at huggingface.co/settings/tokens")
        st.stop()
    
    if not prompt:
        st.warning("Please enter a prompt first!")
        st.stop()
    
    with st.spinner("Creating your masterpiece..."):
        try:
            client = InferenceClient(model=selected_model["id"], token=hf_token)
            
            image = client.text_to_image(
                prompt=prompt,
                negative_prompt=negative_prompt,
                width=width,
                height=height,
                guidance_scale=guidance_scale,
                num_inference_steps=num_inference_steps,
                seed=seed if seed != -1 else None
            )
            
            st.markdown("---")
            st.markdown("### Generated Image")
            
            st.image(image, use_container_width=True)
            
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_image_{timestamp}.png"
            
            st.download_button(
                label="Download Image",
                data=byte_im,
                file_name=filename,
                mime="image/png",
                use_container_width=True
            )
            
            st.caption(f"Model: {selected_model_name}")
            st.caption(f"Prompt: {prompt}")
            st.caption(f"Source: {selected_model['source']}")
            st.caption(f"Rate Limit: {selected_model['limit']}")
            
            del image
            gc.collect()
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Try using a different model or check your token permissions")
            
            if "rate limit" in str(e).lower():
                st.warning("""
                You've hit the rate limit! Try:
                1. Waiting a few minutes
                2. Using a different model
                3. Creating a new token
                """)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8501))
    sys.argv = ["streamlit", "run", "main.py", "--server.port", str(port), "--server.address", "0.0.0.0"]
