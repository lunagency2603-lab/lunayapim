# -*- coding: utf-8 -*-
"""
Sektör ekseni — 17.09.2026.

Gerekçe: 28 günlük Search Console verisinde ürün animasyonu 46 şehir sayfasıyla
8 gösterim / 0 tıklama aldı; 28 sorgunun HİÇBİRİNDE "ürün animasyonu" geçmiyor.
Kimse "kütahya ürün animasyonu" aramıyor — bu talep şehir değil SEKTÖR ekseninde.
İnşaat 3D'de ise talep var (28 sorgunun 11'i 3D/render/mimari) ama sorgular
yapı türüyle geliyor: "konut projesi render", "villa 3d", "fabrika görselleştirme".

Bu modül iki eksen üretiyor:
  /hizmetler/urun-animasyon-<sektor>   — 8 sektör
  /hizmetler/insaat-3d-<tur>           — 6 yapı türü

Her sayfa o sektörün gerçek üretim sorununu anlatıyor; ortak gövde yok.
Şehir sayfalarına bağlantı veriyor (sektörün yoğun olduğu iller), böylece
kademe 2-3 il sayfalarının gelen iç bağlantısı da artıyor.
"""
import re
from kabuk import head, FOOTER
from uretici import KOK, e, j, sss_blok, cta
from yeni_hizmetler import _hizmet_kabugu, _surec, _paketler
import sehirler

