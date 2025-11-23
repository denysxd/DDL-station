import streamlit as st
import yt_dlp
import os
import shutil
import glob

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="DDL Station", page_icon="🛸", layout="centered")

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom right, #0f2027, #203a43, #2c5364);
        color: white;
    }
    h1 {
        color: #ffffff;
        text-align: center;
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 10px #00d2ff; 
        margin-bottom: 5px;
    }
    .subtitle {
        text-align: center;
        color: #b0c4de;
        font-size: 14px;
        margin-bottom: 20px;
    }
    .stTextInput > label {
        color: white !important;
        font-size: 14px !important;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .stTextInput input {
        color: white !important;
        background-color: rgba(0, 0, 0, 0.4);
        border: 1px solid #00d2ff;
        border-radius: 8px;
    }
    .stButton > button {
        width: 100%;
        background: rgba(0, 0, 0, 0.5);
        color: #00d2ff;
        border: 2px solid #00d2ff;
        font-weight: bold;
        border-radius: 10px;
        height: 50px;
        text-transform: uppercase;
        box-shadow: 0 0 10px rgba(0, 210, 255, 0.2);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: #00d2ff;
        color: #0f2027;
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.8);
    }
    div[role="radiogroup"] p {
        color: #00ffff !important;
        font-weight: bold !important;
        background-color: rgba(0, 0, 0, 0.3);
        padding: 5px 10px;
        border-radius: 5px;
        border-left: 3px solid #00ffff;
    }
    .stRadio > label {
        color: white !important;
        font-weight: bold;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(0,0,0,0.3);
        padding: 8px;
        border-radius: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00d2ff !important;
        color: #0f2027 !important;
        font-weight: bold;
    }
    .warning-box {
        background-color: rgba(255, 165, 0, 0.1);
        border: 1px solid #ffa500;
        color: #ffa500;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-size: 12px;
        font-weight: bold;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🚀 DDL Station 🛸</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>YOUTUBE • TIKTOK • FACEBOOK</p>", unsafe_allow_html=True)
st.markdown("<div class='warning-box'>⚠️ MODO ANTI-BLOQUEO ACTIVADO</div>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🟥 YOUTUBE", "🎵 TIKTOK", "📘 FACEBOOK"])

# --- FUNCIÓN DE DESCARGA MAESTRA ---
def descargar_video(url, plataforma, calidad):
    try:
        # Nombre base temporal para evitar conflictos
        temp_name = f"temp_{plataforma}"
        
        # OPCIONES ANTI-BLOQUEO
        ydl_opts = {
            'outtmpl': f'{temp_name}.%(ext)s', # Plantilla de nombre
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            # Falsificamos un navegador real
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'nocheckcertificate': True,
        }

        # Lógica de Formatos
        if plataforma == "youtube":
            if "720p" in calidad:
                ydl_opts['format'] = 'best[height<=720][ext=mp4]/best[ext=mp4]/best'
            elif "1080p" in calidad:
                ydl_opts['format'] = 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            elif "MP3" in calidad:
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
        
        elif plataforma == "tiktok" or plataforma == "facebook":
             if "Normal" in calidad:
                 ydl_opts['format'] = 'best[ext=mp4]/best'
             else:
                 # Evitar HEVC para compatibilidad
                 ydl_opts['format'] = 'best[vcodec!=hvc1][ext=mp4]/best[ext=mp4]/best'

        # EJECUCIÓN
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            titulo = info.get('title', 'video_descargado')
            clean_name = "".join(c for c in titulo if c.isalnum() or c in (' ', '-', '_')).strip()
            
            # Buscamos el archivo que se descargó (yt-dlp a veces cambia la extensión)
            archivos_encontrados = glob.glob(f"{temp_name}.*")
            
            if not archivos_encontrados:
                return None, None, "No se encontró el archivo descargado."
            
            archivo_real = archivos_encontrados[0]
            
            # Definir extensión final y mime type
            ext = os.path.splitext(archivo_real)[1]
            if "MP3" in calidad:
                mime = "audio/mpeg"
                final_name = f"{clean_name}.mp3"
            else:
                mime = "video/mp4"
                final_name = f"{clean_name}{ext}"
            
            return archivo_real, final_name, mime

    except Exception as e:
        return None, None, str(e)

# ==========================================
# YOUTUBE
# ==========================================
with tab1:
    yt_link = st.text_input("ENLACE YOUTUBE:", placeholder="https://...")
    st.write(" ")
    yt_tipo = st.radio("CALIDAD YT:", ["⚡ Rápido (720p)", "💎 Ultra (1080p)", "🎧 MP3"])
    st.write(" ")

    if st.button("DESCARGAR YT"):
        if not yt_link:
            st.warning("⚠️ Falta el enlace")
        else:
            with st.spinner('⏳ BURLANDO SEGURIDAD YOUTUBE...'):
                path, name, mime = descargar_video(yt_link, "youtube", yt_tipo)
                if path:
                    with open(path, "rb") as f:
                        st.success("✅ ¡CONSEGUIDO!")
                        st.download_button("💾 GUARDAR", f, file_name=name, mime=mime)
                    os.remove(path) # Limpieza
                else:
                    st.error(f"❌ Error: {mime}")

# ==========================================
# TIKTOK
# ==========================================
with tab2:
    tt_link = st.text_input("ENLACE TIKTOK:", placeholder="https://...")
    st.write(" ")
    tt_calidad = st.radio("CALIDAD TT:", ["⚡ Normal", "💎 Alta Definición"])
    st.write(" ")
    
    if st.button("DESCARGAR TT"):
        if not tt_link:
            st.warning("⚠️ Falta el enlace")
        else:
            with st.spinner('🔄 PROCESANDO...'):
                path, name, mime = descargar_video(tt_link, "tiktok", tt_calidad)
                if path:
                    with open(path, "rb") as f:
                        st.success("✅ LISTO")
                        st.download_button("💾 GUARDAR", f, file_name=name, mime=mime)
                    os.remove(path)
                else:
                    st.error(f"❌ Error: {mime}")

# ==========================================
# FACEBOOK
# ==========================================
with tab3:
    fb_link = st.text_input("ENLACE FACEBOOK:", placeholder="https://...")
    st.write(" ")
    fb_calidad = st.radio("CALIDAD FB:", ["⚡ Normal", "💎 Alta Definición"])
    st.write(" ")
    
    if st.button("DESCARGAR FB"):
        if not fb_link:
            st.warning("⚠️ Falta el enlace")
        else:
            with st.spinner('🔵 PROCESANDO...'):
                path, name, mime = descargar_video(fb_link, "facebook", fb_calidad)
                if path:
                    with open(path, "rb") as f:
                        st.success("✅ LISTO")
                        st.download_button("💾 GUARDAR", f, file_name=name, mime=mime)
                    os.remove(path)
                else:
                    st.error(f"❌ Error: {mime}")

st.markdown("<br><br><center><p style='color: #ccc; font-size: 10px;'>v9.0 ANTI-BOT EDITION</p></center>", unsafe_allow_html=True)





