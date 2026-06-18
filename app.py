import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Simulasi Pengkajian Daerah Mitra IKN",
    layout="wide"
)

st.title("🎮 Gaming Simulation: Pengkajian Calon Daerah Mitra IKN")
st.caption("Simulasi berbasis Perka OIKN Nomor 2 Tahun 2026 dan Kepka OIKN Nomor 77 Tahun 2026")

# =========================
# DATA DASAR
# =========================

PEMRAKARSA = [
    "Kementerian/Lembaga",
    "Pemerintah Daerah Provinsi",
    "Pemerintah Daerah Kabupaten/Kota",
    "Badan Usaha",
    "Otorita IKN"
]

KLASTER_EKONOMI = [
    "Industri Teknologi Bersih",
    "Farmasi Terintegrasi",
    "Industri Berbasis Pertanian Berkelanjutan",
    "Ekowisata dan Wisata Kebugaran Inklusif",
    "Industri Kimia Maju dan Turunannya",
    "Energi Rendah Karbon"
]

KLASTER_PEMAMPU = [
    "Pusat Pendidikan Abad ke-21",
    "Pusat Industri 4.0"
]

DOKUMEN_WAJIB = [
    "Surat pernyataan minat penetapan Daerah Mitra",
    "Surat pernyataan minat kerja sama dengan Kepala OIKN/Pemerintah Daerah",
    "Peta kartometrik lokasi calon Daerah Mitra",
    "Rencana tata ruang, pengaturan zonasi, dan/atau masterplan kawasan",
    "Studi kelayakan ekonomi dan finansial serta potensi ekonomi",
    "Rencana pengelolaan Daerah Mitra",
    "Rekomendasi dan komitmen dukungan tertulis dari Pemerintah Daerah",
    "Informasi status lahan yang jelas"
]

DOKUMEN_OPSIONAL = [
    "Surat penetapan lokasi sebagai kawasan industri/kawasan khusus/kawasan tertentu lainnya",
    "Akta pendirian badan usaha"
]

SUB_INDIKATOR = {
    "Kesesuaian Bidang Usaha dengan Superhub Ekonomi": 10,
    "Komitmen Dukungan Anggaran Pemerintah Daerah": 2,
    "Insentif Pajak, Retribusi, dan Kemudahan": 2,
    "Status Kepemilikan dan Sengketa Tanah": 1,
    "Kesesuaian dengan Rencana Tata Ruang Wilayah": 2,
    "Tercantum dalam Rencana Pembangunan Jangka Menengah Daerah": 2,
    "Penetapan Lokasi sebagai Kawasan Industri/Khusus/Tertentu": 1,
    "Ketersediaan Infrastruktur Dasar dan Logistik": 10,
    "Potensi Sumber Daya Alam dan Sektor Ekonomi": 10,
    "Potensi Sumber Daya Manusia": 10,
    "Kondisi Makro Ekonomi Lokal": 5,
    "Pengalaman Pengelola Kawasan": 5,
    "Rencana Pengembangan Infrastruktur dan Fasilitas Pendukung": 10,
    "Rencana Penyerapan Tenaga Kerja": 5,
    "Rencana Bisnis": 1,
    "Kelayakan Finansial": 5,
    "Kelayakan Ekonomi": 5,
    "Tahapan Pembangunan Daerah Mitra": 1,
    "Mitigasi Dampak Lingkungan": 2,
    "Pembiayaan Pengelolaan Daerah Mitra": 1
}

# =========================
# SIDEBAR INPUT
# =========================

st.sidebar.header("Input Profil Kawasan")

nama_kawasan = st.sidebar.text_input("Nama calon Daerah Mitra", "KPI/KI Kariangau")
lokasi = st.sidebar.text_input("Lokasi", "Kota Balikpapan, Kalimantan Timur")
pemrakarsa = st.sidebar.selectbox("Pemrakarsa", PEMRAKARSA)

luas = st.sidebar.number_input("Luas kawasan atau area usulan (hektare)", min_value=0.0, value=2000.0)

jenis_lokasi = st.sidebar.selectbox(
    "Status lokasi awal",
    [
        "Telah ditetapkan sebagai kawasan industri",
        "Telah ditetapkan sebagai kawasan khusus/strategis",
        "Kawasan tertentu lainnya",
        "Lokasi baru"
    ]
)

