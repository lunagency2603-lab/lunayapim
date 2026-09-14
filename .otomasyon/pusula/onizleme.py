# -*- coding: utf-8 -*-
"""
ÖNİZLEME — firmanın eksikleri giderilmiş hâlini, kendi malzemesiyle gösterir.

Neden böyle: teklife eklenen genel bir yapay zekâ videosu "bu bana özel
hazırlanmamış" hissi verir ve tam ters etki yapar. En ikna edici görsel,
firmanın <b>kendi</b> projesinin düzgün kurgulanmış hâlidir. O yüzden burada
kredi yakan bir model yok — malzeme firmanın kendi açık sitesinden geliyor,
işi ffmpeg ve Pillow yapıyor. Kredileri ücretli işlere saklıyoruz.

Üretilenler (aday klasörüne):
    onizleme.png      1080×1350 — düzeltilmiş hâlin posteri
    onizleme.mp4      ~8 sn dikey film, aynı malzemeden
    onizleme-kaynak.md hangi görsel nereden alındı (kaynak defteri)

KURALLAR
- Yalnızca firmanın kendi yayınladığı sayfadan malzeme alınır; sosyal medya
  kazılmaz, kişi verisi toplanmaz.
- Üretilen görsel TASLAK'tır ve üzerinde öyle yazar. Firmanın sitesiymiş gibi
  görünen bir sayfa üretilmez.
- Bu dosyalar lunayapim.com'a YAYINLANMAZ; yalnızca o firmaya gönderilir.
- Firmanın görseli bulunamazsa uydurma yapılmaz: poster görselsiz, sade
  tipografiyle çıkar ve teklifte "görsel bulunamadı" notu düşülür.
"""
import os, re, io, html, json, math, datetime, urllib.parse, subprocess, glob
import urllib.request, ssl, gzip, tempfile, shutil

from .kaynaklar.agir import getir
from .ayarlar import KULLANICI_AJANI, ISTEK_ZAMAN_ASIMI

_CTX = ssl.create_default_context()


def ham_getir(url, zaman=15, dogrula=True):
    """Görsel indirmek için HAM bayt getirir — metne çevirmez."""
    istek = urllib.request.Request(url, headers={"User-Agent": KULLANICI_AJANI,
                                                 "Accept": "image/*,*/*"})
    ctx = _CTX if dogrula else ssl._create_unverified_context()
    try:
        with urllib.request.urlopen(istek, timeout=zaman, context=ctx) as c:
            veri = c.read()
            if c.headers.get("Content-Encoding") == "gzip":
                veri = gzip.decompress(veri)
            return c.status, veri
    except Exception:
        return 0, b""

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    PIL_VAR = True
except Exception:
    PIL_VAR = False

EN, BOY = 1080, 1350                     # WhatsApp'ta en iyi duran oran (4:5)
INK = (12, 12, 14)
BONE = (239, 237, 232)
GRI = (150, 148, 142)
VARSAYILAN_VURGU = (232, 69, 44)

_FONT_ADAY = [
    "/usr/share/fonts/truetype/google-fonts/Poppins-%s.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-%s.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf",
]


def _font(kalin, boy):
    for kalip in _FONT_ADAY:
        for ad in (("Bold", "Bold", "-Bold") if kalin else ("Regular", "Regular", "")):
            y = kalip % ad
            if os.path.exists(y):
                try:
                    return ImageFont.truetype(y, boy)
                except Exception:
                    pass
    return ImageFont.load_default()


