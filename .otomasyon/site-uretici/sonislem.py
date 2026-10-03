# -*- coding: utf-8 -*-
"""
ÜRETİM SONRASI İŞLEM — her yeniden üretimde uygulanması gereken adımlar.

Neden var: bir sayfayı yeniden ürettiğimizde, üretici şablonunda olmayan
düzeltmeler siliniyordu. Uzantısız adresler geri .html oluyor, asistan
betiği düşüyor, tablo sarmalı kayboluyordu. Her seferinde elle toparlamak
yerine hepsi burada; üretimden sonra bir kez çalıştırılıyor.

Hepsi ETKİSİZ TEKRARLANABİLİR (idempotent): iki kez çalıştırmak zarar vermez.
"""
import html
import glob, io, os, re, sys

SURUM = {"css": "26", "videolar": "7", "asistan": "2", "ajan": "1", "agac": "5", "fon": "2"}


def _derinlik(yol, kok):
    """Sayfa kaç klasör içeride — assets yolunu ona göre kur."""
    b = os.path.relpath(yol, kok).replace(os.sep, "/")
    return "../" * b.count("/")


def uzantisizlastir(s):
    """Cloudflare Pages .html'i 301 ile kesiyor. Kanonik ve bağlantılar
    doğrudan hedefi göstermeli, yönlendirmeye düşmemeli."""
    s = re.sub(r'(https://lunayapim\.com/[A-Za-z0-9_\-/]+?)\.html\b', r'\1', s)
    s = s.replace("https://lunayapim.com/index", "https://lunayapim.com/")
    # bağlantılar: .html + varsa #çapa / ?sorgu — çapa yüzünden atlanan 421 bağlantı
    # (376 sayfada index.html#urunler) Google'a sürekli yönlendirme besliyordu (14.09.2026)
    def _b(m):
        yol, kuyruk = m.group(1), (m.group(2) or "")
        return 'href="%s%s"' % (yol, kuyruk)
    s = re.sub(r'href="((?:\.\./)*/?[A-Za-z0-9_\-/]+?)\.html([#?][^"]*)?"', _b, s)
    for on in ("../", "/", ""):
        s = s.replace('href="%sindex"' % on, 'href="%s"' % (on or "./"))
        s = s.replace('href="%sindex#' % on, 'href="%s#' % (on or "./"))
        s = s.replace('href="%sindex?' % on, 'href="%s?' % (on or "./"))
    return s


def surumle(s):
    """Önbellek kırıcı sürümleri tek yerden yönet."""
    s = re.sub(r'luna\.css(\?v=\d+)?', 'luna.css?v=' + SURUM["css"], s)
    s = re.sub(r'videolar\.js(\?v=\d+)?', 'videolar.js?v=' + SURUM["videolar"], s)
    s = re.sub(r'asistan\.js(\?v=\d+)?', 'asistan.js?v=' + SURUM["asistan"], s)
    s = re.sub(r'agac\.js(\?v=\d+)?', 'agac.js?v=' + SURUM["agac"], s)
    s = re.sub(r'agac3d\.js(\?v=\d+)?', 'agac3d.js?v=' + SURUM["agac"], s)
    s = re.sub(r'fon\.js(\?v=\d+)?', 'fon.js?v=' + SURUM["fon"], s)
    return s


def asistan_ekle(s, on):
    if "asistan.js" in s or "</body>" not in s:
        return s
    return s.replace("</body>",
                     '<script src="%sassets/asistan.js?v=%s" defer></script>\n</body>'
                     % (on, SURUM["asistan"]))


def ajan_ekle(s, on):
    """Luna Ajan (sor/teklif/plan/takip) — asistanın hemen ardından, her sayfada."""
    if "</body>" not in s:
        return s
    if "ajan.js" in s:
        return re.sub(r'ajan\.js(\?v=\d+)?', 'ajan.js?v=' + SURUM["ajan"], s)
    return s.replace("</body>", '<script src="%sassets/ajan.js?v=%s" defer></script>\n</body>' % (on, SURUM["ajan"]))


