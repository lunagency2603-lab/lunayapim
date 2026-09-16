# -*- coding: utf-8 -*-
"""
ÜRETİM SONRASI İŞLEM — her yeniden üretimde uygulanması gereken adımlar.

Neden var: bir sayfayı yeniden ürettiğimizde, üretici şablonunda olmayan
düzeltmeler siliniyordu. Uzantısız adresler geri .html oluyor, asistan
betiği düşüyor, tablo sarmalı kayboluyordu. Her seferinde elle toparlamak
yerine hepsi burada; üretimden sonra bir kez çalıştırılıyor.

Hepsi ETKİSİZ TEKRARLANABİLİR (idempotent): iki kez çalıştırmak zarar vermez.
"""
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


# AdSense yalnız yayın bölümlerinde: gündem, bülten, TrendSaphiens. Diğer sayfalarda betik varsa kaldırılır.
ADSENSE_BOLUM = ("gundem/", "bulten/", "trend/")


ADSENSE_ASGARI_KELIME = 500      # ince sayfada reklam gösterilmez (AdSense içerik ölçütü)


def _govde_kelime(s):
    t = re.sub(r"(?is)<(script|style|nav|header|footer|svg)[^>]*>.*?</\1>", " ", s)
    return len(re.sub(r"(?s)<[^>]+>", " ", t).split())


def adsense_ekle(s, p=""):
    """AdSense betiği yalnız ADSENSE_BOLUM altındaki YETERLİ İÇERİKLİ sayfaların <head>'ine.

    14.09.2026: liste/kapak sayfaları (bölüm indeksleri, sistem sayfaları) 350-440
    kelimeydi; reklam taşıyan ince sayfa AdSense'in "düşük değerli içerik"
    değerlendirmesini besliyor. Reklam artık yalnız yazı ve veri sayfalarında.
    """
    p = (p or "").replace(os.sep, "/")
    izinli = p.startswith(ADSENSE_BOLUM) and _govde_kelime(s) >= ADSENSE_ASGARI_KELIME
    if not izinli:
        s = re.sub(r'[ \t]*<script async src="https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js[^<]*</script>\n?', "", s)
        s = re.sub(r'\s*<div class="ts-reklam">.*?</div>\s*', "\n", s, flags=re.S)
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


def tablo_sar(s):
    """Dar ekranda tablo sayfayı yatay kaydırıyordu — kendi içinde kaysın."""
    return re.sub(r'(?<!<div class="tablo-kaydir">)<table\b[\s\S]*?</table>',
                  lambda m: '<div class="tablo-kaydir">' + m.group(0) + '</div>', s)


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
        if "/.git" in dizin or "/.otomasyon" in dizin:
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


def calistir(kok, desen="**/*.html"):
    degisen = 0
    for yol in glob.glob(os.path.join(kok, desen), recursive=True):
        p = os.path.relpath(yol, kok)
        if p.startswith(("assets", ".git")) or p in ("matrix.html", "admin.html"):
            continue
        s = io.open(yol, encoding="utf-8").read()
        o = s
        on = _derinlik(yol, kok)
        s = uzantisizlastir(s)
        s = asistan_ekle(s, on)
        s = ajan_ekle(s, on)
        s = okuma_ekle(s, on)
        s = adsense_ekle(s, p)
        s = menu_trend(s, on, p)
        s = altbilgi_yayin(s, on)
        s = gizlilik_ekle(s, on)
        s = surumle(s)
        s = tablo_sar(s)
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
    except Exception as ex:
        print("sitemap:", ex)
    # il x hizmet sayfalari: ortak hizmet metnini incelt, ile ozel bolumleri ekle
    try:
        import yerelles
        print("yerelles:", yerelles.calistir(kok))
    except Exception as ex:
        print("yerelles:", ex)
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
