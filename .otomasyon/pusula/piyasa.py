# -*- coding: utf-8 -*-
"""
PİYASA FİYAT REFERANSI

Aşağıdaki aralıklar 25.08.2026'da Türkiye'de yayınlanmış ajans fiyat listelerinden
derlendi. Canlı veri değildir; ajanslar liste fiyatı yayınlamak zorunda olmadığı ve
gerçek işler pazarlıkla kapandığı için bunlar bir ÇAPA'dır, kesin piyasa ortalaması
değil. Panelden düzenlenebilir; ayrıca duyduğun gerçek rakip teklifleri kaydettikçe
sistem kendi ortalamasını da hesaplar ve o öne çıkar.

Kaynaklar (bkz. KAYNAKLAR):
  · medyabox.com.tr — video prodüksiyon fiyatları 2026
  · allrender.net — 2026 render fiyatları
  · kreativty.com — sosyal medya yönetimi fiyatları 2026
  · armut.com — emlak drone çekimi 2026 (pazaryeri alt bandı)
"""

KAYNAKLAR = [
 ("Video prodüksiyon fiyatları 2026", "https://www.medyabox.com.tr/post/video-produksiyon-fiyatlari-2026"),
 ("Tanıtım filmi fiyat listesi 2026", "https://www.medyabox.com.tr/tanitim-filmi-fiyatlari"),
 ("2026 render fiyatları", "https://www.allrender.net/post/2026-yili-render-fiyatlari"),
 ("Sosyal medya yönetimi fiyatları 2026", "https://kreativty.com/blog/sosyal-medya-yonetimi-ne-kadar-tutar-2026-fiyat-rehberi"),
 ("Emlak drone çekimi 2026", "https://armut.com/fiyatlari/emlak-drone-cekimi_7984"),
]

DERLEME_TARIHI = "25.08.2026"

# hizmet -> {alt, ust, birim, kalemler:[(ad, tutar/aralık, kaynak)], not}
PIYASA = {
"insaat-3d-modelleme": {
  "ad": "İnşaat 3D modelleme / mimari görselleştirme",
  "alt": 60000, "ust": 250000, "birim": "proje",
  "kalemler": [
    ("Dış cephe render (görsel başına)", "25.000 ₺ + KDV", "allrender"),
    ("İç mekân render (tek mekân, 2 görsel)", "20.000 ₺ + KDV", "allrender"),
    ("45 sn mimari animasyon", "135.000 ₺ + KDV", "allrender"),
    ("Kat planı görselleştirme", "10.000 ₺ + KDV", "allrender"),
    ("360° panorama (tek mekân)", "10.000 ₺ + KDV", "allrender"),
  ],
  "not": "Tek blok proje için render seti + kısa animasyon tipik olarak 90–180 bin bandında kapanıyor.",
},
"emlak-video": {
  "ad": "Emlak / gayrimenkul tanıtım videosu",
  "alt": 12000, "ust": 55000, "birim": "mülk",
  "kalemler": [
    ("Emlak drone çekimi (pazaryeri alt bandı)", "2.500 – 12.000 ₺", "armut"),
    ("Kurumsal tanıtım filmi (temel paket)", "35.000 – 65.000 ₺", "medyabox"),
    ("Fotoğraf çekimi (ajans asgari)", "35.000 ₺ + KDV", "medyabox"),
  ],
  "not": "Tek mülk çekim+kurgu 12–45 bin; aylık portföy aboneliği 25–70 bin bandında. "
         "Pazaryeri fiyatları (armut) tek kişilik ekip fiyatıdır, ajans işiyle kıyaslanmamalı.",
},
"urun-animasyon": {
  "ad": "3D ürün / hizmet animasyonu",
  "alt": 40000, "ust": 200000, "birim": "ürün",
  "kalemler": [
    ("Ürün tanıtım filmi — temel", "20.000 – 50.000 ₺", "medyabox"),
    ("Ürün tanıtım filmi — sinematik", "50.000 – 120.000 ₺", "medyabox"),
    ("Ürün seri paketi", "80.000 – 200.000 ₺", "medyabox"),
    ("Fabrika tanıtım filmi — standart", "60.000 – 100.000 ₺", "medyabox"),
    ("Ürün sahne yerleşimi (3D)", "15.000 ₺ + KDV", "allrender"),
  ],
  "not": "3D modelleme gerektiren teknik anlatım, gerçek çekimli ürün filminden %30–60 pahalı. "
         "Çok dilli sürüm başına +%10–15.",
},
"klip-cekimi": {
  "ad": "Müzik / marka klibi",
  "alt": 45000, "ust": 180000, "birim": "klip",
  "kalemler": [
    ("Sosyal medya reklam filmi", "25.000 – 75.000 ₺", "medyabox"),
    ("Dijital reklam filmi", "50.000 – 120.000 ₺", "medyabox"),
    ("Reklam filmi (ajans asgari)", "75.000 ₺ + KDV", "medyabox"),
  ],
  "not": "Tek mekân klip alt banda, senaryolu çok mekânlı iş üst banda oturuyor. "
         "Oyuncu ve mekân izni ayrı kalem.",
},
"drone-cekimi": {
  "ad": "Drone / FPV çekim",
  "alt": 8000, "ust": 40000, "birim": "çekim",
  "kalemler": [
    ("Emlak drone çekimi (pazaryeri)", "2.500 – 12.000 ₺", "armut"),
    ("Etkinlik filmi — yarım gün", "25.000 – 50.000 ₺", "medyabox"),
  ],
  "not": "Tek çekim + kurgu 8–20 bin; aylık şantiye ilerleme serisi 15–40 bin/ay. "
         "İzin gerektiren bölgede +%15–25.",
},
"dugun-cekimi": {
  "ad": "Düğün / etkinlik çekimi",
  "alt": 25000, "ust": 90000, "birim": "gün",
  "kalemler": [
    ("Etkinlik filmi — yarım gün", "25.000 – 50.000 ₺", "medyabox"),
    ("Etkinlik filmi — tam gün", "45.000 – 90.000 ₺", "medyabox"),
    ("Çok günlü / çoklu kamera", "80.000 – 180.000 ₺", "medyabox"),
  ],
  "not": "Düğün tarafı etkinlik fiyatlarının biraz altında seyrediyor; sezon (Mayıs–Eylül) +%15–20.",
},
"isletme-tanitim": {
  "ad": "İşletme tanıtım / sosyal medya (aylık)",
  "alt": 14000, "ust": 55000, "birim": "ay",
  "kalemler": [
    ("Mikro işletme paketi", "8.000 – 14.000 ₺/ay", "kreativty"),
    ("Küçük marka paketi", "14.000 – 28.000 ₺/ay", "kreativty"),
    ("Orta ölçek (içerik üretimi dahil)", "28.000 – 55.000 ₺/ay", "kreativty"),
    ("Kurumsal (çok platform + video)", "55.000 – 120.000 ₺/ay", "kreativty"),
    ("Dikey video / sosyal medya (ajans asgari)", "40.000 ₺ + KDV", "medyabox"),
  ],
  "not": "Çekim dahil paketler 'içerik üretimi' bandından başlar — sadece yönetim yapan "
         "ajanslarla aynı sepete konmamalı.",
},
}

