import streamlit as st
import yt_dlp
import os
import subprocess
import shutil

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="DDL Station", page_icon="🛸", layout="centered")

# --- DISEÑO (CSS) ---
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
st.markdown("<p class='subtitle'>Ready for Download</p>", unsafe_allow_html=True)
st.markdown("<div class='warning-box'>⚠️ LÍMITE SUGERIDO: MÁXIMO 20 MINUTOS POR VIDEO</div>", unsafe_allow_html=True)

# --- VERIFICACIÓN FFMPEG ---
ffmpeg_existe = False
try:
    subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ffmpeg_existe = True
except:
    if os.path.exists("ffmpeg.exe"): ffmpeg_existe = True

tab1, tab2, tab3 = st.tabs(["🟥 YOUTUBE", "🎵 TIKTOK", "📘 FACEBOOK"])

# ==========================================
# YOUTUBE (MOTOR NUEVO: YT-DLP)
# ==========================================
with tab1:
    yt_link = st.text_input("PEGAR ENLACE YOUTUBE:", placeholder="https://...")
    st.write(" ")
    yt_tipo = st.radio("SELECCIONA CALIDAD (YT):", 
                       ["⚡ Video Rápido (720p)", "💎 Video Ultra (1080p)", "🎧 Solo Audio (MP3)"])
    st.write(" ")

    if st.button("INICIAR DESCARGA YT"):
        if not yt_link:
            st.warning("⚠️ ENLACE REQUERIDO")
        else:
            try:
                with st.spinner('⏳ PROCESANDO YOUTUBE...'):
                    # Nombres temporales
                    nombre_archivo = "yt_download.mp4"
                    mime_type = "video/mp4"
                    
                    # Opciones base de yt-dlp
                    ydl_opts = {
                        'outtmpl': nombre_archivo,
                        'noplaylist': True,
                        'quiet': True,
                        'no_warnings': True,
                    }

                    # Configuración según selección
                    if "720p" in yt_tipo:
                        # Busca el mejor video mp4 que no pase de 720p
                        ydl_opts['format'] = 'best[height<=720][ext=mp4]/best[ext=mp4]'
                    
                    elif "1080p" in yt_tipo:
                        # Busca 1080p y lo une con el mejor audio automáticamente
                        ydl_opts['format'] = 'bestvideo[height=1080]+bestaudio/best[height=1080]/best'
                        ydl_opts['merge_output_format'] = 'mp4'
                    
                    else: # MP3
                        # Descarga solo audio y post-procesa a mp3 si es necesario
                        nombre_archivo = "yt_audio.mp3"
                        ydl_opts['outtmpl'] = "yt_audio" # yt-dlp añade la extensión sola
                        ydl_opts['format'] = 'bestaudio/best'
                        ydl_opts['postprocessors'] = [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }]
                        mime_type = "audio/mpeg"

                    # EJECUCIÓN
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(yt_link, download=True)
                        titulo = info.get('title', 'video')
                        # Limpieza de nombre
                        clean_name = "".join(c for c in titulo if c.isalnum() or c in (' ', '-', '_')).strip()
                        
                        # Ajuste final de nombre de archivo real
                        if "MP3" in yt_tipo:
                            real_filename = "yt_audio.mp3"
                            final_display_name = f"{clean_name}.mp3"
                        else:
                            real_filename = nombre_archivo
                            final_display_name = f"{clean_name}.mp4"

                    # Lectura y Botón
                    if os.path.exists(real_filename):
                        with open(real_filename, "rb") as f:
                            st.success("✅ COMPLETADO")
                            st.download_button(f"💾 GUARDAR ARCHIVO", f, file_name=final_display_name, mime=mime_type)
                        
                        # Limpieza
                        os.remove(real_filename)
                    else:
                        st.error("Error: El archivo no se generó correctamente.")

            except Exception as e:
                st.error(f"❌ ERROR: {e}")

# ==========================================
# TIKTOK
# ==========================================
with tab2:
    tt_link = st.text_input("PEGAR ENLACE TIKTOK:", placeholder="https://vm.tiktok.com/...")
    st.write(" ")
    tt_calidad = st.radio("SELECCIONA CALIDAD (TT):", ["⚡ Descarga Normal", "💎 Alta Definición"])
    st.write(" ")
    
    if st.button("OBTENER TIKTOK"):
        if not tt_link:
            st.warning("⚠️ ENLACE REQUERIDO")
        else:
            try:
                with st.spinner('🔄 PROCESANDO TIKTOK...'):
                    nombre_tt = "tiktok_video.mp4"
                    if "Normal" in tt_calidad:
                        ydl_opts = {'outtmpl': nombre_tt, 'format': 'best[ext=mp4]', 'noplaylist': True}
                    else:
                        ydl_opts = {'outtmpl': nombre_tt, 'format': 'best[vcodec!=hvc1][ext=mp4]/best[ext=mp4]', 'noplaylist': True}

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(tt_link, download=True)
                        titulo = info.get('title', 'tiktok_video')
                        clean_name = "".join(c for c in titulo if c.isalnum() or c in (' ', '-', '_')).strip()
                        final_name = f"{clean_name}.mp4"

                    if os.path.exists(nombre_tt):
                        shutil.move(nombre_tt, final_name)
                        with open(final_name, "rb") as f:
                            st.success(f"✅ TIKTOK LISTO")
                            st.download_button("💾 GUARDAR VIDEO", f, file_name=final_name, mime="video/mp4")
                        os.remove(final_name)
            except Exception as e:
                st.error(f"❌ ERROR: {e}")

# ==========================================
# FACEBOOK
# ==========================================
with tab3:
    fb_link = st.text_input("PEGAR ENLACE FACEBOOK:", placeholder="https://www.facebook.com/watch/...")
    st.write(" ")
    fb_calidad = st.radio("SELECCIONA CALIDAD (FB):", ["⚡ Descarga Normal", "💎 Alta Definición"])
    st.write(" ")
    
    if st.button("OBTENER FACEBOOK"):
        if not fb_link:
            st.warning("⚠️ ENLACE REQUERIDO")
        else:
            try:
                with st.spinner('🔵 PROCESANDO FACEBOOK...'):
                    nombre_fb = "fb_video.mp4"
                    if "Normal" in fb_calidad:
                        ydl_opts = {'outtmpl': nombre_fb, 'format': 'best[height<=720][ext=mp4]/best[ext=mp4]', 'noplaylist': True}
                    else:
                        ydl_opts = {'outtmpl': nombre_fb, 'format': 'best[vcodec!=hvc1][ext=mp4]/best[ext=mp4]', 'noplaylist': True}
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(fb_link, download=True)
                        titulo = info.get('title', 'facebook_video')
                        clean_name = "".join(c for c in titulo if c.isalnum() or c in (' ', '-', '_')).strip()
                        final_name = f"{clean_name}.mp4"

                    if os.path.exists(nombre_fb):
                        shutil.move(nombre_fb, final_name)
                        with open(final_name, "rb") as f:
                            st.success(f"✅ FACEBOOK LISTO")
                            st.download_button("💾 GUARDAR VIDEO FB", f, file_name=final_name, mime="video/mp4")
                        os.remove(final_name)
            except Exception as e:
                st.error(f"❌ ERROR: {e}")

st.markdown("<br><br><center><p style='color: #ccc; font-size: 12px; letter-spacing: 2px;'>DDL STATION v8.0 | POWERED </p></center>", unsafe_allow_html=True)




