# Depo Envanter Uygulaması
Bu uygulama, depo envanterini yönetmek için tasarlanmış bir Python uygulamasıdır. Firebase kullanılarak veri depolama ve güncelleme işlemleri desteklenmektedir.Arayüzü de tkinter ile yapılmıştır

## Özellikler
1. Stok Sayfası: Mevcut stokları listeler,kaydeder,siler  ve güncellemeye izin verir.
2. Sipariş Sayfası: Yeni siparişler oluşturabilir ve sipariş durumunu güncelleyebiliriz 
3. Depo Sayfası: Depo envanter yönetimini sağlar, yeni öğeler ekleyebilir ve silebilirsiniz.
4. Firebase Bağlantısı: Verileri Firebase  üzerinde depolar, günceller, siler ve yeni öğeler ekler.
5. Kullanıcı Dostu Arayüz: Tkinter kullanılarak oluşturulmuş basit ve anlaşılır bir kullanıcı arayüzü.
6. login.py: burdan uygulamaya girişi sağlar
7.signup.py: uygulamaya kayıt olup giirş yapmayı sağlar 

## Gereksinimler

Python 3.x
Firebase SDK (firebase_admin kütüphanesi)
Tkinter (genellikle Python ile birlikte gelir)
##
Firebase SDK'yı yüklemek için terminal veya komut istemcisinde şu komutu çalıştırın:
Kodu kopyala
```
pip install firebase-admin
```

# Kullanım Kılavuz

Stok Sayfası: Mevcut stokları görüntüle, güncelle, sil ve kaydet.
Sipariş Sayfası: Yeni sipariş oluştur, siparişleri güncelle ve görüntüle.
Depo Sayfası: Depo adı ,miktarı, tarihi vb...  ekle, güncelle, sil.
Firebase Entegrasyonu: Firebase Firestore üzerinde veri depolama , silme ve güncelleme.

## Geliştirme
anasayfa.py: Anasayfa  dosyası.
stok.py: Stok yönetimi işlevleri.
siparis.py: Sipariş yönetimi işlevleri.
depo.py : depo yönetim işlemleri 

## Firebase Bağlantısı

### Bu proje Firebase kullanılarak yapılandırılmıştır. Firebase'e bağlanmak için aşağıdaki adımları izleyin:


1. Firebase Console'a gidin:[Firebase Console](https://console.firebase.google.com/)
2. Yeni bir proje oluşturun veya mevcut bir proje seçin.
3. Firebase projesini oluşturduktan sonra, proje ayarlarına gidin ve Firebase SDK snippet'inizi alın.
## Firebase Python SDK Kurulumu

1. Firebase'e Python üzerinden bağlanmak için firebase-admin kütüphanesini kullanabilirsiniz.
2. İlk olarak, kütüphaneyi yüklemek için terminal veya komut istemcisinde aşağıdı komutu çalıştırın:
```
pip install firebase-admin

```

### Firebase Kimlik Doğrulama Bilgileri

1. Firebase Console'da proje ayarlarından bir servis hesabı oluşturun ve bir özel anahtar (private key) dosyası indirin (serviceAccountKey.json).
Bu dosyayı projenizin kök dizinine yerleştirin.

2.  Python kodunuzda Firebase bağlantısını yapılandırın:


örnek kod
   ```python
   import firebase_admin
   from firebase_admin import credentials
   from firebase_admin import firestore

   # Firebase'in servis hesabı anahtarını yükleyin
   cred = credentials.Certificate("path/to/serviceAccountKey.json")
   firebase_admin.initialize_app(cred)

   # Firestore veritabanı referansını alın
   db = firestore.client()

   # Kullanım örneği: Veri ekleme
   data = {
       "name": "Bilge ",
       "email": "bilge.doe@example.com",
       "age": 22
   }
   db.collection("users").document("user1").set(data)
