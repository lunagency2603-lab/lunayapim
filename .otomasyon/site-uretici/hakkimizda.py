# -*- coding: utf-8 -*-
"""
HAKKIMIZDA — /hakkimizda
14.10.2026: Sitede "biz kimiz" sayfası yoktu. Google'ın kalite değerlendirmesi
("sitenin arkasında kim var?") ve teklif isteyen müşterinin ilk sorusu aynı:
kimsiniz, nerede duruyorsunuz, ne yaptınız. Bu sayfa yalnız doğrulanabilir
bilgi taşır: kuruluş tarihi, şehir, ekip düzeni, gerçek işler, ilkeler.
Üretim:  cd .otomasyon/site-uretici && python3 -c "import hakkimizda; hakkimizda.yayinla()"
"""
import os, json

from yeni_sayfalar import _kabuk, _sema, SITE, BUGUN
from uretici import KOK, e, j, cta
from isler_blok import kartlar

KURULUS = "2026-03-26"

ILKELER = [
 ("Yapmadığımız işi yazmayız",
  "İşler sayfasındaki her kart gerçek bir müşteri ya da kendi yapımımız. Hangi ilde iş yaptıysak o ilin "
  "sayfasında anılır; başka ilde yapılmış gibi gösterilen tek iş yok."),
 ("Rakamlarımız açık",
  "Aramada kaç kişiye göründüğümüzü, kaç tıklama aldığımızı ve neyi henüz başaramadığımızı "
  "<a href=\"seffaflik\">Şeffaflık</a> sayfasında tarihli olarak yayınlıyoruz. Güzelleştirmiyoruz."),
 ("Ucuz değil, aracısız",
  "Çekim, kurgu, 3D ve yazılım aynı ekipte. Aradan çıkan her halka fiyattan düşüyor; "
  "ışıktan, sesten, renkten ve revizyon hakkından kısmıyoruz. Mekanizması <a href=\"fiyatlar\">Fiyatlar</a> sayfasında."),
 ("Tek çekim, çok format",
  "Bir çekim gününden yatay, kare ve dikey sürümler, kısa kesitler ve kapak görselleri birlikte çıkar. "
  "Aynı işi dört kalemde faturalamıyoruz."),
 ("Ölçmeden değiştirmeyiz",
  "Kendi sitemizde de müşteri sitesinde de her değişiklik önce ölçülür. İşe yaramayan geri alınır; "
  "bunu da yazarız."),
]

YAPTIKLARIMIZ = [
 ("İnşaat 3D ve mimari görselleştirme", "hizmetler/insaat-3d-modelleme",
  "Proje bitmeden satılsın diye dış cephe, iç mekân ve kuş bakışı sahneler; katman katman süreç filmi."),
 ("Ürün ve makine animasyonu", "hizmetler/urun-animasyon",
  "Kameranın giremediği yeri gösteren kesitler; teknik eğitim ve satış sunumu için."),
 ("Drone ve FPV çekim", "hizmetler/drone-fpv",
  "DJI Avata 2 ile iç-dış geçişli uçuşlar, 4K havadan görüntü; 81 ilde yerel ortakla."),
 ("Klip, tanıtım ve kısa film", "hizmetler/klip-cekimi",
  "Müzik klibi, kurumsal tanıtım, emlak filmi, düğün; kurgu ve renk Bursa'daki ekipte."),
 ("Web sitesi, SEO ve site eklentileri", "hizmetler/web-sitesi-tasarimi",
  "Sıfırdan site, 3B tasarlayıcı ve sanal mağaza gibi yaratıcı eklentiler, ölçüm kurulumu."),
 ("Reklam ve sosyal medya yönetimi", "hizmetler/reklam-yonetimi",
  "Google ve Meta kampanyaları, aylık içerik üretimi; hepsi sayıyla raporlanır."),
 ("Baskı ve kişiye özel hediye", "hizmetler/kisiye-ozel-baski-hediye",
  "DTF / UV DTF baskı, tişörtten kupaya promosyon; çiftlere özel animasyon ve albüm."),
 ("Kendi yazılımlarımız", "yazilim",
  "Luna Pusula, Trendyol otomasyonu, KDA Matrix, TrendSaphiens — ekip işini hızlandıran araçları kendi yazar."),
]

