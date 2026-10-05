# -*- coding: utf-8 -*-
"""
İL SAYFASI v2 — 81 il için tek sayfa (05.10.2026).

Neden: 16–17.09.2026'da il × hizmet sayfaları (509 sayfa) aynı kalıpla yeniden
yazıldı ve başlıklara fiyat kancası kondu. 20.09'da Google il sayfalarının
gösterimini %90 kesti (445 → 45 gösterim / 14 gün); sayfalar dizinde kaldı ama
gösterilmedi. Google'ın spam politikası bunu "kapı sayfası" (doorway) ve
"ölçekli içerik" olarak tanımlar: aynı işi her il × her hizmet için ayrı sayfada
anlatmak.

Yapı:
  * Her ilde TEK sayfa (sehir/<il>.html). İl × hizmet sayfaları kaldırılır,
    adresleri _redirects ile il sayfasına 301 yönlenir.
  * Sayfadaki metnin gövdesi ilin kendi verisidir (sehirler.py + iller_ek*.py):
    inşaat, emlak, sanayi, coğrafya, kültür, mekân, işletme ve düğün notları.
  * Çalışma şekli dürüstçe yazılır: kendi ekibin gittiği il ile çözüm ortağıyla
    çekilen il ayrılır; ilde yapılmış bir iş yokken "ilde yaptık" denmez.
  * Başlıkta fiyat kancası yok; fiyat aralıkları sayfada, fiyat sayfasıyla aynı.
  * Sayfa <!-- il-sayfasi:v2 --> işaretini taşır; sonislem'deki eski il
    düzenleyicileri (arama_hizala, sayfa_duzeni.il_sayfasi) bu sayfalara dokunmaz.

Kullanım:  python3 il_sayfasi.py <site kökü>
"""
import html, io, json, math, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sehirler import SEHIRLER, SEHIR_INDEKS

ISARET = "<!-- il-sayfasi:v2 -->"
SITE = "https://lunayapim.com"
TEL_WA = "https://wa.me/905542182603"

# il merkezlerinin yaklaşık koordinatları (kuş uçuşu mesafe için)
KOORD = {
 "adana":(37.00,35.32),"adiyaman":(37.76,38.28),"afyonkarahisar":(38.76,30.54),"agri":(39.72,43.05),
 "amasya":(40.65,35.83),"ankara":(39.93,32.86),"antalya":(36.90,30.70),"artvin":(41.18,41.82),
 "aydin":(37.85,27.84),"balikesir":(39.65,27.88),"bilecik":(40.14,29.98),"bingol":(38.88,40.50),
 "bitlis":(38.40,42.11),"bolu":(40.73,31.61),"burdur":(37.72,30.29),"bursa":(40.19,29.06),
 "canakkale":(40.15,26.41),"cankiri":(40.60,33.62),"corum":(40.55,34.95),"denizli":(37.78,29.09),
 "diyarbakir":(37.91,40.24),"edirne":(41.68,26.56),"elazig":(38.68,39.22),"erzincan":(39.75,39.49),
 "erzurum":(39.90,41.27),"eskisehir":(39.78,30.52),"gaziantep":(37.07,37.38),"giresun":(40.91,38.39),
 "gumushane":(40.46,39.48),"hakkari":(37.58,43.74),"hatay":(36.20,36.16),"isparta":(37.76,30.55),
 "mersin":(36.80,34.63),"istanbul":(41.01,28.98),"izmir":(38.42,27.14),"kars":(40.60,43.10),
 "kastamonu":(41.38,33.78),"kayseri":(38.73,35.49),"kirklareli":(41.73,27.22),"kirsehir":(39.15,34.16),
 "kocaeli":(40.77,29.92),"konya":(37.87,32.48),"kutahya":(39.42,29.98),"malatya":(38.35,38.31),
 "manisa":(38.61,27.43),"kahramanmaras":(37.58,36.94),"mardin":(37.31,40.74),"mugla":(37.22,28.36),
 "mus":(38.75,41.51),"nevsehir":(38.62,34.71),"nigde":(37.97,34.68),"ordu":(40.98,37.88),
 "rize":(41.02,40.52),"sakarya":(40.78,30.40),"samsun":(41.29,36.33),"siirt":(37.93,41.94),
 "sinop":(42.03,35.15),"sivas":(39.75,37.02),"tekirdag":(40.98,27.51),"tokat":(40.31,36.55),
 "trabzon":(41.00,39.72),"tunceli":(39.11,39.55),"sanliurfa":(37.16,38.79),"usak":(38.68,29.41),
 "van":(38.50,43.38),"yozgat":(39.82,34.81),"zonguldak":(41.45,31.79),"aksaray":(38.37,34.03),
 "bayburt":(40.26,40.23),"karaman":(37.18,33.22),"kirikkale":(39.85,33.51),"batman":(37.88,41.13),
 "sirnak":(37.52,42.46),"bartin":(41.64,32.34),"ardahan":(41.11,42.70),"igdir":(39.92,44.04),
 "yalova":(40.65,29.27),"karabuk":(41.20,32.62),"kilis":(36.72,37.12),"osmaniye":(37.07,36.25),
 "duzce":(40.84,31.16),
}

