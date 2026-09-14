# -*- coding: utf-8 -*-
"""
Luna Asistan — sitenin kendi içeriğinden kurulan yapay zekâ destek katmanı.

Neden dış servis değil:
  · API anahtarı yok, aylık ücret yok, kredi tükenmesi yok
  · ziyaretçinin sorusu hiçbir yere gitmiyor — cevap tarayıcıda üretiliyor
  · uydurma cevap veremez; yalnızca BİZİM yazdığımız metni gösterir, kaynak
    sayfayı da bağlar

Ne yapar: 336 sayfadaki başlıkları, açıklamaları ve SSS soru-cevap çiftlerini
tek bir arama dizinine çevirir. assets/asistan-veri.json olarak yazar.
assets/asistan.js bu dizini okuyup soruyu eşler.

Cevabı bulamazsa uydurmaz: "bunu tam bilemedim" der ve WhatsApp'a bağlar.
Sorulan ama karşılığı olmayan sorular ölçüm katmanına düşer — içerik planı
oradan besleniyor.
"""
import html as _html
import json, os, re, unicodedata, datetime

from .ayarlar import SITE_KOK, FIRMA

ATLA_DIZIN = {"assets", ".git", "node_modules", ".github"}
ATLA_DOSYA = {"404.html"}

_ETIKET = re.compile(r"<[^>]+>")
_BETIK = re.compile(r"<(script|style|noscript)[^>]*>.*?</\1>", re.S | re.I)
_SSS = re.compile(r"<details[^>]*>\s*<summary[^>]*>(.*?)</summary>(.*?)</details>", re.S | re.I)
_H1 = re.compile(r"<h1[^>]*>(.*?)</h1>", re.S | re.I)
_H2 = re.compile(r"<h2[^>]*>(.*?)</h2>", re.S | re.I)
_TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
_DESC = re.compile(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', re.S | re.I)


def duz(g, azami=None):
    """HTML'i düz metne çevirir."""
    g = _BETIK.sub(" ", g or "")
    g = _ETIKET.sub(" ", g)
    g = _html.unescape(g)
    g = re.sub(r"\s+", " ", g).strip()
    return g[:azami] if azami else g


def anahtarla(x):
    """Eşleştirme için sadeleştirilmiş biçim: küçük harf, Türkçe harfler ASCII."""
    x = (x or "").lower()
    x = (x.replace("ı", "i").replace("ğ", "g").replace("ü", "u")
          .replace("ş", "s").replace("ö", "o").replace("ç", "c").replace("â", "a"))
    x = unicodedata.normalize("NFKD", x)
    x = "".join(c for c in x if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", x).strip()


def _adres(kok, yol):
    """Dosya yolunu uzantısız site adresine çevirir."""
    b = os.path.relpath(yol, kok).replace(os.sep, "/")
    if b.endswith("index.html"):
        b = b[: -len("index.html")]
    elif b.endswith(".html"):
        b = b[:-5]
    return "/" + b.lstrip("/")


_SEHIR_EK = re.compile(r"\b[A-ZÇĞİÖŞÜ][a-zçğıöşü]+['\u2019]?(?:da|de|ta|te|nda|nde)\b")


def soru_imzasi(soru):
    """Aynı sorunun şehir varyantlarını tek imzada toplar."""
    return anahtarla(_SEHIR_EK.sub(" ", soru))


def _oncelik(adres):
    """Kaynak gösterirken hangi sayfa önce gelsin (küçük = önce)."""
    p = adres.strip("/").split("/")
    ilk = p[0] if p and p[0] else ""
    return {"": 0, "hizmetler": 1, "yazilim": 2, "blog": 3,
            "sektor": 4, "yapay-zeka": 5, "sehir": 9}.get(ilk, 6)


def _kategori(adres):
    p = adres.strip("/").split("/")
    if not p or p == [""]:
        return "Ana sayfa"
    return {"hizmetler": "Hizmet", "sehir": "Bölge", "blog": "Yazı",
            "sektor": "Sektör", "yapay-zeka": "Yapay zekâ"}.get(p[0], "Sayfa")


def tara(kok=None):
    """Siteyi gezip sayfa ve soru listesini çıkarır."""
    kok = kok or SITE_KOK
    sayfalar, sorular, gorulen_soru = [], [], {}
    for dizin, altlar, dosyalar in os.walk(kok):
        altlar[:] = [a for a in altlar if a not in ATLA_DIZIN and not a.startswith(".")]
        for d in sorted(dosyalar):
            if not d.endswith(".html") or d in ATLA_DOSYA:
                continue
            yol = os.path.join(dizin, d)
            try:
                g = open(yol, encoding="utf-8").read()
            except Exception:
                continue
            if "noindex" in g[:4000]:
                continue
            adres = _adres(kok, yol)
            baslik = duz((_H1.search(g) or _TITLE.search(g) or [None, ""])[1], 120) \
                if (_H1.search(g) or _TITLE.search(g)) else ""
            m = _TITLE.search(g)
            tam_baslik = duz(m.group(1), 140) if m else baslik
            m = _DESC.search(g)
            ozet = duz(m.group(1), 260) if m else ""
            h2 = " · ".join(duz(x, 70) for x in _H2.findall(g)[:8])
            si = len(sayfalar)
            sayfalar.append({"u": adres, "b": baslik or tam_baslik,
                             "o": ozet, "h": h2, "k": _kategori(adres)})

            for soru_ham, cevap_ham in _SSS.findall(g):
                soru = duz(soru_ham, 200)
                cevap = duz(cevap_ham, 700)
                if len(soru) < 8 or len(cevap) < 20:
                    continue
                a = soru_imzasi(soru)
                if a in gorulen_soru:
                    # aynı soru başka sayfada da var — sayfa listesine ekle.
                    # Daha genel bir sayfadan geliyorsa metni oradan al: şehir
                    # sayfasının "Adana'da…" varyantı yerine ana hizmet metni kalsın.
                    q0 = sorular[gorulen_soru[a]]
                    q0["p"].append(si)
                    if _oncelik(adres) < _oncelik(sayfalar[q0["p"][0]]["u"]):
                        q0["s"], q0["c"] = soru, cevap
                    continue
                gorulen_soru[a] = len(sorular)
                sorular.append({"s": soru, "c": cevap, "p": [si]})
    return sayfalar, sorular


def veri(kok=None):
    kok = kok or SITE_KOK
    sayfalar, sorular = tara(kok)
    # her sorunun sayfa listesi kısa kalsın (ilk 3 yeter)
    for q in sorular:
        p = sorted(set(q["p"]), key=lambda i: (_oncelik(sayfalar[i]["u"]), i))
        # Yalnızca il sayfalarından gelen soru: 81 ilin şablonu, temsilcisi Adana
        # oldu. Genel bir soruda öne çıkmasın diye işaretliyoruz.
        if p and sayfalar[p[0]]["u"].startswith("/sehir/"):
            q["il"] = 1
        q["p"] = p[:3]
    return {
        "guncel": datetime.date.today().isoformat(),
        "firma": {"ad": FIRMA["ad"], "tel": FIRMA.get("telefon", ""),
                  "wa": FIRMA.get("wa", "")},
        "sayfa": sayfalar,
        "soru": sorular,
    }


def yaz(kok=None):
    kok = kok or SITE_KOK
    d = veri(kok)
    hedef = os.path.join(kok, "assets", "asistan-veri.json")
    with open(hedef, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, separators=(",", ":"))
    return {"dosya": hedef, "boyut_kb": round(os.path.getsize(hedef) / 1024, 1),
            "sayfa": len(d["sayfa"]), "soru": len(d["soru"]), "guncel": d["guncel"]}


if __name__ == "__main__":
    print(json.dumps(yaz(), ensure_ascii=False, indent=2))
