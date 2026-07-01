# DGS Matematik Gunlugu

DGS matematik sinavina hazirlik icin her gun otomatik uretilen konu ozetleri.
Sinav tarihi: **19 Temmuz 2026**.

## Nasil calisiyor

Her gun saat 14:00'te bir rutin calisir ve `gunluk/[YYYY-AA-GG].svg` dosyasini
uretir. Dosya icinde:

1. Konunun kisa kural hatirlatmasi
2. DGS tarzi bir ornek soru + adim adim cozum
3. Sinavda bu soru tipini gorunce izlenecek strateji (ipucu kelimeler, formul, ilk adim)
4. Kendi cozmen icin bir pratik soru (cevabi ayrica, en altta belirtilir)

**Kural:** Butun kesirler, denklemler, oranlar ve uslu ifadeler SVG icinde
gorsel olarak cizilir (pay/payda + cizgi vb.) — asla "1/5" gibi slash ile
yazilmaz. Cizim icin `gunluk/_lib/svg_math.py` yardimci kutuphanesi kullanilir.

## Konu rotasyonu

Baslangic tarihi: **2026-07-01** (gun indeksi 0).

```
0: Yuzde problemleri
1: Hiz-zaman-yol
2: Isci/havuz problemleri
3: Oran-orantı
4: Rasyonel sayilar
5: Denklem/esitsizlik
6: Kumeler
7: Olasilik
8: Geometri (alan/cevre)
9: Sayi problemleri
```

Gunun konusu su formulle bulunur:

```
gun_indeksi = (bugunun_tarihi - 2026-07-01).gun_sayisi % 10
konu = ROTATION[gun_indeksi]
```

10. gunden sonra rotasyon bastan baslar. Bu hesap tarih farkina dayandigi
icin, arada bir gun atlansa bile (rutin calismazsa) sonraki gunlerin konusu
kaymaz — her zaman takvim tarihine gore doğru konu secilir.
