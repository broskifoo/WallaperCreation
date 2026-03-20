# 🎨 WallpaperCreation — AI Wallpaper Generator (Multimodal)

> Generate stunning, personalized wallpapers from text prompts — optionally guided by a reference image.  
> Built with **SDXL Turbo**, **BLIP**, **FastAPI**, and **Streamlit**. Optimized for consumer GPUs (RTX 3060 / Laptop GPUs).

---

## ✨ What It Does

SoTrail WallpaperCreation is a **multimodal generative AI pipeline** that lets you:

- 🖊️ **Text → Wallpaper**: Type a prompt, get a unique 768×768 wallpaper in seconds
- 🖼️ **Image + Text → Wallpaper**: Upload a reference image — BLIP captions it automatically, then SDXL Turbo fuses the visual context with your prompt to produce a semantically guided result

---

## 🏗️ Architecture

```
User (Streamlit UI)
        │
        ▼
FastAPI Backend
        │
        ├── BLIP (CPU)
        │     └── Extracts semantic caption from reference image
        │
        └── SDXL Turbo (GPU)
              └── Generates final 768×768 wallpaper from combined prompt
```

The key design choice: **BLIP runs on CPU** to keep GPU VRAM free for SDXL Turbo — no fragile image-to-image diffusion needed.

---

## 🚀 Features

| Feature | Detail |
|--------|--------|
| 🧠 **Multimodal input** | Text-only OR text + reference image |
| ⚡ **SDXL Turbo** | 1 inference step — blazing fast generation |
| 🔍 **BLIP captioning** | Extracts rich semantic context from uploaded images |
| 🛡️ **GPU memory safety** | Attention slicing, VAE slicing, explicit CUDA cleanup |
| 🔒 **Async GPU locking** | Prevents concurrent inference crashes |
| 🖥️ **Clean UI** | Streamlit frontend — no setup required |
| 📡 **REST API** | FastAPI backend with streaming PNG response |

---

## 🗂️ Project Structure

```
WallaperCreation/
├── backend.py          # FastAPI server — BLIP + SDXL Turbo inference
├── streamlit_app.py    # Streamlit frontend UI
├── requirements.txt    # Python dependencies
├── .gitignore
└── README.md
```

---

## 🛠️ Tech Stack

### Backend
| Library | Purpose |
|--------|---------|
| **FastAPI** | Async REST API server |
| **PyTorch** | Deep learning runtime |
| **Diffusers** | SDXL Turbo pipeline |
| **Transformers** | BLIP image captioning |
| **Uvicorn** | ASGI server |
| **Pillow** | Image I/O |

### Frontend
| Library | Purpose |
|--------|---------|
| **Streamlit** | Interactive web UI |
| **Requests** | HTTP calls to backend |
| **Pillow** | Image display |

---

## ⚙️ Installation

### Prerequisites
- Python 3.10+
- NVIDIA GPU with CUDA (recommended: RTX 3060 12GB or equivalent)
- [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads) installed

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/broskifoo/WallaperCreation.git
cd WallaperCreation
```

**2. Create and activate virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

> ⚠️ On first run, BLIP and SDXL Turbo weights will be auto-downloaded from Hugging Face (~6–8 GB). Ensure a stable internet connection.

---

## ▶️ Running the Project

**Terminal 1 — Start Backend**
```bash
uvicorn backend:app --host 0.0.0.0 --port 8000
```

**Terminal 2 — Start Frontend**
```bash
streamlit run streamlit_app.py
```

Then open your browser at:
- **Frontend UI** → [http://localhost:8501](http://localhost:8501)
- **API Health check** → [http://localhost:8000](http://localhost:8000)

---

## 📡 API Reference

### `GET /`
Health check.

**Response:**
```json
{ "status": "ok", "device": "cuda" }
```

---

### `POST /generate`
Generate a wallpaper image.

**Form Data:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `prompt` | `string` | ✅ | Text description of the desired wallpaper |
| `image` | `file` | ❌ | Optional reference image (JPG/PNG) |

**Response:** PNG image stream (`image/png`)

**Example (curl):**
```bash
# Text only
curl -X POST http://localhost:8000/generate \
  -F "prompt=a futuristic neon city at night, cyberpunk aesthetic" \
  --output wallpaper.png

# Text + reference image
curl -X POST http://localhost:8000/generate \
  -F "prompt=surreal dreamscape" \
  -F "image=@reference.jpg" \
  --output wallpaper.png
```

---

## 🧠 How Multimodality Works

```
1. User provides a text prompt + (optional) reference image
2. BLIP captions the reference image → "a sunset over mountains"
3. Caption is fused:  "surreal dreamscape, inspired by a sunset over mountains"
4. SDXL Turbo generates the final wallpaper from the combined prompt
```

This approach gives **semantic visual guidance** without the instability of raw image-to-image diffusion pipelines.

---

## 🖥️ GPU & Performance Notes

| Setting | Value |
|--------|-------|
| Output resolution | 768 × 768 px (VRAM-safe) |
| Inference steps | 1 (SDXL Turbo optimized) |
| BLIP device | CPU (to preserve GPU VRAM) |
| SDXL device | CUDA (GPU) |
| Attention slicing | ✅ Enabled |
| VAE slicing | ✅ Enabled |
| CUDA cleanup | Explicit after each request |

**Tested on:**
- ✅ NVIDIA RTX 3060 (12 GB VRAM)
- ✅ Laptop GPUs (8 GB VRAM)
- ⚠️ CPU-only mode supported but very slow

---

## 🔮 Future Improvements

- [ ] **IP-Adapter** — stronger visual identity preservation from reference image
- [ ] **ControlNet** — structure-guided generation
- [ ] **Aspect ratio presets** — 16:9, 21:9, mobile portrait
- [ ] **Prompt history & gallery** — browse past generations
- [ ] **Batch generation** — multiple wallpapers per prompt
- [ ] **Dockerized deployment** — one-command startup
- [ ] **Hugging Face Spaces demo** — try it without local setup

---

## 📋 Requirements

```
fastapi==0.115.6
uvicorn[standard]==0.34.0
torch==2.5.1
diffusers==0.32.2
transformers==4.47.1
accelerate==1.2.1
pillow==11.0.0
python-multipart==0.0.20
streamlit==1.41.1
requests==2.32.3
```

---

## 📄 License

This project is for **educational and portfolio purposes**.

---

## 👤 Author

**Aryendra Pandey**  
B.Tech — Electronics & Communication Engineering  
*AI • Computer Vision • Generative Models*

- GitHub: [@broskifoo](https://github.com/broskifoo)
- Repository: [WallaperCreation](https://github.com/broskifoo/WallaperCreation)

---

## 🙏 Acknowledgments

- [Stability AI](https://stability.ai/) — SDXL Turbo model
- [Salesforce BLIP](https://github.com/salesforce/BLIP) — Image captioning
- [Hugging Face Diffusers](https://github.com/huggingface/diffusers) — Diffusion pipeline
- [FastAPI](https://fastapi.tiangolo.com/) — Backend framework
- [Streamlit](https://streamlit.io/) — Frontend framework
