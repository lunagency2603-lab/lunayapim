# -*- coding: utf-8 -*-
"""Kişiye özel baskı & hediye — ÜRÜN ALT SAYFALARI (20.09.2026).

Ana sayfa: hizmetler/kisiye-ozel-baski-hediye (hediye_hizmet.py). Bu dosya her ürün için
ayrı bir sayfa üretir; her sayfada "Kurumsal" ve "Kişiye özel" başlıkları, baskı-malzeme
bilgisi, sipariş süreci, ürüne özel SSS ve ilgili ürün bağlantıları var.

Kurallar: fiyat yazılmaz; "yapay zekâ" ibaresi geçmez; yalnız gerçekten yaptığımız iş
(tasarım + baskı + ürün tedariki) anlatılır; makine/marka adı, sertifika, sayısal dayanım
iddiası yazılmaz.

Çalıştırma: python3 hediye_urunler.py → hizmetler/<slug>.html (10 sayfa)
"""
import os, sys
from kabuk import head, FOOTER
from uretici import KOK, e, j, sss_blok, cta, kisa_baslik, meta_desc
from yeni_hizmetler import _sema, _surec

ANA = "kisiye-ozel-baski-hediye"
ANA_AD = "Kişiye Özel Baskı & Hediye"


# stüdyosu olan ürünler (hediye-katalog.js'teki kimliklerle birebir)
STUDYOLU = {"uv-dtf-baski", "dtf-baski", "baskili-tisort", "baskili-sweatshirt-hoodie",
            "baskili-yelek", "kisiye-ozel-kupa", "baskili-cakmak", "baskili-kalem",
            "kisiye-ozel-anahtarlik", "magnetli-kapak-acacagi"}


def _vitrin(slug):
    return ("""<section class="acik hs-bolum"><div class="wrap">
  <div class="bas"><span class="no">\u25c6</span><div><h2>Vitrin</h2>
    <p class="aciklama">Hazır tasarımlar. Birine dokunun \u2014 aşağıdaki stüdyoda açılır, \
üstünde istediğiniz gibi oynarsınız.</p></div></div>
  <div data-vitrin="%s"></div>
</div></section>

""") % slug


def _studyo(slug, urun_ad):
    return ("""<section class="acik hs-bolum"><div class="wrap">
  <div class="bas"><span class="no">\u270e</span><div><h2>Tasarım stüdyosu</h2>
    <p class="aciklama">Rengi seçin, tasarımı sürükleyip büyütün, yazıyı kendiniz yazın \u2014 \
ya da kendi dosyanızı açın. Beğendiğinizde tek tuşla sipariş.</p></div></div>
  <div data-studyo="%s">
    <p class="hs-yok">Stüdyo yükleniyor\u2026 Açılmazsa \
<a href="https://wa.me/905411602603">WhatsApp\u0027tan</a> yazın, tasarımı birlikte kuralım.</p>
  </div>
  <p class="hs-kucuk" style="margin-top:26px">Önizleme baskının yerini, ölçüsünü ve rengini gösterir; \
kumaş dokusu ve ekran ayarları yüzünden gerçek ürün birebir aynı görünmeyebilir. Baskıdan önce \
size son bir görsel onayı gönderiyoruz. Dosyanız yüklenmiyor \u2014 tarayıcınızda kalıyor, \
sipariş mesajına indirdiğiniz önizlemeyi ekliyorsunuz.</p>
</div></section>

""") % slug


def _p(*paragraflar):
    return "".join("<p>%s</p>" % x for x in paragraflar)


def _ul(maddeler):
    return "<ul>%s</ul>" % "".join("<li>%s</li>" % m for m in maddeler)


