# -*- coding: utf-8 -*-
"""
YAPAY ZEKÂ VE ARAMA GÜNDEMİ SAYFASI

sorgu.py'nin günlük derlemesini siteye tek bir yaşayan sayfa olarak basar:
    <site>/yapay-zeka/index.html

Neden tek sayfa: her gün için ayrı sayfa açmak ince içerik üretir ve Google
bunu "yararsız" sayar. Bunun yerine tek sayfa her gün tazeleniyor; derinlemesine
cevap gerektiren sorgular makale.py'nin 100 puan kapısından geçip blog'a giriyor.

Yayınlanan hiçbir rakam uydurma değil:
  - otomatik tamamlama SIRA verir, hacim vermez — sayfada da sıra yazıyor
  - Trends'in yaklaşık hacmi varsa kaynağıyla birlikte yazılıyor
"""
import os, json, html, datetime

from . import sorgu, ayarlar

BASLIK = "Yapay Zekâ ve Arama Gündemi — Bugün Ne Aranıyor | Luna Yapım"
ACIKLAMA = ("Prodüksiyon, 3D modelleme ve tanıtım videosu alanında insanların "
            "bugün gerçekten ne arattığı. Günlük derleniyor, kaynağı açık yazılıyor.")
ANAHTAR = ("arama gündemi, yapay zeka arama, en çok aranan sorgular, 3d modelleme "
           "arama, tanıtım videosu arama, luna yapım")
KANONIK = "https://lunayapim.com/yapay-zeka/"


def _k(x):
    return html.escape(str(x or ""), quote=True)


def _semalar(paket, sss):
    liste = {
        "@context": "https://schema.org", "@type": "CollectionPage",
        "name": "Yapay Zekâ ve Arama Gündemi",
        "url": KANONIK,
        "description": ACIKLAMA,
        "dateModified": paket.get("tarih"),
        "isPartOf": {"@type": "WebSite", "name": "Luna Yapım",
                     "url": "https://lunayapim.com"},
        "publisher": {"@type": "Organization", "name": "Luna Yapım",
                      "url": "https://lunayapim.com"},
    }
    ogeler = {
        "@context": "https://schema.org", "@type": "ItemList",
        "name": "Bugün en çok aranan sorgular",
        "numberOfItems": min(24, len(paket.get("sorgular", []))),
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": s["sorgu"]}
            for i, s in enumerate(paket.get("sorgular", [])[:24])
        ],
    }
    sssema = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in sss
        ],
    }
    return "\n".join('<script type="application/ld+json">\n%s\n</script>' %
                     json.dumps(x, ensure_ascii=False) for x in (liste, ogeler, sssema))


SSS = [
 ("Bu liste nereden geliyor?",
  "İki kaynaktan: Google'ın arama kutusundaki otomatik tamamlama önerileri ve "
  "Google Trends'in Türkiye günlük yükselen aramalar akışı. İkisi de herkese açık "
  "ve ücretsiz. Otomatik tamamlama bir sorgunun kaç kez arandığını söylemez, "
  "hangi sırada geldiğini söyler; sayfada da hacim değil sıra yazıyor."),
 ("Sıra ne anlama geliyor?",
  "Google, bir kelimeyle başlayan aramaları sıklığına göre sıralar. Sıra 0 o "
  "kelimeyle başlayan en yaygın arama demektir. Yani sıra bir tahmin değil, "
  "Google'ın kendi ölçümünün sırası."),
 ("Neden her sorguya yazı yazmıyorsunuz?",
  "Yazdığımız her sayfa 100 puanlık bir yayın kapısından geçiyor: kaynak, "
  "iç bağlantı, benzersizlik ve kendi sayfalarımızla çakışmama şartı var. "
  "Kapıyı geçmeyen yazı yayınlanmıyor. Listede görünüp yazısı olmayan sorgular "
  "ya sırasını bekliyor ya da bizim gerçekten söyleyecek sözümüz yok."),
 ("Yapay zekâ arama sonuçlarını nasıl değiştiriyor?",
  "Kullanıcı artık soruyu doğrudan yapay zekâya soruyor ve tek bir cevap alıyor. "
  "O cevabın içinde kaynak olarak geçmek, on mavi bağlantıdan birinde çıkmaktan "
  "daha değerli hale geldi. Bunun için sayfanın net soru-cevap yapısı, JSON-LD "
  "şeması ve tarihli, kaynaklı bilgi taşıması gerekiyor."),
 ("Bu sayfa ne sıklıkla güncelleniyor?",
  "Her gün. Derleme kendi panelimizde çalışıyor, sonucu bu sayfaya basılıyor. "
  "Sayfanın altında son güncelleme tarihi yazıyor."),
]


