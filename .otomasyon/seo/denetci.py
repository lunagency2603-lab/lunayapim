# -*- coding: utf-8 -*-
"""
Luna SEO Denetçisi — sitedeki her sayfayı teknik ve içerik kriterlerine göre denetler.
  python3 denetci.py            → özet + hata listesi
  python3 denetci.py --rapor    → HTML rapor da üretir
Hedef: 0 hata, 0 uyarı.
"""
import os, re, sys, json, glob, html, collections
import xml.etree.ElementTree as ET
from urllib.parse import unquote

SITE = os.path.expanduser("~/Documents/GitHub/lunayapim")
if not os.path.isdir(SITE):
    SITE = os.path.expanduser("~/mnt/Documents/GitHub/lunayapim")
ALAN = "https://lunayapim.com"

# --- eşikler ---
E = {
 "baslik_min": 30, "baslik_max": 70,
 "aciklama_min": 110, "aciklama_max": 165,
 "kelime_min": 400,
 "ic_bag_min": 5,
 "h2_min": 2,
}

ETIKET = re.compile(r"<[^>]+>")
BETIK  = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.S | re.I)


def _coz(hedef):
    """Cloudflare Pages uzantıyı kesiyor: /x -> x.html, /x/ -> x/index.html."""
    for aday in (hedef, hedef + ".html",
                 os.path.join(hedef, "index.html"),
                 os.path.join(hedef.rstrip("/"), "index.html")):
        if aday and os.path.exists(aday) and os.path.isfile(aday):
            return aday
    return None

