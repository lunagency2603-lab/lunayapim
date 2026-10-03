# -*- coding: utf-8 -*-
"""
SEO hizmetinin gerçek örnekleri — kendi iki sitemizde ölçülmüş sonuçlar.

02.10.2026 gerekçesi: seo-icerik ve yapay-zeka-seo sayfaları ne yaptığımızı
anlatıyordu ama örnek göstermiyordu. Müşteri işi örnek göstermek müşterinin
iznine bağlı; bu yüzden ilk iki örnek kendi sitelerimiz. Her rakam bir
kaynaktan, tarihiyle okundu (Search Console, Google Analytics 4, Cloudflare
AI Crawl Control). Rakam güzelleştirilmiyor; düşüş varsa o da yazılıyor.

Rakam güncellenecekse yalnız VERI sözlüğü değişir; metin oradan beslenir.
"""
from kabuk import head, FOOTER
from uretici import KOK, e, j, sss_blok, cta, kisa_baslik, meta_desc

GUNCEL = "2026-10-02"
GUNCEL_TR = "2 Ekim 2026"

VERI = {
  "luna": {
    "dizin": [("31 Ağustos 2026", "27"), ("14 Eylül 2026", "266"), ("2 Ekim 2026", "470")],
    "harita": "569",
    "tik_once": "8 tıklama (son 3 ay, 31 Ağustos'ta okundu)",
    "tik_simdi": "43 tıklama, 698 gösterim (2–29 Eylül, 28 gün)",
    "ctr": "%6,2", "sira": "14,6",
    "ai_7gun": "2.340", "perplexity": "528", "chatgpt": "204", "claude": "80",
    "googlebot": "608", "bing": "197",
    "chatgpt_oturum": "66", "google_oturum": "56",
  },
  "ts": {
    "dizin": "61", "dizin_disi": "131",
    "gosterim": "680", "tik": "9", "sira": "22,3",
    "en_cok": ("Yükselen burç hesaplama", "181"),
    "ai_24s": "375", "chatgpt": "87", "claude": "29", "perplexity": "24",
    "breadcrumb": "28",
  },
}


def _sema(tur, **k):
    d = {"@context": "https://schema.org", "@type": tur}
    d.update(k)
    return d


def _tablo(basliklar, satirlar):
    g = ['<div class="tablo-kaydir"><table>',
         "<tr>%s</tr>" % "".join("<th>%s</th>" % e(b) for b in basliklar)]
    for s in satirlar:
        g.append("<tr>%s</tr>" % "".join("<td>%s</td>" % h for h in s))
    g.append("</table></div>")
    return "\n".join(g)


def _kabuk(dosya, baslik, aciklama, anahtar, h1, lede, govde, ad):
    url = "%s/hizmetler/%s" % (KOK, dosya.replace(".html", ""))
    semalar = [
      _sema("BreadcrumbList", itemListElement=[
        {"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": KOK + "/"},
        {"@type": "ListItem", "position": 2, "name": "Prodüksiyon", "item": KOK + "/hizmetler/"},
        {"@type": "ListItem", "position": 3, "name": "SEO ve İçerik",
         "item": KOK + "/hizmetler/seo-icerik"},
        {"@type": "ListItem", "position": 4, "name": ad, "item": url}]),
      _sema("Article", headline=kisa_baslik(baslik, 110), description=aciklama,
            datePublished=GUNCEL, dateModified=GUNCEL, inLanguage="tr", url=url,
            mainEntityOfPage=url, image=KOK + "/assets/og-image.png",
            author={"@type": "Organization", "name": "Luna Yapım", "url": KOK},
            publisher={"@type": "Organization", "name": "Luna Yapım",
                       "logo": {"@type": "ImageObject", "url": KOK + "/assets/karga.png"}},
            about={"@type": "Service", "name": "SEO ve yapay zekâ görünürlüğü",
                   "url": KOK + "/hizmetler/seo-icerik"}),
    ]
    s = "\n".join('<script type="application/ld+json">\n%s\n</script>' % j(x) for x in semalar)
    g = head(e(kisa_baslik(baslik)), e(meta_desc(aciklama)), e(anahtar), url, s)
    g += """<div class="page-hero">
  <img class="karga-buyuk" src="../assets/karga.png" alt="">
  <div class="wrap">
    <div class="crumbs"><a href="../">Ana Sayfa</a> ·
      <a href="./">Prodüksiyon</a> · <a href="seo-icerik">SEO ve İçerik</a> · %s</div>
    <h1>%s</h1>
    <p class="lede">%s</p>
  </div>
</div>

""" % (e(ad), h1, e(lede))
    return g + govde + FOOTER


