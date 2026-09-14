# -*- coding: utf-8 -*-
"""
ARAMA HİZALAMA — il-hizmet sayfalarının başlık/H1/meta/fiyat bölümü, arayanın
gerçekten yazdığı kalıba çekilir. terimler.py kelime düzeyinde çalışır; bu modül
sayfa tipine göre tüm başlığı yeniden kurar ve eksik "fiyat" bölümünü ekler.

Kanıt (04.09.2026, Google otomatik tamamlama TR + Search Console 3 ay):
  "bursa drone çekimi", "bursa drone çekim fiyatları"         → drone sayfası
  "bursa tanıtım filmi çekimi", "bursa tanıtım videosu",
  "bursa reklam ajansı", "bursa reklam filmi" (az)            → işletme/tanıtım sayfası
  "bursa video çekimi", "bursa prodüksiyon şirketleri",
  "bursa video prodüksiyon"                                   → il ana sayfası
  "bursa ürün çekimi", "bursa ürün fotoğraf çekimi"            → ürün sayfası
  "bursa klip çekimi"                                          → klip (zaten uyumlu)
  "bursa 3d modelleme" → 3D yazıcı niyeti; "mimari görselleştirme" il'siz aranıyor
  "reklam çekimi" tek başına oyuncu/iş ilanı niyeti → hedeflenmez.
  Search Console: "ankara tanıtım filmi çekimi" 91., "antalya drone çekim" 52.,
  "kocaeli drone çekimi" 49. → sayfalar var ama 4–10. sayfada.

Kural: gövde metnine dokunulmaz (spun content yok). Yalnız title, h1, meta
description, og:title/description ve tek bir eklenen bölüm (fiyat bandı; fiyatlar.html
ile aynı rakamlar). İdempotent: ikinci çalıştırma hiçbir şeyi değiştirmez.
"""
import io, os, re, sys, html as H

# fiyatlar.html "Luna Yapım" sütunuyla aynı bantlar (31.08.2026 kararı)
FIYAT = {
    "drone-cekimi":     ("drone çekim fiyatları", "10.000 – 25.000 ₺", "yarım günlük çekim + kurgu; şantiye aylık takibi ve çok lokasyonlu işler ayrı fiyatlanır"),
    "isletme-tanitim":  ("tanıtım filmi fiyatları", "25.000 – 55.000 ₺", "kurumsal ve işletme tanıtım filmi: çekim + kurgu + renk + sosyal sürümler; reklam / marka filmi 35.000 – 100.000 ₺"),
    "klip-cekimi":      ("klip çekim fiyatları", "35.000 – 100.000 ₺", "senaryolu, çok planlı çekim; tek mekân ve tek günlük klipler alt banttan başlar"),
    "emlak-video":      ("emlak video çekim fiyatları", "2.500 – 12.000 ₺", "portföy başına tur videosu; mülk büyüklüğü, drone ve aylık paket belirler"),
    "urun-animasyon":   ("ürün animasyonu fiyatları", "40.000 – 95.000 ₺", "modelleme + animasyon + ses tasarımı; gerçek ürün çekimi işletme paketinde"),
    "insaat-3d-modelleme": ("3D render fiyatları", "45.000 – 150.000 ₺", "tek blok için render seti + kısa animasyon; blok sayısı ve ışık senaryosu belirler"),
    "dugun-cekimi":     None,
}

def _kisa(x, azami=68):
    if len(x) <= azami:
        return x
    y = x[:azami].rsplit(" ", 1)[0].rstrip(" —-–|:,")
    return y

def _desc(x, alt=110, ust=150):
    x = x.strip()
    if len(x) > ust:
        x = x[:ust].rsplit(" ", 1)[0].rstrip(",;:—-") + "…"
    return x

def _il_verisi():
    kok = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    yol = os.path.join(kok, "site-uretici")
    if yol not in sys.path:
        sys.path.insert(0, yol)
    from sehirler import SEHIRLER
    return {c["slug"]: c for c in SEHIRLER}

def _ilceler(c, n=3):
    return ", ".join(c.get("ilceler", [])[:n])

# ---- sayfa tipine göre başlık kurgusu ---------------------------------------
def _kurgu(tur, c):
    ad, ek, icin = c["ad"], c["ek"], c.get("icin", "'a")
    il3 = _ilceler(c)
    if tur == "genel":
        return dict(
            title=_kisa("%s Video Çekimi ve Prodüksiyon Şirketi | Luna Yapım" % ad),
            h1="%s%s <i>video çekimi</i> ve prodüksiyon" % (ad, ek),
            desc=_desc("%s%s video çekimi ve prodüksiyon: tanıtım filmi, drone çekimi, klip, emlak videosu, 3D render ve ürün animasyonu. %s ve tüm ilçeler. Aynı gün teklif." % (ad, ek, il3)))
    if tur == "isletme-tanitim":
        return dict(
            title=_kisa("%s Tanıtım Filmi Çekimi ve Reklam Filmi | Luna Yapım" % ad),
            h1="%s%s <i>tanıtım filmi</i> çekimi" % (ad, ek),
            desc=_desc("%s%s tanıtım filmi çekimi: kurumsal tanıtım filmi, işletme reklam filmi, aylık Reels paketi ve ürün çekimi. %s ve tüm ilçeler. Fiyat bandı sayfada." % (ad, ek, il3)))
    if tur == "urun-animasyon":
        return dict(
            title=_kisa("%s Ürün Çekimi ve 3D Ürün Animasyonu | Luna Yapım" % ad),
            h1="%s%s <i>ürün çekimi</i> ve 3D ürün animasyonu" % (ad, ek),
            desc=_desc("%s%s ürün çekimi ve 3D ürün animasyonu: makine çalışma prensibi, kesit anlatım, montaj ve üretim hattı videosu; fuar ve ihracat için çok dilli sürüm. %s." % (ad, ek, il3)))
    if tur == "drone-cekimi":
        return dict(
            title=None, h1=None,
            desc=_desc("%s%s drone çekimi ve drone çekim fiyatları: şantiye, arsa, tesis, otel ve etkinlik için havadan 4K görüntü, FPV tek plan mekân turu. %s ve tüm ilçeler." % (ad, ek, il3)))
    return None

