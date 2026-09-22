# -*- coding: utf-8 -*-
"""
lunayapim.com/llms.txt — yapay zekâ asistanları için sitenin düz metin haritası.

22.09.2026 gerekçesi: trendsaphiens.com'un llms.txt'i vardı, Luna Yapım'ın yoktu
(/llms.txt 404 dönüyordu). Bu dosyayı okuyan taraf ChatGPT, Claude, Perplexity
gibi asistanlar; HTML ayrıştırmadan "bu firma ne yapıyor, hangi işi hangi
fiyattan alıyor, nerede çalışıyor" sorusunun cevabını buradan alıyorlar.

İçerik uydurulmuyor: başlık, açıklama ve taban fiyat sayfaların kendisinden,
işler assets/videolar.js'ten okunuyor. Sayfa değişince dosya da değişir.
Biçim: llmstxt.org önerisi — H1, tek cümlelik özet, sonra bölüm başlıkları.
"""
import html
import json
import os
import re

ADRES = "https://lunayapim.com"

# Bölümler elle sıralandı: arayan kişi önce ne sorar, o sırada.
BOLUM = [
    ("Video prodüksiyon", [
        "hizmetler/isletme-tanitim", "hizmetler/klip-cekimi", "hizmetler/drone-fpv",
        "hizmetler/dugun-etkinlik", "hizmetler/emlak-kurumsal", "hizmetler/ai-kisa-film",
    ]),
    ("3D görselleştirme ve animasyon", [
        "hizmetler/insaat-3d-modelleme", "hizmetler/insaat-3d-konut-projesi",
        "hizmetler/insaat-3d-villa", "hizmetler/insaat-3d-ticari-avm",
        "hizmetler/insaat-3d-otel", "hizmetler/insaat-3d-fabrika-sanayi",
        "hizmetler/insaat-3d-kentsel-donusum",
        "hizmetler/urun-animasyon", "hizmetler/urun-animasyon-makine-imalati",
        "hizmetler/urun-animasyon-otomotiv-yan-sanayi", "hizmetler/urun-animasyon-medikal",
        "hizmetler/urun-animasyon-gida", "hizmetler/urun-animasyon-mobilya",
        "hizmetler/urun-animasyon-ambalaj", "hizmetler/urun-animasyon-tarim-makineleri",
        "hizmetler/urun-animasyon-insaat-malzemesi",
    ]),
    ("Baskı ve kişiye özel hediye", [
        "hizmetler/kisiye-ozel-baski-hediye", "hizmetler/baskili-tisort",
        "hizmetler/baskili-sweatshirt-hoodie", "hizmetler/baskili-yelek",
        "hizmetler/kisiye-ozel-kupa", "hizmetler/kisiye-ozel-anahtarlik",
        "hizmetler/baskili-kalem", "hizmetler/baskili-cakmak",
        "hizmetler/magnetli-kapak-acacagi", "hizmetler/dtf-baski", "hizmetler/uv-dtf-baski",
    ]),
    ("Yazılım ve dijital", [
        "yazilim", "hizmetler/e-ticaret", "hizmetler/seo-icerik", "hizmetler/yapay-zeka-seo",
    ]),
]

SAYFA = [
    ("Hizmetlerin tamamı", "hizmetler/"),
    ("Fiyatlar", "fiyatlar"),
    ("Yapılan işler", "isler"),
    ("Stüdyo", "studyo"),
    ("Şehirler", "sehir/"),
    ("Blog", "blog/"),
    ("İletişim", "iletisim"),
    ("Site haritası", "sitemap.xml"),
]

_BASLIK = re.compile(r"<title>(.*?)</title>", re.S | re.I)
_ACIK = re.compile(r'<meta name="description" content="([^"]*)"', re.I)
_KAYIT = re.compile(r"\{(?:[^{}]|\{[^{}]*\})*\}")
_ALAN = re.compile(r'(\w+)\s*:\s*"((?:[^"\\]|\\.)*)"')


