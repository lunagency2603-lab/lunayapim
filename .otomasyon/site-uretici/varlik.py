# -*- coding: utf-8 -*-
"""
VARLIK KATMANI — firmayı arama motoruna ve yapay zekâya TANITAN alanlar.

22.09.2026'da bulunan sorun:
assets/sosyal.js içinde Instagram hesabı (lunayapim.mov) zaten tanımlıydı ve
dosyanın başındaki not "sameAs alanına da yazılır" diyordu. Ama bu iş
TARAYICIDA, JavaScript ile yapılıyordu. Sonuç: sayfanın ham HTML'inde ne
instagram.com geçiyordu ne de sameAs.

Kimin için fark eder:
  · Googlebot JavaScript çalıştırır — o görüyordu.
  · Bingbot, ChatGPT'nin tarayıcısı, Perplexity ve diğer yapay zekâ
    tarayıcıları çalıştırmaz — onlar için hesap ile firma arasında hiçbir
    bağ yoktu. "Luna Yapım kimdir" sorusunda hesabı eşleştiremiyorlardı.

Bu modül aynı bilgiyi ÜRETİM SIRASINDA, düz HTML'e yazar:
  1. Alt bilgideki [data-sosyal] yer tutucusunu gerçek bağlantılarla doldurur
  2. JSON-LD'deki Organization / LocalBusiness düğümüne sameAs ekler
  3. Aynı düğüme kalıcı bir @id verir — bütün sayfalardaki firma kaydı tek
     varlığa bağlanır (dağınık düğüm, dağınık varlık demektir)
  4. Sayfada "… ₺'den" biçiminde açıkça yazan taban fiyat varsa Service
     düğümüne offers olarak işler — uydurma yok, sayfadaki rakam

JavaScript tarafı olduğu gibi kalır: JS çalışırsa aynı bağlantıları görür,
iki kez basılmaz (yer tutucu doluysa modül dokunmaz).
"""
import json
import os
import re

KURULUS_ID = "https://lunayapim.com/#kurulus"
EPOSTA = "lunagency2603@gmail.com"
ISLETME = ("LocalBusiness", "Organization", "ProfessionalService", "Corporation")

_HESAP = re.compile(
    r'\{\s*ag:\s*"([^"]*)"\s*,\s*ad:\s*"([^"]*)"\s*,\s*kullanici:\s*"([^"]*)"\s*,\s*adres:\s*"([^"]*)"')
_SOSYAL_YER = re.compile(r'(<span[^>]*data-sosyal[^>]*>)(\s*)(</span>)', re.I)
_LD = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)
_TABAN_FIYAT = re.compile(r"([\d][\d.]{2,})\s*₺['’]?d[ae]n", re.I)


def hesaplar(kok):
    """assets/sosyal.js tek kaynak: kullanıcı adı doluysa hesap vardır."""
    yol = os.path.join(kok, "assets", "sosyal.js")
    try:
        s = open(yol, encoding="utf-8").read()
    except Exception:
        return []
    out = []
    for ag, ad, kullanici, adres in _HESAP.findall(s):
        kullanici = kullanici.strip()
        if not kullanici:
            continue
        out.append({"ag": ag, "ad": ad, "url": adres.replace("%s", kullanici)})
    return out


def _sosyal_serit(hsp):
    return "".join('<a href="%s" rel="me noopener" target="_blank">%s</a>' % (h["url"], h["ad"])
                   for h in hsp)


def _dugumler(d):
    """JSON-LD içindeki bütün sözlükleri dolaş."""
    if isinstance(d, dict):
        yield d
        for v in d.values():
            for x in _dugumler(v):
                yield x
    elif isinstance(d, list):
        for v in d:
            for x in _dugumler(v):
                yield x


def _tur(d):
    t = d.get("@type")
    return t if isinstance(t, str) else (t[0] if isinstance(t, list) and t else "")


