# -*- coding: utf-8 -*-
"""
SEKTÖREL DİJİTAL VE ANİMASYON SAYFALARI — 11.10.2026

Sahibinin kararı (11.10.2026): uzaktan teslim edilen işler şehir şehir değil,
SEKTÖR ekseninde anlatılır. Sanal showroom için şehir sayfası açılmaz; her
sektörün kendi satış sorusuna göre ayrı sayfa yazılır. Web sitesi + SEO altyapısı
kanıtlı verilerle anlatılır. Animasyon, talep gören sektörlerin hizmet alanına
dönüştürülür.

Kural (sektor_sayfalari.py ile aynı): her sayfa o sektörün gerçek sorusuyla
yazılır, ortak gövde yok; kanıt yalnız gerçekten yaptığımız işten gelir.

Üretilenler (hizmetler/ altında):
  sanal-showroom                       + sanal-showroom-<sektör> (6)
  animasyon-<alan> (3)                 — ürün animasyonu ailesine bağlanır
  web-sitesi-saglik-denetimi, seo-ornegi-aktas-prefabrik,
  web-sitesi-<sektör> (2)
Kullanım:  python3 sektor_dijital.py <site kökü>
"""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from uretici import e, sss_blok, cta
from yeni_hizmetler import _hizmet_kabugu, _surec

# ================================================================ SANAL SHOWROOM
SHOWROOM_ANA = dict(
 ad="Sanal Showroom",
 lede="Mağazanız kapanınca satış durmasın. Ürünleriniz sitenizde döndürülebilir, yakınlaştırılabilir hâlde durur; müşteri mağazaya gelmeden ne aldığını görür.",
 sorun="Ziyaretçi ürün sayfasına gelip iki fotoğrafa bakıyor ve çıkıyor. Dokuyu, ölçeği, rengin ışıkta nasıl durduğunu göremediği için ya mağazaya gelmeyi erteliyor ya da rakibin sitesine geçiyor. Telefonla gelen sorular da hep aynı: 'yakından nasıl duruyor', 'benim mekânıma olur mu', 'başka rengi var mı'.",
 cozum=[("Ürünü sitede döndür", "Ürün tek fotoğraf yerine 3D model ya da çok açılı çekimle sitede döndürülüyor; müşteri parmağıyla çeviriyor, yakınlaştırıyor."),
        ("Varyantı tek ekranda göster", "Renk, kumaş, kaplama seçenekleri aynı ürün üzerinde değişiyor. Her varyant için ayrı sayfa ve ayrı çekim gerekmiyor."),
        ("Talebi ölç", "Hangi ürünün kaç kez döndürüldüğü, hangi renge bakıldığı, kaç kişinin 'fiyat iste'ye bastığı ölçüme düşüyor. Mağazada göremediğiniz ilgiyi sayı olarak görüyorsunuz."),
        ("Siparişi kısalt", "Ziyaretçi seçtiği ürünü ve varyantı tek tuşla WhatsApp ya da forma taşıyor; satış temsilcisi soruyu baştan sormuyor.")],
 kanit="İlk uygulama bir kumaş satıcısı için kuruldu: 243 ürün görseli, doku yakın planları ve kumaş kartelası tek vitrinde; müşteri ürünü pazaryerine gitmeden inceleyebiliyor. Aynı yaklaşımla bir prefabrik ev üreticisi için müşterinin evini kendisinin tasarladığı 3B tasarlayıcıyı kurduk.",
 sss=[("Sanal showroom için ayrı bir site mi gerekiyor?", "Hayır. Var olan sitenize bir bölüm ya da sayfa olarak eklenir. Siteniz yoksa tanıtım sitesiyle birlikte kuruyoruz."),
      ("Ürünlerin 3D modeli bizde yok, olur mu?", "Olur. Ürün az sayıdaysa modelliyoruz; çoksa çok açılı fotoğraf çekimiyle döndürülebilir görüntü kuruyoruz. Hangisinin uygun olduğunu ürün listenize bakıp söylüyoruz."),
      ("Telefonda yavaş açılır mı?", "Açılmamalı, ölçüyoruz. Görseller ihtiyaç oldukça yükleniyor; sayfa önce açılıyor, model sonra geliyor. Teslimden önce mobil hız ölçümünü size gösteriyoruz.")],
)

