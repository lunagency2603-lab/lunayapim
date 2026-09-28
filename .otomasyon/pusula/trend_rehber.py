# -*- coding: utf-8 -*-
"""
TRENDSAPHIENS REHBERLERİ — kalıcı (evergreen) yazılar: her gün aranan sorunun "nasıl bakılır, nasıl
okunur" cevabı. Günlük sayfalar rakamı verir; rehber, rakamın nereden geldiğini ve nasıl doğrulanacağını.

Kural: tarih/kural bilgisi yalnızca kurumun kendi yayınına dayanır; kaynak listesi her yazının altında.
Rakam, hedef, tavsiye yok. Yazı /trend/<slug> olarak basılır; bölüm akışında kart olur.
"""

REHBERLER = [
    {
        "slug": "dolar-kac-tl-tcmb-kuru-banka-kuru-neden-farkli",
        "kat": "piyasa", "gorsel": "renk-masasi",
        "baslik": "TCMB kuru ile bankadaki dolar kuru neden farklı?",
        "ozet": "Aynı gün üç ayrı dolar kuru görürsünüz: TCMB tablosu, bankanın gişesi, döviz bürosu. Hangisi 'gerçek', hangisi ne işe yarar, saat kaçta değişir — kaynağıyla.",
        "tarih": "2026-09-03",
        "bolumler": [
            ("Üç kur var, üçü de doğru",
             "\"Dolar kaç TL\" diye arayan kişi tek bir sayı bekler; oysa aynı anda geçerli üç ayrı kur vardır. Birincisi Türkiye Cumhuriyet Merkez Bankası'nın her iş günü yayımladığı gösterge kuru: resmî hesaplamalarda, gümrükte, sözleşmelerde \"TCMB döviz satış kuru\" diye anılan rakam budur. İkincisi bankanızın uyguladığı kur: alış ve satış arasında bankanın kendi makası vardır, gün içinde defalarca değişir. Üçüncüsü serbest piyasa, yani döviz bürolarının o anki fiyatı. Haber sitelerinin ekranında akan rakam çoğunlukla bankalararası piyasanın anlık verisidir; hiçbiri yanlış değildir, ama birbirinin yerine kullanılmaz."),
            ("TCMB tablosu saat kaçta çıkar, neyi gösterir",
             "TCMB gösterge kurlarını iş günlerinde 15:30'da yayımlar; tablo o günün tarihini taşır ve ertesi iş gününe kadar geçerli sayılır. Hafta sonu ve resmî tatilde yeni tablo çıkmaz; bu yüzden pazartesi sabahı gördüğünüz TCMB kuru cuma gününün tablosudur. Tabloda dört sütun vardır: döviz alış, döviz satış (hesaptan hesaba işlemler), efektif alış, efektif satış (nakit banknot). Bizim piyasa sayfamız bu tabloyu olduğu gibi alır; rakamın yanında tablonun tarihi ve bülten numarası yazar. Tablo henüz yayımlanmadıysa bir önceki günün tarihi görünür, biz yeni bir sayı uydurmayız."),
            ("Banka kuru neden farklı",
             "Banka, dövizi sizden alırken düşük, size satarken yüksek fiyat verir; aradaki fark bankanın gelirdir ve \"makas\" denir. Makas bankadan bankaya, hatta internet şubesi ile gişe arasında değişir. Gün içinde piyasa hareketlendikçe banka kurunu anlık günceller; TCMB tablosu ise günde bir kez çıkar. Bu yüzden akşam saatlerinde banka kuru ile TCMB kuru arasındaki fark büyüyebilir. Kredi kartı ile yurt dışı harcamada uygulanan kur da bankanın o günkü satış kurudur, TCMB tablosu değil."),
            ("Hangi durumda hangi kura bakılır",
             "Faturada, sözleşmede ya da resmî bir hesaplamada \"kur\" geçiyorsa genellikle TCMB döviz satış kuru kastedilir; metinde aksi yazmıyorsa bunu esas alın. Elinizdeki dövizi bozduracaksanız bankanızın ya da döviz bürosunun alış kuruna bakın. Haber okuyorsanız ekrandaki rakam anlık piyasa verisidir; gün sonunda TCMB tablosuyla birebir tutmayabilir. \"Dolar düştü mü çıktı mı\" sorusunun cevabı hangi kura, hangi saate baktığınıza göre değişir; bu yüzden karşılaştırırken aynı kaynağın aynı saatteki rakamlarını karşılaştırın."),
            ("Bu sitede nasıl gösteriyoruz",
             "Piyasalar bölümündeki günlük sayfa TCMB'nin XML tablosunu okur, kuru olduğu gibi yazar ve alınma saatini üstte gösterir. Altın için açık bir finans beslemesi kullanılır; kaynağın adı ve güncelleme saati satırın altındadır. Yorum, hedef ve tahmin yazılmaz. Rakamın neden değiştiğini merak ediyorsanız Gündem bölümündeki kaynaklı haberlere bakabilirsiniz; orada da rakam yalnızca haberde geçiyorsa yazılır."),
        ],
        "sss": [
            ("TCMB kuru hafta sonu değişir mi?", "Hayır. Tablo yalnızca iş günlerinde 15:30'da yayımlanır; hafta sonu ve tatilde son iş gününün tablosu geçerlidir."),
            ("Haberdeki dolar ile bankadaki dolar neden tutmuyor?", "Haber ekranı anlık bankalararası piyasayı gösterir; banka kendi makasını ekler. İkisi farklı şeyleri ölçer."),
            ("Sözleşmede 'TCMB kuru' yazıyorsa hangi sütun?", "Aksi belirtilmemişse döviz satış sütunu esas alınır; kesin olmak için sözleşme metnine bakın."),
        ],
        "kaynaklar": [("TCMB — Kurlar sayfası", "https://www.tcmb.gov.tr/kurlar/kurlar_tr.html"), ("TCMB — Günlük kur tablosu (XML)", "https://www.tcmb.gov.tr/kurlar/today.xml")],
    },
    {
        "slug": "gram-altin-nasil-hesaplanir-ons-dolar",
        "kat": "piyasa", "gorsel": "render-istasyonu",
        "baslik": "Gram altın kaç TL? Ons, dolar ve 31,1 ile hesabı",
        "ozet": "Gram altın fiyatı gökten inmez: ons fiyatı, dolar kuru ve bir sabit sayıdan hesaplanır. Kuyumcu fiyatı neden farklı, çeyrek neden gramın dörtte biri değil — kaynağıyla.",
        "tarih": "2026-09-03",
        "bolumler": [
            ("Formül tek satır",
             "Dünya piyasasında altın \"ons\" başına dolarla fiyatlanır. Bir ons 31,1035 gramdır. Gram altının TL karşılığı şöyle bulunur: ons fiyatı (dolar) çarpı dolar/TL kuru, bölü 31,1035. Yani gram altın iki şeye bağlıdır: dünyada altının dolar fiyatı ve Türkiye'de doların TL fiyatı. Ons sabit kalsa bile dolar yükselirse gram altın TL bazında yükselir; bu yüzden \"altın arttı\" haberinin bir kısmı aslında kur haberidir."),
            ("Kuyumcu fiyatı neden farklı",
             "Hesapladığınız rakam \"has altın\" değeridir. Kuyumcuda gördüğünüz gram fiyatı buna işçilik, kâr payı ve alış-satış makası ekler. Çeyrek, yarım ve tam altın da gramın katı değildir: çeyrek altın 1,75 gram civarında ve 22 ayardır, yani içinde saf altın oranı daha düşüktür; üstüne darphane ve kuyumcu farkı gelir. Bu yüzden çeyrek altın fiyatı gram altının dörtte birinden her zaman farklıdır."),
            ("Fiyat gün içinde neden değişir",
             "Ons fiyatı dünya piyasalarında 24 saat işlem görür; Asya, Avrupa ve Amerika seansları birbirini izler. Dolar/TL kuru da gün içinde hareket eder. İki değişkenin çarpımı olduğu için gram altın gün içinde sürekli oynar. Bu sitedeki piyasa sayfası fiyatı her sabah ve öğleden sonra bir kez alır; rakamın yanında beslemenin güncelleme saati yazar. Anlık işlem yapacaksanız kuyumcunuzun o anki fiyatını sorun."),
            ("Neye bakarak karar verilmez",
             "Bu sayfa ve günlük piyasa sayfaları bilgi verir, alım-satım önerisi vermez. \"Altın alınır mı\" sorusuna cevap vermeyiz; geçmiş fiyat geleceği göstermez. Bir rakamı paylaşırken kaynağını ve saatini de paylaşın; sosyal medyada dolaşan ekran görüntülerinin çoğu saati ve kaynağı belirsiz olduğu için yanıltır."),
        ],
        "sss": [
            ("Ons kaç gram?", "31,1035 gram. Kısaca 31,1 diye anılır; hassas hesapta tam değer kullanılır."),
            ("Çeyrek altın neden gramın dörtte biri değil?", "Çeyrek yaklaşık 1,75 gram ve 22 ayardır; üstüne işçilik ve makas gelir."),
            ("Bu sitedeki altın fiyatı anlık mı?", "Hayır; sabah ve öğleden sonra bir kez alınır, güncelleme saati satırın altında yazar."),
        ],
        "kaynaklar": [("TCMB — Kurlar", "https://www.tcmb.gov.tr/kurlar/kurlar_tr.html"), ("Borsa İstanbul — Kıymetli Madenler Piyasası", "https://www.borsaistanbul.com/")],
    },
    {
        "slug": "mac-hangi-kanalda-yayinci-nasil-bulunur",
        "kat": "spor", "gorsel": "set-isik",
        "baslik": "Maç hangi kanalda? Yayıncıyı yanılmadan bulmanın yolu",
        "ozet": "Süper Lig, millî maç, Avrupa kupaları ve voleybol: her birinin yayıncısı ayrı ve sezon içinde değişebiliyor. Doğru kanalı ve saati üç adımda, kaynağıyla doğrulama rehberi.",
        "tarih": "2026-09-03",
        "bolumler": [
            ("Yayın hakkı organizasyona göre değişir",
             "\"Maç hangi kanalda\" sorusunun tek cevabı yoktur, çünkü yayın hakları organizasyon bazında satılır. Süper Lig'in yayıncısı ile Türkiye Kupası'nın, millî takımın, Şampiyonlar Ligi'nin ve voleybol millî takımının yayıncısı ayrı ayrı belirlenir; aynı hafta sonu üç farklı platformda maç olabilir. Üstelik haklar sezon başında ya da ihaleyle sezon ortasında el değiştirebilir. Bu yüzden geçen sezon ezberlediğiniz kanal bu sezon geçerli olmayabilir."),
            ("Üç adımda doğrulama",
             "Birinci adım: organizasyonun kendi sitesi. Türkiye Futbol Federasyonu fikstür sayfasında maç saati ve çoğu zaman yayıncı bilgisi yer alır; UEFA ve TVF de kendi fikstürlerini yayımlar. İkinci adım: yayıncının kendi yayın akışı. Kanalın internet sitesindeki \"yayın akışı\" sayfası o günün programını saatiyle gösterir; haberdeki bilgiyle çelişiyorsa yayıncı esas alınır. Üçüncü adım: tarih. Haberdeki \"hangi kanalda\" bilgisi haberin tarihine aittir; ertelenen ya da saati değişen maçlar için en güncel duyuruya bakın."),
            ("Şifreli mi, şifresiz mi",
             "Bir maçın şifresiz yayınlanıp yayınlanmayacağı da organizasyona bağlıdır. Millî takım maçları çoğu zaman ulusal bir kanalda şifresiz verilir; lig maçları ise genellikle abonelik isteyen platformlardadır. \"Şifresiz mi\" sorusunun cevabı da yayıncının duyurusundadır; tahmin yazmayız. Yasal olmayan yayın adresleri için arama yapanlar için not: bu sayfalar hem güvenlik riski taşır hem de yayın kesilir; biz yalnızca resmî yayıncıyı yazarız."),
            ("Bu sitede spor ekranı nasıl çalışır",
             "Spor Ekranı bölümündeki günlük sayfa, o gün ve hafta sonu oynanacak maçlar için haber kaynaklarındaki \"hangi kanalda, saat kaçta\" maddelerini kaynağı ve tarihiyle listeler. Skor, yorum, tahmin ve bahis içeriği yoktur. Derbi ve millî maç günleri takvim kutusunda önceden görünür; sayfa maç günü sabah yenilenir. Yanlış bir yayıncı bilgisi görürseniz iletişim sayfasından yazın; düzeltir, düzelttiğimizi not ederiz."),
        ],
        "sss": [
            ("Millî maç hangi kanalda?", "Organizasyona göre değişir; TFF'nin fikstür sayfası ve yayıncının yayın akışı kesin kaynaktır. Günün maçları Spor Ekranı sayfasında kaynağıyla listelenir."),
            ("Derbi saat kaçta?", "Saat TFF fikstüründe yazar; hava, güvenlik ya da yayın nedeniyle değişebilir, maç günü tekrar bakın."),
            ("Kanal bilgisi neden haberden habere farklı?", "Haberler farklı tarihlerde yazılmıştır; en güncel tarihli duyuru ve yayıncının kendi sayfası esastır."),
        ],
        "kaynaklar": [("Türkiye Futbol Federasyonu", "https://www.tff.org/"), ("Türkiye Voleybol Federasyonu", "https://www.tvf.org.tr/"), ("UEFA", "https://www.uefa.com/")],
    },
    {
        "slug": "vizyona-giren-filmler-ne-zaman-aciklanir-nereden-bakilir",
        "kat": "ekran", "gorsel": "renk-masasi",
        "baslik": "Bu hafta vizyona giren filmler: ne zaman açıklanır, nereden bakılır",
        "ozet": "Türkiye'de filmler cuma günü vizyona girer; liste haftanın başında belli olur. Vizyon takvimi, gişe verisi ve platform yayınları için güvenilir kaynaklar ve okuma yöntemi.",
        "tarih": "2026-09-03",
        "bolumler": [
            ("Cuma günü kuralı",
             "Türkiye'de sinema haftası cuma başlar; yeni filmler cuma vizyona girer ve gişe haftası cuma-perşembe arasıdır. Dağıtımcılar vizyon tarihlerini aylar önceden duyurur, ancak liste son haftada değişebilir: bir film ertelenir, bir başkası eklenir. Bu yüzden \"bu hafta vizyona girenler\" haberi genellikle çarşamba-perşembe kesinleşir. Dizi & Film bölümündeki haftalık sayfa cuma sabahı çıkar; her film için dağıtımcı ya da yayıncı haberinin kaynağı ve tarihi yazılır."),
            ("Nereden bakılır",
             "Vizyon listesi için en sağlam kaynak dağıtımcıların kendi duyuruları ve gişe takip sitelerinin haftalık vizyon tablolarıdır; Türkiye'de gişe verisini derleyen Box Office Türkiye haftalık listeyi ve izleyici sayılarını yayımlar. Sinema zincirlerinin seans sayfaları da o hafta hangi filmin gerçekten gösterimde olduğunu gösterir: listede olup salonda olmayan film olabilir. Dizi ve platform yayınları için ise yayıncının kendi takvim sayfası esastır; \"yeni sezon ne zaman\" sorusunun kesin cevabı yalnızca oradadır."),
            ("Öneri nasıl yazılır, nasıl yazılmaz",
             "Bu bölümde film ve dizi önerisi beğeniyle değil ölçütle yazılır: tür, süre, yönetmen, nerede izlenir, kaynak. Puan vermeyiz; fragman ve afiş yayıncının telifidir, sayfaya alınmaz. Bir yapım şirketi olarak eklediğimiz katman şu: bir sahnenin nasıl çekildiğini, hangi ışıkla kurulduğunu arada yazarız, çünkü işimiz bu. İzleyici yorumu ve spoiler içermeyiz."),
            ("Haftalık düzen",
             "Cuma sabahı vizyon listesi, cuma öğlen haftanın dizi ve platform yayınları, hafta içi ise kaynaklı tekil haberler. Her sayfa tarihle arşivlenir; \"geçen hafta ne girmişti\" sorusunun cevabı arşivde kalır. Vizyon takvimi kutusu ana sayfada her hafta cuma için işaretlidir."),
        ],
        "sss": [
            ("Filmler neden cuma vizyona giriyor?", "Türkiye'de sinema haftası cuma başlar; gişe haftası cuma-perşembe sayılır."),
            ("Liste ne zaman kesinleşir?", "Genellikle çarşamba-perşembe; dağıtımcı erteleyebilir. Cuma sabahı sayfamız son hâli kaynağıyla verir."),
            ("Dizi yeni sezon tarihini nereden öğrenirim?", "Yayıncı kanalın ya da platformun kendi duyurusundan; haberler bu duyuruya bağlanır."),
        ],
        "kaynaklar": [("Box Office Türkiye — vizyon ve gişe", "https://boxofficeturkiye.com/")],
    },
    {
        "slug": "google-trends-bugun-en-cok-aranan-listesi-nasil-okunur",
        "kat": "aranan", "gorsel": "drone-safak",
        "baslik": "\"Bugün en çok aranan\" listesi nasıl okunur: Google Trends rehberi",
        "ozet": "Türkiye bugün ne aradı sayfamız Google Trends'ten beslenir. Hacim neden 'yaklaşık', sıralama kimin, bir başlık listeye nasıl girer, haber bağlantısı neden bazen yok — dürüst bir kullanım kılavuzu.",
        "tarih": "2026-09-03",
        "bolumler": [
            ("Liste kimin",
             "Google Trends, Google aramalarında kısa sürede sıçrama yapan konuları ülke bazında listeler. Türkiye listesi gün boyunca değişir; bir başlık sabah ilk sıradayken akşam listeden düşebilir. Bizim \"Türkiye bugün ne aradı\" sayfamız bu listeyi sabah ve öğleden sonra alır, sıralamayı değiştirmez. Listede olmayan bir konuyu eklemeyiz, listedeki bir konuyu da silmeyiz; yalnızca kaynağı belirsiz olanı yayımlamayız."),
            ("Hacim neden 'yaklaşık'",
             "Trends her başlık için \"100+\", \"1.000+\", \"5.000+\" gibi bir eşik verir; bu kesin arama sayısı değil, aşılan alt sınırdır. \"5.000+\" yazan bir başlık 5 bin de aranmış olabilir, 40 bin de. Bu yüzden sayfada \"yaklaşık\" yazar ve iki başlığı hacme göre kıyaslamak yanıltıcı olabilir. Kesin rakam isteyenler için Google'ın kendi arayüzü de kesin rakam vermez; bunu bilerek okumak gerekir."),
            ("Haber bağlantısı nereden gelir",
             "Google çoğu başlığın yanına o aramayla ilişkilendirdiği bir haberi ekler: başlık, kaynak ve adres. Biz bu bağlantıyı olduğu gibi gösteririz; haberi biz seçmedik, Google eşledi. Bazı başlıklara Google haber bağlamaz; o satırda \"Google bu başlığa haber bağlamadı\" yazar ve biz kendi kafamızdan bir haber eklemeyiz. Haberin kendisi kaynağın sitesindedir; biz metnini kopyalamayız."),
            ("Bölüm eşlemesi bizim, yanılabiliriz",
             "Her başlığı hangi bölümde okuyacağınızı (spor, piyasa, dizi-film, teknoloji…) anahtar kelimelere göre biz eşleriz. Bu eşleme bazen yanılır: bir oyuncu adı hem dizi hem magazin olabilir, bir şirket adı hem borsa hem teknoloji. Yanlış eşleme görürseniz yazın; düzeltiriz. Bu sayfanın amacı Google'ın listesini okunur, kaynaklı ve tarihli biçimde arşivlemektir; günün merakını yarın da bulabilmeniz için."),
        ],
        "sss": [
            ("Listeyi siz mi hazırlıyorsunuz?", "Hayır; Google Trends'in Türkiye listesidir. Biz sıralamaya dokunmayız, yalnız kaynak ve bölüm ekleriz."),
            ("'1.000+' ne demek?", "En az bin arama; üst sınır belirsiz. Kesin sayı değildir."),
            ("Dünkü listeyi görebilir miyim?", "Evet; her gün ayrı sayfa olarak arşivlenir, Bugün Aranan bölümünden tarihe göre açılır."),
        ],
        "kaynaklar": [("Google Trends — Türkiye", "https://trends.google.com/trending?geo=TR")],
    },
    {
        "slug": "enflasyon-verisi-ne-zaman-aciklanir-tuik-takvimi",
        "kat": "piyasa", "gorsel": "render-istasyonu",
        "baslik": "Enflasyon ne zaman açıklanır? TÜİK takvimi ve rakamı doğru okuma",
        "ozet": "Her ayın başında aynı soru aranıyor: enflasyon açıklandı mı, kaç çıktı, memur ve emekli zammına ne olur. Verinin saati, kaynağı ve 'enflasyon farkı' hesabının hangi kurala dayandığı — kaynaklı, tahminsiz.",
        "tarih": "2026-09-03",
        "bolumler": [
            ("Saat 10:00, ayın ilk günleri",
             "Tüketici fiyat endeksini Türkiye İstatistik Kurumu açıklar. Veri her ay TÜİK'in yıllık ulusal veri yayımlama takviminde ilan edilen günde, sabah 10:00'da yayımlanır; bu gün çoğunlukla ayın 3'üdür, hafta sonuna denk gelirse takvimde belirtilen ilk iş gününe kayar. Kesin gün için TÜİK'in yayımlama takvimine bakılır; biz takvim kutusunda ayın 3'ünü işaretleriz, TÜİK farklı bir gün ilan ettiyse o günü esas alırız. Açıklamadan önce dolaşan \"beklenti\" rakamları anket sonuçlarıdır, veri değildir."),
            ("Aylık mı, yıllık mı",
             "Açıklamada iki rakam öne çıkar: aylık değişim (bir önceki aya göre) ve yıllık değişim (geçen yılın aynı ayına göre). Haber başlıkları çoğu zaman yıllık rakamı verir; zam hesapları ise dönemsel toplama bakar. İki rakamı karıştırmamak için TÜİK'in haber bülteninde \"bir önceki aya göre\" ve \"bir önceki yılın aynı ayına göre\" ifadelerini birlikte okuyun. Bültenin sonunda madde gruplarına göre (gıda, ulaştırma, konut…) kırılım vardır; \"benim enflasyonum\" sorusunun cevabı o tabloda aranır."),
            ("Memur ve emekli zammı hesabı neye dayanır",
             "Memur maaş artışları toplu sözleşmeyle belirlenir; sözleşmede ayrıca \"enflasyon farkı\" maddesi vardır: altı aylık TÜFE artışı, sözleşmede o dönem için verilen zam oranını aşarsa aradaki fark maaşa yansır. Emekli aylıkları için de altı aylık TÜFE değişimi esas alınır. Bu yüzden ocak ve temmuz aylarından önceki veriler daha çok aranır. Hesap, dönemin son ayı açıklanınca kesinleşir; ondan önce yazılan her rakam tahmindir. Biz tahmin yazmayız; resmî oran Resmî Gazete'de ve ilgili bakanlık duyurusunda yayımlandığında kaynağıyla veririz."),
            ("Bu sitede nasıl gösteriyoruz",
             "Piyasalar bölümünde enflasyon günü takvim kutusunda görünür; veri açıklandığında günün gündem sayfasında TÜİK bülteninin kaynağıyla yer alır. Yorum ve tahmin yapmayız; rakam yalnızca TÜİK'in bülteninde geçiyorsa yazılır. Bu sayfa bilgi amaçlıdır, mali karar için resmî kaynaklara ve uzman görüşüne başvurulmalıdır."),
        ],
        "sss": [
            ("Enflasyon saat kaçta açıklanır?", "TÜİK verileri sabah 10:00'da yayımlar; gün, yıllık yayımlama takviminde ilan edilir."),
            ("Beklenti anketi ile gerçek veri aynı şey mi?", "Hayır. Anket tahmindir; veri TÜİK bültenidir."),
            ("Enflasyon farkı ne zaman belli olur?", "Altı aylık dönemin son ayı açıklandığında; öncesi tahmindir."),
        ],
        "kaynaklar": [("TÜİK — Veri portalı", "https://data.tuik.gov.tr/"), ("Resmî Gazete", "https://www.resmigazete.gov.tr/")],
    },
    {
        "slug": "yapay-zeka-ile-uretilmis-gorsel-nasil-anlasilir-etiket",
        "kat": "teknoloji", "gorsel": "render-istasyonu",
        "baslik": "Yapay zekâ ile üretilmiş görsel nasıl anlaşılır, ne zaman etiketlenir",
        "ozet": "Gördüğünüz görsel çekim mi, üretim mi? Beş pratik ipucu, üretim araçlarının bıraktığı izler ve reklamlarda etiket kuralı — kendi işimizde nasıl uyguladığımızla birlikte.",
        "tarih": "2026-09-03",
        "bolumler": [
            ("Neden artık anlaşılmıyor",
             "İki yıl önce yapay zekâ görsellerinde altı parmaklı eller, bozuk yazılar ve erimiş arka planlar vardı. Bugünkü görüntü modelleri bu hataları büyük ölçüde geride bıraktı; fotogerçekçi bir mimari kare ya da ürün fotoğrafı ilk bakışta çekimden ayırt edilmiyor. Bu, görselin \"sahte\" olduğu anlamına gelmez; üretim aracının değiştiği anlamına gelir. Sorun, görselin nereden geldiğinin söylenmemesidir."),
            ("Beş pratik ipucu",
             "Birincisi, yazı ve logolar: üretilmiş görsellerde tabela, etiket ve kitap sırtlarındaki yazılar hâlâ sık bozulur. İkincisi, tekrar eden doku: çim, kiremit, kaldırım taşı gibi desenler doğal olmayan biçimde tekrar edebilir. Üçüncüsü, ışık tutarlılığı: gölgelerin yönü ile ışık kaynağının yeri çelişebilir. Dördüncüsü, fiziksel mantık: merdiven hiçbir yere çıkmıyorsa, pencere sayısı iki cephede tutmuyorsa üretimdir. Beşincisi, meta veri: gerçek bir fotoğrafın dosyasında kamera modeli ve çekim ayarları vardır; üretilmiş görselde çoğunlukla yoktur ya da üretim aracının adı vardır. Hiçbiri tek başına kanıt değildir; birkaçı bir arada güçlü işarettir."),
            ("Etiket kuralı ve reklamlar",
             "Türkiye'de ticari reklamlarda yapay zekâ ile üretilmiş içeriğin belirtilmesi yönünde düzenleme yürürlüğe girdi; bu sitenin blogunda düzenlemenin ne getirdiği ayrıca yazılmıştır. Kural dışında da basit bir ilke var: bir görsel müşteriye ya da izleyiciye \"gerçek\" izlenimi veriyorsa ve değilse, bunu söylemek gerekir. Etiket görseli değersizleştirmez; güveni korur."),
            ("Kendi işimizde nasıl yapıyoruz",
             "Bu sitedeki yapay zekâ ile üretilmiş her kare küçük bir etiket taşır; 3D modelleme sayfasındaki \"final kare\" örneğinde blok model ile üretilmiş kare yan yana durur ve hangisinin nereden geldiği yazar. Müşteri teslimlerinde künye zorunludur: hangi kare çekim, hangi kare render, hangi kare üretim. Bu düzen hem düzenlemeyi karşılar hem de müşterinin kendi reklamında doğru etiketi kullanmasını sağlar."),
        ],
        "sss": [
            ("Meta veri yoksa görsel kesin yapay zekâ mı?", "Hayır; sosyal medya platformları meta veriyi siler. Diğer ipuçlarıyla birlikte değerlendirin."),
            ("Etiket görselin değerini düşürür mü?", "Deneyimimiz tersini söylüyor: müşteri ne aldığını bildiğinde güven artıyor."),
            ("Kendi reklamımda etiketi nereye koymalıyım?", "Görselin üzerinde ya da hemen yanında, okunur boyutta; ayrıntı için blogdaki düzenleme yazısına bakın."),
        ],
        "kaynaklar": [("Luna Yapım — Yapay zekâ reklamında etiketleme zorunluluğu", "https://lunayapim.com/blog/yapay-zeka-reklaminda-etiketleme-zorunlulugu"), ("Ticaret Bakanlığı", "https://www.ticaret.gov.tr/")],
    },
    {
        "slug": "isletme-sosyal-medya-haftalik-paylasim-takvimi",
        "kat": "sosyal-medya", "gorsel": "set-isik",
        "baslik": "İşletme hesabı için haftalık paylaşım takvimi: gerçekten sürdürülebilen düzen",
        "ozet": "Sosyal medyada düzenli görünmenin zor tarafı fikir değil, süreklilik. İki kişilik bir stüdyonun kendi hesapları için kullandığı haftalık düzen: içerik türleri, çekim günü, arşiv mantığı ve neyi ölçmeye değer.",
        "tarih": "2026-09-03",
        "bolumler": [
            ("Önce çekim günü, sonra takvim",
             "Çoğu işletme takvimi paylaşım günlerinden başlar ve üçüncü haftada tıkanır; çünkü her gün yeni malzeme üretmek mümkün değildir. Sürdürülebilen düzen tersten kurulur: haftada bir çekim günü, o günde beş-altı parça malzeme, hafta boyunca dağıtım. Bir ürünün dört farklı açısı, bir ustanın işini yaparken üç kısa planı, bir müşterinin bir cümlelik sözü — bir öğleden sonra bir haftayı doldurur."),
            ("Beş içerik türü, döner sırayla",
             "Birincisi \"iş\": bitmiş ürünü ya da hizmeti gösteren kare. İkincisi \"süreç\": nasıl yapıldığını gösteren kısa video; en çok izlenen tür genellikle budur. Üçüncüsü \"insan\": işi yapan kişi, konuşarak ya da çalışırken. Dördüncüsü \"bilgi\": müşterinin sık sorduğu bir sorunun kısa cevabı. Beşincisi \"kanıt\": müşteri sözü, önce-sonra, rakam yalnızca doğruysa. Bu beş tür haftaya dağılır; iki gün boş kalır, boş kalması sorun değildir."),
            ("Platform kuralı değil, format kuralı",
             "Aynı malzeme dikey kısa video, kare görsel ve yatay kapak olarak üç formatta hazırlanır; hangi platformun o hafta ne istediği önemli değildir, elinizde üçü de olur. Yazı platformlarında ise aynı malzemenin bir cümlelik hâli paylaşılır. Bu sitenin TrendSaphiens yayını da böyle çalışır: her sayfa bir başlık ve bir bağlantıyla X'e sırayla gider; metin kısa, rakam sayfada, kaynak sayfada."),
            ("Neyi ölçmeli",
             "Beğeni sayısı değil, iki şey: profil ziyaretinden mesaja ya da aramaya dönen kişi sayısı ve hangi içerik türünün bunu getirdiği. Platformların kendi istatistik ekranı bunu verir; ayrı araç gerekmez. Ayda bir bakılır, takvim ona göre düzeltilir. Algoritma söylentilerini takip etmek yerine kendi hesabınızın verisine bakmak daha az yorar ve daha doğru sonuç verir."),
        ],
        "sss": [
            ("Haftada kaç paylaşım yeterli?", "Sürdürebildiğiniz kadar; beş içerik türü ve bir çekim günüyle haftada 4-5 parça rahat çıkar."),
            ("Hangi platformla başlamalı?", "Müşterinizin olduğu tek platformla; format kuralı sayesinde diğerlerine sonra aynı malzemeyle geçilir."),
            ("Reklam vermeden büyür mü?", "Yavaş ama evet; süreç ve insan içerikleri en çok bunu sağlar. Rakam vaat etmiyoruz."),
        ],
        "kaynaklar": [("Luna Yapım — Sosyal medya yönetimi", "https://lunayapim.com/hizmetler/")],
    },
    {
        "slug": "sergi-konser-tiyatro-takvimi-nereden-takip-edilir",
        "kat": "sanat", "gorsel": "renk-masasi",
        "baslik": "Sergi, konser ve tiyatro takvimi nereden takip edilir",
        "ozet": "'Bu hafta sonu ne yapılır' sorusu için kaynak listesi: devlet kurumlarının takvimleri, belediye etkinlikleri, ücretsiz sergiler ve bilet sitelerini birlikte okuma yöntemi. Bursa ve İstanbul için ayrıca.",
        "tarih": "2026-09-03",
        "bolumler": [
            ("Dört kaynak türü",
             "Sanat takvimi tek yerde toplanmaz; dört kaynağı birlikte okumak gerekir. Birincisi kamu kurumları: Devlet Tiyatroları, Devlet Opera ve Balesi ve Cumhurbaşkanlığı Senfoni Orkestrası kendi sezon programlarını yayımlar, biletler çoğunlukla düşük fiyatlıdır. İkincisi belediyeler: kültür merkezlerinin aylık programları ve ücretsiz konserler belediyenin kültür sayfasında duyurulur. Üçüncüsü özel galeriler ve müzeler: sergi açılışları galerinin kendi sitesinde ve e-bülteninde. Dördüncüsü bilet platformları: ticari konserler ve festivaller için tarih ve fiyat orada kesinleşir."),
            ("Ücretsiz etkinlik nasıl bulunur",
             "Belediye konserleri, üniversite etkinlikleri, galeri açılışları ve kütüphane söyleşileri çoğunlukla ücretsizdir ve az duyurulur. Belediyenin kültür sayfasını ve şehirdeki galerilerin sosyal hesaplarını haftada bir taramak yeter. Sanat bölümündeki haftalık sayfamız ücretsiz etkinlikleri ayrıca işaretler; kaynağı ve tarihi olmayan etkinlik listeye girmez."),
            ("Bursa ve İstanbul",
             "Bursa'da Tayyare Kültür Merkezi, Merinos Atatürk Kongre ve Kültür Merkezi ile Bursa Devlet Tiyatrosu programları şehrin ana takvimini oluşturur; belediyenin festival dönemleri ayrıca yoğundur. İstanbul için sergi yoğunluğu Beyoğlu-Karaköy hattında ve büyük müzelerdedir; bienal yılında program ayrı takip edilir. Biz her iki şehri birlikte izler, diğer illerden kaynaklı duyuruları da alırız."),
            ("Bizim eklediğimiz katman",
             "Sahne ışığı, konser kaydı ve mekân çekimi bizim işimiz. Bu yüzden sanat bölümünde arada \"bir sergi nasıl çekilir, bir konser nasıl kaydedilir\" yazıları çıkar; etkinliğinizi belgelemek isterseniz nasıl yaptığımızı orada görürsünüz. Etkinliğinizin listeye girmesi için duyurunuzun adresini iletişim sayfasından göndermeniz yeter."),
        ],
        "sss": [
            ("Ücretsiz konser nereden öğrenilir?", "Belediyenin kültür sayfası ve üniversite duyuruları; haftalık sanat sayfamız kaynağıyla işaretler."),
            ("Devlet Tiyatrosu biletleri nereden alınır?", "Kurumun kendi bilet sistemi üzerinden; program sezon başında yayımlanır."),
            ("Etkinliğimi nasıl ekletirim?", "Kaynaklı ve tarihli duyuru adresini iletişim sayfasından gönderin."),
        ],
        "kaynaklar": [("Devlet Tiyatroları", "https://www.devtiyatro.gov.tr/"), ("Devlet Opera ve Balesi", "https://www.dobgm.gov.tr/"), ("Bursa Büyükşehir Belediyesi", "https://www.bursa.bel.tr/")],
    },
]