st.sidebar.divider()

st.sidebar.header("Kriteria Dasar Pasal 4")

sesuai_tata_ruang = st.sidebar.checkbox("Sesuai rencana tata ruang wilayah", value=True)
batas_jelas = st.sidebar.checkbox("Memiliki batas wilayah/area yang jelas dan peta memenuhi kaidah kartografi", value=True)
status_lahan_jelas = st.sidebar.checkbox("Status lahan jelas", value=True)
potensi_ekonomi = st.sidebar.checkbox("Memiliki potensi ekonomi mendukung pembangunan IKN", value=True)

klaster_ekonomi = st.sidebar.multiselect(
    "Klaster ekonomi yang didukung",
    KLASTER_EKONOMI,
    default=["Industri Teknologi Bersih", "Energi Rendah Karbon"]
)

klaster_pemampu = st.sidebar.multiselect(
    "Klaster pemampu yang didukung",
    KLASTER_PEMAMPU,
    default=["Pusat Industri 4.0"]
)

st.sidebar.divider()

st.sidebar.header("Kelengkapan Dokumen")

dokumen_ada = []
for dok in DOKUMEN_WAJIB:
    if st.sidebar.checkbox(dok, value=True):
        dokumen_ada.append(dok)

dokumen_opsional_ada = []
for dok in DOKUMEN_OPSIONAL:
    if st.sidebar.checkbox(dok, value=False):
        dokumen_opsional_ada.append(dok)

# =========================
# VERIFIKASI DOKUMEN
# =========================

dokumen_lengkap = len(dokumen_ada) == len(DOKUMEN_WAJIB)

kriteria_dasar_lengkap = all([
    sesuai_tata_ruang,
    batas_jelas,
    status_lahan_jelas,
    potensi_ekonomi,
    len(klaster_ekonomi) > 0,
    len(klaster_pemampu) > 0
])

# =========================
# PENILAIAN BERBOBOT
# =========================

st.header("1. Profil Usulan")

col1, col2, col3 = st.columns(3)
col1.metric("Calon Daerah Mitra", nama_kawasan)
col2.metric("Pemrakarsa", pemrakarsa)
col3.metric("Luas Kawasan", f"{luas:,.0f} ha")

st.write(f"**Lokasi:** {lokasi}")
st.write(f"**Status lokasi:** {jenis_lokasi}")

st.divider()

st.header("2. Verifikasi Awal")

col1, col2 = st.columns(2)

with col1:
    if dokumen_lengkap:
        st.success("Dokumen persyaratan lengkap. Usulan dapat dilanjutkan ke tahap pengkajian.")
    else:
        st.error("Dokumen belum lengkap. Usulan dikembalikan kepada pemrakarsa untuk dilengkapi.")

with col2:
    if kriteria_dasar_lengkap:
        st.success("Kriteria dasar lokasi terpenuhi.")
    else:
        st.warning("Masih terdapat kriteria dasar lokasi yang belum terpenuhi.")

dok_df = pd.DataFrame({
    "Dokumen Wajib": DOKUMEN_WAJIB,
    "Status": ["Ada" if d in dokumen_ada else "Tidak Ada" for d in DOKUMEN_WAJIB]
})

st.dataframe(dok_df, use_container_width=True)

st.divider()

st.header("3. Penilaian oleh Tim Pengkaji")

skor_input = {}

with st.expander("Isi skor sub indikator", expanded=True):
    for indikator, bobot in SUB_INDIKATOR.items():
        skor_input[indikator] = st.slider(
            f"{indikator} | Bobot {bobot}%",
            min_value=0,
            max_value=100,
            value=70
        )

hasil_penilaian = []

for indikator, bobot in SUB_INDIKATOR.items():
    nilai_tertimbang = skor_input[indikator] * bobot / 100
    hasil_penilaian.append({
        "Sub Indikator": indikator,
        "Bobot (%)": bobot,
        "Skor Input": skor_input[indikator],
        "Nilai Tertimbang": nilai_tertimbang
    })

df = pd.DataFrame(hasil_penilaian)
total_skor = df["Nilai Tertimbang"].sum()

st.dataframe(df, use_container_width=True)

