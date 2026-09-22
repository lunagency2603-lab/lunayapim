# -*- coding: utf-8 -*-
"""
LUNA YAPIM SAYFALARINI ARAMA MOTORLARINA BİLDİR.

22.09.2026'da ölçtük: Bing'de (ChatGPT Search ve Copilot'un dizini) Luna Yapım
hizmet sorgularının hiçbirinde çıkmıyoruz. Nedeni yapı değil — sayfalar
sitemap'te var, iç bağlantıları da var. Neden şu: IndexNow bildirimi yalnız
trend.py içinden çağrılıyordu, yani SADECE TrendSaphiens yazıları bildiriliyordu.
Luna Yapım'ın hizmet sayfaları (baskı ve hediye kolunun 12 sayfası dahil) hiç
bildirilmedi; motorlar onları kendi keşfetmeyi bekledi.

Bu modül o boşluğu kapatır:
  · varsayılan: son commit'te değişen .html sayfalarını bildirir
  · --hepsi    : hizmet, şehir, blog ve kök sayfalarının tamamını bildirir
                 (bir kez, yeni bir kol eklendiğinde ya da ilk kurulumda)

/trend/ adresleri buradan bildirilmez — onları trend.py zaten bildiriyor.
Ağ ister; GitHub Actions'ta çalışır.
"""
import os, subprocess, sys

from .ayarlar import SITE_KOK
from . import indexnow as IN

# Bildirilecek kökler: hizmet ve içerik sayfaları
KLASOR = ("hizmetler", "sehir", "blog", "yapay-zeka", "gundem")
KOK_SAYFA = ("index.html", "yazilim.html", "studyo.html", "isler.html",
             "fiyatlar.html", "iletisim.html", "kariyer.html", "matrix.html")
# Bunlar bildirilmez
HARIC = ("trend/", "onizleme/", "admin", "404.html", "bulten/")


def _url(yol):
    """Depo yolu → yayındaki uzantısız adres."""
    y = yol.replace(os.sep, "/")
    if y.endswith("/index.html"):
        y = y[: -len("index.html")]
    elif y.endswith(".html"):
        y = y[:-5]
    return "https://lunayapim.com/" + y.lstrip("/")


def _uygun(yol):
    y = yol.replace(os.sep, "/").lstrip("./")
    if not y.endswith(".html"):
        return False
    if any(y.startswith(h) or ("/" + h) in ("/" + y) for h in HARIC):
        return False
    if "/" not in y:
        return y in KOK_SAYFA
    return y.split("/")[0] in KLASOR


def degisenler(kok=None):
    """Son commit'te değişen uygun sayfalar."""
    kok = kok or SITE_KOK
    try:
        cikti = subprocess.run(["git", "diff", "--name-only", "HEAD~1", "HEAD"],
                               cwd=kok, capture_output=True, text=True, timeout=60).stdout
    except Exception as ex:
        print("git diff okunamadı:", ex)
        return []
    return [y.strip() for y in cikti.splitlines() if _uygun(y.strip())]


def hepsi(kok=None):
    """Sitedeki bütün uygun sayfalar."""
    kok = kok or SITE_KOK
    out = []
    for dp, dn, fn in os.walk(kok):
        dn[:] = [d for d in dn if not d.startswith(".") and d not in ("trend", "onizleme", "assets", "bulten")]
        for f in fn:
            y = os.path.relpath(os.path.join(dp, f), kok)
            if _uygun(y):
                out.append(y)
    return sorted(out)


def calistir(hepsini=False, kok=None):
    kok = kok or SITE_KOK
    yollar = hepsi(kok) if hepsini else degisenler(kok)
    if not yollar:
        return {"bildirilen": 0, "not": "değişen Luna Yapım sayfası yok"}
    adresler = [_url(y) for y in yollar]
    sonuc = IN.bildir(adresler, kok)
    return {"bildirilen": len(adresler),
            "ornek": adresler[:5],
            "uc": [(x.get("uc"), x.get("durum")) for x in (sonuc.get("sonuc") or [])],
            "hata": sonuc.get("hata")}


if __name__ == "__main__":
    import json
    print(json.dumps(calistir("--hepsi" in sys.argv), ensure_ascii=False))