URUNLER = [
# ─────────────────────────────────────────────────────────────── 1. UV DTF
dict(
  dosya="uv-dtf-baski.html", ad="UV DTF Baskı (Soğuk Baskı)",
  baslik_seo="UV DTF Baskı — Soğuk Baskı ile Cam, Metal ve Seramiğe | Luna Yapım",
  aciklama=("UV DTF soğuk baskı: cam bardak, termos, telefon kılıfı, ahşap kutu ve metal yüzeye "
            "ısı gerektirmeyen tam renkli sargı. Firmaya toplu, kişiye tek adet."),
  anahtar=("uv dtf baskı, soğuk baskı, uv dtf sticker, cam bardak baskı, termos baskı, "
           "uv dtf transfer, kişiye özel cam bardak, firmaya özel termos, uv dtf bursa"),
  h1="UV DTF baskı — <i>soğuk baskı</i> ile cam, metal ve seramiğe",
  lede=("Isı gerektirmeyen sargı baskı: cam bardak, termos, telefon kılıfı, ahşap kutu ve metal "
        "yüzeylerde tam renkli, parlak ve suya dayanıklı sonuç. Firmaya toplu, kişiye tek adet."),
  gorsel="uv-dtf-cam-bardak",
  gorsel_alt="UV DTF soğuk baskı: taşıyıcı film soyulurken cam bardakta kalan çiçek deseni ve bitmiş ikinci bardak",
  giris=_p(
    "UV DTF, tasarımın önce özel bir filme basılıp üstüne şeffaf bir taşıyıcı katman "
    "alınmasıyla çalışır. Ortaya çıkan transfer bir çıkartma gibi yüzeye yatırılır, üst film "
    "soyulur ve baskı orada kalır. Isı, pres ya da fırın yok; bu yüzden “soğuk baskı” "
    "deniyor. Sonuç parlak, hafif kabartmalı ve parmakla hissedilen bir katman.",
    "Bu yöntemin asıl gücü kavisli ve sert yüzeylerde. Cam bardağın gövdesi, termosun silindiri, "
    "ahşap kutunun kapağı, metal bir levha: kalıp açmadan, tek adetten başlayarak, fotoğraf "
    "kalitesinde renkle basılabiliyor. Tekstile uygun değil; kumaş için "
    "<a href=\"dtf-baski\">DTF baskı</a> sayfasına bakın."),
  kurumsal=_p(
    "Firmalar UV DTF'yi en çok iki yerde kullanıyor: ofis içi ürünlerde (termos, kahve bardağı, "
    "masa üstü organizatör) ve müşteriye giden ürünlerde (hediye kutusu, şişe, cam kavanoz, "
    "ambalaj üstü küçük seri etiketi). Logo koyu ya da açık zeminde aynı netlikte çıkıyor; "
    "kurumsal renk kodları filme birebir taşınabiliyor.",
    "Kalıp gerektirmediği için elli parçalık bir fuar seti de, beş parçalık bir yönetim hediyesi "
    "de aynı akışla üretiliyor. Aynı tasarımın tekrar siparişinde film yeniden basılıyor, renk "
    "sapması olmuyor. İsteyen firmaya uygulama filmini hazır gönderiyoruz; kendi ekibi ürüne "
    "kendisi yapıştırıyor.") + _ul([
    "Ofis termosu, kahve bardağı, cam sürahi ve bardak takımı",
    "Müşteri hediyesi kutuları ve şişe üstü kişiselleştirme",
    "Vitrin camı, ürün teşhir standı ve masa üstü tabela",
    "Küçük seri ürün ambalajı üstüne logo ve seri etiketi",
    "Fuar ve etkinlik için hızlı, kalıpsız üretim"]),
  kisiye=_p(
    "Kişiye özel tarafta en çok istenen ürün, sosyal medyada sık görülen cam kutu bardak "
    "sargıları: çiçek deseni, isim, tarih ya da kısa bir söz bardağın etrafını dolanıyor. "
    "Onun yanında isimli termos, fotoğraflı telefon kılıfı, düğün ve nişan için üzerine çiftin "
    "adı basılmış cam şişe ve kavanozlar, çocuklar için suluk ve beslenme kutusu geliyor.",
    "Tasarımı sıfırdan biz çiziyoruz ya da elinizdeki fotoğrafı ve el yazısını filme taşıyoruz. "
    "Baskı elle yıkamaya dayanıyor; bulaşık makinesinde zamanla yıpranır, bunu baştan söylüyoruz.") + _ul([
    "İsimli ve tarihli cam kutu bardak, kahve bardağı, termos",
    "Düğün, nişan ve söz için şişe, kavanoz ve hediye kutusu",
    "Fotoğraflı telefon kılıfı ve laptop üstü sargı",
    "Çocuk suluğu, beslenme kutusu ve isimli kalemlik",
    "Ahşap kutu, tepsi ve mum kabı üstüne kişisel tasarım"]),
  teknik=_p(
    "<strong>Uygun yüzeyler:</strong> cam, seramik, metal, sert plastik, cilalı ahşap, akrilik. "
    "Pürüzlü, tozlu ya da yağlı yüzeyde tutmaz; deri ve kumaşa uygulanmaz.",
    "<strong>Renk ve detay:</strong> tam renkli, degrade ve fotoğraf basılabiliyor; beyaz mürekkep "
    "sayesinde koyu ve şeffaf yüzeyde renk kaybolmuyor. Çok ince çizgiler ve küçük punto yazı "
    "için tasarımda asgari kalınlığı biz ayarlıyoruz.",
    "<strong>Boyut:</strong> küçük bir etiketten bardağı tamamen saran sargıya kadar; uygulama "
    "alanının ölçüsünü verin, filmi ona göre kesiyoruz.",
    "<strong>Bakım:</strong> elde yıkama, bulaşık makinesi ve aşındırıcı süngerden uzak tutma. "
    "Uygulama sonrası yirmi dört saat suyla temas etmemesi tutunmayı artırıyor."),
  surec=[("Yüzey ve ölçü", "Hangi ürün, hangi yüzey, kaç adet; uygun olmayan yüzeyi baştan söylüyoruz."),
         ("Tasarım", "Logo, isim ya da desen ürünün ölçüsüne göre çiziliyor; ürün üzerinde ekranda gösteriliyor."),
         ("Film ve uygulama", "Transfer basılıyor; ürünü biz tedarik ediyorsak uygulayıp teslim ediyoruz, istenirse filmi hazır gönderiyoruz."),
         ("Teslim", "Paketlenip elden ya da kargoyla teslim; tasarım dosyası sizde kalıyor.")],
  sss=[
    ("UV DTF ile normal sticker arasındaki fark ne?",
     "Sıradan çıkartma kağıt ya da vinil üstüne basılır ve kenarları görünür. UV DTF'de yalnız "
     "tasarımın kendisi yüzeye geçer, arka plan ya da çerçeve kalmaz; baskı kabartmalı ve "
     "suya dayanıklıdır. Cam bardakta yıkamaya dayanmasının sebebi bu."),
    ("Bulaşık makinesinde çıkar mı?",
     "Zamanla evet, özellikle yüksek sıcaklık programında. Elde yıkanan bardaklarda baskı çok "
     "daha uzun ömürlü oluyor. Bulaşık makinesi şartsa bunu söyleyin, ürün ve yöntemi ona göre "
     "seçelim."),
    ("Kumaşa, tişörte uygulanır mı?",
     "Hayır. UV DTF sert ve pürüzsüz yüzeyler için. Tekstilde ısıyla kumaşa kaynaşan DTF "
     "kullanıyoruz; iki yöntemin adı benziyor ama malzemesi farklı."),
    ("Kendim yapıştırabilir miyim?",
     "Evet. Firmalara ve elinde ürünü olan kişilere uygulama filmini hazır gönderiyoruz; "
     "yüzey temizlenir, film yatırılır, üstü sıyrılır. Kısa bir uygulama notu ekliyoruz."),
    ("Tek bir bardak için de yapıyor musunuz?",
     "Yapıyoruz. Kalıp olmadığı için tek adetle toplu sipariş arasında üretim farkı yok; "
     "yalnız teslim süresi adede göre değişiyor."),
  ],
  ilgili=["dtf-baski", "kisiye-ozel-kupa", "magnetli-kapak-acacagi"],
  cta_bas="Cam, metal ya da seramik — <i>üstüne</i> basalım.",
  cta_alt="Ürünü ve adedi yazın; yüzey uygun mu, tasarım nasıl durur, aynı gün gösterelim.",
),
# ─────────────────────────────────────────────────────────────── 2. DTF
dict(
  dosya="dtf-baski.html", ad="DTF Baskı (Tekstil Transfer)",
  baslik_seo="DTF Baskı — Tişört ve Tekstile Tam Renkli Transfer | Luna Yapım",
  aciklama=("DTF baskı: pamuk, polyester ve karışım kumaşa ısıyla geçen tam renkli transfer. "
            "Koyu kumaşta beyaz alt katman, fotoğraf ve ince detay."),
  anahtar=("dtf baskı, dtf transfer, tekstil baskı, tişört baskı, hoodie baskı, dijital tekstil "
           "baskı, dtf film, kumaşa fotoğraf baskı, dtf baskı bursa"),
  h1="DTF baskı — tekstile <i>tam renkli</i> transfer",
  lede=("Tasarım filme basılıyor, ısıyla kumaşa kaynaşıyor. Pamuk, polyester ve karışım kumaşta "
        "fotoğraf, ince çizgi ve canlı renk; koyu kumaşta beyaz alt katman. Tek tişörtten "
        "ekip setine."),
  gorsel="dtf-isi-presi",
  gorsel_alt="DTF baskı: ısı presinde siyah tişörtten sıcak film soyulurken ortaya çıkan çok renkli desen",
  giris=_p(
    "DTF (direct to film) tekstil baskının son yıllardaki en pratik yöntemi: tasarım önce "
    "özel bir filme basılıyor, üstüne toz yapıştırıcı alınıyor, sonra ısı presinde kumaşa "
    "aktarılıyor. Serigrafideki gibi renk başına kalıp yok, dijital baskıdaki gibi yalnız "
    "açık renkli pamuk şartı yok. Bir fotoğrafı siyah bir hoodie'ye, on renkli bir logoyu "
    "polyester bir forma tek seferde basabiliyoruz.",
    "Baskı kumaşın üstünde ince ve esnek bir katman olarak duruyor; yıkamada çatlamıyor, "
    "ütüde dikkat gerektiriyor. Sert yüzeyler (cam, metal, seramik) bu yöntemin dışında; "
    "onlar için <a href=\"uv-dtf-baski\">UV DTF</a> kullanıyoruz."),
  kurumsal=_p(
    "Firmalar için DTF'nin anlamı basit: küçük adette bile temiz logo. Beş kişilik bir "
    "kafe ekibinin önlükleri, otuz kişilik bir şantiyenin yelekleri, iki yüz kişilik bir "
    "etkinliğin tişörtleri aynı film hattından çıkıyor. Kurumsal renk kodu filme birebir "
    "taşınıyor; lacivert, bordo ya da siyah kumaşta beyaz alt katman logonun rengini "
    "koruyor.",
    "Tekrar siparişte aynı dosya yeniden basıldığı için ilk parti ile üçüncü parti arasında "
    "ton farkı olmuyor. Bedenleri, kumaşı ve baskı yerini (göğüs sol, sırt, kol) tek listede "
    "alıyor, ürünü tedarik edip basılı teslim ediyoruz.") + _ul([
    "Ekip ve personel tişörtü, polo, önlük, iş yeleği",
    "Fuar, kongre ve etkinlik görevli kıyafeti",
    "Kurumsal hoodie ve sweatshirt (kış dönemi, saha ekibi)",
    "Spor kulübü forması ve antrenman tişörtü",
    "Bez çanta ve promosyon tekstili üstüne logo"]),
  kisiye=_p(
    "Kişiye özel tarafta DTF'nin farkı fotoğraf basabilmesi. Doğum günü için çocukluk "
    "fotoğrafı, evlilik yıl dönümü için düğün karesi, bekarlığa veda için grup çizimi, "
    "aile buluşması için aynı tasarımın yirmi bedeni. Tasarımı biz çiziyoruz ya da "
    "gönderdiğiniz görseli baskıya hazırlıyoruz; koyu kumaşta nasıl duracağını basmadan "
    "önce ekranda gösteriyoruz.",
    "Tek parça sipariş alıyoruz; çift tişörtü, anne-bebek takımı, arkadaş grubu hoodie'si "
    "gibi iki-üç parçalık işler en sık gelenler.") + _ul([
    "Fotoğraf baskılı tişört ve sweatshirt",
    "Çift, aile ve arkadaş grubu için eşli tasarımlar",
    "Doğum günü, mezuniyet, bekarlığa veda ve kına tişörtü",
    "Evcil hayvan portresi, çocuk çizimi ve el yazısı baskısı",
    "Bebek zıbını ve çocuk tişörtü üstüne isim"]),
  teknik=_p(
    "<strong>Kumaş:</strong> pamuk, polyester, pamuk-polyester karışımı, likralı kumaş; "
    "açık ve koyu renk fark etmiyor. Çok tüylü polar ve deri uygun değil.",
    "<strong>Baskı alanı:</strong> göğüs sol küçük logo, göğüs orta, sırt tam en, kol ve ense "
    "etiketi; birden fazla alan aynı üründe basılabiliyor.",
    "<strong>Renk ve detay:</strong> sınırsız renk, degrade, fotoğraf; ince çizgi ve küçük "
    "yazı için tasarımda asgari kalınlığı biz koruyoruz. Baskı esnek, kırılmıyor.",
    "<strong>Bakım:</strong> tersten, düşük sıcaklıkta yıkama; baskının üstüne doğrudan ütü "
    "değil, tersten ütü. Kurutma makinesi baskının ömrünü kısaltıyor."),
  surec=[("Ürün ve beden listesi", "Kumaş türü, renk, bedenler ve baskı yeri tek listede alınıyor; ürünü biz tedarik ediyoruz ya da sizinkini basıyoruz."),
         ("Tasarım ve prova", "Logo ya da görsel baskıya hazırlanıyor, ürün üstünde ekranda gösteriliyor; onaysız film basılmıyor."),
         ("Film ve pres", "Transfer basılıyor, ısı presiyle kumaşa aktarılıyor; ilk parça kontrol ediliyor, sonra seri devam ediyor."),
         ("Teslim", "Katlanıp paketleniyor; adede göre elden ya da kargoyla teslim.")],
  sss=[
    ("DTF ile serigrafi arasında ne fark var?",
     "Serigrafi her renk için ayrı kalıp ister; büyük adette ucuzlar, küçük adette ve çok "
     "renkli işte pahalıya gelir. DTF kalıpsızdır: on renkli bir fotoğrafı tek parçaya "
     "basabilirsiniz. Binlerce adetlik tek renkli işte serigrafi hâlâ mantıklı; onu "
     "söylüyoruz."),
    ("Baskı kaç yıkama dayanır?",
     "Doğru bakımla (tersten, düşük sıcaklık, kurutma makinesi yok) kumaşın kendisi kadar "
     "gidiyor. Sayı vermiyoruz çünkü yıkama alışkanlığı ve deterjan sonucu değiştiriyor; "
     "yanlış bakımda önce baskı değil kumaş yıpranıyor."),
    ("Kendi tişörtümü getirsem basar mısınız?",
     "Basarız. Kumaş türünü önceden söyleyin; çok tüylü ya da su itici kaplamalı kumaşta "
     "tutmayabiliyor, o zaman uygun ürünü biz öneriyoruz."),
    ("Koyu renk kumaşta fotoğraf net çıkar mı?",
     "Çıkar. DTF'de renklerin altına beyaz katman basılıyor; siyah hoodie'de fotoğraf beyaz "
     "tişörtteki gibi görünüyor. Provada bunu ekranda gösteriyoruz."),
    ("En az kaç adet?",
     "Tek adet. Toplu siparişte teslim süresi uzuyor, üretim yöntemi değişmiyor."),
  ],
  ilgili=["baskili-tisort", "baskili-sweatshirt-hoodie", "baskili-yelek", "uv-dtf-baski"],
  cta_bas="Kumaşa <i>fotoğraf gibi</i> basalım.",
  cta_alt="Ürünü, kumaşı ve adedi yazın; tasarımı ürün üstünde aynı gün gösterelim.",
),
# ─────────────────────────────────────────────────────────────── 3. TİŞÖRT
dict(
  dosya="baskili-tisort.html", ad="Baskılı Tişört",
  baslik_seo="Baskılı Tişört — Firmaya ve Kişiye Özel Tişört Baskı | Luna Yapım",
  aciklama=("Baskılı tişört: ekip ve etkinlik tişörtünden fotoğraflı hediye tişörte. DTF ile "
            "tam renkli, koyu ve açık kumaşta; tasarım bizden, ürün tedariki dâhil."),
  anahtar=("baskılı tişört, tişört baskı, kişiye özel tişört, firmaya özel tişört, ekip tişörtü, "
           "fotoğraflı tişört, logo baskılı tişört, toplu tişört baskı, tişört baskı bursa"),
  h1="Baskılı tişört — <i>ekip</i> için, <i>hediye</i> için",
  lede=("Göğsünde logo taşıyan ekip tişörtünden üstünde çocukluk fotoğrafı olan doğum günü "
        "tişörtüne: tasarım bizden, kumaş seçimi birlikte, baskı DTF ile."),
  gorsel="tisort-cift",
  gorsel_alt="Aynı karga çizimi baskılı siyah ve beyaz tişört giyen iki kişi, kemik beyazı stüdyo duvarı önünde",
  giris=_p(
    "Tişört, baskının en çok sipariş edilen ürünü; iyi olanla vasat olanı ayıran şey baskı "
    "değil, kumaş ve tasarım dengesi. İnce bir tişörte büyük bir baskı ağır durur, kalın bir "
    "penyeye küçük bir logo kaybolur. Bu yüzden ürünü ve baskıyı ayrı değil, birlikte "
    "seçiyoruz.",
    "Baskıyı <a href=\"dtf-baski\">DTF</a> ile yapıyoruz: koyu ve açık kumaşta aynı canlılık, "
    "fotoğraf ve ince çizgi, tek parçadan başlayan sipariş."),
  kurumsal=_p(
    "Kurumsal tişört iki işe yarıyor: ekibi tanınır kılmak ve markayı gezdirmek. Kafe ve "
    "restoran personeli, teknik servis ekibi, fuar görevlileri, staj programı, şirket "
    "pikniği; her birinde kumaş ve baskı yeri değişiyor. Saha ekibine daha kalın ve koyu "
    "renk, fuar görevlisine açık renk ve büyük sırt baskısı, ofis içine küçük göğüs "
    "logosu öneriyoruz.",
    "Beden listesini alıp ürünü tedarik ediyor, logoyu kurumsal renklerle basıyor, katlanmış "
    "ve bedenine göre etiketlenmiş teslim ediyoruz. Tekrar siparişte aynı ürün ve aynı film "
    "kullanıldığı için partiler arasında fark olmuyor.") + _ul([
    "Personel ve ekip tişörtü (göğüs logo + sırt yazı)",
    "Fuar, kongre, lansman ve tanıtım günü tişörtü",
    "Şirket pikniği, turnuva ve kurumsal koşu takımı",
    "Staj ve oryantasyon seti (tişört + kupa + kalem)",
    "Bayi ve müşteri hediyesi olarak kutulu tişört"]),
  kisiye=_p(
    "Kişiye özel tişörtte kural şu: üzerindeki şey yalnız o kişiye anlam taşımalı. Çocukluk "
    "fotoğrafı, ilk tanışma tarihi, aile içi bir söz, evcil hayvanın portresi, bir çocuk "
    "çizimi. Tasarımı biz yapıyoruz; fotoğrafı temizleyip baskıya hazırlıyoruz, yazıyı "
    "kumaşa uygun kalınlıkta çiziyoruz.",
    "Çiftler için eşli tişört, arkadaş grupları için aynı tasarımın farklı isimli sürümleri, "
    "bebek ve çocuk bedenleri, kına ve bekarlığa veda için toplu ama kişiye özel baskılar en "
    "çok gelen işler.") + _ul([
    "Fotoğraflı doğum günü ve yıl dönümü tişörtü",
    "Çift tişörtü, anne-baba-bebek takımı",
    "Kına, bekarlığa veda ve mezuniyet grubu",
    "Evcil hayvan portresi ve çocuk çizimi baskısı",
    "Hediye kutusunda tek tişört (kurdele ve not kartı dâhil)"]),
  teknik=_p(
    "<strong>Kesim:</strong> oversize (boxy, düşük omuz) ve normal kesim. Oversize tarafta "
    "gövde geniş, boy biraz kısa duruyor ve omuz dikişi kolun üstüne iniyor; sokak giyim "
    "tarafında son iki yıldır istenen kesim bu. Beden seçerken normal bedeninizi söyleyin, "
    "gerisini kesime göre biz ayarlıyoruz.",
    "<strong>Kumaş:</strong> 180 gsm günlük süprem, 220 gsm penye, 240 gsm ağır penye. "
    "Ağır kumaş daha dik duruyor, yıkamada formunu koruyor ve baskı üstüne daha net oturuyor — "
    "oversize kesimin düzgün görünmesi büyük ölçüde buna bağlı.",
    "<strong>Renk:</strong> optik beyaz, ekru krem, yıkamalı siyah, lacivert ve bordo standart; "
    "sezon renkleri stoğa göre. Çocuk, kadın ve erkek bedenleri var; elinizdeki tişörte de "
    "basıyoruz.",
    "<strong>Baskı yeri:</strong> göğüs sol küçük, göğüs orta, sırt tam en, kol, ense; aynı "
    "üründe birden fazla alan mümkün.",
    "<strong>Bakım:</strong> tersten ve düşük sıcaklıkta yıkama, tersten ütü, kurutma makinesi "
    "yok."),
  surec=[("Ürün seçimi", "Kumaş, renk ve bedenler; ekip için beden listesi, hediye için tek beden."),
         ("Tasarım", "Logo ya da fotoğraf baskıya hazırlanıyor, tişört üstünde ekranda gösteriliyor."),
         ("Baskı", "Onaydan sonra DTF ile basılıyor; ilk parça kontrol, sonra seri."),
         ("Teslim", "Katlanmış, bedenine göre etiketli; hediye siparişinde kutu ve kurdele.")],
  sss=[
    ("Hangi kumaş daha iyi: süprem mi penye mi?",
     "Günlük giyim ve hediye için penye daha yumuşak ve dolgun; toplu ekip tişörtünde süprem "
     "daha hafif ve ekonomik. Baskı ikisinde de aynı; kumaşı kullanım yerine göre öneriyoruz."),
    ("Fotoğrafımız düşük çözünürlüklü, basılır mı?",
     "Önce büyütüp temizliyoruz; baskıya yetmiyorsa söylüyor, fotoğrafı çizime çevirme "
     "seçeneğini gösteriyoruz. Basıp sonra “bulanık çıktı” demektense önce ekranda "
     "görmek daha iyi."),
    ("Bedenler karışık olabilir mi?",
     "Olur. Ekip siparişinde her bedenden istediğiniz adedi yazıyorsunuz; tişörtler bedenine "
     "göre etiketlenip teslim ediliyor."),
    ("Baskı yıkanınca çatlar mı?",
     "DTF baskı esnek bir katman; doğru bakımda çatlamıyor. Kurutma makinesi ve doğrudan ütü "
     "ömrünü kısaltıyor, bakım notunu ürünle veriyoruz."),
    ("Tek tişört sipariş edebilir miyim?",
     "Evet. Tek parça hediye siparişi alıyoruz; kutu ve not kartı istenirse ekleniyor."),
  ],
  ilgili=["baskili-sweatshirt-hoodie", "baskili-yelek", "dtf-baski", "kisiye-ozel-kupa"],
  cta_bas="Tişörtün üstünde <i>ne yazsın</i>?",
  cta_alt="Kime, kaç adet, hangi renk — yazın; tasarımı tişört üstünde aynı gün gösterelim.",
),
# ─────────────────────────────────────────────────────────────── 4. SWEATSHIRT & HOODIE
dict(
  dosya="baskili-sweatshirt-hoodie.html", ad="Baskılı Sweatshirt ve Hoodie",
  baslik_seo="Baskılı Sweatshirt ve Hoodie — Kurumsal ve Kişiye Özel | Luna Yapım",
  aciklama=("Baskılı sweatshirt ve hoodie: kış dönemi ekip kıyafeti, kapüşonlu kurumsal hoodie, "
            "çift ve arkadaş grubu için kişiye özel tasarım. DTF ile tam renkli baskı."),
  anahtar=("baskılı hoodie, baskılı sweatshirt, kişiye özel hoodie, firmaya özel sweatshirt, "
           "logo baskılı hoodie, çift hoodie, hoodie baskı, sweatshirt baskı, kapüşonlu baskı"),
  h1="Baskılı sweatshirt ve hoodie — <i>kışın da</i> logo taşısın",
  lede=("Göğüste küçük logo, sırtta büyük tasarım, kolda isim: kalın kumaşta DTF baskı. "
        "Firmaya kış dönemi ekip seti, kişiye çift ve grup hoodie'si."),
  gorsel="tisort-sweatshirt-hoodie",
  gorsel_alt="Karga çizimi baskılı siyah hoodie, beyaz tişört ve krem sweatshirt düz yatış çekimi",
  giris=_p(
    "Sweatshirt ve hoodie, tişörtün kışlık karşılığı ama baskı açısından farklı bir ürün: "
    "kumaş kalın, yüzey daha dokulu, baskı alanı daha geniş. Küçük bir göğüs logosu bu "
    "kumaşta kaybolabiliyor; buna karşılık sırt tam en baskısı ve kol boyunca yazı çok iyi "
    "duruyor. Tasarımı ürünün ölçeğine göre yeniden kuruyoruz, tişörtteki dosyayı olduğu "
    "gibi büyütmüyoruz.",
    "Baskı yöntemi <a href=\"dtf-baski\">DTF</a>; kapüşon, cep ve fermuar gibi dikiş "
    "geçen yerlere değil, düz kumaşa basılıyor."),
  kurumsal=_p(
    "Kış aylarında saha ekibi, kurye, teknik servis ve şantiye personeli tişört yerine "
    "hoodie ve sweatshirt giyiyor; logo görünür kalsın diye göğüs küçük logoyu sırt büyük "
    "yazıyla birlikte öneriyoruz. Ofis ekibi için düz sweatshirt üstüne tek renk logo, "
    "etkinlik ve kamp organizasyonları için kapüşonlu hoodie üstüne büyük tasarım daha "
    "uygun.",
    "Beden listesi alınıyor, ürün tedarik ediliyor, basılıp bedenine göre etiketli teslim "
    "ediliyor. Sezon başında toplu, sezon içinde yeni katılan personel için tek adet ek "
    "sipariş aynı film ve aynı üründen çıkıyor.") + _ul([
    "Kış dönemi saha ve ofis ekibi seti",
    "Kurye, servis ve şantiye personeli hoodie'si",
    "Etkinlik, kamp, gençlik kolu ve kulüp sweatshirt'ü",
    "Bayi ve müşteri hediyesi olarak kutulu hoodie",
    "Okul, kurs ve spor kulübü sezon üniforması"]),
  kisiye=_p(
    "Kişiye özel hoodie en çok çiftler ve arkadaş grupları için geliyor: aynı tasarımın "
    "eşli sürümü, bir yarısı sende bir yarısı bende çizimler, ortak bir tarih ya da şaka. "
    "Doğum günü için sırtta fotoğraf, kolda isim; sınıf ve mezuniyet için aynı tasarımın "
    "yirmi isimli sürümü.",
    "Tasarımı biz çiziyoruz, fotoğrafı baskıya hazırlıyoruz; koyu kumaşta rengin nasıl "
    "duracağını basmadan ekranda gösteriyoruz. Tek parça sipariş alıyoruz.") + _ul([
    "Çift hoodie ve eşli sweatshirt tasarımları",
    "Arkadaş grubu, sınıf ve mezuniyet sürümleri",
    "Sırtta fotoğraf, kolda isim doğum günü hoodie'si",
    "Evcil hayvan portresi ve çocuk çizimi",
    "Hediye kutusunda tek hoodie, not kartıyla"]),
  teknik=_p(
    "<strong>Kesim:</strong> oversize (düşük omuz, geniş gövde) ve normal kesim. Oversize "
    "hoodie'da kapüşon daha dolgun, kol daha uzun duruyor; sırt baskısı için en geniş alan "
    "bu kesimde çıkıyor.",
    "<strong>Ürün:</strong> iki ve üç iplik sweatshirt, şardonlu (içi yumuşak) ve şardonsuz "
    "seçenek, kapüşonlu ve bisiklet yaka, fermuarlı ve fermuarsız; çocuk ve yetişkin "
    "bedenleri; siyah, lacivert, gri, krem ve sezon renkleri.",
    "<strong>Baskı yeri:</strong> göğüs sol küçük, göğüs orta, sırt tam en, kol boyu, kapüşon "
    "ucu; cep ve dikiş üstüne basılmıyor.",
    "<strong>Bakım:</strong> tersten, düşük sıcaklıkta yıkama; baskı üstüne ütü yok; kurutma "
    "makinesi baskının ve kumaşın ömrünü kısaltıyor."),
  surec=[("Ürün ve beden", "Kapüşonlu mu bisiklet yaka mı, şardonlu mu, hangi renk, hangi bedenler."),
         ("Tasarım", "Tasarım hoodie ölçeğine göre yeniden kuruluyor; ürün üstünde ekranda gösteriliyor."),
         ("Baskı", "DTF ile basılıyor; kalın kumaşta ilk parça ayrıca kontrol ediliyor."),
         ("Teslim", "Katlanıp bedenine göre etiketleniyor; hediye siparişinde kutu.")],
  sss=[
    ("Şardonlu ne demek, hangisini seçmeliyim?",
     "Şardonlu kumaşın içi tüylendirilmiş, daha sıcak ve yumuşak; kış ve hediye için uygun. "
     "Şardonsuz daha ince ve serin, sonbahar-ilkbahar ekip kıyafetinde tercih ediliyor. "
     "Baskı ikisinde de aynı."),
    ("Kapüşonun üstüne ya da cebe baskı olur mu?",
     "Kapüşonun düz kısmına küçük bir yazı basılabiliyor; cep ve fermuar gibi dikişli, "
     "katmanlı yerlere basmıyoruz çünkü pres düzgün oturmuyor. Alternatif yerleşimi provada "
     "gösteriyoruz."),
    ("Tişörtteki tasarımımı aynı şekilde hoodie'ye basar mısınız?",
     "Basarız ama ölçeğini yeniden kuruyoruz: tişörtte iyi duran küçük logo hoodie'de "
     "kayboluyor, sırt tasarımı ise büyütülünce çözünürlük ister. Dosyanız vektörse sorun "
     "yok, değilse söylüyoruz."),
    ("Ekip için sezon içinde tek adet ek sipariş verebilir miyiz?",
     "Evet. Aynı ürün ve aynı film dosyası kullanıldığı için sonradan gelen personel için "
     "tek parça basıyoruz; ton farkı olmuyor."),
    ("Çift hoodie'de iki farklı beden ve renk olabilir mi?",
     "Olur. Aynı tasarımın iki yarısı ya da iki sürümü, farklı beden ve renkte, tek "
     "siparişte basılıyor."),
  ],
  ilgili=["baskili-tisort", "baskili-yelek", "dtf-baski"],
  cta_bas="Sırtta büyük, göğüste küçük — <i>hoodie</i>'ye basalım.",
  cta_alt="Kaç kişi, hangi renk, kapüşonlu mu — yazın; tasarımı ürün üstünde gösterelim.",
),
# ─────────────────────────────────────────────────────────────── 5. YELEK
dict(
  dosya="baskili-yelek.html", ad="Baskılı Yelek",
  baslik_seo="Baskılı Yelek — Firmaya Özel İş ve Etkinlik Yeleği | Luna Yapım",
  aciklama=("Baskılı yelek: saha ekibi, kurye ve etkinlik görevlisi için logo baskılı iş yeleği; "
            "hobi ve kulüpler için kişiye özel yelek. Göğüs ve sırt baskısı."),
  anahtar=("baskılı yelek, logo baskılı yelek, iş yeleği baskı, firmaya özel yelek, etkinlik yeleği, "
           "personel yeleği, şantiye yeleği baskı, kişiye özel yelek, yelek baskı bursa"),
  h1="Baskılı yelek — <i>sahada</i> görünür, <i>etkinlikte</i> tanınır",
  lede=("Kurye, saha ekibi, şantiye ve fuar görevlisi için logo baskılı iş yeleği; kulüp ve hobi "
        "grupları için kişiye özel yelek. Göğüste küçük, sırtta büyük baskı."),
  gorsel="kurumsal-yelek-polo-sapka",
  gorsel_alt="Lacivert yelek, polo tişört ve şapkada aynı LY monogramı; yaka kartı ve kalemle kurumsal ekip seti",
  giris=_p(
    "Yelek, kurumsal giyimin en pratik parçası: tişörtün ya da gömleğin üstüne giyiliyor, "
    "mevsime göre çıkarılıyor, logoyu her zaman öne alıyor. Saha ekiplerinde “bizden "
    "biri” demenin en hızlı yolu; etkinliklerde görevliyi kalabalıktan ayıran tek şey.",
    "Baskıyı <a href=\"dtf-baski\">DTF</a> ile yapıyoruz; yeleğin düz göğüs ve sırt "
    "panellerine basılıyor, cep ve fermuar hattına değil. Ürünü de biz tedarik ediyoruz: "
    "şişme (puffer) yelek, softshell yelek, hafif spor yelek ve cepli iş yeleği seçenekleri."),
  kurumsal=_p(
    "Kurumsal yelekte iki ihtiyaç var: kimlik ve işlev. Kurye ve teslimat ekibi için hafif, "
    "cepli ve sırtta büyük logolu; şantiye ve depo için dayanıklı kumaş ve göğüs baskısı; "
    "fuar, kongre ve saha satış ekibi için düzgün duran softshell ve küçük logo. Yeleği "
    "polo tişört ve şapkayla aynı monogramda basınca tek bakışta tanınan bir ekip seti "
    "çıkıyor.",
    "Beden listesini alıyor, ürünü tedarik ediyor, basılı ve etiketli teslim ediyoruz. "
    "Sezon değişiminde aynı logo yaz için tişörte, kış için yeleğe basılıyor; ürün "
    "değişiyor, tasarım dosyası aynı kalıyor.") + _ul([
    "Kurye, teslimat ve servis ekibi yeleği",
    "Şantiye, depo ve üretim sahası iş yeleği",
    "Fuar, kongre ve etkinlik görevli yeleği",
    "Saha satış ve tanıtım ekibi softshell yeleği",
    "Site güvenliği, otopark ve vale ekibi"]),
  kisiye=_p(
    "Kişiye özel yelek daha çok hobi ve grup işi: balıkçılık ve doğa yürüyüşü yeleğine "
    "isim ve rozet, motosiklet grubu için sırt tasarımı, avcılık ve kamp kulübü için grup "
    "logosu, amatör spor takımı için antrenör yeleği. Bir de hediye tarafı var: babaya "
    "isimli balıkçı yeleği, dedeye köy adı işlenmiş hafif yelek.",
    "Tasarımı biz çiziyoruz ya da grubun mevcut amblemini baskıya hazırlıyoruz; tek parça "
    "sipariş alıyoruz.") + _ul([
    "Balıkçılık, doğa yürüyüşü ve kamp yeleği üstüne isim",
    "Motosiklet ve bisiklet grubu sırt tasarımı",
    "Amatör takım antrenör ve saha görevlisi yeleği",
    "Hobi kulübü ve dernek amblemi",
    "Hediye olarak isimli tek yelek"]),
  teknik=_p(
    "<strong>Ürün:</strong> şişme (puffer) yelek, softshell yelek, hafif spor yelek, çok cepli "
    "iş yeleği; siyah, lacivert, gri, haki ve sezon renkleri; yetişkin bedenleri.",
    "<strong>Baskı yeri:</strong> göğüs sol küçük logo, sırt üst orta büyük logo ya da yazı; "
    "cep, fermuar ve kapitone dikişi üstüne basılmıyor, tasarım düz panele göre yerleşiyor.",
    "<strong>Bakım:</strong> düşük sıcaklıkta yıkama, tersten kurutma; şişme yelekte baskı "
    "üstüne ütü yok."),
  surec=[("Model ve beden", "Şişme mi softshell mi, kaç cep, hangi renk, hangi bedenler; kullanım yerine göre model öneriyoruz."),
         ("Tasarım", "Logo göğüs ve sırt paneline göre ölçekleniyor; yelek üstünde ekranda gösteriliyor."),
         ("Baskı", "DTF ile düz panellere basılıyor; kapitone yelekte ilk parça ayrıca kontrol ediliyor."),
         ("Teslim", "Bedenine göre etiketli; polo ve şapkayla set hâlinde istenirse birlikte.")],
  sss=[
    ("Şişme (kapitone) yeleğe baskı olur mu?",
     "Olur; baskı kapitone dikişlerinin arasındaki düz panele yerleşiyor. Çok küçük "
     "panelli modellerde logo ölçüsü sınırlanıyor, o yüzden modeli baştan birlikte "
     "seçiyoruz."),
    ("Reflektif (ışık yansıtan) şerit ekleyebilir misiniz?",
     "Baskı olarak hayır; reflektif şerit ürünün kendisinde olmalı. Reflektifli iş yeleği "
     "modelleri var, ihtiyaç buysa o ürünü tedarik edip üstüne logo basıyoruz."),
    ("Yelek, polo ve şapkayı aynı siparişte alabilir miyiz?",
     "Evet. Aynı monogram ya da logo üç ürüne de basılıyor, set hâlinde teslim ediliyor; "
     "ekip seti en çok bu şekilde gidiyor."),
    ("Sırta büyük yazı, göğse küçük logo aynı yelekte olur mu?",
     "Olur; en yaygın yerleşim bu. Göğüste firma adı ya da logo, sırtta bölüm ya da görev "
     "adı (“Teknik Servis”, “Görevli” gibi)."),
    ("Kendi yeleğimize basar mısınız?",
     "Basarız. Kumaşı ve modelini önceden söyleyin; su itici kaplamalı bazı kumaşlarda "
     "tutunma zayıf oluyor, o durumda uygun ürünü öneriyoruz."),
  ],
  ilgili=["baskili-tisort", "baskili-sweatshirt-hoodie", "baskili-kalem"],
  cta_bas="Ekibi <i>tek bakışta</i> tanıtalım.",
  cta_alt="Kaç kişi, hangi model, göğüs mü sırt mı — yazın; tasarımı yelek üstünde gösterelim.",
),
# ─────────────────────────────────────────────────────────────── 6. KUPA
dict(
  dosya="kisiye-ozel-kupa.html", ad="Kişiye Özel Kupa Bardak",
  baslik_seo="Kişiye Özel Kupa Bardak — Fotoğraflı ve İsimli Kupa | Luna Yapım",
  aciklama=("Kişiye özel kupa bardak: fotoğraflı ve isimli hediye kupa, çift kupa takımı, firmaya "
            "logolu ofis ve müşteri kupası. Beyaz kupa ve renkli iç-kulp seçenekleri."),
  anahtar=("kişiye özel kupa, fotoğraflı kupa, isimli kupa bardak, kupa baskı, firmaya özel kupa, "
           "logolu kupa, renkli kulp kupa, çift kupa, sevgiliye kupa, kupa baskı bursa"),
  h1="Kişiye özel kupa bardak — <i>her sabah</i> eline alınan hediye",
  lede=("Fotoğraf, isim, tarih ya da logo; beyaz seramik kupa ve renkli iç-kulp seçenekleri. "
        "Sevgiliye tek kupa, ofise elli kupa: tasarım bizden, baskı ve kutu dâhil."),
  gorsel="cift-fotografli-kupa",
  gorsel_alt="Elde tutulan beyaz kupa üzerinde çift fotoğrafı, suluboya kenar ve el yazısı isim-tarih; yanında kırmızı kulplu ikinci kupa",
  giris=_p(
    "Kupa, hediyelerin en çok kullanılanı: rafta durmuyor, her gün masada. Bu yüzden "
    "üstündeki tasarım ilk bakışta değil, yüzüncü bakışta da iyi durmalı. Fotoğrafı "
    "kupanın kavisine göre yerleştiriyor, yazıyı kulp çevresine sıkışmayacak şekilde "
    "kuruyor, koyu iç renkte dış tasarımın nasıl duracağını basmadan gösteriyoruz.",
    "Beyaz seramik kupa standart; iç ve kulp rengi (kırmızı, siyah, lacivert, yeşil, "
    "sarı ve diğerleri) tasarıma göre seçiliyor. Kupa gövdesi tam çevre basılıyor, kulp "
    "bölgesi hariç."),
  kurumsal=_p(
    "Kurumsal kupa üç yerde çalışıyor: ofis içinde (personel kupası, toplantı odası "
    "takımı), müşteriye giden hediyede (yeni yıl, bayram, sözleşme yıl dönümü) ve hoş "
    "geldin setinde (yeni personel, staj, bayi). Logo tek başına sıkıcı kalıyor; logoyla "
    "birlikte kurumsal renkte iç-kulp ve kısa bir cümle daha çok tutuluyor.",
    "Adet arttıkça teslim süresi uzuyor, kalite değişmiyor; kutulu ve tek tek paketli "
    "teslim ediyoruz. Tekrar siparişte aynı ürün ve aynı tasarım dosyası kullanılıyor.") + _ul([
    "Personel ve toplantı odası kupası (logo + kurumsal renk kulp)",
    "Yeni yıl, bayram ve yıl dönümü müşteri hediyesi",
    "Hoş geldin seti: kupa + kalem + tişört",
    "Bayi, tedarikçi ve iş ortağı hediyesi",
    "Kafe ve restoran için isimli kupa takımı"]),
  kisiye=_p(
    "Kişiye özel kupa en çok çiftler için isteniyor: bir fotoğraf, iki isim, bir tarih; "
    "eşli iki kupa, biri kırmızı kulp biri siyah. Onun ardından anneler ve babalar günü "
    "için çocukluk fotoğrafı, öğretmene sınıf fotoğrafı, doğum günü için arkadaş grubunun "
    "karesi, evcil hayvanın portresi geliyor.",
    "Fotoğrafı temizleyip kupaya göre kesiyoruz; suluboya kenar, el yazısı isim ve tarih "
    "gibi düzenlemeleri tasarımda biz yapıyoruz. Tek kupa sipariş alıyoruz; kutu ve not "
    "kartı ekleniyor.") + _ul([
    "Çift kupa takımı (fotoğraf + isimler + tarih)",
    "Anneler günü, babalar günü ve doğum günü kupası",
    "Öğretmen, mezuniyet ve sınıf hatırası kupası",
    "Evcil hayvan portresi ve çocuk çizimi kupası",
    "Yeni ev, yeni iş ve emeklilik hediyesi"]),
  teknik=_p(
    "<strong>Ürün:</strong> beyaz seramik kupa; iç ve kulp rengi seçenekleri; standart ve "
    "büyük boy. Renkli iç kupalarda dış tasarım beyaz zemine basılıyor.",
    "<strong>Baskı alanı:</strong> gövde tam çevre, kulp bölgesi hariç; tek fotoğraf, iki "
    "yüzlü farklı tasarım ya da çevreyi dolanan yazı.",
    "<strong>Fotoğraf:</strong> net ve yeterli çözünürlükte olmalı; zayıf fotoğrafı önce "
    "büyütüp temizliyoruz, yetmezse çizim seçeneğini öneriyoruz.",
    "<strong>Bakım:</strong> elde yıkama en uzun ömürlü; bulaşık makinesinde zamanla solma "
    "olabiliyor, bunu ürünle birlikte not olarak veriyoruz."),
  surec=[("Kupa ve renk", "Beyaz mı renkli kulp mu, kaç adet, tek tasarım mı isimli sürümler mi."),
         ("Tasarım", "Fotoğraf ve yazı kupanın kavisine göre yerleştiriliyor; kupa üstünde ekranda gösteriliyor."),
         ("Baskı", "Onaydan sonra basılıyor; renkli iç kupada ilk parça ayrıca kontrol ediliyor."),
         ("Teslim", "Tek tek kutulu; hediye siparişinde kurdele ve not kartı.")],
  sss=[
    ("Kupanın her yerine baskı olur mu?",
     "Gövdenin tamamına, kulp bölgesi hariç. Fotoğraf genellikle bir yüze, isim ve tarih "
     "diğer yüze ya da altına yerleşiyor; çevreyi dolanan yazı da mümkün."),
    ("Bulaşık makinesinde çıkar mı?",
     "Elde yıkamada uzun yıllar gidiyor; bulaşık makinesinde yüksek sıcaklık ve deterjan "
     "zamanla soldurabiliyor. Bunu gizlemiyoruz, bakım notunu kupayla veriyoruz."),
    ("Renkli kulp seçenekleri neler?",
     "Kırmızı, siyah, lacivert, yeşil, sarı, turuncu, pembe ve stoğa göre diğerleri. "
     "Tasarımın ana rengine göre kulp rengini biz öneriyoruz; ekranda gösteriyoruz."),
    ("İki kupaya farklı fotoğraf ve isim basılır mı?",
     "Basılır. Çift takımlarında her kupa ayrı tasarımlı olabiliyor; ofis siparişinde de "
     "her personelin adı ayrı ayrı basılıyor."),
    ("Tek kupa için hediye kutusu var mı?",
     "Var. Kutu, kurdele ve isteğe bağlı el yazısı not kartı; kargoyla gönderimde kupa "
     "ayrıca korumaya alınıyor."),
  ],
  ilgili=["kisiye-ozel-anahtarlik", "magnetli-kapak-acacagi", "uv-dtf-baski", "baskili-kalem"],
  cta_bas="Kupanın üstünde <i>kim</i> olsun?",
  cta_alt="Fotoğrafı ve isimleri gönderin; tasarımı kupa üstünde aynı gün gösterelim.",
),
# ─────────────────────────────────────────────────────────────── 7. ÇAKMAK
dict(
  dosya="baskili-cakmak.html", ad="Baskılı Çakmak",
  baslik_seo="Baskılı Çakmak — Promosyon ve İsimli Çakmak Baskısı | Luna Yapım",
  aciklama=("Baskılı çakmak: kafe, restoran, bar ve bayi için logolu promosyon çakmağı; isimli ve "
            "tasarımlı kişiye özel çakmak. Renk seçenekleri, adede göre üretim."),
  anahtar=("baskılı çakmak, promosyon çakmak, logolu çakmak, firmaya özel çakmak, isimli çakmak, "
           "kişiye özel çakmak, çakmak baskı, toplu çakmak baskı, promosyon ürünleri bursa"),
  h1="Baskılı çakmak — <i>elden ele</i> dolaşan logo",
  lede=("Kafe, restoran, bar ve bayi için logolu promosyon çakmağı; isimli ve tasarımlı kişiye "
        "özel çakmak. Beyaz, siyah, renkli gövde; tek renk ya da tam renkli baskı."),
  gorsel="baskili-cakmak",
  gorsel_alt="Bir sırada beş renkte LY monogramlı çakmak, biri yanık; kemik beyazı keten yüzeyde kraft kutu",
  giris=_p(
    "Çakmak, promosyon ürünleri arasında en çok el değiştireni: masada unutuluyor, "
    "ödünç veriliyor, cepten cebe geçiyor. Üstündeki logo bu yüzden bir kişiye değil, "
    "birkaç kişiye ulaşıyor. Küçük bir baskı alanı var; tasarımı buna göre sadeleştirmek "
    "işin yarısı.",
    "Gövde rengini ve baskı rengini birlikte seçiyoruz; koyu gövdede açık logo, açık "
    "gövdede kurumsal renk. Tam renkli baskı da mümkün ama küçük alanda tek renk çoğu "
    "zaman daha net okunuyor."),
  kurumsal=_p(
    "Çakmağı en çok kafe, restoran, bar, benzin istasyonu, oto yıkama ve tekel bayileri "
    "kullanıyor: kasada verilen, masaya bırakılan, müşteriyle giden en ucuz reklam. "
    "Logo ve telefon numarası ya da Instagram adı en işlevli kombinasyon; adres ve slogan "
    "bu alana sığmıyor, sığdırmaya çalışmıyoruz.",
    "Adede göre üretiliyor; renk karışık olabiliyor (siyah, beyaz, kırmızı, mavi, yeşil "
    "gövde aynı siparişte). Tekrar siparişte aynı gövde ve aynı baskı dosyası.") + _ul([
    "Kafe, bar, restoran ve nargile salonu masa çakmağı",
    "Benzin istasyonu, oto yıkama ve tekel bayii kasa promosyonu",
    "Fuar, festival ve etkinlik dağıtım ürünü",
    "Otel, pansiyon ve kamp alanı hoş geldin seti",
    "Bayi ve müşteri promosyon paketi (çakmak + kalem + anahtarlık)"]),
  kisiye=_p(
    "Kişiye özel çakmakta konu isim ve şaka: bir arkadaşın lakabı, bir çiftin tarihi, "
    "bekarlığa veda için grubun içi sözü, doğum günü için kısa bir çizim. Tek adet "
    "basıyoruz; kutuya koyup not kartı ekliyoruz.",
    "Düğün ve nişan masalarında misafire bırakılan isimli çakmak, kına gecesinde dağıtılan "
    "tarihli çakmak da sık gelen işler; misafir sayısına göre karışık renkte üretiliyor.") + _ul([
    "İsimli ve lakaplı hediye çakmak",
    "Bekarlığa veda ve kına gecesi dağıtım çakmağı",
    "Düğün ve nişan masası hatırası (isim + tarih)",
    "Doğum günü için çizimli ve sözlü tasarım",
    "Hediye kutusunda tek çakmak"]),
  teknik=_p(
    "<strong>Ürün:</strong> plastik gövdeli doldurulabilir çakmak; siyah, beyaz, kırmızı, mavi, "
    "yeşil, sarı ve stoğa göre diğer gövde renkleri; metal gövdeli seçenek de var.",
    "<strong>Baskı alanı:</strong> gövdenin ön yüzü, isteğe göre iki yüz; küçük alan olduğu için "
    "logo sadeleştirilip yazı kalınlığı ayarlanıyor.",
    "<strong>Baskı:</strong> tek renk ya da tam renkli; koyu gövdede beyaz alt katman. Baskı "
    "gövdeye yapışık, tırnakla kazınmıyor, alevden uzak bölgede."),
  surec=[("Gövde ve adet", "Plastik mi metal mi, hangi renkler, kaç adet; karışık renk mümkün."),
         ("Tasarım", "Logo çakmak ölçüsüne göre sadeleştiriliyor; gövde üstünde ekranda gösteriliyor."),
         ("Baskı", "Onaydan sonra basılıyor; ilk parça okunurluk için kontrol ediliyor."),
         ("Teslim", "Kutulu ya da toplu paket; hediye siparişinde tek kutu ve not kartı.")],
  sss=[
    ("Baskı çakmağın üstünden silinir mi?",
     "Gövdeye yapışık bir katman, normal kullanımda silinmiyor. Sert bir cisimle "
     "kazınırsa çizilebilir; alev bölgesinden uzakta durduğu için ısıdan etkilenmiyor."),
    ("Tek renk mi tam renkli mi basmalıyım?",
     "Alan küçük olduğu için tek renk logo daha net okunuyor; çok renkli logoyu tek renge "
     "indirmek gerektiğinde bunu tasarımda gösteriyoruz. Fotoğraf ve degrade istenirse tam "
     "renkli basıyoruz."),
    ("Gövde renkleri karışık olabilir mi?",
     "Olabilir. Aynı siparişte beş rengi de karıştırabilirsiniz; adet dağılımını "
     "listede yazıyorsunuz."),
    ("Telefon numarası ve Instagram adı sığar mı?",
     "Logo ile birlikte biri sığıyor, ikisi zorlanıyor. Kafe ve bar için genellikle "
     "Instagram adı, servis işleri için telefon öneriyoruz."),
    ("Tek çakmak sipariş verebilir miyim?",
     "Evet. Tek adet isimli çakmak basıyoruz; kutu ve not kartı isteğe bağlı."),
  ],
  ilgili=["baskili-kalem", "kisiye-ozel-anahtarlik", "magnetli-kapak-acacagi"],
  cta_bas="Logoyu <i>cebe</i> koyalım.",
  cta_alt="Kaç adet, hangi renk, üstünde ne yazsın — yazın; tasarımı gövde üstünde gösterelim.",
),
# ─────────────────────────────────────────────────────────────── 8. KALEM
dict(
  dosya="baskili-kalem.html", ad="Baskılı Kalem",
  baslik_seo="Baskılı Kalem — Promosyon Kalemi ve İsimli Metal Kalem | Luna Yapım",
  aciklama=("Baskılı kalem: fuar, toplantı ve ofis için logolu promosyon kalem; öğretmen ve "
            "mezuniyet için isimli kalem. Metal ve plastik gövde, kutulu teslim."),
  anahtar=("baskılı kalem, promosyon kalem, logolu kalem, firmaya özel kalem, isimli kalem, "
           "kişiye özel kalem, metal kalem baskı, kalem baskı, toplu kalem baskı"),
  h1="Baskılı kalem — <i>her imzada</i> görünen isim",
  lede=("Fuar, toplantı ve ofis için logolu promosyon kalem; öğretmene, mezuna ve imza masasına "
        "isimli kalem. Metal ve plastik gövde, gövde ve klips baskısı, kutulu teslim."),
  gorsel="baskili-kalem",
  gorsel_alt="Kemik beyazı keten üstünde çapraz dizilmiş LY monogramlı siyah ve gümüş metal kalemler, biri not kartına yazıyor",
  giris=_p(
    "Kalem, promosyonun en eski ve hâlâ en çok dağıtılan ürünü; sebebi basit, herkes "
    "kullanıyor ve kimse geri vermiyor. Ucuz plastik kalemle metal gövdeli kalem arasındaki "
    "fark, kalemin kaç gün cepte kalacağı. Fuarda dağıtılan için plastik, müşteri "
    "hediyesi için metal öneriyoruz.",
    "Baskı gövde boyuna ve isteğe göre klipse yapılıyor; metal kalemde tek renk gravür "
    "görünümlü baskı, plastik kalemde tek ya da çok renkli baskı."),
  kurumsal=_p(
    "Kurumsal kalem üç yerde çalışıyor: fuar ve etkinlik dağıtımı (adet çok, gövde plastik, "
    "logo net), toplantı ve imza masası (metal gövde, kutulu, logo sade) ve hoş geldin seti "
    "(kupa ve tişörtle birlikte). Muhasebe ve mali müşavirlik ofisleri, bankacılık ve "
    "sigorta acenteleri, emlak ofisleri ve klinikler en çok sipariş veren gruplar.",
    "Logo ile birlikte web adresi ya da telefon gövdeye sığıyor; slogan sığmıyor. Tekrar "
    "siparişte aynı model ve aynı dosya kullanılıyor.") + _ul([
    "Fuar, kongre ve etkinlik dağıtım kalemi",
    "Toplantı odası ve imza masası kutulu metal kalem",
    "Muhasebe, sigorta, emlak ve klinik promosyonu",
    "Hoş geldin seti (kalem + kupa + tişört)",
    "Bayi ve müşteri yeni yıl hediyesi"]),
  kisiye=_p(
    "Kişiye özel kalem hediye olarak bir anlam taşıyor: öğretmene ad soyad, mezuna okul ve "
    "yıl, yeni işe başlayana unvan, nikâh masasına çiftin adı ve tarih. Metal gövdeye tek "
    "renk isim baskısı en çok istenen; kutu ve not kartıyla teslim ediyoruz.",
    "Bir de imza kalemi var: düğün nikâh defteri, sözleşme imzası, kitap imza günü için "
    "üstünde isim ve tarih yazan tek kalem.") + _ul([
    "Öğretmenler günü ve yıl sonu hediyesi",
    "Mezuniyet, yeni iş ve terfi hediyesi",
    "Nikâh ve söz masası imza kalemi (isim + tarih)",
    "Doğum günü için isimli metal kalem",
    "Kutulu tek kalem, not kartıyla"]),
  teknik=_p(
    "<strong>Ürün:</strong> plastik gövdeli tükenmez (beyaz, siyah, mavi, kırmızı ve stoğa "
    "göre diğer renkler), metal gövdeli tükenmez (siyah, gümüş, lacivert); mavi ve siyah "
    "mürekkep.",
    "<strong>Baskı alanı:</strong> gövde boyu tek satır, isteğe göre klips; metal kalemde tek "
    "renk, plastik kalemde tek ya da çok renkli baskı.",
    "<strong>Paket:</strong> toplu siparişte poşetli, hediye siparişinde tek kutu ve not "
    "kartı."),
  surec=[("Model ve adet", "Plastik mi metal mi, hangi renk, kaç adet; kullanım yerine göre model öneriyoruz."),
         ("Tasarım", "Logo ya da isim gövde boyuna göre tek satıra kuruluyor; kalem üstünde ekranda gösteriliyor."),
         ("Baskı", "Onaydan sonra basılıyor; ilk parça okunurluk için kontrol ediliyor."),
         ("Teslim", "Toplu poşetli ya da tek tek kutulu; setle birlikte istenirse aynı pakette.")],
  sss=[
    ("Metal kalemde baskı silinir mi?",
     "Metal gövdeye yapılan tek renk baskı normal kullanımda silinmiyor; gravür görünümlü "
     "olduğu için çizilse de okunurluk kalıyor. Plastik kalemde de gövdeye yapışık, tırnakla "
     "çıkmıyor."),
    ("Logo ile birlikte web adresi sığar mı?",
     "Gövde boyu tek satıra logo ve kısa bir adres sığıyor; uzun adresleri kısaltıyor ya da "
     "klipse taşıyoruz. Tasarımda ölçekli gösteriyoruz."),
    ("Her kaleme farklı isim basılır mı?",
     "Basılır. Sınıf, ekip ya da masa listesi gönderirsiniz; her kalem kendi ismiyle "
     "basılıp ayrı poşetleniyor."),
    ("Mürekkep rengi seçebilir miyim?",
     "Mavi ve siyah standart; modele göre kırmızı ve yeşil de var. Nikâh ve imza kalemi "
     "için genellikle siyah öneriyoruz."),
    ("Tek kalem hediye siparişi veriyor musunuz?",
     "Evet. Tek metal kalem, kutu ve not kartıyla; kargoyla da gönderiyoruz."),
  ],
  ilgili=["baskili-cakmak", "kisiye-ozel-kupa", "kisiye-ozel-anahtarlik"],
  cta_bas="İsmi <i>kalemin üstüne</i> yazalım.",
  cta_alt="Kaç adet, metal mi plastik mi, üstünde ne yazsın — yazın; tasarımı gösterelim.",
),
# ─────────────────────────────────────────────────────────────── 9. ANAHTARLIK
dict(
  dosya="kisiye-ozel-anahtarlik.html", ad="Kişiye Özel Anahtarlık",
  baslik_seo="Kişiye Özel Anahtarlık — Fotoğraflı, İsimli ve Logolu | Luna Yapım",
  aciklama=("Kişiye özel anahtarlık: fotoğraflı ve isimli hediye anahtarlık, çocuk çizimi ve "
            "evcil hayvan portresi; emlak, oto galeri ve otel için logolu anahtarlık."),
  anahtar=("kişiye özel anahtarlık, fotoğraflı anahtarlık, isimli anahtarlık, logolu anahtarlık, "
           "firmaya özel anahtarlık, promosyon anahtarlık, metal anahtarlık baskı, ahşap anahtarlık, "
           "anahtarlık baskı bursa"),
  h1="Kişiye özel anahtarlık — <i>cebinde</i> taşınan hatıra",
  lede=("Fotoğraf, isim, çocuk çizimi ya da logo; metal, ahşap ve akrilik gövde. Sevgiliye tek "
        "anahtarlık, emlak ofisine yüz anahtarlık: tasarım bizden, baskı ve kutu dâhil."),
  gorsel="kisiye-ozel-anahtarlik",
  gorsel_alt="Kemik beyazı yüzeyde fotoğraflı metal, çizimli akrilik, monogramlı ahşap ve kırmızı noktalı siyah anahtarlıklar; yanında ev anahtarları",
  giris=_p(
    "Anahtarlık küçük bir ürün ama günde birkaç kez ele alınıyor; bu yüzden hem hediye hem "
    "promosyon tarafında karşılığı büyük. Gövde malzemesi tasarımı belirliyor: metal yüzeye "
    "fotoğraf ve tek renk logo, ahşaba gravür görünümlü baskı, akrilik gövdeye tam renkli "
    "çizim daha iyi oturuyor.",
    "Tasarımı biz yapıyoruz; fotoğrafı anahtarlığın şekline göre kesiyor, yazıyı küçük alanda "
    "okunacak kalınlıkta kuruyoruz. Tek adetten başlıyoruz."),
  kurumsal=_p(
    "Kurumsal anahtarlığın en doğal yeri anahtar teslim edilen işler: emlak ofisi (kiracıya "
    "ve alıcıya verilen anahtar), oto galeri ve servis (araç teslimi), otel ve pansiyon "
    "(oda anahtarı), site yönetimi ve depo. Anahtarlık orada kalıyor, logo her gün "
    "görünüyor.",
    "Fuar ve etkinlik dağıtımında akrilik ya da plastik, müşteri hediyesinde metal ve "
    "ahşap öneriyoruz. Tekrar siparişte aynı gövde ve aynı dosya.") + _ul([
    "Emlak ofisi anahtar teslim anahtarlığı",
    "Oto galeri, servis ve araç kiralama",
    "Otel, pansiyon ve apart oda anahtarlığı",
    "Site yönetimi, depo ve iş yeri anahtar düzeni",
    "Fuar dağıtımı ve müşteri hediyesi seti"]),
  kisiye=_p(
    "Kişiye özel anahtarlıkta fotoğraf başı çekiyor: çiftin karesi, çocuğun ilk fotoğrafı, "
    "evcil hayvanın portresi. Onun yanında çocuk çizimi (çocuğun kendi çizdiği resim "
    "anahtarlığa basılıyor), ilk ev ve ilk araba için tarihli anahtarlık, uzaktaki aile "
    "için aynı fotoğraftan birkaç adet.",
    "Kutu ve not kartıyla teslim ediyoruz; kupa ve magnetle set olarak da gidiyor.") + _ul([
    "Çift ve aile fotoğraflı metal anahtarlık",
    "Çocuk çizimi ve el yazısı basılı akrilik anahtarlık",
    "İlk ev, ilk araba ve yeni iş için tarihli anahtarlık",
    "Evcil hayvan portresi",
    "Kupa ve magnetle hediye seti"]),
  teknik=_p(
    "<strong>Gövde:</strong> metal (yuvarlak, dikdörtgen, kalp), ahşap (gravür görünümlü "
    "baskı), akrilik (tam renkli, iki yüzlü); halka ve zincir dâhil.",
    "<strong>Baskı:</strong> metalde fotoğraf ve tek renk logo, ahşapta tek renk, akrilikte "
    "tam renkli çizim ve fotoğraf; iki yüze farklı tasarım mümkün.",
    "<strong>Bakım:</strong> suya dayanıklı; keskin cisimle çizilmeden normal kullanımda "
    "solmuyor."),
  surec=[("Gövde ve adet", "Metal mi ahşap mı akrilik mi, hangi şekil, kaç adet; tasarıma göre gövde öneriyoruz."),
         ("Tasarım", "Fotoğraf ya da logo gövdenin şekline göre kesiliyor; anahtarlık üstünde ekranda gösteriliyor."),
         ("Baskı", "Onaydan sonra basılıyor; fotoğraflı işte ilk parça ayrıca kontrol ediliyor."),
         ("Teslim", "Kutulu ya da toplu poşetli; setle birlikte istenirse aynı pakette.")],
  sss=[
    ("Fotoğraf küçük alanda seçilir mi?",
     "Yüz ve ana unsur merkeze alınıp kesildiğinde seçiliyor; kalabalık grup fotoğrafı bu "
     "boyutta çalışmıyor, onu söylüyoruz ve kesim önerisini gösteriyoruz."),
    ("Çocuğumun çizimini basabilir misiniz?",
     "Evet; çizimin fotoğrafını ya da taramasını gönderin, temizleyip akrilik ya da ahşap "
     "gövdeye basıyoruz. En çok anneanne-babaanne hediyesi olarak isteniyor."),
    ("İki yüze farklı tasarım olur mu?",
     "Akrilik ve metal gövdede olur: bir yüze fotoğraf, diğerine isim ve tarih."),
    ("Emlak ofisi için üstünde ofis telefonu olsun istiyoruz, olur mu?",
     "Olur; logo bir yüze, telefon diğer yüze. Anahtar kaybolduğunda geri dönmesini "
     "sağlayan en işlevli düzen bu."),
    ("Tek anahtarlık için kutu var mı?",
     "Var. Tek kutu, kurdele ve isteğe bağlı not kartı; kargoyla da gönderiyoruz."),
  ],
  ilgili=["magnetli-kapak-acacagi", "kisiye-ozel-kupa", "baskili-cakmak"],
  cta_bas="Anahtarın ucuna <i>bir hatıra</i> takalım.",
  cta_alt="Fotoğrafı ya da logoyu gönderin; gövdeyi ve tasarımı aynı gün gösterelim.",
),
# ─────────────────────────────────────────────────────────────── 10. MAGNETLİ AÇACAK
dict(
  dosya="magnetli-kapak-acacagi.html", ad="Magnetli Kapak Açacağı",
  baslik_seo="Magnetli Kapak Açacağı — Logolu ve Kişiye Özel Açacak | Luna Yapım",
  aciklama=("Magnetli kapak açacağı: bar, restoran ve içecek bayisi için logolu promosyon açacak; "
            "yeni ev ve düğün hatırası olarak kişiye özel magnet açacak."),
  anahtar=("magnetli kapak açacağı, magnet açacak, logolu açacak, promosyon açacak, kişiye özel "
           "açacak, buzdolabı magneti açacak, firmaya özel açacak, magnet baskı, fotoğraflı magnet"),
  h1="Magnetli kapak açacağı — <i>buzdolabında</i> kalıcı yer",
  lede=("Bar, restoran ve içecek bayisi için logolu promosyon açacak; yeni ev, düğün ve tatil "
        "hatırası olarak kişiye özel magnet açacak. Fotoğraflı magnetle set hâlinde."),
  gorsel="magnetli-kapak-acacagi",
  gorsel_alt="Beyaz buzdolabı kapısında LY monogramlı çelik magnet açacak, yanında aile fotoğraflı yuvarlak magnet ve sahil çizimli kare magnet",
  giris=_p(
    "Magnetli kapak açacağı, promosyon ürünleri arasında en uzun ömürlü olanı: buzdolabına "
    "yapışıyor ve yıllarca orada kalıyor. Çekmecede kaybolan kalem ya da cepten düşen "
    "çakmaktan farkı bu. Mutfakta her gün göz önünde olduğu için tasarımın sade ve okunur "
    "olması gerekiyor.",
    "Metal gövdeye tek renk ya da tam renkli baskı yapıyoruz; fotoğraflı yuvarlak ve kare "
    "magnetlerle set hâlinde de üretiyoruz."),
  kurumsal=_p(
    "Kurumsal tarafta en doğal müşteri içecekle ilgili işler: bar, pub, restoran, kafe, "
    "içecek toptancısı ve bayisi, şarap ve bira üreticisi, tekel bayii. Açacak müşterinin "
    "mutfağına giriyor, logo her akşam görünüyor. Otel ve tatil köyleri için oda hatırası, "
    "emlak ve mobilya firmaları için “yeni eve hoş geldin” hediyesi olarak da "
    "kullanılıyor.",
    "Logo ile birlikte Instagram adı ya da telefon sığıyor; adede göre üretim, tekrar "
    "siparişte aynı gövde ve dosya.") + _ul([
    "Bar, pub, restoran ve kafe masa ve kasa promosyonu",
    "İçecek toptancısı, bayi ve üretici dağıtım ürünü",
    "Otel ve tatil köyü oda hatırası",
    "Emlak ve mobilya firması “yeni ev” hediyesi",
    "Fuar ve festival dağıtımı"]),
  kisiye=_p(
    "Kişiye özel açacak hediye olarak iki yerde çalışıyor: yeni ev (isim, adres numarası, "
    "taşınma tarihi) ve hatıra (düğün tarihi, tatil karesi, aile fotoğrafı). Açacağın "
    "yanına aynı tasarım dilinde fotoğraflı magnet ekleyince buzdolabı kapısında küçük bir "
    "set oluşuyor.",
    "Düğün ve nişanda misafire verilen tarihli magnet açacak, bekarlığa veda için grup "
    "çizimli açacak da sık gelen işler; misafir sayısına göre üretiliyor.") + _ul([
    "Yeni ev ve ev arkadaşı hediyesi (isim + tarih)",
    "Düğün, nişan ve söz misafir hatırası",
    "Tatil ve seyahat karesi magnet + açacak seti",
    "Aile fotoğraflı magnet seti",
    "Hediye kutusunda tek açacak"]),
  teknik=_p(
    "<strong>Ürün:</strong> çelik gövdeli magnetli açacak (dikdörtgen ve oval), arkasında güçlü "
    "mıknatıs; fotoğraflı yuvarlak ve kare magnetler.",
    "<strong>Baskı:</strong> metal yüzeye tek renk ya da tam renkli; fotoğraf ve logo; "
    "magnetlerde tam renkli fotoğraf.",
    "<strong>Bakım:</strong> suya ve mutfak ortamına dayanıklı; keskin cisimle çizilmedikçe "
    "solmuyor."),
  surec=[("Model ve adet", "Dikdörtgen mi oval mi, yanında magnet var mı, kaç adet."),
         ("Tasarım", "Logo ya da fotoğraf açacağın ölçüsüne göre kuruluyor; ürün üstünde ekranda gösteriliyor."),
         ("Baskı", "Onaydan sonra basılıyor; ilk parça kontrol ediliyor."),
         ("Teslim", "Kutulu ya da toplu poşetli; magnet setiyle aynı pakette.")],
  sss=[
    ("Mıknatıs buzdolabında tutar mı?",
     "Tutar; arkasındaki mıknatıs gövdeyi ve açılan şişeyi taşıyacak güçte. Paslanmaz "
     "olmayan yüzeylerde (bazı yeni nesil kapılar) tutmuyor, bunu baştan söylüyoruz."),
    ("Fotoğraf açacağın üstüne basılır mı?",
     "Basılır; dikdörtgen gövdede yatay fotoğraf iyi duruyor. Fotoğrafı ayrı magnet olarak "
     "yanına eklemek çoğu zaman daha iyi sonuç veriyor, ikisini de gösteriyoruz."),
    ("Bar için toplu siparişte karışık tasarım olur mu?",
     "Olur; aynı logo farklı zemin renklerinde ya da birkaç farklı slogan aynı siparişte "
     "basılabiliyor."),
    ("Düğün için misafir sayısı kadar üretir misiniz?",
     "Evet; tarih ve isimlerle, istenirse her masaya farklı renkte. Teslim süresi adede "
     "göre söyleniyor."),
    ("Tek açacak ve magnet seti hediye kutusunda olur mu?",
     "Olur. Açacak ve iki-üç magnet tek kutuda, kurdele ve not kartıyla.")],
  ilgili=["kisiye-ozel-anahtarlik", "kisiye-ozel-kupa", "uv-dtf-baski", "baskili-cakmak"],
  cta_bas="Buzdolabında <i>kalıcı</i> bir yer alalım.",
  cta_alt="Logoyu ya da fotoğrafı gönderin; açacak ve magnet setini aynı gün gösterelim.",
),
]

