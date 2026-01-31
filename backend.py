import io
import gc
import asyncio
import torch
from PIL import Image

from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from diffusers import AutoPipelineForText2Image
from transformers import BlipProcessor, BlipForConditionalGeneration

# ======================================================
# App setup
# ======================================================

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

gpu_lock = asyncio.Lock()

# ======================================================
# Device setup
# ======================================================

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MAX_RES = 768  # RTX 3060 safe

# ======================================================
# BLIP (Image → Text) — CPU ONLY
# ======================================================

blip_processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

blip_model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)
blip_model.eval()

# ======================================================
# SDXL Turbo (Text → Image) — GPU
# ======================================================

pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/sdxl-turbo",
    torch_dtype=torch.float16,
    variant="fp16",
).to(DEVICE)

pipe.enable_attention_slicing()
pipe.enable_vae_slicing()

# ======================================================
# Utils
# ======================================================

def pil_to_bytes(img: Image.Image):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

# ======================================================
# Routes
# ======================================================

@app.get("/")
def health():
    return {"status": "ok", "device": DEVICE}

@app.post("/generate")
async def generate(
    prompt: str = Form(...),
    image: UploadFile | None = File(None),
):
    async with gpu_lock:
        final_prompt = prompt
        output_image = None

        try:
            # --------------------------------------------
            # If reference image exists → caption it
            # --------------------------------------------
            if image is not None:
                ref_img = Image.open(image.file).convert("RGB")

                inputs = blip_processor(ref_img, return_tensors="pt")
                caption_ids = blip_model.generate(
                    **inputs,
                    max_new_tokens=50
                )

                caption = blip_processor.decode(
                    caption_ids[0],
                    skip_special_tokens=True
                )

                final_prompt = f"{prompt}, inspired by {caption}"

            # --------------------------------------------
            # Generate image
            # --------------------------------------------
            with torch.inference_mode():
                result = pipe(
                    prompt=final_prompt,
                    num_inference_steps=1,
                    guidance_scale=0.0,
                    width=MAX_RES,
                    height=MAX_RES,
                )

                output_image = result.images[0]

            return StreamingResponse(
                pil_to_bytes(output_image),
                media_type="image/png"
            )

        finally:
            if output_image is not None:
                del output_image

            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
            gc.collect()