# (eski il×hizmet eki, başlık, hizmet sayfası, fiyat bandı | None)
HIZMET = [
 ("insaat-3d-modelleme", "İnşaat 3D modelleme ve mimari render", "insaat-3d-modelleme", "45.000 – 150.000 ₺"),
 ("emlak-video",         "Emlak videosu",                        "emlak-kurumsal",      "2.500 – 12.000 ₺"),
 ("urun-animasyon",      "3D ürün animasyonu",                   "urun-animasyon",      "40.000 – 95.000 ₺"),
 ("drone-cekimi",        "Drone ve FPV çekim",                   "drone-fpv",           "10.000 – 25.000 ₺"),
 ("klip-cekimi",         "Klip çekimi",                          "klip-cekimi",         "35.000 – 100.000 ₺"),
 ("dugun-cekimi",        "Düğün ve etkinlik çekimi",             "dugun-etkinlik",      None),
 ("isletme-tanitim",     "İşletme tanıtım filmi ve sosyal medya", "isletme-tanitim",    "25.000 – 55.000 ₺"),
]
HIZMET_EKLERI = tuple(h[0] for h in HIZMET)


def _e(x):
    return html.escape(x or "", quote=True)


def _liste(xs):
    xs = [x for x in xs if x]
    if len(xs) <= 1:
        return "".join(xs)
    return ", ".join(xs[:-1]) + " ve " + xs[-1]


def km(slug):
    if slug not in KOORD or slug == "bursa":
        return None
    (a1, o1), (a2, o2) = KOORD["bursa"], KOORD[slug]
    r = math.radians
    d = 2 * 6371 * math.asin(math.sqrt(math.sin(r(a2 - a1) / 2) ** 2 +
        math.cos(r(a1)) * math.cos(r(a2)) * math.sin(r(o2 - o1) / 2) ** 2))
    return int(round(d / 10.0) * 10) if d >= 100 else int(round(d / 5.0) * 5)


def _mekanlar(c, n=None):
    m = [x.strip() for x in (c.get("mekan") or "").split(",") if x.strip()]
    return m[:n] if n else m


# ---------------------------------------------------------------- metinler
def lede(c):
    if c["slug"] == "bursa":
        return "Ekibimiz Bursa'da: çekim, kurgu, renk ve 3D aynı ekipte."
    if c["ekip"] == "kendi":
        return "Çekime Bursa'daki kendi ekibimiz geliyor; kurgu, renk ve 3D de aynı ekipte."
    return "Çekim bölgedeki çözüm ortağımızla; kurgu, renk ve 3D Bursa'daki ekibimizde."


