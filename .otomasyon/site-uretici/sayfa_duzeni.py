# -*- coding: utf-8 -*-
"""Başlık ve metin düzeni — Luna Yapım sayfaları (28.09.2026).

Neden: 28.09 denetiminde il sayfalarında şunlar ölçüldü —
  * H1'ler arama dilini tam karşılamıyordu ("Adana'da 3D render"; arayan "mimari render",
    "3d modelleme", "havadan görüntü" yazıyor — Search Console sorguları).
  * 509 sayfanın hepsinde "<il>'de yerel unsurlar" H2'si ve altında "başka ilden kopyalanmadı",
    "her satır X için yazıldı" gibi dolgu cümleleri vardı (şablon olduğunu kendisi söylüyordu).
  * Aynı sayfada aynı paragraf iki kez geçiyordu (ör. "Abdal müzik geleneğinin merkezi…").
  * "çözüm ortağımız" bir sayfada 4-5 kez geçiyordu; klip/düğün/drone/emlak sayfalarında
    "modelleme ve animasyon işini tamamen uzaktan yürütüyoruz" gibi konu dışı cümle vardı.
Bu modül bunları her üretimde, tekrar çalıştırılabilir biçimde düzeltir. Yeni sayfa açmaz,
anahtar kelime doldurmaz: başlıklar kısa, doğal Türkçe ve sayfanın gerçek içeriğini anlatır.
"""
import re, html, os

HIZMETLER = ["drone-cekimi", "emlak-video", "insaat-3d-modelleme", "urun-animasyon",
             "klip-cekimi", "dugun-cekimi", "isletme-tanitim"]

# H1'in italik kısmı: arayanın kullandığı ifade (Search Console sorgularından)
H1_IFADE = {
    "drone-cekimi": "drone çekimi ve havadan görüntü",
    "emlak-video": "emlak video çekimi",
    "insaat-3d-modelleme": "mimari render ve 3D modelleme",
    "urun-animasyon": "3D ürün animasyonu",
    "klip-cekimi": "klip çekimi ve müzik videosu",
    "dugun-cekimi": "düğün çekimi ve düğün filmi",
    "isletme-tanitim": "tanıtım filmi ve sosyal medya çekimi",
}
# "<İl>'de bu iş neye bakıyor" -> sayfanın o bölümde gerçekten anlattığı şey
H2_NEYE = {
    "drone-cekimi": "{P} havadan neler çekiyoruz",
    "emlak-video": "{P} emlak videosunda neye bakıyoruz",
    "insaat-3d-modelleme": "{P} 3D projelerde neye bakıyoruz",
    "urun-animasyon": "{P} ürün animasyonunda neye bakıyoruz",
    "klip-cekimi": "{P} klip için sahne ve mekân",
    "dugun-cekimi": "{P} düğün düzeni ve dış çekim",
    "isletme-tanitim": "{P} işletme tanıtımında neye bakıyoruz",
}
# "<İl>'de yerel unsurlar" -> bölümün içeriği (coğrafya, mekân, ilçe, sektör)
H2_YEREL = {
    "drone-cekimi": "{A} için uçuş ve çekim notları",
    "emlak-video": "{A} konut dokusu ve çekim notları",
    "insaat-3d-modelleme": "{A} yapı dokusu ve proje notları",
    "urun-animasyon": "{A} sanayisi, ilçeler ve sektörler",
    "klip-cekimi": "{A} için mekân ve çekim notları",
    "dugun-cekimi": "{A} için mekân ve çekim notları",
    "isletme-tanitim": "{A} için sektör ve çekim notları",
    None: "{A}: yapı, sanayi ve çekim notları",
}
DOLGU = [
    r"Aynı işi her ilde aynı şekilde yapmıyoruz; aşağıdaki notlar [^<.]+ için\.",
    r"[^<.]+ özelinde ne yaptığımızı ve neden böyle yaptığımızı aşağıda anlattık\.",
    r"Bir şehirde işe yarayan anlatım diğerinde yaramıyor; [^<.]+ için olan bu\.",
    r"Bu sayfadaki her şey [^<.]+ için ayrı düşünüldü, başka ilden kopyalanmadı\.",
    r"Şehri tanımadan iş yapmıyoruz; aşağıdaki her satır [^<.]+ için yazıldı\.",
    r"Aynı işi her ilde aynı şekilde yapmıyoruz — [^<]+ kendi dinamiği var\.",
]
# 3D ve ürün animasyonu dışındaki sayfalarda konu dışı kalan cümle
UZAKTAN = re.compile(r"\s*[^.<>]{0,40}modelleme ve animasyon işini tamamen uzaktan yürütüyoruz;[^.<]*?programa alıyoruz\.")


