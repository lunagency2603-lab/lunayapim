# -*- coding: utf-8 -*-
"""
KILAVUZ — panelin kendi içindeki kullanım rehberi.

İçerik tek yerde duruyor; hem paneldeki "Kılavuz" sekmesi hem de
KILAVUZ.md dosyası buradan üretiliyor. Böylece ikisi asla ayrışmıyor.

Yazarken tek kural: bir maddeyi okuyan kişi ne yapacağını bilecek.
"Sistemi kullanın" değil, "şu düğmeye bas, şu çıkar" diyor.
"""
import os, datetime


# ============================================================ ilk gün
BASLANGIC = [
 ("Paneli aç",
  "Luna Pusula klasöründe <b>Panel.command</b> dosyasına çift tıkla. "
  "Siyah bir pencere açılır ve tarayıcıda panel gelir. "
  "O pencereyi kapatma — panel o pencerede çalışıyor.",
  "Panel açılmazsa: pencerede yazan hata satırını olduğu gibi kopyala."),
 ("Adını yaz",
  "Panel ilk açılışta adını sorar. İki kişi kullanacağı için her temas ve "
  "iş kaydının yanında kimin yaptığı yazsın diye.",
  "Sonradan değiştirmek için Kılavuz sekmesinin en altındaki alanı kullan."),
 ("Ayarlar sekmesini bir kere doldur",
  "Google anahtarı, imza, e-posta ve SMTP bilgileri. Bir kere yazılıyor, "
  "<code>ayarlar.json</code>'a kaydediliyor, bilgisayardan çıkmıyor.",
  "Google anahtarı yoksa sistem OpenStreetMap ile çalışır — daha az veri ama çalışır."),
 ("İkinci bilgisayarı bağla",
  "<b>Aynı Wi-Fi'deyseniz</b> Panel-Ag.command'a çift tıkla; bağlantı panoya "
  "kopyalanır. <b>Farklı ev/şehirdeyseniz</b> Panel-Uzak.command'a çift tıkla ve "
  "bu sayfadaki Uzaktan erişim bölümünden tüneli başlat.",
  "Uzaktan erişimde karşı tarafa sadece adresi ve sekiz haneli PIN'i söylüyorsun; "
  "uzun bağlantı yapıştırmak yok."),
]


# ============================================================ haftalık ritim
RITIM = [
 ("Her sabah — 10 dakika", [
   "<b>Raf</b> sekmesi: bugün takip edilecekler listesi. Söz verilen günü geçirme.",
   "<b>Gündem</b> sekmesi: taze haber var mı, bizim söyleyecek sözümüz olan bir konu çıktı mı.",
 ]),
 ("Haftada bir — 1 saat", [
   "<b>Tarama</b>: bir şehir + bir sektör seç, başlat. 30-40 aday yeter, "
   "yüzlerce aday çıkarıp hiçbirine dokunmamaktan iyidir.",
   "<b>Adaylar</b>: skoru düşük olanlardan başla (en çok eksiği olan = en çok "
   "anlatacak şeyimiz olan). Beş tanesini seç, <b>Dosya çıkar</b>.",
   "<b>Adaylar</b> → WhatsApp düğmesi: mesaj hazır açılır, temas kaydı otomatik düşer.",
 ]),
 ("Ayda bir — yarım gün", [
   "<b>Arama</b>: Search Console'dan CSV indir, panele bırak. Hangi şehirde "
   "kaç tıklanma aldık, nerede gösteriliyoruz ama tıklanmıyoruz.",
   "<b>Arama</b> alt bölümü: GA4 dosyasını bırak — günlük ziyaretçi, hangi "
   "sayfa, kaç kişi iletişim butonuna bastı.",
   "<b>Arama</b> → Site sağlığı → <b>Şimdi tara</b>: 331 sayfa kategori kategori "
   "denetlenir, bir önceki ölçümle farkı gösterilir.",
   "<b>Üretim</b>: kazanılan işleri aşama aşama ilerlet. Teslim tarihi geçen iş kırmızıya döner.",
 ]),
 ("Talep geldiğinde — 5 dakika", [
   "<b>Talep</b> sekmesi: müşterinin mesajını olduğu gibi yapıştır, "
   "<b>Yanıt taslağı üret</b>. Fiyat bandı, dürüst sınır ve iki hazır yanıt çıkar.",
   "Taslağı olduğu gibi göndermek zorunda değilsin — rakamı ve gerekçeyi al, "
   "kendi cümlelerinle yaz.",
 ]),
]


