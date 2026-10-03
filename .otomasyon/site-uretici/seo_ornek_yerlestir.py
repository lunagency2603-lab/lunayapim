# -*- coding: utf-8 -*-
"""
SEO örnek sayfalarını mevcut canlı sayfa kabuğuna yerleştirir (02.10.2026).

Neden ayrı adım: hizmetler/seo-icerik.html üreticiden çıktıktan sonra başka
adımlarla (video, hizmet özeti, menü, görsel öznitelikleri) zenginleşti;
üreticiyi yeniden çalıştırmak bunları siler. Bu betik var olan sayfaya yalnız
gereken parçayı ekler ve yeni örnek sayfaları aynı kabuktan üretir.
Tekrar çalıştırılırsa aynı sonucu verir (idempotent).

Kullanım: python3 seo_ornek_yerlestir.py <site-kökü>
"""
import os, re, sys, json, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seo_ornekleri as SO

ISARET = "<!-- seo-ornekleri -->"


def _oku(p):
    return open(p, encoding="utf-8").read()


def _yaz(p, s):
    open(p, "w", encoding="utf-8").write(s)


def _govde(sayfa_html):
    """Üretici çıktısından hero + gövde + cta kısmını (page-hero → footer) al."""
    a = sayfa_html.index('<div class="page-hero">')
    b = sayfa_html.index("<footer>")
    return sayfa_html[a:b]


def _semalar(sayfa_html):
    return re.findall(r'<script type="application/ld\+json">.*?</script>', sayfa_html, re.S)


def _meta(sayfa_html, ad):
    if ad == "title":
        return re.search(r"<title>(.*?)</title>", sayfa_html, re.S).group(1)
    return re.search(r'<meta name="%s" content="(.*?)">' % ad, sayfa_html).group(1)


def ornek_sayfa(sablon, uretilen, dosya):
    """Şablonun head/menü/footer'ını koru; başlık, açıklama, şema, gövdeyi değiştir."""
    url = "https://lunayapim.com/hizmetler/" + dosya.replace(".html", "")
    s = sablon
    baslik = _meta(uretilen, "title")
    acik = _meta(uretilen, "description")
    anahtar = _meta(uretilen, "keywords")
    s = re.sub(r"<title>.*?</title>", "<title>%s</title>" % baslik, s, 1, re.S)
    s = re.sub(r'<meta name="description" content=".*?">',
               '<meta name="description" content="%s">' % acik, s, 1)
    s = re.sub(r'<meta name="keywords" content=".*?">',
               '<meta name="keywords" content="%s">' % anahtar, s, 1)
    s = re.sub(r'<link rel="canonical" href=".*?">', '<link rel="canonical" href="%s">' % url, s, 1)
    s = re.sub(r'<meta property="og:title" content=".*?">',
               '<meta property="og:title" content="%s">' % baslik, s, 1)
    s = re.sub(r'<meta property="og:description" content=".*?">',
               '<meta property="og:description" content="%s">' % acik, s, 1)
    s = re.sub(r'<meta property="og:url" content=".*?">',
               '<meta property="og:url" content="%s">' % url, s, 1)
    # şablonun bütün JSON-LD bloklarını sök, üretilenleri koy
    eski = _semalar(s)
    ilk = s.index(eski[0])
    for x in eski:
        s = s.replace(x, "", 1)
    s = s[:ilk] + "\n".join(_semalar(uretilen)) + s[ilk:]
    s = re.sub(r"\n{3,}", "\n\n", s)
    # gövde: şablonun page-hero → footer arasını üretilenle değiştir
    a = s.index('<div class="page-hero">')
    b = s.index("<footer>")
    s = s[:a] + _govde(uretilen) + s[b:]
    return s


