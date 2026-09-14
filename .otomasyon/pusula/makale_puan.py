# -*- coding: utf-8 -*-
"""
YAYIN KAPISI — SEO puanı.

"SEO uygunluğu 100 olanı yayınlarız" cümlesinin kod karşılığı burası.
Puan bir tahmin değil; her madde ya sağlanıyor ya sağlanmıyor. Sağlanmayan
maddenin yanında NE YAPILACAĞI yazıyor, çünkü puanı görüp ne düzelteceğini
bilmemek işe yaramıyor.

Maddeler ve ağırlıkları (toplam 100):

  10  Başlık uzunluğu 30-62 karakter ve ana kelimeyi içeriyor
  10  Özet (meta açıklama) 110-158 karakter ve ana kelimeyi içeriyor
  10  Tek H1, en az üç H2
  10  En az 800 kelime
   8  Ana kelime ilk 120 kelimede geçiyor
   7  Kelime yoğunluğu %0,4 - %2,5 arasında
  10  En az iki iç bağlantı — ve bağlantı verilen dosya gerçekten var
   5  En az bir dış kaynak bağlantısı
   8  En az üç soru-cevap (SSS)
   5  Adres (slug) ascii, 60 karakteri geçmiyor, kelimeyi içeriyor
   7  Ortalama cümle 24 kelimeyi, hiçbir paragraf 130 kelimeyi geçmiyor
   5  İlk 250 kelimede doğrudan cevap bloğu var
   5  Özgünlük: mevcut sayfalarla benzerlik %55'in altında

Not: 100 puan "bu yazı iyi" demek değil. "Biçimsel olarak eksiksiz" demek.
İyi olup olmadığına insan karar veriyor; sistem yalnızca eksik olanı
yayından geçirmiyor.
"""
import os, re, glob, unicodedata

from .ayarlar import SITE_KOK

TR = str.maketrans({"ı": "i", "İ": "i", "ğ": "g", "Ğ": "g", "ş": "s", "Ş": "s",
                    "ö": "o", "Ö": "o", "ü": "u", "Ü": "u", "ç": "c", "Ç": "c",
                    "â": "a", "î": "i", "û": "u"})


def _kucuk(x):
    return str(x).replace("I", "ı").replace("İ", "i").lower()


def slug(x):
    d = _kucuk(x).translate(TR)
    d = unicodedata.normalize("NFKD", d).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", d).strip("-")


def _bolumle(metin):
    """Markdown'ı ölçülebilir parçalara ayırır."""
    satir = metin.splitlines()
    h1 = [s[2:].strip() for s in satir if s.startswith("# ")]
    h2 = [s[3:].strip() for s in satir if s.startswith("## ")]
    govde, sss_modu, sss = [], False, []
    soru = None
    for s in satir:
        t = s.strip()
        if t.startswith("## "):
            sss_modu = "sık sorulan" in _kucuk(t)
            continue
        if t.startswith("#") or t.startswith("---") or t.startswith("*Taslak"):
            continue
        if sss_modu:
            m = re.match(r"\*\*(.+?)\*\*\s*$", t)
            if m:
                soru = m.group(1)
            elif t and soru:
                sss.append((soru, t))
                soru = None
            continue
        if t:
            govde.append(t)
    duz = " ".join(govde)
    duz = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", duz)     # bağlantı metni kalsın
    duz = re.sub(r"[*`>#-]", " ", duz)
    duz = re.sub(r"\s+", " ", duz).strip()
    ic = re.findall(r"\]\((?:\.\./|/)([^)]+)\)", metin)
    dis = re.findall(r"\]\((https?://[^)]+)\)", metin)
    return {"h1": h1, "h2": h2, "govde": govde, "duz": duz,
            "sss": sss, "ic": ic, "dis": dis}