# ============================================================ sekme sözlüğü
SEKMELER = [
 ("Tarama", "Şehir + sektör seçip yeni aday bulur. Beş adım canlı akar.",
  "Yeni aday lazım olduğunda"),
 ("Hedef Kitle", "Her hizmet için kim, hangi unvan, hangi acı noktası, hangi kanal.",
  "Ne söyleyeceğini bilemediğinde"),
 ("Adaylar", "Bulunan firmalar, karneleri ve eksikleri. Dosya çıkarma ve WhatsApp burada.",
  "Her gün"),
 ("Raf", "CRM. Kimi aradık, ne dedi, ne zaman tekrar dönülecek.",
  "Her sabah"),
 ("Piyasa", "Rakip ajans fiyat ortalamaları ve duyduğun teklifleri kaydetme.",
  "Fiyat verirken"),
 ("Huni", "Aday → temas → görüşme → teklif → kazanıldı. Nerede tıkanıyoruz.",
  "Haftada bir"),
 ("Üretim", "Kazanılan işin teklif aşamasından teslime kadar takibi.",
  "İş kazanınca"),
 ("Arama", "Search Console + GA4 + site sağlığı. Sitenin gerçek verisi.",
  "Ayda bir"),
 ("Gündem", "Günlük haberlerden bizim yazabileceğimiz blog konuları.",
  "Her sabah"),
 ("Talep", "Gelen müşteri mesajından fiyat bandı ve hazır yanıt.",
  "Talep geldiğinde"),
 ("İstatistik", "Sayılar, dağılımlar ve dışarı verilebilir arşiv sayfası.",
  "Ayda bir"),
 ("Ayarlar", "Anahtarlar, imza, SMTP, eşikler, kazanç varsayımları.",
  "Bir kere"),
 ("Kılavuz", "Bu sayfa. İş akışı, sık sorunlar ve talep yazma şablonu.",
  "Takıldığında"),
]


# ============================================================ sık karşılaşılanlar
SORUNLAR = [
 ("Tarama yarıda kaldı / hata verdi",
  "Aynı taramayı tekrar başlat. Sistem daha önce araştırılmış adayları atlıyor, "
  "kaldığı yerden devam ediyor. Aynı hata ikinci kez gelirse pencereden hata "
  "satırını kopyalayıp Claude'a ilet."),
 ("GitHub Desktop 'A lock file already exists' diyor",
  "Ayarlar sekmesi → <b>Depo durumu</b> → kilidi çöz. Çalışan bir git işlemi "
  "varsa dokunmuyor, önce onun bitmesini bekle."),
 ("Ziyaretçi bölümü boş",
  "GA4 kimliği girilmemiş olabilir (Ayarlar → Ölçüm) ya da henüz dosya "
  "yüklenmemiştir. Sistem uydurma rakam üretmiyor, o yüzden boş duruyor."),
 ("Sosyal medya bölümünde 'okunamadı' yazıyor",
  "Bu bir hata değil. Sayfa giriş duvarı arkasında ya da o an açılmadı. "
  "'Hesap yok' demiyoruz çünkü bilmiyoruz — müşterinin karşısında yanlış "
  "bilgi vermektense boş bırakıyoruz."),
 ("İkinci bilgisayarda panel açılmıyor",
  "Üç şeye bak: (1) ana bilgisayarda Panel-Ag.command penceresi hâlâ açık mı, "
  "(2) iki bilgisayar aynı Wi-Fi'de mi, (3) bağlantının sonundaki "
  "<code>?anahtar=…</code> kısmı kırpılmadan gitti mi (bazı uygulamalar uzun "
  "bağlantıyı kesiyor — kesiliyorsa <b>bilgisayar adlı</b> ikinci adresi gönder). "
  "Yönlendirici IP'yi değiştirmiş olabilir; o durumda da bilgisayar adlı adres çalışır."),
 ("Aynı anda ikimiz de yazarsak veri bozulur mu",
  "Hayır. Veritabanı tek bilgisayarda duruyor, ikinci bilgisayar sadece "
  "tarayıcıyla bağlanıyor. Ama <b>pusula.db dosyasını iCloud/Dropbox'a "
  "koyup iki makinede birden açmayın</b> — o gerçekten veri bozar."),
 ("Aynı ağda değiliz",
  "O zaman Panel-Ag.command hiç işe yaramaz — ağ kipi sadece aynı Wi-Fi içindir. "
  "<b>Panel-Uzak.command</b>'ı kullan: Cloudflare tüneli açılır, dışarıya tek bir "
  "https adresi çıkar. Karşı taraf adrese girip PIN'i yazar. Kalıcı adres için "
  "bu sayfadaki Uzaktan erişim bölümündeki altı adımı bir kez yap."),
 ("Eşim giriş ekranını görüyor ama giremiyor",
  "PIN yanlış girilmiştir. PIN sekiz hane ve bu sayfanın Uzaktan erişim "
  "bölümünde yazıyor — boşlukla yazması sorun değil, sistem boşluğu atıyor. "
  "Beş yanlış denemeden sonra on dakika kilitleniyor; bu kasıtlı, panelde "
  "müşteri telefonu ve ciro var."),
 ("Uzak adres bir süre sonra çalışmıyor",
  "Hızlı tünelin adresi geçicidir: panel ya da tünel kapanınca ölür, her "
  "başlatmada değişir. Her gün yeni adres göndermemek için kalıcı adres "
  "kurulumunu (altı adım) bir kez yapın."),
 ("Fiyat bandını değiştirmek istiyorum",
  "İki yerde birden değişmeli: sitedeki hizmet sayfası ve <code>pusula/talep.py</code>. "
  "Talep sekmesinin altındaki tablo bu yüzden orada. Tek başına birini "
  "değiştirirsen sistem müşteriye başka, site başka rakam söyler."),
]