# Şehir kademesine göre çarpan (büyük şehirde fiyatlar yukarı)
SEHIR_CARPANI = {
 "İstanbul": 1.25, "Ankara": 1.12, "İzmir": 1.10, "Antalya": 1.10,
 "Bursa": 1.0, "Kocaeli": 1.0, "Muğla": 1.08, "Adana": 0.95, "Gaziantep": 0.95,
 "Mersin": 0.95, "Kayseri": 0.92, "Konya": 0.92, "Denizli": 0.92, "Sakarya": 0.95,
 "Samsun": 0.90, "Trabzon": 0.90, "Eskişehir": 0.95, "Tekirdağ": 0.95,
}
VARSAYILAN_CARPAN = 0.85     # listede olmayan iller


def carpan(sehir):
    """Şehir verilmezse Türkiye geneli (1.0) kabul edilir."""
    s = (sehir or "").strip()
    if not s:
        return 1.0
    return SEHIR_CARPANI.get(s, VARSAYILAN_CARPAN)


def referans(hizmet, sehir=None, b=None):
    """
    Bir hizmet için piyasa aralığı + (varsa) kendi kaydettiğin rakip teklif ortalaması.
    b verilirse veritabanındaki rakip_teklif kayıtları da katılır.
    """
    p = PIYASA.get(hizmet)
    if not p:
        return None
    c = carpan(sehir)
    d = {
        "hizmet": hizmet, "ad": p["ad"], "birim": p["birim"],
        "ulke_alt": p["alt"], "ulke_ust": p["ust"],
        "sehir": sehir, "carpan": round(c, 2),
        "alt": int(round(p["alt"] * c / 500.0)) * 500,
        "ust": int(round(p["ust"] * c / 500.0)) * 500,
        "kalemler": p["kalemler"], "not": p["not"],
        "derleme": DERLEME_TARIHI, "kaynaklar": KAYNAKLAR,
        "kendi_veri": None,
    }
    d["orta"] = int(round((d["alt"] + d["ust"]) / 2.0 / 500.0)) * 500
    if b is not None:
        try:
            from . import veritabani as vt
            k = vt.rakip_ortalama(b, hizmet)
            if k:
                d["kendi_veri"] = {"adet": k["adet"], "ortalama": int(k["ortalama"]),
                                   "alt": int(k["alt"]), "ust": int(k["ust"])}
        except Exception:
            pass
    return d


def konum(hizmet, teklif, sehir=None, b=None):
    """Verilen teklif piyasanın neresinde duruyor?"""
    r = referans(hizmet, sehir, b)
    if not r or not teklif:
        return None
    t = float(teklif)
    alt, ust, orta = r["alt"], r["ust"], r["orta"]
    if r["kendi_veri"] and r["kendi_veri"]["adet"] >= 3:
        orta = r["kendi_veri"]["ortalama"]
    fark = (t - orta) / float(orta) * 100 if orta else 0
    if t < alt:
        yer, yorum = "altında", "Piyasa alt bandının altında — ucuz görünmek işi değersizleştirebilir."
    elif t <= orta:
        yer, yorum = "alt-orta", "Piyasanın alt-orta bandında — fiyat itirazı gelme ihtimali düşük."
    elif t <= ust:
        yer, yorum = "üst-orta", "Piyasanın üst bandında — kapsamı ve farkı net anlatmak gerekiyor."
    else:
        yer, yorum = "üstünde", "Piyasa üst bandının üstünde — ancak çok net bir fark varsa savunulabilir."
    return {"referans": r, "teklif": int(t), "yer": yer, "fark_yuzde": int(round(fark)), "yorum": yorum}


def oneri(hizmet, sehir=None, b=None, agresif=False):
    """Teklif için önerilen tutar. agresif=True → alt-orta banda çeker (kapanış hızı için)."""
    r = referans(hizmet, sehir, b)
    if not r:
        return None
    hedef = r["alt"] + (r["ust"] - r["alt"]) * (0.28 if agresif else 0.45)
    return int(round(hedef / 500.0)) * 500
