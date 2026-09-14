# -*- coding: utf-8 -*-
"""
Sektöre göre ulaşım yolu — kime, hangi kanaldan, ne zaman, nasıl.

İki katman var ve ikisi ayrı tutuluyor:

  1. BAŞLANGIÇ VARSAYIMI  (kaynak="varsayım")
     Sektörün karar yapısından çıkan mantık. Kim karar veriyor, telefonu kim
     açıyor, gün içinde ne zaman müsait. Bu bir tahmindir, istatistik değildir;
     raporda da öyle yazar. Uydurulmuş yüzde yok.

  2. ÖLÇÜLEN GERÇEK  (kaynak="ölçüm")
     temas tablosundaki kendi sonuçlarımız. Yeterli veri birikince (eşik: bir
     sektör-kanal çifti için en az 8 temas) varsayımın yerini alır.

Yani sistem tahminle başlıyor, kendi rakamıyla düzeltiyor.
"""
import datetime

# Ölçüme geçmek için bir sektör-kanal çiftinde gereken en az temas sayısı
ESIK_TEMAS = 8

# "Başarılı" sayılan temas sonuçları
IYI = ("gorusuldu", "arandi gorusuldu", "teklif verildi", "kazanildi", "gorusme")
KOTU = ("arandi ulasilamadi", "ilgilenmiyor", "uygun degil")