# ============================================================ Claude'a talep yazma
TALEP_KURALI = [
 ("Ne olmasını istediğini yaz, çözümü değil",
  "\"Adaylar sekmesine sıralama düğmesi ekle\" yerine \"en çok eksiği olan "
  "firmayı önce görmek istiyorum\" de. İkincisi daha iyi bir çözüm çıkarır."),
 ("Hata varsa satırı olduğu gibi kopyala",
  "Ekrandaki kırmızı yazıyı ya da terminal penceresindeki son satırları "
  "olduğu gibi yapıştır. \"Çalışmadı\" tek başına hiçbir şey anlatmıyor."),
 ("Hangi sekmede olduğunu söyle",
  "Sistemde on üç sekme var; hangisinde olduğunu yazmak aramayı kısaltıyor."),
 ("Ne beklediğini yaz",
  "\"Şunu görmeyi bekliyordum, bunu gördüm\" — arada fark varsa hata orada."),
 ("Uydurmasını isteme",
  "Elimizde olmayan rakamı, referansı ya da yorumu sisteme koymuyoruz. "
  "Bir yer boşsa sebebi budur; doldurmak için gerçek veri gerekiyor."),
]

# Panelde form doldurulunca üretilen metnin iskeleti.
TALEP_SABLON = """[{sekme}] {baslik}

Ne yapmak istedim:
{niyet}

Ne bekliyordum:
{beklenen}

Ne oldu:
{olan}

{hata_blok}Aciliyet: {aciliyet}
Bildiren: {kim} · {tarih}
"""