def kart_bolumu(kok=""):
    """seo-icerik ve yapay-zeka-seo sayfalarına giren 'Gerçek örnekler' bölümü."""
    L, T = VERI["luna"], VERI["ts"]
    return ("<h2>Gerçek örnekler</h2>"
            "<p>Müşteri işini müşterinin izni olmadan yayınlamıyoruz. Bu yüzden ilk iki örnek "
            "kendi sitelerimiz: aynı denetimi, aynı ölçümü kendimize uyguladık ve rakamları "
            "kaynağıyla yazdık.</p>"
            '<div class="paketler">'
            '<div class="paket"><h3><a href="%sseo-ornegi-lunayapim">lunayapim.com</a></h3>'
            "<p>Hizmet sitesi · Bursa merkezli, 81 il</p><ul>"
            "<li>Google dizininde %s → <strong>%s sayfa</strong> (%s → %s)</li>"
            "<li>Son 28 günde %s</li>"
            "<li>Yapay zekâ tarayıcılarından 7 günde %s istek</li>"
            "<li>Eylülde ChatGPT'den gelen ziyaret (%s) Google aramadan gelenden (%s) fazla</li>"
            "</ul></div>"
            '<div class="paket"><h3><a href="%sseo-ornegi-trendsaphiens">trendsaphiens.com</a></h3>'
            "<p>İçerik ve haber sitesi · Eylül 2026'da yeni alan adı</p><ul>"
            "<li>İlk haftalarda <strong>%s sayfa</strong> dizinde</li>"
            "<li>16 günde %s gösterim, %s tıklama</li>"
            "<li>Yapay zekâ tarayıcılarından 24 saatte %s istek</li>"
            "<li>AdSense için site incelemesinde, ads.txt onaylı</li>"
            "</ul></div></div>"
            % (kok, L["dizin"][0][1], L["dizin"][-1][1], L["dizin"][0][0].rsplit(" ", 1)[0],
               L["dizin"][-1][0].rsplit(" ", 1)[0], L["tik_simdi"].split(" (")[0],
               L["ai_7gun"], L["chatgpt_oturum"], L["google_oturum"],
               kok, T["dizin"], T["gosterim"], T["tik"], T["ai_24s"]))