def hepsi():
    return list(REHBERLER)


# ---------------------------------------------------------------- 28.09.2026 genişletme
DEGIS = {}   # slug -> {"degistir": {eski_baslik: (yeni_baslik, metin)}, "ekle": [(baslik, metin)], "sss": [...], "kaynak": [...]}

DEGIS["dolar-kac-tl-tcmb-kuru-banka-kuru-neden-farkli"] = {
 "degistir": {"Bu sitede nasıl gösteriyoruz": ("Günün rakamı tek adreste",
   "Günlük kur için ayrı bir sayfamız var: \"Dolar kaç TL bugün?\" sayfası TCMB'nin tablosunu her yayın turunda okur ve aynı adreste yeniden yazar. Sayfada dolar, euro ve sterlinin dört sütunu, 1-10-100-1.000 dolarlık hızlı çevirme tablosu, altın satırları ve son iki haftanın kur tablosu durur. Rakamın yanında tablonun tarihi ve bülten numarası yazar; tablo henüz yayımlanmadıysa bir önceki iş gününün rakamı görünür. Eski günlerin tam tablosu arşivdedir. Yorum, hedef ve tahmin yazılmaz.")},
 "ekle": [("Efektif kur neden daha geniş",
   "TCMB tablosundaki efektif alış ve satış, elden banknot alıp satarken geçerli olan gösterge kurlardır. Nakit dövizin taşınması, sigortası, kasada tutulması ve sahtelik kontrolü bir maliyettir; bu yüzden efektif sütunda alış ile satış arasındaki fark, hesaptan hesaba işlemlerin yapıldığı döviz sütunundan genellikle daha geniştir. Aynı durum bankada da geçerlidir: dövizi hesabınıza alıp hesapta tutmak ile gişeden banknot olarak çekmek farklı fiyatlanır. Yurt dışına nakit götürecekseniz bu farkı hesaba katın.")],
 "sss": [("Kredi kartıyla yurt dışı harcamada hangi kur uygulanır?", "Kartı veren bankanın, harcamanın hesaba geçtiği gün uyguladığı satış kuru. Bazı bankalar ayrıca yurt dışı işlem ücreti alır; ekstrede ayrı satır olarak görünür."),
         ("Dolar kuru saat kaçta belli olur?", "TCMB gösterge tablosu iş günlerinde 15:30'da yayımlanır. Banka ve piyasa kurları ise gün boyunca değişir.")],
}