def okuma_ekle(s, on):
    """Okuma sayacı — çerezsiz, kimliksiz; panel tıklanmayı buradan okuyor."""
    if "okuma.js" in s or "</body>" not in s:
        return s
    return s.replace("</body>", '<script src="%sassets/okuma.js" defer></script>\n</body>' % on)


ADSENSE = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3059196718190568" crossorigin="anonymous"></script>'


# AdSense yalnız TrendSaphiens'te (trendsaphiens.com = /trend/). 28.09.2026: lunayapim.com
# AdSense'te "düşük değerli içerik" ile reddedildi ve orada reklam hedefi yok; gündem/ ve
# bulten/ (Matrix) listeden çıktı.
ADSENSE_BOLUM = ("trend/",)


ADSENSE_ASGARI_KELIME = 400      # sayfanın KENDİ metni (kenar sütun, kart listesi, menü, form hariç)

# 28.09.2026 — AdSense incelemesi sürerken reklam yalnız yayıncı içeriği olan ekranlarda.
# Politika: "yayıncı içeriği olmayan / yalnız gezinme amaçlı ekranlarda reklam gösterilmez".
# Bölüm indeksleri (başlık listesi), günün bülteni (başka sayfaların özeti), Google Trends
# listesi (başlıklar Google'ın), arşiv gün sayfaları (noindex), araç dizini ve kurumsal
# sayfalar bu yüzden reklamsız. Ana sayfa istisna: inceleme kodu arar, 1.700 kelime kendi metni var.
ADSENSE_YASAK = [
    r"^trend/[^/]+/index\.html$",            # bölüm indeksleri
    r"^trend/(aranan|piyasa)/\d{4}-\d{2}-\d{2}\.html$",
    r"^trend/(bulten|araclar|sistem|hakkimizda|iletisim|gizlilik|kosullar|denetim)(/index)?\.html$",
]

_OZ_ATLA_ETIKET = {"script", "style", "nav", "header", "footer", "svg", "aside", "form", "noscript", "button", "select"}
_OZ_ATLA_SINIF = ("ts-kart", "ts-kartlar", "ts-serit", "ts-paylas", "ts-abone", "ts-reklam", "crumbs",
                  "ts-bolumler", "ts-rehber-liste", "ts-arac-blok", "ts-bant", "ts-yan", "ts-takvim", "ts-rakam")


def _oz_kelime(s):
    """Sayfanın kendi metni: <main> içinde, kenar sütun/kart/menü/form/paylaş dışında kalan kelimeler."""
    from html.parser import HTMLParser
    m = re.search(r"(?is)<main[^>]*>(.*)</main>", s)
    govde = m.group(1) if m else s
    BOS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}

    class P(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True); self.yigin = []; self.atla = 0; self.n = 0
        def handle_starttag(self, tag, attrs):
            if tag in BOS:
                return
            sinif = dict(attrs).get("class") or ""
            gizle = tag in _OZ_ATLA_ETIKET or any(c.startswith(_OZ_ATLA_SINIF) for c in sinif.split())
            self.yigin.append((tag, gizle))
            if gizle:
                self.atla += 1
        def handle_endtag(self, tag):
            if tag in BOS:
                return
            while self.yigin:
                t, g = self.yigin.pop()
                if g:
                    self.atla -= 1
                if t == tag:
                    break
        def handle_data(self, d):
            if not self.atla:
                self.n += len(re.findall(r"[\w]+", d))
    p = P()
    try:
        p.feed(govde)
    except Exception:
        return _govde_kelime(s)
    return p.n


def _govde_kelime(s):
    t = re.sub(r"(?is)<(script|style|nav|header|footer|svg)[^>]*>.*?</\1>", " ", s)
    return len(re.sub(r"(?s)<[^>]+>", " ", t).split())


def reklam_izinli(s, p=""):
    p = (p or "").replace(os.sep, "/")
    if not p.startswith(ADSENSE_BOLUM):
        return False
    if p == "trend/index.html":
        return True
    if any(re.search(d, p) for d in ADSENSE_YASAK):
        return False
    if re.search(r'name="robots" content="[^"]*noindex', s):
        return False
    return _oz_kelime(s) >= ADSENSE_ASGARI_KELIME


