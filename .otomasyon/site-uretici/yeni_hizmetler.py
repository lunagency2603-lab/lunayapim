# -*- coding: utf-8 -*-
"""Yeni hizmet sayfaları: SEO & içerik, yapay zekâ destekli SEO, AI kısa film."""
import os, datetime
from kabuk import head, FOOTER
from uretici import KOK, e, j, sss_blok, cta, video_bolumu, kisa_baslik, meta_desc


def _sema(tur, **k):
    d = {"@context": "https://schema.org", "@type": tur}
    d.update(k)
    return d


def _hizmet_kabugu(dosya, baslik_seo, aciklama, anahtar, h1, lede, govde, hizmet_adi,
                   sss=(), fiyat=None):
    url = "%s/hizmetler/%s" % (KOK, dosya)
    semalar = [
      _sema("BreadcrumbList", itemListElement=[
        {"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": KOK + "/"},
        {"@type": "ListItem", "position": 2, "name": "Prodüksiyon",
         "item": KOK + "/hizmetler/"},
        {"@type": "ListItem", "position": 3, "name": hizmet_adi, "item": url}]),
      _sema("Service", name=hizmet_adi, description=aciklama, url=url,
            serviceType=hizmet_adi, areaServed={"@type": "Country", "name": "Türkiye"},
            provider={"@type": "Organization", "name": "Luna Yapım", "url": KOK},
            **({"offers": {"@type": "Offer", "priceCurrency": "TRY",
                           "priceSpecification": {"@type": "PriceSpecification",
                                                  "minPrice": fiyat[0], "maxPrice": fiyat[1],
                                                  "priceCurrency": "TRY"}}} if fiyat else {})),
    ]
    if sss:
        semalar.append(_sema("FAQPage", mainEntity=[
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in sss]))
    s = "\n".join('<script type="application/ld+json">\n%s\n</script>' % j(x) for x in semalar)
    g = head(e(kisa_baslik(baslik_seo)), e(meta_desc(aciklama)), e(anahtar), url, s)
    g += """<div class="page-hero">
  <img class="karga-buyuk" src="../assets/karga.png" alt="">
  <div class="wrap">
    <div class="crumbs"><a href="../">Ana Sayfa</a> ·
      <a href="./">Prodüksiyon</a> · %s</div>
    <h1>%s</h1>
    <p class="lede">%s</p>
  </div>
</div>

""" % (e(hizmet_adi), h1, e(lede))
    g += govde
    g += FOOTER
    return g


def _surec(adimlar):
    g = ['<div class="surec">']
    for i, (b, p) in enumerate(adimlar, 1):
        g.append('<div class="adim"><span class="n">%02d</span><div><b>%s</b><p>%s</p></div></div>'
                 % (i, e(b), e(p)))
    g.append("</div>")
    return "\n".join(g)


def _paketler(paketler):
    g = ['<div class="paketler">']
    for ad, alt, maddeler in paketler:
        g.append('<div class="paket"><h3>%s</h3><p>%s</p><ul>%s</ul></div>'
                 % (e(ad), e(alt), "".join("<li>%s</li>" % e(m) for m in maddeler)))
    g.append("</div>")
    return "\n".join(g)