AD_HARITA = {u["dosya"][:-5]: u["ad"] for u in URUNLER}


def _kabuk(u, govde):
    slug = u["dosya"][:-5]
    url = "%s/hizmetler/%s" % (KOK, slug)
    semalar = [
      _sema("BreadcrumbList", itemListElement=[
        {"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": KOK + "/"},
        {"@type": "ListItem", "position": 2, "name": "Prodüksiyon", "item": KOK + "/hizmetler/"},
        {"@type": "ListItem", "position": 3, "name": ANA_AD, "item": "%s/hizmetler/%s" % (KOK, ANA)},
        {"@type": "ListItem", "position": 4, "name": u["ad"], "item": url}]),
      _sema("Service", name=u["ad"], description=u["aciklama"], url=url, serviceType=u["ad"],
            areaServed={"@type": "Country", "name": "Türkiye"},
            provider={"@type": "Organization", "name": "Luna Yapım", "url": KOK}),
      _sema("FAQPage", mainEntity=[
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in u["sss"]]),
    ]
    s = "\n".join('<script type="application/ld+json">\n%s\n</script>' % j(x) for x in semalar)
    g = head(e(kisa_baslik(u["baslik_seo"])), e(meta_desc(u["aciklama"])), e(u["anahtar"]), url, s)
    g = g.replace("https://lunayapim.com/assets/og-image.png",
                  "https://lunayapim.com/assets/hediye/%s.jpg" % u["gorsel"])
    g = g.replace("</head>",
                  '<style>.hediye-kahraman{margin:0 0 28px}.hediye-kahraman img{width:100%;'
                  'height:auto;border-radius:4px;display:block}.ilgili-urun a{margin-right:14px}'
                  '</style>\n</head>', 1)
    g += """<div class="page-hero">
  <img class="karga-buyuk" src="../assets/karga.png" alt="">
  <div class="wrap">
    <div class="crumbs"><a href="../">Ana Sayfa</a> ·
      <a href="./">Prodüksiyon</a> · <a href="%s">%s</a> · %s</div>
    <h1>%s</h1>
    <p class="lede">%s</p>
  </div>
</div>

""" % (ANA, e(ANA_AD), e(u["ad"]), u["h1"], e(u["lede"]))
    son = FOOTER
    if u["dosya"][:-5] in STUDYOLU:
        son = son.replace("</body>",
          '<script src="../assets/hediye-katalog.js"></script>\n'
          '<script src="../assets/hediye-studyo.js" defer></script>\n</body>')
    g += govde + son
    return g


