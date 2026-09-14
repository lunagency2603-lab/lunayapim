# -*- coding: utf-8 -*-
"""
YAYIN — gündem taslağını siteye SEO uyumlu blog sayfası olarak koyar.

Yeni bir şablon yazmıyoruz. Sitenin kendi üreticisini (site-uretici/blog.py)
çağırıyoruz; böylece başlık hiyerarşisi, canonical, OG etiketleri, Article +
FAQPage + BreadcrumbList şemaları ve alt bilgi diğer 326 sayfayla birebir aynı
kalıyor. Tek şablon, tek doğru.

Akış:
  1. Gündem sekmesinde taslak çıkıyor      → cikti/gundem/*.md
  2. Metni sen yazıyorsun (iskelet hazır)
  3. "Yayınla" düğmesi                     → blog/<dosya>.html + blog/index.html + sitemap.xml
  4. IndexNow bildirimi                    → yeni adres arama motorlarına duyuruluyor

Yayınlanan yazıların kaydı site-uretici/yazilar.json'da tutuluyor; blog indeksi
her yayında bu kayıttan yeniden üretiliyor, hiçbir yazı kaybolmuyor.
"""
import os, re, sys, json, html, datetime, importlib

from .ayarlar import SITE_KOK

URETICI = os.path.join(os.path.dirname(SITE_KOK.rstrip("/")), "")  # yer tutucu, aşağıda çözülüyor


def _uretici_yolu():
    """site-uretici klasörünü bulur (pusula ile aynı proje içinde)."""
    kok = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    y = os.path.join(kok, "site-uretici")
    return y if os.path.isdir(y) else None


def _modul():
    """site-uretici/blog.py'yi içe aktarır (sys.path'e ekleyerek)."""
    y = _uretici_yolu()
    if not y:
        raise RuntimeError("site-uretici klasörü bulunamadı.")
    if y not in sys.path:
        sys.path.insert(0, y)
    for ad in ("uretici", "kabuk", "blog"):
        if ad in sys.modules:
            importlib.reload(sys.modules[ad])
    import blog as B
    return B


KAYIT = lambda: os.path.join(_uretici_yolu() or ".", "yazilar.json")