DEGIS["gram-altin-nasil-hesaplanir-ons-dolar"] = {
 "degistir": {"Fiyat gün içinde neden değişir": ("Fiyat gün içinde neden değişir",
   "Ons fiyatı dünya piyasalarında hafta içi neredeyse kesintisiz işlem görür; Asya, Avrupa ve Amerika seansları birbirini izler. Dolar/TL kuru da gün içinde hareket eder. İki değişkenin çarpımı olduğu için gram altın gün içinde sürekli oynar. Günün rakamını \"Dolar kaç TL bugün?\" sayfasındaki altın tablosunda, beslemenin güncelleme saatiyle birlikte görebilirsiniz; bu rakam yayın turunda alınır, anlık değildir. Anlık işlem yapacaksanız kuyumcunuzun ya da bankanızın o anki fiyatını sorun.")},
 "ekle": [("Örnek hesap",
   "Formülü bir örnekle okuyalım; rakamlar bugünün fiyatı değil, hesabı göstermek için seçilmiş yuvarlak sayılardır. Ons 2.000 dolar, dolar 40 TL olsun. 2.000 × 40 = 80.000; bunu 31,1035'e bölünce gram başına yaklaşık 2.572 TL çıkar. Şimdi ons aynı kalsın, dolar 42 TL'ye çıksın: 2.000 × 42 / 31,1035 ≈ 2.701 TL. Dünyada altının fiyatı hiç değişmediği hâlde gram altın yaklaşık yüzde 5 artmış görünür; artışın tamamı kurdan gelir. Tersine, ons düşerken dolar yükselirse gram altın yerinde sayabilir. Haberde \"altın rekor kırdı\" yazıyorsa hangisinin rekor kırdığına bakın: ons mu, gram mı?"),
  ("Ayar ne demek",
   "Ayar, bir altın ürünün içindeki saf altın oranıdır ve binde olarak da yazılır. 24 ayar neredeyse saf altındır (999,9 binde); gram altın ve külçe bu ayardadır. 22 ayar binde 916 altın içerir; bilezik ve Cumhuriyet altınları (çeyrek, yarım, tam) bu ayardadır. 18 ayar binde 750, 14 ayar binde 585 altındır; takılarda yaygındır. Bir takının has altın değeri, gramı ile ayar oranının çarpımıdır; üstüne işçilik eklenir. Bu yüzden aynı gramdaki 14 ayar bir kolye ile 22 ayar bir bilezik çok farklı fiyatlanır.")],
 "sss": [("22 ayar ile 24 ayar arasındaki fark nedir?", "24 ayar neredeyse saf altındır; 22 ayar binde 916 altın içerir. Bilezik ve Cumhuriyet altınları 22 ayar, gram altın ve külçe 24 ayardır."),
         ("Gram altın hafta sonu değişir mi?", "Dünya piyasası hafta sonu kapalıdır; kuyumcular kendi makaslarıyla fiyat vermeye devam edebilir, bu fiyat pazartesi açılışta yeniden oluşur.")],
}

