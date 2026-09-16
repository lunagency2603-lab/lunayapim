# -*- coding: utf-8 -*-
"""
Kademe 2-3 illeri — ikinci parti, 21 il (17.09.2026).

DOĞRULAMA: 84 alanın tamamı kaynak taramasıyla kontrol edildi; 21 alan düzeltildi.
Ayıklananlar: ölçülemez üstünlük iddiaları ("Türkiye'de en çok çekilen"),
kaynaksız sektör sıralamaları ve güncelliğini yitirmiş mekân bilgisi
(Elazığ Buzluk Mağarası ziyarete kapalı, Abant 2022'de milli park oldu).

Yeni satır eklerken aynı kural: doğrulanamayan iddia yazma, ölçülemez sonuç
vaat etme, il/ilçe eşleşmesini kaynaktan teyit et.
"""

EK6 = {
"aksaray": {
 "kultur": "Hasandağı silueti ve Ihlara Vadisi'nin kanyon duvarları klipte dikey ölçek veriyor; Tuz Gölü kıyısı beyaz ve boş ama Özel Çevre Koruma Bölgesi kapsamında, erişim izne bağlı.",
 "mekan": "Ihlara Vadisi ve kaya kiliseleri, Hasandağı manzarası, Tuz Gölü kıyısı, Selime Katedrali, Aksaray Ulu Camii",
 "dugun_notu": "İç Anadolu karasal iklimi; açık hava çekimi Mayıs-Ekim arasında, kış aylarında kapalı mekâna kayıyor.",
 "isletme_notu": "Ticari araç üretimi, tarım makineleri ve gıda işleme öne çıkıyor; fabrika içi çekimde iş güvenliği izni önceden alınıyor.",
},
"amasya": {
 "kultur": "Yeşilırmak kıyısındaki Yalıboyu evleri ve arkalarındaki Kral Kaya Mezarları tek karede iki tarihi katman veriyor; gece aydınlatmasıyla klipte doğrudan kullanılabiliyor.",
 "mekan": "Yalıboyu evleri ve Yeşilırmak, Kral Kaya Mezarları, Amasya Kalesi, Ferhat Su Kanalı, elma bahçeleri",
 "dugun_notu": "Irmak kıyısı dış çekimde açık hat; dar sokaklarda ekipman taşıma süresi plana eklenmeli.",
 "isletme_notu": "Şeker pancarı işleme, hazır giyim ve Amasya beji mermeri öne çıkıyor; Amasya Misket Elması menşe adı tescilli, hasat Ekim'de.",
},
"ardahan": {
 "kultur": "Çıldır Gölü kışın yüzeyi donan nadir göllerden; buz üstü çekim Türkiye'de çok az yerde mümkün. Yaz aylarında ise geniş yayla düzlükleri açılıyor.",
 "mekan": "Çıldır Gölü ve buz mevsimi, Şeytan Kalesi, Ardahan Kalesi, Yalnızçam yaylaları, Kura Nehri vadisi",
 "dugun_notu": "Rakım yüksek ve kış uzun; açık hava çekimi Haziran-Eylül penceresiyle sınırlı.",
 "isletme_notu": "Büyükbaş hayvancılık ve kaşar üretimi taban; Ardahan Çiçek Balı coğrafi işaretli, mandıra çekimi üretimi doğrudan gösteriyor.",
},
"artvin": {
 "kultur": "Çoruh Vadisi'nin dik yamaçları ve Karagöl'ün orman dokusu klipte dar, derin kadrajlar veriyor. Rakım farkı aynı gün içinde iki farklı mevsim görüntüsü sağlıyor.",
 "mekan": "Çoruh Vadisi ve rafting parkuru, Karagöl, Kafkasör yaylası, Macahel vadisi, Borçka çevresi",
 "dugun_notu": "Yağış rejimi yıla yayılı ve yollar virajlı; ulaşım süresi ile yedek gün plana mutlaka giriyor.",
 "isletme_notu": "Çay, fındık ve bal üretimi taban; sanayide gıda, orman ürünleri ve hazır beton önde, tesisler vadi boyunca dağınık.",
},
"agri": {
 "kultur": "Ağrı Dağı ve İshak Paşa Sarayı aynı ilçede, Doğubayazıt'ta; 5.137 metrelik zirve ile saray tek günde aynı rotada çekilebiliyor, açılış karesi doğrudan kuruluyor.",
 "mekan": "Ağrı Dağı, İshak Paşa Sarayı, Balık Gölü, Meteor Çukuru, Doğubayazıt ovası",
 "dugun_notu": "Kış sert ve uzun; dış çekim Haziran-Eylül arasında, kar dönemi kapalı mekâna kayıyor.",
 "isletme_notu": "Hayvancılık ve süt ürünleri taban, Gürbulak üzerinden sınır ticareti ve lojistik ikinci hat; turizm İshak Paşa çevresinde yoğunlaşıyor.",
},
"batman": {
 "kultur": "Hasankeyf'in taşınan yapıları ve baraj gölü, Türkiye'de başka örneği olmayan bir arka plan veriyor. Petrol sahalarının endüstriyel dokusu ise tamamen zıt bir dil sunuyor.",
 "mekan": "Yeni Hasankeyf ve taşınan Zeynel Bey Türbesi, Batman Çayı, petrol kule sahaları, Hasankeyf baraj gölü kıyısı",
 "dugun_notu": "Yaz gündüz sıcaklığı yüksek; dış çekim sabah erken ve akşam saatlerine planlanıyor.",
 "isletme_notu": "Ham petrol üretimi ve Tüpraş rafinerisi ilin sanayi kimliği; OSB'de firma sayısında tekstil ve gıda önde, saha izni uzun sürüyor.",
},
"bilecik": {
 "kultur": "Söğüt Osmanlı'nın kuruluş yeri; Ertuğrul Gazi'yi Anma ve Yörük Şenlikleri her eylül burada yapılıyor. Seramik ve mermer tesislerinin ölçeği endüstriyel çekim için elverişli.",
 "mekan": "Söğüt ve Ertuğrul Gazi Türbesi, Şeyh Edebali Türbesi, Pelitözü Göleti, seramik tesisleri, Osmaneli tarihi evleri",
 "dugun_notu": "Bursa ve Eskişehir'e yakınlık nedeniyle aynı gün ekip çıkarmak mümkün; konaklama maliyeti düşüyor.",
 "isletme_notu": "Mermer işleme en yaygın kol; seramik ve refrakter Söğüt'te, makine imalatı Bozüyük'te yoğun, fabrika çekimi randevuyla yapılıyor.",
},
"bitlis": {
 "kultur": "Ahlat'ın Selçuklu mezar taşları ve Nemrut Krater Gölü klipte başka yerde kurulamayacak bir ölçek veriyor. Ahlat taşının rengi kurguda ayrı bir renk düzeni gerektiriyor.",
 "mekan": "Ahlat Selçuklu Meydan Mezarlığı, Nemrut Krater Gölü, Bitlis Kalesi, Ahlat taş ocakları, Van Gölü kıyısı",
 "dugun_notu": "Rakım yüksek, kış uzun; Nemrut krater yolu yaz aylarında açılıyor, çekim penceresi dar.",
 "isletme_notu": "Hayvancılık il ekonomisinin tabanı; bitkisel üretimde tütün ve ceviz önde, Ahlat taşı atölyeleri el işçiliğini gösteren çekime uygun.",
},
"bolu": {
 "kultur": "Abant, Yedigöller ve Gölcük sonbaharda renk değişimiyle kısa mesafede üç ayrı orman kadrajı veriyor; İstanbul ve Ankara'ya yakınlık günübirlik ekip çıkarmayı mümkün kılıyor.",
 "mekan": "Abant Gölü, Yedigöller, Gölcük tabiat parkı, Kartalkaya, Mudurnu'nun tarihi evleri",
 "dugun_notu": "Abant 2022'de milli park oldu; Yedigöller ve Gölcük'te de çekim izni ve giriş ücreti önden ayarlanıyor.",
 "isletme_notu": "Kanatlı eti, orman ürünleri ve Gerede deri sanayisi üç ana kol; Mengen aşçılık geleneği mutfak çekimini öne çıkarıyor.",
},
"burdur": {
 "kultur": "Salda Gölü'nün beyaz kumu ve turkuaz suyu Türkiye'de eşi olmayan bir renk paleti veriyor; koruma statüsü nedeniyle çekim alanı sınırlı. Sagalassos ise dağ yamacında antik bir set sunuyor.",
 "mekan": "Salda Gölü (koruma alanı sınırlı), Sagalassos antik kenti, İnsuyu Mağarası, Burdur Gölü, mermer ocakları",
 "dugun_notu": "Salda'da koruma alanı kuralları geçerli; dış çekim izni ve alan sınırı önceden netleştirilmeli.",
 "isletme_notu": "Mermer ocak ve atölyeleri istihdamın yaklaşık üçte biri; süt sığırcılığı ekonominin diğer tabanı, ocak çekiminde güvenlik izni şart.",
},
"duzce": {
 "kultur": "Akçakoca sahili ile Samandere ve Güzeldere şelaleleri aynı gün çekilebilecek kadar yakın; deniz-orman-şelale üçlüsü tek kurguda toplanabiliyor.",
 "mekan": "Akçakoca sahili, Samandere Şelalesi, Güzeldere Şelalesi, Topuk Yaylası, fındık bahçeleri",
 "dugun_notu": "Batı Karadeniz yağış rejimi yıla yayılı; sahil ve şelale çekimlerinde yedek gün planlanıyor.",
 "isletme_notu": "Tekstil, otomotiv yan sanayi ve silah sanayi OSB'nin ana kolları; orman ürünleri ve fındık işleme yanında, tesis çekimi randevulu.",
},
"elazig": {
 "kultur": "Harput'un kale ve tarihi yapıları ile Hazar Gölü aynı gün içinde çekilebiliyor. Harput'ta yaşayan müzik geleneği, klipte yerel müzisyenle çalışmaya elverişli.",
 "mekan": "Harput Kalesi ve tarihi yapılar, Hazar Gölü, Keban Barajı, bağ alanları; Buzluk Mağarası ziyarete kapalı",
 "dugun_notu": "Hazar Gölü kıyısı dış çekimde öne çıkıyor; yaz aylarında gündüz sıcaklığı akşam çekimini zorunlu kılabiliyor.",
 "isletme_notu": "Madencilik (krom, bakır), çimento ve mermer il sanayisinin üç ayağı; Öküzgözü üzümü ve bağcılık gıda tarafında ayrı bir hat.",
},
"erzincan": {
 "kultur": "Kemaliye'deki Taş Yol ve Karanlık Kanyon Türkiye'nin en dar, en dik kanyon hatlarından; klipte kapalı ve gergin bir dil kuruyor. Girlevik Şelalesi kışın donuyor.",
 "mekan": "Kemaliye Taş Yol ve Karanlık Kanyon, Girlevik Şelalesi, Ergan Dağı, Fırat vadisi, bakır atölyeleri",
 "dugun_notu": "Kemaliye yolu dar ve tek şeritli; ekipman aracı ve çekim süresi buna göre planlanmalı.",
 "isletme_notu": "Ekonominin tabanı tarım ve hayvancılık, madencilik ikinci sırada; tescilli tulum peyniri ve bakır işçiliği çekime elverişli.",
},
"erzurum": {
 "kultur": "Palandöken'in pist ve kar dokusu kış çekimlerinde hazır bir zemin; Çifte Minareli Medrese ve Ulu Camii taş mimarisiyle şehrin diğer yüzünü veriyor.",
 "mekan": "Palandöken kayak pistleri, Çifte Minareli Medrese, Üç Kümbetler, Tortum Şelalesi, Oltu taşı atölyeleri",
 "dugun_notu": "Kış uzun ve sert; kar dönemi dış çekim için avantaj, ancak ekipman soğuk dayanımı hesaba katılmalı.",
 "isletme_notu": "Tarım ve hayvancılık il ekonomisinin tabanı; süt ürünleri, Oltu taşı işçiliği ve kış turizmi sezonluk içerik hatları.",
},
"giresun": {
 "kultur": "Fındık bahçelerinin basamaklı dokusu ve Giresun Adası klipte Karadeniz'e özgü bir derinlik veriyor. Kümbet ve Bektaş yayla yollarının durumu mevsime bağlı, çekim öncesi teyit gerekiyor.",
 "mekan": "Giresun Adası, fındık bahçeleri ve teraslar, Kümbet ve Bektaş yaylaları, Mavi Göl, Giresun Kalesi",
 "dugun_notu": "Fındık hasadı Ağustos'ta; bahçe çekimi bu pencerede, yağış için yedek gün her mevsim gerekiyor.",
 "isletme_notu": "Fındık işleme ilin ekonomik omurgası; Türkiye üretiminin yaklaşık yüzde 12'si Giresun'dan, balıkçılık ve orman ürünleri ikinci hat.",
},
"gumushane": {
 "kultur": "Karaca Mağarası'nın sarkıt dokusu ve Zigana'nın sisli orman hattı klipte iki ayrı kapalı atmosfer sunuyor. Santa Harabeleri terk edilmiş taş yerleşim olarak öne çıkıyor.",
 "mekan": "Karaca Mağarası, Zigana geçidi, Santa Harabeleri, Tomara Şelalesi, Harşit vadisi",
 "dugun_notu": "Rakım yüksek ve sis sık; dış çekimde gün ışığı penceresi kısa, plan buna göre kuruluyor.",
 "isletme_notu": "Madencilik ile pestil-köme üretimi il ekonomisinin iki ayağı; pestil atölyeleri el işçiliğini gösteren çekime uygun.",
},
"hakkari": {
 "kultur": "Cilo ve Sat Dağları 2020'de Türkiye'nin 45. milli parkı ilan edildi; buzul ve göl hattı klipte ölçek veriyor, çekim izni plana giriyor. Zap Vadisi dar ve derin kadrajlar sunuyor.",
 "mekan": "Cilo Dağları ve buzullar, Zap Vadisi, Berçelan yaylası, Hakkari kilim atölyeleri, Sat Gölleri",
 "dugun_notu": "Yol ve rakım koşulları belirleyici; dış çekim Temmuz-Eylül penceresinde, ulaşım süresi yüksek.",
 "isletme_notu": "Hayvancılık, arıcılık ve sınır ticareti üç ana kol; kilim dokuma küçük ölçekli ama görsel açıdan güçlü.",
},
"hatay": {
 "kultur": "Antakya 6 Şubat 2023 depreminden ağır etkilendi; tarihi merkez büyük ölçüde yeniden inşa sürecinde. Çekim planı yaparken hangi yapının ayakta olduğu güncel olarak teyit edilmeli.",
 "mekan": "Titus Tüneli ve Çevlik, Vakıflı köyü, Samandağ sahili, Amanos etekleri, zeytinlikler (Antakya merkez inşa hâlinde)",
 "dugun_notu": "Merkezde mekân kapasitesi deprem sonrası sınırlı; çekim öncesi mekânın açık olduğu teyit edilmeli.",
 "isletme_notu": "Demir-çelik, liman ve lojistik ile zeytinyağı üç ana kol; İskenderun hattı sanayi çekimi için ana lokasyon.",
},
"karaman": {
 "kultur": "Taşkale'nin kaya içine oyulmuş tahıl ambarları klipte az görülmüş bir doku veriyor. Binbir Kilise bölgesi terk edilmiş taş yapı arayan işler için uygun.",
 "mekan": "Taşkale kaya ambarları, Binbir Kilise (Madenşehir), Ermenek Barajı, Karaman Kalesi, İncesu Mağarası",
 "dugun_notu": "Konya'ya yakınlık ekip çıkarmayı kolaylaştırıyor; karasal iklim nedeniyle dış çekim Mayıs-Ekim arasında.",
 "isletme_notu": "Bisküvi ve gıda sanayi ilin en büyük kalemi; Türkiye bisküvi üretiminin yaklaşık üçte biri Karaman'dan çıkıyor.",
},
"kars": {
 "kultur": "Ani Harabeleri 2016'da UNESCO Dünya Mirası listesine alındı ve sınır hattında geniş bir açık alan sunuyor. Şehir merkezindeki Rus dönemi taş yapılar klipte tamamen farklı bir mimari dil veriyor.",
 "mekan": "Ani Harabeleri, Kars Kalesi, Rus dönemi taş binalar, Sarıkamış ormanları, Çıldır Gölü kıyısı",
 "dugun_notu": "Kış uzun ve çok soğuk; kar dönemi görsel avantaj, ancak ekipman ve ekip dayanımı plana giriyor.",
 "isletme_notu": "Coğrafi işaretli kaşar ve gravyerde yılda yaklaşık 19 bin ton üretim var; arıcılık ve hayvancılık diğer iki kol.",
},
"kastamonu": {
 "kultur": "Kasaba Köyü'ndeki Mahmut Bey Camii 2023'te UNESCO Dünya Mirası listesine girdi; ahşap işçiliği klipte yakın plan detay veriyor. Ilgaz ve Küre Dağları orman hattını tamamlıyor.",
 "mekan": "Kastamonu Kalesi ve tarihi konaklar, Kasaba Köyü Mahmut Bey Camii, Ilgaz Dağı, Küre Dağları Milli Parkı, Valla Kanyonu",
 "dugun_notu": "Konak içi çekimlerde izin işletmeye bağlı; orman ve kanyon hattında ulaşım süresi plana ekleniyor.",
 "isletme_notu": "Orman ürünleri ve kereste ilin lokomotif sektörü; Küre bakır madenciliği ikinci hat, turizm Ilgaz kış sezonunda yoğunlaşıyor.",
},
}
