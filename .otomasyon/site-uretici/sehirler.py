# -*- coding: utf-8 -*-
"""
Luna Yapım — şehir verisi.
Her il için buradaki metinler O İLE ÖZELDİR; sayfa üretici bunları kullanarak
her ilde farklı bir yazı çıkarır. Yeni il eklemek için aşağıya aynı alanlarla
bir kayıt eklemen yeterli.

alanlar:
  ad        : İl adı
  ek        : "-de/-da" eki ("Bursa'da" için "'da")
  icin      : "-e/-a" eki ("Bursa'ya" için "'ya")
  ekip      : "kendi" (kendi ekibimiz gider) | "ortak" (çözüm ortağı)
  ilceler   : ilçe listesi (metinde geçer)
  insaat    : o ilin inşaat/konut piyasasına dair 2-3 cümle (ÖZGÜN)
  emlak     : o ilin gayrimenkul piyasasına dair 2-3 cümle (ÖZGÜN)
  sanayi    : o ilin üretim/sanayi profiline dair 2-3 cümle (ÖZGÜN)
  cografya  : havadan çekim ve manzara açısından ilin karakteri (ÖZGÜN)
  sektorler : ürün animasyonunda hedeflenecek sektör listesi
  komsu     : iç bağlantı verilecek komşu il slug'ları
"""