def adsense_ekle(s, p=""):
    """AdSense betiği yalnız TrendSaphiens'in YETERLİ KENDİ İÇERİĞİ olan sayfalarının <head>'ine.

    14.09.2026: liste/kapak sayfaları reklam taşıyınca "düşük değerli içerik" değerlendirmesi besleniyordu.
    28.09.2026: ölçüt sayfanın kendi metnine çekildi (kenar sütun ve kart listeleri sayılmıyor)
    ve yalnız gezinme amaçlı ekranlar kesin yasak listesine alındı.
    """
    if not reklam_izinli(s, p):
        s = re.sub(r'[ \t]*<script async src="https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js[^<]*</script>\n?', "", s)
        s = re.sub(r'\s*<div class="ts-reklam"><ins class="adsbygoogle".*?</ins><script>\(adsbygoogle=window\.adsbygoogle\|\|\[\]\)\.push\(\{\}\);</script></div>\s*', "\n", s, flags=re.S)
        return s
    if "adsbygoogle.js" in s or "</head>" not in s:
        return s
    return s.replace("</head>", ADSENSE + "\n</head>", 1)


def menu_trend(s, on, p=""):
    """Üst menü: Gündem + Bülten yerine tek 'TrendSaphiens' (/trend/). Gündem ve Bülten TrendSaphiens'in içinde ve altbilgide kalır."""
    m = re.search(r"<nav>.*?</nav>", s, re.S)
    if not m:
        return s
    nav = m.group(0)
    if ">TrendSaphiens<" in nav:
        return s
    p = (p or "").replace(os.sep, "/")
    vurgu = ' style="opacity:1;color:var(--kirmizi)"' if p.startswith(("trend/", "gundem/", "bulten/")) else ""
    yeni = '<a href="%strend/"%s>TrendSaphiens</a>' % (on, vurgu)
    yn = re.sub(r"\s*<a href=\"[^\"]*\"[^>]*>Gündem</a>", "", nav)
    if re.search(r"<a href=\"[^\"]*\"[^>]*>Bülten</a>", yn):
        yn = re.sub(r"<a href=\"[^\"]*\"[^>]*>Bülten</a>", yeni, yn, count=1)
    else:
        mb = re.search(r"<a href=\"[^\"]*blog/\"[^>]*>Blog</a>", yn)
        if not mb:
            return s
        yn = yn.replace(mb.group(0), mb.group(0) + "\n      " + yeni, 1)
    return s.replace(nav, yn, 1)


def altbilgi_yayin(s, on):
    """Altbilgi: Ürünler sütununa LunaTrendSaphiens, son sütuna Gündem ve Matrix Bülteni (bir kez)."""
    if ">LunaTrendSaphiens<" not in s:
        h = '<a href="%syazilim.html#fabrika">Luna Fabrika</a>' % on
        if h in s:
            s = s.replace(h, h + '\n        <a href="%strend/">LunaTrendSaphiens</a>' % on, 1)
    if ">Matrix Bülteni<" not in s:
        for h in ('<a href="%ssehir/">Tüm iller</a>' % on, '<a href="./">Tüm iller</a>', '<a href="%smatrix">KDA Matrix</a>' % on):
            if h in s:
                s = s.replace(h, h + '\n        <a href="%strend/">LunaTrendSaphiens</a>\n        <a href="%sgundem/">Gündem</a>\n        <a href="%sbulten/">Matrix Bülteni</a>' % (on, on, on), 1) if ">LunaTrendSaphiens<" not in s else s.replace(h, h + '\n        <a href="%sgundem/">Gündem</a>\n        <a href="%sbulten/">Matrix Bülteni</a>' % (on, on), 1)
                break
    return s