SHOWROOM = {
"mobilya": dict(
 ad="Mobilya için Sanal Showroom",
 lede="Müşterinin sorusu hep aynı: 'bu koltuk benim salonuma olur mu?' Sanal showroom bu soruya mağazaya gelmeden cevap veriyor.",
 sorun="Mobilyada müşteri ölçek ve renk konusunda emin olmadan karar vermiyor. Katalog fotoğrafı stüdyo ışığında çekildiği için kumaşın gerçek tonu evde farklı çıkıyor; iade ve değişim talebinin büyük kısmı buradan doğuyor. Modüler takımlarda da hangi parçanın nereye geldiği fotoğraftan anlaşılmıyor.",
 cozum=[("Modülü kur, göster", "Köşe takımı ya da modüler kanepe parçaları ekranda birleştiriliyor; müşteri kendi dizilimini kurup ölçüsünü görüyor."),
        ("Kumaşı değiştir", "Kartelanızdaki kumaşlar aynı model üzerinde değişiyor. Yeni kumaş geldiğinde numune üretmeden vitrine ekleniyor."),
        ("Ölçeği ver", "Ürün bilinen bir ölçünün yanında (kapı, insan boyu, standart halı) gösteriliyor; 'büyük mü kalır' sorusu azalıyor."),
        ("Bayiye aynı vitrini ver", "Bayi ağınız aynı sanal showroom bağlantısını kendi müşterisine gönderiyor; her bayi için ayrı katalog basılmıyor.")],
 girdi="Ürün ölçü çizimleri ve kumaş/kaplama kartelası. Model sayısı fazlaysa önce en çok satan 10 ürünle başlamayı öneriyoruz.",
 dikkat="Kur kurmadan önce iki şeye bakıyoruz: müşterilerinizin vitrine hangi cihazdan geldiği ve en çok hangi ürün için telefon aldığınız. Mobilya alıcısının büyük kısmı telefondan bakıyor; model ağırlığı bu yüzden önemli. Vitrin, telefonda ilk açılışta hafif bir görselle başlıyor, müşteri ürüne dokunduğunda 3D model yükleniyor. Bayi fiyatıyla perakende fiyatı farklıysa iki ayrı bağlantı veriyoruz.",
 sss=[("Tüm katalogu bir anda mı eklemek gerekiyor?", "Hayır. En çok satan ve en çok soru gelen ürünlerle başlıyoruz; ölçümde ilgi gören grubu genişletiyoruz."),
      ("Fiyatlar vitrinde görünsün mü?", "Sizin kararınız. Fiyat göstermek istemiyorsanız ürün 'fiyat iste' ile biter ve seçilen varyant mesaja otomatik yazılır."),
      ("Gerçek kumaş dokusu nasıl yakalanıyor?", "Numune kumaşı yakın planda çekip modele giydiriyoruz. Kadife, keten, boucle gibi dokularda fark en çok burada görünüyor.")],
),
"ev-tekstili-kumas": dict(
 ad="Kumaş ve Ev Tekstili için Sanal Showroom",
 lede="Kumaş satışında müşterinin bakmak istediği şey dokudur. Sanal vitrin, dokuyu yakın planda ve gerçek ışıkta gösteriyor.",
 sorun="Kumaş ve ev tekstilinde pazaryeri fotoğrafı ürünü anlatmaya yetmiyor: ipliğin kalınlığı, örgünün sıklığı, kumaşın ışığı nasıl tuttuğu tek kareden okunmuyor. Müşteri numune istiyor, numune kargoyla günler sürüyor, karar erteleniyor.",
 cozum=[("Doku yakın planı", "Her kumaş için yakın plan doku görseli ve kısa hareket videosu; kumaşın dökümü ve parlaklığı görülüyor."),
        ("Renk kartelası", "Aynı desenin tüm renkleri yan yana; müşteri renkler arasında gezinip seçiyor."),
        ("Metraj ve kullanım", "Hangi kumaşın perde, döşeme ya da giyim için uygun olduğu ve gramajı ürünün yanında yazıyor."),
        ("Pazaryeriyle bağ", "Vitrindeki ürün pazaryeri mağazanıza bağlanıyor; ürün yükleme işini de Trendyol Satıcı API ile otomatikleştirebiliyoruz.")],
 girdi="Ürün listesi (ad, kod, gramaj, en) ve her kumaştan bir numune ya da yakın plan fotoğraf.",
 dikkat="Kumaşta ekran rengi en büyük risk. Bu yüzden her kumaşı aynı ışık altında, aynı beyaz dengesiyle çekiyoruz ve sayfada 'ekran ayarına göre ton farkı olabilir' notunu açıkça yazıyoruz. Toptan alıcı için en çok sorulan bilgi gramaj, en ve minimum metraj; bu üçü ürün görselinin hemen altında duruyor, ayrıca sormak gerekmiyor.",
 sss=[("Pazaryeri mağazamız var, buna gerek var mı?", "Pazaryeri ürün sayfası fiyat kıyasında kaybolur; sanal vitrin kendi müşterinizi, toptan alıcıyı ve tasarımcıyı doğrudan size getirir. İkisi birlikte çalışır."),
      ("Toptan alıcı için ayrı görünüm olur mu?", "Olur. Toptan fiyat ve minimum metraj yalnız bağlantıyı verdiğiniz kişide görünür."),
      ("Yüzlerce ürünümüz var, nasıl ilerliyoruz?", "Görselleri seri hâlde işleyen bir düzenle çalışıyoruz; ilk vitrinimizde 243 ürün görseli bu yolla hazırlandı.")],
),
"otomotiv-galerisi": dict(
 ad="Oto Galeri için Sanal Showroom",
 lede="İkinci el araç alıcısı galeriye gelmeden önce aracı onlarca kez inceliyor. Sanal showroom bu incelemenin sizin sitenizde olmasını sağlıyor.",
 sorun="İlan sitelerinde araç fotoğrafları aynı açılardan ve çoğu zaman aceleyle çekiliyor; alıcı hasar ve iç mekân sorusunu telefonla soruyor. İlan sitesinde aracınız rakip ilanların arasında duruyor, alıcı sizin galerinizi değil aracı hatırlıyor.",
 cozum=[("Aracın çevresinde dönmek", "Araç aynı ışıkta, sabit açılarla dış çevre ve iç mekân olarak çekiliyor; alıcı sitenizde aracı döndürüyor."),
        ("Hasar ve ekspertiz şeffaflığı", "Boyalı/değişen parçalar ve ekspertiz raporu aracın görselinin üzerinde işaretleniyor; ilk telefonda sorulan soru baştan cevaplanıyor."),
        ("Stok listesi", "Galerideki tüm araçlar marka, yıl, kilometreye göre süzülebilen tek listede; satılan araç listeden kalkıyor."),
        ("Randevu", "Alıcı aracı seçip test sürüşü ya da görme randevusu istiyor; talep hangi araçtan geldiğiyle birlikte size düşüyor.")],
 girdi="Araçların bulunduğu alana bir çekim günü, araç bilgileri ve ekspertiz raporları. Çekim galerinizde yapılır; ildeki çözüm ortağımızla ya da kendi ekibimizle.",
 sss=[("Her yeni araç için tekrar çekim mi gerekiyor?", "Evet ama standart bir düzenle: aynı açılar, aynı sıra. Galeri personelinin uygulayabileceği bir çekim kılavuzu da veriyoruz."),
      ("İlan siteleriyle birlikte kullanılabilir mi?", "Kullanılmalı. İlanın açıklamasına aracın sanal showroom bağlantısını koyuyorsunuz; alıcı sizin sitenize geliyor ve galerinizin diğer araçlarını da görüyor."),
      ("Fiyatı nasıl belirleniyor?", "Kurulum tek seferlik; araç başına çekim ve yükleme ise aylık araç sayısına göre. Stok büyüklüğünüzü söyleyin, net aralık verelim.")],
),
"konut-projesi": dict(
 ad="Konut Projesi için Sanal Örnek Daire",
 lede="Alıcı satış ofisine gelmeden daireyi gezsin, katını ve cephesini seçsin. Proje bitmeden satış başlasın.",
 sorun="İnşaatı süren projede örnek daire ya yok ya da tek bir tipi gösteriyor. Alıcı kat planını okuyamıyor, 2+1 ile 3+1 arasındaki farkı hayal edemiyor; satış ofisine gelen her müşteriye aynı anlatım baştan yapılıyor. Şehir dışındaki ve yurt dışındaki alıcı hiç gelemiyor.",
 cozum=[("Daire içinde gezinme", "Her daire tipi 3D modelleniyor; alıcı odalar arasında dolaşıyor, mobilyalı ve boş hâlini görüyor."),
        ("Daire seçici", "Blok, kat ve cephe seçilerek uygun daireler listeleniyor; satılmış daireler işaretleniyor."),
        ("Manzara ve güneş", "Kata göre manzara ve günün saatine göre güneş alma gösteriliyor; üst kat fiyat farkının sebebi görünür oluyor."),
        ("Talep kaydı", "Alıcının baktığı daire tipi ve kat, form ya da WhatsApp mesajına otomatik yazılıyor; satış ekibi kimin neye baktığını biliyor.")],
 girdi="Mimari proje (DWG), daire tipleri listesi ve kaplama/malzeme listesi. Satış durumunu güncellemek için basit bir tablo yeterli.",
 sss=[("3D render ile farkı ne?", "Render sabit kare verir; sanal örnek daire alıcının kendisinin gezdiği ve seçtiği bir ortamdır. Render setini de aynı modelden çıkarıyoruz, iş iki kez yapılmıyor."),
      ("Satış ofisinde ekranda kullanılabilir mi?", "Evet. Aynı sayfa satış ofisindeki ekranda ve alıcının telefonunda çalışıyor."),
      ("Benzer bir uygulamanız var mı?", "Bir prefabrik ev üreticisi için müşterinin oda ekleyip kaplama seçtiği ve fiyatı anında gördüğü 3B tasarlayıcıyı kurduk; konut projesindeki daire seçici aynı altyapının üzerine kuruluyor.")],
),
"seramik-banyo": dict(
 ad="Seramik ve Banyo için Sanal Showroom",
 lede="Karo tek başına güzel görünür; asıl soru, duvarda ve zeminde birlikte nasıl durduğudur. Sanal showroom bunu müşteriye kendi seçimiyle gösteriyor.",
 sorun="Seramik ve vitrifiyede müşteri kombinasyon seçiyor: zemin karosu, duvar karosu, derz rengi, lavabo, batarya. Mağazadaki örnek pano en fazla birkaç kombinasyonu gösterebiliyor; geri kalanını müşteri hayal ediyor ve çoğu zaman karar veremeden çıkıyor.",
 cozum=[("Odayı kaplat", "Banyo ve mutfak sahnesinde zemin ve duvar karosu ayrı ayrı seçiliyor; derz rengi ve döşeme yönü değişiyor."),
        ("Ürünleri birleştir", "Lavabo, klozet, batarya ve dolap aynı sahneye yerleştiriliyor; seri uyumu görülüyor."),
        ("Metrekare hesabı", "Müşteri oda ölçüsünü giriyor, gereken kutu sayısı fireyle birlikte hesaplanıyor."),
        ("Seçimi gönder", "Müşterinin kurduğu kombinasyon, ürün kodlarıyla birlikte mağazaya mesaj olarak düşüyor.")],
 girdi="Ürün kodları, ebatlar, yüzey görselleri (karo taraması) ve seri bilgisi.",
 dikkat="Seramikte ebat ve yüzey (mat, parlak, rölyef) aynı kombinasyonda bambaşka sonuç veriyor. Rölyefli yüzeyleri düz fotoğraf gibi göstermek yanıltıcı olur; bu yüzden ışığın yüzeyde nasıl kırıldığını gösteren yakın plan görsel her ürünün yanında duruyor. Kombinasyon sahnesi mutfak, banyo ve balkon olarak üç temel mekânla başlıyor; mağazanızın en çok sattığı mekân ilk açılan oluyor.",
 sss=[("Yüzlerce karomuz var, hepsi eklenebilir mi?", "Karo görselleri düz yüzey olduğu için seri hâlde eklenebiliyor. Vitrifiye ürünler model gerektirdiği için önce en çok satan serilerle başlıyoruz."),
      ("Hesaplanan kutu sayısı ne kadar doğru?", "Ebat ve kutu içi adedinizle hesaplanıyor, fire oranını siz belirliyorsunuz. Hesap bilgi amaçlı; kesin metraj ustanın keşfiyle verilir ve sayfada bu yazar."),
      ("Mimarlar kullanabilir mi?", "Kullanmalı. Mimar müşterisine kombinasyonu bağlantı olarak gönderiyor; seçim doğrudan sizin mağazanıza geliyor.")],
),
"aydinlatma": dict(
 ad="Aydınlatma için Sanal Showroom",
 lede="Aydınlatma ürünü kapalıyken bir şey anlatmaz. Sanal showroom ışığın yanınca mekânda ne yaptığını gösteriyor.",
 sorun="Avize ve armatür satışında müşteri ürünün yanınca nasıl göründüğünü, ışık rengini ve mekâna yayılışını görmek istiyor. Katalog fotoğrafı çoğunlukla ürünü kapalı ya da stüdyo ışığında gösteriyor; müşteri ölçeği ve ışık sıcaklığını tahmin etmek zorunda kalıyor.",
 cozum=[("Açık ve kapalı", "Ürün aynı sahnede kapalı ve yanarken gösteriliyor; ışık sıcaklığı (sıcak, nötr, soğuk beyaz) değiştirilebiliyor."),
        ("Mekâna göre ölçek", "Avize bir yemek masasının ya da salon tavanının üzerinde gösteriliyor; çap ve sarkıt boyu ölçekle görülüyor."),
        ("Seri ve renk", "Aynı serinin farklı gövde renkleri ve kol sayıları tek üründe değişiyor."),
        ("Proje listesi", "Mimar ya da müşteri birden fazla ürünü bir listeye ekleyip tek mesajla teklif istiyor.")],
 girdi="Ürün ölçü çizimleri, ışık teknik verileri (lümen, renk sıcaklığı) ve gövde/abajur malzeme bilgisi.",
 dikkat="Aydınlatmada en sık iade sebebi ölçek: katalogda büyük görünen avize tavanda küçük kalıyor ya da tersi. Bu yüzden her üründe çap ve sarkıt boyunu standart bir yemek masası ve tavan yüksekliğiyle birlikte gösteriyoruz. Teknik veriler (lümen, renk sıcaklığı, IP sınıfı) ürün görselinin altında; mimarın sorduğu bilgi tek bakışta bulunuyor.",
 sss=[("Işık efekti gerçeği yansıtıyor mu?", "Teknik verinize göre ayarlanıyor. Ekran parlaklığı cihazdan cihaza değiştiği için sayfada bunu da belirtiyoruz; amaç ölçeği ve ışığın karakterini göstermek."),
      ("Proje (otel, ofis) satışında işe yarar mı?", "En çok orada işe yarıyor: mimar seçtiği ürünleri listeleyip teklif istiyor, liste ürün kodlarıyla size geliyor."),
      ("Ürünleri fotoğrafla mı modelle mi gösteriyorsunuz?", "Işık efekti için model gerekiyor. Ürün sayısı fazlaysa önce en çok satan serilerle başlıyoruz.")],
),
}

