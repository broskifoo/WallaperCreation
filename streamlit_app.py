import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# ======================================================
# App Config
# ======================================================

st.set_page_config(
    page_title="AI Wallpaper Generator",
    layout="wide"
)

st.title("AI Wallpaper Generator")
st.write("Multimodal wallpaper generation using SDXL Turbo")

BACKEND_URL = "http://localhost:8000/generate"

# ======================================================
# Style Presets
# ======================================================

STYLE_PRESETS = {
    "None": "",
    "Photorealistic": "photorealistic, ultra high detail, professional photography",
    "Cinematic": "cinematic lighting, dramatic shadows, epic composition",
    "Anime": "anime style, vibrant colors, detailed illustration",
    "Fantasy": "fantasy art, magical atmosphere, epic lighting",
    "Cyberpunk": "cyberpunk city, neon lights, futuristic mood",
    "Minimalist": "minimalist, clean, modern aesthetic",
}

# ======================================================
# Inputs
# ======================================================

selected_style = st.selectbox(
    "Choose a style",
    STYLE_PRESETS.keys()
)

prompt = st.text_area(
    "Enter your wallpaper description",
    height=120,
    placeholder="A lone traveler standing on a cliff at sunset"
)

ref_image = st.file_uploader(
    "Reference image (optional)",
    type=["png", "jpg", "jpeg"]
)

final_prompt = prompt
if selected_style != "None":
    st.info(f"Style modifier applied: {STYLE_PRESETS[selected_style]}")
    final_prompt = f"{prompt}, {STYLE_PRESETS[selected_style]}"

st.caption("Resolution is fixed at 768×768 for RTX 3060 stability")

# ======================================================
# Generate Button
# ======================================================

if st.button("Generate Wallpaper"):
    if not prompt.strip():
        st.warning("Prompt cannot be empty")
    else:
        with st.spinner("Generating wallpaper..."):
            try:
                data = {"prompt": final_prompt}
                files = {}

                if ref_image is not None:
                    files["image"] = ref_image

                response = requests.post(
                    BACKEND_URL,
                    data=data,
                    files=files,
                    timeout=180
                )

                response.raise_for_status()

                img = Image.open(BytesIO(response.content))
                st.image(img, use_column_width=True)

                buf = BytesIO()
                img.save(buf, format="PNG")

                st.download_button(
                    label="Download Wallpaper",
                    data=buf.getvalue(),
                    file_name="wallpaper.png",
                    mime="image/png"
                )

            except Exception as e:
                st.error("Image generation failed")
                st.exception(e)

# ======================================================
# Footer
# ======================================================

st.markdown("---")
st.caption("Powered by SDXL Turbo • BLIP • FastAPI • Streamlit")
