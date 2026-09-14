# -*- coding: utf-8 -*-
"""
Derin site incelemesi — sayfa kaynağından okunabilen HER şeyi çıkarır.

Yüzeysel denetim "meta açıklama var mı" diye bakar. Bu katman asıl parayı
kaybettiren yere bakar: ziyaretçi siteye girdi, sonra ne oldu?
  · dönüşüm  — arayabiliyor mu, yazabiliyor mu, ne yapması gerektiğini biliyor mu
  · güven    — bu firmanın işini gerçekten yaptığına dair kanıt var mı
  · içerik   — anlatacak bir şeyi var mı, yoksa üç cümle mi
  · teknik   — arama motoru ve paylaşım tarafı

Sadece kamuya açık sayfa kaynağına bakar. Hiçbir yere giriş yapmaz, hiçbir
platformdan veri kazımaz. Her bulgu, hangi adreste ne görüldüğüyle birlikte döner.
"""
import re, urllib.parse, datetime
from .kaynaklar.agir import getir

# ---------------------------------------------------------------- desenler
ETIKET_SIL = re.compile(r"<(script|style|noscript|svg)[^>]*>.*?</\1>", re.S | re.I)
ETIKET = re.compile(r"<[^>]+>")

CTA_SOZ = ("teklif al", "teklif iste", "ücretsiz teklif", "fiyat al", "hemen ara",
           "bizi arayın", "iletişime geç", "bize ulaş", "randevu", "keşif talep",
           "whatsapp'tan yaz", "hemen başla", "görüşme ayarla", "katalog iste",
           "get a quote", "contact us")
REFERANS_SOZ = ("referans", "projelerimiz", "işlerimiz", "portfolyo", "portföy",
                "tamamlanan proje", "çalıştığımız", "müşterilerimiz", "galeri",
                "bitmiş proje", "case study")
YORUM_SOZ = ("müşteri yorum", "müşterilerimiz ne diyor", "görüşleri", "testimonial",
             "memnuniyet", "referans mektubu", "bizi tercih edenler")
EKIP_SOZ = ("hakkımızda", "biz kimiz", "ekibimiz", "kurucu", "yönetim kurulu",
            "kadromuz", "about us", "our team")
BELGE_SOZ = ("sertifika", "iso ", "belge", "üyelik", "ödül", "yetki belgesi",
             "tse", "akreditasyon", "patent", "marka tescil")
FIYAT_SOZ = ("fiyat", "paket", "ücret", "₺", " tl", "başlayan fiyat", "tarife",
             "abonelik", "kampanya")
BLOG_SOZ = ("blog", "haber", "makale", "yazılar", "duyuru", "bülten")
SSS_SOZ = ("sık sorulan", "s.s.s", "sss", "merak edilen", "faq")

HARITA_IZ = ("google.com/maps", "maps.app.goo.gl", "goo.gl/maps", "yandex.com/maps",
             "maps.google", "openstreetmap")
WA_IZ = ("wa.me/", "api.whatsapp.com", "web.whatsapp.com", "whatsapp://")
FORM_HIZMET = ("docs.google.com/forms", "typeform.com", "jotform", "formspree",
               "hubspot", "wufoo")

IC_SAYFA_ONCELIK = ("iletisim", "iletişim", "contact", "hakkimizda", "hakkında",
                    "about", "hizmet", "urun", "ürün", "product", "service",
                    "referans", "proje", "galeri", "blog")


def _metin(govde):
    """Görünen metni kabaca çıkarır."""
    g = ETIKET_SIL.sub(" ", govde or "")
    g = ETIKET.sub(" ", g)
    g = re.sub(r"&[a-z]+;|&#\d+;", " ", g)
    return re.sub(r"\s+", " ", g).strip()


def _kok(url):
    p = urllib.parse.urlparse(url if url.startswith("http") else "https://" + url)
    return "%s://%s" % (p.scheme, p.netloc), p.netloc