# ================================================================ ANİMASYON ALANLARI
ANIM = {
"teknik-egitim-isg": dict(
 ad="Teknik Eğitim ve İş Güvenliği Animasyonu",
 lede="Yeni personele aynı prosedürü her seferinde baştan anlatmak hem zaman alıyor hem de her anlatımda bir adım eksik kalıyor. Animasyon, doğru anlatımı her izlemede aynı şekilde veriyor.",
 sorun="Fabrikada makine kullanımı, bakım ve iş güvenliği eğitimi genellikle usta-çırak ilişkisiyle aktarılıyor. Usta değişince anlatım değişiyor; sahada hata, duruş ve kaza riski buradan doğuyor. Makinenin içini ya da tehlikeli bir anı gerçek çekimle göstermek de çoğu zaman mümkün değil.",
 cozum=[("Prosedürü adım adım ver", "Çalıştırma, durdurma, bakım ve kilitleme-etiketleme adımları sırayla ve her adım ekranda numaralı olarak gösteriliyor."),
        ("Görünmeyeni göster", "Boru içindeki akış, basınç altındaki hat ya da dönen parça kesitle görünür oluyor; personel neden o kurala uyduğunu anlıyor."),
        ("Tehlikeyi riske girmeden göster", "Yanlış uygulamanın sonucu gerçek bir kazayı çekmeden canlandırılıyor."),
        ("Dil ve vardiya", "Aynı video farklı dillerde seslendirilip altyazılanıyor; her vardiya aynı eğitimi alıyor.")],
 kanit="Bir buhar geri kazanım sisteminin çalışma ilkesini ve hat akışını anlatan teknik eğitim animasyonu hazırladık (müşteri adı gizli tutuluyor).",
 girdi="Prosedür dokümanı, makine/hat fotoğrafları ve varsa katı model. İSG içerikleri iş güvenliği uzmanınızın onayından geçmeden yayına girmez.",
 sss=[("Resmî İSG eğitiminin yerine geçer mi?", "Hayır, destekler. Yasal eğitim yükümlülüğü yetkili eğitimciyle yerine getirilir; animasyon o eğitimin kalıcı ve tekrar izlenebilir parçası olur."),
      ("Video ne kadar uzun olmalı?", "Her prosedür için 60–120 saniye öneriyoruz. Uzun tek video yerine konu başına kısa videolar daha çok izleniyor."),
      ("Fabrikada çekim gerekir mi?", "Çoğu zaman gerekmez; fotoğraf ve ölçülerle modelliyoruz. Gerçek görüntüyle açılış isteniyorsa kısa bir çekim günü planlıyoruz.")],
),
"enerji-isi-sistemleri": dict(
 ad="Enerji ve Isı Sistemleri Animasyonu",
 lede="Isı geri kazanım, buhar ve kazan sistemlerinde müşteri tasarrufu görmek istiyor ama tasarruf borunun içinde oluyor. Animasyon o borunun içini açıyor.",
 sorun="Enerji verimliliği ekipmanı satan firma, ürünün getirdiği kazancı rakamla anlatıyor ama karar veren yönetici sistemin nasıl çalıştığını göremiyor. Tesis gezisi her zaman mümkün değil; teknik çizim de yatırım komitesinde okunmuyor.",
 cozum=[("Akışı renklendir", "Sıcak ve soğuk hatlar, buhar ve kondens farklı renklerle akıyor; enerjinin nereden alınıp nereye verildiği tek bakışta görülüyor."),
        ("Önce ve sonra", "Aynı tesis sistemsiz ve sistemli hâliyle yan yana; kaybın nerede oluştuğu gösteriliyor."),
        ("Kazancı sizin verinizle anlat", "Tasarruf ve geri dönüş süresi sizin hesabınızdan alınıyor, kaynağıyla videoda yazıyor; biz rakam üretmiyoruz."),
        ("Bakım ve devreye alma", "Kurulum ve bakım adımları ayrı kısa videolar olarak teslim ediliyor; servis ekibi sahada kullanıyor.")],
 kanit="Bir buhar geri kazanım sistemi için teknik eğitim animasyonu hazırladık: sistemin hatları, akış yönü ve çalışma ilkesi tek videoda.",
 girdi="P&ID ya da akış şeması, ekipman listesi ve varsa katı model. Tasarruf rakamları için kendi hesap ya da ölçüm raporunuz.",
 sss=[("Fuar için uygun sürüm verir misiniz?", "Veriyoruz: sessiz, döngüye giren, metinle anlatan 30–45 saniyelik bir sürüm. Fuarda ses duyulmuyor."),
      ("Teklif dosyasına eklenebilir mi?", "Evet; kısa sürüm teklif e-postasına bağlantı olarak, uzun sürüm toplantıda kullanılıyor."),
      ("Yabancı müşteriler için?", "Aynı görüntü üzerine farklı dillerde seslendirme ve altyazı veriyoruz; görüntü tekrar üretilmiyor.")],
),
"maskot-karakter": dict(
 ad="Maskot ve 3D Karakter Animasyonu",
 lede="Markanızın akılda kalan bir yüzü olsun. Maskotunuzu çizimden 3D modele, hareketten klibe kadar tasarlıyoruz.",
 sorun="Reklamda ürün tek başına çoğu zaman akılda kalmıyor; aynı sektördeki firmaların görselleri birbirine benziyor. Maskot bu benzerliği kırıyor ama tutarsız kullanılırsa — her reklamda farklı çizilirse — markayı güçlendirmek yerine dağıtıyor.",
 cozum=[("Karakteri tasarla", "Markanın sesi ve hedef kitlesine göre karakter taslakları çiziliyor; seçilen taslak 3D modele dönüşüyor."),
        ("Hareket dili kur", "Karakterin yürüyüşü, mimikleri ve tekrar eden hareketleri belirleniyor; her videoda aynı karakter gibi davranıyor."),
        ("Her mecraya uyarla", "Aynı karakter reklam filminde, sosyal medya kısa videosunda, ambalajda ve fuar standında kullanılıyor."),
        ("Karakter kılavuzu", "Renkler, duruşlar ve kullanım kuralları bir kılavuzla teslim ediliyor; başka ajansla çalışsanız da karakter bozulmuyor.")],
 kanit="Kendi müzik kliplerimiz için tasarladığımız YADE karakteri 3D modellenip bir klipte canlandırıldı.",
 girdi="Marka kimliği, hedef kitle ve karakterin hangi mecralarda kullanılacağı. Varsa daha önceki çizim denemeleri.",
 dikkat="Maskot projesinde en çok zaman kaybettiren şey onay döngüsü. Bu yüzden önce üç farklı yönde kaba taslak sunuyoruz, siz birini seçince detaylandırıyoruz; her aşamada neyin değişebileceği ve neyin kilitlendiği yazılı oluyor. Karakter 3D modele geçtikten sonra yüz ve oran değişikliği maliyetli; bu karar taslak aşamasında netleşiyor.",
 sss=[("Karakterin hakları kimde olur?", "Teslimle birlikte sizde. Sözleşmede karakterin kullanım haklarının size geçtiği açıkça yazılır."),
      ("Sadece 2D çizim de yapıyor musunuz?", "Evet; 2D karakter ve 2D animasyon da yapılıyor. 3D, aynı karakteri farklı açılardan ve sahnelerden kullanmayı kolaylaştırıyor."),
      ("Ne kadar sürede hazır olur?", "Karakter tasarımı ve 3D model iki-üç hafta, ilk animasyon bunun üzerine. Takvim taslak onay hızına göre değişir.")],
),
}

