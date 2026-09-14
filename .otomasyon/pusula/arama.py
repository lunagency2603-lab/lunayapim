# -*- coding: utf-8 -*-
"""
ARAMA PERFORMANSI — Google Search Console verisini okur ve şehir kırılımına çevirir.

Neden API değil de dosya:
  Search Console API'si OAuth istiyor, kotası var ve yetki her ay yenileniyor.
  Dışa aktarma ise üç tık: Search Console → Performans → sağ üstteki dışa aktar →
  "CSV indir". İnen ZIP'i panele bırakıyorsun, gerisi burada.

Ne okur:
  · Search Console'un ZIP dışa aktarımı (Sorgular/Sayfalar/Ülkeler/Cihazlar/Tarihler)
  · Tek başına CSV veya TSV
  · Türkçe ve İngilizce arayüz başlıkları
  · Excel'in başa koyduğu BOM ve noktalı virgüllü ayraç

Ne üretir:
  · şehir bazında tıklanma / gösterim / ortalama konum
  · hizmet bazında aynı kırılım
  · hiç gösterim almayan sayfalar ("ölü sayfa")
  · gösterim alıp tıklanmayan sayfalar ("kapıda kaybediyoruz")
  · konum 11-20 arasındaki sayfalar ("ikinci sayfa — itilecek olanlar")
"""
import csv, io, os, re, json, zipfile, datetime, unicodedata

# ---------------------------------------------------------------- başlık eşleme
# Search Console arayüz diline göre başlık değişiyor; anahtar kelimeyle yakalıyoruz.
SUTUN = {
    "tiklama":  ("tıklama", "clicks", "click"),
    "gosterim": ("gösterim", "impression"),
    "to":       ("to", "ctr"),
    "konum":    ("konum", "position"),
}
ANAHTAR_SUTUN = ("sorgu", "query", "sayfa", "page", "url", "ülke", "country",
                 "cihaz", "device", "tarih", "date", "görünüm", "appearance")

DOSYA_TURU = {
    "sorgu": "sorgular", "quer": "sorgular",
    "sayfa": "sayfalar", "page": "sayfalar",
    "ülke": "ulkeler", "countr": "ulkeler",
    "cihaz": "cihazlar", "device": "cihazlar",
    "tarih": "tarihler", "date": "tarihler",
    "görünüm": "gorunum", "appearance": "gorunum",
}


# Türkçe harfleri BOZMADAN küçültür. (NFKD kullanılmıyor: "gösterim" → "go¨sterim"
# oluyor ve başlık eşleşmesi sessizce kayboluyordu.)
_KUCUK = str.maketrans({"İ": "i", "I": "ı", "Ğ": "ğ", "Ü": "ü", "Ş": "ş", "Ö": "ö", "Ç": "ç"})


def _sade(x):
    return (x or "").replace("\ufeff", "").strip().translate(_KUCUK).lower()


def _sayi(x):
    """'1.234', '1,234', '%3,4', '12,7' → sayı. Çevrilemezse None."""
    if x is None:
        return None
    s = str(x).strip().replace("%", "").replace("\xa0", " ").strip()
    if not s or s in ("-", "—"):
        return None
    # binlik ayracı ile ondalık ayracını ayırt et
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".") if s.rfind(",") > s.rfind(".") else s.replace(",", "")
    elif "," in s:
        s = s.replace(",", ".") if len(s.split(",")[-1]) <= 2 else s.replace(",", "")
    else:
        # 1.234 gibi binlik nokta
        if re.fullmatch(r"\d{1,3}(\.\d{3})+", s):
            s = s.replace(".", "")
    try:
        return float(s)
    except ValueError:
        return None


def _ayrac_bul(metin):
    ilk = metin.splitlines()[0] if metin else ""
    return ";" if ilk.count(";") > ilk.count(",") else ","


