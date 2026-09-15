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
# 16.09.2026 CTR REVİZYONU. Teşhis: ilk 10'da olduğumuz 22 sayfa SIFIR tık alıyordu
# (ör. /sehir/tekirdag-emlak-video: 31 gösterim, 8,5. sıra, 0 tık). Sebepleri ölçtük:
#   1. Açıklamada RAKAM yok. Oysa 28 sorgunun 6'sı (%21) doğrudan "fiyat"/"ne kadara"
#      içeriyor — arayanın ilk sorusu bu ve sonuçta cevabı göremiyordu.
#   2. Klip sayfalarının açıklaması 16 ilde BİREBİR aynıydı; sonuçlar ayırt edilemiyordu.
#   3. Açıklamalar ilçe listesinin ortasında "…" ile kesiliyordu (yarım cümle).
# Çözüm: fiyat bandı başlığa ve açıklamaya, her ile kendi ilçeleri/mekânı, kırpma yok —
# açıklama parça parça kurulur ve sınırı aşacaksa parça EKLENMEZ (cümle bölünmez).

# (arama terimi, başlık kancası, açıklamada geçen kapsam)
ARAMA = {
    "genel":               ("video çekimi ve prodüksiyon", None,
                            "tanıtım filmi, drone çekimi, klip, emlak videosu ve 3D render"),
    "drone-cekimi":        ("drone çekimi", "10.000 ₺'den",
                            "şantiye, arsa, tesis ve etkinlik için havadan 4K görüntü"),
    "klip-cekimi":         ("klip çekimi", "35.000 ₺'den",
                            "senaryo, sinematografi ve FPV drone tek elden"),
    "emlak-video":         ("emlak videosu", "2.500 ₺'den",
                            "villa, daire ve konut projesi için drone destekli ilan videosu"),
    "insaat-3d-modelleme": ("3D render", "45.000 ₺'den",
                            "mimari render, proje animasyonu ve iç mekân görselleştirme"),
    "urun-animasyon":      ("ürün animasyonu", "40.000 ₺'den",
                            "çalışma prensibi, kesit anlatım ve üretim hattı videosu"),
    "isletme-tanitim":     ("tanıtım filmi", "25.000 ₺'den",
                            "kurumsal tanıtım filmi, aylık Reels paketi ve ürün çekimi"),
    "dugun-cekimi":        ("düğün çekimi", "aynı gün teaser",
                            "nişan, kına ve düğün için sinematik kısa film, dış çekim ve drone"),
}

BASLIK_AZAMI = 68        # denetçi sınırı 70
ACIKLAMA_AZAMI = 158     # denetçi sınırı 165; kırpma yerine parça atlıyoruz


def _mekan(c, n=2):
    m = [x.strip() for x in (c.get("mekan") or "").split(",") if x.strip()]
    return ", ".join(m[:n])


def _ekle(parcalar, aday, sinir=ACIKLAMA_AZAMI):
    """Cümleyi ancak sınıra sığıyorsa ekler — yarım cümle bırakmaz."""
    deneme = " ".join(parcalar + [aday])
    return parcalar + [aday] if len(deneme) <= sinir else parcalar


def _kurgu(tur, c):
    ad, ek = c["ad"], c["ek"]
    il3 = _ilceler(c)
    a = ARAMA.get(tur)
    if not a:
        return None
    terim, kanca, kapsam = a

    # --- başlık: arayanın yazdığı terim + fiyat kancası, marka sonda
    if tur == "genel":
        title = "%s Video Çekimi ve Prodüksiyon Şirketi | Luna Yapım" % ad
    elif kanca and kanca.endswith("'den"):
        title = "%s %s Fiyatları — %s | Luna Yapım" % (ad, terim.title(), kanca)
    else:
        title = "%s Düğün Çekimi — Aynı Gün Teaser | Luna Yapım" % ad
    title = _kisa(title, BASLIK_AZAMI)

    # --- H1: sayfanın kendi vaadi (başlıkla aynı olmasın)
    h1 = "%s%s <i>%s</i>" % (ad, ek, terim) if tur != "genel" else \
         "%s%s <i>video çekimi</i> ve prodüksiyon" % (ad, ek)

    # --- açıklama: rakam + kapsam + ile özel unsur + aksiyon, kırpmasız
    p = ["%s%s %s: %s." % (ad, ek, terim, kapsam)]
    if kanca and kanca.endswith("'den"):
        p = _ekle(p, "Fiyat %s başlıyor." % kanca)
    elif tur == "dugun-cekimi":
        p = _ekle(p, "Aynı gün teaser teslim.")
    # ile özel unsur kapanıştan ÖNCE gelir: yer bilgisi jenerik çağrıdan değerli
    if il3:
        p = _ekle(p, "%s ve tüm ilçeler." % il3)
    mek = _mekan(c)
    if mek and tur in ("klip-cekimi", "dugun-cekimi"):
        p = _ekle(p, "Çekim noktaları: %s." % mek)
    kapanis = "Tarihi birlikte kuralım." if tur == "dugun-cekimi" else "Aynı gün net teklif."
    p = _ekle(p, kapanis)
    return dict(title=title, h1=h1, desc=" ".join(p))


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