def _tablo(sorgular, kok="../"):
    if not sorgular:
        return '<p class="ornek-not">Bugünün derlemesi henüz çalışmadı.</p>'
    satir = []
    for i, s in enumerate(sorgular, 1):
        rozet = ""
        if s.get("kaynak", "").startswith("trend") or "trend" in s.get("kaynak", ""):
            h = s.get("hacim")
            rozet = ('<span class="sg-rozet">Trends%s</span>' %
                     (" · " + _k(h) if h else ""))
        durum = s.get("durum")
        if durum:
            rozet += '<span class="sg-rozet sg-yeni">%s</span>' % _k(durum)
        satir.append(
            '<tr><td class="sg-no">%02d</td>'
            '<td class="sg-sorgu">%s%s</td>'
            '<td class="sg-hiz"><a href="%s%s">%s</a></td>'
            '<td class="sg-sira">%s</td></tr>'
            % (i, _k(s["sorgu"]), rozet, kok, _k(s["hizmet"]), _k(s["etiket"]),
               ("—" if s.get("kaynak") == "trend" else str(s.get("sira", 0) + 1))))
    return ('<div class="sg-sar"><table class="sg-tablo">'
            '<thead><tr><th>#</th><th>Sorgu</th><th>İlgili hizmetimiz</th>'
            '<th title="Google otomatik tamamlama sırası">Sıra</th></tr></thead>'
            '<tbody>%s</tbody></table></div>' % "".join(satir))


def govde(paket, yukselen):
    bugun = paket.get("tarih") or datetime.date.today().isoformat()
    sorgular = paket.get("sorgular", [])[:24]
    kaynak_notu = ("Kaynak: Google otomatik tamamlama ve Google Trends Türkiye, "
                   "%s tarihli derleme." % bugun)

    sss_html = "".join(
        '<details class="sss"><summary>%s</summary><p>%s</p></details>' % (_k(q), _k(a))
        for q, a in SSS)

    asistan_html = """
<section><div class="wrap">
  <div class="bas"><span class="no">03</span><div>
    <h2>Luna Asistan — sitenin kendi cevap katmanı</h2>
    <p class="aciklama">Sağ alttaki karga düğmesi. Sorduğunuz soruyu bu sitedeki
      144 soru-cevap ve 336 sayfayla eşleştirip cevabı kaynağıyla birlikte
      gösteriyor.</p></div></div>
  <div class="uc">
    <div class="hiz"><h3>Uydurmuyor</h3><p>Cevaplar bizim yazdığımız sayfalardan
      geliyor. Karşılığı yoksa &#8220;bunu tam bilemedim&#8221; deyip sizi
      doğrudan bize bağlıyor. Metin üretmiyor, metin buluyor.</p></div>
    <div class="hiz"><h3>Sorunuz bir yere gitmiyor</h3><p>Eşleştirme tarayıcınızda
      yapılıyor. Dışarıda bir yapay zekâ servisi yok, hesap yok, kayıt yok.
      Yazdığınız cümle sunucuya gönderilmiyor.</p></div>
    <div class="hiz"><h3>Cevabı olmayan soru bize ödev</h3><p>Karşılığı çıkmayan
      sorular içerik planımıza düşüyor. Yukarıdaki arama gündemiyle birlikte,
      bir sonraki yazının konusunu bunlar belirliyor.</p></div>
  </div>
</div></section>"""

    yuk_html = ""
    if yukselen:
        yuk_html = ('<section><div class="wrap">'
                    '<div class="bas"><span class="no">02</span><div>'
                    '<h2>Bu hafta yükselenler</h2>'
                    '<p class="aciklama">Listeye yeni giren ya da sırası belirgin '
                    'şekilde yukarı çıkan sorgular.</p></div></div>%s</div></section>'
                    % _tablo(yukselen))
    yuk_html += asistan_html

    return """
<div class="page-hero">
  <img class="karga-buyuk" src="../assets/karga.png" alt="">
  <div class="wrap">
    <div class="crumbs"><a href="../">Ana Sayfa</a> · Yapay Zekâ ve Arama</div>
    <h1>Bugün ne <i>aranıyor</i>?</h1>
    <p class="lede">Prodüksiyon, 3D modelleme ve tanıtım videosu alanında insanların
      arama kutusuna gerçekten ne yazdığını her gün derliyoruz. Hacim uydurmuyoruz —
      Google'ın kendi sıralamasını olduğu gibi yayınlıyoruz.</p>
  </div>
</div>

<section class="hizmet-ozet">
  <div class="wrap">
    <span class="etk">Neden yayınlıyoruz</span>
    <h2>Ne sorulduğunu bilmeyen doğru cevabı yazamaz</h2>
    <p>Bu listeyi kendi içerik planımız için topluyoruz; sakladığımız bir tarafı olmadığı
      için açık yayınlıyoruz. Aynı veriyle hem kendi sayfalarımızı hem müşterilerimizin
      sayfalarını planlıyoruz.</p>
    <div class="taahhut">
      <div><b>Günlük</b><span>derleme her gün yenileniyor</span></div>
      <div><b>Kaynaklı</b><span>hangi veri nereden geldiği yazılı</span></div>
      <div><b>100 puan</b><span>yazıya dönüşen sorgu yayın kapısından geçiyor</span></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="bas"><span class="no">01</span><div><h2>Bugünün derlemesi</h2>
      <p class="aciklama">%s</p></div></div>
    %s
    <p class="ornek-not">Sıra sütunu, o kelimeyle başlayan aramalar içindeki sırayı
      gösterir; arama sayısı değildir. Trends satırlarında sıra yerine tire vardır,
      çünkü o akış sıra değil yükseliş bildirir.</p>
  </div>
</section>
%s

<section class="acik">
  <div class="wrap">
    <div class="bas"><span class="no">03</span><div><h2>Biz bu konuda ne yapıyoruz</h2>
      <p class="aciklama">Arama tarafındaki iki hizmetimiz doğrudan bu veriyle
        çalışıyor.</p></div></div>
    <div class="urunler">
      <a class="urun" href="../hizmetler/seo-icerik"><i class="cizgi"></i>
        <span class="rom">i.</span><h3>SEO ve İçerik</h3>
        <p>Teknik denetim, şema, site haritası ve gerçek soruya cevap veren içerik.
          Kendi sitemizde 335 sayfayı hatasız geçirdik; aynı denetimi müşteri sitesine
          uyguluyoruz.</p>
        <span class="ok">İncele →</span></a>
      <a class="urun" href="../hizmetler/yapay-zeka-seo"><i class="cizgi"></i>
        <span class="rom">ii.</span><h3>Yapay Zekâ ve Arama</h3>
        <p>Cevabın içinde kaynak olarak geçmek için sayfa yapısı: net soru-cevap,
          JSON-LD şeması, tarihli ve kaynaklı bilgi.</p>
        <span class="ok">İncele →</span></a>
    </div>
  </div>
</section>

<section>
  <div class="wrap prose">
    <h2>Sık sorulanlar</h2>
    %s
  </div>
</section>

<section class="cta">
  <img class="karga-buyuk" src="../assets/karga.png" alt="">
  <div class="wrap">
    <p class="etk">İletişim</p>
    <h2>Sizin sektörünüzde <i>ne aranıyor</i>?</h2>
    <p>Aynı derlemeyi sizin işiniz için de çıkarıyoruz; hangi soruya cevap yazmanız
      gerektiğini rakamla konuşalım.</p>
    <a href="https://wa.me/905411602603" class="btn btn-dolu">WhatsApp'tan Yaz</a>
    <a href="tel:+905411602603" class="btn btn-cizgi">Ara · 0541 160 26 03</a>
  </div>
</section>

<p class="sg-tarih wrap">Son güncelleme: %s · Derleme Luna Pusula panelinde çalışır.</p>
""" % (kaynak_notu, _tablo(sorgular), yuk_html, sss_html, bugun)


