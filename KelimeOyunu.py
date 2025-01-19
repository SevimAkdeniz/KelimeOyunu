import nltk
import random
from nltk.corpus import words
from zemberek.morphology import TurkishMorphology
import requests
import customtkinter as ctk
from tkinter import messagebox


# Ana pencere ayarları

# Entryden oyuncu bilgisi cekimi
def kaydet_bir():
    global birinci_o
    birinci_o = x_entry.get()
def kaydet_iki():
    global ikinci_o
    ikinci_o = y_entry.get()
def kaydet_uc():
    global ucuncu_o
    ucuncu_o = z_entry.get()
def kaydet_dort():
    global dorduncu_o
    dorduncu_o = w_entry.get()


#Eğer oyncu bilgisi girilmediyse otomatik atama yapıyor
birinci_o = "Birinci Oyuncu"
ikinci_o = "İkinci Oyuncu"
ucuncu_o = "Üçüncü Oyuncu"
dorduncu_o = "Dördüncü Oyuncu"



#Oyuna Başla butonuna basılınca oyun penceresi aciliyor
def oyuna_basla():
    global i
    i = 0
    global app
    global puanlar
    global oyuncular
    global row_count
    global harflerim 
    app.destroy()  #ilk pencereyi kapat

    sessiz_harfler = ["b", "c", "ç", "d", "f", "g", "ğ", "h", "j", "k", "l", "m", "n", "p", "r", "s", "ş", "t", "v", "y", "z"]
    sesli_harfler = ["a", "e", "ı", "i", "o", "ö", "u", "ü"]
    oyuncular = [birinci_o,ikinci_o,ucuncu_o,dorduncu_o]
    puanlar = {
        birinci_o : 0,
        ikinci_o : 0,
        ucuncu_o : 0,
        dorduncu_o : 0
    }
    
    

    #Kelime oyunu ekranı
    app = ctk.CTk()
    app.geometry("600x600")
    app.title("Kelime Oyunu")
    app.minsize(600,600)

    
    #frame ayarları
    Main_frame = ctk.CTkFrame(app, width=3000, height=2000, corner_radius=10)
    Input_frame = ctk.CTkFrame(Main_frame,width=500, height=70, corner_radius=5)
    url = ctk.CTkEntry(Input_frame,placeholder_text="Oluşturmak istediginiz kelimeyi giriniz",height=50,font=("Helvetica", 20), state="normal",corner_radius=0,border_width=0)
    oyun_akisi =ctk.CTkFrame(Main_frame,width=1000, height=1000, corner_radius=10)
    puan_tablosu = ctk.CTkFrame(oyun_akisi,width=200, height=500, corner_radius=0)

    #Oyuncuların içinde olduğu framler
    birinci_oyuncu = ctk.CTkFrame(puan_tablosu, width=175, height=80, corner_radius=5, fg_color="pink")
    ikinci_oyuncu = ctk.CTkFrame(puan_tablosu, width=175, height=80, corner_radius=5, fg_color="blue" )
    ucuncu_oyuncu = ctk.CTkFrame(puan_tablosu, width=175, height=80, corner_radius=5, fg_color="yellow")
    dorduncu_oyuncu = ctk.CTkFrame(puan_tablosu, width=175, height=80, corner_radius=5, fg_color="purple" )

    #Oyuncu bilgilerini yazdığımız labellar
    birinci_oyuncu_label = ctk.CTkLabel(birinci_oyuncu, text=birinci_o)
    ikinci_oyuncu_label = ctk.CTkLabel(ikinci_oyuncu, text=ikinci_o)
    ucuncu_oyuncu_label = ctk.CTkLabel(ucuncu_oyuncu, text=ucuncu_o)
    dorduncu_oyuncu_label = ctk.CTkLabel(dorduncu_oyuncu, text=dorduncu_o)

    bir_puan = ctk.CTkLabel(birinci_oyuncu, text="0")
    iki_puan = ctk.CTkLabel(ikinci_oyuncu, text="0")
    uc_puan = ctk.CTkLabel(ucuncu_oyuncu, text="0")
    dort_puan = ctk.CTkLabel(dorduncu_oyuncu, text="0")


    #Harfleri yazagağımı label
    sesli_label = ctk.CTkLabel(Main_frame, text="", font=("Arial", 25),text_color="#E6E6FA")

    #oyunun aktığı yer
    frame = ctk.CTkScrollableFrame(oyun_akisi, width=400, height=1000)

    

    def harfleri_goster():


        sesli_harflerim = random.sample(sesli_harfler,3)
        sessiz_harflerim = random.sample(sessiz_harfler,5)
        harflerim = ""
        for i in range(3):
            if i==0:
                harflerim = sesli_harflerim[i]
            else:
                harflerim = harflerim + " "+  sesli_harflerim[i]

        for i in range(5):
            harflerim = harflerim + " " + sessiz_harflerim[i]

        return harflerim

    def tdk_kontrol(kelime):


        url = f"https://sozluk.gov.tr/gts?ara={kelime}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)  # API'ye istek gönder
            if response.status_code == 200:  # Yanıt başarılıysa
                data = response.json()

                # Yanıtı kontrol et
                if isinstance(data, list) and len(data) > 0:  # Eğer liste doluysa
                    return True  # Türkçe bir kelime
                elif isinstance(data, dict) and "error" in data:  # Eğer hata mesajı varsa
                    return False  # Türkçe bir kelime değil
            else:
                print(f"TDK API'ye erişim başarısız: {response.status_code}")
                return False
        except requests.exceptions.Timeout:
            print("Hata: Bağlantı zaman aşımına uğradı.")
            return False
        except requests.exceptions.RequestException as e:
            print(f"Hata oluştu: {e}")
            return False

    def oyun_baslat():

        global harflerim
        harflerim = harfleri_goster()  # İlk harfler set edilir
        sesli_label.configure(text="Harfler: " + harflerim) 
    oyun_baslat() #oyun_baslat program boyunca sedece bir kere çalışır ilk harfleri atamak için

    row_count = 1
    def oyun():  
        global i
        global puanlar
        global row_count
        global harflerim 
        global Input_Kelime
        global uzunluk
    
        for widget in frame.grid_slaves():
            widget_row = int(widget.grid_info()["row"])
            widget_column = int(widget.grid_info()["column"])
            if widget_row > 0:  # Sadece 0. row haricindekiler
                widget.grid(row=widget_row + 1, column=widget_column)
                row_count=1 #her yeni kelimeyi ilk sıraya yaz, diğerlerini aşşağı kaydır
        
    
        Input_Kelime = url.get()
        uzunluk = len(Input_Kelime)
        
        if Input_Kelime == "":     
            return

        

        kontroll = tdk_kontrol(Input_Kelime)    
        deger = all(harf in harflerim for harf in Input_Kelime)
                
                
        if deger == False:
            puanlar[oyuncular[i]]-=5
            kelime_label = ctk.CTkLabel(frame, text=Input_Kelime, font=("Arial", 20))
            puan_label = ctk.CTkLabel(frame,text="-3", font=("Arial", 20))
            harfler_label = ctk.CTkLabel(frame, text=harflerim, font=("Arial", 20))

            
            
            
        elif deger and kontroll: 
            
            puanlar[oyuncular[i]] =(2 * uzunluk) + puanlar[oyuncular[i]]
            kelime_label = ctk.CTkLabel(frame, text=Input_Kelime, font=("Arial", 20))
            puan_label = ctk.CTkLabel(frame, text=f"{2 * uzunluk}", font=("Arial", 20))
            harfler_label = ctk.CTkLabel(frame, text=harflerim, font=("Arial", 20))
            print(str( deger) + " " +str( kontroll))
            harflerim = harfleri_goster()
            sesli_label.configure(text="Harfler: "+ str(harflerim))
            i = (i + 1) % len(oyuncular)

          
            

        else:
            puanlar[oyuncular[i]]-=5
            kelime_label = ctk.CTkLabel(frame, text=Input_Kelime, font=("Arial", 20))
            puan_label = ctk.CTkLabel(frame, text ="-5", font=("Arial", 20))
            harfler_label = ctk.CTkLabel(frame, text=harflerim, font=("Arial", 20))


            
        



    
        bir_puan.configure(text=str(puanlar[oyuncular[0]]))
        iki_puan.configure(text=str(puanlar[oyuncular[1]]))
        uc_puan.configure(text=str(puanlar[oyuncular[2]]))
        dort_puan.configure(text=str(puanlar[oyuncular[3]]))
        
    
        # Tabloya yeni bir satır ekle
        kelime_label.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        puan_label.grid(row=1, column=1, sticky="nsew", padx=10, pady=5)
        harfler_label.grid(row=1, column=2, sticky="nsew", padx=10, pady=5)

        # Satır sayısını bir artır
        row_count += 1

    button = ctk.CTkButton(Input_frame,text="Gönder",hover_color="blue",width=100,command=oyun)  

    

    Main_frame.pack(fill = "both", expand = True,  pady=10, padx=10)

    sesli_label.pack(side="top", fill="x", padx=25, pady=10)

    Input_frame.pack( pady= 10, padx=20)
    Input_frame.pack_propagate(False)

    url.pack(side="top", fill="x", padx=10, pady=10)

    button.place(relx = 0.75, rely = 0.3)

    oyun_akisi.pack(fill= "both", expand = True, padx =25, pady=10) #oyun akısı kontrol
    oyun_akisi.pack_propagate(False)
    oyun_akisi.pack_propagate(False)

    puan_tablosu.pack(side ="left", padx=10, pady=0)

    birinci_oyuncu.pack(side= "top")
    ikinci_oyuncu.pack(side= "top",pady=10)
    ucuncu_oyuncu.pack(side= "top", pady=10)
    dorduncu_oyuncu.pack(side= "top")

    bir_puan.pack(side= "bottom")
    iki_puan.pack(side= "bottom")
    uc_puan.pack(side= "bottom")
    dort_puan.pack(side= "bottom")


    birinci_oyuncu.pack_propagate(False)
    ikinci_oyuncu.pack_propagate(False)
    ucuncu_oyuncu.pack_propagate(False)
    dorduncu_oyuncu.pack_propagate(False)

    birinci_oyuncu_label.pack(fill="both", expand= True)
    ikinci_oyuncu_label.pack(fill="both", expand= True)
    ucuncu_oyuncu_label.pack(fill="both", expand= True)
    dorduncu_oyuncu_label.pack(fill="both", expand= True)

    frame.pack(side="top",fill="both",expand=True)

    # Grid ile kelimeleri yerleştir
    frame.grid_columnconfigure(0, weight=1)  # Sütunları eşit genişlet
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=1)

    # Kelimeleri Label olarak yerleştir
    kelime_label = ctk.CTkLabel(frame, text="Kelime", font=("Arial", 20))
    pan_label = ctk.CTkLabel(frame, text="Puan", font=("Arial", 20))
    harfler_label = ctk.CTkLabel(frame, text="Harfler", font=("Arial", 20))

    kelime_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    pan_label.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    harfler_label.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

    app.mainloop()


