# -*- coding: utf-8 -*-
"""
Kademe-1 illeri için ek alanlar.
Bu iller 7 hizmetin hepsinde ayrı sayfa aldığı için klip / düğün / işletme / drone
sayfalarında kullanılacak yerel notlara ihtiyaç var.
"""
EKSTRA = {
"bursa": {"kademe":1,
 "kultur":"Bursa'nın canlı bir yerel müzik sahnesi var; üniversite çevresindeki mekânlar ve Merinos parkı çevresi klip çekimlerinde sık kullanılıyor. Tarihi Cumalıkızık ve hanlar bölgesi ise düşük bütçeyle güçlü görünen mekânlar sunuyor.",
 "mekan":"Cumalıkızık'ın taş sokakları, Uludağ'ın sis bandı, Mudanya sahili, kapalı çarşı ve hanlar bölgesi, terk edilmiş tekstil fabrikaları",
 "isletme_notu":"Nilüfer'in kafe-restoran yoğunluğu Türkiye ortalamasının üzerinde; rekabet yüksek olduğu için sosyal medyada görünürlük doğrudan doluluk demek.",
 "dugun_notu":"Bursa'da kır düğünü kültürü güçlü; Uludağ eteklerindeki mekânlar ve zeytinlik içi düğünler yaygın."},

"istanbul": {"kademe":1,
 "kultur":"Türkiye'nin müzik endüstrisinin merkezi; stüdyo, ekip ve mekân çeşitliliği en yüksek olan şehir. Buna karşılık izin süreçleri ve trafik, çekim planlamasını en zor hale getiren şehir de burası.",
 "mekan":"Boğaz sahili, Balat'ın renkli sokakları, Karaköy ve tarihi han katları, Belgrad Ormanı, terk edilmiş sanayi yapıları, Adalar",
 "isletme_notu":"İşletme başına rekabet en yüksek burada; içerik üretmeyen işletme haritada geriye düşüyor. Aynı sokakta on rakip varken görünürlük tercih edilme sebebine dönüşüyor.",
 "dugun_notu":"Boğaz manzaralı mekânlar ve tarihi yalılar kadar, şehir dışına çıkan kır düğünü eğilimi de güçlü."},

"ankara": {"kademe":1,
 "kultur":"Ankara'nın rock ve bağımsız müzik geleneği köklü; Kızılay ve Tunalı çevresindeki sahneler yeni sanatçı çıkaran bir ekosistem. Geniş bulvarlar ve brütalist kamu yapıları kliplerde güçlü bir görsel dil veriyor.",
 "mekan":"Anıtkabir çevresi geniş açı, Hamamönü'nün restore evleri, Eymir Gölü, ODTÜ ormanı, sanayi sitelerinin metal dokusu",
 "isletme_notu":"Kamu çalışanı yoğunluğu nedeniyle öğle ve akşam trafiği net ayrışıyor; işletme içeriğinin bu ritme göre planlanması dönüşümü artırıyor.",
 "dugun_notu":"Otel ve balo salonu düğünleri ağırlıkta; Eymir ve Gölbaşı çevresinde kır düğünü talebi artıyor."},

"izmir": {"kademe":1,
 "kultur":"İzmir'in müzik sahnesi Alsancak ve Kıbrıs Şehitleri hattında yoğun; sahil ve gün batımı kliplerde en çok kullanılan iki unsur. Urla ve Alaçatı ise düşük bütçeyle 'yurt dışı' hissi veren mekânlar sunuyor.",
 "mekan":"Kordon ve gün batımı, Alaçatı sokakları, Urla bağları, Efes ve Şirince, Konak'ın tarihi asansörü",
 "isletme_notu":"Kafe ve gastronomi rekabeti İstanbul'dan sonra en yoğun ikinci şehir; mevsimsel menü değişimleri düzenli içerik ihtiyacı yaratıyor.",
 "dugun_notu":"Çeşme, Urla ve Alaçatı'da bağ ve deniz kenarı düğünleri; şehir dışından gelen davetli oranı yüksek."},

"antalya": {"kademe":1,
 "kultur":"Turizm sezonunda uluslararası sanatçı ve etkinlik trafiği yüksek; otel sahneleri ve festival alanları klip için hazır altyapı sunuyor. Kış aylarında ise sakin sahiller çekim için avantajlı.",
 "mekan":"Falezler ve Düden Şelalesi, Kaleiçi sokakları, Olympos ve Çıralı, Side antik tiyatrosu, Toros yaylaları",
 "isletme_notu":"Sezonluk işletme yoğunluğu nedeniyle içerik üretimi Nisan-Ekim arasında kritik; çok dilli içerik doğrudan yabancı müşteriye ulaşıyor.",
 "dugun_notu":"Destinasyon düğünü pazarının merkezi; yabancı çiftler için çok dilli video ve drone standart beklenti."},

"kocaeli": {"kademe":1,
 "kultur":"Sanayi kenti kimliği kliplerde güçlü bir görsel zemin veriyor: liman, vinç ve fabrika siluetleri. Şehrin genç nüfusu için üniversite çevresi canlı bir sahne.",
 "mekan":"İzmit Körfezi ve liman vinçleri, Kartepe'nin kar örtüsü, Seka Park, Gölcük ormanları, terk edilmiş sanayi yapıları",
 "isletme_notu":"Vardiya düzeni nedeniyle işletme trafiği günün belirli saatlerinde patlıyor; içerik takviminin bu saatlere göre kurulması dönüşümü artırıyor.",
 "dugun_notu":"Kartepe ve Gölcük çevresinde kır düğünü mekânları artıyor; İstanbul'dan gelen çift oranı yüksek."},

"konya": {"kademe":1,
 "kultur":"Konya'nın tasavvuf müziği geleneği ve semazen imgesi klip ve marka filmlerinde güçlü bir görsel referans. Geniş ova ve bozkır ise minimal, sinematik planlar için ideal.",
 "mekan":"Mevlana Müzesi çevresi, Tuz Gölü ve bozkır, Beyşehir Gölü, Sille'nin taş evleri, Çatalhöyük",
 "isletme_notu":"Yerel işletmelerde aile müşterisi ağırlıkta; içerikte hijyen, porsiyon ve mekân genişliği vurgusu doğrudan tercih sebebi.",
 "dugun_notu":"Kalabalık davetli sayısı norm; büyük salon düğünlerinde çok kameralı çekim ve drone talebi yüksek."},

"adana": {"kademe":1,
 "kultur":"Adana'nın sokak kültürü ve gece hayatı kliplerde sıcak, hareketli bir dil sunuyor. Taşköprü ve nehir kenarı en çok kullanılan mekânlar.",
 "mekan":"Taşköprü ve Seyhan Nehri, Sabancı Merkez Camii silueti, Çukurova ovası, Varda Köprüsü, portakal bahçeleri",
 "isletme_notu":"Gastronomi şehri olması işletme içeriğinde yemek görüntüsünü belirleyici kılıyor; sıcak iklim nedeniyle akşam trafiği ağırlıkta.",
 "dugun_notu":"Açık hava ve bahçe düğünleri yaz aylarında yoğun; sıcak nedeniyle çekim planı akşam saatlerine kayıyor."},

"gaziantep": {"kademe":1,
 "kultur":"Gaziantep'in gastronomi kimliği marka filmlerinde en güçlü kart; bakırcılar çarşısı ve tarihi hanlar kliplerde doku sağlıyor. Yerel müzik sahnesi düğün ve fasıl geleneğiyle iç içe.",
 "mekan":"Bakırcılar Çarşısı, Zeugma mozaikleri, Gaziantep Kalesi, tarihi hanlar, fıstık bahçeleri",
 "isletme_notu":"Gastronomi işletmelerinde rekabet çok yüksek ve müşteri görselden karar veriyor; yemek çekimi kalitesi doğrudan masa sayısına yansıyor.",
 "dugun_notu":"Kalabalık ve çok günlü düğün geleneği; kına gecesi ayrı bir prodüksiyon olarak talep ediliyor."},

"mersin": {"kademe":1,
 "kultur":"Liman kenti hareketliliği ve uzun sahil şeridi kliplerde açık, geniş bir dil veriyor. Üniversite nüfusu canlı bir sahne yaratıyor.",
 "mekan":"Kızkalesi, Mersin limanı ve konteyner sahası, Cennet-Cehennem obrukları, narenciye bahçeleri, Tarsus şelalesi",
 "isletme_notu":"Sahil hattındaki işletmelerde sezon farkı keskin; kış aylarında yerel müşteriye dönük ayrı bir içerik dili gerekiyor.",
 "dugun_notu":"Deniz kenarı ve otel düğünleri ağırlıkta; gün batımı çekimi standart beklenti."},

"kayseri": {"kademe":1,
 "kultur":"Erciyes'in şehre hâkim silueti kliplerde güçlü bir arka plan; kış aylarında kar manzarası düşük maliyetle büyük görünen sahneler veriyor.",
 "mekan":"Erciyes Dağı ve pistler, Kayseri Kalesi, Kapadokya'ya uzanan vadiler, tarihi Talas evleri, OSB'nin metal dokusu",
 "isletme_notu":"Ticaret kültürü güçlü; işletme içeriğinde fiyat-değer vurgusu ve ürün çeşidi gösterimi öne çıkıyor.",
 "dugun_notu":"Büyük salon düğünleri ve kalabalık davetli normu; kış düğünlerinde Erciyes çekimi tercih ediliyor."},

"mugla": {"kademe":1,
 "kultur":"Bodrum ve Göcek'in uluslararası müzik ve etkinlik trafiği yazın zirve yapıyor; marina ve tekne sahneleri klipte en çok istenen mekânlar.",
 "mekan":"Bodrum kalesi ve marina, Ölüdeniz, Datça koyları, Göcek adaları, çam ormanları, Kayaköy",
 "isletme_notu":"Sezon dışı doluluk sorunu içerik üretimini yıl boyu gerekli kılıyor; yabancı müşteri için çok dilli içerik doğrudan rezervasyon getiriyor.",
 "dugun_notu":"Türkiye'nin destinasyon düğünü başkenti; yabancı çift oranı ve drone talebi en yüksek il."},

"denizli": {"kademe":1,
 "kultur":"Pamukkale'nin beyaz travertenleri klip ve marka filminde dünya çapında tanınan bir dekor; sabah ışığı bu mekânda en değerli saat.",
 "mekan":"Pamukkale travertenleri, Hierapolis antik tiyatrosu, Salda'ya uzanan yollar, Honaz Dağı, tekstil fabrikaları",
 "isletme_notu":"Turist ve yerel müşteri iki ayrı dil istiyor; işletme içeriğinin iki kanala ayrılması dönüşümü artırıyor.",
 "dugun_notu":"Pamukkale çevresinde dış çekim geleneği güçlü; sabah erken saat çekimi standart."},

"sakarya": {"kademe":1,
 "kultur":"Sapanca ve orman dokusu kliplerde huzurlu, doğa ağırlıklı bir dil sunuyor; İstanbul'a yakınlığı ekip taşımayı kolaylaştırıyor.",
 "mekan":"Sapanca Gölü ve sis, Acarlar Longozu, Karasu sahili, Maşukiye dereleri, otomotiv fabrikalarının hatları",
 "isletme_notu":"Hafta sonu İstanbul'dan gelen ziyaretçi trafiği işletme cirosunun belirleyicisi; içerik Cuma öncesi yayınlandığında dönüşüm en yüksek.",
 "dugun_notu":"Sapanca ve Maşukiye'de kır düğünü yoğun; İstanbul'dan gelen çift oranı çok yüksek."},

"tekirdag": {"kademe":1,
 "kultur":"Şarköy bağları ve uzun sahil şeridi kliplerde açık, yaz hissi veren bir dil sunuyor; Trakya'nın rüzgâr türbinleri güçlü bir modern doku.",
 "mekan":"Şarköy bağları ve sahil, rüzgâr türbini tarlaları, Ganos Dağları, Marmaraereğlisi kumsalı, Rakoczi Müzesi",
 "isletme_notu":"Sanayi çalışanı ve hafta sonu İstanbul ziyaretçisi iki ayrı müşteri; işletme içeriğinin ikisini de kapsaması gerekiyor.",
 "dugun_notu":"Bağ evi ve sahil düğünleri artıyor; İstanbul'a yakınlık nedeniyle davetli sayısı yüksek."},

"balikesir": {"kademe":1,
 "kultur":"Ayvalık ve Cunda'nın taş sokakları kliplerde nostaljik bir dil veriyor; Kaz Dağları ise doğa temalı işlerde tercih ediliyor.",
 "mekan":"Cunda adası sokakları, Ayvalık adaları ve gün batımı, Kaz Dağları, zeytinlikler, Erdek koyları",
 "isletme_notu":"Yazlık nüfus nedeniyle sezon farkı çok keskin; kış aylarında yerel müşteriye dönük ayrı içerik gerekiyor.",
 "dugun_notu":"Zeytinlik ve deniz kenarı düğünleri yaygın; Ayvalık'ta destinasyon düğünü talebi artıyor."},

"eskisehir": {"kademe":1,
 "kultur":"Öğrenci nüfusu Eskişehir'i Türkiye'nin en canlı bağımsız müzik sahnelerinden biri yapıyor; Porsuk kenarı ve Odunpazarı en çok kullanılan mekânlar.",
 "mekan":"Porsuk Çayı ve köprüler, Odunpazarı'nın renkli evleri, Sazova Parkı, tramvay hattı, Frig Vadisi",
 "isletme_notu":"Öğrenci müşteri ağırlıkta; fiyat ve atmosfer vurgusu ile kısa dikey içerik burada en yüksek dönüşümü veriyor.",
 "dugun_notu":"Öğrenci şehri olması nedeniyle genç çift oranı yüksek; sade ve modern konsept talep ediliyor."},

"samsun": {"kademe":1,
 "kultur":"Uzun sahil şeridi ve Amisos tepesi kliplerde geniş, açık planlar veriyor; yerel müzik sahnesi üniversite çevresinde toplanmış.",
 "mekan":"Amisos Tepesi ve teleferik, Bandırma Vapuru, Kızılırmak deltası, Batı Park sahili, Nebiyan yaylası",
 "isletme_notu":"Sahil yürüyüş yolu çevresindeki işletmelerde mevsim farkı keskin; kış aylarında iç mekân atmosferi öne çıkarılmalı.",
 "dugun_notu":"Deniz manzaralı salon düğünleri ağırlıkta; delta ve sahilde dış çekim yaygın."},

"trabzon": {"kademe":1,
 "kultur":"Karadeniz müziği ve horon geleneği klip ve marka filmlerinde güçlü bir yerel kimlik sunuyor; yayla ve sis en çok istenen iki unsur.",
 "mekan":"Sumela Manastırı, Uzungöl, Ayder yolu yaylaları, Boztepe'den şehir manzarası, Fırtına vadisi",
 "isletme_notu":"Körfez turisti sezonu yaz aylarında zirve yapıyor; Arapça içerik yerel işletmelerde doğrudan müşteri getiriyor.",
 "dugun_notu":"Kalabalık ve müzikli düğün geleneği; yayla dış çekimi neredeyse standart."},

"manisa": {"kademe":1,
 "kultur":"Spil Dağı ve bağlar kliplerde sakin, doğal bir dil sunuyor; İzmir'e yakınlık ekip ve ekipman taşımayı kolaylaştırıyor.",
 "mekan":"Spil Dağı, üzüm bağları, Sardes antik kenti, Gediz ovasının geometrik tarlaları, Manisa OSB'nin hatları",
 "isletme_notu":"Sanayi çalışanı yoğunluğu vardiya saatlerine göre trafik yaratıyor; içerik takviminin buna göre kurulması dönüşümü artırıyor.",
 "dugun_notu":"Bahçe ve salon düğünleri ağırlıkta; İzmir'den gelen davetli oranı yüksek."},

"aydin": {"kademe":1,
 "kultur":"Kuşadası ve Didim'in yaz sahnesi uluslararası; incir ve zeytin bahçeleri ise marka filmlerinde güçlü bir yerel doku veriyor.",
 "mekan":"Kuşadası sahili ve Güvercinada, Didim Apollon Tapınağı, zeytinlikler ve incir bahçeleri, Efes'e uzanan yollar, Bafa Gölü",
 "isletme_notu":"Sezonluk yabancı müşteri oranı yüksek; çok dilli içerik ve menü görseli doğrudan doluluk demek.",
 "dugun_notu":"Deniz kenarı ve bağ düğünleri; yabancı çift talebi Kuşadası'nda belirgin."},

"yalova": {"kademe":1,
 "kultur":"Küçük ölçekli ama yoğun ziyaretçi trafiği olan bir il; termal tesisler ve deniz kenarı kliplerde sakin bir dil veriyor. Bursa'ya yakınlık aynı gün ekip çıkarmayı mümkün kılıyor.",
 "mekan":"Yürüyen Köşk, termal tesis bahçeleri, Çınarcık sahili, Erikli ve Delmece yaylaları, fidanlıklar",
 "isletme_notu":"Hafta sonu İstanbul ziyaretçisi cironun büyük kısmını oluşturuyor; içerik Perşembe-Cuma yayınlandığında en yüksek dönüşümü veriyor.",
 "dugun_notu":"Termal otel ve deniz kenarı düğünleri; İstanbul'dan gelen çift oranı yüksek."},
}