def csv_oku(metin):
    """CSV/TSV metnini [{sutun: deger}] listesine çevirir; başlıkları eşler."""
    metin = metin.lstrip("﻿")
    ayrac = "\t" if "\t" in (metin.splitlines()[0] if metin else "") else _ayrac_bul(metin)
    r = list(csv.reader(io.StringIO(metin), delimiter=ayrac))
    if len(r) < 2:
        return [], None
    basliklar = [_sade(b) for b in r[0]]

    # anahtar sütun: sorgu / sayfa / ülke / cihaz / tarih — yoksa ilk sütun
    anahtar_i = 0
    tur = None
    for i, b in enumerate(basliklar):
        for iz, ad in DOSYA_TURU.items():
            if iz in b:
                anahtar_i, tur = i, ad
                break
        if tur:
            break

    olcum_i = {}
    for ad, izler in SUTUN.items():
        for i, b in enumerate(basliklar):
            if i == anahtar_i or i in olcum_i.values():
                continue
            # "TO" çok kısa; onu tam eşleşmeyle arıyoruz ki başka başlığa yapışmasın
            uydu = (b in izler) if ad == "to" else any(iz in b for iz in izler)
            if uydu:
                olcum_i.setdefault(ad, i)
                break

    satirlar = []
    for s in r[1:]:
        if not s or len(s) <= anahtar_i or not s[anahtar_i].strip():
            continue
        kayit = {"anahtar": s[anahtar_i].strip()}
        for ad, i in olcum_i.items():
            kayit[ad] = _sayi(s[i]) if i < len(s) else None
        satirlar.append(kayit)
    return satirlar, tur


def zip_oku(yol):
    """Search Console ZIP dışa aktarımını okur. Döner: {tur: [satır]}"""
    cikti = {}
    with zipfile.ZipFile(yol) as z:
        for ad in z.namelist():
            if not ad.lower().endswith((".csv", ".tsv")):
                continue
            ham = z.read(ad)
            for kod in ("utf-8-sig", "utf-8", "cp1254", "latin-1"):
                try:
                    metin = ham.decode(kod)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                continue
            satir, tur = csv_oku(metin)
            if not satir:
                continue
            if not tur:
                sade_ad = _sade(os.path.basename(ad))
                tur = next((v for k, v in DOSYA_TURU.items() if k in sade_ad), "diger")
            cikti.setdefault(tur, []).extend(satir)
    return cikti


def dosya_oku(yol):
    """ZIP ya da tek CSV — ikisini de kabul eder."""
    if zipfile.is_zipfile(yol):
        return zip_oku(yol)
    with open(yol, "rb") as f:
        ham = f.read()
    for kod in ("utf-8-sig", "utf-8", "cp1254", "latin-1"):
        try:
            metin = ham.decode(kod)
            break
        except UnicodeDecodeError:
            continue
    else:
        return {}
    satir, tur = csv_oku(metin)
    if not satir:
        return {}
    return {tur or "diger": satir}


# ---------------------------------------------------------------- URL → şehir/hizmet
# Sitedeki adres düzeni:  /sehir/<il>.html  ve  /sehir/<il>-<hizmet>.html
HIZMET_EK = ("insaat-3d-modelleme", "urun-animasyon", "klip-cekimi", "emlak-video",
             "emlak-kurumsal", "drone-cekimi", "drone-fpv", "dugun-cekimi",
             "dugun-etkinlik", "isletme-tanitim", "tanitim-filmi", "sanal-tur",
             "mimari-gorsellestirme", "urun-cekimi", "kurumsal-tanitim")

HIZMET_AD = {
    "insaat-3d-modelleme": "İnşaat 3D modelleme",
    "mimari-gorsellestirme": "Mimari görselleştirme",
    "urun-animasyon": "Ürün animasyonu",
    "urun-cekimi": "Ürün çekimi",
    "klip-cekimi": "Klip çekimi",
    "emlak-video": "Emlak videosu",
    "emlak-kurumsal": "Emlak & kurumsal",
    "drone-cekimi": "Drone çekimi",
    "drone-fpv": "Drone / FPV",
    "dugun-cekimi": "Düğün çekimi",
    "dugun-etkinlik": "Düğün & etkinlik",
    "isletme-tanitim": "İşletme tanıtımı",
    "tanitim-filmi": "Tanıtım filmi",
    "sanal-tur": "Sanal tur",
    "kurumsal-tanitim": "Kurumsal tanıtım",
}


def _slug_il(slug, iller_slug):
    """'bursa-drone-cekimi' → ('bursa', 'drone-cekimi'). Bilinmiyorsa (None, None)."""
    slug = slug.strip("/").replace(".html", "")
    if slug in iller_slug:
        return iller_slug[slug], None
    for ek in sorted(HIZMET_EK, key=len, reverse=True):
        if slug.endswith("-" + ek):
            il_slug = slug[: -(len(ek) + 1)]
            if il_slug in iller_slug:
                return iller_slug[il_slug], ek
    # bilinmeyen hizmet eki: ilk parçayı il say
    for il_slug, il_ad in iller_slug.items():
        if slug == il_slug or slug.startswith(il_slug + "-"):
            return il_ad, slug[len(il_slug) + 1:] or None
    return None, None


