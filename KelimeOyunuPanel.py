import nltk
import random
from nltk.corpus import words
from zemberek.morphology import TurkishMorphology
import requests




sessiz_harfler = ["b", "c", "ç", "d", "f", "g", "ğ", "h", "j", "k", "l", "m", "n", "p", "r", "s", "ş", "t", "v", "y", "z"]
sesli_harfler = ["a", "e", "ı", "i", "o", "ö", "u", "ü"]
oyuncular = []
puanlar = {}

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



while True:
        oyuncuSayisi =int( input("Lutfen oyuncu sayisini giriniz (2-5) "))
        if(oyuncuSayisi >=2 and oyuncuSayisi <=5):
            break
for i in range(oyuncuSayisi):
    isim = input(str(i+1)+". Oyuncunun ismini giriniz : ")
    oyuncular.append(isim)
    puanlar[isim] = 0

print(" ------------------------------------------------------------------------------------------------------------------- ")

k = 0
while True:
    
    print(oyuncular[k]+" adli oyuncunun sirasi ")
    print(" ------------------------------------------------------------------------------------------------------------------- ")
    
    
    sesli_harflerim = random.sample(sesli_harfler,3)
    sessiz_harflerim = random.sample(sessiz_harfler,5)
    harflerim = sesli_harfler +sessiz_harfler
    print(" '", end=" ")
    for  i in sesli_harflerim: 
        
        print(i, end=" ")

    for i in sessiz_harflerim:
        print(i, end=" ")
        
    print("'", end=" | ")

    print ("Bu harfleri kullanarak anlamlı bır kelıme oluşturunuz |")
    print("Kelimeniz : ", end=" ")
    kelime = input()
    kelime.lower()

    deger = True
    for harf in kelime:
        if harf not in harflerim:
            deger = False
             
    if deger == False:
        print("Lutfen verilen kelimeler ile bir kelime bulunuz")

    elif deger == True : 
        tdk_kontrol(kelime)
        if tdk_kontrol(kelime):
            print(f"'{kelime}' Türkçe bir kelimedir.")
            uzunluk  = len(kelime)
            puanlar[oyuncular[k]] = puanlar[oyuncular[k]]+ 2*uzunluk
            print("Puaniniz : "+str(puanlar[oyuncular[k]]))
            print(" ")
        else:
            print(f"'{kelime}' Türkçe bir kelime değildir.")
            puanlar[oyuncular[k]] = puanlar[oyuncular[k]] - 5 
            print("Puaniniz : "+str(puanlar[oyuncular[k]]))
            print(" ")
         
        print(" ------------------------------------------------------------------------------------------------------------------- ")
    k = k+1
    if k == 2:
        k = 0

    
   


            
   



    



    












    
     


     
     

















    