def _tur(p):
    m = re.match(r"^sehir/([a-z-]+)\.html$", p)
    if not m or m.group(1) == "index":
        return None, None
    ad = m.group(1)
    for h in HIZMETLER:
        if ad.endswith("-" + h):
            return "hizmet", h
    return "genel", None


def _duz(x):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x))).strip().lower()


def _gram(t, n=4):
    w = re.findall(r"\w+", t)
    return set(tuple(w[i:i + n]) for i in range(max(0, len(w) - n + 1)))


def _metin_temizle(s, hizmet, P=None):
    """Hero'dan sonra, <details> (SSS) ve JSON-LD dışındaki düz <p>'lerde:
    konu dışı cümle, dolgu, sayfa içi tekrar ve fazladan çözüm-ortağı cümlesini ayıklar."""
    bas = s.find('<div class="page-hero"')
    son = s.find("<footer")
    if bas < 0 or son < 0:
        return s
    govde = s[bas:son]
    # SSS blokları dokunulmaz — koruma altına al
    korunan = []
    def _koru(m):
        korunan.append(m.group(0)); return "\x00%d\x00" % (len(korunan) - 1)
    govde = re.sub(r"(?is)<details.*?</details>", _koru, govde)
    if hizmet not in ("insaat-3d-modelleme", "urun-animasyon", None):
        # konu dışı "modelleme uzaktan" cümlesi yerine çekim işine uyan tek cümle; sayfada
        # daha önce çözüm ortağı cümlesi varsa aşağıdaki sınırlayıcı bunu da düşürür
        yerine = (" %s çekim gereken günlerde bölgedeki çözüm ortağımızla, kurgu ve renkte kendi ekibimizle çalışıyoruz." % P) if P else ""
        govde = UZAKTAN.sub(lambda m: yerine, govde)
    for d in DOLGU:
        govde = re.sub(r"\s*<p>\s*%s\s*</p>" % d, "", govde)
    gorulen = set()
    ortak_goruldu = [False]

    def _p(m):
        ic = m.group(1)
        duz = _duz(ic)
        g = _gram(duz)
        if len(duz.split()) >= 8 and g and len(g & gorulen) / len(g) >= 0.7:
            return ""   # bütün paragraf sayfada zaten var
        # cümle düzeyi (etiket içermeyen cümleler)
        parca = re.split(r"(?<=[.!?])\s+(?=[A-ZÇĞİÖŞÜ0-9<])", ic)
        kalan = []
        for c in parca:
            if "<" not in c:
                dc = _duz(c); gc = _gram(dc)
                if len(dc.split()) >= 6 and gc and len(gc & gorulen) / len(gc) >= 0.85:
                    continue
                if "çözüm ortağı" in dc:
                    if ortak_goruldu[0]:
                        continue
                    ortak_goruldu[0] = True
            elif "çözüm ortağı" in _duz(c):
                ortak_goruldu[0] = True
            kalan.append(c)
        yeni = " ".join(kalan).strip()
        gorulen.update(_gram(_duz(yeni)))
        return ("<p>%s</p>" % yeni) if _duz(yeni) else ""

    # sırayla işle: <p> dışındaki başlık/liste metinleri de "görülen"e girsin
    parcalar = re.split(r"(<p>.*?</p>)", govde, flags=re.S)
    out = []
    for pr in parcalar:
        m = re.fullmatch(r"<p>(.*?)</p>", pr, flags=re.S)
        if m:
            out.append(_p(m))
        else:
            gorulen.update(_gram(_duz(re.sub(r"(?is)<(h1|h2|h3|a)[^>]*>.*?</\1>", " ", pr))))
            out.append(pr)
    govde = "".join(out)
    # içi boş kalan H3'ler
    govde = re.sub(r"\s*<h3>[^<]*</h3>(?=\s*(<h3>|</div>|<h2))", "", govde)
    govde = re.sub(r"\x00(\d+)\x00", lambda m: korunan[int(m.group(1))], govde)
    return s[:bas] + govde + s[son:]