def calisma(c):
    ad = c["ad"]
    k = km(c["slug"])
    if c["slug"] == "bursa":
        p = ("Luna Yapım Bursa'da kurulu; kamera, drone, kurgu ve 3D aynı ekipte. "
             "Şehir içindeki çekimlerde ayrı yol planı gerekmiyor.")
    elif c["ekip"] == "kendi":
        p = ("%s, Bursa'ya kuş uçuşu yaklaşık %d km uzakta. Bu mesafede çekime Bursa'daki kendi "
             "ekibimizle geliyoruz." % (ad, k))
    else:
        p = ("%s, Bursa'ya kuş uçuşu yaklaşık %d km uzakta; bu yüzden sahadaki çekimi %s bölgesinde "
             "çalışan ortağımız yapıyor. 3D render ve animasyon işlerinde sahaya çıkmak gerekmiyor."
             % (ad, k, ad))
    return "<p>%s</p>" % _e(p)


def hizmet_metni(c, ek_):
    ad = c["ad"]
    if ek_ == "insaat-3d-modelleme":
        return [c.get("insaat")]
    if ek_ == "emlak-video":
        return [c.get("emlak")]
    if ek_ == "urun-animasyon":
        s = [c.get("sanayi")]
        if c.get("sektorler"):
            s.append("Ürün anlatımına en çok ihtiyaç duyan sektörler: %s." % _liste(c["sektorler"]))
        return s
    if ek_ == "drone-cekimi":
        return [c.get("cografya")]
    if ek_ == "klip-cekimi":
        return [c.get("kultur")]
    if ek_ == "dugun-cekimi":
        return [c.get("dugun_notu")]
    if ek_ == "isletme-tanitim":
        return [c.get("isletme_notu")]
    return []


def hizmetler_html(c):
    out = []
    for ek_, baslik, sayfa, bant in HIZMET:
        par = [p for p in hizmet_metni(c, ek_) if p]
        if not par:
            continue
        out.append('<h3 id="%s"><a href="../hizmetler/%s">%s</a></h3>' % (ek_, sayfa, _e(baslik)))
        for p in par:
            out.append("<p>%s</p>" % _e(p))
    out.append('<p class="il-fiyat">Hizmetlerin fiyat aralıkları <a href="../fiyatlar">fiyat sayfasında</a>; '
               'işinizi anlattığınızda net rakam yazıyoruz.</p>')
    return "\n    ".join(out)


def _ilk_buyuk(x):
    return x[:1].upper() + x[1:]


def sss(c):
    ad, ek, icin = c["ad"], c["ek"], c["icin"]
    out = []
    m = _mekanlar(c)
    if m:
        out.append(("%s%s çekim için hangi yerler öne çıkıyor?" % (ad, ek),
                    "%s. Rota, ışık saatine göre planlanıyor." % _liste(m)))
    ks = [SEHIR_INDEKS[k] for k in (c.get("komsu") or []) if k in SEHIR_INDEKS]
    if ks:
        kendi = [k["ad"] for k in ks if k.get("ekip") == "kendi"]
        ortak = [k["ad"] for k in ks if k.get("ekip") != "kendi"]
        parca = []
        if kendi:
            parca.append("%s tarafında kendi ekibimizle" % _liste(kendi))
        if ortak:
            parca.append("%s tarafında çözüm ortağımızla" % _liste(ortak))
        out.append(("%s%s yakın hangi illerde çalışıyorsunuz?" % (ad, icin),
                    "%s çalışıyoruz; aynı haftaya denk gelen işler tek planda birleştirilebiliyor." % _ilk_buyuk("; ".join(parca))))
    return out


def sss_html(c):
    d = []
    for i, (q, a) in enumerate(sss(c)):
        d.append('<details%s><summary>%s</summary>\n        <div class="cvp"><p>%s</p></div></details>'
                 % (" open" if i == 0 else "", _e(q), _e(a)))
    return "\n      ".join(d)


def komsu_html(c):
    ks = [SEHIR_INDEKS[k] for k in (c.get("komsu") or []) if k in SEHIR_INDEKS]
    a = "".join('<a href="%s">%s</a>' % (k["slug"], _e(k["ad"])) for k in ks)
    return a + '<a href="./" style="border-color:var(--kirmizi);color:var(--kirmizi)">Tüm iller →</a>'


def baslik(c):
    return "%s Video Çekimi, Drone ve 3D Render | Luna Yapım" % c["ad"]