# ---------------------------------------------------------------- varsayımlar
# Her sektör için: karar veren, ilk temas kanalı, saat aralığı, açılış biçimi.
# Gerekçeler sektörün çalışma düzeninden geliyor — sahada doğrulanacak.
SEKTOR = {
    "insaat": {
        "karar": "Şirket sahibi ya da satış/pazarlama müdürü",
        "kanal": ["whatsapp", "telefon", "ziyaret"],
        "saat": "09:30–11:30 ve 14:00–16:30, Salı–Perşembe",
        "kacin": "Pazartesi sabahı (şantiye programı) ve Cuma ikindi",
        "gerekce": "Karar tek kişide. Santral yerine cep hattı bulunursa doğrudan "
                   "sahibe ulaşılıyor. Sahada olduğu için yazılı mesaj sesli aramadan "
                   "daha çok okunuyor — arama kaçıyor, mesaj akşam okunuyor.",
        "kanca": "Satılmamış daire / lansmanı yaklaşan blok. Görsel doğrudan "
                 "satışa bağlı, o yüzden bütçe konuşuluyor.",
        "acilis": "Projenin adını söyle, o projeye ait tek bir kareyi göster, "
                  "iki cümlede ne yaptığını anlat. Fiyatı ilk mesajda verme.",
        "ilk_gorsel": "Kendi projelerinin görselinden üretilmiş dikey film",
    },
    "emlak": {
        "karar": "Ofis sahibi / broker; büyük ofiste pazarlama sorumlusu",
        "kanal": ["whatsapp", "telefon"],
        "saat": "10:00–12:00 ve 15:00–18:00, hafta içi her gün",
        "kacin": "Hafta sonu (gösterim günü, telefon sürekli meşgul)",
        "gerekce": "Emlakçı zaten telefonla yaşıyor; cep numarası halka açık ve "
                   "yanıt hızı yüksek. En kısa satış döngüsü bu sektörde.",
        "kanca": "Portföydeki ilanların video eksikliği — ilan sitesindeki "
                 "rakip ilanla yan yana koyulabilir.",
        "acilis": "Tek bir ilanını seç, o ilanın videosunun nasıl görüneceğini "
                  "göster. Genel konuşma, tek daire üzerinden konuş.",
        "ilk_gorsel": "Tek ilan için dikey tanıtım kesiti",
    },
    "mimarlik": {
        "karar": "Kurucu mimar",
        "kanal": ["eposta", "whatsapp"],
        "saat": "10:00–12:00, Salı–Perşembe",
        "kacin": "Teslim haftaları — proje tesliminden hemen önce cevap gelmez",
        "gerekce": "Görsel dile duyarlı, aceleye getirilmekten hoşlanmıyor. "
                   "Yazılı ve düzgün hazırlanmış bir dosya, aramadan daha iyi "
                   "karşılanıyor. Referans kalitesi fiyattan önce geliyor.",
        "kanca": "Yarışma/portföy sunumu için render ve animasyon; kendi "
                 "ekibini büyütmeden kapasite kazanması.",
        "acilis": "Kendi projelerinden birinin render diliyle konuş. Teknik "
                  "künye (çözünürlük, süre, teslim formatı) ilk mesajda olsun.",
        "ilk_gorsel": "Tek kare yüksek çözünürlüklü render kıyası + teknik künye",
    },
    "sanayi": {
        "karar": "Genel müdür ya da pazarlama/ihracat sorumlusu",
        "kanal": ["eposta", "telefon", "ziyaret"],
        "saat": "09:00–11:00, Pazartesi–Perşembe",
        "kacin": "Vardiya değişim saatleri, ay sonu sevkiyat haftası",
        "gerekce": "Kurumsal yapı: santral var, karar birden fazla kişide. "
                   "Yazılı teklif dosyası şart — sözlü teklif işleme girmiyor. "
                   "İhracat yapan firmada İngilizce/Almanca sürüm belirleyici.",
        "kanca": "Fuar takvimi ve ihracat sunumu. Ürünün nasıl çalıştığını "
                 "anlatan animasyon, katalogdan daha çok iş getiriyor.",
        "acilis": "Konu satırına ürün adını yaz. Tek sayfalık PDF ekle. "
                  "Fuar tarihine referans ver.",
        "ilk_gorsel": "Ürün animasyonu kesiti + çok dilli altyazı örneği",
    },
    "mobilya": {
        "karar": "Mağaza/üretim sahibi",
        "kanal": ["whatsapp", "ziyaret", "telefon"],
        "saat": "11:00–13:00 ve 15:00–18:00; Cumartesi de açık",
        "kacin": "Akşam 18:00 sonrası müşteri yoğunluğu",
        "gerekce": "Sahibi genelde mağazada; yerinde gitmek en etkili kanal. "
                   "Instagram üzerinden satış yapıyorsa görsel dile zaten yatkın, "
                   "karar hızlı veriliyor.",
        "kanca": "Yeni koleksiyon çekimi ve sosyal medya için düzenli içerik.",
        "acilis": "Kendi ürününün fotoğrafından üretilmiş kısa dikey videoyu "
                  "gönder, altına tek cümle yaz.",
        "ilk_gorsel": "Ürün fotoğrafından üretilmiş dikey sosyal kesit",
    },
    "otel": {
        "karar": "İşletme müdürü; zincirdeyse pazarlama merkezi",
        "kanal": ["eposta", "telefon"],
        "saat": "10:00–12:00 ve 14:00–16:00, sezon dışı",
        "kacin": "Sezon zirvesi (temmuz–ağustos) — cevap alınamıyor",
        "gerekce": "Sezon dışında bütçe ve yenileme kararları veriliyor. "
                   "Sezonda kimse yeni iş konuşmuyor. Rezervasyon sitelerindeki "
                   "görsel kalitesi doğrudan doluluk ile bağlantılı olduğu için "
                   "kanıt sunmak kolay.",
        "kanca": "Sezon öncesi tanıtım + drone ile konum/manzara anlatımı.",
        "acilis": "Rezervasyon sitesindeki mevcut görselleriyle bizim "
                  "teslimimizi yan yana koy. Sezon tarihine geri sayım ver.",
        "ilk_gorsel": "Drone ile konum anlatımı kesiti",
    },
    "isletme": {
        "karar": "Sahibi",
        "kanal": ["whatsapp", "ziyaret"],
        "saat": "İşletmenin yoğun olmadığı saat — genelde 14:00–16:00",
        "kacin": "Öğle ve akşam servis saatleri",
        "gerekce": "Küçük işletmede sahibi hem çalışıyor hem karar veriyor. "
                   "Yoğun saatte gelen mesaj kayboluyor. Bütçe küçük, o yüzden "
                   "tek videoluk giriş paketi ile başlamak gerekiyor.",
        "kanca": "Harita profilindeki fotoğraf ve video eksikliği — sonucu "
                 "doğrudan gösterilebilir.",
        "acilis": "Harita profilinin ekran görüntüsünü göster, eksiği işaretle, "
                  "tek videoluk fiyatı ver.",
        "ilk_gorsel": "Harita profili öncesi/sonrası kartı",
    },
}

VARSAYILAN = SEKTOR["isletme"]


def varsayim(sektor):
    return SEKTOR.get((sektor or "").lower(), VARSAYILAN)