SSS = [
 ("Luna Yapım nerede?",
  "Bursa'dayız. Kurgu, renk, 3D ve yazılım Bursa'daki ekipte yapılır; yerinde çekim gereken işlerde "
  "81 ildeki yerel çözüm ortaklarımızla çalışırız."),
 ("Ekip kaç kişi?",
  "Çekirdek ekip iki kişi; bu bilerek böyle. Çekim, kurgu, 3D ve yazılımı aynı masada tutmak "
  "hem fiyatı hem teslim süresini kısaltıyor. İşin büyüklüğüne göre sahada yerel ortaklar ve "
  "oyuncu, ses, ışık ekipleri devreye girer."),
 ("Ne zaman kuruldunuz?",
  "26 Mart 2026'da açıldık. İlk yılın işleri — prefabrik ev üreticisi için 3B ev tasarlayıcı, kumaş "
  "toptancısı için sanal mağaza, müzik klibi, teknik eğitim animasyonu — İşler sayfasında."),
 ("Müşteriyle nasıl çalışıyorsunuz?",
  "Aynı gün net teklif, yazılı kapsam, iki tur revizyon dahil. Teslimden sonra ölçüm: videonun, "
  "sitenin ya da kampanyanın ne getirdiğini birlikte okuruz."),
 ("Sadece Bursa'ya mı hizmet veriyorsunuz?",
  "Hayır. 3D, animasyon, web ve reklam işleri tamamen uzaktan yürür; çekim gereken işlerde "
  "ilinizdeki ortağımız sahaya çıkar, kurgu yine bizde kalır."),
]


def _sss(sss):
    p = ['<div class="sss">']
    for i, (q, a) in enumerate(sss):
        p.append('      <details%s><summary>%s</summary>\n        <div class="cvp"><p>%s</p></div></details>'
                 % (" open" if i == 0 else "", e(q), e(a)))
    p.append('    </div>')
    return "\n".join(p)


def govde():
    g = '<section><div class="wrap prose">\n'
    g += ('<div class="kutu"><h2 style="margin-bottom:8px">Kamerayı da kodu da kendimiz kullanıyoruz.</h2>'
          '<p>Luna Yapım, 26 Mart 2026\'da Bursa\'da kuruldu. Video prodüksiyon, 3D görselleştirme ve web–yazılım '
          'işlerini tek ekipte toplayan küçük bir yapım şirketiyiz.</p></div>\n')
    g += '<h2>Kısa hikâye</h2>\n'
    g += ('<p>Başlangıç noktamız basitti: bir firmanın tanıtım filmi, web sitesi ve reklamı çoğu zaman üç ayrı '
          'ajansa gidiyor, üçü de birbirinin yaptığını bilmiyor. Biz üçünü aynı masada tutmak için kurulduk. '
          'İlk altı ayda bir prefabrik ev üreticisine tarayıcıda çalışan 3B ev tasarlayıcı ve yeni sitesini, '
          'bir kumaş toptancısına sanal mağaza ve dijital mankenli vitrinini, bir müzisyene klibini ve albüm '
          'kapağını, bir enerji firmasına teknik eğitim animasyonunu yaptık. Hepsi yayında; aşağıda.</p>\n')
    g += ('<p>Aynı dönemde kendi araçlarımızı yazdık: teklif hazırlayan ve müşteri adayı bulan Luna Pusula, '
          'fotoğraftan ürün sayfası çıkaran Trendyol otomasyonu, günlük yayın yapan TrendSaphiens. Bir ajansın '
          'elle yaptığı tekrar işlerini yazılıma devredince hem fiyat hem teslim süresi düşüyor; '
          '<a href="fiyatlar">fiyat politikamız</a> bu yüzden "ucuz değil, aracısız".</p>\n')
    g += '<h2>Nasıl çalışıyoruz</h2>\n<div class="surec">\n'
    adimlar = [
     ("Bursa'da çekirdek ekip", "Kurgu, renk, 3D, web ve yazılım Bursa'da iki kişilik çekirdek ekipte. "
      "Karar hızlı, muhatap tek."),
     ("81 ilde yerel ortak", "Yerinde çekim gereken işlerde ilinizdeki çözüm ortağımız sahaya çıkar; "
      "kurgu ve kalite kontrol yine bizde kalır. İş hangi ilde yapıldıysa o ilin sayfasında anılır."),
     ("Aynı gün teklif, yazılı kapsam", "Ne çekileceği, kaç günde teslim edileceği ve neyin dahil olduğu "
      "baştan yazılır. İki tur revizyon fiyata dahil."),
     ("Teslimden sonra ölçüm", "Film, site ya da kampanya ne getirdi — birlikte okuruz. Kendi sitemizin "
      "rakamlarını da aynı dürüstlükle yayınlıyoruz."),
    ]
    for i, (b, p) in enumerate(adimlar, 1):
        g += '<div class="adim"><span class="n">%02d</span><div><b>%s</b><p>%s</p></div></div>\n' % (i, e(b), e(p))
    g += '</div>\n'
    g += '<h2>Neyi kendimiz yapıyoruz</h2>\n<ul>\n'
    for b, u, p in YAPTIKLARIMIZ:
        g += '<li><a href="%s"><b>%s</b></a> — %s</li>\n' % (u, e(b), e(p))
    g += '</ul>\n</div></section>\n\n'
    # gerçek işler
    g += ('<section class="acik" data-is-blok>\n  <div class="wrap">\n    <div class="bas"><span class="no">01</span>'
          '<div><h2>Gerçek işlerden</h2><p class="aciklama">Hepsi yayında; kartlar işin kendi sayfasına gider.</p></div></div>\n')
    g += kartlar(["aktas-3b", "ata-kumas", "aktas-site", "cm", "yade", "bgk"], on="")
    g += '\n    <p style="margin-top:18px"><a class="btn btn-cizgi" href="isler">Tüm işler →</a></p>\n  </div>\n</section>\n\n'
    # ilkeler
    g += '<section><div class="wrap prose">\n<h2>İlkelerimiz</h2>\n<div class="surec">\n'
    for i, (b, p) in enumerate(ILKELER, 1):
        g += '<div class="adim"><span class="n">%02d</span><div><b>%s</b><p>%s</p></div></div>\n' % (i, e(b), p)
    g += '</div>\n'
    g += '<h2>Sık sorulanlar</h2>\n' + _sss(SSS) + '\n'
    g += ('<h2>Ekibe katılmak isteyenler</h2>\n<p>Kurgu, post prodüksiyon ve içerik üretimi alanında yetiştirmek '
          'üzere stajyer ve öğrenci alıyoruz. Başvuru ve şartlar <a href="kariyer">Kariyer ve Staj</a> sayfasında.</p>\n')
    g += '</div></section>\n\n'
    g += cta(None, "Bizi tanıdınız, şimdi <i>işi</i> konuşalım.",
             "Projeni anlat; aynı gün kapsamı ve fiyatı yazılı gönderelim.")
    return g