# --------------------------------------------------------------- ÜRÜN ANİMASYONU
URUN = {
"makine-imalati": dict(
 ad="Makine İmalatı Ürün Animasyonu",
 anahtar_il=("makine","otomasyon","imalat"),
 lede="Gövdesi kapalı bir makinenin içinde ne olduğunu anlatmak, teknik satışın en uzun kısmı. Kesit animasyonu o konuşmayı kısaltıyor.",
 sorun="Makine satışında müşteri ürünü çalışırken göremiyor. Fuarda stant alanına sığmıyor, sahada çalışan örneğe götürmek haftalar alıyor, katalogdaki teknik çizimi de satın alma müdürü okumuyor. Sonuçta satış temsilcisi aynı anlatımı her görüşmede baştan yapıyor.",
 cozum=[("Gövdeyi şeffaflaştır","Dış kasa yarı saydam hâle geliyor, içerideki şaft, rulman ve tahrik hattı görünür oluyor. Müşteri mekanizmayı bir kez görüyor ve soru tipi değişiyor."),
        ("Çevrimi göster","Bir tam iş çevrimi gerçek hızında, sonra yavaşlatılmış olarak veriliyor. Saniyede kaç parça çıktığı iddiadan gözlenen veriye dönüyor."),
        ("Montaj sırasını aç","Parçalar patlatılmış görünümde ayrılıyor; bakım ekibinin hangi parçaya nereden ulaştığı görünüyor. Servis anlaşması görüşmesinde işe yarıyor."),
        ("Opsiyonları varyantla","Aynı gövde üzerinde farklı besleme ünitesi veya kontrol paneli seçenekleri tek modelden çıkıyor; her opsiyon için ayrı çekim gerekmiyor.")],
 girdi="Katı model (STEP, IGES, SolidWorks veya Inventor dosyası) en iyisi. Yoksa teknik resim ve ölçülü fotoğraflarla modelliyoruz, bu süreyi uzatıyor.",
 sss=[("Katı modelimizi vermek zorunda mıyız?","Hayır ama vermeniz süreyi belirgin kısaltıyor ve maliyeti düşürüyor. Model gizliyse gizlilik sözleşmesi imzalıyoruz; modeli teslimden sonra sistemlerimizden siliyoruz."),
      ("Fuar ekranı için farklı sürüm gerekiyor mu?","Evet ve bunu baştan planlıyoruz. Fuar ekranında ses duyulmuyor, izleyici 8-10 saniye bakıyor; sessiz, döngüye giren ve metinle anlatan ayrı bir kurgu veriyoruz."),
      ("Rakibimiz de benzer animasyon yaptırmış, farkı ne olacak?","Fark mekanizmanın kendisinde. Sizin makinenizin rakipten ayrıştığı noktayı bulup animasyonun merkezine onu koyuyoruz; genel tanıtım yerine tek bir teknik iddiayı kanıtlıyoruz.")],
),
"mobilya": dict(
 ad="Mobilya Ürün Animasyonu ve 3D Görsel",
 anahtar_il=("mobilya",),
 lede="Bir kanepenin on iki kumaş seçeneğini fotoğraflamak on iki ayrı çekim demek. Bir kez modellenirse hepsi aynı günde çıkıyor.",
 sorun="Mobilyada asıl maliyet varyantta. Her renk, her kumaş, her modül dizilimi için ayrı numune üretip ayrı stüdyo çekimi yapmak hem pahalı hem yavaş. Üstelik sezon değişince numune elde kalıyor.",
 cozum=[("Bir kez modelle","Ürün bir kez 3D modelleniyor; kumaş, ahşap ve metal yüzeyler ayrı katman olarak tanımlanıyor."),
        ("Varyantı çoğalt","Kumaş ve renk seçenekleri kataloğunuzdan alınıp modele uygulanıyor. Yeni bir kumaş geldiğinde tüm görseller yeniden üretiliyor, yeni çekim gerekmiyor."),
        ("Mekâna yerleştir","Ürün gerçek bir oda sahnesine konuyor. Ölçek algısı burada kuruluyor — müşterinin en çok sorduğu soru zaten 'benim salonuma olur mu'."),
        ("Modül animasyonu","Köşe takımı ve modüler sistemlerde parçaların nasıl birleştiği ve hangi dizilimlerin mümkün olduğu hareketle gösteriliyor.")],
 girdi="Teknik ölçü çizimi ve kumaş/kaplama kartelası. Üretimdeki bir numunenin detay fotoğrafları doku kalitesini belirgin artırıyor.",
 sss=[("Fotoğraf çekiminden ucuz mu?","Tek üründe hayır, varyantta evet. Üç varyanta kadar fotoğraf genelde daha uygun; altı ve üzerinde 3D belirgin öne geçiyor, çünkü ek varyantın maliyeti neredeyse sıfır."),
      ("Kumaş dokusu gerçekçi çıkıyor mu?","Kumaşı tarayıp gerçek dokuyu modele giydiriyoruz. Keten, kadife ve boucle gibi yüzeylerde yakın planda fark edilmiyor; gerekirse numuneyi bize gönderin, taramayı biz yapalım."),
      ("E-ticaret sitesi için hangi ölçüler lazım?","Pazaryerlerinin istediği ölçüler farklı. Ana görsel, kare sürüm ve doku detayını birlikte teslim ediyoruz; e-ticaret tarafını da yapıyorsak listeleme düzeniyle birlikte çıkıyor.")],
),
"ambalaj": dict(
 ad="Ambalaj Ürün Animasyonu",
 anahtar_il=("ambalaj",),
 lede="Ambalajda müşteri ürünü değil kapasiteyi satın alıyor. Kalıptan baskıya giden hattın görünmesi, teklif dosyasından daha ikna edici.",
 sorun="Ambalaj üreticisi marka müşterisine 'bu işi yapabiliriz' demek zorunda ama fabrikayı gezdirmek her müşteri için mümkün değil. Numune göndermek de tek bir ürünü gösteriyor, hattın tamamını değil.",
 cozum=[("Kalıp ve kesim","Karton veya plastiğin kesim planı, katlama çizgileri ve kalıp yapısı animasyonla açılıyor. Tasarımcı müşteri bunu doğrudan okuyabiliyor."),
        ("Baskı ve son işlem","Lak, yaldız, emboss ve pencere uygulamaları ürün üzerinde tek tek gösteriliyor; hangi efektin nasıl duracağı numune beklemeden görülüyor."),
        ("Katlama ve montaj","Düz karton ambalajın nasıl kutu hâline geldiği hareketle veriliyor. Perakende müşterisinin raf hazırlık süresini anlatan en somut materyal."),
        ("Raf simülasyonu","Ambalaj raf ortamına yerleştiriliyor; rakip ürünlerin yanında nasıl göründüğü marka görüşmesinin merkezine oturuyor.")],
 girdi="Kesim planı (dieline) ve baskı dosyası. İkisi varsa modelleme çok hızlı ilerliyor; yoksa numuneden ölçü alıyoruz.",
 sss=[("Müşterimizin markası görünsün mü?","Sadece izin verirse. İzin yoksa temsilî bir marka kuruyoruz — gerçek müşteri markasını izinsiz kullanmak hem hukuki risk hem de ilk görüşmede sorun oluyor."),
      ("Şeffaf ve metalize yüzeyler doğru çıkıyor mu?","Evet, bunlar 3D'nin fotoğrafa üstün olduğu alanlardan. Metalize yüzeyde stüdyoda kontrol edilemeyen yansımalar, modelde tam olarak ayarlanabiliyor."),
      ("Fuar öncesi ne kadar sürede teslim?","Dieline ve baskı dosyası hazırsa iki hafta içinde teslim ediyoruz. Fuar tarihinizi baştan söyleyin, takvimi ona göre kuralım.")],
),
"medikal": dict(
 ad="Medikal Cihaz ve Laboratuvar Animasyonu",
 anahtar_il=("medikal","laboratuvar"),
 lede="Medikal satışta yanlış anlatım geri dönüşü olmayan bir şey. Animasyon, doğru anlatımı her görüşmede aynı şekilde tekrarlıyor.",
 sorun="Cihazın kullanım adımları temsilciden temsilciye değişiyor; biri bir detayı atlıyor, diğeri fazladan bir şey söylüyor. Klinik ortamda çekim yapmak ise hasta mahremiyeti ve hijyen nedeniyle çoğu zaman mümkün değil.",
 cozum=[("Kullanım adımları","Cihazın hazırlık, uygulama ve temizlik adımları sırayla veriliyor. Her adım aynı, her izleyicide aynı."),
        ("İç yapı ve çalışma ilkesi","Sensör, pompa veya optik yolun nasıl çalıştığı kesitle gösteriliyor; teknik satın alma komitesinin sorduğu soru burada cevaplanıyor."),
        ("Hijyen ve sarf akışı","Sarf malzemenin takılması, kullanımı ve atılması net gösteriliyor — eğitim materyali olarak da kullanılabiliyor."),
        ("Klinik ortam kurgusu","Hasta ve personel çekmeden, modellenmiş bir ortamda uygulama anlatılıyor. Mahremiyet sorunu ortadan kalkıyor.")],
 girdi="Cihaz teknik dosyası ve kullanım kılavuzu. Tıbbi iddia içeren her cümleyi yayından önce sizin onayınıza gönderiyoruz.",
 sss=[("Tıbbi iddia sorumluluğu kimde?","Sizde, ve bunu ciddiye alıyoruz. Metindeki her teknik ve tıbbi ifadeyi yazılı onayınıza sunuyoruz; onaylamadığınız hiçbir cümle videoya girmiyor."),
      ("Yurt dışı için farklı sürüm gerekir mi?","Genelde evet. Ülkelere göre izin verilen iddialar değişiyor; metni bölgeye göre ayırıp aynı görüntü üzerinde farklı altyazı ve seslendirme veriyoruz."),
      ("Cihazı bize göndermemiz gerekiyor mu?","Hayır. Teknik dosyadan modelliyoruz. Yüzey ve malzeme detayı için birkaç yakın plan fotoğraf yeterli oluyor.")],
),
"tarim-makineleri": dict(
 ad="Tarım Makineleri Ürün Animasyonu",
 anahtar_il=("tarım makineleri",),
 lede="Bir pulluğun toprak altında ne yaptığı görülmüyor. Kesit animasyonu tam olarak orayı gösteriyor.",
 sorun="Tarım makinesinin asıl işi çoğunlukla gözden uzakta oluyor: toprağın altında, silonun içinde, hasat başlığının arkasında. Üstelik sahada çekim mevsime bağlı — hasat geçtiyse bir yıl beklemek gerekiyor.",
 cozum=[("Toprak kesiti","Makinenin toprakla temas eden kısmı yandan kesitle gösteriliyor; derinlik, devirme açısı ve iz genişliği görünür oluyor."),
        ("Mevsimden bağımsız üretim","Hasat animasyonu Ocak ayında da üretilebiliyor. Fuar takvimi tarım mevsimine uymadığında tek çözüm bu."),
        ("Ayar ve bakım","Ayar noktaları ve günlük bakım adımları gösteriliyor; bayi eğitiminde doğrudan kullanılıyor."),
        ("Traktör uyumu","Farklı traktör güçlerine bağlanma ve kuyruk mili bağlantısı modelleniyor; bayinin en çok sorduğu uyum sorusu cevaplanıyor.")],
 girdi="Teknik resim veya katı model, bir de sahada çekilmiş birkaç referans fotoğraf. Toprak tipi ve çalışma derinliği bilgisi kesit doğruluğu için gerekli.",
 sss=[("Gerçek tarla çekimiyle birleştirebilir miyiz?","Evet, en iyi sonuç bu oluyor. Gerçek tarla görüntüsüyle açıp toprak altına 3D kesitle giriyoruz; izleyici geçişi fark ediyor ve anlatım güven kazanıyor."),
      ("Bayi ağı için ayrı sürüm veriyor musunuz?","Veriyoruz. Bayinin kendi iletişim bilgisiyle biten sürümler tek kurgudan çoğaltılıyor, her bayi için ayrı ücret çıkmıyor."),
      ("Fiyat neye göre değişiyor?","Makinenin hareketli parça sayısına ve kesit isteyip istemediğinize göre. Sabit gövdeli bir römork ile hareketli başlıklı bir biçerdöver aynı iş değil.")],
),
"otomotiv-yan-sanayi": dict(
 ad="Otomotiv Yan Sanayi Ürün Animasyonu",
 anahtar_il=("otomotiv",),
 lede="Ana sanayi görüşmesinde parçanın montaj sırasını ve dayanımını göstermek, teknik sunumun yarısını kısaltıyor.",
 sorun="Yan sanayi firması parçasını tek başına gösterdiğinde anlam kurulmuyor; parça ancak aracın içindeki yerinde anlamlı. Ama araç modelini çekmek ya mümkün değil ya da gizlilik nedeniyle yasak.",
 cozum=[("Montaj konumu","Parça aracın ilgili bölümüne yerleştiriliyor; komşu parçalarla ilişkisi ve montaj sırası görünüyor."),
        ("Dayanım ve yük davranışı","Yük altında davranış temsilî olarak gösteriliyor. Simülasyon verisi sizdeyse onu görselleştiriyoruz; yoksa iddia üretmiyoruz."),
        ("Üretim hattı akışı","Kalıptan çıkış, işleme ve kalite kontrol adımları veriliyor; kapasite anlatımı burada somutlaşıyor."),
        ("Varyant ailesi","Aynı parçanın farklı araç modellerine giden versiyonları tek modelden çoğaltılıyor.")],
 girdi="Parça katı modeli ve montaj çizimi. Araç modeli gizliyse temsilî bir gövde kuruyoruz — marka belirtmeden.",
 sss=[("Ana sanayi markasını gösterebilir miyiz?","Yazılı izniniz yoksa hayır. İzinsiz marka kullanımı hem sözleşme ihlali hem de görüşmede aleyhinize dönebilecek bir şey. Temsilî gövdeyle aynı anlatımı kuruyoruz."),
      ("Simülasyon verimizi kullanabilir misiniz?","Evet. FEA veya CFD çıktınız varsa onu görselleştiriyoruz ve kaynağını videoda belirtiyoruz. Elimizde veri yokken dayanım iddiası üretmiyoruz."),
      ("İhale sunumu için uygun mu?","Uygun ve en çok bu amaçla isteniyor. Sunum süresi kısıtlıysa 45-60 saniyelik sıkı bir sürüm de veriyoruz.")],
),
"insaat-malzemesi": dict(
 ad="İnşaat Malzemesi Ürün Animasyonu",
 anahtar_il=("inşaat malzemesi","çimento","tuğla","yalıtım"),
 lede="Yalıtım malzemesinin katman kesiti anlatılmadan satılmıyor. Kesit animasyonu ustaya da mimara da aynı şeyi gösteriyor.",
 sorun="İnşaat malzemesinde satın alma kararını mimar, müteahhit ve usta birlikte veriyor ama üçü farklı şey soruyor: mimar performans, müteahhit maliyet, usta uygulama kolaylığı. Tek bir katalog üçüne birden cevap veremiyor.",
 cozum=[("Katman kesiti","Duvar veya döşeme kesiti açılıyor, malzemenin hangi katmanda durduğu ve komşu katmanlarla ilişkisi görünüyor."),
        ("Uygulama adımları","Ustanın sahada yapacağı işlem sırayla gösteriliyor; yanlış uygulama kaynaklı şikâyetler bu videoyla belirgin azalıyor."),
        ("Performans anlatımı","Isı, su veya ses davranışı görselleştiriliyor. Test raporunuz varsa ona dayanıyoruz; yoksa sayı vermiyoruz."),
        ("Detay çözümleri","Köşe, birleşim ve dilatasyon detayları ayrı ayrı çözülüyor; mimari ofisin teknik dosyasına giriyor.")],
 girdi="Ürün teknik föyü, test raporları ve uygulama detay çizimleri. Sahada çekilmiş uygulama fotoğrafları gerçekçiliği artırıyor.",
 sss=[("Usta eğitimi için kullanılabilir mi?","Evet, en çok işe yaradığı yerlerden biri bu. Uygulama adımlarını anlatan sürümü bayi ve şantiye eğitiminde kullanan müşterilerimiz var."),
      ("Test değerlerini videoya yazabilir miyiz?","Belgesi varsa evet, belge numarasıyla birlikte yazıyoruz. Belgesiz performans değeri yazmıyoruz — denetimde de sahada da geri dönüyor."),
      ("Mimari ofislere gönderilecek sürüm farklı mı?","Farklı olması daha iyi sonuç veriyor. Mimara detay ve performans, ustaya uygulama odaklı iki ayrı kısa sürüm çıkarıyoruz.")],
),
"gida": dict(
 ad="Gıda Üretimi Süreç Animasyonu",
 anahtar_il=("gıda","süt","konserve","un ","şeker"),
 lede="Zincir market ve ihracat görüşmesinde sorulan ilk şey izlenebilirlik. Hammaddeden pakete giden hattı tek videoda göstermek en kısa cevap.",
 sorun="Gıda tesisinde çekim yapmak hijyen kuralları nedeniyle zor: ekip steril alana giremiyor, üretim durduramıyor, bazı bölümler ticari sır. Ama alıcı tam da o bölümleri görmek istiyor.",
 cozum=[("Hammadde girişi","Ürünün tarladan veya çiftlikten tesise gelişi ve kabul kontrolü anlatılıyor; coğrafi işaretli ürünlerde kaynak vurgusu burada kuruluyor."),
        ("Proses hattı","Yıkama, ayıklama, işleme ve dolum adımları sırayla veriliyor. Gizli kalması gereken bölüm soyutlaştırılıyor — süreç görünüyor, teknoloji görünmüyor."),
        ("Hijyen ve kontrol","Kalite kontrol noktaları ve sertifika süreçleri görselleştiriliyor; ihracat dosyasının görsel karşılığı oluyor."),
        ("Paket ve sevkiyat","Dolum, paketleme ve soğuk zincir çıkışı gösteriliyor; raf ömrü anlatımı buraya bağlanıyor.")],
 girdi="Tesis yerleşim planı, proses akış şeması ve sertifika listesi. Gizli tutulmasını istediğiniz bölümü baştan söyleyin, o kısmı soyut anlatıyoruz.",
 sss=[("Üretimi durdurmamız gerekir mi?","Hayır. Animasyonun amacı zaten tesise girmeden anlatmak. İstenirse birkaç gerçek çekim karesiyle birleştiriyoruz, o da kısa sürüyor."),
      ("Rakibimize aynı şeyi yapar mısınız?","Aynı sektörde çalışabiliriz ama sizin tesisinizin verisi sizde kalıyor; proses şemanız ve gizli bölümleriniz başka hiçbir işte kullanılmıyor."),
      ("İhracat için hangi diller gerekiyor?","Hedef pazarınıza göre. Görüntü aynı kalıyor, altyazı ve seslendirme değişiyor; ek dil maliyeti tam üretimin çok altında.")],
),
}