DEGIS["mac-hangi-kanalda-yayinci-nasil-bulunur"] = {
 "degistir": {"Bu sitede spor ekranı nasıl çalışır": ("Bu sitede maç yazıları nasıl çıkar",
   "Spor bölümünde derbi, millî maç ve büyük Avrupa maçları için ayrı yazı çıkar: maçın tarihi, saati ve yayıncısı, federasyonun ve yayıncının duyurusuna dayanarak yazılır; iki kaynak çelişiyorsa ikisi de adıyla belirtilir. Skor tahmini, yorum ve bahis içeriği yoktur. Maç günü yaklaşan büyük karşılaşmalar ana sayfadaki takvim kutusunda görünür. Yanlış bir yayıncı bilgisi görürseniz iletişim sayfasından yazın; düzeltir, düzelttiğimizi sayfada not ederiz.")},
 "ekle": [("Yurt dışından izlerken",
   "Yayın hakları ülke bazında satılır. Türkiye'deki yayıncının internet yayını çoğunlukla yalnız Türkiye'den izlenebilir; yurt dışındaysanız o ülkedeki hak sahibine bakmanız gerekir. Avrupa kupaları için organizasyonun kendi sitesi ülke ülke yayıncı listesi yayımlar. Millî takım maçlarında da durum aynıdır: aynı maç Türkiye'de bir kanalda, Almanya'da başka bir kanalda verilir. Yurt dışında yaşayan okurlarımızın en sık yaptığı hata, Türkiye'deki kanalın adını arayıp bulunduğu ülkede yayın aramasıdır."),
  ("Saat karışıklığı",
   "Avrupa kupası maçlarının saati organizasyonun sitesinde çoğu zaman bulunduğunuz yerin saatine göre gösterilir; Türk basınında ise Türkiye saati (TSİ) yazılır. Kış aylarında Avrupa'nın büyük bölümü saatini geri alırken Türkiye almadığı için aynı maçın Türkiye saati yaz ve kış arasında bir saat kayar. Maç saatini bir haberden okuduysanız haberin TSİ yazıp yazmadığına bakın.")],
 "sss": [("Maç ertelenirse nereden öğrenirim?", "Federasyonun duyurusu ve kulübün resmî hesabı ilk kaynaktır; yayıncı yayın akışını buna göre günceller."),
         ("Yurt dışında Türk maçları nasıl izlenir?", "Bulunduğunuz ülkedeki yayın hakkı sahibinden; organizasyonların sitelerinde ülke bazında yayıncı listesi bulunur.")],
}