# ================================================================ WEB + SEO
WEB = {
"web-sitesi-saglik-denetimi": dict(
 ad="Web Sitesi Sağlık Denetimi ve İyileştirme",
 lede="Siteniz açılıyor ama müşteri getirmiyor mu? Hızını, Google'daki dizin durumunu, kırık bağlantılarını ve ölçümünü tek tek çıkarıp kanıtıyla düzeltiyoruz.",
 sorun="Çoğu sitede sorun görünmez yerdedir: mobilde açılmayan bir menü, Google'ın taramadığı sayfalar, eski sistemden kalan yüzlerce hatalı adres, iki kez sayılan ya da hiç sayılmayan reklam dönüşümleri. Site sahibi bunları görmediği için çözüm olarak yeni reklam bütçesi ya da yeni site düşünüyor.",
 cozum=[("Ölç", "Mobil ve masaüstü hız (PageSpeed), Search Console dizin raporu, kırık ve yönlendirilen adresler, yapılandırılmış veri, telefon/WhatsApp/form ölçümü tek raporda."),
        ("Önceliklendir", "Bulunan her sorun, getireceği etkiye göre sıralanıyor; 'şunu düzeltirsek ne değişir' sorusu her madde için cevaplanıyor."),
        ("Düzelt", "Bulunanları biz düzeltiyoruz ya da ekibinize uygulanabilir talimat veriyoruz; hangisi olacağı sizin kararınız."),
        ("Tekrar ölç", "Düzeltme sonrası aynı ölçüm tekrar yapılıyor; önce ve sonra yan yana teslim ediliyor.")],
 kanit="Bir prefabrik ev üreticisinin sitesini WordPress'ten taşıdık; taşıma sonrası mobil hız puanını 72'den 100'e çıkardık, eski sistemden kalan hatalı adresleri ve sayfadaki çift fiyat listesini bulup düzelttik. Ayrıntılar <a href=\"seo-ornegi-aktas-prefabrik\">örnek sayfasında</a>. Kendi sitemizde 27 olan dizinli sayfa sayısını 470'in üzerine çıkardık; <a href=\"seo-ornegi-lunayapim\">o örnek de açık</a>.",
 girdi="Search Console ve Analytics erişimi (salt okunur yeterli), varsa reklam hesabı okuma yetkisi. Erişim vermek istemiyorsanız dışarıdan görülebilen kısmı ölçüyoruz.",
 sss=[("Denetim için sitemizi değiştirmeniz gerekiyor mu?", "Hayır. Denetim yalnız okuma yapar; hiçbir şey değiştirilmez. Düzeltme ayrı bir adımdır ve sizin onayınızla başlar."),
      ("Hangi altyapıda çalışıyorsunuz?", "WordPress, hazır paneller ve kendi yazılmış siteler. Gerekiyorsa siteyi daha hızlı ve bakımı kolay statik yapıya taşıyoruz; eski adresler yönlendirmeyle korunur."),
      ("Sıralamada ilk sırayı garanti ediyor musunuz?", "Hayır, kimse edemez; sıralamayı Google belirler. Garanti ettiğimiz şey: sitenizin Google'ın kurallarına uygun, hızlı, doğru ölçülen ve kanıtı belgelenmiş hâle gelmesi.")],
 fiyat="Denetim 8.000 ₺; düzeltme işi bulunan maddelere göre ayrıca fiyatlanır.",
 fiyat_ar=(8000, 15000),
),
"web-sitesi-insaat-ve-yapi-firmalari": dict(
 ad="İnşaat ve Yapı Firmaları için Web Sitesi",
 lede="İnşaat firmasının sitesi bir kartvizit değil, satış ofisidir: proje, daire, fiyat ve teslim edilen işler birlikte durmalı ve her talep ölçülmeli.",
 sorun="İnşaat ve yapı firmalarının sitelerinde genellikle birkaç proje fotoğrafı ve iletişim formu var. Alıcı aradığını bulamıyor: hangi ilde proje var, fiyat aralığı ne, teslim edilmiş işler nerede, arsa sahibiyse ne yapacak. Google'da da 'şehir + konut projesi', 'prefabrik ev fiyatları', 'arsama ev yaptırmak' gibi aramalarda rakipler çıkıyor.",
 cozum=[("Proje ve tip sayfaları", "Her proje ve her daire/ev tipi kendi sayfasında: plan, metrekare, fiyat aralığı, görsel; Google bu sayfaları tek tek bulabiliyor."),
        ("Teslim edilen işler", "Tamamlanan projeler il ve tarih bilgisiyle yayında; alıcının en çok güvendiği kanıt bu."),
        ("Arayanın sorusuna sayfa", "'Tarlaya ev yapılır mı', 'kaç günde teslim' gibi gerçekten aranan sorulara mevzuat kaynaklı cevap sayfaları."),
        ("Ölçülen talep", "Telefon, WhatsApp ve form ayrı ayrı sayılıyor; hangi sayfanın ve hangi reklamın talep getirdiği görülüyor.")],
 kanit="Bir prefabrik ev üreticisinin sitesini taşıyıp yeniden kurduk: 57 model sayfası, kat planları, tamamlanan projeler ve arsa-izin rehberi; mobil hız 100, 'sakarya prefabrik ev' aramasında birinci sıra. <a href=\"seo-ornegi-aktas-prefabrik\">Örneği inceleyin</a>.",
 girdi="Proje listesi, planlar, fiyat aralıkları ve teslim edilen işlerin fotoğrafları. Mevcut siteniz varsa adresi.",
 sss=[("Fiyatları sitede göstermek zorunda mıyız?", "Hayır, ama başlangıç fiyatı veren sayfalar aramada daha çok tıklanıyor. Kesin fiyat yerine 'den başlayan' aralık yeterli."),
      ("3D render ve drone çekimini de siz mi yapıyorsunuz?", "Evet; sitedeki proje görselleri, 3D render ve drone görüntüleri aynı ekipten çıkıyor, ayrı ajans gerekmiyor."),
      ("Satış ekibimiz siteyi güncelleyebilir mi?", "Satılan daire, yeni fotoğraf ya da fiyat değişikliği için basit bir tablo ile güncelleme düzeni kuruyoruz.")],
 fiyat="Tanıtım sitesi 18.000 ₺'den başlıyor; proje ve sayfa sayısı arttıkça kapsam büyür.",
 fiyat_ar=(18000, 60000),
),
"web-sitesi-uretici-firmalar": dict(
 ad="Üretici ve Sanayi Firmaları için Web Sitesi",
 lede="Satın alma müdürü tedarikçiyi önce sitesinden tanıyor. Kapasite, sertifika, ürün ailesi ve teknik föy ilk bakışta bulunmalı.",
 sorun="Sanayi firmalarının sitesi çoğu zaman yıllar önce kurulmuş, mobilde açılmayan, ürün kataloğu tek PDF olan bir sayfadan ibaret. Yurt dışı alıcı İngilizce sayfayı bulamıyor, yerli alıcı hangi ürünü ürettiğinizi anlamak için aramak zorunda kalıyor.",
 cozum=[("Ürün ailesi sayfaları", "Her ürün grubu kendi sayfasında: kullanım alanı, teknik özellik, föy indirme; PDF katalog yerine aranabilir sayfalar."),
        ("Kapasite ve kalite", "Makine parkı, üretim kapasitesi, sertifikalar ve test süreçleri kanıtıyla; fabrika fotoğrafları ve kısa üretim videolarıyla."),
        ("İkinci dil", "İhracat yapılan pazarın dilinde ayrı sayfalar; çeviri değil, o pazarın aradığı terimlerle."),
        ("Teklif talebi", "Ürün koduyla teklif isteme formu; talep hangi üründen geldiğiyle satış ekibine düşüyor.")],
 kanit="Ürün animasyonu, teknik eğitim animasyonu ve 3D ürün görselini aynı ekipte üretiyoruz; sitedeki ürün sayfaları bu görsellerle birlikte kuruluyor.",
 girdi="Ürün listesi ve teknik föyler, sertifikalar, fabrika fotoğrafları. İhracat pazarlarınız.",
 dikkat="Sanayi sitesinde en çok ihmal edilen sayfa 'teklif iste' sonrası. Form gönderildiğinde müşteriye neyin ne zaman olacağını söyleyen bir teşekkür sayfası ve satış ekibinize ürün koduyla düşen bir bildirim kuruyoruz. Böylece hangi ürün grubunun talep getirdiği, ayda kaç teklif istendiği ve hangisinin siparişe döndüğü takip edilebiliyor.",
 sss=[("Katalogumuz PDF, onu koysak yetmez mi?", "PDF'in içindeki ürünleri Google tek tek göstermiyor; her ürün ailesinin kendi sayfası olunca 'ürün adı + üretici' aramalarında görünür olursunuz."),
      ("Yurt dışı pazarlar için ayrı site mi gerekir?", "Gerekmez; aynı sitede dil bölümleri yeterli ve doğru işaretlenirse her ülkede doğru dil gösterilir."),
      ("Yeni ürün eklemek zor mu?", "Ürün bilgilerini tablo olarak verdiğinizde sayfası aynı düzende üretiliyor; tasarım bozulmuyor.")],
 fiyat="Tanıtım sitesi 18.000 ₺'den başlıyor; ürün ailesi ve dil sayısı kapsamı belirler.",
 fiyat_ar=(18000, 60000),
),
}