# --------------------------------------------------------------- İNŞAAT 3D
YAPI = {
"konut-projesi": dict(
 ad="Konut Projesi 3D Görselleştirme",
 lede="Alıcı henüz temeli atılmamış daireyi satın alıyor. Gördüğü tek şey sizin verdiğiniz görsel.",
 sorun="Konut projesinde satış maketin ve broşürün üzerinden yürüyor ama alıcı en çok iki şeyi merak ediyor: dairenin içinden manzara nasıl görünüyor ve site içinde yürürken his ne. İkisini de plan gösteremiyor.",
 cozum=[("Vaziyet planından kütleye","Blok yerleşimi, kat yükseklikleri ve aradaki mesafeler gerçek ölçüyle modelleniyor; komşu parseldeki mevcut yapılar da sahneye giriyor."),
        ("Daire içinden manzara","Her blok ve kat için pencereden görünen gerçek manzara hesaplanıyor. 'Üst katlarda deniz görünür' iddiası kanıtlanabilir hâle geliyor."),
        ("Sosyal donatı turu","Havuz, yürüyüş yolu ve peyzaj günün farklı saatlerinde gösteriliyor; broşürdeki tek karenin anlatamadığı şey bu."),
        ("Kat planı animasyonu","Daire tipi planları üç boyutlu açılıyor; alıcı metrekareyi rakam olarak değil mekân olarak algılıyor.")],
 girdi="Mimari proje (DWG veya Revit), vaziyet planı ve cephe detayları. Malzeme kararları netleşmediyse iki alternatifle ilerliyoruz.",
 sss=[("Satış ofisi ekranı için ayrı sürüm gerekiyor mu?","Genelde evet. Satış ofisinde izleyici yanınızda oturuyor ve soru soruyor; orada uzun ve sessiz döngü, sosyal medyada ise 30 saniyelik dikey sürüm işe yarıyor."),
      ("Proje değişirse görseller boşa mı gider?","Hayır. Model duruyor; cephe rengi, peyzaj veya blok sayısı değiştiğinde yeniden render alıyoruz. Sıfırdan başlamak gerekmiyor."),
      ("Hak sahibi sunumunda kullanılıyor mu?","Kentsel dönüşümde en çok istenen kalem bu. Hak sahibine kendi dairesinin yerini ve manzarasını göstermek, imza sürecini kısaltan tek materyal.")],
),
"villa": dict(
 ad="Villa ve Müstakil Yapı 3D Render",
 lede="Villada alıcı sayı değil his satın alıyor. Işığın gün içinde nasıl dolaştığı, projeden daha çok konuşuluyor.",
 sorun="Villa alıcısı az sayıda ve seçici; onlarca daire değil tek bir yapı satılıyor. Bu yüzden görselin kalitesi doğrudan fiyatı etkiliyor — zayıf bir render, iyi bir projeyi ucuz gösteriyor.",
 cozum=[("Gün ışığı simülasyonu","Arsanın gerçek koordinatına göre güneş açısı hesaplanıyor; sabah, öğle ve akşam ışığında ayrı render alınıyor."),
        ("İç-dış süreklilik","Bahçeden salona, salondan terasa kesintisiz geçen bir kamera hareketi kuruluyor; villada satın alınan şey bu akış."),
        ("Malzeme gerçekçiliği","Ahşap, doğal taş ve cam yüzeyler gerçek malzeme örneğinden tanımlanıyor; yakın planda fark ediliyor."),
        ("Peyzaj ve çevre","Bahçe düzeni, havuz ve mevcut ağaçlar sahneye giriyor. Boş arsa görseli villayı olduğundan küçük gösteriyor.")],
 girdi="Mimari proje, arsa koordinatı ve malzeme kartelası. Arsada mevcut ağaç varsa fotoğrafı sahneye giriyor.",
 sss=[("Kaç render yeterli oluyor?","Satış için genelde 6-8 dış, 4-6 iç kare yeterli. Buna bir de kısa bir tur videosu ekleniyorsa ilan ve sosyal medya tarafı tamamlanıyor."),
      ("Gece render'ı gerekli mi?","Villada evet, belirgin fark yaratıyor. Aydınlatma tasarımı olan projelerde gece karesi genelde en çok paylaşılan görsel oluyor."),
      ("Mevcut villayı da modelliyor musunuz?","Modelliyoruz ama çoğu durumda gerekmiyor; mevcut yapıda drone ve iç mekân çekimi daha hızlı ve daha ucuz sonuç veriyor.")],
),
"ticari-avm": dict(
 ad="Ticari Yapı ve AVM 3D Görselleştirme",
 lede="Ticari yapıda görselin izleyicisi alıcı değil kiracı ve yatırımcı. İkisi de farklı şey soruyor.",
 sorun="Ticari projede yatırımcı getiri, kiracı ise görünürlük ve yaya akışı soruyor. Mimari görsel genelde sadece binayı gösteriyor, bu iki soruyu da cevaplamıyor.",
 cozum=[("Yaya akış simülasyonu","Girişlerden mağaza cephelerine yaya hareketi gösteriliyor; kiracı adayı kendi dükkânının önünden kaç kişinin geçeceğini görüyor."),
        ("Kiralanabilir alan anlatımı","Katlar ve birimler ayrı ayrı vurgulanıyor; birim ölçüleri ve cephe uzunlukları görsel üzerinde okunuyor."),
        ("Çevre bağlamı","Yapı gerçek çevresine yerleştiriliyor — komşu yapılar, yol ve ulaşım hatlarıyla. Yatırımcının konum sorusu burada cevaplanıyor."),
        ("Cephe ve tabela","Kiracı tabelalarının nereye ve hangi ölçüde geleceği gösteriliyor; kiralama görüşmesinin standart sorusu bu.")],
 girdi="Mimari proje, kat planları ve birim listesi. Ulaşım ve çevre verisi için imar planı paftası işimizi kolaylaştırıyor.",
 sss=[("Yatırımcı sunumu için ayrı materyal gerekiyor mu?","Evet. Yatırımcıya bağlam, ölçek ve konum; kiracıya birim, cephe ve yaya akışı anlatılıyor. Aynı modelden iki ayrı kurgu çıkarıyoruz."),
      ("Mağaza içleri de modellenecek mi?","Genelde gerekmiyor. Kiracı kendi iç tasarımını yapıyor; boş birim ve cephe yeterli oluyor. İstenirse temsilî bir iç kurgu ekliyoruz."),
      ("Proje aşamasında mı yapılmalı?","Ne kadar erken o kadar iyi. Ön kiralama sürecinde elde görsel olması, inşaat bitmeden birim doldurmanın en pratik yolu.")],
),
"otel": dict(
 ad="Otel ve Turizm Tesisi 3D Görselleştirme",
 lede="Otel görselinin işi rezervasyon almak. Rezervasyon ise odadan çok manzaradan ve ortak alandan geliyor.",
 sorun="Otel projesinde yatırım kararı ile rezervasyon ayrı zamanlarda veriliyor ama ikisi de aynı görsele bakıyor. Üstelik tesis açılmadan önce acentelerle anlaşma yapılması gerekiyor — elde fotoğraf yokken.",
 cozum=[("Oda tipleri","Her oda tipi ayrı modelleniyor ve pencereden gerçek manzara hesaplanıyor. Acente kataloğuna doğrudan girebilecek kare çıkıyor."),
        ("Ortak alanlar","Lobi, havuz, restoran ve spa günün farklı saatlerinde gösteriliyor; tesisin karakteri burada kuruluyor."),
        ("Mevcut ve yeni birleşimi","Ek bina veya yenileme projelerinde mevcut kısım gerçek çekimle, yeni kısım 3D ile veriliyor; ikisi tek videoda birleşiyor."),
        ("Sezon anlatımı","Yaz ve kış görselleri ayrı üretiliyor; yıl boyu çalışan tesislerde ikisi de gerekiyor.")],
 girdi="Mimari proje, oda tipi listesi ve konsept kararları. Tesis kısmen yapıldıysa drone çekimiyle birleştiriyoruz.",
 sss=[("Acente ve booking platformları için uygun mu?","Görsel olarak uygun ama platformların çoğu gerçek fotoğraf istiyor. 3D'yi açılış öncesi satış ve yatırımcı sürecinde kullanmak, açılışta gerçek çekime geçmek en doğru sıra."),
      ("Yenileme projelerinde ne yapıyorsunuz?","Mevcut hâli drone ve iç mekân çekimiyle alıyoruz, yenilenecek bölümü 3D ile üzerine kuruyoruz. Misafire 'burası böyle olacak' demenin en net yolu."),
      ("Çok dilli teslim veriyor musunuz?","Veriyoruz ve turizmde neredeyse zorunlu. Görüntü aynı, altyazı ve seslendirme hedef pazara göre değişiyor.")],
),
"fabrika-sanayi": dict(
 ad="Fabrika ve Sanayi Yapısı 3D Görselleştirme",
 lede="Sanayi yapısında görselin muhatabı yatırımcı, banka ve izin veren kurum. Üçü de estetik değil işleyiş soruyor.",
 sorun="Fabrika projesinde asıl soru bina değil akış: hammadde nereden giriyor, hangi hat üzerinden ilerliyor, ürün nereden çıkıyor. Mimari görsel binayı gösterip bu soruyu boş bırakıyor.",
 cozum=[("Üretim akışı","Hammadde girişinden sevkiyat çıkışına kadar akış üzerinde gösteriliyor; kapasite ve yerleşim mantığı görünür oluyor."),
        ("Makine yerleşimi","Hat üzerindeki makineler ve aralarındaki mesafeler modelleniyor; forklift ve personel dolaşım alanları kontrol edilebiliyor."),
        ("Etaplı büyüme","İkinci ve üçüncü etap yapılar aynı model üzerinde gösteriliyor; yatırımcıya büyüme planı somut anlatılıyor."),
        ("Çevre ve altyapı","Yol bağlantısı, otopark, arıtma ve enerji hattı sahneye giriyor; teşvik ve izin dosyalarında işe yarıyor.")],
 girdi="Mimari ve yerleşim projesi, makine listesi ve proses akış şeması. Etap planı varsa baştan söyleyin, modeli ona göre kuruyoruz.",
 sss=[("Teşvik ve kredi dosyasında kullanılıyor mu?","Sıkça kullanılıyor. Yatırım tutarını ve yerleşimi görsel olarak anlatmak, dosyayı inceleyen kişinin işini kolaylaştırıyor."),
      ("Makine markalarını göstermeli miyiz?","Gerek yok, hatta göstermemek daha esnek bırakıyor. Makineleri ölçü ve işlev doğruluğuyla temsilî modelliyoruz; tedarikçi değişirse görsel bozulmuyor."),
      ("Mevcut fabrikanın büyümesini gösterebilir misiniz?","Evet, en çok istenen kullanımlardan. Mevcut tesisi drone ile çekip yeni etabı üzerine 3D olarak kuruyoruz.")],
),
"kentsel-donusum": dict(
 ad="Kentsel Dönüşüm 3D Görselleştirme",
 lede="Kentsel dönüşümde ikna edilecek kişi alıcı değil, oturduğu evi bırakacak hak sahibi. Onun sorusu tek: benim dairem nerede olacak.",
 sorun="Dönüşüm sürecinde imza toplanamamasının en sık nedeni belirsizlik. Hak sahibi yeni dairesinin katını, cephesini ve manzarasını bilmiyor; plan üzerinden anlatılan hiçbir şey bu endişeyi gidermiyor.",
 cozum=[("Daire eşleştirme","Yeni projedeki her daire hak sahibiyle eşleştirilip tek tek gösteriliyor; kişi kendi dairesini görüyor, komşusununkini değil."),
        ("Öncesi-sonrası","Mevcut yapı drone ile çekiliyor, yeni proje aynı açıdan modellenip üstüne bindiriliyor. Değişim tek karede anlaşılıyor."),
        ("Manzara kanıtı","Yeni dairenin penceresinden görünen gerçek manzara hesaplanıyor; 'üst kat daha iyi' tartışması veriyle kapanıyor."),
        ("Süreç anlatımı","Yıkım, inşaat ve teslim takvimi görsel olarak anlatılıyor; belirsizlik azaldıkça imza süreci hızlanıyor.")],
 girdi="Mimari proje, mevcut kat mülkiyeti listesi ve yeni daire dağılım tablosu. Mevcut yapının drone çekimini biz yapıyoruz.",
 sss=[("Toplantıda gösterilecek formatta veriyor musunuz?","Veriyoruz. Hak sahibi toplantısı için projeksiyona uygun sürüm, ayrıca her hak sahibine WhatsApp'tan gönderilebilecek kısa dikey sürümler çıkarıyoruz."),
      ("Daire dağılımı değişirse ne oluyor?","Model duruyor, eşleştirme tablosunu güncelleyip yeniden üretiyoruz. Dönüşüm projelerinde dağılımın değişmesi normal, buna göre kuruyoruz."),
      ("Mevcut binanın çekimi dahil mi?","Dahil. Drone ile mevcut yapıyı ve sokağı çekiyoruz; öncesi-sonrası karşılaştırması bu çekim olmadan kurulamıyor.")],
),
}