app = ctk.CTk()
app.geometry("600x600")
app.title("Oyuncu Girişi")
app.minsize(600, 600)


# Başlık
hg_label = ctk.CTkLabel(
    app,
    text="Kelime Oyununa Hoşgeldiniz",
    font=("Helvetica", 20),
    text_color="white"
)

# Oyuna Başla Butonu
basla_button = ctk.CTkButton(
    app, 
    text="Oyuna Başla", 
    font=("Helvetica", 15), 
    fg_color="green",
    hover_color="darkgreen",
    width=150,
    height=50,
    command=oyuna_basla
   
)

# Ana giriş alanı
giris_frame = ctk.CTkFrame(
    app, 
    width=500, 
    height=300, 
    fg_color="lightblue",
    corner_radius=10
)

# Dört çerçeve (frame)
bir_frame = ctk.CTkFrame(giris_frame, fg_color="yellow", corner_radius=10)
iki_frame = ctk.CTkFrame(giris_frame, fg_color="orange", corner_radius=10)
uc_frame = ctk.CTkFrame(giris_frame, fg_color="green", corner_radius=10)
dort_frame = ctk.CTkFrame(giris_frame, fg_color="pink", corner_radius=10)

bir_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
iki_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
uc_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
dort_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# Ana giriş alanı grid ayarları
giris_frame.grid_columnconfigure(0, weight=1)
giris_frame.grid_columnconfigure(1, weight=1)
giris_frame.grid_rowconfigure(0, weight=1)
giris_frame.grid_rowconfigure(1, weight=1)