AKTAS_ORNEK = dict(
 ad="SEO ve Site Sağlığı Örneği: Aktaş Prefabrik Ev",
 lede="Bir prefabrik ev üreticisinin WordPress sitesini hızlı, Google'ın okuduğu ve her talebi ölçen bir yapıya taşıdık. Bu sayfada ne bulduk, ne yaptık ve ne ölçtük yazıyor.",
)
AKTAS_GOVDE = """<section><div class="wrap prose">
<div class="kutu"><h2 style="margin-bottom:8px">Başlangıç</h2><p>Site WordPress üzerindeydi; eski sistemden kalan sayfalama, kategori ve etiket adresleri hata veriyordu, fiyat rehberinde eski ve yeni fiyat tabloları üst üste duruyordu. Siteyi hızlı ve bakımı kolay statik bir yapıya taşıdık. Taşımadan sonraki ilk ölçümde mobil performans puanı 72'ydi; üçüncü taraf etiketler sayfanın açılmasını yavaşlatıyordu.</p></div>
<h2>Ne yaptık</h2>
<ol>
<li><b>Hız.</b> Ölçüm etiketleri ilk etkileşime ertelendi, görseller sırayla yüklenir hâle geldi, stil dosyaları sayfa türüne göre bölündü. Mobil PageSpeed 72'den <b>100/100/100/100</b>'e çıktı.</li>
<li><b>Hatalı adresler.</b> Eski sistemden kalan sayfalama, kategori, etiket ve yazar adresleri ilgili sayfalara kalıcı yönlendirmeyle bağlandı; aramadaki geçmiş korundu.</li>
<li><b>Çift fiyat.</b> Fiyat rehberindeki eski tablolar temizlendi; tüm sayfalarda tek ve güncel fiyat listesi kaldı.</li>
<li><b>Yapılandırılmış veri.</b> Model sayfalarına ürün, il sayfalarına sık sorulan sorular ve ürün listesi şeması eklendi.</li>
<li><b>Yeni içerik.</b> 57 kat planlı plan merkezi, kullanım sayfaları (villa, bungalov, küçük ev, m² fiyatları), tamamlanan 14 proje ve arayanların sorduğu sorulara mevzuat kaynaklı arsa-izin rehberi.</li>
<li><b>Ölçüm.</b> Form, telefon ve WhatsApp ayrı ayrı sayılıyor; form talebinin hangi reklamdan geldiği kayda düşüyor.</li>
</ol>
<h2>Ölçülen sonuç</h2>
<table><thead><tr><th>Ölçü</th><th>Önce</th><th>Sonra</th></tr></thead><tbody>
<tr><td>Mobil PageSpeed (performans)</td><td>72</td><td>100</td></tr>
<tr><td>"sakarya prefabrik ev" Google sırası</td><td>—</td><td>1.</td></tr>
<tr><td>"tek katlı ev projeleri 1+1" Google sırası</td><td>—</td><td>2.</td></tr>
</tbody></table>
<p>Ölçümler Eylül 2026'da PageSpeed Insights ve Google aramasında (konum ve kişiselleştirme kapalı) yapıldı. Sıralama zamanla değişir; ilk sırayı kimse garanti edemez.</p>
<h2>Henüz başaramadıklarımız</h2>
<p>"prefabrik ev fiyatları" gibi genel ve rekabetli aramalarda ilk 10'da değiliz; bu aramalarda binlerce sayfalık rakipler var. Planımız her hafta arayanın sorusuna yeni sayfa eklemek ve sahadan gelen proje fotoğraflarını yayınlamak.</p>
<h2>Aynı ölçümü sizin sitenize yapalım</h2>
<p><a href="web-sitesi-saglik-denetimi">Site sağlık denetimi</a> bu örnekteki ölçümle başlar: önce ne olduğunu gösteririz, sonra neyin düzeleceğini.</p>
</div></section>"""