ORNEK_TALEP = [
 {"iyi": True,
  "baslik": "Aday listesinde en zayıf firmayı önce görmek",
  "metin": ("[Adaylar] Aday listesinde en zayıf firmayı önce görmek\n\n"
            "Ne yapmak istedim:\nBursa mobilya taramasından çıkan 38 adayın içinden "
            "hangisine önce yazacağıma karar vermek.\n\n"
            "Ne bekliyordum:\nEn çok eksiği olan, yani bize en çok anlatacak şey "
            "bırakan firmanın en üstte olmasını.\n\n"
            "Ne oldu:\nListe firma adına göre sıralı geliyor, tek tek skorlara "
            "bakmam gerekiyor.\n\n"
            "Aciliyet: Bu hafta\nBildiren: Elif · 29.08.2026"),
  "neden": "Ne istediğini değil neyi çözmek istediğini yazmış; çözüm bize kalmış."},
 {"iyi": True,
  "baslik": "Tarama hata verdi",
  "metin": ("[Tarama] Tarama 3. adımda düştü\n\n"
            "Ne yapmak istedim:\nEskişehir + emlak taraması, 40 aday.\n\n"
            "Ne bekliyordum:\nAltı adımın da tamamlanmasını.\n\n"
            "Ne oldu:\n3/6 İletişim araştırması adımında durdu, aday listesi yarım kaldı.\n\n"
            "Hata satırı:\nsqlite3.OperationalError: database is locked\n"
            "  File \"pusula/veritabani.py\", line 306, in kanal_ekle\n\n"
            "Aciliyet: Acil — yarın sunum var\nBildiren: Elif · 29.08.2026"),
  "neden": "Hata satırı olduğu gibi kopyalanmış. Sebep bu satırdan bulunuyor."},
 {"iyi": False,
  "baslik": "Sistem çalışmıyor",
  "metin": "sistem çalışmıyor bir bak",
  "neden": ("Hangi sekme, ne yapmaya çalıştın, ne gördün — hiçbiri yok. "
            "Cevap gelmeden önce üç soru sorulması gerekir, yarım gün kaybolur.")},
 {"iyi": False,
  "baslik": "Rakam uydurma isteği",
  "metin": "aday sayfalarına takipçi ve etkileşim rakamı koy dolu gözüksün",
  "neden": ("Elimizde olmayan rakam sisteme girmiyor. Müşteri kendi hesabının "
            "rakamını bizden daha iyi biliyor; yanlış rakam gördüğü an "
            "raporun tamamına güvenmiyor. Gerçek veri girilecek alan zaten var.")},
]


# ============================================================ değişmeyen kurallar
ILKELER = [
 ("Uzaktan erişim ancak kapıyla olur",
  "Panel tünelle internete açıldığında 'bu bilgisayar serbest' muafiyeti "
  "kapanıyor — tünelin trafiği de bu bilgisayardan geldiği için o muafiyet "
  "açık kalsaydı panel herkese açılırdı. Girmek isteyen herkes PIN ya da "
  "Cloudflare Access ile geçiyor. Şifresiz açma (port yönlendirme, ngrok) yok."),
 ("Panel yayına çıkmaz",
  "lunayapim.com Cloudflare Pages üzerinde statik; şifre konulamıyor. Panel "
  "yayına konsaydı müşteri telefonları ve ciro herkese açık olurdu. Dışarı "
  "bir şey göstermek gerekirse İstatistik sekmesindeki arşiv çıktısı kullanılır."),
 ("Kişi kazıma yok",
  "LinkedIn/Instagram içine girip kişi bilgisi toplanmıyor — platform "
  "şartlarına aykırı ve KVKK riski. Firmanın kendi sitesinde yayınladığı "
  "bilgi, kaynak adresiyle toplanıyor."),
 ("Uydurma rakam yok",
  "Takipçi, etkileşim, ziyaretçi — ölçülemeyeni boş bırakıyoruz. Örnek "
  "kurgular 'bu bir kurgudur' etiketiyle çıkıyor."),
 ("Blog metnini insan yazar",
  "Gündem sekmesi konuyu ve iskeleti veriyor; metni siz yazıyorsunuz. "
  "Yapay zekâyla doldurulup yayınlanmış içerik üretmiyoruz."),
 ("Toplu e-postada sorumluluk sizde",
  "Ticari ileti için İYS kaydı ve KVKK aydınlatma yükümlülüğü var. Sistem "
  "tek tek gönderim için kurulu, toplu gönderim aracı değil."),
]