def url_coz(url, iller_slug):
    """
    Bir Search Console sayfa adresini {bolum, il, hizmet, yol} olarak çözer.
    bolum: sehir | hizmet | blog | ana | diger
    """
    yol = re.sub(r"^https?://[^/]+", "", (url or "").strip())
    yol = yol.split("?")[0].split("#")[0]
    d = {"yol": yol or "/", "bolum": "diger", "il": None, "hizmet": None}
    if yol in ("", "/"):
        d["bolum"] = "ana"
        return d
    p = yol.strip("/").split("/")
    if p[0] == "sehir" and len(p) > 1:
        d["bolum"] = "sehir"
        il, hz = _slug_il(p[1], iller_slug)
        d["il"], d["hizmet"] = il, hz
    elif p[0] == "hizmetler":
        d["bolum"] = "hizmet"
        d["hizmet"] = (p[1].replace(".html", "") if len(p) > 1 else None)
    elif p[0] == "blog":
        d["bolum"] = "blog"
    elif len(p) == 1:
        d["bolum"] = "ana"
    return d


def il_slugu(iller):
    """['Bursa','Afyonkarahisar'] → {'bursa': 'Bursa', ...} (site üreticisiyle aynı kural)"""
    TR = str.maketrans({"ı": "i", "İ": "i", "I": "i", "ğ": "g", "Ğ": "g", "ş": "s", "Ş": "s",
                        "ö": "o", "Ö": "o", "ü": "u", "Ü": "u", "ç": "c", "Ç": "c"})
    d = {}
    for il in iller:
        s = unicodedata.normalize("NFKD", il.translate(TR)).encode("ascii", "ignore").decode()
        s = re.sub(r"-{2,}", "-", "".join(c if c.isalnum() else "-" for c in s.lower())).strip("-")
        d[s] = il
    return d


# ---------------------------------------------------------------- analiz
def sayfa_analizi(sayfalar, iller, tum_sayfa_yollari=None):
    """
    sayfalar: [{anahtar(url), tiklama, gosterim, to, konum}]
    tum_sayfa_yollari: sitedeki tüm yollar — hiç görünmeyenleri bulmak için (isteğe bağlı)
    """
    slug = il_slugu(iller)
    il_toplam, hizmet_toplam, bolum_toplam = {}, {}, {}
    satirlar = []
    gorulen_yol = set()

    for s in sayfalar:
        c = url_coz(s["anahtar"], slug)
        t = int(s.get("tiklama") or 0)
        g = int(s.get("gosterim") or 0)
        k = s.get("konum")
        gorulen_yol.add(c["yol"])
        satirlar.append({**c, "tiklama": t, "gosterim": g, "konum": k,
                         "to": (100.0 * t / g) if g else 0.0, "url": s["anahtar"]})

        def ekle(sozluk, anahtar):
            if not anahtar:
                return
            d = sozluk.setdefault(anahtar, {"tiklama": 0, "gosterim": 0, "sayfa": 0,
                                            "konum_toplam": 0.0, "konum_adet": 0})
            d["tiklama"] += t; d["gosterim"] += g; d["sayfa"] += 1
            if k is not None:
                d["konum_toplam"] += k * max(g, 1); d["konum_adet"] += max(g, 1)

        ekle(il_toplam, c["il"])
        ekle(hizmet_toplam, c["hizmet"])
        ekle(bolum_toplam, c["bolum"])

    def duzelt(sozluk):
        cikti = []
        for ad, d in sozluk.items():
            cikti.append({
                "ad": HIZMET_AD.get(ad, ad),
                "anahtar": ad, "tiklama": d["tiklama"], "gosterim": d["gosterim"],
                "sayfa": d["sayfa"],
                "to": round(100.0 * d["tiklama"] / d["gosterim"], 2) if d["gosterim"] else 0.0,
                "konum": round(d["konum_toplam"] / d["konum_adet"], 1) if d["konum_adet"] else None,
            })
        cikti.sort(key=lambda x: (-x["tiklama"], -x["gosterim"]))
        return cikti

    # --- fırsat listeleri
    kapida = [s for s in satirlar if s["gosterim"] >= 20 and s["tiklama"] == 0]
    kapida.sort(key=lambda s: -s["gosterim"])
    ikinci_sayfa = [s for s in satirlar
                    if s["konum"] is not None and 10.5 <= s["konum"] <= 20.5 and s["gosterim"] >= 10]
    ikinci_sayfa.sort(key=lambda s: -s["gosterim"])
    yakin = [s for s in satirlar
             if s["konum"] is not None and 3.5 <= s["konum"] <= 10.5 and s["gosterim"] >= 10]
    yakin.sort(key=lambda s: -s["gosterim"])

    olu = []
    if tum_sayfa_yollari:
        for y in sorted(set(tum_sayfa_yollari) - gorulen_yol):
            c = url_coz(y, slug)
            olu.append({**c, "url": y})

    return {
        "satir": sorted(satirlar, key=lambda s: (-s["tiklama"], -s["gosterim"])),
        "il": duzelt(il_toplam),
        "hizmet": duzelt(hizmet_toplam),
        "bolum": duzelt(bolum_toplam),
        "kapida": kapida[:40],
        "ikinci_sayfa": ikinci_sayfa[:40],
        "yakin": yakin[:40],
        "olu": olu[:200],
        "toplam": {
            "tiklama": sum(s["tiklama"] for s in satirlar),
            "gosterim": sum(s["gosterim"] for s in satirlar),
            "sayfa": len(satirlar),
            "gorunmeyen": len(olu),
        },
    }