# ══════════════════════════════════════════════════════════════ SEO & İÇERİK
def seo_icerik():
    sss = [
     ("SEO'da garanti veriyor musunuz?",
      "Hayır, ve veren varsa uzak durun — sıralamayı Google belirliyor, hiçbir ajans "
      "garanti edemez. Bizim garantimiz süreçte: her ay ne yaptığımızı, neyin değiştiğini "
      "ve rakamların nereden okunduğunu yazılı veriyoruz."),
     ("Ne kadar sürede sonuç alınır?",
      "Teknik düzeltmelerin etkisi 2–6 hafta içinde görülüyor. İçerik tarafında ilk anlamlı "
      "kıyas üçüncü ayda yapılabiliyor. İlk ay ölçüm ayıdır; taban çizgisi o ay yazılır."),
     ("Kendi sitemizde ne yaptınız?",
      "326 sayfayı kendi denetçimizden geçirdik, 385 uyarıyı sıfıra indirdik ve sonucu "
      "şeffaflık sayfamızda yayınlıyoruz. Kendi eksiğini yazmayan bir ajansın sizin "
      "eksiğinizi doğru söylemesi beklenemez."),
     ("İçeriği siz mi yazıyorsunuz?",
      "İskeleti ve araştırmayı biz kuruyoruz; metni birlikte yazıyoruz. Sizin işinizi "
      "sizden iyi bilen yok — yapay zekâyla doldurulmuş, kimsenin okumadığı içerik "
      "üretmiyoruz. Google da bunu 'yararsız içerik' olarak değerlendiriyor."),
     ("Sadece SEO alabilir miyiz, video olmadan?",
      "Evet. Ama şunu da söyleyelim: yerel aramada en hızlı kazanç genelde harita "
      "profilindeki fotoğraf ve videodan geliyor. Gerekmiyorsa 'gerekmiyor' demek de "
      "bizim işimiz."),
    ]
    g = ['<section><div class="wrap prose">']
    g.append("<h2>Neyi düzeltiyoruz</h2>")
    g.append("<p>SEO'yu üç ayrı iş olarak ele alıyoruz. Çoğu ajans yalnızca üçüncüsünü "
             "yapıyor; asıl kayıp ilk ikisinde oluyor.</p>")
    g.append('<div class="kiyas"><div class=\"tablo-kaydir\"><table>'
             '<tr><th>Katman</th><th>Ne yapılıyor</th><th>Etkisi ne zaman görülüyor</th></tr>'
             '<tr><td><strong>Teknik</strong></td><td>Başlık ve açıklama düzeni, şema (JSON-LD), '
             'canonical, sitemap, sayfa hızı, mobil düzen, iç bağlantı mimarisi</td>'
             '<td>2–6 hafta</td></tr>'
             '<tr><td><strong>Dönüşüm</strong></td><td>Eylem çağrısı, tıklanabilir telefon, '
             'WhatsApp butonu, form, fiyat sinyali — gelen ziyaretçinin müşteriye dönmesi</td>'
             '<td>Hemen</td></tr>'
             '<tr><td><strong>İçerik</strong></td><td>Hizmet sayfaları, şehir sayfaları, '
             'SSS, blog; aranan sorulara gerçek cevap</td><td>2–4 ay</td></tr>'
             "</table></div>")
    g.append("<h2>Neyle ölçüyoruz</h2>")
    g.append("<p>44 kontrolden geçen bir denetim çalıştırıyoruz ve sonucu beş başlıkta "
             "notluyoruz: ziyaretçiyi müşteriye çevirme, güven verme, aramada bulunma, "
             "görsel anlatım ve teknik altyapı. Her bulgunun yanında <strong>ne kontrol "
             "ettiğimiz, ne bulduğumuz ve hangi adreste baktığımız</strong> yazılı oluyor — "
             "tahmin yok.</p>")
    g.append("<h2>Süreç</h2>")
    g.append(_surec([
      ("Denetim", "44 kontrol, beş başlıkta karne. Sonuç kaynaklarıyla birlikte yazılı geliyor."),
      ("Öncelik sırası", "En çok kaybettiren başlıktan başlıyoruz; hepsini aynı anda değil."),
      ("Teknik düzeltme", "Şema, başlık düzeni, hız, iç bağlantı, sitemap ve dönüşüm unsurları."),
      ("İçerik", "Hizmet ve şehir sayfaları, SSS, blog. Aranan soruya gerçek cevap."),
      ("Ölçüm", "Search Console ve harita profili verisi her ay okunuyor; ne değişti yazılıyor."),
      ("Devam kararı", "Üçüncü ayda taban çizgisiyle kıyas. Rakam ikna etmezse devam etmiyorsunuz."),
    ]))
    g.append("<h2>Paketler</h2>")
    g.append(_paketler([
      ("Denetim", "Tek seferlik, karar vermeden önce",
       ["44 kontrolde tam denetim", "Beş başlıkta karne", "Kanıtlı eksik listesi",
        "Öncelik sırası ve tahmini etki", "Rapor sizde kalır — kendi ekibinizle de uygularsınız"]),
      ("Teknik düzeltme", "Sitesi olan ama görünmeyen firmalar",
       ["Şema, başlık, açıklama düzeni", "Hız ve mobil düzen", "İç bağlantı mimarisi",
        "Dönüşüm unsurları (CTA, form, WhatsApp)", "Sitemap ve tarama yönergeleri"]),
      ("Aylık SEO ve içerik", "Sürekli görünürlük gereken işler",
       ["Aylık içerik planı ve üretimi", "Hizmet/şehir sayfası genişletme",
        "Aylık ölçüm raporu", "Harita profili yönetimi", "Yeni sayfaların arama motorlarına bildirimi"]),
    ]))
    g.append("<h2>Sık sorulan sorular</h2>")
    g.append(sss_blok(sss))
    g.append('<p><a href="../seffaflik">Kendi sitemizin ölçüm sonuçlarını</a> ve '
             '<a href="../fiyatlar">fiyat aralıklarını</a> açıkça yayınlıyoruz.</p>')
    g.append("</div></section>\n")
    g.append(cta({"slug": "seo"}, "Sitenizi <i>denetleyelim</i>.",
                 "Ne bulduğumuzu kaynaklarıyla yazıp gönderelim — ücretsiz."))
    return "seo-icerik.html", _hizmet_kabugu(
        "seo-icerik.html", "SEO ve İçerik Hizmeti | Luna Yapım",
        "Teknik SEO, dönüşüm düzenlemesi ve içerik üretimi. 44 kontrolden geçen kanıtlı "
        "denetim, beş başlıkta karne ve aylık ölçüm raporu. Kendi sitemizin sonuçları açık.",
        "seo hizmeti, teknik seo, yerel seo, bursa seo, içerik üretimi, site denetimi, "
        "google işletme profili, arama motoru optimizasyonu",
        "<i>SEO</i> ve içerik",
        "Sıralama sözü vermiyoruz — ne yaptığımızı, neyin değiştiğini ve rakamın nereden "
        "okunduğunu yazılı veriyoruz. Aynı denetimi kendi sitemizde de çalıştırıp sonucunu "
        "yayınlıyoruz.",
        "\n".join(g), "SEO ve İçerik", sss)


