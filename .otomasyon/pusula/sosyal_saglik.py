# -*- coding: utf-8 -*-
"""
SOSYAL SAYFA SAĞLIĞI — kişi kazımadan ölçülebilen her şey.

Ne yapmıyoruz: platformlara giriş yapmıyoruz, kişi/takipçi listesi çıkarmıyoruz,
gönderi kazımıyoruz. Bunlar hem platform şartlarına aykırı hem KVKK riski.

Ne yapıyoruz: profil sayfasının herkese açık üstverisine (og: etiketleri) ve
sayfanın kendi HTML'ine bakıp şu soruları cevaplıyoruz —

  · Profil tamamlanmış mı: bio var mı, ne anlatıyor, şehir geçiyor mu,
    hizmet geçiyor mu, iletişim var mı
  · Bio'da siteye bağlantı var mı (link in bio) — sosyaldan gelen trafiğin
    gideceği yer
  · Profil görseli var mı
  · Kullanıcı adı platformlar arasında tutarlı mı (marka aramasında bulunmayı
    doğrudan etkiliyor)
  · Site ile sosyal karşılıklı bağlı mı (siteden hesaba, hesaptan siteye)
  · Yayınlanan üstveride takipçi/gönderi sayısı varsa okunuyor

Okunamayan her alan None kalıyor ve "teyit edilemedi" yazılıyor. Uydurma yok.
"""
import re, html, datetime

from .kaynaklar.agir import getir

OG = lambda ad: re.compile(
    r'<meta[^>]+(?:property|name)=["\']%s["\'][^>]+content=["\'](.*?)["\']' % ad, re.S | re.I)
OG_BASLIK = OG("og:title")
OG_ACIKLAMA = OG("og:description")
OG_GORSEL = OG("og:image")
OG_TUR = OG("og:type")

SAYI = r"([\d.,]+\s?[KMBkmb]?)"
DESEN_TAKIPCI = re.compile(SAYI + r"\s*(?:takipçi|followers?|Followers|abone|subscribers?)", re.I)
DESEN_GONDERI = re.compile(SAYI + r"\s*(?:gönderi|posts?|video(?:lar)?|paylaşım)", re.I)
DESEN_BEGENI = re.compile(SAYI + r"\s*(?:beğeni|likes?)", re.I)

BAGLANTI = re.compile(r"https?://[^\s\"'<>)]+", re.I)

# Bio'da olması beklenen unsurlar — her biri ayrı bir eksik
BIO_UNSUR = (
    ("ne_is", "Ne iş yaptığı", "Bio'da ne yaptığı yazmıyor — profili açan kişi "
                               "hesabın ne olduğunu anlamıyor"),
    ("nerede", "Nerede olduğu", "Bio'da şehir/bölge yok — yerel aramada ve keşfette "
                                "eşleşme şansı düşüyor"),
    ("iletisim", "İletişim yolu", "Bio'da telefon/WhatsApp/e-posta yok — ilgilenen kişi "
                                  "mesaj kutusuna düşmek zorunda kalıyor"),
    ("baglanti", "Siteye bağlantı", "Bio'da bağlantı yok — sosyalden gelen trafiğin "
                                    "gideceği bir yer tanımlanmamış"),
)

ILETISIM_IZ = ("wa.me", "whatsapp", "@", "tel:", "0(", "05", "+90", "iletişim",
               "randevu", "sipariş", "dm", "bilgi için")


def _kucuk(x):
    return (x or "").translate(str.maketrans(
        {"İ": "i", "I": "ı", "Ğ": "ğ", "Ü": "ü", "Ş": "ş", "Ö": "ö", "Ç": "ç"})).lower()


def _sayiya(x):
    """'12,3 B' / '1.2K' / '4500' → 4500 gibi kaba sayı. Çevrilemezse None."""
    if not x:
        return None
    s = str(x).strip().replace(" ", "")
    carpan = 1
    if s and s[-1] in "KkBb":
        carpan = 1000
        s = s[:-1]
    elif s and s[-1] in "Mm":
        carpan = 1000000
        s = s[:-1]
    s = s.replace(".", "").replace(",", ".") if s.count(",") == 1 and len(s.split(",")[-1]) <= 2 \
        else s.replace(".", "").replace(",", "")
    try:
        return int(float(s) * carpan)
    except ValueError:
        return None


