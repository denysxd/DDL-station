import streamlit as st
from pytubefix import YouTube
import yt_dlp
import os
import subprocess
import shutil

# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="DDL Station", page_icon="🚀")

# Estilos CSS para botones grandes y pestañas
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        font-weight: bold;
        border-radius: 10px;
        height: 50px;
    }
    /* Color rojo para botón de YouTube */
    div[data-testid="stHorizontalBlock"] button {
        background-color: #FF0000; 
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Estación de Descarga")

# Verificación de herramientas (Solo necesario para 1080p)
ffmpeg_existe = False
try:
    # Intentamos llamar a ffmpeg para ver si responde
    subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ffmpeg_existe = True
except:
    # Si falla, verificamos si existe el archivo local .exe (para Windows local)
    if os.path.exists("ffmpeg.exe"):
        ffmpeg_existe = True

if not ffmpeg_existe:
    st.warning("⚠️ FFmpeg no detectado. La opción 1080p podría fallar en local, pero 720p y TikTok funcionarán bien.")


# --- CREAMOS PESTAÑAS ---
tab1, tab2 = st.tabs(["🟥 YouTube", "⬛ TikTok"])

# ==========================================
# PESTAÑA 1: YOUTUBE
# ==========================================
with tab1:
    st.header("Descargador YouTube")
    yt_link = st.text_input("Pega el enlace de YouTube:")
    
    yt_tipo = st.radio("Elige la calidad:", 
                       ["Video Rápido (720p)", "Video Ultra (1080p)", "Solo Audio (MP3)"])
    
    # Función auxiliar para unir con FFmpeg
    def unir_ffmpeg(v, a, out):
        # Detectamos si usar comando global o archivo local
        cmd_base = "ffmpeg" if not os.path.exists("ffmpeg.exe") else "ffmpeg.exe"
        cmd = f'{cmd_base} -i "{v}" -i "{a}" -c:v copy -c:a aac "{out}" -y'
        subprocess.run(cmd, shell=True)

    if st.button("DESCARGAR YOUTUBE"):
        if not yt_link:
            st.error("Falta el link.")
        else:
            try:
                with st.spinner('Procesando YouTube...'):
                    yt = YouTube(yt_link)
                    nombre_base = "".join(c for c in yt.title if c.isalnum() or c in (' ', '-', '_')).strip()
                    
                    final_path = ""
                    mime_type = ""
                    
                    if yt_tipo == "Video Rápido (720p)":
                        # Esta opción es la más rápida, baja video+audio juntos
                        stream = yt.streams.get_highest_resolution()
                        final_path = f"{nombre_base}_720p.mp4"
                        stream.download(filename=final_path)
                        mime_type = "video/mp4"
                        
                    elif yt_tipo == "Video Ultra (1080p)":
                        # Requiere FFmpeg
                        vid = yt.streams.filter(res="1080p", file_extension='mp4').first()
                        aud = yt.streams.get_audio_only()
                        
                        if vid:
                            vid.download(filename="temp_v.mp4")
                            aud.download(filename="temp_a.m4a")
                            final_path = f"{nombre_base}_1080p.mp4"
                            unir_ffmpeg("temp_v.mp4", "temp_a.m4a", final_path)
                            
                            # Limpieza
                            if os.path.exists("temp_v.mp4"): os.remove("temp_v.mp4")
                            if os.path.exists("temp_a.m4a"): os.remove("temp_a.m4a")
                            mime_type = "video/mp4"
                        else:
                            st.warning("No hay 1080p, bajando 720p...")
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

                    # Botón de descarga final
                    with open(final_path, "rb") as f:
                        st.download_button(f"📥 BAJAR AHORA ({yt_tipo})", f, file_name=final_path, mime=mime_type)
                        
            except Exception as e:
                st.error(f"Error en YouTube: {e}")

# ==========================================
# PESTAÑA 2: TIKTOK
# ==========================================
with tab2:
    st.header("Descargador TikTok (Sin Marca)")
    tt_link = st.text_input("Pega el enlace de TikTok:")
    
    if st.button("DESCARGAR TIKTOK"):
        if not tt_link:
            st.error("Falta el link.")
        else:
            try:
                with st.spinner('Buscando video de TikTok...'):
                    # Configuración de yt-dlp para TikTok
                    nombre_tt = "tiktok_video.mp4"
                    ydl_opts = {
                        'outtmpl': nombre_tt,
                        'format': 'best[ext=mp4]', # Mejor calidad MP4
                        'noplaylist': True
                    }
                    
                    # Descargar
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(tt_link, download=True)
                        titulo_real = info.get('title', 'tiktok_video')
                        # Limpiamos titulo
                        titulo_limpio = "".join(c for c in titulo_real if c.isalnum() or c in (' ', '-', '_')).strip()
                        final_name = f"{titulo_limpio}.mp4"

                    # Renombrar para que tenga el titulo real
                    if os.path.exists(final_name): os.remove(final_name)
                    shutil.move(nombre_tt, final_name)

                    st.success("¡TikTok procesado!")
                    
                    with open(final_name, "rb") as f:
                        st.download_button("📥 BAJAR TIKTOK", f, file_name=final_name, mime="video/mp4")
                        
            except Exception as e:
                st.error(f"Error en TikTok: {e}")