DEGIS["vizyona-giren-filmler-ne-zaman-aciklanir-nereden-bakilir"] = {
 "degistir": {"Haftalık düzen": ("Bu sitede nasıl yazıyoruz",
   "Ekran bölümünde vizyon haftası, festival programı ve dizilerin yeni sezonu için ayrı yazılar çıkar. Her yazıda film ya da dizinin tarihi dağıtımcının veya yayıncının duyurusuna dayanır ve kaynak adıyla belirtilir; tarih açıklanmamışsa \"henüz açıklanmadı\" yazar, tahmin yürütmeyiz. Yazılar tarihle arşivlenir; \"geçen ay neler girmişti\" sorusunun cevabı bölüm sayfasında kalır.")},
 "ekle": [("Ön gösterim ve seans",
   "Bazı filmler cuma öncesi perşembe akşamı ön gösterimle başlar; ön gösterim seansları sinema zincirlerinin uygulama ve sitelerinde normal seanslardan ayrı listelenir. Bir film vizyon listesindeyken şehrinizdeki salonda olmayabilir: salon sayısı dağıtımcı ile sinema işletmesi arasında belirlenir. İzlemek istediğiniz film için en doğru kaynak, gideceğiniz salonun o haftaki seans listesidir; liste genellikle perşembe günü kesinleşir."),
  ("Dijital platformlar",
   "Platform filmleri ve dizileri sinema takvimine bağlı değildir; yayın günü ve saati platformun kendi duyurusunda yazar. Sinemada gösterilen bir filmin platforma ne zaman geleceği ise dağıtım anlaşmasına bağlıdır ve önceden bilinmeyebilir. \"Bu film hangi platformda\" sorusunun kesin cevabı platformun kendi arama sayfasındadır; haberlerdeki tarih değişebilir.")],
 "sss": [("Film vizyondan ne zaman kalkar?", "Sabit bir süre yoktur; salon programı haftalık belirlenir, izleyici azaldıkça seans sayısı düşer."),
         ("Ön gösterim nedir?", "Resmî vizyon gününden önce, genellikle perşembe akşamı yapılan ilk gösterimlerdir; seansları ayrıca listelenir.")],
}