# İl genel sayfalarında 81 ilde birebir aynı duran hizmet tanımları. Hizmetin adı H3'te,
# ile özgü satır ("<İl> özelinde: …") ve detay bağlantısı hemen altında duruyor; genel tanım
# hizmet sayfasının kendisinde. Bu yedi paragraf şablon payını %38-45'e çıkarıyordu.
GENEL_TANIM_BASI = (
    "Konut projesi, villa, site ve ticari yapı için mimari render",
    "Villa, daire, konut projesi, arsa ve ticari mülk için drone destekli ilan videosu",
    "Ürünü 3D modelleyip videoya çeviriyoruz: çalışma prensibi",
    "Müzik klibi, marka klibi ve sanatçı tanıtım videosu. Senaryo",
    "Havadan 4K görüntü ve FPV ile tek nefeste akan mekân turları.",
    "Sinematik düğün filmi, nişan ve kına çekimi, dış çekim ve kurumsal etkinlik videosu.",
    "Kafe, restoran, mağaza, salon ve yerel hizmet işletmeleri için aylık içerik paketi",
)


def _genel_tanim_ayikla(s):
    for b in GENEL_TANIM_BASI:
        s = re.sub(r"\s*<p>%s[^<]*</p>(?=\s*<p><strong>[^<]*özelinde:</strong>)" % re.escape(b), "", s, count=1)
    return s

def il_sayfasi(s, p):
    tur, hizmet = _tur(p)
    if not tur or "<!-- il-sayfasi:v2 -->" in s:
        return s
    # H1
    m = re.search(r"<h1>([^<]+?) <i>([^<]+)</i></h1>", s)
    P = m.group(1).strip() if m else None
    if not P:
        mh = re.search(r"<h1>([^<']+'[a-zçğıöşü]+) ", s)
        P = mh.group(1) if mh else None
    if not P:
        return s
    A = re.split(r"['’]", P)[0]
    # H1 metni pusula/arama_hizala.py'de kurulur (H1_IFADE orada); burada yalnız P okunur.
    if hizmet in H2_NEYE:
        s = s.replace("<h2>%s bu iş neye bakıyor</h2>" % P, "<h2>%s</h2>" % H2_NEYE[hizmet].format(P=P, A=A), 1)
    s = s.replace("<h2>%s yerel unsurlar</h2>" % P, "<h2>%s</h2>" % H2_YEREL.get(hizmet, H2_YEREL[None]).format(P=P, A=A), 1)
    if tur == "genel":
        s = _genel_tanim_ayikla(s)
    return _metin_temizle(s, hizmet, P)


# Hizmet sayfaları: H1 arayanın kullandığı adla (eski slogan H1'ler hizmeti söylemiyordu)
HIZMET_H1 = {
    "hizmetler/drone-fpv.html": "Drone çekimi ve FPV çekim",
    "hizmetler/dugun-etkinlik.html": "Düğün çekimi ve etkinlik videosu",
    "hizmetler/emlak-kurumsal.html": "Emlak video çekimi ve kurumsal tanıtım filmi",
    "hizmetler/insaat-3d-modelleme.html": "İnşaat 3D modelleme, mimari render ve görselleştirme",
    "hizmetler/isletme-tanitim.html": "İşletme tanıtım filmi ve sosyal medya video çekimi",
    "hizmetler/klip-cekimi.html": "Klip çekimi: müzik klibi ve marka klibi",
    "hizmetler/urun-animasyon.html": "3D ürün animasyonu ve makine animasyonu",
    "hizmetler/seo-icerik.html": "SEO ve içerik hizmeti",
    "hizmetler/index.html": "Hizmetlerimiz: video prodüksiyon, drone, 3D ve baskı",
}


def _kucult(x):
    """'Konut Projesi' -> 'Konut projesi' (cümle ortasında büyük harf düzeltmesi, ilk kelime hariç)."""
    def _tr_kucuk(c):
        return {"İ": "i", "I": "ı"}.get(c, c.lower())
    w = x.split(" ")
    return " ".join([w[0]] + [(_tr_kucuk(k[:1]) + k[1:]) if k[:1].isupper() and not k.isupper() and len(k) > 1 and k not in ("3D", "AVM") else k for k in w[1:]])