def gizlilik_ekle(s, on):
    """Alt bilgiye Gizlilik bağlantısı (AdSense ve KVKK için görünür olmalı)."""
    if 'gizlilik"' in s or "gizlilik.html" in s:
        return s
    hedef = '<a href="%skosullar">Koşullar</a>' % on
    if hedef in s:
        return s.replace(hedef, hedef + '\n        <a href="%sgizlilik">Gizlilik</a>' % on, 1)
    hedef2 = '<a href="%sseffaflik">Şeffaflık</a>' % on
    if hedef2 in s:
        return s.replace(hedef2, hedef2 + '\n        <a href="%sgizlilik">Gizlilik</a>' % on, 1)
    return s


_KOD_BLOK = re.compile(r"<(script|style)\b[\s\S]*?</\1\s*>", re.I)


def kod_disinda(s, islev):
    """islev'i YALNIZ <script>/<style> bloklarının DIŞINDAKI parçalara uygular.

    HTML'i yeniden yazan bir adım kod bloğunun içine girerse, oradaki metin
    HTML değil JavaScript kaynağı olduğu için sayfa sessizce bozulur.
    """
    parca, son = [], 0
    for m in _KOD_BLOK.finditer(s):
        parca.append(islev(s[son:m.start()]))
        parca.append(m.group(0))
        son = m.end()
    parca.append(islev(s[son:]))
    return "".join(parca)


def tablo_sar(s):
    """Dar ekranda tablo sayfayı yatay kaydırıyordu — kendi içinde kaysın.

    03.10.2026 — ikinci pahalı ders, birincisiyle aynı kökten: bu düzenli ifade
    <script> bloklarının içine de giriyordu. Doğum haritası aracının JS'i tablo
    HTML'ini çift tırnaklı bir dizgi içinde kuruyor; araya basılan
    class="tablo-kaydir" o dizgiyi kapatınca sayfadaki BÜTÜN JS
    "Unexpected identifier" ile düştü ve araç canlıda sessizce çalışmaz oldu —
    sayfa normal görünüyordu, yalnız il listesi boştu.
    Kural: HTML'i yeniden yazan her adım <script>/<style> içini atlamalı.
    """
    def _sar(p):
        return re.sub(r'(?<!<div class="tablo-kaydir">)<table\b[\s\S]*?</table>',
                      lambda m: '<div class="tablo-kaydir">' + m.group(0) + '</div>', p)
    return kod_disinda(s, _sar)


BELGE_BLOK = '''<h2 id="belgeler">Yetki ve belgeler</h2>
<p>Drone çekimi Türkiye'de belgeye bağlı bir iştir; belgesiz uçan bir ekiple çalışmak işi yaptıran tarafı da sorumluluk altına sokar. Bizde ikisi de var: <strong>SHGM kayıtlı insansız hava aracı</strong> ve <strong>SHGM lisanslı İHA pilotu</strong>. Uçuşu taşerona vermiyoruz.</p>
<div class="belgeler" id="luna-belgeler"></div>
'''


def belge_ekle(s, yol, on):
    if "drone" not in os.path.basename(yol) or "luna-belgeler" in s:
        return s
    m = re.search(r'<h2 id="surec">', s)
    if not m:
        return s
    s = s[:m.start()] + BELGE_BLOK + s[m.start():]
    if "belgeler.js" not in s:
        s = s.replace("</body>", '<script src="%sassets/belgeler.js"></script>\n</body>' % on)
    return s


def sitemap_uzantisizlastir(kok):
    """Sitemap'teki .html adresleri canonical ile ayni bicime getirir.

    Neden: Cloudflare Pages /x.html adresini /x'e 301 ile yonlendiriyor. Sitemap
    .html'li adres verince Google bunlari "Page with redirect" diye isaretleyip
    dizine almiyordu (14.09.2026: 187 sayfa). Canonical zaten uzantisiz.
    Etkisiz tekrarlanabilir.
    """
    yol = os.path.join(kok, "sitemap.xml")
    if not os.path.exists(yol):
        return {"sitemap": "yok"}
    s = io.open(yol, encoding="utf-8").read()

    def _duzelt(m):
        u = m.group(1)
        if u.endswith("/index.html"):
            u = u[:-len("index.html")]
        elif u.endswith(".html"):
            u = u[:-5]
        return "<loc>%s</loc>" % u

    yeni = re.sub(r"<loc>([^<]+)</loc>", _duzelt, s)
    if yeni != s:
        io.open(yol, "w", encoding="utf-8").write(yeni)
    return {"sitemap_duzelen": len(re.findall(r"<loc>[^<]+\.html</loc>", s))}


