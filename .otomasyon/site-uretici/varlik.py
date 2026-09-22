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


# ------------------------------------------------------------------ iş vitrini
_IS_KAYIT = re.compile(r"\{(?:[^{}]|\{[^{}]*\})*\}")
# Kap boş da olabilir, daha önce bizim bastığımız kartlarla dolu da — her iki
# durumda da yeniden yazılır. (22.09.2026: ilk sürüm yalnız BOŞ kabı dolduruyordu,
# bu yüzden hatalı basılmış kartlar bir sonraki koşuda düzelmiyordu.)
_IS_KAP = re.compile(r'(<div class="isler"[^>]*data-video="([^"]+)"[^>]*>)((?:\s|<a class="is-kart".*?</a>)*)(</div>)', re.S | re.I)


def isler(kok):
    """assets/videolar.js — YALNIZ yayınlanmış işler.

    Sitenin kendi kuralı, isler.html'de yazılı duruyor: "Yayınlanmış örneği
    olmayan bir kalemi işlerimiz gibi göstermiyoruz." Kayıtların 15'i
    "üretim kapsamı" (örneği yok); onlar iş vitrinine GİRMEZ.
    """
    try:
        s = open(os.path.join(kok, "assets", "videolar.js"), encoding="utf-8").read()
    except Exception:
        return []
    out = []
    for m in _IS_KAYIT.finditer(s):
        b = m.group(0)
        if "baslik:" not in b:
            continue
        d = {}
        for k in ("id", "yerel", "baslik", "kat", "musteri", "sure", "olcu", "teslim", "yil", "sehir"):
            mm = re.search(k + r':\s*"([^"]*)"', b)
            if mm and mm.group(1).strip():
                d[k] = mm.group(1).strip()
        et = re.search(r"etiket:\s*\[([^\]]*)\]", b)
        d["etiket"] = [x.strip().strip('"') for x in et.group(1).split(",")] if et else []
        if d.get("id") or d.get("yerel"):      # yayınlanmış örneği olan
            out.append(d)
    return out


def _is_karti(d, on, il=None):
    # ŞEHİR künyeye YAZILMAZ. 22.09.2026, sahibinin sözü: "konum belirtmek
    # zorunda değiliz, her yerde yapıyoruz." Şehir alanı yalnız O İLİN
    # sayfasında rozete dönüşür; başka hiçbir sayfada konum iddiası olmaz.
    kunye = " · ".join(x for x in (d.get("musteri"), d.get("kat"), d.get("sure")) if x)
    rozet = ""
    if il and (d.get("sehir") or "").lower().replace("ı", "i") == il.lower().replace("ı", "i"):
        rozet = '<span class="is-rozet">Bu ildeki işimiz</span>'
    d = dict(d, _rozet=rozet)
    if d.get("id"):
        adres = "https://www.youtube.com/watch?v=" + d["id"]
        dis = ' target="_blank" rel="noopener"'
    else:
        adres, dis = on + "isler", ""
    return ('<a class="is-kart" href="%s"%s>%s<b>%s</b>%s%s</a>'
            % (adres, dis, d.get("_rozet", ""), _kacir(d.get("baslik", "")),
               ('<span class="is-kunye">%s</span>' % _kacir(kunye)) if kunye else "",
               ('<span class="is-teslim">%s</span>' % _kacir(d["teslim"])) if d.get("teslim") else ""))