DEGIS["google-trends-bugun-en-cok-aranan-listesi-nasil-okunur"] = {
 "degistir": {"Haber bağlantısı nereden gelir": ("Haber bilgisi nereden gelir",
   "Google çoğu başlığın yanına o aramayla ilişkilendirdiği bir haberi ekler. Bizim listemizde haberin kaynağı adıyla yazar; başka yayıncının metnini kopyalamayız ve dış bağlantı vermeyiz. Bir başlığı kendimiz araştırıp yazdıysak, o satır doğrudan kendi yazımıza gider: ne oldu, neden arandı, kaynaklarıyla. Google'ın haber bağlamadığı başlıklarda satırda bunu açıkça belirtiriz ve kendi kafamızdan bir haber eklemeyiz.")},
 "ekle": [("Trend, en çok aranan demek değildir",
   "Liste bir konunun kısa sürede ne kadar sıçradığını ölçer, toplam arama sayısını değil. \"Hava durumu\" ya da \"döviz\" gibi her gün çok aranan konular, aramaları olağan düzeyde seyrettiği için listeye girmeyebilir; buna karşılık birkaç saat içinde aniden aranmaya başlayan bir isim ilk sıraya çıkabilir. Bu yüzden listeyi \"Türkiye'nin gündemi\" diye değil, \"Türkiye'nin o gün aniden merak ettiği şeyler\" diye okumak daha doğrudur."),
  ("Kendiniz nasıl bakarsınız",
   "Google Trends'in \"Şu anda trend olanlar\" bölümünde ülke olarak Türkiye'yi seçip listeyi kendiniz görebilirsiniz. Süre filtresiyle son 4 saat, 24 saat, 48 saat ya da 7 günün sıçramalarına bakılabilir; kategori filtresi spor, eğlence, iş gibi alanları ayırır. Bir başlığa tıklayınca aramanın ne zaman başladığı ve ilişkili sorgular görünür. Kesin arama sayısı bu ekranda da yoktur; eşik değerleri kıyas için kullanılır.")],
 "sss": [("Bir başlık neden birkaç gün listede kalır?", "Konu birkaç gün boyunca yeni gelişmelerle aranmaya devam ediyorsa her gün yeniden sıçrama yapar; günlük sayfalarda bu \"devreden başlık\" olarak görünür."),
         ("Listede neden bazı önemli haberler yok?", "Liste sıçramayı ölçer; önemli ama beklenen bir haber, arama sayısı olağan seyrettiği için listeye girmeyebilir.")],
}

