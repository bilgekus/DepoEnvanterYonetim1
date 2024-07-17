from tkinter import *
import os
from PIL import Image, ImageTk
import firebase_admin
from firebase_admin import credentials, db
from tkinter import messagebox

# Firebase'e bağlanmak için kimlik doğrulama bilgisini yükle
cred = credentials.Certificate('.init/firebaseAdmin.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://depo-envanter-default-rtdb.firebaseio.com/'})

# Firebase veritabanı referansı
ref = db.reference('/kullaniciKayit')  # 'users' koleksiyonuna referans alın

# Giriş işlemi için fonksiyon
def signin():
    username = user.get()
    password = code.get()

    # Kullanıcı adı ve şifre kontrolü için veritabanından kullanıcı bilgilerini alır ve kontrol eder
    users = ref.get()
    if users:
        for user_id, info in users.items():
            if info.get('kullanici_adi') == username and info.get('sifre') == password:
                # Giriş başarılı ise hoşgeldin mesajı göster
                messagebox.showinfo("Hoşgeldiniz", " giriş başarıyla gerçekleşti.")
                return
    # Eğer kullanıcı bilgileri yanlışsa veya kullanıcı bulunamazsa
    messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış.")


def open_signup():
    root.destroy()
    os.system('python py/signup.py')

def on_enter_user(e):
    if user.get() == "Kullanıcı Adı":
        user.delete(0, "end")

def on_leave_user(e):
    if user.get() == "":
        user.insert(0, "Kullanıcı Adı")

def on_enter_code(e):
    if code.get() == "Şifre":
        code.delete(0, "end")

def on_leave_code(e):
    if code.get() == "":
        code.insert(0, "Şifre")
        
root = Tk()
root.title("GİRİŞ")
root.attributes('-fullscreen', True)

# Arka plan fotoğrafı için Canvas oluştur
canvas = Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
canvas.pack()

# Fotoğrafı eklemek için bir alan oluştur
photo_path = ".init/arkap.jpg"  # Fotoğraf dosyasının yolunu belirtin
image = Image.open(photo_path)
image = image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)  # Fotoğrafı ekran boyutuna göre yeniden boyutlandırın
background_image = ImageTk.PhotoImage(image)
canvas.create_image(0, 0, anchor=NW, image=background_image)

# Ana çerçeve oluştur
frame = Frame(root, width=400, height=500, bg="white")
frame.place(x=root.winfo_screenwidth()//2 - 200, y=root.winfo_screenheight()//2 - 250)

heading = Label(frame, text="Giriş Yap", fg="#103754", bg="white", font=("Microsoft YaHei UI Light", 23, "bold"))
heading.place(x=120, y=100)

user = Entry(frame, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
user.place(x=50, y=180)
user.insert(0, "Kullanıcı Adı")
user.bind("<FocusIn>", on_enter_user)
user.bind("<FocusOut>", on_leave_user)

Frame(frame, width=295, height=2, bg="black").place(x=50, y=207)

code = Entry(frame, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
code.place(x=50, y=250)
code.insert(0, "Şifre")
code.bind("<FocusIn>", on_enter_code)
code.bind("<FocusOut>", on_leave_code)

Frame(frame, width=295, height=2, bg="black").place(x=50, y=277)

Button(frame, width=39, pady=7, text="Giriş Yap", bg="#103754", fg="white", border=0, command=signin).place(x=55, y=310)

Label(frame, text="Hesabınız yok mu?", fg="black", bg="white", font=("Microsoft YaHei UI Light", 9)).place(x=90, y=360)

Button(frame, width=6, text="Kayıt Ol", border=0, bg="white", cursor="hand2", fg="#103754", command=open_signup).place(x=230, y=360)

root.mainloop()
