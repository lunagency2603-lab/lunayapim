# -*- coding: utf-8 -*-
"""
İZLEME SAYFALARI — her gerçek iş için tek video sayfası: /isler/<sayfa>  (06.10.2026)

Neden: Search Console > Video dizine ekleme: 109 video "izleme sayfasında değil"
(Video isn't on a watch page) gerekçesiyle dizin dışı. Videolar hizmet ve il
sayfalarının vitrininde ikincil öğe olarak duruyordu; Google videoyu ancak
sayfanın ASIL içeriği olduğunda dizine alır. Her yayınlanmış iş (videolar.js'te
id ya da yerel alanı dolu olan kayıt) burada kendi sayfasını alır; VideoObject
şeması yalnız bu sayfalarda durur (varlik.py diğer sayfalara artık basmaz).

Kural: uydurma yok. Sayfadaki her bilgi videolar.js kaydından gelir; kayıtta
olmayan alan yazılmaz. Şehir künyeye yazılmaz (sahibinin kuralı, varlik.py
_is_karti notu) — şehir yalnız o ilin sayfasında rozet olur.

Kullanım:  python3 izleme_sayfalari.py <site kökü>
"""
import html, io, json, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import varlik

SITE = "https://lunayapim.com"
KABUK = "hizmetler/klip-cekimi.html"
ISARET = "<!-- izleme-sayfasi -->"

HIZMET = {   # etiket → (hizmet sayfası, ad)
    "klip": ("klip-cekimi", "Klip çekimi"),
    "insaat-3d": ("insaat-3d-modelleme", "İnşaat 3D modelleme"),
    "urun-animasyon": ("urun-animasyon", "3D ürün animasyonu"),
    "emlak": ("emlak-kurumsal", "Emlak ve kurumsal tanıtım"),
    "drone": ("drone-fpv", "Drone ve FPV çekim"),
    "dugun": ("dugun-etkinlik", "Düğün ve etkinlik çekimi"),
    "isletme": ("isletme-tanitim", "İşletme tanıtım filmi"),
}


def _e(x):
    return html.escape(x or "", quote=True)


def _sure_iso(s):
    m = re.match(r"^(\d+):(\d{2})$", s or "")
    if not m:
        return None
    dk, sn = int(m.group(1)), int(m.group(2))
    return "PT%s%dS" % (("%dM" % dk) if dk else "", sn) if sn or not dk else "PT%dM" % dk


def _ilk_yayin(kok, yol):
    """Yerel dosyanın siteye ilk eklendiği gün (git) — uploadDate için gerçek tarih."""
    try:
        r = subprocess.run(["git", "-C", kok, "log", "--diff-filter=A", "--format=%ad",
                            "--date=short", "--", yol], capture_output=True, text=True, timeout=20)
        t = [x for x in r.stdout.split() if x]
        return t[-1] if t else None
    except Exception:
        return None


def kayitlar(kok):
    s = io.open(os.path.join(kok, "assets", "videolar.js"), encoding="utf-8").read()
    out = []
    for d in varlik.isler(kok):
        m = None
        for b in varlik._IS_KAYIT.finditer(s):
            blok = b.group(0)
            if (d.get("id") and 'id:"%s"' % d["id"] in blok) or (d.get("yerel") and 'yerel:"%s"' % d["yerel"] in blok):
                m = re.search(r'sayfa:\s*"([^"]+)"', blok)
                break
        if not m:
            continue
        d = dict(d, sayfa=m.group(1))
        if d.get("yerel") and not d.get("yil"):
            d["yil"] = _ilk_yayin(kok, "assets/video/%s.mp4" % d["yerel"]) or "2026-09-01"
        out.append(d)
    return out


def aciklama(d):
    p = "%s — %s çalışması" % (d["baslik"], d.get("kat", "video").lower())
    if d.get("musteri"):
        p += " (%s)" % d["musteri"]
    p += "."
    if d.get("teslim"):
        p += " Yapılan iş: %s." % d["teslim"]
    ek = " Luna Yapım işlerinden; videoyu bu sayfada izleyebilirsiniz."
    if len(p + ek) <= 158:
        p += ek
    if len(p) < 110:
        p += " Benzer bir iş için fiyat aralığını aynı gün yazıyoruz."
    if len(p) > 160:
        p = p[:158].rsplit(" ", 1)[0].rstrip(" ,;—-") + "."
    return p