def _var_mi(alt, sozler):
    """Hangi sözcük yakalandı — kanıt olarak geri döner."""
    for s in sozler:
        if s in alt:
            return s
    return None


def _bagli_sayfalar(kok, alan, govde, azami=3):
    """Ana sayfadan, incelemeye değer iç sayfaları seçer."""
    bulunan, gorulen = [], set()
    for m in re.finditer(r'href=["\']([^"\']+)["\']', govde or "", re.I):
        u = m.group(1)
        if u.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue
        tam = urllib.parse.urljoin(kok + "/", u)
        if alan not in tam:
            continue
        yol = urllib.parse.urlparse(tam).path.lower().strip("/")
        if not yol or tam in gorulen:
            continue
        gorulen.add(tam)
        oncelik = next((i for i, a in enumerate(IC_SAYFA_ONCELIK) if a in yol), 99)
        if oncelik < 99:
            bulunan.append((oncelik, tam))
    bulunan.sort()
    return [u for _, u in bulunan[:azami]]


# ---------------------------------------------------------------- ana inceleme
def incele(url, azami_sayfa=4):
    """
    Siteyi gezip derin sinyalleri çıkarır.
    Döner: sinyal sözlüğü (hiçbir alan uydurulmaz; okunamayan None kalır).
    """
    s = {
        "url": url, "ulasildi": False, "gezilen": [], "sayfa_sayisi": 0,
        # dönüşüm
        "tel_link": 0, "mailto": 0, "whatsapp": None, "form": False, "girdi_alani": 0,
        "form_hizmeti": None, "cta": None, "harita_link": None,
        "fiyat_sinyali": None,
        # güven
        "referans": None, "yorum": None, "ekip": None, "belge": None,
        "iletisim_sayfasi": None, "sss": None,
        # içerik
        "kelime": 0, "gorsel": 0, "alt_eksik": 0, "alt_yok": 0, "alt_bos": 0, "h1": 0, "h2": 0,
        "ic_baglanti": 0, "blog": None, "hizmet_sayfasi": 0,
        # teknik
        "canonical": False, "og": False, "twitter": False, "favicon": False,
        "dil": None, "telif_yili": None, "boyut_kb": 0,
        "robots": None, "sitemap": None,
        "zaman": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
    }
    if not url:
        return s
    kok, alan = _kok(url)
    kod, govde, son = getir(kok, zaman_asimi=12)
    if kod == 0 or not govde:
        kod, govde, son = getir(kok, dogrula_ssl=False, zaman_asimi=12)
    if kod == 0 or kod >= 400 or not govde:
        return s

    s["ulasildi"] = True
    s["gezilen"].append(son or kok)
    sayfalar = [(son or kok, govde)]
    for u in _bagli_sayfalar(kok, alan, govde, azami_sayfa - 1):
        k2, g2, _ = getir(u, zaman_asimi=10)
        if k2 == 200 and g2:
            sayfalar.append((u, g2))
            s["gezilen"].append(u)
    s["sayfa_sayisi"] = len(sayfalar)

    ana_govde = govde
    ana_alt = ana_govde.lower()
    tum_alt = " ".join(g.lower() for _, g in sayfalar)
    tum_metin = " ".join(_metin(g) for _, g in sayfalar).lower()

    def nerede(desen_var, sozler, kaynak_alt=None):
        """Sayfalar içinde hangisinde geçtiğini bulur — kanıt için."""
        for u, g in sayfalar:
            hit = _var_mi(_metin(g).lower(), sozler)
            if hit:
                return {"soz": hit, "sayfa": u}
        return None

    # --- dönüşüm
    s["tel_link"] = len(re.findall(r'href=["\']tel:', tum_alt))
    s["mailto"] = len(re.findall(r'href=["\']mailto:', tum_alt))
    wa = next((w for w in WA_IZ if w in tum_alt), None)
    s["whatsapp"] = wa
    # <form> etiketi, bilinen form hizmeti ya da bir arada duran giriş alanları
    girdi = len(re.findall(r"<(?:input|textarea|select)\b", tum_alt))
    s["form"] = (bool(re.search(r"<form[\s>]", tum_alt))
                 or any(f in tum_alt for f in FORM_HIZMET)
                 or girdi >= 3)
    s["girdi_alani"] = girdi
    s["form_hizmeti"] = next((f for f in FORM_HIZMET if f in tum_alt), None)
    s["cta"] = nerede(None, CTA_SOZ)
    s["harita_link"] = next((h for h in HARITA_IZ if h in tum_alt), None)
    s["fiyat_sinyali"] = nerede(None, FIYAT_SOZ)

    # --- güven
    s["referans"] = nerede(None, REFERANS_SOZ)
    s["yorum"] = nerede(None, YORUM_SOZ)
    s["ekip"] = nerede(None, EKIP_SOZ)
    s["belge"] = nerede(None, BELGE_SOZ)
    s["sss"] = nerede(None, SSS_SOZ)
    s["iletisim_sayfasi"] = next(
        (u for u, _ in sayfalar if any(a in u.lower() for a in ("iletisim", "iletişim", "contact"))), None)

    # --- içerik
    ana_metin = _metin(ana_govde)
    s["kelime"] = len([w for w in ana_metin.split() if len(w) > 1])
    imgler = re.findall(r"<img\b[^>]*>", tum_alt)
    s["gorsel"] = len(imgler)
    # alt="" BİLEREK boş bırakılmış olabilir (süs görseli — ekran okuyucu atlasın diye).
    # Bu doğru kullanım; eksik saymıyoruz. Sadece alt niteliği HİÇ olmayanı sayıyoruz.
    s["alt_yok"] = len([i for i in imgler if not re.search(r'\balt\s*=', i)])
    s["alt_bos"] = len([i for i in imgler if re.search(r'\balt\s*=\s*["\']\s*["\']', i)])
    s["alt_eksik"] = s["alt_yok"]
    s["h1"] = len(re.findall(r"<h1[\s>]", ana_alt))
    s["h2"] = len(re.findall(r"<h2[\s>]", ana_alt))
    ic = set()
    for m in re.finditer(r'href=["\']([^"\'#]+)["\']', ana_alt):
        u = m.group(1).strip()
        if u.startswith(("mailto:", "tel:", "javascript:", "data:")):
            continue
        if u.startswith("http"):
            if alan in u:
                ic.add(u)          # kendi alan adına mutlak bağlantı
            continue
        ic.add(u)                  # göreli bağlantı (./sayfa.html, /yol, sayfa.html)
    s["ic_baglanti"] = len(ic)
    s["blog"] = nerede(None, BLOG_SOZ)
    s["hizmet_sayfasi"] = len({m.group(1) for m in re.finditer(r'href=["\']([^"\']*(?:hizmet|service|urun|ürün)[^"\']*)["\']', ana_alt)})

    # --- teknik
    s["canonical"] = bool(re.search(r'rel=["\']canonical["\']', ana_alt))
    s["og"] = bool(re.search(r'property=["\']og:', ana_alt))
    s["twitter"] = bool(re.search(r'name=["\']twitter:', ana_alt))
    s["favicon"] = bool(re.search(r'rel=["\'][^"\']*icon', ana_alt))
    m = re.search(r"<html[^>]+lang=[\"']([a-zA-Z-]+)", ana_govde)
    s["dil"] = m.group(1) if m else None
    yillar = [int(y) for y in re.findall(r"(?:©|&copy;|copyright)[^\d]{0,20}(20\d\d)", ana_alt)]
    s["telif_yili"] = max(yillar) if yillar else None
    s["boyut_kb"] = round(len(ana_govde.encode("utf-8", "ignore")) / 1024, 1)

    for ad, anahtar in (("robots.txt", "robots"), ("sitemap.xml", "sitemap")):
        k3, g3, _ = getir(kok + "/" + ad, zaman_asimi=8)
        s[anahtar] = bool(k3 == 200 and g3 and len(g3.strip()) > 10)

    return s