# --------------------------------------------------------------- ÜRETİM
def _iller(anahtarlar, azami=10):
    """Sektörün yoğun olduğu iller — şehir sayfalarına iç bağlantı için."""
    bulunan = []
    for c in sehirler.SEHIRLER:
        metin = " ".join(c.get("sektorler", []) + [c.get("sanayi", "")]).lower()
        if any(a in metin for a in anahtarlar):
            bulunan.append(c)
    bulunan.sort(key=lambda c: (c["kademe"], c["ad"]))
    return bulunan[:azami]


def _il_bloku(iller, hizmet_slug):
    if not iller:
        return ""
    if hizmet_slug == "insaat-3d-modelleme":
        return _il_bloku_yapi(iller)
    bag = []
    for c in iller:
        if c["kademe"] in (1, 2):
            bag.append('<a href="../sehir/%s-%s">%s</a>' % (c["slug"], hizmet_slug, e(c["ad"])))
        else:
            bag.append('<a href="../sehir/%s">%s</a>' % (c["slug"], e(c["ad"])))
    return ('<h2>Bu sektörün yoğun olduğu iller</h2>\n<p>Aşağıdaki illerde bu alanda üreten '
            'firma sayısı yüksek; il sayfalarında o ildeki üretim profilini ayrıca yazdık. '
            'Listede olmayan bir ildeyseniz de çalışıyoruz — uzak illerde bölgedeki çözüm '
            'ortaklarımızla ilerliyoruz.</p>\n<p>%s</p>' % " · ".join(bag))


