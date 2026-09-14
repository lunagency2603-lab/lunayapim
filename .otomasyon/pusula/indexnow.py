# -*- coding: utf-8 -*-
"""
INDEXNOW — yeni/güncellenen sayfaları arama motorlarına anında bildirir.

Neden bu yol:
  · Google'ın eski "sitemap ping" ucu (google.com/ping?sitemap=) 2023'te
    KAPATILDI. Artık çalışmıyor; hâlâ öneren rehberler eski.
  · Search Console'un "Dizine ekleme iste" düğmesinin API'si (URL Inspection)
    OAuth istiyor ve günlük kotası çok düşük — otomatikleştirmeye uygun değil.
  · IndexNow açık bir protokol: tek anahtar dosyası, tek HTTP isteği.
    Bing, Yandex, Seznam ve Naver destekliyor. Bir motora bildirdiğinde
    protokole dahil olanların hepsine dağıtılıyor.

Google tarafı için dürüst durum: IndexNow'ı resmî olarak kullandığını
söylemiyor. Google'ın yolu sitemap — biz de her yayında sitemap.xml'in
lastmod'unu güncelliyoruz (yayin.py yapıyor) ve Search Console'a bildirilmiş
sitemap zaten düzenli taranıyor. Yeni bir yazıyı acele ettirmek istersen
Search Console → URL İnceleme → "Dizine ekleme iste" tek seferlik el işidir.

Cloudflare kullanıyorsan: Hız (Speed) → Optimizasyon → "Crawler Hints"
açıldığında Cloudflare değişiklikleri IndexNow üzerinden kendi de bildiriyor.
İkisi birlikte çalışır, zararı yok.
"""
import os, json, uuid, datetime, urllib.parse

from .kaynaklar.agir import getir
from .ayarlar import SITE_KOK

# Protokole dahil uçlar. Birine bildirmek yeterli ama iki uç daha sağlam.
UCLAR = (
    ("IndexNow", "https://api.indexnow.org/indexnow"),
    ("Bing", "https://www.bing.com/indexnow"),
)

ALAN = "lunayapim.com"


def anahtar_dosyasi(kok=None):
    """Site kökündeki IndexNow anahtar dosyasını bulur; yoksa None."""
    kok = kok or SITE_KOK
    if not os.path.isdir(kok):
        return None
    for d in os.listdir(kok):
        if d.endswith(".txt") and len(d) == 36 and d[:32].isalnum():
            return os.path.join(kok, d)
    return None


def anahtar(kok=None, uret=True):
    """
    Mevcut anahtarı döner. Yoksa ve uret=True ise yeni anahtar üretip
    site köküne <anahtar>.txt olarak yazar (protokolün istediği biçim).
    """
    kok = kok or SITE_KOK
    y = anahtar_dosyasi(kok)
    if y:
        return {"anahtar": os.path.basename(y)[:-4], "dosya": y, "yeni": False}
    if not uret:
        return None
    a = uuid.uuid4().hex
    y = os.path.join(kok, "%s.txt" % a)
    with open(y, "w", encoding="utf-8") as f:
        f.write(a)
    return {"anahtar": a, "dosya": y, "yeni": True}


def _robots_izin_ver(kok=None):
    """Anahtar dosyası robots.txt tarafından engellenmesin."""
    kok = kok or SITE_KOK
    y = os.path.join(kok, "robots.txt")
    if not os.path.isfile(y):
        return False
    g = open(y, encoding="utf-8").read()
    # kökte Allow: / zaten var; ek bir şey gerekmiyor. Sadece yanlışlıkla
    # .txt engellenmişse uyarmak için kontrol ediyoruz.
    return "Disallow: /*.txt" not in g and "Disallow: /*.txt$" not in g


def bildir(adresler, kok=None, alan=None):
    """
    Adresleri IndexNow ile bildirir.
    Döner: {anahtar, gonderilen, sonuc:[{uc, durum, not}], uyari}
    """
    kok = kok or SITE_KOK
    alan = alan or ALAN
    a = anahtar(kok)
    if not a:
        return {"hata": "Site klasörü bulunamadı: %s" % kok}

    temiz = []
    for u in adresler:
        u = (u or "").strip()
        if not u:
            continue
        if not u.startswith("http"):
            u = "https://%s/%s" % (alan, u.lstrip("/"))
        if urllib.parse.urlparse(u).netloc.endswith(alan):
            temiz.append(u)
    temiz = list(dict.fromkeys(temiz))[:10000]
    if not temiz:
        return {"hata": "Bildirilecek geçerli adres yok."}

    govde = {
        "host": alan,
        "key": a["anahtar"],
        "keyLocation": "https://%s/%s.txt" % (alan, a["anahtar"]),
        "urlList": temiz,
    }
    sonuc = []
    for ad, uc in UCLAR:
        kod, yanit, _ = getir(uc, veri=govde, zaman_asimi=20,
                              basliklar={"Content-Type": "application/json; charset=utf-8"})
        sonuc.append({"uc": ad, "durum": kod, "not": _yorum(kod, yanit)})
    return {
        "anahtar": a["anahtar"],
        "anahtar_yeni": a["yeni"],
        "anahtar_adresi": govde["keyLocation"],
        "gonderilen": len(temiz),
        "adresler": temiz[:25],
        "sonuc": sonuc,
        "robots_uygun": _robots_izin_ver(kok),
        "zaman": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
    }


def _yorum(kod, yanit):
    if kod == 200:
        return "Kabul edildi."
    if kod == 202:
        return "Alındı; anahtar doğrulaması sürüyor (sitenin yayında olması gerekiyor)."
    if kod == 400:
        return "İstek biçimi reddedildi."
    if kod == 403:
        return ("Anahtar doğrulanamadı. Anahtar dosyasının sitede YAYINDA olması gerekiyor — "
                "önce siteyi yayınla, sonra tekrar bildir.")
    if kod == 422:
        return "Adresler bu alan adına ait değil ya da anahtar eşleşmiyor."
    if kod == 429:
        return "Çok fazla istek; bir süre bekle."
    if kod == 0:
        return "Uca ulaşılamadı (internet yok ya da engelli)."
    return "Beklenmeyen yanıt: %s" % (yanit or "")[:120]


def durum(kok=None):
    """Panelde gösterilecek özet."""
    kok = kok or SITE_KOK
    a = anahtar(kok, uret=False)
    return {
        "kurulu": bool(a),
        "anahtar": a["anahtar"] if a else None,
        "dosya": os.path.basename(a["dosya"]) if a else None,
        "adres": ("https://%s/%s" % (ALAN, os.path.basename(a["dosya"]))) if a else None,
        "robots_uygun": _robots_izin_ver(kok),
        "not": ("Anahtar dosyası site kökünde. Yayınladıktan sonra bildirimler çalışır."
                if a else
                "Henüz anahtar yok. 'Anahtar üret' dediğinde site köküne bir .txt dosyası "
                "koyulur; siteyi yayınladıktan sonra bildirim yapılabilir."),
    }
