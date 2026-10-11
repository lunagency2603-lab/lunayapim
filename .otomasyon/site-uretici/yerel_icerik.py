# -*- coding: utf-8 -*-
"""
YEREL ÖZGÜN İÇERİK — yerinde çekim hizmetlerinin il sayfaları (11.10.2026)

Sahibinin kararı: aynı hizmet olsa bile her il sayfası benzersiz olacak. Bu
dosyadaki her metin o il için ELLE yazıldı; cümle kalıbı doldurulmadı.
Rakamlar resmî kaynaktan, kaynak sayfada yazılı:
  - Konut satışı: TÜİK Veri Portalı, Satış Durumuna ve Satış Şekline Göre
    Satış Sayıları (İl), Eylül 2025–Ağustos 2026 (veri/il_veri/konut_satis_2026-08.csv)
  - Evlenme: TÜİK, İl ve İlçe Evlenme Sayısı 2025 (veri/il_veri/evlenme_2025_ham.txt)
  - Kaba evlenme hızı: TÜİK 2025 (veri/il_veri/kaba_evlenme_2025.csv)
  - Drone: SHGM İHA Sistemleri Talimatı (Temmuz 2026)
Yeni il eklerken: önce gerçek veri, sonra metin. Veri yoksa sayfa yazılmaz.
"""

KAYNAK_KONUT = ('TÜİK Veri Portalı — Satış Durumuna ve Satış Şekline Göre Satış Sayıları (İl), Eylül 2025–Ağustos 2026',
                'https://veriportali.tuik.gov.tr/tr/press/58346')
KAYNAK_EVLENME = ('TÜİK Veri Portalı — İl ve İlçe Evlenme Sayısı, 2025',
                  'https://veriportali.tuik.gov.tr/tr/databrowser/tuik/TR,DF_EVLENME_IL_ILCE,1.0')
KAYNAK_IHA = ('SHGM — İHA Sistemleri Talimatı ve İHA Takip Sistemi',
              'https://ihatakip.shgm.gov.tr/')

SAYFA = {

# ------------------------------------------------------------------ TEKİRDAĞ EMLAK
"tekirdag-emlak-video": dict(
 lede="Tekirdağ'da son bir yılda 42.993 konut el değiştirdi; satılanların %41,7'si sıfır konut. İlanınız bu kalabalıkta İstanbul'a yakınlığı değil, kendi farkını göstermeli.",
 bolum=[
  ("Tekirdağ konut piyasası rakamlarla",
   "<p>TÜİK verisine göre Eylül 2025–Ağustos 2026 arasında Tekirdağ'da <strong>42.993 konut</strong> satıldı; il bu sayıyla Türkiye'de <strong>10. sırada</strong>. Satışların <strong>%41,7'si ilk el</strong>, yani yeni konut. Türkiye ortalamasında bu oran %33,5. Tekirdağ'da müteahhit ilanı ile ikinci el ilanı aynı alıcıya, aynı hafta içinde gösteriliyor.</p>"
   "<p>Ağustos 2026'da satış 3.391 konutta kaldı; bir yıl önceki ağustosa göre %9,4 düşüş. Türkiye genelindeki düşüş %14,7 olduğu için Tekirdağ görece dirençli. Ama alıcı daha uzun düşünüyor, daha çok ilan geziyor. Videonun işi bu uzun karar sürecinde ilanı akılda tutmak.</p>"),
  ("İlçeye göre farklı alıcı, farklı video",
   "<p><strong>Çorlu, Çerkezköy, Kapaklı:</strong> sanayiye yakın, çalışan aileye satılan site daireleri. Bu ilanlarda alıcı önce fabrikaya, okula ve otobüs hattına mesafeyi soruyor. Havadan konum planıyla sitenin OSB ve ana yol bağlantısını gösteriyoruz; içeride oda geçişlerini akıcı tek planla veriyoruz.</p>"
   "<p><strong>Süleymanpaşa ve Kumbağ:</strong> deniz manzaralı daire ve yazlık. Burada satılan şey manzara; balkon açısını gün batımı saatinde çekiyoruz.</p>"
   "<p><strong>Şarköy ve Mürefte:</strong> bağ evi ve müstakil ev. Arsa sınırları, bağın büyüklüğü ve yola cephe drone ile tek karede okunuyor; uzaktan ilanı gezen İstanbullu alıcının ilk sorusu da bu.</p>"),
  ("Çekim günü Tekirdağ'da nasıl planlanıyor",
   "<p>Çorlu Havalimanı'nın çevresi kontrollü hava sahası; Çorlu ve Ergene'deki bazı sitelerde drone uçuşu için ayrı izin gerekiyor. Uçuş noktasını SHGM haritasında kontrol ediyor, izin gereken yerde başvuruyu çekim takvimine göre önceden yapıyoruz.</p>"
   "<p>Kıyıda öğleden sonra rüzgâr artıyor; sahil mülklerinin dış çekimini sabah ya da gün batımına, iç çekimleri öğle saatine koyuyoruz. Aynı gün içinde Çorlu hattından Şarköy'e geçmek yaklaşık bir buçuk saat sürüyor. Bu yüzden portföyü ilçe ilçe gruplayıp mülk başına ulaşım maliyetini düşürüyoruz.</p>"),
 ],
 sss=[
  ("Tekirdağ'da sıfır konut satan müteahhit olarak ne çektirmeliyiz?", "Satışların yaklaşık beşte ikisi ilk el olduğu için rekabet asıl müteahhitler arasında. Bitmiş blok için havadan konum ve örnek daire turu, bitmemiş blok için 3D render ile gerçek arsa görüntüsünü birleştiren bir video öneriyoruz."),
  ("İstanbul'da yaşayan alıcıya Tekirdağ'daki mülkü nasıl anlatırız?", "Uzaktan alıcı yolu, çevreyi ve manzarayı görmek istiyor. Mülke yaklaşan sürüş planı, havadan çevre ve 60–90 saniyelik iç tur bu alıcının gelmeden karar vermesini sağlıyor."),
  ("Çorlu'da drone uçabiliyor mu?", "Havalimanına yakın bölgelerde izin gerekiyor. Mülkün konumuna göre uçuşun serbest bölgede olup olmadığını SHGM haritasından kontrol edip size çekimden önce söylüyoruz."),
  ("Aylık portföy çekimi yapıyor musunuz?", "Evet. Aynı ilçedeki mülkleri aynı güne toplayarak aylık paket kuruyoruz; Çorlu–Çerkezköy hattı ile sahil hattını ayrı günlere ayırıyoruz."),
 ],
 kaynak=[KAYNAK_KONUT, KAYNAK_IHA],
),

# ------------------------------------------------------------------ TEKİRDAĞ KLİP
"tekirdag-klip-cekimi": dict(
 lede="Uçmakdere'nin yamaçları, Şarköy bağları, Kumbağ sahili ve rüzgâr türbinleri. Tekirdağ, İstanbul'dan iki saat uzakta bir klip için dört ayrı dünya sunuyor.",
 bolum=[
  ("Tekirdağ'da klip için mekân",
   "<p><strong>Uçmakdere ve Ganos Dağı yamaçları:</strong> denize dik inen yeşil yamaçlar ve yamaç paraşütü kalkış alanı. Akustik ya da duygusal bir parça için geniş, yalnız bir çerçeve; drone ile yamaçtan denize süzülen tek plan buranın imzası.</p>"
   "<p><strong>Şarköy ve Mürefte bağları:</strong> sıra sıra asmalar ve taş bağ evleri. Hasat dönemi (Eylül sonu–Ekim) altın ışık ve hareketli bir arka plan veriyor; yaz kliplerinde ise sıcak, açık bir renk paleti.</p>"
   "<p><strong>Kumbağ ve Marmaraereğlisi kıyısı:</strong> uzun kumsal ve iskeleler; pop ve yaz parçaları için. Marmaraereğlisi'ndeki Perinthos antik kenti kalıntıları ise taş ve deniz bir arada, daha karanlık bir hikâye için.</p>"
   "<p><strong>Trakya rüzgâr türbinleri:</strong> ovada sıralanan dev kanatlar elektronik ve rap için modern, ölçekli bir arka plan. Türbin sahası özel mülk; çekim için işletme izni alıyoruz.</p>"),
  ("İstanbul'dan gelen ekip için Tekirdağ avantajı",
   "<p>İstanbul'da dış çekim izni, trafik ve kalabalık klip bütçesinin önemli kısmını yiyor. Tekirdağ sahili ve bağları hafta içi neredeyse boş; aynı gün içinde iki farklı mekâna geçmek mümkün. Sanatçı ve ekip sabah İstanbul'dan çıkıp akşam dönebiliyor, konaklama maliyeti doğmuyor.</p>"
   "<p>Bağ ve sahil mekânlarında en verimli düzen: sabah ışığında bağ, öğleden sonra iç mekân ya da gölge, gün batımında sahil. Rüzgâr kıyıda öğleden sonra arttığı için drone planlarını sabaha ve akşama koyuyoruz.</p>"),
  ("Tekirdağ'da klip çekiminde izinler",
   "<p>Antik kent alanında çekim için müze müdürlüğünden, bağlarda mülk sahibinden, sahilde belediyeden izin gerekebiliyor; listeyi mekâna göre baştan çıkarıyoruz. Çorlu Havalimanı çevresinde drone uçuşu kısıtlı; sahil ve bağlar havalimanından uzak olduğu için çoğu zaman serbest bölgede kalıyor, yine de her noktayı SHGM haritasından kontrol ediyoruz.</p>"),
 ],
 sss=[
  ("Tekirdağ'da klip çekmek İstanbul'dan ucuz mu?", "Mekân izni ve kalabalık yönetimi daha kolay olduğu için çoğu zaman evet. Ulaşım gün içinde dönülebilecek mesafede olduğu için konaklama kalemi de çıkmıyor."),
  ("Bağda çekim için hangi ay uygun?", "Asmaların yeşil ve dolu olduğu Haziran–Ekim arası. Hasat dönemi Eylül sonu–Ekim, işçilerin ve kasaların olduğu hareketli bir ortam veriyor; bu da hikâyeye katılabiliyor."),
  ("Uçmakdere'de drone uçurulabiliyor mu?", "Yamaç paraşütü uçuşu olan saatlerde hava trafiği var; çekimi paraşüt uçuşlarının olmadığı saate koyuyoruz ve uçuş noktasını önceden kontrol ediyoruz."),
  ("Sanatçının şehir dışı bir ekiple çalışması sorun olur mu?", "Hayır. Kurgu, renk ve yönetmenlik ekibimiz şarkıyı baştan dinliyor; çekim günü Tekirdağ'daki çözüm ortağımızın ekibiyle birlikte sahadayız."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ TEKİRDAĞ İŞLETME
"tekirdag-isletme-tanitim": dict(
 lede="Tekirdağ'ın iki müşterisi var: hafta içi Çorlu–Çerkezköy sanayisinde çalışanlar, hafta sonu İstanbul'dan gelen ziyaretçi. Tanıtım filminiz hangisine konuştuğunu bilmeli.",
 bolum=[
  ("İki ayrı müşteri, iki ayrı film",
   "<p><strong>Sanayi hattı (Çorlu, Çerkezköy, Kapaklı, Ergene):</strong> Çerkezköy Organize Sanayi Bölgesi ve çevresindeki tekstil, ambalaj, cam ve gıda tesislerinde çalışan nüfus öğle arası, servis saati ve hafta içi akşamı yaşıyor. Bu hatta restoran, kafe, spor salonu ve hizmet işletmesi için içerik hızlı, net ve fiyat odaklı olmalı: menü, kampanya, saat.</p>"
   "<p><strong>Sahil ve bağ hattı (Süleymanpaşa, Şarköy, Marmaraereğlisi):</strong> hafta sonu ve yaz aylarında İstanbul'dan gelen misafir deneyim arıyor. Bağ evi, sahil restoranı, butik otel ve kahvaltı mekânı için içerik yavaş, atmosferik ve mekânı gezdiren cinsten olmalı.</p>"),
  ("Tekirdağ'ın sektörlerine göre içerik",
   "<p>Tekstil ve deri üreticisi için kurumsal film ihracat görüşmesinde kullanılıyor; fabrika içinden üretim hattı ve kalite kontrol, çoğu zaman iki dilde. Gıda üreticisi için ürünün tarladan ya da üretim hattından pakete gelişini kısa dikey videolarla anlatıyoruz. Bağ ve şarap turizmine hizmet veren işletmelerde ise içerik ürünü değil ziyareti satıyor: bağda yürüyüş, sofra, manzara.</p>"
   "<p>Tekirdağ köftesi gibi şehrin bilinen tadını satan restoranlar için en çok işe yarayan şey mutfak: ızgaranın başında birkaç saniyelik yakın plan, sosyal medyada uzun bir tanıtım filminden daha çok paylaşılıyor.</p>"),
  ("Aylık içerik düzeni",
   "<p>Ayda bir çekim gününde dört ila sekiz kısa video ve fotoğraf çıkarıyoruz; yaz sezonu öncesi Mayıs çekimi sahil işletmeleri için en kritik olanı. Sanayi hattındaki işletmeler için kampanya dönemleri (maaş günü, bayram öncesi) takvime göre planlanıyor.</p>"),
 ],
 sss=[
  ("Çerkezköy'deki fabrikamız için tanıtım filmi ne kadar sürer?", "Tek gün çekim yeterli: sabah üretim hattı, öğleden sonra yönetim ve dış çekim. Kurgu ile birlikte teslim 7–10 iş günü."),
  ("Şarköy'deki bağ evimiz için sezon öncesi ne zaman çekmeliyiz?", "Asmalar yeşerdikten sonra, Mayıs sonu–Haziran başı. Böylece içerik sezon başında hazır olur."),
  ("Hem Türkçe hem İngilizce sürüm verebiliyor musunuz?", "Evet; ihracat yapan üreticiler için aynı görüntü üzerine iki dilde altyazı ya da seslendirme veriyoruz."),
  ("Sadece sosyal medya için kısa video yeterli mi?", "Sahil ve restoran işletmeleri için çoğu zaman evet. Sanayi tesisleri için ayrıca 2–3 dakikalık kurumsal film öneriyoruz; teklif görüşmesinde o kullanılıyor."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ ANTALYA DRONE
"antalya-drone-cekimi": dict(
 lede="Antalya Havalimanı'nın kontrollü sahası şehrin büyük kısmını kapsıyor. Otel, villa ya da şantiye için drone çekimi burada önce doğru uçuş noktasını bulmakla başlıyor.",
 bolum=[
  ("Antalya'da uçmadan önce: hava sahası",
   "<p>Antalya Havalimanı Türkiye'nin en yoğun havalimanlarından biri ve Lara, Kundu, Muratpaşa'nın doğusu ile Aksu'nun büyük kısmı kontrollü hava sahasında. Alanya tarafında Gazipaşa-Alanya Havalimanı aynı durumu yaratıyor. Temmuz 2026'da yenilenen SHGM İHA talimatıyla haritada yeşil görünen bölgelerde uçuş için ayrı izin gerekmiyor; kalan yerlerde izin çekim tarihine göre önceden alınıyor.</p>"
   "<p>Bu yüzden Antalya'da drone çekimini keşifte netleştiriyoruz: mülkün konumu, uçuş noktası, izin gerekip gerekmediği. Konyaaltı, Kemer, Kaş ve Manavgat'ın büyük kısmı havalimanlarından uzak; burada uçuş planı daha esnek.</p>"),
  ("Antalya'da drone en çok ne için çekiliyor",
   "<p><strong>Otel ve tatil köyü:</strong> sezon öncesi tanıtım; havuz, plaj ve tesisin denizle ilişkisi tek planda. Tesisin kendi plajında, misafir olmayan sabah saatinde uçuyoruz. Misafir yüzleri kadraja girmiyor, kişisel veri tartışması doğmuyor.</p>"
   "<p><strong>Villa ve yabancıya satış:</strong> Kaş, Kalkan yönü, Konyaaltı ve Döşemealtı'nda havuzlu villa ilanları. Yurt dışındaki alıcı mülkü görmeden karar veriyor; havadan çevre, denize mesafe ve manzara açısı ilanın en çok izlenen kısmı.</p>"
   "<p><strong>Şantiye ilerleme:</strong> Kepez, Döşemealtı ve Aksu'daki konut projelerinde aylık aynı noktadan çekim. Antalya son bir yılda 82.450 konut satışıyla Türkiye'de 4. sırada; proje sayısı fazla, alıcıya ilerlemeyi göstermek satışın parçası.</p>"),
  ("Antalya ışığı ve iklimi",
   "<p>Yaz öğlesinde güneş tepeden vuruyor, deniz düz ve gölgesiz görünüyor; en iyi drone ışığı gün doğumundan sonraki ilk iki saat ve gün batımına yakın. Kıyıda öğleden sonra deniz meltemi artıyor; FPV ve alçak geçişleri sabaha koyuyoruz. Kış aylarında hava açık ve sakin, Toros Dağları karlı; otel ve villa çekimi için düşük sezon aslında en temiz görüntüyü veriyor.</p>"),
 ],
 sss=[
  ("Lara'daki otelimiz için drone izni gerekir mi?", "Lara havalimanına yakın olduğu için büyük olasılıkla evet. Uçuş noktasını kontrol edip izni çekim tarihine göre önceden alıyoruz; izin süresini takvime baştan koyuyoruz."),
  ("Plajda misafirler varken çekim yapılır mı?", "Önermiyoruz. Misafirin yüzü ve kişisel alanı kadraja girmemeli; çekimi plajın boş olduğu sabah saatine planlıyoruz."),
  ("Yabancı alıcı için villa videosu nasıl olmalı?", "Kısa ve bilgi yoğun: havadan konum, denize ve merkeze mesafe, havuz ve manzara, sonra iç tur. Altyazıyı alıcının dilinde veriyoruz."),
  ("Şantiye ilerleme çekimini her ay aynı açıdan alabiliyor musunuz?", "Evet, ilk çekimde uçuş noktalarını ve yüksekliği kaydediyoruz; her ay aynı noktadan çekip ilerlemeyi yan yana gösteriyoruz."),
 ],
 kaynak=[KAYNAK_IHA, KAYNAK_KONUT],
),

# ------------------------------------------------------------------ KAYSERİ DÜĞÜN
"kayseri-dugun-cekimi": dict(
 lede="Kayseri'de 2025'te 9.763 çift evlendi; evlenme hızı Türkiye ortalamasının üzerinde. Erciyes'in karı, Kapadokya'nın vadileri ve şehrin salonları aynı düğünün üç farklı sahnesi olabiliyor.",
 bolum=[
  ("Kayseri'de düğün rakamlarla",
   "<p>TÜİK'e göre Kayseri'de 2025'te <strong>9.763 evlilik</strong> kaydedildi. Bin kişi başına <strong>6,71</strong> evlilikle il, Türkiye ortalamasının (6,43) üzerinde. Evliliklerin yaklaşık yarısı iki merkez ilçede: <strong>Melikgazi'de 3.951</strong>, <strong>Kocasinan'da 2.407</strong>; onları <strong>Talas (1.417)</strong> ve <strong>Develi (473)</strong> izliyor.</p>"
   "<p>Bu yoğunluk şunu demek: düğün sezonunda, özellikle Mayıs–Eylül hafta sonlarında, iyi salonlar ve dış çekim noktaları aynı gün birden fazla çifte ev sahipliği yapıyor. Dış çekim saatini salonun programına göre baştan planlamak gerekiyor.</p>"),
  ("Dış çekim için üç seçenek",
   "<p><strong>Erciyes Dağı:</strong> kış düğünlerinde karlı zirve ve çam ormanı, yaz düğünlerinde serin hava ve yayla ışığı. Şehir merkezinden yaklaşık 25 km; dış çekime yarım gün ayırmak yetiyor.</p>"
   "<p><strong>Talas ve Ali Dağı:</strong> şehre tepeden bakan manzara ve eski taş evler; gün batımında şehrin ışıkları yanarken kısa bir çekim için ideal.</p>"
   "<p><strong>Kapadokya:</strong> Ürgüp ve Göreme yaklaşık bir saat uzakta. Peribacaları ve balonlu sabahlar için çiftler düğünden önceki ya da sonraki güne ayrı bir dış çekim günü koyuyor. Balon kalkışı gün doğumunda olduğu için çekim sabah çok erken başlıyor.</p>"),
  ("Kayseri düğününde çekim akışı",
   "<p>Kayseri'de kına gecesi ile düğün çoğu zaman ayrı günlerde ve kalabalık oluyor. Kına gecesinde ışık loş ve alan dar; ikinci kamerayı sabit tutup ana kamerayla aileyi takip ediyoruz. Düğün günü gelin alma, dış çekim ve salon üç ayrı bölüm. Aynı gün akşam teaser istenirse salonun bitişinden önce ilk 60 saniyelik kurguyu hazırlıyoruz.</p>"),
 ],
 sss=[
  ("Erciyes'te kışın dış çekim yapılabiliyor mu?", "Evet, en etkileyici karlar kışın. Gelin ve damadın üşümemesi için çekimi 30–40 dakikaya sığdırıyor, araç ve sıcak mola noktasını önceden ayarlıyoruz."),
  ("Kapadokya dış çekimi düğünle aynı gün olur mu?", "Mesafe nedeniyle önermiyoruz. Düğünden önceki ya da sonraki güne ayrı bir dış çekim günü daha rahat ve daha iyi ışık veriyor."),
  ("Kına gecesini de çekiyor musunuz?", "Evet. Kına gecesi için ayrı kısa film ya da düğün filminin içinde bir bölüm olarak teslim ediyoruz."),
  ("Sezonda tarih bulmak zor mu?", "Mayıs–Eylül hafta sonları erken doluyor; tarihinizi netleştirir netleştirmez yazmanızı öneriyoruz."),
 ],
 kaynak=[KAYNAK_EVLENME],
),

# ------------------------------------------------------------------ ESKİŞEHİR KLİP
"eskisehir-klip-cekimi": dict(
 lede="Odunpazarı'nın renkli konakları, Porsuk'un kıyısı, Sazova'nın masal şatosu ve üç üniversitenin genç kalabalığı. Eskişehir, bir klibe hem sahne hem seyirci veriyor.",
 bolum=[
  ("Eskişehir'de klip için mekân",
   "<p><strong>Odunpazarı:</strong> Osmanlı dönemi cumbalı, renkli ahşap evler ve dar taş sokaklar. Akustik, nostaljik ya da hikâyeli kliplerde sokak arası yürüyüş planı bu mahallenin imzası. Hemen yanında Odunpazarı Modern Müze'nin ahşap blokları geleneksel dokuya modern bir kontrast ekliyor.</p>"
   "<p><strong>Porsuk Çayı:</strong> şehrin ortasından akan nehir, köprüler ve gondollar. Gece kliplerinde nehir kıyısındaki ışıklar ve kafeler kendiliğinden bir sahne kuruyor.</p>"
   "<p><strong>Sazova Parkı:</strong> masal şatosu, korsan gemisi ve göl. Pop ve çocuk ruhlu parçalarda sinematik ama renkli bir dünya; çekim için park yönetiminden izin alınıyor.</p>"),
  ("Öğrenci şehrinde klip",
   "<p>Anadolu, Eskişehir Osmangazi ve Eskişehir Teknik üniversiteleriyle şehir genç nüfusun yoğun olduğu bir öğrenci kenti. Bu iki şekilde işe yarıyor: kalabalık sahneler için gönüllü figüran bulmak kolay, canlı müzik yapan mekânlar da klip için hazır sahne. Konser ya da bar sahnesi gereken bir parçada mekânın kapalı olduğu öğleden önce çekip gerçek seyirci planlarını akşam ekliyoruz.</p>"),
  ("Eskişehir'de çekim planı ve izinler",
   "<p>Şehirde Hasan Polatkan Havalimanı ve askerî hava üssü bulunduğu için merkezin önemli bir kısmı kontrollü hava sahası. Odunpazarı ve Porsuk kıyısında drone planları için izin gerekebiliyor; uçuş noktasını SHGM haritasından kontrol edip takvime koyuyoruz. Odunpazarı sokakları gündüz turist yoğun; sokak planlarını sabah erken, nehir planlarını akşam alıyoruz.</p>"),
 ],
 sss=[
  ("Odunpazarı'nda çekim için izin gerekiyor mu?", "Sokakta kısa çekimler için çoğu zaman gerekmiyor; geniş ekip, ışık kurulumu ya da drone olacaksa belediyeden ve gerekirse hava sahası için izin alıyoruz."),
  ("Figüranları siz mi buluyorsunuz?", "İsterseniz evet. Öğrenci topluluklarıyla iletişim kurup gönüllü ya da ücretli figüran ayarlayabiliyoruz; kişilerin yazılı onayını alıyoruz."),
  ("Gece klibi için en iyi yer neresi?", "Porsuk kıyısı ve köprüler. Kafelerin ışıkları ve suyun yansıması ek ışık kurulumunu azaltıyor."),
  ("Eskişehir'e ekip ne zaman geliyor?", "Çekim gününü birlikte belirliyoruz; Eskişehir'deki çözüm ortağımızın ekibiyle sahadayız, kurgu ve renk bizde."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ MERSİN DRONE
"mersin-drone-cekimi": dict(
 lede="Türkiye'nin en büyük limanlarından biri, Toroslar'a tırmanan seralar ve Kızkalesi'nden Anamur'a uzanan kıyı. Mersin'de drone çekimi sanayiyi de tatili de havadan anlatıyor.",
 bolum=[
  ("Mersin'de hava sahası ve izin",
   "<p>Ağustos 2024'te açılan Çukurova Uluslararası Havalimanı Tarsus sınırında; Tarsus ve çevresi kontrollü hava sahasında. Mersin limanı ve serbest bölge çevresi de güvenlik nedeniyle kısıtlı alan. Gülnar'daki Akkuyu Nükleer Güç Santrali çevresinde ise uçuş yasak; bu bölgeye yakın kıyı çekimlerinde rotayı santralden uzak kuruyoruz.</p>"
   "<p>Temmuz 2026'da yenilenen SHGM talimatıyla haritada yeşil görünen bölgelerde ayrı izin gerekmiyor. Mezitli, Yenişehir'in sahil kesimi, Erdemli ve Silifke'nin büyük kısmında uçuş planı daha esnek.</p>"),
  ("Mersin'de drone en çok ne için çekiliyor",
   "<p><strong>Konut projeleri:</strong> Mersin son bir yılda 56.385 konut satışıyla Türkiye'de 6. sırada; satışların %35,9'u sıfır konut. Mezitli ve Tece hattında denize bakan yeni siteler için havadan manzara ve şantiye ilerlemesi en çok istenen iş.</p>"
   "<p><strong>Sera ve tarım:</strong> Erdemli ve Silifke'deki örtü altı tarım alanları ve narenciye bahçeleri. Üretici ve ihracatçı firmalar için tesisin büyüklüğünü ve düzenini tek planda gösteren havadan çekim, alıcı ziyaretinin yerini tutuyor.</p>"
   "<p><strong>Yazlık ve turizm:</strong> Kızkalesi'nin denizdeki kalesi, Narlıkuyu ve Cennet-Cehennem obrukları, Anamur kıyısı. Pansiyon ve butik otel tanıtımında denizden yaklaşan bir plan, onlarca fotoğraftan daha fazla şey anlatıyor.</p>"),
  ("Mersin'de ışık ve sıcak",
   "<p>Haziran–Eylül arasında öğle sıcaklığı hem drone bataryasını hem görüntüyü zorluyor; ısı kırılması uzak planları bulanıklaştırıyor. Bu aylarda uçuşu gün doğumundan sonraki iki saate ve gün batımına koyuyoruz. Kış ayları açık ve ılık; Toroslar'ın karlı zirvesiyle denizi aynı karede yakalamak için en iyi dönem Aralık–Şubat.</p>"),
 ],
 sss=[
  ("Tarsus'taki fabrikamız için drone izni gerekir mi?", "Çukurova Havalimanı'na yakınlığa göre değişiyor. Tesisin konumunu haritada kontrol edip izin gerekiyorsa başvuruyu çekim tarihinden önce yapıyoruz."),
  ("Sera alanımızı havadan çekebilir misiniz?", "Evet. Seranın büyüklüğünü ve düzenini gösteren yüksek planla, ürünü gösteren alçak geçişi birlikte çekiyoruz; ihracat sunumlarında kullanılıyor."),
  ("Kızkalesi'nde otelimiz için deniz üstü çekim yapılır mı?", "Yapılır. Denizden kıyıya yaklaşan plan için rüzgârın düşük olduğu sabah saatini seçiyoruz."),
  ("Şantiye ilerlemesini her ay çekiyor musunuz?", "Evet. İlk çekimde noktaları kaydediyor, her ay aynı açıdan çekip ilerlemeyi yan yana veriyoruz."),
 ],
 kaynak=[KAYNAK_IHA, KAYNAK_KONUT],
),

# ------------------------------------------------------------------ ESKİŞEHİR DRONE
"eskisehir-drone-cekimi": dict(
 lede="Eskişehir'in gökyüzü kalabalık: sivil havalimanı, Türkiye'nin en köklü hava üslerinden biri ve Sivrihisar'daki havacılık merkezi. Drone çekimi burada iyi bir uçuş planıyla başlıyor.",
 bolum=[
  ("Eskişehir'de hava sahası",
   "<p>Şehir merkezinin önemli bir kısmı Hasan Polatkan Havalimanı ve askerî hava üssü nedeniyle kontrollü hava sahasında; Tepebaşı ve Odunpazarı'nın merkez mahallelerinde drone uçuşu çoğu zaman izin gerektiriyor. Sivrihisar Havacılık Merkezi çevresinde ise hafta sonları yoğun sportif uçuş trafiği oluyor.</p>"
   "<p>Bu yüzden Eskişehir'de her çekimde önce uçuş noktasını SHGM haritasında kontrol ediyoruz. Organize sanayi bölgesi, şehir dışındaki arsalar ve Porsuk vadisinin kırsal kesimi genellikle daha serbest.</p>"),
  ("Eskişehir'de drone ne için çekiliyor",
   "<p><strong>Sanayi tesisi:</strong> Eskişehir Organize Sanayi Bölgesi'ndeki makine, raylı sistem ve beyaz eşya üreticileri için tesisin büyüklüğünü ve lojistik bağlantısını gösteren havadan tanıtım; yabancı alıcı ziyaretinden önce gönderilen ilk video.</p>"
   "<p><strong>Konut:</strong> Eskişehir'de son bir yılda 26.991 konut satıldı; satışların %36,9'u ilk el, Türkiye ortalamasının (%33,5) üzerinde. Yeni gelişen bölgelerdeki siteler için havadan konum, öğrenci kiralamasına yönelik dairelerde ise kampüse mesafe en çok sorulan şey.</p>"
   "<p><strong>Şehir ve etkinlik:</strong> Porsuk kıyısı, Kent Park ve Sazova çevresindeki açık hava etkinlikleri. Kalabalık üzerinde uçuş kurallara takıldığı için etkinlik çekimini alanın kenarından ve izinli olarak planlıyoruz.</p>"),
  ("Eskişehir iklimi ve çekim zamanı",
   "<p>Eskişehir karasal iklimde; kışın sis ve kırağı sabahları sık. Sisli bir sabah Porsuk vadisinde etkileyici bir plan verebiliyor ama tesis tanıtımı için öğleye doğru açılan havayı bekliyoruz. Bahar ve sonbahar en net görüşü veriyor; yaz öğlesinde ise ışık sert, sabah ve akşamüstü tercih ediliyor.</p>"),
 ],
 sss=[
  ("Odunpazarı'nda drone ile çekim yapılabiliyor mu?", "Merkezdeki konumuna göre izin gerekebiliyor. Noktayı haritada kontrol edip gerekiyorsa izni çekim tarihinden önce alıyoruz."),
  ("OSB'deki fabrikamızı çekmek için ne gerekiyor?", "Tesis yönetiminin onayı ve uçuş noktasının kontrolü. OSB genellikle şehir merkezine göre daha serbest bölgede kalıyor."),
  ("Kışın drone çekimi yapılabilir mi?", "Yapılır; soğukta batarya süresi kısalıyor, bu yüzden yedek batarya sayısını artırıyoruz. Sisli günlerde planı hava açılana göre esnek tutuyoruz."),
  ("Öğrenci yurdu ya da kiralık daire için video çekiyor musunuz?", "Evet. Kampüse mesafeyi havadan gösteren kısa bir konum planı ve odayı gezdiren iç çekim, kiralık ilanlarında en çok işe yarayan ikili."),
 ],
 kaynak=[KAYNAK_IHA, KAYNAK_KONUT],
),

# ------------------------------------------------------------------ ADANA KLİP
"adana-klip-cekimi": dict(
 lede="Taşköprü'nün taş kemerleri, Seyhan kıyısında akşam ışığı, Varda Köprüsü'nün kanyon üstündeki demir iskeleti ve uçsuz bucaksız pamuk tarlaları. Adana bir klibe sıcaklığını kendisi veriyor.",
 bolum=[
  ("Adana'da klip için mekân",
   "<p><strong>Taşköprü ve Seyhan kıyısı:</strong> Roma döneminden kalan taş köprü ve arkasında Sabancı Merkez Camii'nin silueti. Gün batımında nehrin üzerindeki ışık, akustik ve duygusal parçalar için hazır bir sahne.</p>"
   "<p><strong>Varda Köprüsü:</strong> Karaisalı'da, derin bir vadinin üzerinden geçen tarihî demiryolu köprüsü. Ölçeği ve yüksekliği drone ile çekildiğinde etkileyici; köprü hâlâ kullanımda olduğu için çekimi tren saatlerine göre planlıyoruz.</p>"
   "<p><strong>Çukurova ovası:</strong> pamuk ve mısır tarlaları, sulama kanalları, uzun düz yollar. Yolculuk, memleket ve emek temalı parçalarda ovanın genişliği başlı başına bir anlatım.</p>"
   "<p><strong>Kapıkaya Kanyonu ve Yılankale:</strong> Karaisalı'daki kanyon serin ve dar bir dünya; Ceyhan'daki Yılankale ise ovaya hâkim tepede, daha dramatik bir çerçeve.</p>"),
  ("Adana sıcağında çekim düzeni",
   "<p>Adana'da Haziran–Eylül öğlesi dış çekim için hem ekip hem görüntü açısından zor; ışık sert, ısı kırılması uzak planları bozuyor. Dış planları sabah 9'dan önce ve gün batımına yakın saatlere, iç mekân ve stüdyo planlarını öğleye koyuyoruz. Ekim–Mayıs arası ise ova yeşilden altına dönen tonlarıyla en verimli dönem.</p>"
   "<p>Gece klibi için Seyhan kıyısındaki aydınlatılmış köprüler ve kafeler ek ışık kurulumunu azaltıyor. Kalabalık sahneler için şehrin canlı müzik mekânları gün içinde kapalıyken çekip gerçek seyirci planlarını akşam ekliyoruz.</p>"),
  ("İzinler",
   "<p>Taşköprü ve Seyhan kıyısında geniş ekip ya da ışık kurulumu için belediye izni, Yılankale gibi tarihî alanlarda müze müdürlüğü izni gerekiyor. Varda Köprüsü çevresinde demiryolu güvenliği nedeniyle köprüye çıkılmıyor; planları vadiden ve havadan alıyoruz.</p>"),
 ],
 sss=[
  ("Varda Köprüsü'nde klip çekilebilir mi?", "Köprünün üzerine çıkmak güvenlik nedeniyle mümkün değil; vadiden ve izinli drone uçuşuyla köprüyü kadraja alıyoruz. Tren saatleri çekim takvimine göre planlanıyor."),
  ("Yazın Adana'da dış çekim nasıl yapılıyor?", "Sabah erken ve gün batımı saatlerinde. Öğleyi iç mekâna ayırıyoruz; böylece hem ekip hem sanatçı verimli kalıyor."),
  ("Tarla çekimi için izin gerekir mi?", "Tarla özel mülk; sahibinden izin alıyoruz. Ovanın geniş planları çoğu zaman yol kenarından ve havadan alınabiliyor."),
  ("Klibin kurgusu ne kadar sürüyor?", "Çekimden sonra genellikle 7–10 iş günü. Kurgu, renk ve efekt işleri Bursa'daki ekibimizde."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ MUĞLA KLİP
"mugla-klip-cekimi": dict(
 lede="Kayaköy'ün terk edilmiş taş evleri, Saklıkent'in buz gibi kanyonu, Babadağ'dan Ölüdeniz'e süzülen yamaç paraşütleri ve Datça'nın badem bahçeleri. Muğla'da her ilçe ayrı bir klip dünyası.",
 bolum=[
  ("Muğla'da klip için mekân",
   "<p><strong>Kayaköy (Fethiye):</strong> yamaca yayılmış yüzlerce terk edilmiş taş ev ve şapel. Hüzünlü, hikâyeli ya da sinematik bir parça için Türkiye'de benzeri az bulunan bir set; ören yeri olduğu için çekim izni alınarak çalışılıyor.</p>"
   "<p><strong>Saklıkent Kanyonu (Seydikemer):</strong> dar kaya duvarları ve diz boyu soğuk su. Işık kanyona öğle saatlerinde iniyor; çekimi buna göre planlıyoruz.</p>"
   "<p><strong>Babadağ ve Ölüdeniz:</strong> 1.900 metreden denize inen yamaç paraşütleri ve turkuaz lagün. Paraşüt pilotlarıyla birlikte havada çekim, klibe başka hiçbir yerde bulunmayan bir açı ekliyor.</p>"
   "<p><strong>Datça, Akyaka ve Bodrum:</strong> Datça'nın sakin koyları ve taş sokakları, Akyaka'nın Azmak nehri ve ahşap evleri, Bodrum'un beyaz evleri ve gece hayatı. Pop ve yaz parçaları için Bodrum, daha dingin parçalar için Datça ve Akyaka.</p>"),
  ("Turizm sezonu ve çekim takvimi",
   "<p>Muğla'da çekim takvimini sezon belirliyor. Temmuz–Ağustos'ta kıyı kalabalık, konaklama pahalı, mekânlar dolu. Mayıs–Haziran ve Eylül–Ekim aylarında deniz hâlâ sıcak, ışık daha yumuşak, mekânlar daha ulaşılabilir. Kış aylarında Kayaköy ve Saklıkent gibi doğal setler neredeyse boş; dramatik ve serin bir görüntü için bu dönem değerli.</p>"),
  ("Hava sahası ve izinler",
   "<p>İlde Dalaman ve Milas-Bodrum olmak üzere iki havalimanı var; çevrelerinde drone uçuşu izne bağlı. Ölüdeniz'de yamaç paraşütü trafiği nedeniyle drone, paraşüt uçuşlarının olmadığı saatlerde kullanılıyor. Kayaköy ve antik kentlerde müze müdürlüğü, koylarda ise belediye ve gerekirse liman başkanlığı izni gerekiyor.</p>"),
 ],
 sss=[
  ("Kayaköy'de klip çekmek için izin gerekiyor mu?", "Evet, ören yeri olduğu için müze müdürlüğünden çekim izni alınıyor. Başvuruyu çekim tarihinden önce biz yapıyoruz."),
  ("Yamaç paraşütüyle havada çekim yapılabilir mi?", "Evet, lisanslı tandem pilotlarla birlikte. Sanatçı tandem uçuşta, kamera pilotta ya da ikinci bir paraşütte oluyor."),
  ("En uygun çekim ayı hangisi?", "Mayıs–Haziran ve Eylül–Ekim. Deniz sıcak, kalabalık az, ışık yumuşak."),
  ("Teknede çekim yapıyor musunuz?", "Evet; Göcek ve Bodrum koylarında tekne kiralayarak denizden planlar alıyoruz. Teknenin izinleri ve güvenliği kaptanla birlikte planlanıyor."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ KAYSERİ KLİP
"kayseri-klip-cekimi": dict(
 lede="Erciyes'in karlı zirvesi, Kapuzbaşı'nın yan yana dökülen şelaleleri, Sultan Sazlığı'nın kuşları ve Ağırnas'ın yeraltı şehri. Kayseri, Kapadokya'nın gölgesinde kalmış bir klip hazinesi.",
 bolum=[
  ("Kayseri'de klip için mekân",
   "<p><strong>Erciyes Dağı:</strong> kışın kayak pistleri ve kar, yazın volkanik taşlı yamaçlar. Kış klipleri için Türkiye'nin en ulaşılabilir karlı dağlarından biri; şehir merkezine yarım saatlik yolda.</p>"
   "<p><strong>Kapuzbaşı Şelaleleri (Yahyalı):</strong> kayalıktan yan yana dökülen çok sayıda şelale; ilkbahar ve yaz başında su en gürken. Doğa ve özgürlük temalı parçalar için güçlü bir arka plan.</p>"
   "<p><strong>Sultan Sazlığı (Develi–Yahyalı):</strong> kuş göçü döneminde flamingolar ve geniş sazlıklar; sakin, ağır tempolu parçalar için. Koruma alanı olduğu için çekim kurallara uygun planlanıyor.</p>"
   "<p><strong>Ağırnas ve Talas:</strong> Mimar Sinan'ın doğduğu köy Ağırnas'ın taş evleri ve yeraltı şehri, Talas'ın eski Rum konakları. Tarihî ve gizemli bir atmosfer için.</p>"),
  ("Şehir merkezinde",
   "<p>Kayseri Kalesi'nin bazalt surları ve Gevher Nesibe Şifahiyesi gibi Selçuklu yapıları, kara taşın sert dokusuyla rap ve rock kliplerinde güçlü bir doku veriyor. Şehrin modern yüzü için ise yeni bulvarlar ve stadyum çevresi. Merkezde geniş ekip ve ışık kurulumu için belediye izni alıyoruz.</p>"),
  ("Kayseri iklimi ve takvim",
   "<p>Kayseri sert karasal iklimde: kışlar karlı ve soğuk, yazlar kuru ve sıcak. Kar klibi için Aralık–Mart, şelale için Nisan–Haziran, sazlıkta kuş göçü için ilkbahar ve sonbahar en uygun aylar. Kışın dağda çekim günü kısa; ışığı verimli kullanmak için çekim listesini saat saat hazırlıyoruz.</p>"),
 ],
 sss=[
  ("Erciyes'te kışın klip çekimi yapılabilir mi?", "Yapılır; pistlerin dışındaki alanlarda kayak merkezi yönetiminden izin alıyoruz. Soğukta ekipman ve sanatçı için sıcak mola noktası planlanıyor."),
  ("Kapuzbaşı'nda ne zaman çekim yapılmalı?", "Kar suları eridikten sonra, ilkbahar ve yaz başında. Yaz sonuna doğru şelalelerin bir kısmı zayıflıyor."),
  ("Kapadokya'yı da klibe ekleyebilir miyiz?", "Evet; Ürgüp ve Göreme yaklaşık bir saat uzakta. Aynı çekim planına ayrı bir gün olarak ekliyoruz."),
  ("Kayseri'de ekip nereden geliyor?", "Çekim gününde Kayseri'deki çözüm ortağımızın ekibiyle sahadayız; yönetmenlik, kurgu ve renk Bursa'daki ekibimizde."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ İZMİR KLİP
"izmir-klip-cekimi": dict(
 lede="Kemeraltı'nın çarşısı, Asansör'den körfez manzarası, Kordon'da gün batımı, Alaçatı'nın taş sokakları ve Şirince'nin bağları. İzmir'de bir klip şehrin kendisiyle konuşuyor.",
 bolum=[
  ("İzmir'de klip için mekân",
   "<p><strong>Kemeraltı ve Kızlarağası Hanı:</strong> dar çarşı sokakları, tarihî hanların avluları ve kalabalık. Şehir ve sokak hissi veren parçalar için; sabah esnaf açılmadan önce boş, öğlen tam tersi kalabalık iki farklı görüntü.</p>"
   "<p><strong>Karataş'taki Tarihî Asansör ve Dario Moreno Sokağı:</strong> körfeze tepeden bakan teras ve merdivenli sokak. Nostaljik ve romantik parçalar için şehrin en çok tanınan karelerinden.</p>"
   "<p><strong>Kordon ve Alsancak:</strong> deniz kenarında gün batımı ve akşam kalabalığı; gece kliplerinde eski Rum evlerinin sokaklarındaki barlar ve kafeler.</p>"
   "<p><strong>Alaçatı, Urla ve Şirince:</strong> Alaçatı'nın taş evleri ve yel değirmenleri, Urla'nın bağ yolu, Selçuk'a bağlı Şirince'nin dağ köyü dokusu. Şehirden bir saatlik mesafede bambaşka bir set.</p>"),
  ("İzmir'in müzik sahnesiyle çalışmak",
   "<p>İzmir'in canlı müzik mekânları ve bağımsız sahnesi klip için hem sahne hem seyirci sağlıyor. Konser görüntüsü gereken parçalarda mekânın provasını ve gerçek konser akşamını birlikte çekip kurguda birleştiriyoruz. Sokak performansı içeren kliplerde Kordon ve Kemeraltı'nda belediye izniyle çalışılıyor.</p>"),
  ("İzinler ve hava sahası",
   "<p>Adnan Menderes Havalimanı Gaziemir'de, Çiğli'de ise askerî hava üssü var; körfezin önemli bir kısmında drone uçuşu izne bağlı. Kordon ve Karşıyaka sahili planlarını önceden kontrol ediyoruz. Efes gibi ören yerlerinde çekim izni Kültür ve Turizm Bakanlığı'ndan, Kemeraltı'nda geniş ekip için belediyeden alınıyor; başvuruları takvime göre biz yapıyoruz.</p>"),
 ],
 sss=[
  ("Kemeraltı'nda klip çekmek için izin gerekiyor mu?", "Küçük ekip ve el kamerasıyla kısa çekimler çoğu zaman sorun olmuyor; ışık kurulumu, kalabalık ekip ya da trafik düzenlemesi gerekiyorsa belediye izni alıyoruz."),
  ("Kordon'da drone kullanılabilir mi?", "Havalimanı ve hava üssü nedeniyle izne bağlı olabiliyor. Uçuş noktasını SHGM haritasından kontrol edip izni önceden alıyoruz."),
  ("Alaçatı'da yazın çekim yapılır mı?", "Yapılır ama Temmuz–Ağustos çok kalabalık. Sokak planları için sabah erken saatleri ya da Mayıs, Haziran ve Eylül aylarını öneriyoruz."),
  ("Canlı konser görüntüsünü klibe ekleyebilir miyiz?", "Evet. Konser akşamı çok kameralı çekip prova günü aldığımız yakın planlarla birleştiriyoruz."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ BURSA DRONE
"bursa-drone-cekimi": dict(
 lede="Bursa bizim şehrimiz. Uludağ'dan Gölyazı'ya, Gemlik'teki fabrikalardan İnegöl'deki mobilya havzasına kadar uçuş noktalarını keşfe gerek kalmadan tanıyoruz.",
 bolum=[
  ("Bursa'da uçuş: nerede serbest, nerede izin",
   "<p>Bursa'nın sivil havalimanı Yenişehir'de; havalimanının çevresi kontrollü hava sahası. Temmuz 2026'da yenilenen SHGM İHA talimatıyla haritada yeşil görünen bölgelerde ayrı uçuş izni gerekmiyor; askerî alanların ve kritik tesislerin çevresi ise izne bağlı. Kent içinde bu durum mahalleden mahalleye değiştiği için uçuş noktasını her mülk için haritadan ayrıca kontrol ediyoruz.</p>"
   "<p><strong>Uludağ Millî Parkı</strong> ayrı bir başlık: millî park sınırları içinde ticari çekim için Doğa Koruma ve Millî Parklar bölge müdürlüğünden çekim izni gerekiyor. Otel ve kayak merkezi çekimlerinde bu izni tesisle birlikte, çekim tarihinden önce alıyoruz. Cumalıkızık gibi yaşayan köylerde ise uçuşu sabah erken, sokaklar boşken yapıyor, avlulara ve pencerelere kamera çevirmiyoruz.</p>"),
  ("Sanayi şehrinde drone ne işe yarıyor",
   "<p>Bursa otomotivin ve tekstilin merkezi; Nilüfer, Demirtaş ve İnegöl organize sanayi bölgelerinde binlerce üretici var. Bu firmaların en sık istediği şey, yabancı alıcıya ya da fuar standına tesisin <strong>ölçeğini</strong> göstermek: kampüsün büyüklüğü, otoyola ve Gemlik limanına yakınlığı, sevkiyat alanı.</p>"
   "<p>Bunun için tesisin üzerinden yükselen tek bir havadan plan ile kapıdan girip üretim hattını gezen FPV planını birleştiriyoruz. İnegöl'de mobilya üreticileri için aynı çekime showroom turunu da ekliyoruz; fabrika ile satış alanı tek filmde birleşiyor.</p>"),
  ("Şehrin havadan en güçlü kareleri",
   "<p><strong>Gölyazı:</strong> Uluabat Gölü'ne uzanan yarımada köyü; gün batımında göl yüzeyi turuncuya dönüyor. <strong>Uludağ:</strong> kışın kar ve teleferik hattı, yazın sis bandının üzerinden şehre bakış. <strong>Mudanya ve Tirilye:</strong> taş evler ve iskele. <strong>Kent merkezi:</strong> Ulu Cami, Koza Han ve Yeşil Türbe çevresi; tarihî dokuyu havadan çekmek için en sakin saat pazar sabahı.</p>"
   "<p>Merkezimiz Bursa olduğu için hava durumuna göre çekimi aynı sabah kaydırabiliyoruz. Başka illerde yol ve konaklama yüzünden mümkün olmayan bu esneklik, Uludağ'ın değişken havasında doğrudan daha iyi görüntü demek.</p>"),
 ],
 sss=[
  ("Bursa'da drone çekimi için izin gerekiyor mu?", "Kent merkezinin büyük kısmı haritada serbest bölgede. Yenişehir Havalimanı çevresi, askerî alanlar ve Uludağ Millî Parkı izne bağlı; mülkün konumuna bakıp çekimden önce size söylüyoruz."),
  ("Fabrikamızın içinde FPV çekim yapılabilir mi?", "Evet. Hat çalışırken güvenlik kurallarınıza göre rota çiziyor, iş güvenliği sorumlunuzla birlikte uçuyoruz; gerekirse çekimi vardiya arasına koyuyoruz."),
  ("Uludağ'daki otelimizi kışın çekebilir misiniz?", "Evet. Millî park çekim iznini önceden alıyor, kar yağışından sonraki ilk açık sabahı bekliyoruz. Bursa'da olduğumuz için o sabahı yakalamak kolay."),
  ("Şantiyeyi her ay aynı açıdan çekiyor musunuz?", "Evet. İlk uçuşta noktaları ve yüksekliği kaydediyor, her ay aynı yerden çekip ilerlemeyi yan yana gösteriyoruz."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ BURSA KLİP
"bursa-klip-cekimi": dict(
 lede="Ceyrose'nin Kirli klibini Bursa'da çektik. Hanlar bölgesinin taş avluları, Cumalıkızık'ın dar sokakları, Gölyazı'nın göl kıyısı ve eski tekstil fabrikaları aynı şehirde, birbirine yarım saat mesafede.",
 bolum=[
  ("Bursa'da klip için mekân",
   "<p><strong>Hanlar bölgesi ve Kapalıçarşı:</strong> Koza Han'ın avlusu, Emir Han ve çarşının kemerli koridorları. Sıcak ışık ve kalabalık doku; performans klipleri için güçlü bir fon. Han yönetiminden izin alıp çarşının sakin olduğu pazar sabahına ya da kapanış sonrasına çekim koyuyoruz.</p>"
   "<p><strong>Cumalıkızık:</strong> UNESCO Dünya Mirası listesindeki Osmanlı köyü. Renkli cumbalı evler ve taş sokaklar dönem havası istiyor; hafta içi sabah çekimi turist kalabalığından kurtarıyor.</p>"
   "<p><strong>Gölyazı:</strong> Uluabat Gölü'ne uzanan yarımada; tahta kayıklar, leylekler ve gün batımı. Akustik ve duygusal parçalar için.</p>"
   "<p><strong>Eski fabrika yapıları:</strong> Bursa'nın tekstil geçmişinden kalan tuğla binalar ve geniş iç mekânlar; rap, rock ve elektronik için endüstriyel doku. Mülk sahibinden izinle çekiyoruz.</p>"),
  ("Ceyrose — Kirli",
   "<p>Ceyrose'nin “Kirli” şarkısının klibinde yönetmenlik Luna Yapım'daydı; çekim ve kurgu da bizim. Klip 21 Ağustos 2026'da sanatçının YouTube kanalında yayınlandı ve 40 binden fazla izlendi. Bu sayfadaki oynatıcıdan izleyebilirsiniz.</p>"),
  ("Bursa'da klip günü nasıl kuruluyor",
   "<p>Şehir içi mekânlar birbirine yakın olduğu için bir günde iki ya da üç mekân mümkün: sabah Cumalıkızık, öğlen iç mekân, akşam Gölyazı ya da Mudanya sahili. Uludağ ise ayrı bir gün istiyor; yolda hava değişebildiği için yedek tarih koyuyoruz.</p>"
   "<p>İstanbul'dan gelen sanatçı için Bursa, otoyolla yaklaşık iki saat. Kalabalık ve izin süreci İstanbul'a göre çok daha hafif; aynı bütçeyle daha fazla mekân ve daha uzun çekim süresi çıkıyor.</p>"),
 ],
 sss=[
  ("Cumalıkızık'ta klip çekmek için izin gerekiyor mu?", "Köy yaşayan bir yerleşim ve koruma altında. Ticari çekim için önceden bilgi verip izin alıyoruz; çekimi köylünün gündelik düzenini bozmayacak saate koyuyoruz."),
  ("Bursa'da kendi ekibinizle mi çalışıyorsunuz?", "Evet, Bursa merkezimiz. Çeken ve kurgulayan aynı kişiler; mekânları çekimden önce yerinde görebiliyoruz."),
  ("İstanbul'dan gelip tek günde çekim bitirebilir miyiz?", "Evet. Mekânları birbirine yakın seçip sabah başlayan, akşam bitip dönüşe yetişen bir plan kuruyoruz."),
  ("Klip için dikey kesimleri de veriyor musunuz?", "Evet. Çekim günü dikey performans planlarını ayrıca alıyor, ana kliple birlikte teaser ve dikey kesimleri teslim ediyoruz."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ BURSA DÜĞÜN
"bursa-dugun-cekimi": dict(
 lede="Bursa'da 2025'te 20.519 çift evlendi; İstanbul, Ankara ve İzmir'den sonra Türkiye'de dördüncü sırada. Gölyazı'nın gün batımı, Uludağ'ın karı ve Mudanya sahili aynı ilde, yarım saat ile bir saat arasında.",
 bolum=[
  ("Bursa'da düğün rakamlarla",
   "<p>TÜİK'e göre Bursa'da 2025'te <strong>20.519 evlilik</strong> kaydedildi. Bin kişi başına <strong>6,31</strong> evlilikle il, Türkiye ortalamasına (6,43) yakın. Evliliklerin üçte biri tek ilçede: <strong>Osmangazi'de 6.731</strong>. Onu <strong>Nilüfer (3.559)</strong>, <strong>Yıldırım (3.159)</strong>, <strong>İnegöl (2.065)</strong> ve <strong>Gemlik (816)</strong> izliyor.</p>"
   "<p>Bu yoğunluk, sezonda aynı salonun aynı gün birden fazla düğüne ev sahipliği yapması demek. Dış çekimi salonun saatine göre baştan planlıyor, gelin alma ile dış çekim arasındaki yolu hesaba katıyoruz.</p>"),
  ("Dış çekim için Bursa'nın seçenekleri",
   "<p><strong>Gölyazı:</strong> Nilüfer'e bağlı, merkezden yaklaşık 40 dakika. Göl kıyısı, kayıklar ve gün batımı; Bursa'nın en çok tercih edilen dış çekim noktası. Sezonda gün batımı saati kalabalık olduğu için bir saat erken gidiyoruz.</p>"
   "<p><strong>Uludağ ve Sarıalan:</strong> yazın serin yayla ve çam ormanı, kışın kar. Kış düğünlerinde çekimi 30–40 dakikaya sığdırıyor, sıcak mola noktasını önceden ayarlıyoruz.</p>"
   "<p><strong>Soğanlı Botanik Parkı ve Cumalıkızık:</strong> şehir içinde kalmak isteyen çiftler için; biri geniş yeşil alan, diğeri taş sokak ve cumbalı evler. <strong>Mudanya ve Tirilye:</strong> deniz, iskele ve taş evler.</p>"),
  ("İnegöl ve Gemlik'teki düğünler",
   "<p>İnegöl ve Gemlik merkeze yarım saat ile 45 dakika uzaklıkta; 2025'te iki ilçede toplam 2.881 evlilik kaydedildi. Kına gecesi ayrı bir gün yapılıyorsa iki geceyi ayrı kısa filmler olarak ya da tek düğün filminin içinde bölümler olarak teslim ediyoruz.</p>"
   "<p>Bursa'da yaşadığımız için düğünden önce salonu ve dış çekim noktasını çiftle birlikte gezebiliyoruz; ışığın hangi saatte nereye düştüğünü düğün gününden önce biliyoruz.</p>"),
 ],
 sss=[
  ("Gölyazı'da dış çekim için izin gerekiyor mu?", "Kıyı ve sokaklarda kısa dış çekim için genellikle gerekmiyor. Drone kullanacaksak uçuş noktasını kontrol ediyoruz; köy sakinlerini kadraja almamaya özen gösteriyoruz."),
  ("Düğünden önce mekânı birlikte görebilir miyiz?", "Evet. Bursa içindeki düğünlerde salonu ve dış çekim noktasını önceden birlikte gezebiliyoruz."),
  ("Kına gecesini de çekiyor musunuz?", "Evet. Kına gecesini ayrı kısa film ya da düğün filminin bir bölümü olarak teslim ediyoruz."),
  ("Sezonda tarih bulmak zor mu?", "Mayıs–Eylül hafta sonları erken doluyor; tarihinizi netleştirdiğinizde hemen yazmanızı öneriyoruz."),
 ],
 kaynak=[KAYNAK_EVLENME],
),

# ------------------------------------------------------------------ BURSA EMLAK
"bursa-emlak-video": dict(
 lede="Bursa'da son bir yılda 57.169 konut satıldı; il Türkiye'de beşinci sırada. Satılanların yalnızca %29,2'si sıfır konut, yani alıcının önünde çoğunlukla ikinci el ilanlar var ve fark yaratan, ilanın nasıl gösterildiği.",
 bolum=[
  ("Bursa konut piyasası rakamlarla",
   "<p>TÜİK verisine göre Eylül 2025–Ağustos 2026 arasında Bursa'da <strong>57.169 konut</strong> el değiştirdi. Bunların <strong>16.669'u (%29,2) ilk el</strong>; Türkiye ortalaması %33,5. Bursa'da piyasanın ağırlığı ikinci elde.</p>"
   "<p>Ağustos 2026'da satışlar <strong>3.914</strong> konutta kaldı; bir önceki ağustosa (4.938) göre <strong>%20,7 düşüş</strong>. Türkiye genelindeki düşüş %14,7. Alıcı daha seçici ve daha uzun düşünüyor; ilanın ilk on saniyesi, alıcının mülkü kısa listeye alıp almayacağını belirliyor.</p>"),
  ("İlçeye göre farklı mülk, farklı video",
   "<p><strong>Nilüfer:</strong> site içi daireler ve yeni projeler; alıcı sosyal alanı, otoparkı ve okula mesafeyi soruyor. Site ortak alanlarını havadan, daireyi tek akıcı planla gösteriyoruz.</p>"
   "<p><strong>Osmangazi ve Yıldırım:</strong> kentsel dönüşüm daireleri ve merkezde eski stok. Burada satılan konum: Bursaray'a, çarşıya ve hastaneye yakınlık. Videoya kısa bir çevre turu ekliyoruz.</p>"
   "<p><strong>Mudanya:</strong> deniz manzaralı daire ve villa. Balkon açısını gün batımında çekiyor, İstanbul'daki alıcı için denize ve iskeleye mesafeyi havadan veriyoruz.</p>"
   "<p><strong>Gemlik ve İnegöl:</strong> sanayi çalışanına satılan daireler. Fabrikaya ve otoyola mesafe ilk soru; konum planı bu soruyu tek karede cevaplıyor.</p>"),
  ("Bursa'da çekim düzeni",
   "<p>Merkezimiz Bursa olduğu için başka illerdeki yol ve konaklama kalemi burada doğmuyor; aynı gün Nilüfer'de üç daire, öğleden sonra Mudanya'da bir villa çekebiliyoruz. Emlak ofisleri için portföyü ilçe ilçe gruplayıp aylık düzen kuruyoruz. Boş dairelerde 3D mobilya yerleştirme ile odanın nasıl yaşanacağını gösterebiliyoruz.</p>"),
 ],
 sss=[
  ("İkinci el daire için video gerçekten fark eder mi?", "Bursa'da satışların çoğu ikinci el; alıcı aynı mahallede onlarca benzer ilan görüyor. Kısa bir video, ilanı listede ayırıp yerinde gezmeye değer olup olmadığını önceden gösteriyor."),
  ("İstanbul'daki alıcıya Mudanya'daki mülkü nasıl anlatırız?", "Mülke yaklaşan sürüş planı, havadan denize ve iskeleye mesafe, ardından 60–90 saniyelik iç tur. Alıcı gelmeden önce karar verecek kadar bilgi alıyor."),
  ("Aynı gün birden fazla mülk çekebilir misiniz?", "Evet. Portföyü ilçe ilçe grupluyoruz; Nilüfer'deki daireleri sabaha, Mudanya'daki mülkleri gün batımına koyuyoruz."),
  ("Teslim ne kadar sürüyor?", "Tek daire yarım gün sürüyor; kurgu ve renk düzenlemesiyle birlikte teslim genellikle 5–7 iş günü."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ BURSA İŞLETME
"bursa-isletme-tanitim": dict(
 lede="İskender salonundan İnegöl'deki mobilya fabrikasına, Çekirge'deki termal otelden Nilüfer'deki yan sanayi firmasına kadar Bursa'da her işletmenin anlatacağı başka bir hikâye var.",
 bolum=[
  ("Üretici firmalar: fuar ve ihracat için",
   "<p>Bursa'nın ekonomisi otomotiv yan sanayi, tekstil, makine ve İnegöl'de mobilya üzerine kurulu. Bu firmaların tanıtım filmi çoğu zaman bir yabancı alıcıya ya da fuar standına gidiyor. Alıcının görmek istediği şeyler belli: üretim kapasitesi, kalite kontrol, makine parkı ve sevkiyat.</p>"
   "<p>Bu yüzden üretici filmlerinde 2–3 dakikalık ana film, fuar ekranı için sessiz döngü sürüm ve LinkedIn için 30 saniyelik kesim hazırlıyoruz. Altyazıyı alıcının dilinde veriyoruz. Ürün çekimi zor olan makine parçaları için 3D ürün animasyonunu aynı filme ekleyebiliyoruz.</p>"),
  ("Yeme-içme ve turizm: sosyal medya için",
   "<p>Bursa'ya gelen ziyaretçinin listesi belli: İskender, kestane şekeri, Cumalıkızık kahvaltısı, Uludağ ve Çekirge'nin termal otelleri. Bu işletmeler için uzun tanıtım filmi yerine düzenli, kısa ve dikey içerik daha çok iş getiriyor: mutfaktan servis anı, ustanın elinden tek plan, sezon açılışı.</p>"
   "<p>Aylık içerik paketinde ayda 4–12 kısa video çekip kurguluyor, paylaşım takvimine göre teslim ediyoruz. Uludağ'daki oteller için kış sezonu öncesi Ekim–Kasım, termal oteller için yıl boyu düzenli çekim öneriyoruz.</p>"),
  ("Bursa'da çalışmanın farkı",
   "<p>Bursa merkezimiz. Firmanızı çekimden önce yerinde görüp çekim planını sizinle birlikte kuruyoruz. Aylık içerik düzeninde aynı ekip her ay geldiği için çalışanlarınız kameraya alışıyor ve görüntüler her ay daha doğal oluyor.</p>"),
 ],
 sss=[
  ("Fabrikamız için tanıtım filmini kaç dilde hazırlıyorsunuz?", "Ana film tek; altyazı ve seslendirmeyi ihtiyaca göre İngilizce, Almanca ya da başka bir dilde ekliyoruz."),
  ("Restoranımız için aylık içerik paketi nasıl işliyor?", "Pakete göre ayda 4–12 kısa video çekip kurguluyoruz; paylaşım takvimine göre teslim ediyoruz."),
  ("Çekim üretimi durdurur mu?", "Hayır. Hattı durdurmadan, iş güvenliği kurallarınıza göre çekiyoruz; gerekirse yakın planları vardiya arasına koyuyoruz."),
  ("Bursa dışındaki şubemizi de çekebilir misiniz?", "Evet. Bursa'daki çekimle aynı planın içine koyuyor, yol maliyetini baştan yazıyoruz."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ TEKİRDAĞ DRONE
"tekirdag-drone-cekimi": dict(
 lede="Çorlu ile Çerkezköy arasındaki fabrikalar, Barbaros'taki liman, Şarköy'ün bağları ve sırt boyunca dizilen rüzgâr türbinleri. Tekirdağ'da havadan çekilen şey çoğu zaman bir manzaradan çok bir ölçek.",
 bolum=[
  ("Tekirdağ'da uçmadan önce",
   "<p>Çorlu Havalimanı'nın çevresi kontrollü hava sahası; Çorlu ve Ergene'nin bir kısmında uçuş izne bağlı. Yeni SHGM talimatıyla yeşil bölgelerde ayrı izne gerek kalmadı. Süleymanpaşa kıyısı, Şarköy ve Malkara tarafı genellikle daha esnek. Her çekimde uçuş noktasını haritadan kontrol ediyor, izin gerekiyorsa başvuruyu çekim tarihine göre önceden yapıyoruz.</p>"
   "<p>Liman ve enerji tesisleri gibi kritik yapıların çevresinde, tesisin kendi izni olmadan uçmuyoruz. Liman ya da sanayi tesisi çekiminde izin yazısını tesis yönetimiyle birlikte hazırlıyoruz.</p>"),
  ("Sanayi ve lojistik: tesisin ölçeğini göstermek",
   "<p>Çerkezköy, Kapaklı ve Çorlu hattı Trakya'nın en yoğun sanayi bölgesi; tekstil, ambalaj, gıda ve cam üretimi yan yana. Barbaros'taki konteyner limanı ve Çorlu'daki serbest bölge ile birlikte il, İstanbul'un lojistik arka bahçesi. Bu firmaların havadan çekimden beklediği şey tesisin büyüklüğü, otoyola ve limana bağlantısı, sevkiyat alanının düzeni.</p>"
   "<p>Bunun için yüksekten başlayıp tesise inen tek bir açılış planı, ardından yükleme alanında alçak geçiş ve gerekirse üretim hattında FPV planı çekiyoruz. Yabancı alıcıya giden filmde lojistik bağlantıyı harita grafiğiyle destekliyoruz.</p>"),
  ("Şantiye ve yeni konut",
   "<p>TÜİK verisine göre Tekirdağ'da son bir yılda satılan 42.993 konutun %41,7'si ilk el. Bu oran Türkiye ortalamasının (%33,5) epey üzerinde; yani ilde çok sayıda yeni proje var. Müteahhitler için aylık şantiye ilerleme çekimi yapıyoruz: aynı koordinat ve yükseklikten her ay bir kare alıp kaba inşaattan teslime kadar bir zaman çizelgesi oluşturuyoruz.</p>"
   "<p><strong>Kıyı ve bağlar:</strong> Uçmakdere yamaçları, Şarköy ve Mürefte bağları, Kumbağ sahili. Bağ evleri ve butik oteller için en iyi ışık gün batımı; kıyıda öğleden sonra rüzgâr arttığı için uçuşu sabaha ya da akşama koyuyoruz.</p>"),
 ],
 sss=[
  ("Çorlu'daki fabrikamızın üzerinde drone uçabilir mi?", "Havalimanına yakınlık nedeniyle izin gerekebilir. Tesisin konumunu haritadan kontrol edip size çekimden önce söylüyor, gerekiyorsa izni tarihe göre önceden alıyoruz."),
  ("Liman ya da serbest bölgede çekim yapıyor musunuz?", "Tesis yönetiminin izniyle evet. İzin yazısını birlikte hazırlıyor, güvenlik kurallarına göre uçuş rotası çiziyoruz."),
  ("Şantiye ilerleme çekimi ne sıklıkta yapılmalı?", "Satış dönemindeki projelerde ayda bir yeterli. Her ay aynı noktadan çekip alıcıya ve yatırımcıya ilerlemeyi kıyaslamalı gösteriyoruz."),
  ("Bağ evi ya da butik otel için drone videosu nasıl olmalı?", "Bağın genişliği, denize mesafe ve gün batımı. 60–90 saniyelik bir havadan tur ve birkaç iç plan yeterli oluyor."),
 ],
 kaynak=[KAYNAK_IHA, KAYNAK_KONUT],
),

# ------------------------------------------------------------------ KONYA DRONE
"konya-drone-cekimi": dict(
 lede="Konya Türkiye'nin yüzölçümü en büyük ili. Uçsuz bucaksız tarlalar, Selçuklu'dan kalan şehir merkezi ve büyüyen sanayi bölgeleri. Havadan bakınca burada asıl anlatılan şey mesafe ve büyüklük.",
 bolum=[
  ("Konya'da uçmadan önce: hava sahası",
   "<p>Konya Havalimanı askerî bir hava üssüyle ortak kullanılıyor; havalimanının çevresi kontrollü hava sahası ve orada uçuş izne bağlı. Şehir dışına çıktıkça ova açılıyor ve SHGM haritasındaki yeşil bölgeler genişliyor; tarla ve arazi çekimlerinde izin nadiren gerekiyor. Her çekimde uçuş noktasını haritadan ayrı ayrı kontrol ediyoruz.</p>"),
  ("Tarla, arazi ve tarım işletmesi",
   "<p>Konya, tarım arazisi en geniş il. Tarla ve arazi satışlarında alıcının ilk sorusu sınır, yol bağlantısı ve sulama: kuyu, kanal, pivot. Bunu tek bir havadan planla, parsel sınırlarını grafikle çizerek gösteriyoruz. Büyük tarım işletmeleri, seralar ve hayvancılık tesisleri için tesisin ölçeğini ve düzenini yukarıdan anlatıyoruz.</p>"
   "<p>Ova düz olduğu için yüksekten çekilen plan ufka kadar uzanıyor; ölçeği göstermek için tarlanın içinden geçen yol ya da bir traktör gibi bir referans kullanıyoruz. Yazın öğle saatinde ışık sert ve hava titreşimli; çekimi sabah erken ya da akşamüstü yapıyoruz.</p>"),
  ("Sanayi ve konut",
   "<p>Konya tarım makineleri, döküm ve otomotiv yan sanayinde güçlü; organize sanayi bölgelerinde ihracat yapan yüzlerce firma var. Bu firmalar için tesisin ölçeğini havadan, üretim hattını FPV ile gösteriyoruz.</p>"
   "<p>TÜİK verisine göre Konya'da son bir yılda 43.814 konut satıldı; il Türkiye'de 9. sırada. Satışların <strong>%41,6'sı ilk el</strong>; Türkiye ortalaması %33,5. Selçuklu ve Meram'da yeni projeler yoğun; müteahhitlere aylık şantiye ilerleme çekimi ve proje çevresinin havadan anlatımını yapıyoruz.</p>"
   "<p><strong>Şehir ve çevre:</strong> Mevlana Müzesi ve Alaaddin Tepesi çevresi, Sille'nin taş evleri, Beyşehir Gölü. Tarihî alanlarda ibadet saatlerine dikkat ediyor, ziyaretçinin az olduğu sabah saatinde uçuyoruz.</p>"),
 ],
 sss=[
  ("Tarla satışı için drone videosu ne işe yarar?", "Alıcı uzaktaysa tarlayı görmeden karar veremez. Sınırları, yola cepheyi ve sulama düzenini havadan gösteren 60 saniyelik bir video ilk görüşmeyi gereksiz kılabiliyor."),
  ("Konya merkezde drone uçuşu serbest mi?", "Havalimanına yakın kesimlerde izin gerekiyor. Mülkün konumunu haritadan kontrol edip çekimden önce size söylüyoruz."),
  ("Tarım makinesini çalışırken çekebilir misiniz?", "Evet. Hasat ya da ekim sırasında makineyi tarlada, yandan ve yukarıdan takip ederek çekiyoruz; tanıtım ve fuar filmi için en ikna edici görüntü bu."),
  ("Konya'nın ilçelerine de geliyor musunuz?", "Evet. Ereğli, Akşehir, Beyşehir ve Karapınar dahil ilin tamamında çalışıyoruz; birden fazla lokasyonu aynı güne topluyoruz."),
 ],
 kaynak=[KAYNAK_IHA, KAYNAK_KONUT],
),

# ------------------------------------------------------------------ KOCAELİ DRONE
"kocaeli-drone-cekimi": dict(
 lede="Kocaeli'de körfezin bir yanında rafineri, liman ve fabrikalar, öbür yanında Kartepe'nin ormanları var. Havadan çekimde en zor iş, bu kadar kritik tesisin arasında doğru uçuş noktasını bulmak.",
 bolum=[
  ("Kocaeli'de uçmadan önce: kısıtlı bölgeler",
   "<p>Kocaeli, drone için Türkiye'nin en karmaşık illerinden biri. Gebze, Darıca ve Çayırova İstanbul Sabiha Gökçen Havalimanı'nın yakınında; Kartepe'deki Cengiz Topel Havalimanı da kendi kontrollü sahasını yaratıyor. Gölcük'teki askerî alan, Körfez'deki rafineri ve körfez boyunca sıralanan limanlar kritik tesis sayılıyor; çevrelerinde izinsiz uçulmuyor.</p>"
   "<p>SHGM'nin Temmuz 2026 talimatı yeşil bölgelerde uçuşu izinsiz bırakıyor, ama Kocaeli'nin haritasında yeşil alanlar küçük ve dağınık. Bu yüzden çekimi teklif aşamasında netleştiriyoruz: mülkün tam konumu, uçuş noktası, izin gerekip gerekmediği ve süresi.</p>"),
  ("Sanayi ve lojistik",
   "<p>Kocaeli otomotivin, kimyanın, lastik ve boya üretiminin merkezi. Gebze ve Dilovası'ndaki organize sanayi bölgeleri, Körfez ve Derince'deki limanlar, otoyol ile Osmangazi Köprüsü bağlantısı. Firmaların havadan çekimden beklediği şey tesisin limana, otoyola ve İstanbul'a yakınlığını tek karede göstermek.</p>"
   "<p>Gizlilik gereken tesislerde dış çekimi izinli alanla sınırlı tutuyor, üretim sürecini 3D animasyonla anlatmayı öneriyoruz. Kamera ancak izin verilen yere girer; gerisini modelle gösteriyoruz.</p>"),
  ("Konut ve doğa",
   "<p>TÜİK verisine göre Kocaeli'de son bir yılda 47.112 konut satıldı; il Türkiye'de 7. sırada. Satışların %37,8'i ilk el. Ağustos 2026'da satış bir yıl öncesine göre yalnızca %6 düştü; Türkiye genelindeki düşüş %14,7. Başiskele, Kartepe ve Gebze'deki projelerde alıcı körfez manzarasını ve otoyola mesafeyi soruyor; ikisini de havadan gösteriyoruz.</p>"
   "<p><strong>Kartepe:</strong> kışın kayak merkezi, yazın orman ve göl manzarası; otel ve villa çekimlerinde en güçlü kare. <strong>Kerpe ve Kandıra sahili:</strong> Karadeniz kıyısında koylar; yaz tesisleri için. Bursa'dan Kocaeli'ne Osmangazi Köprüsü üzerinden bir saatte geçiyoruz; aynı gün keşif ve çekim mümkün.</p>"),
 ],
 sss=[
  ("Gebze'de drone çekimi yapılabiliyor mu?", "Sabiha Gökçen'e yakınlık nedeniyle Gebze, Darıca ve Çayırova'da çoğu konum izne bağlı olabiliyor. Konumu kontrol edip izin süresini çekim takvimine baştan koyuyoruz."),
  ("Fabrikamız gizlilik istiyor, nasıl çekiyorsunuz?", "Dış çekimi izin verilen alanla sınırlıyor, hassas süreçleri 3D animasyonla anlatıyoruz. Çekilen her kareyi teslimden önce sizin onayınıza sunuyoruz."),
  ("Kartepe'deki otelimizi kışın çekebilir misiniz?", "Evet. Kar yağışından sonraki ilk açık sabahı hedefliyoruz; Bursa'dan bir saatte geldiğimiz için hava durumuna göre tarihi kaydırabiliyoruz."),
  ("Körfez manzaralı dairenin manzarasını nasıl kanıtlarız?", "Dairenin katına denk gelen yükseklikte drone ile balkondan bakış açısını çekiyoruz; bina henüz bitmemiş olsa bile alıcı manzarayı gerçek haliyle görüyor."),
 ],
 kaynak=[KAYNAK_IHA, KAYNAK_KONUT],
),

# ------------------------------------------------------------------ GAZİANTEP KLİP
"gaziantep-klip-cekimi": dict(
 lede="Gaziantep'te 2025'te 17.131 çift evlendi; bin kişide 7,76 ile Türkiye ortalamasının çok üzerinde. Düğünü, faslı ve türküsü canlı bir şehirde müzik hep sahnede. Klip de bu sahneden, bakır çarşısından ve taş sokaklardan besleniyor.",
 bolum=[
  ("Gaziantep'te klip için mekân",
   "<p><strong>Bakırcılar Çarşısı ve hanlar:</strong> çekiç sesi, sıcak metal parıltısı ve kemerli avlular. Ritmik, perküsyonlu parçalar için güçlü bir doku. Esnafın çalışma saatinde çekim yapılıyorsa dükkân sahipleriyle önceden konuşuyor, akışı bozmayan planlar kuruyoruz.</p>"
   "<p><strong>Bey Mahallesi ve eski Antep evleri:</strong> taş avlular, ahşap kapılar, dar sokaklar. Türkü, uzun hava ve dönem havası isteyen klipler için.</p>"
   "<p><strong>Fıstık bahçeleri:</strong> Ağustos–Eylül hasadında yeşil-kırmızı salkımlar ve hareketli bir arka plan. <strong>Rumkale ve Fırat:</strong> Yavuzeli'nde nehre bakan kale kalıntıları; geniş, sinematik planlar için şehirden yaklaşık bir saat uzakta.</p>"
   "<p>2023 depreminden sonra restorasyonu süren tarihî yapılarda çekim yapmıyor, çevresinde de iskele ve çalışma alanını kadraja almamaya dikkat ediyoruz.</p>"),
  ("Yerel sanatçı ve düğün sahnesi",
   "<p>Gaziantep'te evliliklerin büyük kısmı iki merkez ilçede: <strong>Şahinbey'de 8.462</strong>, <strong>Şehitkamil'de 5.653</strong>. Bu yoğunluk düğün orkestraları ve yerel sanatçılar için sürekli bir sahne demek. Bu sanatçıların en çok istediği şey, sahnedeki enerjiyi sosyal medyada taşıyacak kısa ve güçlü bir klip.</p>"
   "<p>Bunun için iki düzen öneriyoruz: tek mekânda performans ağırlıklı, aynı gün çekilip kısa sürede teslim edilen klip; ya da birkaç mekânda hikâyeli, daha uzun bir prodüksiyon. Her ikisinde de dikey kesimleri ayrıca çekiyoruz.</p>"),
  ("Çekim günü Gaziantep'te",
   "<p>Yaz öğleden sonraları çok sıcak; dış çekimi sabaha ve gün batımına, iç mekânı öğlene koyuyoruz. Çarşı ve hanlar akşam erken kapandığı için o planları gündüz bitiriyoruz. Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Bakırcılar Çarşısı'nda klip çekmek için izin gerekiyor mu?", "Çarşı kamuya açık ama ticari çekimde esnafın rızası ve gerekirse belediye izni gerekiyor. Bunu çekimden önce biz ayarlıyoruz."),
  ("Düğün orkestramız için hızlı bir klip çekebilir misiniz?", "Evet. Tek mekânda, performans ağırlıklı bir gün çekip ana klibi ve dikey kesimleri kısa sürede teslim ediyoruz."),
  ("Fıstık bahçesinde ne zaman çekim yapmalıyız?", "En canlı görüntü Ağustos sonu–Eylül hasadında. Bahçe sahibinin izniyle, hasat işini aksatmadan sabah saatlerinde çekiyoruz."),
  ("Türkü ya da uzun hava için nasıl bir klip önerirsiniz?", "Az kesmeli, uzun planlı ve mekânın dokusunu öne çıkaran bir anlatım. Eski Antep evleri ve Rumkale bu tür parçalara çok yakışıyor."),
 ],
 kaynak=[KAYNAK_EVLENME],
),

# ------------------------------------------------------------------ BALIKESİR EMLAK
"balikesir-emlak-video": dict(
 lede="Balıkesir'in iki denizi var: kuzeyde Marmara, güneyde Ege. Ayvalık'taki taş ev, Akçay'daki yazlık, Erdek'teki daire ve Kaz Dağları eteğindeki zeytinlik aynı ilde, ama alıcıları birbirinden çok farklı.",
 bolum=[
  ("Balıkesir konut piyasası rakamlarla",
   "<p>TÜİK verisine göre Eylül 2025–Ağustos 2026 arasında Balıkesir'de <strong>34.462 konut</strong> satıldı; il Türkiye'de 13. sırada. Satışların <strong>%34,5'i ilk el</strong>, Türkiye ortalamasına (%33,5) yakın. Ağustos 2026'da satışlar bir yıl öncesine göre <strong>%15,2</strong> geriledi.</p>"
   "<p>Balıkesir'de satışın önemli bir kısmı yazlık ve ikinci konut; alıcı çoğu zaman İstanbul, Bursa ya da İzmir'de yaşıyor. Mülkü görmeye gelmeden önce videoyla elemek istiyor. Bu yüzden Balıkesir'de ilan videosu, alıcının ilk ziyaretinin yerini tutacak kadar bilgi vermeli.</p>"),
  ("Bölgeye göre farklı video",
   "<p><strong>Edremit Körfezi (Akçay, Altınoluk, Güre, Burhaniye):</strong> denize yakın yazlık ve site daireleri. Alıcının sorusu denize mesafe ve Kaz Dağları manzarası; ikisini havadan tek planda veriyoruz.</p>"
   "<p><strong>Ayvalık ve Cunda:</strong> restore taş evler ve butik oteller. Burada satılan şey doku ve sokak; dar sokaktan eve giren tek akıcı plan ve avlu çekimi öne çıkıyor.</p>"
   "<p><strong>Erdek ve Marmara Adası:</strong> yazlık daire ve müstakil ev; sahile, iskeleye ve feribot bağlantısına yakınlık. <strong>Bandırma ve merkez:</strong> limana ve sanayiye yakın, yıl boyu oturulan daireler; konum ve çevre turu.</p>"
   "<p><strong>Zeytinlik ve arazi:</strong> sınırlar, ağaç sayısı, yola cephe ve eğim. Havadan çekip parsel sınırını grafikle çiziyoruz; alıcının en çok sorduğu soru tek videoda kapanıyor.</p>"),
  ("Çekim düzeni ve drone",
   "<p>Edremit'teki havalimanının ve Balıkesir merkezdeki askerî hava üssünün çevresi kontrollü hava sahası; bu bölgelerdeki mülklerde uçuşu haritadan kontrol edip gerekiyorsa izni önceden alıyoruz. Yazlık mülkleri sezon öncesi, Nisan–Mayıs'ta çekmenizi öneriyoruz: hava açık, sahil boş, ilan yazın en çok bakıldığı haftalara hazır oluyor.</p>"
   "<p>Bandırma Bursa'ya bir buçuk saat; Edremit körfezi ve Ayvalık daha uzak. Portföyü bölgeye göre gruplayıp aynı güne birkaç mülk koyuyoruz.</p>"),
 ],
 sss=[
  ("Yazlığımızı İstanbul'daki alıcıya nasıl anlatırız?", "Mülke yaklaşan sürüş, havadan denize ve sahile mesafe, ardından iç tur. Alıcı mülkü görmeye gelmeden önce karar verecek kadar bilgi alıyor."),
  ("Zeytinlik satışında video gerçekten fark eder mi?", "Evet. Zeytinlikte en çok sorulan soru sınır ve ağaç düzeni; bunu havadan, sınırı çizerek göstermek alıcıyla yapılan ilk görüşmeyi çok kısaltıyor."),
  ("Yazlık ilanı ne zaman çekilmeli?", "Nisan–Mayıs ideal. Hava açık, sahil boş ve ilan, alıcının en çok baktığı yaz başına hazır oluyor."),
  ("Ayvalık'taki taş evi dar sokakta nasıl çekiyorsunuz?", "Sokaktan avluya, avludan odalara giren tek akıcı plan ve gerekirse çatıdan havadan bir açılış. Komşu evleri ve pencereleri kadraja almamaya dikkat ediyoruz."),
 ],
 kaynak=[KAYNAK_KONUT, KAYNAK_IHA],
),

# ------------------------------------------------------------------ SAKARYA DRONE
"sakarya-drone-cekimi": dict(
 lede="Sapanca Gölü, Karasu'nun uzun kumsalı, Acarlar Longozu'nun su ormanı ve Arifiye'deki fabrikalar. Sakarya'da drone hem göl kıyısındaki bungalovu hem bir otomotiv tesisini çekiyor.",
 bolum=[
  ("Sakarya'da havadan ne çekiliyor",
   "<p><strong>Sapanca ve göl kıyısı:</strong> bungalov, otel ve villa. İstanbul'dan gelen hafta sonu misafirinin rezervasyon kararını, göl manzarasının ve tesisin ormanla ilişkisinin havadan görüntüsü veriyor. Sis sabahları ayrı bir güzellik; göl yüzeyinden yükselen sisin üzerinden alınan planlar için sabah erken saatte uçuyoruz.</p>"
   "<p><strong>Karasu ve Acarlar Longozu:</strong> Karadeniz sahili ve Türkiye'nin en büyük longoz ormanlarından biri. Longoz bir koruma alanı; ticari çekim için izni önceden alıyor, kuş ve yaban hayatını rahatsız edecek alçak uçuştan kaçınıyoruz.</p>"),
  ("Sanayi, şantiye ve konut",
   "<p>Sakarya otomotiv ana ve yan sanayinin, beyaz eşya ve makine üretiminin güçlü olduğu bir il. Arifiye ve Hendek çevresindeki tesislerde havadan çekimin işi, kampüsün büyüklüğünü ve otoyolun hemen yanında durduğunu tek karede söylemek.</p>"
   "<p>TÜİK verisine göre Sakarya'da son bir yılda 28.081 konut satıldı; satışların <strong>%39,2'si ilk el</strong>. Dikkat çekici olan şu: Ağustos 2026'da satış bir yıl öncesiyle aynı düzeyde kaldı, Türkiye geneli ise %14,7 düştü. Serdivan, Erenler ve Adapazarı'nda yükselen projelerde satış ofisinin en güçlü malzemesi, binanın her ay biraz daha yükseldiğini gösteren havadan seri.</p>"),
  ("Uçuş ve çekim düzeni",
   "<p>Sakarya'da sivil havalimanı yok; bu, uçuş planını çoğu yerde kolaylaştırıyor. Yine de SHGM haritasında kısıtlı görünen askerî alanlar ve enerji hatları var; Temmuz 2026 talimatına göre yeşil bölge dışındaki her noktada izni çekim tarihinden önce alıyoruz.</p>"
   "<p>Bursa'dan Sakarya'ya yaklaşık iki saatte geliyoruz; Sapanca'daki tesis ile Adapazarı'ndaki şantiyeyi aynı güne koyabiliyoruz. Göl çevresinde rüzgâr genellikle sabah sakin; drone planlarını sabaha, iç çekimleri öğlene planlıyoruz.</p>"),
 ],
 sss=[
  ("Sapanca'daki bungalovumuz için drone videosu nasıl olmalı?", "Göl manzarası, ormanla ilişki ve tesisin içinden kısa bir tur. 30–60 saniyelik dikey ve yatay sürümler rezervasyon sayfası ve sosyal medya için yeterli."),
  ("Acarlar Longozu'nda drone uçurabilir miyiz?", "Koruma alanı olduğu için ticari çekimde izin gerekiyor. İzni önceden alıyor, yaban hayatını rahatsız etmeyecek yükseklikte uçuyoruz."),
  ("Arifiye'deki tesisimizi yabancı alıcıya nasıl gösterebiliriz?", "Kampüsü yukarıdan, otoyol ve İstanbul bağlantısını harita grafiğiyle, üretim hattını FPV ile tek filmde topluyoruz. İngilizce altyazılı sürümü ayrıca veriyoruz."),
  ("1999 depreminden sonra yapılan dönüşüm projelerini de çekiyor musunuz?", "Evet. Eski ve yeni dokunun yan yana durduğu mahallelerde, projenin çevresini değiştirdiğini havadan göstermek alıcıya güven veriyor."),
 ],
 kaynak=[KAYNAK_IHA, KAYNAK_KONUT],
),

# ------------------------------------------------------------------ SAKARYA KLİP
"sakarya-klip-cekimi": dict(
 lede="Sapanca'nın sisli sabahı, Taraklı'nın ahşap konakları, Karasu'nun boş kumsalı ve Sakarya Nehri üzerindeki bin beş yüz yıllık köprü. İstanbul'a bir buçuk saat mesafede, kalabalıktan uzak dört ayrı klip dünyası.",
 bolum=[
  ("Sakarya'da klip için mekân",
   "<p><strong>Sapanca Gölü:</strong> sabah sisi, iskeleler ve göle inen orman. Akustik, duygusal ve yavaş parçalar için. Sisli kareler için çekim gün doğumunda başlıyor; güneş yükseldikçe sis kalkıyor.</p>"
   "<p><strong>Taraklı:</strong> Osmanlı döneminden kalan ahşap konaklarıyla korunmuş küçük bir ilçe. Dönem havası, türkü ve hikâyeli klipler için; sokaklar dar, ekip küçük tutulmalı.</p>"
   "<p><strong>Beşköprü (Justinianus Köprüsü):</strong> Adapazarı'nda, 6. yüzyıldan kalan taş köprü. Taş kemerler ve geniş açı; dramatik, karanlık parçalar için.</p>"
   "<p><strong>Karasu sahili ve Acarlar Longozu:</strong> uzun, boş bir Karadeniz kumsalı ve sular altında kalan orman. Longoz koruma altında; ticari çekim için izin gerekiyor.</p>"),
  ("İstanbul'dan gelen sanatçı için Sakarya",
   "<p>İstanbul'da dış çekimin en büyük maliyeti izin, trafik ve kalabalık. Sakarya'da Sapanca, köprü ve nehir kıyısı birbirine yarım saat mesafede; aynı gün iki ya da üç mekân çekilebiliyor. Ekip için konaklama gerekmiyor; gün ışığı bittiğinde herkes evinde.</p>"
   "<p>Sakarya Üniversitesi çevresindeki genç müzik sahnesi de ayrı bir kaynak: yeni başlayan gruplar için düşük bütçeli, tek mekânlı performans klipleri planlıyoruz. Bursa'dan Sakarya'ya yaklaşık iki saatte geliyoruz.</p>"),
  ("Çekim düzeni",
   "<p>Göl ve nehir kıyısında rüzgâr genellikle sabah sakin; drone ve sis planlarını sabaha, iç mekânı öğlene, köprüyü gün batımına koyuyoruz. Hafta sonları Sapanca kıyısı kalabalık; göl çekimlerini hafta içine planlamayı öneriyoruz.</p>"),
 ],
 sss=[
  ("Sapanca'da sisli plan garantili mi?", "Hayır, sis havaya bağlı. En yüksek ihtimal sonbahar ve ilkbaharda serin, sakin sabahlarda. Yedek tarih koyup hava tahminine göre son günü seçiyoruz."),
  ("Taraklı'da klip çekmek için izin gerekiyor mu?", "Ticari çekim için belediyeye bilgi verip izin alıyoruz. Konaklarda ev sahibinin rızasıyla çekiyoruz."),
  ("Sapanca, Taraklı ve Karasu'yu aynı güne sığdırabilir miyiz?", "Önermiyoruz. Taraklı ve Karasu ters yönlerde; ikisini aynı güne koymak çekim süresini yolda harcatır. Sapanca ile Beşköprü'yü bir güne, Taraklı'yı ayrı bir güne koymak daha verimli."),
  ("Yeni başlayan bir grup için uygun bütçeli klip çekiyor musunuz?", "Evet. Bir prova stüdyosu ya da Sapanca kıyısında tek mekânlı bir performans çekimi; ana klip ve dikey kesimlerle birlikte. Fiyat bandımızın alt ucundan başlıyor."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ SAKARYA İŞLETME
"sakarya-isletme-tanitim": dict(
 lede="Sakarya'da işletmelerin müşterisi iki ayrı kitle: hafta sonu Sapanca'ya gelen İstanbullu misafir ve hafta içi şehirde yaşayan öğrenci ile çalışan. İçerik de ikisine ayrı ayrı konuşmalı.",
 bolum=[
  ("Sapanca ve turizm işletmeleri",
   "<p>Sapanca'daki bungalov, otel, kahvaltı ve göl kıyısı restoranları için rezervasyon kararı çoğu zaman hafta içinde, telefon ekranında veriliyor. Bu yüzden içerik Perşembe–Cuma öncesi yayında olmalı. Göl manzarası, sabah kahvaltısı, şömine ve havuz gibi kısa, dikey planlar bu kitleye en hızlı ulaşan içerik.</p>"
   "<p>Mevsim değiştikçe içerik de değişmeli: yazın göl ve havuz, sonbaharda orman renkleri, kışın şömine ve sıcak içecek. Aylık pakette ayda bir çekim günüyle mevsimi yakalayan bir takvim kuruyoruz.</p>"),
  ("Adapazarı ve Serdivan: şehirde yaşayanlar",
   "<p>Adapazarı'nın ıslama köftesi, Serdivan'daki kafe ve mağazalar, üniversite çevresindeki öğrenci işletmeleri. Bu işletmelerin müşterisi şehirde yaşıyor ve her hafta gelebiliyor; içerik ilk ziyareti değil, tekrar gelmeyi hedeflemeli: yeni menü, kampanya, ustanın elinden tek plan.</p>"
   "<p>Sakarya'da 2025'te 7.451 evlilik kaydedildi; düğün salonu, gelinlik ve organizasyon firmaları için de sezon öncesi tanıtım içeriği hazırlıyoruz.</p>"),
  ("Sanayi firmaları",
   "<p>Otomotiv yan sanayi, makine ve beyaz eşya tedarikçileri için tanıtım filmi farklı bir iş: hedef kitle yabancı alıcı ve fuar ziyaretçisi. Üretim kapasitesini, kalite kontrolü ve sevkiyatı gösteren 2–3 dakikalık ana film ile fuar ekranı için sessiz döngü sürümü hazırlıyoruz.</p>"
   "<p>Bursa'dan Sakarya'ya yaklaşık iki saatte geliyoruz; aylık pakette Sapanca ve Adapazarı'ndaki işletmeleri aynı çekim gününe topluyoruz.</p>"),
 ],
 sss=[
  ("Sapanca'daki bungalovumuz için hangi içerik daha çok rezervasyon getirir?", "Kısa dikey videolar: göl manzarası, kahvaltı, şömine ya da havuz. Hafta sonu kararını hafta içinde veren misafire Perşembe'den önce ulaşmalı."),
  ("Hem Sapanca'daki tesisimizi hem Adapazarı'ndaki şubemizi aynı pakete koyabilir miyiz?", "Evet. İki lokasyonu aynı çekim gününe koyuyor, içerikleri iki ayrı kitleye göre ayrı kurguluyoruz: hafta sonu misafiri ve şehirde yaşayan müşteri."),
  ("Restoranımız için ustanın çekimini mesai sırasında yapabilir misiniz?", "Evet. Servisi aksatmadan, yoğun saatten önce ya da sonra çekiyoruz."),
  ("Düğün salonumuz için ne zaman çekim yapmalıyız?", "Sezon başlamadan, Mart–Nisan'da. Boş salonu ve süslemeyi gün ışığında, bir düğün akşamını da çiftin izniyle çekip ikisini birleştiriyoruz."),
 ],
 kaynak=[KAYNAK_EVLENME],
),

# ------------------------------------------------------------------ MANİSA DRONE
"manisa-drone-cekimi": dict(
 lede="Ağustos sonunda Gediz ovasında serilen kuru üzüm, havadan bakınca kilometrelerce altın rengi bir halı. Manisa'da drone; bağı, Türkiye'nin en büyük sanayi bölgelerinden birini ve volkanik Kula arazisini aynı ilde çekiyor.",
 bolum=[
  ("Bağ, ova ve hasat",
   "<p>Salihli, Alaşehir ve Sarıgöl'ün bağları çekirdeksiz üzümün ana üretim alanı. Hasat sonrası üzümün güneşte kurutulduğu birkaç hafta, havadan çekimin en özel dönemi: ova geometrik desenli bir renk tarlasına dönüşüyor. İhracatçı firmalar, kooperatifler ve bağ evleri için bu dönemi takvime baştan koymanızı öneriyoruz.</p>"
   "<p>Bağ ve tarla satışında da drone işe yarıyor: parselin sınırı, sulama düzeni ve yola cephe tek karede görünüyor. Sınırı grafikle çizip alıcıya gönderilecek kısa bir ilan videosu hazırlıyoruz.</p>"),
  ("Manisa OSB ve sanayi",
   "<p>Manisa Organize Sanayi Bölgesi Türkiye'nin en büyük üretim bölgelerinden biri; beyaz eşya, elektronik, kablo ve gıda tesisleri yan yana. Bu tesislerin havadan tanıtımında ölçek kadar düzen de önemli: hammadde girişi, üretim binaları, depo ve sevkiyat akışı yukarıdan bakınca bir şema gibi okunuyor. Planı bu akışı izleyecek şekilde kuruyoruz.</p>"
   "<p>Soma ve çevresindeki enerji tesisleri, askerî alanlar ve barajlar kritik yapı sayılıyor; çevrelerinde izinsiz uçmuyoruz. SHGM'nin Temmuz 2026 talimatıyla haritada yeşil görünen bölgelerde ise ayrı izin gerekmiyor; Manisa'nın ova ve bağ alanlarının büyük kısmı bu kapsamda.</p>"),
  ("Koruma alanlarında uçuş",
   "<p><strong>Spil Dağı Millî Parkı</strong> ve <strong>Sardes antik kenti</strong> ayrı izin istiyor: millî parkta Doğa Koruma ve Millî Parklar'dan, ören yerinde Kültür ve Turizm Bakanlığı'ndan. <strong>Kula</strong>'nın volkanik arazisi ve peribacaları da korunan bir jeopark alanı. Bu bölgelerde çekim yapacaksak izni tarihe göre önceden başlatıyor, süresini teklifte yazıyoruz.</p>"
   "<p>Manisa'da yaz sıcağı sert; ovada öğle saatinde hava titreşiyor. Uçuşları gün doğumuna ve akşamüstüne koyuyoruz.</p>"),
 ],
 sss=[
  ("Kuru üzüm serme dönemini ne zaman çekmeliyiz?", "Hasadın ardından, genellikle Ağustos sonu ile Eylül arası. Tarih yıla göre değiştiği için bağdan haber geldiğinde birkaç gün içinde çekim yapacak şekilde plan kuruyoruz."),
  ("Manisa OSB'deki tesisimizin üzerinde uçabilir misiniz?", "Çoğu konumda evet. Tesisin koordinatını haritadan kontrol edip çekimden önce size söylüyoruz; tesis içi uçuşu güvenlik birimiyle birlikte planlıyoruz."),
  ("Sardes'te drone çekimi yapılabilir mi?", "Ören yeri olduğu için Bakanlık izni gerekiyor. İzin süreci haftalar sürebiliyor; tarihi buna göre koyuyoruz."),
  ("Bağ satışı için video ne kadar olmalı?", "60 saniye yeterli: havadan sınır ve yol, bağın içinden kısa bir plan, varsa bağ evi."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ BALIKESİR DRONE
"balikesir-drone-cekimi": dict(
 lede="Marmara Adası'nın beyaz mermer ocakları, Bandırma'nın limanı, Edremit Körfezi'nin zeytinlikleri ve Kaz Dağları. Balıkesir'de drone her bölgede başka bir iş çekiyor; ama ilde iki askerî hava üssü olduğu için önce harita.",
 bolum=[
  ("Balıkesir'de uçmadan önce",
   "<p>Balıkesir merkezde ve Bandırma'da askerî hava üsleri, Edremit'te ise Koca Seyit Havalimanı var. Bu üç noktanın çevresi kontrollü hava sahası; şehir merkezinde ve Bandırma'da çoğu konum izne bağlı. Kuş Cenneti Millî Parkı ve Kaz Dağları Millî Parkı ise ayrıca koruma altında: buralarda ticari çekim için Doğa Koruma ve Millî Parklar izni gerekiyor, kuş göç döneminde uçuş yapmıyoruz.</p>"
   "<p>Temmuz 2026'da yenilenen SHGM talimatıyla bu alanların dışındaki yeşil bölgelerde ayrı izin gerekmiyor. Ayvalık, Burhaniye, Erdek ve Gönen çevresi genellikle daha esnek.</p>"),
  ("Bölgeye göre drone işi",
   "<p><strong>Edremit Körfezi ve Ayvalık:</strong> zeytinlik, otel, butik pansiyon ve yazlık siteler. Zeytinyağı üreticileri için hasat döneminde, Kasım–Ocak arasında, bahçeden fabrikaya uzanan bir hikâye çekiyoruz.</p>"
   "<p><strong>Bandırma:</strong> liman, gübre ve kimya tesisleri; Susurluk ve Gönen'de süt ve gıda üretimi. Tesisin limana ve otoyola bağlantısını havadan göstermek ihracat sunumunun ilk karesi.</p>"
   "<p><strong>Marmara Adası:</strong> mermer ocakları havadan bakınca dev beyaz basamaklar gibi görünüyor. Maden ve taş firmaları için ocağın ölçeğini ve iş makinelerinin hareketini çekiyoruz; ocak içi uçuşu işletmenin iş güvenliği kurallarına göre planlıyoruz.</p>"),
  ("Bursa'dan Balıkesir'e",
   "<p>Balıkesir'de kendi ekibimizle çalışıyoruz; Bandırma Bursa'ya yaklaşık bir buçuk saat. Edremit Körfezi ve Ayvalık için çekimi tek güne sığdırmak yerine bir gece konaklayıp gün batımı ve gün doğumunu birlikte almayı öneriyoruz; körfezin en güzel ışığı bu iki saatte.</p>"),
 ],
 sss=[
  ("Bandırma'da drone uçuşu serbest mi?", "Askerî hava üssü nedeniyle şehir merkezinin büyük kısmı izne bağlı. Tesisinizin konumunu kontrol edip izni çekim tarihine göre önceden başlatıyoruz."),
  ("Zeytinyağı markamız için ne zaman çekim yapmalıyız?", "Hasat ve sıkım dönemi, yani Kasım–Ocak. Bahçede toplama, fabrikada sıkım ve şişeleme tek filmde birleşiyor."),
  ("Mermer ocağımızı havadan çekebilir misiniz?", "Evet. Ocağın ölçeğini yüksekten, iş makinelerini ve blok kesimini alçaktan çekiyoruz; patlatma ve yükleme saatlerinde uçmuyoruz."),
  ("Kuş Cenneti çevresinde çekim yapılabilir mi?", "Millî park olduğu için izin gerekiyor ve göç döneminde kuşları rahatsız etmemek için uçmuyoruz. Çevre arazilerde haritaya göre planlıyoruz."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ TRABZON KLİP
"trabzon-klip-cekimi": dict(
 lede="Kemençenin sesi, yaylada kalkan sis, denize dik inen yamaçlar. Trabzon'da klip, şarkının hızına ayak uyduran bir manzara bulmakla başlıyor: horon için hareketli, ağıt için yalnız.",
 bolum=[
  ("Trabzon'da klip için mekân",
   "<p><strong>Uzungöl (Çaykara):</strong> göl, cami ve dik ormanlar; sisli sabahlarda Karadeniz'in en tanınan karelerinden. Yaz ve bayram dönemlerinde çok kalabalık; çekimi hafta içi ve gün doğumuna koyuyoruz.</p>"
   "<p><strong>Sumela Manastırı (Maçka):</strong> kayaya oyulmuş yapı ve Altındere vadisi. Ören yeri olduğu için ticari çekim Bakanlık iznine bağlı; vadinin ve yolun dışarıdan görüntüsü izin süreci olmadan da güçlü bir arka plan.</p>"
   "<p><strong>Zigana ve Hamsiköy yaylaları:</strong> çayırlar, ahşap yayla evleri ve kalkan sis. Kemençe ve tulum eşliğindeki parçalar için en doğal set.</p>"
   "<p><strong>Boztepe ve Ortahisar:</strong> şehre ve limana tepeden bakış; eski mahallenin taş sokakları. Gece kliplerinde şehrin ışıkları.</p>"),
  ("Karadeniz müziği ve klip dili",
   "<p>Horon parçalarında kamera da oynamalı: halkanın içinde dönen el kamerası, yukarıdan halka planı ve ayakların yakın planı. Ağıt ve türkülerde ise tersine, az kesme ve uzun planlar. İki tarzı aynı klipte birleştirmek isteyen sanatçılar için yayla ve köy evi çekimini aynı güne koyuyoruz.</p>"
   "<p>Trabzon'un genç sahnesi Karadeniz müziğini rock ve elektronikle birleştiriyor; bu parçalar için şehir merkezi, liman ve sahil yolu daha modern bir doku veriyor.</p>"),
  ("Hava ve çekim günü",
   "<p>Trabzon'da hava gün içinde birkaç kez değişebiliyor; yaylada sis bir saatte gelip gidiyor. Bu yüzden her yayla çekimine yedek gün koyuyoruz. Havalimanı şehir merkezine çok yakın ve sahil boyunca uzanıyor; merkezde drone uçuşu izne bağlı, yayla ve göl çekimlerinde ise çoğu zaman serbest bölgedeyiz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Uzungöl'de klip çekmek için izin gerekiyor mu?", "Göl kıyısında kısa çekim için genellikle gerekmiyor; drone ve kalabalık ekip için belediyeye bilgi veriyoruz. Kalabalıktan kaçmak için hafta içi sabahı öneriyoruz."),
  ("Sumela'da klip çekilebilir mi?", "Ören yeri olduğu için Bakanlık izni gerekiyor ve süreç uzun. Çoğu zaman vadiyi ve manastırı dışarıdan çekmek klip için yeterli oluyor."),
  ("Horon sahnesi için kaç kişilik ekip gerekiyor?", "Halkanın büyüklüğüne göre değişiyor. Oyuncuları yerel horon ekiplerinden buluyor, provayı çekimden bir gün önce yapıyoruz."),
  ("Yaylada hava bozarsa ne oluyor?", "Her yayla çekimine yedek gün koyuyoruz; sis ve yağmur bazen tam aradığımız görüntüyü de veriyor, karar o sabah yerinde veriliyor."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ DENİZLİ KLİP
"denizli-klip-cekimi": dict(
 lede="Pamukkale'nin beyaz travertenleri dünyanın en tanınan doğal sahnelerinden biri. Ama Denizli'de klip için sadece Pamukkale yok: Buldan'ın dokuma tezgâhları, Çal'ın bağları ve şehrin tekstil fabrikaları da bekliyor.",
 bolum=[
  ("Pamukkale ve Hierapolis",
   "<p>Travertenler ve Hierapolis antik kenti UNESCO Dünya Mirası listesinde ve ören yeri olarak korunuyor. Ticari klip çekimi Kültür ve Turizm Bakanlığı iznine bağlı; travertenlerde ayakkabıyla yürümek yasak, ekipman sınırlı. İzin süreci haftalar sürebildiği için Pamukkale'li bir klibin takvimini en baştan buna göre kuruyoruz.</p>"
   "<p>İzin beklemeden güçlü bir alternatif <strong>Karahayıt</strong>: kırmızı travertenler ve sıcak su kaynakları. Gün batımında travertenlerin rengi turuncuya dönüyor; Pamukkale'nin beyaz sabah ışığından bambaşka bir duygu.</p>"),
  ("Denizli'nin diğer setleri",
   "<p><strong>Buldan:</strong> el dokuma tezgâhları ve eski evler. Ritmik, zanaat temalı ya da nostaljik parçalar için; tezgâh sesi müziğin içine bile girebiliyor.</p>"
   "<p><strong>Çal ve bağlar:</strong> Denizli'nin bağ bölgesi; hasat döneminde altın ışık ve geniş açık alan.</p>"
   "<p><strong>Tekstil fabrikaları:</strong> Denizli havlu ve bornozun merkezi. Dokuma makinelerinin sıra sıra dizildiği salonlar, elektronik ve rap için güçlü bir endüstriyel doku. Fabrika sahibiyle çekimi üretimi aksatmayacak saate koyuyoruz.</p>"
   "<p><strong>Laodikeia:</strong> şehre çok yakın, kazıları süren büyük bir antik kent; Pamukkale'ye göre daha sakin. Burada da ören yeri izni gerekiyor.</p>"),
  ("Çekim günü Denizli'de",
   "<p>Denizli yazın çok sıcak; travertenlerde öğle ışığı beyaz yüzeyden sert biçimde yansıyor. Dış çekimleri gün doğumuna ve gün batımına, fabrika ve iç mekânı öğlene koyuyoruz. Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Pamukkale'de klip çekmek için ne kadar önce başvurmalıyız?", "En az bir ay önce. Bakanlık izni gerekiyor; başvuruyu biz hazırlıyor, takvimi izne göre kuruyoruz."),
  ("İzin çıkmazsa Pamukkale'ye benzer bir mekân var mı?", "Karahayıt'ın kırmızı travertenleri yakın ve daha esnek. Farklı bir renk ama aynı doğal doku."),
  ("Fabrikada klip çekmek için ne gerekiyor?", "Fabrika sahibinin izni ve iş güvenliği kurallarına uygun bir plan. Makinelerin çalışırken görünmesi için üretimi durdurmadan, güvenli mesafeden çekiyoruz."),
  ("Buldan'da dokuma tezgâhlarını çekebilir miyiz?", "Evet. Atölye sahibiyle önceden konuşup tezgâh başında çalışan ustayla birlikte, işini aksatmadan çekiyoruz."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ ANKARA KLİP
"ankara-klip-cekimi": dict(
 lede="Ankara'da klip çekmenin iki yüzü var: Türkiye'nin en köklü rock ve bağımsız müzik sahnelerinden biri ve drone uçurmanın en zor olduğu başkent hava sahası.",
 bolum=[
  ("Ankara sahnesi",
   "<p>Kızılay, Sakarya Caddesi ve Tunalı Hilmi çevresindeki mekânlar uzun yıllardır yeni grup çıkaran bir sahne. Bu grupların klipleri çoğu zaman düşük bütçeli ama güçlü fikirli: tek mekân, iyi ışık ve doğru kurgu. Bunun için prova stüdyosu, sahne ya da bodrum kat mekânında performans ağırlıklı bir gün planlıyoruz.</p>"
   "<p>Ankara'nın geniş bulvarları, 20. yüzyıldan kalan kamu binaları ve beton yapılar, kliplerde başka bir şehirde bulunmayan sert ve ölçekli bir görsel dil veriyor.</p>"),
  ("Mekânlar ve izinler",
   "<p><strong>Hamamönü ve Ankara Kalesi:</strong> restore edilmiş ahşap evler, taş sokaklar ve kaleden şehre bakış. Dönem havası ve türküler için.</p>"
   "<p><strong>Eymir ve Mogan gölleri:</strong> şehre yakın su ve sazlık; sakin, açık hava parçaları için. Eymir bir üniversite arazisinde; çekim için izin alıyoruz.</p>"
   "<p><strong>Beypazarı:</strong> yaklaşık bir buçuk saat mesafede, Osmanlı evleriyle korunmuş bir ilçe. Şehirden uzaklaşan, tarihî doku isteyen klipler için.</p>"
   "<p>Bakanlıklar, Meclis, Anıtkabir ve askerî alanların çevresinde çekim ve drone uçuşu sıkı kurallara bağlı. Esenboğa, Etimesgut ve diğer hava üsleri de şehrin büyük kısmını kontrollü hava sahasına sokuyor. Bu yüzden Ankara'da drone planlarını şehir dışına, göl kıyısına ya da Beypazarı'na koyuyor, şehir içinde yerden çekiyoruz.</p>"),
  ("Çekim düzeni",
   "<p>Ankara kışın soğuk ve gri, yazın kuru ve aydınlık. Gri kış ışığı soğuk tonlu bir rock klibi için avantaj bile olabiliyor; renk düzenlemesini parçanın duygusuna göre kuruyoruz. Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde Ankara'daki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Ankara şehir merkezinde drone ile klip çekebilir miyiz?", "Çoğu yerde hayır ya da uzun izin süreci gerekiyor. Havadan planları şehir dışında, göl kıyısında ya da Beypazarı'nda çekmeyi öneriyoruz."),
  ("Yeni bir grubuz, bütçemiz düşük. Ne önerirsiniz?", "Tek mekânda, performans ağırlıklı bir gün. Ana klip ve sosyal medya için dikey kesimlerle birlikte; fiyat bandımızın alt ucundan başlıyor."),
  ("Hamamönü'nde çekim için izin gerekiyor mu?", "Kamuya açık sokaklarda kısa çekim için genellikle gerekmiyor; kalabalık ekip ve ekipman için belediyeye bilgi veriyoruz. Kafe ve evlerin içinde işletme sahibinin izniyle çekiyoruz."),
  ("Konser kaydını klibe çevirebilir misiniz?", "Evet. Konser akşamı çok kameralı çekip ayrı bir günde aldığımız yakın planlarla birleştiriyoruz."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ MANİSA DÜĞÜN
"manisa-dugun-cekimi": dict(
 lede="Manisa'da 2025'te 9.522 çift evlendi. Düğünler tek bir merkezde değil, ilin dört bir yanına dağılmış durumda: Turgutlu'dan Akhisar'a, Salihli'den Soma'ya her ilçenin kendi salonu, kendi düzeni var.",
 bolum=[
  ("Manisa'da düğün rakamlarla",
   "<p>TÜİK'e göre 2025'te Manisa'da <strong>9.522 evlilik</strong> kaydedildi; bin kişide <strong>6,45</strong> ile il Türkiye ortalamasında (6,43). Dikkat çeken şey dağılım: iki merkez ilçe <strong>Yunusemre (1.432)</strong> ve <strong>Şehzadeler (1.272)</strong> kadar <strong>Turgutlu (1.279)</strong>, <strong>Akhisar (1.179)</strong> ve <strong>Salihli (1.122)</strong> de kalabalık. Alaşehir (716) ve Soma (701) onları izliyor.</p>"
   "<p>Yani Manisa'da düğün çekimi çoğu zaman ilçede. İlçeler arası mesafe bir saati bulabildiği için gelin alma, dış çekim ve salonu aynı güne yerleştirirken yolu baştan hesaplıyoruz.</p>"),
  ("Dış çekim için Manisa'nın seçenekleri",
   "<p><strong>Bağlar:</strong> Salihli ve Alaşehir'in üzüm bağları; yaz sonu hasada yakın dönemde yeşil-altın tonlar. Bağ sahibinin izniyle, sıraların arasında geniş planlar.</p>"
   "<p><strong>Spil Dağı:</strong> şehre tepeden bakan millî park; serin hava ve çam ormanı. Millî park sınırlarında drone için izin gerekiyor.</p>"
   "<p><strong>Kula:</strong> volkanik arazi, peribacaları ve eski Kula evleri. Bambaşka bir doku isteyen çiftler için ayrı bir dış çekim günü.</p>"
   "<p><strong>Şehir merkezi:</strong> Muradiye ve Sultan camileri çevresi ile tarihî sokaklar; ibadet saatlerine dikkat ederek kısa çekim.</p>"),
  ("İzmir'e yakınlık",
   "<p>Manisa merkezi İzmir'e yaklaşık 40 dakika. Bazı çiftler dış çekimi İzmir'in sahilinde, düğünü Manisa'da yapıyor; bazı aileler de davetlilerin bir kısmını İzmir'den ağırlıyor. İki şehri aynı güne koyan programlarda zamanlamayı trafiğe göre kuruyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Turgutlu ya da Akhisar'daki düğünümüze geliyor musunuz?", "Evet, ilin tüm ilçelerine geliyoruz. Gelin evi, dış çekim ve salon arasındaki mesafeyi baştan hesaplayıp günü buna göre planlıyoruz."),
  ("Bağda dış çekim için en iyi dönem ne zaman?", "Yaz sonu, hasattan önce. Asmalar dolu, ışık yumuşak; bağ sahibinin iznini önceden alıyoruz."),
  ("Kula'da dış çekim düğünle aynı gün olur mu?", "Mesafe nedeniyle önermiyoruz. Düğünden önceki ya da sonraki güne ayrı bir dış çekim günü daha rahat."),
  ("Kına gecesini de çekiyor musunuz?", "Evet. Ayrı kısa film ya da düğün filminin bir bölümü olarak teslim ediyoruz."),
 ],
 kaynak=[KAYNAK_EVLENME],
),

# ------------------------------------------------------------------ SAMSUN DÜĞÜN
"samsun-dugun-cekimi": dict(
 lede="Samsun'da 2025'te 8.588 çift evlendi. Karadeniz'in en büyük şehrinde düğün; sahilde gün batımı, Kızılırmak Deltası'nın sazlıkları ve horonla biten bir salon gecesi demek.",
 bolum=[
  ("Samsun'da düğün rakamlarla",
   "<p>TÜİK'e göre Samsun'da 2025'te <strong>8.588 evlilik</strong> kaydedildi; bin kişide 6,19. Evliliklerin önemli kısmı merkezde: <strong>İlkadım (1.652)</strong>, <strong>Atakum (1.481)</strong> ve <strong>Canik (922)</strong>. Ama <strong>Çarşamba (964)</strong> ve <strong>Bafra (946)</strong> gibi ova ilçeleri de neredeyse merkez kadar kalabalık; bu ilçelerdeki düğünler çoğu zaman daha büyük ve daha geleneksel.</p>"),
  ("Dış çekim için Samsun'un seçenekleri",
   "<p><strong>Atakum sahili ve Amisos Tepesi:</strong> sahil yolu, iskeleler ve teleferikle çıkılan tepeden şehre bakış. Gün batımı denize düştüğü için akşam çekimi Samsun'un en güçlü kartı.</p>"
   "<p><strong>Kızılırmak Deltası (Bafra):</strong> sazlıklar, göller ve vahşi atlar. Doğal ve geniş planlar için; koruma alanı olduğu için drone ve araçla girişte kurallara uyuyoruz.</p>"
   "<p><strong>Bandırma Vapuru Müzesi ve sahil:</strong> şehir merkezinde, tarihî vapur ve deniz kıyısı. Kısa ve kolay bir dış çekim; düğünle aynı güne rahat sığıyor.</p>"
   "<p><strong>Şahinkaya Kanyonu (Vezirköprü):</strong> tekneyle gezilen yeşil kanyon. Uzak ama çok farklı bir set; ayrı bir dış çekim günü öneriyoruz.</p>"),
  ("Samsun düğününün akışı",
   "<p>Karadeniz düğününde horon gecenin doruk noktası; halka büyüdükçe kamera da içine giriyor. Salonda bir kamerayı yüksekte sabit tutup halkayı yukarıdan, ikinci kamerayla içeriden çekiyoruz. Kemençe ya da davul-zurna canlı çalınıyorsa sesi ayrıca kaydediyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Atakum sahilinde dış çekim için en iyi saat ne?", "Gün batımından önceki bir saat. Yazın sahil kalabalık olduğu için çekim noktasını önceden seçiyoruz."),
  ("Kızılırmak Deltası'nda çekim yapılabilir mi?", "Evet, kurallara uyarak. Koruma alanı olduğu için drone ve araç girişini önceden kontrol ediyoruz; kuşları ve atları rahatsız etmeden çekiyoruz."),
  ("Bafra ya da Çarşamba'daki düğünümüze geliyor musunuz?", "Evet. Gelin alma, dış çekim ve salonun ilçeler arası mesafesini baştan planlıyoruz."),
  ("Horonu nasıl çekiyorsunuz?", "Biri yukarıdan sabit, biri halkanın içinden iki kamerayla. Canlı müziği ayrıca kaydedip kurguda öne çıkarıyoruz."),
 ],
 kaynak=[KAYNAK_EVLENME],
),

# ------------------------------------------------------------------ KAYSERİ EMLAK
"kayseri-emlak-video": dict(
 lede="Kayseri'de Ağustos 2026'da konut satışı bir yıl öncesine göre %23,9 düştü; Türkiye geneli %14,7. Alıcı azaldığında ilanın kalitesi daha çok fark ediyor.",
 bolum=[
  ("Kayseri konut piyasası rakamlarla",
   "<p>TÜİK verisine göre Eylül 2025–Ağustos 2026 arasında Kayseri'de <strong>34.847 konut</strong> satıldı; il Türkiye'de 12. sırada. Satışların <strong>%29,1'i ilk el</strong>, Türkiye ortalamasının (%33,5) altında; piyasanın ağırlığı ikinci elde. Ağustos 2026'da satış <strong>2.932</strong> konutta kaldı; bir yıl önce 3.854'tü.</p>"
   "<p>Bu düşüş, satıcının alıcıyı daha uzun beklemesi demek. Video ilanı listede öne çıkarıyor ve alıcının mülkü görmeden önce elemesini sağlıyor; gezmeye gelen alıcı artık gerçekten ilgilenen alıcı oluyor.</p>"),
  ("Kayseri'de mülke göre video",
   "<p><strong>Melikgazi ve Kocasinan:</strong> merkezdeki site daireleri ve kentsel dönüşüm projeleri. Alıcı otoparkı, sosyal alanı ve raylı sisteme mesafeyi soruyor.</p>"
   "<p><strong>Talas:</strong> üniversiteye yakın, öğrenciye kiralanan daireler ve şehre tepeden bakan yeni projeler. Kiralık dairede kısa dikey video, satılıkta tam tur ve manzara.</p>"
   "<p><strong>Erciyes çevresi:</strong> kayak merkezine yakın dağ evleri ve oteller; kışın karla, yazın yayla havasıyla iki ayrı sezon videosu.</p>"
   "<p><strong>Sanayi ve depo:</strong> organize sanayi bölgesindeki fabrika ve depo ilanları. Yatırımcı tesisin büyüklüğünü ve yol bağlantısını görmek istiyor; havadan konum planı bunu tek karede veriyor.</p>"),
  ("Çekim düzeni",
   "<p>Kayseri Havalimanı askerî üsle ortak kullanılıyor; Kocasinan'ın kuzeyinde drone uçuşu izne bağlı. Mülkün konumunu haritadan kontrol edip uçuş planını teklifte netleştiriyoruz. Kışın kar sonrası açık bir sabah Erciyes'i şehrin arkasında en net gösteren an; ilan çekimini mümkünse o güne denk getiriyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Satışlar düşükken video çektirmek mantıklı mı?", "Tam da bu dönemde. Alıcı azken ilanınızın listede ayrışması ve gezmeye gelenin gerçekten ilgilenen biri olması zaman kazandırıyor."),
  ("Talas'taki kiralık dairemiz için ne çekmeliyiz?", "30–45 saniyelik dikey bir tur: giriş, odalar, mutfak ve balkon. Öğrenci ve genç çalışan kitlesi ilanı telefondan izliyor."),
  ("Fabrika ya da depo ilanı için video ne içermeli?", "Havadan konum ve yol bağlantısı, bina dışı, iç hacim ve yükleme alanı. Yatırımcıya giden sunumda kapalı alanı ve tavan yüksekliğini grafikle yazıyoruz."),
  ("Erciyes'teki dağ evini ne zaman çekmeliyiz?", "İki kez öneriyoruz: kışın kayak sezonu için karla, yazın yayla kiralaması için yeşille."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ İZMİR DÜĞÜN
"izmir-dugun-cekimi": dict(
 lede="İzmir'de 2025'te 27.951 çift evlendi; İstanbul ve Ankara'dan sonra üçüncü sıra. Bir kısmı Buca'daki düğün salonunda, bir kısmı Alaçatı'daki bağ evinde; İzmir'de düğün filmi mekânla birlikte değişiyor.",
 bolum=[
  ("İzmir'de düğün rakamlarla",
   "<p>TÜİK'e göre İzmir'de 2025'te <strong>27.951 evlilik</strong> kaydedildi; bin kişide 6,21. En kalabalık ilçeler <strong>Buca (3.379)</strong>, <strong>Bornova (2.836)</strong>, <strong>Konak (2.836)</strong>, <strong>Karşıyaka (1.980)</strong> ve <strong>Karabağlar (1.678)</strong>. Kıyı ilçelerinde sayı düşük ama düğün büyük: Çeşme ve Urla, şehir dışından gelen çiftlerin de tercih ettiği yerler.</p>"),
  ("İki ayrı düğün tipi",
   "<p><strong>Şehir düğünü:</strong> Buca, Bornova, Karşıyaka çevresindeki salon ve bahçe düğünleri. Gelin alma, kısa bir dış çekim ve salon aynı gün; İzmir trafiği nedeniyle ilçeler arası geçişi saat saat planlıyoruz. Dış çekim için Kordon'un gün batımı ve Karşıyaka sahili şehirden çıkmadan en güçlü seçenek.</p>"
   "<p><strong>Kıyı ve bağ düğünü:</strong> Alaçatı, Urla, Seferihisar ve Foça'da açık havada, çoğu zaman gün batımına göre başlayan düğünler. Bu düğünlerde ışık her şey; töreni güneşin batışına göre konumlandırmayı düğün planlayıcınızla birlikte öneriyoruz.</p>"),
  ("İzmir'in havası ve rüzgârı",
   "<p>İzmir'de yaz öğleden sonraları körfezden esen imbat serinletiyor ama açık hava düğününde gelinliği, saçı ve süslemeyi etkiliyor; Alaçatı ise zaten rüzgârıyla bilinen bir yer. Dış çekim noktasını rüzgâra göre korunaklı seçiyor, mikrofonu rüzgâra karşı ayrıca koruyoruz. Temmuz–Ağustos öğlesi çok sıcak; dış çekimi akşamüstüne koyuyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde İzmir'deki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Alaçatı'daki düğünümüz için en iyi tören saati ne?", "Gün batımından yaklaşık bir saat önce. Işık yumuşak, sıcak azalmış oluyor; tören bitince altın saatte kısa bir çift çekimi yapılabiliyor."),
  ("Rüzgârlı havada yeminleri net kaydedebilir misiniz?", "Evet. Çiftin ve nikâh memurunun üzerine rüzgâra dayanıklı yaka mikrofonu takıyor, sesi ayrıca kaydediyoruz."),
  ("Buca'dan Çeşme'ye aynı gün geçebilir miyiz?", "Mümkün ama yaklaşık bir saatlik yol hesaba katılmalı. Gelin alma ile dış çekim arasına bu süreyi baştan koyuyoruz."),
  ("Sezonda tarih bulmak zor mu?", "Kıyı düğünlerinde Mayıs–Eylül hafta sonları erken doluyor. Tarihinizi netleştirdiğinizde hemen yazmanızı öneriyoruz."),
 ],
 kaynak=[KAYNAK_EVLENME],
),

# ------------------------------------------------------------------ ESKİŞEHİR EMLAK
"eskisehir-emlak-video": dict(
 lede="Eskişehir'de üç büyük üniversite var ve şehrin konut piyasası öğrenci takvimine göre nefes alıyor: Ağustos–Eylül'de kiralık, yıl boyu satılık. İlan videosu da bu iki ayrı alıcıya göre çekilmeli.",
 bolum=[
  ("Eskişehir konut piyasası rakamlarla",
   "<p>TÜİK verisine göre Eylül 2025–Ağustos 2026 arasında Eskişehir'de <strong>26.991 konut</strong> satıldı; il Türkiye'de 19. sırada. Ağustos 2026'da satışlar bir yıl öncesine göre <strong>%16,8</strong> geriledi (2.556'dan 2.127'ye). Türkiye genelinde düşüş %14,7.</p>"
   "<p>Satış yavaşladığında mülk sahiplerinin bir kısmı kiraya yöneliyor; öğrenci şehri Eskişehir'de bu, kiralık ilan sayısının arttığı ve rekabetin sertleştiği anlamına geliyor.</p>"),
  ("Kiralık: öğrenci ve genç çalışan",
   "<p>Anadolu, Osmangazi ve Teknik üniversitelerin kampüslerine yakın daireler Ağustos sonundan Eylül ortasına kadar hızla kiralanıyor. Bu dönemde ilan telefonda, birkaç saniyede değerlendiriliyor. 30–45 saniyelik dikey bir tur, kampüse ve tramvaya mesafe yazısıyla birlikte, ilanı rakiplerinden ayırıyor.</p>"
   "<p>Öğrenci kiralaması yapan emlak ofisleri için yaz sonundan önce portföyü toplu çekiyor, aynı gün içinde onlarca daireyi bitirecek bir düzen kuruyoruz.</p>"),
  ("Satılık: Odunpazarı'ndan yeni projelere",
   "<p><strong>Odunpazarı'nın restore evleri:</strong> renkli cepheler, ahşap cumbalar, avlular. Bu evlerin alıcısı dokuyu satın alıyor; sokaktan avluya giren akıcı bir plan ve detay çekimi öne çıkıyor. Koruma alanında olduğu için cephe ve sokak çekimlerinde komşu evlere saygıya dikkat ediyoruz.</p>"
   "<p><strong>Yeni projeler ve siteler:</strong> şehrin dış halkasında yükselen siteler için sosyal alan, otopark ve ulaşım bağlantısı. Merkezde drone uçuşu havalimanı ve askerî üs nedeniyle çoğu zaman izne bağlı; havadan planı gerekiyorsa izni önceden alıyor, gerekmiyorsa yüksek bir terastan yerden çekiyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Öğrenci dairesi için video ne zaman hazır olmalı?", "Ağustos ortasında. Kiralamaların büyük kısmı Ağustos sonu ile Eylül ortası arasında kararlaştırılıyor."),
  ("Odunpazarı'ndaki tarihî evi nasıl çekiyorsunuz?", "Sokaktan avluya giren tek plan, oda oda tur ve ahşap, taş ve cumba detayları. Işığı avluya düşen saate göre planlıyoruz."),
  ("Eskişehir merkezinde drone ile çekim yapılabiliyor mu?", "Çoğu konumda izin gerekiyor. Mülkün yerine bakıp izni önceden alıyor ya da havadan planı yüksek bir noktadan yerden çekimle karşılıyoruz."),
  ("Emlak ofisi olarak toplu çekim yaptırabilir miyiz?", "Evet. Aynı mahalledeki daireleri tek güne topluyor, her biri için kısa dikey ve yatay sürüm teslim ediyoruz."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ ANTALYA KLİP
"antalya-klip-cekimi": dict(
 lede="Antalya'da kış bile klip mevsimi. Kaleiçi'nin taş sokakları, falezlerden denize dökülen Düden Şelalesi, Olympos'un çam ormanı ve Toros'un karlı zirveleri yılın her ayı ışık veriyor.",
 bolum=[
  ("Antalya'da klip için mekân",
   "<p><strong>Kaleiçi:</strong> Hadrian Kapısı'ndan limana inen dar sokaklar, cumbalı evler, yat limanı. Gece ışıklarıyla romantik ve nostaljik parçalar için; yaz akşamları çok kalabalık, sabah erken saatler boş.</p>"
   "<p><strong>Falezler ve Düden Şelalesi:</strong> Lara tarafında suyun falezden doğrudan denize döküldüğü yer. Geniş, dramatik planlar için; deniz ve kayalar aynı karede.</p>"
   "<p><strong>Olympos ve Çıralı:</strong> çam ormanı içinde antik kalıntılar, nehrin denize karıştığı kumsal ve Yanartaş'ın gece yanan alevleri. Doğal, serbest ruhlu parçalar için.</p>"
   "<p><strong>Köprülü Kanyon ve Toros yaylaları:</strong> turkuaz su, taş köprüler, yüksek yaylalarda kar ve ardıç. Sahilden bir buçuk saatte bambaşka bir iklim.</p>"),
  ("Kışın çekim, yazın kalabalık",
   "<p>Antalya'nın en büyük avantajı kış ışığı: Kasım'dan Mart'a kadar hava çoğu gün açık, deniz sakin, sahil ve antik kentler boş. Toros'un zirveleri ise karla kaplı; aynı gün içinde karlı dağ ve deniz kıyısı çekilebiliyor. Kuzeydeki şehirlerden gelen sanatçılar için kışın Antalya'da çekim, ışık açısından yazdan daha verimli.</p>"
   "<p>Yazın ise sahil ve Kaleiçi turizmin içinde. Kalabalık planları ya gün doğumuna ya da otel ve özel mülklerin içine taşıyoruz.</p>"),
  ("İzinler",
   "<p>Aspendos, Perge ve Side gibi ören yerlerinde ticari çekim Kültür ve Turizm Bakanlığı iznine bağlı; Olympos ve Termessos ayrıca millî park sınırları içinde. Antalya Havalimanı'nın kontrollü sahası Lara ve Aksu tarafını kapsadığı için falezlerde drone planı ayrı izin gerektirebiliyor. Bu izinlerin süresini klibin takvimine en baştan koyuyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde Antalya'daki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Kışın Antalya'da klip çekmek mantıklı mı?", "Çok. Kasım–Mart arası ışık temiz, sahil ve antik kentler boş, Toros karlı. Aynı gün dağ ve deniz çekilebiliyor."),
  ("Aspendos'ta klip çekebilir miyiz?", "Bakanlık izniyle evet; süreç haftalar sürebiliyor. Takvimi izne göre kuruyoruz."),
  ("Kaleiçi'nde gece çekimi nasıl yapılıyor?", "Sokak ışıklarını ve vitrinleri kullanıyor, gerekirse küçük bir ışık seti ekliyoruz. Kalabalık olmayan geç saatleri tercih ediyoruz."),
  ("Otel ya da villa içinde klip çekebilir miyiz?", "Evet, mülk sahibinin izniyle. Havuz, teras ve deniz manzarası olan özel mülkler yazın kalabalıktan kaçmanın en iyi yolu."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ AYDIN KLİP
"aydin-klip-cekimi": dict(
 lede="Aydın efelerin, zeybeğin memleketi. Ağır ve vakur bir zeybek ritmi, Afrodisias'ın mermer sütunları, incir bahçeleri ve Kuşadası'nın sahili aynı klipte buluşabiliyor.",
 bolum=[
  ("Zeybek ve yerel müzik",
   "<p>Zeybek, Ege'nin en tanınan halk oyunu ve Aydın efeleriyle özdeşleşmiş bir gelenek. Bu ritimle yazılmış ya da ondan beslenen parçalar için kamera yavaş ve aşağıdan çalışmalı: yere vuran adım, açılan kollar, ağır dönüş. Yerel halk oyunları ekipleriyle çalışarak geleneği doğru temsil eden bir koreografi kuruyoruz.</p>"),
  ("Aydın'da klip için mekân",
   "<p><strong>Afrodisias (Karacasu):</strong> UNESCO Dünya Mirası listesindeki antik kent; mermer sütunlar, stadyum ve Tetrapylon. Ören yeri olduğu için çekim Kültür ve Turizm Bakanlığı iznine bağlı.</p>"
   "<p><strong>Priene ve Milet:</strong> Söke ve Didim'de, ova üzerinde yükselen antik kentler; Didim'deki Apollon Tapınağı'nın dev sütunları. Bunlar da izin gerektiriyor.</p>"
   "<p><strong>Kuşadası ve Dilek Yarımadası:</strong> Güvercinada, marina ve millî park içindeki koylar. Yaz kliplerinde deniz ve kıyı.</p>"
   "<p><strong>İncir ve zeytin bahçeleri:</strong> ovanın her yerinde. Yaz sonu incir toplama dönemi canlı bir arka plan; bahçe sahibinin izniyle, kolay ulaşılan ve izin süreci gerektirmeyen bir set.</p>"),
  ("Çekim düzeni",
   "<p>Aydın yazın Türkiye'nin en sıcak illerinden biri. Ova ve antik kent çekimlerini gün doğumuna ve akşamüstüne koyuyor, öğleyi iç mekâna ayırıyoruz. Ören yeri izinleri haftalar sürebildiği için izin gerektiren mekânlarla izinsiz çekilebilen mekânları aynı plana koyup takvimi buna göre kuruyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Zeybek koreografisi için ekip bulabiliyor musunuz?", "Evet. Yerel halk oyunları ekipleriyle çalışıyor, kostümü ve figürleri geleneğe uygun kuruyoruz."),
  ("Afrodisias'ta klip çekmek ne kadar sürer?", "Asıl süre izin sürecinde. Bakanlık başvurusunu en az bir ay önce yapmak gerekiyor; çekimin kendisi yarım gün."),
  ("İzin gerektirmeyen güçlü bir mekân var mı?", "İncir ve zeytin bahçeleri, köy meydanları ve sahil. Bahçe ya da mülk sahibinin izniyle hemen çekilebiliyor."),
  ("Yazın sıcakta nasıl çekiyorsunuz?", "Dış çekimi sabah erken ve akşamüstü yapıyoruz; ekip ve sanatçı için gölge ve su planı çekim gününün parçası."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ BALIKESİR KLİP
"balikesir-klip-cekimi": dict(
 lede="Ayvalık'ta Şeytan Sofrası'ndan adalara batan güneş, Cunda'nın taş sokakları, Kaz Dağları'nın şelaleleri. Balıkesir, Bursa'dan birkaç saat mesafede hem Ege hem Marmara kıyısı olan bir klip seti.",
 bolum=[
  ("Balıkesir'de klip için mekân",
   "<p><strong>Ayvalık ve Cunda:</strong> eski Rum evleri, taş sokaklar, sabun ve zeytinyağı fabrikalarından kalan yapılar. Şeytan Sofrası'nın tepesinden adalara bakan gün batımı planı Ege'nin en tanınan karelerinden biri; akşamları çok kalabalık, erken gidip yer tutmak gerekiyor.</p>"
   "<p><strong>Kaz Dağları:</strong> Edremit'teki Hasanboğuldu ve Sutüven şelaleleri, çam ve kestane ormanı, dağ dereleri. Mitolojik, doğal ya da akustik parçalar için. Millî park sınırlarında ticari çekim için izin gerekiyor.</p>"
   "<p><strong>Eski zeytinyağı fabrikaları:</strong> Ayvalık ve Edremit çevresinde, yüksek tavanlı taş yapılar. Bir kısmı restore edilip mekân oldu; endüstriyel ve sıcak bir doku aynı anda.</p>"
   "<p><strong>Erdek ve Marmara Adası:</strong> sakin koylar ve beyaz mermer ocakları. Ocakların dev basamakları, elektronik ve deneysel işler için olağanüstü bir görsel.</p>"),
  ("Bursa'dan Balıkesir'e",
   "<p>Balıkesir'de kendi ekibimizle çalışıyoruz. Erdek ve Bandırma Bursa'ya yaklaşık bir buçuk saat; Ayvalık ve Kaz Dağları daha uzak. Ege kıyısındaki çekimler için bir gece konaklayıp gün batımını ve sabah ışığını birlikte almayı öneriyoruz. Edremit'teki dağ ve Ayvalık'taki deniz aynı plana sığıyor.</p>"),
  ("Mevsim seçimi",
   "<p>Ayvalık ve Cunda Temmuz–Ağustos'ta çok kalabalık; sokak ve kıyı çekimleri için Mayıs–Haziran ve Eylül–Ekim çok daha rahat. Kaz Dağları'nın şelaleleri ilkbaharda en gür; sonbaharda ise kestane ve meşe ormanı renk değiştiriyor.</p>"),
 ],
 sss=[
  ("Şeytan Sofrası'nda gün batımı çekimi yapılabilir mi?", "Evet ama yaz akşamları kalabalık. Bir saat erken gidip kadrajı kalabalığın dışında kuruyoruz; sezon dışında çok daha rahat."),
  ("Kaz Dağları'nda çekim için izin gerekiyor mu?", "Millî park sınırlarında ticari çekim için evet. Başvuruyu çekimden önce biz yapıyoruz."),
  ("Mermer ocağında klip çekebilir miyiz?", "İşletmenin izniyle ve iş güvenliği kurallarına uyarak evet; patlatma ve yükleme saatlerinin dışında çekiyoruz."),
  ("Bursa'dan Ayvalık'a tek günde gidip dönülür mü?", "Mümkün ama yorucu. Gün batımı ve sabah ışığını birlikte almak için bir gece konaklamayı öneriyoruz."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ İSTANBUL KLİP
"istanbul-klip-cekimi": dict(
 lede="Müzik endüstrisinin kalbi İstanbul'da, ama İstanbul'da klip çekmenin en pahalı kısmı çoğu zaman kamera değil: izin, trafik ve kalabalık. Doğru plan, aynı bütçeyle iki kat çekim süresi demek.",
 bolum=[
  ("İstanbul'da klip için mekân",
   "<p><strong>Balat ve Fener:</strong> renkli evler, yokuşlar, eski Rum okulu ve kiliseler. Çok çekildiği için kadrajı farklı kurmak gerekiyor: ana caddeler yerine arka sokaklar, gündüz yerine akşamüstü.</p>"
   "<p><strong>Karaköy, Galata ve Beyoğlu:</strong> eski hanlar, merdivenli sokaklar, çatı katları. Hanların iç avluları ve çatılar, kalabalık sokağa göre çok daha kontrollü bir set.</p>"
   "<p><strong>Kadıköy ve Moda:</strong> sahil, eski apartmanlar ve gece hayatı; bağımsız müzik sahnesinin kalbi.</p>"
   "<p><strong>Belgrad Ormanı, Şile ve Kilyos:</strong> şehrin içinde ya da kenarında orman ve Karadeniz kıyısı; sokakların dışına çıkmak isteyen klipler için.</p>"),
  ("İzin ve drone",
   "<p>İstanbul'da kamuya açık alanda ticari çekim ilçe belediyesinin ve çoğu zaman valiliğin iznine bağlı; tarihî yarımadada ve müzelerde ayrıca Bakanlık izni gerekiyor. İki büyük havalimanı ve Boğaz nedeniyle şehrin neredeyse tamamı kontrollü hava sahasında; drone planları ayrı izin süreci istiyor. Bu süreçlerin takvimini çekim tarihinden haftalar önce başlatıyoruz.</p>"),
  ("Bütçeyi verimli kullanmak",
   "<p>İstanbul'da tüm klibi şehirde çekmek zorunda değilsiniz. İstanbul'un tanınan karelerini kısa ve izinli bir yarım günde alıp, uzun performans ve hikâye sahnelerini daha sakin bir mekânda çekmek bütçeyi rahatlatıyor. Bursa'dan İstanbul'a deniz otobüsü ya da otoyolla iki saatte geliyoruz; Bursa, Sakarya ve Yalova'daki mekânlar da İstanbul'dan gelen sanatçı için günübirlik.</p>"
   "<p>İstanbul'da çekimi kendi ekibimizle yapıyoruz; kurgu, renk ve yönetmenlik de bizde.</p>"),
  ("İstanbul'da çektiğimiz klip",
   "<p><strong>Bir Peron</strong> klibini İstanbul'da çektik; çekim ve kurgu bizde. Klip bu sayfadaki oynatıcıda. Şehrin içinde, kalabalığın arasında ama kontrollü bir set kurmanın nasıl olduğunu bu işten biliyoruz: mekânı saatine göre seçmek, izni önceden almak, ekibi küçük tutmak.</p>"),
 ],
 sss=[
  ("İstanbul'da klip için izin ne kadar sürer?", "Mekâna göre değişiyor. İlçe belediyesi izni birkaç gün ile iki hafta arasında; tarihî yarımada ve müzelerde Bakanlık izni daha uzun. Takvimi izne göre kuruyoruz."),
  ("İstanbul'da drone ile klip çekebilir miyiz?", "Çoğu konumda ayrı izin gerekiyor ve süreç uzun. Havadan planı şehir dışında ya da izni çıkan tek bir noktada almayı öneriyoruz."),
  ("Balat çok çekildi, farklı ne yapabiliriz?", "Arka sokaklar, iç avlular, evlerin içi ve akşamüstü ışığı. Mekânı değil, onu nasıl gösterdiğimizi değiştirmek yeterli."),
  ("Bütçemiz sınırlı, tüm klibi İstanbul'da mı çekmeliyiz?", "Gerekmiyor. Tanınan İstanbul karelerini yarım günde alıp kalan sahneleri daha sakin, izin derdi olmayan bir mekânda çekmek bütçeyi önemli ölçüde rahatlatıyor."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ KOCAELİ KLİP
"kocaeli-klip-cekimi": dict(
 lede="Bir yanda körfez boyunca liman vinçleri ve fabrika bacaları, öbür yanda Kartepe'nin ormanı ve karı. Kocaeli'nde klip, Türkiye'nin sanayi kalbiyle doğasını aynı karede buluşturuyor.",
 bolum=[
  ("Kocaeli'de klip için mekân",
   "<p><strong>Seka Park:</strong> İzmit'te eski kâğıt fabrikasının sahasına kurulan park ve fabrika yapılarından kalan müze. Endüstriyel geçmiş ile körfez kıyısı yan yana; rap, rock ve elektronik için doğal bir set.</p>"
   "<p><strong>Kartepe ve Maşukiye:</strong> derelerin, şelalelerin ve gölgeli ormanın arasından geçen yol; kışın karlı zirve ve kayak merkezi. Akustik ve duygusal parçalar için.</p>"
   "<p><strong>Körfez kıyısı:</strong> akşam ışığında liman vinçleri ve tankerler. Uzaktan çekildiğinde etkileyici bir siluet; liman ve tesis içleri izne bağlı, biz kamuya açık kıyıdan çekiyoruz.</p>"
   "<p><strong>Kerpe ve Kandıra sahili:</strong> Karadeniz kıyısında kayalık koylar ve sakin kumsallar; şehirden bir saat uzakta bambaşka bir kıyı.</p>"),
  ("İstanbul'dan ve Bursa'dan yakın",
   "<p>Kocaeli İstanbul'a bir saat; Bursa'dan da Osmangazi Köprüsü üzerinden yaklaşık bir saatte geliyoruz. Kocaeli'de kendi ekibimizle çalışıyoruz; mekân keşfini çekimden önce yerinde yapabiliyoruz. Bir günde Seka Park, körfez kıyısı ve Kartepe'yi birleştirmek mümkün.</p>"
   "<p>Kocaeli Üniversitesi çevresindeki genç müzik sahnesi için tek mekânlı, uygun bütçeli performans klipleri de planlıyoruz.</p>"),
  ("Çekim düzeni",
   "<p>Körfez kıyısında akşamüstü ışık sanayi siluetini en dramatik gösterdiği an; Kartepe'de ise sis ve bulut gün içinde hızla değişiyor. Dağ çekimine yedek saat ya da yedek gün koyuyoruz. Kocaeli'nin çoğu yeri drone için izne bağlı olduğu için havadan planları baştan haritaya göre seçiyoruz.</p>"),
 ],
 sss=[
  ("Seka Park'ta klip çekmek için izin gerekiyor mu?", "Park kamuya açık; ticari çekim ve kalabalık ekip için belediyeye bilgi veriyoruz. Müze içi için ayrıca izin alıyoruz."),
  ("Fabrika içinde klip çekebilir miyiz?", "Fabrika sahibinin izniyle ve iş güvenliği kurallarına uyarak evet. Üretimi durdurmadan, güvenli mesafeden çekiyoruz."),
  ("Kartepe'de karlı çekim için ne zaman gelmeliyiz?", "Ocak–Şubat. Kar yağışından sonraki ilk açık güne göre esnek bir tarih koyuyoruz."),
  ("Kocaeli'ne kendi ekibinizle mi geliyorsunuz?", "Evet. Bursa'dan yaklaşık bir saatte geliyoruz; çeken ve kurgulayan aynı kişiler."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ KONYA KLİP
"konya-klip-cekimi": dict(
 lede="Ney sesi, sema eden bir derviş, ufka kadar uzanan bozkır ve Tuz Gölü'nün beyaz yüzeyi. Konya, ruhani ve sade bir klip için Türkiye'nin en güçlü setlerinden biri.",
 bolum=[
  ("Konya'da klip için mekân",
   "<p><strong>Tuz Gölü (Cihanbeyli kıyısı):</strong> yazın kuruyan, bembeyaz bir tuz düzlüğü; ince bir su tabakası olduğunda gökyüzünü yansıtan bir ayna. Minimal, gerçeküstü planlar için. Gün batımında beyaz yüzey pembe ve turuncuya dönüyor.</p>"
   "<p><strong>Beyşehir ve Eşrefoğlu Camii:</strong> gölün kıyısında, ahşap sütunlu Selçuklu camisi ve göle batan güneş. Cami ibadete açık; iç çekim için izin ve ibadet saatlerine uyum gerekiyor.</p>"
   "<p><strong>Sille ve Kilistra:</strong> Sille'nin taş evleri ve vadisi; Kilistra'da kayaya oyulmuş yapılar. Dönem havası ve hikâyeli klipler için.</p>"
   "<p><strong>Bozkır:</strong> şehrin dışında, çıplak ve geniş ufuk. Tek bir figürün uzakta durduğu planlar, yalnızlık ve arayış temalı parçalar için.</p>"),
  ("Sema ve ney ile çalışmak",
   "<p>Sema bir ibadet; gösteri olarak ya da klipte kullanılacaksa bunu saygıyla ve Mevlevi geleneğini bilen semazen ve neyzenlerle birlikte yapmak gerekiyor. Kostümü, hareketi ve mekânı geleneğe uygun kuruyor, semayı bir dekor gibi değil, anlamıyla birlikte çekiyoruz.</p>"),
  ("Çekim düzeni",
   "<p>Konya yazın sıcak ve kuru, kışın sert soğuk. Tuz Gölü'nde öğle ışığı beyaz yüzeyden göz alacak kadar sert yansıyor; çekimi gün doğumuna ve gün batımına koyuyoruz. Göl şehirden yaklaşık iki saat uzakta; ayrı bir gün olarak planlıyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Tuz Gölü'nde ayna etkisini ne zaman yakalarız?", "Yüzeyde ince bir su tabakası olduğunda, genellikle ilkbaharda ya da yağmurdan sonra. Yazın göl kuru ve bembeyaz; ikisi de farklı bir görüntü veriyor."),
  ("Klipte sema kullanabilir miyiz?", "Evet, geleneğe saygıyla ve deneyimli semazenlerle. Semanın anlamını bozmayan bir kurgu öneriyoruz."),
  ("Eşrefoğlu Camii'nde çekim yapılabilir mi?", "İzinle ve ibadet saatlerinin dışında. Dış çekim ve göl kıyısı için izin süreci daha kısa."),
  ("Konya'da tek günde kaç mekân çekilir?", "Şehir içi ve Sille aynı gün; Tuz Gölü ve Beyşehir uzak olduğu için her biri ayrı gün."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ MANİSA KLİP
"manisa-klip-cekimi": dict(
 lede="Kula'nın siyah volkanik arazisi, Spil'in ormanı, bağların arasında uzanan toprak yollar. Manisa, İzmir'in hemen yanında, kalabalıktan uzak ve hâlâ az keşfedilmiş bir klip coğrafyası.",
 bolum=[
  ("Manisa'da klip için mekân",
   "<p><strong>Kula volkanik arazisi:</strong> sönmüş volkan konileri, siyah lav akıntıları ve peribacaları; korunan bir jeopark. Türkiye'de başka bir yere benzemeyen, neredeyse başka bir gezegen gibi duran bir set. Eski Kula evleri ve dar sokaklar da hemen yanında.</p>"
   "<p><strong>Spil Dağı:</strong> şehrin üzerinde yükselen millî park; çam ormanı ve şehre bakış. Ticari çekim için millî park izni gerekiyor.</p>"
   "<p><strong>Bağlar ve ova:</strong> Salihli ve Alaşehir'in bitmeyen bağ sıraları; yaz sonunda kuru üzüm serilen tarlalar. Sıcak, toprak tonlu ve geniş planlar için.</p>"
   "<p><strong>Gölmarmara ve kırsal:</strong> sazlık göl kıyısı ve köy yolları; akustik ve sakin parçalar için.</p>"),
  ("İzmir'den gelen sanatçı için Manisa",
   "<p>İzmir'in müzik sahnesi büyük ama şehir içinde dış çekim kalabalık ve izne bağlı. Manisa'nın merkezi İzmir'e yaklaşık 40 dakika; Kula ve bağlar bir buçuk saat. İzmir'deki sanatçılar için Manisa, günübirlik ve izin süreci daha hafif bir alternatif.</p>"
   "<p>Manisa'nın baharda yapılan Mesir Macunu Festivali de kalabalık ve renkli bir sahne; festival görüntüsünü klibe eklemek isteyenler için tarihi önceden planlıyoruz.</p>"),
  ("Çekim düzeni",
   "<p>Manisa yazın çok sıcak; Kula'nın siyah toprağı öğlen ısıyı daha da artırıyor. Dış çekimleri gün doğumuna ve akşamüstüne koyuyoruz. Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Kula'da klip çekmek için izin gerekiyor mu?", "Jeopark ve koruma alanlarında ticari çekim için izin gerekiyor; köy ve kasaba içinde belediyeye bilgi veriyoruz."),
  ("İzmir'den gelip tek günde çekim yapabilir miyiz?", "Evet. Spil ve bağlar aynı gün; Kula'yı da eklemek için erken başlamak gerekiyor."),
  ("Bağda klip için en iyi dönem hangisi?", "Haziran–Ağustos arası bağlar dolu ve yeşil; Ağustos sonunda kuru üzüm serme dönemi altın tonlar veriyor."),
  ("Mesir Festivali'nde çekim yapılabilir mi?", "Kalabalık bir kamusal etkinlik; seyirci olarak çekim mümkün. Sahne ya da protokol alanı için organizasyondan izin alıyoruz."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ MERSİN KLİP
"mersin-klip-cekimi": dict(
 lede="Denizin ortasında bir kale, yerin içine açılan dev obruklar, narenciye bahçeleri ve bir liman şehrinin gece ışıkları. Mersin, Akdeniz'in en az çekilmiş klip setlerinden biri.",
 bolum=[
  ("Mersin'de klip için mekân",
   "<p><strong>Kızkalesi:</strong> kıyıdan birkaç yüz metre açıkta, denizin içinde yükselen Orta Çağ kalesi. Kıyıdaki Korykos Kalesi ile karşılıklı; gün batımında silüet etkisi güçlü. Kaleye tekneyle geçiliyor.</p>"
   "<p><strong>Cennet ve Cehennem obrukları (Silifke):</strong> yerin içine açılan dev çukurlar ve dibindeki küçük şapel. Karanlık, gizemli ve dramatik parçalar için; ören yeri kuralları geçerli.</p>"
   "<p><strong>Narenciye bahçeleri:</strong> kışın portakal ve limonla dolu ağaçlar; Erdemli ve Tarsus çevresinde. Sıcak, renkli ve kolay ulaşılan bir set.</p>"
   "<p><strong>Tarsus:</strong> tarihî sokaklar, Kleopatra Kapısı ve şehrin içindeki şelale. Gündüz tarih, akşam şehir.</p>"
   "<p><strong>Liman ve sahil yolu:</strong> konteyner vinçleri, uzun sahil parkı ve gece ışıkları; modern ve şehirli parçalar için.</p>"),
  ("Kışın Akdeniz",
   "<p>Mersin'de kış ılık ve çoğu gün açık. Narenciye hasadı Kasım'dan Şubat'a kadar sürüyor; bahçeler tam bu dönemde en renkli. Kuzeyden gelen sanatçılar için kış, hem ışık hem fiyat açısından avantajlı bir çekim dönemi. Yazın ise nem ve sıcak yüksek; dış çekimi sabaha ve akşama koyuyoruz.</p>"),
  ("İzinler ve ekip",
   "<p>Kızkalesi, obruklar ve diğer ören yerlerinde ticari çekim Bakanlık iznine bağlı; liman sahası kapalı alan. Kamuya açık sahil ve şehir içi için belediyeye bilgi veriyoruz. Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Kızkalesi'nde klip çekebilir miyiz?", "İzinle evet. Kaleye tekneyle geçiliyor; ekipmanı ve ekip sayısını buna göre küçük tutuyoruz. Kıyıdan çekilen kale silüeti de güçlü bir alternatif."),
  ("Narenciye bahçesinde ne zaman çekim yapmalıyız?", "Kasım–Şubat arası; meyveler ağaçta, ışık yumuşak. Bahçe sahibinin izniyle çekiyoruz."),
  ("Obruklarda çekim zor mu?", "Cennet obruğuna uzun bir merdivenle iniliyor; ekipmanı hafif tutuyoruz. Işık dibe öğle saatlerinde ulaşıyor."),
  ("Mersin'de gece klibi için nereyi önerirsiniz?", "Sahil yolu, marina ve şehir merkezi; liman vinçlerini uzaktan arka plan olarak kullanıyoruz."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ SAMSUN KLİP
"samsun-klip-cekimi": dict(
 lede="Ladik Gölü'nün sisli kıyısı, Akdağ'ın yaylaları, Terme'nin Amazon efsanesi ve Karadeniz'in en büyük liman şehirlerinden birinin gece ışıkları. Samsun klip için sahilden ibaret değil.",
 bolum=[
  ("Samsun'da klip için mekân",
   "<p><strong>Ladik Gölü ve Akdağ:</strong> şehirden yaklaşık bir saat uzakta, sazlıklı göl ve üzerindeki yayla. Sisli sabahlar ve yeşil yamaçlar; akustik, türkü ve duygusal parçalar için.</p>"
   "<p><strong>Terme ve Amazon efsanesi:</strong> antik kaynaklara göre Amazon kadın savaşçıların yaşadığı topraklar. Güçlü, kadın temalı ya da destansı bir hikâye kurmak isteyenler için hem mekân hem anlam.</p>"
   "<p><strong>Liman ve şehir:</strong> Samsun limanı, Cumhuriyet Meydanı ve sahil yolu. Gece kliplerinde şehrin ışıkları ve liman siluet.</p>"
   "<p><strong>Kızılırmak ve Yeşilırmak ovaları:</strong> Bafra ve Çarşamba'nın düz ve verimli ovaları, nehir kıyıları. Geniş, sade ve açık planlar için.</p>"),
  ("Samsun'un müzik sahnesi",
   "<p>Samsun hem Karadeniz hem İç Anadolu müziğinin kesiştiği bir yer: Bafra ve Çarşamba'nın türküleri, Karadeniz'in ritmi ve büyük bir üniversite şehrinin genç sahnesi. Bu çeşitlilik, aynı şehirde hem türkü hem rock klibi için uygun mekân bulmayı kolaylaştırıyor. Yerel sanatçılar için tek mekânlı performans klibi, daha büyük işler için hikâyeli çok mekânlı klip planlıyoruz.</p>"),
  ("Çekim düzeni",
   "<p>Samsun'da hava gün içinde değişebiliyor; yayla ve göl çekimine yedek gün koyuyoruz. Çarşamba'daki havalimanı ve liman çevresinde drone izne bağlı; havadan planları göl ve yayla tarafına koyuyoruz. Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Ladik Gölü'nde sisli plan için ne zaman gitmeliyiz?", "İlkbahar ve sonbahar sabahları; gün doğumunda. Sis havaya bağlı olduğu için yedek gün koyuyoruz."),
  ("Amazon temalı bir klip için kostüm ve oyuncu bulabiliyor musunuz?", "Evet. Kostüm, oyuncu ve dublör koordinasyonunu hikâyeye göre kuruyoruz."),
  ("Samsun'da gece klibi için nereyi önerirsiniz?", "Sahil yolu ve liman çevresi; şehrin ışıkları ve gemilerin silueti arka planı kuruyor."),
  ("Türkü klibi için hangi mekân uygun?", "Ladik ve Akdağ yaylaları ya da Bafra ovasında bir köy; az kesmeli ve uzun planlı bir anlatım öneriyoruz."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ YALOVA KLİP
"yalova-klip-cekimi": dict(
 lede="Yalova küçük ama içinde termal kaplıcalar, ormanın içindeki şelaleler, Türkiye'nin en büyük fidanlıkları ve İstanbul'a deniz otobüsüyle bir saatlik mesafe var. Bursa'dan da bir saat.",
 bolum=[
  ("Yalova'da klip için mekân",
   "<p><strong>Termal:</strong> ormanla çevrili Osmanlı hamamları, eski oteller ve Sudüşen Şelalesi. Sıcak su buharı, taş ve yeşil; nostaljik ve gizemli parçalar için. Termal tesisler içinde çekim işletmenin iznine bağlı.</p>"
   "<p><strong>Erikli Şelalesi ve Teşvikiye ormanı:</strong> Çınarcık'a bağlı, ormanın içinden ulaşılan kademeli şelaleler. Doğal ve sakin bir set; hafta içi neredeyse boş.</p>"
   "<p><strong>Fidanlıklar ve seralar:</strong> Yalova, süs bitkisi ve fidan üretiminde Türkiye'nin merkezi. Sıra sıra seralar ve çiçek tarlaları renkli, düzenli ve alışılmadık bir görsel; sera sahibinin izniyle çekiliyor.</p>"
   "<p><strong>Çınarcık ve Esenköy sahili:</strong> küçük iskeleler, sakin kıyı ve karşıda İstanbul'un adaları.</p>"),
  ("İstanbul'a en yakın sakin set",
   "<p>Yalova'ya İstanbul'dan deniz otobüsü ve feribotla, Osmangazi Köprüsü üzerinden de karayoluyla bir saat civarında geliniyor. İstanbul'daki sanatçı sabah çıkıp akşam dönebiliyor; şehrin izin ve kalabalık yükü olmadan orman, şelale, deniz ve termal tek günde çekilebiliyor.</p>"
   "<p>Yalova'da kendi ekibimizle çalışıyoruz; Bursa'dan yaklaşık bir saatte geliyoruz.</p>"),
  ("Çekim düzeni",
   "<p>Termal ve şelaleler orman içinde olduğu için ışık öğle saatinde en iyi; sahil ise gün batımında. Bir günü Termal ve şelale ile başlayıp sahilde bitirecek şekilde kuruyoruz. Yaz hafta sonları Termal kalabalık; hafta içini öneriyoruz.</p>"),
 ],
 sss=[
  ("Termal'deki tarihî hamamlarda çekim yapılabilir mi?", "İşletmenin izniyle evet. Ziyaretçi saatleri dışında çekim için tarihi önceden ayarlıyoruz."),
  ("İstanbul'dan gelip tek günde bitirebilir miyiz?", "Evet. Sabah deniz otobüsüyle gelip akşam dönecek bir plan kuruyoruz; mekânlar birbirine yakın."),
  ("Sera ya da fidanlıkta klip çekebilir miyiz?", "Üreticinin izniyle evet. Bitkilere zarar vermeyecek şekilde, küçük bir ekiple çekiyoruz."),
  ("Şelaleler hangi mevsimde en gür?", "İlkbaharda. Yaz sonunda su azalıyor ama orman hâlâ yeşil."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ ADANA DÜĞÜN
"adana-dugun-cekimi": dict(
 lede="Adana'da 2025'te 15.039 çift evlendi. Seyhan Nehri'nin kıyısında gün batımı, Taşköprü'nün taş kemerleri ve yaz gecelerinin geç saate kadar süren düğünleri; Adana'da düğün filmi sıcağa göre planlanıyor.",
 bolum=[
  ("Adana'da düğün rakamlarla",
   "<p>TÜİK'e göre Adana'da 2025'te <strong>15.039 evlilik</strong> kaydedildi; bin kişide <strong>6,59</strong> ile il Türkiye ortalamasının (6,43) üzerinde. Evliliklerin üçte biri <strong>Seyhan'da (5.267)</strong>; onu <strong>Yüreğir (2.572)</strong>, <strong>Çukurova (2.437)</strong> ve <strong>Sarıçam (1.821)</strong> izliyor. Ceyhan (951) ve Kozan (872) ilçe düğünlerinin en kalabalık olduğu yerler.</p>"),
  ("Dış çekim için Adana'nın seçenekleri",
   "<p><strong>Seyhan Nehri ve Taşköprü:</strong> Roma döneminden kalan ve hâlâ ayakta duran taş köprü, karşısında Sabancı Merkez Camii'nin silueti. Gün batımında nehir kıyısı Adana'nın en güçlü dış çekim noktası.</p>"
   "<p><strong>Merkez Park ve nehir kıyısı:</strong> geniş yeşil alan, ağaçlıklı yürüyüş yolları; şehirden çıkmadan sakin bir çekim.</p>"
   "<p><strong>Varda Köprüsü (Karaisalı):</strong> derin bir vadinin üzerinden geçen yüksek demiryolu köprüsü. Şehirden yaklaşık bir saat; dramatik ve geniş planlar isteyen çiftler için ayrı bir dış çekim.</p>"
   "<p><strong>Seyhan Baraj Gölü:</strong> şehrin kuzeyinde göl kıyısı; akşam ışığında su ve ufuk.</p>"),
  ("Sıcakla çalışmak",
   "<p>Adana'nın yazı uzun ve çok sıcak. Haziran–Eylül düğünlerinde dış çekimi gün batımından önceki bir saate sıkıştırıyor, gelin ve damadın serinleyeceği araç ve gölge noktasını önceden ayarlıyoruz. Gelinliğin ve makyajın sıcakta bozulmaması için çekimi kısa ve hızlı tutuyoruz. Ekim–Mayıs arası ise Adana dış çekim için ideal; ışık yumuşak, hava rahat.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Yazın Adana'da dış çekim yapılabilir mi?", "Evet, ama gün batımından önceki bir saatte. Öğle sıcağında hem çift hem görüntü yoruluyor; çekimi kısa ve planlı tutuyoruz."),
  ("Taşköprü'de dış çekim için izin gerekiyor mu?", "Kamuya açık bir alan; kısa dış çekim için genellikle gerekmiyor. Drone kullanacaksak uçuş noktasını önceden kontrol ediyoruz."),
  ("Ceyhan ya da Kozan'daki düğünümüze geliyor musunuz?", "Evet. Gelin alma, dış çekim ve salon arasındaki yolu baştan hesaplayıp günü buna göre planlıyoruz."),
  ("Varda Köprüsü'nde dış çekim için ne kadar zaman ayırmalıyız?", "Yol dahil yarım gün. Vadiye inen yol dar olduğu için ekipmanı hafif tutuyor, ışığın vadiye düştüğü öğleden sonrayı seçiyoruz."),
 ],
 kaynak=[KAYNAK_EVLENME],
),

# ------------------------------------------------------------------ ANKARA DÜĞÜN
"ankara-dugun-cekimi": dict(
 lede="Ankara'da 2025'te 36.210 çift evlendi; İstanbul'dan sonra en yüksek sayı. Bu kadar düğünün yapıldığı bir şehirde dış çekim noktaları aynı saatlerde dolu; iyi bir düğün filmi zamanlamayla başlıyor.",
 bolum=[
  ("Ankara'da düğün rakamlarla",
   "<p>TÜİK'e göre Ankara'da 2025'te <strong>36.210 evlilik</strong> kaydedildi. En kalabalık ilçe <strong>Yenimahalle (7.010)</strong>; onu <strong>Keçiören (5.084)</strong>, <strong>Çankaya (4.894)</strong>, <strong>Etimesgut (3.795)</strong>, <strong>Sincan (3.102)</strong> ve <strong>Mamak (3.060)</strong> izliyor. Bin kişide 6,15 ile Türkiye ortalamasının biraz altında; ama nüfus büyük olduğu için hafta sonu salonlar ve dış çekim noktaları yoğun.</p>"),
  ("Dış çekim için Ankara'nın seçenekleri",
   "<p><strong>Gölbaşı ve Mogan Gölü:</strong> şehrin güneyinde göl kıyısı, sazlık ve gün batımı. Etimesgut ve Yenimahalle'den gelen çiftler için de yarım saatlik bir yol.</p>"
   "<p><strong>Eymir Gölü:</strong> ağaçlarla çevrili sakin bir göl; üniversite arazisinde olduğu için profesyonel çekimde izin gerekiyor.</p>"
   "<p><strong>Hamamönü ve Ankara Kalesi:</strong> restore edilmiş ahşap evler ve kaleden şehre bakış; şehirden çıkmadan tarihî doku.</p>"
   "<p><strong>Kızılcahamam ve Beypazarı:</strong> çam ormanı ya da Osmanlı evleri. Bir saatten fazla yol; düğünden önceki ya da sonraki güne ayrı bir dış çekim günü olarak öneriyoruz.</p>"),
  ("Ankara'ya özgü dikkat edilecekler",
   "<p>Ankara'nın büyük kısmı drone için kısıtlı hava sahasında; bakanlıklar, askerî alanlar ve havalimanları nedeniyle şehir içinde havadan plan çoğu yerde mümkün değil. Havadan görüntü isteyen çiftler için göl ya da şehir dışı bir noktayı seçiyor, izin gerekip gerekmediğini önceden söylüyoruz.</p>"
   "<p>Kışın Ankara'ya kar yağıyor; karlı dış çekim güzel ama soğuk. Çekimi 30–40 dakikaya sığdırıyor, araç ve sıcak mola noktasını hazır tutuyoruz. Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde Ankara'daki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Ankara'da düğünde drone kullanılabilir mi?", "Şehir içinde çoğu yerde hayır. Gölbaşı ya da şehir dışındaki bir dış çekim noktasında konuma göre mümkün; önceden kontrol ediyoruz."),
  ("Mogan'da gün batımı için ne zaman gitmeliyiz?", "Gün batımından bir saat önce. Hafta sonları kıyı kalabalık; çekim noktasını önceden seçiyoruz."),
  ("Karlı bir dış çekim istiyoruz, ne önerirsiniz?", "Kar yağışından sonraki ilk açık gün, kısa ve planlı bir çekim. Hamamönü ya da Kızılcahamam ormanı karla çok güzel görünüyor."),
  ("Sezonda tarih bulmak zor mu?", "Mayıs–Eylül hafta sonları erken doluyor. Tarihinizi netleştirdiğinizde hemen yazmanızı öneriyoruz."),
 ],
 kaynak=[KAYNAK_EVLENME],
),

# ------------------------------------------------------------------ ANTALYA DÜĞÜN
"antalya-dugun-cekimi": dict(
 lede="Antalya'da 2025'te 18.728 çift evlendi; bin kişide 6,81 ile Türkiye ortalamasının üzerinde. Bunlara bir de dışarıdan gelip Antalya'da evlenen çiftler ekleniyor: otel bahçesinde, deniz kenarında, Toroslar'ın gölgesinde.",
 bolum=[
  ("Antalya'da düğün rakamlarla",
   "<p>TÜİK'e göre Antalya'da 2025'te <strong>18.728 evlilik</strong> kaydedildi; il Türkiye'de beşinci sırada. En kalabalık ilçeler <strong>Muratpaşa (3.874)</strong> ve <strong>Kepez (3.793)</strong>; onları <strong>Alanya (2.255)</strong>, <strong>Manavgat (1.935)</strong> ve <strong>Konyaaltı (1.503)</strong> izliyor. Alanya ve Manavgat'ın kendi düğün düzeni var; merkeze bir buçuk–iki saat uzaklıkta.</p>"),
  ("İki ayrı düğün: şehir ve otel",
   "<p><strong>Şehir düğünü:</strong> Muratpaşa ve Kepez'deki salon ve bahçe düğünleri. Dış çekim için Konyaaltı sahili ve arkasında yükselen Beydağları, Kaleiçi'nin yat limanı ve falezler şehirden çıkmadan en güçlü seçenekler.</p>"
   "<p><strong>Otel ve tesis düğünü:</strong> Belek, Side, Kemer ve Alanya'daki otellerde, çoğu zaman davetlilerin de konakladığı düğünler. Tören, kokteyl ve gece aynı tesiste; çekim akışı otelin etkinlik ekibiyle birlikte kuruluyor. Misafirlerin yüzü ve otelin diğer konukları kadraja girmemeli; bunu baştan planlıyoruz.</p>"),
  ("Antalya'nın ışığı ve mevsimi",
   "<p>Yaz öğlesinde ışık sert, hava nemli ve sıcak; dış çekimi gün batımına koyuyoruz. Antalya'nın asıl avantajı ilkbahar ve sonbahar: Nisan–Haziran ve Eylül–Kasım arası deniz hâlâ güzel, sıcak yumuşamış, oteller daha sakin. Kışın bile açık ve ılık günler çok; karlı Toroslar'ın önünde bir deniz kıyısı çekimi Antalya'ya özgü bir kare.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde Antalya'daki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Otelde düğün yapıyoruz, çekimi otelle nasıl koordine ediyorsunuz?", "Otelin etkinlik ekibiyle akışı önceden konuşuyor, tören ve gece için ışık ve ses düzenini birlikte kuruyoruz."),
  ("Konyaaltı'nda dış çekim için en iyi saat ne?", "Gün batımından bir saat önce. Güneş denize batarken Beydağları sıcak bir ışık alıyor."),
  ("Alanya ya da Manavgat'taki düğünümüze geliyor musunuz?", "Evet. Mesafeyi hesaba katıp gelin alma, dış çekim ve salonu aynı güne yerleştiriyoruz."),
  ("Kışın Antalya'da dış çekim yapılabilir mi?", "Evet, çoğu gün açık ve ılık. Karlı Toroslar'ın önünde deniz kıyısı çekimi kışa özgü bir fırsat."),
 ],
 kaynak=[KAYNAK_EVLENME],
),

# ------------------------------------------------------------------ AYDIN DÜĞÜN
"aydin-dugun-cekimi": dict(
 lede="Aydın'da 2025'te 7.321 çift evlendi. Efeler'deki salon düğününden Kuşadası'ndaki sahil düğününe, Nazilli'deki köy düğününden Didim'deki gün batımı törenine kadar Aydın'ın düğünü ilçeye göre değişiyor.",
 bolum=[
  ("Aydın'da düğün rakamlarla",
   "<p>TÜİK'e göre Aydın'da 2025'te <strong>7.321 evlilik</strong> kaydedildi; bin kişide 6,26. Merkez <strong>Efeler (1.821)</strong> ilk sırada; ama <strong>Kuşadası (1.002)</strong>, <strong>Nazilli (979)</strong> ve <strong>Söke (821)</strong> da kalabalık. Didim'de 542 evlilik var ve kıyı düğünleri yaz boyunca sürüyor.</p>"
   "<p>Düğünlerin ilçelere dağılması, çekim gününde yolun önemli olduğu anlamına geliyor. Nazilli ile Kuşadası arası bir buçuk saati buluyor; gelin evi, dış çekim ve salon arasındaki mesafeyi baştan hesaplıyoruz.</p>"),
  ("Dış çekim için Aydın'ın seçenekleri",
   "<p><strong>Kuşadası:</strong> Güvercinada, marina ve sahil yolu; deniz ve gün batımı. Yaz akşamları kalabalık, erken gidip yer seçiyoruz.</p>"
   "<p><strong>Dilek Yarımadası:</strong> millî park içinde çam ormanı ve sakin koylar; doğal bir dış çekim. Millî park kurallarına uyuyor, drone için izin alıyoruz.</p>"
   "<p><strong>Zeytinlik ve incir bahçeleri:</strong> ovanın her yerinde, köylerin hemen kıyısında. Yaz sonunda incir, sonbaharda zeytin; bahçe sahibinin izniyle sakin ve sıcak tonlu bir çekim.</p>"
   "<p><strong>Didim:</strong> Apollon Tapınağı'nın sütunları ve deniz kıyısında gün batımı. Tapınak ören yeri; kısa çekim için de izin gerekiyor.</p>"),
  ("Ege düğününün akışı",
   "<p>Aydın'da köy düğünlerinde zeybek hâlâ gecenin önemli anlarından biri. Zeybeği yere yakın bir kamerayla, ağır ritmine uygun uzun planlarla çekiyoruz. Yaz düğünleri genellikle açık havada ve gece geç saate kadar; ışığı baştan planlıyor, gerekirse ek ışık getiriyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Kuşadası'nda sahil düğünü çekiyor musunuz?", "Evet. Tören saatini gün batımına göre kurmayı, rüzgâr için mikrofonu korumalı kullanmayı öneriyoruz."),
  ("Zeybeği nasıl çekiyorsunuz?", "Yere yakın bir kamera ve ağır ritme uygun uzun planlarla. Figürün tamamı görünsün diye kesmeyi az tutuyoruz."),
  ("Açık hava gece düğünü için ek ışık getiriyor musunuz?", "Gerekiyorsa evet. Mekânın ışığına bakıp yetmiyorsa, davetlileri rahatsız etmeyecek yumuşak bir ek ışık kuruyoruz."),
  ("Nazilli'deki düğünümüze gelip Kuşadası'nda dış çekim yapabilir miyiz?", "Mümkün ama yaklaşık bir buçuk saatlik yol var. Dış çekimi düğünden önceki ya da sonraki güne koymak daha rahat."),
 ],
 kaynak=[KAYNAK_EVLENME],
),

# ------------------------------------------------------------------ BALIKESİR DÜĞÜN
"balikesir-dugun-cekimi": dict(
 lede="Balıkesir'de 2025'te 8.111 çift evlendi. Merkezdeki salon düğününden Ayvalık'ın zeytinliklerindeki açık hava törenine kadar; iki denize kıyısı olan bir ilde düğün filmi de iki ayrı karakter taşıyor.",
 bolum=[
  ("Balıkesir'de düğün rakamlarla",
   "<p>TÜİK'e göre Balıkesir'de 2025'te <strong>8.111 evlilik</strong> kaydedildi; bin kişide 6,34. Merkez ilçeler <strong>Altıeylül (1.300)</strong> ve <strong>Karesi (1.116)</strong> ilk sırada; ama <strong>Bandırma (1.097)</strong> ve <strong>Edremit (1.000)</strong> neredeyse onlar kadar kalabalık. Gönen (524), Ayvalık (505) ve Burhaniye (476) onları izliyor.</p>"),
  ("Marmara ve Ege kıyısı",
   "<p><strong>Bandırma, Erdek ve Gönen:</strong> Marmara kıyısında salon ve bahçe düğünleri. Dış çekim için Erdek'in koyları ve sahil yolu, Bandırma'nın sahil parkı; Bursa'ya bir buçuk saat mesafede.</p>"
   "<p><strong>Edremit Körfezi ve Ayvalık:</strong> zeytinliklerde, bağ evlerinde ve deniz kıyısında açık hava düğünleri. Dış çekim için Cunda'nın taş sokakları, zeytin ağaçlarının arasında ikindi ışığı ve Kaz Dağları'nın eteği. Ayvalık ve Cunda, şehir dışından gelip burada evlenen çiftlerin de tercihi.</p>"),
  ("Zeytinlikte düğün",
   "<p>Zeytinlikte açık hava düğünü Balıkesir'in Ege kıyısına özgü. Gün batımında ağaçların arasından süzülen ışık, düğün filminin en güzel dakikaları. Ama gece için ışık planı şart: zeytinlik karanlık; mekânın kurduğu ışığı görüp gerekiyorsa yumuşak bir ek ışık getiriyoruz.</p>"
   "<p>Balıkesir'de kendi ekibimizle çalışıyoruz. Edremit ve Ayvalık düğünlerinde yolu hesaba katıyor, gerekirse bir gece önceden bölgeye geçmeyi planlıyoruz.</p>"),
 ],
 sss=[
  ("Ayvalık'taki zeytinlik düğünümüzü çekiyor musunuz?", "Evet. Töreni gün batımına göre kurmayı ve gece için ışık planını mekânla birlikte yapmayı öneriyoruz."),
  ("Cunda'da dış çekim için en iyi saat ne?", "Sabah erken ya da gün batımı. Yaz öğlesi hem sıcak hem kalabalık."),
  ("Bandırma'daki düğünümüz için Bursa'dan mı geliyorsunuz?", "Evet, yaklaşık bir buçuk saatlik yol. Gelin alma saatine göre erken çıkıyoruz."),
  ("Edremit ile Ayvalık arasında dış çekim için hangisini seçmeliyiz?", "Deniz ve taş sokak istiyorsanız Cunda, orman ve dağ havası istiyorsanız Kaz Dağları'nın eteği. İkisi arası yarım saat; aynı gün ikisi de mümkün."),
 ],
 kaynak=[KAYNAK_EVLENME],
),

# ------------------------------------------------------------------ DENİZLİ DÜĞÜN
"denizli-dugun-cekimi": dict(
 lede="Denizli'de 2025'te 6.958 çift evlendi. Çoğu şehrin iki merkez ilçesinde; dış çekim için ise Denizli'nin elinde Türkiye'de başka hiçbir şehirde olmayan bir şey var: beyaz travertenler.",
 bolum=[
  ("Denizli'de düğün rakamlarla",
   "<p>TÜİK'e göre Denizli'de 2025'te <strong>6.958 evlilik</strong> kaydedildi; bin kişide <strong>6,56</strong> ile Türkiye ortalamasının (6,43) biraz üzerinde. Evliliklerin büyük kısmı iki merkez ilçede: <strong>Pamukkale (2.817)</strong> ve <strong>Merkezefendi (2.066)</strong>. Çivril (408) ve Acıpayam (311) ilçe düğünlerinin öne çıktığı yerler.</p>"),
  ("Dış çekim için Denizli'nin seçenekleri",
   "<p><strong>Pamukkale travertenleri:</strong> beyaz teraslar ve sıcak su havuzları. Ören yeri olduğu için profesyonel dış çekim izne ve kurallara bağlı: travertenlerde ayakkabıyla yürünmüyor, gelinlik ve ekipman için dikkat gerekiyor. Güneş doğarken ve batarken travertenler pembe ve altın renge dönüyor; ziyaretçinin en az olduğu saatleri seçiyoruz.</p>"
   "<p><strong>Karahayıt:</strong> Pamukkale'nin hemen yanında kırmızı travertenler; daha sakin ve izni daha kolay bir alternatif.</p>"
   "<p><strong>Bağbaşı Yaylası:</strong> teleferikle çıkılan, şehre tepeden bakan çam ormanı ve serin yayla. Yaz düğünlerinde sıcaktan kaçmak için.</p>"
   "<p><strong>Bağlar:</strong> Çal ve çevresinin bağları; yaz sonunda hasada yakın dönemde sıcak, açık planlar.</p>"),
  ("Çekim düzeni",
   "<p>Denizli yazın sıcak; travertenlerde öğle ışığı beyaz yüzeyden sert yansıyor. Dış çekimi gün batımına, gelin alma ve hazırlığı sabaha koyuyoruz. Pamukkale'de dış çekim isteyen çiftler için izin süresini düğün takvimine baştan yazıyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Pamukkale'de gelinlikle dış çekim yapılabilir mi?", "Kurallara uyarak evet; travertenlerde ayakkabısız yürünüyor ve bazı alanlar kapalı. İzin ve saat planını önceden yapıyoruz."),
  ("Pamukkale'ye alternatif bir dış çekim yeri var mı?", "Karahayıt'ın kırmızı travertenleri yakın ve daha sakin; Bağbaşı Yaylası ise orman ve şehir manzarası istiyorsanız."),
  ("Çivril ya da Acıpayam'daki düğünümüze geliyor musunuz?", "Evet. Yol süresini hesaba katıp günü buna göre planlıyoruz."),
  ("Bağbaşı Yaylası'na ekipmanla çıkılabiliyor mu?", "Evet, teleferikle ya da araçla. Yazın yayla şehirden belirgin şekilde serin; öğleden sonra çekim için iyi bir kaçış."),
 ],
 kaynak=[KAYNAK_EVLENME],
),

# ------------------------------------------------------------------ ESKİŞEHİR DÜĞÜN
"eskisehir-dugun-cekimi": dict(
 lede="Eskişehir'de 2025'te 5.768 çift evlendi; yarısından fazlası Tepebaşı'nda. Porsuk'un kıyısı, Odunpazarı'nın renkli evleri ve Sazova'nın masal şatosu, şehirden çıkmadan üç ayrı dış çekim.",
 bolum=[
  ("Eskişehir'de düğün rakamlarla",
   "<p>TÜİK'e göre Eskişehir'de 2025'te <strong>5.768 evlilik</strong> kaydedildi; bin kişide 6,24. Evliliklerin <strong>3.255'i Tepebaşı'nda</strong>, <strong>1.860'ı Odunpazarı'nda</strong>. Yani düğünlerin neredeyse tamamı şehir merkezinde; gelin evi, dış çekim ve salon birbirine yakın. Bu, Eskişehir'de dış çekime daha çok zaman ayırabilmek demek.</p>"),
  ("Dış çekim için Eskişehir'in seçenekleri",
   "<p><strong>Porsuk Çayı:</strong> köprüler, nehir kıyısı yürüyüş yolları ve gondollar. Akşam ışığında şehrin en romantik karesi; hafta sonları kalabalık, hafta içi rahat.</p>"
   "<p><strong>Odunpazarı:</strong> renkli Osmanlı evleri, cumbalar ve taş sokaklar. Dönem havası isteyen çiftler için; sabah erken saatlerde boş.</p>"
   "<p><strong>Sazova Parkı:</strong> masal şatosu, korsan gemisi ve göl. Eğlenceli, renkli ve masalsı bir dış çekim; çocuklu aile fotoğrafları için de uygun.</p>"
   "<p><strong>Kent Park ve kumsal:</strong> şehrin içinde yapay kumsal ve göl; yazın sahil havası.</p>"),
  ("Çekim düzeni",
   "<p>Eskişehir karasal iklimde: yaz akşamları serin ve uzun, kış soğuk ve çoğu zaman karlı. Karlı bir Odunpazarı sabahı çok güzel ama kısa sürmeli; araç ve sıcak mola noktasını hazır tutuyoruz. Şehir merkezinde drone çoğu yerde izne bağlı; havadan plan isteyen çiftlere uygun noktayı önceden söylüyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Porsuk'ta gondolla dış çekim yapılabilir mi?", "Evet. Gondol işletmesiyle önceden konuşup sakin bir saat seçiyoruz; köprüden ve kıyıdan da çekiyoruz."),
  ("Odunpazarı'nda dış çekim için en iyi saat ne?", "Sabah erken. Sokaklar boş, ışık evlerin renklerini yumuşak gösteriyor."),
  ("Sazova Parkı'nda çekim için izin gerekiyor mu?", "Profesyonel çekim için belediyeye bilgi veriyoruz; kısa dış çekimlerde süreç basit."),
  ("Karlı bir Odunpazarı çekimi mümkün mü?", "Kar yağışından sonraki ilk sabah en güzeli. Tarihi esnek tutup havaya göre bir gün içinde karar veriyoruz."),
 ],
 kaynak=[KAYNAK_EVLENME],
),

# ------------------------------------------------------------------ GAZİANTEP DÜĞÜN
"gaziantep-dugun-cekimi": dict(
 lede="Gaziantep'te bin kişide 7,76 evlilik var; Türkiye ortalaması 6,43. 2025'te 17.131 çiftin evlendiği şehirde düğün sezonu uzun, düğünler kalabalık ve aileler büyük.",
 bolum=[
  ("Gaziantep'te düğün rakamlarla",
   "<p>TÜİK'e göre Gaziantep'te 2025'te <strong>17.131 evlilik</strong> kaydedildi; il Türkiye'de altıncı sırada. Evliliklerin neredeyse yarısı <strong>Şahinbey'de (8.462)</strong>; onu <strong>Şehitkamil (5.653)</strong> ve <strong>Nizip (1.059)</strong> izliyor. Kaba evlenme hızı 7,76 ile Türkiye ortalamasının belirgin üzerinde: genç nüfus, büyük aileler ve uzun bir düğün sezonu.</p>"),
  ("Kalabalık düğünü çekmek",
   "<p>Gaziantep düğünlerinde davetli sayısı çoğu zaman yüzlerle ölçülüyor. Böyle bir gecede tek kamera yetmiyor: biri sahneyi ve gelin-damadı sabit takip ederken, diğeri aileyi, halayı ve önemli anları yakalıyor. Takı merasimi uzun sürebiliyor; tamamını kaydedip filmde özetliyor, istenirse ayrı bir uzun sürüm teslim ediyoruz.</p>"
   "<p>Kına gecesi ayrı bir gün ve kendi başına bir tören. Işık loş, alan dar; ikinci kamerayı sabit tutup ana kamerayla aileyi takip ediyoruz.</p>"),
  ("Dış çekim için Gaziantep'in seçenekleri",
   "<p><strong>Bey Mahallesi ve eski Antep evleri:</strong> taş avlular, ahşap kapılar ve dar sokaklar; restore konaklarda iç mekân çekimi.</p>"
   "<p><strong>Fıstık bahçeleri:</strong> şehrin hemen dışında, Ağustos–Eylül'de hasat dönemi. Sıra sıra ağaçlar ve sıcak ışık.</p>"
   "<p><strong>Zeugma (Nizip):</strong> Fırat kıyısında antik kent. Ören yeri olduğu için dış çekim izne bağlı; Fırat'ın kıyısı ise kısa çekim için güçlü bir alternatif.</p>"
   "<p>Yaz öğleden sonraları çok sıcak; dış çekimi gün batımına koyuyoruz. Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Yüzlerce davetlinin olduğu düğünü nasıl çekiyorsunuz?", "En az iki kamerayla: biri sahne ve çift için, biri aile, halay ve anlar için. Takı merasimini baştan sona kaydediyoruz."),
  ("Takı merasimini ayrıca teslim edebilir misiniz?", "Evet. Filmde kısa bir özet, isterseniz ayrı bir dosyada tam sürüm."),
  ("Fıstık bahçesinde dış çekim için ne zaman gitmeliyiz?", "Ağustos sonu–Eylül hasat döneminde. Bahçe sahibinin izniyle ve hasat işini aksatmadan."),
  ("Restore bir konakta dış çekim yapabilir miyiz?", "Evet, konak sahibinin ya da işletmenin izniyle. Avlu ve iç mekânı ışığın en yumuşak olduğu ikindi saatine koyuyoruz."),
 ],
 kaynak=[KAYNAK_EVLENME],
),

# ------------------------------------------------------------------ İSTANBUL DÜĞÜN
"istanbul-dugun-cekimi": dict(
 lede="İstanbul'da 2025'te 99.032 çift evlendi; Türkiye'deki evliliklerin yaklaşık %18'i. Bu şehirde düğün filminin en zor kısmı çoğu zaman çekim değil, trafik.",
 bolum=[
  ("İstanbul'da düğün rakamlarla",
   "<p>TÜİK'e göre İstanbul'da 2025'te <strong>99.032 evlilik</strong> kaydedildi; Türkiye toplamı 552.237. En kalabalık ilçeler <strong>Küçükçekmece (4.411)</strong>, <strong>Esenyurt (4.288)</strong>, <strong>Üsküdar (4.012)</strong>, <strong>Pendik (3.999)</strong> ve <strong>Sultangazi (3.910)</strong>. Yani düğünlerin büyük kısmı şehrin dış halkasında; dış çekim için istenen Boğaz kıyısı ise çoğu zaman bir saatten fazla uzakta.</p>"),
  ("Günü trafiğe göre kurmak",
   "<p>Gelin evi Esenyurt'ta, dış çekim Bebek'te, salon Pendik'te olan bir düğün günü, aslında yolda geçen bir gün. Bu yüzden İstanbul'da önce haritaya bakıyoruz: dış çekimi salona ya da gelin evine yakın seçmek, aynı süreyle iki kat fazla çekim demek. Avrupa yakasındaki çiftlere Belgrad Ormanı ve Kilyos, Anadolu yakasındakilere Kuzguncuk, Beykoz ve Polonezköy'ü öneriyoruz.</p>"
   "<p>Boğaz kıyısında dış çekim yapılacaksa saat çok önemli: hafta sonu öğleden sonra kıyı kalabalık; sabah erken ya da hafta içi gün batımı çok daha rahat.</p>"),
  ("İzinler",
   "<p>Sarayların, koruların ve bazı tarihî mekânların bahçelerinde profesyonel çekim izne ve ücrete bağlı; Emirgan, Yıldız ve benzeri korularda kurallar değişebiliyor. Mekânı seçtiğinizde izin durumunu ve süresini kontrol edip size söylüyoruz. Şehrin neredeyse tamamı drone için kontrollü hava sahasında; havadan plan çoğu yerde ayrı izin istiyor.</p>"
   "<p>İstanbul'da kendi ekibimizle çalışıyoruz; kurgu, renk ve yönetmenlik de bizde.</p>"),
 ],
 sss=[
  ("Boğaz'da dış çekim için en iyi saat ne?", "Hafta içi gün batımı ya da hafta sonu sabah erken. Hafta sonu öğleden sonra kıyı çok kalabalık."),
  ("Dış çekim yerini nasıl seçmeliyiz?", "Gelin evine ya da salona yakın olanı. Yolda geçen her saat, çekimden giden bir saat."),
  ("Korularda çekim için izin gerekiyor mu?", "Çoğu koruda ve saray bahçesinde profesyonel çekim izne bağlı. Mekânı seçtiğinizde kontrol edip size söylüyoruz."),
  ("Düğünümüzde drone kullanabilir miyiz?", "İstanbul'da çoğu yerde ayrı izin gerekiyor. Konuma bakıp mümkün olup olmadığını önceden söylüyoruz."),
 ],
 kaynak=[KAYNAK_EVLENME],
),

# ------------------------------------------------------------------ KOCAELİ DÜĞÜN
"kocaeli-dugun-cekimi": dict(
 lede="Kocaeli'de 2025'te 13.953 çift evlendi. Gebze'den Kartepe'ye uzanan bir ilde düğün günü; körfezin bir ucundan öbürüne trafik, ama karşılığında deniz, orman ve kar aynı ilde.",
 bolum=[
  ("Kocaeli'de düğün rakamlarla",
   "<p>TÜİK'e göre Kocaeli'de 2025'te <strong>13.953 evlilik</strong> kaydedildi; il Türkiye'de onuncu sırada, bin kişide 6,50. Düğünler iki merkeze bölünmüş durumda: batıda <strong>Gebze (2.620)</strong>, <strong>Darıca (1.489)</strong> ve <strong>Çayırova (1.312)</strong>; doğuda <strong>İzmit (2.526)</strong>, <strong>Gölcük (1.047)</strong>, <strong>Körfez (1.045)</strong> ve <strong>Başiskele (966)</strong>.</p>"
   "<p>Gebze ile Kartepe arası trafiksiz bir saat, yoğun saatte çok daha uzun. Dış çekimi düğünün yapıldığı yakaya göre seçiyoruz.</p>"),
  ("Dış çekim için Kocaeli'nin seçenekleri",
   "<p><strong>Kartepe ve Maşukiye:</strong> çam ormanı, dereler ve şelaleler; kışın karlı zirve. İzmit tarafındaki çiftler için yarım saatlik yol.</p>"
   "<p><strong>Eskihisar (Gebze):</strong> küçük bir liman, eski kale ve Osman Hamdi Bey'in evi. Gebze ve Darıca'daki çiftler için şehirden çıkmadan tarihî ve deniz kıyısı bir çekim.</p>"
   "<p><strong>Seka Park ve İzmit sahili:</strong> körfez kıyısında geniş park ve eski fabrika yapıları; akşam ışığında modern ve sade.</p>"
   "<p><strong>Kerpe ve Kandıra:</strong> Karadeniz kıyısında kayalık koylar; yaz düğünlerinde ayrı bir dış çekim günü için.</p>"),
  ("Bursa'dan bir saat",
   "<p>Kocaeli'de kendi ekibimizle çalışıyoruz; Bursa'dan Osmangazi Köprüsü üzerinden yaklaşık bir saatte geliyoruz. Düğünden önce mekânı ve dış çekim noktasını birlikte görmek isteyen çiftler için önceden bir keşif günü ayarlayabiliyoruz.</p>"),
 ],
 sss=[
  ("Kartepe'de kışın dış çekim yapılabilir mi?", "Evet. Kar yağışından sonraki ilk açık gün en iyisi; çekimi kısa tutuyor, araç ve sıcak mola noktasını hazırlıyoruz."),
  ("Gebze'deki düğünümüz için Kartepe uzak mı?", "Trafiğe göre bir saati geçebiliyor. Gebze tarafındaki çiftlere Eskihisar'ı ya da dış çekimi ayrı bir güne koymayı öneriyoruz."),
  ("Eskihisar'da çekim için izin gerekiyor mu?", "Kamuya açık liman ve sahil için kısa dış çekimde genellikle gerekmiyor; müze bahçesi için ayrıca izin alıyoruz."),
  ("Düğünden önce mekânı birlikte görebilir miyiz?", "Evet. Bursa'dan bir saat uzaktayız; önceden bir keşif günü ayarlayabiliyoruz."),
 ],
 kaynak=[KAYNAK_EVLENME],
),

# ------------------------------------------------------------------ KONYA DÜĞÜN
"konya-dugun-cekimi": dict(
 lede="Konya'da bin kişide 7,08 evlilik var; Türkiye ortalaması 6,43. 2025'te 16.540 çiftin evlendiği şehirde düğünlerin çoğu üç merkez ilçede, sezon uzun ve aileler kalabalık.",
 bolum=[
  ("Konya'da düğün rakamlarla",
   "<p>TÜİK'e göre Konya'da 2025'te <strong>16.540 evlilik</strong> kaydedildi; il Türkiye'de sekizinci sırada. Evliliklerin büyük kısmı üç merkez ilçede: <strong>Selçuklu (4.816)</strong>, <strong>Meram (3.014)</strong> ve <strong>Karatay (2.535)</strong>. <strong>Ereğli (1.111)</strong>, Akşehir (612) ve Beyşehir (515) ilçe düğünlerinin öne çıktığı yerler.</p>"),
  ("Dış çekim için Konya'nın seçenekleri",
   "<p><strong>Japon Parkı:</strong> Selçuklu'da, Japon bahçesi düzeninde havuzlar, köprüler ve ağaçlar. Şehir içinde sakin ve düzenli bir set; ilkbaharda çiçekler, sonbaharda kızıl yapraklar.</p>"
   "<p><strong>Meram bağları ve Meram çayı:</strong> şehrin eski sayfiye yeri; ağaçlık yollar, dere kıyısı ve bağ evleri.</p>"
   "<p><strong>Sille:</strong> taş evler, eski kilise ve vadi; dönem havası isteyen çiftler için şehirden yirmi dakika.</p>"
   "<p><strong>Tropikal Kelebek Bahçesi:</strong> kapalı, sıcak ve yeşil bir mekân; Konya'nın sert kışında ya da yaz sıcağında iklimden bağımsız bir dış çekim alternatifi. Çekim için işletmeden izin alıyoruz.</p>"),
  ("Konya iklimiyle çalışmak",
   "<p>Konya'da yazlar kuru ve sıcak, kışlar sert ve soğuk. Yaz düğünlerinde dış çekimi gün batımına, kış düğünlerinde öğle ışığına koyuyoruz. Kar yağmışsa Sille ve Meram çok güzel görünüyor ama çekim kısa tutulmalı.</p>"
   "<p>Kalabalık düğünlerde iki kamerayla çalışıyoruz: biri çift ve sahne için, biri aile ve önemli anlar için. Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Japon Parkı'nda dış çekim için izin gerekiyor mu?", "Profesyonel çekim için belediyeye bilgi veriyoruz; kısa çekimlerde süreç basit. Hafta içi daha sakin."),
  ("Kışın Konya'da dış çekim nerede yapılır?", "Karlıysa Sille ve Meram; çok soğuksa kapalı Kelebek Bahçesi ya da tarihî bir konağın içi."),
  ("Ereğli ya da Akşehir'deki düğünümüze geliyor musunuz?", "Evet. Mesafeyi hesaba katıp gelin alma, dış çekim ve salonu aynı güne yerleştiriyoruz."),
  ("Kalabalık düğünde kaç kamera öneriyorsunuz?", "En az iki. Biri sahne ve çifti sabit takip ederken diğeri aileyi ve önemli anları yakalıyor."),
 ],
 kaynak=[KAYNAK_EVLENME],
),

# ------------------------------------------------------------------ MERSİN DÜĞÜN
"mersin-dugun-cekimi": dict(
 lede="Mersin'de 2025'te 12.911 çift evlendi. Akdeniz'in uzun sahil şeridinde düğün; Pompeiopolis'in antik sütunları, Gözne'nin serin yaylası ve kışın bile ılık bir gün batımı.",
 bolum=[
  ("Mersin'de düğün rakamlarla",
   "<p>TÜİK'e göre Mersin'de 2025'te <strong>12.911 evlilik</strong> kaydedildi; bin kişide <strong>6,60</strong> ile Türkiye ortalamasının (6,43) üzerinde. Düğünler sahil boyunca dağılmış: <strong>Mezitli (2.576)</strong> ve <strong>Tarsus (2.450)</strong> başta; onları <strong>Toroslar (1.618)</strong>, <strong>Akdeniz (1.534)</strong>, <strong>Yenişehir (1.322)</strong>, <strong>Erdemli (1.108)</strong> ve <strong>Silifke (950)</strong> izliyor.</p>"),
  ("Dış çekim için Mersin'in seçenekleri",
   "<p><strong>Pompeiopolis (Mezitli):</strong> denize uzanan sütunlu antik cadde; Mezitli'deki çiftler için şehirden çıkmadan güçlü bir kare. Ören yeri olduğu için profesyonel çekimde izin gerekiyor.</p>"
   "<p><strong>Sahil yolu ve marina:</strong> uzun sahil parkı, yürüyüş yolu ve gün batımında tekneler. Kolay ulaşılan, düğün gününe rahat sığan bir dış çekim.</p>"
   "<p><strong>Gözne yaylası:</strong> şehrin kuzeyinde, çam ormanı ve eski yayla evleri; yazın serin. Sıcaktan kaçmak isteyen yaz düğünleri için.</p>"
   "<p><strong>Kızkalesi:</strong> denizin ortasındaki kale ve kıyıda Korykos; Erdemli ve Silifke'deki düğünler için en tanınan arka plan.</p>"),
  ("Akdeniz sıcağıyla çalışmak",
   "<p>Mersin'de yaz nemli ve sıcak; Haziran–Eylül arası dış çekimi gün batımından önceki bir saate koyuyor, makyaj ve gelinlik için gölge ve serin bir mola noktası ayarlıyoruz. Kış ise ılık ve çoğu gün açık; Kasım–Mart düğünlerinde gün boyu rahat çekim yapılabiliyor.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Pompeiopolis'te dış çekim yapılabilir mi?", "İzinle evet. Ören yeri olduğu için başvuruyu önceden yapıyoruz; sütunların denize uzandığı açı için gün batımını seçiyoruz."),
  ("Yazın Mersin'de dış çekim için en iyi yer neresi?", "Sıcaktan kaçmak istiyorsanız Gözne yaylası; deniz istiyorsanız gün batımında sahil yolu."),
  ("Tarsus ya da Silifke'deki düğünümüze geliyor musunuz?", "Evet. Yol süresini hesaba katıp günü buna göre planlıyoruz."),
  ("Kışın Mersin'de dış çekim mantıklı mı?", "Çok. Kış ılık ve çoğu gün açık; ışık yazdan daha yumuşak."),
 ],
 kaynak=[KAYNAK_EVLENME],
),

# ------------------------------------------------------------------ MUĞLA DÜĞÜN
"mugla-dugun-cekimi": dict(
 lede="Muğla'da 2025'te 6.845 evlilik kaydedildi; ama Muğla'nın düğün takvimi bu sayıdan büyük. Bodrum, Fethiye, Marmaris ve Datça, Türkiye'nin ve yurt dışının dört bir yanından gelen çiftlerin evlenmek için seçtiği yerler.",
 bolum=[
  ("Muğla'da düğün rakamlarla",
   "<p>TÜİK'e göre Muğla'da 2025'te <strong>6.845 evlilik</strong> kaydedildi; bin kişide 6,28. En kalabalık ilçeler <strong>Fethiye (1.359)</strong> ve <strong>Bodrum (1.176)</strong>; onları <strong>Milas (997)</strong>, <strong>Menteşe (759)</strong> ve <strong>Marmaris (615)</strong> izliyor. Bunlara il dışından gelip Muğla'da düğün yapan çiftler ekleniyor.</p>"),
  ("Destinasyon düğünü",
   "<p>Bodrum'da villa ve beach club, Fethiye ve Göcek'te koylar, Datça'da bağ evleri; davetliler çoğu zaman birkaç gün boyunca bölgede kalıyor. Bu düğünlerde film tek bir geceden fazlasını anlatıyor: karşılama akşamı, tören, gece ve ertesi günün brunch'ı. Çiftlerle akışı önceden konuşup hangi anların filmde yer alacağını birlikte belirliyoruz.</p>"
   "<p>Yurt dışından gelen davetlilerin olduğu düğünlerde konuşmaları ve yeminleri net kaydedip altyazılı sürüm hazırlayabiliyoruz.</p>"),
  ("Dış çekim için Muğla'nın seçenekleri",
   "<p><strong>Kayaköy (Fethiye):</strong> taş evlerden oluşan terk edilmiş köy; gün batımında yamaç boyunca uzanan duvarlar. <strong>Ölüdeniz ve Babadağ:</strong> lagün ve tepeden deniz manzarası. <strong>Akyaka ve Azmak:</strong> berrak dere, sazlık ve Gökova'nın kıyısı. <strong>Bodrum Kalesi ve yarımadanın koyları:</strong> beyaz evler, gün batımı ve tekneler.</p>"
   "<p>Muğla'da yaz rüzgârlı; açık hava törenlerinde mikrofonu rüzgâra karşı koruyor, saç ve duvak için korunaklı bir köşe seçiyoruz. Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Birkaç gün süren düğünümüzün tamamını çekiyor musunuz?", "Evet. Hangi günlerin ve anların filmde olacağını önceden konuşuyor, çekim planını buna göre kuruyoruz."),
  ("Yabancı davetliler için altyazılı film hazırlıyor musunuz?", "Evet. Konuşmaları ve yeminleri net kaydedip istediğiniz dilde altyazılı sürüm veriyoruz."),
  ("Kayaköy'de dış çekim yapılabilir mi?", "Evet; ören yeri kuralları geçerli. Gün batımına doğru, ziyaretçinin azaldığı saatte çekiyoruz."),
  ("Rüzgârlı havada yeminleri net kaydedebilir misiniz?", "Evet. Çiftin ve nikâh memurunun üzerine rüzgâra dayanıklı yaka mikrofonu takıyor, sesi ayrıca kaydediyoruz."),
 ],
 kaynak=[KAYNAK_EVLENME],
),

# ------------------------------------------------------------------ SAKARYA DÜĞÜN
"sakarya-dugun-cekimi": dict(
 lede="Sakarya'da 2025'te 7.451 çift evlendi; bin kişide 6,67 ile Türkiye ortalamasının üzerinde. Sapanca Gölü'nün kıyısı ise İstanbul'dan gelen çiftlerin de en çok tercih ettiği düğün mekânlarından.",
 bolum=[
  ("Sakarya'da düğün rakamlarla",
   "<p>TÜİK'e göre Sakarya'da 2025'te <strong>7.451 evlilik</strong> kaydedildi. Merkez ilçeler <strong>Serdivan (1.204)</strong> ve <strong>Adapazarı (1.203)</strong> neredeyse eşit; onları <strong>Erenler (818)</strong> ve <strong>Akyazı (754)</strong> izliyor. Bin kişide 6,67 ile il, Türkiye ortalamasının (6,43) üzerinde.</p>"),
  ("Sapanca'da göl kıyısı düğünü",
   "<p>Sapanca'nın kıyısındaki oteller, bahçeler ve bungalov tesisleri açık hava törenleri için Marmara'nın en sevilen yerlerinden. Göle karşı yapılan tören, arkada orman ve gün batımı. Sabah sisi varsa göl kıyısında çift çekimi için bundan güzel bir saat yok; düğün öncesi sabahı bunun için ayırmayı öneriyoruz.</p>"
   "<p>Hafta sonları göl kıyısı ve tesisler kalabalık. Tesisin diğer misafirlerini kadraja almadan çekmek için tören ve dış çekim noktasını mekânla birlikte önceden belirliyoruz.</p>"),
  ("Dış çekim için diğer seçenekler",
   "<p><strong>Poyrazlar Gölü:</strong> Adapazarı'na yakın, ağaçlarla çevrili sakin bir göl; şehirden çıkmadan doğa.</p>"
   "<p><strong>Taraklı:</strong> Osmanlı döneminden kalan ahşap konaklar ve taş sokaklar; dönem havası isteyen çiftler için bir saatlik yol.</p>"
   "<p><strong>Karasu sahili:</strong> uzun Karadeniz kumsalı; yaz düğünlerinde gün batımı.</p>"
   "<p>Sakarya'da kendi ekibimizle çalışıyoruz; Bursa'dan yaklaşık iki saatte geliyoruz. Kurgu, renk ve yönetmenlik de bizde.</p>"),
 ],
 sss=[
  ("Sapanca'daki göl kıyısı düğünümüzü çekiyor musunuz?", "Evet. Töreni gün batımına göre kurmayı, tesisle tören ve çekim noktalarını önceden belirlemeyi öneriyoruz."),
  ("Sisli göl çekimi için ne yapmalıyız?", "Düğünden önceki ya da düğün sabahını ayırmak. Sis sonbahar ve ilkbaharın serin sabahlarında daha sık."),
  ("Taraklı'da dış çekim düğünle aynı gün olur mu?", "Mesafe nedeniyle önermiyoruz; ayrı bir gün daha rahat ve ışık daha iyi."),
  ("İstanbul'dan gelen davetlilerle Sapanca'da düğün yapıyoruz, çekim planı nasıl olmalı?", "Davetlilerin varış saatine göre akış: karşılama, tören, yemek ve gece. Davetlilerin geliş ve kutlama anlarını da filme ekliyoruz."),
 ],
 kaynak=[KAYNAK_EVLENME],
),

# ------------------------------------------------------------------ TEKİRDAĞ DÜĞÜN
"tekirdag-dugun-cekimi": dict(
 lede="Tekirdağ'da 2025'te 7.237 çift evlendi; en çok düğün sahildeki Süleymanpaşa'da değil, sanayi kenti Çorlu'da yapıldı. Ama dış çekim için çiftlerin yönü genellikle denize ve bağlara dönük.",
 bolum=[
  ("Tekirdağ'da düğün rakamlarla",
   "<p>TÜİK'e göre Tekirdağ'da 2025'te <strong>7.237 evlilik</strong> kaydedildi; bin kişide 6,04. En kalabalık ilçeler <strong>Çorlu (1.706)</strong>, <strong>Çerkezköy (1.429)</strong> ve <strong>Süleymanpaşa (1.332)</strong>; onları <strong>Kapaklı (953)</strong> ve <strong>Ergene (551)</strong> izliyor. Yani düğünlerin çoğu sanayi hattında, dış çekim için istenen sahil ve bağlar ise yarım saat ile bir saat uzakta.</p>"),
  ("Dış çekim için Tekirdağ'ın seçenekleri",
   "<p><strong>Süleymanpaşa sahili:</strong> uzun sahil parkı, iskele ve gün batımı. Çorlu'dan yaklaşık yarım saat; düğün gününe sığan en kolay deniz kenarı çekimi.</p>"
   "<p><strong>Bağ evleri ve şaraphaneler:</strong> Şarköy, Mürefte ve çevresindeki bağlar. Bazı bağ evleri düğün de ağırlıyor; sıra sıra asmalar ve gün batımında denize bakan yamaçlar.</p>"
   "<p><strong>Uçmakdere:</strong> denize dik inen yeşil yamaçlar; geniş ve dramatik bir manzara. Yol virajlı ve uzun; ayrı bir dış çekim günü olarak öneriyoruz.</p>"
   "<p><strong>Kumbağ:</strong> sakin kumsal ve iskeleler; yaz düğünlerinde akşamüstü.</p>"),
  ("Çekim düzeni",
   "<p>Çorlu ve Çerkezköy'deki düğünlerde gelin alma ve salon birbirine yakın; dış çekim için sahile gidilecekse bu yolu baştan hesaplıyoruz. Kıyıda öğleden sonra rüzgâr artıyor; açık hava törenlerinde mikrofonu korumalı kullanıyor, saç ve duvak için korunaklı bir köşe seçiyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde Tekirdağ'daki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Çorlu'daki düğünümüz için dış çekimi sahilde yapabilir miyiz?", "Evet. Süleymanpaşa sahili yaklaşık yarım saat; gelin alma ile salon arasına bu süreyi koyuyoruz."),
  ("Bağ evinde düğün yapıyoruz, ne önerirsiniz?", "Töreni gün batımına göre kurmak ve gece için ışık planını mekânla birlikte yapmak. Bağda ikindi ışığı filmin en güzel dakikaları."),
  ("Uçmakdere'de dış çekim düğünle aynı gün olur mu?", "Yol uzun ve virajlı; ayrı bir gün çok daha rahat."),
  ("Rüzgârlı havada açık hava töreni nasıl çekiliyor?", "Rüzgâra dayanıklı yaka mikrofonu ve korunaklı bir tören noktası. Mekânla birlikte rüzgârı kesen bir köşe seçiyoruz."),
 ],
 kaynak=[KAYNAK_EVLENME],
),

# ------------------------------------------------------------------ TRABZON DÜĞÜN
"trabzon-dugun-cekimi": dict(
 lede="Trabzon'da 2025'te 4.674 çift evlendi. Bulutların altında kalan yaylalar, Akçaabat'ın kıyısı ve gecenin sonunda büyüyen bir horon halkası; Karadeniz düğünü, kendi ritmiyle çekilmeli.",
 bolum=[
  ("Trabzon'da düğün rakamlarla",
   "<p>TÜİK'e göre Trabzon'da 2025'te <strong>4.674 evlilik</strong> kaydedildi; bin kişide <strong>5,68</strong>. Bu oran Türkiye ortalamasının (6,43) altında; nüfusa göre düğün sayısı az ama düğünler kalabalık ve uzun. Sezon yaza yoğunlaşıyor; yayla ve dış çekim için en uygun aylar da bunlar.</p>"),
  ("Dış çekim için Trabzon'un seçenekleri",
   "<p><strong>Hıdırnebi Yaylası (Akçaabat):</strong> sabah erken saatlerde bulutların üstünde kalan yayla; aşağıda bulut denizi, yukarıda açık gök. Trabzon'un en etkileyici dış çekim karesi; çekim gün doğumunda başlıyor.</p>"
   "<p><strong>Sera Gölü:</strong> Akçaabat'ta, ormanla çevrili sakin bir göl; şehirden çıkmadan doğa.</p>"
   "<p><strong>Boztepe:</strong> şehre ve limana tepeden bakış; gün batımında şehrin ışıkları.</p>"
   "<p><strong>Atatürk Köşkü ve bahçesi:</strong> Soğuksu'da, beyaz köşk ve çam ağaçları; müze olduğu için bahçede çekim izne bağlı.</p>"),
  ("Karadeniz düğününün akışı",
   "<p>Horon gecenin doruk noktası; halka büyüdükçe kamera da içine giriyor. Bir kamera yukarıdan halkayı, diğeri içeriden ayakları ve yüzleri çekiyor. Kemençe ya da tulum canlı çalınıyorsa sesi ayrıca kaydedip kurguda öne çıkarıyoruz.</p>"
   "<p>Trabzon'da hava gün içinde değişebiliyor; yayla çekimine yedek saat ya da yedek gün koyuyoruz. Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Hıdırnebi'de bulut denizini garanti edebilir misiniz?", "Hayır, havaya bağlı. Sabah erken saatlerde ihtimal yüksek; yedek gün koyup hava tahminine göre karar veriyoruz."),
  ("Horonu nasıl çekiyorsunuz?", "Biri yukarıdan sabit, biri halkanın içinden iki kamerayla. Canlı müziği ayrıca kaydediyoruz."),
  ("Yağmur yağarsa dış çekim ne olur?", "Karadeniz'de yağmur sık; yedek gün koyuyoruz. Hafif yağmur ve sis bazen en güzel kareleri veriyor; karar o gün yerinde veriliyor."),
  ("Uzungöl'de dış çekim yapılabilir mi?", "Evet ama şehirden iki saate yakın ve yazın kalabalık. Ayrı bir gün ve sabah erken saat öneriyoruz."),
 ],
 kaynak=[KAYNAK_EVLENME],
),

# ------------------------------------------------------------------ YALOVA DÜĞÜN
"yalova-dugun-cekimi": dict(
 lede="Yalova'da 2025'te 1.968 çift evlendi. Küçük bir il, ama İstanbul'a deniz yoluyla bir saat; termal ormanı, çiçek tarlaları ve Marmara kıyısıyla şehirden kaçmak isteyen çiftler için yakın bir seçenek.",
 bolum=[
  ("Yalova'da düğün",
   "<p>TÜİK'e göre Yalova'da 2025'te <strong>1.968 evlilik</strong> kaydedildi; bin kişide <strong>6,35</strong>, Türkiye ortalamasına yakın. Yalova'nın düğün takvimi buna İstanbul'dan gelen çiftlerin kır ve bahçe düğünleri eklenince büyüyor: deniz otobüsüyle bir saat, Osmangazi Köprüsü üzerinden de yakın.</p>"),
  ("Dış çekim için Yalova'nın seçenekleri",
   "<p><strong>Termal:</strong> ormanın içinde tarihî hamamlar, eski oteller ve Sudüşen Şelalesi. Gölgeli ve serin; yaz düğünlerinde gün ortasında bile çekim yapılabiliyor. Tesislerin içinde işletmenin izniyle.</p>"
   "<p><strong>Yürüyen Köşk:</strong> deniz kıyısında, çınar ağacının dibinde tarihî köşk ve bahçesi. Müze olduğu için profesyonel çekim izne bağlı.</p>"
   "<p><strong>Çiçek tarlaları ve fidanlıklar:</strong> Yalova süs bitkisi üretiminin merkezi; ilkbaharda renk renk seralar ve tarlalar. Üreticinin izniyle, bitkilere zarar vermeden.</p>"
   "<p><strong>Çınarcık ve Esenköy sahili:</strong> küçük iskeleler ve gün batımı; karşıda adalar.</p>"),
  ("Bursa'dan bir saat",
   "<p>Yalova'da kendi ekibimizle çalışıyoruz; Bursa'dan yaklaşık bir saatte geliyoruz. Mekân ve dış çekim noktalarını düğünden önce birlikte görmek mümkün. Bir günde Termal'de orman, sahilde gün batımı ve gece salonu rahatça sığıyor; mekânlar birbirine yakın.</p>"),
 ],
 sss=[
  ("İstanbul'dan gelip Yalova'da düğün yapıyoruz, çekim nasıl planlanır?", "Davetlilerin varış saatine göre: karşılama, tören, yemek ve gece. Dış çekimi düğünden önceki sabaha ya da öğleden sonraya koyuyoruz."),
  ("Termal'de dış çekim için izin gerekiyor mu?", "Ormanlık alan ve yollar için kısa çekimde genellikle gerekmiyor; hamam ve otel içleri için işletmenin izni gerekiyor."),
  ("Çiçek tarlasında dış çekim için en iyi mevsim hangisi?", "İlkbahar. Üreticiyle önceden konuşup tarlanın en renkli olduğu haftayı seçiyoruz."),
  ("Düğünden önce mekânı birlikte görebilir miyiz?", "Evet. Bursa'dan bir saat uzaktayız; önceden bir keşif günü ayarlayabiliyoruz."),
 ],
 kaynak=[KAYNAK_EVLENME],
),

# ------------------------------------------------------------------ ADANA İŞLETME
"adana-isletme-tanitim": dict(
 lede="Adana'da bir kebapçının en güçlü reklamı, ustanın zırhı kullandığı ve kebabı közün üstüne koyduğu beş saniye. İçerik, o beş saniyeyi doğru çekmekle başlıyor.",
 bolum=[
  ("Yeme-içme: Adana'nın vitrini",
   "<p>Adana kebabı, şalgamı ve gece geç saate kadar açık kalan sofralarıyla yeme-içme, şehrin en görünür sektörü. Rekabet çok; aynı caddede onlarca kebapçı var. Burada müşteriyi durduran şey menü değil, ocağın başındaki usta: zırhla çekilen kıyma, şişe sarılan et, közün üstünde dönen kebap. Zırhın tahtaya vuruşu ve közün cızırtısı da görüntü kadar önemli; sesi ayrı mikrofonla kaydediyoruz.</p>"
   "<p>Adana yazın gece yaşayan bir şehir. Yaz aylarında akşam ve gece servisini, Seyhan kıyısındaki terasları ve kalabalığı çekiyor; içerikleri akşam yemeği kararının verildiği öğleden sonra saatlerine göre paylaşmayı öneriyoruz.</p>"),
  ("Festival ve sezon",
   "<p>Nisan'daki Portakal Çiçeği Karnavalı ve sonbahardaki lezzet festivali, şehre dışarıdan ziyaretçi getiren iki dönem. İşletmeler için bu haftalar, yeni müşteriye ulaşmanın en kolay zamanı; festival öncesinde yayına girecek içeriği bir ay önceden çekiyoruz.</p>"),
  ("Üretici ve sanayi firmaları",
   "<p>Adana'nın organize sanayi bölgelerinde tekstil, gıda ve plastik üreticileri var. Bu firmalar için çekim mutfaktan çok farklı: makine parkının genişliği, hattın hızı, depodaki düzen. Pamuktan kumaşa ya da tarladan pakete giden yolu tek filmde anlatıyoruz.</p>"
   "<p>Restoran ve kafeler için aylık pakette çekim gününü sıcaktan etkilenmeyen bir saate sabitliyoruz. Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Kebapçımız için en etkili video hangisi?", "Ocağın başından kısa ve yakın planlar: zırh, şiş, köz. Dikey ve sesli; ilk saniyede ateş görünmeli."),
  ("Yazın gece servisini çekebilir misiniz?", "Evet. Akşam ışığında teras ve kalabalık, gece servisinde mutfak ve sofra. Işığı mekânın kendi ışığına göre kuruyoruz."),
  ("Festival dönemi için içerik ne zaman çekilmeli?", "Festivalden bir ay önce. İçerik festival haftasından önce yayında olmalı."),
  ("Fabrikamız için tanıtım filmi yapıyor musunuz?", "Evet. Üretim kapasitesi, kalite ve sevkiyatı anlatan ana film ve fuar için sessiz döngü sürümü hazırlıyoruz."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ ANKARA İŞLETME
"ankara-isletme-tanitim": dict(
 lede="Ankara'da işletme tanıtımının iki ayrı müşterisi var: Tunalı'daki kafe ve Bahçelievler'deki restoran gibi şehrin içine konuşan işletmeler, bir de teknoparklardaki yazılım ve savunma firmaları gibi dünyaya konuşanlar.",
 bolum=[
  ("Kafe, restoran ve mağaza",
   "<p>Tunalı Hilmi, Bahçelievler 7. Cadde, Kızılay ve Çayyolu, Ankara'nın kafe ve restoran yoğunluğunun en yüksek olduğu yerler. Müşteri çoğunlukla öğrenci, genç çalışan ve aileler; karar telefonda ve hızlı veriliyor. Kısa dikey videolar, menüdeki yeni ürün ve mekânın atmosferi bu kitleye en hızlı ulaşan içerik.</p>"
   "<p>Ankara'da hava mevsime göre çok değişiyor; kışın kapalı, sıcak ve samimi mekân; yazın teras ve bahçe. İçerik takvimini mevsim geçişlerine göre kuruyoruz.</p>"),
  ("Teknopark ve savunma firmaları",
   "<p>Ankara'nın üniversite teknoparkları ve organize sanayi bölgeleri, yazılım, elektronik ve savunma sanayi firmalarıyla dolu. Bu firmaların tanıtım filmi yatırımcıya, fuara ve yabancı müşteriye gidiyor. Ürün çoğu zaman bir yazılım ya da gizli bir sistem; kamerayla gösterilemeyen kısımları 3D animasyon ve ekran grafikleriyle anlatıyoruz.</p>"
   "<p>Gizlilik gereken tesislerde çekim yapılacak alanları ve kadraja girmeyecek şeyleri firmayla birlikte önceden belirliyor, çekilen her kareyi teslimden önce onayınıza sunuyoruz.</p>"),
  ("Kamu ve kurum",
   "<p>Başkentte dernekler, vakıflar, meslek odaları ve kurumlar da tanıtım filmi ve etkinlik videosu istiyor: kongre, panel, açılış. Bu işlerde hızlı teslim önemli; etkinlikten sonraki gün paylaşılacak kısa özeti ayrıca hazırlıyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde Ankara'daki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Kafemiz için ayda kaç video yeterli?", "Haftada bir ya da iki paylaşım için ayda 4–8 video yeterli. Pakete göre 12'ye kadar çıkıyoruz."),
  ("Yazılım firmasıyız, ürünümüzü nasıl gösterirsiniz?", "Ekip ve ofis çekimi, ekran kayıtlarından hazırlanan arayüz grafikleri ve gerekirse 3D animasyonla. Teknik olmayan bir izleyicinin de anlayacağı bir dille."),
  ("Gizlilik gereken bir tesiste çekim yapabilir misiniz?", "Evet. Çekim alanını önceden birlikte belirliyor, her kareyi teslimden önce onayınıza sunuyoruz."),
  ("Etkinlik videosunu ne kadar sürede teslim ediyorsunuz?", "Kısa özet ertesi gün; tam kurgu birkaç gün içinde."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ ANTALYA İŞLETME
"antalya-isletme-tanitim": dict(
 lede="Antalya'da bir otelin, bir tur şirketinin ya da Kaleiçi'ndeki bir restoranın müşterisi bu şehirde yaşamıyor. Müşteri Rusya'da, Almanya'da, İngiltere'de; tatil kararını aylar önce telefonundan veriyor.",
 bolum=[
  ("Otel ve turizm: sezon öncesi",
   "<p>Antalya'da turizm işletmeleri için en önemli içerik, sezon başlamadan, kış ve ilkbaharda yayına girenler. Tatilci rezervasyonunu aylar önce yapıyor; bu yüzden içeriği sezon dışında çekmek gerekiyor. Avantajı da var: tesis boş, havuz ve plaj misafirsiz, ışık yumuşak.</p>"
   "<p>Antalya'ya gelen misafir çok dilli; tanıtım filmini altyazı ve seslendirmeyle İngilizce, Almanca, Rusça ya da ihtiyaç duyulan dilde hazırlıyoruz. Otelin kendi sosyal medyası için ayrıca dikey ve kısa sürümler veriyoruz.</p>"),
  ("Restoran ve kafe: iki ayrı kitle",
   "<p>Kaleiçi, Konyaaltı ve Lara'daki restoranların yazın müşterisi turist, kışın şehirde yaşayanlar. İçerik de buna göre değişmeli: yazın çok dilli, manzara ve deneyim odaklı; kışın yerel, kampanya ve tekrar ziyaret odaklı. Aylık pakette bu iki mevsim için iki ayrı takvim kuruyoruz.</p>"),
  ("Seracılık ve tarım ihracatı",
   "<p>Kumluca, Demre ve Serik'teki seralar Türkiye'nin meyve ve sebze ihracatının önemli bir parçası. İhracatçı firmalar için seradan paketlemeye, soğuk zincirden sevkiyata kadar süreci anlatan bir tanıtım filmi, yabancı alıcıya güven veren en somut belge. Seranın ölçeğini drone ile havadan, iç süreçleri yerden çekiyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde Antalya'daki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Otelimizin tanıtım filmini ne zaman çekmeliyiz?", "Sezon dışında, Kasım–Nisan arası. Tesis boş, ışık yumuşak ve film rezervasyon döneminden önce hazır oluyor."),
  ("Rusça ve Almanca seslendirme yapabiliyor musunuz?", "Evet, profesyonel seslendirme sanatçılarıyla. Altyazı her dilde mümkün."),
  ("Misafirler varken çekim yapılabilir mi?", "Önermiyoruz. Misafirlerin yüzü kadraja girmemeli; boş saatleri ya da sezon dışını tercih ediyoruz."),
  ("Seramız için ihracat filmi nasıl olmalı?", "Kısa ve somut: seranın ölçeği, hasat, paketleme, soğuk zincir ve sevkiyat. 2–3 dakika yeterli."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ AYDIN İŞLETME
"aydin-isletme-tanitim": dict(
 lede="Aydın inciri ve zeytinyağı Türkiye'nin dört bir yanına ve dünyaya gidiyor; ama üreticinin çoğu hâlâ kendi hikâyesini anlatmıyor. Bahçeden şişeye kadar olan yolculuk, Aydın'ın en güçlü tanıtım malzemesi.",
 bolum=[
  ("Üretici ve e-ticaret",
   "<p>Aydın'da incir, zeytin ve zeytinyağı üreticileri giderek daha fazla internetten, doğrudan tüketiciye satıyor. Bu satışta müşteri ürünü dokunmadan alıyor; güveni, ürünün nereden geldiğini görmek veriyor. Bahçeden kısa planlar, hasat, kurutma ya da sıkım ve paketleme; 30–60 saniyelik videolarla ürün sayfasını ve sosyal medyayı besliyoruz.</p>"
   "<p>Hasat dönemleri içerik takviminin omurgası: incirde yaz sonu, zeytinde sonbahar ve kış. Bu dönemleri yıl başında takvime koyuyor, her hasatta bir çekim günü yapıyoruz.</p>"),
  ("Kuşadası ve Didim: turizm",
   "<p>Kuşadası'nın kruvaziyer limanı, oteller, restoranlar ve tur şirketleri; Didim'in sahil işletmeleri. Turizm işletmeleri için içeriği sezon başlamadan çekmeyi, yabancı ziyaretçiye konuşacak sürümleri altyazılı hazırlamayı öneriyoruz. Kruvaziyer gemilerinin yanaştığı günlerde liman ve çarşı çevresinin hareketi de içeriğe malzeme oluyor.</p>"),
  ("Efeler ve Nazilli: şehir işletmeleri",
   "<p>Aydın merkezi ve Nazilli'deki kafe, restoran ve mağazaların müşterisi şehirde yaşıyor. Burada içerik ilk ziyareti değil, tekrar gelmeyi hedefliyor: yeni ürün, kampanya, mekânın atmosferi. Haritada aranan bir işletme için profildeki fotoğrafların güncel olması da önemli; çekim gününde onları da yeniliyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("İnternetten incir satıyoruz, video satışları artırır mı?", "Müşteri ürünü dokunmadan alıyor; bahçeyi, hasadı ve paketlemeyi görmek güven veriyor. Ürün sayfasına ve sosyal medyaya kısa videolar öneriyoruz."),
  ("Zeytinyağı için en iyi çekim dönemi hangisi?", "Hasat ve sıkım dönemi, yani sonbahar ve kış. Bahçeden şişeye kadar olan yolu tek seferde çekiyoruz."),
  ("Kuşadası'ndaki otelimiz için içerik ne zaman çekilmeli?", "Sezon başlamadan, ilkbaharda. İçerik rezervasyon döneminden önce hazır oluyor."),
  ("Hasat dışında da içerik çıkar mı?", "Evet: paketleme, tadım, ürünle yapılan tarifler ve müşteri yorumları yıl boyu içerik sağlıyor."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ BALIKESİR İŞLETME
"balikesir-isletme-tanitim": dict(
 lede="Ayvalık'ta bir butik otel, Edremit'te bir zeytinyağı fabrikası, Susurluk'ta bir mandıra, Bandırma'da bir lojistik firması. Balıkesir'de her işletme aynı ilde ama bambaşka bir müşteriye konuşuyor.",
 bolum=[
  ("Zeytinyağı ve süt ürünleri",
   "<p>Edremit Körfezi'nin zeytinyağı ve Susurluk, Gönen çevresinin süt ürünleri Balıkesir'in en tanınan markaları. Bu üreticiler için içerik, ürünün nereden geldiğini gösteren bir yolculuk: zeytinlikten sıkıma, mandıradan şişeye. Hasat ve üretim dönemlerini takvime koyup her dönemde bir çekim günü yapıyoruz.</p>"),
  ("Ayvalık, Cunda ve körfez: turizm",
   "<p>Ayvalık ve Cunda'daki butik oteller, pansiyonlar ve restoranlar, Akçay ve Altınoluk'taki yaz işletmeleri. Müşteri çoğunlukla İstanbul, Bursa ve İzmir'den; tatil kararını bahardan veriyor. İçeriği sezon başlamadan, Nisan–Mayıs'ta çekmeyi öneriyoruz: sokaklar boş, deniz güzel, ışık yumuşak.</p>"
   "<p>Butik otellerde odayı değil deneyimi göstermek gerekiyor: sabah kahvaltısı, avlu, sokağa açılan pencere, akşam yemeği. Kısa dikey videolar ve web sitesi için daha uzun bir tanıtım sürümü hazırlıyoruz.</p>"),
  ("Merkez ve Bandırma",
   "<p>Balıkesir merkezde ve Bandırma'da kafe, restoran ve mağazaların yanında, limana ve sanayiye bağlı firmalar var. Lojistik ve sanayi firmaları için tesisin ölçeğini ve limana yakınlığını havadan da gösteren bir tanıtım filmi; şehir işletmeleri için ise düzenli, kısa ve dikey içerik.</p>"
   "<p>Balıkesir'de kendi ekibimizle çalışıyoruz; Bandırma Bursa'ya yaklaşık bir buçuk saat.</p>"),
 ],
 sss=[
  ("Butik otelimiz için hangi içerik daha çok rezervasyon getirir?", "Deneyimi gösteren kısa videolar: kahvaltı, avlu, oda manzarası, akşam. Bahar sonunda yayında olmalı."),
  ("Zeytinyağı markamız için ne zaman çekim yapmalıyız?", "Hasat ve sıkım döneminde; ardından şişeleme ve paketleme. Bir çekim günüyle bütün yolculuğu anlatabiliyoruz."),
  ("Bandırma'daki firmamız için drone çekimi de yapıyor musunuz?", "Evet. Askerî hava üssüne yakın konumlarda izin gerekebiliyor; tesisin konumunu kontrol edip önceden söylüyoruz."),
  ("Yaz işletmesiyiz, kışın içerik gerekiyor mu?", "Az ama evet. Geçen sezonun en iyi anlarını ve gelecek sezonun hazırlığını paylaşmak, müşteriyi bahar kararına kadar sıcak tutuyor."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ DENİZLİ İŞLETME
"denizli-isletme-tanitim": dict(
 lede="Denizli'nin havlusu ve bornozu dünyanın dört bir yanındaki otellerde. Ev tekstili ihracatçısından Karahayıt'taki termal otele, mermer ocağından şehir merkezindeki kafeye, Denizli'de tanıtım filmi önce ürünün dokusunu göstermeli.",
 bolum=[
  ("Tekstil ihracatçıları",
   "<p>Denizli, ev tekstili ve havlu ihracatında Türkiye'nin en güçlü şehirlerinden biri. Bu firmaların tanıtım filmi yabancı alıcıya ve fuar standına gidiyor; alıcının görmek istediği şey iplikten sevkiyata üretimin her aşaması, kapasite ve kalite kontrol. Kumaşın dokusunu makro planlarla, dokuma salonunun büyüklüğünü geniş planlarla gösteriyoruz.</p>"
   "<p>Katalogdaki her koleksiyon için 15–20 saniyelik ürün videosu, alıcının numune istemeden önce dokuyu görmesini sağlıyor.</p>"),
  ("Mermer ve doğal taş",
   "<p>Denizli çevresinde traverten ve mermer ocakları ile işleme tesisleri var. Bu firmalar için ocağın ölçeğini drone ile, blok kesimini ve yüzey işlemeyi yakından çekiyoruz. Taşın rengini ve damarını doğru göstermek için ışığı kontrollü kuruyoruz; renk düzenlemesi bu işlerde çok önemli.</p>"),
  ("Termal turizm ve şehir işletmeleri",
   "<p>Pamukkale ve Karahayıt'taki termal oteller yıl boyu misafir ağırlıyor; içerik de mevsime göre değişmeli: kışın sıcak havuz ve buhar, yazın açık havuz ve traverten manzarası. Şehir merkezindeki kafe, restoran ve mağazalar için ise düzenli, kısa içerik.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Fuara yetişmesi gereken bir film var, ne kadar önce başlamalıyız?", "Çekim bir iki gün, kurgu ve renk bir haftaya yakın. Fuar tarihinden en az üç hafta önce başlamayı öneriyoruz."),
  ("Kumaşın dokusunu videoda nasıl gösteriyorsunuz?", "Makro lens, yan ışık ve yavaş kamera hareketi. Havlunun yumuşaklığını görünür kılan planlar ürün filminin en etkili kısmı."),
  ("Mermer ocağını çekerken üretim durur mu?", "Hayır. İş güvenliği kurallarınıza göre, patlatma ve yükleme saatlerinin dışında çekiyoruz."),
  ("Termal otelimiz için kışın çekim yapmak mantıklı mı?", "Çok. Soğuk havada sıcak havuzdan yükselen buhar, termal otelin en güçlü görüntüsü."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ ESKİŞEHİR İŞLETME
"eskisehir-isletme-tanitim": dict(
 lede="Eskişehir'de üç üniversitenin öğrencisi var ve şehrin kafeleri, restoranları ve mağazaları her Eylül yeni bir müşteri kitlesiyle tanışıyor. İçerik takvimi de okul takvimine göre kurulmalı.",
 bolum=[
  ("Öğrenci şehrinde içerik takvimi",
   "<p>Eskişehir'de Eylül ve Ekim, şehre yeni gelen binlerce öğrencinin mekân keşfettiği aylar. Bu dönemde yayında olan kafe ve restoranlar, yıl boyu gelecek müdavimleri kazanıyor. Yaz aylarında ise şehir sakinleşiyor; kampanya ve içerik buna göre değişmeli. Aylık pakette okul takvimine göre bir içerik takvimi kuruyoruz: Eylül'de tanışma, kışın sıcak mekân, sınav haftalarında çalışma köşesi.</p>"
   "<p>Öğrenci kitlesi içeriği telefonda ve hızlı tüketiyor. Kısa, dikey, müzikli ve mekânın atmosferini gösteren videolar; menü ve fiyatın net okunduğu bir görsel dil.</p>"),
  ("Yerel lezzet ve zanaat",
   "<p>Çibörek, met helvası ve Eskişehir'e özgü lületaşı işçiliği, şehre gelen ziyaretçinin aradığı şeyler. Odunpazarı'ndaki atölyeler ve dükkânlar için ustanın elini, işin aşamalarını ve ürünün dokusunu gösteren kısa videolar, hem ziyaretçiye hem internetten satışa konuşuyor.</p>"),
  ("Sanayi: raylı sistem, havacılık, beyaz eşya",
   "<p>Eskişehir Türkiye'nin raylı sistem, havacılık ve beyaz eşya üretiminde güçlü şehirlerinden biri; organize sanayi bölgesinde bu sektörlere tedarik yapan yüzlerce firma var. Bu firmalar için tanıtım filmi tedarik zincirindeki büyük müşteriye ve fuara gidiyor: kalite belgeleri, hassas üretim ve ölçüm süreçleri. Gizlilik gereken parçaları 3D animasyonla gösteriyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Kafemiz için içerik ne zaman yayında olmalı?", "Eylül başında. Yeni öğrencilerin şehri keşfettiği ilk haftalar yıl boyu müşteri kazanmanın en iyi zamanı."),
  ("Lületaşı atölyemiz için video internetten satışı artırır mı?", "Ürünü dokunmadan alan müşteri için ustanın elini ve işin aşamalarını görmek güven veriyor. Kısa videolar ürün sayfasında çok işe yarıyor."),
  ("Tedarikçi firmayız, müşterimiz gizlilik istiyor. Ne yapabiliriz?", "Çekim alanını önceden belirliyor, hassas parçaları 3D animasyonla anlatıyoruz. Her kare teslimden önce onayınıza sunuluyor."),
  ("Yazın öğrenciler gidince içerik ne olmalı?", "Şehirde kalanlara ve ziyaretçiye konuşan içerik: Porsuk kıyısı, teras, yaz menüsü. Yaz aylarında paketi küçültmek de mümkün."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ GAZİANTEP İŞLETME
"gaziantep-isletme-tanitim": dict(
 lede="Gaziantep UNESCO'nun gastronomi şehirleri ağında. Baklavacının tezgâhı, kebapçının ocağı ve bakırcının çekici; Gaziantep'te bir işletmenin en güçlü içeriği, ustanın elinde.",
 bolum=[
  ("Gastronomi: ustayı göstermek",
   "<p>Gaziantep'te baklava, kebap ve yöresel yemek işletmeleri çok; aynı caddede onlarca usta. Müşteri ustanın elinden gözünü alamıyor: neredeyse şeffaf açılan yufka, kat kat serilen fıstık, tepsiye dökülen sıcak şerbet. Bu anları makro lensle ve ışığı yandan vererek çekiyoruz.</p>"
   "<p>Baklava ve fıstık ürünleri internetten Türkiye'nin her yerine ve yurt dışına satılıyor. Ürün sayfası ve sosyal medya için kısa videolar, paketlemenin ve kargonun özenini gösteren planlarla birlikte, uzaktaki müşteriye güven veriyor.</p>"),
  ("İhracatçı üreticiler",
   "<p>Gaziantep, makine halısı, tekstil, gıda ve plastikte Türkiye'nin en büyük ihracatçı şehirlerinden biri. Yabancı alıcı fabrikayı ziyaret etmeden önce filmi izliyor; bu yüzden film bir fabrika turu gibi kurulmalı: giriş, makine parkı, kalite odası, depo. Halı gibi desen ve renk ağırlıklı ürünlerde, ürünün dokusunu ve rengini doğru göstermek için ışığı kontrollü kuruyoruz.</p>"
   "<p>Orta Doğu ve Avrupa'daki alıcılar için Arapça ve İngilizce altyazılı sürümler hazırlıyoruz.</p>"),
  ("Aylık içerik",
   "<p>Baklavacı, kebapçı ve kahvehaneler için en verimli düzen aylık tek bir çekim günü: aynı gün mutfak, servis ve müşteri anlarını toplayıp bir ayın paylaşımını çıkarıyoruz. Bayram ve sezon öncesi haftaları takvime ayrıca koyuyoruz. Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Baklavacımız için en etkili video hangisi?", "Yufkanın açıldığı, fıstığın serpildiği ve şerbetin döküldüğü anlar. Dikey, kısa ve sesli; ilk saniyede ürünün çıtırtısı duyulmalı."),
  ("İnternetten satış için ürün videosu çekiyor musunuz?", "Evet. Ürün, paketleme ve kargo özenini gösteren kısa videolar hazırlıyoruz."),
  ("Halı fabrikamız için filmi hangi dillerde hazırlıyorsunuz?", "Arapça ve İngilizce en sık istenenler; diğer diller için de altyazı ve seslendirme ekleyebiliyoruz."),
  ("Bayram öncesi için içerik ne zaman çekilmeli?", "Bayramdan iki üç hafta önce. Sipariş ve kargo kararı bayramdan önceki haftalarda veriliyor."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ İSTANBUL İŞLETME
"istanbul-isletme-tanitim": dict(
 lede="İstanbul'da bir kafenin rakibi aynı sokaktaki on kafe, bir markanın rakibi ise aynı gün aynı ekranda gösterilen yüzlerce marka. Burada içerik çok; fark eden, ilk iki saniyede durduran içerik.",
 bolum=[
  ("Kalabalık bir ekranda öne çıkmak",
   "<p>İstanbul'da kullanıcı her gün yüzlerce işletme videosu görüyor. Bu kalabalıkta işe yarayan içerik ilk iki saniyede durduruyor: güçlü bir açılış planı, net bir ürün, gerçek bir insan. Uzun ve genel tanıtım filmi yerine, her biri tek bir şeyi anlatan kısa videolar öneriyoruz: bir ürün, bir usta, bir an.</p>"
   "<p>Aylık pakette ayda 4–12 kısa video çekip kurguluyoruz. Birden fazla şubesi olan işletmeler için şubeleri trafiğe göre gruplayıp aynı çekim gününe koyuyoruz.</p>"),
  ("Marka ve e-ticaret",
   "<p>İstanbul, e-ticaret markalarının ve yeni kurulan markaların merkezi. Bu markalar için ürün videosu, kullanım videosu ve reklam kesimleri; aynı çekimden web sitesi, pazaryeri sayfası ve sosyal medya için ayrı formatlar çıkarıyoruz. Gerektiğinde stüdyo yerine gerçek bir mekânda, ürünün kullanıldığı ortamda çekiyoruz.</p>"),
  ("Bursa'dan İstanbul'a",
   "<p>İstanbul'da kendi ekibimizle çalışıyoruz; Bursa'dan deniz otobüsü ya da otoyolla yaklaşık iki saatte geliyoruz. İstanbul'un trafiğinde bir çekim gününün ne kadar sürdüğünü baştan planlamak bütçenin önemli bir kısmı; mekânları birbirine yakın seçip yolda geçen zamanı azaltıyoruz.</p>"
   "<p>Google işletme profilinizin fotoğraflarını da aynı çekim gününde yeniliyoruz; haritada görünürlük, İstanbul'daki yerel aramalarda en çok fark yaratan şeylerden biri.</p>"),
 ],
 sss=[
  ("İstanbul'da birden fazla şubemiz var, nasıl planlıyorsunuz?", "Şubeleri yakaya ve trafiğe göre gruplayıp aynı güne koyuyoruz; her şube için ayrı içerik çıkarıyoruz."),
  ("E-ticaret markamız için hangi videolar gerekli?", "Ürün videosu, kullanım videosu ve reklam kesimleri. Aynı çekimden web, pazaryeri ve sosyal medya için ayrı formatlar hazırlıyoruz."),
  ("İstanbul'a kendi ekibinizle mi geliyorsunuz?", "Evet. Bursa'dan yaklaşık iki saatte geliyoruz; çeken ve kurgulayan aynı kişiler."),
  ("Reklam için ayrı çekim gerekiyor mu?", "Gerekmiyor. Aynı çekim gününden organik paylaşım ve reklam için ayrı kesimler çıkarıyoruz."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ İZMİR İŞLETME
"izmir-isletme-tanitim": dict(
 lede="Kemeraltı'nın esnafı, Alsancak'ın kafeleri, Urla'nın bağları, Çeşme'nin yaz otelleri ve Çiğli'nin fabrikaları. İzmir'de işletme tanıtımı, aynı şehirde dört ayrı dil konuşmayı gerektiriyor.",
 bolum=[
  ("Şehir işletmeleri: kafe, restoran, mağaza",
   "<p>Alsancak, Karşıyaka ve Bornova'daki kafe ve restoranların müşterisi şehirde yaşıyor ve sık geliyor. İçerik ilk ziyareti değil, tekrar gelmeyi hedeflemeli: yeni menü, sabah kahvaltısı, akşam atmosferi. Boyoz, kumru ya da gevrek gibi İzmir'e özgü ürünler, kısa videolarda en çok ilgi gören içerik. Sabah ve akşam iki ayrı atmosferi aynı gün çekmek için çekim gününü öğleden sonraya yayıyoruz.</p>"
   "<p>Kemeraltı'ndaki esnaf için ise içerik ustalığı ve geleneği göstermeli: çarşının sesi, ustanın eli, yıllardır aynı yerde duran dükkân.</p>"),
  ("Bağ, zeytin ve yaz turizmi",
   "<p>Urla ve Seferihisar'ın bağ ve zeytin üreticileri, Çeşme ve Alaçatı'nın butik otelleri ve restoranları. Bu işletmelerin müşterisi şehir dışından, çoğu zaman yurt dışından geliyor; karar sezondan aylar önce veriliyor. İçeriği bahar başında, yer boşken ve ışık yumuşakken çekip sezon öncesi yayına koymayı öneriyoruz.</p>"),
  ("Sanayi ve fuar",
   "<p>Çiğli ve Kemalpaşa'daki organize sanayi bölgelerinde gıda, makine ve tekstil üreticileri; İzmir'in fuar takvimi de bu firmalar için önemli bir vitrin. Fuar standı için sessiz döngü videosu ve yabancı alıcı için altyazılı tanıtım filmi hazırlıyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde İzmir'deki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Boyoz ya da kumru gibi yerel ürünleri öne çıkarmalı mıyız?", "Evet. İzmir'e özgü ürünler hem şehirliye hem ziyaretçiye konuşuyor ve paylaşımda en çok ilgiyi görüyor."),
  ("Çeşme'deki otelimiz için içerik ne zaman çekilmeli?", "Nisan–Mayıs. Tesis boş, ışık yumuşak ve içerik rezervasyon döneminden önce hazır."),
  ("Fuar için ne tür video hazırlıyorsunuz?", "Standda dönecek sessiz döngü video, yabancı alıcı için altyazılı tanıtım filmi ve sosyal medya için kısa kesimler."),
  ("Kemeraltı'nda çekim için izin gerekiyor mu?", "Dükkânın içi için sizin izniniz yeterli; çarşı içinde kısa çekimlerde komşu esnafla önceden konuşuyoruz."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ KAYSERİ İŞLETME
"kayseri-isletme-tanitim": dict(
 lede="Kayseri'de mobilya fabrikaları dünyaya ihracat yapıyor, pastırmacılar ve mantıcılar ise Türkiye'nin her yerine kargo gönderiyor. Kayseri esnafının hikâyesi tezgâhtan çok daha büyük.",
 bolum=[
  ("Mobilya ve sanayi",
   "<p>Kayseri, Türkiye'nin mobilya, yatak ve ev tekstili üretiminde en büyük merkezlerinden biri; organize sanayi bölgesinde metal, makine ve gıda üreticileri de var. Mobilya firmaları için tanıtım iki parçalı: fabrikada üretimin ölçeği ve kalitesi, showroom ya da gerçek bir evde ürünün nasıl yaşandığı. Fabrikayı geniş planlarla, ürünü sıcak ışıkta ve kullanılırken çekiyoruz.</p>"
   "<p>Bayilere, mağazalara ve yurt dışındaki alıcıya gidecek katalog videoları için her ürün grubuna kısa bir video hazırlıyoruz; aynı çekim gününden web sitesi, pazaryeri ve sosyal medya için farklı formatlar çıkıyor.</p>"),
  ("Pastırma, sucuk, mantı: lezzet esnafı",
   "<p>Kayseri'nin pastırmacıları ve şarküteri dükkânları, internetten satışla Türkiye'nin her yerine ulaşıyor. Uzaktaki müşteri için güven, ürünün nasıl yapıldığını görmek: çemenin hazırlanışı, kurutma, dilimleme. Mantıcılar için de ustanın parmaklarının arasında kapanan küçük hamur parçaları, en çok izlenen kare.</p>"
   "<p>Bayram ve kış aylarından önce sipariş yoğunlaşıyor; içeriği bu dönemlerden birkaç hafta önce çekmeyi öneriyoruz.</p>"),
  ("Erciyes ve şehir işletmeleri",
   "<p>Erciyes Kayak Merkezi'ndeki oteller ve kiralık dağ evleri için kış sezonundan önce, Ekim–Kasım'da içerik; şehir merkezindeki kafe ve restoranlar için düzenli kısa video. Üniversite çevresindeki işletmelerin müşterisi ise öğrenci; okul takvimine göre bir içerik planı kuruyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Mobilya firmamız için katalog videosu nasıl olmalı?", "Her ürün grubu için 15–30 saniye: ürünün tamamı, detay ve kullanım anı. Aynı çekimden web, pazaryeri ve sosyal medya için ayrı formatlar çıkarıyoruz."),
  ("Pastırmayı internetten satıyoruz, hangi videolar işe yarar?", "Üretimi gösteren kısa videolar: çemen, kurutma, dilimleme ve paketleme. Uzaktaki müşteri ürünün nasıl yapıldığını görünce güveniyor."),
  ("Erciyes'teki otelimiz için içerik ne zaman çekilmeli?", "Sezon öncesi tanıtım için Ekim–Kasım; karlı görüntüler için ilk kar yağışından sonra ikinci bir çekim günü."),
  ("Fabrika çekimi üretimi durdurur mu?", "Hayır. Hat çalışırken, iş güvenliği kurallarınıza uyarak çekiyoruz."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ KOCAELİ İŞLETME
"kocaeli-isletme-tanitim": dict(
 lede="Kocaeli'de işletmelerin çoğu bir başka işletmeye satış yapıyor: yan sanayi ana sanayiye, lojistik firması ihracatçıya, kimya üreticisi fabrikaya. Böyle bir müşteriye konuşan tanıtım filmi, sosyal medya videosundan çok farklı kurulmalı.",
 bolum=[
  ("Firmadan firmaya: tedarikçi tanıtımı",
   "<p>Gebze, Dilovası ve İzmit'teki organize sanayi bölgelerinde otomotiv, kimya, makine ve plastik üreticileri, büyük bir müşteriye tedarikçi olmak için yarışıyor. Satın almacının görmek istediği şey belli: kalite belgeleri, ölçüm ve test süreçleri, kapasite, teslimat güvenilirliği. Tanıtım filmini bu sorulara sırayla cevap veren bir yapıda kuruyoruz.</p>"
   "<p>Gizlilik gereken süreçlerde kamerayı izin verilen alanla sınırlıyor, gerisini 3D animasyonla anlatıyoruz. Film; satış sunumunda, web sitesinde ve tedarikçi denetimine gelen müşteriye ön bilgi olarak kullanılıyor.</p>"),
  ("Kartepe ve Maşukiye: turizm",
   "<p>Kartepe'deki kayak otelleri ve dağ evleri, Maşukiye'deki dere kenarı restoranları İstanbul'dan gelen hafta sonu misafirine konuşuyor. Bu işletmeler için kısa, mevsime göre değişen içerik: kışın kar ve şömine, yazın dere, gölge ve alabalık. Hafta sonu kararını hafta içinde veren misafire Perşembe'den önce ulaşmak gerekiyor.</p>"),
  ("Şehir işletmeleri",
   "<p>İzmit'in pişmaniyecileri, Gebze ve Darıca'nın kafe ve restoranları, üniversite çevresindeki işletmeler için düzenli kısa video ve Google işletme profili fotoğrafları. Kocaeli'de kendi ekibimizle çalışıyoruz; Bursa'dan yaklaşık bir saatte geliyoruz ve aynı gün birkaç işletmeyi çekebiliyoruz.</p>"),
 ],
 sss=[
  ("Tedarikçi firmayız, tanıtım filmi neyi anlatmalı?", "Satın almacının sorularını: kalite belgeleri, ölçüm ve test, kapasite ve teslimat. 2–3 dakikalık, net ve sade bir film."),
  ("Müşterimizin parçalarını çekemiyoruz, ne yapabiliriz?", "Kamerayı izin verilen alanla sınırlıyor, süreçleri 3D animasyonla gösteriyoruz. Her kare teslimden önce onayınıza sunuluyor."),
  ("Kartepe'deki otelimiz için ne zaman çekim yapmalıyız?", "Kış içeriği için ilk ciddi kar yağışından sonra, sezon öncesi tanıtım için Ekim–Kasım."),
  ("Aynı gün birden fazla şubeyi çekebilir misiniz?", "Evet. Gebze ve İzmit tarafındaki şubeleri trafiğe göre ayrı günlere ya da aynı güne topluyoruz."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ KONYA İŞLETME
"konya-isletme-tanitim": dict(
 lede="Konya'nın tarım makineleri dünyanın tarlalarında çalışıyor, etliekmeği ise şehre gelen herkesin ilk durağı. Aralık'taki Şeb-i Arus törenleri de her yıl şehri dünyanın dört bir yanından ziyaretçiyle dolduruyor.",
 bolum=[
  ("Tarım makinesi ve döküm üreticileri",
   "<p>Konya, tarım makineleri, döküm ve otomotiv yedek parçasında Türkiye'nin en güçlü şehirlerinden biri. Bu firmaların en ikna edici tanıtım malzemesi, makinenin tarlada çalışırken çekilmiş görüntüsü: ekim, hasat, toprak işleme. Bunu sezonuna göre tarlada, üretim sürecini ise fabrikada çekiyoruz; ikisini tek filmde birleştiriyoruz.</p>"
   "<p>Yurt dışı fuarları ve bayi ağı için altyazılı sürümler; makinenin iç yapısını göstermek gerekiyorsa 3D animasyon.</p>"),
  ("Lezzet ve turizm",
   "<p>Etliekmek, fırın kebabı ve Konya'ya özgü tatlılar şehre gelen ziyaretçinin listesinde. Bu işletmeler için en güçlü içerik fırının ağzı: uzun ekmeğin fırına girip çıktığı an, kebabın fırından çıkışı. Kısa ve sıcak videolar.</p>"
   "<p>Mevlana Müzesi çevresindeki oteller, restoranlar ve hediyelik dükkânları için yılın en yoğun dönemi Aralık'taki Şeb-i Arus haftası. Bu dönemden önce yayında olacak içeriği Ekim–Kasım'da çekmeyi öneriyoruz.</p>"),
  ("Şehir işletmeleri",
   "<p>Selçuklu ve Meram'daki kafe, restoran ve mağazalar için aylık düzenli içerik ve Google işletme profili fotoğrafları. Üniversite çevresindeki işletmelerin takvimini okul dönemine göre kuruyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Tarım makinemizi tarlada çekebilir misiniz?", "Evet, sezonuna göre. Ekim ya da hasat zamanını takvime koyuyor, makineyi çalışırken yerden ve havadan çekiyoruz."),
  ("Etliekmek salonumuz için hangi video en etkili?", "Fırının ağzından kısa planlar: ekmeğin fırına girişi ve çıkışı. Sıcak, sesli ve dikey."),
  ("Şeb-i Arus dönemi için içerik ne zaman hazır olmalı?", "Kasım sonunda. Ziyaretçi otel ve restoran kararını Aralık'tan önce veriyor."),
  ("Döküm sürecini videoda göstermek güvenli mi?", "İş güvenliği kurallarınıza uyarak, güvenli mesafeden ve uygun koruyucu ekipmanla çekiyoruz."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ MANİSA İŞLETME
"manisa-isletme-tanitim": dict(
 lede="Manisa'da bir beyaz eşya tedarikçisi, bir kuru üzüm ihracatçısı, Akhisar'da bir zeytin üreticisi ve şehir merkezinde bir kebapçı. Manisa'nın işletmeleri, ürünü gösterecek kadar hikâyeyi de anlatmalı.",
 bolum=[
  ("Manisa OSB tedarikçileri",
   "<p>Manisa Organize Sanayi Bölgesi'ndeki beyaz eşya ve elektronik üreticilerine parça, kalıp ve hizmet veren yüzlerce firma var. Bu firmaların tanıtım filmi satın almacıya ve denetime gelen müşteriye gidiyor: kalite süreçleri, ölçüm, kapasite. Gizlilik gereken ürünleri 3D animasyonla anlatıyor, kamerayı izin verilen alanla sınırlıyoruz.</p>"),
  ("Üzüm, zeytin, mesir: tarım ve gıda",
   "<p>Salihli ve Alaşehir'in kuru üzümü, Akhisar'ın sofralık zeytini, Manisa'nın mesir macunu. İhracatçı ve üreticiler için içerik bağdan ya da bahçeden başlıyor: hasat, kurutma, ayıklama, paketleme. Kuru üzümde serme dönemi, zeytinde hasat dönemi içerik takviminin en değerli haftaları.</p>"
   "<p>Mesir macunu üreten işletmeler için baharda yapılan Mesir Festivali öncesi, festivalin kalabalığına ve ziyaretçisine konuşan kısa içerik hazırlıyoruz.</p>"),
  ("Şehir işletmeleri",
   "<p>Manisa kebabı yapan lokantalar, kafe ve mağazalar için kısa ve düzenli video; Google işletme profilinin güncel fotoğrafları. Manisa İzmir'e yakın; müşterinin bir kısmı hafta sonu İzmir'den geliyor, içerik de bu kitleye ulaşacak şekilde paylaşılmalı.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("OSB'de tedarikçiyiz, müşterimiz çekime izin vermezse?", "Kamerayı izin verilen alanla sınırlıyor, ürünü ve süreci 3D animasyonla gösteriyoruz. Her kare teslimden önce onayınıza sunuluyor."),
  ("Kuru üzüm ihracatı için film ne zaman çekilmeli?", "Hasat ve serme döneminde, yaz sonunda. Bağdan paketlemeye bütün süreç aynı haftalarda çekilebiliyor."),
  ("Zeytin markamız için hangi içerik işe yarar?", "Hasat, ayıklama, salamura ve paketlemeyi gösteren kısa videolar; internetten alan müşteriye ürünün nereden geldiğini gösteriyor."),
  ("İzmir'den gelen müşteriye nasıl ulaşırız?", "İçeriği hafta sonu planının yapıldığı Perşembe–Cuma günlerinde paylaşmayı ve reklamı İzmir'e de hedeflemeyi öneriyoruz."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ MERSİN İŞLETME
"mersin-isletme-tanitim": dict(
 lede="Mersin'de tantuninin tezgâhı da var, narenciyenin ihracat paketi de, Türkiye'nin en büyük limanlarından biri de. Liman şehrinin işletmeleri hem sokaktaki müşteriye hem dünyaya konuşuyor.",
 bolum=[
  ("Tantuni, cezerye, kerebiç: sokak lezzetleri",
   "<p>Tantuni Mersin'in imzası; tezgâhta sacın üstünde pişen et, dürüm ve limon. Tarsus'un cezeryesi ve kerebici de şehre gelen ziyaretçinin listesinde. Bu işletmeler için en güçlü içerik ustanın sacın başındaki hızı: birkaç saniyelik dikey bir video, uzun bir tanıtımdan daha çok müşteri getiriyor.</p>"),
  ("Narenciye ve lojistik ihracatı",
   "<p>Mersin ve çevresinin limon, portakal ve mandalina üreticileri ve paketleme tesisleri, Mersin limanı ve serbest bölgedeki lojistik firmaları dünyaya konuşuyor. İhracat filmi için bahçeden paketleme tesisine, soğuk hava deposundan konteynere kadar süreci çekiyoruz. Hasat Kasım'dan Şubat'a kadar sürüyor; çekimi bu döneme koyuyoruz.</p>"
   "<p>Lojistik firmaları için tesisin limana yakınlığını ve depo ölçeğini havadan, operasyonu yerden gösteriyoruz. Arapça, İngilizce ya da ihtiyaç duyulan dilde altyazı ekliyoruz.</p>"),
  ("Sahil ve turizm",
   "<p>Kızkalesi, Erdemli ve Silifke'deki yaz işletmeleri, Mersin sahil yolundaki kafe ve restoranlar. Yaz işletmeleri için içeriği sezon öncesi, Mayıs'ta; şehir işletmeleri için yıl boyu düzenli kısa video ve Google işletme profili fotoğrafları.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Tantuni dükkânımız için hangi video işe yarar?", "Sacın başından birkaç saniyelik hızlı planlar: et, dürüm, limon. Dikey ve sesli; ilk saniyede ateş ve hız görünmeli."),
  ("Narenciye ihracatı için film ne zaman çekilmeli?", "Hasat döneminde, Kasım–Şubat. Bahçe, paketleme ve sevkiyat aynı haftalarda çekilebiliyor."),
  ("Liman sahasında çekim yapılabilir mi?", "Liman işletmesinin izniyle ve güvenlik kurallarına uyarak. İzni firmanızla birlikte önceden alıyoruz."),
  ("Yaz işletmemiz için içerik ne zaman hazır olmalı?", "Mayıs sonunda. Tatil kararı sezon başlamadan veriliyor."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ MUĞLA İŞLETME
"mugla-isletme-tanitim": dict(
 lede="Bodrum'da bir beach club, Göcek'te bir gulet, Fethiye'de bir yamaç paraşütü firması, Marmaris'te bir çam balı üreticisi. Muğla'nın işletmeleri yılın altı ayında kazanıyor; içerik de bu altı aydan önce hazır olmalı.",
 bolum=[
  ("Sezon öncesi içerik",
   "<p>Muğla'nın turizm işletmeleri için içeriğin en değerli zamanı sezonun kendisi değil, öncesi. Tatilci kararını Ocak ile Mayıs arasında veriyor; bu dönemde yayında olan otel, restoran ve tur firması, yazın dolu oluyor. Bu yüzden çekimi ilkbaharda, tesis hazır ama misafir yokken yapıyoruz: ışık yumuşak, deniz berrak, kadraj boş.</p>"
   "<p>Muğla'ya gelen misafirin önemli kısmı yurt dışından. Tanıtım filmlerini İngilizce ve ihtiyaç duyulan diğer dillerde altyazılı, sosyal medya sürümlerini metinsiz ve görsel ağırlıklı hazırlıyoruz.</p>"),
  ("Gulet, tekne ve aktivite",
   "<p>Bodrum, Göcek ve Marmaris'teki gulet ve yat kiralama firmaları için tekneyi denizde, seyir halinde ve koyda demirliyken çekiyoruz; kabinler, güverte, yemek ve yüzme anı. Drone ile teknenin koyla ilişkisi tek karede görünüyor. Ölüdeniz'in yamaç paraşütü, dalış ve tekne turu firmaları için aktiviteyi yaşayan misafirin bakış açısını veren aksiyon kamerası planları ekliyoruz.</p>"),
  ("Çam balı ve yerel üreticiler",
   "<p>Muğla, çam balı üretiminin merkezi. Bal üreticileri ve kooperatifler için ormandan kovana, süzmeden kavanoza giden yolu anlatan kısa videolar, internetten alan müşteriye ürünün nereden geldiğini gösteriyor. Hasat dönemi içerik takviminin en önemli haftası.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Otelimiz için içerik ne zaman çekilmeli?", "Mart–Mayıs. Tesis hazır, misafir yok, ışık yumuşak; içerik rezervasyon dönemine yetişiyor."),
  ("Guletimizi nasıl çekiyorsunuz?", "Seyir halinde ve koyda demirliyken; güverte, kabin, yemek ve yüzme anı. Drone ile tekneyi koyla birlikte gösteriyoruz."),
  ("Yabancı misafire yönelik içerik nasıl olmalı?", "Görsel ağırlıklı, metinsiz ya da altyazılı. Ana tanıtım filmi için İngilizce ve diğer dillerde altyazı ekliyoruz."),
  ("Çam balı için ne zaman çekim yapmalıyız?", "Hasat döneminde. Kovan, süzme ve kavanozlama aynı haftalarda çekilebiliyor."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ SAMSUN İŞLETME
"samsun-isletme-tanitim": dict(
 lede="Samsun, tıbbi cihaz üretiminde Türkiye'nin öncü şehirlerinden biri; Bafra pidesi ve Çarşamba ovasının sebzesi ise Karadeniz'in sofrasında. Samsun'un işletmeleri hem bir hastaneye hem bir aileye satış yapıyor.",
 bolum=[
  ("Tıbbi cihaz ve sanayi",
   "<p>Samsun'daki tıbbi cihaz üreticileri hastanelere, distribütörlere ve yurt dışına satış yapıyor. Bu firmaların tanıtım filmi için en önemli şey güven: temiz üretim alanı, kalite ve sterilizasyon süreçleri, belgeler. Temiz odalarda çekim kurallara bağlı; ekipmanı ve ekibi bu kurallara göre hazırlıyoruz. Ürünün nasıl çalıştığını anlatmak gerekiyorsa 3D animasyon ekliyoruz.</p>"
   "<p>Uluslararası fuarlar ve distribütörler için altyazılı sürümler, ürün kataloğu için her cihaza kısa bir video.</p>"),
  ("Bafra pidesi ve yerel lezzet",
   "<p>Bafra pidesinin uzun hamuru, ustanın elinde açılırken ve fırından çıkarken; Samsun'un pideci ve lokantaları için en güçlü içerik bu birkaç saniye. Çarşamba ve Bafra ovasının üreticileri için ise tarladan sofraya giden yolu anlatan kısa videolar.</p>"),
  ("Şehir işletmeleri ve üniversite",
   "<p>Atakum sahilindeki kafe ve restoranlar, üniversite çevresindeki işletmeler, şehir merkezindeki mağazalar. Atakum'da yazın müşteri sahilde, kışın şehirde; içerik takvimini mevsime göre kuruyoruz. Google işletme profilinin fotoğraflarını da aynı çekim gününde güncelliyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Temiz odada çekim yapabiliyor musunuz?", "Evet, kurallara uyarak. Ekipmanı temizlik standardınıza göre hazırlıyor, giyim ve giriş prosedürünüze uyuyoruz."),
  ("Tıbbi cihazın çalışmasını nasıl gösterirsiniz?", "Gerçek kullanım görüntüsü ve iç yapıyı gösteren 3D animasyonun birleşimiyle; teknik olmayan bir alıcının da anlayacağı sadelikte."),
  ("Pidecimiz için hangi video en etkili?", "Hamurun açıldığı ve pidenin fırından çıktığı anlar. Kısa, sıcak ve sesli."),
  ("Atakum'daki kafemiz için içerik takvimi nasıl olmalı?", "Yazın sahil ve teras, kışın sıcak iç mekân ve kampanya. Mevsim geçişlerinde içeriği değiştiriyoruz."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ TRABZON İŞLETME
"trabzon-isletme-tanitim": dict(
 lede="Trabzon'a gelen ziyaretçi Uzungöl'ü görmek, hamsi ve Akçaabat köftesi yemek, yaylada bir gece geçirmek istiyor. Bu ziyaretçinin önemli bir kısmı Körfez ülkelerinden; içerik de onların diliyle konuşmalı.",
 bolum=[
  ("Turizm: Uzungöl, yayla ve otel",
   "<p>Trabzon'un otelleri, yayla evleri, tur firmaları ve araç kiralama şirketleri için müşteri çoğu zaman yurt dışında, özellikle Körfez ülkelerinde. Tanıtım filmlerini Arapça altyazı ve gerekirse seslendirmeyle hazırlıyor, sosyal medya için görsel ağırlıklı, az metinli sürümler çıkarıyoruz.</p>"
   "<p>Karadeniz'in en güçlü görüntüsü sis ve yeşil; ama bu görüntü havaya bağlı. Yayla ve göl çekimlerine yedek gün koyuyor, sisli ve açık havayı ayrı ayrı yakalamaya çalışıyoruz.</p>"),
  ("Lezzet: hamsi, köfte, tereyağı",
   "<p>Akçaabat köftesi, kuymak, hamsi ve Trabzon ekmeği şehre gelenin listesinde. Lokantalar için ocağın başından kısa planlar; tereyağı, fındık ve yöresel ürün satan işletmeler için ise üreticiden kavanoza, yayladan dükkâna giden yolu anlatan videolar, internetten satışa güven veriyor.</p>"),
  ("Fındık ve yerel üretici",
   "<p>Trabzon'un fındık bahçeleri Ağustos'ta hasatta. Fındık ve fındık ürünleri üreten işletmeler için hasattan kırma ve paketlemeye kadar süreci çekmenin en iyi zamanı bu hafta. Şehir merkezindeki kafe ve mağazalar için ise düzenli kısa video ve Google işletme profili fotoğrafları.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Körfez ülkelerinden gelen misafire nasıl ulaşırız?", "Arapça altyazılı ya da seslendirmeli tanıtım filmi ve görsel ağırlıklı kısa videolarla. İçeriği misafirin tatil planı yaptığı dönemden önce yayına koyuyoruz."),
  ("Yayla evimiz için sisli görüntü garanti mi?", "Hayır, havaya bağlı. Yedek gün koyup hem sisli hem açık havayı yakalamaya çalışıyoruz."),
  ("Fındık ürünlerimiz için ne zaman çekim yapmalıyız?", "Ağustos hasat döneminde; kırma ve paketlemeyi aynı haftalarda çekebiliyoruz."),
  ("Lokantamız için hangi video işe yarar?", "Ocağın başından kısa planlar: kuymak, köfte, hamsi. Sıcak, sesli ve dikey."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ YALOVA İŞLETME
"yalova-isletme-tanitim": dict(
 lede="Yalova'nın termal otelleri İstanbul'dan gelen misafiri, süs bitkisi üreticileri Avrupa'daki alıcıyı, Altınova'nın tersaneleri dünyadaki armatörü bekliyor. Küçük bir ilin işletmeleri, çok farklı müşterilere konuşuyor.",
 bolum=[
  ("Termal ve turizm",
   "<p>Termal'deki oteller ve kaplıcalar, Çınarcık ve Armutlu'nun yaz işletmeleri İstanbul'a bir saat mesafede. Hafta sonu kararını hafta içinde veren İstanbullu misafire, termal suyun buharı, ormanın yeşili ve rahatlama hissi kısa videolarla ulaşıyor. Termal oteller için kış, içeriğin en güçlü olduğu mevsim: soğuk havada sıcak havuz.</p>"),
  ("Süs bitkisi ve fidan üreticileri",
   "<p>Yalova, süs bitkisi ve fidan üretiminde Türkiye'nin merkezi; üreticilerin önemli bir kısmı yurt dışına satış yapıyor. Alıcıya gidecek tanıtım filmi için seraların ölçeğini drone ile, bitkinin kalitesini ve paketleme sürecini yakından çekiyoruz. İlkbahar, seraların en dolu ve renkli olduğu dönem.</p>"),
  ("Tersane ve sanayi",
   "<p>Altınova'daki tersaneler gemi ve yat üretiyor. Tersaneler için tanıtım filmi armatöre ve uluslararası fuara gidiyor: kızak, kapasite, yapım süreci, denize indirme. Denize indirme töreni gibi tek seferlik anları kaçırmamak için takvimi tersaneyle birlikte kuruyoruz; kızaktaki gemiyi havadan da çekiyoruz.</p>"
   "<p>Yalova'da kendi ekibimizle çalışıyoruz; Bursa'dan yaklaşık bir saatte geliyoruz.</p>"),
 ],
 sss=[
  ("Termal otelimiz için hangi mevsim en iyi?", "Kış. Soğuk havada sıcak havuzdan yükselen buhar, termal otelin en güçlü görüntüsü."),
  ("Fidan ihracatı için film nasıl olmalı?", "Kısa ve somut: seraların ölçeği, bitkinin kalitesi, paketleme ve sevkiyat. İngilizce ya da ihtiyaç duyulan dilde altyazı."),
  ("Denize indirme törenini çekebilir misiniz?", "Evet. Tarihi tersaneyle önceden netleştiriyor, töreni yerden ve havadan birden fazla açıdan çekiyoruz."),
  ("Bursa'dan mı geliyorsunuz?", "Evet, kendi ekibimizle. Yaklaşık bir saatlik yol; keşif ve çekim aynı gün mümkün."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ İSTANBUL ÜRÜN ANİMASYONU
"istanbul-urun-animasyon": dict(
 lede="İstanbul'da bir kozmetik markası, bir medikal cihaz üreticisi ve bir akıllı ev girişimi aynı sorunu yaşıyor: ürünün asıl farkı kutunun içinde ve kamera onu göstermiyor.",
 bolum=[
  ("İstanbul'da ürün animasyonu kime lazım",
   "<p><strong>E-ticaret ve tüketici markaları:</strong> kozmetik, küçük ev aletleri, elektronik aksesuar. Ürün sayfasında 10–20 saniyelik bir animasyon, ürünün içindeki teknolojiyi, katmanları ya da kullanım adımlarını gösteriyor; fotoğrafın anlatamadığını anlatıyor. Aynı modelden reklam kesimleri ve dikey sürümler de çıkıyor.</p>"
   "<p><strong>Medikal ve teknik ürünler:</strong> İstanbul'daki medikal cihaz, filtre, pompa ve ölçüm cihazı üreticileri için kesit animasyonu; cihazın içindeki akışı ve mekanizmayı şeffaf gövde üzerinden gösteriyor. Satış temsilcisinin sahada tablette açtığı bir video, uzun bir teknik anlatımın yerini tutuyor.</p>"
   "<p><strong>Henüz üretilmemiş ürünler:</strong> yatırım arayan girişimler ve ön satış yapan markalar için prototip aşamasındaki ürünü fotogerçekçi göstermek. Kalıp çıkmadan pazarlama başlıyor.</p>"),
  ("Uzaktan nasıl çalışıyoruz",
   "<p>Ürün animasyonu için İstanbul'da bulunmamız gerekmiyor: CAD dosyası, teknik çizim ya da ürünün farklı açılardan fotoğrafları yeterli. Bu sayfadaki örnek işin müşterisi Avusturya'da; süreç ekran paylaşımlı toplantılar ve taslak onaylarıyla yürüyor. Ürünün gerçek çekimle birleşmesi gerekiyorsa İstanbul'a kendi ekibimizle bir günlüğüne geliyoruz.</p>"),
  ("İstanbul'a özgü bir avantaj",
   "<p>İstanbul'da stüdyo ve ürün çekimi pahalı; her renk ve varyant için ayrı çekim bütçeyi hızla büyütüyor. 3D modelde ise ürün bir kez modelleniyor, renk, malzeme ve ambalaj varyantları aynı modelden çıkıyor. Yeni sezon ya da yeni renk geldiğinde çekim yeniden yapılmıyor, yalnızca model güncelleniyor.</p>"),
 ],
 sss=[
  ("İstanbul'a gelmeniz gerekiyor mu?", "Hayır. CAD dosyası, teknik çizim ya da fotoğraflar yeterli; gerçek çekim gerekiyorsa bir günlüğüne geliyoruz."),
  ("Elimizde CAD dosyası yok, yine de olur mu?", "Olur. Ürünü ölçüleri ve fotoğraflarıyla sıfırdan modelliyoruz; süre biraz uzuyor."),
  ("Aynı modelden farklı renkleri gösterebilir misiniz?", "Evet. Model bir kez kuruluyor; renk, malzeme ve ambalaj varyantları aynı modelden çıkıyor."),
  ("Ürün sayfası için animasyon ne kadar olmalı?", "10–20 saniye. Tek bir şeyi göstermeli: içindeki teknoloji, katmanlar ya da kullanım adımı."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ ANKARA ÜRÜN ANİMASYONU
"ankara-urun-animasyon": dict(
 lede="Ankara'nın savunma, medikal ve yazılım firmalarının ürünleri çoğu zaman kameraya gösterilemiyor: ya gizli, ya çok büyük, ya da bir yazılımın içinde. 3D animasyon, gösterilemeyeni anlatmanın yolu.",
 bolum=[
  ("Gizlilik gereken ürünler",
   "<p>Ankara'nın organize sanayi bölgeleri ve teknoparklarında savunma sanayine tedarik yapan yüzlerce firma var. Bu firmalar fuarda ve müşteri sunumunda ürünlerini anlatmak zorunda; ama gerçek ürünün fotoğrafı ya da videosu çoğu zaman paylaşılamıyor. 3D modelde neyin gösterileceğine firma karar veriyor: hassas detaylar sadeleştiriliyor, genel yapı ve işlev anlatılıyor.</p>"
   "<p>Model ve render dosyaları sizin onayınız olmadan hiçbir yerde kullanılmıyor; gizlilik sözleşmesi gerekiyorsa çalışmaya başlamadan imzalıyoruz.</p>"),
  ("Medikal, makine ve yazılım",
   "<p><strong>Medikal cihaz:</strong> cihazın içindeki mekanizmayı ve hastaya nasıl uygulandığını gösteren animasyon; hastane satın almacısı ve distribütör sunumunda kullanılıyor.</p>"
   "<p><strong>Makine ve iş makinesi:</strong> çalışma prensibini kesit üzerinden, montajı patlatılmış görünümle gösteren animasyon; bayi eğitimi ve fuar ekranı için.</p>"
   "<p><strong>Yazılım ve donanım ürünleri:</strong> arayüz grafikleriyle birleşen ürün animasyonu; teknik olmayan yatırımcıya ve kamu kurumuna ürünü bir dakikada anlatan bir video.</p>"),
  ("Uzaktan çalışma",
   "<p>Ürün animasyonu için Ankara'da bulunmamız gerekmiyor: teknik çizim, CAD dosyası ya da fotoğraflar yeterli. Taslakları ekran paylaşımlı toplantılarda birlikte inceliyoruz. Gerçek çekimle birleştirilecek işlerde kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde Ankara'daki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Gizlilik sözleşmesi imzalıyor musunuz?", "Evet. Çalışmaya başlamadan imzalıyor, model ve dosyaları onayınız olmadan hiçbir yerde kullanmıyoruz."),
  ("Ürünün hassas detaylarını nasıl gizliyorsunuz?", "Neyin gösterileceğine siz karar veriyorsunuz; hassas parçaları sadeleştirip genel yapıyı ve işlevi anlatıyoruz."),
  ("Yazılım ürünümüzü animasyonla anlatabilir misiniz?", "Evet. Arayüz grafiklerini ve ürünün kullanım senaryosunu bir dakikalık bir videoda birleştiriyoruz."),
  ("Ankara'ya gelmeniz gerekiyor mu?", "Hayır. Modelleme ve animasyon tamamen uzaktan yürüyor; gerçek çekim gerekirse planlıyoruz."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ İZMİR ÜRÜN ANİMASYONU
"izmir-urun-animasyon": dict(
 lede="İzmir'in gıda, makine ve kimya üreticileri ürünlerinin çoğunu yurt dışına satıyor. Yabancı alıcı fabrikayı ziyaret etmeden önce ürünü ve süreci görmek istiyor; animasyon, o ilk ziyaretin yerini tutabiliyor.",
 bolum=[
  ("İzmir'in üreticileri için animasyon",
   "<p><strong>Gıda işleme ve paketleme:</strong> Kemalpaşa, Torbalı ve Çiğli'deki gıda üreticileri için hammaddeden pakete uzanan süreç animasyonu. Zincir marketin ve ithalatçının sorduğu izlenebilirlik, hijyen ve kapasite sorularına tek videoda cevap veriyor.</p>"
   "<p><strong>Makine ve ekipman:</strong> tarım makineleri, gıda işleme makineleri, pompa ve vana üreticileri için çalışma prensibi ve kesit animasyonu. Fuar ekranında sessiz dönen bir döngü, standın önünden geçen ziyaretçiyi durduruyor.</p>"
   "<p><strong>Kimya, boya ve yapı malzemesi:</strong> ürünün uygulandığı yüzeyde ne yaptığını gösteren animasyon: katman katman uygulama, yalıtım, koruma. Uygulayıcı ve bayi eğitimi için de kullanılıyor.</p>"),
  ("Çok dilli ve çok formatlı",
   "<p>İzmir'den yapılan ihracat Avrupa'dan Orta Doğu'ya uzanıyor. Animasyon bir kez hazırlanıyor; İngilizce, Almanca, Arapça ya da ihtiyaç duyulan dilde altyazı ve seslendirme aynı projeden çıkıyor. Fuar ekranı için yatay, sosyal medya için dikey ve web sitesi için kısa sürümler.</p>"),
  ("Uzaktan çalışma",
   "<p>Ürün animasyonu için İzmir'de bulunmamız gerekmiyor; teknik çizim, CAD dosyası ya da fotoğraflar yeterli. Bu sayfadaki örnek işin müşterisi Avusturya'da. Gerçek çekimle birleştirilecek işlerde kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde İzmir'deki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Gıda üretim sürecimizi animasyonla anlatmak mantıklı mı?", "Özellikle hijyen ve izlenebilirlik anlatımında evet; kamera girmesi zor alanlar ve tesisin akışı animasyonda net görünüyor."),
  ("Fuar için animasyon ne kadar önce hazırlanmalı?", "Ürünün karmaşıklığına göre üç ila altı hafta. Fuar tarihini ilk görüşmede söylemeniz yeterli."),
  ("Hangi dillerde hazırlıyorsunuz?", "İhtiyaç duyduğunuz her dilde altyazı; İngilizce, Almanca ve Arapça seslendirme de mümkün."),
  ("Elimizde CAD dosyası yok, ne yapabiliriz?", "Ölçüler ve fotoğraflarla sıfırdan modelliyoruz; süre biraz uzuyor."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ BURSA ÜRÜN ANİMASYONU
"bursa-urun-animasyon": dict(
 lede="Bursa'da üretilen bir otomotiv parçası yüzlerce kilometre uzaktaki bir montaj hattına, İnegöl'de üretilen bir koltuk takımı başka bir ülkedeki mağazaya gidiyor. Ürün animasyonu bu yolculukta satıcının yerine konuşuyor.",
 bolum=[
  ("Otomotiv yan sanayi ve makine",
   "<p>Nilüfer, Demirtaş ve diğer organize sanayi bölgelerindeki otomotiv yan sanayi firmaları için parçanın montaj sırasını, aracın içindeki yerini ve çalışma prensibini gösteren animasyon; ana sanayi ve yabancı müşteri sunumunda teknik anlatımı kısaltıyor. Makine üreticileri için gövdeyi şeffaflaştırıp içerideki hareketi gösteren kesit animasyonu.</p>"),
  ("İnegöl mobilyası",
   "<p>Mobilyada her model onlarca kumaş, renk ve modül seçeneğiyle satılıyor. Her varyantı ayrı ayrı fotoğraflamak yerine ürünü bir kez 3D modelliyoruz; varyantlar aynı modelden, istendiği kadar çıkıyor. Koltuğun açılıp yatağa dönüşmesi ya da modüllerin birleşmesi gibi mekanizmaları animasyonla gösteriyoruz; katalog, e-ticaret ve fuar için.</p>"),
  ("Tekstil",
   "<p>Bursa'nın tekstil üreticileri için kumaşın örgü yapısını, katmanlarını ve teknik özelliğini (nefes alma, su itme, esneme) görünür kılan animasyon. Teknik kumaş satışında alıcının sorduğu sorulara numune göndermeden cevap veriyor.</p>"),
  ("Bursa'da olmanın farkı",
   "<p>Ürün animasyonu uzaktan yürüyen bir iş; ama Bursa merkezimiz olduğu için Bursa'daki üreticilerle fark şu: ürünü yerinde görüp ölçebiliyor, üretim hattını gerçek çekimle animasyonun içine yerleştirebiliyoruz. Gerçek çekim ve 3D animasyonun birleştiği filmler Bursa'da en kolay kurduğumuz iş.</p>"),
 ],
 sss=[
  ("Mobilya varyantlarını 3D'de göstermek fotoğraftan ucuz mu?", "Varyant sayısı arttıkça evet. Model bir kez kuruluyor; her yeni renk ve kumaş için yeniden çekim gerekmiyor."),
  ("Fabrikamıza gelip ürünü yerinde görebilir misiniz?", "Evet, Bursa merkezimiz. Ürünü yerinde inceleyip gerekirse üretim hattını da çekiyoruz."),
  ("Otomotiv parçamızın çalışma prensibini nasıl anlatırsınız?", "Parçanın araçtaki yerinden başlayıp kesit ve patlatılmış görünümle iç yapıyı gösteren kısa bir animasyonla."),
  ("Teknik kumaş özelliklerini animasyonla gösterebilir misiniz?", "Evet. Nefes alma, su itme ya da esneme gibi özellikleri kumaşın içinden gösteren yakın plan animasyonla."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ KOCAELİ ÜRÜN ANİMASYONU
"kocaeli-urun-animasyon": dict(
 lede="Kocaeli'de üretilen kimyasallar, boyalar, lastikler ve otomotiv parçaları gözle görülmeyen işler yapıyor: korozyonu durduruyor, ısıyı yalıtıyor, yükü taşıyor. Animasyon, bu görünmeyen işi görünür kılıyor.",
 bolum=[
  ("Kimya ve boya",
   "<p>Gebze, Dilovası ve Körfez çevresindeki kimya ve boya üreticileri için ürünün yüzeyde ne yaptığını gösteren animasyon: astarın metale tutunması, katmanların oluşması, nemin ve korozyonun durdurulması. Mikroskobik ölçekte olan biteni büyüterek gösteriyoruz. Bayi ve uygulayıcı eğitimi için uygulama adımları ayrı bir sürüm olarak hazırlanıyor.</p>"),
  ("Lastik, otomotiv ve makine",
   "<p>Lastik ve otomotiv parçası üreticileri için ürünün iç yapısını katman katman açan patlatılmış görünüm, yol ve yük altında nasıl davrandığını gösteren simülasyon görselleri. Makine üreticileri için çalışma prensibi ve bakım adımları; servis ekibinin ve müşterinin aynı videodan öğrendiği bir anlatım.</p>"),
  ("Tesis ve süreç animasyonu",
   "<p>Kocaeli'deki büyük tesislerde kamera çoğu yere giremiyor; güvenlik ve gizlilik kuralları buna izin vermiyor. Tesisin akışını, hammaddenin girişinden ürünün sevkiyatına kadar 3D olarak modellemek, hem yabancı müşteri sunumunda hem iş güvenliği eğitiminde kullanılabilen bir anlatım sağlıyor.</p>"
   "<p>Kocaeli Bursa'ya yaklaşık bir saat; modelleme uzaktan yürüyor, ama ürünü yerinde görmek ya da gerçek çekimle birleştirmek gerektiğinde kendi ekibimizle geliyoruz.</p>"),
 ],
 sss=[
  ("Boyamızın korozyon koruma özelliğini nasıl gösterirsiniz?", "Yüzeyi büyüterek: katmanların oluşumu, nemin ve tuzun yüzeye ulaşamaması. Kısa, net ve bilimsel olarak doğru bir anlatım için teknik ekibinizle çalışıyoruz."),
  ("Tesisimize kamera giremiyor, süreç nasıl anlatılır?", "Tesisin akışını 3D olarak modelliyoruz. Hangi detayların gösterileceğine siz karar veriyorsunuz."),
  ("İş güvenliği eğitimi için animasyon yapıyor musunuz?", "Evet. Tehlikeli anları gerçek kişileri riske atmadan gösteren eğitim animasyonları hazırlıyoruz."),
  ("Kocaeli'ye gelmeniz gerekiyor mu?", "Modelleme için hayır. Ürünü görmek ya da gerçek çekim için Bursa'dan bir saatte geliyoruz."),
 ],
 kaynak=[],
),

# ------------------------------------------------------------------ İSTANBUL İNŞAAT 3D
"istanbul-insaat-3d-modelleme": dict(
 lede="İstanbul'da son bir yılda 80.864 sıfır konut satıldı. Bu konutların önemli bir kısmı alıcıya bina bitmeden, çoğu zaman temel atılmadan önce satılıyor; alıcının gördüğü ilk şey bir render.",
 bolum=[
  ("İstanbul'da yeni konut rakamlarla",
   "<p>TÜİK verisine göre Eylül 2025–Ağustos 2026 arasında İstanbul'da <strong>305.407 konut</strong> satıldı; bunun <strong>80.864'ü (%26,5) ilk el</strong>. İlk el satışların büyük kısmı yeni projelerden ve kentsel dönüşümden geliyor. Bu projelerde satış ofisi, ilan sitesi ve sosyal medya, inşaat bitmeden açılıyor; projenin ilk yüzü 3D görselleştirme.</p>"),
  ("Kentsel dönüşüm ve küçük projeler",
   "<p>İstanbul'da yeni konutun önemli bir kısmı büyük sitelerden değil, eski binanın yıkılıp yerine yapıldığı tek bina dönüşüm projelerinden çıkıyor. Bu projelerde render iki işe yarıyor: kat maliklerine ve komşulara yeni binayı göstermek, ardından boş daireleri satmak. Küçük bütçeli dönüşüm projeleri için tek bina, birkaç dış cephe ve iç mekân görseli ile kısa bir animasyon yeterli oluyor.</p>"
   "<p>Dar sokakta, komşu binaların arasında duran bir yapıyı doğru göstermek için çevreyi de modelliyoruz; böylece alıcı binanın gerçekte nasıl göründüğünü, ışığın daireye nereden girdiğini görüyor.</p>"),
  ("Manzara ve güneş",
   "<p>İstanbul'da dairenin fiyatını manzara belirliyor: Boğaz, deniz, ada ya da orman. Henüz yükselmemiş bir binanın her katından ne görüneceğini, gerçek konuma ve yüksekliğe göre drone ile çekip render ile birleştirerek gösteriyoruz. Güneşin hangi saatte hangi cepheye vurduğunu da gerçek koordinata göre hesaplıyoruz.</p>"
   "<p>Modelleme ve animasyon uzaktan yürüyor; drone ve şantiye çekimi gereken işlerde İstanbul'a kendi ekibimizle geliyoruz.</p>"),
 ],
 sss=[
  ("Kentsel dönüşüm projemiz küçük, render bütçesi ne kadar olmalı?", "Tek bina için birkaç dış cephe, birkaç iç mekân görseli ve kısa bir animasyon çoğu zaman yeterli. Fiyat bandımızın alt ucundan başlıyor."),
  ("Henüz yükselmemiş binanın manzarasını nasıl gösterirsiniz?", "Gerçek konumda, ilgili kat yüksekliğinde drone ile çekip render ile birleştiriyoruz."),
  ("Kat malikleri için sunum hazırlıyor musunuz?", "Evet. Yeni binanın dış görünüşünü ve dairelerin planını gösteren sade bir sunum ve kısa bir video hazırlıyoruz."),
  ("İstanbul'a gelmeniz gerekiyor mu?", "Modelleme için hayır; drone ve şantiye çekimi gerekiyorsa geliyoruz."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ ANKARA İNŞAAT 3D
"ankara-insaat-3d-modelleme": dict(
 lede="Ankara'da son bir yılda 147.984 konut satıldı; il Türkiye'de ikinci sırada. Bunların 44.781'i sıfır konut. Başkentte yeni proje çok; projenin önce görselde ayrışması gerekiyor.",
 bolum=[
  ("Ankara'da yeni konut rakamlarla",
   "<p>TÜİK verisine göre Eylül 2025–Ağustos 2026 arasında Ankara'da <strong>147.984 konut</strong> satıldı; <strong>44.781'i (%30,3) ilk el</strong>. Ağustos 2026'da satış bir yıl öncesine göre <strong>%13,4</strong> düştü. Alıcının azaldığı bir dönemde yeni projeler arasında rekabet artıyor; satış ofisi ve ilan sitelerindeki görselin kalitesi alıcının hangi projeyi gezmeye gideceğini belirliyor.</p>"),
  ("Ankara'nın proje tipleri",
   "<p><strong>Etimesgut, Yenimahalle, Gölbaşı ve İncek hattı:</strong> sosyal donatılı büyük siteler. Alıcı aile; havuz, oyun alanı, yürüyüş yolu ve otopark soruyor. Sitenin yerleşimini kuş bakışı maketle, ortak alanları insan gözü yüksekliğinden render ile gösteriyoruz.</p>"
   "<p><strong>Çankaya ve merkez:</strong> kentsel dönüşüm ve tek bina projeleri; dar arsada yükselen modern cepheler. Çevre binalarla birlikte modellemek, alıcıya binanın sokakta nasıl duracağını gösteriyor.</p>"
   "<p><strong>Ticari yapılar ve ofisler:</strong> kamu kurumlarına yakın ofis ve iş merkezi projeleri; lobi, ofis katı ve otopark görselleri.</p>"),
  ("Ankara ışığı",
   "<p>Ankara'nın karasal ikliminde kış ışığı gri, yaz ışığı sert ve kuru. Render'da projenin en iyi göründüğü mevsimi ve saati seçiyoruz; ama alıcının güvenini kazanmak için cephenin gerçek yönünü ve güneşin gerçek açısını koruyoruz. Kar altında bir site görseli, kış satış dönemi için ayrıca hazırlanabiliyor.</p>"
   "<p>Modelleme ve animasyon uzaktan yürüyor; şantiye ve drone çekimi gereken işlerde Ankara'daki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Site projemizin sosyal alanlarını nasıl gösterirsiniz?", "Kuş bakışı yerleşim maketi ve insan gözü yüksekliğinden ortak alan render'ları; ailelerin sorduğu havuz, oyun alanı ve otoparkı tek tek."),
  ("Kentsel dönüşüm projesi için çevre binaları da modelliyor musunuz?", "Evet. Binanın sokakta nasıl duracağını göstermek için çevreyi sade bir şekilde modelliyoruz."),
  ("Kış görseli hazırlayabilir misiniz?", "Evet. Aynı modelden karlı bir sahne üretmek kış satış dönemi için ayrı bir görsel sağlıyor."),
  ("Ankara'ya gelmeniz gerekiyor mu?", "Modelleme için hayır; şantiye ve drone çekimi gerekiyorsa planlıyoruz."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ İZMİR İNŞAAT 3D
"izmir-insaat-3d-modelleme": dict(
 lede="İzmir'de son bir yılda 95.859 konut satıldı; 28.201'i sıfır konut. Şehirde dönüşüm projeleri, kıyıda villa ve yazlık; iki ayrı alıcı, iki ayrı görsel dil.",
 bolum=[
  ("İzmir'de yeni konut rakamlarla",
   "<p>TÜİK verisine göre Eylül 2025–Ağustos 2026 arasında İzmir'de <strong>95.859 konut</strong> satıldı; il Türkiye'de üçüncü sırada. Satışların <strong>%29,4'ü ilk el</strong>. Ağustos 2026'da satış bir yıl öncesine göre <strong>%17</strong> düştü; Türkiye genelindeki düşüş %14,7. Yavaşlayan piyasada alıcı daha uzun düşünüyor ve projeleri daha dikkatli karşılaştırıyor.</p>"),
  ("Şehir içi ve kıyı projeleri",
   "<p><strong>Şehir içi:</strong> Bayraklı, Bornova, Buca ve Karşıyaka'da dönüşüm projeleri ve yeni siteler. İzmir'de deprem sonrası güven önemli bir konu; yapının taşıyıcı sistemini, zemin iyileştirmesini ve kullanılan malzemeyi anlatan kısa bir teknik animasyon, alıcının en çok sorduğu soruya cevap veriyor.</p>"
   "<p><strong>Kıyı:</strong> Urla, Çeşme, Seferihisar ve Menderes'te villa ve yazlık projeleri. Alıcı çoğu zaman İzmir dışında, bazen yurt dışında; projeyi görmeden karar veriyor. Deniz manzarası, bahçe ve havuzun gün batımındaki görüntüsü, 360° sanal turla birlikte satışın asıl aracı.</p>"),
  ("Gerçek konum, gerçek ışık",
   "<p>Kıyı projelerinde manzara fiyatı belirliyor. Arsanın gerçek konumunda drone ile çekim yapıp render'ı bu görüntünün içine yerleştiriyoruz; alıcı villanın terasından gerçekte neyi göreceğini görüyor. Güneş açısını gerçek koordinata ve mevsime göre hesaplıyoruz.</p>"
   "<p>Modelleme ve animasyon uzaktan yürüyor; şantiye ve drone çekimi gereken işlerde İzmir'deki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Yapının deprem güvenliğini animasyonla anlatabilir miyiz?", "Evet. Taşıyıcı sistemi, zemin iyileştirmesini ve malzemeyi sade bir dille gösteren kısa bir teknik animasyon hazırlıyoruz; içerik statik projenize dayanıyor."),
  ("Yurt dışındaki alıcı için ne önerirsiniz?", "Gerçek konumda çekilmiş drone görüntüsüyle birleşen render, 360° sanal tur ve altyazılı kısa bir tanıtım filmi."),
  ("Villa projemizin manzarasını gerçeğe uygun gösterebilir misiniz?", "Evet. Arsada ilgili yükseklikte drone ile çekip render'ı bu görüntüye yerleştiriyoruz."),
  ("İzmir'e gelmeniz gerekiyor mu?", "Modelleme için hayır; drone ve şantiye çekimi gerekiyorsa planlıyoruz."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ BURSA İNŞAAT 3D
"bursa-insaat-3d-modelleme": dict(
 lede="Bursa'da son bir yılda satılan 57.169 konutun 16.669'u sıfır. Nilüfer'deki siteden Mudanya'daki deniz manzaralı projeye, Bursa'nın yeni konutu çoğu zaman alıcıya bir render olarak ulaşıyor.",
 bolum=[
  ("Bursa'da yeni konut rakamlarla",
   "<p>TÜİK verisine göre Eylül 2025–Ağustos 2026 arasında Bursa'da <strong>57.169 konut</strong> satıldı; <strong>16.669'u (%29,2) ilk el</strong>. Ağustos 2026'da satış bir yıl öncesine göre <strong>%20,7</strong> düştü. Satışın yavaşladığı bir dönemde yeni projenin, ikinci el ilanlar arasından sıyrılması gerekiyor; görselleştirme bunun ilk adımı.</p>"),
  ("Bursa'nın proje tipleri",
   "<p><strong>Nilüfer, Görükle ve Özlüce hattı:</strong> sosyal donatılı siteler; aile alıcılar havuz, otopark ve okula yakınlık soruyor. Yerleşim maketi ve ortak alan render'ları.</p>"
   "<p><strong>Mudanya ve Güzelyalı:</strong> deniz manzaralı daire ve villa projeleri. Manzara fiyatı belirliyor; arsada drone ile çekip render ile birleştirerek her kattan görünen manzarayı gösteriyoruz.</p>"
   "<p><strong>Osmangazi ve Yıldırım:</strong> kentsel dönüşüm projeleri; dar arsada, eski dokunun arasında yükselen binalar. Çevreyle birlikte modellemek, yapının sokakta nasıl duracağını gösteriyor.</p>"
   "<p><strong>Uludağ eteği ve yayla evleri:</strong> manzaralı müstakil ve villa projeleri; doğa ile yapının ilişkisi.</p>"),
  ("Bursa'da olmanın farkı",
   "<p>Bursa merkezimiz. Arsayı yerinde görüyor, güneşin hangi saatte nereye vurduğunu yerinde ölçüyor, drone çekimini ayrı bir yol gideri olmadan yapıyoruz. Satış ofisi açılmadan önce render'ları, açıldıktan sonra şantiye ilerleme videolarını aynı ekipten alabiliyorsunuz. Bu sayfadaki konut projesi animasyonu, Avusturya'daki bir müşterimiz için yaptığımız bir iş.</p>"),
 ],
 sss=[
  ("Mudanya'daki projemizin manzarasını nasıl gösterirsiniz?", "Arsada, ilgili kat yüksekliklerinde drone ile çekip render ile birleştiriyoruz; alıcı her kattan gerçekte neyi göreceğini görüyor."),
  ("Arsayı yerinde görebilir misiniz?", "Evet, Bursa merkezimiz. Arsayı, çevreyi ve ışığı yerinde inceliyoruz."),
  ("Render ve şantiye videosunu aynı ekipten alabilir miyiz?", "Evet. Satış öncesi görselleri, inşaat sürecinde aylık şantiye çekimini ve teslim filmini birlikte planlayabiliyoruz."),
  ("Kentsel dönüşüm projesi için ne önerirsiniz?", "Çevre binalarla birlikte modellenmiş birkaç dış cephe görseli, iç mekân render'ları ve kat malikleri için sade bir sunum."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ KOCAELİ İNŞAAT 3D
"kocaeli-insaat-3d-modelleme": dict(
 lede="Kocaeli'de son bir yılda satılan konutların %37,8'i sıfır; Türkiye ortalaması %33,5. Sanayi büyüdükçe yeni konut da büyüyor ve projelerin çoğu bitmeden satışa çıkıyor.",
 bolum=[
  ("Kocaeli'de yeni konut rakamlarla",
   "<p>TÜİK verisine göre Eylül 2025–Ağustos 2026 arasında Kocaeli'de <strong>47.112 konut</strong> satıldı; il Türkiye'de yedinci sırada. Bunların <strong>17.823'ü ilk el</strong>. Ağustos 2026'da satış bir yıl öncesine göre yalnızca <strong>%6</strong> düştü; Türkiye geneli %14,7. Piyasa görece dirençli, yeni proje sayısı yüksek; projelerin birbirinden ayrışması gerekiyor.</p>"),
  ("Kocaeli'nin proje tipleri",
   "<p><strong>Gebze, Darıca ve Çayırova:</strong> İstanbul'a yakın, sanayi çalışanına ve İstanbul'dan taşınan ailelere satılan siteler. Alıcının ilk sorusu ulaşım: Marmaray, otoyol, fabrika. Yerleşim maketinde ulaşım bağlantılarını da gösteriyoruz.</p>"
   "<p><strong>Başiskele ve Kartepe:</strong> körfez ve orman manzaralı siteler, müstakil ve villa projeleri. Manzara satışın merkezinde; arsada drone ile çekip render ile birleştiriyoruz.</p>"
   "<p><strong>İzmit ve Gölcük:</strong> 1999 depreminden sonra yenilenen şehirde dönüşüm ve yeni projeler. Taşıyıcı sistemi ve zemini anlatan kısa bir teknik animasyon, alıcının güven sorusuna cevap veriyor.</p>"),
  ("Bursa'dan bir saat",
   "<p>Modelleme ve animasyon uzaktan yürüyor; ama Kocaeli Bursa'ya yaklaşık bir saat. Arsayı yerinde görmek, drone ile manzara çekimi yapmak ya da şantiye ilerleme videosu çekmek için kendi ekibimizle geliyoruz.</p>"),
 ],
 sss=[
  ("Projemizin ulaşım avantajını görselde nasıl gösteririz?", "Yerleşim maketine çevredeki otoyol, Marmaray durağı ve sanayi bölgesi bağlantılarını ekliyoruz; alıcı mesafeyi tek bakışta görüyor."),
  ("Körfez manzarasını gerçeğe uygun gösterebilir misiniz?", "Evet. Arsada ilgili kat yüksekliğinde drone ile çekip render ile birleştiriyoruz."),
  ("Deprem güvenliğini anlatan bir animasyon hazırlar mısınız?", "Evet. Statik projenize dayanarak taşıyıcı sistemi ve zemin iyileştirmesini sade bir dille gösteriyoruz."),
  ("Kocaeli'ye gelmeniz gerekiyor mu?", "Modelleme için hayır; arsa, drone ve şantiye çekimi için Bursa'dan bir saatte geliyoruz."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ ADANA EMLAK
"adana-emlak-video": dict(
 lede="Adana'da bir daireyi satan şey çoğu zaman metrekare değil, Temmuz'da o dairenin ne kadar serin kaldığı. Cephe, gölge, havuz ve klima; Adanalı alıcının ilk baktığı şeyler.",
 bolum=[
  ("Adana konut piyasası rakamlarla",
   "<p>TÜİK verisine göre Eylül 2025–Ağustos 2026 arasında Adana'da <strong>35.439 konut</strong> satıldı; il Türkiye'de 11. sırada. Satışların <strong>%29'u ilk el</strong>, Türkiye ortalamasının (%33,5) altında; Adana'da alıcının önündeki ilanların çoğu ikinci el. Ağustos 2026'da satış <strong>2.600</strong> konutta kaldı; bir yıl önce 3.159'du, düşüş <strong>%17,7</strong>.</p>"),
  ("İlçeye göre alıcı",
   "<p><strong>Çukurova:</strong> Turgut Özal Bulvarı çevresinde havuzlu, güvenlikli siteler; alıcı aile ve yüksek gelirli. Ortak alanlar, havuz ve otopark videonun merkezinde.</p>"
   "<p><strong>Sarıçam:</strong> üniversiteye yakın, yeni gelişen bölgeler; hem yatırımcı hem kiralık daire arayan öğrenci ve akademisyen.</p>"
   "<p><strong>Seyhan:</strong> şehrin merkezinde, eski ve geniş daireler; çarşıya, nehre ve hastanelere yakınlık. <strong>Yüreğir:</strong> daha uygun fiyatlı stok ve ilk evini alan genç aileler.</p>"),
  ("Sıcakla çekim",
   "<p>Adana yazın Türkiye'nin en sıcak şehirlerinden biri; alıcı dairenin güneyden mi kuzeyden mi ışık aldığını, balkonun gölgede kalıp kalmadığını soruyor. Videoda cephenin yönünü ve günün farklı saatlerindeki ışığı gösteriyor, klima ve yalıtım gibi detayları yakın planda veriyoruz. Dış çekimi sabah erken ya da akşamüstüne koyuyoruz; öğle ışığı hem sert hem yanıltıcı.</p>"
   "<p>Sarıçam'daki İncirlik Hava Üssü ve şehir içindeki bazı alanlar drone için izne bağlı; mülkün konumunu haritadan kontrol ediyoruz. Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Adana'da ilan videosunda en çok neye dikkat edilmeli?", "Cephenin yönü, gölge ve serinlik. Alıcı dairenin yazın nasıl olacağını merak ediyor; bunu ışık ve detay planlarıyla gösteriyoruz."),
  ("Çukurova'daki site dairesi için video nasıl olmalı?", "Site girişinden başlayan, havuz ve ortak alanları gösteren, ardından daireye giren tek akıcı tur. 60–90 saniye yeterli."),
  ("Kiralık daire için de video çekiyor musunuz?", "Evet. Sarıçam ve üniversite çevresindeki kiralıklar için 30–45 saniyelik dikey turlar hazırlıyoruz."),
  ("Yazın çekim hangi saatte yapılmalı?", "Dış çekim sabah erken ya da akşamüstü; iç çekim gün içinde. Öğle ışığında dış cephe sert görünüyor."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ ANKARA EMLAK
"ankara-emlak-video": dict(
 lede="Ankara'da Çankaya'nın geniş odalı eski apartmanı, Eryaman'ın havuzlu sitesi ve İncek'in müstakil evi aynı ilan sitesinde yan yana duruyor. Her birinin alıcısı başka bir şey arıyor.",
 bolum=[
  ("Başkentin konut piyasası",
   "<p>TÜİK'e göre Ankara'da son bir yılda <strong>147.984 konut</strong> el değiştirdi; İstanbul'dan sonra Türkiye'nin en büyük ikinci piyasası. Satışların yaklaşık <strong>%70'i ikinci el</strong>. Ağustos 2026'da 10.851 satışla bir yıl öncesinin (12.534) <strong>%13,4</strong> gerisinde kaldı.</p>"
   "<p>Bu büyüklükte bir piyasada aynı mahallede onlarca benzer ilan oluyor. Video, alıcının listede durup ilanı açmasını ve gezmeye gelmeden önce mülkü elemesini sağlıyor.</p>"),
  ("Semte göre video",
   "<p><strong>Çankaya, Kavaklıdere, Ayrancı:</strong> geniş odalı, yüksek tavanlı eski apartmanlar. Alıcının merak ettiği şey dairenin ferahlığı ve bakımı; geniş açılı, yavaş planlar ve yenilenmiş mutfak-banyo detayları.</p>"
   "<p><strong>Eryaman, Etimesgut, Yenimahalle:</strong> sosyal donatılı siteler. Ortak alan, otopark ve metroya mesafe videonun ilk kısmı.</p>"
   "<p><strong>Gölbaşı ve İncek:</strong> müstakil ev ve villa; bahçe, şömine, göle ve şehre mesafe.</p>"
   "<p><strong>Keçiören ve Mamak:</strong> kentsel dönüşümle yenilenen daireler; binanın yeni olduğunu ve deprem yönetmeliğine uygunluğunu öne çıkaran bilgi.</p>"),
  ("Çekim düzeni",
   "<p>Ankara'nın büyük kısmı drone için kısıtlı hava sahasında; şehir içinde havadan plan çoğu zaman izin istiyor. Havadan görüntü gereken site ve villa ilanlarında konumu önceden kontrol ediyor, gerekmiyorsa yüksek bir noktadan yerden çekiyoruz. Kış ışığı gri ve kısa; iç çekimi öğle saatlerine koyuyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde Ankara'daki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Çankaya'daki eski daire için video fark eder mi?", "Çok. Eski binanın geniş odalarını fotoğraf küçük gösteriyor; geniş açılı ve yavaş bir video ferahlığı doğru anlatıyor."),
  ("Site dairesi videosunda neler olmalı?", "Site girişi, ortak alanlar, otopark, ardından daire. Metroya ve okula mesafeyi yazıyla ekliyoruz."),
  ("Ankara'da drone ile ilan çekimi yapılabilir mi?", "Konuma bağlı; şehrin önemli kısmı izin gerektiriyor. Mülkün yerini kontrol edip önceden söylüyoruz."),
  ("Emlak ofisi olarak toplu çekim yaptırabilir miyiz?", "Evet. Aynı semtteki mülkleri tek güne topluyor, her biri için dikey ve yatay sürüm teslim ediyoruz."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ ANTALYA EMLAK
"antalya-emlak-video": dict(
 lede="Antalya'da bir dairenin alıcısı Moskova'da, Berlin'de ya da İstanbul'da olabilir. Mülkü görmeden karar veren alıcı için ilan videosu, mülkün kendisi kadar önemli.",
 bolum=[
  ("Antalya konut piyasası rakamlarla",
   "<p>TÜİK verisine göre Eylül 2025–Ağustos 2026 arasında Antalya'da <strong>82.450 konut</strong> satıldı; il Türkiye'de 4. sırada. Satışların <strong>%34,3'ü ilk el</strong>. Ağustos 2026'da satış 5.855'e geriledi; bir yıl önce 7.077'ydi, düşüş <strong>%17,3</strong>.</p>"
   "<p>Antalya, yabancıya konut satışında Türkiye'nin öne çıkan illerinden biri. Uzaktan alıcı mülkü videodan değerlendiriyor; video kötüyse ilan listede kalıyor, iyiyse alıcı uçak bileti alıyor.</p>"),
  ("Bölgeye göre alıcı",
   "<p><strong>Konyaaltı ve Lara:</strong> denize yürüme mesafesinde site daireleri; hem yerli hem yabancı alıcı. Denize ve plaja mesafe, havuz ve balkon manzarası videonun merkezinde.</p>"
   "<p><strong>Alanya ve Mahmutlar:</strong> yabancı alıcının yoğun olduğu, havuzlu ve sosyal tesisli siteler. Video çoğu zaman İngilizce, Almanca ya da Rusça altyazılı; alıcı sitenin sunduğu yaşamı görmek istiyor.</p>"
   "<p><strong>Döşemealtı ve Kaş:</strong> bahçeli müstakil ev ve havuzlu villa. Arsa, manzara ve mahremiyet; havadan bir plan şart.</p>"
   "<p><strong>Kepez ve Muratpaşa'nın iç kesimi:</strong> şehirde yaşayan aileler için uygun fiyatlı daireler; okul ve ulaşım bilgisi.</p>"),
  ("Çekim düzeni",
   "<p>Antalya Havalimanı'nın kontrollü sahası Lara ve Aksu tarafını kapsıyor; Lara'daki mülklerde drone planı izin gerektirebiliyor. Yaz öğlesinin sert ışığı yerine sabah ya da gün batımını seçiyoruz; deniz manzaralı dairede balkon planını gün batımına koyuyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde Antalya'daki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Yabancı alıcı için ilan videosu nasıl olmalı?", "Kısa ve bilgi yoğun: denize, havalimanına ve merkeze mesafe, site olanakları, ardından daire. Altyazıyı alıcının dilinde veriyoruz."),
  ("Lara'daki dairemiz için drone kullanılabilir mi?", "Havalimanına yakınlık nedeniyle izin gerekebilir. Konumu kontrol edip çekimden önce söylüyoruz."),
  ("Villa ilanında neler mutlaka olmalı?", "Havadan arsa ve çevre, havuz ve bahçe, manzara, ardından iç tur. Mahremiyet alıcının en çok sorduğu şeylerden."),
  ("Videoyu hangi dillerde hazırlıyorsunuz?", "İngilizce, Almanca ve Rusça en çok istenenler; diğer diller için de altyazı ekleyebiliyoruz."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ AYDIN EMLAK
"aydin-emlak-video": dict(
 lede="Aydın'da satılan konutların yalnızca %26,4'ü sıfır; Türkiye'nin en düşük oranlarından biri. Kuşadası'ndaki yazlıktan Efeler'deki apartman dairesine kadar alıcının önündeki ilanların çoğu ikinci el.",
 bolum=[
  ("Aydın konut piyasası rakamlarla",
   "<p>TÜİK verisine göre Eylül 2025–Ağustos 2026 arasında Aydın'da <strong>29.339 konut</strong> satıldı; il Türkiye'de 16. sırada. Satışların <strong>%26,4'ü ilk el</strong>; Türkiye ortalaması %33,5. Ağustos 2026'da satış 2.174'e geriledi; bir yıl önce 2.773'tü, düşüş <strong>%21,6</strong>, Türkiye genelinin (%14,7) belirgin üzerinde.</p>"
   "<p>İkinci el ağırlıklı ve yavaşlayan bir piyasada satıcı daha uzun bekliyor; benzer ilanlar arasında fark yaratan şey ilanın sunumu.</p>"),
  ("Kıyı ve iç kesim",
   "<p><strong>Kuşadası:</strong> deniz manzaralı daireler ve yazlık siteler; alıcı İstanbul'dan, Ankara'dan ve yurt dışından. Denize mesafe, manzara ve site olanakları.</p>"
   "<p><strong>Didim:</strong> yazlık ve emekli alıcının tercih ettiği, yabancı sakinlerin de yaşadığı bir sahil kasabası. Uygun fiyat, sahile yakınlık ve kış yaşamı; çok dilli video bu alıcıya ulaşıyor.</p>"
   "<p><strong>Efeler, Nazilli ve Söke:</strong> şehirde yıl boyu yaşayan aileler için daireler; okul, çarşı ve ulaşım bilgisi.</p>"
   "<p><strong>Köy evi ve bahçe:</strong> zeytinlik ve incir bahçesi içinde taş evler; arsa sınırı ve bahçe havadan gösterilmeli.</p>"),
  ("Yazlık ilanı ne zaman çekilmeli",
   "<p>Kuşadası ve Didim'de yazlık alıcısı kararını baharda veriyor. İlanın Nisan–Mayıs'ta, sahil boşken ve hava açıkken çekilmesi, alıcının en çok baktığı haftalara hazır olması demek. Yazın ise öğle sıcağından kaçıp sabah ve akşamüstü çekiyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Didim'deki yazlığımızı yabancı alıcıya nasıl anlatırız?", "Kısa, manzara ve yaşam odaklı bir video; sahile, çarşıya ve havalimanına mesafe. İngilizce altyazıyla."),
  ("Köy evi ilanında drone gerekli mi?", "Bahçe ve arsa sınırını göstermek için çok faydalı. Konumu haritadan kontrol edip izin durumunu önceden söylüyoruz."),
  ("Satışlar düşükken video çektirmek mantıklı mı?", "Tam bu dönemde. Alıcı azken ilanınızın ayrışması ve gezmeye gelen alıcının gerçekten ilgili olması zaman kazandırıyor."),
  ("Yazlık ilanı için en iyi dönem ne zaman?", "Nisan–Mayıs. Sahil boş, ışık yumuşak ve ilan yaz başına hazır oluyor."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ DENİZLİ EMLAK
"denizli-emlak-video": dict(
 lede="Denizli'de alıcı genellikle şehirde çalışan, şehirde yaşayan bir aile. Okula, fabrikaya ve çarşıya mesafe; Denizli'de ilan videosu önce günlük hayatı göstermeli.",
 bolum=[
  ("Denizli konut piyasası rakamlarla",
   "<p>TÜİK verisine göre Eylül 2025–Ağustos 2026 arasında Denizli'de <strong>20.478 konut</strong> satıldı; il Türkiye'de 22. sırada. Satışların <strong>%33,6'sı ilk el</strong>, Türkiye ortalamasıyla neredeyse aynı. Ağustos 2026'da satış bir yıl öncesine göre <strong>%13</strong> geriledi (1.766'dan 1.536'ya).</p>"),
  ("Denizli'de mülk tipleri",
   "<p><strong>Pamukkale ve Merkezefendi ilçelerinde site daireleri:</strong> şehrin iki merkez ilçesinde yeni siteler ve apartmanlar. Tekstil ve sanayide çalışan aileler için okula, servise ve alışverişe mesafe önemli; bunu videonun başında havadan ya da yazıyla veriyoruz.</p>"
   "<p><strong>Bağbaşı ve yamaç evleri:</strong> şehre tepeden bakan, serin ve manzaralı müstakil evler. Yaz sıcağında serinlik ve manzara satışın merkezi.</p>"
   "<p><strong>Karahayıt ve termal bölge:</strong> termal suyu olan devre mülk ve yazlık daireler; tesis olanakları ve havuz.</p>"
   "<p><strong>Çal, Buldan ve köyler:</strong> bağ evi ve köy evleri; arsa, bağ ve manzara.</p>"),
  ("Çekim düzeni",
   "<p>Denizli yazın sıcak; öğle ışığında dış cephe sert görünüyor. Dış çekimleri sabah ve akşamüstüne, iç çekimleri gün ortasına koyuyoruz. Havalimanı şehirden uzakta, Çardak'ta; şehir içindeki mülklerde drone planı çoğu zaman daha esnek, yine de her konumu haritadan kontrol ediyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; çekim günlerinde bölgedeki çözüm ortağımızla birlikte çalışıyoruz.</p>"),
 ],
 sss=[
  ("Site dairesi videosunda mesafeleri nasıl gösteriyorsunuz?", "Havadan bir konum planı ve ekranda kısa yazılarla: okula, çarşıya, ana yola mesafe."),
  ("Bağbaşı'ndaki evin manzarasını nasıl çekersiniz?", "Gün batımında, şehrin ışıkları yanmaya başlarken. Havadan bir plan ve terastan manzara."),
  ("Termal bölgedeki daire için ne önerirsiniz?", "Tesis olanaklarını, havuzu ve daireyi birlikte gösteren kısa bir video; termal suyun avantajını öne çıkaran planlar."),
  ("Teslim ne kadar sürüyor?", "Tek daire yarım gün; kurgu ve renk düzenlemesiyle teslim genellikle birkaç iş günü."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ GAZİANTEP EMLAK
"gaziantep-emlak-video": dict(
 lede="Şubat 2023 depremlerinden sonra Gaziantep'te alıcının ilk sorusu değişti: önce binanın yaşı, zemini ve ruhsat tarihi, sonra oda sayısı. İlan videosu bu soruya baştan cevap vermeli.",
 bolum=[
  ("Gaziantep konut piyasası rakamlarla",
   "<p>TÜİK verisine göre Eylül 2025–Ağustos 2026 arasında Gaziantep'te <strong>44.581 konut</strong> satıldı; il Türkiye'de 8. sırada. Satışların <strong>%29,9'u ilk el</strong>. Ağustos 2026'da satış bir yıl öncesine göre <strong>%11,4</strong> geriledi; Türkiye genelinden (%14,7) daha az.</p>"),
  ("Güven sorusu",
   "<p>Alıcı için binanın hangi deprem yönetmeliğine göre yapıldığı artık en önemli bilgilerden biri. 2018 Türkiye Bina Deprem Yönetmeliği 2019'da yürürlüğe girdi; bu tarihten sonra ruhsat almış binalar ilanlarda bunu öne çıkarıyor. Videonun başında yapı yılı, ruhsat tarihi ve varsa zemin etüdü bilgisini ekranda veriyoruz; binanın taşıyıcı sistemi, otoparkı ve ortak alanları da turun parçası.</p>"
   "<p>Bilgi doğru olmalı: ekrana yazdığımız her şeyi ilan sahibinin belgesine göre yazıyoruz.</p>"),
  ("Semte göre video",
   "<p><strong>Şehitkamil ve İbrahimli çevresi:</strong> yeni siteler, havuz ve sosyal alanlar; aile alıcılar. <strong>Şahinbey:</strong> kentsel dönüşüm ve merkezdeki eski stok; çarşıya ve hastanelere yakınlık. <strong>Nizip ve ilçeler:</strong> müstakil evler ve bahçeli mülkler.</p>"
   "<p>Gaziantep yazın sıcak; dış çekimi sabah ve akşamüstüne koyuyoruz. Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("İlan videosunda binanın deprem bilgilerini vermeli miyiz?", "Evet, alıcının ilk sorusu bu. Yapı yılı, ruhsat tarihi ve varsa zemin etüdü bilgisini belgenize göre ekranda veriyoruz."),
  ("Yeni sitedeki dairemiz için video nasıl olmalı?", "Site girişi, ortak alanlar, otopark ve sığınak gibi alanlar, ardından daire. 60–90 saniye yeterli."),
  ("Kentsel dönüşüm dairesi için ne öne çıkarılmalı?", "Binanın yeni olduğu, yapı bilgileri ve merkezi konum. Eski dokuyla yeni bina arasındaki farkı göstermek güven veriyor."),
  ("Emlak ofisi olarak düzenli çalışabilir miyiz?", "Evet. Aynı semtteki mülkleri tek güne toplayan aylık bir düzen kuruyoruz."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ İSTANBUL EMLAK
"istanbul-emlak-video": dict(
 lede="İstanbul'da son bir yılda 305.407 konut satıldı; Türkiye'deki konut satışlarının yaklaşık %18'i. Bu kadar ilanın içinde bir dairenin fark edilmesi, ilk üç saniyeye bağlı.",
 bolum=[
  ("İstanbul konut piyasası rakamlarla",
   "<p>TÜİK verisine göre Eylül 2025–Ağustos 2026 arasında İstanbul'da <strong>305.407 konut</strong> satıldı; bunların <strong>%73,5'i ikinci el</strong>. Ağustos 2026'da satış 20.426'ya geriledi; bir yıl önce 24.331'di, düşüş <strong>%16</strong>.</p>"
   "<p>İkinci elin bu kadar baskın olduğu bir piyasada aynı sokakta onlarca benzer daire satışta. Alıcı ilan sitesinde parmağıyla kaydırırken duruyorsa, bunun sebebi çoğu zaman ilk görüntü.</p>"),
  ("Semte göre alıcı",
   "<p><strong>Kadıköy, Beşiktaş, Şişli:</strong> eski ama değerli apartman daireleri; yüksek tavan, cumba, balkon ve semtin kendisi. Video sokağı ve mahalle hayatını da göstermeli.</p>"
   "<p><strong>Esenyurt, Beylikdüzü, Başakşehir:</strong> sitelerde yeni daireler; yerli ve yabancı yatırımcı. Site olanakları, metrobüse ve metroya mesafe.</p>"
   "<p><strong>Ümraniye, Ataşehir, Pendik, Kartal:</strong> Anadolu yakasında aile alıcılar; okul, ulaşım ve dönüşümle yenilenmiş binalar.</p>"
   "<p><strong>Boğaz ve Adalar:</strong> manzara ve tarihî dokuyla satılan mülkler; manzarayı gün ışığının en iyi olduğu saatte çekmek şart.</p>"),
  ("Deprem, trafik ve izin",
   "<p>İstanbul'da alıcının en çok sorduğu şeylerden biri binanın yaşı ve deprem yönetmeliğine uygunluğu; bu bilgiyi belgeye göre ekranda veriyoruz. Çekim gününü trafiğe göre planlıyor, aynı yakadaki mülkleri tek güne topluyoruz. Şehrin neredeyse tamamı drone için kontrollü hava sahasında; havadan plan gerekiyorsa izni önceden alıyoruz.</p>"
   "<p>İstanbul'da kendi ekibimizle çalışıyoruz; Bursa'dan yaklaşık iki saatte geliyoruz.</p>"),
 ],
 sss=[
  ("İstanbul'da bu kadar ilan varken video gerçekten fark eder mi?", "Evet. Kaydırarak bakan alıcıyı durduran şey ilk görüntü; video ilanınızı aynı sokaktaki benzerlerinden ayırıyor."),
  ("Eski apartman dairesi için nasıl bir video öneriyorsunuz?", "Sokaktan girişle başlayan, yüksek tavanı ve ışığı gösteren yavaş bir tur. Semtin kendisi de satılan şeyin parçası."),
  ("Drone ile çekim yapılabilir mi?", "Çoğu yerde izin gerekiyor. Konumu kontrol edip izin sürecini çekim takvimine baştan koyuyoruz."),
  ("Emlak ofisi olarak aynı gün birden fazla mülk çekebilir misiniz?", "Evet. Aynı yakadaki mülkleri trafiğe göre sıralayıp tek güne topluyoruz."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ İZMİR EMLAK
"izmir-emlak-video": dict(
 lede="İzmir'de bir dairenin değerini çoğu zaman körfez belirliyor: balkondan deniz görünüyor mu, gün batımı hangi yöne düşüyor? Karşıyaka'dan Bayraklı'ya, ilan videosunun ilk sorusu manzara.",
 bolum=[
  ("İzmir konut piyasası rakamlarla",
   "<p>TÜİK verisine göre İzmir'de son bir yılda <strong>95.859 konut</strong> satıldı; il, İstanbul ve Ankara'dan sonra üçüncü. Satılan her on konuttan yaklaşık yedisi ikinci el. Ağustos 2026'da satış 6.532'ye geriledi; bir yıl önce 7.867'ydi.</p>"),
  ("Semte göre video",
   "<p><strong>Karşıyaka, Bostanlı, Alsancak:</strong> körfeze bakan daireler; manzara satışın merkezi. Balkon ve pencere planlarını gün batımına koyuyor, sahile yürüme mesafesini gösteriyoruz.</p>"
   "<p><strong>Bayraklı:</strong> 2020 depreminden sonra dönüşümle yükselen yeni binalar ve rezidanslar. Alıcı binanın yeni olduğunu ve yapı bilgilerini görmek istiyor; bunları belgeye göre ekranda veriyoruz.</p>"
   "<p><strong>Bornova ve Buca:</strong> üniversitelere yakın, öğrenciye kiralanan daireler ve aile siteleri. Kiralıkta 30–45 saniyelik dikey tur, satılıkta tam tur.</p>"
   "<p><strong>Urla, Çeşme, Seferihisar:</strong> villa, müstakil ev ve yazlık; bahçe, havuz ve denize mesafe havadan gösterilmeli.</p>"),
  ("Çekim düzeni",
   "<p>İzmir'de yaz öğleden sonraları körfezden imbat esiyor; gökyüzü genellikle açık ve ışık temiz. Dış çekimi akşamüstüne, iç çekimi öğleye koyuyoruz. Gaziemir'deki havalimanı ve Çiğli'deki hava üssü çevresi drone için izne bağlı; mülkün konumunu önceden kontrol ediyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde İzmir'deki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Körfez manzarasını videoda nasıl öne çıkarırsınız?", "Balkon ve pencere planlarını gün batımına koyuyor, manzarayı içeriden dışarıya açılan tek bir planla gösteriyoruz."),
  ("Bornova'daki kiralık dairemiz için ne çekmeliyiz?", "30–45 saniyelik dikey bir tur; üniversiteye ve metroya mesafeyi ekranda yazıyoruz."),
  ("Bayraklı'daki yeni binada hangi bilgileri vermeliyiz?", "Yapı yılı, ruhsat tarihi ve varsa zemin bilgisi; hepsini belgenize göre yazıyoruz."),
  ("Çeşme'deki villamız için ne önerirsiniz?", "Havadan arsa ve denize mesafe, havuz ve bahçe, ardından iç tur. Yazlık alıcı için Nisan–Mayıs'ta çekim."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ KOCAELİ EMLAK
"kocaeli-emlak-video": dict(
 lede="Kocaeli'de kiralık ve satılık dairelerin önemli bir kısmının alıcısı fabrikada çalışıyor: mühendis, teknisyen, yönetici. Bu alıcı için en önemli bilgi, evden işe kaç dakika olduğu.",
 bolum=[
  ("Kocaeli konut piyasası",
   "<p>TÜİK'e göre Kocaeli'de son bir yılda <strong>47.112 konut</strong> satıldı; il Türkiye'de yedinci. Ağustos 2026'da satış bir önceki ağustosa göre yalnızca <strong>%6</strong> düştü; Türkiye genelinde düşüş %14,7. Sanayinin taşıdığı bir piyasa: iş olduğu sürece konut talebi de sürüyor.</p>"),
  ("Alıcıya göre video",
   "<p><strong>Sanayi çalışanı:</strong> Gebze, Çayırova, Dilovası ve Körfez'deki organize sanayi bölgelerine yakın siteler ve daireler. Videoda servis güzergâhına, otoyola ve Marmaray'a mesafeyi baştan veriyoruz. Şirket lojmanı ve kiralık daire ilanları için kısa, bilgi yoğun dikey turlar.</p>"
   "<p><strong>Aile alıcı:</strong> İzmit, Başiskele ve Kartepe'de bahçeli siteler, okul ve sosyal alanlar. Körfez ya da orman manzarası olan mülklerde havadan bir plan.</p>"
   "<p><strong>Yatırımcı:</strong> İstanbul'a yakın Gebze ve Darıca'da yeni projeler; kira getirisi ve ulaşım bağlantısı.</p>"),
  ("Bursa'dan bir saat",
   "<p>Kocaeli'de kendi ekibimizle çalışıyoruz; Bursa'dan Osmangazi Köprüsü üzerinden yaklaşık bir saatte geliyoruz. Emlak ofisleri için Gebze ve İzmit tarafını ayrı günlere ayırıp her gün birkaç mülk çekiyoruz. Gebze tarafı Sabiha Gökçen'e, İzmit tarafının bir kısmı askerî ve kritik tesislere yakın; drone planını her mülk için ayrıca kontrol ediyoruz.</p>"),
 ],
 sss=[
  ("Sanayi çalışanına yönelik kiralık için ne çekmeliyiz?", "30–45 saniyelik dikey tur ve ekranda fabrikaya, otoyola, Marmaray'a mesafe. Bu alıcı kararını hızlı veriyor."),
  ("Başiskele'deki bahçeli ev için ne önerirsiniz?", "Havadan bahçe ve çevre, körfez ya da orman manzarası, ardından iç tur."),
  ("Gebze'de drone ile çekim yapılabilir mi?", "Sabiha Gökçen'e yakınlık nedeniyle çoğu konum izne bağlı. Mülkün yerini kontrol edip önceden söylüyoruz."),
  ("Aylık portföy çekimi yapıyor musunuz?", "Evet. Gebze ve İzmit tarafını ayrı günlere ayırıp her ay düzenli çekim yapıyoruz."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ KONYA EMLAK
"konya-emlak-video": dict(
 lede="Konya'da satılan her beş konuttan ikisi sıfır. Düz ve geniş bir şehirde yeni siteler hızla yükseliyor; alıcı için soru hangi sitenin daha iyi yaşattığı.",
 bolum=[
  ("Konya konut piyasası rakamlarla",
   "<p>TÜİK verisine göre Eylül 2025–Ağustos 2026 arasında Konya'da <strong>43.814 konut</strong> satıldı; bunların <strong>%41,6'sı ilk el</strong>. Bu oran Türkiye ortalamasının (%33,5) epey üzerinde; Konya'da rekabet en çok yeni projeler arasında. Ağustos 2026'da satış bir yıl öncesine göre <strong>%10,3</strong> geriledi.</p>"),
  ("Semte göre video",
   "<p><strong>Selçuklu:</strong> yeni siteler, geniş bulvarlar ve tramvay hattı. Alıcı aile; sosyal alan, otopark, okul ve tramvaya mesafe. Sitenin yerleşimini havadan, daireyi tek akıcı turla gösteriyoruz.</p>"
   "<p><strong>Meram:</strong> bağ evleri, müstakil ev ve villalar; yeşil, bahçe ve sessizlik. Bahçe ve çevre havadan.</p>"
   "<p><strong>Karatay:</strong> merkezde eski stok ve dönüşüm projeleri; çarşıya, Mevlana'ya ve hastanelere yakınlık.</p>"
   "<p><strong>Öğrenci kiralığı:</strong> üniversitelere yakın daireler; Eylül öncesi kısa dikey turlar.</p>"),
  ("Çekim düzeni",
   "<p>Konya'nın ışığı geniş ve açık; ama yazın öğle saatinde sert. Dış çekimi sabah ya da akşamüstüne koyuyoruz. Kışın ise kar sonrası açık bir gün, siteleri en temiz gösteren an. Havalimanının askerî üsle ortak olması nedeniyle şehrin bir kısmında drone uçuşu izne bağlı; her mülkü haritadan kontrol ediyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Yeni sitedeki dairemizi rakip sitelerden nasıl ayırırız?", "Sitenin yaşamını göstererek: ortak alanlar, çocuk parkı, otopark, güvenlik. Sonra daire. Alıcı daireden önce siteyi seçiyor."),
  ("Meram'daki bağ evi için ne önerirsiniz?", "Havadan bahçe ve çevre, ağaçların arasından eve yaklaşan bir plan, ardından iç tur."),
  ("Öğrenci kiralığı için ne zaman çekim yapmalıyız?", "Ağustos ortasında; ilan Eylül başında yayında olmalı."),
  ("Konya'da drone ile çekim yapılabilir mi?", "Konuma bağlı; havalimanı çevresinde izin gerekiyor. Mülkün yerini kontrol edip önceden söylüyoruz."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ MANİSA EMLAK
"manisa-emlak-video": dict(
 lede="Manisa'da daire arayanların bir kısmı İzmir'de çalışıyor ama Manisa'da oturmak istiyor; bir kısmı OSB'de çalışıyor ve fabrikaya yakın bir ev arıyor. İki alıcının da ilk sorusu aynı: işe kaç dakika?",
 bolum=[
  ("Manisa'da satılan konutlar",
   "<p>TÜİK'e göre Manisa'da Eylül 2025–Ağustos 2026 arasında <strong>26.040 konut</strong> satıldı; il Türkiye'de 20. sırada. Satılanların <strong>%36'sı sıfır konut</strong>. Ağustos 2026'da satış 1.752'ye indi; bir önceki ağustosta 2.149'du, düşüş <strong>%18,5</strong>.</p>"),
  ("İlçeye göre alıcı",
   "<p><strong>Yunusemre ve Şehzadeler:</strong> şehrin iki merkez ilçesinde yeni siteler ve apartmanlar. Organize sanayi bölgesinde çalışan aileler için OSB'ye, okula ve hastaneye mesafe videonun başında.</p>"
   "<p><strong>Turgutlu:</strong> İzmir'e yakınlığıyla, İzmir'de çalışıp daha uygun fiyata ev arayan aileler için. Otoyola ve İzmir'e mesafeyi baştan veriyoruz.</p>"
   "<p><strong>Akhisar ve Salihli:</strong> kendi çarşısı, okulu ve iş hayatı olan büyük ilçeler; ilçede yaşayan aileler için daire ve müstakil ev.</p>"
   "<p><strong>Bağ ve bahçe evi:</strong> Salihli, Alaşehir ve Sarıgöl'de bağın içinde evler; arsa sınırı ve bağ havadan gösterilmeli.</p>"),
  ("Çekim düzeni",
   "<p>Manisa yazın çok sıcak; dış çekimi sabaha ve akşamüstüne koyuyoruz. Şehrin arkasında yükselen Spil Dağı, havadan açılış planı için güçlü bir fon. İlçeler arası mesafe bir saati bulabildiği için portföyü ilçe ilçe gruplayıp aynı güne birkaç mülk koyuyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; çekim günlerinde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Turgutlu'daki dairemizi İzmir'deki alıcıya nasıl anlatırız?", "İzmir'e ve otoyola mesafeyi baştan veren, sitenin olanaklarını ve daireyi gösteren 60 saniyelik bir video."),
  ("OSB çalışanına yönelik ilan için neyi öne çıkarmalıyız?", "Fabrikaya, servis güzergâhına ve okula mesafe. Ekranda kısa yazılarla veriyoruz."),
  ("Bağ evi ilanı nasıl çekilmeli?", "Havadan bağ ve arsa sınırı, bağın içinden eve yaklaşan bir plan, ardından iç tur."),
  ("Aynı gün farklı ilçelerde çekim yapabilir misiniz?", "Mesafeye göre evet; portföyü ilçe ilçe gruplayıp günü buna göre planlıyoruz."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ MERSİN EMLAK
"mersin-emlak-video": dict(
 lede="Mersin'de son bir yılda 56.385 konut satıldı; il Türkiye'de altıncı. Mezitli'nin deniz manzaralı kulelerinden Erdemli'nin yazlıklarına, Mersin'in konutu büyük ölçüde denize bakıyor.",
 bolum=[
  ("Mersin konut piyasasında son durum",
   "<p>TÜİK verisine göre Mersin'de Eylül 2025–Ağustos 2026 döneminde <strong>56.385 konut</strong> el değiştirdi; bunların <strong>20.254'ü (%35,9) ilk el</strong>. Ağustos 2026'da satış bir yıl öncesine göre <strong>%19,6</strong> düştü (5.088'den 4.090'a); Türkiye genelindeki düşüşün belirgin üzerinde.</p>"),
  ("Bölgeye göre alıcı",
   "<p><strong>Mezitli ve Yenişehir:</strong> sahile paralel yükselen, havuzlu ve sosyal tesisli yeni siteler; yerli alıcının yanında yabancı alıcının da ilgi gösterdiği bölge. Deniz manzarası, kat yüksekliği ve sitenin olanakları videonun merkezinde.</p>"
   "<p><strong>Erdemli, Kızkalesi ve Silifke:</strong> yazlık daireler ve sahil siteleri; alıcı çoğu zaman İç Anadolu'dan, yazı geçirmek için ev arıyor. Plaja mesafe ve sahil yaşamı.</p>"
   "<p><strong>Tarsus:</strong> kendi iş hayatı olan büyük bir ilçe; aile alıcılar için daire ve müstakil ev.</p>"
   "<p><strong>Toroslar ve yayla evleri:</strong> Gözne ve çevresinde yaz sıcağından kaçmak için yayla evleri; serinlik ve manzara.</p>"),
  ("Nem, ışık ve drone",
   "<p>Mersin'de yaz nemli; öğleden sonra hava puslanıyor ve deniz manzarası soluk görünüyor. Deniz manzaralı daireleri sabah erken ya da gün batımında çekiyoruz. Yeni havalimanı Tarsus tarafında; şehir merkezinde ve sahil boyunca drone planı çoğu konumda daha esnek, yine de her mülkü haritadan kontrol ediyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; çekim günlerinde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Mezitli'deki deniz manzaralı dairemiz için ne önerirsiniz?", "Manzarayı sabah ya da gün batımında, salondan balkona açılan tek bir planla göstermek; ardından sitenin havuzu ve ortak alanları."),
  ("Yazlık daire ilanı ne zaman çekilmeli?", "Mayıs başında; ilan yazlık arayanların karar verdiği haftalara hazır olmalı."),
  ("Yabancı alıcı için altyazı ekliyor musunuz?", "Evet. İngilizce, Rusça, Arapça ya da ihtiyaç duyulan dilde."),
  ("Yayla evinin manzarasını nasıl gösterirsiniz?", "Havadan bir açılış planı ve terastan manzara; serinliği anlatan yeşil ve gölge planları."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ MUĞLA EMLAK
"mugla-emlak-video": dict(
 lede="Bodrum'da bir villanın, Fethiye'de bir taş evin, Datça'da bir bahçeli müstakilin alıcısı çoğu zaman ülkenin öbür ucunda ya da yurt dışında. Muğla'da ilan videosu, mülkün ilk gezisi.",
 bolum=[
  ("İkinci konutun ili",
   "<p>Muğla'da son on iki ayda TÜİK kayıtlarına göre <strong>22.730 konut</strong> satıldı; satışların <strong>%31'i ilk el</strong>. Ağustos 2026'da satış bir yıl öncesine göre <strong>%13,7</strong> geriledi; Türkiye genelinden biraz daha az. Muğla'da satılan konutların önemli bir kısmı ikinci konut ve yatırım; alıcı çoğu zaman il dışında.</p>"),
  ("Bölgeye göre video",
   "<p><strong>Bodrum yarımadası:</strong> Yalıkavak, Gündoğan, Türkbükü ve Turgutreis'te deniz manzaralı villa ve siteler. Manzara, havuz, mahremiyet ve koya mesafe; havadan bir plan şart.</p>"
   "<p><strong>Fethiye ve Göcek:</strong> yabancı alıcının uzun yıllardır yaşadığı bir bölge; Ovacık ve Hisarönü'nde havuzlu villalar, Kayaköy çevresinde taş evler. İngilizce altyazılı video.</p>"
   "<p><strong>Marmaris ve Datça:</strong> yazlık daire ve bahçeli evler; denize ve çarşıya mesafe.</p>"
   "<p><strong>Menteşe:</strong> il merkezi; üniversite öğrencilerine kiralanan daireler ve şehirde yaşayan aileler için konut.</p>"),
  ("Çekim ve izinler",
   "<p>Milas-Bodrum ve Dalaman havalimanlarının çevresi kontrollü hava sahası; Bodrum ve Dalaman tarafındaki bazı mülklerde drone planı izin istiyor. Kıyıda sit alanları ve koruma bölgeleri de var. Yaz rüzgârı öğleden sonra artıyor; drone planlarını sabaha, villa dış çekimini gün batımına koyuyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; çekim günlerinde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Bodrum'daki villamız için ne çekmeliyiz?", "Havadan villa, havuz ve koya mesafe; gün batımında teras ve manzara; ardından iç tur. 90–120 saniye."),
  ("Fethiye'deki yabancı alıcıya nasıl ulaşırız?", "İngilizce altyazılı, manzara ve yaşam odaklı bir video; havalimanına ve sahile mesafeyle."),
  ("Drone için izin gerekiyor mu?", "Havalimanlarına yakın bölgelerde evet. Konumu kontrol edip izin sürecini takvime baştan koyuyoruz."),
  ("Sit alanındaki taş ev için nelere dikkat etmeliyiz?", "Koruma kuralları ve izinli tadilatlar alıcının sorduğu ilk şeyler; belgenize dayanarak bu bilgiyi videoda veriyoruz."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ SAKARYA EMLAK
"sakarya-emlak-video": dict(
 lede="Adapazarı'nda alıcının ilk sorusu çoğu zaman zemin. 1999'da yaşanan depremden sonra Sakarya'da binanın nerede ve nasıl yapıldığı, kaç odalı olduğundan önce soruluyor.",
 bolum=[
  ("Dirençli bir piyasa",
   "<p>TÜİK verilerine bakınca Sakarya'da son on iki ayda <strong>28.081 konut</strong> satıldı; il Türkiye'de 17. sırada. Satılanların <strong>%39,2'si sıfır konut</strong>. Ağustos 2026'da satış bir yıl öncesiyle aynı düzeyde kaldı (2.423); Türkiye genelinde %14,7 düşüş varken Sakarya'nın piyasası dirençli.</p>"),
  ("Zemin ve güven",
   "<p>Adapazarı ovası alüvyon zemin üzerinde kurulu; bu yüzden şehirde yeni projeler zemin iyileştirmesi ve daha az katlı yapılarla öne çıkıyor. İlan videosunda yapı yılını, ruhsat tarihini ve varsa zemin etüdü bilgisini belgeye göre ekranda veriyoruz. Alıcı bu bilgiyi videonun başında görünce mülkü listesine alıyor.</p>"),
  ("Bölgeye göre alıcı",
   "<p><strong>Serdivan:</strong> üniversiteye yakın, öğrenciye kiralanan daireler ve yeni siteler. Kiralıkta kısa dikey tur, satılıkta tam tur.</p>"
   "<p><strong>Sapanca ve Kırkpınar:</strong> göl manzaralı villa, müstakil ev ve bungalov arazileri; alıcı çoğu zaman İstanbul'dan. Havadan göl ve orman, bahçe ve mahremiyet.</p>"
   "<p><strong>Karasu:</strong> Karadeniz kıyısında yazlık daireler; plaja mesafe ve yaz yaşamı.</p>"
   "<p>Sakarya'da kendi ekibimizle çalışıyoruz; Bursa'dan yaklaşık iki saatte geliyoruz. Sapanca ve Serdivan'daki mülkleri aynı güne topluyoruz.</p>"),
 ],
 sss=[
  ("İlan videosunda zemin bilgisini vermeli miyiz?", "Adapazarı'nda alıcının ilk sorusu bu. Belgeniz varsa yapı yılı, ruhsat ve zemin bilgisini ekranda veriyoruz."),
  ("Sapanca'daki villamızı İstanbul'daki alıcıya nasıl anlatırız?", "Havadan göl ve orman, villaya yaklaşan bir plan, bahçe ve iç tur. İstanbul'a mesafeyi de ekranda veriyoruz."),
  ("Karasu'daki yazlık için ne zaman çekim yapmalıyız?", "Mayıs sonunda; deniz ve plaj yaz görüntüsünü verirken kalabalık henüz başlamamış oluyor."),
  ("Bursa'dan mı geliyorsunuz?", "Evet, kendi ekibimizle; yaklaşık iki saatlik yol. Birden fazla mülkü aynı güne topluyoruz."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ SAMSUN EMLAK
"samsun-emlak-video": dict(
 lede="Samsun'da satılan konutların %43,7'si sıfır; Türkiye ortalamasının on puan üzerinde. Atakum sahilinde yükselen kuleler, alıcının önüne aynı manzarayı vaat eden onlarca proje koyuyor.",
 bolum=[
  ("Samsun'da satılan konutlar",
   "<p>TÜİK'e göre Samsun'da Eylül 2025–Ağustos 2026 arasında <strong>32.946 konut</strong> satıldı; il Türkiye'de 15. sırada. Bunların <strong>14.383'ü ilk el</strong>. Ağustos 2026'da satış bir yıl öncesine göre <strong>%11,6</strong> düştü; Türkiye geneline göre daha az.</p>"
   "<p>Bu kadar yeni projenin olduğu bir piyasada rekabet en çok müteahhitler arasında; aynı sahil hattında, aynı manzarayı satan projeler birbirinden görselle ayrışıyor.</p>"),
  ("Bölgeye göre video",
   "<p><strong>Atakum:</strong> sahile paralel yükselen siteler ve kuleler; deniz manzarası, kat yüksekliği ve site olanakları. Hangi kattan neyin göründüğünü gerçek yükseklikten drone ile göstermek, aynı manzarayı vaat eden projeler arasında fark yaratıyor.</p>"
   "<p><strong>Kurupelit ve üniversite çevresi:</strong> öğrenciye kiralanan daireler; kısa dikey turlar.</p>"
   "<p><strong>İlkadım ve Canik:</strong> şehrin merkezinde eski stok ve dönüşüm; çarşıya, hastaneye ve tramvaya yakınlık.</p>"
   "<p><strong>Bafra ve Çarşamba:</strong> ova ilçelerinde müstakil ev ve bahçeli mülkler.</p>"),
  ("Çekim düzeni",
   "<p>Karadeniz kıyısında hava gün içinde değişebiliyor; deniz manzaralı daireler için açık bir sabah ya da gün batımı bekliyoruz ve yedek gün koyuyoruz. Havalimanı Çarşamba'da, şehrin doğusunda; Atakum ve merkezdeki mülklerde drone planı çoğu zaman daha esnek, yine de her konumu kontrol ediyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; çekim günlerinde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Atakum'daki projemizi rakiplerden nasıl ayırırız?", "Her katın gerçek manzarasını drone ile göstererek ve sitenin yaşamını anlatarak. Alıcı aynı manzara vaadini her projede duyuyor; gerçeğini görmek istiyor."),
  ("Hava kapalıysa çekim ne olur?", "Deniz manzaralı mülklerde yedek gün koyuyoruz; iç çekimleri kapalı havada da yapabiliyoruz."),
  ("Öğrenci kiralığı için ne önerirsiniz?", "30–45 saniyelik dikey tur ve üniversiteye, tramvaya mesafe."),
  ("Müteahhit olarak satış öncesi video yaptırabilir miyiz?", "Evet. Bitmemiş projede gerçek manzara görüntüsünü 3D render ile birleştirerek satışa başlayabiliyorsunuz."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ TRABZON EMLAK
"trabzon-emlak-video": dict(
 lede="Trabzon'da evlerin çoğu yamaçta; bir dairenin değeri büyük ölçüde balkondan denizin görünüp görünmediğine bağlı. Alıcının bir kısmı da yurt dışından, özellikle Körfez ülkelerinden.",
 bolum=[
  ("Trabzon'da satılan konutlar",
   "<p>TÜİK'e göre Trabzon'da Eylül 2025–Ağustos 2026 arasında <strong>10.829 konut</strong> satıldı; satışların <strong>%29,1'i ilk el</strong>. Ağustos 2026'da satış bir yıl öncesine göre <strong>%16,3</strong> geriledi (1.017'den 851'e).</p>"),
  ("Bölgeye göre video",
   "<p><strong>Ortahisar ve sahil:</strong> şehrin merkezinde, denize bakan daireler; manzara, kat ve cephe. Yamaçta eğimli sokakları ve binanın konumunu havadan göstermek, alıcının en çok merak ettiği şeyi anlatıyor.</p>"
   "<p><strong>Akçaabat ve Yomra:</strong> sahil boyunca yeni siteler; deniz manzarası ve ulaşım.</p>"
   "<p><strong>Yayla ve dağ evleri:</strong> Uzungöl, Hıdırnebi ve diğer yaylalarda ahşap yayla evleri; Körfez ülkelerinden gelen alıcının da ilgi gösterdiği mülkler. Arapça altyazılı, doğayı ve sisi gösteren video.</p>"),
  ("Hava ve çekim",
   "<p>Trabzon'da hava gün içinde birkaç kez değişebiliyor; deniz manzaralı daireler için açık bir saat bekliyor, yedek gün koyuyoruz. Havalimanı şehir merkezine çok yakın ve sahil boyunca uzanıyor; merkez ve sahil hattındaki mülklerde drone çoğu zaman izne bağlı. Yayla mülklerinde havadan plan daha kolay.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; çekim günlerinde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
 ],
 sss=[
  ("Yamaçtaki dairemizin manzarasını nasıl gösterirsiniz?", "Salondan balkona açılan tek bir planla; drone izni varsa binanın konumunu ve eğimi havadan da gösteriyoruz."),
  ("Körfez ülkelerinden alıcı için ne önerirsiniz?", "Arapça altyazılı, doğayı ve yaylayı öne çıkaran kısa bir video; havalimanına mesafeyi de ekranda veriyoruz."),
  ("Merkezde drone uçuşu yapılabilir mi?", "Havalimanına yakınlık nedeniyle çoğu yerde izin gerekiyor. Konumu kontrol edip önceden söylüyoruz."),
  ("Yayla evini ne zaman çekmeliyiz?", "Yaz başında; yayla yeşil ve yol açık. Sisli ve açık havayı ayrı ayrı yakalamak için yedek gün koyuyoruz."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ YALOVA EMLAK
"yalova-emlak-video": dict(
 lede="Yalova'da satılan konutların önemli bir kısmının alıcısı İstanbul'da yaşıyor: emekli olunca taşınmak, yazı geçirmek ya da deniz otobüsüyle işe gidip gelmek için. Bu alıcı mülkü önce telefonda geziyor.",
 bolum=[
  ("Yalova'da satılan konutlar",
   "<p>TÜİK'e göre Yalova'da son bir yılda <strong>15.578 konut</strong> satıldı; il Türkiye'de 23. sırada, nüfusuna göre yüksek bir sayı. Satışların <strong>%31,3'ü ilk el</strong>. Ağustos 2026'da satış bir yıl öncesine göre <strong>%23,3</strong> düştü (1.506'dan 1.155'e); Türkiye genelindeki düşüşün belirgin üzerinde.</p>"),
  ("Bölgeye göre alıcı",
   "<p><strong>Çınarcık ve Esenköy:</strong> deniz kenarında yazlık daireler ve siteler; alıcı İstanbullu. Denize, iskeleye ve deniz otobüsüne mesafe.</p>"
   "<p><strong>Armutlu ve Termal:</strong> termal suyu olan siteler ve emeklilerin tercih ettiği sakin bölgeler; doğa ve sağlık vurgusu.</p>"
   "<p><strong>Yalova merkez:</strong> iskeleye yakın daireler; İstanbul'a deniz yoluyla günlük gidip gelen çalışanlar için.</p>"
   "<p><strong>Altınova ve köyler:</strong> bahçeli müstakil evler ve tarım arazileri; arsa sınırı havadan.</p>"),
  ("Bursa'dan bir saat",
   "<p>Yalova'da kendi ekibimizle çalışıyoruz; Bursa'dan yaklaşık bir saatte geliyoruz. Çınarcık ve merkezdeki mülkleri aynı güne koyabiliyoruz. Yazlık alıcısı kararını baharda veriyor; ilanı Nisan–Mayıs'ta çekmenizi öneriyoruz.</p>"
   "<p>Satışların yavaşladığı bir dönemde video, ilanınızı benzerlerinden ayırıyor ve gezmeye gelen alıcının gerçekten ilgili olmasını sağlıyor.</p>"),
 ],
 sss=[
  ("İstanbul'daki alıcıya Yalova'daki dairemizi nasıl anlatırız?", "Deniz otobüsüne ve iskeleye mesafeyi baştan veren, manzarayı ve siteyi gösteren 60–90 saniyelik bir video."),
  ("Yazlık ilanı ne zaman çekilmeli?", "Nisan–Mayıs. Hava açık, sahil boş ve ilan yaz başına hazır oluyor."),
  ("Termal'deki sitemiz için neyi öne çıkarmalıyız?", "Termal suyu, doğayı ve sakin yaşamı; havuz, yürüyüş yolları ve çevre."),
  ("Bursa'dan mı geliyorsunuz?", "Evet, kendi ekibimizle; yaklaşık bir saatlik yol."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ ÇANAKKALE EMLAK
"canakkale-emlak-video": dict(
 lede="1915 Çanakkale Köprüsü açıldıktan sonra Gelibolu ile Lapseki arası dakikalara indi. Çanakkale'nin konut piyasası, köprünün iki yakasında yeniden şekilleniyor.",
 bolum=[
  ("Çanakkale'de satılan konutlar",
   "<p>TÜİK'e göre Çanakkale'de Eylül 2025–Ağustos 2026 arasında <strong>14.166 konut</strong> satıldı; satışların <strong>%38,7'si ilk el</strong>, Türkiye ortalamasının (%33,5) üzerinde. Ağustos 2026'da satış yalnızca <strong>%5,1</strong> geriledi; Türkiye genelinde düşüş %14,7. Yeni projelerin bol olduğu ve görece dirençli bir piyasa.</p>"),
  ("Bölgeye göre alıcı",
   "<p><strong>Merkez, Kepez ve Güzelyalı:</strong> Boğaz'a bakan daireler ve yeni siteler; üniversiteye yakın kiralıklar. Boğaz manzarası ve gemi trafiği, Çanakkale'ye özgü bir görüntü.</p>"
   "<p><strong>Lapseki ve Gelibolu:</strong> köprüyle birlikte ilgi artan iki yaka; yeni projeler ve arsalar. Köprüye ve otoyola mesafe.</p>"
   "<p><strong>Assos, Ayvacık ve Küçükkuyu:</strong> taş evler, zeytinlikler ve deniz manzaralı villalar; alıcı İstanbul'dan. Havadan arsa ve manzara.</p>"
   "<p><strong>Bozcaada ve Gökçeada:</strong> adada taş evler ve bağ evleri; feribot bağlantısı ve ada yaşamı.</p>"),
  ("Çekim düzeni",
   "<p>Çanakkale rüzgârlı bir il; drone planlarını rüzgârın sakin olduğu sabah saatlerine koyuyoruz. Boğaz kıyısındaki askerî alanlar ve havalimanı çevresi izne bağlı; ada ve Kaz Dağları eteğindeki mülklerde uçuş daha esnek, yine de her konumu kontrol ediyoruz.</p>"
   "<p>Çanakkale'de kendi ekibimizle çalışıyoruz; adalar ve Assos için bir gece konaklayarak gün batımı ve sabah ışığını birlikte almayı öneriyoruz.</p>"),
 ],
 sss=[
  ("Boğaz manzaralı dairemizi nasıl gösterirsiniz?", "Salondan balkona açılan bir planla ve geçen bir geminin önünde; manzarayı Çanakkale'ye özgü kılan şey bu hareket."),
  ("Assos'taki taş evimiz için ne önerirsiniz?", "Havadan zeytinlik ve deniz, taş dokuyu gösteren detaylar ve avlu; gün batımında teras."),
  ("Rüzgârlı havada drone uçabiliyor mu?", "Belirli bir hıza kadar evet; ama en temiz görüntü için sakin sabah saatlerini seçiyoruz."),
  ("Bozcaada'ya da geliyor musunuz?", "Evet. Feribot saatine göre bir gün ya da bir gece konaklamayla planlıyoruz."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ BOLU EMLAK
"bolu-emlak-video": dict(
 lede="Bolu'da ev arayanların bir kısmı orada yaşıyor, bir kısmı İstanbul ile Ankara arasında ikinci bir ev, ormanın içinde bir hafta sonu evi arıyor. Bolu'da ilan videosu, ormanı ve sessizliği de satmalı.",
 bolum=[
  ("Bolu'da satılan konutlar",
   "<p>TÜİK'e göre Bolu'da Eylül 2025–Ağustos 2026 arasında <strong>8.005 konut</strong> satıldı; satışların <strong>%31'i ilk el</strong>. Ağustos 2026'da satış bir yıl öncesine göre <strong>%22,1</strong> düştü (653'ten 509'a); Türkiye genelindeki düşüşün belirgin üzerinde. Daha sakin bir piyasada ilanın sunumu daha çok fark ediyor.</p>"),
  ("Mülk tipine göre video",
   "<p><strong>Şehir merkezi:</strong> üniversite öğrencilerine kiralanan daireler ve şehirde yaşayan aileler için konut; kampüse ve çarşıya mesafe.</p>"
   "<p><strong>Dağ evi ve bungalov:</strong> Abant, Gölcük ve Yedigöller yönünde ormanın içinde ahşap evler. Alıcı İstanbul ya da Ankara'dan; doğayı, şömineyi ve sessizliği görmek istiyor. Kışın karla, yazın yeşille iki ayrı video.</p>"
   "<p><strong>Mudurnu ve Göynük:</strong> tarihî dokusu korunmuş ilçelerde ahşap konaklar; restorasyon ve doku.</p>"),
  ("Mevsim ve çekim",
   "<p>Bolu kışın karlı; dağ evi ve bungalovlar için karlı bir sabah, ilanın en güçlü görüntüsü. Yollar ve erişim kar sonrası değişebildiği için çekim tarihini havaya göre esnek tutuyoruz. Sonbaharda ise orman sarı ve kırmızıya dönüyor; ikinci konut alıcısının en çok aradığı mevsim.</p>"
   "<p>Bolu'da kendi ekibimizle çalışıyoruz.</p>"),
 ],
 sss=[
  ("Dağ evimizi kışın mı yazın mı çekmeliyiz?", "İkisini de öneriyoruz: kış sezonu için karla, yaz ve sonbahar için yeşil ve renkli ormanla. Aynı mülkten iki ayrı video."),
  ("Öğrenci kiralığı için ne önerirsiniz?", "30–45 saniyelik dikey tur ve kampüse, çarşıya mesafe; Ağustos sonunda yayında olmalı."),
  ("Ormandaki evimizi havadan çekebilir misiniz?", "Evet; konumu haritadan kontrol edip uçuş planını önceden yapıyoruz."),
  ("Mudurnu'daki konağımız için nasıl bir video olmalı?", "Ahşap dokuyu, odaları ve avluyu gösteren yavaş bir tur; restorasyon detayları yakın planda."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ DÜZCE EMLAK
"duzce-emlak-video": dict(
 lede="Düzce, 1999 depreminden sonra neredeyse yeniden kurulan bir şehir. Bugün satılan konutların önemli bir kısmı bu yeni dokunun içinde; alıcı da binanın yaşını ve yapısını ilk sırada soruyor.",
 bolum=[
  ("Otoyolun üzerindeki şehir",
   "<p>Resmî verilere göre Düzce'de bir yıl içinde (Eylül 2025–Ağustos 2026) <strong>8.523 konut</strong> satıldı; satışların <strong>%35,1'i ilk el</strong>. Ağustos 2026'da satış bir yıl öncesine göre yalnızca <strong>%4,5</strong> geriledi; Türkiye genelindeki düşüşün çok altında. İstanbul–Ankara otoyolu üzerindeki konumu ve görece uygun fiyatları ilin talebini canlı tutuyor.</p>"),
  ("Mülk tipine göre video",
   "<p><strong>Şehir merkezi ve yeni siteler:</strong> aile alıcılar için yeni daireler. Yapı yılını, ruhsat tarihini ve varsa zemin etüdü bilgisini belgeye göre ekranda veriyoruz; Düzce'de alıcının ilk sorusu bu.</p>"
   "<p><strong>Akçakoca:</strong> Karadeniz kıyısında yazlık daireler ve deniz manzaralı siteler; alıcı İstanbul ve Ankara'dan. Plaja mesafe ve yaz yaşamı.</p>"
   "<p><strong>Konuralp ve kırsal:</strong> bahçeli müstakil evler ve arsalar; fındık bahçeleri arasında. Arsa sınırı havadan.</p>"
   "<p><strong>Öğrenci kiralığı:</strong> üniversiteye yakın daireler; kısa dikey turlar.</p>"),
  ("Çekim düzeni",
   "<p>Düzce'de kendi ekibimizle çalışıyoruz. Karadeniz ikliminde hava gün içinde değişebiliyor; deniz manzaralı Akçakoca mülkleri için açık bir saat bekliyoruz. Şehirde havalimanı yok; drone planı çoğu konumda esnek, yine de her mülkü haritadan kontrol ediyoruz.</p>"),
 ],
 sss=[
  ("İlan videosunda yapı bilgilerini vermeli miyiz?", "Kesinlikle. Binanın 1999 sonrası hangi yönetmeliğe göre yapıldığı Düzce'de satışın kilidi; belgenize dayanarak ekranda gösteriyoruz."),
  ("Akçakoca'daki yazlığımızı nasıl anlatırız?", "Denize ve plaja mesafe, manzara ve sitenin yaz yaşamı; 60 saniyelik bir video."),
  ("Fındık bahçeli arsamız için ne önerirsiniz?", "Havadan arsa sınırı, yol bağlantısı ve bahçe; kısa bir ilan videosu."),
  ("Hava kapalıysa çekim ne olur?", "İç çekimi yapıyor, dış ve manzara planları için yedek gün koyuyoruz."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ ADIYAMAN EMLAK
"adiyaman-emlak-video": dict(
 lede="Şubat 2023 depremlerinden sonra Adıyaman'da konut, yeniden kurulan mahallelerin konusu. Bugün alıcının görmek istediği şey, yeni binanın nasıl ve ne zaman yapıldığı.",
 bolum=[
  ("Yeniden yapılanan bir piyasa",
   "<p>TÜİK'e göre Adıyaman'da Eylül 2025–Ağustos 2026 arasında <strong>6.493 konut</strong> satıldı; satışların <strong>%30,2'si ilk el</strong>. Ağustos 2026'da satış bir yıl öncesine göre <strong>%17,7</strong> geriledi (621'den 511'e).</p>"
   "<p>Depremden sonra şehrin önemli bir kısmında yeni binalar yükseliyor. Bu ortamda ilan videosunun ilk işi güven vermek: binanın yapı yılı, ruhsat tarihi ve varsa zemin etüdü bilgisi, ilan sahibinin belgesine göre ekranda. Ardından daire, ortak alanlar ve çevre.</p>"),
  ("Adıyaman'da hangi mülk, nasıl anlatılır",
   "<p><strong>Yeni siteler ve daireler:</strong> aile alıcılar için oda düzeni, otopark ve sığınak gibi ortak alanlar; okula ve hastaneye mesafe.</p>"
   "<p><strong>Kahta ve Atatürk Barajı kıyısı:</strong> göl manzaralı arsalar ve müstakil evler; manzara ve arsa sınırı havadan.</p>"
   "<p><strong>Bahçeli müstakil ev:</strong> tek katlı, bahçeli evler; depremden sonra bu tipe ilgi arttı. Bahçeyi ve yapının tamamını gösteren bir dış plan.</p>"),
  ("Çekim düzeni",
   "<p>Temmuz ve Ağustos'ta öğle saatlerinde ışık sert ve sıcaklık yüksek; dış cepheyi ve bahçeyi güneş alçalınca, iç mekânı gün ortasında çekiyoruz. Baraj gölü kıyısındaki mülklerde gün batımı, suyun üzerinde en sıcak rengi veriyor.</p><p>Görüntü yönetimi ve kurgu bizim ekipte; çekim gününde bölgede birlikte çalıştığımız kamera ekibiyle sahadayız.</p>"),
  ("Nemrut'un ili, yeni mahalleleri",
   "<p>Adıyaman'ın merkezinde yeni konut alanları şehrin dışına doğru genişliyor; alıcı çoğu zaman eski mahallesinden uzaklaşan bir aile. Bu aileye yeni mahallenin günlük hayatını göstermek gerekiyor: en yakın okul, market, cami ve otobüs durağı. Videonun sonuna mahalleyi gösteren kısa bir sürüş planı ekliyoruz. Kahta tarafında ise alıcının bir kısmı turizmle uğraşan aileler; Nemrut yoluna ve baraj gölüne yakın mülklerde bu konum başlı başına bir değer.</p>"),
 ],
 sss=[
  ("İlan videosunda yapı bilgisi nasıl veriliyor?", "Yapı yılı, ruhsat tarihi ve zemin etüdü gibi bilgileri ilan sahibinin belgesine göre ekranda yazıyoruz; belge yoksa yazmıyoruz."),
  ("Göl manzaralı arsamız için ne önerirsiniz?", "Havadan arsa sınırı, göle mesafe ve yol bağlantısını gösteren kısa bir video."),
  ("Bahçeli müstakil evi nasıl çekiyorsunuz?", "Evin tamamını ve bahçeyi gösteren bir dış plan, ardından oda oda iç tur."),
  ("Kahta'daki evimizi şehir dışındaki alıcıya nasıl anlatırız?", "Baraj gölüne, Nemrut yoluna ve ilçe merkezine mesafeyi baştan veren, ardından evi gösteren 60 saniyelik bir video."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ AFYONKARAHİSAR EMLAK
"afyonkarahisar-emlak-video": dict(
 lede="Afyonkarahisar'da bir dairenin ilanında termal su varsa, alıcının ilk sorduğu şey o oluyor. Termal sitelerden kale manzaralı daireye, Afyon'da konut kendine özgü.",
 bolum=[
  ("Afyonkarahisar'da konut satışı",
   "<p>TÜİK'e göre Afyonkarahisar'da Eylül 2025–Ağustos 2026 arasında <strong>11.440 konut</strong> satıldı; il Türkiye'de 32. sırada. Satışların <strong>%32,3'ü ilk el</strong>. Ağustos 2026'da satış bir yıl öncesine göre <strong>%15,9</strong> geriledi (1.176'dan 989'a).</p>"),
  ("Termal, kale ve kampüs",
   "<p><strong>Termal siteler ve devre mülk:</strong> şehrin çevresindeki termal bölgede, evine termal su gelen siteler ve devre mülkler. Alıcı çoğu zaman il dışından, emekli ya da sağlık için ikinci ev arayan biri. Termal havuzu, tesis olanaklarını ve dairenin kendisini birlikte gösteren bir video.</p>"
   "<p><strong>Şehir merkezi:</strong> kayalığın üzerindeki kaleye bakan daireler ve yeni siteler; çarşıya, üniversiteye ve hastaneye mesafe.</p>"
   "<p><strong>Öğrenci kiralığı:</strong> üniversite kampüsüne yakın daireler; Eylül öncesi kısa dikey turlar.</p>"
   "<p><strong>Arsa ve bağ evi:</strong> şehrin çevresinde arsalar; sınır ve yol bağlantısı havadan. Afyon'un kayalık siluetinin önünde bir açılış planı, ilanı diğer illerin arsalarından hemen ayırıyor.</p>"),
  ("Çekim düzeni",
   "<p>Afyon karasal iklimde; kışın soğuk ve sisli sabahlar sık. Termal tesislerde soğuk havada havuzdan yükselen buhar, ilanın en güçlü görüntüsü; bu yüzden termal mülkleri kışın çekmeyi öneriyoruz. Kurguyu ve renk düzenlemesini biz yapıyoruz; çekimlerde bölgedeki kamera ortağımızla birlikteyiz.</p>"),
  ("Otoyolların kesiştiği şehir",
   "<p>Afyonkarahisar, İstanbul, Ankara, İzmir ve Antalya yönlerine giden yolların kavşağında. Bu yüzden termal mülklerin alıcısı Türkiye'nin dört bir yanından gelebiliyor; ilan videosunda büyük şehirlere sürüş süresini yazmak, uzaktaki alıcının ilk sorusunu cevaplıyor. Şehir içinde ise kaymak, sucuk ve lokum üreticilerinin çevresinde büyüyen bir iş hayatı var; bu ailelerin aradığı şey okula ve işe yakın, ferah bir daire.</p>"),
 ],
 sss=[
  ("Termal sitedeki dairemiz için ne çekmeliyiz?", "Termal havuz, tesis olanakları ve daire; soğuk bir günde havuzdan yükselen buhar en etkili görüntü."),
  ("Devre mülk satışı için video işe yarar mı?", "Evet. Alıcı tesisi görmeden karar veriyor; tesisin yaşamını ve olanaklarını gösteren video güven veriyor."),
  ("Kale manzaralı daireyi nasıl gösterirsiniz?", "Salondan balkona açılan bir planla ve akşam ışığında kalenin aydınlatılmış hâliyle."),
  ("Afyon dışındaki alıcıya termal daireyi nasıl tanıtırız?", "Otoyola, Ankara ve İzmir yönüne mesafeyi ekranda veriyor; tesisin kış ve yaz hâlini birlikte gösteriyoruz."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ BİLECİK EMLAK
"bilecik-emlak-video": dict(
 lede="Bilecik'te satılan konutların yarıya yakını sıfır; Türkiye'deki en yüksek oranlardan biri. Bozüyük'ün fabrikaları ve hızlı tren, küçük bir ilde yeni konutu büyütüyor.",
 bolum=[
  ("Bilecik'te yeni konut",
   "<p>TÜİK'e göre Bilecik'te Eylül 2025–Ağustos 2026 arasında <strong>4.047 konut</strong> satıldı; bunların <strong>1.954'ü (%48,3) ilk el</strong>. Türkiye ortalaması %33,5; Bilecik'te her iki satıştan biri yeni konut. Ağustos 2026'da satış bir yıl öncesine göre <strong>%14,3</strong> geriledi.</p>"
   "<p>Yeni konutun bu kadar ağır bastığı bir piyasada alıcı projeleri karşılaştırıyor; müteahhit için sitenin ve dairenin iyi gösterilmesi, satışın hızını belirliyor.</p>"),
  ("İlçeye göre alıcı",
   "<p><strong>Bozüyük:</strong> seramik, metal ve sanayi tesislerinin şehri; fabrika çalışanları ve aileleri için yeni siteler. Fabrikaya, okula ve hızlı tren istasyonuna mesafe.</p>"
   "<p><strong>Bilecik merkez:</strong> üniversite çevresinde öğrenciye kiralanan daireler ve yeni siteler; vadinin içinde kurulu şehirde manzara ve eğim.</p>"
   "<p><strong>Osmaneli ve Söğüt:</strong> bahçeli müstakil evler ve sakin ilçe yaşamı; Osmaneli'de nehir kıyısı ve bağlar.</p>"),
  ("Bursa'ya yakın",
   "<p>Bilecik'te kendi ekibimizle çalışıyoruz; Bursa'dan yaklaşık bir buçuk saatte geliyoruz. Müteahhitler için satış öncesi 3D render ile gerçek arsa görüntüsünü birleştiren videolar, inşaat sürecinde de aylık şantiye çekimi yapabiliyoruz.</p>"),
  ("Hızlı trenin durduğu yer",
   "<p>Bozüyük ve Bilecik, İstanbul–Ankara hızlı tren hattı üzerinde. İstanbul'da ya da Eskişehir'de çalışıp daha sakin ve uygun fiyatlı bir şehirde oturmak isteyen alıcı için istasyona mesafe, ilanın ilk satırı. Videonun açılışında istasyonu ve oradan eve giden yolu kısa bir planla göstermek, bu alıcıya doğrudan konuşuyor.</p>"),
 ],
 sss=[
  ("Müteahhit olarak projemizi rakiplerden nasıl ayırırız?", "Sitenin yaşamını, ortak alanlarını ve dairenin ışığını gösteren bir video; bitmemiş projede 3D render ile gerçek arsa görüntüsünü birleştiriyoruz."),
  ("Bozüyük'teki fabrika çalışanına yönelik ilan için ne önerirsiniz?", "Fabrikaya, okula ve istasyona mesafeyi baştan veren kısa bir video."),
  ("Söğüt ya da Osmaneli'deki bahçeli ev için ne önerirsiniz?", "Bahçeyi ve evin tamamını havadan, ardından odaları gösteren sakin bir tur; ilçenin huzurunu anlatan birkaç sokak planı."),
  ("Bursa'dan mı geliyorsunuz?", "Evet, kendi ekibimizle; yaklaşık bir buçuk saatlik yol."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ ÇORUM EMLAK
"corum-emlak-video": dict(
 lede="Çorum'da satılan konutların %41,8'i sıfır ve Ağustos'taki düşüş Türkiye genelinin yarısından az. Sanayisi büyüyen bir Anadolu şehrinde yeni siteler hızla doluyor.",
 bolum=[
  ("Çorum'da konut piyasası",
   "<p>TÜİK'e göre Çorum'da Eylül 2025–Ağustos 2026 arasında <strong>9.682 konut</strong> satıldı; satışların <strong>%41,8'i ilk el</strong>. Ağustos 2026'da satış bir yıl öncesine göre yalnızca <strong>%5,7</strong> geriledi; Türkiye genelinde düşüş %14,7.</p>"),
  ("Çorum'da alıcı ne arıyor",
   "<p><strong>Yeni siteler:</strong> şehrin genişleyen bölgelerinde sosyal donatılı siteler; organize sanayi bölgesinde çalışan aileler. Fabrikaya, okula ve hastaneye mesafe; sitenin ortak alanları ve daire.</p>"
   "<p><strong>Merkez:</strong> çarşıya ve saat kulesine yakın eski stok ve dönüşüm daireleri; konum ve yenilenmiş iç mekân.</p>"
   "<p><strong>Leblebi ve sanayi şehri:</strong> Çorum'un un, makine ve tuğla-kiremit üreticileri şehre sürekli yeni çalışan getiriyor; kiralık ve satılık talebinin önemli kısmı bu ailelerden.</p>"
   "<p><strong>Arsa ve tarla:</strong> şehir çevresinde arsalar ve tarım arazileri; sınır ve yol bağlantısı havadan.</p>"),
  ("Çekim düzeni",
   "<p>Çorum karasal iklimde: kış soğuk, yaz kuru ve aydınlık. Dış çekimi yazın sabah ve akşamüstüne, kışın öğleye koyuyoruz. Çekimi bölgedeki kamera ortağımızla yapıyor, kurgu ve rengi kendimiz tamamlıyoruz.</p>"),
  ("Hattuşa'nın yanı başında",
   "<p>Çorum'un bir saat kadar uzağında, UNESCO Dünya Mirası listesindeki Hattuşa var; Boğazkale ve Alacahöyük çevresinde köy evleri ve pansiyonlar turizmle değer kazanıyor. Şehir merkezinde ise alıcı daha çok yerli: leblebi, un ve makine sanayinde çalışan aileler. İki alıcıya iki ayrı video: köyde tarih ve doğa, şehirde günlük hayat ve ulaşım.</p>"),
 ],
 sss=[
  ("Yeni sitedeki dairemiz için ne çekmeliyiz?", "Site girişi, ortak alanlar ve otopark, ardından daire; OSB'ye ve okula mesafeyi ekranda veriyoruz."),
  ("Merkezdeki eski daire için video fark eder mi?", "Evet. Yenilenmiş iç mekânı ve merkezi konumu öne çıkaran bir video, fotoğrafın anlatamadığını anlatıyor."),
  ("Hattuşa yönündeki köy evimizi nasıl tanıtırız?", "Köyün ve bahçenin havadan görüntüsü, ardından evin içi; Boğazkale'ye ve şehre mesafeyi ekranda veriyoruz."),
  ("Hitit Üniversitesi'ne yakın kiralık için ne çekmeliyiz?", "30–45 saniyelik dikey bir tur; kampüse ve çarşıya mesafeyi ekranda yazıyoruz. Ağustos'ta yayında olmalı."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ DİYARBAKIR EMLAK
"diyarbakir-emlak-video": dict(
 lede="Diyarbakır'da son bir yılda 27.205 konut satıldı; il Türkiye'de 18. sırada. Kayapınar'ın yeni sitelerinden surların içindeki taş evlere, şehrin konutu iki ayrı zamanda yaşıyor.",
 bolum=[
  ("Diyarbakır'da konut piyasası",
   "<p>TÜİK'e göre Diyarbakır'da Eylül 2025–Ağustos 2026 döneminde <strong>27.205 konut</strong> el değiştirdi; satışların <strong>%35,5'i ilk el</strong>. Ağustos 2026'da satış 2.057'ye indi; bir yıl önce 2.747'ydi, düşüş <strong>%25,1</strong>. Türkiye genelindeki düşüşün belirgin üzerinde; alıcının azaldığı bir dönemde ilanın sunumu daha çok fark ediyor.</p>"),
  ("Semte göre video",
   "<p><strong>Kayapınar ve Diclekent:</strong> yeni, havuzlu ve sosyal donatılı siteler; geniş daireler ve aile alıcılar. Site yaşamı, otopark ve okula mesafe.</p>"
   "<p><strong>Yenişehir ve Bağlar:</strong> şehrin merkezinde apartman daireleri; çarşıya, hastaneye ve ulaşıma yakınlık.</p>"
   "<p><strong>Sur içi:</strong> UNESCO Dünya Mirası listesindeki surların ve Hevsel Bahçeleri'nin hemen yanında, avlulu taş evler. Bu evlerin alıcısı dokuyu ve tarihi satın alıyor; avlu, bazalt taş ve kemerler yakın planda.</p>"),
  ("Sıcak, ışık ve drone",
   "<p>Diyarbakır yazın çok sıcak; dış çekimi sabah erken ve akşamüstüne koyuyoruz. Havalimanı askerî bir hava üssüyle ortak kullanılıyor ve şehrin önemli bir kısmı kontrollü hava sahasında; drone planını her mülk için haritadan kontrol ediyoruz.</p>"
   "<p>Kurgu ve renk bizde; çekim günlerinde Diyarbakır'da birlikte çalıştığımız kamera ekibiyle sahadayız.</p>"),
  ("Geniş aileler, geniş daireler",
   "<p>Diyarbakır'da aileler büyük; 4+1 ve 5+1 daireler şehirdeki talebin önemli bir kısmı. Bu dairelerde oda sayısı fazla ve fotoğraf, düzeni anlatmakta zorlanıyor. Video, odaları sırayla dolaşarak dairenin akışını gösteriyor: mutfağın salona yakınlığı, yatak odalarının ayrı bir koridorda olup olmadığı, balkonların sayısı. Alıcı daireyi gezmeye gelmeden düzeni kafasında kuruyor.</p>"),
 ],
 sss=[
  ("Kayapınar'daki site dairemiz için ne önerirsiniz?", "Site girişinden başlayan, havuz ve ortak alanları gösteren, ardından daireye giren bir tur; 60–90 saniye."),
  ("Sur içindeki taş ev için nasıl bir video olmalı?", "Sokaktan avluya giren tek akıcı plan, bazalt ve kemer detayları, odalar; yavaş ve dokuyu öne çıkaran bir anlatım."),
  ("Diyarbakır'da drone kullanılabilir mi?", "Şehrin önemli kısmında izin gerekiyor. Konumu kontrol edip önceden söylüyoruz."),
  ("Geniş aile dairesi için video ne kadar olmalı?", "4+1 ve 5+1 dairelerde oda sayısı fazla; her odayı kısa tutan 90–120 saniyelik bir tur, alıcının düzeni kafasında kurmasını sağlıyor."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ EDİRNE EMLAK
"edirne-emlak-video": dict(
 lede="Edirne'de Ağustos 2026'da konut satışı bir yıl öncesine göre %27,3 düştü; Türkiye'deki en sert düşüşlerden biri. Alıcının azaldığı bir şehirde ilanın listede fark edilmesi her zamankinden önemli.",
 bolum=[
  ("Edirne'de konut piyasası",
   "<p>TÜİK'e göre Edirne'de Eylül 2025–Ağustos 2026 arasında <strong>7.721 konut</strong> satıldı; satışların <strong>%36,2'si ilk el</strong>. Ağustos 2026'da satış 562'ye indi; bir yıl önce 773'tü.</p>"),
  ("Selimiye'den Saros'a",
   "<p><strong>Merkez:</strong> Selimiye'nin silueti altında apartman daireleri ve yeni siteler; çarşıya, üniversiteye ve hastaneye mesafe. Selimiye manzarası olan dairelerde bu manzara ilanın en güçlü kartı.</p>"
   "<p><strong>Öğrenci kiralığı:</strong> Trakya Üniversitesi'nin kampüsüne yakın daireler; Eylül öncesi kısa dikey turlar. Edirne'de kiralık ilanlar yaz sonunda yoğunlaşıyor.</p>"
   "<p><strong>Keşan ve Uzunköprü:</strong> kendi iş hayatı olan ilçelerde aile konutu ve bahçeli evler.</p>"
   "<p><strong>Enez ve Saros kıyısı:</strong> yazlık daireler ve sahil siteleri; plaja mesafe ve yaz yaşamı.</p>"),
  ("Çekim düzeni",
   "<p>Edirne'nin nehirleri ve düz ovası, şehrin havadan en güzel göründüğü kareleri veriyor; Selimiye'nin dört minaresi havadan bakıldığında bile şehrin merkezini işaret ediyor. Sınır bölgesindeki askerî alanlar ve bazı kesimler drone için izne bağlı; her mülkün konumunu önceden kontrol ediyoruz.</p>"
   "<p>Kamera gereken günlerde Trakya'daki çözüm ortağımızla birlikteyiz; kurgu ve renk düzenlemesi bizde.</p>"),
  ("Sınır şehri, öğrenci şehri",
   "<p>Edirne'de konut talebinin iki sabit kaynağı var: Trakya Üniversitesi'nin öğrencileri ve kamuda, sağlıkta, sınır kapılarında çalışanlar. Bu iki grup da şehre dışarıdan geliyor ve çoğu zaman evi görmeden önce internetten eliyor. İlan videosu, Edirne'yi tanımayan alıcıya mahalleyi, Selimiye'ye ve çarşıya mesafeyi ve dairenin kendisini birkaç dakikada anlatıyor.</p>"),
 ],
 sss=[
  ("Selimiye manzaralı dairemizi nasıl gösterirsiniz?", "Salondan balkona açılan bir planla ve akşam aydınlatmasında; manzarayı gün batımında da çekiyoruz."),
  ("Satışlar düşükken video çektirmek mantıklı mı?", "Tam bu dönemde. Alıcı azken ilanınızın fark edilmesi ve gezmeye gelen alıcının gerçekten ilgili olması zaman kazandırıyor."),
  ("Enez'deki yazlığımız için ne zaman çekim yapmalıyız?", "Mayıs sonunda; deniz ve plaj yaz görüntüsünü verirken kalabalık henüz yok."),
  ("Edirne'de drone kullanılabilir mi?", "Konuma bağlı; sınıra ve askerî alanlara yakın yerlerde izin gerekiyor. Önceden kontrol ediyoruz."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ ELAZIĞ EMLAK
"elazig-emlak-video": dict(
 lede="Elazığ iki depremi yakından yaşadı: Ocak 2020'de Sivrice'de, Şubat 2023'te bütün bölgede. Bugün alıcının ilk sorusu, binanın bu yıllardan sonra hangi kurallarla yapıldığı.",
 bolum=[
  ("Elazığ'da konut piyasası",
   "<p>TÜİK'e göre Elazığ'da Eylül 2025–Ağustos 2026 arasında <strong>13.578 konut</strong> satıldı; il Türkiye'de 27. sırada. Satışların <strong>%37,3'ü ilk el</strong>, Türkiye ortalamasının üzerinde. Ağustos 2026'da satış bir yıl öncesine göre <strong>%11,8</strong> geriledi.</p>"
   "<p>Yeni konutun payı yüksek; alıcı yeni binaları birbiriyle karşılaştırıyor. İlan videosunda yapı yılını, ruhsat tarihini ve zemin bilgisini belgeye göre ekranda veriyor, ardından daireyi ve ortak alanları gösteriyoruz.</p>"),
  ("Kampüs, göl ve Harput",
   "<p><strong>Yeni siteler:</strong> şehrin genişleyen bölgelerinde aile siteleri; sosyal alan, otopark ve okula mesafe.</p>"
   "<p><strong>Öğrenci kiralığı:</strong> üniversite kampüsüne yakın daireler; Eylül öncesi kısa dikey turlar.</p>"
   "<p><strong>Hazar Gölü kıyısı:</strong> Sivrice'de göl manzaralı yazlık evler ve arsalar; göle mesafe ve manzara havadan.</p>"
   "<p><strong>Harput ve bağ evleri:</strong> şehre tepeden bakan tarihî Harput çevresinde bahçeli evler.</p>"),
  ("Çekim düzeni",
   "<p>Elazığ'da yaz sıcak ve kuru, kış soğuk. Hazar Gölü'nde göl yüzeyi sabahları sakin ve parlak; göl manzaralı mülkleri sabah çekiyoruz. Kurgu, renk ve yönetmenliği biz yürütüyoruz; sahada bölgedeki kamera ortağımızla çalışıyoruz.</p>"),
  ("Fırat'ın kıyısında bir üniversite şehri",
   "<p>Elazığ'da Fırat Üniversitesi şehrin en büyük kiralık talep kaynağı; her yaz sonunda binlerce öğrenci ev arıyor. Bu öğrencilerin ve ailelerinin çoğu başka şehirlerde; daireyi önce telefonda görüyorlar. Kampüse mesafeyi, ulaşımı ve dairenin eşyalı olup olmadığını net gösteren kısa bir video, ilanın kısa sürede kapanmasını sağlıyor.</p>"),
 ],
 sss=[
  ("İlan videosunda deprem ve yapı bilgisi veriyor musunuz?", "Evet; yapı yılı, ruhsat tarihi ve zemin bilgisini ilan sahibinin belgesine göre ekranda yazıyoruz."),
  ("Hazar Gölü kıyısındaki yazlığımız için ne önerirsiniz?", "Havadan göl ve evin konumu, terastan manzara, ardından iç tur; sabah ışığında."),
  ("Harput'taki bahçeli evimiz için ne önerirsiniz?", "Şehre tepeden bakan konumu havadan, bahçeyi ve evi yerden; gün batımında Harput'tan şehir manzarası."),
  ("Yeni sitedeki dairemizi diğer projelerden nasıl ayırırız?", "Yapı bilgisini baştan vererek ve sitenin yaşamını göstererek; alıcı önce güveni, sonra daireyi görmek istiyor."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ ERZURUM EMLAK
"erzurum-emlak-video": dict(
 lede="Erzurum'da kış uzun ve sert; bir dairenin değerini çoğu zaman ısınma belirliyor. Doğalgaz, yalıtım, kapalı otopark; Erzurum'da ilan videosu, kışı da anlatmalı.",
 bolum=[
  ("Erzurum'da konut piyasası",
   "<p>TÜİK'e göre Erzurum'da Eylül 2025–Ağustos 2026 arasında <strong>12.095 konut</strong> satıldı; satışların <strong>%38,9'u ilk el</strong>. Ağustos 2026'da satış bir yıl öncesine göre <strong>%15,4</strong> geriledi (1.060'tan 897'ye).</p>"),
  ("Mülk tipine göre video",
   "<p><strong>Yeni siteler:</strong> Palandöken ve Yakutiye'nin genişleyen bölgelerinde aile siteleri. Alıcı kapalı otoparkı, ısınma sistemini ve yalıtımı soruyor; bu detayları videoda yakın planda gösteriyoruz.</p>"
   "<p><strong>Öğrenci kiralığı:</strong> Türkiye'nin en büyük kampüslerinden birine sahip üniversitenin çevresinde öğrenciye kiralanan daireler; kampüse ve otobüs hatlarına mesafe.</p>"
   "<p><strong>Palandöken eteği:</strong> kayak merkezine yakın daireler ve apartlar; kış sezonunda kiralama potansiyeli.</p>"
   "<p><strong>Merkez:</strong> tarihî çarşıya ve Çifte Minareli Medrese çevresine yakın eski stok.</p>"),
  ("Kışın çekim",
   "<p>Erzurum'da kar Ekim'den Nisan'a kadar uzanabiliyor. Karlı bir sabah dış cephe ve site için güzel bir görüntü ama yollar ve ışık değişken; çekimi havaya göre esnek tutuyoruz. Kış ilanında iç mekânın sıcak ve aydınlık görünmesi önemli; ışığı buna göre kuruyoruz. Havalimanı askerî üsle ortak kullanılıyor; drone planını her mülk için kontrol ediyoruz.</p>"
   "<p>Kurgu, renk ve yönetmenlik bizde; kamera gereken günlerde bölgedeki çözüm ortağımızla birlikte sahadayız.</p>"),
  ("Bir kampüs şehri",
   "<p>Atatürk Üniversitesi Erzurum'un en büyük kurumlarından biri; öğrenciler, akademisyenler ve sağlık çalışanları şehrin kiralık ve satılık piyasasının önemli bir kısmını oluşturuyor. Bu alıcıların çoğu Erzurum'a başka bir şehirden geliyor ve şehri tanımıyor. Videoda kampüse, hastanelere ve çarşıya mesafeyi, mahallenin kışın nasıl göründüğünü de göstermek, uzaktan karar vermeyi kolaylaştırıyor.</p>"),
 ],
 sss=[
  ("Kış ilanında neyi öne çıkarmalıyız?", "Isınma sistemi, yalıtım, kapalı otopark ve iç mekânın sıcaklığı. Bu detayları yakın planda gösteriyoruz."),
  ("Öğrenci dairesi için kış görüntüsü mü yaz görüntüsü mü?", "Kiralık kararları yaz sonunda veriliyor; Ağustos'ta çekip dairenin kışın sıcak tuttuğunu anlatan detayları ekliyoruz."),
  ("Palandöken'e yakın apartımız için ne önerirsiniz?", "Kayak merkezine mesafeyi ve kış manzarasını gösteren bir video; sezon öncesi, Ekim–Kasım'da yayında olmalı."),
  ("Karlı havada çekim yapılabilir mi?", "Evet; kar sonrası açık bir gün en iyisi. Tarihi havaya göre esnek tutuyoruz."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ HATAY EMLAK
"hatay-emlak-video": dict(
 lede="Hatay, Şubat 2023 depremlerinin en ağır yaşandığı il. Antakya'da, İskenderun'da ve Defne'de bugün yeni binalar ve yeni mahalleler yükseliyor; konutun hikâyesi yeniden yazılıyor.",
 bolum=[
  ("Hatay'da konut piyasası",
   "<p>TÜİK'e göre Hatay'da Eylül 2025–Ağustos 2026 arasında <strong>14.987 konut</strong> satıldı; satışların <strong>%26'sı ilk el</strong>. Ağustos 2026'da satış bir yıl öncesine göre yalnızca <strong>%4,4</strong> geriledi; Türkiye genelinde düşüş %14,7.</p>"),
  ("Güven ve bilgi",
   "<p>Hatay'da alıcının ilk bakacağı şey binanın ne zaman ve nasıl yapıldığı. İlan videosunda yapı yılını, ruhsat tarihini, varsa zemin etüdünü ve hasar tespit bilgisini ilan sahibinin belgesine göre ekranda veriyoruz. Bilgi doğru ve belgeye dayalı olmalı; belgesi olmayan bilgiyi yazmıyoruz.</p>"
   "<p>Ardından daireyi ve ortak alanları gösteriyoruz. Yeni kurulan mahallelerde çevre henüz tamamlanmamış olabiliyor; alıcıya mahallenin bugünkü hâlini dürüstçe, yapılmakta olan okul ve yolları da göstererek anlatıyoruz.</p>"),
  ("Bölgeye göre video",
   "<p><strong>İskenderun:</strong> liman ve sanayi şehri; deniz manzaralı daireler ve sahile mesafe.</p>"
   "<p><strong>Antakya ve Defne:</strong> yeniden yapılanan şehir merkezi ve yeni konut alanları.</p>"
   "<p><strong>Samandağ ve Arsuz:</strong> sahil boyunca yazlık ve müstakil evler; deniz ve bahçe.</p>"
   "<p>Görüntü yönetimi ve kurgu bizde; çekim günlerinde bölgede birlikte çalıştığımız ekiple sahadayız.</p>"),
  ("Yeniden kurulan bir şehirde ilan",
   "<p>Hatay'da bugün ev arayanların önemli bir kısmı depremden sonra il dışına gidip geri dönmeyi düşünen aileler. Bu aileler evi uzaktan, telefonda görüyor; mahallenin bugünkü hâlini, binanın yapı bilgilerini ve evin içini dürüst bir şekilde görmek istiyor. Video, onlar için şehre gelmeden önceki ilk adım.</p>"),
 ],
 sss=[
  ("İlan videosunda hasar tespit ya da yapı bilgisi verilmeli mi?", "Belgeniz varsa evet. Yapı yılı, ruhsat ve hasar tespit bilgisini belgeye göre ekranda yazıyoruz; belge yoksa yazmıyoruz."),
  ("Yeni mahalledeki dairemiz için ne önerirsiniz?", "Yapı bilgisi, ardından daire ve ortak alanlar; okula, sağlık kuruluşuna ve ulaşıma mesafe."),
  ("İskenderun'daki deniz manzaralı dairemizi nasıl gösterirsiniz?", "Salondan balkona açılan bir planla, sabah ya da gün batımı ışığında."),
  ("Samandağ'daki bahçeli evimiz için ne önerirsiniz?", "Bahçeyi ve denize mesafeyi havadan, evi yerden gösteren 60 saniyelik bir video."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ ISPARTA EMLAK
"isparta-emlak-video": dict(
 lede="Isparta'da kiralık piyasasını büyük ölçüde üniversite belirliyor; satılık piyasasında ise Eğirdir Gölü'nün kıyısı ve gül bahçeleri arasındaki evler ayrı bir alıcıya konuşuyor.",
 bolum=[
  ("Isparta'da konut piyasası",
   "<p>TÜİK'e göre Isparta'da Eylül 2025–Ağustos 2026 arasında <strong>7.255 konut</strong> satıldı; satışların <strong>%31,1'i ilk el</strong>. Ağustos 2026'da satış bir yıl öncesine göre <strong>%20</strong> geriledi (741'den 593'e); Türkiye genelindeki düşüşün üzerinde.</p>"),
  ("Kampüs, göl ve gül bahçesi",
   "<p><strong>Öğrenci kiralığı:</strong> üniversite kampüsüne ve şehir merkezine yakın daireler. Kiralamaların büyük kısmı yaz sonunda; ilanın Ağustos'ta 30–45 saniyelik dikey bir turla yayında olması gerekiyor.</p>"
   "<p><strong>Şehir merkezi ve yeni siteler:</strong> aile alıcılar için daireler; okula, çarşıya ve hastaneye mesafe.</p>"
   "<p><strong>Eğirdir Gölü kıyısı:</strong> göl manzaralı evler, pansiyonlar ve arsalar; alıcı çoğu zaman il dışından. Havadan göl ve evin konumu.</p>"
   "<p><strong>Gül ve lavanta bölgesi:</strong> bahçeli köy evleri; Mayıs–Haziran'da gül, Temmuz'da lavanta. Bahçeli mülkü bu dönemde çekmek ilanı bambaşka gösteriyor.</p>"),
  ("Çekim düzeni",
   "<p>Isparta karasal ve dağlık; kışın kar, yazın serin akşamlar. Göl manzaralı mülkleri sabah ya da gün batımında çekiyoruz. Kurguyu kendimiz yapıyoruz; çekimde bölgedeki kamera ortağımızla birlikteyiz.</p>"),
  ("Gül, lavanta ve göl",
   "<p>Isparta'nın kırsalı yılın belli haftalarında renk değiştiriyor: Mayıs sonunda gül bahçeleri, Temmuz'da Kuyucak çevresindeki lavanta tarlaları. Bu dönemde çekilen bir köy evi ilanı, aynı evin kış görüntüsünden çok daha fazla ilgi görüyor. Eğirdir Gölü kıyısında ise manzara her mevsim güçlü; göl sabah saatlerinde ayna gibi duruyor.</p>"),
 ],
 sss=[
  ("Gül bahçeli evin satışı için video ne kadar olmalı?", "60–90 saniye: bahçe, gül ya da lavanta sıraları, ev ve manzara. Çiçek dönemini kaçırmamak için tarihi baştan koyuyoruz."),
  ("Eğirdir'deki göl manzaralı evimiz için ne önerirsiniz?", "Havadan göl ve evin konumu, terastan manzara, ardından iç tur."),
  ("Bahçeli köy evimizi ne zaman çekmeliyiz?", "Gül ya da lavanta döneminde; bahçe en renkli hâliyle görünüyor."),
  ("Eğirdir'deki pansiyonumuzu da çekiyor musunuz?", "Evet; hem satış hem kiralama için. Göl manzarası, odalar ve kahvaltı alanını gösteren kısa bir video hazırlıyoruz."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ KAHRAMANMARAŞ EMLAK
"kahramanmaras-emlak-video": dict(
 lede="Kahramanmaraş, Şubat 2023 depremlerinin merkezi. Şehirde bugün yeni binalar, yeni mahalleler ve yeniden açılan çarşılar var; alıcının ilk sorusu her zaman binanın kendisi.",
 bolum=[
  ("Kahramanmaraş'ta konut piyasası",
   "<p>TÜİK'e göre Kahramanmaraş'ta Eylül 2025–Ağustos 2026 arasında <strong>12.850 konut</strong> satıldı; satışların <strong>%29,5'i ilk el</strong>. Ağustos 2026'da satış bir yıl öncesine göre <strong>%7,3</strong> geriledi; Türkiye genelindeki düşüşün yarısı kadar.</p>"),
  ("Yapı bilgisi ve güven",
   "<p>Kahramanmaraş'ta ilan videosunun ilk saniyeleri yapıya ayrılmalı: yapı yılı, ruhsat tarihi, varsa zemin etüdü ve hasar tespit bilgisi. Bu bilgileri ilan sahibinin belgesine göre ekranda veriyoruz; belgesi olmayan bilgiyi yazmıyoruz. Ardından daire, ortak alanlar ve çevre.</p>"),
  ("Yeni mahalleler, yeni evler",
   "<p><strong>Onikişubat ve Dulkadiroğlu'nda yeni siteler:</strong> aile alıcılar için yeni daireler; sosyal alan, otopark ve okula mesafe.</p>"
   "<p><strong>Bahçeli müstakil ev:</strong> depremden sonra ilgi artan tek ya da iki katlı evler; bahçe ve yapının tamamı.</p>"
   "<p><strong>Ahır Dağı eteği ve yayla evleri:</strong> şehre tepeden bakan, yazın serin bölgelerde müstakil evler.</p>"
   "<p>Kahramanmaraş'ta çekim günlerinde bölgedeki kamera ortağımızla çalışıyor, kurgu ve renk düzenlemesini kendimiz yapıyoruz.</p>"),
  ("Uzaktaki aileye konuşmak",
   "<p>Kahramanmaraş'ta ev arayanların bir kısmı depremden sonra başka şehirlere taşınmış ve dönmeyi düşünen aileler. Bu aileler için ilan videosu, şehre gelmeden önce evi ve mahalleyi görmenin yolu: yapı bilgisi, dairenin içi, mahallenin bugünkü hâli ve okul, sağlık kuruluşu gibi yakın noktalar. Bilgiyi abartmadan, olduğu gibi göstermek güveni artırıyor.</p>"),
 ],
 sss=[
  ("İlan videosunda yapı bilgisi nasıl veriliyor?", "Yapı yılı, ruhsat, zemin ve hasar tespit bilgisini belgenize göre ekranda yazıyoruz; belge yoksa yazmıyoruz."),
  ("Bahçeli müstakil evimiz için ne önerirsiniz?", "Evin tamamını ve bahçeyi gösteren bir dış plan, ardından iç tur; havadan bir açılış da mümkün."),
  ("Yayla evimizi ne zaman çekmeliyiz?", "Yaz başında; yeşil ve serin hâliyle. Şehre mesafeyi ve yolu da ekranda veriyoruz."),
  ("Yeni açılan çarşıya yakın dükkânlı binayı da çekiyor musunuz?", "Evet. Ticari birimi ve üstteki daireleri ayrı ayrı gösteren, çarşıya ve ana caddeye mesafeyi veren bir video hazırlıyoruz."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ KÜTAHYA EMLAK
"kutahya-emlak-video": dict(
 lede="Çinisiyle, porseleniyle, kaplıcalarıyla tanınan Kütahya'da yeni konut çok, alıcı az. Ağustos 2026'daki satışlar bir önceki ağustosun dörtte üçünde kaldı.",
 bolum=[
  ("Yavaşlayan bir piyasa",
   "<p>Resmî kayıtlara göre Kütahya'da on iki ayda (Eylül 2025–Ağustos 2026) <strong>8.835</strong> konut el değiştirdi. Her beş satıştan ikisi yeni konut (<strong>%40,5</strong>). Ağustos 2026'da sadece 601 konut satılabildi; bir önceki yılın aynı ayında 826'ydı, yani <strong>%27,2</strong> geride. Müteahhit için bu tablo şu demek: alıcı az, seçenek çok, öne çıkan proje kazanır.</p>"),
  ("Çini şehrinde konut",
   "<p><strong>Yeni konut alanları:</strong> çini ve porselen atölyelerinde, maden işletmelerinde, hastanelerde çalışan ailelerin aradığı 3+1 daireler. Bu alıcı için en önemli bilgi okul servisinin geçip geçmediği ve kışın binanın nasıl ısındığı.</p>"
   "<p><strong>Kampüs çevresi:</strong> Dumlupınar Üniversitesi'nin Evliya Çelebi yerleşkesine yakın, öğrenciye kiralanan küçük daireler. Ev sahibinin ihtiyacı hızlı kiralamak; telefonda izlenecek, eşyaları ve odayı net gösteren kısa bir video.</p>"
   "<p><strong>Tarihî evler:</strong> kalenin eteğindeki eski mahallelerde ahşap ve kerpiç evler; restorasyon ve doku.</p>"),
  ("Termal evler",
   "<p>Yoncalı, Ilıca (Harlek) ve Simav'daki kaplıca bölgelerinde, dairesine sıcak su gelen apart ve siteler satılıyor. Bu evlerin çoğunu Ankara, İstanbul ve İzmir'de yaşayan, hafta sonu ya da emeklilikte kaplıcaya yakın olmak isteyenler alıyor. Ekranda büyük şehirlere sürüş süresini, havuzun ve dairenin gerçek hâlini birlikte vermek gerekiyor.</p>"),
  ("Bursa'dan iki buçuk saat",
   "<p>Kütahya'ya çekime Bursa'dan kendi ekibimizle, Tavşanlı üzerinden yaklaşık iki buçuk saatte geliyoruz. Yolu bir kez yapıp aynı gün birkaç mülkü çekmek maliyeti düşürüyor; emlak ofislerine bu yüzden toplu çekim günü öneriyoruz. Zafer Havalimanı Altıntaş'ta, şehirden uzakta; merkezdeki binalarda havadan plan genelde sorun çıkarmıyor.</p>"),
 ],
 sss=[
  ("Satışlar yavaşken müteahhide ne önerirsiniz?", "Projeyi rakiplerden ayıracak tek bir güçlü video: girişten daireye kesintisiz bir tur ve kışın ısınmayı anlatan detaylar. İnşaat bitmediyse arsanın gerçek görüntüsüne render yerleştiriyoruz."),
  ("Yoncalı'daki apartımızı nasıl satarız?", "Kaplıcaya yürüme mesafesini, havuzu ve dairenin içini gösteren bir video; ekranda Ankara ve İzmir'e sürüş süresi."),
  ("Kiralık öğrenci dairesi için video şart mı?", "Şart değil ama hızlandırıyor: aileler evi uzaktan seçiyor ve odanın gerçek hâlini görmek istiyor. Yarım dakikalık dikey bir video yetiyor."),
  ("Tek bir daire için Bursa'dan gelir misiniz?", "Gelir miyiz, evet; ama aynı gün birkaç mülk olursa yol maliyeti bölünüyor. Çekim takvimini buna göre birlikte kuruyoruz."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ MALATYA EMLAK
"malatya-emlak-video": dict(
 lede="Malatya, Ağustos 2026'da konut satışı bir önceki yıla göre artan nadir illerden biri: %5,2. Depremden sonra yeniden kurulan şehirde yeni konutlar sahiplerini buluyor.",
 bolum=[
  ("Malatya'da konut piyasası",
   "<p>TÜİK'e göre Malatya'da Eylül 2025–Ağustos 2026 arasında <strong>9.894 konut</strong> satıldı; satışların <strong>%28,9'u ilk el</strong>. Ağustos 2026'da satış <strong>809</strong> oldu; bir yıl önce 769'du. Türkiye genelinde satışlar %14,7 düşerken Malatya'da artış var.</p>"),
  ("Yeniden kurulan şehirde güven",
   "<p>Şubat 2023 depremleri Malatya'nın çarşısını ve merkez mahallelerini derinden etkiledi; bugün şehirde yeni bir çarşı ve yeni yerleşim alanları kuruluyor. Malatyalı alıcı ev bakarken önce binanın ne zaman, hangi projeyle yapıldığını öğrenmek istiyor. Elinizde ruhsat, iskân ya da zemin raporu varsa bunları videonun ilk saniyelerinde gösteriyoruz; olmayan bir belgeyi varmış gibi sunmuyoruz.</p>"),
  ("Malatya'da mülk tipleri",
   "<p><strong>Yeşilyurt ve Battalgazi'de yeni konut alanları:</strong> aile alıcılar için yeni daireler; okula, hastaneye ve yeni çarşıya mesafe.</p>"
   "<p><strong>Kayısı bahçeli evler:</strong> şehrin çevresinde, kayısı bahçeleri içinde müstakil evler. Haziran–Temmuz'da kayısı olgunlaşırken bahçe en canlı hâlinde; bahçeli mülkü bu dönemde çekmek ilanı bambaşka gösteriyor.</p>"
   "<p><strong>İnönü Üniversitesi çevresi:</strong> öğrenci ve sağlık çalışanlarının kiraladığı daireler; hastaneye ve kampüse yakınlık ilanın ilk satırı.</p>"),
  ("Çekim düzeni",
   "<p>Malatya'nın yazı kuru ve parlak; cepheyi akşamüstü, içeriyi gün ortasında çekiyoruz. Erhaç'taki havalimanı askerî üsle ortak olduğu için şehrin kuzeyinde havadan plan izne bağlı olabiliyor. Sahada bölgedeki kamera ortağımız, kurguda biz varız.</p>"),
 ],
 sss=[
  ("Ruhsat ve iskân belgesini videoda göstermeli miyiz?", "Varsa evet; Malatya'da alıcının ilk sorduğu şey bu. Belgenin kendisini ya da özet bilgisini kısa bir ekranla veriyoruz."),
  ("Kayısı bahçeli evimizi ne zaman çekmeliyiz?", "Haziran–Temmuz'da, meyve ağaçtayken. Bahçeyi havadan, evi yerden gösteriyoruz."),
  ("Yeni çarşıya yakın dükkân ya da ofis de çekiyor musunuz?", "Evet. Cadde cephesini, iç hacmi ve çevredeki hareketi gösteren kısa bir video hazırlıyoruz."),
  ("Kayısı bahçesi satarken neyi göstermeliyiz?", "Ağaç sayısını ve düzenini havadan, sulama ve yol bağlantısını yerden; hasat döneminde çekmek bahçenin verimini kendiliğinden anlatıyor."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ MARDİN EMLAK
"mardin-emlak-video": dict(
 lede="Mardin'de bir yanda Mezopotamya ovasına bakan taş konaklar, öbür yanda yeni şehirde yükselen siteler var. İkisinin alıcısı da ayrı; ilan videosu da ayrı bir dil konuşmalı.",
 bolum=[
  ("Mardin'de konut piyasası",
   "<p>TÜİK'e göre Mardin'de Eylül 2025–Ağustos 2026 arasında <strong>13.739 konut</strong> satıldı; satışların <strong>%38,7'si ilk el</strong>, Türkiye ortalamasının üzerinde. Ağustos 2026'da satış bir yıl öncesine göre <strong>%18,2</strong> geriledi.</p>"),
  ("Eski Mardin: taş konak",
   "<p>Eski şehirde, yamaca basamak basamak yerleşmiş taş evler ve konaklar. Bu evlerin alıcısı çoğu zaman il dışından: butik otel, restoran ya da ikinci ev için. Satılan şey taş işçiliği, avlu, teras ve ovaya bakan manzara. Dar sokaktan avluya giren akıcı bir plan, oymalı taş detayları ve gün batımında teras; video, mülkün tarihini de anlatmalı.</p>"
   "<p>Eski Mardin koruma altında; tadilat ve kullanım izinleri alıcının sorduğu ilk şeylerden. Bu bilgiyi ilan sahibinin belgesine dayanarak veriyoruz.</p>"),
  ("Yeni şehir ve ilçeler",
   "<p><strong>Artuklu yeni yerleşim alanları:</strong> aile siteleri, sosyal alanlar ve otopark; okula ve hastaneye mesafe.</p>"
   "<p><strong>Kızıltepe:</strong> ovanın üzerinde büyüyen kalabalık bir ilçe; geniş aile daireleri ve müstakil evler.</p>"
   "<p><strong>Midyat:</strong> kendine özgü taş mimarisiyle konaklar ve turizme dönük mülkler.</p>"),
  ("Çekim düzeni",
   "<p>Mardin yazın çok sıcak; taş evlerin dış cephesi gün batımında bal rengine dönüyor, bu yüzden dış çekimi akşamüstüne koyuyoruz. Avlu ve iç mekân öğle ışığında daha dengeli. Kurgu ve renk bizim ekipte; çekim günlerinde bölgedeki kamera ortağımızla sahadayız.</p>"),
 ],
 sss=[
  ("Eski Mardin'deki taş evimizi nasıl tanıtırız?", "Sokaktan avluya giren bir plan, taş işçiliği detayları, odalar ve gün batımında teras; ovaya bakan manzara videonun doruk noktası."),
  ("Butik otele dönüştürülebilecek bir konak satıyoruz, video ne anlatmalı?", "Mevcut hâli, oda sayısı ve avlu, teras gibi ortak alanlar; potansiyeli göstermek için gerekirse 3D görselleştirme de ekliyoruz."),
  ("Kızıltepe'deki geniş aile dairesi için ne önerirsiniz?", "Odaları sırayla dolaşan, düzeni net gösteren 90 saniyelik bir tur."),
  ("Yazın çekim ne zaman yapılmalı?", "Dış cephe akşamüstü, iç mekân gün içinde."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ NEVŞEHİR EMLAK
"nevsehir-emlak-video": dict(
 lede="Kapadokya'da bir mağara evin alıcısı İstanbul'da, Seul'de ya da Madrid'de olabilir. Nevşehir'in merkezindeki dairenin alıcısı ise şehirde yaşayan bir aile. Aynı ilde iki bambaşka piyasa.",
 bolum=[
  ("Nevşehir'de konut piyasası",
   "<p>TÜİK'e göre Nevşehir'de Eylül 2025–Ağustos 2026 arasında <strong>5.720 konut</strong> satıldı; satışların <strong>%38,8'i ilk el</strong>. Ağustos 2026'da satış bir yıl öncesine göre <strong>%9,8</strong> geriledi; Türkiye genelinden daha az.</p>"),
  ("Kapadokya: mağara ev ve taş konak",
   "<p>Göreme, Uçhisar, Ürgüp ve Mustafapaşa'da kayaya oyulmuş mağara evler ve taş konaklar; alıcı çoğu zaman butik otel, pansiyon ya da ikinci ev için arıyor. Satılan şey peribacalarına bakan teras, kayadan oyulmuş odaların serinliği ve sabah gökyüzünü dolduran balonlar. Video bunu göstermeli: balonların kalktığı bir sabah terastan manzara, odaların dokusu ve avlu.</p>"
   "<p>Kapadokya koruma alanı; tadilat ve kullanım izinleri alıcının sorduğu ilk şeylerden. Bu bilgiyi belgeye dayanarak veriyoruz.</p>"),
  ("Şehir merkezi",
   "<p>Nevşehir merkezinde aile alıcılar için daireler ve yeni siteler; turizmde, kamuda ve üniversitede çalışanlar. Okula, hastaneye ve çarşıya mesafe; üniversite çevresinde öğrenci kiralıkları.</p>"),
  ("Balonlar ve drone",
   "<p>Kapadokya'da sabahları sıcak hava balonları uçuyor ve bölgede drone uçuşu sıkı kurallara bağlı; balon saatlerinde ve uçuş alanlarında drone kullanmıyoruz. Havadan görüntü gereken mülklerde izin durumunu önceden kontrol ediyor, gerekirse yüksek bir terastan yerden çekiyoruz. Kurgu ve renk bizde; çekim günlerinde bölgedeki kamera ortağımızla sahadayız.</p>"),
 ],
 sss=[
  ("Mağara evimizi yabancı alıcıya nasıl anlatırız?", "Balonlu bir sabah terastan manzara, oda oda tur ve kaya dokusu; İngilizce ya da ihtiyaç duyulan dilde altyazıyla."),
  ("Kapadokya'da drone kullanılabilir mi?", "Kurallar sıkı; balon saatlerinde ve uçuş alanlarında kullanmıyoruz. Mülkün konumuna göre izin durumunu önceden kontrol ediyoruz."),
  ("Butik otel olarak kullanılan mülk için video ne anlatmalı?", "Oda sayısı, ortak alanlar, teras ve manzara; mülkün işletme potansiyelini gösteren bir anlatım."),
  ("Merkezdeki dairemiz için ne önerirsiniz?", "60 saniyelik bir tur ve okula, çarşıya mesafe; öğrenci kiralığında dikey kısa bir sürüm."),
 ],
 kaynak=[KAYNAK_KONUT, KAYNAK_IHA],
),

# ------------------------------------------------------------------ ORDU EMLAK
"ordu-emlak-video": dict(
 lede="Ordu'da satılan konutların %45'i sıfır; Türkiye'deki en yüksek oranlardan biri. Sahile paralel yükselen yeni binalarda alıcının ilk sorusu aynı: denizi görüyor mu?",
 bolum=[
  ("Ordu'da konut piyasası",
   "<p>TÜİK'e göre Ordu'da Eylül 2025–Ağustos 2026 arasında <strong>13.268 konut</strong> satıldı; bunların <strong>5.965'i ilk el</strong>. Ağustos 2026'da satış bir yıl öncesine göre <strong>%15,5</strong> geriledi (1.141'den 964'e).</p>"
   "<p>Yeni konutun bu kadar yoğun olduğu bir piyasada müteahhitler aynı sahil hattında, benzer manzara vaadiyle satış yapıyor. Fark yaratan, manzaranın gerçek hâlini gösterebilmek.</p>"),
  ("Sahil ve yamaç",
   "<p><strong>Altınordu sahili:</strong> deniz manzaralı yeni binalar ve siteler. Hangi kattan neyin göründüğünü gerçek yükseklikten göstermek, aynı manzarayı vaat eden projeler arasında fark yaratıyor.</p>"
   "<p><strong>Boztepe eteği:</strong> şehre ve denize tepeden bakan evler; teleferikle çıkılan tepenin manzarası.</p>"
   "<p><strong>Ünye ve Fatsa:</strong> kendi çarşısı ve sahili olan büyük ilçeler; aile konutu ve yazlık.</p>"
   "<p><strong>Fındık bahçeli evler:</strong> köylerde, fındık bahçesi içinde müstakil evler; bahçe ve arazi sınırı havadan.</p>"),
  ("Gurbetteki alıcı",
   "<p>Ordu'dan büyük şehirlere göç etmiş aileler memlekette ev alıyor; emeklilik ya da yaz için. Bu alıcı evi uzaktan, telefonda görüyor. Mahalleyi, denize ve çarşıya mesafeyi ve evin içini gösteren bir video, onun için ilk gezi.</p>"),
  ("Çekim düzeni",
   "<p>Ordu-Giresun Havalimanı denizin üzerine kurulu ve şehre yakın; çevresinde drone uçuşu izne bağlı. Karadeniz'de hava gün içinde değişebiliyor; deniz manzaralı mülkler için açık bir saat bekliyor, yedek gün koyuyoruz. Kurgu ve renk bizde; çekimde bölgedeki kamera ortağımızla çalışıyoruz.</p>"),
 ],
 sss=[
  ("Deniz manzaralı dairemizin manzarasını nasıl kanıtlarız?", "Dairenin katına denk gelen yükseklikten drone ile çekip balkondan bakışı gösteriyoruz; izin gerekiyorsa önceden alıyoruz."),
  ("İstanbul'da yaşayan alıcıya Ordu'daki evi nasıl anlatırız?", "Mahalle, denize ve çarşıya mesafe ve evin içi; 60–90 saniyelik bir video."),
  ("Fındık bahçeli evin ilanı için ne önerirsiniz?", "Havadan bahçe ve arazi sınırı, ardından ev; hasat öncesi, yaz sonunda en yeşil hâlinde."),
  ("Hava kapalıysa ne oluyor?", "İç çekimi yapıyor, manzara için yedek gün koyuyoruz."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ RİZE EMLAK
"rize-emlak-video": dict(
 lede="Rize'de düz arazi neredeyse yok; evler denizle dağ arasındaki dar şeride ve çay bahçelerinin içine yerleşmiş. Bir evin değerini çoğu zaman yolu, eğimi ve manzarası belirliyor.",
 bolum=[
  ("Rize'de konut piyasası",
   "<p>TÜİK'e göre Rize'de Eylül 2025–Ağustos 2026 arasında <strong>3.624 konut</strong> satıldı; satışların <strong>%29,4'ü ilk el</strong>. Ağustos 2026'da satış 228'e indi; bir yıl önce 312'ydi, düşüş <strong>%26,9</strong>. Küçük ve yavaşlayan bir piyasada her ilan daha uzun süre bekliyor; iyi sunum bu süreyi kısaltıyor.</p>"),
  ("Mülk tipine göre video",
   "<p><strong>Şehir merkezi ve sahil:</strong> deniz manzaralı daireler; denizi dolduran yeni sahil yolu ve havalimanı ile değişen kıyı. Manzara ve kat.</p>"
   "<p><strong>Çay bahçeli evler:</strong> yamaçta, çay bahçeleri içinde müstakil evler. Alıcının sorduğu ilk şey yol: eve araçla çıkılıyor mu, kışın yol açık mı? Havadan yolu, bahçeyi ve evin yamaçtaki yerini gösteren bir plan bu soruyu cevaplıyor.</p>"
   "<p><strong>Yayla evleri:</strong> Ayder ve çevresindeki yaylalarda ahşap evler; yazın kullanılan, turizme de açık mülkler.</p>"),
  ("Gurbetteki alıcı",
   "<p>Rize'nin önemli bir nüfusu büyük şehirlerde yaşıyor; memlekette ev, emeklilik ya da yaz için alınıyor. Bu alıcı evi telefonda görüyor. Yolu, bahçeyi, manzarayı ve evin içini gösteren bir video, ona eve gelmeden karar verecek kadar bilgi veriyor.</p>"),
  ("Hava ve drone",
   "<p>Rize Türkiye'nin en çok yağış alan şehri; açık bir gün bulmak için yedek gün koyuyoruz. Sis ve bulut ise yayla evleri için bazen en güzel görüntü. Rize-Artvin Havalimanı denizin üzerinde, Pazar'da; çevresinde drone uçuşu izne bağlı. Kurgu ve renk bizde; çekim günlerinde bölgedeki kamera ortağımızla sahadayız.</p>"),
 ],
 sss=[
  ("Yamaçtaki evimizin yolunu nasıl gösterirsiniz?", "Havadan, ana yoldan eve çıkan yolu takip eden bir planla; alıcı erişimi tek bakışta görüyor."),
  ("Yağmurlu havada çekim yapılır mı?", "İç çekim evet; dış ve manzara için açık bir gün bekliyor, yedek gün koyuyoruz."),
  ("Yayla evimiz için ne zaman çekim yapmalıyız?", "Yaz başında, yol açık ve yayla yeşilken. Sisli ve açık havayı ayrı ayrı yakalamaya çalışıyoruz."),
  ("Çay bahçeli arazi ilanı için ne önerirsiniz?", "Havadan arazi sınırı, bahçe ve yol bağlantısı; kısa bir ilan videosu."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ ŞANLIURFA EMLAK
"sanliurfa-emlak-video": dict(
 lede="Şanlıurfa'da son bir yılda 33.387 konut satıldı; il Türkiye'de 14. sırada. Genç ve kalabalık ailelerin şehrinde talep geniş dairelerde; Karaköprü'nün siteleri bu talebin merkezinde.",
 bolum=[
  ("Şanlıurfa'da konut piyasası",
   "<p>TÜİK'e göre Şanlıurfa'da Eylül 2025–Ağustos 2026 arasında <strong>33.387 konut</strong> satıldı; satışların <strong>%35,4'ü ilk el</strong>. Ağustos 2026'da satış bir yıl öncesine göre <strong>%18,3</strong> geriledi (3.188'den 2.604'e).</p>"),
  ("Geniş daireyi göstermek",
   "<p>Şanlıurfa'da aileler kalabalık; 4+1 ve daha büyük daireler talebin önemli bir kısmı. Bu dairelerde oda sayısı fazla, düzen karmaşık ve fotoğraf yetersiz kalıyor. Video odaları sırayla dolaşarak dairenin akışını gösteriyor: salonun büyüklüğü, mutfağın yeri, yatak odalarının ayrı koridorda olup olmadığı, balkonlar.</p>"),
  ("Semte göre video",
   "<p><strong>Karaköprü:</strong> yeni siteler, havuzlar ve sosyal alanlar; şehrin en çok tercih edilen yeni konut bölgesi. Site yaşamı ve ortak alanlar.</p>"
   "<p><strong>Haliliye ve Eyyübiye:</strong> merkezde apartmanlar ve eski mahalleler; Balıklıgöl'e, çarşıya ve hastaneye yakınlık.</p>"
   "<p><strong>Siverek, Viranşehir ve ilçeler:</strong> kendi çarşısı olan büyük ilçelerde aile konutu ve müstakil evler.</p>"
   "<p><strong>Tarım arazisi:</strong> Harran ovasında sulanan araziler; sınır, kanal ve yol bağlantısı havadan.</p>"),
  ("Sıcakla çekim",
   "<p>Şanlıurfa yazın Türkiye'nin en sıcak şehirlerinden biri; öğle saatinde hem ekip hem görüntü zorlanıyor. Dış çekimi gün doğumundan sonraki ilk saatlere ve akşamüstüne, iç çekimi gün ortasına koyuyoruz. Kurgu ve renk bizde; çekim günlerinde bölgedeki kamera ortağımızla birlikteyiz.</p>"),
 ],
 sss=[
  ("Geniş aile dairesi için video ne kadar olmalı?", "90–120 saniye; her odayı kısa tutup dairenin akışını gösteren bir tur."),
  ("Karaköprü'deki site dairemiz için ne önerirsiniz?", "Site girişi, havuz ve ortak alanlar, ardından daire; okula ve ana yola mesafe."),
  ("Tarım arazisi ilanı için drone gerekli mi?", "Sınırı, kanalı ve yol bağlantısını göstermek için çok faydalı; konumu haritadan kontrol ediyoruz."),
  ("Yazın çekim hangi saatte yapılmalı?", "Dış çekim gün doğumundan sonraki ilk saatlerde ya da akşamüstü; iç çekim gün ortasında."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ SİVAS EMLAK
"sivas-emlak-video": dict(
 lede="Sivas'ta satılan konutların %46,2'si sıfır ve Ağustos 2026'da satışlar bir önceki yılın üzerine çıktı. Hızlı trenle Ankara'ya bağlanan şehirde yeni konut hızla büyüyor.",
 bolum=[
  ("Sivas'ta konut piyasası",
   "<p>TÜİK'e göre Sivas'ta Eylül 2025–Ağustos 2026 arasında <strong>10.898 konut</strong> satıldı; bunların <strong>5.035'i (%46,2) ilk el</strong>, Türkiye'nin en yüksek oranlarından biri. Ağustos 2026'da satış <strong>1.091</strong> oldu; bir yıl önce 1.058'di, artış <strong>%3,1</strong>. Türkiye genelinde düşüş %14,7 iken Sivas'ın piyasası büyüyor.</p>"),
  ("Yeni siteler arasında fark",
   "<p>Bu kadar yeni projenin olduğu bir şehirde alıcı siteleri karşılaştırıyor. Sivas'ın uzun ve soğuk kışında alıcının sorduğu şeyler belli: ısınma sistemi, yalıtım, kapalı otopark, asansör. Bunları videoda yakın planda gösteriyor, sitenin ortak alanlarını ve dairenin ışığını öne çıkarıyoruz. Bitmemiş projelerde 3D render ile gerçek arsa görüntüsünü birleştiriyoruz.</p>"),
  ("Alıcıya göre video",
   "<p><strong>Aile alıcı:</strong> yeni sitelerde geniş daireler; okula, hastaneye ve çarşıya mesafe.</p>"
   "<p><strong>Öğrenci ve akademisyen:</strong> Cumhuriyet Üniversitesi şehrin en büyük kiralık talebini yaratıyor; kampüs şehrin dışında olduğu için alıcı otobüs hattını ve yolu soruyor.</p>"
   "<p><strong>Ankara bağlantılı alıcı:</strong> hızlı trenle Ankara'ya gidip gelen ya da Ankara'dan emekli olup memlekete dönen aileler. İstasyona mesafe ve şehrin sakin yaşamı.</p>"),
  ("Kışın çekim",
   "<p>Sivas'ta kış uzun; karlı bir gün site ve dış cephe için güzel bir görüntü, ama yollar ve ışık değişken. Çekim tarihini havaya göre esnek tutuyoruz; iç mekânın sıcak ve aydınlık görünmesi için ışığı buna göre kuruyoruz. Kurgu ve renk bizde; çekim günlerinde bölgedeki kamera ortağımızla sahadayız.</p>"),
 ],
 sss=[
  ("Yeni sitemizi rakip projelerden nasıl ayırırız?", "Isınma, yalıtım, kapalı otopark gibi kış detaylarını ve sitenin yaşamını göstererek; alıcı bunları soruyor."),
  ("Ankara'dan dönecek alıcıya nasıl ulaşırız?", "Hızlı tren istasyonuna mesafeyi ve şehrin sakin yaşamını gösteren, Ankara'daki alıcının telefonunda izleyeceği kısa bir video; reklamı Ankara'ya da hedefliyoruz."),
  ("Kampüs çevresindeki kiralıkta neyi göstermeliyiz?", "Odanın gerçek boyutunu, ısınmayı ve otobüs durağına yürüme süresini. Sivaslı olmayan öğrenci ailesi en çok bunları soruyor."),
  ("Kongre binası ya da Gök Medrese manzaralı daire için ne önerirsiniz?", "Manzarayı akşam aydınlatmasında, balkondan tek planla; tarihî merkezin hemen yanında oturmak bu dairelerin asıl satış noktası."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ VAN EMLAK
"van-emlak-video": dict(
 lede="Van'da bir dairenin değerini çoğu zaman göl belirliyor: balkondan Van Gölü'nün mavisi ve karşısında Süphan'ın karlı zirvesi görünüyor mu?",
 bolum=[
  ("Van'da konut piyasası",
   "<p>TÜİK'e göre Van'da Eylül 2025–Ağustos 2026 arasında <strong>13.277 konut</strong> satıldı; satışların <strong>%39,1'i ilk el</strong>, Türkiye ortalamasının üzerinde. Ağustos 2026'da satış bir yıl öncesine göre yalnızca <strong>%3,9</strong> geriledi; Türkiye genelinde düşüş %14,7. Van, görece dirençli bir piyasa.</p>"),
  ("2011'den sonra yeniden kurulan şehir",
   "<p>Van, 2011 depremlerinden sonra büyük ölçüde yeniden yapıldı; şehrin önemli bir kısmı o yıllardan sonra yükselen binalardan oluşuyor. Alıcı yine de binanın yapı bilgilerini görmek istiyor; yapı yılını ve ruhsat tarihini ilan sahibinin belgesine göre ekranda veriyoruz.</p>"),
  ("Semte göre video",
   "<p><strong>Edremit ve göl kıyısı:</strong> göl manzaralı siteler ve yazlık evler; manzara ve göle mesafe. Göl manzarasını sabah ışığında, gölün en mavi olduğu saatte çekiyoruz.</p>"
   "<p><strong>Tuşba ve İpekyolu:</strong> şehrin merkezinde yeni siteler ve apartmanlar; okula, hastaneye ve çarşıya mesafe.</p>"
   "<p><strong>Kampüs ve göl arası:</strong> Van Yüzüncü Yıl Üniversitesi'nin yerleşkesi göl kıyısına yakın; kampüs çevresindeki daireler hem öğrenciye hem göl manzarası arayan aileye satılıyor.</p>"
   "<p><strong>Erciş:</strong> gölün kuzey kıyısında büyük bir ilçe; aile konutu ve müstakil evler.</p>"),
  ("Çekim düzeni",
   "<p>Van'ın kışı uzun ve karlı, yazı serin ve aydınlık. Havalimanı göl kıyısında, şehre yakın; çevresinde drone uçuşu izne bağlı. Göl manzaralı mülklerde konumu önceden kontrol ediyoruz. Kurgu ve renk bizde; çekim günlerinde bölgedeki kamera ortağımızla birlikteyiz.</p>"),
 ],
 sss=[
  ("Göl manzaralı dairemizi nasıl gösterirsiniz?", "Salondan balkona açılan bir planla, sabah ışığında; izin varsa havadan göl ve binanın konumu."),
  ("Van'da drone kullanılabilir mi?", "Havalimanına yakın göl kıyısında izin gerekiyor; konumu önceden kontrol ediyoruz."),
  ("Edremit'teki göl kıyısı yazlığımız için ne zaman çekim yapmalıyız?", "Haziran–Eylül arası; göl en mavi, çevre en yeşil. Sabah saatlerinde göl yüzeyi durgun ve parlak."),
  ("Van'a gelmeden daireyi görmek isteyen alıcıya ne gönderelim?", "Mahalleyi, binanın girişini ve dairenin her odasını gösteren tek bir video; alıcı karar vermeden önce gezmiş gibi oluyor."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ ZONGULDAK EMLAK
"zonguldak-emlak-video": dict(
 lede="Zonguldak'ta Ağustos 2026'da satışlar bir yıl önceyle neredeyse aynı kaldı. Yamaçlara yaslanan şehirde satılan konutların %43,3'ü sıfır; madenci şehri yeni binalarla yenileniyor.",
 bolum=[
  ("Zonguldak'ta konut piyasası",
   "<p>TÜİK'e göre Zonguldak'ta Eylül 2025–Ağustos 2026 arasında <strong>7.872 konut</strong> satıldı; bunların <strong>3.407'si ilk el</strong>. Ağustos 2026'da satış 688 oldu; bir yıl önce 691'di. Türkiye genelinde %14,7 düşüş varken Zonguldak'ın piyasası yerinde duruyor.</p>"),
  ("Yamaç şehrinde ev",
   "<p>Zonguldak denizle dağ arasında, dik yamaçlara kurulu bir şehir. Alıcının ilk sorduğu şey çoğu zaman binaya giden yol, eğim, otopark ve asansör. Havadan binanın yamaçtaki yerini, yolu ve deniz manzarasını gösteren bir plan bu soruları tek seferde cevaplıyor.</p>"),
  ("İlçeye göre alıcı",
   "<p><strong>Merkez ve Kozlu:</strong> deniz manzaralı daireler; maden ve kamu çalışanı aileler. Okula, hastaneye ve çarşıya mesafe.</p>"
   "<p><strong>Ereğli:</strong> çelik fabrikasıyla büyüyen, kendi sahili ve çarşısı olan büyük bir ilçe; aile konutu ve deniz manzaralı yeni siteler.</p>"
   "<p><strong>Çaycuma ve Devrek:</strong> daha düz ve sakin ilçelerde bahçeli evler ve yeni siteler.</p>"
   "<p><strong>Kampüs çevresi:</strong> Zonguldak'ta üniversite kampüsü de yamaçta; öğrenci evlerinde yokuş ve ulaşım, eşyalardan önce sorulan şey.</p>"),
  ("Hava ve çekim",
   "<p>Zonguldak'ta güneşli bir sabahın ardından öğleden sonra sis inebiliyor; denizi gösteren planlar için hava tahminine göre gün seçiyor, gerekirse ikinci bir güne kaydırıyoruz. Çaycuma'daki havalimanı merkezden uzak; ama liman, santral ve çelik tesislerinin çevresinde havadan çekim izin istiyor. Sahadaki kamera ekibi bölgeden, kurgu ve renk bizden.</p>"),
 ],
 sss=[
  ("Yamaçtaki binamızın yolunu nasıl gösterirsiniz?", "Havadan, ana yoldan binaya çıkan yolu takip eden bir planla; otopark ve giriş de görünüyor."),
  ("Ereğli'deki deniz manzaralı dairemiz için ne önerirsiniz?", "Balkondan manzara, sitenin ortak alanları ve daire; sahile ve çarşıya mesafe."),
  ("Madenci lojmanı ya da eski kooperatif dairesi için ne önerirsiniz?", "Yenilenmiş iç mekânı ve binanın konumunu öne çıkaran kısa bir tur; şehrin merkezine ve sahile yürüme süresini ekranda veriyoruz."),
  ("Devrek ya da Çaycuma'daki bahçeli ev için ne önerirsiniz?", "Bahçeyi ve evin tamamını havadan, ardından odaları; ilçe merkezine ve Zonguldak'a sürüş süresi ekranda."),
 ],
 kaynak=[KAYNAK_KONUT],
),

# ------------------------------------------------------------------ ADANA DRONE
"adana-drone-cekimi": dict(
 lede="Çukurova'nın ufka kadar uzanan pamuk ve narenciye tarlaları, Seyhan'ın kıyısında yükselen siteler ve Hacı Sabancı OSB'nin fabrikaları. Adana'yı havadan anlatmak, ovanın büyüklüğünü anlatmak demek.",
 bolum=[
  ("Adana'da uçuş: İncirlik ve şehir",
   "<p>Sarıçam'daki İncirlik Hava Üssü ve Seyhan'daki Şakirpaşa havalimanı sahası, Adana'nın hava sahasını şekillendiren iki nokta. Bu alanların çevresinde drone uçuşu izne bağlı; şehrin içinde de durum mahalleden mahalleye değişiyor. Temmuz 2026'da yenilenen SHGM talimatına göre haritada yeşil görünen yerlerde ayrı izne gerek yok. Her çekimden önce mülkün koordinatını haritada kontrol ediyor, gerekiyorsa başvuruyu çekim tarihine göre önceden yapıyoruz.</p>"),
  ("Ovada drone ne işe yarıyor",
   "<p><strong>Tarım ve narenciye:</strong> Kozan, Ceyhan ve Yüreğir'in bahçeleri ve tarlaları; arazinin büyüklüğünü, sulama düzenini ve yola bağlantısını tek karede gösteriyor. Narenciye ihracatçıları için hasattan paketlemeye uzanan filmin açılışı.</p>"
   "<p><strong>Sanayi:</strong> Hacı Sabancı OSB ve Ceyhan çevresindeki tesisler; kampüsün ölçeği, otoyola ve limana bağlantı. Ceyhan'daki enerji ve liman tesisleri kritik yapı sayılıyor; çevrelerinde izinsiz uçmuyoruz.</p>"
   "<p><strong>Şantiye ve konut:</strong> Çukurova ve Sarıçam'da yükselen yeni siteler için aylık ilerleme çekimi; aynı noktadan, aynı yükseklikten.</p>"),
  ("Sıcakla uçmak",
   "<p>Adana yazın çok sıcak; öğle saatinde hava titreşiyor, ova soluk görünüyor ve drone bataryaları sıcakta daha hızlı tükeniyor. Uçuşları gün doğumundan sonraki ilk iki saate ve akşamüstüne koyuyoruz. Ekim–Mayıs arası ise Adana'da havadan çekim için en temiz ışığı veriyor.</p>"
   "<p>Kurgu ve renk bizde; çekim günlerinde bölgedeki kamera ortağımızla sahadayız.</p>"),
 ],
 sss=[
  ("Sarıçam'daki tesisimizin üzerinde drone uçabilir mi?", "İncirlik'e yakınlık nedeniyle izin gerekebilir. Koordinatı kontrol edip çekimden önce size söylüyoruz."),
  ("Narenciye bahçemiz için ne zaman çekim yapmalıyız?", "Hasat döneminde, kışın; meyve ağaçtayken bahçe en canlı görünüyor."),
  ("Yazın uçuş yapılabilir mi?", "Evet, sabah erken ya da akşamüstü. Öğle sıcağında hem görüntü hem ekipman zorlanıyor."),
  ("Şantiye çekimini her ay aynı açıdan alıyor musunuz?", "Evet; ilk uçuşta noktaları kaydedip her ay aynı yerden çekiyoruz."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ ADIYAMAN DRONE
"adiyaman-drone-cekimi": dict(
 lede="Nemrut Dağı'nın zirvesindeki dev heykeller, Atatürk Barajı'nın uçsuz bucaksız göl yüzeyi ve depremden sonra yeniden yükselen şehir. Adıyaman'da drone, hem tarihi hem yeniden yapılanmayı çekiyor.",
 bolum=[
  ("Şantiye ve yeniden yapılanma",
   "<p>Şubat 2023 depremlerinden sonra Adıyaman'da yeni konut alanları ve yeni binalar hızla yükseliyor. Müteahhitler ve kurumlar için şantiye ilerlemesini aylık olarak, aynı noktadan ve aynı yükseklikten çekmek, hem iş sahibine hem alıcıya ilerlemenin somut kanıtı. Proje bitiminde bu kareler, temelden teslime kadar süren bir zaman çizelgesine dönüşüyor.</p>"),
  ("Nemrut, baraj ve doğa",
   "<p><strong>Nemrut Dağı:</strong> UNESCO Dünya Mirası listesinde, millî park ve ören yeri. Drone ile çekim Bakanlık ve millî park izinlerine bağlı; gün doğumu ve gün batımında heykellerin üzerine düşen ışık, Türkiye'nin en tanınan karelerinden. İzin sürecini takvime baştan koyuyoruz.</p>"
   "<p><strong>Atatürk Barajı ve Kahta:</strong> geniş göl yüzeyi, adalar ve kıyı köyleri. Baraj gövdesi ve santral kritik tesis; çevresinde izinsiz uçmuyoruz, göl kıyısındaki mülk ve turizm çekimlerini izinli bölgelerde yapıyoruz.</p>"
   "<p><strong>Cendere Köprüsü:</strong> Roma döneminden kalan taş köprü; Nemrut yolundaki en güçlü havadan karelerden biri.</p>"),
  ("Uçuş ve ışık",
   "<p>Adıyaman Havalimanı'nın çevresi kontrollü hava sahası; şehirdeki diğer noktalar için koordinatı haritada kontrol ediyoruz. Yazın öğle saatinde ışık çok sert; uçuşları sabaha ve akşamüstüne koyuyoruz. Kurgu ve renk bizde; çekim günlerinde bölgedeki kamera ortağımızla sahadayız.</p>"),
 ],
 sss=[
  ("Nemrut'ta drone ile çekim yapılabilir mi?", "Bakanlık ve millî park izniyle. Süreç uzun olabiliyor; başvuruyu çekim tarihinden önce başlatıyoruz."),
  ("Şantiye ilerleme çekimi ne sıklıkta yapılmalı?", "Ayda bir genellikle yeterli. Her ay aynı noktadan çekip ilerlemeyi yan yana gösteriyoruz."),
  ("Baraj gölü kıyısındaki tesisimizi çekebilir misiniz?", "Evet, baraj gövdesi ve santralden uzak, izinli bölgelerde."),
  ("Hangi saatte uçmak daha iyi?", "Gün doğumu ve gün batımı; yaz öğlesinde ışık sert ve hava titreşimli."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ AFYONKARAHİSAR DRONE
"afyonkarahisar-drone-cekimi": dict(
 lede="Şehrin ortasında yükselen kayalık ve tepesindeki kale, İscehisar'ın beyaz mermer ocakları, termal otellerin havuzları ve Frig Vadisi'nin kayaya oyulmuş anıtları. Afyonkarahisar havadan bakınca bambaşka görünüyor.",
 bolum=[
  ("Mermer ocakları ve sanayi",
   "<p>Afyonkarahisar, İscehisar çevresindeki ocaklarıyla Türkiye'nin mermer başkentlerinden biri. Ocağın havadan görüntüsü, dev beyaz basamaklar ve iş makineleriyle, mermer firmasının en etkileyici tanıtım karesi; alıcıya ocağın ölçeğini ve rezervini tek bakışta gösteriyor. Ocak içi uçuşu işletmenin iş güvenliği kurallarına göre planlıyor, patlatma ve yükleme saatlerinde uçmuyoruz.</p>"
   "<p>Organize sanayi bölgesindeki gıda ve mermer işleme tesisleri için kampüsün ölçeği ve otoyol bağlantısı.</p>"),
  ("Termal turizm ve şehir",
   "<p><strong>Termal oteller:</strong> şehrin çevresindeki termal bölgede büyük oteller ve devre mülk siteleri. Havuzların, tesisin ve çevrenin havadan görüntüsü, otel tanıtımının açılışı. Kışın havuzlardan yükselen buhar havadan da etkileyici.</p>"
   "<p><strong>Afyon Kalesi:</strong> şehrin ortasında, kayalığın üzerinde. Kale ve şehir silueti akşam ışığında en güçlü hâlinde.</p>"
   "<p><strong>Frig Vadisi:</strong> İhsaniye çevresinde kayaya oyulmuş anıtlar ve peribacası benzeri oluşumlar. Ören yeri olan noktalarda izin gerekiyor.</p>"),
  ("Uçuş planı",
   "<p>Afyonkarahisar'ın merkezinde sivil havalimanı yok; en yakın havalimanı Kütahya sınırındaki Zafer Havalimanı. Bu, şehir içindeki uçuşları çoğu konumda kolaylaştırıyor; yine de askerî alanlar ve kritik tesisler için her koordinatı haritada kontrol ediyoruz. Karasal iklimde kış sabahları sisli; sisin kalktığı öğle saatlerini ya da sisin üzerinden yükselen kale görüntüsünü hedefliyoruz.</p>"
   "<p>Kurgu ve renk bizde; çekim günlerinde bölgedeki kamera ortağımızla sahadayız.</p>"),
 ],
 sss=[
  ("Mermer ocağımızı havadan çekebilir misiniz?", "Evet. İş güvenliği kurallarınıza uyarak, patlatma ve yükleme saatlerinin dışında uçuyoruz."),
  ("Termal otelimiz için drone ne zaman çekilmeli?", "Kışın soğuk bir sabah; havuzlardan yükselen buhar havadan çok etkileyici."),
  ("Kaleyi havadan çekebilir miyiz?", "Koordinata göre çoğu zaman mümkün; tarihî alan olduğu için kurallara uyuyor, akşam ışığını seçiyoruz."),
  ("Frig Vadisi'nde drone uçabilir mi?", "Ören yeri olan noktalarda izin gerekiyor; başvuruyu önceden yapıyoruz."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ ANKARA DRONE
"ankara-drone-cekimi": dict(
 lede="Ankara, drone için Türkiye'nin en zor şehri. Esenboğa, Etimesgut ve Akıncı'daki hava üsleri, bakanlıklar ve Meclis; başkentte uçmadan önce bir harita, bir de izin süreci gerekiyor.",
 bolum=[
  ("Başkentin hava sahası",
   "<p>Esenboğa Havalimanı şehrin kuzeyinde, Etimesgut ve Akıncı'daki askerî hava üsleri batıda; Güvercinlik de şehrin içinde. Çankaya'daki bakanlıklar, Meclis, Cumhurbaşkanlığı yerleşkesi ve Anıtkabir çevresi ayrıca yasak ya da sıkı kısıtlı alan. Bu yüzden Ankara'nın merkezinin büyük kısmında drone uçuşu ya izne bağlı ya da hiç mümkün değil.</p>"
   "<p>Temmuz 2026'da yenilenen SHGM talimatıyla haritada yeşil görünen bölgelerde ayrı izin gerekmiyor; Ankara'da bu bölgeler çoğunlukla şehrin dışında. Her teklifte önce koordinata bakıyor, uçuşun mümkün olup olmadığını ve izin süresini baştan yazıyoruz.</p>"),
  ("Ankara'da drone nerede işe yarıyor",
   "<p><strong>Gölbaşı, İncek ve güney:</strong> villa ve site projeleri, Mogan Gölü kıyısı; uçuş planı şehir merkezine göre daha esnek.</p>"
   "<p><strong>Sanayi bölgeleri:</strong> OSTİM, İvedik ve Sincan'daki organize sanayi bölgeleri. Bazıları askerî üslere yakın; tesis tanıtımında havadan planı mümkünse alıyor, değilse yüksek bir noktadan yerden ve 3D animasyonla tamamlıyoruz.</p>"
   "<p><strong>Polatlı, Beypazarı ve kırsal:</strong> tarım arazileri, Gordion ve Beypazarı'nın tarihî dokusu; açık bozkırda geniş planlar.</p>"
   "<p><strong>Etkinlik:</strong> kongre, fuar ve açık hava etkinlikleri; kalabalık üzerinde uçuş kurallara takıldığı için alanın kenarından ve izinli olarak.</p>"),
  ("Planı izne göre kurmak",
   "<p>Ankara'da havadan çekim isteyen bir işin takvimi izinle başlıyor. İzin süresi konuma göre değiştiği için çekim tarihini buna göre koyuyor, izin çıkmazsa aynı anlatımı verebilecek alternatif bir yöntem öneriyoruz. Kurgu ve renk bizde; çekim günlerinde Ankara'daki kamera ortağımızla sahadayız.</p>"),
 ],
 sss=[
  ("Çankaya'da drone ile çekim yapılabilir mi?", "Çoğu yerde hayır; resmî binalar ve kısıtlı alanlar nedeniyle uçuş mümkün değil ya da izin çok sıkı. Alternatif bir anlatım öneriyoruz."),
  ("Sincan'daki fabrikamızı havadan çekebilir misiniz?", "Askerî üsse yakınlık nedeniyle izin gerekebilir. Koordinatı kontrol edip önceden söylüyoruz; mümkün değilse 3D animasyonla tamamlıyoruz."),
  ("Gölbaşı'ndaki villa projemiz için drone kullanılabilir mi?", "Çoğu konumda evet; koordinatı haritada kontrol ediyoruz."),
  ("İzin ne kadar sürer?", "Konuma göre değişiyor. Teklif aşamasında süreyi yazıyor, çekim tarihini buna göre koyuyoruz."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ AYDIN DRONE
"aydin-drone-cekimi": dict(
 lede="Büyük Menderes ovası havadan bakınca incir, zeytin ve pamuktan dokunmuş bir halı gibi. Kuşadası'nın otelleri, Didim'in koyları ve Afrodisias'ın mermer sütunları aynı ilde.",
 bolum=[
  ("Ova, bahçe ve üretici",
   "<p>Aydın'ın incir, zeytin ve kestane bahçeleri, pamuk tarlaları ve zeytinyağı fabrikaları. Bahçenin büyüklüğünü, ağaçların düzenini ve fabrikaya giden yolu havadan göstermek, hem satış hem ihracat filmi için en güçlü açılış. Arazi satışlarında sınırı havadan çizmek, alıcının ilk sorusunu cevaplıyor.</p>"),
  ("Kıyı ve turizm",
   "<p><strong>Kuşadası:</strong> oteller, marina ve kruvaziyer limanı. Otel tanıtımında tesisin denizle ilişkisi ve plaj; sezon dışında, misafir yokken. Liman sahasında uçuş liman işletmesinin iznine bağlı.</p>"
   "<p><strong>Didim ve Akbük:</strong> yazlık siteler ve koylar; Apollon Tapınağı'nın çevresi ören yeri, izin gerekiyor.</p>"
   "<p><strong>Dilek Yarımadası:</strong> millî park; koylar ve orman. Ticari çekim için millî park izni.</p>"),
  ("Antik kentler ve izin",
   "<p>Aydın, Türkiye'nin en çok antik kente sahip illerinden biri: Afrodisias, Priene, Milet, Nysa, Tralleis. Bu alanlarda drone ile çekim Kültür ve Turizm Bakanlığı iznine bağlı ve süreç haftalar alabiliyor. İzin gerektiren işlerde takvimi baştan buna göre kuruyoruz.</p>"
   "<p>Aydın'daki küçük havalimanı ve Didim tarafına yakın Milas-Bodrum Havalimanı'nın sahası dışında, ovanın çoğu SHGM haritasında daha esnek. Yaz sıcağında uçuşları sabaha ve akşamüstüne koyuyoruz. Kurgu ve renk bizde; çekim günlerinde bölgedeki kamera ortağımızla sahadayız.</p>"),
 ],
 sss=[
  ("İncir bahçemizi ne zaman çekmeliyiz?", "Yaz sonunda, meyve olgunlaşırken; bahçe en yeşil ve hareketli hâlinde."),
  ("Kuşadası'ndaki otelimizi sezon dışında çekmek mantıklı mı?", "Çok. Misafir yok, ışık yumuşak; görüntü sezon öncesi rezervasyon dönemine hazır oluyor."),
  ("Afrodisias'ta drone ile çekim yapılabilir mi?", "Bakanlık izniyle. Süreç uzun olabildiği için başvuruyu önceden başlatıyoruz."),
  ("Arazi satışında drone ne işe yarar?", "Sınırı, yolu ve ağaç düzenini tek karede gösteriyor; alıcı araziyi gelmeden değerlendirebiliyor."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ BİLECİK DRONE
"bilecik-drone-cekimi": dict(
 lede="Sakarya Nehri'nin vadisi, Söğüt'ün tarihî tepeleri, Bozüyük'ün seramik fabrikaları ve hızlı tren hattı. Bilecik küçük bir il ama havadan bakınca her köşesi başka bir hikâye.",
 bolum=[
  ("Bozüyük ve sanayi",
   "<p>Bozüyük, seramik, metal ve plastik üreticilerinin toplandığı bir sanayi ilçesi. Bu tesislerin tanıtımında havadan plan, kampüsün ölçeğini, depo ve sevkiyat alanını, otoyol ve demiryolu bağlantısını tek karede gösteriyor. Yabancı alıcıya giden filmin ilk saniyeleri çoğu zaman bu plan.</p>"),
  ("Vadi, nehir ve tarih",
   "<p><strong>Sakarya vadisi ve Osmaneli:</strong> nehrin kıvrımları, bağlar ve vadinin içinden geçen demiryolu. Havadan, sonbaharda bağların rengi değişirken en güzel.</p>"
   "<p><strong>Söğüt:</strong> Osmanlı'nın kuruluş topraklarında tarihî alanlar ve her yıl düzenlenen anma etkinlikleri; etkinlik çekiminde kalabalık üzerinde uçmuyor, alanın kenarından çekiyoruz.</p>"
   "<p><strong>Bilecik merkez:</strong> vadinin yamaçlarına kurulu şehir ve yeni konut alanları; şantiye ilerleme ve konut projesi tanıtımı.</p>"),
  ("Uçuş ve ekip",
   "<p>Bilecik'te sivil havalimanı yok; ilin büyük kısmı SHGM haritasında daha esnek. Yine de demiryolu, enerji hatları ve kritik tesisler için her koordinatı kontrol ediyoruz. Vadide rüzgâr gün içinde değişebiliyor; uçuşları sabah ve akşamüstüne koyuyoruz.</p>"
   "<p>Bilecik'te kendi ekibimizle çalışıyoruz; Bursa'dan yaklaşık bir buçuk saatte geliyoruz.</p>"),
 ],
 sss=[
  ("Bozüyük'teki fabrikamızı havadan çekebilir misiniz?", "Evet. Kampüsü, sevkiyat alanını ve yol bağlantısını havadan; üretim hattını gerekirse FPV ile içeriden çekiyoruz."),
  ("Söğüt'teki etkinlikte drone kullanılabilir mi?", "Kalabalık üzerinde uçmuyoruz; alanın kenarından ve izinli olarak çekiyoruz."),
  ("Vadide rüzgâr sorun olur mu?", "Gün içinde değişebiliyor; sakin sabah saatlerini seçiyoruz."),
  ("Bursa'dan mı geliyorsunuz?", "Evet, kendi ekibimizle; yaklaşık bir buçuk saatlik yol."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ BOLU DRONE
"bolu-drone-cekimi": dict(
 lede="Abant'ın gölü, Yedigöller'in sonbaharı, Kartalkaya'nın karlı pistleri ve İstanbul ile Ankara arasında uzanan ormanlar. Bolu'da drone çekimi çoğu zaman bir mevsim çekimi.",
 bolum=[
  ("Mevsimlerin ili",
   "<p><strong>Sonbahar:</strong> Yedigöller ve Gölcük'te kayın ve meşe ormanı sarıya, turuncuya ve kırmızıya dönüyor; göllerin yüzeyine yansıyan renkler havadan Türkiye'nin en etkileyici sonbahar karelerinden. Ekim ortası ile Kasım başı en renkli dönem.</p>"
   "<p><strong>Kış:</strong> Kartalkaya'nın pistleri ve otelleri; karlı ormanın üzerinden süzülen planlar otel ve kayak merkezi tanıtımının açılışı.</p>"
   "<p><strong>Yaz:</strong> Abant ve göl kıyısındaki tesisler, yayla evleri, bungalovlar; yeşil ve serin.</p>"),
  ("Koruma alanları ve izin",
   "<p>Yedigöller millî park, Abant ve Gölcük tabiat parkı; bu alanlarda ticari çekim için Doğa Koruma ve Millî Parklar izni gerekiyor. Otel ve tesis çekimlerinde izni tesisle birlikte alıyoruz. Göl kıyısında yaban hayatını ve ziyaretçileri rahatsız etmeyecek yükseklikte uçuyoruz.</p>"),
  ("Turizm ve konut",
   "<p>Bolu'daki otel, bungalov ve dağ evi işletmeleri için tanıtım; Mudurnu ve Göynük'ün tarihî dokusu için havadan şehir planları; İstanbul ve Ankara'dan ikinci ev arayan alıcıya yönelik orman içi konut projeleri. Bolu'da kendi ekibimizle çalışıyoruz; kar ve sis gibi hava değişimlerine göre çekim tarihini esnek tutuyoruz.</p>"),
 ],
 sss=[
  ("Yedigöller'de sonbahar çekimi için ne zaman gelmeliyiz?", "Ekim ortası ile Kasım başı arası; renkler her yıl biraz değiştiği için tarihi yakın zamanda netleştiriyoruz."),
  ("Abant'ta drone uçurmak için izin gerekiyor mu?", "Tabiat parkı olduğu için ticari çekimde evet. Başvuruyu önceden yapıyoruz."),
  ("Kartalkaya'daki otelimizi kışın çekebilir misiniz?", "Evet; kar yağışından sonraki ilk açık gün en iyisi."),
  ("Bungalov işletmemiz için ne önerirsiniz?", "Ormanın içindeki konumu havadan, bungalovları ve iç mekânı yerden; mevsime göre ayrı videolar."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ ÇANAKKALE DRONE
"canakkale-drone-cekimi": dict(
 lede="İki kıtayı birleştiren köprü, Boğaz'dan geçen gemiler, Gelibolu'nun tarihî alanı, Truva ve iki ada. Çanakkale'de drone çekimi, Türkiye'nin en özel hava sahalarından birinde yapılıyor.",
 bolum=[
  ("Çanakkale'de uçuş kuralları",
   "<p>Çanakkale Boğazı askerî ve stratejik bir bölge; kıyıdaki askerî alanlar ve şehir merkezindeki havalimanı çevresi drone için izne bağlı. <strong>Gelibolu Yarımadası Tarihî Alanı</strong> ayrı bir yönetimle korunuyor; şehitliklerde ve anıt alanlarında ticari çekim ve drone uçuşu izne bağlı. <strong>Truva</strong> UNESCO Dünya Mirası listesinde ve ören yeri; Bakanlık izni gerekiyor.</p>"
   "<p>Bu yüzden Çanakkale'de her işin takvimi izinle başlıyor. Koordinatı kontrol edip uçuşun mümkün olup olmadığını ve izin süresini teklifte yazıyoruz.</p>"),
  ("Çanakkale'de drone ne çekiyor",
   "<p><strong>Konut ve arsa:</strong> 1915 Çanakkale Köprüsü'nden sonra Lapseki ve Gelibolu yakasında artan projeler ve arsalar; köprüye ve otoyola mesafe havadan.</p>"
   "<p><strong>Turizm:</strong> Assos, Küçükkuyu ve Kaz Dağları eteğindeki butik oteller; Bozcaada'nın bağları ve taş evleri; Gökçeada'nın koyları.</p>"
   "<p><strong>Tarım ve üretici:</strong> Bozcaada ve Ezine çevresinde bağlar ve şaraphaneler, Ayvacık'ta zeytinlikler, Ezine'de peynir üreticileri.</p>"),
  ("Rüzgâr ve ekip",
   "<p>Çanakkale rüzgârlı; Boğaz'da ve adalarda öğleden sonra rüzgâr artıyor. Uçuşları sabah saatlerine koyuyor, ada çekimlerinde feribot saatine göre bir gece konaklamayı öneriyoruz. Çanakkale'de kendi ekibimizle çalışıyoruz.</p>"),
 ],
 sss=[
  ("Gelibolu Yarımadası'nda drone ile çekim yapılabilir mi?", "Tarihî alan yönetiminin izniyle. Şehitliklerde ve anıt alanlarında kurallar sıkı; başvuruyu önceden yapıyoruz."),
  ("Köprüyü havadan çekebilir miyiz?", "Köprü kritik yapı; çevresinde uçuş izne bağlı. Konuma göre izin durumunu kontrol ediyoruz."),
  ("Bozcaada'daki bağımızı çekmek için ne zaman gelmeliyiz?", "Bağların yeşil olduğu yaz ya da hasat dönemi; rüzgârın sakin olduğu sabah saatleri."),
  ("Rüzgârlı havada uçuş yapılabilir mi?", "Belirli bir hıza kadar evet; ama en temiz görüntü için sakin sabahları seçiyoruz."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ ÇORUM DRONE
"corum-drone-cekimi": dict(
 lede="Hititlerin başkenti Hattuşa'nın surları, Çorum ovasının buğday tarlaları ve şehrin büyüyen sanayisi. Çorum'u havadan çekmek, üç bin yıllık bir hikâyeyi bugünle yan yana koymak.",
 bolum=[
  ("Hattuşa ve tarih",
   "<p>Boğazkale'deki Hattuşa, UNESCO Dünya Mirası listesinde; surları, kapıları ve yazılıkaya kutsal alanıyla havadan bakınca ölçeği anlaşılan bir başkent. Ören yeri olduğu için drone ile çekim Kültür ve Turizm Bakanlığı iznine bağlı; turizm ve belgesel işlerinde başvuruyu çekim tarihinden önce yapıyoruz. Alacahöyük de aynı kurallara tabi.</p>"),
  ("Sanayi, tarım ve şehir",
   "<p><strong>Sanayi:</strong> organize sanayi bölgesindeki un, makine, tuğla-kiremit ve plastik üreticileri. Tesisin ölçeği, depo ve sevkiyat alanı havadan; yabancı alıcıya giden filmin açılışı.</p>"
   "<p><strong>Tarım:</strong> ovanın buğday tarlaları, sulama ve büyük tarım işletmeleri. Hasat dönemi, biçerdöverlerin tarlada çalıştığı görüntüler için en iyi zaman.</p>"
   "<p><strong>Konut:</strong> şehrin genişleyen bölgelerinde yeni siteler; şantiye ilerleme ve satış için havadan konum planı.</p>"),
  ("Uçuş planı",
   "<p>Çorum'da sivil havalimanı yok; en yakını Amasya sınırındaki Merzifon. Şehir ve ova SHGM haritasında çoğu konumda daha esnek; yine de askerî alanlar ve kritik tesisler için koordinatı kontrol ediyoruz. Karasal iklimde yaz öğlesi sert ve titreşimli; uçuşları sabah ve akşamüstüne koyuyoruz.</p>"
   "<p>Kurgu ve renk bizde; çekim günlerinde bölgedeki kamera ortağımızla sahadayız.</p>"),
 ],
 sss=[
  ("Hattuşa'da drone ile çekim yapılabilir mi?", "Bakanlık izniyle. Süreç haftalar sürebiliyor; başvuruyu önceden başlatıyoruz."),
  ("Fabrikamızı havadan çekebilir misiniz?", "Evet; kampüsü, depoyu ve yol bağlantısını havadan, üretimi gerekirse içeriden."),
  ("Hasat çekimi için ne zaman gelmeliyiz?", "Temmuz başında; tarih yıla göre değiştiği için yakın zamanda netleştiriyoruz."),
  ("Çorum'da drone için izin gerekiyor mu?", "Çoğu konumda hayır; askerî alanlar, kritik tesisler ve ören yerlerinde evet."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ DENİZLİ DRONE
"denizli-drone-cekimi": dict(
 lede="Pamukkale'nin beyaz basamakları havadan bakınca bir buz şelalesi gibi görünüyor. Ama Denizli'de drone sadece Pamukkale'yi değil, havlu fabrikalarını, traverten ocaklarını ve bağları da çekiyor.",
 bolum=[
  ("Pamukkale ve izin",
   "<p>Pamukkale travertenleri ve Hierapolis, UNESCO Dünya Mirası listesinde ve ören yeri olarak korunuyor. Bu alanda drone ile çekim Kültür ve Turizm Bakanlığı iznine bağlı ve kurallar sıkı. Karahayıt'taki termal oteller ve çevredeki tesisler ise ören yerinin dışında; otel tanıtımlarında havadan planı koordinata göre planlıyoruz.</p>"),
  ("Sanayi ve üretici",
   "<p><strong>Tekstil:</strong> Denizli'nin havlu ve ev tekstili fabrikaları; organize sanayi bölgelerindeki kampüslerin ölçeği ve sevkiyat alanı havadan. İhracat filminin ilk karesi.</p>"
   "<p><strong>Traverten ve mermer:</strong> Kaklık ve Honaz çevresindeki ocaklar; ocağın basamakları, blok kesimi ve iş makineleri. Ocak içi uçuşu iş güvenliği kurallarına göre planlıyoruz.</p>"
   "<p><strong>Bağlar:</strong> Çal ve Güney çevresinin bağları ve şaraphaneleri; hasat dönemi.</p>"),
  ("Uçuş ve ışık",
   "<p>Denizli'nin havalimanı Çardak'ta, şehirden uzakta; şehir içi ve sanayi bölgelerinde uçuş çoğu konumda daha esnek. Yaz öğlesinde travertenlerin beyaz yüzeyi ışığı sert yansıtıyor; havadan çekimi sabaha ve akşamüstüne koyuyoruz. Kurgu ve renk bizde; çekim günlerinde bölgedeki kamera ortağımızla sahadayız.</p>"),
 ],
 sss=[
  ("Pamukkale'yi drone ile çekebilir miyiz?", "Bakanlık izniyle ve kurallar çerçevesinde; süreç uzun olabiliyor, başvuruyu önceden yapıyoruz."),
  ("Termal otelimizi havadan çekebilir misiniz?", "Ören yeri dışında kalan tesislerde çoğu zaman evet; koordinatı kontrol ediyoruz."),
  ("Traverten ocağımızı çekerken nelere dikkat ediyorsunuz?", "İş güvenliği kurallarınıza, patlatma ve yükleme saatlerine; ocak içinde güvenli yükseklikte uçuyoruz."),
  ("Tekstil fabrikamız için drone ne katar?", "Kampüsün ölçeğini ve sevkiyat düzenini tek karede; yabancı alıcıya kapasiteyi gösteren ilk görüntü."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ DİYARBAKIR DRONE
"diyarbakir-drone-cekimi": dict(
 lede="Diyarbakır surları, Çin Seddi'nden sonra dünyanın en uzun surlarından biri olarak anılır; Hevsel Bahçeleri Dicle'ye doğru yeşil bir halı gibi uzanır. Ama şehrin hava sahası da en kısıtlılarından biri.",
 bolum=[
  ("Diyarbakır'da uçuş",
   "<p>Diyarbakır Havalimanı askerî bir hava üssüyle ortak kullanılıyor ve şehrin önemli bir kısmı kontrollü hava sahasında. Sur içi, Hevsel Bahçeleri ve kalenin çevresi UNESCO Dünya Mirası alanı; burada çekim ayrıca izne bağlı. Bu yüzden Diyarbakır'da havadan çekimin ilk adımı her zaman koordinat ve izin kontrolü. Temmuz 2026 SHGM talimatına göre haritada yeşil görünen bölgelerde ayrı izne gerek yok; şehir dışındaki tarım alanları ve bazı ilçeler bu kapsamda.</p>"),
  ("Diyarbakır'da drone ne çekiyor",
   "<p><strong>Şantiye ve konut:</strong> Kayapınar ve Diclekent'teki yeni siteler; aylık şantiye ilerleme ve satış öncesi konum planı.</p>"
   "<p><strong>Tarım:</strong> Dicle ovasının tarlaları, karpuz ve pamuk; sulama düzeni ve arazi sınırları. Diyarbakır karpuzu ve hasadı, havadan da yerden de güçlü bir görüntü.</p>"
   "<p><strong>Tarih ve turizm:</strong> surlar, On Gözlü Köprü ve Dicle vadisi; izin gerektiren alanlarda başvuruyu önceden yapıyoruz.</p>"),
  ("Sıcak ve ışık",
   "<p>Diyarbakır yazın çok sıcak; öğle saatinde hava titreşiyor ve bataryalar hızla ısınıyor. Uçuşları gün doğumundan sonraki ilk saatlere ve akşamüstüne koyuyoruz; bazalt surların koyu rengi, alçak güneşte en güzel dokusunu gösteriyor. Kurgu ve renk bizde; çekim günlerinde bölgedeki kamera ortağımızla sahadayız.</p>"),
 ],
 sss=[
  ("Sur içinde drone ile çekim yapılabilir mi?", "UNESCO alanı ve kontrollü hava sahası nedeniyle izin gerekiyor. Başvuruyu önceden yapıyor, süresini takvime koyuyoruz."),
  ("Kayapınar'daki şantiyemizi havadan çekebilir misiniz?", "Koordinata bağlı; havalimanına yakınlık nedeniyle izin gerekebilir. Önceden kontrol ediyoruz."),
  ("Tarım arazimizi havadan çekmek mümkün mü?", "Şehir dışındaki arazilerde çoğu zaman evet; sınır ve sulama düzenini tek karede gösteriyoruz."),
  ("Yazın uçuş hangi saatte yapılmalı?", "Gün doğumundan sonraki ilk saatlerde ve akşamüstü."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ DÜZCE DRONE
"duzce-drone-cekimi": dict(
 lede="Akçakoca'nın kıyısı, Efteni Gölü'nün sazlıkları, Güzeldere'nin şelalesi ve fındık bahçelerinin arasından geçen otoyol. Düzce küçük ama havadan bakınca yemyeşil bir il.",
 bolum=[
  ("Düzce'de drone ne çekiyor",
   "<p><strong>Sanayi ve lojistik:</strong> İstanbul–Ankara otoyolunun üzerindeki konumuyla Düzce'nin organize sanayi bölgeleri büyüyor; tesislerin ölçeği ve otoyola bağlantısı havadan.</p>"
   "<p><strong>Konut ve şantiye:</strong> 1999 depreminden sonra yeniden kurulan şehirde yeni projeler; aylık şantiye ilerleme ve satış öncesi konum planı.</p>"
   "<p><strong>Fındık ve tarım:</strong> fındık bahçeleri ve tarım arazileri; arazi sınırı ve yol bağlantısı.</p>"
   "<p><strong>Turizm:</strong> Akçakoca'nın sahil otelleri ve yazlık siteleri, Güzeldere Şelalesi ve çevresindeki doğa tesisleri, Efteni Gölü'nün kuş gözlem alanı.</p>"),
  ("Uçuş ve koruma alanları",
   "<p>Düzce'de sivil havalimanı yok; ilin büyük kısmı SHGM haritasında daha esnek. Efteni Gölü bir kuş alanı; kuşları rahatsız edecek alçak uçuştan kaçınıyor, göç döneminde uçmuyoruz. Koruma altındaki alanlarda ticari çekim için izin alıyoruz.</p>"),
  ("Hava ve ekip",
   "<p>Karadeniz ikliminde hava gün içinde değişebiliyor; deniz ve şelale çekimleri için açık bir saat bekliyor, yedek gün koyuyoruz. Düzce'de kendi ekibimizle çalışıyoruz; Akçakoca ile şehir merkezini aynı güne koyabiliyoruz.</p>"),
 ],
 sss=[
  ("Akçakoca'daki otelimizi havadan çekebilir misiniz?", "Evet; sahil ve otelin denizle ilişkisini havadan, sezon öncesi misafir yokken çekiyoruz."),
  ("Fındık bahçesi satışında drone ne işe yarar?", "Bahçenin sınırını, eğimini ve yol bağlantısını tek karede gösteriyor."),
  ("Efteni Gölü'nde drone uçurabilir miyiz?", "Kuş alanı olduğu için dikkatli ve izinli; göç döneminde uçmuyoruz."),
  ("Hava kapalıysa çekim ne olur?", "Yedek gün koyuyoruz; Karadeniz'de bu sık oluyor."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ EDİRNE DRONE
"edirne-drone-cekimi": dict(
 lede="Selimiye'nin dört minaresi, Meriç ve Tunca'nın kıvrımları, Kırkpınar'ın er meydanı. Edirne havadan bakınca bir sınır şehrinin bütün katmanlarını aynı karede gösteriyor.",
 bolum=[
  ("Sınır şehrinde uçuş",
   "<p>Edirne Bulgaristan ve Yunanistan sınırında; sınıra yakın bölgeler, sınır kapıları ve askerî alanlar drone için kısıtlı. Şehrin merkezinde de koordinata göre durum değişiyor. Temmuz 2026 SHGM talimatıyla haritada yeşil görünen yerlerde ayrı izin gerekmiyor; diğer yerlerde başvuruyu çekim tarihinden önce yapıyoruz.</p>"
   "<p><strong>Selimiye Camii</strong> UNESCO Dünya Mirası listesinde; ibadet saatlerine ve çevredeki ziyaretçilere saygı göstererek, izinli olarak ve uygun yükseklikte çekiyoruz.</p>"),
  ("Edirne'de drone ne çekiyor",
   "<p><strong>Kırkpınar:</strong> her yaz Sarayiçi'nde yapılan yağlı güreşler; kalabalığın üzerinde uçmuyor, alanın kenarından ve organizasyonun izniyle çekiyoruz.</p>"
   "<p><strong>Nehirler ve köprüler:</strong> Meriç ve Tunca üzerindeki tarihî köprüler ve nehir kıyıları; sabah sisinde ya da gün batımında.</p>"
   "<p><strong>Tarım:</strong> Trakya'nın ayçiçeği ve çeltik tarlaları; yaz ortasında ayçiçeğinin sarısı havadan çok güçlü.</p>"
   "<p><strong>Enez ve Saros:</strong> kıyı ve yazlık siteler; deniz ve kumsal.</p>"),
  ("Işık ve ekip",
   "<p>Edirne'de nehir kıyısında sabahları sis sık; sisin içinden yükselen minareler etkileyici ama tesis ve konut tanıtımında sisin kalkmasını bekliyoruz. Kurgu ve renk bizde; çekim günlerinde Trakya'daki kamera ortağımızla sahadayız.</p>"),
 ],
 sss=[
  ("Selimiye'yi drone ile çekebilir miyiz?", "İzinli olarak ve kurallara uyarak; ibadet saatlerinin dışında, uygun yükseklikte."),
  ("Kırkpınar'da drone kullanılabilir mi?", "Kalabalık üzerinde uçulmuyor; organizasyonun izniyle alanın kenarından çekiyoruz."),
  ("Ayçiçeği tarlası için ne zaman gelmeliyiz?", "Temmuz ortası; çiçekler tam açıkken."),
  ("Sınıra yakın arazimizi havadan çekebilir misiniz?", "Sınır bölgesinde kısıtlar sıkı; koordinatı kontrol edip mümkün olup olmadığını önceden söylüyoruz."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ ELAZIĞ DRONE
"elazig-drone-cekimi": dict(
 lede="Keban Barajı'nın göl yüzeyi, Hazar Gölü'nün mavisi ve Harput'un şehre tepeden bakan kalesi. Elazığ'ı havadan çekmek, iki büyük suyun arasında kurulmuş bir şehri göstermek.",
 bolum=[
  ("Su, baraj ve kurallar",
   "<p>Keban Barajı'nın gövdesi ve hidroelektrik santrali kritik tesis; çevresinde izinsiz uçuş yapılmıyor. Baraj gölünün kıyısındaki köyler, tesisler ve arazilerde ise koordinata göre uçuş planlıyoruz. Elazığ Havalimanı'nın çevresi de kontrollü hava sahası.</p>"
   "<p><strong>Hazar Gölü:</strong> Sivrice'de, dağlarla çevrili göl; yazlık evler, kamp alanları ve göl kıyısı tesisler. Göl yüzeyi sabahları ayna gibi; havadan en güzel saat.</p>"),
  ("Elazığ'da drone ne çekiyor",
   "<p><strong>Şantiye ve yeni konut:</strong> 2020 ve 2023 depremlerinden sonra yükselen yeni konut alanları; aylık şantiye ilerleme ve teslim filmi.</p>"
   "<p><strong>Harput:</strong> kale, tarihî camiler ve şehre bakan yamaç; turizm ve tanıtım işleri.</p>"
   "<p><strong>Sanayi ve maden:</strong> organize sanayi bölgesindeki tesisler ve ilin maden işletmeleri; ocağın ve tesisin ölçeği.</p>"
   "<p><strong>Bağlar:</strong> Öküzgözü ve Boğazkere üzümlerinin bağları; hasat dönemi.</p>"),
  ("Işık ve ekip",
   "<p>Elazığ yazın sıcak ve kuru, kışın soğuk. Göl ve baraj çekimlerinde sabah ışığını, şehir ve Harput çekimlerinde akşamüstünü seçiyoruz. Kurgu ve renk bizde; çekim günlerinde bölgedeki kamera ortağımızla sahadayız.</p>"),
 ],
 sss=[
  ("Keban Barajı'nı havadan çekebilir miyiz?", "Baraj gövdesi ve santral kritik tesis; izinsiz uçmuyoruz. Göl kıyısındaki alanlarda koordinata göre planlıyoruz."),
  ("Hazar Gölü'ndeki tesisimiz için en iyi saat ne?", "Sabah; göl yüzeyi durgun ve parlak."),
  ("Şantiye ilerleme çekimi yapıyor musunuz?", "Evet; her ay aynı noktadan ve aynı yükseklikten çekip ilerlemeyi yan yana gösteriyoruz."),
  ("Bağ çekimi için ne zaman gelmeliyiz?", "Eylül hasat döneminde; bağlar en canlı hâlinde."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ ERZURUM DRONE
"erzurum-drone-cekimi": dict(
 lede="Palandöken'in pistleri, Tortum Şelalesi'nin kayalıklardan dökülen suyu ve kışın bembeyaz kalan bir şehir. Erzurum'da drone çekimi çoğu zaman eksi derecelerde yapılıyor.",
 bolum=[
  ("Soğukta uçmak",
   "<p>Erzurum Türkiye'nin en soğuk şehirlerinden biri; kışın eksi yirminin altına inen sabahlar oluyor. Soğukta drone bataryaları hızla tükeniyor; bataryaları sıcak tutuyor, uçuşları kısa tutuyor ve yedek batarya ile çalışıyoruz. Kar sonrası açık bir gün, şehir ve dağ için en temiz görüntüyü veriyor.</p>"
   "<p>Erzurum Havalimanı askerî üsle ortak kullanılıyor; şehrin önemli bir kısmında uçuş izne bağlı. Koordinatı her çekimde kontrol ediyoruz.</p>"),
  ("Erzurum'da drone ne çekiyor",
   "<p><strong>Palandöken ve kayak turizmi:</strong> pistler, oteller ve teleferik hattı; otel tanıtımının açılışı. Kayakçıları takip eden planlar için pist işletmesinin izniyle.</p>"
   "<p><strong>Tortum ve Uzundere:</strong> Tortum Şelalesi, Tortum Gölü ve vadideki köyler; ilkbaharda şelale en gür.</p>"
   "<p><strong>Şehir ve tarih:</strong> Çifte Minareli Medrese ve tarihî merkez; kar altında şehrin silueti.</p>"
   "<p><strong>Şantiye ve konut:</strong> yeni konut alanlarında aylık ilerleme çekimi; kış aylarında şantiyenin durduğu dönem de takvimde.</p>"),
  ("Ekip",
   "<p>Kurgu ve renk bizde; çekim günlerinde bölgedeki kamera ortağımızla sahadayız. Kış çekimlerinde yol ve hava koşullarına göre tarihi esnek tutuyoruz.</p>"),
 ],
 sss=[
  ("Soğukta drone uçabiliyor mu?", "Evet ama bataryalar hızlı tükeniyor. Bataryaları sıcak tutuyor, uçuşları kısa ve planlı yapıyoruz."),
  ("Palandöken'deki otelimizi havadan çekebilir misiniz?", "Evet; kar sonrası açık bir gün ve pist işletmesinin izniyle."),
  ("Tortum Şelalesi'ni ne zaman çekmeliyiz?", "İlkbaharda, kar suları eridiğinde; şelale en gür hâlinde."),
  ("Erzurum merkezinde drone için izin gerekiyor mu?", "Havalimanı ve askerî alanlar nedeniyle çoğu konumda evet. Koordinatı önceden kontrol ediyoruz."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ GAZİANTEP DRONE
"gaziantep-drone-cekimi": dict(
 lede="Gaziantep'in organize sanayi bölgeleri havadan bakınca bir şehir kadar büyük. Şehrin yanı başında fıstık bahçeleri, biraz ötede Fırat'ın kıyısında Zeugma ve Rumkale.",
 bolum=[
  ("Sanayi: ölçeği göstermek",
   "<p>Gaziantep, makine halısı, tekstil, gıda ve plastikte Türkiye'nin en büyük ihracatçı şehirlerinden biri; organize sanayi bölgelerinde yüzlerce büyük tesis var. Yabancı alıcıya giden tanıtım filminin ilk saniyeleri çoğu zaman havadan: kampüsün büyüklüğü, depo ve sevkiyat alanı, otoyola ve lojistik merkezlere bağlantı. Fabrika içinde ise hat boyunca FPV planı.</p>"),
  ("Fıstık, Fırat ve tarih",
   "<p><strong>Fıstık bahçeleri:</strong> şehrin çevresindeki bahçeler; Ağustos–Eylül hasadında. Üretici ve ihracatçılar için bahçeden fabrikaya uzanan filmin açılışı.</p>"
   "<p><strong>Zeugma ve Rumkale:</strong> Fırat kıyısında antik kent ve nehre bakan kale kalıntıları. Ören yerlerinde drone ile çekim Bakanlık iznine bağlı; başvuruyu önceden yapıyoruz.</p>"
   "<p><strong>Şantiye ve konut:</strong> Şehitkamil'de yükselen yeni siteler; aylık ilerleme ve satış öncesi konum planı.</p>"),
  ("Uçuş ve ışık",
   "<p>Gaziantep Havalimanı Oğuzeli'nde, şehrin güneydoğusunda; çevresi kontrollü hava sahası. Suriye sınırına yakın bölgeler ve askerî alanlar da kısıtlı. Her çekimde koordinatı haritada kontrol ediyoruz. Yaz öğlesinde ışık çok sert; uçuşları sabaha ve akşamüstüne koyuyoruz.</p>"
   "<p>Görüntü yönetimi ve kurgu bizim ekipte; sahada Gaziantep'teki kamera ortağımızla birlikteyiz.</p>"),
  ("Kalabalık bir şehirde yeni konut",
   "<p>Gaziantep hem genç hem hızla büyüyen bir şehir; Şehitkamil ve İbrahimli yönünde her yıl yeni siteler yükseliyor. Bu projelerde alıcı, sitenin şehre göre nerede durduğunu, ana yollara ve hastanelere ne kadar uzak olduğunu soruyor. Havadan bir konum planı bu soruyu tek seferde cevaplıyor; satış ofisindeki ekranda da, ilan sitesinde de ilk açılan görüntü oluyor.</p>"),
 ],
 sss=[
  ("Fabrikamızın hem dışını hem içini çekebilir misiniz?", "Evet; kampüsü havadan, üretim hattını FPV ile içeriden, iş güvenliği kurallarınıza uyarak."),
  ("Fıstık bahçesi için ne zaman gelmeliyiz?", "Ağustos sonu–Eylül hasat döneminde."),
  ("Zeugma'da drone uçurmak mümkün mü?", "Bakanlık izniyle. Süreç uzun olabiliyor; başvuruyu önceden başlatıyoruz."),
  ("Oğuzeli yakınındaki arazimizi çekebilir misiniz?", "Havalimanına yakınlık nedeniyle izin gerekebilir; koordinatı kontrol edip önceden söylüyoruz."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ HATAY DRONE
"hatay-drone-cekimi": dict(
 lede="Hatay'da bugün havadan çekilen görüntülerin çoğu bir yeniden doğuşu kayda geçiriyor: yükselen yeni binalar, açılan yollar, kurulan mahalleler. Drone, şantiyenin ilerlemesini en dürüst gösteren araç.",
 bolum=[
  ("Yeniden yapılanmayı kayda geçirmek",
   "<p>Şubat 2023 depremlerinden sonra Antakya, Defne, İskenderun ve diğer ilçelerde büyük bir yeniden yapılanma sürüyor. Müteahhitler, kurumlar ve kooperatifler için şantiyeyi her ay aynı noktadan ve aynı yükseklikten çekmek, ilerlemeyi belgeliyor; iş sahibine, hak sahibine ve alıcıya somut bir kanıt sunuyor. Proje bitiminde bu görüntüler, temelden teslime uzanan bir zaman çizelgesine dönüşüyor.</p>"),
  ("Uçuş kuralları",
   "<p>Hatay'da havalimanı çevresi, Suriye sınırına yakın bölgeler ve askerî alanlar drone için kısıtlı. İskenderun'daki liman ve büyük demir-çelik tesisleri kritik yapı sayılıyor; çevrelerinde izinsiz uçmuyoruz. Temmuz 2026 SHGM talimatına göre haritada yeşil görünen yerlerde ayrı izne gerek yok; her koordinatı çekimden önce kontrol ediyoruz.</p>"),
  ("Hatay'da drone ne çekiyor",
   "<p><strong>Şantiye ve yeni konut alanları:</strong> aylık ilerleme ve teslim filmi.</p>"
   "<p><strong>Tarım:</strong> Amik ovasının tarlaları ve sera bölgeleri; sulama ve arazi düzeni.</p>"
   "<p><strong>Kıyı:</strong> Samandağ ve Arsuz sahili; sahil tesisleri ve yazlık alanlar.</p>"
   "<p>Hatay'ın yaz nemi öğleden sonra görüntüyü puslandırıyor; havadan çekimi sabahın ilk saatlerine alıyoruz. Sahada bölgedeki kamera ortağımız, kurguda biz varız.</p>"),
  ("Hak sahiplerine güven",
   "<p>Yeniden yapılanan bir şehirde şantiye görüntüsü sadece bir tanıtım malzemesi değil, aynı zamanda bir güven belgesi. Kooperatif üyeleri ve hak sahipleri çoğu zaman şehir dışında yaşıyor ve evlerinin ne aşamada olduğunu merak ediyor. Her ay paylaşılan kısa bir havadan video, binaların yükseldiğini kendi gözleriyle görmelerini sağlıyor; iş sahibine gelen soru sayısını da azaltıyor.</p>"),
 ],
 sss=[
  ("Şantiye ilerleme çekimi ne sıklıkta yapılmalı?", "Ayda bir genellikle yeterli; kritik aşamalarda ek çekim yapılabiliyor."),
  ("İskenderun'daki tesisimizi havadan çekebilir misiniz?", "Liman ve sanayi tesislerinin çevresi izne bağlı; koordinatı kontrol edip önceden söylüyoruz."),
  ("Hak sahiplerine ilerlemeyi göstermek için ne önerirsiniz?", "Her ay aynı noktadan çekilen görüntülerden kısa bir video; ilerleme yan yana görülüyor."),
  ("Amik ovasındaki arazimizi çekebilir misiniz?", "Koordinata göre çoğu zaman evet; sınır ve sulama düzenini havadan gösteriyoruz."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ ISPARTA DRONE
"isparta-drone-cekimi": dict(
 lede="Mayıs sonunda Isparta'nın gül bahçeleri pembeye, Temmuz'da Kuyucak'ın tarlaları mora dönüyor. Eğirdir Gölü'nün mavisi ve Davraz'ın karı da aynı ilin içinde.",
 bolum=[
  ("Renk takvimi",
   "<p><strong>Gül:</strong> Mayıs sonu ile Haziran ortası arasında gül bahçeleri çiçekte; hasat sabah çok erken başlıyor. Gül yağı ve kozmetik üreticileri için bahçeden imbiğe uzanan filmin açılışı havadan.</p>"
   "<p><strong>Lavanta:</strong> Temmuz'da Kuyucak ve çevresindeki tarlalar mor; sıra sıra lavanta havadan geometrik bir desen gibi görünüyor. Bu dönem ziyaretçi de çok; kalabalık üzerinde uçmuyoruz.</p>"
   "<p><strong>Kış:</strong> Davraz Kayak Merkezi ve karlı dağlar; otel ve tesis tanıtımı.</p>"),
  ("Eğirdir Gölü",
   "<p>Türkiye'nin büyük tatlı su göllerinden biri olan Eğirdir, yarımada üzerindeki kasabası ve Can Ada'sıyla havadan çok güçlü bir kare. Göl kıyısındaki pansiyonlar, oteller ve arsalar için sabah ışığında, göl yüzeyi durgunken çekiyoruz. Göl çevresindeki askerî alanlar izne bağlı; koordinatı önceden kontrol ediyoruz.</p>"),
  ("Uçuş ve ekip",
   "<p>Isparta'nın havalimanı Keçiborlu'da, şehrin kuzeyinde; şehir merkezi ve çevredeki tarım alanları çoğu konumda daha esnek. Temmuz 2026 SHGM talimatına göre haritada yeşil görünen yerlerde ayrı izne gerek yok. Kurgu ve renk bizde; çekim günlerinde bölgedeki kamera ortağımızla sahadayız.</p>"),
 ],
 sss=[
  ("Gül hasadını havadan çekmek için ne zaman gelmeliyiz?", "Mayıs sonu–Haziran başı, sabah çok erken; hasat güneş yükselmeden yapılıyor."),
  ("Lavanta tarlası için en iyi zaman?", "Temmuz başı ile ortası; gün batımında renk en derin."),
  ("Eğirdir'deki pansiyonumuzu havadan çekebilir misiniz?", "Evet; sabah ışığında göl ve kasabayla birlikte."),
  ("Davraz'daki tesisimizi kışın çekebilir misiniz?", "Evet; kar sonrası açık bir gün en iyisi."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ İSTANBUL DRONE
"istanbul-drone-cekimi": dict(
 lede="İstanbul'u havadan çekmek isteyen herkesin karşılaştığı ilk gerçek: şehrin neredeyse tamamı kontrollü hava sahası. İstanbul Havalimanı, Sabiha Gökçen, Boğaz ve tarihî yarımada; her uçuş bir izin süreciyle başlıyor.",
 bolum=[
  ("İstanbul'da uçuş kuralları",
   "<p>İstanbul'un iki büyük havalimanı, Atatürk Havalimanı'nın sahası, Boğaz'daki askerî ve stratejik alanlar, tarihî yarımada, saraylar ve resmî binalar drone için sıkı kurallara bağlı. Şehrin büyük kısmında uçuş ya izin gerektiriyor ya da hiç mümkün değil. Temmuz 2026'da yenilenen SHGM talimatıyla yeşil bölgelerde ayrı izin gerekmiyor; ama İstanbul'da bu bölgeler çoğunlukla şehrin kuzey ve doğu ucunda.</p>"
   "<p>Bu yüzden İstanbul'da drone işinin takvimi koordinatla başlıyor: uçuşun mümkün olup olmadığı, izin gerekip gerekmediği, sürenin ne kadar olduğu. Bunları teklif aşamasında yazıyoruz.</p>"),
  ("İstanbul'da drone nerede işe yarıyor",
   "<p><strong>Şantiye ve proje:</strong> kentsel dönüşüm ve büyük konut projelerinde aylık ilerleme; izni bir kez alınan noktadan düzenli çekim.</p>"
   "<p><strong>Sanayi ve lojistik:</strong> Tuzla, Hadımköy, Esenyurt ve Silivri tarafındaki tesisler ve lojistik merkezleri; koordinata göre.</p>"
   "<p><strong>Kuzey ormanları ve Karadeniz kıyısı:</strong> Şile, Kilyos, Riva ve Belgrad Ormanı çevresi; villa, otel ve doğa çekimleri.</p>"
   "<p><strong>Etkinlik:</strong> açık hava etkinlikleri ve konserler; kalabalık üzerinde uçmuyor, alanın kenarından ve izinli olarak çekiyoruz.</p>"),
  ("İzin çıkmazsa",
   "<p>İzin çıkmayan ya da süresi takvime uymayan işlerde, aynı anlatımı verebilecek alternatifleri öneriyoruz: yüksek bir binanın terasından çekim, iç mekânda FPV ile kesintisiz plan ya da 3D görselleştirme. İstanbul'da kendi ekibimizle çalışıyoruz; Bursa'dan yaklaşık iki saatte geliyoruz.</p>"),
 ],
 sss=[
  ("İstanbul'da drone ile çekim yapılabilir mi?", "Konuma bağlı; şehrin büyük kısmında izin gerekiyor, bazı yerlerde uçuş hiç mümkün değil. Koordinatı kontrol edip önceden söylüyoruz."),
  ("Boğaz'ı havadan çekebilir miyiz?", "Boğaz çevresi sıkı kısıtlı; izin süreci uzun ve sonuç garantili değil. Alternatif yöntemler de öneriyoruz."),
  ("Şantiyemizi her ay çekebilir misiniz?", "Evet; izni alınan noktadan her ay aynı açıdan çekiyoruz."),
  ("İzin çıkmazsa ne yapıyoruz?", "Teras çekimi, iç mekânda FPV ya da 3D görselleştirme gibi alternatiflerle aynı anlatımı kuruyoruz."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ İZMİR DRONE
"izmir-drone-cekimi": dict(
 lede="Körfezin kıvrımı, Kordon'un gün batımı, Çeşme'nin koyları ve Urla'nın bağları. İzmir havadan Türkiye'nin en fotojenik şehirlerinden biri; ama körfezin iki yanında iki büyük kısıt var.",
 bolum=[
  ("İzmir'de uçuş",
   "<p>Gaziemir'deki Adnan Menderes Havalimanı ve Çiğli'deki askerî hava üssü, körfezin güney ve kuzey yakasının önemli bir kısmını kontrollü hava sahasına sokuyor. Aliağa'daki rafineri ve sanayi tesisleri, limanlar ve askerî alanlar da kritik yapı. Temmuz 2026 SHGM talimatına göre haritada yeşil görünen yerlerde ayrı izne gerek yok; Urla, Çeşme, Seferihisar ve Karaburun'un büyük kısmı daha esnek. Her çekimde koordinatı kontrol ediyoruz.</p>"),
  ("İzmir'de drone ne çekiyor",
   "<p><strong>Villa ve yazlık:</strong> Çeşme, Alaçatı, Urla ve Seferihisar'da villa ve site projeleri; denize mesafe, havuz ve manzara.</p>"
   "<p><strong>Bağ ve zeytin:</strong> Urla bağ yolunun şaraphaneleri, Karaburun ve Seferihisar'ın zeytinlikleri; hasat dönemi.</p>"
   "<p><strong>Sanayi:</strong> Kemalpaşa, Torbalı ve Atatürk OSB'deki tesisler; kampüsün ölçeği ve liman bağlantısı.</p>"
   "<p><strong>Şantiye:</strong> Bayraklı ve Bornova'daki dönüşüm projeleri; havalimanı ve hava üssüne yakınlık nedeniyle koordinata göre izinli.</p>"),
  ("Rüzgâr ve ışık",
   "<p>İzmir'de yaz öğleden sonraları imbat esiyor; Alaçatı ve Çeşme ise rüzgârıyla bilinen yerler. Drone uçuşlarını rüzgârın sakin olduğu sabah saatlerine, gün batımı planlarını rüzgâr hafiflediğinde akşama koyuyoruz. Kurgu ve renk bizde; çekim günlerinde İzmir'deki kamera ortağımızla sahadayız.</p>"),
 ],
 sss=[
  ("Alaçatı'da rüzgârlı havada drone uçar mı?", "Belirli bir hıza kadar evet; ama en temiz görüntü için sabahın sakin saatlerini seçiyoruz."),
  ("Bayraklı'daki şantiyemizi havadan çekebilir misiniz?", "Havalimanına ve hava üssüne yakınlık nedeniyle izin gerekebilir; koordinatı kontrol edip önceden söylüyoruz."),
  ("Urla'daki bağımızı ne zaman çekmeliyiz?", "Bağlar yeşilken yaz başında ya da hasatta, Eylül'de."),
  ("Kordon'u havadan çekebilir miyiz?", "Konuma göre izin gerekiyor; uçuşun mümkün olup olmadığını önceden kontrol ediyoruz."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ KAHRAMANMARAŞ DRONE
"kahramanmaras-drone-cekimi": dict(
 lede="Kahramanmaraş'ta bugün havadan bakınca en çok görünen şey vinçler: yeni konut alanları, yeni çarşı, yeni yollar. Şehir yeniden kuruluyor ve drone bunu ay ay kayda geçiriyor.",
 bolum=[
  ("Şantiye ve yeniden yapılanma",
   "<p>Şubat 2023 depremlerinin merkezi olan Kahramanmaraş'ta yeniden yapılanma sürüyor. Müteahhitler ve kurumlar için aylık şantiye ilerleme çekimi, işin ilerleyişini iş sahibine ve hak sahiplerine somut olarak gösteriyor. İlk uçuşta noktaları ve yükseklikleri kaydediyor, her ay aynı yerden çekip ilerlemeyi yan yana koyuyoruz; proje bitiminde bu görüntüler teslim filmine dönüşüyor.</p>"),
  ("Kahramanmaraş'ta drone ne çekiyor",
   "<p><strong>Sanayi:</strong> tekstil ve iplik fabrikaları; organize sanayi bölgesindeki kampüslerin ölçeği ve sevkiyat alanı.</p>"
   "<p><strong>Ahır Dağı ve yaylalar:</strong> şehre tepeden bakan dağ ve yayla evleri; yazın yeşil, kışın karlı.</p>"
   "<p><strong>Barajlar ve göller:</strong> Menzelet ve diğer baraj gölleri; göl yüzeyi ve çevredeki tesisler. Baraj gövdeleri kritik tesis; izinsiz uçmuyoruz.</p>"
   "<p><strong>Tarım:</strong> ovadaki tarlalar ve bahçeler; arazi sınırı ve sulama.</p>"),
  ("Uçuş ve ışık",
   "<p>Kahramanmaraş Havalimanı şehre yakın; çevresi kontrollü hava sahası. Her çekimde koordinatı kontrol ediyor, gerekiyorsa izni önceden alıyoruz. Yaz sıcağında uçuşları sabaha ve akşamüstüne koyuyoruz. Çekimde bölgedeki kamera ortağımızla birlikteyiz; kurgu ve renk düzenlemesi bizim işimiz.</p>"),
  ("Dondurmanın şehri, tekstilin şehri",
   "<p>Kahramanmaraş'ın adı dondurmasıyla anılıyor ama şehrin ekonomisinin belkemiği tekstil: iplik, dokuma ve konfeksiyon fabrikaları. Bu fabrikaların büyük kısmı ihracat yapıyor ve yeniden yapılanma döneminde yeni tesisler de açılıyor. Yeni bir tesisin açılışını, ilk üretim gününü ya da genişleme yatırımını havadan kayda geçirmek, firmanın hikâyesinin bir parçası.</p>"),
 ],
 sss=[
  ("Şantiye ilerleme çekimini her ay aynı açıdan alıyor musunuz?", "Evet; noktaları ve yükseklikleri kaydedip her ay aynı yerden çekiyoruz."),
  ("Tekstil fabrikamızı havadan çekebilir misiniz?", "Evet; kampüsü ve sevkiyat alanını havadan, hattı gerekirse içeriden."),
  ("Havalimanına yakın şantiyemiz için izin gerekir mi?", "Büyük olasılıkla evet; koordinatı kontrol edip izni önceden alıyoruz."),
  ("Ahır Dağı'ndaki yayla evimizi çekebilir misiniz?", "Evet; yazın yeşil, kışın karlı iki ayrı görüntüyle."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ KAYSERİ DRONE
"kayseri-drone-cekimi": dict(
 lede="Erciyes'in karlı zirvesi, organize sanayi bölgesinin uçsuz bucaksız fabrikaları ve Sultan Sazlığı'nın kuşları. Kayseri'de drone, dağ, sanayi ve doğa arasında gidip geliyor.",
 bolum=[
  ("Sanayi: mobilya ve metal",
   "<p>Kayseri Organize Sanayi Bölgesi Türkiye'nin en büyüklerinden biri; mobilya, yatak, metal ve makine üreticileri burada. Fabrikanın ölçeğini, depo ve sevkiyat düzenini havadan; üretim hattını FPV ile içeriden çekiyoruz. Yabancı alıcıya, bayiye ve fuara giden filmin ilk saniyeleri.</p>"),
  ("Erciyes ve doğa",
   "<p><strong>Erciyes Kayak Merkezi:</strong> pistler, oteller ve teleferik; kar sonrası açık bir gün otel tanıtımının en güçlü görüntüsü.</p>"
   "<p><strong>Sultan Sazlığı:</strong> Yahyalı ve Develi arasında, Türkiye'nin önemli kuş alanlarından biri. Koruma altında; ticari çekim için izin alıyor, kuşları rahatsız edecek alçak uçuştan kaçınıyor, göç döneminde uçmuyoruz.</p>"
   "<p><strong>Kapadokya'ya yakınlık:</strong> İncesu ve Ürgüp yönü; balon uçuş alanlarına yakın bölgelerde sabah saatlerinde drone kullanılmıyor.</p>"),
  ("Uçuş planı",
   "<p>Kayseri Havalimanı askerî bir üsle ortak kullanılıyor ve şehrin kuzeyinde; Kocasinan'ın kuzeyi ve Erkilet çevresinde uçuş izne bağlı. Temmuz 2026 SHGM talimatına göre haritada yeşil görünen yerlerde ayrı izne gerek yok; organize sanayi bölgesinde ve Talas tarafında koordinata göre planlıyoruz. Çekimi Kayseri'deki kamera ortağımızla yapıyor, kurguyu kendimiz tamamlıyoruz.</p>"),
  ("Yatırımı göstermek",
   "<p>Kayseri'de bir fabrikanın tanıtım filmi çoğu zaman bir yatırım hikâyesi anlatıyor: yeni bir hal, genişleyen bir depo, ikinci bir üretim tesisi. Aynı noktadan farklı yıllarda çekilmiş havadan görüntüler bu büyümeyi en net gösteren malzeme. İlk çekimde koordinatları kaydediyor, sonraki yıllarda aynı karelerle büyümeyi yan yana koyuyoruz.</p>"),
 ],
 sss=[
  ("OSB'deki fabrikamızı havadan çekebilir misiniz?", "Çoğu konumda evet; koordinatı kontrol edip önceden söylüyoruz. İçeride FPV ile hat boyunca kesintisiz plan da çekiyoruz."),
  ("Erciyes'teki otelimizi kışın çekebilir misiniz?", "Evet; kar yağışından sonraki ilk açık gün en iyisi."),
  ("Sultan Sazlığı'nda drone uçurabilir miyiz?", "Koruma alanı olduğu için izin gerekiyor; göç döneminde uçmuyoruz."),
  ("Erkilet yakınındaki şantiyemiz için izin gerekir mi?", "Büyük olasılıkla evet; koordinatı kontrol edip izni önceden alıyoruz."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ KÜTAHYA DRONE
"kutahya-drone-cekimi": dict(
 lede="Aizanoi'nin Zeus Tapınağı, Seyitömer'in dev açık ocakları, Yoncalı'nın termal tesisleri ve şehrin tepesindeki kale. Kütahya havadan bakınca hem çok eski hem çok endüstriyel.",
 bolum=[
  ("Maden ve sanayi",
   "<p>Kütahya, linyit ve bor gibi madenleriyle Türkiye'nin önemli maden illerinden biri; Seyitömer ve Tavşanlı çevresindeki açık ocaklar havadan bakınca dev basamaklı vadiler gibi görünüyor. Maden işletmeleri için ocağın ölçeğini, iş makinelerinin hareketini ve rehabilitasyon alanlarını havadan çekiyoruz; ocak içi uçuşu işletmenin iş güvenliği kurallarına göre, patlatma ve yükleme saatleri dışında planlıyoruz.</p>"
   "<p>Çini ve porselen üreticileri, organize sanayi bölgesindeki tesisler için kampüsün ölçeği ve sevkiyat alanı.</p>"),
  ("Tarih ve termal",
   "<p><strong>Aizanoi:</strong> Çavdarhisar'da, Zeus Tapınağı ve antik tiyatrosuyla bir ören yeri; drone ile çekim Bakanlık iznine bağlı.</p>"
   "<p><strong>Termal tesisler:</strong> Yoncalı, Ilıca ve Simav'daki oteller ve siteler; havuzlar ve çevre. Kışın havuzdan yükselen buhar havadan da etkileyici.</p>"
   "<p><strong>Kütahya Kalesi ve şehir:</strong> şehre tepeden bakan kale; akşam ışığında şehrin silueti.</p>"),
  ("Uçuş ve ekip",
   "<p>Zafer Havalimanı Altıntaş'ta, şehrin güneyinde; şehir merkezi ve maden bölgeleri çoğu konumda daha esnek. Termik santraller ve enerji tesisleri ise kritik yapı; çevrelerinde izinsiz uçmuyoruz. Kütahya'da kendi ekibimizle çalışıyoruz; Bursa'dan yaklaşık iki buçuk saatte geliyoruz.</p>"),
  ("Bursa'ya en yakın maden ili",
   "<p>Kütahya'nın maden ve enerji işletmeleri için havadan görüntü sadece tanıtım değil, aynı zamanda bir kayıt: ocağın ilerleyişi, döküm sahalarının değişimi, rehabilitasyonla yeniden yeşillenen alanlar. Bunları belirli aralıklarla aynı noktalardan çekmek, işletmenin hem kendi raporlarında hem kamuoyuna yönelik iletişimde kullanabileceği bir arşiv oluşturuyor.</p>"),
 ],
 sss=[
  ("Maden ocağımızı havadan çekebilir misiniz?", "Evet; iş güvenliği kurallarınıza uyarak, patlatma ve yükleme saatlerinin dışında."),
  ("Aizanoi'de drone ile çekim yapılabilir mi?", "Bakanlık izniyle; başvuruyu önceden yapıyoruz."),
  ("Termal otelimizi havadan çekmek için en iyi zaman?", "Kışın soğuk bir sabah; havuzlardan yükselen buhar en etkili görüntü."),
  ("Bursa'dan mı geliyorsunuz?", "Evet, kendi ekibimizle; yaklaşık iki buçuk saatlik yol."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ MALATYA DRONE
"malatya-drone-cekimi": dict(
 lede="Haziran'da Malatya'nın kayısı bahçeleri turuncuya dönüyor; havadan bakınca ova boyunca uzanan bir renk tarlası. Şehrin merkezinde ise vinçler ve yeni binalar, yeniden kurulan bir Malatya'yı gösteriyor.",
 bolum=[
  ("Kayısı ve tarım",
   "<p>Malatya, dünyanın en büyük kayısı üretim bölgelerinden biri. Kayısı bahçelerinin hasat döneminde havadan görüntüsü, ihracatçı ve üreticiler için bahçeden kurutma alanına, oradan paketleme tesisine uzanan filmin açılışı. Hasattan sonra kayısıların güneşte kurutulduğu alanlar da havadan çok güçlü bir kare.</p>"),
  ("Şantiye ve yeniden yapılanma",
   "<p>Şubat 2023 depremlerinden sonra Malatya'nın merkezinde yeni çarşı, yeni konut alanları ve yeni yollar yapılıyor. Müteahhitler ve kurumlar için aylık şantiye ilerleme çekimi; aynı noktadan ve aynı yükseklikten. Bu görüntüler, iş sahibine ve hak sahiplerine ilerlemenin somut kanıtı.</p>"),
  ("Uçuş, baraj ve ışık",
   "<p>Malatya Havalimanı Erhaç'ta ve askerî bir üsle ortak kullanılıyor; çevresinde uçuş izne bağlı. Karakaya Barajı ve diğer baraj gövdeleri kritik tesis; çevrelerinde izinsiz uçmuyoruz. Temmuz 2026 SHGM talimatına göre haritada yeşil görünen yerlerde ayrı izne gerek yok; kayısı bahçelerinin çoğu bu kapsamda.</p>"
   "<p>Malatya'da yaz kuru ve parlak; uçuşları sabaha ve akşamüstüne koyuyoruz. Malatya'da sahadaki kamera ekibi bölgeden; kurgu ve renk bizden.</p>"),
  ("Nemrut'a Malatya'dan",
   "<p>Nemrut Dağı'na Malatya tarafından da çıkılıyor; turizm işletmeleri için bu güzergâh önemli bir kart. Dağın ören yeri ve millî park sınırları içinde drone ile çekim Bakanlık ve millî park iznine bağlı; Malatya'dan yola çıkan turlar ve konaklama tesisleri için güzergâhın kendisi, vadiler ve köyler ise daha esnek bir çekim alanı.</p>"),
 ],
 sss=[
  ("Kayısı bahçesini ne zaman çekmeliyiz?", "Haziran–Temmuz hasat döneminde; kurutma alanları için hasattan hemen sonra."),
  ("Şantiye çekimini her ay yapıyor musunuz?", "Evet; aynı noktadan ve yükseklikten çekip ilerlemeyi yan yana gösteriyoruz."),
  ("Havalimanına yakın arazimiz için izin gerekir mi?", "Büyük olasılıkla evet; koordinatı kontrol edip önceden söylüyoruz."),
  ("Kurutma tesisimizi de çekebilir misiniz?", "Evet; havadan alanın büyüklüğünü, yerden süreci gösteriyoruz."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ MARDİN DRONE
"mardin-drone-cekimi": dict(
 lede="Mardin'in taş evleri yamaçtan Mezopotamya ovasına doğru basamak basamak iniyor; havadan bakınca şehir ovanın üzerinde asılı duruyor gibi. Ama sınıra yakın bir şehirde gökyüzü de kurallarla çevrili.",
 bolum=[
  ("Mardin'de uçuş",
   "<p>Mardin Suriye sınırına yakın; Nusaybin ve Kızıltepe'nin güneyi gibi sınır bölgeleri ve askerî alanlar drone için sıkı kısıtlı. Kızıltepe yönündeki havalimanının çevresi de kontrollü hava sahası. Eski Mardin ve Midyat'ın tarihî dokusu koruma altında; tarihî yapıların yakınında uçuş ayrıca izne bağlı olabiliyor. Bu yüzden her işin ilk adımı koordinat ve izin kontrolü.</p>"),
  ("Mardin'de drone ne çekiyor",
   "<p><strong>Eski Mardin ve butik oteller:</strong> taş konaklar, teraslar ve ovaya bakan manzara; otel ve restoran tanıtımlarının açılışı. Gün batımında taşın bal rengi en güzel hâlinde.</p>"
   "<p><strong>Midyat ve Tur Abdin:</strong> taş mimari, manastırlar ve köyler; turizm ve belgesel işleri. Dini yapılarda ve çevresinde izin ve saygı öncelikli.</p>"
   "<p><strong>Tarım:</strong> Kızıltepe ovasının buğday ve mercimek tarlaları; hasat döneminde geniş ve sade planlar.</p>"
   "<p><strong>Şantiye ve yeni şehir:</strong> Artuklu'daki yeni yerleşim alanlarında konut projeleri; aylık ilerleme.</p>"),
  ("Işık ve ekip",
   "<p>Mardin yazın çok sıcak; öğle saatinde ova puslu görünüyor. Uçuşları gün doğumu ve gün batımına yakın saatlere koyuyoruz. Kurgu ve renk bizim ekipte; çekim günlerinde bölgedeki kamera ortağımızla sahadayız.</p>"),
 ],
 sss=[
  ("Eski Mardin'de drone ile çekim yapılabilir mi?", "Koordinata ve izin durumuna bağlı; tarihî doku koruma altında. Başvuruyu önceden yapıyoruz."),
  ("Butik otelimizi havadan nasıl gösterirsiniz?", "Gün batımında teras ve ovaya bakan manzara; otelin şehir içindeki yeri ve çevresi."),
  ("Kızıltepe'deki tarlamızı çekebilir misiniz?", "Sınıra uzaklığına ve koordinata göre; önceden kontrol ediyoruz."),
  ("Yazın uçuş hangi saatte yapılmalı?", "Gün doğumundan sonraki ilk saatlerde ve gün batımına yakın."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ MUĞLA DRONE
"mugla-drone-cekimi": dict(
 lede="Bodrum'un beyaz evleri, Göcek'in koylarına demirlemiş guletler, Ölüdeniz'in lagünü ve Dalyan'ın kaya mezarları. Muğla'da drone çekiminin müşterisi çoğu zaman turizm, malzemesi her zaman deniz.",
 bolum=[
  ("Muğla'da uçuş: havalimanları ve koruma alanları",
   "<p>Milas-Bodrum ve Dalaman havalimanlarının çevresi kontrollü hava sahası; Bodrum yarımadasının bir kısmı ve Dalaman-Ortaca hattı izne bağlı. Muğla'nın kıyısında millî parklar, özel çevre koruma bölgeleri ve sit alanları da çok: Köyceğiz-Dalyan'daki İztuzu, deniz kaplumbağalarının yuva yaptığı bir kumsal; yuvalama döneminde kurallar sıkı. Bu alanlarda çekimi izinle ve yaban hayatını rahatsız etmeden planlıyoruz.</p>"),
  ("Muğla'da drone ne çekiyor",
   "<p><strong>Gulet ve yat:</strong> seyir hâlinde ve koyda demirliyken; teknenin koyla ilişkisi, güverte ve yüzme anı. Tekne kiralama firmalarının en etkili tanıtım karesi.</p>"
   "<p><strong>Villa ve otel:</strong> Bodrum, Fethiye, Marmaris ve Datça'da havuzlu villalar ve oteller; denize mesafe, manzara ve mahremiyet.</p>"
   "<p><strong>Aktivite:</strong> Ölüdeniz'in yamaç paraşütü, dalış ve tekne turları; aksiyonu havadan takip eden planlar.</p>"
   "<p><strong>Çam balı ve zeytin:</strong> ormanlar, kovanlar ve zeytinlikler; üretici tanıtımı.</p>"),
  ("Rüzgâr ve sezon",
   "<p>Muğla'nın kıyısında yaz öğleden sonraları rüzgâr artıyor; drone planlarını sabaha, villa ve otel dış çekimini gün batımına koyuyoruz. Otel ve tekne işletmeleri için çekimi sezon başlamadan, Nisan–Mayıs'ta yapmanızı öneriyoruz: tesis hazır, misafir yok, deniz berrak. Kurgu ve renk bizde; sahada bölgedeki kamera ortağımızla çalışıyoruz.</p>"),
 ],
 sss=[
  ("Guletimizi seyir hâlinde çekebilir misiniz?", "Evet; ayrı bir tekneden ya da kıyıdan kalkışla, teknenin koyla ilişkisini gösteren planlarla."),
  ("Bodrum'da drone için izin gerekiyor mu?", "Havalimanına yakın kesimlerde evet. Koordinatı kontrol edip izin sürecini takvime koyuyoruz."),
  ("İztuzu'nda çekim yapılabilir mi?", "Koruma alanı ve kaplumbağa yuvalama bölgesi; izinle ve kurallara uyarak, yuvalama döneminde çok sınırlı."),
  ("Otelimiz için en iyi çekim dönemi ne zaman?", "Nisan–Mayıs; tesis hazır, misafir yok, ışık yumuşak."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ NEVŞEHİR DRONE
"nevsehir-drone-cekimi": dict(
 lede="Kapadokya'nın gökyüzü sabahları yüzlerce sıcak hava balonuyla doluyor. Bu yüzden Kapadokya'da drone çekimi, Türkiye'nin en dikkatli planlanması gereken uçuşlarından biri.",
 bolum=[
  ("Balonlar ve drone",
   "<p>Göreme, Uçhisar, Ürgüp ve çevresinde sabah saatlerinde balon uçuşları yapılıyor; balonların uçtuğu alanlarda ve saatlerde drone kullanmak hem kurallara aykırı hem tehlikeli. Bölgede drone uçuşları sıkı kısıtlamalara tabi; ayrıca Göreme ve çevresi UNESCO Dünya Mirası alanı ve millî park statüsünde. Kapadokya Havalimanı da Gülşehir'de, ilin kuzeyinde.</p>"
   "<p>Bu yüzden Kapadokya'da havadan çekim isteyen her işte önce koordinatı, saati ve izin durumunu kontrol ediyoruz. Balonları göstermek isteyen işlerde, balonları yerden ya da terastan çekmek çoğu zaman en doğru ve en güzel çözüm.</p>"),
  ("Kapadokya'da drone ne çekiyor",
   "<p><strong>Butik otel ve mağara evler:</strong> izin verilen koşullarda otelin vadiyle ilişkisi; terastan balonlar ise yerden.</p>"
   "<p><strong>Şarap ve bağ:</strong> Ürgüp ve Mustafapaşa'nın bağları ve şaraphaneleri; hasat dönemi.</p>"
   "<p><strong>Nevşehir merkez ve şantiye:</strong> şehirde yeni konut projeleri ve tesisler; koordinata göre.</p>"
   "<p><strong>Etkinlik ve tur:</strong> at turları, ATV ve vadi yürüyüşleri; aktiviteyi yerden ve izin verilen yerlerde havadan.</p>"),
  ("Işık ve ekip",
   "<p>Kapadokya'nın ışığı sabah ve akşam çok yumuşak; peribacaları gün batımında pembeye dönüyor. Yaz öğlesi sert ve tozlu. Kurgu ve renk bizde; çekim günlerinde bölgedeki kamera ortağımızla sahadayız.</p>"),
 ],
 sss=[
  ("Kapadokya'da balonların arasında drone uçurabilir miyiz?", "Hayır. Balon saatlerinde ve uçuş alanlarında drone kullanılmıyor; balonları yerden ya da terastan çekiyoruz."),
  ("Otelimizi havadan çekmek mümkün mü?", "Koordinata ve izin durumuna bağlı; önceden kontrol ediyor, mümkün değilse yerden ve terastan güçlü bir anlatım kuruyoruz."),
  ("Bağımızı ne zaman çekmeliyiz?", "Eylül–Ekim hasat döneminde."),
  ("Nevşehir merkezdeki şantiyemizi çekebilir misiniz?", "Koordinata göre çoğu zaman evet; önceden kontrol ediyoruz."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ ORDU DRONE
"ordu-drone-cekimi": dict(
 lede="Ordu'da havalimanı denizin içinde, fındık bahçeleri yamaçlarda, yaylalar bulutların üstünde. Karadeniz'in en geniş fındık havzası, havadan bakınca yeşilin bütün tonlarını gösteriyor.",
 bolum=[
  ("Fındık ve yayla",
   "<p><strong>Fındık bahçeleri:</strong> Ordu, Türkiye'nin en büyük fındık üretim illerinden biri; bahçeler denizden yaylalara kadar yamaçları kaplıyor. Ağustos'taki hasat dönemi, üretici ve ihracatçılar için bahçeden kırma tesisine uzanan filmin en canlı zamanı. Bahçe satışlarında arazi sınırı ve eğim havadan.</p>"
   "<p><strong>Yaylalar:</strong> Perşembe Yaylası, Çambaşı ve diğer yaylalar; sabah sisinin ve bulut denizinin üzerinden yayla evleri. Turizm ve konaklama tesisleri için.</p>"),
  ("Şehir, sahil ve uçuş",
   "<p><strong>Boztepe ve sahil:</strong> teleferikle çıkılan tepeden şehir ve deniz; Altınordu sahilindeki yeni siteler ve kuleler. Konut projelerinde gerçek kat yüksekliğinden manzara çekimi.</p>"
   "<p>Ordu-Giresun Havalimanı denizi doldurarak yapılmış ve Gülyalı'da, şehre yakın; çevresinde uçuş izne bağlı. Altınordu sahilinin bir kısmı bu sahaya yakın; koordinatı her çekimde kontrol ediyoruz.</p>"),
  ("Hava ve ekip",
   "<p>Karadeniz ikliminde hava gün içinde değişebiliyor; yaylada sis bir saatte gelip gidiyor. Yayla ve deniz çekimlerine yedek gün koyuyoruz. Kurgu ve renk bizde; sahada bölgedeki kamera ortağımızla çalışıyoruz.</p>"),
  ("Ünye, Fatsa ve sahil yolu",
   "<p>Ordu'nun batısında Ünye ve Fatsa, kendi limanları, sahil parkları ve sanayi tesisleriyle ayrı birer şehir gibi. Karadeniz sahil yolu bu ilçeleri birbirine bağlıyor; yolun denizle dağ arasındaki ince şeritte ilerlemesi havadan bakınca bölgenin coğrafyasını tek karede anlatıyor. Ünye Kalesi ve çevresindeki koylar, turizm tanıtımları için güçlü bir açılış.</p>"),
 ],
 sss=[
  ("Fındık bahçemizi ne zaman çekmeliyiz?", "Ağustos hasat döneminde; bahçe ve işçiler en hareketli hâlinde."),
  ("Altınordu'daki projemizin manzarasını havadan gösterebilir misiniz?", "Havalimanına yakınlık nedeniyle izin gerekebilir; koordinatı kontrol edip önceden söylüyoruz."),
  ("Yayla tesisimiz için sisli görüntü mümkün mü?", "Havaya bağlı; yedek gün koyup sabah saatlerinde deniyoruz."),
  ("Boztepe'den şehir çekimi yapılabilir mi?", "Koordinata göre; yerden teleferik ve şehir manzarası her zaman güçlü bir alternatif."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ RİZE DRONE
"rize-drone-cekimi": dict(
 lede="Rize'de dağ denize dik iniyor; çay bahçeleri yamaçlara basamak basamak tırmanıyor, Fırtına Vadisi'nde taş köprüler köpüklü derenin üzerinden geçiyor. Havadan bakınca Türkiye'nin en yeşil ili.",
 bolum=[
  ("Rize'de drone ne çekiyor",
   "<p><strong>Çay bahçeleri ve fabrikalar:</strong> Mayıs'tan Ekim'e kadar süren hasat dönemlerinde çay toplayıcıları ve yamaçlardaki bahçeler; çay fabrikalarının ölçeği ve yaprağın taşınması. Çay üreticileri ve markaları için bahçeden bardağa uzanan filmin açılışı.</p>"
   "<p><strong>Fırtına Vadisi ve Ayder:</strong> taş köprüler, dere, rafting ve yayla evleri; turizm ve konaklama tesisleri için. Yayla yolları yazın açık; kışın erişim sınırlı.</p>"
   "<p><strong>Konut ve sahil:</strong> denizi doldurarak açılan sahil yolu ve yeni binalar; yamaçtaki evlerin yolu ve konumu.</p>"),
  ("Uçuş ve koruma",
   "<p>Rize-Artvin Havalimanı Pazar'da, denizin üzerine kurulu; çevresinde uçuş izne bağlı. Kaçkar Dağları Millî Parkı ve yaylaların bir kısmı koruma altında; ticari çekim için izin alıyoruz. Vadilerde rüzgâr ve bulut hızla değişiyor; uçuşları kısa ve planlı tutuyoruz.</p>"),
  ("Yağmur ve ekip",
   "<p>Rize Türkiye'nin en çok yağış alan ili; açık bir gün bulmak için yedek gün koymak şart. Sis ve alçak bulut ise bazen en güzel kareyi veriyor: bulutların arasından görünen çay bahçeleri. Kurgu ve renk bizde; çekim günlerinde bölgedeki kamera ortağımızla sahadayız.</p>"),
 ],
 sss=[
  ("Çay hasadını ne zaman çekmeliyiz?", "Mayıs sonundaki ilk hasat, yaprakların en taze olduğu dönem; yaz boyunca ikinci ve üçüncü hasat da mümkün."),
  ("Ayder'deki tesisimizi havadan çekebilir misiniz?", "Koruma alanı kurallarına göre izinle; yazın yol açıkken."),
  ("Yağmurlu havada ne yapıyoruz?", "Yedek gün koyuyoruz; alçak bulut ve sis bazen en güzel görüntüyü veriyor, karar o sabah veriliyor."),
  ("Pazar'daki projemiz için drone kullanılabilir mi?", "Havalimanına yakınlık nedeniyle izin gerekebilir; koordinatı kontrol ediyoruz."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ SAMSUN DRONE
"samsun-drone-cekimi": dict(
 lede="Kızılırmak'ın Karadeniz'e döküldüğü delta, Atakum'da sahile dizilen kuleler, Bafra ve Çarşamba'nın sebze ovaları ve Karadeniz'in en büyük limanlarından biri. Samsun'u havadan çekmek, suyun şehri nasıl şekillendirdiğini göstermek.",
 bolum=[
  ("Delta ve kurallar",
   "<p>Kızılırmak Deltası uluslararası öneme sahip bir sulak alan ve kuş cenneti; yaban atları ve yüzlerce kuş türü burada yaşıyor. Ticari çekim izne bağlı; kuşları rahatsız edecek alçak uçuştan kaçınıyor, göç ve kuluçka dönemlerinde uçmuyoruz. Yeşilırmak Deltası da benzer bir alan.</p>"
   "<p>Samsun-Çarşamba Havalimanı şehrin doğusunda; çevresi kontrollü hava sahası. Liman ve sanayi tesisleri kritik yapı. Temmuz 2026 SHGM talimatına göre haritada yeşil görünen yerlerde ayrı izne gerek yok.</p>"),
  ("Samsun'da drone ne çekiyor",
   "<p><strong>Konut ve kule projeleri:</strong> Atakum ve İlkadım sahilindeki yeni projeler; dairenin katından gerçek manzara. Aynı manzarayı vaat eden onlarca proje arasında fark yaratan görüntü.</p>"
   "<p><strong>Sanayi ve medikal:</strong> organize sanayi bölgelerindeki tıbbi cihaz, makine ve gıda tesisleri; kampüsün ölçeği ve liman bağlantısı.</p>"
   "<p><strong>Tarım:</strong> Bafra ve Çarşamba ovalarının sebze ve çeltik tarlaları; seralar ve sulama düzeni.</p>"),
  ("Hava ve ekip",
   "<p>Karadeniz kıyısında hava gün içinde değişebiliyor; deniz ve delta çekimlerine yedek gün koyuyoruz. Kurgu ve renk bizde; sahada bölgedeki kamera ortağımızla çalışıyoruz.</p>"),
  ("Tarihî liman, yeni şehir",
   "<p>Samsun, Kurtuluş Savaşı'nın başladığı liman; Bandırma Vapuru'nun replikası ve sahildeki Onur Anıtı şehrin simgeleri. Bu tarihî kıyı ile Atakum'un yeni siteleri arasındaki dönüşüm, havadan bakınca tek bir sahil şeridinde görülüyor. Belediye ve kurum tanıtımlarında, şehrin bu iki yüzünü aynı planda göstermek güçlü bir anlatım.</p>"),
 ],
 sss=[
  ("Kızılırmak Deltası'nda drone uçurabilir miyiz?", "İzinle ve kurallara uyarak; göç ve kuluçka dönemlerinde uçmuyoruz."),
  ("Atakum'daki projemizin manzarasını nasıl gösterirsiniz?", "Dairenin katına denk gelen yükseklikten drone ile çekip balkondan bakışı gösteriyoruz."),
  ("Fabrikamızı havadan çekebilir misiniz?", "Koordinata göre çoğu zaman evet; liman ve kritik tesislere yakınsa izin gerekebilir."),
  ("Hava kapalıysa ne oluyor?", "Yedek gün koyuyoruz; Karadeniz'de bu sık oluyor."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ ŞANLIURFA DRONE
"sanliurfa-drone-cekimi": dict(
 lede="Göbeklitepe'nin taş sütunları, Harran'ın kümbet evleri, Balıklıgöl ve GAP kanallarıyla yeşeren Harran ovası. Şanlıurfa'yı havadan çekmek, insanlığın en eski yerleşimleriyle en büyük sulama projelerinden birini yan yana koymak.",
 bolum=[
  ("Tarih ve izin",
   "<p><strong>Göbeklitepe</strong> UNESCO Dünya Mirası listesinde ve korunan bir ören yeri; çatı ile örtülü kazı alanı ve çevresinde drone ile çekim Bakanlık iznine bağlı. <strong>Harran</strong>'ın kümbet evleri ve antik kenti de aynı şekilde. Turizm ve belgesel işlerinde başvuruyu çekim tarihinden önce yapıyoruz.</p>"),
  ("Ova ve sulama",
   "<p>Harran ovası, GAP kapsamında açılan sulama kanallarıyla Türkiye'nin en büyük tarım alanlarından birine dönüştü. Pamuk, mısır ve buğday tarlaları, kanalların geometrik düzeni ve sulama sistemleri havadan çok güçlü bir görüntü. Tarım işletmeleri, kooperatifler ve sulama projeleri için arazinin ölçeğini ve düzenini gösteriyoruz.</p>"
   "<p>Atatürk Barajı ve diğer baraj gövdeleri kritik tesis; çevrelerinde izinsiz uçmuyoruz.</p>"),
  ("Şehir, sınır ve sıcak",
   "<p>Şanlıurfa Suriye sınırında; Akçakale, Ceylanpınar ve sınıra yakın bölgeler drone için sıkı kısıtlı. GAP Havalimanı şehrin kuzeydoğusunda; çevresi kontrollü. Şehir içinde Karaköprü'nün yeni sitelerinde şantiye ve konut çekimleri koordinata göre.</p>"
   "<p>Şanlıurfa yazın Türkiye'nin en sıcak şehirlerinden biri; bataryalar sıcakta hızlı tükeniyor, hava öğlen titreşiyor. Uçuşları gün doğumuna ve gün batımına yakın saatlere koyuyoruz. Kurgu ve renk bizde; çekim günlerinde bölgedeki kamera ortağımızla sahadayız.</p>"),
  ("Balıklıgöl ve tarihî merkez",
   "<p>Balıklıgöl, Ayn-ı Zeliha Gölü ve çevresindeki tarihî yapılar Şanlıurfa'nın kalbi. Bu alan hem ziyaretçi hem ibadet yeri; havadan çekimde kalabalığın üzerinde uçmuyor, ibadet saatlerine saygı gösteriyor ve izin durumunu önceden kontrol ediyoruz. Sabahın erken saatlerinde gölün çevresi en sakin ve ışık en yumuşak hâlinde.</p>"),
 ],
 sss=[
  ("Göbeklitepe'de drone ile çekim yapılabilir mi?", "Bakanlık izniyle; süreç uzun olabiliyor, başvuruyu önceden yapıyoruz."),
  ("Harran ovasındaki arazimizi çekebilir misiniz?", "Sınıra uzaklığa ve koordinata göre çoğu zaman evet; önceden kontrol ediyoruz."),
  ("Karaköprü'deki şantiyemiz için izin gerekir mi?", "Koordinata bağlı; havalimanından ve kısıtlı alanlardan uzaksa genellikle gerekmiyor."),
  ("Yazın uçuş hangi saatte yapılmalı?", "Gün doğumu ve gün batımına yakın saatlerde."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ SİVAS DRONE
"sivas-drone-cekimi": dict(
 lede="Divriği Ulu Camii'nin taş kapıları, Gökpınar Gölü'nün inanılmaz mavisi, Kangal'ın bozkırları ve Ankara'ya hızlı trenle bağlanan bir şehir. Sivas, Türkiye'nin yüzölçümü en büyük ikinci ili.",
 bolum=[
  ("Geniş bir il, geniş planlar",
   "<p>Sivas'ın bozkırları, yaylaları ve vadileri havadan bakınca ölçeğini gösteriyor. <strong>Gökpınar Gölü</strong> (Gürün): berrak, turkuaz bir kaynak gölü; havadan çok güçlü bir kare, koruma kurallarına uyarak. <strong>Divriği Ulu Camii ve Darüşşifası</strong>: UNESCO Dünya Mirası listesinde; ibadet saatlerine ve kurallara uyarak, izinli olarak.</p>"
   "<p><strong>Kangal ve yaylalar:</strong> sürüler, çobanlar ve geniş bozkır; tanıtım ve belgesel işleri.</p>"),
  ("Şehir ve şantiye",
   "<p>Sivas'ta satılan konutların yarıya yakını yeni; şehirde çok sayıda yeni proje var. Müteahhitler için aylık şantiye ilerleme çekimi ve satış öncesi konum planı. Sanayi bölgesindeki tesisler ve demiryolu araçları üreten fabrika gibi büyük tesisler için kampüsün ölçeği.</p>"
   "<p>Sivas Havalimanı şehrin kuzeybatısında; çevresi kontrollü. Temmuz 2026 SHGM talimatına göre haritada yeşil görünen yerlerde ayrı izne gerek yok; şehir dışındaki bozkır ve yaylaların çoğu bu kapsamda.</p>"),
  ("Kış ve ekip",
   "<p>Sivas'ta kış uzun ve soğuk; bataryalar soğukta hızlı tükeniyor, uçuşları kısa ve planlı tutuyoruz. Kar sonrası açık bir gün, şehir ve tarihî yapılar için en temiz görüntü. Kurgu ve renk bizde; çekim günlerinde bölgedeki kamera ortağımızla sahadayız.</p>"),
  ("Hızlı trenin getirdiği",
   "<p>Ankara–Sivas hızlı tren hattıyla Sivas, başkente birkaç saatlik mesafeye indi. Bu bağlantı, şehirde yeni konut projelerinin ve istasyon çevresinde yeni yapılaşmanın önünü açıyor. Projenin istasyona ve şehir merkezine göre nerede durduğunu havadan göstermek, Ankara'dan dönmeyi düşünen alıcıya en net bilgiyi veriyor.</p>"),
 ],
 sss=[
  ("Gökpınar Gölü'nü havadan çekebilir miyiz?", "Koruma kurallarına uyarak çoğu zaman mümkün; koordinatı ve izin durumunu önceden kontrol ediyoruz."),
  ("Divriği Ulu Camii'nde drone kullanılabilir mi?", "İzinli olarak ve kurallara uyarak; ibadet saatlerinin dışında."),
  ("Şantiye ilerleme çekimi yapıyor musunuz?", "Evet; her ay aynı noktadan ve yükseklikten çekip ilerlemeyi yan yana gösteriyoruz."),
  ("Kışın uçuş yapılabilir mi?", "Evet; bataryaları sıcak tutuyor, kar sonrası açık bir günü seçiyoruz."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ TRABZON DRONE
"trabzon-drone-cekimi": dict(
 lede="Trabzon'un havalimanı şehrin tam ortasında, sahil boyunca uzanıyor. Bu yüzden şehirde drone çekimi çoğu zaman şehrin dışında başlıyor: Sumela'nın vadisinde, Uzungöl'ün kıyısında, yaylalarda.",
 bolum=[
  ("Trabzon'da uçuş",
   "<p>Trabzon Havalimanı şehir merkezine bitişik ve sahil boyunca uzanıyor; Ortahisar'ın sahil kesiminin büyük kısmı kontrollü hava sahası. Liman da kritik yapı. Şehir merkezinde havadan çekim çoğu yerde izne bağlı ya da mümkün değil. Temmuz 2026 SHGM talimatına göre haritada yeşil görünen yerlerde ayrı izne gerek yok; yaylaların ve iç kesimlerin çoğu bu kapsamda.</p>"),
  ("Trabzon'da drone ne çekiyor",
   "<p><strong>Sumela ve Altındere Vadisi:</strong> kayaya oyulmuş manastır ve vadinin ormanı. Millî park ve ören yeri; drone ile çekim izne bağlı.</p>"
   "<p><strong>Uzungöl ve yaylalar:</strong> göl, cami ve dik ormanlar; Hıdırnebi ve diğer yaylalarda bulut denizi. Turizm ve konaklama tesisleri için en güçlü kareler.</p>"
   "<p><strong>Konut:</strong> Akçaabat ve Yomra'daki yeni projeler; yamaçtaki binaların konumu ve manzara.</p>"
   "<p><strong>Fındık ve tarım:</strong> yamaçlardaki fındık bahçeleri; hasat dönemi.</p>"),
  ("Hava ve ekip",
   "<p>Trabzon'da hava gün içinde birkaç kez değişebiliyor; yaylada sis bir saatte gelip gidiyor. Yayla ve göl çekimlerine yedek gün koyuyoruz. Kurgu ve renk bizde; sahada bölgedeki kamera ortağımızla çalışıyoruz.</p>"),
  ("Körfez'den gelen misafir",
   "<p>Trabzon'un otel, yayla evi ve tur işletmeleri için misafirlerin önemli bir kısmı Körfez ülkelerinden geliyor. Bu misafirin aradığı şey yeşil, serin ve bulutlu bir manzara; havadan çekilmiş bir yayla ya da göl görüntüsü, tanıtım filminin ilk saniyelerinde bu duyguyu veriyor. Tanıtım filmlerini Arapça altyazılı hazırlayabiliyoruz.</p>"),
 ],
 sss=[
  ("Trabzon merkezde drone ile çekim yapılabilir mi?", "Havalimanı şehrin içinde olduğu için çoğu yerde izin gerekiyor ya da uçuş mümkün değil. Koordinatı kontrol edip önceden söylüyoruz."),
  ("Uzungöl'deki otelimizi havadan çekebilir misiniz?", "Koordinata göre çoğu zaman evet; hafta içi sabah, kalabalıktan önce."),
  ("Sumela'da drone uçurabilir miyiz?", "Millî park ve ören yeri olduğu için izin gerekiyor; başvuruyu önceden yapıyoruz."),
  ("Bulut denizi için ne zaman gitmeliyiz?", "Sabah erken; havaya bağlı olduğu için yedek gün koyuyoruz."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ VAN DRONE
"van-drone-cekimi": dict(
 lede="Türkiye'nin en büyük gölü, Akdamar Adası'nın taş kilisesi, Van Kalesi'nin kayalığı ve karşıda Süphan'ın karlı zirvesi. Van'ı havadan çekmek, bir gölün bir şehri nasıl tanımladığını göstermek.",
 bolum=[
  ("Göl ve kurallar",
   "<p>Van Ferit Melen Havalimanı göl kıyısında, şehre yakın; çevresi kontrollü hava sahası. İran sınırına yakın bölgeler ve askerî alanlar sıkı kısıtlı. <strong>Akdamar Adası</strong> ve Van Kalesi ören yeri; drone ile çekim Bakanlık iznine bağlı. Temmuz 2026 SHGM talimatına göre haritada yeşil görünen yerlerde ayrı izne gerek yok; gölün bazı kıyıları ve iç kesimler bu kapsamda.</p>"),
  ("Van'da drone ne çekiyor",
   "<p><strong>Göl kıyısı tesisleri:</strong> Edremit ve Gevaş kıyısındaki oteller, tesisler ve yazlık siteler; gölün mavisi ve dağlar.</p>"
   "<p><strong>Muradiye Şelalesi ve doğa:</strong> bazalt kayalıklardan dökülen şelale; kışın donmuş hâli de etkileyici.</p>"
   "<p><strong>Şantiye ve konut:</strong> Tuşba, İpekyolu ve Edremit'teki yeni projeler; aylık ilerleme ve göl manzarası.</p>"
   "<p><strong>Tarım ve hayvancılık:</strong> yaylalar, sürüler ve Van otlu peyniri üreticileri; tanıtım filmlerinin açılışı.</p>"),
  ("Işık ve ekip",
   "<p>Van Gölü sabah saatlerinde en mavi ve durgun; göl çekimlerini sabaha koyuyoruz. Kış uzun ve karlı; soğukta bataryalar hızlı tükendiği için uçuşları kısa tutuyoruz. Kurgu ve renk bizde; çekim günlerinde bölgedeki kamera ortağımızla sahadayız.</p>"),
 ],
 sss=[
  ("Akdamar Adası'nı drone ile çekebilir miyiz?", "Ören yeri olduğu için Bakanlık izni gerekiyor; başvuruyu önceden yapıyoruz."),
  ("Göl kıyısındaki otelimizi havadan çekebilir misiniz?", "Koordinata göre; havalimanına yakın kıyılarda izin gerekebilir."),
  ("Muradiye Şelalesi için en iyi zaman?", "İlkbaharda su en gür; kışın donmuş hâli de çok etkileyici."),
  ("Kışın uçuş yapılabilir mi?", "Evet; bataryaları sıcak tutup kısa ve planlı uçuyoruz."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ YALOVA DRONE
"yalova-drone-cekimi": dict(
 lede="Yalova'nın seraları havadan bakınca beyaz bir mozaik gibi; Altınova'nın tersanelerinde gemiler kızakta, Termal'in ormanında buhar yükseliyor. Bursa'ya bir saat, İstanbul'a deniz yoluyla bir saat.",
 bolum=[
  ("Seralar ve fidanlıklar",
   "<p>Yalova, süs bitkisi ve fidan üretiminde Türkiye'nin merkezi; il boyunca uzanan seralar ve fidanlıklar havadan çok güçlü bir görüntü. İhracatçı üreticiler için seraların ölçeğini, üretim alanlarının düzenini ve sevkiyat noktalarını havadan; bitkinin kalitesini yerden gösteriyoruz. İlkbahar, seraların en dolu ve renkli olduğu dönem.</p>"),
  ("Tersaneler",
   "<p>Altınova'daki tersaneler gemi ve yat üretiyor. Kızaktaki geminin havadan görüntüsü, yapım sürecinin aylık kaydı ve denize indirme töreni; tersanenin armatöre ve fuara gidecek tanıtımının en güçlü anları. Tersane sahasında uçuşu işletmenin iş güvenliği kurallarına göre planlıyoruz.</p>"),
  ("Termal, sahil ve konut",
   "<p><strong>Termal:</strong> ormanın içindeki oteller ve kaplıcalar; kışın havuzlardan yükselen buhar.</p>"
   "<p><strong>Çınarcık ve Armutlu:</strong> sahil siteleri ve yazlıklar; denize mesafe ve manzara.</p>"
   "<p>Yalova'da sivil havalimanı yok; ilin büyük kısmı SHGM haritasında daha esnek. Askerî alanlar ve kritik tesisler için koordinatı kontrol ediyoruz. Yalova'da kendi ekibimizle çalışıyoruz; Bursa'dan yaklaşık bir saatte geliyoruz.</p>"),
  ("İstanbul'a bakan kıyı",
   "<p>Yalova'nın kıyısından bakınca karşıda İstanbul'un adaları görünüyor; havadan bu bakış, Yalova'nın İstanbul'a ne kadar yakın olduğunu tek karede anlatıyor. Deniz otobüsü iskelesi, Osmangazi Köprüsü bağlantısı ve sahil boyunca uzanan siteler; İstanbul'dan ev ya da tesis arayan alıcıya Yalova'yı tanıtmanın en kısa yolu.</p>"),
 ],
 sss=[
  ("Seralarımızı havadan çekmek için ne zaman gelmeliyiz?", "İlkbaharda; seralar en dolu ve renkli hâlinde."),
  ("Denize indirme törenini havadan çekebilir misiniz?", "Evet; tarihi tersaneyle netleştirip töreni havadan ve yerden birden fazla açıdan çekiyoruz."),
  ("Termal otelimiz için drone ne zaman çekilmeli?", "Kışın soğuk bir sabah; buhar ve orman birlikte."),
  ("Bursa'dan mı geliyorsunuz?", "Evet, kendi ekibimizle; yaklaşık bir saatlik yol."),
 ],
 kaynak=[KAYNAK_IHA],
),

# ------------------------------------------------------------------ ZONGULDAK DRONE
"zonguldak-drone-cekimi": dict(
 lede="Zonguldak'ta maden ocakları, Ereğli'nin çelik fabrikası ve Kozlu'nun yamaçları denize kadar iniyor. Gökgöl Mağarası'nın ağzı, Filyos'un kumsalı ve Bartın yönüne uzanan yeşil kıyı da aynı ilin içinde.",
 bolum=[
  ("Sanayi ve enerji",
   "<p>Zonguldak, Türkiye'nin taş kömürü havzası; maden ocakları, lavvarlar ve termik santraller. Ereğli'deki demir-çelik fabrikası ve liman da ilin en büyük tesisleri. Bu tesislerin çoğu kritik yapı sayılıyor; çevrelerinde izinsiz uçmuyoruz. İşletme adına yapılan çekimlerde izni işletmeyle birlikte alıyor, iş güvenliği kurallarına göre uçuş planı kuruyoruz.</p>"),
  ("Kıyı, doğa ve konut",
   "<p><strong>Kıyı:</strong> Kilimli, Filyos ve Ereğli kıyıları; yamaçtan denize inen yeşil ve kayalık sahiller.</p>"
   "<p><strong>Gökgöl Mağarası ve doğa:</strong> ormanlık vadiler ve mağara girişleri; turizm tanıtımı.</p>"
   "<p><strong>Konut:</strong> yamaçtaki yeni binalar; binaya giden yol, eğim ve deniz manzarası havadan. Satılan konutların önemli kısmının yeni olduğu bir şehirde müteahhit için konum planı.</p>"),
  ("Uçuş ve hava",
   "<p>Zonguldak Havalimanı Çaycuma'da, şehrin doğusunda; çevresi kontrollü. Karadeniz ikliminde hava gün içinde değişebiliyor; deniz ve kıyı çekimlerine yedek gün koyuyoruz. Kurgu ve renk bizde; çekim günlerinde bölgedeki kamera ortağımızla sahadayız.</p>"),
 ],
 sss=[
  ("Maden sahamızı havadan çekebilir misiniz?", "İşletmenin izniyle ve iş güvenliği kurallarına uyarak evet."),
  ("Ereğli'deki tesisimiz için drone kullanılabilir mi?", "Kritik tesislerin çevresinde izin gerekiyor; işletmeyle birlikte planlıyoruz."),
  ("Yamaçtaki projemizin konumunu nasıl gösterirsiniz?", "Havadan, ana yoldan binaya çıkan yolu ve denizi aynı karede gösteren bir planla."),
  ("Hava kapalıysa ne oluyor?", "Yedek gün koyuyoruz; Karadeniz'de bu sık oluyor."),
 ],
 kaynak=[KAYNAK_IHA],
),
}
