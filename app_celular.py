import streamlit as st
from pytubefix import YouTube
import yt_dlp
import os
import subprocess
import shutil

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="DDL Station", page_icon="🛸", layout="centered")

# --- DISEÑO NEÓN DARK (CSS) ---
st.markdown("""
    <style>
    /* 1. FONDO DEEP BLACK (Negro Profundo) */
    .stApp {
        background-color: #000000;
        background-image: radial-gradient(circle at center, #1a1a1a 0%, #000000 100%);
        color: white;
    }

    /* 2. TÍTULO PRINCIPAL */
    h1 {
        color: #ffffff;
        text-align: center;
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 10px #00d2ff, 0 0 20px #00d2ff; /* Efecto Neón Azul */
        margin-bottom: 10px;
    }
    
    /* Subtítulo */
    .subtitle {
        text-align: center;
        color: #888;
        font-size: 14px;
        margin-bottom: 30px;
    }

    /* 3. BOTONES DE ACCIÓN (Estilo Cyberpunk) */
    .stButton>button {
        width: 100%;
        background: black;
        color: #00d2ff;
        border: 2px solid #00d2ff; /* Borde Neón */
        font-weight: bold;
        border-radius: 10px;
        height: 50px;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 0 10px rgba(0, 210, 255, 0.2);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: #00d2ff;
        color: black;
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.8);
    }

    /* 4. INPUTS (Cajas de texto) */
    .stTextInput>div>div>input {
        background-color: #111;
        color: #00d2ff;
        border: 1px solid #333;
        border-radius: 5px;
    }
    .stTextInput>div>div>input:focus {
        border-color: #00d2ff;
        box-shadow: 0 0 10px rgba(0, 210, 255, 0.3);
    }

    /* 5. SOLUCIÓN AL TEXTO INVISIBLE (Radio Buttons) */
    /* Esto hace que las opciones (720p, 1080p) brillen */
    div[role="radiogroup"] p {
        color: #00ffff !important; /* Cian brillante */
        font-size: 18px !important;
        font-weight: bold !important;
        text-shadow: 0 0 5px rgba(0, 255, 255, 0.5); /* Resplandor */
        background-color: rgba(0,0,0,0.5); /* Fondo semitransparente para leer mejor */
        padding: 5px 10px;
        border-radius: 5px;
        border-left: 3px solid #00ffff;
        margin-bottom: 8px;
    }
    
    /* El título de "Elige la calidad" */
    .stRadio > label {
        color: #ffffff !important;
        font-size: 20px !important;
        font-weight: bold;
        margin-bottom: 10px;
        text-decoration: underline decoration-cyan;
    }

    /* 6. PESTAÑAS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #111;
        padding: 10px;
        border-radius: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00d2ff !important;
        color: black !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ESTRUCTURA VISUAL ---
st.markdown("<h1>🚀 DDL Station 🛸</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>SYSTEM ONLINE • READY FOR DOWNLOAD</p>", unsafe_allow_html=True)

# --- VERIFICACIÓN FFMPEG ---
ffmpeg_existe = False
try:
    subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ffmpeg_existe = True
except:
    if os.path.exists("ffmpeg.exe"): ffmpeg_existe = True

# --- PESTAÑAS ---
tab1, tab2 = st.tabs(["🟥 YOUTUBE", "🎵 TIKTOK"])

# ==========================================
# PESTAÑA 1: YOUTUBE
# ==========================================
with tab1:
    yt_link = st.text_input("PEGAR ENLACE YOUTUBE:", placeholder="https://...")
    
    st.write(" ")
    
    # Radio buttons con el nuevo estilo neón
    yt_tipo = st.radio("SELECCIONA CALIDAD:", 
                       ["⚡ Video Rápido (720p)", "💎 Video Ultra (1080p)", "🎧 Solo Audio (MP3)"])
    
    st.write(" ")

    # Función auxiliar
    def unir_ffmpeg(v, a, out):
        cmd_base = "ffmpeg" if not os.path.exists("ffmpeg.exe") else "ffmpeg.exe"
        cmd = f'{cmd_base} -i "{v}" -i "{a}" -c:v copy -c:a aac "{out}" -y'
        subprocess.run(cmd, shell=True)

    if st.button("INICIAR DESCARGA"):
        if not yt_link:
            st.warning("⚠️ ERROR: ENLACE NO DETECTADO")
        else:
            try:
                with st.spinner('⏳ PROCESANDO DATOS...'):
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
                            st.warning("⚠️ 1080p NO DISPONIBLE. DESCARGANDO 720p.")
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
                        st.success("✅ DESCARGA COMPLETADA")
                        st.download_button(f"💾 GUARDAR ARCHIVO", f, file_name=final_path, mime=mime_type)
                        
            except Exception as e:
                st.error(f"❌ ERROR DEL SISTEMA: {e}")

# ==========================================
# PESTAÑA 2: TIKTOK
# ==========================================
with tab2:
    tt_link = st.text_input("PEGAR ENLACE TIKTOK:", placeholder="https://vm.tiktok.com/...")
    
    st.write(" ")
    
    if st.button("OBTENER VIDEO"):
        if not tt_link:
            st.warning("⚠️ ERROR: ENLACE REQUERIDO")
        else:
            try:
                with st.spinner('🔄 ELIMINANDO MARCA DE AGUA...'):
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
                        st.success("✅ VIDEO LISTO")
                        st.download_button("💾 GUARDAR EN GALERÍA", f, file_name=final_name, mime="video/mp4")
                        
            except Exception as e:
                st.error(f"❌ ERROR: {e}")

st.markdown("<br><center><p style='color: #333; font-size: 10px;'>DDL STATION v5.0</p></center>", unsafe_allow_html=True)