def _il_bloku_yapi(iller):
    bag = []
    for c in iller:
        if c["kademe"] in (1, 2):
            bag.append('<a href="../sehir/%s-insaat-3d-modelleme">%s</a>' % (c["slug"], e(c["ad"])))
        else:
            bag.append('<a href="../sehir/%s">%s</a>' % (c["slug"], e(c["ad"])))
    return ('<h2>Hangi illerde çalışıyoruz</h2>\n<p>Konut üretiminin yoğun olduğu illerde ayrı '
            'sayfa tuttuk; her il sayfasında o ildeki konut piyasasının kendine özgü yanını '
            'yazdık — Nilüfer\'de manzara üzerinden satılan proje ile deprem sonrası hak sahibi '
            'sunumu aynı anlatımı kaldırmıyor. Bu yüzden görselleştirmeyi de ile göre kuruyoruz.</p>'
            '\n<p>%s</p>\n<p>Listede olmayan bir ildeyseniz de çalışıyoruz; mimari proje dijital '
            'geldiği için modelleme mesafeden etkilenmiyor. Yalnızca mevcut yapının drone çekimi '
            'gerekiyorsa o gün için yerinde olmamız gerekiyor.</p>' % " · ".join(bag))


def _govde(v, hizmet_slug, il_anahtar, fiyat_metni, kardesler, kok_baslik, kok_yol):
    g = ['<section><div class="wrap prose">']
    g.append('<div class="kutu"><h2 style="margin-bottom:8px">Sorun</h2><p>%s</p></div>' % e(v["sorun"]))
    g.append("<h2>Ne yapıyoruz</h2>")
    g.append(_surec(v["cozum"]))
    g.append("<h2>Bizden ne isteniyor</h2>")
    g.append("<p>%s</p>" % e(v["girdi"]))
    g.append("<h2>Fiyat</h2>")
    g.append("<p>%s Aralıkların tamamı <a href=\"../fiyatlar\">fiyat sayfasında</a> açık yazılı; "
             "işi anlattığınız gün net bir aralık veriyoruz.</p>" % fiyat_metni)
    if il_anahtar:
        g.append(_il_bloku(_iller(il_anahtar), hizmet_slug))
    if kardesler:
        g.append("<h2>Diğer alanlar</h2>")
        g.append("<p>Aynı hizmetin başka alanlardaki karşılığı: %s. Genel anlatım "
                 "<a href=\"%s\">%s sayfasında</a>.</p>" % (" · ".join(kardesler), kok_yol, e(kok_baslik)))
    g.append("</div></section>")
    g.append('<section><div class="wrap prose"><h2>Sık sorulan sorular</h2>%s</div></section>'
             % sss_blok(v["sss"]))
    g.append(cta({"slug": hizmet_slug}, "Ürününüzü <i>anlatılır</i> hâle getirelim.",
                 "Ne ürettiğinizi ve elinizde hangi teknik dosya olduğunu yazın; aynı gün dönüş yapalım."))
    return "\n".join(g)


