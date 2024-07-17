import tkinter as tk
from tkinter import ttk
import firebase_admin
from firebase_admin import credentials, db

# Firebase Admin SDK ile bağlantı kurma
cred = credentials.Certificate('.init/firebaseAdmin.json')  # Bu dosyanın doğru yolunu belirtin
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://depo-envanter-default-rtdb.firebaseio.com/'
})

class DepoYonetimiUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Depo Yönetimi")

        # Ana çerçeve oluştur
        main_frame = tk.Frame(root, bg='white', padx=20, pady=20, bd=20, relief="ridge")
        main_frame.pack(padx=20, pady=20)

        # Malzeme listesi için bir tablo oluşturuyoruz
        self.tree = ttk.Treeview(main_frame, columns=('Malzeme Adı', 'Miktar', 'Depo Lokasyonu', 'Son Güncelleme'))
        self.tree.heading('#0', text='ID')
        self.tree.heading('#1', text='Malzeme Adı')
        self.tree.heading('#2', text='Miktar')
        self.tree.heading('#3', text='Depo Lokasyonu')
        self.tree.heading('#4', text='Son Güncelleme')
        self.tree.pack(padx=10, pady=10)

        # Firebase'den verileri çekip tabloya ekleyelim
        self.load_data_from_firebase()

        # Malzeme hareketi kayıt formu
        self.malzeme_adi = tk.StringVar()
        self.miktar_degisimi = tk.IntVar()
        self.depo_lokasyonu = tk.StringVar()
        self.islem_tarihi = tk.StringVar()

        # Etiketler ve giriş alanları
        form_frame = tk.Frame(main_frame, bg='white')
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Malzeme Adı:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        tk.Entry(form_frame, textvariable=self.malzeme_adi).grid(row=0, column=1, padx=10, pady=5)
        tk.Label(form_frame, text="Miktar Değişimi:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        tk.Entry(form_frame, textvariable=self.miktar_degisimi).grid(row=1, column=1, padx=10, pady=5)
        tk.Label(form_frame, text="Depo Lokasyonu:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        tk.Entry(form_frame, textvariable=self.depo_lokasyonu).grid(row=2, column=1, padx=10, pady=5)
        tk.Label(form_frame, text="İşlem Tarihi (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=5, sticky='w')
        tk.Entry(form_frame, textvariable=self.islem_tarihi).grid(row=3, column=1, padx=10, pady=5)

        # Kaydet, Güncelle, Sil ve Temizle butonları
        button_frame = tk.Frame(main_frame, bg='white')
        button_frame.pack()

        tk.Button(button_frame, text="Kaydet", command=self.malzeme_hareketi_kaydet).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Güncelle", command=self.malzeme_hareketi_guncelle).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Sil", command=self.malzeme_hareketi_sil).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Temizle", command=self.malzeme_hareketi_temizle).pack(side=tk.LEFT, padx=10)

    def load_data_from_firebase(self):
        ref = db.reference('depo')
        data = ref.get()
        if data:
            for key, value in data.items():
                self.tree.insert('', 'end', text=key, values=(value['malzeme_adi'], value['miktar'], value['depo_lokasyonu'], value['islem_tarihi']))

    def malzeme_hareketi_kaydet(self):
        malzeme_adi = self.malzeme_adi.get()
        miktar_degisimi = self.miktar_degisimi.get()
        depo_lokasyonu = self.depo_lokasyonu.get()
        islem_tarihi = self.islem_tarihi.get()

        if not malzeme_adi or not depo_lokasyonu or not islem_tarihi:
            return

        ref = db.reference('depo').push()
        ref.set({
            'malzeme_adi': malzeme_adi,
            'miktar': miktar_degisimi,
            'depo_lokasyonu': depo_lokasyonu,
            'islem_tarihi': islem_tarihi
        })

        self.tree.insert('', 'end', text=ref.key, values=(malzeme_adi, miktar_degisimi, depo_lokasyonu, islem_tarihi))
        self.malzeme_hareketi_temizle()

    def malzeme_hareketi_guncelle(self):
        selected_item = self.tree.focus()
        if not selected_item:
            return

        malzeme_adi = self.malzeme_adi.get()
        miktar_degisimi = self.miktar_degisimi.get()
        depo_lokasyonu = self.depo_lokasyonu.get()
        islem_tarihi = self.islem_tarihi.get()

        ref = db.reference('depo').child(selected_item)
        ref.update({
            'malzeme_adi': malzeme_adi,
            'miktar': miktar_degisimi,
            'depo_lokasyonu': depo_lokasyonu,
            'islem_tarihi': islem_tarihi
        })

        self.tree.item(selected_item, values=(malzeme_adi, miktar_degisimi, depo_lokasyonu, islem_tarihi))
        self.malzeme_hareketi_temizle()

    def malzeme_hareketi_sil(self):
        selected_item = self.tree.focus()
        if not selected_item:
            return

        db.reference('depo').child(selected_item).delete()
        self.tree.delete(selected_item)
        self.malzeme_hareketi_temizle()

    def malzeme_hareketi_temizle(self):
        self.malzeme_adi.set("")
        self.miktar_degisimi.set(0)
        self.depo_lokasyonu.set("")
        self.islem_tarihi.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = DepoYonetimiUygulamasi(root)
    root.configure(bg="#02577A")
    root.mainloop()
