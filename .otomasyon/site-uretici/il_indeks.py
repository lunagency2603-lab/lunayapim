# -*- coding: utf-8 -*-
"""sehir/index.html — 81 ilin dizin sayfası."""
import os, json
from sehirler import SEHIRLER, SEHIR_INDEKS, KADEME1, KADEME2, KADEME3
from kabuk import head, FOOTER
from uretici import HEDEF, KOK, e, j, sss_blok, cta, video_bolumu, sayfa_var, HIZMET_ADLARI

BOLGELER = {
 "Marmara": ["istanbul","bursa","kocaeli","sakarya","tekirdag","balikesir","canakkale","edirne",
             "kirklareli","yalova","bilecik","duzce"],
 "Ege": ["izmir","manisa","aydin","denizli","mugla","afyonkarahisar","kutahya","usak"],
 "Akdeniz": ["antalya","adana","mersin","hatay","isparta","burdur","kahramanmaras","osmaniye"],
 "İç Anadolu": ["ankara","konya","kayseri","eskisehir","sivas","yozgat","aksaray","karaman",
                "kirikkale","kirsehir","nevsehir","nigde","cankiri"],
 "Karadeniz": ["samsun","trabzon","ordu","rize","giresun","zonguldak","bolu","kastamonu",
               "corum","amasya","tokat","artvin","bartin","karabuk","sinop","gumushane","bayburt"],
 "Doğu Anadolu": ["erzurum","malatya","elazig","van","erzincan","agri","ardahan","bingol","bitlis",
                  "hakkari","igdir","kars","mus","tunceli"],
 "Güneydoğu Anadolu": ["gaziantep","sanliurfa","diyarbakir","mardin","batman","adiyaman","siirt",
                       "sirnak","kilis"],
}