DEGIS["enflasyon-verisi-ne-zaman-aciklanir-tuik-takvimi"] = {
 "degistir": {"Bu sitede nasıl gösteriyoruz": ("Bu sitede nasıl gösteriyoruz",
   "Enflasyon günü ana sayfadaki takvim kutusunda önceden işaretlidir. Veri açıklandığında haber bölümünde TÜİK bülteninin kaynağıyla bir yazı çıkar: aylık ve yıllık oran, 12 aylık ortalama ve kira artışına etkisi. Yorum ve tahmin yapmayız; rakam yalnızca TÜİK'in bülteninde geçiyorsa yazılır. Bu sayfa bilgi amaçlıdır; mali karar için resmî kaynaklara ve uzman görüşüne başvurulmalıdır.")},
 "ekle": [("Kira artışında hangi rakam geçerli",
   "Konut kiralarında yıllık artış için yasal üst sınır, Türk Borçlar Kanunu'nun 344. maddesine göre bir önceki kira yılında TÜFE'nin on iki aylık ortalamalara göre değişimidir. Bu oran TÜİK bülteninde \"on iki aylık ortalamalara göre\" satırında yer alır; haber başlıklarındaki yıllık enflasyonla aynı rakam değildir. Kira sözleşmeniz hangi ayda yenileniyorsa, o aydan önce açıklanan son bültendeki on iki aylık ortalama rakamına bakılır. İşyeri kiralarında da aynı ölçüt uygulanır; sözleşmede daha düşük bir oran yazıyorsa sözleşme geçerlidir."),
  ("TÜFE ile ÜFE farkı",
   "TÜFE, hanelerin satın aldığı mal ve hizmetlerin fiyat değişimini ölçer; maaş, emekli aylığı ve kira hesaplarında esas alınan budur. Yurt içi üretici fiyat endeksi (Yİ-ÜFE) ise üreticinin sattığı malların fiyatını ölçer ve aynı gün açıklanır. Ticari sözleşmelerde ve bazı vergi hesaplarında Yİ-ÜFE geçebilir; hangi endeksin geçerli olduğu sözleşme ya da mevzuat metninde yazar.")],
 "sss": [("Kira artışı için hangi oran kullanılır?", "Bir önceki kira yılının TÜFE on iki aylık ortalamalara göre değişimi; TÜİK bülteninde ayrı satırda yer alır."),
         ("Yıllık enflasyon ile 12 aylık ortalama aynı şey mi?", "Hayır. Yıllık oran geçen yılın aynı ayına göre değişimdir; 12 aylık ortalama son on iki ayın ortalamasını önceki on iki ayla karşılaştırır.")],
 "kaynak": [("Türk Borçlar Kanunu md. 344", "https://www.mevzuat.gov.tr/mevzuatmetin/1.5.6098.pdf")],
}

