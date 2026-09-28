# -*- coding: utf-8 -*-
"""Kişiye ve firmaya özel baskı, hediye ve anı tasarımı — ANA HİZMET SAYFASI (20.09.2026).

Bu sayfa on ürün sayfasının dizini: UV DTF, DTF, tişört, sweatshirt-hoodie, yelek, kupa,
çakmak, kalem, anahtarlık, magnetli kapak açacağı (hediye_urunler.py). Ayrıca çiftlere özel
animasyon ve albüm hikâyesi, nişan/düğün animasyon filmi, çocukluk fotoğrafından hediyelik
ve Suno ile kişiye özel şarkı bu sayfada anlatılıyor.

Kurallar (kullanıcı kararı, 20.09.2026): fiyat ve fiyat bandı YAZILMAZ; "yapay zekâ" ibaresi
sayfada GEÇMEZ; her ürün kurumsal ve kişiye özel başlıklarıyla ayrı sayfada detaylı anlatılır.
Galeri kareleri müşteri işi değildir, örnek üretim kapsamı olarak sunulur.

Çalıştırma: python3 hediye_hizmet.py → hizmetler/kisiye-ozel-baski-hediye.html
"""
import os, sys
from yeni_hizmetler import _hizmet_kabugu, _surec, _paketler
from uretici import e, sss_blok, cta

DOSYA = "kisiye-ozel-baski-hediye.html"

# ── ürün dizini: (slug, görsel kökü, kategori etiketi, başlık, alt satır, alt metin)
URUN_KARTLARI = [
  ("uv-dtf-baski", "uv-dtf-cam-bardak", "UV DTF · Soğuk baskı",
   "UV DTF baskı", "Cam, metal, seramik ve ahşaba",
   "UV DTF soğuk baskı: taşıyıcı film soyulurken cam bardakta kalan çiçek deseni ve bitmiş ikinci bardak"),
  ("dtf-baski", "dtf-isi-presi", "DTF · Tekstil baskı",
   "DTF baskı", "Kumaşa ısıyla geçen tam renkli transfer",
   "DTF baskı: ısı presinde siyah tişörtten sıcak film soyulurken ortaya çıkan çok renkli desen"),
  ("baskili-tisort", "tisort-cift", "Tekstil",
   "Baskılı tişört", "Ekip tişörtü ve fotoğraflı hediye",
   "Aynı karga çizimi baskılı siyah ve beyaz tişört giyen iki kişi, kemik beyazı stüdyo duvarı önünde"),
  ("baskili-sweatshirt-hoodie", "tisort-sweatshirt-hoodie", "Tekstil",
   "Sweatshirt ve hoodie", "Kalın kumaşta sırt ve göğüs baskısı",
   "Karga çizimi baskılı siyah hoodie, beyaz tişört ve krem sweatshirt düz yatış çekimi"),
  ("baskili-yelek", "kurumsal-yelek-polo-sapka", "Kurumsal",
   "Baskılı yelek", "Saha, kurye ve etkinlik ekibi",
   "Lacivert yelek, polo tişört ve şapkada aynı monogram; yaka kartı ve kalemle kurumsal ekip seti"),
  ("kisiye-ozel-kupa", "cift-fotografli-kupa", "Kupa bardak",
   "Kişiye özel kupa", "Fotoğraflı, isimli, renkli kulp",
   "Elde tutulan beyaz kupa üzerinde çift fotoğrafı ve el yazısı isim-tarih; yanında kırmızı kulplu ikinci kupa"),
  ("baskili-cakmak", "baskili-cakmak", "Promosyon",
   "Baskılı çakmak", "Kafe, bar ve bayi promosyonu",
   "Bir sırada beş renkte monogramlı çakmak, biri yanık; kemik beyazı keten yüzeyde kraft kutu"),
  ("baskili-kalem", "baskili-kalem", "Promosyon",
   "Baskılı kalem", "Fuar, toplantı ve imza masası",
   "Kemik beyazı keten üstünde çapraz dizilmiş monogramlı siyah ve gümüş metal kalemler"),
  ("kisiye-ozel-anahtarlik", "kisiye-ozel-anahtarlik", "Hediyelik",
   "Kişiye özel anahtarlık", "Fotoğraflı, çizimli, logolu",
   "Fotoğraflı metal, çocuk çizimli akrilik, monogramlı ahşap ve siyah anahtarlıklar; yanında ev anahtarları"),
  ("magnetli-kapak-acacagi", "magnetli-kapak-acacagi", "Promosyon",
   "Magnetli kapak açacağı", "Buzdolabında kalıcı yer",
   "Beyaz buzdolabı kapısında monogramlı çelik magnet açacak, yanında aile fotoğraflı ve manzaralı magnetler"),
]

