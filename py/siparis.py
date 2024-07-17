import tkinter as tk
from tkinter import ttk
import firebase_admin
from firebase_admin import credentials, db

# Firebase kimlik bilgilerini yüklüyoruz ve Firebase uygulamasını başlatıyoruz
cred = credentials.Certificate('.init/firebaseAdmin.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://depo-envanter-default-rtdb.firebaseio.com/'
})

class OrderManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sipariş Yönetimi")
        self.root.configure(bg="#02577A")  # Arka plan rengini ayarla
        self.frame = tk.Frame(root)

        # Sol frame oluşturuluyor
        left_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

        # Başlık: Sipariş Durumu Güncelleme
        tk.Label(left_frame, text="Sipariş Durumu Güncelle", font=('Helvetica', 14, 'bold')).pack(pady=10)

        # Güncelleme formu için değişkenler
        self.order_id = tk.StringVar()
        self.new_status = tk.StringVar()

        # Güncelleme formu
        update_frame = tk.Frame(left_frame)
        update_frame.pack(pady=10)

        tk.Label(update_frame, text="Sipariş No:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(update_frame, textvariable=self.order_id).grid(row=0, column=1, padx=5, pady=5)
        tk.Label(update_frame, text="Yeni Durum:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(update_frame, textvariable=self.new_status).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(update_frame, text="Güncelle", command=self.update_order_status).grid(row=2, columnspan=2, padx=5, pady=10)

        # Başlık: Yeni Sipariş Oluşturma
        tk.Label(left_frame, text="Yeni Sipariş Oluştur", font=('Helvetica', 14, 'bold')).pack(pady=10)

        # Sipariş ekleme formu için değişkenler
        self.customer_name = tk.StringVar()
        self.product_name = tk.StringVar()
        self.quantity = tk.IntVar()

        # Sipariş ekleme formu
        add_order_frame = tk.Frame(left_frame)
        add_order_frame.pack(pady=10)

        tk.Label(add_order_frame, text="Müşteri Adı:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(add_order_frame, textvariable=self.customer_name).grid(row=0, column=1, padx=5, pady=5)
        tk.Label(add_order_frame, text="Ürün:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(add_order_frame, textvariable=self.product_name).grid(row=1, column=1, padx=5, pady=5)
        tk.Label(add_order_frame, text="Miktar:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(add_order_frame, textvariable=self.quantity).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(add_order_frame, text="Sipariş Ekle", command=self.add_order).grid(row=3, columnspan=2, padx=5, pady=10)

        # Sipariş Silme Butonu
        tk.Button(left_frame, text="Sipariş Sil", command=self.delete_order).pack(pady=10)

        # Sipariş listesi için bir tablo oluşturuyoruz
        self.tree = ttk.Treeview(root, columns=('Order ID', 'Customer', 'Product', 'Quantity', 'Status'))
        self.tree.heading('#0', text='ID')
        self.tree.heading('#1', text='Sipariş No')
        self.tree.heading('#2', text='Müşteri')
        self.tree.heading('#3', text='Ürün')
        self.tree.heading('#4', text='Miktar')
        self.tree.heading('#5', text='Durum')
        self.tree.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Firebase veritabanı referansı
        self.db_ref = db.reference('/siparisler')

        # "Siparişleri Listele" butonu
        tk.Button(left_frame, text="Siparişleri Listele", command=self.initialize_orders).pack(pady=10)

    # Firebase'den siparişleri alıp tabloya ekleyen işlev
    def initialize_orders(self):
        orders = self.db_ref.get()
        if orders:
            for order_id, order_data in orders.items():
                musteri = order_data.get('musteri', '')
                urun = order_data.get('urun', '')
                miktar = order_data.get('miktar', 0)
                durum = order_data.get('durum', '')

                self.tree.insert('', 'end', text=order_id,
                                 values=(order_id, musteri, urun, miktar, durum))
        else:
            print("Firebase'den veri alınamadı veya boş.")

    def update_order_status(self):
        order_id = self.order_id.get()
        new_status = self.new_status.get()

        if order_id:
            self.db_ref.child(str(order_id)).update({'durum': new_status})

            # Sipariş tablosunu güncelle
            selected_item = self.tree.focus()
            self.tree.item(selected_item, values=(order_id,
                                                  self.tree.item(selected_item)['values'][1],
                                                  self.tree.item(selected_item)['values'][2],
                                                  self.tree.item(selected_item)['values'][3],
                                                  new_status))
        else:
            print("Geçersiz sipariş numarası.")

    def add_order(self):
        customer_name = self.customer_name.get()
        product_name = self.product_name.get()
        quantity = self.quantity.get()

        new_order_id = len(self.tree.get_children()) + 1

        # Firebase'e yeni siparişi ekleyelim
        self.db_ref.child(str(new_order_id)).set({
            'musteri': customer_name,
            'urun': product_name,
            'miktar': quantity,
            'durum': 'Hazırlanıyor'
        })

        # Tabloya yeni siparişi ekleyelim
        self.tree.insert('', 'end', text=str(new_order_id), values=(str(new_order_id), customer_name, product_name, str(quantity), 'Hazırlanıyor'))

        # Girdi alanlarını temizleyelim
        self.customer_name.set('')
        self.product_name.set('')
        self.quantity.set('')

    def delete_order(self):
        selected_item = self.tree.focus()
        order_id = self.tree.item(selected_item)['text']

        # Firebase'den siparişi sil
        self.db_ref.child(order_id).delete()

        # Tablodan siparişi sil
        self.tree.delete(selected_item)

if __name__ == "__main__":
    root = tk.Tk()
    app = OrderManagementApp(root)
    root.mainloop()
