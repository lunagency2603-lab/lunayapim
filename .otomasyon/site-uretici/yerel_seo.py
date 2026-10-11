# -*- coding: utf-8 -*-
"""
YEREL SAYFA SEO TAMAMLAYICI — 11.10.2026

yerel_ozgun.py ile yeniden yazılan il sayfalarına (<!-- yerel-ozgun:v1 -->):
  1) Service şemasına sayfadaki fiyat bandını Offer/PriceSpecification olarak ekler
     (rakam sayfada zaten yazılı; şema yalnızca onu tekrar eder).
  2) "…" ile kesilmiş başlıkları (title, og:title) 60 karakter altına kısaltır.
  3) sitemap.xml'de bu sayfaların lastmod tarihini verilen güne çeker
     (içerik değişti; Google'ın yeniden taraması için).
Etkisiz tekrarlanabilir. Kullanım: python3 yerel_seo.py <kök> [YYYY-MM-DD] [slug ...]
"""
import datetime, glob, html, json, os, re, sys

ISARET = "<!-- yerel-ozgun:v1 -->"


def _rakam(x):
    return int(x.replace(".", ""))


def sema_fiyat(s):
    m = re.search(r'<!-- arama:fiyat -->.*?<strong>([\d.]+)\s*[–-]\s*([\d.]+)\s*₺</strong>', s, re.S)
    if not m:
        return s, False
    lo, hi = _rakam(m.group(1)), _rakam(m.group(2))
    degisti = [False]

    def duzelt(mm):
        d = json.loads(mm.group(1))
        nodes = d.get("@graph") if isinstance(d, dict) and "@graph" in d else [d]
        for o in nodes:
            if isinstance(o, dict) and o.get("@type") == "Service":
                yeni = {"@type": "Offer", "priceCurrency": "TRY",
                        "priceSpecification": {"@type": "PriceSpecification",
                                               "minPrice": lo, "maxPrice": hi, "priceCurrency": "TRY"},
                        "url": o.get("url", "") + "#fiyat"}
                if o.get("offers") != yeni:
                    o["offers"] = yeni
                    degisti[0] = True
        return '<script type="application/ld+json">%s</script>' % json.dumps(d, ensure_ascii=False)

    s2 = re.sub(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', duzelt, s, flags=re.S)
    return s2, degisti[0]


KISA = {"drone-cekimi": "Drone Çekimi — Havadan 4K Video",
        "emlak-video": "Emlak Video Çekimi",
        "klip-cekimi": "Klip Çekimi",
        "dugun-cekimi": "Düğün Çekimi",
        "isletme-tanitim": "İşletme Tanıtım Filmi"}


def baslik(s):
    m = re.search(r"<title>(.*?)</title>", s, re.S)
    t = html.unescape(m.group(1))
    if "…" not in t:
        return s, False
    il = re.search(r'"areaServed":\s*\{"@type":\s*"City",\s*"name":\s*"([^"]+)"', s)
    hz = re.search(r'href="https://lunayapim\.com/sehir/[a-z-]+?-(drone-cekimi|emlak-video|klip-cekimi|dugun-cekimi|isletme-tanitim)"', s)
    if not (il and hz):
        return s, False
    yeni = "%s %s | Luna Yapım" % (il.group(1), KISA[hz.group(1)])
    s = s.replace(m.group(0), "<title>%s</title>" % html.escape(yeni, quote=False), 1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda mm: mm.group(1) + html.escape(yeni) + mm.group(2), s, 1)
    return s, True


def sitemap_tarih(kok, adresler, gun):
    yol = os.path.join(kok, "sitemap.xml")
    s = open(yol, encoding="utf-8").read()
    n = 0
    for a in adresler:
        rx = r"(<loc>https://lunayapim\.com/%s</loc><lastmod>)[^<]*(</lastmod>)" % re.escape(a)
        s2 = re.sub(rx, r"\g<1>%s\g<2>" % gun, s)
        if s2 != s:
            n += 1
            s = s2
    open(yol, "w", encoding="utf-8").write(s)
    return n


def calistir(kok, gun=None, slugs=None):
    gun = gun or datetime.date.today().isoformat()
    dosyalar = [os.path.join(kok, "sehir", x + ".html") for x in slugs] if slugs else glob.glob(os.path.join(kok, "sehir", "*.html"))
    adres, fiyat, bas = [], 0, 0
    for f in dosyalar:
        s = open(f, encoding="utf-8").read()
        if ISARET not in s:
            continue
        s, a = sema_fiyat(s)
        s, b = baslik(s)
        if a or b:
            open(f, "w", encoding="utf-8").write(s)
        fiyat += a; bas += b
        adres.append("sehir/" + os.path.basename(f)[:-5])
    n = sitemap_tarih(kok, adres, gun)
    return {"sayfa": len(adres), "fiyat_semasi": fiyat, "baslik": bas, "sitemap_tarih": n}


if __name__ == "__main__":
    kok = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    gun = sys.argv[2] if len(sys.argv) > 2 else None
    print(calistir(kok, gun, sys.argv[3:] or None))