def _benzerlik(duz, haric=()):
    """Mevcut sayfalarla en yüksek kelime örtüşmesi (0-1)."""
    kendi = set(w for w in re.findall(r"\w{5,}", _kucuk(duz)))
    if not kendi:
        return 0.0
    enb = 0.0
    yollar = (glob.glob(os.path.join(SITE_KOK, "*.html")) +
              glob.glob(os.path.join(SITE_KOK, "hizmetler", "*.html")) +
              glob.glob(os.path.join(SITE_KOK, "blog", "*.html")))
    haric = set(os.path.abspath(h) for h in haric)
    for y in yollar[:80]:
        if os.path.abspath(y) in haric:
            continue          # güncellenen sayfanın kendisiyle kıyaslanmaz
        try:
            g = open(y, encoding="utf-8").read()
        except Exception:
            continue
        g = re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", g, flags=re.S)
        o = set(w for w in re.findall(r"\w{5,}", _kucuk(g)))
        if not o:
            continue
        ort = len(kendi & o) / float(len(kendi))
        if ort > enb:
            enb = ort
    return enb


def _cakisan_yazi(kelime, adres):
    """Aynı ana kelimeyi zaten hedefleyen başka bir yazı var mı?

    İki sayfanın aynı aramayı hedeflemesi ikisini birden geriletiyor
    (anahtar kelime yamyamlığı). Doğrusu ikinci sayfa değil, birinci
    sayfanın güçlendirilmesi.
    """
    k = _kucuk(kelime).strip()
    if not k:
        return ""
    hedef = "%s.html" % adres
    for y in glob.glob(os.path.join(SITE_KOK, "blog", "*.html")):
        d = os.path.basename(y)
        if d in ("index.html", hedef):
            continue
        try:
            g = open(y, encoding="utf-8").read()
        except Exception:
            continue
        bas = re.search(r"<title>(.*?)</title>", g, re.S)
        ana = re.search(r'name="keywords" content="([^"]*)"', g)
        havuz = _kucuk((bas.group(1) if bas else "") + " " + (ana.group(1) if ana else ""))
        if k in havuz:
            return d
    return ""


def _m(ad, agirlik, tam, neden="", nasil=""):
    return {"ad": ad, "agirlik": agirlik, "tam": bool(tam),
            "puan": agirlik if tam else 0, "neden": neden, "nasil": nasil}


