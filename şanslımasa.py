import streamlit as st
import random
import plotly.graph_objects as go
import time
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Tavuk Dünyası | Şans Çarkı", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Montserrat', sans-serif;
    }
    .stButton>button {
        background-color: #FF3C00;
        color: white;
        font-size: 18px;
        border-radius: 10px;
        padding: 10px 24px;
    }
    .stButton>button:hover {
        background-color: #96004B;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎡 Tavuk Dünyası Şans Çarkı")
st.write("Bilgilerini doldur, kaydet ve çarkı döndürerek sürpriz ödüllerden birini kazan! 🐔")

# Ödül listesi (ağırlıklı)
ağırlıklı_oduller = [
    ("LİMONATA", 5),
    ("KARADUTLU LİMONATA", 3),
    ("ÇİLEKLİ LİMONATA", 3),
    ("KARADUT SUYU", 3),
    ("SIKMA PORTAKAL SUYU", 3),
    ("SÜTLAÇ", 5),
    ("PATATES", 1),
    ("STICKER", 5)
]

oduller = [o[0] for o in ağırlıklı_oduller]
ağırlıklar = [o[1] for o in ağırlıklı_oduller]

if "form_kaydedildi" not in st.session_state:
    st.session_state.form_kaydedildi = False

if not st.session_state.form_kaydedildi:
    form = st.form(key="user_info_form")
    with form:
        st.subheader("Bilgilerinizi doldurun")
        telefon_girdi = st.text_input("Telefon Numaranız", max_chars=11, help="Lütfen telefon numaranızı 05XXXXXXXXX şeklinde giriniz.")
        dogum_tarihi = st.date_input("Doğum Tarihiniz", min_value=datetime(1900, 1, 1), max_value=datetime(2007, 7, 17))
        cinsiyet = st.selectbox("Cinsiyetiniz", ["Seçiniz", "Kadın", "Erkek", "Diğer"])
        sehir = st.selectbox("Şube Seçimi", ["Seçiniz"] + [f"Şube {i+1}" for i in range(10)])
        form_submitted = st.form_submit_button("Bilgileri Kaydet")

    if form_submitted:
        if not telefon_girdi.startswith("05") or not telefon_girdi.isdigit() or len(telefon_girdi) != 11:
            st.error("Lütfen telefon numaranızı 05XXXXXXXXX şeklinde eksiksiz giriniz.")
        elif cinsiyet == "Seçiniz" or sehir == "Seçiniz":
            st.error("Lütfen cinsiyet ve şube seçimlerini yapınız.")
        else:
            st.session_state.form_kaydedildi = True
            st.session_state.kayit = {
                "Telefon": telefon_girdi,
                "Doğum Tarihi": dogum_tarihi.strftime("%Y-%m-%d"),
                "Cinsiyet": cinsiyet,
                "Şube": sehir
            }
            st.success("Bilgileriniz başarıyla kaydedildi. Şimdi çarkı döndürebilirsiniz.")

# ÇARK
if st.session_state.form_kaydedildi:
    if st.button("🎯 Çarkı Döndür"):
        secilen_odul = random.choices(population=oduller, weights=ağırlıklar, k=1)[0]
        secilen_index = oduller.index(secilen_odul)
        rotation_angle = 360 - (secilen_index * 45 + 22.5)
        colors = ["#96004B" if i % 2 == 0 else "#FFC800" for i in range(8)]

        with st.spinner("🎡 Çark dönüyor..."):
            time.sleep(3)

        fig = go.Figure(data=[
            go.Pie(
                labels=[""] * 8,
                values=[1] * 8,
                marker_colors=colors,
                hole=0.4,
                textinfo="none",
                direction="clockwise",
                rotation=rotation_angle
            )
        ])

        fig.update_layout(
            showlegend=False,
            width=500,
            height=500,
            margin=dict(t=0, b=0, l=0, r=0)
        )

        st.plotly_chart(fig)
        st.success(f"🎉 Tebrikler! {secilen_odul} kazandınız!")

        yeni_kayit = pd.DataFrame({
            "Tarih": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "Telefon": [st.session_state.kayit["Telefon"]],
            "Doğum Tarihi": [st.session_state.kayit["Doğum Tarihi"]],
            "Cinsiyet": [st.session_state.kayit["Cinsiyet"]],
            "Şube": [st.session_state.kayit["Şube"]],
            "Kazandığı Ödül": [secilen_odul]
        })

        try:
            mevcut = pd.read_csv("kazananlar_log.csv")
            guncel = pd.concat([mevcut, yeni_kayit], ignore_index=True)
        except FileNotFoundError:
            guncel = yeni_kayit

        guncel.to_csv("kazananlar_log.csv", index=False)
        st.info("Bilgiler ve kazanan başarıyla kaydedildi. Teşekkürler!")