def semalar():
    org = _sema("Organization", **{
        "@id": KOK + "/#org",
        "name": "Luna Yapım", "url": KOK + "/", "logo": KOK + "/assets/og-image.png",
        "foundingDate": KURULUS,
        "description": "Bursa merkezli video prodüksiyon, 3D görselleştirme ve web–yazılım şirketi; "
                       "81 ilde yerel çözüm ortağıyla çalışır.",
        "telephone": "+905542182603", "email": "info@lunayapim.com",
        "address": {"@type": "PostalAddress", "addressLocality": "Bursa", "addressCountry": "TR"},
        "areaServed": {"@type": "Country", "name": "Türkiye"},
        "sameAs": ["https://www.instagram.com/luna.yapim/"],
        "contactPoint": {"@type": "ContactPoint", "telephone": "+905542182603",
                         "contactType": "sales", "availableLanguage": "tr"},
    })
    about = _sema("AboutPage", **{
        "name": "Hakkımızda — Luna Yapım", "url": KOK + "/hakkimizda",
        "about": {"@id": KOK + "/#org"}, "inLanguage": "tr", "dateModified": BUGUN,
    })
    crumbs = _sema("BreadcrumbList", itemListElement=[
        {"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": KOK + "/"},
        {"@type": "ListItem", "position": 2, "name": "Hakkımızda", "item": KOK + "/hakkimizda"},
    ])
    faq = _sema("FAQPage", mainEntity=[
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in SSS])
    return [org, about, crumbs, faq]


def yayinla():
    h = _kabuk(
        "hakkimizda",
        "Hakkımızda — Bursa'da Yapım ve Yazılım Ekibi | Luna Yapım",
        "Luna Yapım kimdir: 26 Mart 2026'da Bursa'da kurulan, video prodüksiyon, 3D görselleştirme ve "
        "web–yazılımı tek ekipte toplayan şirket. Ekip düzeni, gerçek işler, ilkeler.",
        "luna yapım hakkında, bursa video prodüksiyon şirketi, bursa yapım şirketi, luna yapım kimdir",
        semalar(),
        "Luna Yapım kimdir?",
        "Bursa'da kurulmuş, kamerayı da kodu da kendi kullanan küçük bir yapım ve yazılım ekibi. "
        "Kurgu burada, çekim 81 ilde yerel ortakla.",
        govde(), kok="")
    h = h.replace('<meta property="og:type" content="article">', '<meta property="og:type" content="website">')
    # kök sayfa: hizmet kartı bağlantısı ve "Tüm iller" kök yerine doğru klasöre gitsin
    h = h.replace('href="seo-ornegi-', 'href="hizmetler/seo-ornegi-')
    h = h.replace('<a href="./">Tüm iller</a>', '<a href="sehir/">Tüm iller</a>')
    h = h.replace('<a href="index">Ana Sayfa</a>', '<a href="./">Ana Sayfa</a>')
    yol = os.path.join(SITE, "hakkimizda.html")
    open(yol, "w", encoding="utf-8").write(h)
    return yol


if __name__ == "__main__":
    print(yayinla())