# Birinci frame içeriği
x_oyuncu = ctk.CTkLabel(bir_frame, text="Birinci Oyuncu", font=("Helvetica", 20))
x_entry = ctk.CTkEntry(bir_frame, font=("Helvetica", 20))
x_button = ctk.CTkButton(
    bir_frame, 
    text="Kaydet", 
    font=("Helvetica", 15), 
    fg_color="blue",
    hover_color="darkblue",
    command=kaydet_bir
)

# Birinci frame grid ayarları
bir_frame.grid_rowconfigure(0, weight=1)
bir_frame.grid_rowconfigure(1, weight=1)
bir_frame.grid_rowconfigure(2, weight=1)
bir_frame.grid_columnconfigure(0, weight=1)

x_oyuncu.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
x_entry.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
x_button.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

# İkinci frame içeriği
y_oyuncu = ctk.CTkLabel(iki_frame, text="İkinci Oyuncu", font=("Helvetica", 20))
y_entry = ctk.CTkEntry(iki_frame, font=("Helvetica", 20))
y_button = ctk.CTkButton(
    iki_frame, 
    text="Kaydet", 
    font=("Helvetica", 15), 
    fg_color="blue",
    hover_color="darkblue",
    command=kaydet_iki
)

iki_frame.grid_rowconfigure(0, weight=1)
iki_frame.grid_rowconfigure(1, weight=1)
iki_frame.grid_rowconfigure(2, weight=1)
iki_frame.grid_columnconfigure(0, weight=1)