def ornek_lunayapim():
    L = VERI["luna"]
    g = ['<section><div class="wrap prose">']
    g.append('<div class="kutu"><p><strong>Kısaca:</strong> 31 Ağustos 2026\'da Google dizininde '
             '%s sayfamız vardı; %s itibarıyla <strong>%s</strong>. Arama tıklaması son 3 ayda 8\'den '
             'son 28 günde 43\'e çıktı. Yapay zekâ asistanları siteyi düzenli tarıyor ve '
             'Eylül\'de ChatGPT\'den gelen ziyaretçi, Google aramadan gelenden fazlaydı. '
             'Tüm rakamlar aşağıda, kaynağı ve okunduğu tarihle.</p></div>'
             % (L["dizin"][0][1], GUNCEL_TR, L["dizin"][-1][1] + " sayfa"))
    g.append("<h2>Başlangıç noktası</h2>")
    g.append("<p>Ağustos sonunda site yayındaydı ama Google onu neredeyse görmüyordu. Site "
             "haritası 1 Temmuz'da gönderilmiş, Google 5 Temmuz'dan beri okumamıştı; 331 "
             "sayfanın yalnızca 24'ü keşfedilmişti. Search Console'da son 3 ayın toplamı 8 "
             "tıklamaydı.</p>")
    g.append("<h2>Ne yaptık</h2>")
    g.append("<ul>"
             "<li><strong>Taranabilirlik:</strong> Site haritasını yeniden gönderdik; aynı gün "
             "okundu ve keşfedilen sayfa 24'ten 331'e çıktı. 421 iç bağlantının eski uzantılı "
             "adrese gidip her taramada yönlendirmeye düştüğünü bulup düzelttik.</li>"
             "<li><strong>Yapılandırılmış veri:</strong> Her sayfaya JSON-LD (Service, FAQPage, "
             "BreadcrumbList, Article) ekledik; sameAs ile sosyal hesapları bağladık.</li>"
             "<li><strong>Arayanın diliyle başlık:</strong> 331 il sayfasının başlık ve "
             "açıklamasını Search Console'daki gerçek sorgulara göre yeniden yazdık; 648 "
             "başlık ve açıklamanın hepsi benzersiz.</li>"
             "<li><strong>Yapay zekâ erişimi:</strong> llms.txt yayınladık, yapay zekâ "
             "tarayıcılarını engellemedik, içerik kullanım tercihlerini robots.txt'ye yazdık "
             "ve yapay zekâ ajanlarının istediğinde sayfaları düz metin (Markdown) olarak "
             "sunduk.</li>"
             "<li><strong>Ölçüm:</strong> Telefon, WhatsApp ve form tıklamalarını Google "
             "Analytics'te ayrı ölçüyoruz; kendi ziyaretlerimizi raporlardan ayıklıyoruz.</li>"
             "</ul>")
    g.append("<h2>Google dizini</h2>")
    g.append(_tablo(["Tarih", "Dizindeki sayfa", "Kaynak"],
                    [(d, "<strong>%s</strong>" % n, "Search Console · Sayfa dizine ekleme")
                     for d, n in L["dizin"]]))
    g.append("<p>Site haritasında %s adres var ve Google onu düzenli okuyor (son okuma 30 "
             "Eylül). Dizin dışı kalan sayfaların çoğu bilerek kalıcı yönlendirme yaptığımız "
             "eski adresler; bunlar dizine girmez, girmesi de gerekmez.</p>" % L["harita"])
    g.append("<h2>Arama performansı</h2>")
    g.append(_tablo(["Dönem", "Sonuç", "Kaynak"],
                    [("Ağustos sonu (son 3 ay)", L["tik_once"], "Search Console"),
                     ("2–29 Eylül 2026", L["tik_simdi"], "Search Console"),
                     ("Aynı dönem", "Tıklama oranı %s · ortalama sıra %s" % (L["ctr"], L["sira"]),
                      "Search Console")]))
    g.append("<p><strong>Düşüş de var, saklamıyoruz:</strong> 20 Eylül'den sonra il "
             "sayfalarının gösterimi belirgin biçimde azaldı; tıklama ise neredeyse aynı kaldı, "
             "çünkü kaybolan gösterimlerin çoğu 50.–90. sıradaki, zaten tıklanmayan "
             "aramalardı. Bunu bir haftada çok sayıda sayfa ekleyip yeniden yazmamıza bağlıyoruz "
             "ve izliyoruz. Ders: yeni sayfaları tek seferde değil, parça parça yayınlamak.</p>")
    g.append("<h2>Yapay zekâ görünürlüğü</h2>")
    g.append(_tablo(["Ölçüm", "Değer", "Kaynak"],
                    [("Yapay zekâ tarayıcı isteği (son 7 gün)", "<strong>%s</strong>" % L["ai_7gun"],
                      "Cloudflare AI Crawl Control"),
                     ("PerplexityBot", L["perplexity"], "Cloudflare"),
                     ("ChatGPT-User (sohbette kullanıcı adına açılan sayfa)", L["chatgpt"], "Cloudflare"),
                     ("ClaudeBot ve Claude arama botları", L["claude"], "Cloudflare"),
                     ("Googlebot / Bingbot", "%s / %s" % (L["googlebot"], L["bing"]), "Cloudflare"),
                     ("ChatGPT'den gelen ziyaret · Google aramadan gelen ziyaret (Eylül, 28 gün)",
                      "%s · %s" % (L["chatgpt_oturum"], L["google_oturum"]), "Google Analytics 4")]))
    g.append("<p>ChatGPT-User satırı önemli: bu, bir kişinin ChatGPT'ye soru sorduğu ve "
             "ChatGPT'nin cevap için sayfamızı açtığı anlamına geliyor. Yapay zekâ "
             "aramalarında görünmek tam olarak bu.</p>")
    g.append("<h2>Neyi henüz başaramadık</h2>")
    g.append("<ul><li>Bursa'daki rekabetli aramalarda (ör. \"bursa drone çekimi\") henüz ilk "
             "sayfada değiliz; bu aramalarda Haritalar'daki işletme profilleri ve yorum "
             "sayısı belirleyici.</li>"
             "<li>Google İşletme Profilimiz doğrulama aşamasında.</li></ul>")
    g.append("<p>Bu sayfadaki rakamlar %s tarihinde okundu ve düzenli güncelleniyor. "
             "Aynı denetimi sizin sitenize de uyguluyoruz: "
             '<a href="seo-icerik">SEO ve içerik</a> · '
             '<a href="yapay-zeka-seo">Yapay zekâ destekli SEO</a> · '
             '<a href="seo-ornegi-trendsaphiens">İkinci örnek: trendsaphiens.com</a></p>' % GUNCEL_TR)
    g.append("</div></section>\n")
    g.append(cta({"slug": "seo"}, "Aynı ölçümü <i>sizin sitenize</i> yapalım.",
                 "Sitenizin adresini yazın; dizin, arama ve yapay zekâ görünürlüğünü kaynaklarıyla gönderelim."))
    return "seo-ornegi-lunayapim.html", _kabuk(
        "seo-ornegi-lunayapim.html",
        "SEO Örneği: lunayapim.com — 27'den 470 Dizinli Sayfaya | Luna Yapım",
        "Kendi sitemizde ölçülmüş SEO sonucu: Google dizininde 27'den 470 sayfaya, son 28 günde "
        "43 tıklama, 7 günde 2.340 yapay zekâ tarayıcı isteği. Kaynaklı ve tarihli.",
        "seo örneği, seo vaka çalışması, yapay zeka seo örneği, bursa seo, google dizin, "
        "search console, chatgpt görünürlük",
        "SEO örneği: <i>lunayapim.com</i>",
        "Kendi sitemize uyguladığımız SEO ve yapay zekâ görünürlüğü çalışması — ne yaptık, "
        "rakamlar ne dedi, neyi henüz başaramadık.",
        "\n".join(g), "Örnek: lunayapim.com")