def uret():
    url = KOK + "/sehir/"
    baslik = "Hizmet Verdiğimiz 81 İl — Video ve 3D Modelleme | Luna Yapım"
    aciklama = ("Luna Yapım 81 ilde hizmet veriyor. Her il için ayrı yazılmış 3D modelleme, emlak video, "
        "ürün animasyonu, klip, drone ve düğün çekimi sayfaları.")
    anahtar = ("il il video çekimi, türkiye geneli drone çekimi, şehir şehir inşaat 3d modelleme, "
        "emlak video çekimi illeri, ürün animasyonu türkiye, prodüksiyon şirketi iller")

    sss = [
     ("81 ilin hepsinde çekim yapıyor musunuz?",
      "3D modelleme, mimari görselleştirme ve ürün animasyonu tamamen uzaktan yürüyor; 81 ilin hepsinde "
      "çalışabiliyoruz. Kamera ve drone gerektiren işlerde Bursa ve çevre illerde kendi ekibimizle, "
      "diğer illerde bölgedeki çözüm ortaklarımızla gidiyoruz."),
     ("Neden bazı illerde daha fazla sayfa var?",
      "Her il için o ilin gerçek talebine göre sayfa açıyoruz. Talebin yoğun olduğu illerde yedi hizmetin "
      "her biri ayrı ayrı anlatılıyor; diğer illerde tüm hizmetler tek ve daha kapsamlı bir il sayfasında "
      "toplanıyor. İçi boş sayfa üretmiyoruz."),
     ("Şehir dışı çekimde ek ücret var mı?",
      "Ulaşım ve gerekiyorsa konaklama teklife ayrı kalem olarak ekleniyor; sürpriz çıkmıyor. Aynı ilde "
      "aynı gün birden fazla iş planlandığında bu maliyet bölünüyor."),
    ]

    semalar = "\n".join('<script type="application/ld+json">\n%s\n</script>' % j(x) for x in (
      {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Ana Sayfa","item":KOK+"/"},
        {"@type":"ListItem","position":2,"name":"İller","item":url}]},
      {"@context":"https://schema.org","@type":"ItemList","name":"Luna Yapım hizmet verdiği iller",
       "numberOfItems":len(SEHIRLER),
       "itemListElement":[{"@type":"ListItem","position":i+1,"name":s["ad"],
                           "url":"%s/sehir/%s.html" % (KOK, s["slug"])} for i, s in enumerate(SEHIRLER)]},
      {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in sss]}))

    g = head(e(baslik), e(aciklama), e(anahtar), url, semalar)
    g += """<div class="page-hero">
  <img class="karga-buyuk" src="../assets/karga.png" alt="">
  <div class="wrap">
    <div class="crumbs"><a href="../">Ana Sayfa</a> · İller</div>
    <h1>Hizmet verdiğimiz <i>81 il</i></h1>
    <p class="lede">Her il için ayrı yazdık — o ilin inşaat piyasası, sanayi profili, coğrafyası ve
      yerel unsurlarıyla. Şablon çoğaltmadık; şehrini seç, kendi sayfanı oku.</p>
  </div>
</div>

<section>
  <div class="wrap prose">
    <p>Luna Yapım Bursa merkezli çalışıyor. Modelleme, mimari görselleştirme ve animasyon işleri tamamen
      uzaktan yürüdüğü için Türkiye'nin her ilinden proje alabiliyoruz. Kamera ve drone gerektiren işlerde
      Bursa ve çevre illerde kendi ekibimizle sahaya çıkıyor, uzak illerde bölgedeki çözüm ortaklarımızla
      çalışıyoruz.</p>
    <p>Aşağıdaki listede <strong>%d ilin</strong> hepsi var. Talebin yoğun olduğu illerde yedi hizmetin her biri
      ayrı sayfada anlatılıyor; diğer illerde hepsi tek ve kapsamlı bir il sayfasında toplanıyor.</p>
  </div>
</section>

""" % len(SEHIRLER)

    for bolge, sluglar in BOLGELER.items():
        iller = [SEHIR_INDEKS[s] for s in sluglar if s in SEHIR_INDEKS]
        iller.sort(key=lambda x: x["ad"])
        satirlar = []
        for c in iller:
            baglar = []
            for anahtar, kalip, _a, _t in HIZMET_ADLARI:
                if sayfa_var(c, anahtar):
                    kisa = {"insaat-3d-modelleme":"3D modelleme","emlak-video":"emlak video",
                            "urun-animasyon":"ürün animasyonu","klip-cekimi":"klip",
                            "drone-cekimi":"drone","dugun-cekimi":"düğün",
                            "isletme-tanitim":"işletme"}[anahtar]
                    baglar.append('<a href="%s-%s">%s</a>' % (c["slug"], anahtar, kisa))
            satirlar.append('<tr><td><a href="%s"><strong>%s</strong></a></td><td>%s</td></tr>'
                            % (c["slug"], e(c["ad"]), " · ".join(baglar) if baglar
                               else '<small>tüm hizmetler il sayfasında</small>'))
        g += """<section class="%s">
  <div class="wrap prose" style="max-width:none">
    <h2>%s</h2>
    <div class='tablo-kaydir'><table>
      <tr><th>İl</th><th>Hizmet sayfaları</th></tr>
      %s
    </table></div>
  </div>
</section>

""" % ("acik" if list(BOLGELER).index(bolge) % 2 == 1 else "", e(bolge), "\n      ".join(satirlar))

    g += video_bolumu("isler", "İşlerimizden")
    g += """<section>
  <div class="wrap prose">
    <h2>Sık sorulan sorular</h2>
    %s
  </div>
</section>

""" % sss_blok(sss)
    g += cta({"slug":"index","ad":"Türkiye"}, "Hangi ildeysen, <i>oradayız</i>.",
             "Projeni ve ilini yaz; kim gidecek, ne kadar sürecek ve neye mal olacak aynı gün söyleyelim.")
    g += FOOTER

    yol = os.path.join(HEDEF, "index.html")
    open(yol, "w", encoding="utf-8").write(g)
    return yol, len(SEHIRLER)

if __name__ == "__main__":
    y, n = uret()
    print("sehir/index.html güncellendi —", n, "il")
