import streamlit as st
import yt_dlp
import os
import shutil
import glob

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="DDL Station", page_icon="🛸", layout="centered")

# --- DISEÑO PRO (CSS ELIMINADO EN LA v9.5, AHORA RESTAURADO) ---
st.markdown("""
    <style>
    /* 1. FONDO AZUL PETRÓLEO */
    .stApp {
        background: linear-gradient(to bottom right, #0f2027, #203a43, #2c5364);
        color: white;
    }

    /* 2. TÍTULO PRINCIPAL */
    h1 {
        color: #ffffff;
        text-align: center;
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 10px #00d2ff; 
        margin-bottom: 5px;
    }
    
    /* Subtítulo */
    .subtitle {
        text-align: center;
        color: #b0c4de;
        font-size: 14px;
        margin-bottom: 20px;
    }

    /* 3. INPUTS (Cajas de texto) */
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

    /* 4. BOTONES NEÓN (Estilo Restaurado) */
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

    /* 5. RADIO BUTTONS */
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

    /* 6. PESTAÑAS */
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
    
    /* 7. ADVERTENCIA */
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

# --- VISUALES ---
st.markdown("<h1>🚀 DDL Station 🛸</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>YOUTUBE • TIKTOK • FACEBOOK</p>", unsafe_allow_html=True)
st.markdown("<div class='warning-box'>⚠️ LÍMITE SUGERIDO: MÁXIMO 20 MINUTOS</div>", unsafe_allow_html=True)

# --- MOTOR DE DESCARGA (LÓGICA v9.5 QUE SÍ FUNCIONA) ---
def descargar_video(url, plataforma, calidad):
    try:
        # Nombre base temporal
        temp_name = f"temp_{plataforma}"
        
        # CONFIGURACIÓN "MODO GUERRA" (Anti-Bloqueo)
        ydl_opts = {
            'outtmpl': f'{temp_name}.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'ignoreerrors': True,
            'geo_bypass': True,
            'source_address': '0.0.0.0', # Forzar IPv4
            'cachedir': False,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }

        # Selección de formatos
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
                 # Evitar codec hvc1 para compatibilidad
                 ydl_opts['format'] = 'best[vcodec!=hvc1][ext=mp4]/best[ext=mp4]/best'

        # EJECUTAR DESCARGA
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=True)
            
            # Buscar qué archivo soltó yt-dlp
            archivos = glob.glob(f"{temp_name}.*")
            if not archivos: return None, None, "Error: Bloqueo o enlace inválido."
            
            archivo_real = archivos[0]
            ext = os.path.splitext(archivo_real)[1]
            
            # Nombres finales bonitos
            final_name = "audio_sandreke.mp3" if "MP3" in calidad else f"video_sandreke{ext}"
            mime = "audio/mpeg" if "MP3" in calidad else "video/mp4"
            
            return archivo_real, final_name, mime

    except Exception as e:
        return None, None, str(e)

# --- INTERFAZ ---
tab1, tab2, tab3 = st.tabs(["🟥 YOUTUBE", "🎵 TIKTOK", "📘 FACEBOOK"])

# ==========================================
# YOUTUBE
# ==========================================
with tab1:
    yt_link = st.text_input("PEGAR ENLACE YOUTUBE:", placeholder="https://...")
    st.write(" ")
    yt_tipo = st.radio("SELECCIONA CALIDAD (YT):", ["⚡ Rápido (720p)", "💎 Ultra (1080p)", "🎧 Audio MP3"])
    st.write(" ")

    if st.button("INICIAR DESCARGA YT"):
        if not yt_link:
            st.warning("⚠️ ENLACE REQUERIDO")
        else:
            with st.spinner('⏳ BURLANDO SEGURIDAD...'):
                path, name, mime = descargar_video(yt_link, "youtube", yt_tipo)
                if path:
                    with open(path, "rb") as f:
                        st.success("✅ COMPLETADO")
                        st.download_button("💾 GUARDAR ARCHIVO", f, file_name=name, mime=mime)
                    os.remove(path)
                else:
                    st.error(f"❌ Error: {mime}")

# ==========================================
# TIKTOK
# ==========================================
with tab2:
    tt_link = st.text_input("PEGAR ENLACE TIKTOK:", placeholder="https://vm.tiktok.com/...")
    st.write(" ")
    tt_tipo = st.radio("SELECCIONA CALIDAD (TT):", ["⚡ Normal", "💎 Alta Definición"])
    st.write(" ")
    
    if st.button("OBTENER TIKTOK"):
        if not tt_link:
            st.warning("⚠️ ENLACE REQUERIDO")
        else:
            with st.spinner('🔄 PROCESANDO TIKTOK...'):
                path, name, mime = descargar_video(tt_link, "tiktok", tt_tipo)
                if path:
                    with open(path, "rb") as f:
                        st.success("✅ TIKTOK LISTO")
                        st.download_button("💾 GUARDAR VIDEO", f, file_name=name, mime=mime)
                    os.remove(path)
                else:
                    st.error(f"❌ Error: {mime}")

# ==========================================
# FACEBOOK
# ==========================================
with tab3:
    fb_link = st.text_input("PEGAR ENLACE FACEBOOK:", placeholder="https://www.facebook.com/watch/...")
    st.write(" ")
    fb_tipo = st.radio("SELECCIONA CALIDAD (FB):", ["⚡ Normal", "💎 Alta Definición"])
    st.write(" ")
    
    if st.button("OBTENER FACEBOOK"):
        if not fb_link:
            st.warning("⚠️ ENLACE REQUERIDO")
        else:
            with st.spinner('🔵 PROCESANDO FACEBOOK...'):
                path, name, mime = descargar_video(fb_link, "facebook", fb_tipo)
                if path:
                    with open(path, "rb") as f:
                        st.success("✅ FACEBOOK LISTO")
                        st.download_button("💾 GUARDAR VIDEO", f, file_name=name, mime=mime)
                    os.remove(path)
                else:
                    st.error(f"❌ Error: {mime}")

# --- FOOTER ---
st.markdown("<br><br><center><p style='color: #ccc; font-size: 12px;'>DDL STATION v10.0 | POWERED BY YT-DLP</p></center>", unsafe_allow_html=True)