SEHIRLER = [
{
 "slug":"bursa","ad":"Bursa","ek":"'da","icin":"'ya","ekip":"kendi",
 "ilceler":["Nilüfer","Osmangazi","Yıldırım","Mudanya","Gemlik","İnegöl","Gürsu","Kestel","Mustafakemalpaşa","Karacabey"],
 "insaat":"Bursa'nın konut üretimi ağırlıklı olarak Nilüfer ve Mudanya hattında yoğunlaşıyor; şehir merkezinde ise kentsel dönüşüm projeleri sürüyor. Bu iki farklı piyasa aynı anlatımı kaldırmıyor: Nilüfer'de yeni site projeleri manzara ve sosyal donatı üzerinden satılırken, dönüşüm projelerinde hak sahibine yeni yapının somut olarak gösterilmesi gerekiyor.",
 "emlak":"Uludağ manzaralı konutlar, Mudanya'da deniz cepheli projeler ve merkezdeki dönüşüm daireleri Bursa portföyünün üç ana kolunu oluşturuyor. İstanbul'dan gelen alıcı payı yüksek olduğu için mülkün uzaktan gezilebilir olması burada özellikle önemli.",
 "sanayi":"Bursa Türkiye'nin otomotiv ve tekstil merkezi; İnegöl ise mobilyada ülkenin en büyük üretim havzalarından biri. Makine, otomotiv yan sanayi, tekstil ve mobilya firmaları ürünlerini fuarda ve ihracat görüşmelerinde anlatmak zorunda — bu da 3D anlatımı doğrudan işe dönüştürüyor.",
 "cografya":"Uludağ'ın eteklerinden ovaya inen şehir silueti, tarihi Cumalıkızık, Yeşil Türbe ve Mudanya sahili havadan çekim için zengin bir kütüphane sunuyor.",
 "sektorler":["Otomotiv yan sanayi","Tekstil ve konfeksiyon","Mobilya (İnegöl)","Makine imalatı","Gıda"],
 "komsu":["yalova","kocaeli","balikesir","istanbul"]
},
{
 "slug":"istanbul","ad":"İstanbul","ek":"'da","icin":"'a","ekip":"kendi",
 "ilceler":["Beşiktaş","Kadıköy","Ataşehir","Başakşehir","Beylikdüzü","Sarıyer","Üsküdar","Maltepe","Bahçeşehir","Zeytinburnu"],
 "insaat":"İstanbul'da konut projesi tanıtımı artık tek başına render'la yürümüyor; alıcı hem projenin bitmiş halini hem de bulunduğu sokağın gerçek dokusunu görmek istiyor. Kentsel dönüşümün hızlandığı Bahçelievler, Küçükçekmece ve Zeytinburnu hattında hak sahibi sunumları için görselleştirme neredeyse zorunlu hale geldi.",
 "emlak":"Rekabetin en yüksek olduğu pazar İstanbul. Aynı bölgede yüzlerce benzer ilan varken videosu olan ilan listede farklı bir yerde duruyor. Yurt dışı alıcıya satış yapan ofisler için sanal tur ve çok dilli tanıtım videosu doğrudan satış aracı.",
 "sanayi":"Tuzla, İkitelli, Hadımköy ve Dudullu hatlarındaki üretici firmalar için ürün anlatımı çoğunlukla fuar ve ihracat odaklı. Makine, medikal, ambalaj, kimya ve tekstil firmaları ürünlerini yurt dışı müşterisine anlatmak için çok dilli animasyona ihtiyaç duyuyor.",
 "cografya":"Boğaz, Haliç, adalar silueti ve tarihi yarımada; havadan çekimde izin gerektiren bölgeler bulunduğu için planlamayı önceden yapıyoruz.",
 "sektorler":["Makine ve otomasyon","Medikal ve laboratuvar","Ambalaj","Kimya","Tekstil","Yazılım ve fintek"],
 "komsu":["kocaeli","tekirdag","bursa","yalova"]
},
{
 "slug":"ankara","ad":"Ankara","ek":"'da","icin":"'ya","ekip":"ortak",
 "ilceler":["Çankaya","Yenimahalle","Etimesgut","Keçiören","Gölbaşı","Sincan","Pursaklar","Mamak"],
 "insaat":"Ankara'da konut üretimi Çankaya'nın güneyi, Gölbaşı ve Etimesgut hattında yoğunlaşıyor. Kamu kurumlarına yakınlık ve ulaşım aksı, projelerin satış argümanının merkezinde; yerleşim maketi ve vaziyet planı animasyonu bu argümanı en net anlatan araç.",
 "emlak":"Ankara alıcısı fiyat/metrekare dengesine ve konumun ulaşım avantajına odaklanıyor. Bu yüzden burada emlak videosunun işi sadece daireyi göstermek değil; çevre yolu, metro hattı ve kamu binalarına mesafeyi havadan görünür kılmak.",
 "sanayi":"Başkentte savunma sanayi, yazılım ve makine imalatı öne çıkıyor. OSTİM ve İvedik hattındaki üretici firmalar ile teknokent şirketleri için teknik anlatım animasyonu ve süreç videosu en çok istenen iki format.",
 "cografya":"Anıtkabir, Atakule ve şehrin geniş bulvar dokusu; yüksek irtifada geniş açı planlar için elverişli bir şehir.",
 "sektorler":["Savunma sanayi","Yazılım ve teknoloji","Makine imalatı (OSTİM)","Medikal","İnşaat malzemesi"],
 "komsu":["eskisehir","konya","kayseri"]
},
{
 "slug":"izmir","ad":"İzmir","ek":"'de","icin":"'e","ekip":"ortak",
 "ilceler":["Konak","Karşıyaka","Bornova","Buca","Çeşme","Urla","Seferihisar","Gaziemir","Menemen","Alaçatı"],
 "insaat":"İzmir'de iki ayrı konut piyasası var: şehir içinde dönüşüm ve yeni site projeleri, Urla-Çeşme hattında ise butik villa ve yazlık projeleri. Villa projelerinde alıcı çoğunlukla şehir dışında olduğundan, projenin 3D olarak gezilebilir hale getirilmesi satışı doğrudan hızlandırıyor.",
 "emlak":"Deniz manzarası, bağ evi ve butik villa İzmir portföyünün en çok video isteyen kısmı. Alaçatı ve Urla'da mülkün mimarisi ve bahçesi kadar çevresindeki dokunun da gösterilmesi gerekiyor — bu da havadan çekimi zorunlu kılıyor.",
 "sanayi":"Kemalpaşa, Torbalı ve Aliağa hatlarında gıda, plastik, makine ve kimya üretimi yoğun. İhracat oranı yüksek firmalar için İngilizce ve Almanca seslendirmeli ürün animasyonu en sık istenen iş.",
 "cografya":"Körfez silueti, Çeşme ve Urla kıyıları, bağlar ve zeytinlikler; gün batımı çekimleri için Türkiye'nin en verimli sahillerinden biri.",
 "sektorler":["Gıda ve içecek","Plastik ve ambalaj","Makine","Kimya","Tarım teknolojileri"],
 "komsu":["mugla","aydin","manisa","denizli"]
},
{
 "slug":"kocaeli","ad":"Kocaeli","ek":"'nde","icin":"'ne","ekip":"kendi",
 "ilceler":["İzmit","Gebze","Darıca","Çayırova","Körfez","Gölcük","Kartepe","Başiskele"],
 "insaat":"Gebze-Darıca hattı İstanbul'a çalışan nüfus için yoğun konut üretimi yapıyor; İzmit ve Başiskele tarafında ise körfez manzaralı projeler öne çıkıyor. Alıcının çoğu İstanbul'dan geldiği için proje tanıtımının uzaktan izlenebilir olması kritik.",
 "emlak":"Kocaeli'de mülkün değerini belirleyen en önemli unsurlardan biri ulaşım: TEM, D-100, Marmaray ve OSB'lere mesafe. Bunları anlatmanın en hızlı yolu havadan tek plan bir konum videosu.",
 "sanayi":"Türkiye'nin en yoğun sanayi havzalarından biri; otomotiv, kimya, petrokimya, lastik ve boya üretimi burada toplanmış. Büyük tesislerde çekim izni ve gizlilik kuralları olduğu için 3D animasyon, üretim hattını anlatmanın hem güvenli hem net yolu.",
 "cografya":"İzmit Körfezi, Kartepe ve Gölcük sahili; sanayi siluetiyle doğanın yan yana durduğu ilginç bir görsel karakter.",
 "sektorler":["Otomotiv","Kimya ve petrokimya","Lastik","Boya","Ambalaj","Lojistik"],
 "komsu":["istanbul","sakarya","yalova","bursa"]
},
{
 "slug":"yalova","ad":"Yalova","ek":"'da","icin":"'ya","ekip":"kendi",
 "ilceler":["Merkez","Çınarcık","Termal","Armutlu","Çiftlikköy","Altınova"],
 "insaat":"Yalova konut üretiminin büyük kısmı ikinci konut ve yazlık projelerinden oluşuyor. Alıcının neredeyse tamamı şehir dışında olduğu için proje, tanıtım videosu ve 3D görsel üzerinden satılıyor — maket ofisine gelmeden karar veren alıcı oranı Türkiye ortalamasının üzerinde.",
 "emlak":"Çınarcık ve Armutlu hattında deniz manzaralı daireler, Termal'de ise doğayla iç içe villa portföyü öne çıkıyor. Manzaranın hangi kattan nasıl göründüğünü göstermek burada satışın kendisi.",
 "sanayi":"Altınova tersaneler bölgesi ve süs bitkiciliği ilin iki ayrı üretim kimliği. Tersane tarafında büyük ölçekli iş anlatımı için havadan çekim, fidancılıkta ise ürün ve üretim süreci videosu talep ediliyor.",
 "cografya":"Marmara kıyısı, termal kaynaklar ve yeşil yamaçlar; Bursa'ya yakınlığı sayesinde kendi ekibimizle aynı gün gidip dönebildiğimiz bir il.",
 "sektorler":["Tersanecilik","Süs bitkiciliği ve fidancılık","Turizm ve termal","Gıda"],
 "komsu":["bursa","kocaeli","istanbul"]
},
{
 "slug":"balikesir","ad":"Balıkesir","ek":"'de","icin":"'e","ekip":"kendi",
 "ilceler":["Merkez","Bandırma","Edremit","Ayvalık","Burhaniye","Gönen","Erdek","Susurluk"],
 "insaat":"Balıkesir'de konut üretimi merkez ile Edremit körfezi arasında ikiye ayrılıyor. Körfez hattında emekli ve yazlık alıcıya yönelik butik projeler, merkezde ise yerel talebe dönük siteler üretiliyor. İki piyasa da farklı bir anlatım dili istiyor.",
 "emlak":"Ayvalık ve Erdek'te deniz cepheli mülk, Edremit'te zeytinlik içinde ev, merkezde ise klasik daire portföyü var. Zeytinlik ve arazi satışlarında sınırların havadan gösterilmesi alıcının en çok sorduğu soruyu tek videoda kapatıyor.",
 "sanayi":"Bandırma gübre, kimya ve liman lojistiğiyle; Susurluk ve Gönen gıda ve süt ürünleriyle öne çıkıyor. Zeytinyağı üreticileri için ürün ve üretim süreci videosu ihracatta doğrudan işe yarıyor.",
 "cografya":"Kaz Dağları, zeytinlikler, Ayvalık adaları ve Erdek koyları; kıyı ile dağın bir arada olduğu az sayıdaki ilden biri.",
 "sektorler":["Zeytinyağı ve gıda","Süt ürünleri","Kimya ve gübre","Liman lojistiği","Tarım makineleri"],
 "komsu":["bursa","canakkale","manisa","izmir"]
},
{
 "slug":"sakarya","ad":"Sakarya","ek":"'da","icin":"'ya","ekip":"kendi",
 "ilceler":["Adapazarı","Serdivan","Erenler","Sapanca","Hendek","Karasu","Akyazı"],
 "insaat":"Serdivan ve Sapanca hattı Sakarya'nın en hareketli konut bölgesi; göl ve orman manzarasına bakan projeler İstanbul'dan alıcı çekiyor. Karasu'da ise deniz cepheli yatırım projeleri yoğun.",
 "emlak":"Sapanca'da bungalov ve villa, Karasu'da yazlık daire, Adapazarı'nda ise yerel talebe dönük konut. Turizm amaçlı kiralanan mülklerde tanıtım videosu doluluk oranını doğrudan etkiliyor.",
 "sanayi":"Otomotiv ana sanayi ve yan sanayi Sakarya'nın belkemiği; ayrıca beyaz eşya ve makine üretimi güçlü. Büyük tesislerde üretim hattı animasyonu, gizlilik gerektiren süreçleri anlatmanın en pratik yolu.",
 "cografya":"Sapanca Gölü, Karasu sahili ve Acarlar Longozu; su ve orman aynı karede buluşuyor.",
 "sektorler":["Otomotiv","Beyaz eşya","Makine","Gıda","Tarım"],
 "komsu":["kocaeli","bursa","duzce"]
},
{
 "slug":"tekirdag","ad":"Tekirdağ","ek":"'da","icin":"'a","ekip":"ortak",
 "ilceler":["Süleymanpaşa","Çorlu","Çerkezköy","Kapaklı","Marmaraereğlisi","Malkara","Şarköy"],
 "insaat":"Çorlu, Çerkezköy ve Kapaklı hattı sanayi nüfusuna dönük yoğun konut üretimi yapıyor. Süleymanpaşa ve Şarköy tarafında ise deniz manzaralı yatırım projeleri öne çıkıyor; bu ikisi tamamen farklı alıcıya hitap ediyor.",
 "emlak":"Şarköy'de bağ evi ve yazlık, Marmaraereğlisi'nde sahil daireleri, Çorlu hattında ise yatırım amaçlı konut. İstanbul'a mesafenin avantaj olarak anlatılması bölgedeki her ilanın ortak sorunu — havadan konum videosu bunu tek karede çözüyor.",
 "sanayi":"Trakya'nın tekstil ve deri üretim merkezi; ayrıca cam, ambalaj ve gıda tesisleri yoğun. İhracat oranı yüksek olduğu için çok dilli ürün animasyonu talebi fazla.",
 "cografya":"Marmara kıyı şeridi, Ganos Dağları ve Şarköy bağları; uzun sahil hattı havadan takip çekimleri için elverişli.",
 "sektorler":["Tekstil ve deri","Cam","Ambalaj","Gıda","Tarım ve bağcılık"],
 "komsu":["istanbul","edirne","kirklareli"]
},
{
 "slug":"eskisehir","ad":"Eskişehir","ek":"'de","icin":"'e","ekip":"ortak",
 "ilceler":["Odunpazarı","Tepebaşı","Sivrihisar","Çifteler"],
 "insaat":"Eskişehir'de konut talebi büyük ölçüde öğrenci ve genç nüfus tarafından şekilleniyor. Şehrin planlı dokusu ve tramvay hattı, proje tanıtımlarında en çok kullanılan satış argümanı; yerleşim animasyonunda bu bağlantının gösterilmesi işe yarıyor.",
 "emlak":"Porsuk çevresindeki daireler ve Odunpazarı'nın tarihi dokusundaki restore evler iki ayrı portföy oluşturuyor. Kiralık öğrenci konutunda kısa dikey video, satılık dairede ise tam tur videosu tercih ediliyor.",
 "sanayi":"Havacılık, raylı sistemler, beyaz eşya ve seramik Eskişehir'in üretim kimliğini oluşturuyor. Teknik ürünlerin çalışma prensibini anlatan animasyon, özellikle savunma ve havacılık tedarikçilerinde sık isteniyor.",
 "cografya":"Porsuk Çayı, Odunpazarı'nın renkli evleri ve geniş bozkır çevresi; şehir içi düşük irtifa çekimleri için düzenli bir doku.",
 "sektorler":["Havacılık","Raylı sistemler","Beyaz eşya","Seramik","Maden ve bor"],
 "komsu":["ankara","bursa","kutahya","konya"]
},
{
 "slug":"antalya","ad":"Antalya","ek":"'da","icin":"'ya","ekip":"ortak",
 "ilceler":["Muratpaşa","Konyaaltı","Kepez","Lara","Alanya","Manavgat","Side","Kaş","Kemer","Belek"],
 "insaat":"Antalya'da konut üretiminin önemli kısmı yabancı alıcıya dönük. Bu da tanıtım materyalinin baştan çok dilli, sanal tur destekli ve uzaktan karar verdirebilecek nitelikte olmasını gerektiriyor. Lara ve Konyaaltı hattında lüks proje rekabeti oldukça yüksek.",
 "emlak":"Deniz manzarası, havuz, site içi sosyal donatı ve havalimanına mesafe Antalya ilanlarının belirleyici unsurları. Rus, Alman ve Orta Doğu pazarına satış yapan ofisler için altyazılı ve seslendirilmiş video adeta standart hale geldi.",
 "sanayi":"Turizm dışında sera tarımı, gıda işleme ve Antalya OSB'de plastik-makine üretimi bulunuyor. Otel ve turizm tesisleri için tanıtım filmi ise ilin en yoğun prodüksiyon kalemi.",
 "cografya":"Toroslar, falezler, Düden Şelalesi ve uzun sahil şeridi; Türkiye'nin havadan çekim açısından en zengin illerinden biri.",
 "sektorler":["Turizm ve otelcilik","Sera tarımı","Gıda işleme","Plastik ve makine","İnşaat malzemesi"],
 "komsu":["mugla","konya","mersin"]
},
{
 "slug":"mugla","ad":"Muğla","ek":"'da","icin":"'ya","ekip":"ortak",
 "ilceler":["Bodrum","Fethiye","Marmaris","Datça","Milas","Göcek","Dalaman","Ortaca","Seydikemer"],
 "insaat":"Muğla'da inşaat neredeyse tamamen butik ölçekte: az katlı, taş ve ahşap dokulu, arazinin eğimine oturan villa projeleri. Bu yapılar standart render'la anlatılmıyor; arazi eğimi, manzara açısı ve peyzaj modellemesi işin merkezinde.",
 "emlak":"Bodrum ve Göcek'te lüks villa, Datça'da butik ev, Fethiye'de ise hem yerleşim hem yatırım amaçlı konut. Alıcının çoğu şehir dışında ya da yurt dışında; sanal tur burada lüks segmentte satışı kapatan adım.",
 "sanayi":"Milas ve çevresinde madencilik, zeytincilik ve seracılık; kıyı hattında ise yat imalatı ve marina hizmetleri öne çıkıyor. Yat üreticileri için 3D ürün animasyonu, fuar sunumlarında birebir işe yarıyor.",
 "cografya":"Koylar, çam ormanları, Ölüdeniz ve Datça yarımadası; deniz üstü takip çekimleri için Türkiye'nin en etkileyici kıyısı.",
 "sektorler":["Yat imalatı ve marina","Turizm","Zeytincilik","Madencilik","Seracılık"],
 "komsu":["antalya","aydin","denizli","izmir"]
},
{
 "slug":"konya","ad":"Konya","ek":"'da","icin":"'ya","ekip":"ortak",
 "ilceler":["Selçuklu","Meram","Karatay","Ereğli","Akşehir","Beyşehir","Çumra"],
 "insaat":"Konya'da konut üretimi Selçuklu ve Meram hattında yoğunlaşıyor; geniş parseller sayesinde site projelerinde iç peyzaj ve sosyal donatı önemli bir satış argümanı. Yerleşim maketi animasyonu bu geniş yerleşimleri anlatmanın en verimli yolu.",
 "emlak":"Konya alıcısı metrekare, otopark ve site içi güvenlik gibi somut başlıklara odaklanıyor. Video burada duygu satmaktan çok, planı ve kullanım alanını net göstermek için kullanılıyor.",
 "sanayi":"Türkiye'nin tarım makineleri ve otomotiv yedek parça üretiminde en güçlü illerinden biri; ayrıca döküm, kalıp ve savunma sanayi tedarikçileri var. Bu ürünlerin çalışma prensibini anlatan animasyon ihracat görüşmelerinin standart parçası haline geldi.",
 "cografya":"Geniş ova, Mevlana Müzesi, Beyşehir Gölü ve Tuz Gölü çevresi; yüksek irtifa geniş açı planlarında ovanın ölçeği etkileyici duruyor.",
 "sektorler":["Tarım makineleri","Otomotiv yedek parça","Döküm ve kalıp","Savunma sanayi tedarik","Gıda"],
 "komsu":["ankara","antalya","eskisehir","kayseri"]
},
{
 "slug":"gaziantep","ad":"Gaziantep","ek":"'te","icin":"'e","ekip":"ortak",
 "ilceler":["Şahinbey","Şehitkamil","Oğuzeli","Nizip","İslahiye"],
 "insaat":"Şehitkamil hattı Gaziantep'in en hızlı büyüyen konut bölgesi. Sanayinin çektiği nüfus ve genç yaş ortalaması, orta segment site projelerinde sürekli talep yaratıyor; projelerin okul, hastane ve sanayiye mesafesi satışta belirleyici oluyor.",
 "emlak":"Gaziantep'te ticari mülk ve depo portföyü konut kadar hareketli. Depo, fabrika ve dükkân ilanlarında iç hacmin ve yükseklik-manevra alanının videoyla gösterilmesi, yerinde gezme sayısını ciddi biçimde azaltıyor.",
 "sanayi":"Halı, tekstil, gıda ve makine Gaziantep'in dört temel üretim kolu. Dünyaya halı ihraç eden firmalar için ürün dokusunu ve üretim sürecini anlatan animasyon, fuar standının en çok izlenen ekranı oluyor.",
 "cografya":"Zeugma, kale ve tarihi çarşı dokusu; sanayi bölgelerinin geniş ölçeği havadan çekimde etkileyici bir kontrast veriyor.",
 "sektorler":["Halı ve tekstil","Gıda işleme","Makine","Plastik","Ambalaj"],
 "komsu":["hatay","kayseri","adana"]
},
{
 "slug":"kayseri","ad":"Kayseri","ek":"'de","icin":"'ye","ekip":"ortak",
 "ilceler":["Melikgazi","Kocasinan","Talas","Hacılar","İncesu"],
 "insaat":"Talas ve Melikgazi hattında Erciyes manzaralı konut projeleri, Kocasinan'da ise daha yoğun kentsel üretim var. Erciyes'e bakan cephelerin değeri belirgin biçimde yüksek; bu farkı anlatmanın en net yolu 3D cephe ve manzara simülasyonu.",
 "emlak":"Kayseri'de organize sanayi çevresindeki lojistik depo ve fabrika binaları, konut kadar aktif bir portföy oluşturuyor. Yatırımcıya sunumda tesisin ölçeği ve yol bağlantısı havadan çekimle anlatılıyor.",
 "sanayi":"Mobilya, çelik kapı, kablo ve gıda Kayseri'nin ihracat kalemleri. Mobilyada modül ve renk varyantlarını 3D ile göstermek, her varyant için ayrı fotoğraf çekiminden çok daha ucuza geliyor.",
 "cografya":"Erciyes Dağı, Kapadokya'ya uzanan vadiler ve geniş sanayi düzlükleri; kış aylarında Erciyes çekimleri ayrı bir görsel değer taşıyor.",
 "sektorler":["Mobilya","Çelik kapı","Kablo","Gıda","Metal işleme"],
 "komsu":["ankara","konya","gaziantep"]
},
{
 "slug":"denizli","ad":"Denizli","ek":"'de","icin":"'ye","ekip":"ortak",
 "ilceler":["Merkezefendi","Pamukkale","Çivril","Sarayköy","Honaz","Buldan"],
 "insaat":"Denizli'de konut üretimi Pamukkale ve Merkezefendi hattında yoğunlaşıyor. Şehrin sanayiyle büyüyen nüfusu orta segment site projelerine sürekli talep yaratıyor; projelerin OSB'ye ve üniversiteye mesafesi satış argümanının merkezinde.",
 "emlak":"Termal bölge çevresindeki turizm amaçlı mülkler ile şehir içi konut portföyü birbirinden ayrı iki pazar. Termal tesis ve otel satışlarında tanıtım filmi, yatırımcı sunumunun ana materyali oluyor.",
 "sanayi":"Türkiye'nin ev tekstili ve havlu üretiminin merkezi; ayrıca kablo, traverten ve mermer üretimi güçlü. Kumaş dokusunu ve mermer damarını gerçekçi gösteren 3D ürün animasyonu ihracatta belirgin fark yaratıyor.",
 "cografya":"Pamukkale travertenleri, Honaz Dağı ve geniş ova; travertenlerin havadan görüntüsü dünya çapında tanınan bir kare.",
 "sektorler":["Ev tekstili ve havlu","Mermer ve traverten","Kablo","Gıda","Jeotermal enerji"],
 "komsu":["izmir","mugla","aydin","manisa"]
},
{
 "slug":"adana","ad":"Adana","ek":"'da","icin":"'ya","ekip":"ortak",
 "ilceler":["Seyhan","Çukurova","Yüreğir","Sarıçam","Ceyhan"],
 "insaat":"Çukurova ilçesi Adana'nın en hareketli konut bölgesi; yüksek katlı rezidans projeleri şehir siluetini değiştiriyor. Sıcak iklim nedeniyle cephe gölgelemesi ve iç mekân serinliği satış argümanı haline geliyor — bu, 3D görselde ışık simülasyonunu önemli kılıyor.",
 "emlak":"Adana'da tarım arazisi ve depo portföyü konut kadar aktif. Geniş arazilerde sınırların ve sulama altyapısının havadan gösterilmesi alıcının ilk sorusunu tek videoda cevaplıyor.",
 "sanayi":"Gıda işleme, tekstil, plastik ve tarım makineleri öne çıkıyor; Ceyhan tarafında enerji ve lojistik yatırımları var. Tarım makinesi üreticileri için tarlada çalışma animasyonu, fuar öncesi en çok istenen iş.",
 "cografya":"Seyhan Nehri, taş köprü, Çukurova ovası ve Akdeniz kıyısı; ovanın ölçeği yüksek irtifa planlarda etkileyici.",
 "sektorler":["Gıda işleme","Tarım makineleri","Tekstil","Plastik","Enerji ve lojistik"],
 "komsu":["mersin","gaziantep","hatay"]
},
{
 "slug":"mersin","ad":"Mersin","ek":"'de","icin":"'e","ekip":"ortak",
 "ilceler":["Yenişehir","Mezitli","Toroslar","Erdemli","Silifke","Tarsus","Anamur"],
 "insaat":"Mersin'de sahil hattı boyunca uzanan konut projeleri deniz manzarası üzerinden satılıyor. Kaç kattan sonra denizin göründüğü, alıcının en çok sorduğu soru; 3D cephe simülasyonu bu soruyu daire bazında cevaplayabiliyor.",
 "emlak":"Yazlık daire, sahil villası ve limana yakın ticari mülk üç ana portföy. Yurt dışından yatırımcı ilgisi olan bölgelerde çok dilli tanıtım videosu talebi artıyor.",
 "sanayi":"Mersin Limanı ve serbest bölge lojistiğin merkezi; ayrıca gıda işleme, narenciye ve cam üretimi güçlü. Lojistik firmalarının hizmet süreçlerini anlatan animasyon burada sık istenen bir format.",
 "cografya":"Toroslar'ın denize indiği kıyı şeridi, Kızkalesi ve narenciye bahçeleri; kıyı ile dağın kısa mesafede buluşması havadan çekimde güçlü bir geçiş sağlıyor.",
 "sektorler":["Liman ve lojistik","Gıda işleme ve narenciye","Cam","Kimya","Turizm"],
 "komsu":["adana","antalya","konya"]
},
{
 "slug":"samsun","ad":"Samsun","ek":"'da","icin":"'a","ekip":"ortak",
 "ilceler":["İlkadım","Atakum","Canik","Bafra","Çarşamba","Tekkeköy"],
 "insaat":"Atakum hattı Samsun'un en hızlı büyüyen konut bölgesi; deniz cepheli projeler Karadeniz'de nadir bulunan geniş sahil şeridi avantajını kullanıyor. Manzara ve sahil yürüyüş yoluna mesafe, satışın belirleyici iki unsuru.",
 "emlak":"Samsun'da yazlık talebi düşük, sürekli oturuma dönük konut talebi yüksek. Bu yüzden emlak videosunda odak manzaradan çok, dairenin gerçek yaşanabilirliği: ışık alma durumu, oda ölçüleri, ısıtma ve yalıtım.",
 "sanayi":"Tıbbi cihaz, gübre, gıda ve tarım makineleri ilin üretim kolları; Tekkeköy ve Bafra OSB'leri üretimin merkezinde. Tıbbi cihaz üreticileri için kullanım ve hijyen sürecini anlatan animasyon en çok istenen iş.",
 "cografya":"Uzun sahil şeridi, Kızılırmak deltası ve yeşil yamaçlar; deltada kuş cenneti çevresi havadan çekim için ayrı bir zenginlik.",
 "sektorler":["Tıbbi cihaz","Gübre ve kimya","Gıda","Tarım makineleri","Mobilya"],
 "komsu":["ordu","amasya","trabzon"]
},
{
 "slug":"trabzon","ad":"Trabzon","ek":"'da","icin":"'a","ekip":"ortak",
 "ilceler":["Ortahisar","Akçaabat","Yomra","Araklı","Of","Maçka","Sürmene"],
 "insaat":"Trabzon'da eğimli arazi inşaatın hem zorluğu hem satış argümanı. Hangi dairenin denizi gördüğü, kotlar arası farktan dolayı planda anlaşılmıyor — bu yüzden 3D arazi modellemesi ve manzara simülasyonu burada neredeyse zorunlu.",
 "emlak":"Körfez ülkelerinden gelen alıcı ilgisi Trabzon portföyünde belirleyici. Arapça altyazılı ve seslendirilmiş tanıtım videosu, yayla evi ve deniz manzaralı daire satışında doğrudan sonuç veriyor.",
 "sanayi":"Fındık işleme, çay, gıda ve balıkçılık ilin üretim kimliği; ayrıca liman lojistiği güçlü. Fındık ve çay üreticileri için hasattan pakete uzanan süreç videosu, ihracat sunumlarının merkezinde.",
 "cografya":"Sumela Manastırı, Uzungöl, yaylalar ve dik yamaçlarda kurulu şehir dokusu; Türkiye'nin havadan çekimde en dramatik topografyalarından biri.",
 "sektorler":["Fındık işleme","Çay","Gıda ve balıkçılık","Liman lojistiği","Turizm"],
 "komsu":["rize","samsun","gumushane"]
},
{
 "slug":"aydin","ad":"Aydın","ek":"'da","icin":"'a","ekip":"ortak",
 "ilceler":["Efeler","Kuşadası","Didim","Söke","Nazilli","Çine","Germencik"],
 "insaat":"Kuşadası ve Didim hattı Aydın'ın konut üretiminin merkezi; alıcının önemli kısmı yurt dışından ya da İstanbul'dan. Bu yüzden proje tanıtımı baştan uzaktan satış için kurgulanıyor: sanal tur, çok dilli video ve 3D daire tipi çalışması.",
 "emlak":"Deniz manzaralı daire, site içi villa ve zeytinlik içinde ev üç ana portföy. Zeytinlik ve arazi satışında sınır, yol ve su bağlantısının havadan gösterilmesi alıcının ilk sorularını kapatıyor.",
 "sanayi":"İncir, zeytin ve kestane işleme; ayrıca jeotermal enerji ve tekstil üretimi güçlü. Gıda ihracatçıları için ürünün üretim ve paketleme sürecini anlatan video, yurt dışı alıcıya güven veriyor.",
 "cografya":"Ege kıyısı, Büyük Menderes ovası, zeytinlikler ve antik kentler; kıyı ile ova arasındaki geçiş havadan çekimde güzel duruyor.",
 "sektorler":["İncir ve zeytin işleme","Jeotermal enerji","Tekstil","Turizm","Tarım makineleri"],
 "komsu":["izmir","mugla","denizli"]
},
{
 "slug":"manisa","ad":"Manisa","ek":"'da","icin":"'ya","ekip":"ortak",
 "ilceler":["Şehzadeler","Yunusemre","Turgutlu","Salihli","Akhisar","Soma","Alaşehir"],
 "insaat":"Manisa'da konut talebi büyük ölçüde OSB'nin çektiği çalışan nüfustan geliyor. Yunusemre hattındaki projelerde sanayiye ve İzmir yoluna mesafe, satışın en güçlü argümanı; yerleşim animasyonunda bu bağlantının gösterilmesi işe yarıyor.",
 "emlak":"Şehir içi konut portföyünün yanında bağ, zeytinlik ve tarım arazisi satışları oldukça hareketli. Arazi ilanlarında havadan sınır ve topografya gösterimi, alıcının yerinde gezme ihtiyacını azaltıyor.",
 "sanayi":"Manisa OSB Türkiye'nin en büyük elektronik ve beyaz eşya üretim havzalarından biri; ayrıca gıda ve kablo üretimi güçlü. Elektronik ürünlerde iç yapıyı gösteren kesit animasyonu, teknik satışın en etkili aracı.",
 "cografya":"Spil Dağı, Gediz ovası ve üzüm bağları; ovanın geometrik doku düzeni havadan etkileyici bir görüntü veriyor.",
 "sektorler":["Elektronik ve beyaz eşya","Kablo","Gıda ve kuru üzüm","Tarım","Madencilik"],
 "komsu":["izmir","denizli","balikesir"]
},
]