def uret_urun():
    cikti = []
    slugs = list(URUN)
    for slug, v in URUN.items():
        dosya = "urun-animasyon-%s.html" % slug
        # 22.09.2026 — burada [:5] vardi: sozlukteki son iki sektor (gida,
        # insaat-malzemesi) HICBIR kardesinden baglanti almiyordu, tek gelen
        # baglantilari hizmetler/index'ti. Google onlari "kesfedildi, taranmadi"
        # diye bekletti. Kardeslerin tamami listelenir; sekiz ad kisa bir satir.
        kardes = ['<a href="urun-animasyon-%s">%s</a>' % (k, e(URUN[k]["ad"].split(" Ürün")[0]))
                  for k in slugs if k != slug]
        govde = _govde(v, "urun-animasyon", v["anahtar_il"],
                       "3D ürün animasyonu 40.000 ₺'den başlıyor; süre ve hareketli parça sayısı belirleyici.",
                       kardes, "Ürün Animasyonu", "urun-animasyon")
        baslik = "%s | Luna Yapım" % v["ad"]
        aciklama = (v["lede"][:150] if len(v["lede"]) >= 110 else
                    (v["lede"] + " Fiyat 40.000 ₺'den başlıyor, teknik dosyanızdan modelliyoruz."))
        anahtar = "%s, 3d ürün animasyonu, ürün tanıtım videosu, fuar animasyonu" % v["ad"].lower()
        cikti.append((dosya, _hizmet_kabugu(dosya, baslik, aciklama, anahtar,
                                            v["ad"].replace(" Ürün Animasyonu", " için <i>ürün animasyonu</i>")
                                                   .replace(" Ürün Animasyonu ve 3D Görsel", " için <i>3D görsel</i>")
                                                   .replace(" Süreç Animasyonu", " için <i>süreç animasyonu</i>"),
                                            v["lede"], govde, v["ad"], v["sss"], (40000, 120000))))
    return cikti