# ------------------------------------------------------------------ profil sağlığı
def profil_saglik(url, firma="", sehir="", hizmet_sozcukleri=()):
    """
    Bir sosyal profil sayfasının herkese açık hâline bakar.
    Döner: sağlık sözlüğü + kanıtlı eksik listesi.
    """
    zaman = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    d = {"url": url, "zaman": zaman, "ulasildi": False, "durum": 0,
         "baslik": None, "bio": None, "gorsel": None, "tur": None,
         "takipci": None, "gonderi": None, "begeni": None,
         "bio_baglanti": None, "bio_uzunluk": 0,
         "unsur": {}, "eksik": [], "teyit": "teyit edilemedi",
         "okunabilirlik": "kapalı"}

    kod, govde, _ = getir(url, zaman_asimi=10)
    d["durum"] = kod
    if kod in (404, 410):
        d["teyit"] = "hesap bulunamadı (%s)" % kod
        return d
    if kod not in (200, 999) or not govde:
        d["teyit"] = "sayfa okunamadı (durum %s)" % (kod or "bağlantı yok")
        return d

    d["ulasildi"] = True
    m = OG_BASLIK.search(govde)
    if m:
        d["baslik"] = html.unescape(m.group(1))[:160]
    a = OG_ACIKLAMA.search(govde)
    if a:
        d["bio"] = html.unescape(a.group(1)).strip()[:600]
    g = OG_GORSEL.search(govde)
    if g:
        d["gorsel"] = g.group(1)[:400]
    t = OG_TUR.search(govde)
    if t:
        d["tur"] = t.group(1)

    if not (d["baslik"] or d["bio"]):
        d["teyit"] = "sayfa açıldı ama üstverisi okunamadı (giriş duvarı olabilir)"
        d["okunabilirlik"] = "kısıtlı"
        return d

    d["okunabilirlik"] = "açık"
    bio = d["bio"] or ""
    d["bio_uzunluk"] = len(bio)

    # sayılar — yayınlanmışsa
    for ad, desen in (("takipci", DESEN_TAKIPCI), ("gonderi", DESEN_GONDERI),
                      ("begeni", DESEN_BEGENI)):
        mm = desen.search(bio) or desen.search(d["baslik"] or "")
        if mm:
            d[ad] = _sayiya(mm.group(1))
    if d["takipci"] is not None or d["gonderi"] is not None:
        d["teyit"] = "sayfanın herkese açık üstverisinden okundu"
    else:
        d["teyit"] = "hesap açık; takipçi/gönderi sayısı sayfada yayınlanmıyor"

    # bio unsurları
    bk = _kucuk(bio + " " + (d["baslik"] or ""))
    firma_k = _kucuk(firma)
    d["unsur"]["ne_is"] = bool(hizmet_sozcukleri) and any(
        _kucuk(k) in bk for k in hizmet_sozcukleri)
    d["unsur"]["nerede"] = bool(sehir) and _kucuk(sehir) in bk
    d["unsur"]["iletisim"] = any(iz in bk for iz in ILETISIM_IZ)
    bag = BAGLANTI.search(bio)
    d["bio_baglanti"] = bag.group(0) if bag else None
    d["unsur"]["baglanti"] = bool(d["bio_baglanti"])

    for kod_u, ad_u, aciklama in BIO_UNSUR:
        if not d["unsur"].get(kod_u):
            d["eksik"].append({
                "kod": "bio_%s" % kod_u, "baslik": "%s: %s eksik" % (_platform_ad(url), ad_u),
                "kontrol": "%s profilinin herkese açık açıklaması (bio)" % _platform_ad(url),
                "bulgu": aciklama, "kaynak": url, "zaman": zaman, "agirlik": 1,
            })

    if d["bio_uzunluk"] < 25:
        d["eksik"].append({
            "kod": "bio_kisa", "baslik": "%s: profil açıklaması çok kısa" % _platform_ad(url),
            "kontrol": "Profil açıklamasının uzunluğu",
            "bulgu": "Açıklama %d karakter — profili açan kişiye anlatacak yer bırakılmamış"
                     % d["bio_uzunluk"],
            "kaynak": url, "zaman": zaman, "agirlik": 1})
    if not d["gorsel"]:
        d["eksik"].append({
            "kod": "profil_gorsel_yok", "baslik": "%s: profil görseli okunamadı" % _platform_ad(url),
            "kontrol": "Profil görseli (og:image)",
            "bulgu": "Profil görseli bulunamadı — hesap paylaşıldığında görselsiz çıkıyor",
            "kaynak": url, "zaman": zaman, "agirlik": 1})
    return d