def aciklama(c):
    ad, ek = c["ad"], c["ek"]
    if c["slug"] == "bursa":
        p = "Bursa'da video çekimi, drone ve 3D render: çekim, kurgu ve 3D aynı ekipte."
    elif c["ekip"] == "kendi":
        p = "%s%s video çekimi, drone ve 3D render: çekime Bursa'daki ekibimiz geliyor." % (ad, ek)
    else:
        p = "%s%s video çekimi, drone ve 3D render: çekim bölgedeki ortağımızla, kurgu ve 3D Bursa'da." % (ad, ek)
    ilce = c.get("ilceler") or []
    for n in (3, 2, 1):
        ek2 = " %s ve tüm ilçeler." % ", ".join(ilce[:n])
        if ilce and len(p + ek2) <= 158:
            return p + ek2
    return p


# ---------------------------------------------------------------- JSON-LD
def jsonld(c, url):
    ad = c["ad"]
    teklif = []
    for ek_, b, sayfa, bant in HIZMET:
        o = {"@type": "Offer", "itemOffered": {"@type": "Service", "name": b,
             "url": "%s/hizmetler/%s" % (SITE, sayfa)}}
        if bant:
            lo, hi = [int(x.replace(".", "")) for x in re.findall(r"[\d.]+", bant)[:2]]
            o["priceSpecification"] = {"@type": "PriceSpecification", "minPrice": lo,
                                       "maxPrice": hi, "priceCurrency": "TRY"}
        teklif.append(o)
    servis = {"@context": "https://schema.org", "@type": "Service",
              "name": "%s video prodüksiyon, drone ve 3D render" % ad,
              "serviceType": "Video prodüksiyon",
              "url": url,
              "provider": {"@id": SITE + "/#kurulus"},
              "areaServed": {"@type": "AdministrativeArea", "name": ad,
                             "containedInPlace": {"@type": "Country", "name": "Türkiye"}},
              "hasOfferCatalog": {"@type": "OfferCatalog", "name": "%s hizmetleri" % ad,
                                  "itemListElement": teklif}}
    sss_ = {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in sss(c)]}
    iz = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "İller", "item": SITE + "/sehir/"},
        {"@type": "ListItem", "position": 3, "name": ad, "item": url}]}
    return "\n".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False)
                     for x in (iz, servis, sss_))


# ---------------------------------------------------------------- sayfa
R_LD = re.compile(r'\s*<script type="application/ld\+json">.*?</script>', re.S)
R_VITRIN = re.compile(r'<section class="acik" data-video-bolum[^>]*>.*?</section>', re.S)