# ── anı ve hikâye işleri (ürün değil, iş): (görsel kökü, etiket, başlık, alt, alt metin)
ANI_KARTLARI = [
  ("cift-albumu-animasyon", "Çiftlere özel", "Anılar albüm hikâyesine",
   "Basılı albüm + animasyon sürümü",
   "Masada açık keten kapaklı fotoğraf albümü ve yanında aynı anıların animasyon sürümünü oynatan tablet"),
  ("nisan-animasyon-filmi", "Nişan · Düğün", "Animasyon film karesi",
   "Çiftin hikâyesi, çizilmiş",
   "Nişan için hazırlanmış el çizimi animasyon karesi: gün batımında teras üzerinde dans eden çift"),
  ("cocukluk-fotografi-hediyelik", "Çocukluk fotoğrafı", "Eski fotoğraftan çizime",
   "Kupa, magnet, anahtarlık",
   "Solmuş çocukluk fotoğrafı ve aynı çocuğun çizim sürümünün basıldığı kupa, magnet ve ahşap anahtarlık"),
  ("kisiye-ozel-sarki", "Kişiye özel şarkı", "Hikâyenizden şarkı",
   "Söz kartı + QR + dijital teslim",
   "Siyah hediye kutusunda şarkı sözü kartı, QR kod, kulaklık ve şarkıyı çalan telefon"),
]


def _urun_izgara():
    g = ['<div class="isler">']
    for slug, kok, kat, bas, alt, altmetin in URUN_KARTLARI:
        g.append(
          '<a class="is" href="%s"><div class="kapak"><img src="../assets/hediye/%s-k.jpg" '
          'srcset="../assets/hediye/%s-k.jpg 672w, ../assets/hediye/%s.jpg 1344w" '
          'sizes="(max-width:700px) 100vw, 33vw" alt="%s" width="672" height="376" '
          'loading="lazy" decoding="async"></div>'
          '<div class="is-alt"><span class="kat">%s</span><h3>%s</h3>'
          '<span class="musteri">%s</span></div></a>'
          % (slug, kok, kok, kok, e(altmetin), e(kat), e(bas), e(alt)))
    g.append('</div>')
    return "\n".join(g)


def _ani_izgara():
    g = ['<div class="isler">']
    for kok, kat, bas, alt, altmetin in ANI_KARTLARI:
        g.append(
          '<div class="is"><div class="kapak"><img src="../assets/hediye/%s-k.jpg" '
          'srcset="../assets/hediye/%s-k.jpg 672w, ../assets/hediye/%s.jpg 1344w" '
          'sizes="(max-width:700px) 100vw, 33vw" alt="%s" width="672" height="376" '
          'loading="lazy" decoding="async"></div>'
          '<div class="is-alt"><span class="kat">%s</span><h3>%s</h3>'
          '<span class="musteri">%s</span></div></div>'
          % (kok, kok, kok, e(altmetin), e(kat), e(bas), e(alt)))
    g.append('</div>')
    return "\n".join(g)