def _platform_ad(url):
    u = (url or "").lower()
    for iz, ad in (("instagram", "Instagram"), ("facebook", "Facebook"),
                   ("linkedin", "LinkedIn"), ("youtube", "YouTube"),
                   ("tiktok", "TikTok"), ("x.com", "X"), ("twitter", "X")):
        if iz in u:
            return ad
    return "Sosyal hesap"


# ------------------------------------------------------------------ tutarlılık
def kullanici_tutarliligi(hesaplar):
    """
    Kullanıcı adları platformlar arasında aynı mı?
    Farklıysa marka araması bölünüyor — bulunması zorlaşıyor.
    """
    adlar = {p: (h.get("kullanici") or "").lower().strip("@")
             for p, h in (hesaplar or {}).items() if h.get("kullanici")}
    if len(adlar) < 2:
        return {"tutarli": None, "adlar": adlar, "not": "Kıyaslanacak ikinci hesap yok."}
    kume = set(adlar.values())
    if len(kume) == 1:
        return {"tutarli": True, "adlar": adlar,
                "not": "Tüm platformlarda aynı kullanıcı adı — marka araması bölünmüyor."}
    return {"tutarli": False, "adlar": adlar,
            "not": "Platformlarda farklı kullanıcı adları var (%s). Marka araması bölünüyor; "
                   "birini arayan diğerini bulamıyor." % ", ".join(sorted(kume))}


def karsiliklilik(hesaplar, site_kanallari, site_url=None):
    """
    Site → hesap ve hesap → site bağlantısı var mı?
    Tek yönlü bağ, Google'ın hesabı firmayla eşleştirmesini zorlaştırıyor.
    """
    siteden = {k.get("tur") for k in (site_kanallari or []) if k.get("tur") in
               ("instagram", "facebook", "linkedin", "youtube", "tiktok", "x")}
    hesaptan, okunamayan = set(), set()
    for p, h in (hesaplar or {}).items():
        sg = h.get("saglik") or {}
        if sg.get("okunabilirlik") != "açık":
            # Sayfayı okuyamadıysak "bağlantı yok" DİYEMEYİZ. Bilmiyoruz demektir.
            okunamayan.add(p)
        elif sg.get("bio_baglanti"):
            hesaptan.add(p)
    tumu = set(hesaplar or {})
    olculebilen = tumu - okunamayan
    return {
        "siteden_bagli": sorted(siteden),
        "hesaptan_bagli": sorted(hesaptan),
        "tek_yonlu": sorted(olculebilen - hesaptan),       # okunabildi ve bağlantı yok
        "okunamayan": sorted(okunamayan),                   # hüküm verilemedi
        "hic_bagli_degil": sorted(olculebilen - siteden - hesaptan),
        "tam": sorted(siteden & hesaptan),
    }


# ------------------------------------------------------------------ etkileşim kıyası
# Kaynak: yayınlanmış sektör kıyas derlemeleri, 2026 başı. Aralık verilmesinin
# sebebi bunların hesap büyüklüğüne göre değişmesi — küçük hesapta oran yüksek çıkar.
KIYAS = {
 # sektör: {platform: (zayıf, normal, iyi)}  → etkileşim oranı yüzde
 "insaat":   {"instagram": (0.6, 1.4, 3.0), "youtube": (0.5, 1.2, 2.5), "linkedin": (1.0, 2.2, 4.0)},
 "emlak":    {"instagram": (0.8, 1.8, 3.6), "tiktok": (2.0, 4.5, 9.0),  "youtube": (0.6, 1.4, 2.8)},
 "mimarlik": {"instagram": (1.0, 2.4, 4.5), "linkedin": (1.2, 2.6, 4.5)},
 "sanayi":   {"linkedin": (1.0, 2.2, 4.0),  "youtube": (0.5, 1.1, 2.2), "instagram": (0.5, 1.2, 2.5)},
 "mobilya":  {"instagram": (1.0, 2.2, 4.2), "tiktok": (2.5, 5.0, 10.0)},
 "otel":     {"instagram": (1.2, 2.8, 5.5), "tiktok": (2.5, 5.5, 11.0)},
 "isletme":  {"instagram": (1.0, 2.4, 4.8), "tiktok": (2.5, 5.0, 10.0), "facebook": (0.4, 1.0, 2.0)},
}
VARSAYILAN_KIYAS = {"instagram": (1.0, 2.2, 4.2), "youtube": (0.5, 1.2, 2.5),
                    "linkedin": (1.0, 2.2, 4.0), "tiktok": (2.5, 5.0, 10.0),
                    "facebook": (0.4, 1.0, 2.0), "x": (0.3, 0.8, 1.8)}

