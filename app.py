import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date

st.set_page_config(
    page_title="Simulasi Daerah Mitra IKN",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================
# STYLE
# =====================

st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
.block-container {
    padding-top: 2rem;
}
.metric-card {
    background-color: #151A21;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #2C333A;
}
.big-title {
    font-size: 42px;
    font-weight: 800;
}
.subtle {
    color: #9CA3AF;
}
</style>
""", unsafe_allow_html=True)

# =====================
# DATA MASTER
# =====================

KAWASAN_DB = {
    "KPI/KI Kariangau": {
        "lokasi": "Kota Balikpapan, Kalimantan Timur",
        "luas": 2000,
        "status": "Telah ditetapkan sebagai kawasan industri",
        "klaster": ["Teknologi Bersih", "Energi Rendah Karbon", "Kimia Maju"],
        "investasi": 28.5,
        "tenaga_kerja": 12000
    },
    "KI Buluminung": {
        "lokasi": "Kabupaten Penajam Paser Utara, Kalimantan Timur",
        "luas": 4200,
        "status": "Kawasan industri potensial",
        "klaster": ["Industri Berbasis Pertanian Berkelanjutan", "Logistik"],
        "investasi": 18.0,
        "tenaga_kerja": 8000
    },
    "KEK Maloy Batuta Trans Kalimantan": {
        "lokasi": "Kabupaten Kutai Timur, Kalimantan Timur",
        "luas": 557,
        "status": "Kawasan ekonomi khusus",
        "klaster": ["Industri Berbasis Pertanian Berkelanjutan", "Energi Rendah Karbon"],
        "investasi": 12.5,
        "tenaga_kerja": 5000
    },
    "KIPI/KIHI Tanah Kuning-Mangkupadi": {
        "lokasi": "Kabupaten Bulungan, Kalimantan Utara",
        "luas": 10000,
        "status": "Kawasan industri hijau",
        "klaster": ["Energi Rendah Karbon", "Teknologi Bersih", "Kimia Maju"],
        "investasi": 45.0,
        "tenaga_kerja": 20000
    }
}

BOBOT = {
    "Kesesuaian Bidang Usaha dengan Superhub Ekonomi": 10,
    "Dukungan Pemerintah Daerah": 20,
    "Potensi Ekonomi dan Kesiapan Infrastruktur": 35,
    "Rencana Pengembangan Daerah Mitra": 35
}

DOKUMEN = [
    "Surat pernyataan minat penetapan Daerah Mitra",
    "Surat pernyataan minat kerja sama",
    "Peta kartometrik lokasi",
    "Rencana tata ruang, zonasi, dan masterplan",
    "Studi kelayakan ekonomi dan finansial",
    "Rencana pengelolaan Daerah Mitra",
    "Rekomendasi dan dukungan Pemerintah Daerah",
    "Informasi status lahan yang jelas"
]

INTERVENSI = {
    "Penyusunan studi kelayakan ekonomi dan finansial": 7,
    "Penyelesaian status lahan": 8,
    "Sinkronisasi rencana tata ruang dan masterplan": 7,
    "Peningkatan konektivitas jalan dan logistik": 6,
    "Penyediaan infrastruktur air, listrik, dan limbah": 6,
    "Penguatan dukungan Pemerintah Daerah": 5,
    "Pemberian insentif dan kemudahan berusaha": 4,
    "Integrasi dengan klaster Superhub Ekonomi Nusantara": 5
}

# =====================
# SIDEBAR
# =====================

st.sidebar.title("⚙️ Input Simulasi")

pilihan_kawasan = st.sidebar.selectbox(
    "Pilih calon Daerah Mitra",
    list(KAWASAN_DB.keys())
)

data = KAWASAN_DB[pilihan_kawasan]

pemrakarsa = st.sidebar.selectbox(
    "Pemrakarsa",
    [
        "Kementerian/Lembaga",
        "Pemerintah Daerah Provinsi",
        "Pemerintah Daerah Kabupaten/Kota",
        "Badan Usaha",
        "Otorita IKN"
    ]
)

st.sidebar.divider()
st.sidebar.subheader("Checklist Dokumen")

dokumen_terpenuhi = []
for dok in DOKUMEN:
    if st.sidebar.checkbox(dok, value=True):
        dokumen_terpenuhi.append(dok)

kelengkapan_dokumen = len(dokumen_terpenuhi) / len(DOKUMEN) * 100

st.sidebar.divider()
st.sidebar.subheader("Skor Tim Pengkaji")

skor = {}
for indikator, bobot in BOBOT.items():
    skor[indikator] = st.sidebar.slider(
        f"{indikator} ({bobot}%)",
        0,
        100,
        75
    )

nilai_awal = sum(skor[i] * BOBOT[i] / 100 for i in BOBOT)

st.sidebar.divider()
st.sidebar.subheader("Simulasi Intervensi")

intervensi_dipilih = st.sidebar.multiselect(
    "Pilih intervensi kebijakan",
    list(INTERVENSI.keys())
)

bonus = sum(INTERVENSI[i] for i in intervensi_dipilih)
nilai_akhir = min(nilai_awal + bonus, 100)

# =====================
# STATUS
# =====================

def status_rekomendasi(nilai, dokumen):
    if dokumen < 100:
        return "Layak dengan Perbaikan", "Dokumen belum sepenuhnya lengkap."
    if nilai >= 80:
        return "Layak untuk Ditetapkan", "Calon Daerah Mitra dapat direkomendasikan untuk penetapan."
    if nilai >= 65:
        return "Layak dengan Perbaikan", "Calon Daerah Mitra memerlukan perbaikan terbatas."
    return "Belum Layak", "Calon Daerah Mitra memerlukan penguatan substansial."

status_awal, catatan_awal = status_rekomendasi(nilai_awal, kelengkapan_dokumen)
status_akhir, catatan_akhir = status_rekomendasi(nilai_akhir, kelengkapan_dokumen)

# =====================
# HEADER
# =====================

st.markdown('<div class="big-title">🎮 Gaming Simulation Daerah Mitra IKN</div>', unsafe_allow_html=True)
st.markdown('<p class="subtle">Simulasi penilaian calon Daerah Mitra IKN berbasis kriteria Perka OIKN Nomor 2 Tahun 2026 dan pedoman Tim Pengkaji.</p>', unsafe_allow_html=True)

st.divider()

# =====================
# EXECUTIVE DASHBOARD
# =====================

st.subheader("1. Executive Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Skor Awal", f"{nilai_awal:.1f}")
col2.metric("Skor Setelah Intervensi", f"{nilai_akhir:.1f}", f"+{bonus}")
col3.metric("Dokumen Lengkap", f"{len(dokumen_terpenuhi)}/{len(DOKUMEN)}")
col4.metric("Status Akhir", status_akhir)

col5, col6, col7, col8 = st.columns(4)

col5.metric("Estimasi Investasi", f"Rp {data['investasi']} T")
col6.metric("Tenaga Kerja", f"{data['tenaga_kerja']:,} orang")
col7.metric("Luas Kawasan", f"{data['luas']:,} ha")
col8.metric("Jumlah Klaster", len(data["klaster"]))

st.divider()

# =====================
# PROFIL KAWASAN
# =====================

st.subheader("2. Profil Calon Daerah Mitra")

col1, col2 = st.columns([2, 1])

with col1:
    st.write(f"**Nama Kawasan:** {pilihan_kawasan}")
    st.write(f"**Lokasi:** {data['lokasi']}")
    st.write(f"**Status Lokasi:** {data['status']}")
    st.write(f"**Pemrakarsa:** {pemrakarsa}")
    st.write(f"**Klaster SEN yang Didukung:** {', '.join(data['klaster'])}")

with col2:
    if status_akhir == "Layak untuk Ditetapkan":
        st.success(status_akhir)
    elif status_akhir == "Layak dengan Perbaikan":
        st.warning(status_akhir)
    else:
        st.error(status_akhir)

    st.write(catatan_akhir)

st.divider()

# =====================
# DOKUMEN
# =====================

st.subheader("3. Verifikasi Kelengkapan Dokumen")

dok_df = pd.DataFrame({
    "Dokumen": DOKUMEN,
    "Status": ["Ada" if d in dokumen_terpenuhi else "Belum Ada" for d in DOKUMEN]
})

st.dataframe(dok_df, width="stretch")

fig_doc = go.Figure(
    data=[
        go.Pie(
            labels=["Terpenuhi", "Belum Terpenuhi"],
            values=[len(dokumen_terpenuhi), len(DOKUMEN) - len(dokumen_terpenuhi)],
            hole=0.55
        )
    ]
)

fig_doc.update_layout(
    title="Kelengkapan Dokumen",
    height=350
)

st.plotly_chart(fig_doc, width="stretch")

st.divider()

# =====================
# SKOR TIM PENGKAJI
# =====================

st.subheader("4. Penilaian Tim Pengkaji")

penilaian_df = pd.DataFrame({
    "Indikator": list(BOBOT.keys()),
    "Bobot (%)": list(BOBOT.values()),
    "Skor": [skor[i] for i in BOBOT],
    "Nilai Tertimbang": [skor[i] * BOBOT[i] / 100 for i in BOBOT]
})

st.dataframe(penilaian_df, width="stretch")

fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(
    x=penilaian_df["Indikator"],
    y=penilaian_df["Nilai Tertimbang"],
    text=penilaian_df["Nilai Tertimbang"].round(1),
    textposition="auto"
))

fig_bar.update_layout(
    title="Nilai Tertimbang per Indikator",
    xaxis_title="Indikator",
    yaxis_title="Nilai Tertimbang",
    height=450
)

st.plotly_chart(fig_bar, width="stretch")

# Radar chart
fig_radar = go.Figure()

fig_radar.add_trace(go.Scatterpolar(
    r=[skor[i] for i in BOBOT],
    theta=list(BOBOT.keys()),
    fill="toself",
    name="Skor Kawasan"
))

fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
    title="Radar Chart Kesiapan Kawasan",
    height=500
)

st.plotly_chart(fig_radar, width="stretch")

st.divider()

# =====================
# SIMULASI INTERVENSI
# =====================

st.subheader("5. Simulasi Intervensi Kebijakan")

if intervensi_dipilih:
    intervensi_df = pd.DataFrame({
        "Intervensi": intervensi_dipilih,
        "Tambahan Skor": [INTERVENSI[i] for i in intervensi_dipilih]
    })

    st.dataframe(intervensi_df, width="stretch")
else:
    st.info("Belum ada intervensi dipilih.")

col1, col2, col3 = st.columns(3)
col1.metric("Skor Awal", f"{nilai_awal:.1f}")
col2.metric("Bonus Intervensi", f"+{bonus}")
col3.metric("Skor Akhir", f"{nilai_akhir:.1f}")

st.divider()

# =====================
# REKOMENDASI OTOMATIS
# =====================

st.subheader("6. Rekomendasi Otomatis")

rekomendasi_text = f"""
Berdasarkan hasil simulasi pengkajian calon Daerah Mitra IKN terhadap **{pilihan_kawasan}**, diperoleh skor awal sebesar **{nilai_awal:.1f}** dan skor setelah intervensi sebesar **{nilai_akhir:.1f}**. 

Kelengkapan dokumen mencapai **{kelengkapan_dokumen:.0f}%**, dengan status akhir **{status_akhir}**.

Dengan mempertimbangkan profil kawasan, dukungan terhadap klaster Superhub Ekonomi Nusantara, kesiapan dokumen, potensi investasi, serta hasil penilaian Tim Pengkaji, maka calon Daerah Mitra ini direkomendasikan sebagai berikut:

**{status_akhir}**

Catatan:
{catatan_akhir}
"""

st.info(rekomendasi_text)

# =====================
# GENERATOR NOTA DINAS
# =====================

st.subheader("7. Draft Ringkasan Nota Dinas")

nota_dinas = f"""
NOTA DINAS

Hal: Penyampaian Hasil Simulasi Pengkajian Calon Daerah Mitra IKN

Yth. Kepala Otorita Ibu Kota Nusantara

Dalam rangka mendukung pembangunan dan pengembangan Superhub Ekonomi Nusantara, telah dilakukan simulasi pengkajian terhadap calon Daerah Mitra IKN sebagai berikut:

1. Nama kawasan: {pilihan_kawasan}
2. Lokasi: {data['lokasi']}
3. Pemrakarsa: {pemrakarsa}
4. Luas kawasan: {data['luas']:,} hektare
5. Klaster yang didukung: {', '.join(data['klaster'])}
6. Estimasi investasi: Rp {data['investasi']} triliun
7. Estimasi penyerapan tenaga kerja: {data['tenaga_kerja']:,} orang
8. Skor awal pengkajian: {nilai_awal:.1f}
9. Skor setelah intervensi: {nilai_akhir:.1f}
10. Status rekomendasi: {status_akhir}

Berdasarkan hasil simulasi tersebut, {pilihan_kawasan} dinilai {status_akhir.lower()} sebagai calon Daerah Mitra IKN.

Demikian disampaikan, sebagai bahan pertimbangan lebih lanjut.
"""

st.text_area("Draft Nota Dinas", nota_dinas, height=420)

# =====================
# DOWNLOAD
# =====================

st.subheader("8. Download Hasil")

output = {
    "Tanggal": date.today(),
    "Kawasan": pilihan_kawasan,
    "Lokasi": data["lokasi"],
    "Pemrakarsa": pemrakarsa,
    "Luas Hektare": data["luas"],
    "Status Lokasi": data["status"],
    "Klaster": ", ".join(data["klaster"]),
    "Investasi Triliun Rupiah": data["investasi"],
    "Tenaga Kerja": data["tenaga_kerja"],
    "Dokumen Terpenuhi": len(dokumen_terpenuhi),
    "Total Dokumen": len(DOKUMEN),
    "Kelengkapan Dokumen Persen": kelengkapan_dokumen,
    "Skor Awal": nilai_awal,
    "Bonus Intervensi": bonus,
    "Skor Akhir": nilai_akhir,
    "Status Rekomendasi": status_akhir,
    "Catatan": catatan_akhir
}

output_df = pd.DataFrame([output])

csv = output_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Hasil Simulasi CSV",
    data=csv,
    file_name="hasil_simulasi_daerah_mitra_ikn.csv",
    mime="text/csv"
)

st.download_button(
    label="Download Draft Nota Dinas TXT",
    data=nota_dinas.encode("utf-8"),
    file_name="draft_nota_dinas_daerah_mitra_ikn.txt",
    mime="text/plain"
)
