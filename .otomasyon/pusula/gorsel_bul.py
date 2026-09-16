# -*- coding: utf-8 -*-
"""
GÖRSEL BUL — yazıya kapak: önce İNDİR, gerekmedikçe ÜRETME.

Yalnız serbest lisanslı kaynaklar (16.09.2026 kararı):
  · Wikimedia Commons  — CC0 / Kamu malı / CC BY / CC BY-SA
  · Openverse (WordPress'in açık görsel dizini) — ticari kullanıma açık lisanslar
Haber sitelerinin fotoğrafı, Google Trends'in verdiği resim, afiş ve maç görüntüsü ALINMAZ:
yayıncının telifidir; indirmek "görsel buldum" değil, izinsiz kullanımdır.

Her görselin künyesi (eser adı, yazar, lisans, kaynak sayfası) yazıyla birlikte saklanır ve
sayfada görselin altında basılır — CC BY / BY-SA lisanslarının şartı budur.

Çıktı: <site>/assets/ts/<ad>.jpg  +  {"dosya", "baslik", "yazar", "lisans", "lisans_url", "kaynak_url", "kaynak"}
Pillow varsa 960 px'e küçültülür (depo şişmesin); yoksa kaynağın 960 px önizlemesi olduğu gibi kaydedilir.
"""
import html, io, json, os, re, unicodedata, urllib.parse, urllib.request

from .ayarlar import SITE_KOK, KULLANICI_AJANI

GENISLIK = 960
IZINLI = re.compile(r"^(cc0|cc[- ]?zero|public domain|pd|kamu|cc[- ]?by(?:[- ]?sa)?(?:[- ]?\d(?:\.\d)?)?(?:[- ].*)?)$", re.I)
YASAK = re.compile(r"\b(nc|nd|non-?commercial|no-?deriv|fair use)\b", re.I)

# bölüme göre yedek arama (konunun kendisi bulunamazsa)
YEDEK_SORGU = {
    "spor": "stadium football", "muzik": "concert stage", "edebiyat": "books library reading",
    "ekran": "cinema hall", "film": "cinema hall", "dizi": "film set camera", "piyasa": "istanbul stock exchange",
    "teknoloji": "computer server", "sanat": "art gallery exhibition", "haber": "istanbul skyline",
    "gundem": "istanbul skyline", "muhendislik": "factory production line", "sosyal-medya": "smartphone",
    "hava": "rain clouds", "saglik": "hospital", "egitim": "classroom",
}


def _al(url, zaman=25):
    istek = urllib.request.Request(url, headers={"User-Agent": KULLANICI_AJANI + " gorsel_bul", "Accept": "*/*"})
    with urllib.request.urlopen(istek, timeout=zaman) as c:
        return c.read()


def _duz(t):
    return html.unescape(re.sub(r"<[^>]+>", " ", t or "")).replace("\xa0", " ").strip()


def _norm(t):
    t = (t or "").replace("ı", "i").replace("İ", "i")
    t = unicodedata.normalize("NFKD", t)
    return "".join(c for c in t if not unicodedata.combining(c)).lower()


def _ortak_var(sorgu, metin):
    """Görsel konuyla ilgili mi: sorgunun anlamlı kelimelerinden en az biri eser adında/açıklamasında geçmeli."""
    kel = [k for k in re.findall(r"[a-z0-9]{3,}", _norm(sorgu)) if k not in {"ile", "icin", "nedir", "the", "and", "zaman", "mac", "son", "dakika", "bugun", "haber"}]
    m = _norm(metin)
    if not kel:
        return False
    # tek kelimede biri yeter; iki ve üstünde en az iki kelime tutmalı ("erkan baş" → her Erkan olmaz)
    return sum(1 for k in kel if k in m or (len(k) >= 5 and k[:4] in m)) >= min(2, len(kel))


def lisans_uygun(lisans):
    l = re.sub(r"\s+", " ", (lisans or "").strip())
    return bool(l) and not YASAK.search(l) and bool(IZINLI.match(l))


