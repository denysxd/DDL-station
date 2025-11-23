import streamlit as st
from pytubefix import YouTube
import yt_dlp
import os
import subprocess
import shutil

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="DDL Station", page_icon="🛸", layout="centered")

# --- GESTIÓN DE ESTADO (LIMPIAR LINKS) ---
if 'yt_url' not in st.session_state: st.session_state.yt_url = ''
if 'tt_url' not in st.session_state: st.session_state.tt_url = ''
if 'fb_url' not in st.session_state: st.session_state.fb_url = ''

def clear_yt(): st.session_state.yt_url = ''
def clear_tt(): st.session_state.tt_url = ''
def clear_fb(): st.session_state.fb_url = ''

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
        letter-spacing: 1px;
    }
    .stTextInput > label {
        color: white !important;
        font-size: 16px !important;
        font-weight: bold;
    }
    .stTextInput input {
        color: white !important;
        background-color: rgba(0, 0, 0, 0.3);
        border: 1px solid #00d2ff;
    }
    .stButton>button {
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
    .stButton>button:hover {
        background: #00d2ff;
        color: #0f2027;
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.8);
    }
    div[data-testid="column"] button {
        background: transparent;
        border: 1px solid #ff4444;
        color: #ff4444;
        height: 42px;
        margin-top: 28px;
    }
    div[data-testid="column"] button:hover {
        background: #ff4444;
        color: white;
        box-shadow: none;
    }
    div[role="radiogroup"] p {
        color: #00ffff !important;
        font-size: 18px !important;
        font-weight: bold !important;
        text-shadow: 0 0 5px rgba(0, 255, 255, 0.5);
        background-color: rgba(0, 0, 0, 0.3);
        padding: 5px 10px;
        border-radius: 5px;
        border-left: 3px solid #00ffff;
    }
    .stRadio > label {
        color: white !important;
        font-size: 18px !important;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: rgba(0,0,0,0.3);
        padding: 10px;
        border-radius: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00d2ff !important;
        color: #0f2027 !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA ---
st.markdown("<h1>🚀 DDL Station 🛸</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>YOUTUBE • TIKTOK • FACEBOOK</p>", unsafe_allow_html=True)
st.markdown("<div class='warning-box'>⚠️ LÍMITE SUGERIDO: MÁXIMO 20 MINUTOS POR VIDEO</div>", unsafe_allow_html=True)

# --- FFMPEG CHECK ---
ffmpeg_existe = False
try:
    subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ffmpeg_existe = True
except:
    if os.path.exists("ffmpeg.exe"): ffmpeg_existe = True

# --- PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["🟥 YOUTUBE", "🎵 TIKTOK", "📘 FACEBOOK"])

# ==========================================
# YOUTUBE
# ==========================================
with tab1:
    col1, col2 = st.columns([5, 1])
    with col1:
        yt_link = st.text_input("PEGAR ENLACE YOUTUBE:", placeholder="https://...", key="yt_url")
    with col2:
        st.button("🗑️", on_click=clear_yt, help="Limpiar enlace")

    st.write(" ")
    yt_tipo = st.radio("SELECCIONA CALIDAD (YT):", 
                       ["⚡ Video Rápido (720p)", "💎 Video Ultra (1080p)", "🎧 Solo Audio (MP3)"])
    st.write(" ")

    def unir_ffmpeg(v, a, out):
        cmd_base = "ffmpeg" if not os.path.exists("ffmpeg.exe") else "ffmpeg.exe"
        cmd = f'{cmd_base} -i "{v}" -i "{a}" -c:v copy -c:a aac "{out}" -y'
        subprocess.run(cmd, shell=True)

    if st.button("INICIAR DESCARGA YT"):
        if not yt_link:
            st.warning("⚠️ ENLACE REQUERIDO")
        else:
            try:
                with st.spinner('⏳ PROCESANDO YOUTUBE...'):
                    yt = YouTube(yt_link)
                    if yt.length > 1800:
                         st.warning("⚠️ Video muy largo (>30min). Podría fallar.")
                    
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
                            st.warning("⚠️ 1080p NO DISPONIBLE. BAJANDO 720p.")
                            stream = yt.streams.get_highest_resolution()
                            final_path = f"{nombre_base}_720p.mp4"
                            stream.download(filename=final_path)
                            mime_type = "video/mp4"
                    else: 
                        aud = yt.streams.get_audio_only()
                        aud.download(filename="temp_aud.m4a")
                        final_path = f"{nombre_base}.mp3"
                        if os.path.exists(final_path): os.remove(final_path)
                        os.rename("temp_aud.m4a", final_path)
                        mime_type = "audio/mpeg"

                    with open(final_path, "rb") as f:
                        st.success("✅ COMPLETADO")
                        st.download_button(f"💾 GUARDAR ARCHIVO", f, file_name=final_path, mime=mime_type)
            except Exception as e:
                st.error(f"❌ ERROR: {e}")

# ==========================================
# TIKTOK
# ==========================================
with tab2:
    col1, col2 = st.columns([5, 1])
    with col1:
        tt_link = st.text_input("PEGAR ENLACE TIKTOK:", placeholder="https://vm.tiktok.com/...", key="tt_url")
    with col2:
        st.button("🗑️", on_click=clear_tt, help="Limpiar enlace", key="btn_clear_tt")

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
                        titulo_real = info.get('title', 'tiktok_video')
                        titulo_limpio = "".join(c for c in titulo_real if c.isalnum() or c in (' ', '-', '_')).strip()
                        final_name = f"{titulo_limpio}.mp4"

                    if os.path.exists(final_name): os.remove(final_name)
                    shutil.move(nombre_tt, final_name)

                    with open(final_name, "rb") as f:
                        st.success(f"✅ TIKTOK ({tt_calidad}) LISTO")
                        st.download_button("💾 GUARDAR VIDEO", f, file_name=final_name, mime="video/mp4")
            except Exception as e:
                st.error(f"❌ ERROR: {e}")

# ==========================================
# FACEBOOK
# ==========================================
with tab3:
    col1, col2 = st.columns([5, 1])
    with col1:
        fb_link = st.text_input("PEGAR ENLACE FACEBOOK:", placeholder="https://www.facebook.com/watch/...", key="fb_url")
    with col2:
        st.button("🗑️", on_click=clear_fb, help="Limpiar enlace", key="btn_clear_fb")

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
                        titulo_real = info.get('title', 'facebook_video')
                        titulo_limpio = "".join(c for c in titulo_real if c.isalnum() or c in (' ', '-', '_')).strip()
                        final_name = f"{titulo_limpio}.mp4"

                    if os.path.exists(final_name): os.remove(final_name)
                    shutil.move(nombre_fb, final_name)

                    with open(final_name, "rb") as f:
                        st.success(f"✅ FACEBOOK ({fb_calidad}) LISTO")
                        st.download_button("💾 GUARDAR VIDEO FB", f, file_name=final_name, mime="video/mp4")
            except Exception as e:
                st.error(f"❌ ERROR: {e}")

# --- FOOTER ---
st.markdown("<br><br><center><p style='color: #ccc; font-size: 12px; letter-spacing: 2px;'>DDL STATION v6.5 | BY SANDREKE</p></center>", unsafe_allow_html=True)
