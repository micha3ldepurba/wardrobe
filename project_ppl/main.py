import os
import json
import random
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

DB_FILE = "wardrobe_db.json"
IMAGE_FOLDER = "images"

def get_or_create_local_database(image_folder):
    """Membangun database lokal secara instan berdasarkan nama file gambar."""
    if not os.path.exists(image_folder):
        os.makedirs(image_folder, exist_ok=True)

    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.png', '.jpeg', '.webp'))]
    
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    database = []
    for idx, filename in enumerate(image_files, start=1):
        kategori = "atasan" if "atasan" in filename.lower() else "bawahan"
        
        warna = "netral"
        if any(c in filename.lower() for c in ['pink', 'merah', 'cokelat', 'khaki', 'mustard']):
            warna = "hangat"
        elif any(c in filename.lower() for c in ['navy', 'biru', 'abu', 'olive']):
            warna = "dingin"

        clean_name = filename.replace('.jpg', '').replace('.png', '').replace('_', ' ').title()

        database.append({
            "id_pakaian": idx,
            "file_name": filename,
            "file_path": os.path.join(image_folder, filename),
            "nama_item": clean_name,
            "kategori": kategori,
            "kelompok_warna": warna
        })

    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(database, f, indent=4, ensure_ascii=False)
        
    return database