def commons(sorgu, adet=12, ilgili_sart=True):
    url = ("https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search"
           "&gsrnamespace=6&gsrlimit=%d&gsrsearch=%s&prop=imageinfo&iiprop=url|size|mime|extmetadata&iiurlwidth=%d"
           % (adet, urllib.parse.quote(sorgu + " filetype:bitmap"), GENISLIK))
    try:
        d = json.loads(_al(url).decode("utf-8"))
    except Exception:
        return []
    out = []
    for s in sorted((d.get("query") or {}).get("pages", {}).values(), key=lambda x: x.get("index", 99)):
        ii = (s.get("imageinfo") or [{}])[0]
        em = ii.get("extmetadata") or {}
        lis = _duz((em.get("LicenseShortName") or {}).get("value"))
        if ii.get("mime") not in ("image/jpeg", "image/png") or (ii.get("width") or 0) < 800:
            continue
        if not lisans_uygun(lis):
            continue
        ad = re.sub(r"^File:|\.\w+$", "", s.get("title", ""))
        aciklama = _duz((em.get("ImageDescription") or {}).get("value"))[:300]
        if ilgili_sart and not _ortak_var(sorgu, ad + " " + aciklama):
            continue
        out.append({"url": ii.get("thumburl") or ii.get("url"), "baslik": ad.replace("_", " ")[:120],
                    "yazar": _duz((em.get("Artist") or {}).get("value"))[:120] or "Wikimedia Commons katkıcısı",
                    "lisans": lis, "lisans_url": _duz((em.get("LicenseUrl") or {}).get("value")),
                    "kaynak_url": ii.get("descriptionurl", ""), "kaynak": "Wikimedia Commons"})
    return out


def openverse(sorgu, adet=12, ilgili_sart=True):
    url = ("https://api.openverse.org/v1/images/?q=%s&license_type=commercial,modification&page_size=%d&mature=false"
           % (urllib.parse.quote(sorgu), adet))
    try:
        d = json.loads(_al(url).decode("utf-8"))
    except Exception:
        return []
    out = []
    for r in d.get("results", []):
        lis = ("CC0" if r.get("license") == "cc0" else "Public domain" if r.get("license") == "pdm"
               else "CC %s %s" % (r.get("license", "").upper(), r.get("license_version", ""))).strip()
        if not lisans_uygun(lis) or (r.get("width") or 0) < 800:
            continue
        if ilgili_sart and not _ortak_var(sorgu, (r.get("title") or "") + " " + " ".join(t.get("name", "") for t in r.get("tags") or [])):
            continue
        out.append({"url": r.get("url"), "baslik": (r.get("title") or "")[:120], "yazar": (r.get("creator") or "Openverse")[:120],
                    "lisans": lis, "lisans_url": r.get("license_url", ""), "kaynak_url": r.get("foreign_landing_url", ""),
                    "kaynak": r.get("source") or "Openverse"})
    return out


def _kaydet(veri, yol):
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    try:
        from PIL import Image
        im = Image.open(io.BytesIO(veri)).convert("RGB")
        if im.width > GENISLIK:
            im = im.resize((GENISLIK, round(im.height * GENISLIK / im.width)))
        im.save(yol, "JPEG", quality=78, optimize=True, progressive=True)
        return im.width, im.height
    except ImportError:
        open(yol, "wb").write(veri)
        return GENISLIK, round(GENISLIK * 9 / 16)


def bul(sorgular, ad, bolum=None, kok=None):
    """sorgular: en özgülden genele. Bulursa indirir, künyeyi döndürür; bulamazsa None (sayfa bölüm görselini kullanır)."""
    kok = kok or SITE_KOK
    yol = os.path.join(kok, "assets", "ts", ad + ".jpg")
    denemeler = [(q, True) for q in sorgular if q]
    if bolum in YEDEK_SORGU:
        denemeler.append((YEDEK_SORGU[bolum], False))
    for q, sart in denemeler:
        for kaynak in (commons, openverse):
            for aday in kaynak(q, ilgili_sart=sart):
                try:
                    veri = _al(aday["url"], 40)
                    if len(veri) < 15000:
                        continue
                    g, y = _kaydet(veri, yol)
                except Exception:
                    continue
                aday.update({"dosya": ad + ".jpg", "genislik": g, "yukseklik": y, "sorgu": q, "genel": not sart})
                aday.pop("url", None)
                return aday
    return None


if __name__ == "__main__":
    import sys
    print(json.dumps(bul(sys.argv[1:] or ["Bursa"], "deneme", "haber"), ensure_ascii=False, indent=1))
