import streamlit as st
import pandas as pd
import io
matplotlib.use("Agg")  # Guna backend tanpa GUI untuk Streamlit
import matplotlib.pyplot as plt


st.set_page_config(page_title="Aplikasi Kesihatan Ringkas", layout="centered")
st.title("Aplikasi Kalorimatik ✅")

# -------------------
# Nama Pengguna
# -------------------
nama = st.text_input("Masukkan nama anda:")
safe_name = nama.replace(" ", "_") if nama else "data_kesihatan"

st.markdown("---")

# -------------------
# Kalkulator BMI
# -------------------
st.header("📏 Kalkulator BMI")

berat = st.number_input("Berat (kg)", min_value=1.0, format="%.1f")
tinggi = st.number_input("Tinggi (cm)", min_value=1.0, format="%.1f")

bmi = None
kategori_bmi = ""
if berat >= 20 and tinggi >= 100:  # Validasi realistik
    bmi = berat / ((tinggi / 100) ** 2)
    st.write(f"BMI: *{bmi:.2f}*")

    if bmi < 18.5:
        kategori_bmi = "Kurus"
    elif bmi < 25:
        kategori_bmi = "Normal"
    elif bmi < 30:
        kategori_bmi = "Berlebihan berat"
    else:
        kategori_bmi = "Obes"

    st.success(f"Status BMI: *{kategori_bmi}*")
elif berat > 0 and tinggi > 0:
    st.warning("⚠ Sila masukkan berat ≥ 20kg dan tinggi ≥ 100cm.")

st.markdown("---")

# -------------------
# Pengira Kalori Ringkas
# -------------------
st.header("🔥 Pengira Kalori Harian Ringkas")

gender = st.selectbox("Pilih jantina:", ["Lelaki", "Perempuan"])
default_cal = 2500 if gender == "Lelaki" else 2000

target_cal = st.number_input("Sasaran kalori harian (kcal):", value=default_cal)
eaten = st.number_input("Masukkan jumlah kalori yang telah dimakan (kcal):", min_value=0, value=0)

baki = target_cal - eaten

# Papar status kalori
if nama:
    st.write(f"{nama}, jumlah kalori dimakan: *{eaten} kcal*")
else:
    st.write(f"Jumlah kalori dimakan: *{eaten} kcal*")

if baki > 0:
    st.success(f"Kalori belum cukup: {baki} kcal lagi")
elif baki < 0:
    st.error(f"Terlampau {abs(baki)} kcal dari sasaran!")
else:
    st.info("Tepat cukup kalori!")

st.markdown("---")

# -------------------
# Papar & Simpan Graf
# -------------------
if nama and bmi is not None:
    # Data hari ini
    df_hari_ini = pd.DataFrame([{
        "Nama": nama,
        "Berat (kg)": berat,
        "Tinggi (cm)": tinggi,
        "BMI": round(bmi, 2),
        "Kategori BMI": kategori_bmi,
        "Jantina": gender,
        "Kalori Dimakan": eaten,
        "Baki Kalori": baki
    }])

    # -------------------
    # Graf bar kalori
    # -------------------
    fig, ax = plt.subplots(figsize=(5, 3))
    warna_baki = "green" if baki >= 0 else "red"
    bars = ax.bar(["Dimakan", "Baki/Defisit"], [eaten, baki], color=["orange", warna_baki])

    ax.set_ylabel("Kalori (kcal)")
    ax.set_title("Kalori Harian")
    ax.axhline(0, color='black', linewidth=0.8)  # Garis tengah untuk lebihan kalori

    # Label atas bar
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3 if height >= 0 else -12),
                    textcoords="offset points",
                    ha='center', va='bottom' if height >= 0 else 'top')

    # Info ringkas di bawah graf
    info_teks = f"{nama} | Berat: {berat}kg | Tinggi: {tinggi}cm | {kategori_bmi}"
    plt.figtext(0.5, -0.05, info_teks, wrap=True, ha='center', fontsize=9)

    st.pyplot(fig)  # Papar graf di Streamlit

    # -------------------
    # Muat Turun CSV
    # -------------------
    csv = df_hari_ini.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Muat Turun Data Kesihatan (CSV)",
        data=csv,
        file_name=f"{safe_name}.csv",
        mime='text/csv'
    )

    # -------------------
    # Muat Turun Graf PNG
    # -------------------
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='png', bbox_inches='tight')
    img_buffer.seek(0)
    plt.close(fig)  # Tutup figure untuk elak memory leak

    st.download_button(
        label="📸 Muat Turun Graf Kalori (PNG)",
        data=img_buffer,
        file_name=f"graf_kalori_{safe_name}.png",
        mime="image/png"
    )

else:
    st.info("ℹ Sila lengkapkan maklumat Nama, Berat dan Tinggi sebelum meneruskan.")
