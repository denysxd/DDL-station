import streamlit as st
import yt_dlp
import os
import glob
import shutil

st.set_page_config(page_title="DDL Station", page_icon="🛸", layout="centered")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom right, #0f2027, #203a43, #2c5364); color: white; }
    h1 { color: #ffffff; text-align: center; font-family: 'Courier New', monospace; text-shadow: 0 0 10px #00d2ff; }
    .warning-box { background-color: rgba(255, 68, 68, 0.2); border: 1px solid #ff4444; color: white; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold; margin-bottom: 20px; }
    .stTextInput input { background-color: rgba(0,0,0,0.4); border: 1px solid #00d2ff; color: white; }
    .stButton>button { background: rgba(0,0,0,0.5); color: #00d2ff; border: 2px solid #00d2ff; border-radius: 10px; font-weight: bold; }
    .stButton>button:hover { background: #00d2ff; color: black; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🚀 DDL Station v9.5</h1>", unsafe_allow_html=True)

# --- FUNCIÓN DE DESCARGA MAESTRA ---
def descargar_video(url, plataforma, calidad):
    try:
        temp_name = f"temp_{plataforma}"
        
        # --- CONFIGURACIÓN DE GUERRA ---
        # Estas opciones intentan evadir el bloqueo de IP de centro de datos
        ydl_opts = {
            'outtmpl': f'{temp_name}.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'ignoreerrors': True,
            'geo_bypass': True,
            'source_address': '0.0.0.0', # Forzar IPv4
            'cachedir': False, # No usar caché para evitar rastros
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'referer': 'https://www.google.com/',
        }

        if plataforma == "youtube":
            if "720p" in calidad:
                ydl_opts['format'] = 'best[height<=720][ext=mp4]/best[ext=mp4]/best'
            elif "1080p" in calidad:
                ydl_opts['format'] = 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            elif "MP3" in calidad:
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}]
        
        elif plataforma == "tiktok" or plataforma == "facebook":
             if "Normal" in calidad:
                 ydl_opts['format'] = 'best[ext=mp4]/best'
             else:
                 ydl_opts['format'] = 'best[vcodec!=hvc1][ext=mp4]/best[ext=mp4]/best'

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=True)
            
            # Buscar el archivo generado (cualquier extensión)
            archivos = glob.glob(f"{temp_name}.*")
            if not archivos: return None, None, "Bloqueo detectado: El archivo no se pudo descargar."
            
            archivo_real = archivos[0]
            ext = os.path.splitext(archivo_real)[1]
            final_name = "audio.mp3" if "MP3" in calidad else f"video{ext}"
            mime = "audio/mpeg" if "MP3" in calidad else "video/mp4"
            
            return archivo_real, final_name, mime

    except Exception as e:
        return None, None, str(e)

# --- INTERFAZ SIMPLIFICADA ---
tab1, tab2, tab3 = st.tabs(["🟥 YOUTUBE", "🎵 TIKTOK", "📘 FACEBOOK"])

with tab1:
    yt_link = st.text_input("YouTube Link:")
    yt_tipo = st.radio("Calidad:", ["⚡ 720p", "💎 1080p", "🎧 MP3"])
    if st.button("DESCARGAR YT"):
        if yt_link:
            with st.spinner('⏳ Intentando burlar bloqueo...'):
                path, name, mime = descargar_video(yt_link, "youtube", yt_tipo)
                if path:
                    with open(path, "rb") as f:
                        st.download_button("💾 GUARDAR", f, file_name=name, mime=mime)
                    os.remove(path)
                else:
                    st.error(f"❌ Error: {mime}")

with tab2:
    tt_link = st.text_input("TikTok Link:")
    tt_tipo = st.radio("Calidad TT:", ["⚡ Normal", "💎 HD"])
    if st.button("DESCARGAR TT"):
        if tt_link:
            with st.spinner('🔄 Procesando...'):
                path, name, mime = descargar_video(tt_link, "tiktok", tt_tipo)
                if path:
                    with open(path, "rb") as f:
                        st.download_button("💾 GUARDAR", f, file_name=name, mime=mime)
                    os.remove(path)
                else:
                    st.error(f"❌ Error: {mime}")

with tab3:
    fb_link = st.text_input("Facebook Link:")
    fb_tipo = st.radio("Calidad FB:", ["⚡ Normal", "💎 HD"])
    if st.button("DESCARGAR FB"):
        if fb_link:
            with st.spinner('🔵 Procesando...'):
                path, name, mime = descargar_video(fb_link, "facebook", fb_tipo)
                if path:
                    with open(path, "rb") as f:
                        st.download_button("💾 GUARDAR", f, file_name=name, mime=mime)
                    os.remove(path)
                else:
                    st.error(f"❌ Error: {mime}")