def sitemap_noindex_cikar(kok):
    """noindex'li sayfayı site haritasından çıkar.

    22.09.2026: eski gün sayfaları (piyasa/aranan arşivi) noindex'e alındı ama
    site haritasında kaldıkları için çelişkili sinyal veriyorlardı — "bu adresi
    tara" deyip sayfada "dizine ekleme" demek. Google bunu "sitemapte noindex"
    hatası olarak raporlar. Ekleyen taraf zaten noindex'i atlıyordu; eksik olan
    ÇIKARAN taraftı.
    """
    yol = os.path.join(kok, "sitemap.xml")
    if not os.path.exists(yol):
        return {"sitemap": "yok"}
    s = open(yol, encoding="utf-8").read()
    bloklar = re.findall(r"[ \t]*<url>.*?</url>\s*", s, re.S)
    cikan = []
    for b in bloklar:
        m = re.search(r"<loc>https://lunayapim\.com/([^<]*)</loc>", b)
        if not m:
            continue
        adres = m.group(1)
        adaylar = [adres, adres + ".html", os.path.join(adres, "index.html"),
                   (adres.rstrip("/") + "/index.html") if adres else "index.html"]
        for a in adaylar:
            tam = os.path.join(kok, a)
            if os.path.isfile(tam):
                govde = open(tam, encoding="utf-8", errors="replace").read(4000)
                if re.search(r'<meta[^>]+name="robots"[^>]+noindex', govde, re.I):
                    s = s.replace(b, "")
                    cikan.append(adres)
                break
    if cikan:
        open(yol, "w", encoding="utf-8").write(s)
    return {"sitemap_noindex_cikan": len(cikan), "ornek": cikan[:3]}


def sitemap_yeni_ekle(kok):
    """Diskte olup sitemap'te olmayan sayfaları ekler (noindex olanlar hariç).
    17.09.2026: yeni il sayfaları sitemap'e elle giriyordu, artık otomatik."""
    import datetime
    yol = os.path.join(kok, "sitemap.xml")
    if not os.path.exists(yol):
        return {"sitemap": "yok"}
    s = open(yol, encoding="utf-8").read()
    mevcut = set(re.findall(r"<loc>https://lunayapim\.com/([^<]*)</loc>", s))
    bugun = datetime.date.today().isoformat()
    eklenen = []
    for dizin, _, dosyalar in os.walk(kok):
        if "/.git" in dizin or "/.otomasyon" in dizin or "/onizleme" in dizin:
            continue
        for d in sorted(dosyalar):
            if not d.endswith(".html") or d in ("admin.html", "404.html"):
                continue
            tam = os.path.join(dizin, d)
            govde = open(tam, encoding="utf-8").read()
            if re.search(r'<meta[^>]+name="robots"[^>]+noindex', govde, re.I):
                continue
            bag = os.path.relpath(tam, kok).replace(os.sep, "/")
            adres = "" if bag == "index.html" else (
                bag[:-len("index.html")] if bag.endswith("/index.html") else bag[:-5])
            if adres in mevcut:
                continue
            eklenen.append(adres)
            kayit = ('<url><loc>https://lunayapim.com/%s</loc><lastmod>%s</lastmod>'
                     '<changefreq>monthly</changefreq><priority>0.7</priority></url>\n' % (adres, bugun))
            i = s.rindex("</urlset>")
            s = s[:i] + kayit + s[i:]
            mevcut.add(adres)
    if eklenen:
        open(yol, "w", encoding="utf-8").write(s)
    return {"sitemap_eklenen": len(eklenen), "ornek": eklenen[:3]}


