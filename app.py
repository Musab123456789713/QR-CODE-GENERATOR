import streamlit as st
from gtts import gTTS
from pathlib import Path
import qrcode
import socket
import io
 
# Force gTTS to use IPv4
_original_getaddrinfo = socket.getaddrinfo
def ipv4only(host, port, *args, **kwargs):
    return _original_getaddrinfo(
        host, port, socket.AF_INET, *args[1:], **kwargs)
socket.getaddrinfo = ipv4only


def speech(words):
    BASE_DIR = Path(__file__).resolve().parent
    audio_file = BASE_DIR / "audio.mp3"
    
    tts = gTTS(text=words, lang="en")    
    tts.save(str(audio_file))
    with st.expander("🔊 VOICE RESPONSE"):
        st.audio(str(audio_file))


st.set_page_config(page_title="Advanced QR Generator")
st.markdown("""<h1 style="text-align:center;">QR CODE GENERATOR</h1>""",unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""<p style='font-family: Arial; font-size: 18px';>Welcome to Smart QR Code Generator.
                Create QR codes for Websites, Text, Email, Phone Numbers and Wi-Fi in just a few clicks. 
                <br> © 2026 Muhammad Musab Ali.</p>""", unsafe_allow_html=True)
    
    speech(words= """Welcome to Smart QR Code Generator.
                Create QR codes for Websites, Text, Email, Phone Numbers and Wi-Fi in just a few clicks. """)
    
qr_type = st.selectbox( "SELECT QR TYPE", 
                       ["TEXT", "WEBSITE", "EMAIL", "PHONE NUMBER", "WIFI"] )


data = ""
if qr_type == "TEXT":
    data = st.text_area("ENTER TEXT")

elif qr_type == "WEBSITE":
    url = st.text_input("WEBSITE URL")
    data = url

elif qr_type == "EMAIL":
    email = st.text_input("EMAILl")
    subject = st.text_input("SUBJECT")
    data = f"mailto:{email}?subject={subject}"

elif qr_type == "PHONE NUMBER":
    phone = st.text_input("PHONE NUMBER")
    data = f"tel:{phone}"

elif qr_type == "WIFI":
    ssid = st.text_input("WIFI NAME")
    password = st.text_input("PASSWORD")
    data = f"WIFI:T:WPA;S:{ssid};P:{password};;"


st.markdown("""<p style='font-family: Arial; font-size: 18px';>Review your selected QR type and information above. 
            You can also customize the QR code and background colors according to your preference. Once everything looks good, 
            click Generate QR Code to create your customized QR code instantly</p>""", unsafe_allow_html=True)


col01, col02 = st.columns(2)
with col01:
    fill = st.color_picker("QR COLOR", "#000000")
with col02:
    back = st.color_picker("BACKGROUND", "#FFFFFF")
    
    
if st.button("🎯 GENERATE QR CODE"):
    if data != "":
        qr = qrcode.QRCode(version=1, box_size=10, border=4)

        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(
        fill_color=fill,
        back_color=back )

        # Convert QR image into PNG bytes
        with st.sidebar:
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            st.image(buffer.getvalue(), width=300)

            st.download_button(
                "DOWNLOAD QR CODE",
                data = buffer.getvalue(),
                file_name = "qrcode.png",
                mime = "image/png"
            )
            
    else:
        st.warning("PLEASE ENTER DATA.")


st.markdown("""            
        <style>
        .block-container {
            padding-top: 2rem;
        }
        </style>
        """, unsafe_allow_html=True
)