def hizmet_sayfasi(s, p):
    if p in HIZMET_H1:
        s = re.sub(r"<h1([^>]*)>(?:(?!</h1>).)*</h1>", lambda m: "<h1%s>%s</h1>" % (m.group(1), HIZMET_H1[p]), s, count=1, flags=re.S)
    m = re.match(r"^hizmetler/(insaat-3d|urun-animasyon)-[a-z-]+\.html$", p)
    if m:
        h1 = re.search(r"<h1([^>]*)>([^<]+)((?:<i>[^<]*</i>)?[^<]*)</h1>", s)
        if h1:
            yeni = _kucult(h1.group(2).rstrip()) + (" " if h1.group(2).endswith(" ") else "")
            if yeni != h1.group(2):
                s = s.replace(h1.group(0), "<h1%s>%s%s</h1>" % (h1.group(1), yeni, h1.group(3)), 1)
            duz = re.sub(r"<[^>]+>", "", yeni + h1.group(3)).strip()
            konu = re.split(r" için ", duz)[0] if " için " in duz else re.sub(r" (Animasyonu|animasyonu|ve Laboratuvar).*$", "", duz)
            ins = m.group(1) == "insaat-3d"
            s = re.sub(r"<h2([^>]*)>Sorun</h2>", lambda mm: "<h2%s>%s: sık karşılaşılan sorun</h2>" % (mm.group(1), konu), s, count=1)
            s = s.replace("<h2>Ne yapıyoruz</h2>", "<h2>%s için ne üretiyoruz</h2>" % konu, 1)
            s = s.replace("<h2>Fiyat</h2>", "<h2>%s %s fiyatı</h2>" % (konu, "3D görselleştirme" if ins else "animasyon"), 1)
            if ins:
                s = s.replace("<h2>Ürününüzü <i>anlatılır</i> hâle getirelim.</h2>", "<h2>Projenizi <i>görünür</i> hâle getirelim.</h2>")
    return s


ANA_H1_ESKI = '<span class="satir"><span>Çalışan <i>sistemler</i></span></span><span class="satir"><span>kuruyoruz.</span></span>'
ANA_H1_YENI = '<span class="satir"><span>Video, drone ve <i>3D</i></span></span><span class="satir"><span>Bursa\'dan 81 ile.</span></span>'


ANA_ETK_ESKI = "Bursa · Yazılım · Otonom Sistemler · Prodüksiyon"
ANA_ETK_YENI = "Bursa · Prodüksiyon · Drone · 3D · Yazılım"
ANA_LEDE_RE = re.compile(r"<p>Kendi yazılımlarımızı kendimiz yazıyoruz:.*?kamerayı da biz alıyoruz\.</p>", re.S)
ANA_LEDE_YENI = ("<p>Tanıtım filmi, drone ve FPV çekim, klip, mimari render ve 3D ürün animasyonu — "
                 "çekimden kurguya aynı ekip. Merkezimiz Bursa; 81 ilde çözüm ortaklarımızla sahadayız. "
                 "Kendi yazılımlarımızı da biz yazıyoruz: otonom sistemler, e-ticaret otomasyonu, içerik üretim hatları.</p>")


def ana_sayfa(s, p):
    """Ana sayfa: arayanların %50'si buraya geliyor (Search Console); başlık hizmeti söylesin."""
    if p != "index.html":
        return s
    s = s.replace(ANA_H1_ESKI, ANA_H1_YENI, 1)
    s = s.replace(ANA_ETK_ESKI, ANA_ETK_YENI, 1)
    s = s.replace('<a class="btn btn-dolu" href="matrix">Çalışan bir sistemi gör</a>',
                  '<a class="btn btn-dolu" href="https://wa.me/905542182603">Fiyat iste</a>\n      <a class="btn btn-cizgi" href="hizmetler/">Hizmetler</a>', 1)
    s = s.replace("<title>Luna Yapım — İnşaat 3D Modelleme, Video ve Yazılım</title>",
                  "<title>Luna Yapım — Video Prodüksiyon, Drone ve 3D Render | Bursa</title>", 1)
    s = s.replace('og:title" content="Luna Yapım — Yazılım, Otonom Sistemler ve Prodüksiyon"',
                  'og:title" content="Luna Yapım — Video Prodüksiyon, Drone ve 3D Render | Bursa"', 1)
    s = s.replace("Bursa merkezli yazılım ve yapım şirketi. Otonom sistemler, iş otomasyonu ve kendi yazılım ürünleri; yapay zekâ destekli reklam ve görsel üretim.",
                  "Bursa merkezli video prodüksiyon ve yazılım şirketi: tanıtım filmi, drone ve FPV çekim, klip, mimari render ve 3D ürün animasyonu; 81 ilde çözüm ortaklarıyla çekim. Otonom sistem ve iş otomasyonu yazılımları.", 1)
    return ANA_LEDE_RE.sub(ANA_LEDE_YENI, s, count=1)


def uygula(s, p):
    p = (p or "").replace(os.sep, "/")
    if p.startswith("trend/"):
        return s
    s = ana_sayfa(s, p)
    if p.startswith("sehir/"):
        return il_sayfasi(s, p)
    if p.startswith("hizmetler/"):
        return hizmet_sayfasi(s, p)
    return s