def _kacir(x):
    return (x.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def _video_sema(liste):
    d = []
    for x in liste:
        if not x.get("id"):
            continue
        v = {"@context": "https://schema.org", "@type": "VideoObject",
             "name": x.get("baslik", ""),
             "description": x.get("teslim") or x.get("baslik", ""),
             "thumbnailUrl": "https://i.ytimg.com/vi/%s/hqdefault.jpg" % x["id"],
             "embedUrl": "https://www.youtube.com/embed/" + x["id"],
             "publisher": {"@id": KURULUS_ID}}
        # uploadDate UYDURULMUYOR: yayın tarihini bilmiyoruz. Tarih girilince
        # (videolar.js'te yil:"2026-03-14") Google video zengin sonucuna aday olur.
        if x.get("yil"):
            v["uploadDate"] = x["yil"]
        d.append(v)
    return "".join('<script type="application/ld+json">%s</script>' % json.dumps(v, ensure_ascii=False)
                   for v in d)


def isler_bas(s, yol, kok):
    """Boş bırakılmış iş vitrinini HTML'e basar + VideoObject şeması ekler.

    22.09.2026 — bulunan sorun: işler yalnız JavaScript ile basılıyordu.
    Hizmet sayfalarının ham HTML'inde tek bir YouTube bağlantısı bile yoktu.
    Yani "bu işi yaptık" kanıtı, JavaScript çalıştırmayan her tarayıcı için —
    Bing, yapay zekâ tarayıcıları — hiç yoktu. Kanıt görünmüyorsa kanıt değil.
    JS çalışınca aynı listeyi yeniden basıyor; çelişki çıkmıyor.
    """
    kaplar = _IS_KAP.findall(s)
    if not kaplar:
        return s
    hepsi = isler(kok)
    if not hepsi:
        return s
    on = "../" if "/" in yol.replace("\\", "/") else ""
    kullanilan = []

    bos_etiket = []

    # sayfa bir il sayfasıysa ilin adını çıkar: sehir/bursa-drone-cekimi.html
    il = None
    yy = yol.replace("\\", "/")
    if yy.startswith("sehir/"):
        ad = os.path.basename(yy)[:-5].split("-")[0]
        il = ad

    def _doldur(m):
        etiket = m.group(2)
        # YEDEK YOK: etikete uyan yayınlanmış iş yoksa hiçbir şey basılmaz.
        # 22.09.2026 — ilk sürümde "uyan yoksa bütün işleri bas" diye bir yedek
        # vardı; drone sayfasında Avusturya'daki 3D animasyonu "drone işimiz"
        # gibi gösterdi. Sitenin kendi kuralı bunun tersi: örneği olmayan kalem
        # iş vitrininde görünmez. JavaScript tarafı da aynısını yapıp bölümü
        # gizliyor; statik taraf artık onunla aynı davranıyor.
        liste = [x for x in hepsi if etiket in x["etiket"]]
        if il:
            # o ilde çekilmiş iş varsa EN ÜSTE — yerel aramada en ağır kanıt bu
            def _il_mi(x):
                return (x.get("sehir") or "").lower().replace("ı", "i") == il.lower().replace("ı", "i")
            liste = sorted(liste, key=lambda x: (0 if _il_mi(x) else 1))
        liste = liste[:8]
        if not liste:
            bos_etiket.append(etiket)
            return m.group(1) + m.group(4)
        kullanilan.extend(liste)
        return m.group(1) + "".join(_is_karti(x, on, il) for x in liste) + m.group(4)

    # önceki koşudan kalan VideoObject şemalarını temizle — şema, sayfada
    # GÖRÜNEN işle birebir aynı olmalı; vitrin boşaldıysa şema da gitmeli
    s = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "VideoObject".*?</script>\n?',
               "", s, flags=re.S)
    s = _IS_KAP.sub(_doldur, s)
    # işi olmayan vitrin bölümü JS'siz tarayıcıda da görünmesin (JS de gizliyor)
    s = s.replace("<section class=\"acik\" data-video-bolum hidden>", "<section class=\"acik\" data-video-bolum>")
    if bos_etiket:
        s = s.replace("<section class=\"acik\" data-video-bolum>",
                      "<section class=\"acik\" data-video-bolum hidden>", 1)
    sema = _video_sema({x.get("id") or x.get("yerel"): x for x in kullanilan}.values())
    if sema:
        i = s.lower().rfind("</head>")
        if i > 0:
            s = s[:i] + sema + "\n" + s[i:]
    return s


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
    s = isler_bas(s, yol, kok)
    return sss_sema(s)
