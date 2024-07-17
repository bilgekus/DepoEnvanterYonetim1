from tkinter import *
from tkinter import ttk, messagebox
import firebase_admin
from firebase_admin import credentials, db

# Firebase'e bağlanma
cred = credentials.Certificate(".init/firebaseAdmin.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://depo-envanter-default-rtdb.firebaseio.com/'
})

# Veritabanı referansı
ref = db.reference('/stok1')
def create_stok_yonetim_frame(parent):
    pencere = Tk()
    pencere.title("Stok Yönetim Sistemi")
    pencere.geometry("720x640")
    pencere.configure(bg="#02577A")
    #pencere.attributes('-fullscreen', True)

    # Yer tutucu dizisi
    yerTutucuDizi = [None] * 5

    def kaydet():
        # Giriş alanlarından verileri al
        isim = yerTutucuDizi[0].get()
        fiyat = yerTutucuDizi[1].get()
        barkod = yerTutucuDizi[2].get()
        miktar = yerTutucuDizi[3].get()

        # Verileri Firebase'e kaydet
        yeni_veri = {
            'isim': isim,
            'fiyat': fiyat,
            'barkod': barkod,
            'miktar': miktar
        }
        ref.push(yeni_veri)
        messagebox.showinfo("Başarılı", "Veri Firebase'e kaydedildi.")
        listele()  # Kayıt yapıldıktan sonra listeyi güncelle
        temizle()  # Giriş alanlarını temizle

    # Sil butonuna basıldığında çalışacak fonksiyon
    def sil():
        selected_item = agac.focus()  # Seçili öğeyi al
        if selected_item:
            item = agac.item(selected_item)
            urun_id = item['values'][0]  # Ürün ID'yi al
            if urun_id:
                try:
                    # Firebase'den veriyi sil
                    ref.child(urun_id).delete()
                    messagebox.showinfo("Başarılı", "Veri silindi.")
                    listele()  # Silindikten sonra listeyi güncelle
                except Exception as e:
                    messagebox.showerror("Hata", f"Veri silinirken bir hata oluştu:\n{str(e)}")
            else:
                messagebox.showwarning("Uyarı", "Geçersiz bir ürün ID'si.")
        else:
            messagebox.showwarning("Uyarı", "Lütfen silinecek bir öğe seçin.")

    # Listele butonuna basıldığında çalışacak fonksiyon
    def listele():
        for row in agac.get_children():
            agac.delete(row)  # Tablodan mevcut tüm verileri sil

        veriler = ref.get()
        if veriler:
            for urun_id, veri in veriler.items():
                isim = veri.get('isim')
                fiyat = veri.get('fiyat')
                barkod = veri.get('barkod')
                miktar = veri.get('miktar')
                agac.insert("", "end", values=(urun_id, isim, fiyat, barkod, miktar))

    # Temizle butonuna basıldığında çalışacak fonksiyon
    def temizle():
        for i in range(5):
            yerTutucuDizi[i].set("")

    def guncelle():
        selected_item = agac.focus()
        if selected_item:
            item = agac.item(selected_item)
            urun_id = item['values'][0]
            if urun_id:
                isim = yerTutucuDizi[0].get()
                fiyat = yerTutucuDizi[1].get()
                barkod = yerTutucuDizi[2].get()
                miktar = yerTutucuDizi[3].get()
                
                # Firebase'deki veriyi güncelle
                guncelle_veri = {
                    'isim': isim,
                    'fiyat': fiyat,
                    'barkod': barkod,
                    'miktar': miktar
                }
                try:
                    ref.child(urun_id).update(guncelle_veri)
                    messagebox.showinfo("Başarılı", "Veri güncellendi.")
                    listele()
                    temizle()
                except Exception as e:
                    messagebox.showerror("Hata", f"Veri güncellenirken bir hata oluştu:\n{str(e)}")
            else:
                messagebox.showwarning("Uyarı", "Geçersiz bir ürün ID'si.")
        else:
            messagebox.showwarning("Uyarı", "Lütfen güncellenecek bir öğe seçin.")

    # Ana çerçeve oluştur ve ortala
    cerceve = Frame(pencere, bg="white", borderwidth=100)
    cerceve.pack(expand=True)

    # Yönetim çerçevesi oluştur
    yonetimCercevesi = LabelFrame(cerceve, borderwidth=20)
    yonetimCercevesi.grid(row=1, column=0, padx=[10, 10], pady=[10, 10], ipadx=[6], sticky='ew')

    # Butonları oluştur ve yerleştir
    kaydetButon = Button(yonetimCercevesi, text="KAYDET", width=10, borderwidth=3, bg="#0c0685", fg='white', command=kaydet)
    guncelleButon = Button(yonetimCercevesi, text="GÜNCELLE", width=10, borderwidth=3, bg="#0d8401", fg='white', command=guncelle)
    silButon = Button(yonetimCercevesi, text="SİL", width=10, borderwidth=3, bg="#a02109", fg='white', command=sil)
    bulButon = Button(yonetimCercevesi, text="Listele", width=10, borderwidth=3, bg="#f8c5d5", fg='white', command=listele)
    temizleButon = Button(yonetimCercevesi, text="TEMİZLE", width=10, borderwidth=3, bg="#196E78", fg='white', command=temizle)

    kaydetButon.grid(row=0, column=0, padx=5, pady=5)
    guncelleButon.grid(row=0, column=1, padx=5, pady=5)
    silButon.grid(row=0, column=2, padx=5, pady=5)
    bulButon.grid(row=0, column=3, padx=5, pady=5)
    temizleButon.grid(row=0, column=4, padx=5, pady=5)

    # Form çerçevesi oluştur ve yerleştir
    formCercevesi = LabelFrame(cerceve, borderwidth=20)
    formCercevesi.grid(row=0, column=0, padx=[10, 10], pady=[10, 10], ipadx=[6], sticky='ew')

    # Etiketleri oluştur ve yerleştir
    Label(formCercevesi, text="ÜRÜN ADI", anchor="e", width=10).grid(row=0, column=0, padx=10)
    Label(formCercevesi, text="ÜRÜN FİYATI", anchor="e", width=10).grid(row=1, column=0, padx=10)
    Label(formCercevesi, text="BARKODU", anchor="e", width=10).grid(row=2, column=0, padx=10)
    Label(formCercevesi, text=" MİKTAR", anchor="e", width=10).grid(row=3, column=0, padx=10)

    # Giriş alanlarını oluştur ve yerleştir
    for i in range(4):
        yerTutucuDizi[i] = StringVar()

    Entry(formCercevesi, width=50, textvariable=yerTutucuDizi[0]).grid(row=0, column=1, padx=5, pady=5)
    Entry(formCercevesi, width=50, textvariable=yerTutucuDizi[1]).grid(row=1, column=1, padx=5, pady=5)
    Entry(formCercevesi, width=50, textvariable=yerTutucuDizi[2]).grid(row=2, column=1, padx=5, pady=5)
    Entry(formCercevesi, width=50, textvariable=yerTutucuDizi[3]).grid(row=3, column=1, padx=5, pady=5)

    # Ağaç görünümü oluştur ve yerleştir
    stil = ttk.Style()
    agac = ttk.Treeview(cerceve, show='headings', height=20)
    stil.configure(pencere)
    agac['columns'] = ("Ürün ID", "İsim", "Fiyat", "Barkod", "Miktar")
    agac.column("#0", width=0, stretch=NO)
    agac.column("Ürün ID", anchor=W, width=70)
    agac.column("İsim", anchor=W, width=125)
    agac.column("Fiyat", anchor=W, width=125)
    agac.column("Barkod", anchor=W, width=125)
    agac.column("Miktar", anchor=W, width=100)
    agac.heading("Ürün ID", text="Ürün ID", anchor=W)
    agac.heading("İsim", text="İsim", anchor=W)
    agac.heading("Fiyat", text="Fiyat", anchor=W)
    agac.heading("Barkod", text="Barkod", anchor=W)
    agac.heading("Miktar", text="Miktar", anchor=W)
    agac.grid(row=0, column=1, padx=20, pady=10, rowspan=2)

    # Listeleme fonksiyonunu çağırarak başlat
    listele()

    pencere.mainloop()