def puanla(metin, kelime="", ozet="", adres=""):
    """metin: markdown. kelime: ana anahtar kelime. Döner: dict."""
    p = _bolumle(metin)
    k = _kucuk(kelime).strip()
    baslik = p["h1"][0] if p["h1"] else ""
    duz = p["duz"]
    kelimeler = duz.split()
    n = len(kelimeler)
    ilk120 = " ".join(kelimeler[:120])
    ilk250 = " ".join(kelimeler[:250])
    adres = adres or slug(baslik)
    maddeler = []

    # 1 başlık
    tam = bool(baslik) and 30 <= len(baslik) <= 62 and (not k or k.split()[0] in _kucuk(baslik))
    maddeler.append(_m("Başlık", 10, tam,
                       "Başlık %d karakter." % len(baslik),
                       "30-62 karakter olsun ve ana kelimeyi taşısın."))
    # 2 özet
    o = (ozet or "").strip()
    tam = 110 <= len(o) <= 158 and (not k or k.split()[0] in _kucuk(o))
    maddeler.append(_m("Özet (meta açıklama)", 10, tam,
                       "Özet %d karakter." % len(o),
                       "110-158 karakter yaz ve ana kelimeyi içine koy."))
    # 3 yapı
    tam = len(p["h1"]) == 1 and len(p["h2"]) >= 3
    maddeler.append(_m("Başlık yapısı", 10, tam,
                       "%d adet H1, %d adet H2." % (len(p["h1"]), len(p["h2"])),
                       "Tek H1 ve en az üç H2 olmalı."))
    # 4 uzunluk
    maddeler.append(_m("Uzunluk", 10, n >= 800, "%d kelime." % n,
                       "En az 800 kelime. Kısa yazı aramada tutunmuyor."))
    # 5 ilk geçiş
    tam = (not k) or (k in _kucuk(ilk120))
    maddeler.append(_m("Ana kelime girişte", 8, tam,
                       "Ana kelime ilk 120 kelimede %s." % ("var" if tam else "yok"),
                       "Ana kelimeyi giriş paragrafında doğal biçimde kullan."))
    # 6 yoğunluk
    gecis = _kucuk(duz).count(k) if k else 0
    yog = (gecis / float(n) * 100) if n else 0
    tam = (not k) or (0.4 <= yog <= 2.5)
    maddeler.append(_m("Kelime yoğunluğu", 7, tam,
                       "%%%.2f (%d geçiş)." % (yog, gecis),
                       "%0,4 ile %2,5 arasında olmalı; altı zayıf, üstü şişirme."))
    # 7 iç bağlantı
    var = [y for y in p["ic"] if os.path.isfile(os.path.join(SITE_KOK, y))]
    tam = len(var) >= 2
    maddeler.append(_m("İç bağlantı", 10, tam,
                       "%d bağlantının %d tanesi gerçek sayfaya gidiyor."
                       % (len(p["ic"]), len(var)),
                       "En az iki iç bağlantı ver; hedef sayfa gerçekten var olsun."))
    # 8 dış kaynak
    maddeler.append(_m("Dış kaynak", 5, len(p["dis"]) >= 1,
                       "%d dış bağlantı." % len(p["dis"]),
                       "İddiayı kaynağa bağla; kaynaksız rakam yazma."))
    # 9 SSS
    maddeler.append(_m("Soru-cevap", 8, len(p["sss"]) >= 3,
                       "%d soru-cevap." % len(p["sss"]),
                       "En az üç soru-cevap yaz; SSS şeması buradan çıkıyor."))
    # 10 adres
    tam = (adres == slug(adres)) and len(adres) <= 60 and (
          (not k) or slug(k).split("-")[0] in adres)
    maddeler.append(_m("Adres (slug)", 5, tam, "/blog/%s.html" % adres,
                       "Kısa, ascii ve ana kelimeyi içeren bir adres kullan."))
    # 11 okunabilirlik
    cumleler = [c for c in re.split(r"(?<=[.!?])\s+", duz) if c.strip()]
    ort = (sum(len(c.split()) for c in cumleler) / float(len(cumleler))) if cumleler else 0
    uzun_p = max([len(g.split()) for g in p["govde"]] or [0])
    tam = ort <= 24 and uzun_p <= 130
    maddeler.append(_m("Okunabilirlik", 7, tam,
                       "Ortalama cümle %.1f kelime, en uzun paragraf %d kelime."
                       % (ort, uzun_p),
                       "Cümleleri kısalt (24 kelime altı), paragrafları böl."))
    # 12 doğrudan cevap
    tam = ("kısa cevap" in _kucuk(" ".join(p["h2"]))) or (
          bool(k) and k in _kucuk(ilk250))
    maddeler.append(_m("Doğrudan cevap", 5, tam,
                       "Girişte cevap bloğu %s." % ("var" if tam else "yok"),
                       "İlk 250 kelimede soruyu doğrudan cevaplayan bir blok koy."))
    # 13 özgünlük — güncellenen sayfanın kendisi kıyasa girmez
    kendi = os.path.join(SITE_KOK, "blog", "%s.html" % adres)
    b = _benzerlik(duz, haric=(kendi,))
    cak = _cakisan_yazi(kelime, adres)
    maddeler.append(_m("Özgünlük", 5, b < 0.55 and not cak,
                       ("Aynı kelimeyi zaten /blog/%s hedefliyor." % cak) if cak
                       else "Mevcut sayfalarla en yüksek örtüşme %%%.0f." % (b * 100),
                       "Var olan sayfayı tekrar etme; ya açıyı değiştir ya da "
                       "o sayfayı bu yazıyla güncelle (aynı adrese bas)."))

    puan = sum(m["puan"] for m in maddeler)
    return {"puan": puan, "gecti": puan >= 100, "kelime_sayisi": n,
            "maddeler": maddeler,
            "eksik": [m for m in maddeler if not m["tam"]]}