def _govde(v, kok_slug, kardes, kok_ad, kok_yol, cta_baslik, cta_alt, fiyat=None):
    g = ['<section><div class="wrap prose">']
    g.append('<div class="kutu"><h2 style="margin-bottom:8px">Sorun</h2><p>%s</p></div>' % e(v["sorun"]))
    g.append("<h2>Ne yapıyoruz</h2>")
    g.append(_surec(v["cozum"]))
    if v.get("kanit"):
        g.append("<h2>Yaptığımız iş</h2>")
        g.append("<p>%s</p>" % v["kanit"])   # bağlantı içerebilir, kaynağı bu dosya
    if v.get("dikkat"):
        g.append("<h2>Nelere dikkat ediyoruz</h2>")
        g.append("<p>%s</p>" % e(v["dikkat"]))
    if v.get("girdi"):
        g.append("<h2>Bizden ne isteniyor</h2>")
        g.append("<p>%s</p>" % e(v["girdi"]))
    g.append("<h2>Fiyat</h2>")
    g.append("<p>%s Aralıkların tamamı <a href=\"../fiyatlar\">fiyat sayfasında</a>; "
             "işi anlattığınız gün net bir aralık veriyoruz.</p>" % e(fiyat or "Fiyat ürün sayısına ve kapsamına göre değişiyor."))
    if kardes:
        g.append("<h2>Diğer alanlar</h2>")
        g.append("<p>Aynı hizmetin başka sektörlerdeki karşılığı: %s. Genel anlatım "
                 "<a href=\"%s\">%s sayfasında</a>.</p>" % (" · ".join(kardes), kok_yol, e(kok_ad)))
    g.append("</div></section>")
    g.append('<section><div class="wrap prose"><h2>Sık sorulan sorular</h2>%s</div></section>' % sss_blok(v["sss"]))
    g.append(cta({"slug": kok_slug}, cta_baslik, cta_alt))
    return "\n".join(g)