# ---------------------------------------------------------------- eksiğe çevir
# (kod, başlık, ağırlık, ne kontrol ettik, bulgu üretici)
def eksikler(s, bugun=None):
    """Derin sinyalleri kanıtlı eksik listesine çevirir."""
    if not s.get("ulasildi"):
        return []
    yil = (bugun or datetime.date.today()).year
    kaynak = s["gezilen"][0] if s["gezilen"] else s["url"]
    cikti = []

    def ek(kod, kontrol, bulgu, kaynak_=None):
        cikti.append({"kod": kod, "kontrol": kontrol, "bulgu": bulgu,
                      "kaynak": kaynak_ or kaynak, "zaman": s["zaman"]})

    # ---- dönüşüm: ziyaretçi ne yapacağını biliyor mu
    if not s["cta"]:
        ek("cta_yok", "Sayfalarda 'teklif al / bize ulaşın / hemen ara' gibi bir eylem çağrısı",
           "Ziyaretçiye ne yapması gerektiğini söyleyen tek bir düğme/cümle bulunamadı — "
           "ilgilenen kişi sayfayı okuyup çıkıyor")
    if not s["tel_link"]:
        ek("tel_tiklanmaz", "Telefon numarasının tel: bağlantısı olması",
           "Numara tıklanabilir değil — telefondan bakan kişi numarayı elle yazmak zorunda; "
           "çoğu bunu yapmıyor")
    if not s["whatsapp"]:
        ek("whatsapp_yok", "Sayfada WhatsApp bağlantısı (wa.me / api.whatsapp.com)",
           "WhatsApp butonu yok — Türkiye'de ilk temasın en sık kurulduğu kanal kapalı")
    if not s["form"]:
        ek("form_yok", "Sayfalarda iletişim formu (<form> veya form hizmeti)",
           "Form yok — mesai dışında gelen ziyaretçinin iz bırakacağı yer yok")
    if not s["harita_link"]:
        ek("harita_link_yok", "Sayfada haritaya/yol tarifine bağlantı",
           "Yol tarifi bağlantısı yok — adrese gelmek isteyen kişi adresi kopyalamak zorunda")
    if not s["fiyat_sinyali"]:
        ek("fiyat_sinyali_yok", "Sayfalarda fiyat, paket veya 'başlayan fiyatlarla' türü bir işaret",
           "Hiçbir fiyat sinyali yok — ziyaretçi bütçesine uyup uymadığını anlayamıyor, "
           "sormaya üşenen kişi rakibe gidiyor")

    # ---- güven: bu iş gerçekten yapılıyor mu
    if not s["referans"]:
        ek("referans_yok", "'referanslarımız / projelerimiz / işlerimiz' bölümü",
           "Yapılmış iş gösteren bir bölüm yok — ilk kez gelen ziyaretçi için firma kanıtsız")
    else:
        pass
    if not s["yorum"]:
        ek("yorum_gomulu_yok", "Sitede müşteri yorumu / referans görüşü",
           "Sitede tek bir müşteri sözü yok — güven yalnızca firmanın kendi iddiasına dayanıyor")
    if not s["ekip"]:
        ek("ekip_yok", "'hakkımızda / ekibimiz / kurucu' bölümü",
           "Arkasında kim olduğu görünmüyor — kurumsal alıcı ve büyük iş için ilk elenme sebebi")
    if not s["belge"]:
        ek("belge_yok", "Sertifika, üyelik, ödül veya yetki belgesi",
           "Belge/üyelik gösterilmemiş — teknik yeterlilik iddiası doğrulanamıyor")
    if not s["iletisim_sayfasi"]:
        ek("iletisim_sayfasi_yok", "Ayrı bir iletişim sayfası",
           "Ayrı iletişim sayfası yok — Google'ın işletme bilgisini eşlediği sayfa eksik")
    if not s["sss"]:
        ek("sss_yok", "Sık sorulan sorular bölümü",
           "SSS yok — hem ziyaretçinin ilk itirazı karşılanmıyor hem de aramada "
           "soru şeklindeki sorgulara çıkma şansı kaçıyor")

    # ---- içerik
    if s["kelime"] < 250:
        ek("icerik_sig", "Ana sayfadaki görünen metin miktarı",
           "Ana sayfada yaklaşık %d kelime var — Google'ın sıralayacağı içerik yok denecek kadar az"
           % s["kelime"])
    if s["hizmet_sayfasi"] < 2:
        ek("hizmet_sayfasi_yok", "Her hizmet için ayrı sayfa",
           "Hizmetler tek sayfaya sıkışmış — her hizmet kendi aramasında görünemiyor")
    if not s["blog"]:
        ek("blog_yok", "Blog / haber / makale bölümü",
           "Taze içerik üretilmiyor — site Google için 'duran' bir site")
    if s["gorsel"] and s["alt_yok"] >= max(3, s["gorsel"] // 3):
        ek("gorsel_alt_yok", "Görsellerin alt niteliği (alt=\"\" süs görseli sayılır, eksik değil)",
           "%d görselin %d tanesinde alt niteliği hiç yok — görsel aramasında çıkmıyor"
           % (s["gorsel"], s["alt_yok"]))
    if s["ic_baglanti"] < 5:
        ek("ic_baglanti_az", "Ana sayfadan iç sayfalara verilen bağlantılar",
           "Ana sayfadan yalnızca %d iç bağlantı var — site derinliği taranamıyor" % s["ic_baglanti"])

    # ---- teknik
    if s["h1"] == 0:
        ek("h1_yok", "Ana sayfada <h1> başlığı", "Sayfanın ana başlığı tanımsız")
    elif s["h1"] > 1:
        ek("h1_coklu", "Ana sayfada <h1> sayısı",
           "%d adet H1 var — sayfanın asıl konusu belirsizleşiyor" % s["h1"])
    if not s["canonical"]:
        ek("canonical_yok", "rel=canonical etiketi",
           "Canonical yok — aynı içerik farklı adreslerden görünürse Google hangisini "
           "sıralayacağını bilmiyor")
    if not s["og"]:
        ek("og_yok", "Open Graph (og:) etiketleri",
           "OG etiketi yok — WhatsApp'ta veya sosyal medyada link paylaşıldığında "
           "görselsiz, başlıksız çıplak bağlantı görünüyor")
    if not s["favicon"]:
        ek("favicon_yok", "Favicon (sekme simgesi)",
           "Favicon yok — tarayıcı sekmesinde boş sayfa simgesi duruyor")
    if not s["dil"]:
        ek("dil_etiketi_yok", "<html lang=\"tr\"> dil etiketi",
           "Dil etiketi yok — arama motoru sayfanın Türkçe olduğunu varsaymak zorunda")
    if s["telif_yili"] and s["telif_yili"] < yil - 1:
        ek("eski_icerik", "Alt bilgideki telif yılı",
           "Telif yılı %d — ziyaretçi siteyi terk edilmiş sanıyor" % s["telif_yili"])
    if s["robots"] is False:
        ek("robots_yok", "robots.txt dosyası", "robots.txt yok veya boş")
    if s["sitemap"] is False:
        ek("sitemap_yok", "sitemap.xml dosyası",
           "Site haritası yok — Google sayfaları tek tek keşfetmek zorunda")
    if s["boyut_kb"] > 900:
        ek("agir_sayfa", "Ana sayfa HTML boyutu",
           "Ana sayfanın HTML'i %.0f KB — mobil bağlantıda açılış gecikiyor" % s["boyut_kb"])

    return cikti