def uret_yapi():
    cikti = []
    slugs = list(YAPI)
    for slug, v in YAPI.items():
        dosya = "insaat-3d-%s.html" % slug
        kardes = ['<a href="insaat-3d-%s">%s</a>' % (k, e(YAPI[k]["ad"].split(" 3D")[0]))
                  for k in slugs if k != slug]
        govde = _govde(v, "insaat-3d-modelleme", ("insaat", "inşaat", "konut", "yapı"),
                       "İnşaat 3D modelleme ve mimari render 45.000 ₺'den başlıyor; blok sayısı ve istenen kare adedi belirleyici.",
                       kardes, "İnşaat 3D Modelleme", "insaat-3d-modelleme")
        baslik = "%s | Luna Yapım" % v["ad"]
        aciklama = (v["lede"][:150] if len(v["lede"]) >= 110 else
                    (v["lede"] + " Fiyat 45.000 ₺'den başlıyor, mimari projenizden modelliyoruz."))
        anahtar = "%s, mimari render, 3d görselleştirme, proje tanıtım videosu" % v["ad"].lower()
        h1 = v["ad"].replace(" 3D Görselleştirme", " için <i>3D görselleştirme</i>").replace(" 3D Render", " için <i>3D render</i>")
        cikti.append((dosya, _hizmet_kabugu(dosya, baslik, aciklama, anahtar, h1,
                                            v["lede"], govde, v["ad"], v["sss"], (45000, 250000))))
    return cikti