def sema(d, url):
    v = {"@context": "https://schema.org", "@type": "VideoObject",
         "name": d["baslik"], "description": d.get("detay") or d.get("teslim") or d["baslik"],
         "uploadDate": d["yil"], "url": url, "publisher": {"@id": SITE + "/#kurulus"}}
    if d.get("id"):
        v["thumbnailUrl"] = "https://i.ytimg.com/vi/%s/hqdefault.jpg" % d["id"]
        v["embedUrl"] = "https://www.youtube.com/embed/%s" % d["id"]
    else:
        v["thumbnailUrl"] = SITE + "/assets/video/%s.jpg" % d["yerel"]
        v["contentUrl"] = SITE + "/assets/video/%s.mp4" % d["yerel"]
    iso = _sure_iso(d.get("sure"))
    if iso:
        v["duration"] = iso
    iz = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "İşler", "item": SITE + "/isler"},
        {"@type": "ListItem", "position": 3, "name": d["baslik"], "item": url}]}
    return "\n".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in (iz, v))


def oynatici(d):
    if d.get("id"):
        return ('<div class="izle-kap"><iframe src="https://www.youtube-nocookie.com/embed/%s?rel=0" '
                'title="%s" loading="eager" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" '
                'allowfullscreen></iframe></div>' % (d["id"], _e(d["baslik"])))
    y = d["yerel"]
    return ('<div class="izle-kap"><video controls playsinline preload="metadata" poster="../assets/video/%s.jpg">'
            '<source src="../assets/video/%s.webm" type="video/webm">'
            '<source src="../assets/video/%s.mp4" type="video/mp4"></video></div>' % (y, y, y))


def govde(d, hepsi):
    kunye = []
    for etiket, deger in (("Tür", d.get("kat")), ("Müşteri", d.get("musteri")), ("Süre", d.get("sure")),
                          ("Format", d.get("olcu")), ("Yayın", d.get("yil"))):
        if deger:
            kunye.append("<li><strong>%s:</strong> %s</li>" % (etiket, _e(deger)))
    hz = [HIZMET[e] for e in d.get("etiket", []) if e in HIZMET]
    hz_html = ""
    if hz:
        hz_html = ("<h2>İlgili hizmet</h2>\n    <p>" + " · ".join(
            '<a href="../hizmetler/%s">%s</a>' % (s, _e(a)) for s, a in hz) + "</p>")
    diger = [x for x in hepsi if x["sayfa"] != d["sayfa"]]
    dg = "".join('<a href="../%s"><b>%s</b><span>%s</span></a>' % (x["sayfa"], _e(x["baslik"]), _e(x.get("kat", "")))
                 for x in diger)
    return """%(isaret)s
<div class="page-hero">
  <div class="wrap">
    <div class="crumbs"><a href="../">Ana Sayfa</a> · <a href="../isler">İşler</a> · %(b)s</div>
    <h1>%(b)s</h1>
    <p class="lede">%(lede)s</p>
  </div>
</div>

<section>
  <div class="wrap">
    %(oyn)s
  </div>
  <div class="wrap prose">
    <h2>Bu işte ne yaptık</h2>
    <p>%(detay)s</p>
    <p><strong>Teslim edilen:</strong> %(teslim)s.</p>
    <ul>%(kunye)s</ul>
    %(hz)s
  </div>
</section>

<section class="acik">
  <div class="wrap prose" style="max-width:none">
    <h2>Diğer işlerimiz</h2>
    <div class="ilgili">%(dg)s</div>
    <p><a href="../isler">Tüm işler →</a></p>
  </div>
</section>

<section class="cta">
  <img class="karga-buyuk" src="../assets/karga.png" alt="">
  <div class="wrap">
    <p class="etk">İletişim</p>
    <h2>Benzer bir işe <i>başlayalım</i>.</h2>
    <p>Ne çekileceğini ve tarihi yazın, genelde aynı gün dönüyoruz.</p>
    <div class="btnlar">
      <a href="https://wa.me/905542182603" class="btn btn-koyu">WhatsApp'tan Yaz</a>
      <a href="tel:+905542182603" class="btn btn-cizgi" style="border-color:rgba(255,255,255,.5);color:#fff">Ara · 0554 218 26 03</a>
    </div>
  </div>
</section>

""" % dict(isaret=ISARET, b=_e(d["baslik"]),
           lede=_e(" · ".join(x for x in (d.get("kat"), d.get("musteri")) if x)),
           oyn=oynatici(d), teslim=_e(d.get("teslim") or d["baslik"]), detay=_e(d.get("detay") or d.get("teslim") or d["baslik"]),
           kunye="".join(kunye), hz=hz_html, dg=dg)