y_oyuncu.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
y_entry.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
y_button.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

# Üçüncü frame içeriği
z_oyuncu = ctk.CTkLabel(uc_frame, text="Üçüncü Oyuncu", font=("Helvetica", 20))
z_entry = ctk.CTkEntry(uc_frame, font=("Helvetica", 20))
z_button = ctk.CTkButton(
    uc_frame, 
    text="Kaydet", 
    font=("Helvetica", 15), 
    fg_color="blue",
    hover_color="darkblue",
    command=kaydet_uc
    
)

uc_frame.grid_rowconfigure(0, weight=1)
uc_frame.grid_rowconfigure(1, weight=1)
uc_frame.grid_rowconfigure(2, weight=1)
uc_frame.grid_columnconfigure(0, weight=1)

z_oyuncu.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
z_entry.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
z_button.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

# Dördüncü frame içeriği
w_oyuncu = ctk.CTkLabel(dort_frame, text="Dördüncü Oyuncu", font=("Helvetica", 20))
w_entry = ctk.CTkEntry(dort_frame, font=("Helvetica", 20))
w_button = ctk.CTkButton(
    dort_frame, 
    text="Kaydet", 
    font=("Helvetica", 15), 
    fg_color="blue",
    hover_color="darkblue",
    command=kaydet_dort
)

dort_frame.grid_rowconfigure(0, weight=1)
dort_frame.grid_rowconfigure(1, weight=1)
dort_frame.grid_rowconfigure(2, weight=1)
dort_frame.grid_columnconfigure(0, weight=1)

w_oyuncu.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
w_entry.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
w_button.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

# Ana widget yerleşimleri
hg_label.pack(pady=20)
giris_frame.pack(padx=20, pady=20, fill="both", expand=True)
basla_button.pack(pady=20)

app.mainloop()