# ---------------------------------------------------------------- birleştirme
from iller_ek0 import EKSTRA as _EKSTRA
import iller_ek1, iller_ek2, iller_ek3, iller_ek4

for _s in SEHIRLER:
    _s.setdefault("kademe", 1)
    if _s["slug"] in _EKSTRA:
        _s.update(_EKSTRA[_s["slug"]])

for _m in (iller_ek1, iller_ek2, iller_ek3, iller_ek4):
    SEHIRLER.extend(_m.EK)

# 17.09.2026 — kademe 2-3 illerine yerel notlar (kademe DEĞİŞMİYOR;
# klip/düğün/işletme sayfası artık veri varlığına bakıyor)
from iller_ek5 import EK5 as _EK5
from iller_ek6 import EK6 as _EK6
from iller_ek7 import EK7 as _EK7
for _s in SEHIRLER:
    for _kaynak in (_EK5, _EK6, _EK7):
        if _s["slug"] in _kaynak:
            for _k, _v in _kaynak[_s["slug"]].items():
                _s.setdefault(_k, _v)

SEHIRLER.sort(key=lambda x: x["ad"])
SEHIR_INDEKS = {s["slug"]: s for s in SEHIRLER}

# kademe listeleri
KADEME1 = [s for s in SEHIRLER if s["kademe"] == 1]   # 7 hizmetin hepsi ayrı sayfa
KADEME2 = [s for s in SEHIRLER if s["kademe"] == 2]   # 3 çekirdek hizmet ayrı sayfa
KADEME3 = [s for s in SEHIRLER if s["kademe"] == 3]   # sadece zengin il sayfası