def uret(kok=None, yenile=False):
    """Sayfayı yazar. (yol, sorgu_adedi) döner."""
    kok = kok or ayarlar.SITE_KOK
    if not kok:
        raise RuntimeError("Site kökü bulunamadı — ayarlar.json içindeki site_kok'a bak.")
    paket = sorgu.gunluk(yenile=yenile)
    yukselen = sorgu.yukselenler()

    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "site-uretici"))
    import kabuk

    bas = kabuk.head(BASLIK, ACIKLAMA, ANAHTAR, KANONIK, _semalar(paket, SSS))
    # üst menüde doğru bağlantı işaretlensin
    bas = bas.replace('<a href="./" style="opacity:1;color:var(--kirmizi)">İller</a>',
                      '<a href="../sehir/">İller</a>')
    bas = bas.replace('<a href="../blog/">Blog</a>',
                      '<a href="../blog/">Blog</a>\n      '
                      '<a href="./" style="opacity:1;color:var(--kirmizi)">Yapay Zekâ</a>')
    bas = bas.replace('href="../assets/luna.css"', 'href="../assets/luna.css?v=6"')
    bas = bas.replace('href="../assets/luna.css?v=5"', 'href="../assets/luna.css?v=6"')
    alt = kabuk.FOOTER.replace('src="../assets/videolar.js"', 'src="../assets/videolar.js?v=5"')
    # Luna Asistan her yeniden üretimde de kalsın
    if "asistan.js" not in alt:
        alt = alt.replace("</body>",
                          '<script src="../assets/asistan.js?v=1" defer></script>\n</body>')

    klasor = os.path.join(kok, "yapay-zeka")
    os.makedirs(klasor, exist_ok=True)
    yol = os.path.join(klasor, "index.html")
    with open(yol, "w", encoding="utf-8") as f:
        f.write(bas + govde(paket, yukselen) + alt)
    return yol, len(paket.get("sorgular", []))