def _aciklama(lede, ek):
    a = lede if len(lede) <= 155 else lede[:lede.rfind(" ", 0, 150)] + "…"
    if len(a) < 110:
        a = (a + " " + ek).strip()
    return a[:158]


def uret():
    cikti = []
    # sanal showroom ana + sektör
    kardes_sr = ['<a href="sanal-showroom-%s">%s</a>' % (k, e(v["ad"].replace(" için Sanal Showroom", "").replace(" için Sanal Örnek Daire", "")))
                 for k, v in SHOWROOM.items()]
    v = SHOWROOM_ANA
    govde = _govde(dict(v, girdi="Ürün listeniz ve varsa mevcut ürün fotoğraflarınız. İlk görüşmede hangi ürünlerle başlayacağımızı birlikte seçiyoruz."),
                   "web-sitesi-tasarimi", [], "", "", "Ürününüz sitede <i>dönsün</i>.",
                   "Ne sattığınızı ve kaç ürününüz olduğunu yazın; aynı gün dönüş yapalım.")
    govde = govde.replace("<h2>Fiyat</h2>", "<h2>Sektörlere göre sanal showroom</h2><p>%s</p><h2>Fiyat</h2>" % " · ".join(kardes_sr), 1)
    cikti.append(("sanal-showroom.html", _hizmet_kabugu(
        "sanal-showroom.html", "Sanal Showroom — Ürünleriniz Sitede 3D | Luna Yapım",
        _aciklama(v["lede"], ""), "sanal showroom, sanal mağaza, 3d ürün vitrini, sanal vitrin",
        "Sanal <i>showroom</i>", v["lede"], govde, "Sanal Showroom", v["sss"])))
    for slug, v in SHOWROOM.items():
        dosya = "sanal-showroom-%s.html" % slug
        kardes = [k for k in kardes_sr if 'sanal-showroom-%s"' % slug not in k]
        govde = _govde(v, "web-sitesi-tasarimi", kardes, "Sanal Showroom", "sanal-showroom",
                       "Vitrininizi <i>sitede</i> açalım.",
                       "Ürünlerinizi ve kaç çeşit olduğunu yazın; hangi ürünlerle başlayacağımızı aynı gün söyleyelim.")
        baslik = "%s | Luna Yapım" % v["ad"]
        h1 = v["ad"].replace(" için Sanal Showroom", " için <i>sanal showroom</i>").replace(" için Sanal Örnek Daire", " için <i>sanal örnek daire</i>")
        cikti.append((dosya, _hizmet_kabugu(dosya, baslik, _aciklama(v["lede"], "Ürününüzü mağazaya gelmeden gösterin."),
                                            "%s, sanal showroom, 3d vitrin" % v["ad"].lower(), h1, v["lede"], govde, v["ad"], v["sss"])))
    # animasyon alanları
    kardes_an = ['<a href="animasyon-%s">%s</a>' % (k, e(v["ad"].replace(" Animasyonu", ""))) for k, v in ANIM.items()]
    for slug, v in ANIM.items():
        dosya = "animasyon-%s.html" % slug
        kardes = [k for k in kardes_an if 'animasyon-%s"' % slug not in k]
        fiyat = ("Karakter tasarımı ve 3D model ile ilk animasyon birlikte fiyatlanır; karakter sayısı ve süre belirleyici."
                 if slug == "maskot-karakter" else "Teknik animasyon 40.000 ₺'den başlıyor; süre ve hareketli parça sayısı belirleyici.")
        govde = _govde(v, "urun-animasyon", kardes, "Ürün Animasyonu", "urun-animasyon",
                       "Anlatması zor olanı <i>gösterelim</i>.", "Ne anlatmak istediğinizi ve elinizdeki dokümanı yazın; aynı gün dönüş yapalım.", fiyat)
        h1 = v["ad"].replace(" Animasyonu", " <i>animasyonu</i>")
        cikti.append((dosya, _hizmet_kabugu(dosya, "%s | Luna Yapım" % v["ad"], _aciklama(v["lede"], "Reklamda, sosyal medyada ve ambalajda aynı karakter."),
                                            "%s, teknik animasyon, 3d animasyon" % v["ad"].lower(), h1, v["lede"], govde, v["ad"], v["sss"],
                                            None if slug == "maskot-karakter" else (40000, 120000))))
    # web + seo
    kardes_web = ['<a href="%s">%s</a>' % (k, e(v["ad"].replace(" için Web Sitesi", ""))) for k, v in WEB.items() if k != "web-sitesi-saglik-denetimi"]
    for slug, v in WEB.items():
        dosya = slug + ".html"
        kardes = [k for k in kardes_web if '"%s"' % slug not in k] if slug != "web-sitesi-saglik-denetimi" else []
        govde = _govde(v, "web-sitesi-tasarimi", kardes, "Web Sitesi Tasarımı", "web-sitesi-tasarimi",
                       "Sitenizi <i>ölçelim</i>." if "saglik" in slug else "Sitenizi <i>satış ofisine</i> çevirelim.",
                       "Site adresinizi yazın; ilk ölçümü aynı gün paylaşalım.", v.get("fiyat"))
        h1 = (v["ad"].replace(" için Web Sitesi", " için <i>web sitesi</i>")
                     .replace("Sağlık Denetimi ve İyileştirme", "<i>sağlık denetimi</i> ve iyileştirme"))
        cikti.append((dosya, _hizmet_kabugu(dosya, "%s | Luna Yapım" % v["ad"], _aciklama(v["lede"], ""),
                                            "%s, web sitesi, seo, site hızı" % v["ad"].lower(), h1, v["lede"], govde, v["ad"], v["sss"],
                                            v.get("fiyat_ar"))))
    # Aktaş örneği
    cikti.append(("seo-ornegi-aktas-prefabrik.html", _hizmet_kabugu(
        "seo-ornegi-aktas-prefabrik.html", "SEO Örneği: Aktaş Prefabrik — Mobil Hız 72'den 100'e | Luna Yapım",
        "Prefabrik ev üreticisinin sitesini WordPress'ten taşıdık: mobil hız 72'den 100'e, eski adresler ve çift fiyat düzeltildi; ölçülen sonuçlar.",
        "seo örneği, site hızı, pagespeed 100, prefabrik ev sitesi", "SEO örneği: <i>Aktaş Prefabrik</i>",
        AKTAS_ORNEK["lede"], AKTAS_GOVDE, AKTAS_ORNEK["ad"])))
    return cikti


def yayinla(kok):
    n = 0
    for dosya, html_ in uret():
        y = os.path.join(kok, "hizmetler", dosya)
        io.open(y, "w", encoding="utf-8").write(html_)
        n += 1
    return n


if __name__ == "__main__":
    print(yayinla(os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")))
