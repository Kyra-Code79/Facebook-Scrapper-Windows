<div align="center">
  <img src="logo.png" alt="Logo Project" width="120" height="120">
  
  # FB Marketplace Scraper Indonesia V1
  
  **Tools Desktop Automation berbasis Python untuk mengambil data produk dari Facebook Marketplace secara massal.**
  
  Developed by **Kyra-Code**
  
  ---
</div>

## 📋 Deskripsi
Aplikasi desktop berbasis GUI (Graphical User Interface) untuk melakukan *scraping* data barang di Facebook Marketplace. Dibuat khusus untuk target lokasi kota-kota besar di **Indonesia**. 

Aplikasi ini menggunakan **Selenium** untuk automasi browser dan **BeautifulSoup** untuk parsing data, dibalut dengan tampilan modern menggunakan **CustomTkinter**.

## ✨ Fitur Utama
* **Modern GUI:** Tampilan antarmuka yang bersih dengan dukungan **Dark Mode / Light Mode**.
* **Responsive Layout:** Ukuran jendela fleksibel dan responsif.
* **Filter Pencarian Lengkap:**
    * Kata Kunci (Keyword).
    * Lokasi (Pilihan Kota-kota besar di Indonesia).
    * Range Harga (Minimum & Maksimum).
* **Smart Automation:**
    * **Login Detection:** Otomatis mendeteksi jika Facebook meminta login dan menunggu user login secara manual (aman dari blokir bot).
    * **Auto Scroll:** Melakukan scrolling otomatis untuk memuat produk.
* **Export Data:** Hasil scraping otomatis disimpan ke format **Excel (.xlsx)**.
* **Data Lengkap:** Mengambil Judul, Harga, Lokasi, Deskripsi, Link Produk, hingga estimasi RAM/ROM (untuk Handphone).
* **Tombol Stop:** Proses scraping bisa dibatalkan kapan saja tanpa merusak data yang sudah tersimpan.

## 🛠️ Teknologi yang Digunakan
* [Python](https://www.python.org/) - Bahasa Pemrograman utama.
* [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Untuk tampilan GUI modern.
* [Selenium](https://www.selenium.dev/) - Untuk mengontrol browser Chrome.
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) - Untuk parsing HTML.
* [Pandas](https://pandas.pydata.org/) - Untuk manajemen data dan export Excel.

## 🚀 Cara Instalasi (Pengguna Biasa)
1. **Release**
   Pilih Tulisan Release Sebelah Kanan
2. **Assets**
   Pilih Fb Scraper.Exe dan Download
3. **Jalankan Fb Scrapper**
   Jalankan Fb Scrapper, lalu masukkan perintah yang anda butuhkan
4. **Login Facebook pada Tab Chrome**
   Login terlebih dahulu untuk pertama kali ke facebook
5. **Program Berjalan**
   Program akan Berjalan, Tunggu hingga selesai
6. **Ulangi**
   Ketika program sudah selesai, anda tinggal menggunakan nya kembali tanpa harus login facebook kembali

## 🚀 Cara Instalasi (Developer)
Jika Anda ingin menjalankan atau mengedit source code-nya:
1.  **Clone Repository**
    ```bash
    git clone [https://github.com/username-kamu/nama-repo.git](https://github.com/username-kamu/nama-repo.git)
    cd nama-repo
    ```

2.  **Buat Virtual Environment**
    ```bash
    python -m venv venv
    venv\Scripts\activate  # Untuk Windows
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *(Pastikan library berikut terinstall: customtkinter, pandas, selenium, webdriver-manager, beautifulsoup4, pillow, openpyxl, packaging)*

4.  **Jalankan Aplikasi**
    ```bash
    python scraper_v2.py
    ```

## 📦 Cara Build ke .EXE
Aplikasi ini dapat diubah menjadi file Executable portable menggunakan **Auto-Py-To-Exe** atau **PyInstaller**.

**Command PyInstaller:**
```bash
pyinstaller --noconsole --onefile --windowed --icon=icon.ico --add-data "logo.png;." --collect-all customtkinter --hidden-import PIL --hidden-import Pillow scraper_v2.py
```
## DISCLAIMER
Tools ini dibuat untuk tujuan Edukasi dan Penelitian. Pengembang tidak bertanggung jawab atas penyalahgunaan aplikasi ini atau pelanggaran terhadap Ketentuan Layanan (ToS) Facebook. Gunakan dengan bijak dan bertanggung jawab.
© 2025 Kyra-Code. All rights reserved.
