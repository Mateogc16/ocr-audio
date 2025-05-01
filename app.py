import os
import time
import glob
import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image
from gtts import gTTS
from googletrans import Translator

# ----------------------------------------
# Estética Mágica Unificada: Azul y Morado
# ----------------------------------------
magic_theme = """
<style>
body {
    background-color: #0b032d;
    color: #d0caff;
    font-family: 'Georgia', serif;
}
h1, h2, h3 {
    color: #cba6f7;
    text-shadow: 0 0 5px #b892ff, 0 0 10px #8f43f8;
}
.stButton>button {
    background: linear-gradient(145deg, #6a00ff, #9c4dff);
    border: 1px solid #d6b3ff;
    color: #ffffff;
    border-radius: 10px;
    padding: 0.6em 1.2em;
    font-weight: bold;
    box-shadow: 0 0 10px #a463ff;
}
.stSelectbox, .stTextInput, .stTextArea, .css-1offfwp {
    background-color: #150034 !important;
    color: #e0dfff !important;
    border: 1px solid #4b0082 !important;
}
.sidebar .sidebar-content {
    background-color: #120a3b;
    color: #dcd6f7;
}
.stCameraInput > div > video,
.stCameraInput > div > canvas {
    border: 5px solid #6a00ff;
    border-radius: 12px;
    box-shadow: 0 0 15px #9c4dff;
}
hr {
    border-top: 1px solid #8854d0;
}
</style>
"""
st.markdown(magic_theme, unsafe_allow_html=True)

# ----------------------------------------
# Título Principal
# ----------------------------------------
st.title("🔮 Grimorio y Espejo Arcano")
st.subheader("Fusiona OCR místico y traducción de conjuros")

# ----------------------------------------
# Inicializar Sistema
# ----------------------------------------
translator = Translator()

# Limpiar archivos antiguos
def remove_files(days=7):
    files = glob.glob("temp/*.mp3")
    now = time.time()
    for f in files:
        if os.stat(f).st_mtime < now - days * 86400:
            os.remove(f)
remove_files()

# ----------------------------------------
# Sección de OCR: Espejo Arcano
# ----------------------------------------
st.markdown("---")
st.header("📜 Espejo Arcano: Reconocimiento Óptico (OCR)")
st.write("Muestra tu texto al espejo para que revele su secreto.")

use_camera = st.checkbox("Usar Cámara para OCR")
if use_camera:
    img_buffer = st.camera_input("Acércate al espejo y muestra el texto")
else:
    img_buffer = None
    uploaded = st.file_uploader("Cargar imagen al espejo:", type=["png","jpg","jpeg"])
    if uploaded:
        img_buffer = uploaded
        st.image(uploaded, caption="Imagen cargada al espejo", use_column_width=True)

ocr_text = ""
if img_buffer is not None:
    data = img_buffer.getvalue()
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    ocr_mode = st.radio("Filtro del reflejo:", ["Normal", "Inversión Mística"], index=0)
    if ocr_mode == "Inversión Mística":
        img = cv2.bitwise_not(img)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    ocr_text = pytesseract.image_to_string(rgb)
    st.subheader("✨ Texto revelado por el espejo:")
    st.code(ocr_text)
else:
    st.info("🔍 Selecciona Cámara o sube una imagen para iniciar OCR.")

# ----------------------------------------
# Sección de Traducción: Conjuro Parlante
# ----------------------------------------
st.markdown("---")
st.header("🗣️ Conjuro Parlante: Texto a Voz y Traducción")

input_text = st.text_area("Texto fuente:", value=ocr_text)

col1, col2 = st.columns(2)
with col1:
    in_sel = st.selectbox("Lengua de origen", ("Inglés","Español","Bengali","Coreano","Mandarín","Japonés"))
with col2:
    out_sel = st.selectbox("Lengua de destino", ("Inglés","Español","Bengali","Coreano","Mandarín","Japonés"))

accent = st.selectbox(
    "Acento para el conjuro (solo inglés):",
    ["Defecto","Reino Unido","Estados Unidos","Canadá","Australia","India","Irlanda","Sudáfrica"],
    index=0
)

tld_map = {
    "Defecto":"com","Reino Unido":"co.uk","Estados Unidos":"com",
    "Canadá":"ca","Australia":"com.au","India":"co.in",
    "Irlanda":"ie","Sudáfrica":"co.za"
}

lg_map = {"Inglés":"en","Español":"es","Bengali":"bn","Coreano":"ko","Mandarín":"zh-cn","Japonés":"ja"}

if st.button("🔊 Invocar Traducción"):  
    in_lang = lg_map[in_sel]
    out_lang = lg_map[out_sel]
    tld = tld_map[accent]
    fname, translated = text_to_speech(in_lang, out_lang, input_text, tld)
    path = f"temp/{fname}.mp3"
    with open(path, "rb") as f:
        audio = f.read()
    st.audio(audio, format="audio/mp3")
    st.subheader("📜 Texto traducido:")
    st.write(translated)

st.markdown("---")
st.write("&copy; 2025 GrimorioTech")