def metin(s):
    s = BETIK.sub(" ", s)
    s = ETIKET.sub(" ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()

def kelime_sayisi(s):
    return len([w for w in metin(s).split() if len(w) > 1])

def sayfalar():
    eski = os.getcwd(); os.chdir(SITE)
    l = [f for f in sorted(glob.glob("**/*.html", recursive=True)) if f not in ("admin.html", "404.html") and not f.startswith("onizleme/")]
    os.chdir(eski)
    return l

def denetle():
    eski = os.getcwd(); os.chdir(SITE)
    bulgu = collections.defaultdict(list)   # dosya -> [(seviye, kod, mesaj)]
    basliklar, aciklamalar, kanonikler = {}, {}, {}
    sayfa_listesi = sorted(glob.glob("**/*.html", recursive=True))
    # dizine kapalı yönetim sayfaları (noindex) denetim dışı — herkese açık değil
    sayfa_listesi = [f for f in sayfa_listesi if f not in ("admin.html", "404.html") and not f.startswith("onizleme/")]  # onizleme/: musteriye ozel gizli teklif sayfalari
    icerik = {f: open(f, encoding="utf-8").read() for f in sayfa_listesi}

    # gelen bağlantı sayımı
    gelen = collections.Counter()

    for f, s in icerik.items():
        d = os.path.dirname(f)
        def hata(kod, msg): bulgu[f].append(("HATA", kod, msg))
        def uyari(kod, msg): bulgu[f].append(("UYARI", kod, msg))

        # 1 lang
        if not re.search(r'<html[^>]+lang="tr"', s): hata("lang", "html lang=\"tr\" yok")
        # 2 charset
        if not re.search(r'<meta charset="[Uu][Tt][Ff]-8">', s): hata("charset", "meta charset yok")
        # 3 viewport
        if 'name="viewport"' not in s: hata("viewport", "viewport meta yok")
        # 4 title
        m = re.search(r"<title>(.*?)</title>", s, re.S)
        if not m: hata("title", "title yok")
        else:
            t = re.sub(r"\s+", " ", html.unescape(m.group(1))).strip()
            basliklar.setdefault(t, []).append(f)
            if len(t) < E["baslik_min"]: uyari("title_kisa", "title %d karakter (<%d)" % (len(t), E["baslik_min"]))
            if len(t) > E["baslik_max"]: uyari("title_uzun", "title %d karakter (>%d)" % (len(t), E["baslik_max"]))
        # 5 description
        m = re.search(r'<meta name="description" content="(.*?)">', s, re.S)
        if not m: hata("desc", "meta description yok")
        else:
            dsc = html.unescape(m.group(1)).strip()
            aciklamalar.setdefault(dsc, []).append(f)
            if len(dsc) < E["aciklama_min"]: uyari("desc_kisa", "description %d karakter (<%d)" % (len(dsc), E["aciklama_min"]))
            if len(dsc) > E["aciklama_max"]: uyari("desc_uzun", "description %d karakter (>%d)" % (len(dsc), E["aciklama_max"]))
        # 6 canonical
        m = re.search(r'rel="canonical" href="([^"]+)"', s)
        if not m: hata("canonical", "canonical yok")
        else:
            k = m.group(1)
            kanonikler.setdefault(k, []).append(f)
            # Cloudflare Pages .html uzantısını 301 ile kesiyor; kanonik uzantısız olmalı
            if f == "index.html":
                beklenen = ALAN + "/"
            elif os.path.basename(f) == "index.html":
                beklenen = ALAN + "/" + os.path.dirname(f) + "/"
            else:
                beklenen = ALAN + "/" + f[:-5]
            if k.rstrip("/") != beklenen.rstrip("/"):
                uyari("canonical_yanlis", "canonical %s ≠ beklenen %s" % (k, beklenen))
        # 7 H1
        h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", s, re.S)
        if len(h1) == 0: hata("h1_yok", "H1 yok")
        elif len(h1) > 1: hata("h1_coklu", "%d adet H1" % len(h1))
        # 8 H2
        h2 = re.findall(r"<h2[^>]*>(.*?)</h2>", s, re.S)
        if len(h2) < E["h2_min"]: uyari("h2_az", "%d adet H2 (<%d)" % (len(h2), E["h2_min"]))
        # 9 kelime sayısı
        ks = kelime_sayisi(s)
        if ks < E["kelime_min"]: uyari("ince_icerik", "%d kelime (<%d)" % (ks, E["kelime_min"]))
        # 10 og
        for og in ("og:title", "og:description", "og:url", "og:image"):
            if 'property="%s"' % og not in s: uyari("og", "%s yok" % og)
        # 11 twitter
        if 'name="twitter:card"' not in s: uyari("twitter", "twitter:card yok")
        # 12 img alt
        for img in re.findall(r"<img[^>]*>", s):
            if "alt=" not in img: hata("img_alt", "alt'sız img: %s" % img[:70])
        # 13 JSON-LD
        bloklar = re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
        if not bloklar: uyari("jsonld_yok", "JSON-LD yok")
        for b in bloklar:
            try: json.loads(b)
            except Exception as ex: hata("jsonld_bozuk", "JSON-LD geçersiz: %s" % str(ex)[:60])
        # 14 iç bağlantılar + kırık kontrolü
        ic = 0
        for u in re.findall(r'href="([^"]+)"', s):
            if u.startswith(("http", "mailto:", "tel:", "#", "data:", "//")): continue
            y = unquote(u.split("#")[0].split("?")[0])
            if not y: continue
            ic += 1
            hedef = os.path.normpath(os.path.join(d, y))
            coz = _coz(hedef)
            if not coz:
                hata("kirik_bag", "kırık bağlantı: %s" % u)
            else:
                gelen[coz] += 1
        if ic < E["ic_bag_min"]: uyari("ic_bag_az", "%d iç bağlantı (<%d)" % (ic, E["ic_bag_min"]))
        # 15 keywords
        if 'name="keywords"' not in s: uyari("keywords", "meta keywords yok")
        # 16 favicon
        if 'rel="icon"' not in s: uyari("favicon", "favicon yok")
        # 17 h1 ile title uyumu
        if h1 and m:
            h1m = metin(h1[0]).lower()
            tm = metin(basliklar and list(basliklar.keys())[0] or "")
        # 18 boş başlık etiketi
        for etk in re.findall(r"<h[1-3][^>]*>\s*</h[1-3]>", s):
            hata("bos_baslik", "boş başlık etiketi")

    # --- site geneli ---
    genel = []
    for t, fs in basliklar.items():
        if len(fs) > 1: genel.append(("HATA", "cift_title", "aynı title %d sayfada: %r → %s" % (len(fs), t[:48], fs[:3])))
    for dsc, fs in aciklamalar.items():
        if len(fs) > 1: genel.append(("HATA", "cift_desc", "aynı description %d sayfada: %s" % (len(fs), fs[:3])))
    for k, fs in kanonikler.items():
        if len(fs) > 1: genel.append(("HATA", "cift_canonical", "aynı canonical %d sayfada: %s" % (len(fs), fs[:3])))

    # sitemap kapsamı
    try:
        kok = ET.parse("sitemap.xml").getroot()
        ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        sm = set()
        for u in kok.findall(ns + "url"):
            loc = u.find(ns + "loc").text.replace(ALAN + "/", "")
            if loc == "":
                sm.add("index.html")
            elif loc.endswith("/"):
                sm.add(loc + "index.html")
            else:
                sm.add(loc + ".html" if os.path.exists(loc + ".html") else loc)
        for f in sayfa_listesi:
            if f in sm: continue
            # noindex işaretli sayfa sitemap'te olmamalı — eksik sayılmaz (17.09.2026)
            try:
                govde = open(f, encoding="utf-8").read()
            except Exception:
                govde = ""
            if re.search(r'<meta[^>]+name="robots"[^>]+noindex', govde, re.I):
                continue
            genel.append(("HATA", "sitemap_eksik", "sitemap'te yok: %s" % f))
        for u in sm:
            if not _coz(u): genel.append(("HATA", "sitemap_fazla", "sitemap'te olmayan dosya: %s" % u))
    except Exception as ex:
        genel.append(("HATA", "sitemap", "sitemap okunamadı: %s" % ex))

    # yetim sayfa (hiç iç bağlantı almayan)
    for f in sayfa_listesi:
        if f == "index.html": continue
        if gelen.get(f, 0) == 0:
            genel.append(("UYARI", "yetim", "hiçbir sayfadan bağlantı almıyor: %s" % f))

    os.chdir(eski)
    return sayfa_listesi, bulgu, genel


def ozet(sayfa_listesi, bulgu, genel):
    hata = sum(1 for f in bulgu for s, _, _ in bulgu[f] if s == "HATA") + sum(1 for s, _, _ in genel if s == "HATA")
    uyari = sum(1 for f in bulgu for s, _, _ in bulgu[f] if s == "UYARI") + sum(1 for s, _, _ in genel if s == "UYARI")
    kod = collections.Counter()
    for f in bulgu:
        for s, k, _ in bulgu[f]: kod[(s, k)] += 1
    for s, k, _ in genel: kod[(s, k)] += 1
    return hata, uyari, kod


if __name__ == "__main__":
    sl, bulgu, genel = denetle()
    hata, uyari, kod = ozet(sl, bulgu, genel)
    puan = 100.0 if (hata == 0 and uyari == 0) else max(0, 100 - (hata * 100.0 / max(1, len(sl))) - (uyari * 25.0 / max(1, len(sl))))
    print("Sayfa: %d | HATA: %d | UYARI: %d | SEO uygunluk: %%%.1f" % (len(sl), hata, uyari, puan))
    # sonucu makine okunur biçimde de bırak — ana sayfadaki canlı künye bunu okuyor
    try:
        import json as _j, os as _o, datetime as _d
        _kok = _o.path.dirname(_o.path.dirname(_o.path.abspath(__file__)))
        _o.makedirs(_o.path.join(_kok, "veri"), exist_ok=True)
        with open(_o.path.join(_kok, "veri", "denetim.json"), "w", encoding="utf-8") as _f:
            _j.dump({"sayfa": len(sl), "hata": hata, "uyari": uyari,
                     "puan": round(puan, 1), "tarih": _d.date.today().isoformat()},
                    _f, ensure_ascii=False)
    except Exception:
        pass
    print()
    for (s, k), n in sorted(kod.items(), key=lambda x: (-x[1])):
        print("  %-6s %-18s %d" % (s, k, n))
    if "--detay" in sys.argv:
        print()
        for f in sorted(bulgu):
            for s, k, m in bulgu[f][:6]:
                print("  %-6s %-46s %s" % (s, f, m))
        for s, k, m in genel[:40]:
            print("  %-6s %-46s %s" % (s, "(site geneli)", m))
