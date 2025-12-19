import urllib.parse 
import customtkinter as ctk
import pandas as pd
import time
import os
import sys
from PIL import Image
import threading
import random
import re
from datetime import datetime
from tkinter import filedialog 

# Library Selenium & BS4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# --- KONFIGURASI TAMPILAN AWAL ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# --- FUNGSI PENTING (Agar gambar terbaca di dalam .exe) ---
def resource_path(relative_path):
    """ Dapatkan path absolut ke resource, bekerja untuk dev dan untuk PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class FBMarketplaceScraper(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("FB Marketplace Scraper V.1")
        self.geometry("750x850") 
        self.minsize(600, 700)   # Ukuran minimum agar UI tidak hancur

        # Grid Configuration agar Responsive
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.indonesia_cities = {
            "Jakarta": "jakarta", "Medan": "medan", "Surabaya": "surabaya",
            "Bandung": "bandung", "Deli Serdang": "deli-serdang", "Tanjung Morawa": "tanjung-morawa",
            "Binjai": "binjai", "Denpasar (Bali)": "denpasar", "Makassar": "makassar",
            "Semarang": "semarang", "Yogyakarta": "yogyakarta", "Palembang": "palembang",
            "Batam": "batam", "Pekanbaru": "pekanbaru", "Malang": "malang", "Bekasi": "bekasi",
            "Bogor": "bogor", "Depok": "depok", "Tangerang": "tangerang"
        }

        self.driver = None
        self.is_running = False
        self.stop_signal = False 

        self.create_widgets()

    def create_widgets(self):
        # --- 1. FRAME UTAMA (SCROLLABLE) ---
        self.main_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1) 

        # --- 2. HEADER (Toggle Mode & Logo) ---
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 20))

        # Toggle Light/Dark Mode (Pojok Kanan Atas)
        self.switch_mode = ctk.CTkSwitch(self.header_frame, text="Dark Mode", command=self.toggle_mode, onvalue="Dark", offvalue="Light")
        self.switch_mode.select() # Default Dark
        self.switch_mode.pack(side="right", padx=10)

        # Logo & Judul (Center)
        try:
            image_path = resource_path("logo.png")
            my_image = ctk.CTkImage(light_image=Image.open(image_path), 
                                    dark_image=Image.open(image_path), 
                                    size=(80, 80))
            self.logo_label = ctk.CTkLabel(self.header_frame, image=my_image, text="")
            self.logo_label.pack(side="top")
        except: pass

        self.label_title = ctk.CTkLabel(self.header_frame, text="FB Marketplace Scraper V.1", font=("Arial", 24, "bold"))
        self.label_title.pack(side="top", pady=5)

        # --- 3. FORM INPUT (Responsive) ---
        self.form_frame = ctk.CTkFrame(self.main_frame)
        self.form_frame.pack(fill="x", padx=10, pady=10)
        self.form_frame.grid_columnconfigure(1, weight=1)

        # --- Kata Kunci ---
        ctk.CTkLabel(self.form_frame, text="Kata Kunci:", anchor="w").grid(row=0, column=0, padx=15, pady=10, sticky="w")
        self.entry_query = ctk.CTkEntry(self.form_frame, placeholder_text="Contoh: iPhone 11, Laptop Gaming...")
        self.entry_query.grid(row=0, column=1, padx=15, pady=10, sticky="ew")

        # --- Kota ---
        ctk.CTkLabel(self.form_frame, text="Lokasi:", anchor="w").grid(row=1, column=0, padx=15, pady=10, sticky="w")
        self.combo_location = ctk.CTkComboBox(self.form_frame, values=list(self.indonesia_cities.keys()))
        self.combo_location.set("Medan")
        self.combo_location.grid(row=1, column=1, padx=15, pady=10, sticky="ew")

        # --- Range Harga (Dual Input) ---
        ctk.CTkLabel(self.form_frame, text="Harga (Rp):", anchor="w").grid(row=2, column=0, padx=15, pady=10, sticky="w")
        
        self.price_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.price_frame.grid(row=2, column=1, padx=15, pady=10, sticky="ew")
        
        self.entry_min_price = ctk.CTkEntry(self.price_frame, placeholder_text="Min (Cth: 100000)")
        self.entry_min_price.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        ctk.CTkLabel(self.price_frame, text="-").pack(side="left")
        
        self.entry_max_price = ctk.CTkEntry(self.price_frame, placeholder_text="Max (Cth: 5000000)")
        self.entry_max_price.pack(side="left", fill="x", expand=True, padx=(5, 0))

        # --- Limit ---
        ctk.CTkLabel(self.form_frame, text="Jumlah Data:", anchor="w").grid(row=3, column=0, padx=15, pady=10, sticky="w")
        self.entry_limit = ctk.CTkEntry(self.form_frame, placeholder_text="Contoh: 50")
        self.entry_limit.grid(row=3, column=1, padx=15, pady=10, sticky="ew")

        # --- FILE OUTPUT (Browse Button) ---
        ctk.CTkLabel(self.form_frame, text="Simpan File:", anchor="w").grid(row=4, column=0, padx=15, pady=10, sticky="w")
        
        self.file_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.file_frame.grid(row=4, column=1, padx=15, pady=10, sticky="ew")
        
        self.entry_filename = ctk.CTkEntry(self.file_frame, placeholder_text="Klik tombol cari folder...")
        self.entry_filename.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.btn_browse = ctk.CTkButton(self.file_frame, text="📁 Cari Folder", width=100, command=self.browse_file)
        self.btn_browse.pack(side="right")

        # --- Opsi Tambahan ---
        self.var_deskripsi = ctk.BooleanVar(value=True)
        self.check_deskripsi = ctk.CTkCheckBox(self.main_frame, text="Ambil Deskripsi Lengkap & Deteksi RAM/ROM (Lebih Lambat)", variable=self.var_deskripsi, text_color="orange")
        self.check_deskripsi.pack(pady=10)

        # --- TOMBOL ACTION ---
        self.btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.btn_frame.pack(pady=20, fill="x")

        self.btn_start = ctk.CTkButton(self.btn_frame, text="MULAI SCRAPING", command=self.start_scraping_thread, fg_color="#1877F2", height=50, font=("Arial", 16, "bold"))
        self.btn_start.pack(side="left", fill="x", expand=True, padx=10)

        self.btn_stop = ctk.CTkButton(self.btn_frame, text="STOP", command=self.stop_scraping, fg_color="#D9534F", hover_color="#C9302C", width=100, height=50, font=("Arial", 14, "bold"), state="disabled")
        self.btn_stop.pack(side="right", padx=10)

        # --- LOGGING AREA ---
        ctk.CTkLabel(self.main_frame, text="Log Aktivitas:", anchor="w").pack(fill="x", padx=15)
        self.textbox_log = ctk.CTkTextbox(self.main_frame, height=200)
        self.textbox_log.pack(fill="x", padx=15, pady=(0, 10))
        self.textbox_log.insert("0.0", "Siap...\n")

    # --- FUNGSI UI BARU ---
    def toggle_mode(self):
        mode = self.switch_mode.get() # 'Dark' atau 'Light'
        ctk.set_appearance_mode(mode)
        if mode == "Dark":
            self.switch_mode.configure(text="Dark Mode")
        else:
            self.switch_mode.configure(text="Light Mode")

    def browse_file(self):
        # Buka dialog save file
        filename = filedialog.asksaveasfilename(
            initialdir="/",
            title="Simpan Data Excel",
            initialfile="data_hp.xlsx",
            filetypes=(("Excel Files", "*.xlsx"), ("All Files", "*.*"))
        )
        if filename:
            self.entry_filename.delete(0, "end")
            self.entry_filename.insert(0, filename)

    # --- LOGIKA SYSTEM ---
    def log(self, message):
        self.textbox_log.insert("end", f"> {message}\n")
        self.textbox_log.see("end")

    def extract_spec(self, text):
        if not text: return "N/A"
        text = text.lower().replace('\n', ' ').strip()
        match_slash = re.search(r'\b(\d{1,2})\s?/\s?(\d{2,3})\b', text)
        if match_slash: return f"{match_slash.group(1)}/{match_slash.group(2)}"
        match_plus = re.search(r'\b(\d{1,2})\s?\+\s?(\d{2,3})\b', text)
        if match_plus: return f"{match_plus.group(1)}/{match_plus.group(2)}"
        match_ram = re.search(r'ram\s?(\d{1,2})', text)
        match_rom = re.search(r'(?:rom|internal|memori)\s?(\d{2,3})', text)
        if match_ram and match_rom: return f"{match_ram.group(1)}/{match_rom.group(1)}"
        if match_ram: return f"{match_ram.group(1)}GB (RAM Only)"
        return "N/A"

    def start_scraping_thread(self):
        if not self.is_running:
            self.is_running = True
            self.stop_signal = False 
            self.btn_start.configure(state="disabled") 
            self.btn_stop.configure(state="normal") 
            threading.Thread(target=self.run_scraper, daemon=True).start()

    def stop_scraping(self):
        if self.is_running:
            self.stop_signal = True
            self.log("⚠️ PERMINTAAN STOP DITERIMA! Sedang menyelesaikan proses terakhir...")
            self.btn_stop.configure(state="disabled")

    def run_scraper(self):
        query = self.entry_query.get()
        city_name = self.combo_location.get()
        location_slug = self.indonesia_cities.get(city_name, "medan")
        limit_str = self.entry_limit.get()
        filename = self.entry_filename.get()
        min_price = self.entry_min_price.get()
        max_price = self.entry_max_price.get()
        need_description = self.var_deskripsi.get()

        if not query or not limit_str or not filename:
            self.log("Error: Mohon isi semua kolom (termasuk lokasi simpan file).")
            self.reset_ui_state()
            return
        
        try:
            limit = int(limit_str)
        except: 
            self.log("Error: Jumlah item harus angka.")
            self.reset_ui_state()
            return

        self.log("Membuka Browser...")
        options = Options()
        options.add_argument("--disable-notifications")
        options.add_argument("--start-maximized")
        current_dir = os.getcwd()
        options.add_argument(f"user-data-dir={os.path.join(current_dir, 'chrome_profile')}") 

        try:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            safe_query = urllib.parse.quote(query) 
            base_url = f"https://www.facebook.com/marketplace/{location_slug}/search?query={safe_query}"
            if min_price and min_price.isdigit(): base_url += f"&minPrice={min_price}"
            if max_price and max_price.isdigit(): base_url += f"&maxPrice={max_price}"
            
            self.log(f"Target: {city_name} | Harga: {min_price}-{max_price}")
            self.driver.get(base_url)
            time.sleep(3) 

            if self.stop_signal: raise Exception("Proses dibatalkan oleh user.")

            # --- DETEKSI LOGIN ---
            if "login" in self.driver.current_url or "Log into Facebook" in self.driver.title:
                self.log("⚠️ BUTUH LOGIN! Silakan login di browser sekarang (Max 5 menit).")
                max_wait = 300 
                waited = 0
                while waited < max_wait:
                    if self.stop_signal: raise Exception("Login dibatalkan user.")
                    if "login" not in self.driver.current_url and "Log into Facebook" not in self.driver.title:
                        self.log("✅ Login sukses!")
                        break
                    time.sleep(2)
                    waited += 2
                    if waited % 10 == 0: self.log(f"Menunggu login... ({waited}s)")
                
                self.log("Redirect kembali ke pencarian...")
                self.driver.get(base_url)
                time.sleep(5)

            extracted_data = []

            # --- MODE DETAIL ---
            if need_description:
                self.log("Mengumpulkan link produk...")
                links = set()
                scroll_attempts = 0
                last_height = self.driver.execute_script("return document.body.scrollHeight")
                
                while len(links) < limit:
                    if self.stop_signal: break 

                    soup = BeautifulSoup(self.driver.page_source, "html.parser")
                    items = soup.find_all('a', href=True)
                    for a in items:
                        if '/marketplace/item/' in a['href']:
                            full_link = "https://www.facebook.com" + a['href'].split("?")[0]
                            links.add(full_link)
                            if len(links) >= limit: break
                    
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(3)
                    new_height = self.driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        scroll_attempts += 1
                        if scroll_attempts > 4: break
                    else:
                        last_height = new_height
                        scroll_attempts = 0

                link_list = list(links)[:limit]
                self.log(f"Mulai scan detail {len(link_list)} produk...")

                for i, link in enumerate(link_list):
                    if self.stop_signal: 
                        self.log("Scraping dihentikan user.")
                        break

                    try:
                        self.log(f"[{i+1}/{len(link_list)}] Mengambil data...")
                        self.driver.get(link)
                        time.sleep(random.uniform(3, 5)) # Sedikit dipercepat
                        
                        soup_detail = BeautifulSoup(self.driver.page_source, "html.parser")
                        
                        title = "N/A"
                        h1 = soup_detail.find('h1')
                        if h1: title = h1.text.strip()
                        
                        price = "N/A"
                        spans = soup_detail.find_all('span')
                        for sp in spans:
                            txt = sp.text.strip()
                            if ("Rp" in txt or txt.replace('.','').isdigit()) and len(txt) < 18:
                                price = txt
                                break

                        desc = "Tidak ada deskripsi"
                        desc_divs = soup_detail.find_all('div', attrs={"dir": "auto"})
                        for d in desc_divs:
                            if len(d.text) > 30 and d.text != title:
                                desc = d.text.strip()
                                break
                        if desc == "Tidak ada deskripsi":
                             text_blocks = soup_detail.get_text(separator="\n").split("\n")
                             longest = max(text_blocks, key=len) if text_blocks else ""
                             if len(longest) > 50: desc = longest

                        ram_rom = self.extract_spec(f"{title} {desc}")
                        
                        img_url = "N/A"
                        imgs = soup_detail.find_all('img')
                        for img in imgs:
                            if img.has_attr('src') and "https" in img['src'] and "p200x200" not in img['src']:
                                img_url = img['src']
                                break
                        
                        extracted_data.append({
                            "Kata Kunci": query, "Judul": title, "RAM/ROM": ram_rom, "Harga": price,
                            "Lokasi": city_name, "Deskripsi": desc, "Link": link, "Gambar": img_url,
                            "Waktu": datetime.now().strftime("%H:%M:%S")
                        })

                    except Exception as e: continue

            # --- MODE CEPAT ---
            else:
                self.log("Mode Cepat berjalan...")
                scroll_attempts = 0
                while len(extracted_data) < limit:
                    if self.stop_signal: break

                    soup = BeautifulSoup(self.driver.page_source, "html.parser")
                    items = [a for a in soup.find_all('a', href=True) if '/marketplace/item/' in a['href']]
                    for item in items:
                        if len(extracted_data) >= limit: break
                        try:
                            link = "https://www.facebook.com" + item['href'].split("?")[0]
                            text_content = item.get_text(separator="|").strip()
                            parts = [p for p in text_content.split("|") if p.strip()]
                            
                            title = parts[0] if parts else "N/A"
                            price = "N/A"
                            for p in parts:
                                if "Rp" in p: price = p

                            extracted_data.append({
                                "Kata Kunci": query, "Judul": title, "RAM/ROM": self.extract_spec(title),
                                "Harga": price, "Lokasi": city_name, "Deskripsi": "- (Mode Cepat)", 
                                "Link": link, "Gambar": "N/A", "Waktu": datetime.now().strftime("%H:%M:%S")
                            })
                        except: continue
                    
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(3)
                    if self.driver.execute_script("return document.body.scrollHeight") == scroll_attempts: break 
                    scroll_attempts = self.driver.execute_script("return document.body.scrollHeight")

            # --- SIMPAN DATA ---
            if extracted_data:
                self.log(f"Menyimpan {len(extracted_data)} data ke Excel...")
                df = pd.DataFrame(extracted_data)
                
                # Pastikan format .xlsx
                if not filename.endswith(".xlsx"): filename += ".xlsx"
                
                if os.path.exists(filename):
                     with pd.ExcelWriter(filename, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                        try:
                            reader = pd.read_excel(filename)
                            df.to_excel(writer, index=False, header=False, startrow=len(reader) + 1)
                        except: df.to_excel(writer, index=False)
                else:
                    df.to_excel(filename, index=False)
                
                self.log(f"✅ Selesai! File tersimpan di:\n{filename}")
            else:
                self.log("⚠️ Tidak ada data yang berhasil diambil.")
            
            self.driver.quit()
            self.reset_ui_state()

        except Exception as e:
            self.log(f"Status/Error: {e}")
            self.reset_ui_state()
            if self.driver: self.driver.quit()

    def reset_ui_state(self):
        self.is_running = False
        self.stop_signal = False
        self.btn_start.configure(state="normal")
        self.btn_stop.configure(state="disabled")
        self.log("--- Siap untuk tugas berikutnya ---")

if __name__ == "__main__":
    app = FBMarketplaceScraper()
    app.mainloop()