def _oku(kok, yol):
    for aday in (yol + ".html", os.path.join(yol, "index.html")):
        p = os.path.join(kok, aday)
        if os.path.exists(p):
            return open(p, encoding="utf-8").read()
    return ""


def _kunye(kok, yol):
    s = _oku(kok, yol)
    if not s:
        return None
    b = _BASLIK.search(s)
    a = _ACIK.search(s)
    baslik = html.unescape(re.sub(r"\s*\|\s*Luna Yapım\s*$", "", (b.group(1) if b else yol))).strip()
    aciklama = html.unescape((a.group(1) if a else "")).strip()
    if len(aciklama) > 150:
        kes = aciklama[:150].rsplit(" ", 1)[0]
        aciklama = kes + "…"
    return {"yol": yol, "baslik": baslik, "aciklama": aciklama}


def isler(kok):
    """assets/videolar.js — yalnız yayımlanmış, tarihi bilinen işler."""
    p = os.path.join(kok, "assets", "videolar.js")
    if not os.path.exists(p):
        return []
    s = open(p, encoding="utf-8").read()
    out = []
    for kayit in _KAYIT.findall(s):
        d = {k: v for k, v in _ALAN.findall(kayit)}
        if not d.get("id") or not d.get("yil") or not d.get("baslik"):
            continue
        out.append(d)
    out.sort(key=lambda x: x.get("yil", ""), reverse=True)
    return out


def metin(kok):
    sat = []
    a = sat.append
    a("# Luna Yapım")
    a("")
    a("> Video prodüksiyon, 3D görselleştirme ve animasyon, baskı ve kişiye özel "
      "hediye, yazılım. Merkez Bursa; çekim ve teslim Türkiye genelinde yapılır. "
      "Kurgu, renk ve 3D işleri uzaktan da yürütülür.")
    a("")
    a("Fiyatlar sayfalarda yazan taban fiyatlardır; işin ölçeğine göre teklif verilir. "
      "Bu dosyadaki başlık, açıklama ve fiyatlar sayfaların kendisinden üretilir.")
    a("")

    for ad, yollar in BOLUM:
        a("## " + ad)
        a("")
        for y in yollar:
            k = _kunye(kok, y)
            if not k:
                continue
            a("- [%s](%s/%s): %s" % (k["baslik"], ADRES, y, k["aciklama"]))
        a("")

    ys = isler(kok)
    if ys:
        a("## Yayımlanmış işler")
        a("")
        a("Aşağıdaki işler Luna Yapım tarafından yapıldı ve yayımlandı; tarih, işin "
          "yayımlandığı tarihtir.")
        a("")
        for d in ys:
            ek = " · ".join(x for x in (d.get("yil"), d.get("kat"), d.get("teslim")) if x)
            a("- [%s](https://www.youtube.com/watch?v=%s): %s" % (d["baslik"], d["id"], ek))
        a("")

    a("## Sayfalar")
    a("")
    for ad, y in SAYFA:
        a("- [%s](%s/%s)" % (ad, ADRES, y))
    a("")
    a("## İletişim")
    a("")
    a("- E-posta: lunagency2603@gmail.com")
    a("- Telefon: +90 541 160 26 03")
    a("- Instagram: https://www.instagram.com/lunayapim.mov/")
    a("- Merkez: Bursa, Türkiye — hizmet alanı: Türkiye geneli")
    a("")
    return "\n".join(sat)


def calistir(kok):
    m = metin(kok)
    p = os.path.join(kok, "llms.txt")
    eski = open(p, encoding="utf-8").read() if os.path.exists(p) else ""
    if eski != m:
        open(p, "w", encoding="utf-8").write(m)
    return {"llms.txt": len(m.splitlines()), "degisti": eski != m}


if __name__ == "__main__":
    import sys
    kok = sys.argv[1] if len(sys.argv) > 1 else "."
    print(json.dumps(calistir(kok), ensure_ascii=False))