# --------------------------------------------------------------- malzeme toplama
_IMG = re.compile(r'<img[^>]+>', re.I)
_SRC = re.compile(r'(?:data-src|data-original|srcset|src)\s*=\s*["\']([^"\']+)["\']', re.I)
_OG = re.compile(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', re.I)
_TITLE = re.compile(r'<title[^>]*>(.*?)</title>', re.I | re.S)
_TEL = re.compile(r'(?:tel:|href=["\']tel:)\s*([+0-9\s\(\)\-]{7,})', re.I)


def _mutlak(kok, u):
    if not u:
        return None
    u = u.split()[0].strip()
    if u.startswith("data:"):
        return None
    return urllib.parse.urljoin(kok, u)


def varliklar(url, azami_gorsel=14):
    """Firmanın kendi sayfasından malzeme çıkarır. Hiçbir alan uydurulmaz."""
    s = {"url": url, "ulasildi": False, "baslik": None, "logo": None,
         "gorseller": [], "telefon": None, "kaynak": []}
    if not url:
        return s
    if not url.startswith("http"):
        url = "https://" + url
    kod, govde, son = getir(url, zaman_asimi=14)
    if kod == 0 or not govde:
        kod, govde, son = getir(url, dogrula_ssl=False, zaman_asimi=14)
    if kod == 0 or kod >= 400 or not govde:
        return s
    s["ulasildi"] = True
    kok = son or url
    s["kaynak"].append(kok)

    m = _TITLE.search(govde)
    if m:
        s["baslik"] = re.sub(r"\s+", " ", html.unescape(m.group(1))).strip()[:120]
    m = _TEL.search(govde)
    if m:
        s["telefon"] = re.sub(r"\s+", " ", m.group(1)).strip()

    bulunan, logolar = [], []
    for etiket in _IMG.findall(govde):
        sm = _SRC.search(etiket)
        if not sm:
            continue
        tam = _mutlak(kok, sm.group(1))
        if not tam or tam in bulunan:
            continue
        alt = etiket.lower()
        if "logo" in alt or "brand" in alt:
            logolar.append(tam)
        else:
            bulunan.append(tam)
    og = _OG.search(govde)
    if og:
        t = _mutlak(kok, og.group(1))
        if t and t not in bulunan:
            bulunan.insert(0, t)

    s["logo"] = logolar[0] if logolar else None
    s["gorseller"] = bulunan[:azami_gorsel]
    return s


def indir(url, hedef, azami_mb=8):
    """Tek görsel indirir. Başarısızsa None döner — uydurma yok."""
    kod, ham = ham_getir(url)
    if kod != 200 or not ham:
        kod, ham = ham_getir(url, dogrula=False)
    if kod != 200 or not ham:
        return None
    if len(ham) > azami_mb * 1024 * 1024:
        return None
    try:
        im = Image.open(io.BytesIO(ham))
        im.load()
    except Exception:
        return None
    if im.width < 400 or im.height < 260:      # küçük ikon/rozet işimize yaramaz
        return None
    im = im.convert("RGB")
    im.save(hedef, "JPEG", quality=92)
    return hedef


def malzeme_indir(v, klasor, azami=4):
    """Kullanılabilir görselleri indirir. (liste, logo_yolu) döner."""
    os.makedirs(klasor, exist_ok=True)
    alinan, defter = [], []
    logo = None
    if v.get("logo"):
        y = os.path.join(klasor, "logo.jpg")
        if indir(v["logo"], y):
            logo = y
            defter.append(("logo", v["logo"]))
    for i, u in enumerate(v.get("gorseller", [])):
        if len(alinan) >= azami:
            break
        y = os.path.join(klasor, "g%d.jpg" % (i + 1))
        if indir(u, y):
            alinan.append(y)
            defter.append(("görsel %d" % len(alinan), u))
    return alinan, logo, defter


def vurgu_rengi(logo_yolu):
    """Logodan marka rengini çıkarır; bulamazsa Luna kırmızısına düşer."""
    if not logo_yolu or not PIL_VAR:
        return VARSAYILAN_VURGU
    try:
        im = Image.open(logo_yolu).convert("RGB").resize((60, 60))
    except Exception:
        return VARSAYILAN_VURGU
    sayac = {}
    for p in im.getdata():
        r, g, b = p
        enb, enk = max(p), min(p)
        if enb < 60 or enb > 245:            # siyah/beyaz sayılmaz
            continue
        if enb - enk < 40:                   # gri sayılmaz
            continue
        k = (r // 24, g // 24, b // 24)
        sayac[k] = sayac.get(k, 0) + 1
    if not sayac:
        return VARSAYILAN_VURGU
    k = max(sayac, key=sayac.get)
    return (k[0] * 24 + 12, k[1] * 24 + 12, k[2] * 24 + 12)


# --------------------------------------------------------------- çizim yardımcıları
def _kirp(im, en, boy):
    o = max(en / im.width, boy / im.height)
    im = im.resize((max(1, int(im.width * o)), max(1, int(im.height * o))), Image.LANCZOS)
    x = (im.width - en) // 2
    y = (im.height - boy) // 2
    return im.crop((x, y, x + en, y + boy))


def _sar(cizim, metin, font, genislik):
    kelimeler, satir, cikti = metin.split(), "", []
    for k in kelimeler:
        deneme = (satir + " " + k).strip()
        if cizim.textlength(deneme, font=font) <= genislik or not satir:
            satir = deneme
        else:
            cikti.append(satir); satir = k
    if satir:
        cikti.append(satir)
    return cikti


def _yuvarlak(cizim, kutu, r, dolgu):
    cizim.rounded_rectangle(kutu, radius=r, fill=dolgu)


# --------------------------------------------------------------- poster
def poster(hedef, firma, basliklar, gorsel=None, logo=None, vurgu=None,
           telefon=None, madde=(), tarih=None):
    """Düzeltilmiş hâlin 1080×1350 posteri. Üzerinde TASLAK yazar."""
    if not PIL_VAR:
        raise RuntimeError("Pillow kurulu değil.")
    vurgu = vurgu or VARSAYILAN_VURGU
    tarih = tarih or datetime.date.today().strftime("%d.%m.%Y")

    tuval = Image.new("RGB", (EN, BOY), INK)
    if gorsel and os.path.exists(gorsel):
        try:
            f = _kirp(Image.open(gorsel).convert("RGB"), EN, int(BOY * 0.62))
            f = ImageEnhance.Color(f).enhance(0.92)
            f = ImageEnhance.Brightness(f).enhance(0.86)
            tuval.paste(f, (0, 0))
            # alta doğru koyulaşan perde — yazı her zaman okunur kalsın
            perde = Image.new("L", (1, f.height))
            for y in range(f.height):
                t = y / max(1, f.height - 1)
                perde.putpixel((0, y), int(255 * min(1, (t ** 2) * 1.35)))
            perde = perde.resize((EN, f.height))
            tuval.paste(Image.new("RGB", (EN, f.height), INK), (0, 0), perde)
        except Exception:
            pass

    c = ImageDraw.Draw(tuval)
    f_kucuk = _font(False, 26)
    f_mono = _font(True, 22)
    f_bas = _font(True, 68)
    f_alt = _font(False, 30)
    f_dug = _font(True, 32)

    # --- üst: logo / firma adı
    ust = 54
    if logo and os.path.exists(logo):
        try:
            lg = Image.open(logo).convert("RGBA")
            o = 92 / max(1, lg.height)
            lg = lg.resize((max(1, int(lg.width * o)), 92), Image.LANCZOS)
            if lg.width > 460:
                lg = lg.crop((0, 0, 460, 92))
            tuval.paste(lg, (56, ust), lg)
        except Exception:
            c.text((56, ust + 24), firma[:34], font=_font(True, 40), fill=BONE)
    else:
        c.text((56, ust + 20), firma[:34], font=_font(True, 40), fill=BONE)

    # --- TASLAK rozeti
    rz = "ÖNİZLEME · TASLAK"
    w = c.textlength(rz, font=f_mono)
    _yuvarlak(c, (EN - 56 - w - 32, ust + 26, EN - 56, ust + 26 + 44), 4, vurgu)
    c.text((EN - 56 - w - 16, ust + 36), rz, font=f_mono, fill=(255, 255, 255))

    # --- başlık bloğu
    y = int(BOY * 0.44)
    for i, satir in enumerate(basliklar[:3]):
        for l in _sar(c, satir, f_bas, EN - 112)[:2]:
            c.text((56, y), l, font=f_bas, fill=BONE)
            y += 76
    y += 10

    # --- düğmeler (sitede eksik olan eylem çağrıları, yerine konmuş hâliyle)
    dy = y
    d1 = "Teklif Al"
    w1 = c.textlength(d1, font=f_dug) + 64
    _yuvarlak(c, (56, dy, 56 + w1, dy + 68), 4, vurgu)
    c.text((56 + 32, dy + 16), d1, font=f_dug, fill=(255, 255, 255))
    d2 = "WhatsApp"
    w2 = c.textlength(d2, font=f_dug) + 64
    c.rounded_rectangle((56 + w1 + 16, dy, 56 + w1 + 16 + w2, dy + 68), radius=4,
                        outline=BONE, width=2)
    c.text((56 + w1 + 16 + 32, dy + 16), d2, font=f_dug, fill=BONE)
    if telefon:
        c.text((56, dy + 92), "Tel: " + telefon, font=f_alt, fill=(210, 208, 202))
        dy += 40
    y = dy + 104

    # --- düzeltilenler şeridi
    c.line((56, y, EN - 56, y), fill=(70, 70, 74), width=1)
    y += 26
    for m in list(madde)[:4]:
        c.ellipse((58, y + 8, 74, y + 24), fill=vurgu)
        for l in _sar(c, m, f_alt, EN - 160)[:1]:
            c.text((92, y), l, font=f_alt, fill=(216, 214, 208))
        y += 46

    # --- alt künye
    c.line((56, BOY - 96, EN - 56, BOY - 96), fill=(70, 70, 74), width=1)
    c.text((56, BOY - 74), "LUNA YAPIM · lunayapim.com", font=f_mono, fill=GRI)
    sag = "%s · taslak" % tarih
    c.text((EN - 56 - c.textlength(sag, font=f_mono), BOY - 74), sag, font=f_mono, fill=GRI)

    tuval.save(hedef, "PNG")
    return hedef


# --------------------------------------------------------------- kısa film
def _kare_dizisi(gorseller, gecici, kare=90):
    """Her görsel için yavaş yaklaşan kareler üretir (Ken Burns)."""
    kd = os.path.join(gecici, "kare")
    os.makedirs(kd, exist_ok=True)
    n = 0
    for g in gorseller:
        try:
            im = Image.open(g).convert("RGB")
        except Exception:
            continue
        for i in range(kare):
            t = i / max(1, kare - 1)
            olcek = 1.06 + 0.10 * t
            en2, boy2 = int(EN * olcek), int(BOY * olcek)
            k = _kirp(im, en2, boy2)
            x = (en2 - EN) // 2
            y = int((boy2 - BOY) * (0.35 + 0.30 * t))
            kare_im = k.crop((x, y, x + EN, y + BOY))
            kare_im = ImageEnhance.Color(kare_im).enhance(0.94)
            n += 1
            kare_im.save(os.path.join(kd, "%04d.jpg" % n), quality=90)
    return kd, n


def film(hedef, gorseller, poster_yolu, klasor=None, sn_basi=2.4, fps=30):
    """Firmanın kendi görsellerinden ~8 sn dikey film. Kredi harcamaz.

    Ara dosyalar sistem geçici klasöründe tutulur; müşteri klasörüne yalnızca
    bitmiş mp4 yazılır."""
    kullan = [g for g in gorseller if os.path.exists(g)][:3]
    if not kullan:
        return None
    gecici = tempfile.mkdtemp(prefix="luna-onizleme-")
    try:
        kd, adet = _kare_dizisi(kullan, gecici, kare=int(sn_basi * fps))
        if not adet:
            return None
        kapanis = poster_yolu if (poster_yolu and os.path.exists(poster_yolu)) else None

        ara = os.path.join(gecici, "akis.mp4")
        subprocess.run(["ffmpeg", "-y", "-v", "error",
                        "-framerate", str(fps), "-i", os.path.join(kd, "%04d.jpg"),
                        "-vf", "format=yuv420p", "-c:v", "libx264", "-preset", "medium",
                        "-crf", "21", ara], check=True)

        parcalar = [ara]
        if kapanis:
            kap = os.path.join(gecici, "kapanis.mp4")
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-t", "1.8",
                            "-i", kapanis, "-vf",
                            "scale=%d:%d:force_original_aspect_ratio=increase,"
                            "crop=%d:%d,format=yuv420p" % (EN, BOY, EN, BOY),
                            "-r", str(fps), "-c:v", "libx264", "-preset", "medium",
                            "-crf", "21", kap], check=True)
            parcalar.append(kap)

        liste = os.path.join(gecici, "liste.txt")
        with open(liste, "w", encoding="utf-8") as f:
            for p in parcalar:
                f.write("file '%s'\n" % os.path.abspath(p))
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                        "-i", liste, "-c:v", "libx264", "-preset", "slow", "-crf", "23",
                        "-pix_fmt", "yuv420p", "-movflags", "+faststart", hedef],
                       check=True)
        return hedef
    finally:
        shutil.rmtree(gecici, ignore_errors=True)


