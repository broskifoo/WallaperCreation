AI Wallpaper Generator (Multimodal)

A GPU-optimized multimodal AI wallpaper generator that creates high-quality aesthetic wallpapers using text prompts and optional reference images.
Built with FastAPI, Streamlit, SDXL Turbo, and BLIP, designed to run efficiently on consumer GPUs like RTX 3060.

Overview

This project demonstrates a practical multimodal generative AI pipeline:

Text → Image generation using Stable Diffusion XL Turbo

Image → Text understanding using BLIP image captioning

Intelligent fusion of user prompt + visual context

Memory-safe inference with GPU locking and cleanup

Simple, clean frontend for interactive generation

The system supports:

Prompt-only image generation

Prompt + reference image guided generation

Architecture
User (Streamlit UI)
        |
        v
FastAPI Backend
        |
        ├── BLIP (CPU)
        |     └─ Extracts semantic caption from reference image
        |
        └── SDXL Turbo (GPU)
              └─ Generates final image from combined prompt

Key Features

Multimodal input (text + optional image)

SDXL Turbo for fast, high-quality generation

BLIP-based image understanding (no fragile hacks)

GPU memory safety:

Attention slicing

VAE slicing

Explicit CUDA cleanup

RTX 3060-safe resolution (768×768)

Asynchronous GPU locking to prevent crashes

Clean separation of frontend and backend

Tech Stack
Backend

Python

FastAPI

PyTorch

Diffusers

Transformers

BLIP Image Captioning

SDXL Turbo

Frontend

Streamlit

Requests

Pillow

Installation
1. Clone the repository
git clone https://github.com/broskifoo/WallpaperCreation.git
cd WallpaperCreation

2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt


Make sure you have NVIDIA CUDA installed if using GPU.

Running the Project
Start Backend (FastAPI)
uvicorn backend:app --host 0.0.0.0 --port 8000

Start Frontend (Streamlit)
streamlit run streamlit_app.py


Open browser at:

http://localhost:8501

API Endpoint
POST /generate

Form Data

prompt (string, required)

image (file, optional)

Response

PNG image stream

How Multimodality Works

User uploads a reference image (optional)

BLIP generates a semantic caption from the image

Caption is merged with the user’s prompt

SDXL Turbo generates an image based on combined context

This avoids unstable image-to-image diffusion while preserving semantic guidance.

GPU & Performance Notes

Resolution is clamped to 768×768

SDXL Turbo uses 1 inference step

BLIP runs on CPU to preserve GPU memory

Explicit cleanup prevents CUDA OOM errors

Designed specifically for:

RTX 3060 (12GB)

Laptop GPUs

Student-grade hardware

Project Status

Stable

Modular

Easily extensible to:

IP-Adapter

ControlNet

Image variations

Batch generation

Future Improvements

IP-Adapter for stronger visual identity preservation

Prompt history & gallery

Aspect ratio presets (wallpaper formats)

Dockerized deployment

Hugging Face Spaces demo

Author

Aryendra Pandey
B.Tech Electronics & Communication Engineering
AI / Computer Vision / Generative Models

License

This project is for educational and portfolio purposes.