# ============================================================ sayfa anlatımları
# Her sekmenin başında görünen "burada ne yapıyoruz" kutusu.
# Kural: okuyan kişi ne yapacağını bilecek. Teknik ayrıntı yok.
SAYFA = {
 "tarama": {
   "amac": "Müşterinin bize yazmasını beklemek yerine biz gidip buluyoruz. "
           "Bu sayfa, seçtiğin şehirdeki firmaları bulup her birinin sitesini "
           "ve dijital görünürlüğünü tek tek inceliyor.",
   "adim": [
     "Şehri ve sektörü seç.",
     "Taramayı başlat ve ekranda akan adımları izle — birkaç dakika sürüyor.",
     "Bittiğinde hiçbir şey yapman gerekmiyor, sonuç kendiliğinden düşüyor.",
   ],
   "sonra": "Bulunan firmalar <b>Adaylar</b> sayfasına, karneleriyle birlikte geçiyor.",
   "ipucu": "Bir seferde 30–40 aday yeter. Yüzlerce aday çıkarıp hiçbirine "
            "dokunmamak, otuz adayla konuşmaktan kötüdür.",
 },
 "fabrika": {
   "amac": "Hangi hizmeti kime, hangi cümleyle anlatacağımız burada yazılı. "
           "Karşındaki kişinin derdi ne, ne duymak istiyor, hangi itirazı yapar.",
   "adim": [
     "Anlatacağın hizmeti seç.",
     "Karşındaki kişinin acı noktasını ve açılış cümlesini oku.",
     "İtirazlar bölümüne göz at — telefonda hazırlıksız yakalanma.",
   ],
   "sonra": "Buradaki cümleleri Adaylar sayfasında mesaj yazarken kullanıyorsun.",
   "ipucu": "Satış konuşması ezberlemek değil amaç. Tek bir doğru cümle, "
            "beş paragraf tanıtımdan daha çok cevap getiriyor.",
 },
 "adaylar": {
   "amac": "Bulunan her firmanın karnesi. Neyi eksik, bu eksik ona ne "
           "kaybettiriyor ve biz ne yapabiliriz — hepsi kanıtıyla birlikte.",
   "adim": [
     "Puanı en düşük olandan başla: en çok eksiği olan, bize en çok "
     "anlatacak şey bırakan firmadır.",
     "Firmaya tıkla; eksikleri, sosyal medyası ve önerilen çözümü aç.",
     "<b>Dosya çıkar</b> — o firmaya özel analiz, teklif ve çekim planı hazırlanır.",
     "<b>WhatsApp</b> düğmesi mesajı hazır açar; sen sadece gönder.",
   ],
   "sonra": "Mesajı gönderdiğin an firma <b>Raf</b>'a düşüyor ve takip başlıyor.",
   "ipucu": "Dosyayı göndermeden önce bir kez kendin oku. Müşteriye giden "
            "her şeyin arkasında durabiliyor olmalıyız.",
 },
 "raf": {
   "amac": "Kimi aradık, ne dedi, ne zaman geri döneceğiz. Hiçbir şey akılda "
           "tutulmuyor — söz verilen gün burada yazıyor.",
   "adim": [
     "Sabah ilk iş burayı aç.",
     "<b>Bugün takip edilecekler</b> listesindekileri bitir.",
     "Her görüşmeden sonra sonucu kaydet; firma bir sonraki aşamaya geçer.",
   ],
   "sonra": "Görüşme olumluya dönerse teklif aşamasına, oradan <b>Üretim</b>'e geçiyor.",
   "ipucu": "İşi kaybettiren şey genelde kötü teklif değil, unutulan takip. "
            "Bu liste her sabah boşalmalı.",
 },
 "piyasa": {
   "amac": "Fiyat verirken piyasanın nerede olduğunu bilelim. Ne para bırakalım "
           "ne de işi kaçıralım.",
   "adim": [
     "Hizmeti ve şehri seç, aralığa bak.",
     "Müşteriden duyduğun rakip teklifi kaydet.",
   ],
   "sonra": "Birkaç kayıttan sonra kendi gerçek ortalamamız öne çıkıyor ve "
            "aralık bizim piyasamıza göre şekilleniyor.",
   "ipucu": "Buradaki rakamlar çapa; pazarlık masasında güven veriyor.",
 },
 "huni": {
   "amac": "Nerede tıkanıyoruz? Mesaj mı atmıyoruz, görüşme mi olmuyor, "
           "teklif mi kapanmıyor — darboğazı gösteriyor.",
   "adim": [
     "Haftada bir bak.",
     "En dar basamağı bul ve o hafta oraya yüklen.",
   ],
   "sonra": "Darboğaz nerede ise haftalık planın da orası olmalı.",
   "ipucu": "Aday sayısını artırmak her zaman çözüm değil. Çoğu zaman sorun "
            "üstte değil, ortada oluyor.",
 },
 "uretim": {
   "amac": "Kazanılan işin tekliften teslime kadar takibi. Hangi iş hangi "
           "aşamada, teslime ne kadar kaldı.",
   "adim": [
     "İş kazanınca buraya ekle: müşteri, hizmet, bedel, teslim tarihi.",
     "İş ilerledikçe aşamasını güncelle.",
   ],
   "sonra": "Teslim edilen iş kapanıyor ve ciroya işleniyor.",
   "ipucu": "Teslim tarihini müşteriye söylerken buraya bak — açık iş "
            "sayısını görmeden söz vermek en pahalı hata.",
 },
 "arama": {
   "amac": "Kendi sitemizin gerçek durumu. Kaç kişi geldi, hangi sayfaya baktı, "
           "kaç kişi iletişim butonuna bastı, hangi şehirde görünüyoruz.",
   "adim": [
     "Google'dan indirdiğin arama dosyasını buraya bırak.",
     "Ziyaretçi dosyasını da aynı şekilde bırak.",
     "<b>Site sağlığı → Şimdi tara</b> ile sitenin tamamını denetle.",
   ],
   "sonra": "Çıkan eksikleri buradan konuşup sırayla kapatıyoruz.",
   "ipucu": "Rakam boş görünüyorsa uydurulmadığı içindir. Dosya yüklenince doluyor.",
 },
 "gundem": {
   "amac": "Günün haberleri içinden bizim söyleyecek sözümüz olanları ayıklıyor. "
           "Amaç haber paylaşmak değil, o konuda bilen taraf olarak görünmek.",
   "adim": [
     "Sabah aç, önerilenlere bak.",
     "Uygun bir konu varsa seç — bölüm başlıklı bir taslak çıkıyor.",
     "Metni sen yazıyorsun; her bölümün altında ne yazılacağı not düşülü.",
   ],
   "sonra": "Yazı bitince tek tuşla siteye ekleniyor ve arama motorlarına bildiriliyor.",
   "ipucu": "Gündem yazısı bir haftada bayatlar. Yazacaksan o hafta yaz; "
            "yazamayacaksan Makale sekmesindeki kalıcı konulara geç.",
 },
 "sorgu": {
  "baslik": "Arama Gündemi",
  "ozet": "İnsanların bugün ne arattığını derler ve siteye basar.",
  "adimlar": [
   "Bugünü derle — tohum kelimeler genişletilir, sorgular puanlanır.",
   "Yazıya değer sorgular listesine bak; sitede karşılığı olmayanlar orada.",
   "Siteye bas — /yapay-zeka/ sayfası yenilenir.",
   "GitHub Desktop → Commit → Push origin ile yayına al.",
  ],
  "kural": "Otomatik tamamlama sıra verir, hacim vermez. Sitede de sıra yazıyor.",
 },
 "makale": {
   "amac": "Sitenin arama tarafındaki yüzeyini büyütmek. Hizmet sayfaları "
           "\"biz ne yapıyoruz\" diyor; makaleler müşterinin sorduğu soruya "
           "cevap veriyor. Aranan şey çoğu zaman ikincisi.",
   "adim": [
     "Konuyu seç, <b>Üret ve puanla</b>'ya bas — yazı ve 100 üzerinden karnesi çıkıyor.",
     "Eksik madde varsa yanında ne yapılacağı yazıyor.",
     "Puan 100 olunca <b>Yayınla</b> açılıyor; yazı siteye basılıyor.",
     "GitHub Desktop → Commit → Push origin ile yayına gidiyor.",
   ],
   "sonra": "Yayınlanan yazı blog indeksine ve site haritasına kendiliğinden giriyor.",
   "ipucu": "100 puan \"bu yazı iyi\" demek değil, \"biçimsel olarak eksiksiz\" "
            "demek. İyi olup olmadığına biz karar veriyoruz; sistem yalnızca "
            "eksik yazının yayınlanmasını engelliyor.",
 },
 "talep": {
   "amac": "Gelen müşteri mesajına ne cevap vereceğimiz. Fiyatı her seferinde "
           "sıfırdan düşünmek yerine, işin hangi banda oturduğunu çıkarıyor.",
   "adim": [
     "Müşterinin mesajını olduğu gibi yapıştır.",
     "<b>Yanıt taslağı üret</b>'e bas.",
     "Fiyat bandını, gerekçesini ve hazır yanıtı al.",
   ],
   "sonra": "Taslağı olduğu gibi göndermek zorunda değilsin — rakamı ve gerekçeyi "
            "alıp kendi cümlelerinle yazabilirsin.",
   "ipucu": "Fiyatı yukarı çeken kalemler müşteriye de gösteriliyor. Pazarlık "
            "değil, şeffaflık — pahalı görünmüyor, gerekçeli görünüyor.",
 },
 "istatistik": {
   "amac": "Toplu resim: kaç aday var, kaçıyla konuştuk, kaç iş kazandık, ne kadar ciro.",
   "adim": [
     "Ayda bir bak.",
     "Dışarıya göstermen gereken bir özet varsa arşiv çıktısı al.",
   ],
   "sonra": "Aylık planı bu sayfadaki eğilime göre kuruyoruz.",
   "ipucu": "Tek bir ayın rakamı bir şey söylemez; üç ayın yönü söyler.",
 },
 "ayarlar": {
   "amac": "Bir kere doldurulup unutulacak bilgiler: imza, e-posta, ölçüm "
           "kimlikleri ve fiyat varsayımları.",
   "adim": [
     "Boş alanları doldur, kaydet.",
     "Bir daha buraya nadiren geleceksin.",
   ],
   "sonra": "Buradaki bilgiler müşteriye giden tüm belgelerde kullanılıyor.",
   "ipucu": "Hepsi bu bilgisayarda kalıyor, dışarı gitmiyor.",
 },
}