# --------------------------------------------------------------- birleştirici
# Firma adı sol üstteki kilitte zaten var; başlıkta tekrar etmiyor.
BASLIK_KALIP = {
 "insaat-3d-modelleme": ["Proje bitmeden", "satılmaya başlar"],
 "emlak-video":         ["Mekânı gerçekten", "gezdirin"],
 "urun-animasyon":      ["Ürünün içini", "görünür kılın"],
 "drone-cekimi":        ["Yerden görünmeyeni", "gösterin"],
 "isletme-tanitim":     ["Bir çekim günü,", "bir aylık içerik"],
 "klip-cekimi":         ["Senaryolu,", "çok planlı çekim"],
 "dugun-cekimi":        ["Gün bir kez", "yaşanır"],
}

MADDE_KALIP = {
 "cta_yok": "Sayfaya net bir 'Teklif Al' düğmesi kondu",
 "whatsapp_yok": "WhatsApp butonu eklendi",
 "tel_tiklanmaz": "Telefon tek dokunuşla aranır hâle getirildi",
 "form_yok": "Mesai dışı için iletişim formu eklendi",
 "referans_yok": "Yapılmış işler bölümü açıldı",
 "video_yok": "Proje tanıtım videosu üretildi",
 "og_yok": "WhatsApp'ta paylaşılınca görsel çıkıyor",
 "harita_link_yok": "Yol tarifi bağlantısı eklendi",
 "yorum_gomulu_yok": "Müşteri görüşleri sayfaya taşındı",
 "fiyat_sinyali_yok": "Fiyat bandı görünür hâle getirildi",
}


