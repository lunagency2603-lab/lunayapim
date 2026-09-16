# -*- coding: utf-8 -*-
"""
Kademe 2-3 illeri — üçüncü ve son parti, 20 il (17.09.2026).
Bu dosyayla 81 ilin tamamında kultur/mekan/dugun_notu/isletme_notu dolu.

DOĞRULAMA: 80 alanın tamamı kaynak taramasıyla kontrol edildi.
Yakalanan hatalar: Muş Ovası'nı kaplayan tür ters lale değil endemik MUŞ LALESİ
(Tulipa sintenisii); Kazdağı Milli Parkı Balıkesir'de, Çanakkale'de yalnız
Bayramiç eteği var; Şırnak'ta madencilik taş kömürü değil Silopi ASFALTİTİ;
Kırıkkale'de rafineri ve savunma sanayi stratejik alan, çekime kapalı;
Karakeçili yayla değil ilçe.

Yeni satır eklerken aynı kural: doğrulanamayan iddia yazma, ölçülemez sonuç
vaat etme, il/ilçe eşleşmesini kaynaktan teyit et.
"""

EK7 = {
"kilis": {
 "kultur": "Zeytinlikler ve taş yapılar klipte sıcak, düşük kontrastlı bir palet veriyor. Şehir küçük olduğu için lokasyonlar arası mesafe kısa, tek günde çok kare çıkıyor.",
 "mekan": "Kilis zeytinlikleri, Ravanda Kalesi, Oylum Höyük, tarihi taş konaklar, Öncüpınar hattı",
 "dugun_notu": "Zeytin hasadı Kasım-Aralık'ta; bahçe çekimi bu pencerede, yaz sıcağında akşam saatleri tercih ediliyor.",
 "isletme_notu": "Zeytinyağı, bağcılık ve sabun üretimi il ekonomisinin üç kolu; sabunhane ve yağhane çekimi üretim sürecini doğrudan gösteriyor.",
},
"kirklareli": {
 "kultur": "İğneada longoz ormanları Türkiye'de çok az bulunan su basar orman tipi; klipte başka yerde kurulamayacak bir doku veriyor. Kıyıköy'ün kayalık sahili buna zıt bir hat sunuyor.",
 "mekan": "İğneada longoz ormanları, Dupnisa Mağarası, Kıyıköy sahili, bağ alanları, Vize antik tiyatrosu",
 "dugun_notu": "İstanbul'a yakınlık nedeniyle günübirlik ekip mümkün; longoz milli park, giriş ve çekim kuralları geçerli.",
 "isletme_notu": "Şişecam'ın Lüleburgaz düzcam tesisiyle cam ilin güçlü sanayi kolu; tekstil ve bağcılık ikinci hat, şaraplıklar hasat içeriği istiyor.",
},
"kirikkale": {
 "kultur": "Rafineri ve savunma sanayi tesisleri stratejik alan olduğu için çekime kapalı sayılır; endüstriyel doku uzak siluetten alınıyor. Kapulukaya Barajı açık alan sağlıyor.",
 "mekan": "Kapulukaya Barajı, Hasandede, Kızılırmak vadisi, sanayi tesis siluetleri, Karakeçili ilçe kırsalı",
 "dugun_notu": "Ankara'ya yakınlık ekip ve ekipman lojistiğini kolaylaştırıyor; karasal iklim dış çekimi yaz aylarına topluyor.",
 "isletme_notu": "Savunma sanayi, petrol rafinajı ve makine imalatı il ekonomisinin belirleyicileri; tesis içi çekimde güvenlik izni zorunlu.",
},
"mus": {
 "kultur": "Muş Ovası ilkbaharda endemik Muş lalesiyle kızıla dönüyor; bu pencere iki-üç hafta sürüyor ve klipte tek renkli geniş alanlar veriyor. Malazgirt Ovası tarihi ölçek veriyor.",
 "mekan": "Muş Ovası ve Muş lalesi alanları, Malazgirt Ovası, Bingöl Dağları eteği, Murat Nehri vadisi, Ulu Camii",
 "dugun_notu": "Muş lalesi dönemi Nisan-Mayıs'ta ve birkaç hafta sürüyor; bu pencerede dış çekim talebi yoğunlaşıyor.",
 "isletme_notu": "Hayvancılık, süt ürünleri ve şeker pancarı il ekonomisinin tabanı; tarımsal işleme tesisleri hasat döneminde çekime uygun.",
},
"nigde": {
 "kultur": "Aladağlar'ın sarp kaya hattı Türkiye'de dağcılık merkezlerinden; klipte dikey ölçek veriyor. Gümüşler Manastırı kaya içine oyulmuş kapalı bir mekân sunuyor.",
 "mekan": "Aladağlar, Gümüşler Manastırı, Narlıgöl krater gölü, elma bahçeleri, Niğde Kalesi",
 "dugun_notu": "Elma hasadı Eylül-Ekim'de; bahçe çekimi bu pencerede, rakım nedeniyle kış dış çekimi kısıtlı.",
 "isletme_notu": "Elma üretimi ve soğuk hava depoculuğu ilin ekonomik omurgası; mermer ve çimento sanayi ikinci hat.",
},
"ordu": {
 "kultur": "Boztepe'den şehre ve denize bakan hat, teleferikle ulaşılabildiği için ekipman taşıma sorunu olmadan çekilebiliyor. Perşembe ve Çambaşı yaylaları yaz aylarında açılıyor.",
 "mekan": "Boztepe ve teleferik hattı, Perşembe Yaylası, Çambaşı, Yason Burnu, fındık bahçeleri",
 "dugun_notu": "Yayla düğünü talebi yaz aylarında yoğunlaşıyor; yağış için her mevsim yedek gün planlanıyor.",
 "isletme_notu": "Fındık işleme ilin en büyük sanayi kalemi; balıkçılık ve gıda ikinci hat, hasat dönemi Ağustos'ta çekime açılıyor.",
},
"osmaniye": {
 "kultur": "Karatepe-Aslantaş'ın Geç Hitit kabartmaları açık hava müzesi olarak klipte taş doku veriyor. Zorkun Yaylası yaz aylarında şehirden hızlı ulaşılabilen bir yükselti sunuyor.",
 "mekan": "Karatepe-Aslantaş açık hava müzesi, Kastabala antik kenti, Zorkun Yaylası, Aslantaş Barajı, yer fıstığı tarlaları",
 "dugun_notu": "Yaz sıcağı yüksek; yayla çekimi serinlik avantajı veriyor, ova çekimi akşama kayıyor.",
 "isletme_notu": "Demir-çelik ve haddehane ilin sanayi tabanı; yer fıstığı işleme tarım tarafında, OSB çekimi güvenlik izniyle.",
},
"rize": {
 "kultur": "Çay bahçelerinin basamaklı yeşili ve Fırtına Deresi'nin taş köprüleri Türkiye'de tek bir bölgede toplanıyor. Ayder ve Pokut'un sis hattı klipte doğal bir filtre sağlıyor.",
 "mekan": "Çay bahçeleri ve teraslar, Ayder Yaylası, Zil Kale, Fırtına Deresi ve kemer köprüler, Pokut yaylası",
 "dugun_notu": "Yağış Türkiye ortalamasının çok üstünde; her dış çekim için yedek gün ve su koruması standart.",
 "isletme_notu": "Çay işleme ilin ekonomik omurgası; balıkçılık ve yayla turizmi ikinci hat, fabrika çekimi hasat döneminde en hareketli.",
},
"sivas": {
 "kultur": "Divriği Ulu Camii UNESCO Dünya Mirası listesinde ve taş işçiliğiyle klipte yakın plan detay veriyor. Sivas Kongre Binası ile demiryolu fabrikası şehrin diğer iki yüzünü oluşturuyor.",
 "mekan": "Divriği Ulu Camii ve Darüşşifası, Sivas Kongre Binası, Kangal balıklı kaplıca, demiryolu fabrikası, Gökpınar Gölü",
 "dugun_notu": "Karasal iklim; dış çekim Mayıs-Ekim arasında, Divriği'ye ulaşım süresi plana ayrıca ekleniyor.",
 "isletme_notu": "Demir-çelik ve demiryolu araçları il sanayisinin merkezinde; çimento ve halıcılık ikinci hat, halı atölyesi el işçiliği çekimine uygun.",
},
"tokat": {
 "kultur": "Ballıca Mağarası'nın salon ölçeği kapalı mekân çekimlerinde nadir bir imkân. Tokat yazmacılığı ve tarihi konaklar klipte el işçiliği dokusu veriyor.",
 "mekan": "Ballıca Mağarası, Tokat Kalesi, tarihi konaklar ve Latifoğlu Konağı, Zile Kalesi, yazmacı atölyeleri",
 "dugun_notu": "Konak ve mağara çekimlerinde izin işletmeye bağlı; iç mekân ışık planı önceden kurulmalı.",
 "isletme_notu": "Gıda ve konserve ile şeker sanayi il ekonomisinin tabanı; süt ve et işleme ikinci hat, yazmacılık küçük ölçekli ama görsel.",
},
"tunceli": {
 "kultur": "Munzur Vadisi Milli Parkı Türkiye'nin en büyük milli parkı; su, kaya ve orman aynı hat üzerinde toplanıyor. Klipte doğal ve sakin bir dil kuruyor.",
 "mekan": "Munzur Vadisi Milli Parkı, Munzur gözeleri, Pülümür vadisi, Ovacık yaylaları, Uzunçayır Baraj Gölü",
 "dugun_notu": "Vadi içi yollar dar ve kış kapanabiliyor; dış çekim Haziran-Eylül penceresinde planlanıyor.",
 "isletme_notu": "Munzur balı ilin coğrafi işaretli kalemi; hayvancılık ve su ürünleri ikinci hat, kovan çekimi mevsime bağlı.",
},
"usak": {
 "kultur": "Ulubey Kanyonu Türkiye'nin en uzun kanyonlarından biri; cam terastan bakan hat klipte dikey ölçek veriyor. Battaniye tezgâhları detay çekiminde şehre özgü doku sağlıyor.",
 "mekan": "Ulubey Kanyonu ve cam teras, Blaundos antik kenti, Clandras Köprüsü, battaniye ve tekstil atölyeleri, Banaz ovası",
 "dugun_notu": "Kanyon çekiminde güvenlik ve erişim planı gerekiyor; karasal iklim dış çekimi yaz aylarına topluyor.",
 "isletme_notu": "Tekstil ve battaniye üretimi ilin ekonomik omurgası; tekstil geri dönüşümü ve deri ikinci hat, tezgâh çekimi üretimi doğrudan gösteriyor.",
},
"van": {
 "kultur": "Van Gölü ve Akdamar Adası'ndaki kilise Türkiye'nin en çok tanınan siluetlerinden; tekne geçişi klipte hareketli bir açılış sağlıyor. Muradiye Şelalesi asma köprüsüyle ayrı bir kadraj veriyor.",
 "mekan": "Akdamar Adası ve kilisesi, Van Gölü kıyısı, Van Kalesi ve Eski Van, Muradiye Şelalesi, Çavuştepe",
 "dugun_notu": "Akdamar'a tekne ile geçiliyor; ekipman taşıma ve hava koşulu plana ayrıca giriyor.",
 "isletme_notu": "Otlu peynir ve süt ürünleri ilin tescilli kalemi; hayvancılık ve Kapıköy üzerinden sınır ticareti diğer iki kol.",
},
"yozgat": {
 "kultur": "Çamlık Milli Parkı Türkiye'nin ilk milli parkı; çam dokusu klipte sade bir zemin veriyor. Sarıkaya Roma Hamamı hâlâ su veren antik bir yapı olarak öne çıkıyor.",
 "mekan": "Çamlık Milli Parkı, Sarıkaya Roma Hamamı, Kerkenes antik kenti, Bozok yaylası, Yozgat Saat Kulesi",
 "dugun_notu": "Karasal iklim ve yüksek rakım; dış çekim Mayıs-Ekim arasında, kış aylarında kapalı mekâna kayıyor.",
 "isletme_notu": "Tarımsal işleme, un ve yem sanayi il ekonomisinin tabanı; mermer ikinci hat, tesis çekimi hasat döneminde hareketli.",
},
"zonguldak": {
 "kultur": "Maden ocakları ve lavvar tesislerinin endüstriyel dokusu Türkiye'nin tek taşkömürü havzasına ait; klipte ağır ve koyu bir dil kuruyor. Gökgöl Mağarası buna zıt bir iç mekân veriyor.",
 "mekan": "Maden ocağı ve lavvar siluetleri, Gökgöl Mağarası, Kapuz ve Kozlu sahili, Harmankaya Şelalesi, Filyos antik kenti",
 "dugun_notu": "Batı Karadeniz yağış rejimi yıla yayılı; sahil çekimlerinde yedek gün standart.",
 "isletme_notu": "Taş kömürü madenciliği ve demir-çelik il ekonomisinin belirleyicileri; ocak ve tesis çekiminde güvenlik izni zorunlu.",
},
"canakkale": {
 "kultur": "Truva, Assos ve Gelibolu Yarımadası aynı ilde üç ayrı tarihi katman veriyor. Bozcaada'nın bağ ve rüzgâr hattı ile Kazdağı eteği klipte farklı iki doku sunuyor.",
 "mekan": "Truva antik kenti, Assos ve Athena Tapınağı, Gelibolu Yarımadası, Bozcaada bağları, Kazdağı'nın Bayramiç etekleri",
 "dugun_notu": "Bozcaada'ya feribotla geçiliyor; sefer saatleri ve rüzgâr koşulu çekim planına doğrudan giriyor.",
 "isletme_notu": "Seramik ve kaolen ilin sanayi tabanı; gıda-konserve ve balıkçılık ikinci hat, bağ işletmeleri hasat içeriği istiyor.",
},
"cankiri": {
 "kultur": "Çankırı kaya tuzu mağarası tuz duvarlarıyla klipte ender bulunan bir iç mekân veriyor. Ilgaz hattı ise orman ve kar dokusunu tamamlıyor.",
 "mekan": "Çankırı Tuz Mağarası, Ilgaz Dağı, Taşmescit, Çerkeş yaylaları, Kızılırmak vadisi",
 "dugun_notu": "Ankara'ya yakınlık ekip çıkarmayı kolaylaştırıyor; tuz mağarasında çekim izni işletmeden alınıyor.",
 "isletme_notu": "Kaya tuzu ve madencilik ilin öne çıkan kalemi; çimento ve gıda ikinci hat, mağara içi çekim aydınlatma planı gerektiriyor.",
},
"corum": {
 "kultur": "Hattuşa UNESCO Dünya Mirası listesinde ve Hitit başkenti olarak klipte tarihi ölçek veriyor. Alacahöyük ile birlikte tek günde iki antik yerleşim çekilebiliyor.",
 "mekan": "Hattuşa ve Yazılıkaya, Alacahöyük, İncesu Kanyonu, Çorum Kalesi, leblebi atölyeleri",
 "dugun_notu": "Ören yeri statüsündeki alanlarda çekim izni önceden alınıyor; karasal iklim dış çekimi yaza topluyor.",
 "isletme_notu": "Makine imalatı ve döküm ilin sanayi tabanı; tuğla-kiremit ve leblebi-un gıda tarafında, döküm çekimi görsel açıdan güçlü.",
},
"sanliurfa": {
 "kultur": "Göbeklitepe UNESCO Dünya Mirası listesinde ve bilinen en eski anıtsal tapınak alanlarından; klipte güçlü bir tarihi ölçek veriyor. Halfeti'nin sular altındaki minaresi ayrı bir kadraj veriyor.",
 "mekan": "Göbeklitepe, Balıklıgöl ve Halil-ür Rahman, Halfeti ve batık minare, Harran kubbeli evleri, Şanlıurfa Kalesi",
 "dugun_notu": "Yaz gündüz sıcaklığı çok yüksek; dış çekim sabah erken ve akşam saatlerine planlanıyor.",
 "isletme_notu": "Tekstil, gıda-yağ sanayi ve GAP sulamalı tarım il ekonomisinin üç kolu; tarla ve fabrika çekimi aynı günde mümkün.",
},
"sirnak": {
 "kultur": "Cizre'nin tarihi taş yapıları ve Cudi Dağı hattı klipte sert, taş ağırlıklı bir dil kuruyor. Uludere yaylaları yaz aylarında tamamen farklı bir renk veriyor.",
 "mekan": "Cizre Ulu Camii ve Kırmızı Medrese, Cudi Dağı hattı, Uludere yaylaları, Dicle kıyısı, Habur çevresi",
 "dugun_notu": "Yaz sıcağı yüksek, yayla erişimi yaz aylarıyla sınırlı; iki lokasyon ayrı gün planlanıyor.",
 "isletme_notu": "Silopi asfaltiti ve Habur üzerinden sınır ticareti-lojistik il ekonomisinin iki ayağı; Gabar petrol üretimi üçüncü hat.",
},
}
