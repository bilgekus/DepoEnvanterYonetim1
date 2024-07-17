from tkinter import *
from PIL import Image, ImageTk
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from tkinter import messagebox

# Firebase Admin SDK'yı başlat
cred = credentials.Certificate('.init/firebaseAdmin.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://depo-envanter-default-rtdb.firebaseio.com/'
})

# Firebase veritabanı referansı
ref = db.reference('/kullaniciKayit')

# Kayıt işlemi için kullanılacak fonksiyon
def register_to_firebase():
    ad = fname.get()
    soyad = lname.get()
    kullanici_adi = user.get()
    sifre = code.get()

    try:
        # Firebase veritabanına veri ekleme işlemi
        ref.push({
            'ad': ad,
            'soyad': soyad,
            'kullanici_adi': kullanici_adi,
            'sifre': sifre
        })
        print("Kayıt işlemi Firebase'e başarıyla tamamlandı.")
        messagebox.showinfo("Başarılı", "Kayıt işlemi başarıyla tamamlandı.")
        open_login()
    except Exception as e:
        print(f"Firebase'e kayıt eklenirken hata: {e}")
        messagebox.showerror("Hata", f"Kayıt eklenirken hata oluştu: {e}")

# Ad giriş alanı için odaklanıldığında tetiklenen fonksiyonlar
def on_enter_fname(e):
    fname.delete(0, END)

def on_leave_fname(e):
    if fname.get() == "":
        fname.insert(0, "Ad")

def on_enter_lname(e):
    lname.delete(0, END)

def on_leave_lname(e):
    if lname.get() == "":
        lname.insert(0, "Soyad")

def on_enter_user(e):
    user.delete(0, END)

def on_leave_user(e):
    if user.get() == "":
        user.insert(0, "Kullanıcı Adı")

def on_enter_code(e):
    code.delete(0, END)

def on_leave_code(e):
    if code.get() == "":
        code.insert(0, "Şifre")

# Kayıt ol butonuna basıldığında tetiklenen fonksiyon
def open_login():
    signup_screen.destroy()
    os.system('python py/login.py')

# Kayıt olma ekranı penceresi oluştur
signup_screen = Tk()
signup_screen.title("Kayıt Ol")
signup_screen.attributes('-fullscreen', True)
signup_screen.configure(bg="#fff")
signup_screen.resizable(False, False)

# Arka plan resmini yükle
background_image = Image.open(".init/arkap.jpg")
background_image = background_image.resize((signup_screen.winfo_screenwidth(), signup_screen.winfo_screenheight()), Image.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)

# Arka plan resmini eklemek için bir etiket oluştur
background_label = Label(signup_screen, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Ana çerçeveyi oluştur ve ortala
frame = Frame(signup_screen, width=700, height=550, bg="white", highlightbackground="black", highlightthickness=2)
frame.place(x=signup_screen.winfo_screenwidth()//2 - 350, y=signup_screen.winfo_screenheight()//2 - 275)

# Form çerçevesi oluştur
form_frame = Frame(frame, width=350, height=500, bg="white")
form_frame.place(x=150, y=30)

heading = Label(form_frame, text="Kayıt Ol", fg="#103754", bg="white", font=("Microsoft YaHei UI Light", 23, "bold"))
heading.place(x=100, y=5)

# Ad giriş alanı oluşturma ve yerleştirme
fname = Entry(form_frame, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
fname.place(x=30, y=80)
fname.insert(0, "Ad")
fname.bind("<FocusIn>", on_enter_fname)
fname.bind("<FocusOut>", on_leave_fname)
Frame(form_frame, width=295, height=2, bg="black").place(x=25, y=107)

# Soyad giriş alanı oluşturma ve yerleştirme
lname = Entry(form_frame, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
lname.place(x=30, y=150)
lname.insert(0, "Soyad")
lname.bind("<FocusIn>", on_enter_lname)
lname.bind("<FocusOut>", on_leave_lname)
Frame(form_frame, width=295, height=2, bg="black").place(x=25, y=177)

# Kullanıcı adı giriş alanı oluşturma ve yerleştirme
user = Entry(form_frame, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
user.place(x=30, y=220)
user.insert(0, "Kullanıcı Adı")
user.bind("<FocusIn>", on_enter_user)
user.bind("<FocusOut>", on_leave_user)
Frame(form_frame, width=295, height=2, bg="black").place(x=25, y=247)

# Şifre giriş alanı oluşturma ve yerleştirme
code = Entry(form_frame, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
code.place(x=30, y=290)
code.insert(0, "Şifre")
code.bind("<FocusIn>", on_enter_code)
code.bind("<FocusOut>", on_leave_code)
Frame(form_frame, width=295, height=2, bg="black").place(x=25, y=317)

# Kayıt ol butonunu oluştur ve yerleştir
Button(form_frame, width=39, pady=7, text="Kayıt Ol", bg="#103754", fg="white", border=0, command=register_to_firebase).place(x=35, y=420)

signup_screen.mainloop()