def paket(firma, site, klasor, hizmet="insaat-3d-modelleme", eksik_kodlari=(),
          telefon=None):
    """
    Bir aday için önizleme paketini üretir.
    Döner: {"poster":…, "film":…, "kaynak":…, "not":[…]} — üretilemeyenler None.
    """
    os.makedirs(klasor, exist_ok=True)
    notlar = []
    if not PIL_VAR:
        return {"poster": None, "film": None, "kaynak": None,
                "not": ["Pillow kurulu değil — 'pip3 install pillow' gerekiyor."]}

    ham = os.path.join(klasor, "_malzeme")
    v = varliklar(site)
    if not v["ulasildi"]:
        notlar.append("Siteye ulaşılamadı (%s) — poster görselsiz üretildi." % site)
        gorseller, logo, defter = [], None, []
    else:
        gorseller, logo, defter = malzeme_indir(v, ham)
        if not gorseller:
            notlar.append("Sitede kullanılabilir çözünürlükte görsel bulunamadı — "
                          "poster görselsiz üretildi.")

    vurgu = vurgu_rengi(logo)
    basliklar = [x % firma if "%s" in x else x
                 for x in BASLIK_KALIP.get(hizmet, BASLIK_KALIP["insaat-3d-modelleme"])]
    maddeler = [MADDE_KALIP[k] for k in eksik_kodlari if k in MADDE_KALIP][:4]
    if not maddeler:
        maddeler = ["Net eylem çağrısı", "WhatsApp ve tıklanabilir telefon",
                    "Proje tanıtım videosu"]

    p_yol = os.path.join(klasor, "onizleme.png")
    poster(p_yol, firma, basliklar, gorseller[0] if gorseller else None, logo,
           vurgu, telefon or v.get("telefon"), maddeler)

    f_yol = None
    if gorseller:
        try:
            f_yol = film(os.path.join(klasor, "onizleme.mp4"), gorseller, p_yol, klasor)
        except Exception as ex:
            notlar.append("Film üretilemedi: %s" % ex)
    else:
        notlar.append("Görsel olmadığı için film üretilmedi.")

    k_yol = os.path.join(klasor, "onizleme-kaynak.md")
    with open(k_yol, "w", encoding="utf-8") as f:
        f.write("# Önizleme malzemesi — %s\n\n" % firma)
        f.write("Tarih: %s\n\n" % datetime.datetime.now().strftime("%d.%m.%Y %H:%M"))
        f.write("Bütün görseller firmanın kendi açık sitesinden alındı. "
                "Bu dosyalar yalnızca firmaya gönderilir, hiçbir yerde yayınlanmaz.\n\n")
        if defter:
            for ad, u in defter:
                f.write("- **%s** — %s\n" % (ad, u))
        else:
            f.write("- Görsel alınamadı.\n")
        if notlar:
            f.write("\n## Notlar\n")
            for n in notlar:
                f.write("- %s\n" % n)

    # --- teklife giren diğer görseller (site düzeni, sosyal düzen, aşama, kalite)
    alan = (site or "").replace("https://", "").replace("http://", "").strip("/").split("/")[0]
    ornek = _ornek_kare()
    set_ = {}
    try:
        set_ = gorsel_seti(klasor, firma, alan, hizmet, gorseller, logo, vurgu,
                           ornek_gorsel=ornek)
    except Exception as ex:
        notlar.append("Görsel seti üretilemedi: %s" % ex)

    d = {"poster": p_yol, "film": f_yol, "kaynak": k_yol, "not": notlar,
         "vurgu": "#%02X%02X%02X" % vurgu, "gorsel_adet": len(gorseller)}
    for ad in ("site", "sosyal", "asama", "kalite"):
        d["taslak_" + ad] = set_.get(ad)
        if set_.get(ad + "_hata"):
            notlar.append("%s taslağı: %s" % (ad, set_[ad + "_hata"]))
    d["gorseller"] = [x for x in (p_yol, d.get("taslak_site"), d.get("taslak_sosyal"),
                                  d.get("taslak_asama"), d.get("taslak_kalite"))
                      if x and os.path.exists(x)]
    return d


