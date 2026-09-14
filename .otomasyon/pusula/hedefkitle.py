# -*- coding: utf-8 -*-
"""
HEDEF KİTLE FABRİKASI
Her Luna Yapım hizmeti için: kimi arıyoruz, nereden tanırız, ne deriz,
ne kadar sürer, ne kadar eder, hangi itiraz gelir ve nasıl cevaplanır.

Panelde kart olarak görünür; Pusula avlanırken de bu tanımları kullanır.
"""

HIZMETLER = {

"insaat-3d-modelleme": {
  "ad": "İnşaat 3D Modelleme & Mimari Görselleştirme",
  "kisa": "Projeyi temeli atılmadan sattıran görselleştirme",
  "sayfa": "hizmetler/insaat-3d-modelleme.html",
  "renk": "#E8452C",

  "kim": [
    "Müteahhit / yapı kooperatifi — 1-5 bloklu konut projesi geliştiren",
    "Gayrimenkul geliştirici — çok etaplı site, karma proje",
    "Mimarlık ofisi — yarışma ve müşteri sunumu yapan",
    "Kentsel dönüşüm müteahhidi — hak sahibine yeni yapıyı anlatması gereken",
    "Sanayi yatırımcısı — fabrika / tesis projesi kredilendiren",
  ],
  "unvan": ["Şirket sahibi / ortak", "Proje müdürü", "Satış ve pazarlama müdürü", "Mimar / tasarım sorumlusu"],

  "sinyal": [
    "Yeni proje ilanı açmış ama ilanda sadece kat planı ve şantiye fotoğrafı var",
    "Sitesinde 'yakında' / 'satışta' etiketli proje sayfası var, görsel yok",
    "Instagram'da şantiye fotoğrafı paylaşıyor, render paylaşmıyor",
    "Yapı ruhsatı yeni alınmış (belediye ilan panosu / e-devlet duyuruları)",
    "Satış ofisi açmış ama maket yok",
    "Fuar katılım listesinde adı geçiyor (Yapı Fuarı, MIPIM Türkiye vb.)",
  ],
  "nerede": ["Google Haritalar 'inşaat firması' + il", "Sahibinden/Emlakjet proje ilanları",
             "İl müteahhitler derneği üye listeleri", "Yapı fuarı katılımcı listeleri",
             "Belediye ruhsat duyuruları", "LinkedIn 'proje müdürü' + il"],

  "aci": [
    "Maket satışı geç başlıyor, finansman sıkışıyor",
    "Alıcı metrekareyi hayal edemiyor, satış ofisinde tek tek anlatılıyor",
    "Şehir dışı ve yurt dışı alıcı ikna edilemiyor",
    "Rakip projede render var, kendi ilanı sönük duruyor",
  ],
  "acilis": ("{firma} için {sehir}'daki {proje} projesine baktım — ilanda kat planı var ama alıcının "
             "bitmiş hali görebileceği bir görsel yok. Temel atılmadan maket satışına başlayan projelerde "
             "bu tek başına ciddi fark yaratıyor. 3D tanıtımın neye benzeyeceğini gösteren kısa bir sayfa "
             "hazırladım, göndereyim mi?"),

  "kanal": ["WhatsApp (birincil)", "Telefon", "Yüz yüze satış ofisi ziyareti", "E-posta (kurumsal)"],
  "ritim": "1. gün mesaj → 3. gün arama → 7. gün demo linki → 14. gün 'proje ne durumda' → aylık takip",

  "butce": "Görsel paketi orta, lansman paketi yüksek, tam satış seti en yüksek segment",
  "dongu": "2-6 hafta (satış ofisi açılışına bağlı; lansman tarihi varsa hızlanır)",
  "mevsim": "Yılbaşı-Mart arası lansman hazırlığı en yoğun dönem; fuar öncesi 6-8 hafta ikinci pik",

  "itirazlar": [
    ("Pahalı geliyor.",
     "Bir dairenin komisyonunu düşünün — tek satışı öne çeken bir çalışma kendini ödüyor. "
     "Ayrıca paketleri bölebiliyoruz: önce render seti, satış başlayınca animasyon."),
    ("Mimarımız zaten render yapıyor.",
     "Mimari render sunum içindir, satış filmi değildir. Biz kamera hareketi, ışık senaryosu ve "
     "kurgu tarafını ekliyoruz — çıkan şey ilan sitesinde ve reklamda çalışıyor."),
    ("Proje henüz kesinleşmedi.",
     "En doğru zaman tam da bu. Kesinleşince zaten satışa çıkacaksınız; modelleme süresi 2-4 hafta, "
     "şimdi başlarsak lansmana yetişir."),
    ("Yapay zekâ ile ucuza yaptırıyorlar.",
     "Ölçüsüz görsel alıcıyı yanıltır ve teslimde sorun çıkarır. Biz mimari projeden ölçülü "
     "modelliyoruz; teslim edilen bina görseldekiyle aynı oluyor."),
  ],
  "kanit": ["Bitmiş proje animasyonu", "Aynı projenin render + gerçek teslim karşılaştırması",
            "Satış ofisinde kullanılan sanal tur"],
  "capraz": ["emlak-video", "drone-fpv"],
},

"emlak-video": {
  "ad": "Emlak Video Çekimi & Gayrimenkul Tanıtımı",
  "kisa": "İlanı listede öne çıkaran, ayak izini azaltan video",
  "sayfa": "hizmetler/emlak-kurumsal.html",
  "renk": "#E8452C",

  "kim": [
    "Emlak ofisi sahibi — 30+ aktif portföyü olan",
    "Bağımsız gayrimenkul danışmanı — lüks segment çalışan",
    "Site / rezidans yönetimi — kiralama yapan",
    "Butik otel ve pansiyon sahibi",
    "Arsa ve arazi satıcısı — büyük parsel elinde tutan",
  ],
  "unvan": ["Ofis sahibi / broker", "Gayrimenkul danışmanı", "Pazarlama sorumlusu"],

  "sinyal": [
    "İlanlarında sadece telefonla çekilmiş fotoğraf var",
    "Portföyünde 5 milyon TL üstü mülk var ama videosu yok",
    "İlan 60+ gündür yayında, düşmüyor",
    "Instagram hesabı var ama içerik sadece ilan görseli",
    "Sitesinde 'sanal tur' sekmesi var ama içi boş",
  ],
  "nerede": ["Sahibinden / Emlakjet / Hepsiemlak ofis sayfaları", "Google Haritalar 'emlak ofisi' + ilçe",
             "Instagram konum etiketi", "Emlak fuarları", "Broker ağı tavsiyesi"],

  "aci": [
    "İlan çok ama arayan az; gelenler ciddi değil",
    "Aynı evi günde üç kez gezdirmek zaman öldürüyor",
    "Şehir dışı alıcı 'bir de yerinde göreyim' deyip gelmiyor",
    "Lüks portföyde rakip ofis daha profesyonel görünüyor",
  ],
  "acilis": ("{firma} portföyünde {ipucu} gördüm — bu segmentte video olan ilanlar çok daha uzun "
             "inceleniyor ve gelen kişi daha nitelikli oluyor. Sizin ilanlarınız için nasıl olacağını "
             "gösteren kısa bir analiz çıkardım, atayım mı?"),

  "kanal": ["WhatsApp (birincil)", "Instagram DM", "Ofis ziyareti", "Telefon"],
  "ritim": "Aynı gün mesaj → 2. gün arama → 5. gün örnek video → 10. gün aylık paket teklifi",

  "butce": "Tek mülk düşük, aylık portföy aboneliği orta — asıl kazanç abonelikte",
  "dongu": "3 gün - 2 hafta (en kısa döngülü hizmetimiz)",
  "mevsim": "Mart-Haziran ve Eylül-Kasım en hareketli; kış aylarında lüks segment devam eder",

  "itirazlar": [
    ("Kendim telefonla çekiyorum.",
     "Telefon çekimi ilanı kurtarır ama farklılaştırmaz. Asıl fark ışık saatinde ve odaların "
     "hangi sırayla gezildiğinde — o kurgu satışı hızlandırıyor."),
    ("Ev satılırsa video boşa gider.",
     "Video satılınca da işe yarıyor: 'bu evi biz sattık' içeriği ofisinizin en iyi reklamı. "
     "Ayrıca aylık pakette maliyeti ilan başına düşüyor."),
    ("Mal sahibi izin vermiyor.",
     "Boş mülkte hiç sorun olmuyor. Dolu mülkte kişisel eşyaları kadrajdan çıkarıyoruz, "
     "istenirse dijital mobilyalama ile boş çekip döşüyoruz."),
    ("Bütçemiz yok.",
     "Ayda 4 mülk çekimiyle başlayalım; tek satışın komisyonu paketin katı. "
     "İlk ay sonuç alamazsanız devam etmeyin."),
  ],
  "kanit": ["Önce/sonra ilan performansı", "Sanal tur örneği", "Aylık paket referansı"],
  "capraz": ["insaat-3d-modelleme", "drone-fpv"],
},

"urun-animasyon": {
  "ad": "3D Ürün & Hizmet Animasyonu",
  "kisa": "Kameranın gösteremediğini gösteren anlatım",
  "sayfa": "hizmetler/urun-animasyon.html",
  "renk": "#E8452C",

  "kim": [
    "Makine imalatçısı — ihracat yapan veya yapmak isteyen",
    "Otomotiv yan sanayi — parça üreticisi",
    "Medikal / laboratuvar cihazı üreticisi",
    "İnşaat malzemesi üreticisi — uygulama anlatması gereken",
    "Mobilya üreticisi — çok varyantlı ürünü olan",
    "Yazılım / hizmet şirketi — fiziksel ürünü olmayan",
  ],
  "unvan": ["Fabrika sahibi / ortak", "İhracat müdürü", "Pazarlama müdürü", "Ar-Ge / ürün müdürü", "Fuar sorumlusu"],

  "sinyal": [
    "Fuar katılımcı listesinde adı var (önümüzdeki 3 ay)",
    "Sitesi İngilizce/Almanca ama ürün anlatımı sadece PDF katalog",
    "YouTube kanalı var, son video 2+ yıl önce",
    "Ürün sayfasında sadece stüdyo fotoğrafı, çalışma videosu yok",
    "Yeni ürün / model duyurusu yapmış",
    "İhracatçı birlikleri üye listesinde",
  ],
  "nerede": ["Fuar katılımcı listeleri (TÜYAP, Messe, Hannover)", "OSB firma rehberleri",
             "İhracatçı birlikleri üye listeleri", "Sanayi odası rehberi",
             "LinkedIn 'export manager' + sektör", "Google Haritalar 'makine imalat' + OSB"],

  "aci": [
    "Fuarda ürünü anlatmak için tercümana ve 20 dakikaya ihtiyaç var",
    "Ürünün içinde ne olduğu görünmüyor, müşteri anlamıyor",
    "Katalog PDF'i kimse sonuna kadar okumuyor",
    "Yurt dışı müşteri fabrikayı göremiyor, güven kurulamıyor",
    "Ürün gizli, hattı çekemiyoruz",
  ],
  "acilis": ("{firma}'nın {fuar} katılımını gördüm. Standda ürünü anlatan bir ekran, tercümandan "
             "hızlı iş görüyor — özellikle içi görünmeyen ürünlerde. Sizin ürününüz için nasıl bir "
             "anlatım çıkar, kısa bir sayfada topladım; bakmak ister misiniz?"),

  "kanal": ["E-posta (kurumsal, birincil)", "LinkedIn", "Telefon", "Fuarda yüz yüze"],
  "ritim": "E-posta → 4. gün LinkedIn → 8. gün arama → fuar öncesi 6 hafta yoğunlaştır",

  "butce": "Vitrin düşük-orta, teknik anlatım orta-yüksek, kurumsal hat yüksek (çok dilli)",
  "dongu": "3 hafta - 3 ay (kurumsal onay zinciri uzun; fuar tarihi varsa kısalır)",
  "mevsim": "Fuar takvimi belirler — katılımdan 8-10 hafta önce temas kur",

  "itirazlar": [
    ("Ürünümüzü zaten fotoğraflıyoruz.",
     "Fotoğraf 'nasıl göründüğünü' anlatır, animasyon 'nasıl çalıştığını'. Teknik satışta "
     "ikincisi karar verdiriyor."),
    ("Teknik çizimlerimiz gizli.",
     "Gizlilik sözleşmesi imzalıyoruz ve dosyalar bizde kalmıyor. Zaten animasyonda görünen "
     "kadarını siz belirliyorsunuz — hattı göstermeden süreci anlatmak mümkün."),
    ("Fuara az kaldı, yetişmez.",
     "Vitrin animasyonu 7-10 iş günü. Yetişecek kadar zaman varsa önce onu çıkarıp, teknik "
     "anlatımı fuardan sonraya bırakıyoruz."),
    ("Yurt dışı ajansla çalışıyoruz.",
     "Sorun değil — bizden sadece 3D modeli alıp kendi kurgunuzda kullanabilirsiniz. "
     "Model bir kez yapılır, sonra her yeni varyantta işinize yarar."),
  ],
  "kanit": ["Kesit animasyonu örneği", "Fuar döngü videosu", "Çok dilli sürüm örneği"],
  "capraz": ["isletme-tanitim", "insaat-3d-modelleme"],
},

"klip-cekimi": {
  "ad": "Klip Çekimi",
  "kisa": "Şarkıya dünya kuran prodüksiyon",
  "sayfa": "hizmetler/klip-cekimi.html",
  "renk": "#E8452C",

  "kim": [
    "Bağımsız müzisyen — yeni single çıkaracak",
    "Menajerlik / plak şirketi — sanatçı portföyü olan",
    "Marka — müzik odaklı reklam isteyen",
    "Yeni çıkan sanatçı — kimlik oluşturması gereken",
  ],
  "unvan": ["Sanatçının kendisi", "Menajer", "Plak şirketi A&R", "Marka pazarlama sorumlusu"],

  "sinyal": [
    "Spotify/YouTube'da yeni single yayınlamış, klibi yok",
    "Sosyal medyada 'stüdyodayım' içeriği paylaşıyor",
    "Önceki klibi düşük prodüksiyonlu",
    "Konser takvimi dolmaya başlamış (bütçesi var demektir)",
    "Menajerlik yeni imza atmış",
  ],
  "nerede": ["YouTube yeni yüklemeler + il", "Spotify yerel çalma listeleri", "Instagram müzik hashtag'leri",
             "Stüdyo ve prova salonu ağı", "Konser mekânları"],

  "aci": [
    "Şarkı iyi ama görsel karşılığı yok, algoritma taşımıyor",
    "Kliple şarkı aynı gün çıkmıyor, lansman dağılıyor",
    "Bütçe küçük, büyük görünen iş çıkmıyor",
    "Klip çıkıyor ama paylaşacak ek içerik kalmıyor",
  ],
  "acilis": ("{firma}'nın yeni parçasını dinledim — {ipucu}. Buna görsel olarak nasıl bir dünya "
             "kurulabileceğine dair bir fikrim var, kısaca anlatayım mı?"),

  "kanal": ["Instagram DM (birincil)", "WhatsApp", "Stüdyo/menajer tavsiyesi"],
  "ritim": "DM → 2. gün ses/konsept notu → 5. gün görüşme → lansman tarihine göre plan",

  "butce": "Tek mekân düşük-orta, senaryolu orta, lansman seti yüksek",
  "dongu": "1-4 hafta (şarkı çıkış tarihine kilitli)",
  "mevsim": "Yaz öncesi (Nisan-Haziran) ve sonbahar (Eylül-Ekim) çıkış yoğunluğu",

  "itirazlar": [
    ("Bütçem çok kısıtlı.",
     "Tek mekân paketiyle başlayalım. Çekim gününde ekstra malzeme de topluyoruz; "
     "üç haftalık sosyal medya içeriği aynı bütçeden çıkıyor."),
    ("Arkadaşım çekiyor.",
     "Sorun değil — biz kurgu ve renk tarafını devralabiliriz. Çoğu klipte fark orada oluşuyor."),
    ("Klip artık işe yaramıyor, kısa video devri.",
     "Doğru, o yüzden ana klibin yanında dikey kesimleri ve teaser'ları da teslim ediyoruz. "
     "Aynı çekimden hem klip hem kampanya çıkıyor."),
  ],
  "kanit": ["Önceki klipler", "Dikey kesim örnekleri", "Düşük bütçe/yüksek görünüm örneği"],
  "capraz": ["isletme-tanitim", "drone-fpv"],
},

"drone-fpv": {
  "ad": "Drone & FPV Çekim",
  "kisa": "Az ekibin yapabildiği havadan ve tek nefeste akan planlar",
  "sayfa": "hizmetler/drone-fpv.html",
  "renk": "#E8452C",

  "kim": [
    "İnşaat firması — şantiye ilerleme takibi isteyen",
    "Otel / tesis — konum ve çevre anlatması gereken",
    "Etkinlik organizatörü",
    "Sanayi tesisi — ölçeğini göstermek isteyen",
    "Emlak ofisi — arsa ve büyük parsel satan",
    "Belediye / kurum — tanıtım filmi yaptıran",
  ],
  "unvan": ["Proje müdürü", "Tesis müdürü", "Pazarlama sorumlusu", "Organizasyon sorumlusu"],

  "sinyal": [
    "Devam eden büyük şantiyesi var",
    "Tesisin sitesinde sadece iç mekân fotoğrafı var",
    "Yakın tarihli büyük etkinlik duyurusu",
    "Geniş arazi ilanı var, sınırları anlaşılmıyor",
  ],
  "nerede": ["Şantiye tabelaları (saha gezisi)", "Google Haritalar uydu görünümü + yeni yapı",
             "Etkinlik takvimleri", "Otel rehberleri", "İhale duyuruları"],

  "aci": [
    "Konumun avantajı anlatılamıyor",
    "Şantiye ilerlemesi yatırımcıya raporlanamıyor",
    "Tesisin ölçeği yerden anlaşılmıyor",
  ],
  "acilis": ("{firma}'nın {sehir}'daki sahasına baktım — havadan tek plan bir açılış, konumu "
             "anlatmanın en hızlı yolu. Aylık ilerleme çekimi de yatırımcı raporunuza doğrudan giriyor. "
             "Örnek göndereyim mi?"),

  "kanal": ["WhatsApp", "Telefon", "Saha ziyareti"],
  "ritim": "Mesaj → 2. gün arama → 5. gün örnek → şantiyede aylık abonelik teklifi",

  "butce": "Tek çekim düşük, aylık ilerleme aboneliği orta (en iyi tekrar eden gelir)",
  "dongu": "3 gün - 3 hafta",
  "mevsim": "Hava koşullarına bağlı; Nisan-Ekim yoğun",

  "itirazlar": [
    ("Drone'umuz var, kendimiz çekiyoruz.",
     "Çoğu firma çekiyor ama kurgu ve renk aşamasında takılıyor. İsterseniz sadece "
     "kurgu tarafını devralalım."),
    ("İzin sorunu çıkar.",
     "İzinleri biz takip ediyoruz; uçuş kısıtı olan bölgelerde alternatif plan çıkarıyoruz."),
    ("Bir kere çektirdik, yeter.",
     "Şantiyede bir kere yetmiyor — asıl değerli olan aylık seri, çünkü sonunda projenin "
     "sıfırdan yükselişini gösteren tek bir film oluyor."),
  ],
  "kanit": ["FPV tek plan örneği", "Aylık şantiye serisi", "Zaman atlamalı montaj"],
  "capraz": ["insaat-3d-modelleme", "emlak-video"],
},

"isletme-tanitim": {
  "ad": "İşletme Tanıtım & Sosyal Medya",
  "kisa": "Yerel işletme için düzenli içerik hattı",
  "sayfa": "hizmetler/isletme-tanitim.html",
  "renk": "#E8452C",

  "kim": [
    "Kafe / restoran sahibi",
    "Güzellik salonu, kuaför, klinik",
    "Spor salonu / stüdyo",
    "Butik mağaza",
    "Yerel hizmet işletmesi (oto servis, veteriner, kreş)",
  ],
  "unvan": ["İşletme sahibi", "Şube müdürü", "Sosyal medya sorumlusu (varsa)"],

  "sinyal": [
    "Instagram hesabı var ama son paylaşım 1+ ay önce",
    "Google profilinde 10'dan az fotoğraf",
    "Yorum sayısı düşük ya da yorumlara cevap verilmiyor",
    "Yeni şube açmış",
    "Menü/hizmet değişikliği yapmış ama görsel yok",
  ],
  "nerede": ["Google Haritalar + ilçe", "Instagram konum etiketi", "Yemeksepeti/Trendyol Yemek listeleri",
             "Yerel esnaf grupları"],

  "aci": [
    "İçerik üretmeye vakit yok",
    "Telefonla çekilen içerik amatör duruyor",
    "Rakip işletme sosyal medyada daha görünür",
    "Yeni müşteri hep aynı kaynaktan geliyor",
  ],
  "acilis": ("{firma}'ya baktım — {ipucu}. Ayda bir çekimle dört haftalık içeriği tek seferde "
             "çıkarabiliyoruz, sizin uğraşmanıza gerek kalmıyor. Nasıl olacağını gösteren kısa "
             "bir sayfa hazırladım."),

  "kanal": ["Instagram DM (birincil)", "WhatsApp", "Yerinde ziyaret"],
  "ritim": "DM → 3. gün ziyaret → deneme çekimi → aylık paket",

  "butce": "Aylık paket düşük-orta; hacim işi, çok sayıda müşteriyle ölçeklenir",
  "dongu": "3 gün - 2 hafta (en hızlı kapanan hizmet)",
  "mevsim": "Yıl boyu; sezon açılışları (yaz, okul dönemi, yılbaşı) pik",

  "itirazlar": [
    ("Sosyal medya bize müşteri getirmiyor.",
     "Getirmiyorsa içerik yanlış. Ölçelim: bir ay deneyip gelen aramaları sayalım, "
     "işe yaramazsa devam etmeyin."),
    ("Kendi çekiyoruz.",
     "Devam edin — biz ayda bir gelip 'omurga' içerikleri çekelim, aradaki günleri siz doldurun. "
     "En verimli karışım bu."),
    ("Pahalı.",
     "Aylık paketi bir günlük ciroyla kıyaslayın. İki yeni masa/müşteri paketi karşılıyor."),
  ],
  "kanit": ["Önce/sonra profil görünümü", "Aylık içerik seti örneği", "Yerel işletme referansı"],
  "capraz": ["urun-animasyon", "klip-cekimi"],
},

"dugun-etkinlik": {
  "ad": "Düğün & Etkinlik",
  "kisa": "Özel anın sinematik kısa filmi",
  "sayfa": "hizmetler/dugun-etkinlik.html",
  "renk": "#E8452C",

  "kim": [
    "Çift ve aileler",
    "Düğün organizasyon firmaları",
    "Düğün salonu / kır düğünü mekânı",
    "Kurumsal etkinlik ekibi (lansman, açılış, gala)",
  ],
  "unvan": ["Çift", "Organizasyon sahibi", "Mekân işletmecisi", "Kurumsal etkinlik sorumlusu"],

  "sinyal": [
    "Nişan/söz paylaşımı yapmış",
    "Salon rezervasyonu duyurusu",
    "Organizasyon firmasının takvimi dolu ama video ortağı yok",
    "Kurumsal açılış/lansman duyurusu",
  ],
  "nerede": ["Instagram nişan/düğün hashtag'leri + il", "Düğün salonu iş ortaklığı",
             "Organizasyon firmaları", "Wedding fuarları"],

  "aci": ["Gün bir kere yaşanıyor, telafisi yok", "Fotoğrafçı var ama video zayıf",
          "Salonun tanıtımı için kaliteli görüntü yok"],
  "acilis": "{firma} ile çalışan çiftlere sinematik video tarafını biz veriyoruz — mekânınızın tanıtımı da aynı çekimden çıkıyor. Ortaklık konuşalım mı?",

  "kanal": ["Instagram DM", "WhatsApp", "Salon/organizasyon ortaklığı (en verimli)"],
  "ritim": "Mekân ve organizasyoncularla ortaklık kur → yönlendirme akışı kur → bireysel takip",

  "butce": "Paket bazlı orta segment",
  "dongu": "1 gün - 6 ay (düğün tarihine göre)",
  "mevsim": "Mayıs-Eylül zirve; rezervasyon Ocak-Mart'ta alınır",

  "itirazlar": [
    ("Fotoğrafçımızın videocusu var.",
     "Çoğu paket videoyu ek olarak veriyor. Sinematik kurgu ayrı bir iş — "
     "kısa bir örnek izleyip karşılaştırın."),
    ("Bütçemiz fotoğrafa gitti.",
     "Kısa versiyon paketi var: sadece tören ve ilk dans, sinematik kurguyla."),
  ],
  "kanit": ["Düğün klibi örneği", "Mekân tanıtım videosu"],
  "capraz": ["klip-cekimi", "drone-fpv"],
},
}

# Pusula sektörlerinden hizmetlere eşleme (ayarlar.SEKTORLER ile uyumlu)
SEKTOR_HIZMET = {
  "insaat": "insaat-3d-modelleme",
  "emlak": "emlak-video",
  "mimarlik": "insaat-3d-modelleme",
  "sanayi": "urun-animasyon",
  "mobilya": "urun-animasyon",
  "otel": "emlak-video",
  "isletme": "isletme-tanitim",
}

def hizmet_getir(anahtar):
    return HIZMETLER.get(anahtar)

def sektorden_hizmet(sektor):
    return HIZMETLER.get(SEKTOR_HIZMET.get(sektor, "isletme-tanitim"))