# ------------------------------------------------------------------ kayıt defteri
def kayitlar():
    """Yayındaki tüm yazılar. Dosya yoksa blog klasöründen bir kere kurar."""
    y = KAYIT()
    if os.path.isfile(y):
        try:
            with open(y, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    # ilk kurulum: diskteki yazılardan künye çıkar
    liste = []
    blog = os.path.join(SITE_KOK, "blog")
    if os.path.isdir(blog):
        for d in sorted(os.listdir(blog)):
            if not d.endswith(".html") or d == "index.html":
                continue
            g = open(os.path.join(blog, d), encoding="utf-8").read()
            b = re.search(r"<h1[^>]*>(.*?)</h1>", g, re.S)
            o = re.search(r'<p class="lede">(.*?)</p>', g, re.S)
            t = re.search(r'"datePublished"\s*:\s*"([^"]+)"', g)
            liste.append({
                "dosya": d,
                "baslik": html.unescape(re.sub(r"<[^>]+>", "", b.group(1)).strip()) if b else d,
                "ozet": html.unescape(re.sub(r"<[^>]+>", "", o.group(1)).strip()) if o else "",
                "tarih": t.group(1) if t else "2026-01-01",
            })
    kaydet(liste)
    return liste


def kaydet(liste):
    y = KAYIT()
    os.makedirs(os.path.dirname(y), exist_ok=True)
    with open(y, "w", encoding="utf-8") as f:
        json.dump(liste, f, ensure_ascii=False, indent=1)


# ------------------------------------------------------------------ markdown → yazı
YER_TUTUCU_IZ = ("iki paragraf", "somut, uygulanabilir", "tek paragraf",
                 "haber sadece kapı", "uydurma rakam yok", "üç soru yaz")


_TR_KUCUK = str.maketrans({"İ": "i", "I": "ı", "Ğ": "ğ", "Ü": "ü", "Ş": "ş", "Ö": "ö", "Ç": "ç"})


def _kucuk(x):
    return (x or "").translate(_TR_KUCUK).lower()


def _kunye_bul(kunye, *izler):
    """Künye anahtarını parça eşleşmesiyle bulur — noktalı İ sorununa takılmaz."""
    for k, v in kunye.items():
        for iz in izler:
            if iz in k:
                return v
    return ""


def _slug(x):
    TR = str.maketrans({"ı": "i", "İ": "i", "I": "i", "ğ": "g", "Ğ": "g", "ş": "s", "Ş": "s",
                        "ö": "o", "Ö": "o", "ü": "u", "Ü": "u", "ç": "c", "Ç": "c",
                        "â": "a", "î": "i", "û": "u"})
    d = x.translate(TR).encode("ascii", "ignore").decode().lower()
    return re.sub(r"-{2,}", "-", re.sub(r"[^a-z0-9]+", "-", d)).strip("-")[:70]


def _paragrafla(metin):
    """Düz metni <p> bloklarına çevirir; listeyi <ul> yapar."""
    parcalar, tampon, madde = [], [], []

    def bosalt():
        if tampon:
            parcalar.append("<p>%s</p>" % html.escape(" ".join(tampon), quote=False))
            tampon.clear()

    def bosalt_madde():
        if madde:
            parcalar.append("<ul>%s</ul>" % "".join(
                "<li>%s</li>" % html.escape(m, quote=False) for m in madde))
            madde.clear()

    for satir in metin.splitlines():
        s = satir.strip()
        if not s:
            bosalt(); bosalt_madde(); continue
        if s.startswith(("- ", "* ", "• ")):
            bosalt(); madde.append(s[2:].strip()); continue
        if re.match(r"^\d+[\.\)]\s", s):
            bosalt(); madde.append(re.sub(r"^\d+[\.\)]\s*", "", s)); continue
        bosalt_madde(); tampon.append(s)
    bosalt(); bosalt_madde()
    # **kalın** ve [bağlantı](adres) desteği
    cikti = "\n    ".join(parcalar)
    cikti = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", cikti)
    cikti = re.sub(r"\[([^\]]+)\]\((https?://[^\s)]+)\)",
                   r'<a href="\2" target="_blank" rel="noopener">\1</a>', cikti)
    # Site içi bağlantı: aynı sekmede açılır, rel eklenmez.
    cikti = re.sub(r"\[([^\]]+)\]\(((?:\.\./|\./|/)[^\s)]*)\)", r'<a href="\2">\1</a>', cikti)
    return cikti or "<p></p>"


def md_coz(metin):
    """
    Gündem taslağı markdown'ını blog üreticisinin beklediği sözlüğe çevirir.
    Döner: (yazi, uyarilar)
    """
    satirlar = metin.splitlines()
    baslik = next((s[2:].strip() for s in satirlar if s.startswith("# ")), "")
    uyari = []

    # üstteki künye satırları (Tetikleyen haber / Neden bu yazı / hizmet sayfası)
    kunye = {}
    for s in satirlar:
        m = re.match(r"\*\*(.+?):\*\*\s*(.+)", s.strip())
        if m:
            kunye[_kucuk(m.group(1).strip())] = m.group(2).strip()

    # bölümler
    bolumler, sss = [], []
    su_an, tampon, sss_modu = None, [], False
    for s in satirlar:
        if s.startswith("## "):
            if su_an and not sss_modu:
                bolumler.append((su_an, "\n".join(tampon)))
            su_an = s[3:].strip()
            sss_modu = "sık sorulan" in su_an.lower()
            tampon = []
            continue
        if s.startswith("### ") or s.startswith("---"):
            if su_an and not sss_modu:
                bolumler.append((su_an, "\n".join(tampon)))
            su_an, tampon = None, []
            continue
        if su_an is not None:
            tampon.append(s)
    if su_an and not sss_modu:
        bolumler.append((su_an, "\n".join(tampon)))
    elif su_an and sss_modu:
        # SSS bölümü: "**Soru?**" satırı + altındaki cevap
        soru, cevap = None, []
        for s in tampon:
            t = s.strip()
            if not t:
                continue
            m = re.match(r"\*\*(.+?)\*\*\s*$", t) or re.match(r"^[-*]\s*\*\*(.+?)\*\*\s*$", t)
            if m or t.endswith("?"):
                if soru:
                    sss.append((soru, " ".join(cevap).strip() or "—"))
                soru = (m.group(1) if m else t).strip().lstrip("-*• ").strip()
                cevap = []
            elif soru:
                cevap.append(t.lstrip("> ").strip())
        if soru:
            sss.append((soru, " ".join(cevap).strip() or "—"))

    # yer tutucu (henüz doldurulmamış) bölümleri ayıkla
    temiz = []
    for b, ic in bolumler:
        duz = re.sub(r"[>\s]+", " ", ic).strip().lower()
        if not duz:
            uyari.append("'%s' bölümü boş — yayına girmedi." % b)
            continue
        if any(iz in duz for iz in YER_TUTUCU_IZ):
            uyari.append("'%s' bölümünde hâlâ taslak notu var — yayına girmedi." % b)
            continue
        temiz.append((b, _paragrafla(re.sub(r"^>\s?", "", ic, flags=re.M))))

    if not sss:
        uyari.append("SSS bölümü boş — FAQ şeması eklenmedi. Aramada soru kutusuna "
                     "çıkma şansını kaçırıyorsun.")
    sss = [(q, a) for q, a in sss if a and a != "—" and "üç soru yaz" not in a.lower()]

    ozet = ""
    for b, ic in temiz:
        duz = re.sub(r"<[^>]+>", " ", ic)
        ozet = re.sub(r"\s+", " ", duz).strip()
        if len(ozet) > 60:
            break
    ozet = (ozet[:157] + "…") if len(ozet) > 158 else ozet

    yazi = {
        "dosya": _slug(baslik) + ".html",
        "baslik": baslik,
        "tarih": datetime.date.today().strftime("%Y-%m-%d"),
        "ozet": ozet or _kunye_bul(kunye, "neden bu")[:158],
        "anahtar": "",
        "bolumler": temiz,
        "sss": sss,
        "kaynak_haber": _kunye_bul(kunye, "tetikleyen"),
        "hizmet_sayfa": _kunye_bul(kunye, "hizmet sayfa").strip("` "),
        "il": _kunye_bul(kunye, "yerel bağ").split("—")[0].split(" geçiyor")[0].strip(),
    }
    if not baslik:
        uyari.append("Başlık bulunamadı — dosyanın ilk satırı '# Başlık' olmalı.")
    if len(temiz) < 2:
        uyari.append("En az iki dolu bölüm gerekiyor; şu an %d." % len(temiz))
    return yazi, uyari


# Hizmet sayfasına göre çekirdek anahtar kelimeler — başlık kelimeleri tek başına
# arama terimi değildir; asıl aranan kelimeler bunlar.
CEKIRDEK = {
 "insaat-3d-modelleme": ("inşaat 3d modelleme", "mimari görselleştirme",
                         "proje tanıtım animasyonu", "3d render", "kentsel dönüşüm görselleştirme"),
 "emlak-kurumsal": ("emlak videosu", "ilan videosu", "gayrimenkul tanıtım",
                    "portföy tanıtımı", "sanal tur"),
 "urun-animasyon": ("ürün animasyonu", "3d ürün tanıtımı", "makine animasyonu",
                    "fuar videosu", "süreç anlatım animasyonu"),
 "klip-cekimi": ("klip çekimi", "müzik klibi", "marka klibi"),
 "drone-fpv": ("drone çekimi", "fpv çekim", "havadan çekim"),
 "dugun-etkinlik": ("düğün çekimi", "etkinlik çekimi"),
 "isletme-tanitim": ("işletme tanıtım videosu", "sosyal medya içerik üretimi",
                     "yerel işletme pazarlama"),
}
GEREKSIZ = ("nedir", "nasıl", "neden", "hangi", "için", "olur", "oluyor", "yapmalı",
            "asıl", "mesele", "şimdi", "nerede", "varız", "neye", "biliyor", "değişir")


def anahtar_uret(yazi, ek=()):
    """Anahtar kelime satırı: hizmet çekirdeği + başlıktan çıkan anlamlı kelimeler."""
    tohum = list(ek)
    sayfa = (yazi.get("hizmet_sayfa") or "")
    for anahtar, kelimeler in CEKIRDEK.items():
        if anahtar in sayfa:
            tohum = list(kelimeler) + tohum
            break
    if yazi.get("il"):
        tohum = ["%s %s" % (yazi["il"].lower(), tohum[0]) if tohum else yazi["il"].lower()] + tohum
    kelimeler = []
    for kaynak in [yazi["baslik"]] + [b for b, _ in yazi["bolumler"]]:
        for k in re.split(r"[^\wçğıöşüÇĞİÖŞÜ]+", kaynak.lower()):
            if len(k) > 3 and k not in kelimeler:
                kelimeler.append(k)
    kelimeler = [k for k in kelimeler if k not in GEREKSIZ]
    # tohumda zaten geçen tekil kelimeleri tekrar etme
    tohum_metin = " ".join(tohum).lower()
    kelimeler = [k for k in kelimeler if k not in tohum_metin]
    return ", ".join((tohum + kelimeler)[:12])


# ------------------------------------------------------------------ yayınlama
def yayinla(yazi, sitemap=True):
    """Yazıyı siteye basar, blog indeksini ve sitemap'i günceller."""
    B = _modul()
    if not yazi.get("anahtar"):
        yazi["anahtar"] = anahtar_uret(yazi)

    adi, icerik = B.yazi_uret(yazi)
    blog = os.path.join(SITE_KOK, "blog")
    os.makedirs(blog, exist_ok=True)
    yol = os.path.join(blog, adi)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(icerik)

    # kayıt defterini güncelle
    liste = [k for k in kayitlar() if k["dosya"] != adi]
    liste.append({k: yazi[k] for k in ("dosya", "baslik", "tarih", "ozet")})
    liste.sort(key=lambda m: m["tarih"], reverse=True)
    kaydet(liste)

    # blog indeksi
    iadi, iicerik = B.indeks_uret(liste)
    with open(os.path.join(blog, iadi), "w", encoding="utf-8") as f:
        f.write(iicerik)

    # Cloudflare Pages .html uzantısını 301 ile kesiyor — adres uzantısız veriliyor
    adresler = ["https://lunayapim.com/blog/%s" % adi[:-5] if adi.endswith(".html") else
                "https://lunayapim.com/blog/%s" % adi, "https://lunayapim.com/blog/"]
    if sitemap:
        sitemap_guncelle(adresler)
    return {"dosya": adi, "yol": yol, "url": adresler[0],
            "yazi_sayisi": len(liste), "adresler": adresler}


def sitemap_guncelle(adresler):
    """Yeni adresleri sitemap.xml'e ekler / lastmod'unu bugüne çeker."""
    yol = os.path.join(SITE_KOK, "sitemap.xml")
    if not os.path.isfile(yol):
        return False
    g = open(yol, encoding="utf-8").read()
    bugun = datetime.date.today().strftime("%Y-%m-%d")
    for u in adresler:
        if "<loc>%s</loc>" % u in g:
            g = re.sub(r"(<loc>%s</loc><lastmod>)[^<]+(</lastmod>)" % re.escape(u),
                       r"\g<1>%s\g<2>" % bugun, g)
        else:
            satir = ('  <url><loc>%s</loc><lastmod>%s</lastmod>'
                     '<changefreq>monthly</changefreq><priority>0.6</priority></url>\n'
                     % (u, bugun))
            g = g.replace("</urlset>", satir + "</urlset>")
    open(yol, "w", encoding="utf-8").write(g)
    return True


def sitemap_sil(adresler):
    """Yayından kaldırılan adresleri sitemap'ten çıkarır."""
    yol = os.path.join(SITE_KOK, "sitemap.xml")
    if not os.path.isfile(yol):
        return 0
    g = open(yol, encoding="utf-8").read()
    n = 0
    for u in adresler:
        yeni_g = re.sub(r"<url>\s*<loc>%s</loc>.*?</url>" % re.escape(u), "", g, flags=re.S)
        if yeni_g != g:
            n += 1
            g = yeni_g
    if n:
        with open(yol, "w", encoding="utf-8") as f:
            f.write(g)
    return n


def taslak_listesi(klasor):
    """cikti/gundem altındaki taslaklar."""
    if not os.path.isdir(klasor):
        return []
    cikti = []
    for d in sorted(os.listdir(klasor), reverse=True):
        if not d.endswith(".md"):
            continue
        t = os.path.join(klasor, d)
        metin = open(t, encoding="utf-8").read()
        yazi, uyari = md_coz(metin)
        cikti.append({"dosya": d, "yol": t, "baslik": yazi["baslik"],
                      "dolu_bolum": len(yazi["bolumler"]), "sss": len(yazi["sss"]),
                      "uyari": uyari, "hazir": not uyari,
                      "boyut": os.path.getsize(t)})
    return cikti


# ------------------------------------------------------------------ ölçüm kimlikleri
def olcum_oku():
    """assets/olcum.js içindeki GA4 ve Cloudflare değerlerini okur."""
    y = os.path.join(SITE_KOK, "assets", "olcum.js")
    if not os.path.isfile(y):
        return {"var": False, "ga4": "", "cloudflare": ""}
    g = open(y, encoding="utf-8").read()
    def al(ad):
        m = re.search(r'%s\s*:\s*"([^"]*)"' % ad, g)
        return m.group(1) if m else ""
    return {"var": True, "ga4": al("ga4"), "cloudflare": al("cloudflare"), "yol": y}


def olcum_yaz(ga4="", cloudflare=""):
    """
    Ölçüm kimliklerini assets/olcum.js'e yazar. Kullanıcı dosya düzenlemiyor.
    Biçim doğrulaması yapılıyor — yanlış değer sessizce yazılmıyor.
    """
    y = os.path.join(SITE_KOK, "assets", "olcum.js")
    if not os.path.isfile(y):
        return {"hata": "assets/olcum.js bulunamadı: %s" % y}
    ga4 = (ga4 or "").strip()
    cf = (cloudflare or "").strip()
    uyari = []
    if ga4 and not re.fullmatch(r"G-[A-Z0-9]{6,12}", ga4):
        return {"hata": "GA4 ölçüm kimliği 'G-' ile başlamalı ve büyük harf/rakam olmalı. "
                        "Girdiğin: %r" % ga4}
    if cf and not re.fullmatch(r"[a-f0-9]{20,64}", cf):
        uyari.append("Cloudflare token'ı beklenen biçimde değil (uzun bir onaltılık dizi "
                     "olmalı). Yine de yazıldı; çalışmazsa değeri kontrol et.")
    g = open(y, encoding="utf-8").read()
    g = re.sub(r'(ga4\s*:\s*")[^"]*(")', lambda m: m.group(1) + ga4 + m.group(2), g, count=1)
    g = re.sub(r'(cloudflare\s*:\s*")[^"]*(")', lambda m: m.group(1) + cf + m.group(2), g, count=1)
    open(y, "w", encoding="utf-8").write(g)
    return {"ok": True, "ga4": ga4, "cloudflare": cf, "uyari": uyari,
            "not": ("Yazıldı. Ölçümün başlaması için siteyi yayınlaman gerekiyor."
                    if (ga4 or cf) else "Alanlar boşaltıldı — hiçbir ölçüm scripti yüklenmeyecek.")}