def mevcut_sayfa_guncelle(p, tur):
    s = _oku(p)
    kart = ISARET + SO.kart_bolumu() + ISARET
    if ISARET in s:  # yeniden çalıştırma: eski kartı yenisiyle değiştir
        s = re.sub(re.escape(ISARET) + ".*?" + re.escape(ISARET), lambda m: kart, s, 1, re.S)
    elif tur == "seo":
        s = s.replace("<h2>Neyle ölçüyoruz</h2>", kart + "\n<h2>Neyle ölçüyoruz</h2>", 1)
    else:
        s = s.replace("<h2>Süreç</h2>", kart + "\n<h2>Süreç</h2>", 1)
    if tur == "seo":
        eski = ("326 sayfayı kendi denetçimizden geçirdik, 385 uyarıyı sıfıra indirdik ve sonucu "
                "şeffaflık sayfamızda yayınlıyoruz.")
        yeni = ("Google dizinindeki sayfa sayımızı 31 Ağustos'taki 27'den 2 Ekim'de 470'e "
                "çıkardık; arama tıklaması son 3 ayda 8'den son 28 günde 43'e yükseldi. "
                "Düşüşler dahil bütün rakamları kaynağıyla örnek sayfamızda yayınlıyoruz.")
        s = s.replace(eski, yeni)
        s = s.replace('<p><a href="../seffaflik">Kendi sitemizin ölçüm sonuçlarını</a> ve '
                      '<a href="../fiyatlar">fiyat aralıklarını</a> açıkça yayınlıyoruz.</p>',
                      '<p>Örnekler: <a href="seo-ornegi-lunayapim">lunayapim.com</a> · '
                      '<a href="seo-ornegi-trendsaphiens">trendsaphiens.com</a>. '
                      '<a href="../seffaflik">Kendi ölçüm sonuçlarımızı</a> ve '
                      '<a href="../fiyatlar">fiyat aralıklarını</a> açıkça yayınlıyoruz.</p>')
        s = s.replace("<b>331 sayfa</b><span>denetimden geçti, hata sıfır</span>",
                      "<b>470 sayfa</b><span>Google dizininde (2 Ekim 2026)</span>")
    else:
        ek = ("<li><strong>Yapay zekâ erişimi</strong> — llms.txt dosyası, yapay zekâ "
              "tarayıcılarının engellenmemesi, robots.txt'de içerik kullanım tercihi "
              "(Content-Signal) ve istendiğinde sayfanın düz metin (Markdown) sürümü</li>"
              "<li><strong>Ölçüm</strong> — hangi yapay zekâ tarayıcısının siteyi ne sıklıkla "
              "okuduğu (Cloudflare) ve ChatGPT gibi asistanlardan gelen ziyaretçi sayısı "
              "(Google Analytics) her ay raporda</li>")
        if "Yapay zekâ erişimi</strong>" not in s:
            s = s.replace("duran site bu sistemlerde de geri düşüyor</li></ul>",
                          "duran site bu sistemlerde de geri düşüyor</li>" + ek + "</ul>", 1)
        s = s.replace('<p>Klasik tarafı <a href="seo-icerik">SEO ve içerik sayfamızda</a>, '
                      'kendi ölçümlerimiz <a href="../seffaflik">şeffaflık sayfamızda</a>.</p>',
                      '<p>Klasik tarafı <a href="seo-icerik">SEO ve içerik sayfamızda</a>; '
                      'ölçülmüş örnekler: <a href="seo-ornegi-lunayapim">lunayapim.com</a> ve '
                      '<a href="seo-ornegi-trendsaphiens">trendsaphiens.com</a>.</p>')
    _yaz(p, s)


def calistir(kok):
    hz = os.path.join(kok, "hizmetler")
    sablon = _oku(os.path.join(hz, "seo-icerik.html"))
    for dosya, uretilen in SO.hepsi():
        _yaz(os.path.join(hz, dosya), ornek_sayfa(sablon, uretilen, dosya))
    mevcut_sayfa_guncelle(os.path.join(hz, "seo-icerik.html"), "seo")
    mevcut_sayfa_guncelle(os.path.join(hz, "yapay-zeka-seo.html"), "ai")
    # site haritası: yoksa ekle
    sm = os.path.join(kok, "sitemap.xml")
    x = _oku(sm)
    for dosya, _ in SO.hepsi():
        loc = "https://lunayapim.com/hizmetler/" + dosya.replace(".html", "")
        if "<loc>%s</loc>" % loc not in x:
            x = x.replace("</urlset>", "  <url><loc>%s</loc><lastmod>%s</lastmod>"
                          "<changefreq>monthly</changefreq><priority>0.8</priority></url>\n</urlset>"
                          % (loc, SO.GUNCEL))
    _yaz(sm, x)
    return {"ornek": [d for d, _ in SO.hepsi()]}


if __name__ == "__main__":
    print(calistir(sys.argv[1] if len(sys.argv) > 1 else "."))