def sitemap_olu_temizle(kok):
    """Site haritasından, dosyası artık olmayan adresleri düşürür.

    Neden (14.09.2026): yayından kaldırılan derleme sayfaları haritada kalınca
    Google 404 tarıyor ve "kaldırıldı" kaydı açıyor. Üretici kendi haritasından
    sorumlu. Etkisiz tekrarlanabilir.
    """
    yol = os.path.join(kok, "sitemap.xml")
    if not os.path.exists(yol):
        return {"sitemap": "yok"}
    s = io.open(yol, encoding="utf-8").read()
    dusen = []

    def _kalsin(m):
        u = m.group(1)
        if not u.startswith("https://lunayapim.com/"):
            return m.group(0)
        p = u[len("https://lunayapim.com/"):]
        aday = os.path.join(kok, (p + "index.html") if (p == "" or p.endswith("/")) else (p + ".html"))
        if os.path.exists(aday):
            return m.group(0)
        dusen.append(u)
        return ""

    yeni = re.sub(r"[ \t]*<url><loc>([^<]+)</loc>.*?</url>\n?", _kalsin, s, flags=re.S)
    if yeni != s:
        io.open(yol, "w", encoding="utf-8").write(yeni)
    return {"sitemap_dusen": len(dusen), "ornek": dusen[:3]}


def ilk_gorsel_oncelik(s):
    """Sayfadaki ILK gorseli erken yukle — LCP dogrudan bu karede olculuyor.

    20.09.2026 bagimsiz olcum (PageSpeed Insights, mobil): LCP 9,7 sn. Uretici
    her gorseli loading="lazy" basiyordu; ekranin ustundeki kapak da gec
    basliyordu. Ilk gorsel eager + fetchpriority=high, gerisi lazy kalir.
    """
    if 'fetchpriority="high"' in s:
        return s                      # daha once isaretlenmis — her kosuda bir tane daha eager olmasin
    i = s.find('loading="lazy"')
    if i < 0:
        return s
    return s[:i] + 'loading="eager" fetchpriority="high"' + s[i + len('loading="lazy"'):]




def varlik_kat(s, p, kok):
    """Sosyal hesap + sameAs + taban fiyat: JS'te kalmasın, HTML'e yazılsın.

    22.09.2026: sameAs yalnız tarayıcıda ekleniyordu; JavaScript çalıştırmayan
    tarayıcılar (Bing, yapay zekâ tarayıcıları) firma ile hesabı hiç
    eşleştiremiyordu. Ayrıntılı gerekçe site-uretici/varlik.py başında.
    """
    try:
        import varlik
        return varlik.calistir(s, p, kok)
    except Exception as ex:
        print("varlik:", ex)
        return s



def il_hizmet_bagla(s, p, kok):
    """İl sayfası, o ilin VAR OLAN her hizmet sayfasına bağlansın (idempotent).

    28.09.2026 bulgusu: 46 ilin drone sayfası var ama 24'ü (kademe-2) kendi il sayfasından
    hiç bağlantı almıyordu — il sayfasındaki drone bölümü genel /hizmetler/drone-fpv'ye
    gidiyordu, "hizmet sayfalarımız" kutusunda da drone kartı yoktu. Arayan "<il> drone
    çekimi" sayfasına il sayfasından ulaşamıyordu; Google da o sayfayı sahipsiz görüyordu.
    """
    pp = (p or "").replace(os.sep, "/")
    m = re.match(r"^sehir/([a-z]+)\.html$", pp)
    if not m or m.group(1) == "index":
        return s
    il = m.group(1)
    hedef = il + "-drone-cekimi"
    if not os.path.exists(os.path.join(kok, "sehir", hedef + ".html")):
        return s
    mt = re.search(r"<title>(.+?) Video Çekimi", s)
    ad = html.unescape(mt.group(1)).strip() if mt else il.capitalize()
    s = s.replace('<p><a href="../hizmetler/drone-fpv">Drone ve FPV çekim hizmet detayı →</a></p>',
                  '<p><a href="%s">%s Drone ve FPV çekim detay sayfası →</a></p>' % (hedef, ad), 1)
    s = s.replace('"name": "%s Drone ve FPV çekim", "url": "https://lunayapim.com/hizmetler/drone-fpv"' % ad,
                  '"name": "%s Drone ve FPV çekim", "url": "https://lunayapim.com/sehir/%s"' % (ad, hedef), 1)
    if ('href="%s"><b>' % hedef) not in s:
        kart = '<a href="%s"><b>%s Drone Çekimi</b><span>Havadan 4K ve FPV planlar</span></a>' % (hedef, ad)
        for sonraki in (il + "-klip-cekimi", il + "-dugun-cekimi", il + "-isletme-tanitim"):
            k = '<a href="%s"><b>' % sonraki
            if k in s:
                i = s.index(k)
                s = s[:i] + kart + "\n      " + s[i:]
                break
    return s


