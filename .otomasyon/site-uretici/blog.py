# -*- coding: utf-8 -*-
"""Blog yazıları ve blog/index.html üretici."""
import os, json, html
from kabuk import head, FOOTER
from uretici import HEDEF, KOK, e, j, sss_blok, cta, video_bolumu, kisa_baslik, meta_desc

BLOG = os.path.join(os.path.dirname(HEDEF), "blog")

YAZILAR = [
 {"dosya":"insaat-3d-modelleme-fiyatlari.html",
  "baslik":"İnşaat 3D Modelleme Fiyatları Neye Göre Belirlenir?",
  "tarih":"2026-08-25",
  "ozet":"Mimari render ve proje tanıtım animasyonunda maliyeti belirleyen altı kalem, tipik süreler ve bütçeyi doğru yere harcamanın yolu.",
  "anahtar":"inşaat 3d modelleme fiyatları, mimari render fiyat, proje tanıtım animasyonu maliyeti, 3d görselleştirme ücreti, sanal tur fiyatı",
  "bolumler":[
   ("Kısa cevap", """<p>3D modellemede tek bir liste fiyatı yok, çünkü aynı başlık altında çok farklı işler var: tek bir dış cephe görseli ile çok bloklu bir sitenin iki dakikalık tanıtım filmi arasında on kat fark olabiliyor. Ama maliyeti belirleyen kalemler her projede aynı. Bunları bilirseniz aldığınız teklifi okuyabilir, gereksiz kalemi ayıklayabilirsiniz.</p>"""),
   ("1. Modellenecek hacim", """<p>En büyük kalem bu. Tek blok bir apartman ile on bloklu bir site aynı iş değil; modelleme süresi blok sayısı, cephe karmaşıklığı ve peyzaj alanıyla doğrudan artıyor. Bir de "çevre" var: yapıyı boşlukta göstermek ucuz, gerçek sokağıyla, komşu binalarıyla ve manzarasıyla göstermek pahalı — ama satışa asıl etki eden ikincisi.</p>"""),
   ("2. Daire tipi sayısı", """<p>İç mekân çalışmasında maliyet, blok sayısından çok <strong>daire tipi</strong> sayısına bağlı. 1+1'den 4+1'e altı farklı tipiniz varsa altı ayrı iç mekân kurulumu demektir. Bütçe kısıtlıysa en çok satılan iki tiple başlayıp diğerlerini satış ilerledikçe eklemek mantıklı bir yol.</p>"""),
   ("3. Statik görsel mi, animasyon mu?", """<p>Render görseli tek bir kareyi hesaplar; animasyon saniyede 25 kare. Bu yüzden 60 saniyelik bir tanıtım filmi, aynı kalitede 15 statik görselden belirgin şekilde pahalı. Lansmana yetiştirme baskısı varsa şu sıralamayı öneriyoruz: önce render seti (ilan ve broşür için), sonra animasyon (reklam ve sosyal medya için).</p>"""),
   ("4. Işık senaryosu sayısı", """<p>Aynı modelin gündüz, gün batımı ve gece hâlleri üç ayrı hesaplama demek. Her senaryo maliyeti artırıyor ama işe yarıyor: gün batımı görselleri ilan sitelerinde belirgin şekilde daha çok tıklanıyor, gece görselleri ise cephe aydınlatmasını satan tek şey.</p>"""),
   ("5. Gerçek çekimle birleşim", """<p>Arsanın ya da devam eden şantiyenin drone çekimi yapılıp 3D modelin bu görüntüye oturtulması ayrı bir iş kalemi. Maliyeti artırıyor, buna karşılık projeyi hayali bir boşluktan çıkarıp gerçek konumuna yerleştiriyor. Şehir dışı projelerde ulaşım da bu kaleme giriyor.</p>"""),
   ("6. Revizyon ve teslim formatları", """<p>Ciddi teklifler revizyon hakkını yazar. Bizde taslak aşamasında yön değişikliği sınırsız, yüksek çözünürlüklü render alındıktan sonra iki tur revizyon fiyata dahil. Teslim tarafında ise yatay, dikey ve kare kurgular ile baskı/web çözünürlüğündeki görseller genelde standart olmalı; ayrı ayrı ücretlendiriliyorsa sorun.</p>"""),
   ("Tipik süreler", """<div class='tablo-kaydir'><table>
      <tr><th>İş</th><th>Tipik süre</th></tr>
      <tr><td>Dış cephe render seti (6–10 görsel)</td><td>7–12 iş günü</td></tr>
      <tr><td>Tek blok proje tanıtım animasyonu</td><td>10–15 iş günü</td></tr>
      <tr><td>Çok bloklu site + yerleşim maketi</td><td>3–5 hafta</td></tr>
      <tr><td>İç mekân (daire tipi başına)</td><td>3–5 iş günü</td></tr>
      <tr><td>360° sanal tur</td><td>5–8 iş günü</td></tr>
    </table></div>"""),
   ("Bütçeyi nereye harcamalı", """<p>Kısıtlı bütçeyle en çok işe yarayan sıralama şu: <strong>(1)</strong> ilanda kullanılacak 6–8 dış cephe görseli, <strong>(2)</strong> en çok satılan iki daire tipinin iç mekânı, <strong>(3)</strong> yerleşim maketi, <strong>(4)</strong> tanıtım animasyonu, <strong>(5)</strong> sanal tur. İlk iki madde satışın büyük kısmını taşıyor; animasyon ve sanal tur ise satış hızlandıkça reklam tarafında değer üretiyor.</p>
    <p>Detaylı hizmet açıklaması ve paketler için <a href="../hizmetler/insaat-3d-modelleme">inşaat 3D modelleme sayfamıza</a>, şehrinize özel bilgi için <a href="../sehir/">il sayfalarımıza</a> bakabilirsiniz.</p>"""),
  ],
  "sss":[
   ("Mimari projemiz yok, sadece eskiz var. Yapılabilir mi?",
    "Yapılabilir ama süre uzar ve sonuçta çıkan yapı gerçek projeyle birebir olmaz. Ölçülü bir proje (DWG ya da PDF) verdiğinizde hem maliyet düşer hem de teslim edilen bina görseldekiyle aynı olur."),
   ("Fiyatı metrekare üzerinden mi hesaplıyorsunuz?",
    "Hayır. Metrekare tek başına yanıltıcı; 200 metrekarelik karmaşık cepheli bir villa, 2000 metrekarelik sade bir depodan daha çok emek isteyebiliyor. Blok sayısı, daire tipi ve teslim edilecek çıktı sayısı üzerinden hesaplıyoruz."),
   ("Ödeme nasıl yapılıyor?",
    "İşe başlarken ön ödeme, taslak onayında ara ödeme, teslimde kalan. Uzun projelerde aşamalara bölüyoruz; tutarlar teklifte açıkça yazılı oluyor."),
  ]},

 {"dosya":"emlak-videosu-ilan-performansi.html",
  "baslik":"Emlak Videosu İlan Performansını Gerçekten Değiştiriyor mu?",
  "tarih":"2026-08-25",
  "ozet":"Videolu ilanın asıl faydası tıklanma değil, gelen alıcının niteliği. Ne çekilmeli, hangi sırayla ve ne kadar uzun olmalı.",
  "anahtar":"emlak videosu, ilan videosu, gayrimenkul video çekimi, emlak drone çekimi, sanal tur, ilan performansı, emlak pazarlama",
  "bolumler":[
   ("Asıl fayda tıklanmada değil", """<p>Emlak videosu denince akla ilk gelen "ilan daha çok tıklanır" oluyor. Doğru ama eksik. Videonun asıl faydası <strong>ayak izini azaltması</strong>: alıcı mülkü gelmeden önce gezmiş oluyor, yerinde gezmeye gelen kişi ise gerçekten ilgilenen kişi oluyor. Danışman için bu, günde üç boş gezdirme yerine bir ciddi görüşme demek.</p>
    <p>İkinci fayda ise portföyün kendisiyle ilgili: videosu olan bir ofis, mal sahibinin gözünde "bu evi daha iyi pazarlayacak ofis" oluyor. Portföy toplamak, satmak kadar zor bir işken bu tek başına yeterli bir sebep.</p>"""),
   ("Video ne kadar uzun olmalı", """<p>İlan sitesi için 60–90 saniye. Sosyal medya için 20–30 saniyelik dikey kesim. Web sitesi ve sunum için 2–3 dakikaya kadar çıkılabilir. Bunun ötesi izlenmiyor — özellikle ilan sitelerinde ilk 10 saniyede evin karakteri anlaşılmıyorsa video kapatılıyor.</p>"""),
   ("Hangi sırayla çekilmeli", """<p>Emlak videosunda en çok yapılan hata odaları rastgele gezmek. Doğru sıra genelde şu: <strong>(1)</strong> havadan konum ve çevre, <strong>(2)</strong> giriş ve ilk izlenim, <strong>(3)</strong> yaşam alanı, <strong>(4)</strong> mutfak, <strong>(5)</strong> yatak odaları, <strong>(6)</strong> banyo, <strong>(7)</strong> balkon/bahçe ve manzarayla kapanış. Bu sıra, alıcının evi gerçekte nasıl gezdiğine en yakın olan sıra.</p>"""),
   ("Işık saati her şeyi belirliyor", """<p>Aynı ev sabah 8'de ve öğlen 13'te iki farklı ev gibi görünüyor. Güneye bakan bir salonu öğlen çekerseniz pencereler patlar, kuzeye bakan bir odayı akşamüstü çekerseniz iç karartıcı olur. Çekim öncesi mülkü gezip hangi odanın hangi saatte çekileceğini planlamak, ekipmandan daha çok fark yaratıyor.</p>"""),
   ("Boş mülkte ne yapmalı", """<p>Boş mekân videoda soğuk durur çünkü ölçek algısı kaybolur. İki çözüm var: geniş açı ve akıcı kamera hareketiyle mekânı akıcı göstermek, ya da <strong>dijital mobilyalama</strong> yapmak — boş odaya 3D mobilya yerleştirip mekânın nasıl kullanılacağını göstermek. İkincisi özellikle yeni teslim projelerde satışı hızlandırıyor.</p>"""),
   ("Bitmemiş projede video", """<p>Devam eden bir şantiyeyi tanıtmanın en güçlü yolu gerçek çekimle 3D'yi birleştirmek: şantiyeyi drone ile çekip henüz yapılmamış blokları ve bitmiş iç mekânları <a href="../hizmetler/insaat-3d-modelleme">3D modelleme</a> ile tamamlamak. Alıcı tek filmde hem inşaatın gerçekten ilerlediğini hem de teslimde neyle karşılaşacağını görüyor.</p>"""),
   ("Ofisler için: tek tek mi, abonelik mi?", """<p>Portföyü düzenli çeken ofisler için aylık paket hem ucuz hem pratik: ay içinde belirli sayıda mülk çekimi, sabit fiyat ve öncelikli takvim. Her yeni portföyde ayrı pazarlık yapmak, hem zaman kaybı hem de genelde daha pahalıya geliyor. Detaylar için <a href="../hizmetler/emlak-kurumsal">emlak ve kurumsal sayfamıza</a> bakabilirsiniz.</p>"""),
  ],
  "sss":[
   ("Telefonla çektiğimiz video yeterli olmaz mı?",
    "İlanı kurtarır ama farklılaştırmaz. Asıl fark ışık saatinde, odaların gezilme sırasında ve kurgunun ritminde. Bu üçü doğruysa ekipman ikinci planda kalıyor."),
   ("Mal sahibi çekime izin vermiyor, ne yapmalı?",
    "Dolu mülkte kişisel eşyaları kadrajdan çıkarıyoruz; istenirse boş çekip dijital mobilyalama yapıyoruz. Çoğu itiraz mahremiyet kaygısından geliyor ve bu şekilde çözülüyor."),
   ("Ev satıldıktan sonra video boşa mı gidiyor?",
    "Hayır. 'Bu evi biz sattık' içeriği ofisin en iyi reklamı oluyor; ayrıca benzer portföy arayan mal sahibine gösterilecek örnek işe dönüşüyor."),
  ]},
]