# ══════════════════════════════════════════════════════ YAPAY ZEKÂ DESTEKLİ SEO
def yapay_zeka_seo():
    sss = [
     ("Yapay zekâ ile içerik mi üretiyorsunuz?",
      "Hayır — o iş ters tepiyor. Google'ın yararsız içerik değerlendirmesi tam olarak "
      "bunu hedefliyor. Yapay zekâyı ARAŞTIRMA ve ÖLÇÜM tarafında kullanıyoruz: hangi "
      "sorunun sorulduğunu, hangi sayfanın kapıda müşteri kaybettiğini, hangi gündemin "
      "sizin işinizle kesiştiğini bulmakta. Metni insan yazıyor."),
     ("Yapay zekâ arama motorlarında (AI Overviews, ChatGPT) çıkmak mümkün mü?",
      "Kısmen ve dolaylı olarak. Bu sistemler net cevabı olan, yapılandırılmış ve "
      "kaynak gösterilebilir içeriği tercih ediyor. Yaptığımız iş bu: soruya doğrudan "
      "cevap veren bölümler, FAQ şeması, tanımlı varlıklar. Garanti veren varsa inanmayın; "
      "bu alanda kimsenin garanti verebileceği bir mekanizma yok."),
     ("Bu hizmet klasik SEO'nun yerine mi geçiyor?",
      "Hayır, üstüne biniyor. Teknik temel ve içerik olmadan yapay zekâ katmanının "
      "tutunacağı bir şey olmuyor. Sitesi zayıf olan firmada önce temeli kuruyoruz."),
     ("Ne veriliyor elimize?",
      "Aylık: hangi sorularda görünüyorsunuz, hangi sayfa gösterim alıp tıklanmıyor, "
      "hangi sayfa ikinci sayfada takılı, gündemde sizin işinizle kesişen ne var. "
      "Hepsi tek sayfalık, okunabilir bir rapor."),
    ]
    g = ['<section><div class="wrap prose">']
    g.append('<div class="kutu"><p><strong>Önce dürüst olalım:</strong> "Yapay zekâ SEO" '
             'adı altında satılan şeylerin çoğu, yapay zekâya toplu metin yazdırıp siteye '
             'yığmaktan ibaret. Bu iş kısa vadede bile çalışmıyor; Google\'ın yararsız '
             'içerik değerlendirmesi doğrudan bunu hedefliyor. Biz yapay zekâyı '
             '<strong>içerik üretmekte değil, doğru işi bulmakta</strong> kullanıyoruz.</p></div>')
    g.append("<h2>Yapay zekâyı nerede kullanıyoruz</h2>")
    g.append('<div class="kiyas"><div class=\"tablo-kaydir\"><table>'
             '<tr><th>İş</th><th>Yapay zekâ ne yapıyor</th><th>İnsan ne yapıyor</th></tr>'
             '<tr><td>Denetim</td><td>44 kontrolü her sayfada çalıştırıyor, bulguları '
             'kanıtıyla topluyor</td><td>Hangi bulgunun gerçekten önemli olduğuna karar veriyor</td></tr>'
             '<tr><td>Arama verisi</td><td>Search Console verisini şehir ve hizmet '
             'kırılımına çeviriyor, fırsatları ayıklıyor</td><td>Hangi fırsatın peşine '
             'düşüleceğini seçiyor</td></tr>'
             '<tr><td>Gündem takibi</td><td>Günlük haberlerden işinizle kesişenleri buluyor '
             've yazı açısı öneriyor</td><td>Yazıyı yazıyor</td></tr>'
             '<tr><td>Rakip ve boşluk analizi</td><td>Hangi sorunun cevapsız kaldığını '
             'çıkarıyor</td><td>Cevabı üretiyor</td></tr>'
             '<tr><td>Görsel üretim</td><td>Kavram aşaması, varyasyon, storyboard</td>'
             '<td>Çekim, yönetim, kurgu, teslim</td></tr>'
             "</table></div>")
    g.append("<h2>Yapay zekâ aramalarına hazırlık</h2>")
    g.append("<p>Arama artık tek biçimde değil: klasik sonuç listesi, yapay zekâ özetleri "
             "ve sohbet arayüzleri bir arada. Bu sistemlerin ortak tercihi aynı: "
             "<strong>net cevabı olan, yapılandırılmış ve kaynak gösterilebilir</strong> içerik. "
             "Yaptığımız hazırlık şunlar:</p>")
    g.append("<ul>"
             "<li><strong>Soruya doğrudan cevap</strong> — her sayfada, ilk paragrafta, "
             "dolandırmadan</li>"
             "<li><strong>Yapılandırılmış veri</strong> — Service, FAQPage, LocalBusiness, "
             "Article şemaları; makinenin okuyabileceği biçimde</li>"
             "<li><strong>Varlık netliği</strong> — firma adı, hizmet adı, hizmet bölgesi "
             "her yerde aynı yazılıyor; sosyal hesaplar sameAs ile bağlanıyor</li>"
             "<li><strong>Kaynak gösterilebilirlik</strong> — rakam veriyorsak nereden "
             "geldiği yazılı; kaynağı olmayan iddia yazmıyoruz</li>"
             "<li><strong>Güncellik</strong> — tarih damgası ve düzenli güncelleme; "
             "duran site bu sistemlerde de geri düşüyor</li>"
             "</ul>")
    g.append('<div class="kutu"><p><strong>Garanti sözü yok.</strong> Yapay zekâ '
             'sistemlerinin hangi kaynağı seçtiği açıklanmıyor ve sık değişiyor. '
             'Yapabileceğimiz şey, seçilme ihtimalini artıran her koşulu sağlamak ve '
             'sonucu ölçmek. "AI aramalarında birinci sıra" diyen bir teklif alırsanız, '
             'o teklifin ölçemeyeceği bir şeyi sattığını bilin.</p></div>')
    g.append("<h2>Süreç</h2>")
    g.append(_surec([
      ("Tam denetim", "44 kontrol + yapılandırılmış veri kontrolü + varlık tutarlılığı."),
      ("Veri okuma", "Search Console dışa aktarımı şehir ve hizmet kırılımına çevriliyor."),
      ("Boşluk analizi", "Hangi soru cevapsız, hangi sayfa kapıda kaybediyor, hangisi ikinci sayfada."),
      ("Yapılandırma", "Şemalar, varlık netliği, cevap bölümleri, iç bağlantı."),
      ("İçerik", "Gündem ve arama verisinden çıkan konular; metni birlikte yazıyoruz."),
      ("Aylık ölçüm", "Ne değişti, ne çalıştı, ne bırakılacak — tek sayfa."),
    ]))
    g.append("<h2>Sık sorulan sorular</h2>")
    g.append(sss_blok(sss))
    g.append('<p>Klasik tarafı <a href="seo-icerik">SEO ve içerik sayfamızda</a>, '
             'kendi ölçümlerimiz <a href="../seffaflik">şeffaflık sayfamızda</a>.</p>')
    g.append("</div></section>\n")
    g.append(cta({"slug": "ai-seo"}, "Önce <i>ölçelim</i>.",
                 "Denetim sonucunu kaynaklarıyla gönderelim; sonra ne yapılacağını konuşalım."))
    return "yapay-zeka-seo.html", _hizmet_kabugu(
        "yapay-zeka-seo.html", "Yapay Zekâ Destekli SEO | Luna Yapım",
        "Yapay zekâyı içerik üretmekte değil, doğru işi bulmakta kullanıyoruz: denetim, "
        "arama verisi analizi, boşluk tespiti ve yapay zekâ aramalarına hazırlık.",
        "yapay zeka seo, ai seo, ai overviews optimizasyon, yapılandırılmış veri, "
        "schema markup, arama verisi analizi, seo denetimi",
        "Yapay zekâ destekli <i>SEO</i>",
        "Yapay zekâya metin yazdırıp siteye yığmıyoruz — o iş ters tepiyor. Yapay zekâyı "
        "denetim, arama verisi analizi ve boşluk tespitinde kullanıyoruz; metni insan yazıyor.",
        "\n".join(g), "Yapay Zekâ Destekli SEO", sss)