def _ornek_kare():
    """Kalite kartı için KENDİ teslimimizden gerçek bir kare bulur."""
    from .ayarlar import SITE_KOK as kok
    if not kok:
        return None
    # Kendi teslimimizden gerçek kareler — süs görseli değil, iş görseli.
    for aday in ("assets/video/ornek-cm.jpg", "assets/video/ornek-galzura.jpg",
                 "assets/video/insaat-3d-modelleme.jpg", "assets/video/luna-marka.jpg",
                 "assets/hero-poster.jpg"):
        y_ = os.path.join(kok, aday)
        if os.path.exists(y_):
            return y_
    return None


# ==================================================================
# TEKLİF GÖRSELLERİ — site taslağı, sosyal düzen, aşama şeması, kalite kartı
# Hepsi firmanın kendi malzemesiyle; hiçbiri kredi harcamıyor.
# ==================================================================

def _rozet(c, x, y, metin, vurgu, font):
    w = c.textlength(metin, font=font)
    c.rounded_rectangle((x, y, x + w + 30, y + 42), radius=4, fill=vurgu)
    c.text((x + 15, y + 9), metin, font=font, fill=(255, 255, 255))
    return w + 30


def _taslak_rozeti(c, font, vurgu):
    rz = "ÖNİZLEME · TASLAK"
    w = c.textlength(rz, font=font)
    c.rounded_rectangle((EN - 56 - w - 32, 56, EN - 56, 100), radius=4, fill=vurgu)
    c.text((EN - 56 - w - 16, 66), rz, font=font, fill=(255, 255, 255))


