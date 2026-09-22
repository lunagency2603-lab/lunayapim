# -*- coding: utf-8 -*-
"""
ANA HİZMET SAYFASI → SEKTÖR/ALT TÜR SAYFALARI BAĞLANTI BLOĞU

Bulgu (22.09.2026): Search Console'da 162 sayfa "keşfedildi, dizine alınmadı"
diyordu ve listenin tamamı sektör sayfalarıydı (insaat-3d-*, urun-animasyon-*).
İç bağlantı sayımı sebebi açıkça gösterdi:

    urun-animasyon.html        575 gelen bağlantı
    insaat-3d-modelleme.html   572
    klip-cekimi.html           566
    ...
    urun-animasyon-gida.html     1      ← yalnız hizmetler/index'ten
    urun-animasyon-insaat-malzemesi.html  1

Yani sitenin bütün iç otoritesi üç sayfada toplanmış, o üç sayfa da kendi alt
sayfalarına HİÇ bağlanmıyordu. Google bir sayfayı keşfedip taramıyorsa çoğu
zaman söylediği şudur: "buraya giden yol zayıf, sıraya aldım". Yol buydu.

Bu modül her ana sayfaya "… göre" bloğu ekler: gerçekten var olan alt
sayfalara bağlantı, başlığı da o sayfanın kendi <title>'ından okunur.
Etkisiz tekrarlanabilir — ikinci çalıştırma bloğu yeniler, çoğaltmaz.
(Kardeş sayfalar arası bağlantı ayrı iş: sektor_sayfalari.py içinde.)
"""
import html
import io
import os
import re

# ana sayfa slug → (alt sayfa önek(ler)i, blok başlığı, açıklama)
AILE = {
    "urun-animasyon": (
        ("urun-animasyon-",),
        "Sektöre göre ürün animasyonu",
        "Her sektörün anlatım sorunu başka: birinde kesit, ötekinde üretim hattı, "
        "ötekinde montaj sırası konuşuyor. Aşağıdaki sayfaların her biri o sektörün "
        "kendi sorusuna göre yazıldı."),
    "insaat-3d-modelleme": (
        ("insaat-3d-",),
        "Yapı türüne göre 3D görselleştirme",
        "Görseli kimin izlediği yapıya göre değişiyor: konutta alıcı, sanayide "
        "yatırımcı ve izin veren kurum, kentsel dönüşümde hak sahibi. Her tür için "
        "ayrı sayfa var."),
    "kisiye-ozel-baski-hediye": (
        ("baskili-", "kisiye-ozel-", "dtf-", "uv-dtf-", "magnetli-"),
        "Ürüne göre baskı ve hediye",
        "Baskı yöntemi ürüne göre değişiyor: tekstilde DTF, cam ve metalde UV DTF. "
        "Her ürünün kendi sayfasında ölçü, adet ve teslim süresi yazılı."),
}

BAS = "<!-- sektor-baglari -->"
SON = "<!-- /sektor-baglari -->"


def _baslik(yol):
    """Alt sayfanın kendi <title>'ından kısa etiket üret."""
    try:
        s = io.open(yol, encoding="utf-8").read(4000)
    except Exception:
        return None
    m = re.search(r"<title>(.*?)</title>", s, re.S | re.I)
    if not m:
        return None
    t = html.unescape(m.group(1)).strip()
    t = re.sub(r"\s*\|\s*Luna Yapım\s*$", "", t)
    t = re.sub(r"\s*—\s*[\d.]+\s*₺.*$", "", t)     # fiyat ekini at
    t = re.sub(r"\s+Fiyatları$", "", t)
    return t.strip()


def cocuklar(kok, ana, onekler):
    d = os.path.join(kok, "hizmetler")
    out = []
    for f in sorted(os.listdir(d)):
        if not f.endswith(".html"):
            continue
        slug = f[:-5]
        if slug == ana or slug == "index":
            continue
        if not any(slug.startswith(o) for o in onekler):
            continue
        ad = _baslik(os.path.join(d, f))
        if ad:
            out.append((ad, slug))
    out.sort(key=lambda x: x[0].lower().replace("ç", "c").replace("ğ", "g")
             .replace("ı", "i").replace("ö", "o").replace("ş", "s").replace("ü", "u"))
    return out


