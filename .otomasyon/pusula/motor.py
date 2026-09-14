# -*- coding: utf-8 -*-
"""
MOTOR — siteyi işleten sistemin canlı künyesi.

Amaç: siteye ilk defa giren birinin "bunlar yazılım da yazıyor" cümlesini
OKUMASI değil, GÖRMESİ. İddia yerine ölçüm koyuyoruz.

Buradaki her sayı gerçek ve kaynağı belli:
  · sayfa sayısı        → repoda gerçekten kaç HTML var
  · denetim puanı       → seo/denetci.py'nin son çalıştırdığı sonuç
  · sorgu derlemesi     → veri/sorgular/ içindeki son günün kaydı
  · asistan soru sayısı → assets/asistan-veri.json
  · yayınlanmış iş      → assets/videolar.js içinde kimliği dolu kayıtlar
  · yazı sayısı         → blog/ altındaki sayfalar

Hiçbiri elle yazılmıyor; hepsi dosyadan sayılıyor. Sayamadığımız alan
JSON'a hiç girmiyor — sayfada da görünmüyor.
"""
import datetime, json, os, re

from .ayarlar import SITE_KOK, KOK_DIZIN


def _html_say(kok):
    n = 0
    for d, altlar, dosyalar in os.walk(kok):
        altlar[:] = [a for a in altlar if a not in ("assets", ".git", ".github", "node_modules")]
        n += sum(1 for f in dosyalar if f.endswith(".html"))
    return n


def _blog_say(kok):
    b = os.path.join(kok, "blog")
    if not os.path.isdir(b):
        return None
    return sum(1 for f in os.listdir(b) if f.endswith(".html") and f != "index.html")


def _il_say(kok):
    s = os.path.join(kok, "sehir")
    if not os.path.isdir(s):
        return None
    iller = set()
    for f in os.listdir(s):
        if f.endswith(".html") and f != "index.html":
            iller.add(f[:-5].split("-")[0])
    return len(iller) or None


def _is_say(kok):
    y = os.path.join(kok, "assets", "videolar.js")
    if not os.path.exists(y):
        return None
    s = open(y, encoding="utf-8").read()
    return len(re.findall(r'id:"[A-Za-z0-9_-]{6,}"', s)) + len(re.findall(r'yerel:"[a-z0-9-]+"', s))


def _asistan(kok):
    y = os.path.join(kok, "assets", "asistan-veri.json")
    if not os.path.exists(y):
        return None, None
    try:
        d = json.load(open(y, encoding="utf-8"))
    except Exception:
        return None, None
    return len(d.get("soru") or []), len(d.get("sayfa") or [])


def _sorgular():
    """Son sorgu derlemesi: kaç sorgu, hangi gün."""
    dizin = os.path.join(KOK_DIZIN, "veri", "sorgular")
    if not os.path.isdir(dizin):
        return None, None
    dosyalar = sorted(f for f in os.listdir(dizin) if f.endswith(".json"))
    if not dosyalar:
        return None, None
    son = dosyalar[-1]
    try:
        d = json.load(open(os.path.join(dizin, son), encoding="utf-8"))
    except Exception:
        return None, None
    n = len(d.get("sorgular") or [])
    return (n or None), son[:-5]


def _denetim():
    """seo/denetci.py son sonucu — varsa dosyadan, yoksa None."""
    for aday in (os.path.join(KOK_DIZIN, "veri", "denetim.json"),
                 os.path.join(KOK_DIZIN, "cikti", "denetim.json")):
        if os.path.exists(aday):
            try:
                d = json.load(open(aday, encoding="utf-8"))
                return d.get("sayfa"), d.get("hata"), d.get("uyari"), d.get("puan")
            except Exception:
                pass
    return None, None, None, None


def veri(kok=None):
    kok = kok or SITE_KOK
    soru, dizin_sayfa = _asistan(kok)
    sorgu_adet, sorgu_gun = _sorgular()
    d_sayfa, d_hata, d_uyari, d_puan = _denetim()

    olcum = []

    def ekle(anahtar, deger, etiket, alt):
        if deger is None:
            return          # sayamadığımızı yazmıyoruz
        olcum.append({"k": anahtar, "d": deger, "e": etiket, "a": alt})

    ekle("sayfa", _html_say(kok), "sayfa yayında",
         "hepsi kendi üreticimizden çıktı, elle yazılmadı")
    ekle("il", _il_say(kok), "il için ayrı sayfa",
         "her il kendi metniyle, şablon kopyası değil")
    ekle("yazi", _blog_say(kok), "yazı",
         "SEO kapısını geçmeyen yazı yayınlanmıyor")
    ekle("soru", soru, "soru-cevap",
         "site asistanı bunlardan cevap veriyor")
    ekle("is", _is_say(kok), "yayınlanmış iş",
         "künyesiyle birlikte")
    if d_puan is not None:
        ekle("denetim", d_puan, "SEO denetim puanı",
             "%d hata, %d uyarı" % (d_hata or 0, d_uyari or 0))
    ekle("sorgu", sorgu_adet, "arama sorgusu derlendi",
         "son derleme: %s" % (sorgu_gun or "—"))

    return {
        "guncel": datetime.date.today().isoformat(),
        "saat": datetime.datetime.now().strftime("%H:%M"),
        "olcum": olcum,
        "boru": [
            {"ad": "tara",   "not": "Google otomatik tamamlama ve Trends'ten günün sorguları"},
            {"ad": "puanla", "not": "niyet ve rekabet skoru, 0–10"},
            {"ad": "yaz",    "not": "konu seçimi ve taslak"},
            {"ad": "denetle","not": "SEO kapısı — 100 altı yayınlanmıyor"},
            {"ad": "yayınla","not": "sayfa, site haritası ve şema aynı anda"},
        ],
    }


def yaz(kok=None):
    kok = kok or SITE_KOK
    d = veri(kok)
    hedef = os.path.join(kok, "assets", "motor.json")
    with open(hedef, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, separators=(",", ":"))
    return {"dosya": hedef, "olcum": len(d["olcum"]), "guncel": d["guncel"]}


if __name__ == "__main__":
    print(json.dumps(yaz(), ensure_ascii=False, indent=2))
