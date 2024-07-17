import tkinter as tk
from stok import create_stok_yonetim_frame



def show_stok_yonetim():
    for widget in main_fm.winfo_children():
        widget.destroy()
    stok_yonetim_frame = create_stok_yonetim_frame(main_fm)
    stok_yonetim_frame.pack(fill="both", expand=True)
    


# Ana pencere oluşturuluyor
root = tk.Tk()
root.geometry("500x400")
root.title("Ana Sayfa")
root.configure(bg="#02577A")

# Ana menü çerçevesi oluşturuluyor
option_fm = tk.Frame(root)

# Butonlar ve göstergeler oluşturuluyor
stok_btn = tk.Button(option_fm, text="Stok Yönetimi", font=("Arial", 13), bd=0, fg="#0097e8",
                     activeforeground="#0097e8", command=show_stok_yonetim)
stok_btn.place(x=0, y=0, width=125)

depo_btn = tk.Button(option_fm, text="Depo Yönetimi", font=("Arial", 13), bd=0, fg="#0097e8",
                     activeforeground="#0097e8")
depo_btn.place(x=150, y=0, width=125)

siparis_btn = tk.Button(option_fm, text="Sipariş Yönetimi", font=("Arial", 13), bd=0, fg="#0097e8",
                        activeforeground="#0097e8")
siparis_btn.place(x=295, y=0, width=125)

raporlama_btn = tk.Button(option_fm, text="Raporlama", font=("Arial", 13), bd=0, fg="#0097e8",
                          activeforeground="#0097e8")
raporlama_btn.place(x=425, y=0, width=125)

# Ana menü çerçevesini yerleştirme ve konfigürasyon
option_fm.pack(pady=0)
option_fm.pack_propagate(False)
option_fm.configure(width=2000, height=45)

# Ana içerik çerçevesi oluşturuluyor

main_fm = tk.Frame(root)
main_fm.pack(fill=tk.BOTH, expand=True)
main_fm.configure(bg="#02577A")

# Ana pencereyi çalıştırma döngüsü
root.mainloop()
