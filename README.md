# Kelime Oyunu - Python ve CustomTkinter ile Oyunculu Kelime Oyunu

Bu proje, Python programlama dili ve `CustomTkinter` kütüphanesi kullanılarak geliştirilen bir kelime oyunu uygulamasıdır. Oyuncuların sırayla kelime türettiği, harf havuzundan yararlanarak puan kazandığı bir oyun mekaniğine sahiptir.

---

## Özellikler

- **Oyuncu Girişi**: Oyuna başlamadan önce, 4 oyuncunun isimleri kaydedilir. Varsayılan olarak "Birinci Oyuncu", "İkinci Oyuncu" gibi otomatik atamalar yapılır.
- **Sıralı Oyun Akışı**: Oyuncular sırayla kelime girer. Geçerli bir kelime girildiğinde puan kazanır, geçersiz kelimede ise puan kaybeder.
- **Harf Havuzu**: Her turda oyunculara sesli ve sessiz harflerden oluşan rastgele bir harf seti verilir.
- **Puan Takibi**: Her oyuncunun puanı ekrandaki kendi bölümünde canlı olarak güncellenir.
- **Türkçe Kelime Doğrulama**: Girdiğiniz kelimenin geçerli bir Türkçe kelime olup olmadığını kontrol etmek için TDK API'si kullanılır.

---

## Gereksinimler

- Python 3.9 veya daha üstü
- Aşağıdaki Python kütüphaneleri:
  - `customtkinter`
  - `nltk`
  - `requests`

Kütüphaneleri yüklemek için:
```bash
pip install customtkinter nltk requests