col1, col2, col3 = st.columns(3)
col1.metric("Total Skor Pengkajian", f"{total_skor:.2f}")
col2.metric("Dokumen", "Lengkap" if dokumen_lengkap else "Belum Lengkap")
col3.metric("Kriteria Dasar", "Terpenuhi" if kriteria_dasar_lengkap else "Belum Terpenuhi")

st.bar_chart(df.set_index("Sub Indikator")["Nilai Tertimbang"])

st.divider()

st.header("4. Tahapan Gaming Simulation")

tahap = st.radio(
    "Pilih tahapan simulasi",
    [
        "Penilaian Dokumen",
        "Presentasi dan Wawancara",
        "Kunjungan Lapangan",
        "Perumusan Rekomendasi"
    ],
    horizontal=True
)

if tahap == "Penilaian Dokumen":
    st.info("Fokus: mengecek kesesuaian dokumen dengan kriteria Daerah Mitra dan pembobotan penilaian.")
elif tahap == "Presentasi dan Wawancara":
    st.info("Fokus: pendalaman substansi, klarifikasi dokumen, kesiapan kelembagaan, pendanaan, dan komitmen.")
elif tahap == "Kunjungan Lapangan":
    st.info("Fokus: verifikasi faktual kondisi lahan, batas kawasan, infrastruktur, kelembagaan, dan sumber daya manusia.")
else:
    st.info("Fokus: menyusun rekomendasi akhir kepada Kepala OIKN.")

st.divider()

st.header("5. Rekomendasi Simulasi")

if not dokumen_lengkap:
    status_rekomendasi = "Belum Layak"
    rekomendasi = "Dokumen persyaratan belum lengkap. Usulan perlu dikembalikan kepada pemrakarsa untuk dilengkapi."
elif not kriteria_dasar_lengkap:
    status_rekomendasi = "Layak dengan Perbaikan"
    rekomendasi = "Kriteria dasar lokasi belum sepenuhnya terpenuhi. Perlu pemenuhan aspek tata ruang, batas kawasan, status lahan, potensi ekonomi, atau dukungan klaster."
elif total_skor >= 80:
    status_rekomendasi = "Layak untuk Ditetapkan"
    rekomendasi = "Calon Daerah Mitra dinilai layak untuk direkomendasikan kepada Kepala OIKN."
elif total_skor >= 65:
    status_rekomendasi = "Layak dengan Perbaikan"
    rekomendasi = "Calon Daerah Mitra dapat dilanjutkan dengan pemenuhan persyaratan atau perbaikan tertentu."
else:
    status_rekomendasi = "Belum Layak"
    rekomendasi = "Calon Daerah Mitra belum layak untuk ditetapkan dan memerlukan penguatan substansial."

if status_rekomendasi == "Layak untuk Ditetapkan":
    st.success(status_rekomendasi)
elif status_rekomendasi == "Layak dengan Perbaikan":
    st.warning(status_rekomendasi)
else:
    st.error(status_rekomendasi)

st.write(rekomendasi)

isu_prioritas = df[df["Skor Input"] < 60].sort_values("Skor Input")

if not isu_prioritas.empty:
    st.subheader("Isu Prioritas Perbaikan")
    st.dataframe(isu_prioritas, use_container_width=True)

st.divider()

st.header("6. Output Simulasi")

output = {
    "Tanggal Simulasi": date.today(),
    "Nama Kawasan": nama_kawasan,
    "Lokasi": lokasi,
    "Pemrakarsa": pemrakarsa,
    "Luas": luas,
    "Status Lokasi": jenis_lokasi,
    "Dokumen Lengkap": dokumen_lengkap,
    "Kriteria Dasar Terpenuhi": kriteria_dasar_lengkap,
    "Total Skor": total_skor,
    "Status Rekomendasi": status_rekomendasi,
    "Rekomendasi": rekomendasi,
    "Klaster Ekonomi": ", ".join(klaster_ekonomi),
    "Klaster Pemampu": ", ".join(klaster_pemampu)
}

output_df = pd.DataFrame([output])

st.dataframe(output_df, use_container_width=True)

csv = output_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Hasil Simulasi",
    data=csv,
    file_name="hasil_simulasi_daerah_mitra_ikn.csv",
    mime="text/csv"
)