# ══════════════════════════════════════════════════════════════ AI KISA FİLM
def ai_kisa_film():
    sss = [
     ("Karakter tutarlılığı gerçekten sağlanabiliyor mu?",
      "Yüksek oranda evet, %100 değil. Referans fotoğraflardan karakter kimliği kuruluyor "
      "ve her sahnede aynı kimlik kullanılıyor. Yakın planda benzerlik çok yüksek çıkıyor; "
      "zorlandığımız yerler aşırı geniş planlar, hızlı hareket ve kalabalık sahneler. "
      "Bunu baştan söylüyoruz çünkü teslimde sürpriz olmasın."),
     ("Kaç referans fotoğraf gerekiyor?",
      "Kişi başına en az 15–20 fotoğraf, farklı açı ve ışıkta. Ne kadar çok ve çeşitli "
      "olursa benzerlik o kadar yükseliyor. Yıllara yayılmış fotoğraflar ayrıca işe "
      "yarıyor: yaş değişimi gereken sahnelerde referans oluyor."),
     ("Fotoğraf slaytından farkı ne?",
      "Slaytta fotoğraf hareket eder, oyunculuk olmaz. Bizim yaptığımız iş sahne kurmak: "
      "farklı plan ölçekleri, kamera hareketi, bakış yönü, mimik ve sahne içi eylem. "
      "Kurgu, ses tasarımı ve müzik sinema mantığıyla çalışılıyor."),
     ("Ne kadar sürüyor?",
      "3 dakikalık bir film için tipik olarak 3–5 hafta. Süreyi belirleyen sahne sayısı, "
      "karakter sayısı ve tutarlılık zorluğu. Acil işlerde takvimi sıkıştırabiliyoruz "
      "ama bunu kaliteyi düşürmeden yapabileceğimiz sınırı da söylüyoruz."),
     ("Revizyon var mı?",
      "Kavram aşamasında (karakter testi ve ilk sahne) sınırsız yön değişikliği; final "
      "üretime geçildikten sonra iki tur revizyon fiyata dahil. Karakter testini onaylamadan "
      "film üretimine başlamıyoruz — asıl risk orada."),
     ("Telif ve kullanım hakları kimde?",
      "Teslim edilen filmin kullanım hakkı sizde. Referans fotoğraflardaki kişilerin "
      "rızasının alınmış olması gerekiyor; gerçek kişilerin yüzü kullanıldığı için bu "
      "sözleşmede yazılı olarak yer alıyor."),
    ]
    g = ['<section><div class="wrap prose">']
    g.append("<h2>Ne yapıyoruz</h2>")
    g.append("<p>Elinizdeki gerçek fotoğraflardan karakter kimliği kuruyoruz ve o kimliği "
             "sahneler boyunca sabit tutarak sinema mantığıyla çekilmiş bir film üretiyoruz. "
             "Fotoğraf slaytı değil, basit görsel-videoya çevirme de değil: farklı plan "
             "ölçekleri, kamera hareketi, oyunculuk ve kurgu ritmi olan bir kısa film.</p>")
    g.append('<div class="kiyas"><div class=\"tablo-kaydir\"><table>'
             '<tr><th>Genelde yapılan</th><th>Bizim yaptığımız</th></tr>'
             '<tr><td>Fotoğraf hareket ettirilir (ken burns, parallax)</td>'
             '<td>Sahne kurulur: plan ölçeği, kamera hareketi, bakış yönü, sahne içi eylem</td></tr>'
             '<tr><td>Her sahnede yüz biraz değişir, izleyici fark eder</td>'
             '<td>Karakter kimliği sabitlenir; sahne aralarında yüz denetimi yapılır</td></tr>'
             '<tr><td>Üretilen klipler arka arkaya dizilir</td>'
             '<td>Kurgu ritmi, renk uyumu ve ses tasarımı ayrı ayrı çalışılır</td></tr>'
             '<tr><td>Müzik hazır kütüphaneden konur</td>'
             '<td>Müzik ve ses tasarımı sahneye göre seçilir/kurgulanır; ortam sesi eklenir</td></tr>'
             "</table></div>")

    g.append("<h2>Karakter tutarlılığı nasıl sağlanıyor</h2>")
    g.append(_surec([
      ("Referans toplama", "Kişi başına 15–20+ fotoğraf; farklı açı, ışık ve yıllar. "
                           "Mekân referansları ayrıca toplanıyor."),
      ("Karakter kimliği", "Referanslardan sabit bir karakter kimliği kuruluyor. "
                           "Bu aşamada test kareleri üretilip sizinle onaylanıyor."),
      ("Karakter testi", "Üç farklı plan ölçeğinde (yakın, orta, genel) test. "
                         "Benzerlik yeterli değilse referans ekleyip tekrarlıyoruz — "
                         "bu aşama onaylanmadan film üretimine geçmiyoruz."),
      ("Sahne üretimi", "Senaryodaki her sahne ayrı ayrı üretiliyor; her karede "
                        "aynı karakter kimliği kullanılıyor."),
      ("Yüz denetimi", "Üretilen her sahne referansla karşılaştırılıyor; "
                       "sapan kareler yeniden üretiliyor."),
      ("Kurgu ve renk", "Sahneler kurgulanıyor, tüm film tek renk paletinde birleştiriliyor — "
                        "sahneler arası fark burada da kapanıyor."),
      ("Ses ve müzik", "Ortam sesi, efekt ve müzik. Sessiz izlenebilmesi için altyazı seçeneği."),
      ("Teslim", "Master dosya + sosyal medya sürümleri (yatay, kare, dikey) + kapak görselleri."),
    ]))

    g.append('<div class="kutu"><p><strong>Dürüst sınır:</strong> Karakter tutarlılığı '
             'yüksek oranda sağlanıyor ama %100 değil. En iyi sonuç yakın ve orta planlarda '
             'çıkıyor. Aşırı geniş planlar, hızlı hareket ve kalabalık sahneler zorlanılan '
             'yerler — senaryoyu bu bilgiyle birlikte planlıyoruz. Karakter testini '
             'onaylamadan üretime geçmememizin sebebi de bu: riski baştan görüyorsunuz.</p></div>')

    g.append("<h2>Fiyat aralığı</h2>")
    g.append("<p>3 dakikalık, karakter tutarlılığı olan bir kısa film için <strong>"
             "120.000 – 400.000 ₺</strong> bandında çalışıyoruz. Aralığı belirleyen kalemler:</p>")
    g.append('<div class=\"tablo-kaydir\"><table><tr><th>Kalem</th><th>Fiyatı nasıl etkiliyor</th></tr>'
             '<tr><td><strong>Sahne sayısı</strong></td><td>En belirleyici kalem. '
             '3 dakika 12 sahneyle de anlatılabilir, 40 sahneyle de.</td></tr>'
             '<tr><td><strong>Karakter sayısı</strong></td><td>Her karakter ayrı kimlik ve '
             'ayrı test demek. İki kişilik bir hikâye ile beş kişilik bir hikâye aynı iş değil.</td></tr>'
             '<tr><td><strong>Tutarlılık zorluğu</strong></td><td>Yaş değişimi, kostüm '
             'değişimi, farklı dönemler — her biri ek test turu.</td></tr>'
             '<tr><td><strong>Mekân çeşitliliği</strong></td><td>Tek mekânlı film ile on '
             'mekânlı film arasında belirgin fark var.</td></tr>'
             '<tr><td><strong>Ses tasarımı</strong></td><td>Sadece müzik mi, yoksa diyalog, '
             'seslendirme ve ortam sesi de var mı.</td></tr>'
             "</table></div>")
    g.append("<p>Teklifte tek bir rakam ve kapsamı yazılı veriyoruz; kapsam değişmedikçe "
             "fiyat değişmiyor. <a href=\"../fiyatlar.html\">Fiyat yaklaşımımızı</a> "
             "ayrıca yazdık.</p>")

    g.append("<h2>Paketler</h2>")
    g.append(_paketler([
      ("Karakter testi", "Karar vermeden önce riski görmek için",
       ["Referans fotoğraflardan karakter kimliği", "Üç plan ölçeğinde test kareleri",
        "Benzerlik değerlendirmesi ve dürüst görüş",
        "Devam edilirse bedeli film fiyatından düşülür"]),
      ("Kısa film — 60–90 sn", "Tek anlatım, sınırlı sahne",
       ["Karakter kimliği ve test", "8–15 sahne üretimi", "Kurgu, renk, ses tasarımı",
        "Yatay + kare + dikey teslim", "İki tur revizyon"]),
      ("Kısa film — 3 dk", "Tam hikâye anlatımı",
       ["Karakter kimliği ve test", "20–40 sahne üretimi", "Kurgu, renk, müzik ve ses tasarımı",
        "Altyazılı ve altyazısız sürümler", "Yatay + kare + dikey teslim", "İki tur revizyon"]),
    ]))

    g.append("<h2>Benzer işlerimiz</h2>")
    g.append("<p>Karakter tutarlılığı konusunda gösterebileceğimiz en yakın çalışma "
             "<strong>Karga serisi</strong>: tamamen üretilmiş bir karakterin açılış, geçiş, "
             "makro göz, kanat açılışı ve kapanış olmak üzere birden çok sahnede aynı kimlikle "
             "korunduğu bir seri. Tüy dokusu, göz içi kırılma ve ışık her sahnede tutarlı. "
             "Bunun yanında kısa film ve klip işlerimiz kurgu ve ışık tarafını gösteriyor.</p>")
    g.append('<div class="rozetler">'
             '<div class="rozet"><b>Karga serisi</b><span>3D karakter</span>'
             '<small>Çok sahnede sabit karakter kimliği</small></div>'
             '<div class="rozet"><b>Galzura</b><span>Anlatım animasyonu</span>'
             '<small>TR/DE, yatay + dikey, tek üretimden çok sürüm</small></div>'
             '<div class="rozet"><b>Kısa film</b><span>Kurgu ve ışık</span>'
             '<small>Hikâye ritmi ve oyuncu yönetimi</small></div>'
             "</div>")
    g.append('<p style="color:var(--gri);font-size:14.5px;margin-top:14px">'
             'Gerçek kişilerin yüzünden üretilmiş, yayınlanmış bir referans filmimiz '
             'henüz yok — bu tür işler kişisel olduğu için müşterilerimiz genelde '
             'yayınlanmasını istemiyor. Onun yerine <strong>size özel karakter testi</strong> '
             'yapıyoruz: kendi fotoğraflarınızla üç plan ölçeğinde test kareleri üretip '
             'gösteriyoruz. Böylece başkasının işine değil, kendi işinizin sonucuna bakarak '
             'karar veriyorsunuz.</p>')
    g.append(video_bolumu("isler", "İşlerimizden"))
    g.append('<section><div class="wrap prose">')
    g.append("<h2>Sık sorulan sorular</h2>")
    g.append(sss_blok(sss))
    g.append("</div></section>\n")
    g.append(cta({"slug": "ai-film"}, "Önce <i>karakter testi</i> yapalım.",
                 "Fotoğrafları gönderin; üç plan ölçeğinde test üretip benzerliği "
                 "birlikte değerlendirelim."))
    return "ai-kisa-film.html", _hizmet_kabugu(
        "ai-kisa-film.html", "AI Kısa Film ve Karakter Tutarlılığı | Luna Yapım",
        "Gerçek fotoğraflardan karakter kimliği kurup sahneler boyunca sabit tutuyoruz. "
        "Fotoğraf slaytı değil: plan ölçekleri, kamera hareketi, oyunculuk ve kurgu ritmi "
        "olan sinematik kısa film. Fiyat aralığı ve süreç açık.",
        "ai kısa film, yapay zeka film, character consistency, karakter tutarlılığı, "
        "ai video üretimi, sinematik ai film, yapay zeka klip, kişiye özel film",
        "AI kısa film ve <i>karakter tutarlılığı</i>",
        "Gerçek fotoğraflardan karakter kimliği kuruyoruz ve sahneler boyunca sabit "
        "tutuyoruz. Fotoğraf slaytı değil — plan ölçekleri, kamera hareketi ve oyunculuk "
        "içeren gerçek bir kısa film.",
        "\n".join(g), "AI Kısa Film", sss=sss, fiyat=(120000, 400000))