DEGIS["yapay-zeka-ile-uretilmis-gorsel-nasil-anlasilir-etiket"] = {
 "ekle": [("İçerik kimlik bilgisi ve görünmez filigran",
   "Bazı görsel üretim araçları ve kamera üreticileri, dosyanın içine \"içerik kimlik bilgisi\" (C2PA standardı) ekler: görselin hangi araçla üretildiği ya da düzenlendiği bu kayıtta yazar ve herkese açık doğrulama sitelerinde okunabilir. Google da kendi modelleriyle üretilen görsellere SynthID adlı, gözle görülmeyen bir filigran ekliyor. Bu işaretler güçlü bir kanıttır ama her zaman yoktur: kayıt eklemeyen araçlar var, ekran görüntüsü alınınca ya da sosyal medyaya yüklenince dosya içindeki kayıt çoğunlukla silinir. Bu yüzden işaretin olması kesin sonuç verir, olmaması ise hiçbir şey kanıtlamaz."),
  ("Ters görsel araması",
   "Bir görselin nereden çıktığını anlamanın en hızlı yolu ters görsel aramasıdır: görseli arama motorunun görsel arama bölümüne yükleyin ya da bağlantısını verin. Görsel daha önce bir haber ajansında, bir fotoğrafçının arşivinde ya da bir stok sitesinde yayımlandıysa ilk kaynağı ve tarihi çoğunlukla bulunur. Hiçbir yerde önceki bir kaydı yoksa ve yukarıdaki ipuçlarından birkaçı da görülüyorsa, görselin üretilmiş olma ihtimali yükselir.")],
 "sss": [("Ekran görüntüsü alınınca yapay zekâ kaydı kalır mı?", "Dosyaya gömülü içerik kimlik bilgisi çoğunlukla silinir; görünmez filigranlar bazı düzenlemelere dayanabilir ama kesin değildir."),
         ("Ters görsel araması ne işe yarar?", "Görselin daha önce nerede ve ne zaman yayımlandığını gösterir; ilk kaynağı bulmanın en hızlı yoludur.")],
 "kaynak": [("Content Credentials (C2PA)", "https://contentcredentials.org/")],
}

DEGIS["isletme-sosyal-medya-haftalik-paylasim-takvimi"] = {
 "ekle": [("Örnek bir hafta",
   "Kafe örneğiyle: pazartesi öğleden sonra bir saatlik çekim — yeni tatlının dört açısı, hazırlanışının üç kısa planı, baristanın bir cümlelik önerisi, bir müşterinin izniyle kısa sözü. Salı sabahı tatlının bitmiş karesi (iş), çarşamba hazırlanış videosu (süreç), perşembe baristanın önerisi (insan), cuma \"şekersiz seçenek var mı\" sorusunun cevabı (bilgi), cumartesi müşterinin sözü (kanıt). Pazar ve pazartesi boş kalır. Toplam hazırlık bir öğleden sonra ve her gün beş dakikalık paylaşım."),
  ("Ayda bir yapılacak kontrol",
   "Ay sonunda üç soruya bakın. Hangi içerik türü en çok mesaj ya da arama getirdi? Hangi gün ve saatte paylaşılan içerik daha çok izlendi? Hangi tür hiç karşılık bulmadı? Karşılık bulmayan türü bırakmak yerine bir ay farklı biçimde deneyin: aynı ürünü süreç yerine insan üzerinden anlatmak gibi. Takvimi bu üç cevaba göre değiştirin; platformların istatistik ekranı bu soruların hepsini cevaplar.")],
 "sss": [("Çekimi telefonla yapabilir miyiz?", "Evet; iyi ışık ve sabit tutuş çoğu işletme içeriği için yeterlidir. Profesyonel çekim tanıtım filmi ve reklam için ayrılabilir."),
         ("Hangi saatte paylaşmak gerekir?", "Genel bir doğru saat yoktur; kendi hesabınızın istatistik ekranı takipçilerinizin çevrimiçi olduğu saatleri gösterir.")],
}

DEGIS["sergi-konser-tiyatro-takvimi-nereden-takip-edilir"] = {
 "degistir": {"Ücretsiz etkinlik nasıl bulunur": ("Ücretsiz etkinlik nasıl bulunur",
   "Belediye konserleri, üniversite etkinlikleri, galeri açılışları ve kütüphane söyleşileri çoğunlukla ücretsizdir ve az duyurulur. Belediyenin kültür sayfasını ve şehirdeki galerilerin sosyal hesaplarını haftada bir taramak yeter. Sanat bölümünde yoğun haftalar için konser ve etkinlik takvimi yazıları çıkar; bu yazılarda ücretsiz etkinlikler ayrıca belirtilir, kaynağı ve tarihi olmayan etkinlik listeye girmez.")},
 "ekle": [("Bilet alırken dikkat edilecekler",
   "Bileti etkinliğin resmî satış kanalından alın; organizatörün duyurusunda hangi platformun yetkili olduğu yazar. İkinci el satışlarda sahte ya da iptal edilmiş bilet riski yüksektir ve etkinlik iptal edilirse iade alınamayabilir. İade ve değişim koşulları organizatöre göre değişir; satın almadan önce etkinlik sayfasındaki koşulları okuyun. Etkinlik ertelenir ya da iptal edilirse duyuru genellikle bilet platformundan ve e-postayla gelir; iade de aynı kanal üzerinden yapılır."),
  ("Sezon ne zaman başlar",
   "Kamu tiyatroları ve opera-bale sezonları genellikle ekim ayında açılır, mayıs-haziranda kapanır; sezon programı ve bilet satış tarihleri kurumların sitesinde sezon başından önce duyurulur. Yaz aylarında salonlardan çok açık hava konserleri ve festivaller öne çıkar. Galeriler ise sergi programını genellikle sonbahar ve ilkbaharda yoğunlaştırır; açılış davetleri çoğu zaman herkese açıktır.")],
 "sss": [("İptal edilen etkinliğin bileti nasıl iade edilir?", "Bileti aldığınız resmî platform üzerinden; iade koşullarını organizatör belirler ve duyurusunu yapar."),
         ("Tiyatro sezonu ne zaman başlar?", "Kamu tiyatrolarında genellikle ekimde; program ve satış tarihleri kurumların sitesinde önceden duyurulur.")],
}


def _genislet():
    for r in REHBERLER:
        d = DEGIS.get(r["slug"])
        if not d:
            continue
        bol = list(r["bolumler"])
        for eski, (yeni, metin) in d.get("degistir", {}).items():
            bol = [(yeni, metin) if h == eski else (h, p) for h, p in bol]
        mevcut = {h for h, _ in bol}
        # yeni bölümler, sitenin kendini anlattığı son bölümden ÖNCE girer
        son = bol[-1] if bol and ("sitede" in bol[-1][0].lower() or "bizim" in bol[-1][0].lower() or "tek adreste" in bol[-1][0].lower() or "nasıl yazıyoruz" in bol[-1][0].lower() or "maç yazıları" in bol[-1][0].lower()) else None
        govde = bol[:-1] if son else bol
        for h, p in d.get("ekle", []):
            if h not in mevcut:
                govde.append((h, p))
        r["bolumler"] = govde + ([son] if son else [])
        sorular = {q for q, _ in r.get("sss", [])}
        r["sss"] = list(r.get("sss", [])) + [x for x in d.get("sss", []) if x[0] not in sorular]
        kay = {a for a, _ in r.get("kaynaklar", [])}
        r["kaynaklar"] = list(r.get("kaynaklar", [])) + [x for x in d.get("kaynak", []) if x[0] not in kay]
        r["guncelleme"] = "2026-09-28"


_genislet()