def site_taslagi(hedef, firma, alan, basliklar, gorsel=None, logo=None, vurgu=None):
    """Masaüstü + telefon çerçevesinde 'düzeltilmiş site' taslağı."""
    if not PIL_VAR:
        raise RuntimeError("Pillow kurulu değil.")
    vurgu = vurgu or VARSAYILAN_VURGU
    t = Image.new("RGB", (EN, BOY), (18, 18, 21))
    c = ImageDraw.Draw(t)
    f_mono = _font(True, 22)
    f_kucuk = _font(False, 24)
    f_bas = _font(True, 34)
    f_dug = _font(True, 20)
    f_baslik = _font(True, 30)

    c.text((56, 62), "Site düzeni", font=_font(True, 40), fill=BONE)
    c.text((56, 112), "eksikler yerine konmuş hâliyle", font=f_kucuk, fill=GRI)
    _taslak_rozeti(c, f_mono, vurgu)

    # --- masaüstü çerçeve
    mx, my, mw, mh = 56, 190, EN - 112, 560
    c.rounded_rectangle((mx, my, mx + mw, my + mh), radius=10, fill=(30, 30, 34))
    c.rounded_rectangle((mx, my, mx + mw, my + 44), radius=10, fill=(46, 46, 51))
    for i, renk in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        c.ellipse((mx + 18 + i * 24, my + 15, mx + 32 + i * 24, my + 29), fill=renk)
    c.rounded_rectangle((mx + 110, my + 11, mx + mw - 20, my + 33), radius=4, fill=(24, 24, 28))
    c.text((mx + 124, my + 15), (alan or "siteniz.com")[:46], font=_font(False, 17),
           fill=(150, 150, 156))

    ic = (mx + 2, my + 46, mx + mw - 2, my + mh - 2)
    ien, iboy = ic[2] - ic[0], ic[3] - ic[1]
    if gorsel and os.path.exists(gorsel):
        try:
            g = _kirp(Image.open(gorsel).convert("RGB"), ien, iboy)
            g = ImageEnhance.Brightness(g).enhance(0.62)
            t.paste(g, (ic[0], ic[1]))
        except Exception:
            c.rectangle(ic, fill=(20, 20, 24))
    else:
        c.rectangle(ic, fill=(20, 20, 24))

    # sayfa üst menüsü
    if logo and os.path.exists(logo):
        try:
            lg = Image.open(logo).convert("RGBA")
            o = 34 / max(1, lg.height)
            lg = lg.resize((max(1, int(lg.width * o)), 34), Image.LANCZOS)
            if lg.width > 200:
                lg = lg.crop((0, 0, 200, 34))
            t.paste(lg, (ic[0] + 26, ic[1] + 22), lg)
        except Exception:
            c.text((ic[0] + 26, ic[1] + 24), firma[:22], font=_font(True, 24), fill=BONE)
    else:
        c.text((ic[0] + 26, ic[1] + 24), firma[:22], font=_font(True, 24), fill=BONE)
    mx2 = ic[0] + 260
    for m in ("Projeler", "Hakkımızda", "İletişim"):
        c.text((mx2, ic[1] + 28), m, font=_font(False, 18), fill=(206, 204, 199))
        mx2 += int(c.textlength(m, font=_font(False, 18))) + 28
    _rozet(c, ic[2] - 150, ic[1] + 18, "Teklif Al", vurgu, f_dug)

    # sayfa başlığı + eylem
    by = ic[1] + iboy - 210
    for satir in basliklar[:2]:
        c.text((ic[0] + 26, by), satir, font=f_bas, fill=BONE)
        by += 42
    by += 14
    w1 = _rozet(c, ic[0] + 26, by, "Teklif Al", vurgu, f_dug)
    c.rounded_rectangle((ic[0] + 26 + w1 + 12, by, ic[0] + 26 + w1 + 12 + 150, by + 42),
                        radius=4, outline=BONE, width=2)
    c.text((ic[0] + 26 + w1 + 40, by + 9), "WhatsApp", font=f_dug, fill=BONE)

    # --- telefon çerçevesi (sağ altta bindirme)
    pw, ph = 250, 500
    px, py = EN - 56 - pw, my + mh - 190
    c.rounded_rectangle((px - 8, py - 8, px + pw + 8, py + ph + 8), radius=32, fill=(52, 52, 58))
    c.rounded_rectangle((px, py, px + pw, py + ph), radius=26, fill=(20, 20, 24))
    if gorsel and os.path.exists(gorsel):
        try:
            g2 = _kirp(Image.open(gorsel).convert("RGB"), pw, int(ph * 0.58))
            g2 = ImageEnhance.Brightness(g2).enhance(0.6)
            yuvarlak = Image.new("L", (pw, int(ph * 0.58)), 0)
            ImageDraw.Draw(yuvarlak).rounded_rectangle(
                (0, 0, pw, int(ph * 0.58)), radius=26, fill=255)
            t.paste(g2, (px, py), yuvarlak)
        except Exception:
            pass
    c.text((px + 18, py + 200), firma[:16], font=_font(True, 22), fill=BONE)
    for i, satir in enumerate(basliklar[:2]):
        c.text((px + 18, py + 236 + i * 26), satir[:22], font=_font(True, 20), fill=BONE)
    _rozet(c, px + 18, py + 300, "Teklif Al", vurgu, _font(True, 17))
    c.rounded_rectangle((px + 18, py + 352, px + pw - 18, py + 390), radius=4,
                        outline=BONE, width=2)
    c.text((px + 40, py + 361), "WhatsApp", font=_font(True, 17), fill=BONE)
    c.text((px + 18, py + 408), "Tel — tek dokunuş", font=_font(False, 16), fill=(190, 188, 182))

    # --- alt açıklama
    ay = my + mh + 40
    c.line((56, ay, EN - 56, ay), fill=(70, 70, 74), width=1)
    ay += 22
    for m in ("Masaüstü ve telefonda aynı düzen",
              "Teklif Al ve WhatsApp her ekranda görünür",
              "Telefon numarası tek dokunuşla aranıyor"):
        c.ellipse((58, ay + 9, 74, ay + 25), fill=vurgu)
        c.text((92, ay), m, font=_font(False, 27), fill=(214, 212, 206))
        ay += 44

    c.line((56, BOY - 96, EN - 56, BOY - 96), fill=(70, 70, 74), width=1)
    c.text((56, BOY - 74), "LUNA YAPIM · lunayapim.com", font=f_mono, fill=GRI)
    t.save(hedef, "PNG")
    return hedef