# ============================================================ süreç zinciri
# Bir firmanın baştan sona geçtiği yol. Kılavuzun kalbi bu.
SUREC = [
 ("Buluyoruz", "Tarama",
  "Şehir ve sektör seçiyoruz; firmalar bulunup her biri tek tek inceleniyor."),
 ("Neyi eksik görüyoruz", "Adaylar",
  "Her firmanın karnesi çıkıyor: sitesi, sosyal medyası, görünürlüğü. "
  "Eksiklerin her biri kanıtıyla duruyor."),
 ("Ne söyleyeceğimizi hazırlıyoruz", "Adaylar → Dosya çıkar",
  "O firmaya özel analiz, teklif, çekim planı ve mesaj hazırlanıyor."),
 ("Yazıyoruz", "Adaylar → WhatsApp",
  "Mesaj hazır açılıyor. Amaç satmak değil, cevap almak: tek eksik, tek fikir, tek soru."),
 ("Takip ediyoruz", "Raf",
  "Kim ne dedi, ne zaman dönülecek. Söz verilen gün geçirilmiyor."),
 ("Fiyat veriyoruz", "Piyasa + Talep",
  "Piyasanın nerede olduğuna bakıp bandı belirliyoruz; gerekçesiyle birlikte."),
 ("Üretiyoruz", "Üretim",
  "Kazanılan iş aşama aşama teslime gidiyor."),
 ("Kendi evimizi topluyoruz", "Arama + Gündem",
  "Kendi sitemizin ziyaretçisini, sıralamasını ve eksiklerini ölçüyoruz. "
  "Kendi işimizi yapamıyorsak kimseye anlatamayız."),
]


