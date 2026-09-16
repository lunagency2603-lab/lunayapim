# -*- coding: utf-8 -*-
"""
Kademe 2-3 illeri için yerel notlar — 17.09.2026.
Search Console'da gösterim alan ama klip/düğün/işletme verisi olmayan 18 il.
Bu dört alan dolduğunda üretici o il için klip, düğün ve işletme sayfalarını
da açıyor (bkz. uretici.sayfa_var / VERI_KOSULU).

DOĞRULAMA: 17.09.2026'da 72 alanın tamamı kaynak taramasıyla tek tek kontrol
edildi; 44 alan düzeltildi. Kaynaksız kültürel genellemeler, ölçülemez pazarlama
iddiaları ve il/ilçe karışıklıkları ayıklandı. Yeni satır eklerken aynı kuralı
uygula: doğrulanamayan iddia yazma, ölçülemez sonuç vaat etme.
"""

EK5 = {
"mardin": {
 "kultur": "Mardin taş mimarisi ve Mezopotamya ovasına bakan teraslarıyla Türkiye'de en çok dizi ve klip çekilen şehirlerden biri. Gün batımında kireç taşının aldığı renk, kurguda ayrı bir ışık düzeni gerektirmeyecek kadar güçlü.",
 "mekan": "Eski Mardin sokakları ve taş cepheler, Deyrulzafaran Manastırı, Kasımiye Medresesi, Dara antik kenti, Midyat'ın konak avluları",
 "dugun_notu": "Kına gecesi düğünden ayrı günde; iki ayrı çekim günü planlamak gerekiyor. Teras düğünlerinde ova manzarası belirleyici.",
 "isletme_notu": "İl ekonomisi ağırlıkla tarım ve hayvancılığa dayanıyor; turizm işletmeleri eski şehirde yoğunlaşıyor. Yaz sıcağı nedeniyle çekim sabah ve akşama kayıyor.",
},
"adiyaman": {
 "kultur": "Nemrut'un şafak saati şehrin görsel kimliğini tek başına taşıyor; klipte açılış karesi olarak sık kullanılıyor. Şehir merkezi ise hâlâ şantiye; yeni konut alanları dışında arka plan seçimi sınırlı.",
 "mekan": "Nemrut Dağı zirvesi ve dev heykeller, Cendere Köprüsü, Atatürk Baraj Gölü, Perre antik kenti, Karakuş tümülüsü",
 "dugun_notu": "Köy düğünleri hasat sonrasına, şehir düğünleri bahar ve yaza toplanıyor; Nemrut'ta yol süresi eklenmeli.",
 "isletme_notu": "Yeniden yapılanma sürüyor; çarşı projeleri tamamlanmadığı için esnafın bir bölümü hâlâ geçici alanlarda, tanıtım ihtiyacı bu nedenle yoğun.",
},
"siirt": {
 "kultur": "Botan Vadisi ve kanyon manzaraları klipte geniş açılı, sakin bir dil kuruyor. Yerel dokuma ve battaniye atölyeleri detay çekiminde şehre özgü doku veriyor.",
 "mekan": "Botan Vadisi ve kanyon, Tillo'nun taş yapıları, Siirt fıstığı bahçeleri, Billoris (Sağlarca) kaplıcası, tarihi Ulu Camii",
 "dugun_notu": "Siirt düğünü genelde dört güne yayılıyor ve kalabalık; çok kameralı plan ve çok günlü kayıt gerekiyor.",
 "isletme_notu": "Fıstık ve hayvancılık il ekonomisinin tabanı, bakır madenciliği ise en büyük sanayi işvereni; dokuma atölyeleri küçük ölçekli ama çekime elverişli.",
},
"diyarbakir": {
 "kultur": "Bazalt surlar ve Hevsel Bahçeleri klipte koyu taş ile yeşil arasında güçlü bir kontrast kuruyor. Alan UNESCO Dünya Mirası listesinde olduğu için drone çekimi izne bağlı.",
 "mekan": "Diyarbakır surları, On Gözlü Köprü ve Dicle, Hevsel Bahçeleri, Ulu Camii avlusu, tarihi bazalt konaklar",
 "dugun_notu": "Yaz düğünlerinde gündüz sıcaklığı 40 dereceyi aşıyor; dış çekim akşam saatlerine planlanmalı.",
 "isletme_notu": "Surlar ve Hevsel Bahçeleri 2015'ten beri UNESCO Dünya Mirası listesinde; tarihi doku ve mutfak, işletme çekimlerinde en hazır arka planı veriyor.",
},
"kahramanmaras": {
 "kultur": "Dondurma ustalığı ve bakır işçiliği şehre özgü, hareketli detay çekimleri veriyor; klipte ritim kurmak için doğrudan kullanılabiliyor. Deprem sonrası yeniden kurulan alanlar güncel ve az görüntülenmiş.",
 "mekan": "Maraş Kalesi, bakırcılar çarşısı, Ceyhan Nehri kıyısı, Yedikuyular yaylası, Döngel mağaraları",
 "dugun_notu": "Kına gecesi düğünden önceki gün yapılıyor; iki ayrı çekim günü planlanmalı, tarih erken netleşmeli.",
 "isletme_notu": "Tekstil ilin ihracatını sürükleyen ana sektör; dondurma ve bakır işçiliği ise tescilli, üretim anını gösteren çekime elverişli kalemler.",
},
"bartin": {
 "kultur": "Amasra'nın koy ve kale manzarası şehrin en çok paylaşılan karesi; klipte deniz-orman geçişi tek günde çekilebiliyor. Merkezdeki tescilli Bartın evleri yakın plan için hazır bir set.",
 "mekan": "Amasra kalesi ve Kuşkayası yolu, Bartın Irmağı, Küre Dağları ormanları, İnkumu sahili, tarihi ahşap konaklar",
 "dugun_notu": "Deniz ve orman dış çekimi aynı gün mümkün; Batı Karadeniz yağış rejimi için yedek gün planlanıyor.",
 "isletme_notu": "İl ekonomisinde madencilik, ormancılık ve tarım belirleyici; turizm işletmeleri Amasra ve İnkumu'da yoğunlaşıyor, içerik takvimi yaz sezonuna göre kuruluyor.",
},
"bayburt": {
 "kultur": "Yüksek rakım ve geniş yayla düzlükleri klipte boşluk ve sadelik isteyen işler için uygun. Baksı Müzesi çağdaş sanat ile yaylayı aynı karede buluşturan az rastlanır bir mekân.",
 "mekan": "Bayburt Kalesi, Baksı Müzesi, Çoruh Vadisi, Kop Dağı geçidi, yayla düzlükleri",
 "dugun_notu": "Gurbetçilik ilin geçiminde önemli; yaz aylarındaki dönüşler dış çekim takvimini sıkıştırıyor.",
 "isletme_notu": "Ekonomi tarım ve hayvancılığa dayanıyor, sanayi yok denecek kadar az; işletme videosunda küçük esnaf ve süt-bal üreticisi öncelikli hedef.",
},
"bingol": {
 "kultur": "Yüzen Adalar ve yayla gölleri klipte başka şehirde bulunmayan bir arka plan sunuyor. Kar mevsimi ile yeşil mevsim arasındaki keskin fark, aynı mekânda iki ayrı iş çıkarmaya izin veriyor.",
 "mekan": "Yüzen Adalar, Özlüce Barajı, Hesarek ve Yolaçtı Kurucadağ kayak merkezleri, Kös kaplıcaları, Murat Nehri vadisi",
 "dugun_notu": "Yayla ve göl kenarı dış çekimde ulaşım ve gün ışığı süresi plana giriyor; kar dönemi erişimi kısıtlıyor.",
 "isletme_notu": "Ekonomi hayvancılık, arıcılık ve ormancılığa dayanıyor; süt-bal üreticisi ile Kös kaplıcaları çevresindeki tesisler içeriğin ana müşterisi.",
},
"igdir": {
 "kultur": "Ağrı Dağı'nın en net göründüğü şehir; klipte tek karede dağ silueti ve ova birlikte giriyor. Iğdır Ovası mikroklima alanı, Kars ve Ağrı'ya göre ılıman; çekim sezonu belirgin uzun.",
 "mekan": "Ağrı Dağı manzarası, Aras Nehri ovası, Tuzluca tuz mağaraları, Aras Kuş Cenneti, kayısı bahçeleri, sınır düzlükleri",
 "dugun_notu": "Temmuz-Ağustos ortalama en yüksek 34 derece; açık hava çekimi ilkbahar ve sonbahara planlanıyor.",
 "isletme_notu": "Tarım ve Dilucu üzerinden sınır ticareti belirleyici; üretimden sevkiyata giden süreci gösteren içerik ticari müşteriye doğrudan hitap ediyor.",
},
"sinop": {
 "kultur": "Türkiye'nin en kuzey noktası; deniz, orman ve tarihi yapı aynı gün içinde çekilebiliyor. Hamsilos'un koyu ve Erfelek şelaleleri klipte sakin, doğal bir dil kuruyor.",
 "mekan": "Sinop Kalesi ve tarihi cezaevi, Hamsilos koyu, İnceburun feneri, Erfelek Şelaleleri, ahşap tekne atölyeleri",
 "dugun_notu": "Yağış yıla yayılı, en yağışlı aylar sonbahar ve kış; deniz kenarı çekimlerde yedek gün şart.",
 "isletme_notu": "Kayıtlı sanayide taş-toprak ve su ürünleri işleme ile kereste öne çıkıyor; ahşap tekne atölyeleri ve pansiyonculuk küçük ölçekli ama görsel açıdan güçlü.",
},
"kutahya": {
 "kultur": "Çini atölyeleri klipte şehre özgü bir renk ve doku paleti veriyor. Aizanoi merkezin güneybatısında, Frig kaya yapıları kuzeydoğusunda; ikisi ayrı çekim günü olarak planlanmalı.",
 "mekan": "Aizanoi Zeus Tapınağı, çini atölyeleri, Frig Vadisi kaya yapıları, Kütahya Kalesi, Yoncalı kaplıcaları",
 "dugun_notu": "Aizanoi ve Frig Vadisi ören yeri statüsünde; dış çekim için Bakanlık film çekim izni önceden alınmalı.",
 "isletme_notu": "Seramik ve çini üreticileri için ihracat odaklı içerik talebi var; üretim sürecini gösteren video fuar ve katalog işinde de kullanılıyor.",
},
"malatya": {
 "kultur": "Kayısı bahçeleri hasat mevsiminde klipte güçlü bir renk ve hareket sunuyor. Arslantepe ve Battalgazi'nin taş dokusu ise şehrin modern hattıyla zıtlık kurmaya elverişli.",
 "mekan": "Arslantepe Höyüğü, Battalgazi'nin tarihi yapıları (bir kısmı restorasyonda), kayısı bahçeleri, Levent Vadisi, Sultansuyu",
 "dugun_notu": "Kayısı hasadı Haziran sonu ile Ağustos ortası arasında; bahçe çekimi bu pencerede, salon çekimi yıl boyunca.",
 "isletme_notu": "Kayısı ihracatı belirleyici; bahçeden paketlemeye giden süreci gösteren içerik yurtdışı alıcıya doğrudan hitap ediyor.",
},
"afyonkarahisar": {
 "kultur": "Kale kayası şehrin her yerinden görünüyor ve klipte doğal bir çapa oluşturuyor. İscehisar mermer ocakları ile Ayazini-Frig Vadisi merkeze yakın; üçü aynı gün çekilebiliyor.",
 "mekan": "Afyon Kalesi kayalığı, Frig Vadisi ve Ayazini, İscehisar mermer ocakları, termal tesis havuzları, Utku Anıtı meydanı",
 "dugun_notu": "Termal tesisler kapalı mekân çekimine kış aylarında da imkân veriyor; takvim yıla yayılabiliyor.",
 "isletme_notu": "Termal turizm ve mermer ihracatı iki ayrı içerik hattı gerektiriyor; termal tesisler için sezon dışı içerik doluluk açısından kritik.",
},
"isparta": {
 "kultur": "Gül hasadı Mayıs ortası ile Haziran sonu arasında yılın en güçlü görsel malzemesini veriyor; lavanta tarlaları Temmuz-Ağustos'ta klipte tek renkli geniş alanlar sunuyor. İkisi de kısa sezonlu.",
 "mekan": "Kuyucak lavanta tarlaları, gül bahçeleri ve hasat, Eğirdir Gölü ve yarımada, Davraz zirvesi, Yalvaç antik kenti",
 "dugun_notu": "Gül Mayıs ortası-Haziran sonu, lavanta Temmuz-Ağustos başı; dış çekim takvimi iki ayrı pencereye kuruluyor.",
 "isletme_notu": "Gül yağı ve halı ihracatı sürüyor; ancak Isparta ihracatında ilk sıra elma ve maden ürünlerinde. İçerik hattı bu üç koldan kurgulanmalı.",
},
"edirne": {
 "kultur": "Selimiye'nin silueti şehrin her karesine giriyor; klipte mimari ölçek isteyen işler için hazır bir zemin. Kırkpınar haftasında şehir tamamen hareketli bir sete dönüşüyor.",
 "mekan": "Selimiye Camii ve avlusu, Meriç ve Tunca köprüleri, Karaağaç istasyonu, Sarayiçi Kırkpınar er meydanı",
 "dugun_notu": "Balkan göçmeni aile gelenekleri düğün akışını değiştiriyor; Rumeli havaları ve karşılama için ayrı ses planı gerekiyor.",
 "isletme_notu": "İlde beş gümrük kapısı var ve Kapıkule tek başına yılda milyonlarca yolcu geçiriyor; çok dilli içerik bu trafiğe göre planlanabiliyor.",
},
"karabuk": {
 "kultur": "Safranbolu'nun konak sokakları klipte dönem işleri için hazır bir set; aynı şehirde Kardemir'in endüstriyel dokusu tamamen zıt bir dil veriyor. Bu iki uç, tek günde çekilebilecek kadar yakın.",
 "mekan": "Safranbolu konakları ve Çarşı, Kardemir tesis siluetleri, Yörük Köyü, Bulak Mencilis mağarası, Tokatlı Kanyonu",
 "dugun_notu": "Safranbolu konaklarında düğün ve nişan çekimi yaygın; müze-ev ve özel konak içi çekimler işletmenin kendi iznine bağlı.",
 "isletme_notu": "İlde imalat istihdamının yarısından fazlası demir-çelikte; sanayi ile Safranbolu konak turizmi iki ayrı içerik dili gerektiriyor.",
},
"kirsehir": {
 "kultur": "Abdal müzik geleneğinin merkezi; bozlak ve bağlama şehrin kendi sesi. Kırşehir, müzik alanında UNESCO Yaratıcı Şehirler Ağı'na Türkiye'den giren ilk şehir; klipte yerel müzisyenle çalışmak şehre özgü bir doku veriyor.",
 "mekan": "Cacabey Medresesi, Ahi Evran Türbesi, Kaman Kalehöyük, termal tesisler, Seyfe Gölü kuş alanı",
 "dugun_notu": "Düğünlerde canlı müzik ve bozlak geleneği güçlü; ses kaydı planı görüntü kadar belirleyici oluyor.",
 "isletme_notu": "Tarım ve hayvancılığın yanında PETLAS ve döküm sanayi öne çıkıyor; il UNESCO müzik şehri olduğu için içerikte müzik dili yerinde duruyor.",
},
"nevsehir": {
 "kultur": "Kapadokya balonları ve peribacaları dünyada tanınan bir arka plan; klipte tek karede yer ve gök birlikte giriyor. Şafak saatinde balon kalkışı, planlamanın en kritik ve en kısa penceresi.",
 "mekan": "Göreme vadileri ve peribacaları, balon kalkış alanı, Ortahisar ve Uçhisar kaleleri, Avanos çömlek atölyeleri, Kızılırmak kıyısı",
 "dugun_notu": "Destinasyon düğünü talebi olan bir bölge; yabancı çiftler için çok dilli teslim ve şafak çekimi sık istenen kalemler.",
 "isletme_notu": "Kapadokya müze ve ören yerleri 2025'te 4,5 milyon ziyaretçi ağırladı; otel ve balon işletmelerinde İngilizce içerik pratik bir gereklilik.",
},
}