def sorgu_analizi(sorgular, iller):
    """Sorguları şehir adı geçip geçmediğine göre ayırır — yerel niyeti ölçer."""
    ad_kucuk = {il.lower(): il for il in iller}
    yerel, genel = [], []
    il_sorgu = {}
    for s in sorgular:
        q = (s["anahtar"] or "").lower()
        t = int(s.get("tiklama") or 0); g = int(s.get("gosterim") or 0)
        kayit = {"sorgu": s["anahtar"], "tiklama": t, "gosterim": g,
                 "konum": s.get("konum"),
                 "to": round(100.0 * t / g, 2) if g else 0.0}
        bulunan = next((ad for k, ad in ad_kucuk.items() if k in q), None)
        if bulunan:
            kayit["il"] = bulunan
            yerel.append(kayit)
            d = il_sorgu.setdefault(bulunan, {"tiklama": 0, "gosterim": 0, "sorgu": 0})
            d["tiklama"] += t; d["gosterim"] += g; d["sorgu"] += 1
        else:
            genel.append(kayit)
    il_liste = [{"ad": a, **d} for a, d in il_sorgu.items()]
    il_liste.sort(key=lambda x: (-x["tiklama"], -x["gosterim"]))
    return {
        "yerel": sorted(yerel, key=lambda x: (-x["tiklama"], -x["gosterim"]))[:80],
        "genel": sorted(genel, key=lambda x: (-x["tiklama"], -x["gosterim"]))[:80],
        "il": il_liste,
        "yerel_pay": round(100.0 * sum(x["gosterim"] for x in yerel) /
                           max(1, sum(x["gosterim"] for x in yerel + genel)), 1),
    }


def ice_aktar(yol, iller, tum_sayfa_yollari=None):
    """Tek giriş noktası: dosyayı oku, analiz et, tek sözlük döndür."""
    ham = dosya_oku(yol)
    if not ham:
        return {"hata": "Dosya okunamadı ya da içinde tanınan bir tablo yok."}
    sayfalar = ham.get("sayfalar", [])
    sorgular = ham.get("sorgular", [])
    sonuc = {
        "kaynak": os.path.basename(yol),
        "zaman": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
        "bulunan_tablo": sorted(ham.keys()),
        "tarih": ham.get("tarihler", []),
        "cihaz": ham.get("cihazlar", []),
        "ulke": ham.get("ulkeler", []),
    }
    if sayfalar:
        sonuc["sayfa"] = sayfa_analizi(sayfalar, iller, tum_sayfa_yollari)
    if sorgular:
        sonuc["sorgu"] = sorgu_analizi(sorgular, iller)
    if not sayfalar and not sorgular:
        sonuc["hata"] = ("Dosyada 'Sayfalar' veya 'Sorgular' tablosu bulunamadı. "
                         "Search Console → Performans → Dışa aktar → 'CSV indir' ile inen "
                         "ZIP'i olduğu gibi yükleyin.")
    return sonuc


def site_yollari(kok):
    """Sitedeki yayınlanmış tüm sayfaların yolları — 'hiç görünmeyen' listesi için."""
    yollar = []
    for dizin, _, dosyalar in os.walk(kok):
        for d in dosyalar:
            if not d.endswith(".html"):
                continue
            tam = os.path.join(dizin, d)
            gor = "/" + os.path.relpath(tam, kok).replace(os.sep, "/")
            if gor.endswith("/index.html"):
                gor = gor[: -len("index.html")]
            yollar.append(gor)
    return yollar