# ---------------------------------------------------------------- ölçüm
def olcum(b, sektor=None):
    """
    temas tablosundan gerçek sonuçları çıkarır.
    Döner: {kanal: {"temas": n, "iyi": n, "oran": 0-1, "yeterli": bool}}
    """
    if b is None:
        return {}
    q = """SELECT t.kanal, t.durum, COUNT(*) n
           FROM temas t JOIN adaylar a ON a.id = t.aday_id
           WHERE t.yon='giden' AND t.kanal IS NOT NULL"""
    p = []
    if sektor:
        q += " AND a.sektor = ?"
        p.append(sektor)
    q += " GROUP BY t.kanal, t.durum"
    d = {}
    try:
        for r in b.execute(q, p):
            k = (r["kanal"] or "").strip().lower()
            if not k:
                continue
            g = d.setdefault(k, {"temas": 0, "iyi": 0})
            g["temas"] += r["n"]
            if (r["durum"] or "").strip().lower() in IYI:
                g["iyi"] += r["n"]
    except Exception:
        return {}
    for k, g in d.items():
        g["oran"] = round(g["iyi"] / g["temas"], 3) if g["temas"] else 0.0
        g["yeterli"] = g["temas"] >= ESIK_TEMAS
    return d


def oneri(sektor, bulunan_kanallar=(), b=None):
    """
    Bir aday için ulaşım kararı.
    bulunan_kanallar: o firmada gerçekten bulunan kanallar ("whatsapp","telefon",
                      "eposta","ziyaret").
    Döner: sıralı kanal listesi + gerekçe + kaynak (varsayım/ölçüm).
    """
    v = varsayim(sektor)
    sira = [k for k in v["kanal"] if not bulunan_kanallar or k in bulunan_kanallar]
    if not sira:
        sira = list(bulunan_kanallar) or v["kanal"][:1]
    kaynak, not_ = "varsayım", v["gerekce"]

    o = olcum(b, sektor)
    yeterliler = {k: g for k, g in o.items() if g["yeterli"]}
    if yeterliler:
        # ölçülen başarı oranına göre yeniden sırala
        olculu = sorted(yeterliler, key=lambda k: -yeterliler[k]["oran"])
        kalan = [k for k in sira if k not in olculu]
        yeni = [k for k in olculu if (not bulunan_kanallar or k in bulunan_kanallar)] + kalan
        if yeni:
            sira = yeni
        kaynak = "ölçüm"
        not_ = "Kendi temas kayıtlarımızdan: " + ", ".join(
            "%s %d temasta %%%d" % (k, yeterliler[k]["temas"], round(yeterliler[k]["oran"] * 100))
            for k in olculu)
    return {
        "sira": sira, "birincil": sira[0] if sira else None,
        "kaynak": kaynak, "gerekce": not_,
        "saat": v["saat"], "kacin": v["kacin"], "karar": v["karar"],
        "kanca": v["kanca"], "acilis": v["acilis"], "ilk_gorsel": v["ilk_gorsel"],
        "olcum": o,
    }


def rapor(b=None):
    """Bütün sektörler için ulaşım haritası (markdown)."""
    bugun = datetime.date.today().strftime("%d.%m.%Y")
    s = ["# Sektör bazlı ulaşım haritası", "",
         "Tarih: %s" % bugun, "",
         "Her satırın kaynağı belirtiliyor. **varsayım** = sektörün çalışma",
         "düzeninden çıkarılmış mantık, sahada doğrulanacak. **ölçüm** = kendi",
         "temas kayıtlarımızdan gelen gerçek sonuç. Uydurulmuş yüzde yok;",
         "bir çiftte %d temas birikmeden oran yazılmıyor." % ESIK_TEMAS, ""]
    for ad in SEKTOR:
        o = oneri(ad, (), b)
        v = SEKTOR[ad]
        s += ["## %s" % ad.capitalize(), "",
              "- **Karar veren:** %s" % v["karar"],
              "- **Kanal sırası:** %s  *(kaynak: %s)*" % (" → ".join(o["sira"]), o["kaynak"]),
              "- **Saat:** %s" % v["saat"],
              "- **Kaçın:** %s" % v["kacin"],
              "- **Neden:** %s" % o["gerekce"],
              "- **Kanca:** %s" % v["kanca"],
              "- **Açılış:** %s" % v["acilis"],
              "- **İlk gönderilecek görsel:** %s" % v["ilk_gorsel"], ""]
    return "\n".join(s)