def sosyal_taslak(hedef, firma, gorseller, logo=None, vurgu=None, kullanici=None):
    """Instagram profil düzeni taslağı — 3×3 ızgara, tek görsel dil."""
    if not PIL_VAR:
        raise RuntimeError("Pillow kurulu değil.")
    vurgu = vurgu or VARSAYILAN_VURGU
    t = Image.new("RGB", (EN, BOY), (18, 18, 21))
    c = ImageDraw.Draw(t)
    f_mono = _font(True, 22)

    c.text((56, 62), "Sosyal medya düzeni", font=_font(True, 40), fill=BONE)
    c.text((56, 112), "tek görsel dil, tek renk paleti", font=_font(False, 24), fill=GRI)
    _taslak_rozeti(c, f_mono, vurgu)

    # profil başlığı
    py = 190
    c.ellipse((56, py, 56 + 116, py + 116), fill=(40, 40, 46))
    if logo and os.path.exists(logo):
        try:
            lg = Image.open(logo).convert("RGB")
            lg = _kirp(lg, 116, 116)
            maske = Image.new("L", (116, 116), 0)
            ImageDraw.Draw(maske).ellipse((0, 0, 116, 116), fill=255)
            t.paste(lg, (56, py), maske)
        except Exception:
            pass
    c.text((196, py + 8), (kullanici or firma)[:26], font=_font(True, 32), fill=BONE)
    c.text((196, py + 52), firma[:34], font=_font(False, 23), fill=(200, 198, 192))
    c.text((196, py + 84), "lunayapim.com bağlantısı burada", font=_font(False, 21), fill=vurgu)

    # 3×3 ızgara
    gy = py + 156
    bosluk = 6
    # ızgara alta taşmasın: yükseklikten de sınırla
    alt_pay = 3 * 42 + 70          # madde şeridi + künye
    yer = (BOY - 96 - alt_pay) - gy
    hucre = min((EN - 112 - bosluk * 2) // 3, (yer - bosluk * 2) // 3)
    izgara_en = hucre * 3 + bosluk * 2
    sol = (EN - izgara_en) // 2
    for i in range(9):
        sx = sol + (i % 3) * (hucre + bosluk)
        sy = gy + (i // 3) * (hucre + bosluk)
        g = gorseller[i % len(gorseller)] if gorseller else None
        if g and os.path.exists(g):
            try:
                im = _kirp(Image.open(g).convert("RGB"), hucre, hucre)
                # tek görsel dil: hepsine aynı hafif düzeltme
                im = ImageEnhance.Color(im).enhance(0.92)
                im = ImageEnhance.Brightness(im).enhance(0.94)
                t.paste(im, (sx, sy))
            except Exception:
                c.rectangle((sx, sy, sx + hucre, sy + hucre), fill=(34, 34, 38))
        else:
            c.rectangle((sx, sy, sx + hucre, sy + hucre), fill=(34, 34, 38))
        # her üçüncü karede yazı şeridi — düzenin tutarlı olduğu görünsün
        if i % 3 == 0:
            yh = 44
            c.rectangle((sx, sy + hucre - yh, sx + hucre, sy + hucre), fill=(0, 0, 0))
            c.rectangle((sx, sy + hucre - yh, sx + 4, sy + hucre), fill=vurgu)
            c.text((sx + 12, sy + hucre - yh + 13), ["PROJE", "ŞANTİYE", "TESLİM"][i // 3],
                   font=_font(True, 16), fill=BONE)

    ay = gy + hucre * 3 + bosluk * 2 + 28
    c.line((56, ay, EN - 56, ay), fill=(70, 70, 74), width=1)
    ay += 22
    for m in ("Ayda 10–12 içerik, tek çekim gününden",
              "Profil fotoğrafı, bio ve site bağlantısı düzenli",
              "Her gönderi aynı renk ve tipografiyle"):
        c.ellipse((58, ay + 9, 74, ay + 25), fill=vurgu)
        c.text((92, ay), m, font=_font(False, 26), fill=(214, 212, 206))
        ay += 42

    c.line((56, BOY - 96, EN - 56, BOY - 96), fill=(70, 70, 74), width=1)
    c.text((56, BOY - 74), "LUNA YAPIM · lunayapim.com", font=f_mono, fill=GRI)
    t.save(hedef, "PNG")
    return hedef


ASAMA = [
 ("01", "Keşif", "Mekânı ve projeyi görüyoruz; ne çekileceği yazılı çıkıyor."),
 ("02", "Plan", "Çekim listesi ve takvim onayınıza gidiyor."),
 ("03", "Çekim", "Ekip sahada. İzinler ve yedek gün bizde."),
 ("04", "Kurgu", "Renk, ses ve ritim; ilk kesim size geliyor."),
 ("05", "Teslim", "Yatay, kare ve dikey sürümler + ham kayıt."),
]


def asama_gorseli(hedef, firma, vurgu=None, sure_notu=None):
    """Sürecin beş aşaması — müşteri ne olacağını baştan görsün."""
    if not PIL_VAR:
        raise RuntimeError("Pillow kurulu değil.")
    vurgu = vurgu or VARSAYILAN_VURGU
    t = Image.new("RGB", (EN, BOY), (18, 18, 21))
    c = ImageDraw.Draw(t)
    f_mono = _font(True, 22)

    c.text((56, 62), "Nasıl ilerliyor", font=_font(True, 40), fill=BONE)
    c.text((56, 112), (sure_notu or "baştan sona beş aşama"), font=_font(False, 24), fill=GRI)
    _taslak_rozeti(c, f_mono, vurgu)

    y = 210
    f_no = _font(True, 30)
    f_ad = _font(True, 34)
    f_ac = _font(False, 25)
    for i, (no, ad, ac) in enumerate(ASAMA):
        c.ellipse((56, y, 56 + 62, y + 62), fill=vurgu)
        w = c.textlength(no, font=f_no)
        c.text((56 + 31 - w / 2, y + 15), no, font=f_no, fill=(255, 255, 255))
        if i < len(ASAMA) - 1:
            c.line((87, y + 66, 87, y + 168), fill=(70, 70, 74), width=2)
        c.text((150, y + 4), ad, font=f_ad, fill=BONE)
        for j, l in enumerate(_sar(c, ac, f_ac, EN - 210)[:2]):
            c.text((150, y + 46 + j * 32), l, font=f_ac, fill=(200, 198, 192))
        y += 172

    c.line((56, BOY - 96, EN - 56, BOY - 96), fill=(70, 70, 74), width=1)
    c.text((56, BOY - 74), "LUNA YAPIM · %s" % firma[:28], font=f_mono, fill=GRI)
    t.save(hedef, "PNG")
    return hedef


def kalite_karti(hedef, ornek_gorsel, vurgu=None, kunye=None):
    """Teslim kalitesini KENDİ işimizden bir kareyle gösterir — kıyas uydurmaz."""
    if not PIL_VAR:
        raise RuntimeError("Pillow kurulu değil.")
    if not (ornek_gorsel and os.path.exists(ornek_gorsel)):
        return None
    vurgu = vurgu or VARSAYILAN_VURGU
    t = Image.new("RGB", (EN, BOY), (18, 18, 21))
    c = ImageDraw.Draw(t)
    f_mono = _font(True, 22)

    ust = _kirp(Image.open(ornek_gorsel).convert("RGB"), EN, int(BOY * 0.60))
    t.paste(ust, (0, 0))
    perde = Image.new("L", (1, ust.height))
    for y in range(ust.height):
        v = y / max(1, ust.height - 1)
        perde.putpixel((0, y), int(255 * min(1, (v ** 3) * 1.6)))
    t.paste(Image.new("RGB", (EN, ust.height), (18, 18, 21)),
            (0, 0), perde.resize((EN, ust.height)))

    c.text((56, 62), "Teslim kalitesi", font=_font(True, 40), fill=BONE)
    rz = "BİZİM İŞİMİZ"
    w = c.textlength(rz, font=f_mono)
    c.rounded_rectangle((EN - 56 - w - 32, 62, EN - 56, 106), radius=4, fill=vurgu)
    c.text((EN - 56 - w - 16, 72), rz, font=f_mono, fill=(255, 255, 255))

    y = int(BOY * 0.60) + 26
    c.text((56, y), "Bu kare gerçek bir teslimimizden.", font=_font(True, 32), fill=BONE)
    y += 56
    for ad, deger in (kunye or [
            ("Çözünürlük", "8K render · 4K teslim"),
            ("Format", "yatay, kare ve dikey aynı üretimden"),
            ("Renk", "tek palet, tüm kesimlerde aynı"),
            ("Durgun kare", "baskı çözünürlüğünde ayrıca teslim")]):
        c.text((56, y), ad.upper(), font=_font(True, 19), fill=vurgu)
        for l in _sar(c, deger, _font(False, 27), EN - 130)[:2]:
            c.text((56, y + 28), l, font=_font(False, 27), fill=(214, 212, 206))
        y += 84

    c.line((56, BOY - 96, EN - 56, BOY - 96), fill=(70, 70, 74), width=1)
    c.text((56, BOY - 74), "LUNA YAPIM · lunayapim.com", font=f_mono, fill=GRI)
    t.save(hedef, "PNG")
    return hedef


def gorsel_seti(klasor, firma, alan, hizmet, gorseller, logo, vurgu,
                ornek_gorsel=None, kullanici=None):
    """Teklife giren tüm görselleri üretir. Üretilemeyen None kalır."""
    basliklar = BASLIK_KALIP.get(hizmet, BASLIK_KALIP["insaat-3d-modelleme"])
    cikti = {}
    try:
        cikti["site"] = site_taslagi(os.path.join(klasor, "taslak-site.png"), firma,
                                     alan, basliklar,
                                     gorseller[0] if gorseller else None, logo, vurgu)
    except Exception as ex:
        cikti["site"] = None; cikti["site_hata"] = str(ex)
    try:
        cikti["sosyal"] = sosyal_taslak(os.path.join(klasor, "taslak-sosyal.png"),
                                        firma, gorseller, logo, vurgu, kullanici)
    except Exception as ex:
        cikti["sosyal"] = None; cikti["sosyal_hata"] = str(ex)
    try:
        cikti["asama"] = asama_gorseli(os.path.join(klasor, "taslak-asama.png"),
                                       firma, vurgu)
    except Exception as ex:
        cikti["asama"] = None; cikti["asama_hata"] = str(ex)
    if ornek_gorsel:
        try:
            cikti["kalite"] = kalite_karti(os.path.join(klasor, "taslak-kalite.png"),
                                           ornek_gorsel, vurgu)
        except Exception as ex:
            cikti["kalite"] = None; cikti["kalite_hata"] = str(ex)
    return cikti