class WardrobeApp:
    def __init__(self, root, database):
        self.root = root
        self.root.title("WardrobeIn - Smart Outfit Stylist")
        self.root.geometry("880x680")
        self.root.configure(bg="#f5f6fa")

        self.database = database
        self.atasan_list = [item for item in self.database if "atasan" in item['kategori']]
        self.bawahan_list = [item for item in self.database if "bawahan" in item['kategori']]

        self.selected_atasan_var = tk.StringVar()
        self.selected_bawahan_var = tk.StringVar()

        self.setup_ui()

    def setup_ui(self):
        # Header Judul
        header_frame = tk.Frame(self.root, bg="#2f3640", pady=12)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(header_frame, text="✨ WardrobeIn - Smart Color & Model Matching ✨", fg="white", bg="#2f3640", font=("Arial", 16, "bold"))
        title_label.pack()

        main_frame = tk.Frame(self.root, bg="#f5f6fa", padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- KOLOM KIRI: KONTROL & TOMBOL ---
        left_frame = tk.LabelFrame(main_frame, text=" Panel Kontrol Pakaian ", bg="#f5f6fa", font=("Arial", 11, "bold"), padx=12, pady=12)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Pilihan Atasan
        tk.Label(left_frame, text="Pilih Atasan:", bg="#f5f6fa", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5, 2))
        self.atasan_combo = ttk.Combobox(left_frame, textvariable=self.selected_atasan_var, state="readonly", width=38)
        self.atasan_combo['values'] = [item['nama_item'] for item in self.atasan_list]
        self.atasan_combo.pack(anchor="w", pady=(0, 5))
        self.atasan_combo.bind("<<ComboboxSelected>>", lambda e: self.update_display(update_reason=False))

        # Tombol Find Match untuk Atasan
        btn_match_atasan = tk.Button(left_frame, text="🔍 Cari Pasangan untuk Atasan Ini (Find Match)", bg="#0984e3", fg="white", font=("Arial", 9), command=self.find_match_for_atasan)
        btn_match_atasan.pack(fill=tk.X, pady=(0, 15))

        # Pilihan Bawahan
        tk.Label(left_frame, text="Pilih Bawahan:", bg="#f5f6fa", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5, 2))
        self.bawahan_combo = ttk.Combobox(left_frame, textvariable=self.selected_bawahan_var, state="readonly", width=38)
        self.bawahan_combo['values'] = [item['nama_item'] for item in self.bawahan_list]
        self.bawahan_combo.pack(anchor="w", pady=(0, 5))
        self.bawahan_combo.bind("<<ComboboxSelected>>", lambda e: self.update_display(update_reason=False))

        # Tombol Find Match untuk Bawahan
        btn_match_bawahan = tk.Button(left_frame, text="🔍 Cari Pasangan untuk Bawahan Ini (Find Match)", bg="#0984e3", fg="white", font=("Arial", 9), command=self.find_match_for_bawahan)
        btn_match_bawahan.pack(fill=tk.X, pady=(0, 20))

        # Tombol Rekomendasi Pintar AI (Pure Matching Berdasarkan Tone & Model)
        rec_btn = tk.Button(left_frame, text="⚡ Rekomendasi Pintar (Color & Model Matching)", bg="#4cd137", fg="white", font=("Arial", 10, "bold"), pady=8, command=self.smart_ai_recommendation)
        rec_btn.pack(fill=tk.X, pady=(5, 10))

        # Label Alasan Stylist
        tk.Label(left_frame, text="Analisis & Catatan Stylist:", bg="#f5f6fa", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 2))
        self.alasan_text = tk.Text(left_frame, height=5, width=35, wrap=tk.WORD, font=("Arial", 9))
        self.alasan_text.pack(fill=tk.BOTH, expand=True)
        self.alasan_text.config(state=tk.DISABLED)

        # --- KOLOM KANAN: PREVIEW GAMBAR ---
        right_frame = tk.LabelFrame(main_frame, text=" Preview Visual Pakaian ", bg="#f5f6fa", font=("Arial", 11, "bold"), padx=12, pady=12)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        img_atasan_frame = tk.Frame(right_frame, bg="#ffffff", bd=1, relief=tk.SOLID)
        img_atasan_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(0, 5))
        tk.Label(img_atasan_frame, text="Atasan Terpilih", bg="#ffffff", font=("Arial", 9, "italic")).pack(anchor="nw", padx=5, pady=2)
        
        self.lbl_img_atasan = tk.Label(img_atasan_frame, bg="#ffffff")
        self.lbl_img_atasan.pack(fill=tk.BOTH, expand=True, pady=5)

        img_bawahan_frame = tk.Frame(right_frame, bg="#ffffff", bd=1, relief=tk.SOLID)
        img_bawahan_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, pady=(5, 0))
        tk.Label(img_bawahan_frame, text="Bawahan Terpilih", bg="#ffffff", font=("Arial", 9, "italic")).pack(anchor="nw", padx=5, pady=2)
        
        self.lbl_img_bawahan = tk.Label(img_bawahan_frame, bg="#ffffff")
        self.lbl_img_bawahan.pack(fill=tk.BOTH, expand=True, pady=5)

        if self.atasan_list and self.bawahan_list:
            self.atasan_combo.current(0)
            self.bawahan_combo.current(0)
            self.update_display(update_reason=True)

    def load_image(self, path):
        try:
            img = Image.open(path)
            img = img.resize((170, 170), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception:
            return None

    def update_display(self, update_reason=True):
        selected_atasan_name = self.selected_atasan_var.get()
        selected_bawahan_name = self.selected_bawahan_var.get()

        atasan_item = next((item for item in self.atasan_list if item['nama_item'] == selected_atasan_name), None)
        bawahan_item = next((item for item in self.bawahan_list if item['nama_item'] == selected_bawahan_name), None)

        if atasan_item and os.path.exists(atasan_item['file_path']):
            self.img_atasan_tk = self.load_image(atasan_item['file_path'])
            self.lbl_img_atasan.config(image=self.img_atasan_tk)
        else:
            self.lbl_img_atasan.config(image='', text="Gambar tidak ditemukan")

        if bawahan_item and os.path.exists(bawahan_item['file_path']):
            self.img_bawahan_tk = self.load_image(bawahan_item['file_path'])
            self.lbl_img_bawahan.config(image=self.img_bawahan_tk)
        else:
            self.lbl_img_bawahan.config(image='', text="Gambar tidak ditemukan")

        if update_reason and atasan_item and bawahan_item:
            alasan = f"Memadukan {atasan_item['nama_item']} ({atasan_item['kelompok_warna']}) dengan {bawahan_item['nama_item']} ({bawahan_item['kelompok_warna']})."
            self.set_alasan(alasan)

    def set_alasan(self, text):
        self.alasan_text.config(state=tk.NORMAL)
        self.alasan_text.delete("1.0", tk.END)
        self.alasan_text.insert(tk.END, text)
        self.alasan_text.config(state=tk.DISABLED)

    def calculate_match_score(self, atasan, bawahan):
        """Menghitung skor kecocokan berdasarkan Color Tone dan Kategori Model Pakaian."""
        score = 0
        t_a = atasan['kelompok_warna']
        t_b = bawahan['kelompok_warna']
        
        # 1. Aturan Pencocokan Warna (Color Tone)
        if t_a == 'netral' or t_b == 'netral':
            score += 50  
        elif t_a == t_b:
            score += 40  
        else:
            score += 15  
            
        # 2. Aturan Kesesuaian Model / Gaya Pakaian
        nama_a = atasan['nama_item'].lower()
        nama_b = bawahan['nama_item'].lower()
        
        is_formal_a = any(k in nama_a for k in ['blouse', 'linen', 'formal', 'kemeja'])
        is_formal_b = any(k in nama_b for k in ['formal', 'wide leg', 'rok plisket', 'chinos'])
        
        is_casual_a = any(k in nama_a for k in ['kaos', 'crop', 'hoodie', 'sweater'])
        is_casual_b = any(k in nama_b for k in ['sweatpants', 'cargo', 'shorts', 'jeans', 'denim'])

        if (is_formal_a and is_formal_b) or (is_casual_a and is_casual_b):
            score += 40  
        else:
            score += 20  
            
        return score

    def find_match_for_atasan(self):
        selected_atasan_name = self.selected_atasan_var.get()
        atasan_item = next((item for item in self.atasan_list if item['nama_item'] == selected_atasan_name), None)
        
        if not atasan_item:
            messagebox.showwarning("Peringatan", "Pilih atasan terlebih dahulu!")
            return

        best_match = None
        highest_score = -1
        for bawahan in self.bawahan_list:
            score = self.calculate_match_score(atasan_item, bawahan)
            if score > highest_score:
                highest_score = score
                best_match = bawahan

        self.selected_bawahan_var.set(best_match['nama_item'])
        self.update_display(update_reason=False)
        
        alasan = f"🔍 [Smart Find Match]\nAtasan '{atasan_item['nama_item']}' ({atasan_item['kelompok_warna']}) dipasangkan dengan '{best_match['nama_item']}' ({best_match['kelompok_warna']}).\nAlasan: Kecocokan tone warna dan model pakaian teruji selaras."
        self.set_alasan(alasan)

    def find_match_for_bawahan(self):
        selected_bawahan_name = self.selected_bawahan_var.get()
        bawahan_item = next((item for item in self.bawahan_list if item['nama_item'] == selected_bawahan_name), None)
        
        if not bawahan_item:
            messagebox.showwarning("Peringatan", "Pilih bawahan terlebih dahulu!")
            return

        best_match = None
        highest_score = -1
        for atasan in self.atasan_list:
            score = self.calculate_match_score(atasan, bawahan_item)
            if score > highest_score:
                highest_score = score
                best_match = atasan

        self.selected_atasan_var.set(best_match['nama_item'])
        self.update_display(update_reason=False)
        
        alasan = f"🔍 [Smart Find Match]\nBawahan '{bawahan_item['nama_item']}' ({bawahan_item['kelompok_warna']}) dipasangkan dengan '{best_match['nama_item']}' ({best_match['kelompok_warna']}).\nAlasan: Kombinasi model dan warna dipilih berdasarkan skor keserasian tertinggi."
        self.set_alasan(alasan)

    def smart_ai_recommendation(self):
        if not self.atasan_list or not self.bawahan_list:
            messagebox.showerror("Error", "Data lemari kosong!")
            return

        best_pair = None
        highest_total_score = -1
        
        for atasan in self.atasan_list:
            for bawahan in self.bawahan_list:
                score = self.calculate_match_score(atasan, bawahan)
                if score > highest_total_score:
                    highest_total_score = score
                    best_pair = (atasan, bawahan)

        atasan_pilihan, bawahan_pilihan = best_pair

        self.selected_atasan_var.set(atasan_pilihan['nama_item'])
        self.selected_bawahan_var.set(bawahan_pilihan['nama_item'])
        self.update_display(update_reason=False)
        
        alasan = f"⚡ [Smart AI Pure Recommendation]\nSistem memilihkan setelan terbaik berdasarkan analisis Color Tone & Model:\n• Atasan: {atasan_pilihan['nama_item']} ({atasan_pilihan['kelompok_warna']})\n• Bawahan: {bawahan_pilihan['nama_item']} ({bawahan_pilihan['kelompok_warna']})\n\nKombinasi ini memiliki skor harmoni tertinggi di lemari Anda!"
        self.set_alasan(alasan)

if __name__ == "__main__":
    database_lemari = get_or_create_local_database(IMAGE_FOLDER)

    if not database_lemari:
        print("Folder gambar kosong!")
    else:
        root = tk.Tk()
        app = WardrobeApp(root, database_lemari)
        root.mainloop()