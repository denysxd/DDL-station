import streamlit as st
from pytubefix import YouTube
import yt_dlp
import os
import subprocess
import shutil

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Sandreke Station", page_icon="🚀", layout="centered")

# --- DISEÑO PERSONALIZADO (CSS) ---
# Aquí sucede la magia visual
st.markdown("""
    <style>
    /* 1. Fondo de la aplicación (Degradado oscuro) */
    .stApp {
        background: linear-gradient(to bottom right, #0f2027, #203a43, #2c5364);
        color: white;
    }

    /* 2. Títulos y Encabezados */
    h1 {
        color: #00d2ff; /* Azul neón */
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        text-shadow: 0 0 10px rgba(0, 210, 255, 0.5);
    }
    h3 {
        color: #e0e0e0;
        border-bottom: 2px solid #00d2ff;
        padding-bottom: 10px;
    }

    /* 3. Personalización de los botones (Rojos para acción) */
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #FF416C, #FF4B2B);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 25px;
        height: 50px;
        box-shadow: 0 4px 15px rgba(255, 75, 43, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(255, 75, 43, 0.6);
    }

    /* 4. Cajas de texto (Inputs) */
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid #00d2ff;
        border-radius: 10px;
    }
    
    /* 5. Pestañas (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: rgba(255,255,255,0.05);
        border-radius: 10px;
        color: white;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(0, 210, 255, 0.2) !important;
        border: 1px solid #00d2ff;
        color: #00d2ff !important;
    }

    /* 6. Radio Buttons (Bolitas de selección) */
    .stRadio > label {
        color: white !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- TÍTULO CON EMOJIS ---
st.markdown("<h1>🚀 Sandreke Station 🛸</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #b0c4de;'>Tu centro de descargas universal</p>", unsafe_allow_html=True)

# --- VERIFICACIÓN FFMPEG (Silenciosa) ---
ffmpeg_existe = False
try:
    subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ffmpeg_existe = True
except:
    if os.path.exists("ffmpeg.exe"): ffmpeg_existe = True

# --- PESTAÑAS ---
tab1, tab2 = st.tabs(["🟥 YouTube", "🎵 TikTok"])

# ==========================================
# PESTAÑA 1: YOUTUBE
# ==========================================
with tab1:
    st.markdown("### 📺 Descargar de YouTube")
    yt_link = st.text_input("🔗 Pega el enlace aquí:", placeholder="https://youtube.com/...")
    
    st.write(" ") # Espacio
    yt_tipo = st.radio("✨ Elige la calidad:", 
                       ["⚡ Video Rápido (720p)", "🌟 Video Ultra (1080p)", "🎧 Solo Audio (MP3)"])
    
    st.write(" ") # Espacio

    # Función auxiliar
    def unir_ffmpeg(v, a, out):
        cmd_base = "ffmpeg" if not os.path.exists("ffmpeg.exe") else "ffmpeg.exe"
        cmd = f'{cmd_base} -i "{v}" -i "{a}" -c:v copy -c:a aac "{out}" -y'
        subprocess.run(cmd, shell=True)

    if st.button("🚀 DESCARGAR YOUTUBE"):
        if not yt_link:
            st.warning("⚠️ ¡Oye! Te olvidaste del link.")
        else:
            try:
                with st.spinner('🤖 Procesando en la nube...'):
                    yt = YouTube(yt_link)
                    nombre_base = "".join(c for c in yt.title if c.isalnum() or c in (' ', '-', '_')).strip()
                    final_path = ""
                    mime_type = ""
                    
                    if "720p" in yt_tipo:
                        stream = yt.streams.get_highest_resolution()
                        final_path = f"{nombre_base}_720p.mp4"
                        stream.download(filename=final_path)
                        mime_type = "video/mp4"
                        
                    elif "1080p" in yt_tipo:
                        vid = yt.streams.filter(res="1080p", file_extension='mp4').first()
                        aud = yt.streams.get_audio_only()
                        if vid:
                            vid.download(filename="temp_v.mp4")
                            aud.download(filename="temp_a.m4a")
                            final_path = f"{nombre_base}_1080p.mp4"
                            unir_ffmpeg("temp_v.mp4", "temp_a.m4a", final_path)
                            if os.path.exists("temp_v.mp4"): os.remove("temp_v.mp4")
                            if os.path.exists("temp_a.m4a"): os.remove("temp_a.m4a")
                            mime_type = "video/mp4"
                        else:
                            st.warning("⚠️ No hay 1080p disponible, bajando 720p.")
                            stream = yt.streams.get_highest_resolution()
                            final_path = f"{nombre_base}_720p.mp4"
                            stream.download(filename=final_path)
                            mime_type = "video/mp4"

                    else: # MP3
                        aud = yt.streams.get_audio_only()
                        aud.download(filename="temp_aud.m4a")
                        final_path = f"{nombre_base}.mp3"
                        if os.path.exists(final_path): os.remove(final_path)
                        os.rename("temp_aud.m4a", final_path)
                        mime_type = "audio/mpeg"

                    with open(final_path, "rb") as f:
                        st.success("¡Listo! Tu archivo está caliente 🔥")
                        st.download_button(f"💾 GUARDAR ARCHIVO", f, file_name=final_path, mime=mime_type)
                        
            except Exception as e:
                st.error(f"Ups, algo falló: {e}")

# ==========================================
# PESTAÑA 2: TIKTOK
# ==========================================
with tab2:
    st.markdown("### 🎵 Descargar de TikTok")
    tt_link = st.text_input("🔗 Pega el enlace de TikTok:", placeholder="https://vm.tiktok.com/...")
    
    st.write(" ")
    
    if st.button("🌪️ DESCARGAR TIKTOK"):
        if not tt_link:
            st.warning("⚠️ Necesito un link para trabajar.")
        else:
            try:
                with st.spinner('🕵️ Quitándole la marca de agua...'):
                    nombre_tt = "tiktok_video.mp4"
                    ydl_opts = {'outtmpl': nombre_tt, 'format': 'best[ext=mp4]', 'noplaylist': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(tt_link, download=True)
                        titulo_real = info.get('title', 'tiktok_video')
                        titulo_limpio = "".join(c for c in titulo_real if c.isalnum() or c in (' ', '-', '_')).strip()
                        final_name = f"{titulo_limpio}.mp4"

                    if os.path.exists(final_name): os.remove(final_name)
                    shutil.move(nombre_tt, final_name)

                    with open(final_name, "rb") as f:
                        st.success("¡TikTok limpio y listo! ✨")
                        st.download_button("💾 GUARDAR TIKTOK", f, file_name=final_name, mime="video/mp4")
                        
            except Exception as e:
                st.error(f"Error en TikTok: {e}")

# Footer discreto
st.markdown("<br><hr><center><p style='color: #555;'>Creado por Sandreke | Powered by Python</p></center>", unsafe_allow_html=True)