# ============================================================ dışa aktarım
_SEKME_ANAHTAR = {
 "Tarama": "tarama", "Hedef Kitle": "fabrika", "Adaylar": "adaylar", "Raf": "raf",
 "Piyasa": "piyasa", "Huni": "huni", "Üretim": "uretim", "Arama": "arama",
 "Gündem": "gundem", "Arama Gündemi": "sorgu", "Makale": "makale", "Talep": "talep", "İstatistik": "istatistik",
 "Ayarlar": "ayarlar", "Kılavuz": "kilavuz",
}


def _sekme_anahtar(ad):
    return _SEKME_ANAHTAR.get(ad, "")


def veri():
    """Panelin okuduğu sözlük."""
    return {
        "baslangic": [{"baslik": a, "metin": b, "not": c} for a, b, c in BASLANGIC],
        "ritim": [{"baslik": a, "maddeler": b} for a, b in RITIM],
        "sekmeler": [{"ad": a, "ne": b, "ne_zaman": c} for a, b, c in SEKMELER],
        "sorunlar": [{"baslik": a, "cozum": b} for a, b in SORUNLAR],
        "talep_kurali": [{"baslik": a, "metin": b} for a, b in TALEP_KURALI],
        "ornek": ORNEK_TALEP,
        "ilkeler": [{"baslik": a, "metin": b} for a, b in ILKELER],
        "sayfa": SAYFA,
        "surec": [{"asama": a, "nerede": b, "metin": c} for a, b, c in SUREC],
    }