# Aylık paylaşım temposu beklentisi (sektör × platform)
TEMPO_BEKLENTI = {
 "instagram": 12, "tiktok": 12, "youtube": 2, "linkedin": 8, "facebook": 8, "x": 12,
}


def etkilesim_hesapla(sektor, platform, takipci, ortalama_etkilesim, kaynak="elle girildi"):
    """
    Etkileşim oranı = ortalama etkileşim / takipçi × 100.
    Sektör kıyasına göre yorumlanır. Rakamlar ELLE GİRİLİYOR ve öyle işaretleniyor.
    """
    try:
        takipci = int(takipci); ortalama_etkilesim = float(ortalama_etkilesim)
    except (TypeError, ValueError):
        return {"hata": "Takipçi ve ortalama etkileşim sayısal olmalı."}
    if takipci <= 0:
        return {"hata": "Takipçi sayısı sıfırdan büyük olmalı."}

    oran = round(100.0 * ortalama_etkilesim / takipci, 2)
    zayif, normal, iyi = (KIYAS.get(sektor) or {}).get(
        platform, VARSAYILAN_KIYAS.get(platform, (1.0, 2.2, 4.2)))

    if oran >= iyi:
        seviye, yorum = "iyi", ("Sektör üstü. İçerik tutuyor; sorun erişimde değil, "
                                "bu erişimin işe dönmesinde olabilir.")
    elif oran >= normal:
        seviye, yorum = "normal", ("Sektör ortalamasında. Format ve ilk üç saniye "
                                   "çalışmasıyla üst banda taşınabilir.")
    elif oran >= zayif:
        seviye, yorum = "zayif", ("Sektör ortalamasının altında. Takipçi var ama içerik "
                                  "onları harekete geçirmiyor — biçim sorunu.")
    else:
        seviye, yorum = "kotu", ("Belirgin şekilde düşük. Ya takipçi kitlesi gerçek "
                                 "müşteri değil ya da içerik hiç izlenmiyor.")
    return {
        "oran": oran, "seviye": seviye, "yorum": yorum,
        "kiyas": {"zayif": zayif, "normal": normal, "iyi": iyi},
        "takipci": takipci, "ortalama_etkilesim": ortalama_etkilesim,
        "platform": platform, "sektor": sektor,
        "kaynak": kaynak,
        "hedef_etkilesim": int(round(takipci * iyi / 100.0)),
        "fark": round(iyi - oran, 2),
        "zaman": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
    }


def tempo_yorumu(platform, aylik_paylasim):
    """Paylaşım temposu beklenen bandın neresinde?"""
    beklenen = TEMPO_BEKLENTI.get(platform, 8)
    try:
        n = int(aylik_paylasim)
    except (TypeError, ValueError):
        return None
    if n == 0:
        return {"seviye": "durmus", "beklenen": beklenen,
                "yorum": "Hesap duruyor. Duran hesap, olmayan hesaptan daha kötü sinyal "
                         "veriyor — ziyaretçi 'iş bırakmışlar' diye düşünüyor."}
    if n < beklenen * 0.5:
        return {"seviye": "seyrek", "beklenen": beklenen,
                "yorum": "Ayda %d paylaşım, beklenen %d. Bu tempoda algoritma hesabı "
                         "taşımıyor; içerik birikmiyor." % (n, beklenen)}
    if n > beklenen * 2:
        return {"seviye": "yogun", "beklenen": beklenen,
                "yorum": "Tempo yüksek. Sorun sıklıkta değil; her paylaşımın işe "
                         "yarayıp yaramadığına bakmak gerekiyor."}
    return {"seviye": "uygun", "beklenen": beklenen,
            "yorum": "Tempo beklenen bantta."}