def blok(kok, ana, onekler, baslik, aciklama):
    c = cocuklar(kok, ana, onekler)
    if len(c) < 2:
        return ""
    baglar = "".join('<a href="%s">%s</a>' % (slug, html.escape(ad)) for ad, slug in c)
    return ('%s\n<section>\n  <div class="wrap">\n'
            '    <div class="bas"><span class="no">◎</span><div><h2>%s</h2>\n'
            '      <p class="aciklama">%s</p></div></div>\n'
            '    <div class="iller">%s</div>\n  </div>\n</section>\n%s\n'
            % (BAS, html.escape(baslik), html.escape(aciklama), baglar, SON))



# --------------------------------------------------- kardeş sayfalar arası bağlantı
# sektor_sayfalari.py'de kardeş listesi [:5] ile kırpılıyordu; sözlükteki son iki
# sektör (gıda, inşaat malzemesi) hiçbir kardeşinden bağlantı almıyordu. Kaynak
# düzeltildi ama YAYINDAKİ sayfaları yeniden üretmek gereksiz risk — bu işlev
# sayfadaki "Diğer alanlar" satırını yerinde tamamlar, her koşuda aynı sonucu verir.
_DIGER = re.compile(r'(<h2>Diğer alanlar</h2>\s*<p>[^<]*karşılığı:\s*)(.*?)(\.\s*Genel anlatım)', re.S)

AILE_COCUK = {
    "urun-animasyon-": (" Ürün Animasyonu", " Ürün Animasyonu ve 3D Görsel", " Süreç Animasyonu",
                        " Animasyonu"),
    "insaat-3d-": (" 3D Görselleştirme", " 3D Render", " 3D Modelleme"),
}


def _kisa(ad, ekler):
    for x in sorted(ekler, key=len, reverse=True):
        if ad.endswith(x):
            return ad[: -len(x)].strip()
    return ad


def kardes_tamamla(kok):
    d = os.path.join(kok, "hizmetler")
    degisen = 0
    for onek, ekler in AILE_COCUK.items():
        aile = [f[:-5] for f in sorted(os.listdir(d))
                if f.endswith(".html") and f[:-5].startswith(onek) and f[:-5] != onek.rstrip("-")]
        etiket = {}
        for slug in aile:
            ad = _baslik(os.path.join(d, slug + ".html"))
            if ad:
                etiket[slug] = _kisa(ad, ekler)
        for slug in aile:
            y = os.path.join(d, slug + ".html")
            s = io.open(y, encoding="utf-8").read()
            if not _DIGER.search(s):
                continue
            liste = " · ".join('<a href="%s">%s</a>' % (k, html.escape(etiket[k]))
                               for k in aile if k != slug and k in etiket)
            yeni, n = _DIGER.subn(lambda m: m.group(1) + liste + m.group(3), s, count=1)
            if n and yeni != s:
                io.open(y, "w", encoding="utf-8").write(yeni)
                degisen += 1
    return degisen

def calistir(kok):
    n = 0
    bag = 0
    for ana, (onekler, baslik, aciklama) in AILE.items():
        y = os.path.join(kok, "hizmetler", ana + ".html")
        if not os.path.exists(y):
            continue
        s = io.open(y, encoding="utf-8").read()
        s = re.sub(re.escape(BAS) + r"[\s\S]*?" + re.escape(SON) + r"\n?", "", s)
        b = blok(kok, ana, onekler, baslik, aciklama)
        if not b:
            continue
        # il bloğunun ÜSTÜNE koy: önce "ne yaptığımız", sonra "nerede"
        if "<!-- il-baglari -->" in s:
            s = s.replace("<!-- il-baglari -->", b + "<!-- il-baglari -->", 1)
        elif '<section class="cta">' in s:
            s = s.replace('<section class="cta">', b + '<section class="cta">', 1)
        else:
            s = s.replace("</main>", b + "</main>", 1)
        io.open(y, "w", encoding="utf-8").write(s)
        n += 1
        bag += b.count('<a href="')
    kardes = kardes_tamamla(kok)
    return {"guncellenen_ana_sayfa": n, "eklenen_baglanti": bag, "kardes_tamamlanan": kardes}


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from pusula.ayarlar import SITE_KOK
    print(calistir(SITE_KOK))