# Google İşletme Profili (Maps kaydı). 28.09.2026'da Maps'ten okundu: place_id ChIJkzRhVngRyhQRuTGCxlEWQfg.
GBP_HARITA = "https://maps.google.com/?cid=17888603735370903993"
_GBP_TIP = {"Organization", "LocalBusiness", "ProfessionalService"}


def _gbp_isle(d):
    """JSON-LD ağacında Luna Yapım kuruluş düğümlerine hasMap + sameAs ekler. Değişti mi döner."""
    import json as _j
    degisti = False
    if isinstance(d, list):
        for x in d:
            degisti = _gbp_isle(x) or degisti
        return degisti
    if not isinstance(d, dict):
        return False
    t = d.get("@type")
    tipler = set(t if isinstance(t, list) else [t])
    if tipler & _GBP_TIP and (d.get("name") == "Luna Yapım"):
        if d.get("hasMap") != GBP_HARITA:
            d["hasMap"] = GBP_HARITA; degisti = True
        sa = d.get("sameAs")
        sa = [sa] if isinstance(sa, str) else list(sa or [])
        if GBP_HARITA not in sa:
            sa.append(GBP_HARITA); d["sameAs"] = sa; degisti = True
    for k, v in list(d.items()):
        if isinstance(v, (dict, list)):
            degisti = _gbp_isle(v) or degisti
    return degisti


def gbp_ekle(s, p=""):
    """Luna Yapım sayfalarının şemasına İşletme Profili bağlantısı (TrendSaphiens hariç)."""
    import json as _j
    if (p or "").replace(os.sep, "/").startswith("trend/"):
        return s
    def _blok(m):
        try:
            d = _j.loads(m.group(2))
        except Exception:
            return m.group(0)
        if not _gbp_isle(d):
            return m.group(0)
        return m.group(1) + _j.dumps(d, ensure_ascii=False) + m.group(3)
    return re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', _blok, s, flags=re.S)


# 29.09.2026: Luna Yapım telefonu 0554 218 26 03 oldu. Eski numara hiçbir sayfada kalmasın —
# üreticiler, önbellekteki veri ya da elle yazılmış bir sayfa geri getirse bile her turda düzeltilir.
TELEFON_ESKI_YENI = [("+90 541 160 26 03", "+90 554 218 26 03"), ("0541 160 26 03", "0554 218 26 03"),
                     ("905411602603", "905542182603")]


def telefon_guncelle(s):
    for a, b in TELEFON_ESKI_YENI:
        if a in s:
            s = s.replace(a, b)
    return s


# 30.09.2026 — _headers /assets/* için "max-age=1 yıl, immutable" veriyor. Sürüm eki olmayan
# ya da elle artırılmayı bekleyen JS/CSS (olcum.js, form.js, ajan.js?v=1 …) değiştiğinde geri
# dönen ziyaretçi ESKİSİNİ görüyordu (29.09 telefon değişikliği ajan.js ve form.js'e böyle
# ulaşmazdı). Artık her assets/*.js ve *.css bağlantısına dosyanın içerik özeti eklenir:
# dosya değişince adres değişir, değişmeyince önbellek aynen çalışır.
_VARLIK_OZET = {}


def _varlik_ozeti(kok, yol):
    anahtar = (kok, yol)
    if anahtar not in _VARLIK_OZET:
        import hashlib
        try:
            with open(os.path.join(kok, yol), "rb") as f:
                _VARLIK_OZET[anahtar] = hashlib.md5(f.read()).hexdigest()[:8]
        except Exception:
            _VARLIK_OZET[anahtar] = None
    return _VARLIK_OZET[anahtar]