# ══════════════════════════════════════════════════════════════ E-TİCARET
def e_ticaret():
    """E-ticaret danışmanlığı ve pazaryeri entegrasyonu.

    Dürüstlük notu: yalnız GERÇEKTEN yaptığımız iş yazılır. Trendyol Satıcı API'siyle
    uçtan uca çalışan bir otomasyon yazdık (fotoğraf → açıklama → çoklu görsel → barkod →
    yükleme); ürün çekimi ve 3D ürün animasyonu zaten ana işimiz. Stok/muhasebe/kargo
    yazılımı satmıyoruz ve öyleymiş gibi yazmıyoruz — "Neyi yapmıyoruz" bölümü bunun için.
    """
    dosya = "e-ticaret.html"
    ad = "E-ticaret Danışmanlığı ve Pazaryeri Entegrasyonu"
    aciklama = ("E-ticaret danışmanlığı ve pazaryeri entegrasyonu: ürün görseli ve videosu, "
                "listeleme kalitesi, Trendyol Satıcı API ile otomatik ürün yükleme. "
                "Katalog büyüklüğüne göre fiyat, aynı gün net aralık.")
    anahtar = ("e-ticaret danışmanlığı, pazaryeri entegrasyonu, trendyol entegrasyonu, "
               "trendyol api ürün yükleme, e-ticaret ürün çekimi, ürün görseli hazırlama, "
               "e-ticaret video, ürün animasyonu, listeleme optimizasyonu")
    sss = [
      ("Hangi pazaryerleriyle çalışıyorsunuz?",
       "Trendyol'da Satıcı API'si üzerinden uçtan uca çalışan bir hattımız var: ürün fotoğrafından "
       "açıklama, çoklu format görsel, barkod ve stok kodu üretilip ürün mağazaya yükleniyor. "
       "Diğer pazaryerlerinde aynı hattı o platformun API belgesine göre kuruyoruz; "
       "daha önce yapmadığımız bir platform için bunu önceden söylüyoruz."),
      ("Ürün fotoğrafım var, yeniden çekim şart mı?",
       "Şart değil. Elinizdeki fotoğraf pazaryeri ölçülerine uygunsa onu düzenleyip çoğaltıyoruz. "
       "Ama ürün sayfanız dönüşmüyorsa sorunun büyük kısmı genellikle görselde oluyor; "
       "önce mevcut görsellerinizi ölçüp size nerede kaybettiğinizi gösteriyoruz."),
      ("Kaç üründen sonra otomasyon mantıklı oluyor?",
       "Kabaca 50 ürünün üzerinde. Altında elle yapmak daha ucuza geliyor ve bunu söylüyoruz. "
       "Katalog büyüdükçe fark açılıyor: aynı işi elle yapan ekip o saatleri size faturalıyor."),
      ("Ürün videosu gerçekten satışa etki ediyor mu?",
       "Ürüne göre değişiyor. Fiziksel detayın belirleyici olduğu kalemlerde (tekstil dokusu, "
       "makine çalışma prensibi, mobilya modülü) etkisi belirgin; standart ambalajlı üründe "
       "sınırlı. Hangi grupta olduğunuzu ilk görüşmede söylüyoruz."),
      ("Mağazamı sıfırdan kurar mısınız?",
       "Mağaza açılışı ve evrak süreci sizde; biz açılıştan sonraki tarafı yapıyoruz — "
       "ürün görseli, video, listeleme metni ve yükleme otomasyonu."),
    ]
    g = ['<section><div class="wrap prose">']
    g.append("<p>Ürün sayfası satmıyorsa sorun çoğu zaman üründe değil. Aynı ürün, aynı fiyatla, "
             "başka bir mağazada satıyor. Aradaki fark genellikle üç yerde birikiyor: görselin "
             "kalitesi, listelemenin eksiksizliği ve kataloğun güncel tutulup tutulmadığı.</p>")
    g.append("<h2>Neyi çözüyoruz</h2>")
    g.append("<ul>"
             "<li><strong>Görsel</strong> — pazaryerinin istediği ölçülerde ana görsel, kare sürüm, "
             "doku detayı ve etiketli kapak. Tek çekimden çoklu format çıkıyor.</li>"
             "<li><strong>Listeleme</strong> — başlık, öznitelik ve açıklama; arayanın yazdığı "
             "kelimelerle, kategori kurallarına uygun.</li>"
             "<li><strong>Yükleme</strong> — 50'nin üzerinde ürünü elle girmek gün alıyor; "
             "hattı kurduğumuzda fotoğraftan yüklemeye kadar tek komutla ilerliyor.</li>"
             "</ul>")
    g.append("<h2>Pazaryeri entegrasyonu — ne yaptık</h2>")
    g.append("<p>Trendyol Satıcı API'si üzerinde çalışan bir hattımız var. Ürün fotoğrafından "
             "açıklama yazılıyor, pazaryeri standartlarında çoklu görsel üretiliyor "
             "(1200×1800 ana görsel, 1080×1080 kare, doku detayı, etiketli kapak), benzersiz "
             "barkod ve stok kodu oluşturuluyor ve ürün mağazaya yükleniyor. Bu hat bizim "
             "kendi yazdığımız yazılım; kiraladığımız bir araç değil.</p>")
    g.append("<p>Başka bir pazaryeri için aynı hattı kurmak, o platformun API belgesine bağlı. "
             "Daha önce çalışmadığımız bir platformsa bunu baştan söylüyoruz — "
             "\u201cher yerde çalışır\u201d demiyoruz.</p>")
    g.append("<h2>Ürün görseli ve videosu</h2>")
    g.append("<p>Asıl işimiz burası. Stüdyoda ürün çekimi, 360° dönen ürün, doku makrosu; "
             "fiziksel olarak çekilemeyen ya da henüz üretilmemiş ürün için "
             "<a href=\"urun-animasyon\">3D ürün animasyonu</a>. Aynı çekimden pazaryeri "
             "görselleri, reklam kesimleri ve sosyal medya sürümleri birlikte çıkıyor.</p>")
    g.append("<h2>Süreç</h2></div><div class=\"wrap\">")
    g.append(_surec([
        ("Katalog bakışı", "Kaç ürün, hangi pazaryeri, mevcut görseller ne durumda — ölçüyoruz."),
        ("Örnek ürün", "Tek üründe baştan sona yapıyoruz: görsel, listeleme, yükleme."),
        ("Onay ve hat", "Örnek onaylanınca aynı kalıbı katalogun tamamına kuruyoruz."),
        ("Teslim", "Görseller, listeleme metinleri ve çalışan yükleme hattı sizde kalır."),
    ]))
    g.append('</div><div class="wrap prose">')
    g.append("<h2>Paketler</h2>")
    g.append(_paketler([
        ("Görsel paketi", "Ürün başına", ["Pazaryeri ölçülerinde ana görsel ve kare sürüm",
                                          "Doku/detay karesi", "Etiketli kapak görseli"]),
        ("Listeleme paketi", "Ürün grubu başına", ["Başlık ve öznitelik düzeni",
                                                   "Arayan diliyle açıklama metni",
                                                   "Kategori kuralı kontrolü"]),
        ("Otomasyon hattı", "Katalog başına", ["Fotoğraftan açıklama ve görsel üretimi",
                                               "Barkod ve stok kodu",
                                               "Satıcı API ile yükleme"]),
    ]))
    g.append("<h2>Neyi yapmıyoruz</h2>")
    g.append("<p>Stok, muhasebe, kargo ve fatura entegrasyonu yapmıyoruz; bunlar ayrı bir "
             "uzmanlık ve piyasada iyi çözümleri var. Mağaza açılışı ve evrak süreci de sizde. "
             "Reklam bütçesi yönetimi (pazaryeri içi reklam) da bu hizmetin kapsamı dışında. "
             "Yapmadığımız işi yapıyormuş gibi yazmak, ilk toplantıda anlaşılıyor zaten.</p>")
    g.append("<h2>Fiyat</h2>")
    g.append("<p>Katalog büyüklüğüne göre değişiyor; tek fiyat vermek doğru olmuyor. "
             "Ürün sayınızı ve hangi pazaryerinde olduğunuzu söyleyin, aynı gün net bir aralık "
             "verelim. Diğer hizmetlerin bantları "
             "<a href=\"../fiyatlar\">fiyat sayfamızda</a> açık yazılı.</p>")
    g.append("</div></section>")
    g.append('<section><div class="wrap prose"><h2>Sık sorulan sorular</h2>%s</div></section>' % sss_blok(sss))
    g.append(cta({"slug": "e-ticaret"}, "Kataloğunuzu <i>satan</i> hâle getirelim.",
                 "Ürün sayınızı ve pazaryerinizi yazın; ne yapılabileceğini aynı gün konuşalım."))
    return dosya, _hizmet_kabugu(dosya, ad + " | Luna Yapım", aciklama, anahtar,
                                 "E-ticaret danışmanlığı ve <i>pazaryeri entegrasyonu</i>",
                                 "Ürün görseli, listeleme ve yükleme otomasyonu — Trendyol Satıcı "
                                 "API'siyle uçtan uca çalışan kendi hattımızla.",
                                 "\n".join(g), ad, sss)