# ---- html alanları ------------------------------------------------------------
R_TITLE = re.compile(r"<title>(.*?)</title>", re.S)
R_H1 = re.compile(r"(<h1[^>]*>)(.*?)(</h1>)", re.S)
R_DESC = re.compile(r'(<meta name="description" content=")(.*?)(")', re.S)
R_OGT = re.compile(r'(<meta property="og:title" content=")(.*?)(")', re.S)
R_OGD = re.compile(r'(<meta property="og:description" content=")(.*?)(")', re.S)
R_SSS = re.compile(r'(<h2>[^<]*—\s*sık sorulan sorular</h2>)', re.I)
ISARET = "<!-- arama:fiyat -->"

def _fiyat_blok(tur, c):
    f = FIYAT.get(tur)
    if not f:
        return ""
    etiket, bant, not_ = f
    ad, ek = c["ad"], c["ek"]
    return (ISARET + '\n<h2 id="fiyat">%s %s</h2>\n'
            '<p>%s%s %s: <strong>%s</strong> — %s. Rakamlar <a href="../fiyatlar">fiyat sayfamızdaki</a> bantla aynı; '
            'işi anlattığınızda aynı gün net bir aralık veriyoruz, sürpriz kalem çıkarmıyoruz.</p>\n'
            % (H.escape(ad), H.escape(etiket), H.escape(ad), ek, H.escape(etiket), bant, H.escape(not_)))

def hizala(s, tur, c):
    d = 0
    k = _kurgu(tur, c)
    if k:
        if k.get("title"):
            t = H.escape(k["title"], quote=False)
            if R_TITLE.search(s) and R_TITLE.search(s).group(1) != t:
                s = R_TITLE.sub("<title>%s</title>" % t, s, count=1); d += 1
            if R_OGT.search(s) and R_OGT.search(s).group(2) != H.escape(k["title"]):
                s = R_OGT.sub(lambda m: m.group(1) + H.escape(k["title"]) + m.group(3), s, count=1); d += 1
        if k.get("h1"):
            m = R_H1.search(s)
            if m and m.group(2).strip() != k["h1"]:
                s = s[:m.start(2)] + k["h1"] + s[m.end(2):]; d += 1
        if k.get("desc"):
            t = H.escape(k["desc"])
            for R in (R_DESC, R_OGD):
                m = R.search(s)
                if m and m.group(2) != t:
                    s = R.sub(lambda mm: mm.group(1) + t + mm.group(3), s, count=1); d += 1
    # fiyat bölümü: SSS başlığının hemen önüne, bir kez
    if tur in FIYAT and FIYAT[tur] and ISARET not in s:
        m = R_SSS.search(s)
        if m:
            s = s[:m.start()] + _fiyat_blok(tur, c) + "\n    " + s[m.start():]; d += 1
    return s, d

TURLER = ("drone-cekimi", "isletme-tanitim", "urun-animasyon", "klip-cekimi", "emlak-video", "insaat-3d-modelleme", "dugun-cekimi")

def calistir(kok):
    iller = _il_verisi()
    dz = os.path.join(kok, "sehir")
    sayfa = degisim = 0
    for f in sorted(os.listdir(dz)):
        if not f.endswith(".html") or f == "index.html":
            continue
        ad = f[:-5]
        tur, slug = "genel", ad
        for t in TURLER:
            if ad.endswith("-" + t):
                tur, slug = t, ad[:-(len(t) + 1)]
                break
        c = iller.get(slug)
        if not c:
            continue
        yol = os.path.join(dz, f)
        s = io.open(yol, encoding="utf-8").read()
        s2, d = hizala(s, tur, c)
        if d:
            io.open(yol, "w", encoding="utf-8").write(s2)
            sayfa += 1; degisim += d
    # ana hizmet sayfası: arayan "tanıtım filmi çekimi" diyor
    y = os.path.join(kok, "hizmetler", "isletme-tanitim.html")
    if os.path.exists(y):
        s = io.open(y, encoding="utf-8").read()
        t = "Tanıtım Filmi Çekimi — Kurumsal ve İşletme Tanıtım Filmi | Luna Yapım"
        if R_TITLE.search(s) and R_TITLE.search(s).group(1) != t:
            s = R_TITLE.sub("<title>%s</title>" % t, s, count=1)
            s = R_OGT.sub(lambda m: m.group(1) + H.escape(t) + m.group(3), s, count=1)
            io.open(y, "w", encoding="utf-8").write(s); sayfa += 1; degisim += 1
    return {"sayfa": sayfa, "degisen_alan": degisim}

if __name__ == "__main__":
    from .ayarlar import SITE_KOK
    print(calistir(SITE_KOK))