def talep_metni(sekme, baslik, niyet, beklenen, olan, hata="", aciliyet="", kim=""):
    """Formdan gelen alanları Claude'a yapıştırılabilir tek metne çeviriyor."""
    hb = ("Hata satırı:\n%s\n\n" % hata.strip()) if hata.strip() else ""
    return TALEP_SABLON.format(
        sekme=(sekme or "Genel").strip(),
        baslik=(baslik or "Başlıksız").strip(),
        niyet=(niyet or "—").strip(),
        beklenen=(beklenen or "—").strip(),
        olan=(olan or "—").strip(),
        hata_blok=hb,
        aciliyet=(aciliyet or "Acil değil").strip(),
        kim=(kim or "—").strip(),
        tarih=datetime.date.today().strftime("%d.%m.%Y"),
    )


def _md_kacis(s):
    return (s or "").replace("<b>", "**").replace("</b>", "**") \
                    .replace("<code>", "`").replace("</code>", "`")


def markdown():
    """KILAVUZ.md içeriği."""
    y = []
    y.append("# Luna Pusula — Kullanım Kılavuzu\n")
    y.append("_Bu dosya panelin **Kılavuz** sekmesiyle aynı kaynaktan üretiliyor._\n")

    y.append("\n## İlk gün\n")
    for i, (a, b, c) in enumerate(BASLANGIC, 1):
        y.append("%d. **%s** — %s" % (i, a, _md_kacis(b)))
        y.append("   > %s" % _md_kacis(c))

    y.append("\n## Ritim\n")
    for a, mad in RITIM:
        y.append("### %s\n" % a)
        for m in mad:
            y.append("- %s" % _md_kacis(m))
        y.append("")

    y.append("\n## Süreç — bir firma baştan sona nasıl ilerliyor\n")
    for i, (a, b, c) in enumerate(SUREC, 1):
        y.append("%d. **%s** _(%s)_ — %s" % (i, a, b, _md_kacis(c)))

    y.append("\n## Sayfa sayfa ne yapıyoruz\n")
    for anahtar, ad, _ in SEKMELER:
        d = SAYFA.get(anahtar.lower()) or SAYFA.get(_sekme_anahtar(anahtar))
        if not d:
            continue
        y.append("### %s\n" % anahtar)
        y.append(_md_kacis(d["amac"]) + "\n")
        for j, ad_ in enumerate(d["adim"], 1):
            y.append("%d. %s" % (j, _md_kacis(ad_)))
        y.append("\n**Sonra ne oluyor:** %s" % _md_kacis(d["sonra"]))
        if d.get("ipucu"):
            y.append("\n> %s" % _md_kacis(d["ipucu"]))
        y.append("")

    y.append("\n## Hangi sekme ne işe yarar\n")
    y.append("| Sekme | Ne yapar | Ne zaman |")
    y.append("|---|---|---|")
    for a, b, c in SEKMELER:
        y.append("| **%s** | %s | %s |" % (a, _md_kacis(b), c))

    y.append("\n## Sık karşılaşılanlar\n")
    for a, b in SORUNLAR:
        y.append("**%s**\n\n%s\n" % (a, _md_kacis(b)))

    y.append("\n## Claude'a talep nasıl yazılır\n")
    for a, b in TALEP_KURALI:
        y.append("- **%s** — %s" % (a, _md_kacis(b)))
    y.append("\n### Örnekler\n")
    for o in ORNEK_TALEP:
        y.append("**%s — %s**\n" % ("İYİ" if o["iyi"] else "YETERSİZ", o["baslik"]))
        y.append("```\n%s\n```\n" % o["metin"])
        y.append("> %s\n" % o["neden"])

    y.append("\n## Değişmeyen kurallar\n")
    for a, b in ILKELER:
        y.append("**%s** — %s\n" % (a, _md_kacis(b)))

    y.append("\n---\n_Üretim tarihi: %s_\n" % datetime.date.today().strftime("%d.%m.%Y"))
    return "\n".join(y)


def yaz(kok):
    yol = os.path.join(kok, "KILAVUZ.md")
    with open(yol, "w", encoding="utf-8") as f:
        f.write(markdown())
    return yol
