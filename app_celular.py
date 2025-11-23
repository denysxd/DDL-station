import streamlit as st
import yt_dlp
import os
import shutil
import glob

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="DDL Station Social", page_icon="📲", layout="centered")

# --- DISEÑO PRO (NEON DARK) ---
st.markdown("""
    <style>
    /* 1. FONDO AZUL PETRÓLEO */
    .stApp {
        background: linear-gradient(to bottom right, #0f2027, #203a43, #2c5364);
        color: white;
    }

    /* 2. TÍTULOS */
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
        letter-spacing: 3px;
    }

    /* 3. INPUTS */
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

    /* 4. BOTONES */
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
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🚀 DDL Station 🛸</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>TIKTOK • FACEBOOK</p>", unsafe_allow_html=True)

# --- MOTOR DE DESCARGA ---
def descargar_video(url, plataforma, calidad):
    try:
        temp_name = f"temp_{plataforma}"
        
        # Configuración yt-dlp
        ydl_opts = {
            'outtmpl': f'{temp_name}.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'ignoreerrors': True,
            'geo_bypass': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }

        # Selección de formatos para TT y FB
        if "Normal" in calidad:
             ydl_opts['format'] = 'best[ext=mp4]/best'
        else:
             # Evitar codec hvc1 para compatibilidad, buscar mejor calidad
             ydl_opts['format'] = 'best[vcodec!=hvc1][ext=mp4]/best[ext=mp4]/best'

        # EJECUTAR DESCARGA
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=True)
            
            # Buscar archivo
            archivos = glob.glob(f"{temp_name}.*")
            if not archivos: return None, None, "Error: No se pudo descargar el archivo."
            
            archivo_real = archivos[0]
            ext = os.path.splitext(archivo_real)[1]
            
            final_name = f"video_social{ext}"
            mime = "video/mp4"
            
            return archivo_real, final_name, mime

    except Exception as e:
        return None, None, str(e)

# --- INTERFAZ (Solo 2 Pestañas) ---
tab1, tab2 = st.tabs(["🎵 TIKTOK", "📘 FACEBOOK"])

# ==========================================
# TIKTOK
# ==========================================
with tab1:
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
with tab2:
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
                        st.download_button("💾 GUARDAR VIDEO FB", f, file_name=name, mime=mime)
                    os.remove(path)
                else:
                    st.error(f"❌ Error: {mime}")

st.markdown("<br><br><center><p style='color: #ccc; font-size: 12px;'>DDL STATION SOCIAL | BY SANDREKE</p></center>", unsafe_allow_html=True)