def kisiye_ozel_baski():
    ad = "Kişiye ve Firmaya Özel Baskı, Hediye ve Anı Tasarımı"
    aciklama = ("Kişiye ve firmaya özel baskılı tişört, hoodie, kupa ve promosyon ürünü; "
                "DTF ve UV DTF baskı, çiftlere özel animasyon-albüm ve kişiye özel şarkı.")
    anahtar = ("kişiye özel baskı, dtf baskı, uv dtf baskı, soğuk baskı, baskılı tişört, "
               "baskılı hoodie, kişiye özel kupa, promosyon ürünleri, firmaya özel hediye, "
               "çiftlere özel hediye, kişiye özel animasyon, düğün animasyon, nişan animasyon, "
               "çocukluk fotoğrafı hediye, kişiye özel şarkı, kişiye özel müzik, bursa baskı")
    sss = [
      ("DTF ile UV DTF arasındaki fark ne?",
       "DTF ısıyla kumaşa geçen bir transfer: tişört, sweatshirt, hoodie, yelek, bez çanta gibi "
       "tekstil ürünlerinde kullanılıyor; tam renkli basıyor ve yıkamaya dayanıklı. UV DTF ise "
       "ısı gerektirmeyen bir “soğuk baskı”: film cam, seramik, metal, plastik ve ahşap "
       "gibi sert yüzeylere yapıştırılıyor; cam bardak, termos, telefon kılıfı, kutu ve tabela "
       "için doğru yöntem bu. Hangisinin gerektiğini ürünü söylediğinizde biz seçiyoruz."),
      ("Tek bir parça sipariş verebilir miyim?",
       "Evet. Sevgiliye, arkadaşa ya da aileye tek kupa, tek tişört basıyoruz; toplu sipariş "
       "şartı yok. Adet arttıkça birim maliyet düşüyor, bunu teklifte açık yazıyoruz."),
      ("Elimde yalnız eski, düşük çözünürlüklü bir fotoğraf var; olur mu?",
       "Çoğu zaman olur. Fotoğrafı önce büyütüp temizliyoruz; baskıya yetmeyecek kadar kötüyse "
       "çizim yoluna geçiyoruz: fotoğraftaki kişi illüstrasyona çevrilip kupa, magnet ya da "
       "anahtarlığa o hâliyle basılıyor. Sonucu basmadan önce ekranda onaylıyorsunuz."),
      ("Çiftlere özel animasyon ve albüm hikâyesi tam olarak nedir?",
       "Fotoğraflarınızı ve kısa hikâyenizi alıyoruz; tanışma, ilk seyahat, teklif gibi anlar "
       "sıralı bir hikâyeye dönüşüyor. İki teslim var: basılı albüm (sayfa tasarımı ve baskı) "
       "ve aynı hikâyenin animasyon sürümü (telefonda, düğün ekranında ya da dijital çerçevede "
       "izlenen kısa film). İkisi birlikte de, ayrı ayrı da alınabiliyor."),
      ("Kişiye özel şarkı nasıl yapılıyor, gerçekten bize mi özel?",
       "Sizden hikâyeyi alıyoruz: isimler, tarih, ortak anılar, tarz (akustik, pop, düğün "
       "girişi, doğum günü). Sözleri bu bilgiyle yazıp Suno ile iki-üç sürüm üretiyoruz; "
       "seçtiğiniz sürüm mp3 olarak, söz kartı ve QR kodla teslim ediliyor. İsterseniz şarkı "
       "albüm animasyonuna ya da düğün filmine gömülüyor."),
      ("Firma logomuzu basabilir misiniz? Ya da sevdiğimiz bir çizgi karakteri?",
       "Kendi logonuzu evet, dosyasını gönderin yeter; yoksa monogram ya da logo tasarımını "
       "biz yapıyoruz. Telifli karakter, marka ve lisanslı görselleri lisans belgesi olmadan "
       "basmıyoruz; bunu baştan söylüyoruz ki sipariş yarıda kalmasın."),
      ("Teslim süresi ne kadar?",
       "Tek parça baskılı ürün genellikle 2-4 iş günü; toplu sipariş adede göre. Albüm ve "
       "animasyon işleri fotoğraf sayısına bağlı, ilk taslağı bir hafta içinde gösteriyoruz. "
       "Tarih verirken onay ve kargo süresini de sayıyoruz; “yarın hazır” demiyoruz."),
      ("Türkiye'nin her yerine gönderiyor musunuz?",
       "Gönderiyoruz. Bursa'da elden teslim ediyoruz, diğer illere kargoyla; kırılabilir "
       "ürünler (kupa, cam bardak) ayrıca korumaya alınıyor."),
    ]

    g = ['<section><div class="wrap prose">']
    g.append('<figure class="hediye-kahraman"><img src="../assets/hediye/kahraman.jpg" '
             'alt="Kişiye özel baskı ve hediye masası: baskılı hoodie ve tişört, UV DTF cam bardak, '
             'fotoğraflı kupa, açık albüm, anahtarlıklar ve kraft hediye kutusu" width="1344" '
             'height="752" decoding="async"></figure>')
    g.append("<p>Hazır hediye herkese aynı şeyi söylüyor. Kişiye özel olanı ise iki şeyden "
             "ibaret: doğru fikir ve temiz bir baskı. Biz ikisini de aynı masada yapıyoruz — "
             "tasarımı çiziyoruz, DTF ya da UV DTF ile basıyoruz, ürünü tedarik edip "
             "paketliyoruz. Tek kupa da olur, üç yüz kişilik ekip seti de.</p>")
    g.append("<p>Aşağıdaki her ürünün kendi sayfası var; o sayfalarda ürünün kurumsal kullanımı "
             "ve kişiye özel hâli, baskı yöntemi, malzeme bilgisi ve sipariş süreci ayrı ayrı "
             "yazılı.</p>")
    g.append("</div></section>")

    # ── ürün dizini
    g.append('<section class="acik hediye"><div class="wrap">')
    g.append('<div class="bas"><span class="no">◆</span><div><h2>Ürünler</h2>'
             '<p class="aciklama">Her ürünün kendi sayfasında kurumsal ve kişiye özel '
             'kullanımı ayrı ayrı anlatılıyor.</p></div></div>')
    g.append(_urun_izgara())
    g.append('</div></section>')

    # ── vitrin: hazır tasarımlar, ürün sayfasındaki stüdyoya götürür
    g.append('<section class="hs-bolum"><div class="wrap">')
    g.append('<div class="bas"><span class="no">\u25c6</span><div><h2>Tasarım stüdyosu</h2>'
             '<p class="aciklama">Hazır tasarımlardan birine dokunun; ürün sayfasındaki '
             'stüdyoda açılır. Rengi, yazıyı ve yerleşimi kendiniz ayarlar, beğendiğinizde '
             'sipariş verirsiniz \u2014 ya da kendi tasarım dosyanızı açarsınız.</p></div></div>')
    g.append('<div data-vitrin="baskili-tisort" data-vitrin-hedef="baskili-tisort" '
             'data-vitrin-adet="3"></div>')
    g.append('<div data-vitrin="kisiye-ozel-kupa" data-vitrin-hedef="kisiye-ozel-kupa" '
             'data-vitrin-adet="3" style="margin-top:18px"></div>')
    g.append('<p class="hs-kucuk" style="margin-top:22px">Stüdyo on ürünün her birinin '
             'kendi sayfasında: <a href="baskili-tisort">tişört</a>, '
             '<a href="baskili-sweatshirt-hoodie">hoodie</a>, '
             '<a href="baskili-yelek">yelek</a>, <a href="kisiye-ozel-kupa">kupa</a>, '
             '<a href="uv-dtf-baski">cam bardak</a>, <a href="baskili-cakmak">çakmak</a>, '
             '<a href="baskili-kalem">kalem</a>, '
             '<a href="kisiye-ozel-anahtarlik">anahtarlık</a>, '
             '<a href="magnetli-kapak-acacagi">magnetli açacak</a>.</p>')
    g.append('</div></section>')

    # ── kurumsal
    g.append('<section><div class="wrap prose">')
    g.append("<h2>Kurumsal: firmalara toplu baskı ve promosyon</h2>")
    g.append("<p>Kurumsal tarafta iş üç başlıkta toplanıyor. Birincisi <strong>ekip "
             "giyimi</strong>: personel tişörtü, polo, sweatshirt ve hoodie, saha ve kurye "
             "yeleği, fuar görevlisi kıyafeti. İkincisi <strong>promosyon ürünleri</strong>: "
             "kalem, çakmak, anahtarlık, magnetli kapak açacağı, kupa. Üçüncüsü "
             "<strong>müşteriye giden hediye</strong>: yeni yıl ve bayram setleri, bayi ve "
             "tedarikçi hediyesi, yeni personel için hoş geldin paketi.</p>")
    g.append("<p>Bunların hepsini aynı tasarım dilinde basmak işin asıl kıymeti: aynı monogram "
             "yeleğin göğsünde, kalemin gövdesinde ve kupanın yüzünde aynı ölçekte durduğunda "
             "ortaya dağınık bir promosyon yığını değil, tanınan bir set çıkıyor. Logo "
             "dosyanız yoksa monogramı biz tasarlıyoruz; varsa kurumsal renk kodlarını baskıya "
             "birebir taşıyoruz.</p>")
    g.append("<p>Tekrar siparişte aynı ürün ve aynı baskı dosyası kullanıldığı için partiler "
             "arasında ton farkı olmuyor — sezon içinde işe yeni giren bir kişi için tek parça "
             "ek baskı da yapıyoruz. Beden ve adet listesini alıyor, ürünü tedarik ediyor, "
             "basılı ve etiketli teslim ediyoruz.</p>")
    g.append('<figure class="hediye-kahraman"><img src="../assets/hediye/firma-toplu-siparis.jpg" '
             'alt="Kraft kutularda katlanmış monogramlı tişört yığınları, kupa ve kalem kutuları; '
             'sevkiyat notu" width="1344" height="752" loading="lazy" decoding="async"></figure>')
    g.append("<p>Hangi sektörde ne işe yaradığına dair kısa bir harita: kafe, bar ve restoran "
             "için <a href=\"baskili-cakmak\">çakmak</a> ve "
             "<a href=\"magnetli-kapak-acacagi\">magnetli açacak</a>; emlak, oto galeri ve otel "
             "için <a href=\"kisiye-ozel-anahtarlik\">anahtarlık</a>; muhasebe, sigorta ve "
             "klinik için <a href=\"baskili-kalem\">kalem</a>; saha ve lojistik ekipleri için "
             "<a href=\"baskili-yelek\">yelek</a>; ofis ve müşteri hediyesi için "
             "<a href=\"kisiye-ozel-kupa\">kupa</a>.</p>")
    g.append("</div></section>")

    # ── kişiye özel
    g.append('<section><div class="wrap prose">')
    g.append("<h2>Kişiye özel: hediye, anı ve hikâye işleri</h2>")
    g.append("<p>Kişiye özel tarafta kural şu: üründen önce fikir. Üzerindeki şey yalnız o "
             "kişiye bir şey anlatmalı — bir çocukluk fotoğrafı, ilk tanışma tarihi, aile "
             "içinde tekrarlanan bir söz, çocuğun kendi çizdiği resim, evcil hayvanın "
             "portresi. Tasarımı biz çiziyoruz, fotoğrafı baskıya hazırlıyoruz, ürünün "
             "üzerinde ekranda gösteriyoruz; onaysız hiçbir şey basılmıyor.</p>")
    g.append("<p><strong>Sevgiliye, eşe, aileye.</strong> Yıl dönümü, doğum günü, sevgililer "
             "günü, anneler ve babalar günü. En çok istenen ürünler "
             "<a href=\"kisiye-ozel-kupa\">çift kupa takımı</a>, "
             "<a href=\"baskili-tisort\">eşli tişört</a>, "
             "<a href=\"kisiye-ozel-anahtarlik\">fotoğraflı anahtarlık</a> ve "
             "<a href=\"uv-dtf-baski\">isimli cam bardak</a>.</p>")
    g.append("<p><strong>Çiftlere özel animasyon ve albüm hikâyesi.</strong> Tanışmadan bugüne "
             "fotoğraflar sıralı bir hikâyeye dönüşüyor; sayfa sayfa tasarlanıp albüm olarak "
             "basılıyor, aynı hikâye kısa bir animasyon film olarak da teslim ediliyor. Nişan "
             "ve düğün gecesinde ekranda oynatılan sürümü ayrı hazırlıyoruz.</p>")
    g.append("<p><strong>Nişan, düğün ve benzeri günler için animasyon film.</strong> Çiftin "
             "hikâyesi çizilmiş karakterlerle anlatılıyor: ilk buluşma, teklif, düğün günü. "
             "Gerçek çekimle karışık istenirse <a href=\"dugun-etkinlik\">düğün ve etkinlik "
             "çekimi</a> ile aynı ekipten çıkıyor.</p>")
    g.append("<p><strong>Çocukluk fotoğraflarıyla hediyelik.</strong> Eski, solmuş bir fotoğraf "
             "büyütülüp temizleniyor ya da çizime çevriliyor; kupa, magnet, anahtarlık, tablo "
             "ve tişörte basılıyor. Anne-babaya, kardeşe, kendi çocuğunuza.</p>")
    g.append("<p><strong>Toplu ama kişiye özel işler.</strong> Düğün ve nişan masası hatırası, "
             "kına gecesi dağıtımı, bekarlığa veda grubu, sınıf ve mezuniyet: aynı tasarımın "
             "isim isim değişen sürümleri tek siparişte basılıyor.</p>")
    g.append("</div></section>")

    # ── anı galerisi
    g.append('<section class="acik hediye"><div class="wrap">')
    g.append('<div class="bas"><span class="no">◆</span><div><h2>Anı ve hikâye işleri</h2>'
             '<p class="aciklama">Baskının ötesinde: albüm, animasyon, çizim ve şarkı.</p>'
             '</div></div>')
    g.append(_ani_izgara())
    g.append('<p class="ornek-not">Bu kareler hizmet kapsamını anlatmak için hazırlanmış örnek '
             'görsellerdir; müşteri işi değildir. Müşteri işlerini yalnız izin alınca '
             'paylaşıyoruz.</p>')
    g.append('</div></section>')

    # ── şarkı
    g.append('<section><div class="wrap prose">')
    g.append("<h2>Kişiye özel şarkı</h2>")
    g.append("<p>Hediyenin bir de sesi olsun isteyenler için: hikâyenizi, isimleri, tarihleri ve "
             "tarzı alıyoruz; sözleri buna göre yazıp Suno ile iki-üç sürüm üretiyoruz. "
             "Seçtiğiniz sürüm mp3 olarak, basılı söz kartı ve QR kodla teslim ediliyor; kutuya "
             "kulaklıkla birlikte konabiliyor. Şarkı, albüm animasyonuna ya da düğün filmine "
             "gömülebiliyor; düğün girişi ve ilk dans için ayrı kurgu yapıyoruz.</p>")
    g.append("<p>Bu şarkılar ticari yayın için değil, hediye için üretiliyor; radyo ve platform "
             "yayını için lisans ve hak durumunu baştan konuşuyoruz.</p>")

    g.append("<h2>Sipariş süreci</h2></div><div class=\"wrap\">")
    g.append(_surec([
        ("Fikir ve ürün", "Kime, hangi gün için, kaç adet — ürünü ve baskı yöntemini birlikte seçiyoruz."),
        ("Tasarım ve onay", "Fotoğraf ve metinleri alıyoruz; tasarımı ürünün üzerinde ekranda gösteriyoruz, onaysız basmıyoruz."),
        ("Baskı ve üretim", "DTF ya da UV DTF ile basılıyor; albüm, animasyon ve şarkı aynı sırada üretiliyor."),
        ("Paket ve teslim", "Kraft kutu ve kurdeleyle paketlenip elden ya da kargoyla teslim ediliyor; tasarım dosyaları sizde kalıyor."),
    ]))
    g.append('</div><div class="wrap prose">')

    g.append("<h2>Paketler</h2>")
    g.append(_paketler([
        ("Tek parça hediye", "Kişiye özel", ["Kupa, tişört, hoodie ya da promosyon ürünü",
                                            "Fotoğraf düzenleme ve tasarım",
                                            "Kraft kutu ve kurdele"]),
        ("Çift & anı paketi", "Çiftlere ve ailelere", ["Basılı albüm (sayfa tasarımı dâhil)",
                                                        "Aynı hikâyenin animasyon sürümü",
                                                        "İsteğe bağlı kişiye özel şarkı"]),
        ("Firma promosyon seti", "Adede göre", ["Ekip tekstili: tişört, yelek, şapka",
                                                "Kupa, kalem, çakmak, anahtarlık, açacak",
                                                "Monogram ya da logo düzenleme"]),
    ]))

    g.append("<h2>Neyi yapmıyoruz</h2>")
    g.append("<p>Telifli karakter, marka logosu ve lisanslı görselleri lisans belgesi olmadan "
             "basmıyoruz. Kişiye özel üründe kusur dışında iade almıyoruz; bu yüzden basmadan "
             "önce ekran onayı alıyoruz. Baskıya yetmeyecek fotoğrafı “olur” demeden "
             "önce söylüyoruz, çizim seçeneğini o zaman öneriyoruz.</p>")
    g.append("</div></section>")
    g.append('<section><div class="wrap prose"><h2>Sık sorulan sorular</h2>%s</div></section>'
             % sss_blok(sss))
    g.append(cta({"slug": "kisiye-ozel-baski-hediye"},
                 "Hediyeyi <i>kişiye</i> özel yapalım.",
                 "Kime, ne zaman, kaç adet — yazın; tasarımı aynı gün gösterelim."))
    govde = "\n".join(g)
    sayfa = _hizmet_kabugu(DOSYA, ad + " | Luna Yapım", aciklama, anahtar,
                           "Kişiye ve firmaya özel <i>baskı, hediye</i> ve anı tasarımı",
                           "DTF ve UV DTF baskılı tişört, hoodie, kupa ve promosyon ürünleri; "
                           "çiftlere özel animasyon ve albüm, çocukluk fotoğrafından hediyelik, "
                           "kişiye özel şarkı. Tek parçadan toplu siparişe.",
                           govde, ad, sss)
    stil = ('<style>.hediye .is .kapak img{filter:none}.hediye a.is{text-decoration:none;'
            'color:inherit;display:block}.hediye .is:not(a){cursor:default}'
            '.hediye-kahraman{margin:0 0 28px}.hediye-kahraman img{width:100%;height:auto;'
            'border-radius:4px;display:block}</style>\n</head>')
    sayfa = sayfa.replace("</head>", stil, 1)
    sayfa = sayfa.replace("https://lunayapim.com/assets/og-image.png",
                          "https://lunayapim.com/assets/hediye/kahraman.jpg")
    sayfa = sayfa.replace("</body>",
        '<script src="../assets/hediye-katalog.js"></script>\n'
        '<script src="../assets/hediye-studyo.js" defer></script>\n</body>')
    return DOSYA, sayfa


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from pusula.ayarlar import SITE_KOK
    dosya, sayfa = kisiye_ozel_baski()
    hedef = os.path.join(SITE_KOK, "hizmetler", dosya)
    open(hedef, "w", encoding="utf-8").write(sayfa)
    print("yazildi:", hedef, len(sayfa.encode()), "bayt")