def ornek_trendsaphiens():
    T = VERI["ts"]
    g = ['<section><div class="wrap prose">']
    g.append('<div class="kutu"><p><strong>Kısaca:</strong> trendsaphiens.com Eylül 2026\'da yeni '
             'alan adına taşınan bir içerik sitesi. İlk haftalarda <strong>%s sayfası</strong> '
             'Google dizinine girdi, 16 günde %s gösterim aldı ve yapay zekâ tarayıcıları '
             'siteyi her gün ziyaret ediyor. Rakamlar %s tarihinde okundu.</p></div>'
             % (T["dizin"], T["gosterim"], GUNCEL_TR))
    g.append("<h2>Durum</h2>")
    g.append("<p>Yeni bir alan adı Google'ın gözünde geçmişi olmayan bir sitedir; ilk "
             "haftalar hem tarama hem güven açısından en zor dönem. Hedefimiz sayfaların hızla "
             "keşfedilmesi, doğru sayfaların dizine girmesi ve sitenin reklam yayınlamaya "
             "(AdSense) uygun hâle gelmesiydi.</p>")
    g.append("<h2>Ne yaptık</h2>")
    g.append("<ul>"
             "<li><strong>Tek kalıcı sayfa ilkesi:</strong> Her gün yeni tarihli sayfa açmak yerine "
             "\"dolar kaç TL bugün\" gibi sorular için her gün güncellenen tek sayfa kurduk; "
             "eski günlük sayfaları dizin dışı bıraktık. Sıralama gücü tek adreste birikiyor.</li>"
             "<li><strong>İnce içeriği ayıkladık:</strong> 400 kelimenin altındaki sayfalarda reklam "
             "göstermiyoruz; rehber yazıları 500–760 özgün kelimeye genişlettik.</li>"
             "<li><strong>Yapılandırılmış veri:</strong> Haber ve rehberlerde Article, FAQPage ve "
             "BreadcrumbList şemaları; Search Console'da %s geçerli içerik haritası (breadcrumb) "
             "kaydı.</li>"
             "<li><strong>Gizlilik ve reklam uyumu:</strong> Gizlilik sayfasında üçüncü taraf "
             "çerez açıklaması, rıza mesajı ve ads.txt.</li>"
             "<li><strong>Yapay zekâ erişimi:</strong> llms.txt, açık robots kuralları ve "
             "yapay zekâ tarayıcılarına izin.</li>"
             "</ul>" % T["breadcrumb"])
    g.append("<h2>Rakamlar</h2>")
    g.append(_tablo(["Ölçüm", "Değer", "Kaynak"],
                    [("Dizindeki sayfa", "<strong>%s</strong> (dizin dışı %s)" % (T["dizin"], T["dizin_disi"]),
                      "Search Console"),
                     ("Gösterim / tıklama (14–29 Eylül)", "%s / %s" % (T["gosterim"], T["tik"]),
                      "Search Console"),
                     ("Ortalama sıra", T["sira"], "Search Console"),
                     ("En çok gösterim alan sayfa", "%s · %s gösterim" % T["en_cok"], "Search Console"),
                     ("Yapay zekâ tarayıcı isteği (son 24 saat)", "<strong>%s</strong>" % T["ai_24s"],
                      "Cloudflare AI Crawl Control"),
                     ("ChatGPT-User / Claude / Perplexity", "%s / %s / %s"
                      % (T["chatgpt"], T["claude"], T["perplexity"]), "Cloudflare"),
                     ("AdSense", "ads.txt onaylı · site incelemede", "Google AdSense")]))
    g.append("<p><strong>Dürüst not:</strong> Tıklama henüz düşük (16 günde %s). Yeni alan "
             "adında ortalama sıra 20'nin altına inmeden tıklama artmıyor; şu an %s. Bu sitenin "
             "asıl sınavı önümüzdeki iki ay.</p>" % (T["tik"], T["sira"]))
    g.append('<p><a href="seo-ornegi-lunayapim">Birinci örnek: lunayapim.com</a> · '
             '<a href="seo-icerik">SEO ve içerik hizmeti</a> · '
             '<a href="yapay-zeka-seo">Yapay zekâ destekli SEO</a></p>')
    g.append("</div></section>\n")
    g.append(cta({"slug": "seo"}, "Yeni sitenizi <i>doğru başlatalım</i>.",
                 "Alan adı taşıma, dizine girme ve reklam uygunluğunu baştan planlayalım."))
    return "seo-ornegi-trendsaphiens.html", _kabuk(
        "seo-ornegi-trendsaphiens.html",
        "SEO Örneği: trendsaphiens.com, Yeni Alan Adı | Luna Yapım",
        "Yeni alan adına taşınan içerik sitesinde ilk haftalar: 61 sayfa Google dizininde, 16 "
        "günde 680 gösterim, günde 375 yapay zekâ tarayıcı isteği, AdSense incelemesi.",
        "seo örneği, yeni alan adı seo, içerik sitesi seo, adsense onayı, yapay zeka "
        "görünürlüğü, search console",
        "SEO örneği: <i>trendsaphiens.com</i>",
        "Yeni alan adına taşınan bir içerik sitesinin ilk haftaları: dizine girme, reklam "
        "uyumu ve yapay zekâ görünürlüğü.",
        "\n".join(g), "Örnek: trendsaphiens.com")


def hepsi():
    return [ornek_lunayapim(), ornek_trendsaphiens()]
