# -*- coding: utf-8 -*-
"""
TERİM HİZALAMA — bizim dediğimiz kelime ≠ arayanın yazdığı kelime.

Kanıt: Search Console'da "ankara tanıtım filmi çekimi", "kurumsal tanıtım filmi
ankara" sorgularında çıkıyoruz; sayfalarımız "tanıtım videosu" diyor. Arayan
"3d render fiyatları" yazıyor, biz "3D modelleme fiyatları". Google eş anlam
bilir ama başlıkta birebir kelime hâlâ tıklanmayı belirliyor.

Kural: yalnızca BAŞLIK, H1, H2, giriş (lede) ve meta açıklamaya dokunulur.
Gövde metni doğal kalır — her yerde aynı kelime yapay durur.
Her satır: (bizim biçim, arayanın biçimi, kanıt). Kanıt "sc" = Search Console,
"ac" = otomatik tamamlama (sorgu.py derleyince buraya eklenir).
"""
import io, os, re

ESLEME = [
    ("tanıtım videosu",       "tanıtım filmi",          "sc"),
    ("Tanıtım Videosu",       "Tanıtım Filmi",          "sc"),
    ("kurumsal tanıtım videosu", "kurumsal tanıtım filmi", "sc"),
    ("Havadan 4K Video",      "Havadan Görüntü ve 4K Video", "sc"),
    ("mimari görselleştirme", "3D render ve mimari görselleştirme", "sc"),
]

ALANLAR = [
    (re.compile(r"(<title>)(.*?)(</title>)", re.S), 2),
    (re.compile(r"(<h1[^>]*>)(.*?)(</h1>)", re.S), 2),
    (re.compile(r"(<h2[^>]*>)(.*?)(</h2>)", re.S), 2),
    (re.compile(r'(<p class="lede">)(.*?)(</p>)', re.S), 2),
    (re.compile(r'(<meta name="description" content=")(.*?)(")', re.S), 2),
    (re.compile(r'(<meta property="og:title" content=")(.*?)(")', re.S), 2),
    (re.compile(r'(<meta property="og:description" content=")(.*?)(")', re.S), 2),
]


def _uygula(metin):
    for bizim, arayan, _ in ESLEME:
        if bizim in metin and arayan not in metin:
            metin = metin.replace(bizim, arayan)
    return metin


def hizala(html):
    d = 0
    for desen, _ in ALANLAR:
        def yer(m):
            nonlocal d
            y = _uygula(m.group(2))
            if y != m.group(2):
                d += 1
            return m.group(1) + y + m.group(3)
        html = desen.sub(yer, html)
    return html, d


def calistir(kok):
    sayfa = degisim = 0
    for dz, altlar, dosyalar in os.walk(kok):
        altlar[:] = [a for a in altlar if a not in ("assets", ".git", ".github")]
        for f in dosyalar:
            if not f.endswith(".html") or f == "matrix.html":
                continue
            y = os.path.join(dz, f)
            s = io.open(y, encoding="utf-8").read()
            s2, d = hizala(s)
            if d:
                io.open(y, "w", encoding="utf-8").write(s2)
                sayfa += 1; degisim += d
    return {"sayfa": sayfa, "degisen_alan": degisim}


if __name__ == "__main__":
    from .ayarlar import SITE_KOK
    print(calistir(SITE_KOK))