def govde(c, vitrin):
    ad, ek = c["ad"], c["ek"]
    if vitrin:
        vitrin = re.sub(r"<h2>[^<]*</h2>", "<h2>Ekibimizin işlerinden</h2>", vitrin, count=1)
        not_ = ("Bu işler farklı illerde ve yurt dışında çekildi. %s%s çekilen bir işimiz "
                "yayımlandığında bu listenin en üstünde görünür." % (ad, ek))
        vitrin = re.sub(r'<p class="aciklama">.*?</p>', '<p class="aciklama">%s</p>' % _e(not_), vitrin, count=1, flags=re.S)
    return """%(isaret)s
<div class="page-hero">
  <img class="karga-buyuk" src="../assets/karga.png" alt="">
  <div class="wrap">
    <div class="crumbs"><a href="../">Ana Sayfa</a> · <a href="./">İller</a> · %(ad)s</div>
    <h1>%(ad)s%(ek)s <i>video çekimi</i>, drone ve 3D render</h1>
    <p class="lede">%(lede)s</p>
    <div class="btnlar">
      <a class="btn btn-dolu" href="%(wa)s">%(ad)s için fiyat sorun</a>
      <a class="btn btn-cizgi" href="#hizmetler">Hizmetleri gör</a>
    </div>
  </div>
</div>

<section>
  <div class="wrap prose">
    <h2 id="calisma">%(ad)s%(ek)s nasıl çalışıyoruz</h2>
    %(calisma)s
    <h2 id="hizmetler">%(ad)s%(ek)s hizmetler</h2>
    %(hizmetler)s
    <h3 id="ilceler">Çalıştığımız ilçeler</h3>
    <p>%(ilceler)s</p>
  </div>
</section>

<section class="acik">
  <div class="wrap prose">
    <h2>%(ad)s — sık sorulan sorular</h2>
    <div class="sss">
      %(sss)s
    </div>
  </div>
  <div class="wrap"><p style="margin:18px 0 8px;font-weight:600">Yakın iller</p><div class="iller">%(komsu)s</div></div>
</section>

<section class="cta">
  <img class="karga-buyuk" src="../assets/karga.png" alt="">
  <div class="wrap">
    <p class="etk">İletişim</p>
    <h2>%(ad)s%(ek)ski işinizi <i>anlatın</i>.</h2>
    <p>Ne çekileceğini ve tarihi yazın, genelde aynı gün dönüyoruz.</p>
    <div class="btnlar">
      <a href="%(wa)s" class="btn btn-koyu">WhatsApp'tan Yaz</a>
      <a href="tel:+905542182603" class="btn btn-cizgi" style="border-color:rgba(255,255,255,.5);color:#fff">Ara · 0554 218 26 03</a>
    </div>
  </div>
</section>

""" % dict(isaret=ISARET, ad=_e(ad), ek=ek, lede=_e(lede(c)), wa=TEL_WA,
           calisma=calisma(c), hizmetler=hizmetler_html(c),
           ilceler=_e(("%s ve diğer ilçeler." % ", ".join(c.get("ilceler") or [])) if c.get("ilceler") else "İlin tamamı."),
           vitrin=vitrin or "", sss=sss_html(c), komsu=komsu_html(c))


def sayfa_yap(eski, c):
    url = "%s/sehir/%s" % (SITE, c["slug"])
    s = eski
    t, d = _e(baslik(c)), _e(aciklama(c))
    s = re.sub(r"<title>.*?</title>", "<title>%s</title>" % t, s, count=1, flags=re.S)
    s = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % d, s, count=1)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="%s">' % t, s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="%s">' % d, s, count=1)
    a = c["ad"].replace("I", "ı").replace("İ", "i").lower()
    kw = '<meta name="keywords" content="%s video çekimi, %s drone çekimi, %s 3d render, %s tanıtım filmi">' % (a, a, a, a)
    if re.search(r'<meta name="keywords" content="[^"]*">', s):
        s = re.sub(r'<meta name="keywords" content="[^"]*">', kw, s, count=1)
    else:
        s = s.replace('<link rel="canonical"', kw + '\n<link rel="canonical"', 1)
    s = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="%s">' % url, s, count=1)
    # head JSON-LD: hepsini çıkar, yenisini koy (VideoObject ve firma düğümünü sonislem/varlik yeniden ekler)
    bas_h, son_h = s.find("<head>"), s.find("</head>")
    head = R_LD.sub("", s[bas_h:son_h])
    head = head.rstrip() + "\n" + jsonld(c, url) + "\n"
    s = s[:bas_h] + head + s[son_h:]
    # gövde: page-hero (ya da işaret) → footer
    vm = R_VITRIN.search(s)
    vitrin = vm.group(0) if vm else ""
    i = s.find(ISARET)
    if i < 0:
        i = s.find('<div class="page-hero"')
    j = s.find("<footer")
    if i < 0 or j < 0:
        raise ValueError("kabuk bulunamadı: " + c["slug"])
    return s[:i] + govde(c, vitrin) + s[j:]


def calistir(kok):
    dz = os.path.join(kok, "sehir")
    n = 0
    for c in SEHIRLER:
        y = os.path.join(dz, c["slug"] + ".html")
        if not os.path.exists(y):
            print("yok:", c["slug"]); continue
        eski = io.open(y, encoding="utf-8").read()
        yeni = sayfa_yap(eski, c)
        if yeni != eski:
            io.open(y, "w", encoding="utf-8").write(yeni); n += 1
    return {"il_sayfasi": n}


if __name__ == "__main__":
    print(calistir(sys.argv[1] if len(sys.argv) > 1 else "."))