def yazi_uret(y):
    url = "%s/blog/%s" % (KOK, y["dosya"])
    baslik_seo = kisa_baslik("%s | Luna Yapım" % y["baslik"])
    aciklama = meta_desc(y["ozet"])
    semalar = "\n".join('<script type="application/ld+json">\n%s\n</script>' % j(x) for x in (
      {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Ana Sayfa","item":KOK+"/"},
        {"@type":"ListItem","position":2,"name":"Blog","item":KOK+"/blog/"},
        {"@type":"ListItem","position":3,"name":y["baslik"],"item":url}]},
      {"@context":"https://schema.org","@type":"Article","headline":y["baslik"],"description":y["ozet"],
       "url":url,"datePublished":y["tarih"],"dateModified":y["tarih"],"inLanguage":"tr-TR",
       "image":KOK+"/assets/og-image.png",
       "author":{"@type":"Organization","name":"Luna Yapım","url":KOK},
       "publisher":{"@type":"Organization","name":"Luna Yapım",
         "logo":{"@type":"ImageObject","url":KOK+"/assets/og-image.png"}},
       "mainEntityOfPage":{"@type":"WebPage","@id":url}},
      {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in y["sss"]]}))

    g = head(e(baslik_seo), e(aciklama), e(y["anahtar"]), url, semalar)
    g += """<div class="page-hero">
  <img class="karga-buyuk" src="../assets/karga.png" alt="">
  <div class="wrap">
    <div class="crumbs"><a href="../">Ana Sayfa</a> · <a href="./">Blog</a> · Yazı</div>
    <h1>{baslik}</h1>
    <p class="lede">{ozet}</p>
  </div>
</div>

<section>
  <div class="wrap prose">
""".format(baslik=e(y["baslik"]), ozet=e(y["ozet"]))
    for b, icerik in y["bolumler"]:
        g += "    <h2>%s</h2>\n    %s\n\n" % (e(b), icerik)
    g += "    <h2>Sık sorulan sorular</h2>\n    %s\n  </div>\n</section>\n\n" % sss_blok(y["sss"])
    g += video_bolumu("isler", "İşlerimizden")
    g += cta({"slug":"blog"}, "Projenizi <i>konuşalım</i>.",
             "Aklınızdaki işi anlatın; süresini ve maliyetini aynı gün söyleyelim.")
    g += FOOTER
    return y["dosya"], g