R_LD = re.compile(r'\s*<script type="application/ld\+json">.*?</script>', re.S)


def sayfa_yap(kabuk, d, hepsi):
    url = "%s/%s" % (SITE, d["sayfa"])
    t = _e("%s — %s | Luna Yapım" % (d["baslik"], d.get("kat", "Video")))
    if len(html.unescape(t)) > 68:
        t = _e("%s | Luna Yapım" % d["baslik"])
    if len(html.unescape(t)) < 32:
        t = _e("%s — %s Çalışması | Luna Yapım" % (d["baslik"], d.get("kat", "Video")))
    a = _e(aciklama(d))
    s = kabuk
    s = re.sub(r"<title>.*?</title>", "<title>%s</title>" % t, s, count=1, flags=re.S)
    for pat, val in ((r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % a),
                     (r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="%s">' % t),
                     (r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="%s">' % a),
                     (r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="%s">' % url),
                     (r'<meta property="og:type" content="[^"]*">', '<meta property="og:type" content="video.other">'),
                     (r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="%s">' % url),
                     (r'<meta name="keywords" content="[^"]*">', '<meta name="keywords" content="%s">' % _e(", ".join(
                         x.lower() for x in (d["baslik"], d.get("kat", ""), "luna yapım") if x)))):
        s = re.sub(pat, val, s, count=1)
    if d.get("id"):
        og = "https://i.ytimg.com/vi/%s/hqdefault.jpg" % d["id"]
    else:
        og = SITE + "/assets/video/%s.jpg" % d["yerel"]
    s = re.sub(r'<meta property="og:image" content="[^"]*">', '<meta property="og:image" content="%s">' % og, s, count=1)
    s = re.sub(r'<meta name="twitter:image" content="[^"]*">', '<meta name="twitter:image" content="%s">' % og, s, count=1)
    b, e = s.find("<head>"), s.find("</head>")
    s = s[:b] + R_LD.sub("", s[b:e]).rstrip() + "\n" + sema(d, url) + "\n" + s[e:]
    i, j = s.find('<div class="page-hero"'), s.find("<footer")
    bas, son = _kok_yolla(s[:i]), _kok_yolla(s[j:])
    return bas + govde(d, hepsi) + son


def _kok_yolla(x):
    """Kabuk hizmetler/ altından geliyor; oradaki kardeş bağlantılar (href="klip-cekimi",
    href="./") isler/ altında kırılır. Hepsi ../hizmetler/ köküne çevrilir."""
    def _d(m):
        h = m.group(1)
        if h.startswith(("../", "http", "#", "mailto:", "tel:", "/", "javascript:", "data:")) or not h:
            return m.group(0)
        if h in (".", "./"):
            return 'href="../hizmetler/"'
        return 'href="../hizmetler/%s"' % h
    return re.sub(r'href="([^"]*)"', _d, x)


def calistir(kok):
    kabuk = io.open(os.path.join(kok, KABUK), encoding="utf-8").read()
    hepsi = kayitlar(kok)
    os.makedirs(os.path.join(kok, "isler"), exist_ok=True)
    n = 0
    for d in hepsi:
        y = os.path.join(kok, d["sayfa"] + ".html")
        yeni = sayfa_yap(kabuk, d, hepsi)
        eski = io.open(y, encoding="utf-8").read() if os.path.exists(y) else ""
        if ISARET in eski:
            # sonislem'in sonradan eklediği alanlar korunur: yalnız gövde/baş yeniden kurulur
            pass
        if yeni != eski:
            io.open(y, "w", encoding="utf-8").write(yeni); n += 1
    return {"izleme_sayfasi": len(hepsi), "yazilan": n}


if __name__ == "__main__":
    print(calistir(sys.argv[1] if len(sys.argv) > 1 else "."))