def _sema_zenginlestir(blok, hsp, taban, url):
    try:
        d = json.loads(blok)
    except Exception:
        return blok, False
    degisti = False
    adresler = [h["url"] for h in hsp]
    for n in _dugumler(d):
        t = _tur(n)
        if t in ISLETME:
            if adresler and not n.get("sameAs"):
                n["sameAs"] = adresler
                degisti = True
            if not n.get("@id"):
                n["@id"] = KURULUS_ID
                degisti = True
            if not n.get("email"):
                n["email"] = EPOSTA
                degisti = True
        elif t == "Service" and taban and not n.get("offers"):
            n["offers"] = {
                "@type": "Offer",
                "priceCurrency": "TRY",
                "availability": "https://schema.org/InStock",
                "priceSpecification": {
                    "@type": "PriceSpecification",
                    "priceCurrency": "TRY",
                    "minPrice": taban,
                },
            }
            if url:
                n["offers"]["url"] = url
            degisti = True
    if not degisti:
        return blok, False
    return json.dumps(d, ensure_ascii=False), True


# --------------------------------------------------------------- sayfadaki SSS
_SSS_BLOK = re.compile(r'<div class="sss">(.*?)</div>\s*(?=<h2|<section|</div>)', re.S | re.I)
_SSS_CIFT = re.compile(
    r"<details[^>]*>\s*<summary[^>]*>(.*?)</summary>\s*<div class=\"cvp\">(.*?)</div>\s*</details>",
    re.S | re.I)


def _duz(x):
    x = re.sub(r"<[^>]+>", " ", x)
    x = x.replace("&nbsp;", " ").replace("&amp;", "&").replace("&#x27;", "'")
    x = x.replace("&quot;", '"').replace("&lt;", "<").replace("&gt;", ">")
    return re.sub(r"\s+", " ", x).strip()


def sss_sema(s):
    """Sayfada zaten duran soru-cevapları FAQPage şemasına çevirir.

    22.09.2026: hizmet sayfalarının neredeyse hepsinde "Sık sorulan sorular"
    bolumu vardi ama uc sayfada sema yoktu — yani soru-cevap okura gorunuyor,
    arama motoruna gorunmuyordu. Icerik uretilmiyor; var olan metin
    isaretleniyor. Soru uydurulmuyor.
    """
    if "FAQPage" in s:
        return s
    cift = []
    for blok in _SSS_BLOK.findall(s):
        for soru, cevap in _SSS_CIFT.findall(blok):
            q, a = _duz(soru), _duz(cevap)
            if q and a and len(a) > 20:
                cift.append((q, a))
    if len(cift) < 2:
        return s
    sema = {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in cift[:10]]}
    etiket = '<script type="application/ld+json">%s</script>' % json.dumps(sema, ensure_ascii=False)
    i = s.lower().rfind("</head>")
    return (s[:i] + etiket + "\n" + s[i:]) if i > 0 else s


def calistir(s, yol, kok):
    """Bir sayfanın HTML'ini alır, varlık alanları eklenmiş hâlini döndürür."""
    hsp = hesaplar(kok)
    if not hsp:
        return s

    # 1) alt bilgideki yer tutucu — yalnız boşsa doldur (iki kez basmayalım)
    if "data-sosyal" in s and _SOSYAL_YER.search(s):
        s = _SOSYAL_YER.sub(lambda m: m.group(1) + _sosyal_serit(hsp) + m.group(3), s, count=0)

    # 2) sayfada açıkça yazan taban fiyat (başlıkta ya da metinde)
    taban = None
    m = _TABAN_FIYAT.search(s)
    if m:
        try:
            taban = int(m.group(1).replace(".", ""))
        except Exception:
            taban = None
    kan = re.search(r'<link rel="canonical" href="([^"]+)"', s)
    url = kan.group(1) if kan else None

    # 3) JSON-LD düğümleri
    def _yer(mm):
        yeni, degisti = _sema_zenginlestir(mm.group(2), hsp, taban, url)
        return mm.group(1) + (yeni if degisti else mm.group(2)) + mm.group(3)

    s = _LD.sub(_yer, s)
    return sss_sema(s)