def indeks_uret(mevcut):
    url = KOK + "/blog/"
    baslik = "Blog — Video, Drone ve 3D Modelleme Rehberleri | Luna Yapım"
    aciklama = meta_desc("Video prodüksiyon, drone çekimi, inşaat 3D modelleme ve emlak tanıtımı üzerine pratik rehberler: fiyatlar neye göre belirlenir, hangi format ne zaman işe yarar.")
    semalar = "\n".join('<script type="application/ld+json">\n%s\n</script>' % j(x) for x in (
      {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Ana Sayfa","item":KOK+"/"},
        {"@type":"ListItem","position":2,"name":"Blog","item":url}]},
      {"@context":"https://schema.org","@type":"Blog","name":"Luna Yapım Blog","url":url,
       "description":"Video prodüksiyon, drone çekimi, 3D modelleme ve emlak tanıtımı üzerine yazılar.",
       "publisher":{"@type":"Organization","name":"Luna Yapım","url":KOK},
       "blogPost":[{"@type":"BlogPosting","headline":m["baslik"],"url":KOK+"/blog/"+m["dosya"],
                    "datePublished":m["tarih"],"description":m["ozet"]} for m in mevcut]}))

    g = head(e(baslik), e(aciklama), e("video prodüksiyon blog, drone çekimi rehberi, inşaat 3d modelleme yazıları, emlak video rehberi, tanıtım filmi ipuçları"), url, semalar)
    g += """<div class="page-hero">
  <img class="karga-buyuk" src="../assets/karga.png" alt="">
  <div class="wrap">
    <div class="crumbs"><a href="../">Ana Sayfa</a> · Blog</div>
    <h1>Blog</h1>
    <p class="lede">Müşterilerimizin bize en çok sorduğu soruları bir kere düzgün cevaplamak için tutuyoruz. Reklam metni değil, işin içinden gelen not.</p>
  </div>
</div>

<section>
  <div class="wrap prose">
    <h2>Yazılar</h2>
  </div>
  <div class="wrap">
    <div class="urunler">
"""
    for i, m in enumerate(mevcut, 1):
        g += ('      <a class="urun" href="%s"><i class="cizgi"></i><span class="rom">%s</span>'
              '<h3>%s</h3><p>%s</p><span class="ok">Yazıyı oku →</span></a>\n'
              % (m["dosya"], m["tarih"], e(m["baslik"]), e(m["ozet"])))
    g += """    </div>
  </div>
  <div class="wrap prose" style="margin-top:40px">
    <h2>Burada ne yazıyoruz</h2>
    <p>Blogu içerik doldurmak için değil, aynı soruları tekrar tekrar cevaplamamak için tutuyoruz. Fiyatların neye göre değiştiği, hangi işte hangi formatın işe yaradığı, bir çekim gününün gerçekte nasıl geçtiği gibi konular. Kısa cevabı olan bir soruya uzun yazı yazmıyoruz.</p>

    <h2>Sık dokunduğumuz konular</h2>
    <ul>
      <li><strong>Fiyatlandırma</strong> — drone, emlak videosu ve 3D modellemede maliyeti gerçekte ne belirliyor</li>
      <li><strong>İnşaat ve gayrimenkul</strong> — maket satışını hızlandıran görselleştirme, ilan videosunun ilan performansına etkisi</li>
      <li><strong>Sanayi ve ihracat</strong> — fuar öncesi hazırlık, çok dilli ürün anlatımı, gizlilik gerektiren tesislerde 3D kullanımı</li>
      <li><strong>Yerel işletme</strong> — Google işletme profili, düzenli içerik ve haritada görünürlük</li>
      <li><strong>Teknik</strong> — FPV ile klasik drone farkı, ışık saatleri, çekim öncesi hazırlık listesi</li>
    </ul>

    <h2>Yazıları kimin için yazıyoruz</h2>
    <p>Okuyucumuz genelde üç gruptan biri oluyor: bir projeyi tanıtması gereken müteahhit ya da emlak danışmanı, ürününü anlatması gereken üretici, ve sosyal medyada görünmek isteyen yerel işletme sahibi. Üçünün de ortak sorusu aynı: "Bu iş ne kadar tutar ve gerçekten işe yarar mı?" Yazıların çoğu bu iki sorunun etrafında dönüyor.</p>
    <p>Rakam verirken de dikkatli oluyoruz. İnternette dolaşan "drone çekimi şu kadar" tarzı listeler işin kapsamını gizlediği için yanıltıcı; biz bunun yerine <strong>fiyatı neyin belirlediğini</strong> anlatmayı tercih ediyoruz. Böylece aldığınız teklifi okuyabiliyor, gereksiz kalemi ayıklayabiliyorsunuz — teklifi bizden almasanız bile.</p>

    <h2>Sık sorulan sorular</h2>
    <div class="sss">
      <details open><summary>Yazılarda verilen süreler bağlayıcı mı?</summary>
        <div class="cvp"><p>Hayır, tipik aralıklar. Kendi projeniz için net süreyi teklifte yazılı veriyoruz ve teklif çıktıktan sonra değiştirmiyoruz.</p></div></details>
      <details><summary>Neden liste fiyatı yayınlamıyorsunuz?</summary>
        <div class="cvp"><p>Aynı başlık altında çok farklı işler var; tek blok bir proje ile çok bloklu bir site arasında on kat fark olabiliyor. Liste fiyatı ya fazla ödetir ya da işi eksik yaptırır.</p></div></details>
      <details><summary>Yazıdaki konuyu kendi işimize uyarlar mısınız?</summary>
        <div class="cvp"><p>Evet. Projenizi anlatın; hangi formatın işinize yarayacağını, neyi yaptırmanıza gerek olmadığını da söyleyerek konuşalım.</p></div></details>
    </div>

    <h2>Aradığınızı bulamadıysanız</h2>
    <p>Merak ettiğiniz konuyu yazın, sıradaki yazıyı ona ayıralım. Acele bir sorunuz varsa beklemeyin — <a href="../iletisim">iletişim sayfasından</a> ya da WhatsApp'tan doğrudan sorun, aynı gün cevap veriyoruz. Hizmetlerin tamamı için <a href="../hizmetler/">prodüksiyon sayfamıza</a>, şehrinize özel detaylar için <a href="../sehir/">il sayfalarımıza</a> bakabilirsiniz.</p>
  </div>
</section>

"""
    g += cta({"slug":"blog"}, "Sorunuz mu var?", "Yazıya gerek kalmadan cevaplayalım — aynı gün dönüyoruz.")
    g += FOOTER
    return "index.html", g


if __name__ == "__main__":
    mevcut = [{"dosya":"drone-cekimi-fiyatlari.html","baslik":"Drone Çekimi Fiyatları — Neye Göre Belirlenir?",
               "tarih":"2026-07-15","ozet":"Havadan çekimde maliyeti belirleyen kalemler, izin süreçleri ve bütçenizi nereye harcamanız gerektiği."}]
    for y in YAZILAR:
        adi, icerik = yazi_uret(y)
        open(os.path.join(BLOG, adi), "w", encoding="utf-8").write(icerik)
        mevcut.append({k: y[k] for k in ("dosya","baslik","tarih","ozet")})
        print("yazı:", adi)
    mevcut.sort(key=lambda m: m["tarih"], reverse=True)
    adi, icerik = indeks_uret(mevcut)
    open(os.path.join(BLOG, adi), "w", encoding="utf-8").write(icerik)
    print("blog/index.html güncellendi —", len(mevcut), "yazı")