def varlik_surumu(s, kok):
    def _d(m):
        oz = _varlik_ozeti(kok, m.group(2))
        return (m.group(1) + m.group(2) + "?v=" + oz) if oz else m.group(0)
    return re.sub(r'((?:\.\./)*|/|https://lunayapim\.com/)(assets/[A-Za-z0-9_\-/]+\.(?:js|css))(?:\?v=[A-Za-z0-9]+)?(?=["\'])', _d, s)


def calistir(kok, desen="**/*.html"):
    degisen = 0
    for yol in glob.glob(os.path.join(kok, desen), recursive=True):
        p = os.path.relpath(yol, kok)
        if p.startswith(("assets", ".git", "onizleme")) or p in ("matrix.html", "admin.html"):
            continue
        s = io.open(yol, encoding="utf-8").read()
        o = s
        on = _derinlik(yol, kok)
        s = uzantisizlastir(s)
        s = telefon_guncelle(s)
        s = asistan_ekle(s, on)
        s = ajan_ekle(s, on)
        s = okuma_ekle(s, on)
        s = adsense_ekle(s, p)
        s = il_hizmet_bagla(s, p, kok)
        s = gbp_ekle(s, p)
        try:
            import sayfa_duzeni as _SD
            s = _SD.uygula(s, p)
        except Exception as _ex:
            print("sayfa_duzeni:", p, _ex)
        s = menu_trend(s, on, p)
        s = altbilgi_yayin(s, on)
        s = gizlilik_ekle(s, on)
        s = surumle(s)
        s = varlik_surumu(s, kok)
        s = tablo_sar(s)
        s = ilk_gorsel_oncelik(s)
        s = varlik_kat(s, p, kok)
        s = belge_ekle(s, yol, on)
        if s != o:
            io.open(yol, "w", encoding="utf-8").write(s)
            degisen += 1
    # başlık/H1/giriş/meta: arayanın diliyle hizala
    try:
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from pusula import terimler
        terimler.calistir(kok)
    except Exception as ex:
        print("terimler:", ex)
    # ana hizmet sayfaları → il sayfaları bağlantı bloğu
    try:
        import il_baglari
        il_baglari.calistir(kok)
    except Exception as ex:
        print("il_baglari:", ex)
    # ana hizmet sayfaları → sektör/alt tür sayfaları bağlantı bloğu
    try:
        import sektor_baglari
        print("sektor_baglari:", sektor_baglari.calistir(kok))
    except Exception as ex:
        print("sektor_baglari:", ex)
    # sayfa tipine göre başlık/H1/meta + fiyat bölümü: arayanın kalıbı (arama_hizala)
    try:
        from pusula import arama_hizala
        print("arama_hizala:", arama_hizala.calistir(kok))
    except Exception as ex:
        print("arama_hizala:", ex)
    # sitemap: .html'li adresleri canonical bicimine cek (yonlendirme -> dizin disi kalmasin)
    try:
        print("sitemap:", sitemap_uzantisizlastir(kok))
        print("sitemap-yeni:", sitemap_yeni_ekle(kok))
        print("sitemap-noindex:", sitemap_noindex_cikar(kok))
    except Exception as ex:
        print("sitemap:", ex)
    # il x hizmet sayfalari: ortak hizmet metnini incelt, ile ozel bolumleri ekle
    try:
        import yerelles
        print("yerelles:", yerelles.calistir(kok))
    except Exception as ex:
        print("yerelles:", ex)
    # llms.txt — yapay zeka asistanlarina sitenin duz metin haritasi
    try:
        import llms_luna
        print("llms.txt:", llms_luna.calistir(kok))
    except Exception as ex:
        print("llms.txt:", ex)
    # sitemap: dosyasi kalmayan adresleri dusur (yayindan kaldirilan sayfalar)
    try:
        print("sitemap-olu:", sitemap_olu_temizle(kok))
    except Exception as ex:
        print("sitemap-olu:", ex)
    return {"degisen_sayfa": degisen}


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from pusula.ayarlar import SITE_KOK
    print(calistir(SITE_KOK))