def sayfa(u):
    g = ['<section><div class="wrap prose">']
    g.append('<figure class="hediye-kahraman"><img src="../assets/hediye/%s.jpg" alt="%s" '
             'width="1344" height="752" decoding="async"></figure>' % (u["gorsel"], e(u["gorsel_alt"])))
    g.append(u["giris"])
    g.append("</div></section>")
    slug = u["dosya"][:-5]
    if slug in STUDYOLU:
        g.append(_vitrin(slug))
        g.append(_studyo(slug, u["ad"]))
    g.append('<section><div class="wrap prose">')
    g.append("<h2>Kurumsal kullanım</h2>")
    g.append(u["kurumsal"])
    g.append("<h2>Kişiye özel</h2>")
    g.append(u["kisiye"])
    g.append("<h2>Baskı ve malzeme</h2>")
    g.append(u["teknik"])
    g.append('<h2>Sipariş süreci</h2></div><div class="wrap">')
    g.append(_surec(u["surec"]))
    g.append('</div><div class="wrap prose">')
    g.append("<h2>İlgili ürünler</h2>")
    bag = " · ".join('<a href="%s">%s</a>' % (s, e(AD_HARITA[s])) for s in u["ilgili"])
    g.append('<p class="ilgili-urun">%s · <a href="%s">Tüm baskı ve hediye ürünleri</a></p>'
             % (bag, ANA))
    g.append("</div></section>")
    g.append('<section><div class="wrap prose"><h2>Sık sorulan sorular</h2>%s</div></section>'
             % sss_blok(u["sss"]))
    g.append(cta({"slug": u["dosya"][:-5]}, u["cta_bas"], u["cta_alt"]))
    return _kabuk(u, "\n".join(g))


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from pusula.ayarlar import SITE_KOK
    for u in URUNLER:
        hedef = os.path.join(SITE_KOK, "hizmetler", u["dosya"])
        html = sayfa(u)
        open(hedef, "w", encoding="utf-8").write(html)
        print("yazildi:", u["dosya"], len(html.encode()), "bayt")
