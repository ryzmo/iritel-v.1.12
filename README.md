# Smart Retail and Consumer Behavior Analysis

Sistem ini merupakan solusi berbasis **Computer Vision dan AI** untuk menganalisis **interaksi pelanggan di toko ritel** (seperti Indomaret atau Alfamart), menggunakan kamera, deteksi manusia (YOLOv5), dan analitik perilaku berbasis waktu.

---

## Tujuan Proyek

1. Mendeteksi keberadaan pelanggan di depan **zona rak tertentu**
2. Mengukur **durasi interaksi** setiap pelanggan di tiap rak
3. Menyimpan data secara otomatis ke **file log (CSV)**
4. Menyediakan **dashboard visualisasi** real-time (jumlah interaksi, durasi, dan log data)
5. Menggunakan **Gemini AI** (Google) untuk menghasilkan **analisis dan insight otomatis** dari data

---

## Arsitektur Sistem

```
Kamera Laptop/Webcam
        ↓
   YOLOv5 (Deteksi Person)
        ↓
 Zona Rak A & B (Tracking Lokasi)
        ↓
  Hitung Waktu Interaksi
        ↓
  Log ke CSV → Dashboard + Gemini AI
```

---

## Teknologi yang Digunakan

| Komponen      | Teknologi                                       |
| ------------- | ----------------------------------------------- |
| Deteksi Objek | [YOLOv5](https://github.com/ultralytics/yolov5) |
| Video Capture | OpenCV                                          |
| Dashboard     | Streamlit                                       |
| Analisis AI   | Google Gemini (via API)                         |
| Data Log      | CSV                                             |
| Bahasa        | Python 3.10+                                    |

---

## Struktur Folder

```
project/
│
├── interaksi_log.csv           # File log otomatis
├── deteksi_interaksi.py        # YOLOv5 + OpenCV real-time tracker
├── dashboard_interaksi.py      # Dashboard Streamlit + Gemini AI
├── README.md                   # Dokumentasi proyek
└── requirements.txt            # (opsional) daftar dependencies
```

---

## Instalasi

### 1. Pastikan sudah berada di folder ini

```bash
cd iritel-v.1.12
```

### 2. Buat Virtual Environment (opsional tapi disarankan)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install dependencies (optional, harusnya tanpa install ini langsung run saja bisa)

```bash
pip install -r requirements.txt
```

Jika belum ada `requirements.txt`, kamu bisa install manual:

```bash
pip install opencv-python torch streamlit pandas matplotlib google-generativeai
```

---

## Menjalankan Program

### 1. Jalankan Deteksi Kamera

```bash
python deteksi_interaksi.py
```

> Kamera akan menyala. Jika ada orang masuk ke zona Rak A atau B, durasi interaksi akan dicatat ke `interaksi_log.csv`.

### 2. Jalankan Dashboard Streamlit

```bash
streamlit run dashboard_interaksi.py
```

> Dashboard akan terbuka di browser dan menampilkan data + insight Gemini secara real-time.

---

## Contoh Insight dari Gemini AI

> "Pelanggan lebih sering berinteraksi dengan Rak A, tetapi durasi interaksi lebih tinggi di Rak B. Produk impulsif disarankan di Rak A, dan produk high-involvement di Rak B."

---

## Hasil Dashboard

* Jumlah interaksi per rak
* Rata-rata durasi
* Tabel riwayat interaksi
* Analisis cerdas dari Gemini AI (langsung dari data CSV)