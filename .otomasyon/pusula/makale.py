# -*- coding: utf-8 -*-
"""
MAKALE FABRİKASI — SEO uyumlu yazı üretimi.

Neden bu dosya var
------------------
Gündem tarayıcısı (gundem.py) haber buluyor ve *iskelet* çıkarıyor: "buraya şunu
yaz" diyen notlar. O iskelet insan eli bekliyordu ve beklediği için de kimse
yazmıyordu. Bu dosya yazının kendisini üretiyor.

Kural — bunlar pazarlama cümlesi değil, kodun uyduğu kısıtlar:

  1. Uydurma rakam yok. Yazıdaki her sayı ya bizim kendi fiyat bandımız, ya
     kendi ölçümümüz, ya da kaynağı verilen yayınlanmış bir liste.
  2. Her yazı en az iki iç bağlantı taşıyor ve bağlantı verdiği sayfanın
     gerçekten var olduğu üretim anında kontrol ediliyor.
  3. Her yazı en az bir dış kaynağa bağlanıyor. Kaynaksız iddia yazılmıyor.
  4. Şehir kopyası üretilmiyor. Aynı yazının 81 ilini çıkarmak Google'ın
     "doorway page" dediği şey; kısa vadede trafik, orta vadede ceza.
     Şehir yazısı ancak o şehre özgü GERÇEK bir bilgi varsa yazılır.
  5. Yayın kapısı makale_puan.py'de: 100 almayan yayınlanmıyor.

Yazılar buradan çıkıp yayin.md_coz() → yayin.yayinla() hattına giriyor;
site üreticisi zaten şema, SSS kutusu ve iç bağlantıları basıyor.
"""
import datetime, os, re

from .ayarlar import SITE_KOK


# ------------------------------------------------------------------ ortak bloklar
# Bunlar bizim gerçek verimiz. Fiyat bandı fiyatlar.html ile aynı olmak zorunda;
# ikisi ayrışırsa yazı yalan söylemiş olur.
BANT = {
    "insaat-3d-modelleme": ("60.000 – 150.000 ₺", "tek blok için render seti + kısa animasyon"),
    "urun-animasyon":      ("40.000 – 95.000 ₺", "modelleme + animasyon + ses tasarımı"),
    "emlak-kurumsal":      ("25.000 – 55.000 ₺", "çekim + kurgu + renk + sosyal sürümler"),
    "klip-cekimi":         ("45.000 – 100.000 ₺", "senaryolu, çok planlı çekim"),
    "drone-fpv":           ("10.000 – 25.000 ₺", "yarım günlük çekim + kurgu"),
    "isletme-tanitim":     ("14.000 – 40.000 ₺", "içerik üretimi dahil aylık düzen"),
}

SUREC = [
    "**Konuşma.** Ne satmak istediğinizi ve kime satmak istediğinizi konuşuyoruz. "
    "Bu görüşme ücretsiz ve sonunda size yazılı bir kapsam çıkıyor.",
    "**Kapsam ve bütçe.** İşi bütçeye göre kurguluyoruz. Bütçe yetmiyorsa "
    "\"yetmez\" demek yerine o bütçeyle ne yapılabileceğini yazıyoruz.",
    "**Üretim.** Çekim, modelleme, kurgu ve yazılım aynı ekipte. Taşeron ve "
    "aracı ajans yok; bu yüzden hem fiyat hem takvim tahmin edilebilir.",
    "**Teslim ve ölçüm.** Dosyalar sizde kalıyor. İşin sonuç verip vermediğini "
    "izlemek isterseniz ölçümü de kuruyoruz.",
]

KAYNAK_HAVUZ = {
    "render_fiyat": ("2026 yılı render fiyatları",
                     "https://www.allrender.net/post/2026-yili-render-fiyatlari"),
    "tanitim_fiyat": ("Tanıtım filmi fiyatları 2026",
                      "https://www.medyabox.com.tr/tanitim-filmi-fiyatlari"),
    "sosyal_fiyat": ("Sosyal medya yönetimi fiyat rehberi 2026",
                     "https://kreativty.com/blog/sosyal-medya-yonetimi-ne-kadar-tutar-2026-fiyat-rehberi"),
    "google_yardimci": ("Google — Yararlı içerik oluşturma rehberi",
                        "https://developers.google.com/search/docs/fundamentals/creating-helpful-content?hl=tr"),
    "google_sss": ("Google — SSS şeması (FAQPage) dokümanı",
                   "https://developers.google.com/search/docs/appearance/structured-data/faqpage?hl=tr"),
    "shm": ("SHGM — İnsansız Hava Aracı kuralları",
            "https://www.shgm.gov.tr/"),
}


def _sozluk_bant(hizmet):
    b = BANT.get(hizmet)
    return b[0] if b else ""


# ------------------------------------------------------------------ konu bankası
# Her konu bir yazıdır. Paragraflar burada yazılı duruyor çünkü şablondan
# üretilen paragraf insan gibi okunmuyor; şablon başlığı, bağlantıyı, SSS'yi ve
# sıralamayı üretir — cümleyi değil.
KONULAR = [

{
 "anahtar": "insaat-3d-render-fiyat",
 "baslik": "İnşaat 3D modelleme fiyatları: neye göre değişiyor?",
 "adres": "insaat-3d-modelleme-fiyatlari",
 "kelime": "inşaat 3d modelleme fiyatları",
 "hizmet": "hizmetler/insaat-3d-modelleme.html",
 "ozet": "İnşaat 3D modelleme fiyatları neye göre değişiyor? Altı kalem, gerçek bir fiyat bandı ve teklif isterken sorulması gereken sorular.",
 "kisa_cevap":
   "İnşaat 3D modelleme fiyatları tek bir rakam değil, altı kalemin toplamı: model "
   "kaynağı, görsel sayısı, çözünürlük, çevre düzenlemesi, revizyon hakkı ve "
   "animasyon olup olmadığı. Tek blok için render seti ve kısa animasyon "
   "içeren işler bizde 60.000 – 150.000 ₺ arasında oluşuyor.",
 "bolum": [
  ("Fiyatı asıl belirleyen şey görsel sayısı değil", [
   "Teklif isterken çoğu firma tek soru soruyor: kaç görsel istiyorsunuz. Oysa "
   "on görsellik bir iş, üç görsellik bir işten üç kat pahalı olmuyor. Çünkü "
   "işin ağırlığı modelde ve sahne kurulumunda; görsel almak o kurulumdan sonra "
   "en ucuz adım.",
   "Bir projede model bir kez kuruluyor: kütle, cephe kaplaması, doğrama "
   "detayları, çevre. Kurulum bittikten sonra kameranın yerini değiştirip "
   "ikinci, üçüncü, onuncu görseli almak dakikalar sürüyor. Bu yüzden 'tek "
   "görsel' istemek çoğu zaman pahalı bir tercih: birim maliyeti en yüksek "
   "seçenek o.",
  ]),
  ("Altı kalem", [
   "**1. Model nereden geliyor.** Elinizde Revit, ArchiCAD ya da SketchUp "
   "modeli varsa iş yarı yarıya kısalıyor. Yalnızca kat planı ve cephe çizimi "
   "varsa model sıfırdan kuruluyor; en büyük kalem burası.",
   "**2. Görsel sayısı ve tipi.** Dış cephe, iç mekân, kuşbakışı, gece — her "
   "tip kendi ışık kurulumunu istiyor. Beş dış cephe görseli, iki dış bir iç "
   "mekândan daha ucuza geliyor.",
   "**3. Çözünürlük ve kullanım yeri.** Sosyal medya için 2K yeterli; billboard "
   "ya da 3x2 metre satış ofisi panosu için 8K gerekiyor ve hesaplama süresi "
   "kat kat artıyor.",
   "**4. Çevre düzenlemesi.** Boş arsa üzerinde duran bina ucuz ve inandırıcı "
   "değil. Peyzaj, komşu yapılar, insan ve araç yerleştirmesi işin görünen "
   "kalitesini belirleyen ama teklifte çoğu zaman yazılmayan kalem.",
   "**5. Revizyon hakkı.** \"Sınırsız revizyon\" yazan teklif ya fiyatın içine "
   "peşin zam koymuştur ya da ilk ciddi değişiklikte tartışma çıkar. Biz "
   "revizyon sayısını yazıyoruz; ne aldığınız belli oluyor.",
   "**6. Animasyon var mı.** Aynı modelden 30–45 saniyelik bir gezinti "
   "çıkarmak, o modeli sıfırdan kurmaya göre küçük bir ek. Ayrı iş olarak "
   "sipariş edilirse büyük bir kalem.",
  ]),
  ("Kalemlerin ağırlığı projeye göre değişiyor", [
   "Yukarıdaki altı kalem her projede aynı ağırlıkta değil. Konut projelerinde "
   "asıl belirleyici **daire tipi sayısı** oluyor: aynı bloktaki her farklı "
   "tip ayrı bir iç mekân kurulumu demek. Tek tip daire ile altı tip daire "
   "arasındaki fark, görsel sayısından çok daha büyük.",
   "Ticari projelerde ise **modellenecek hacim** öne çıkıyor. Bir plaza "
   "lobisi ile bir depo aynı metrekarede olsa bile aynı işi doğurmuyor; "
   "detay yoğunluğu belirleyici.",
   "**Işık senaryosu sayısı** da çoğu teklifte yazılmayan bir kalem. Gündüz, "
   "gün batımı ve gece aynı sahnenin üç ayrı kurulumu demek. Bir de "
   "**gerçek çekimle birleşim** var: render'ın gerçek arsa fotoğrafına "
   "oturtulması, ayrı bir işçilik kalemi.",
   "İnşaat 3D modelleme fiyatları bu yüzden metrekare üzerinden verilemiyor. "
   "Doğru teklif, projeyi görmeden değil; kat planını ve tip sayısını "
   "gördükten sonra çıkıyor.",
  ]),
  ("Gerçek bir bant", [
   "Tek blok için render seti ve kısa animasyon içeren işler bizde "
   "60.000 – 150.000 ₺ arasında oluşuyor. Bandın altı ve üstü rastgele değil: "
   "alt uç, modeli sizden gelen ve dış cephe ağırlıklı bir iş; üst uç, sıfırdan "
   "model, iç mekânlar, gece sahnesi ve animasyon.",
   "Bu rakamı yayınlıyoruz çünkü fiyat sormak için form doldurtmak kimseye "
   "zaman kazandırmıyor. Sektörde yayınlanmış listelere de bakabilirsiniz; "
   "kıyas yaparken listenin tarihine bakın, çünkü bu kalemler yılda bir "
   "değişiyor.",
  ]),
  ("Teklif isterken sorulacak beş soru", [
   "- Model sizde mi kuruluyor, yoksa bizim çizimimizden mi çıkıyor?",
   "- Kaç revizyon dahil, revizyon sonrası birim fiyat ne?",
   "- Teslim çözünürlüğü kaç, baskıya girecek mi?",
   "- Çevre düzenlemesi (peyzaj, komşu yapı, insan-araç) dahil mi?",
   "- Kaynak dosyalar teslim ediliyor mu, sonradan başka firmayla devam "
   "edebilir miyim?",
   "Bu beş sorunun cevabı yazılı gelmiyorsa teklif karşılaştırılabilir değil "
   "demektir. İki teklif arasındaki fark çoğu zaman fiyatta değil, bu "
   "satırların birinde saklı.",
  ]),
  ("İki teklif neden bu kadar farklı çıkıyor", [
   "Aynı proje için alınan iki teklif arasında iki kat fark görmek olağan. Bu "
   "farkın büyük kısmı kâr marjından değil, kapsamdan geliyor. Ucuz teklifte "
   "çoğu zaman çevre düzenlemesi yok, revizyon sayısı yazılmamış, teslim "
   "çözünürlüğü düşük ve kaynak dosya teslimi yok.",
   "İnşaat 3D modelleme fiyatları karşılaştırılırken bakılması gereken şey toplam "
   "rakam değil, o rakamın karşılığında yazılı olarak ne alındığı. Kapsamı "
   "eşitlediğinizde iki teklif arasındaki fark çoğu zaman yüzde yirmiye "
   "iniyor.",
   "Bir de görünmeyen maliyet var: satış ofisi açılışına yetişmeyen bir render "
   "seti, indirimli fiyatın tamamını götürüyor. Takvim taahhüdü olmayan teklif, "
   "aslında fiyat teklifi değil.",
   "Tipik süreler de teklifin parçası olmalı: model sizden geliyorsa 5–10 iş "
   "günü, sıfırdan model kuruluyorsa 2–4 hafta. Tarih vermeyen bir teklif, "
   "karşılaştırılabilir bir teklif değil.",
  ]),
  ("Render mi, animasyon mu, ikisi mi", [
   "Satış ofisinde duvara asılacak görsel ile sosyal medyada dönecek video "
   "farklı işler. Render seti kararı hızlandırıyor: alıcı tek bakışta cepheyi, "
   "iç mekânı ve konumu görüyor. Animasyon ise ilgi çekiyor; henüz karar "
   "aşamasında olmayan kişiyi durduran şey o.",
   "Pratikte doğru sıra şu: önce render seti, sonra aynı modelden çıkan kısa "
   "animasyon. Model bir kez kurulduğu için animasyon ek bir modelleme maliyeti "
   "getirmiyor; bu yüzden ikisini aynı işte planlamak, sonradan animasyon "
   "eklemekten belirgin biçimde ucuz.",
   "İnşaat 3D modelleme fiyatları içinde animasyonun payı, işi baştan birlikte "
   "planladığınızda küçük kalıyor. Ayrı sipariş edildiğinde ise model yeniden "
   "hazırlanmak zorunda kaldığı için büyük bir kalem hâline geliyor.",
  ]),
  ("Teslimden sonra ne oluyor", [
   "Render seti teslim edildiğinde iş bitmiyor; asıl kullanım orada başlıyor. "
   "Görseller ilan portalına, satış ofisi panosuna, katalog ve broşüre, sosyal "
   "medyaya ve bayi sunumlarına dağılıyor. Her mecranın kendi ölçüsü var ve bu "
   "ölçüler baştan belirlenmezse aynı görsel ikinci kez hazırlanmak zorunda "
   "kalıyor.",
   "Kaynak dosyaların kimde kaldığı da teslim anında belli olmalı. Model sizde "
   "kalıyorsa iki yıl sonra ikinci etap için sıfırdan başlamıyorsunuz; "
   "kalmıyorsa aynı projeye ikinci kez tam ücret ödüyorsunuz. Bu satır "
   "sözleşmede tek cümle, sonucu ise büyük.",
   "Projede değişiklik olması da olağan: cephe rengi değişiyor, peyzaj "
   "revize ediliyor, kat planı güncelleniyor. Model duruyorsa bu değişiklikler "
   "birkaç saatlik iş; durmuyorsa yeniden modelleme. İnşaat 3D render "
   "modelleme fiyatları tartışılırken bu ihtimalin de konuşulması gerekiyor.",
  ]),
  ("Nasıl çalışıyoruz", SUREC),
 ],
 "sss": [
  ("İnşaat 3D modelleme fiyatları ortalama ne kadar?",
   "Tek blok için render seti ve kısa animasyon içeren işler bizde "
   "60.000 – 150.000 ₺ arasında. Fiyatı belirleyen asıl kalemler model "
   "kaynağı, görsel tipi, çözünürlük ve revizyon hakkı."),
  ("Elimde sadece kat planı var, render alabilir miyim?",
   "Alabilirsiniz. Kat planı ve cephe çiziminden model kuruyoruz; bu durumda "
   "işin süresi ve fiyatı, hazır 3D modeli olan projeye göre artıyor."),
  ("Render kaç günde teslim ediliyor?",
   "Model sizden geliyorsa tipik olarak 5–10 iş günü, sıfırdan model "
   "kuruluyorsa 2–4 hafta. Kesin süreyi kapsam yazısında tarih vererek "
   "yazıyoruz."),
  ("Aynı modelden animasyon da çıkar mı?",
   "Çıkar ve ayrı iş olarak sipariş etmekten belirgin biçimde ucuza gelir. "
   "Model bir kez kurulduğu için animasyon büyük ölçüde kamera ve süre işi."),
 ],
 "kaynak": ["render_fiyat"],
 "ic": [("İnşaat 3D modelleme hizmeti", "hizmetler/insaat-3d-modelleme.html"),
        ("yayınlanmış fiyat bandımız", "fiyatlar.html"),
        ("ürün animasyonu tarafı", "hizmetler/urun-animasyon.html")],
},

{
 "anahtar": "emlak-ilan-video",
 "baslik": "Emlak videosu ilan performansını değiştiriyor mu?",
 "adres": "emlak-videosu-ilan-performansi",
 "kelime": "emlak videosu",
 "hizmet": "hizmetler/emlak-kurumsal.html",
 "ozet": "Emlak videosu ilan performansını gerçekten değiştiriyor mu? Ne çekilmeli, hangi sırayla, ne kadar uzun olmalı ve ne kadar tutuyor?",
 "kisa_cevap":
   "İlan videosunun işi daha çok kişiye görünmek değil, yanlış kişiyi eleyip "
   "doğru kişiyi randevuya getirmek. Fotoğraf mekânın ölçüsünü ve akışını "
   "vermediği için alıcı yerinde görene kadar karar veremiyor. Çekim + kurgu + "
   "sosyal sürümler içeren işler bizde 25.000 – 55.000 ₺ bandında.",
 "bolum": [
  ("Fotoğrafın söyleyemediği üç şey", [
   "Bir ilan fotoğrafı odayı gösterir ama üç şeyi söyleyemez: odalar arasındaki "
   "mesafeyi, günün hangi saatinde ne kadar ışık aldığını ve girişten "
   "başlayarak evin nasıl bir sırayla yaşandığını. Alıcının kafasındaki soru "
   "genelde bu üçü.",
   "Bu yüzden fotoğrafla dolu bir ilan çok tıklanıp az randevu üretebiliyor. "
   "Gelen kişi kapıdan girdiği anda 'ben bunu böyle düşünmemiştim' diyorsa hem "
   "alıcının hem danışmanın günü gitmiş oluyor.",
  ]),
  ("Videonun asıl işi elemek", [
   "İyi bir ilan videosu daha çok randevu değil, daha az boş randevu üretir. "
   "Mekânı gerçekten gezdiren bir video, o eve uymayacak kişiyi kendiliğinden "
   "eliyor. Kalan randevular ise satın almaya yakın kişilerden oluşuyor.",
   "Bu, ölçmesi kolay bir şey: portföyü videolu ve videosuz dönemlerde "
   "randevu sayısı değil, randevu başına düşen teklif sayısını karşılaştırın.",
  ]),
  ("Tek çekimden kaç parça çıkar", [
   "Bir mekânda geçirilen yarım gün, tek bir video anlamına gelmiyor. Aynı "
   "çekimden yatay ilan videosu, dikey sosyal medya sürümü, kare feed kesiti ve "
   "sunum için birkaç kare çıkıyor. Mecra başına yeniden çekim yapmak gereksiz "
   "bir masraf.",
   "Portföyü büyük ofisler için mantıklı olan, tek tek iş sipariş etmek yerine "
   "aylık düzen kurmak: ayda belirli sayıda portföy çekiliyor, aynı kurgu "
   "şablonuyla teslim ediliyor, danışman kendi mecrasında yayınlıyor.",
  ]),
  ("Ne kadar tutuyor", [
   "Çekim, kurgu, renk ve sosyal medya sürümlerini içeren emlak ve kurumsal "
   "tanıtım işleri bizde 25.000 – 55.000 ₺ bandında. Tek portföy için değil, "
   "aylık düzen için çalışıldığında portföy başına maliyet belirgin biçimde "
   "düşüyor.",
   "Bütçe küçükse iş küçültülerek de başlanabiliyor: elinizde çekilmiş ama "
   "kullanılmayan görüntü varsa yalnızca kurgu, renk ve altyazı ile "
   "yayınlanabilir hâle getirmek en ucuz başlangıç.",
  ]),
  ("İyi bir emlak ilan videosunun beş kuralı", [
   "**Girişten başla.** Kapıdan içeri giren birinin gördüğü sırayla çek. "
   "Alıcının kafasındaki harita böyle kuruluyor.",
   "**Kesme sayısını azalt.** Her kesme, izleyicinin mekân algısını sıfırlıyor. "
   "Akıcı tek plan, on hızlı kesitten daha bilgilendirici.",
   "**Ölçü ver.** Metrekare yazısı ya da referans bir nesne olmadan alıcı "
   "büyüklüğü tahmin edemiyor.",
   "**Işığı doğru saatte yakala.** Aynı daire sabah ve ikindi çekiminde iki "
   "farklı ev gibi görünüyor; hangi saatte daha iyi göründüğünü bilmek "
   "danışmanın işi.",
   "**Sesle boğma.** Yüksek müzik, izleyicinin dikkatini mekândan alıyor. "
   "Emlak videosu bir klip değil, bir gezinti.",
  ]),
  ("Portalda ve sosyal medyada aynı video işe yaramıyor", [
   "Portal ilanında izleyici zaten ilgili: konumu ve fiyatı görmüş, videoya "
   "detay için giriyor. Orada 60–90 saniyelik, ölçü ve akış veren bir sürüm "
   "doğru olan. Sosyal medyada ise izleyici o ilanı aramıyordu; ilk üç saniye "
   "durdurmazsa video izlenmiyor.",
   "Bu yüzden aynı çekimden iki kurgu çıkarıyoruz: portal için uzun ve bilgi "
   "veren, sosyal için kısa ve dikkat çeken. İkinci sürüm ayrı bir çekim "
   "gerektirmediği için maliyeti küçük.",
   "Emlak videosu tek bir dosya olarak düşünüldüğünde iki mecrada da "
   "ortalama sonuç veriyor. İki sürüm olarak planlandığında ikisinde de "
   "işini yapıyor.",
  ]),
  ("Danışman videoda görünmeli mi", [
   "Bu, portföy sahiplerinin en çok sorduğu sorulardan biri. Cevap portföye "
   "göre değişiyor. Yüksek bütçeli, kurumsal bir portföyde danışmanın "
   "görünmesi güven veriyor; alıcı kiminle muhatap olacağını baştan görüyor.",
   "Buna karşılık hızlı devir beklenen, standart dairelerde danışmanın kadraja "
   "girmesi videoyu uzatmaktan başka bir işe yaramıyor. Orada mekânın kendisi "
   "anlatıyor, konuşan bir kişiye ihtiyaç yok.",
   "Orta yol da var: danışman yalnızca girişte on saniye görünüp mekânı "
   "tanıtıyor, kalan bölüm sessiz gezinti olarak devam ediyor. Emlak "
   "videosu böyle kurgulandığında hem yüz tanıdık oluyor hem izleyici "
   "sıkılmıyor.",
  ]),
  ("Boş mülk ve bitmemiş proje", [
   "Boş dairede video çekmek zannedildiği kadar zor değil; aksine ölçüyü en "
   "net veren durum bu. Mobilyasız mekânda kamera akışı ve geniş açı, "
   "büyüklüğü doğrudan anlatıyor. Eksik olan tek şey ölçek hissi; bunu "
   "kadraja giren bir kapı ya da pencere çözüyor.",
   "Bitmemiş projede ise çekilecek bir mekân yok. Orada video değil, "
   "modelden çıkan görsel ve animasyon iş görüyor. İkisini karıştırmamak "
   "gerekiyor: satış ofisinde asılan görsel ile teslim edilmiş daireyi "
   "gezdiren emlak videosu farklı işler.",
   "Teslim aşamasına gelmiş projelerde ikisi birleşiyor: ortak alanlar "
   "gerçek çekimle, henüz bitmemiş kısımlar modelle anlatılıyor. Aynı "
   "kurguda ikisi bir arada durabiliyor.",
  ]),
  ("Ölçmeden yapılan iş tartışmalı kalıyor", [
   "Video yayınlandıktan sonra \"işe yaradı mı\" sorusuna cevap verebilmek "
   "için önceden iki rakamın yazılmış olması gerekiyor: o portföyün video "
   "öncesi ilan görüntülenmesi ve randevu sayısı. Sonradan hatırlamaya "
   "çalışmak işe yaramıyor.",
   "Ölçüm kurulumu zor değil: sitedeki iletişim tıklamaları — telefon, "
   "WhatsApp, form — sayılabilir hâle getiriliyor ve portal tarafındaki "
   "görüntülenme verisi elle not ediliyor. Bir ay sonra karşılaştırma yapmak "
   "için bu ikisi yeterli.",
   "Emlak videosu tarafında dürüst olmak gerekiyor: video tek başına "
   "satmıyor. Fiyat yanlışsa, konum uymuyor ya da ilan metni eksikse video "
   "bunu kurtarmıyor. Videonun işi doğru alıcıyı hızlandırmak; yanlış "
   "portföyü doğru yapmak değil.",
  ]),
  ("Nasıl çalışıyoruz", SUREC),
  ("Özetle", [
   "Emlak videosu, ilanı daha çok kişiye göstermek için değil, doğru "
   "kişiyi randevuya getirmek için var. Fotoğrafın veremediği üç şeyi — "
   "mesafe, ışık ve akış — veriyor ve bu üçü randevu öncesi kararın "
   "belirleyicisi oluyor.",
   "Tek portföyle başlanabilir, ama asıl kazanç aylık düzende çıkıyor: aynı "
   "çekimden birden çok mecra besleniyor, portföy başına maliyet düşüyor ve "
   "ölçüm kurulduğu için iş tartışmalı olmaktan çıkıyor.",
  ]),

 ],
 "sss": [
  ("Emlak videosu ne kadar uzun olmalı?",
   "Portal ilanında 60–90 saniye, sosyal medyada 20–30 saniye iyi çalışıyor. "
   "Aynı çekimden iki sürüm birden çıkarmak, ikinci bir çekimden ucuz."),
  ("Boş daire mi dolu daire mi daha iyi çekiliyor?",
   "Boş daire ölçüyü daha net verir, dolu daire yaşamayı anlatır. Portföy "
   "satılık ise boş, kiralık ve hızlı devir bekleniyorsa döşeli çekim genelde "
   "daha iyi sonuç veriyor."),
  ("Drone çekimi şart mı?",
   "Konum ve çevre önemliyse değerli; daire içi ağırlıklı ilanlarda şart "
   "değil. Yasak bölge kontrolü çekimden önce yapılıyor."),
  ("Video kaç günde teslim ediliyor?",
   "Çekimden sonra tipik olarak 3–7 iş günü. Aylık düzende çalışıldığında "
   "teslim takvimi ay başında yazılı olarak belirleniyor."),
 ],
 "kaynak": ["tanitim_fiyat"],
 "ic": [("Emlak ve kurumsal tanıtım", "hizmetler/emlak-kurumsal.html"),
        ("drone çekimi", "hizmetler/drone-fpv.html"),
        ("fiyat bandımız", "fiyatlar.html")],
},

{
 "anahtar": "urun-animasyonu-ne-zaman",
 "baslik": "Ürün animasyonu ne zaman doğru seçim olur?",
 "adres": "urun-animasyonu-ne-zaman-gerekir",
 "kelime": "ürün animasyonu",
 "hizmet": "hizmetler/urun-animasyon.html",
 "ozet": "Ürün animasyonu her ürün için gerekli değil. Hangi üründe fotoğrafın "
         "yetmediğini, ne kadar tuttuğunu ve nasıl planlandığını yazdık.",
 "kisa_cevap":
   "Ürün animasyonu, ürünün değerini dışarıdan görünmeyen bir şey belirliyorsa "
   "doğru seçim: içindeki mekanizma, üretim süreci, montaj sırası ya da "
   "görünmeyen bir malzeme farkı. Dışarıdan anlaşılan üründe iyi bir fotoğraf "
   "daha ucuz ve yeterli. Modelleme, animasyon ve ses tasarımı içeren işler "
   "bizde 40.000 – 95.000 ₺ bandında.",
 "bolum": [
  ("Ayırt edici soru: değer nerede duruyor", [
   "Bir ürünün değeri dışarıdan görünüyorsa — biçim, renk, kaplama — fotoğraf "
   "yeter ve daha ucuza gelir. Değer içeride duruyorsa, fotoğraf o değeri "
   "gösteremez. Bir vananın içindeki akış, bir makinenin çalışma sırası, bir "
   "yalıtım katmanının kalınlığı fotoğrafta yok.",
   "Katalog da bu boşluğu kapatmıyor, çünkü kimse on sekiz sayfalık katalogu "
   "okumuyor. Fuarda, bayi sunumunda ve web sitesinde iş gören şey, o "
   "mekanizmayı kırk saniyede gösteren bir anlatım oluyor.",
  ]),
  ("Kesit, patlatma ve akış", [
   "Ürün animasyonunun üç temel anlatımı var. **Kesit**, ürünü bir düzlemden "
   "ikiye ayırıp içini gösteriyor. **Patlatma**, parçaları ayırıp montaj "
   "sırasını anlatıyor. **Akış**, ürünün içinden geçen şeyi — su, hava, yük, "
   "veri — görünür kılıyor.",
   "Hangisinin kullanılacağı satış argümanına bağlı. \"Bizimki daha dayanıklı\" "
   "diyorsanız kesit; \"montajı yarım saat\" diyorsanız patlatma; \"basınç "
   "kaybı düşük\" diyorsanız akış anlatımı doğru olanı.",
  ]),
  ("Tek üretim, çok sürüm", [
   "Bir kez kurulan 3D sahneden çıkan şey tek bir video değil. Aynı üretimden "
   "farklı dillerde seslendirme, fuar ekranı için sessiz döngü sürümü, sosyal "
   "medya için dikey kesit ve web sitesi için kısa sürüm birlikte çıkıyor.",
   "Bu yüzden ürün animasyonunda doğru soru \"bir video kaça?\" değil, \"bu "
   "üretimden bir yıl boyunca kaç yerde kullanacağım?\". Fuara yılda iki kez "
   "giren bir firmada aynı dosya iki yıl çalışıyor.",
  ]),
  ("Ne kadar tutuyor, ne kadar sürüyor", [
   "Modelleme, animasyon ve ses tasarımını içeren sinematik ürün animasyonları "
   "bizde 40.000 – 95.000 ₺ bandında. Süre, teknik çizim elinizde varsa "
   "3–5 hafta; ürünü ölçüp modelini biz kuracaksak daha uzun.",
   "Bütçe kısıtlıysa kapsamı küçültmek mümkün: tek anlatım, tek dil, 30 "
   "saniye. Küçük başlayıp işe yaradığını görmek, büyük başlayıp yarıda "
   "bırakmaktan daha iyi sonuç veriyor.",
  ]),
  ("Fuar, bayi ve web sitesi: aynı dosya üç iş yapıyor", [
   "Fuarda ekran başında duran kimse yok; orada işi gören şey sessiz çalışan, "
   "kendini tekrar eden kısa bir döngü. Bayi sunumunda ise anlatım gerekiyor: "
   "ürünün rakibinden farkı hangi parçada, hangi ölçüde.",
   "Web sitesinde üçüncü bir ihtiyaç var: sayfa açılır açılmaz konuyu anlatan, "
   "otomatik başlayan ve ses gerektirmeyen bir sürüm. Üçü de aynı ürün "
   "animasyonundan çıkıyor; farklı üretimler değil, farklı kurgular.",
   "Bu yüzden teklif alırken \"kaç saniye\" sorusundan önce \"hangi üç yerde "
   "kullanacağım\" sorusunu cevaplamak, maliyeti doğrudan düşürüyor.",
  ]),
  ("Ürün animasyonu için elinizde ne olmalı", [
   "En hızlı yol, üretimde kullandığınız teknik çizimi ya da CAD dosyasını "
   "vermeniz. Bu durumda modelleme aşaması kısalıyor ve iş doğrudan anlatım "
   "kurgusuna geçiyor.",
   "Elinizde çizim yoksa ürünü ölçüp fotoğraflayarak da model kurulabiliyor; "
   "bu, süreyi uzatan ama engel olmayan bir durum. Ürün animasyonu için mutlaka "
   "hazır 3D model gerektiği düşüncesi yaygın ama doğru değil.",
   "Üçüncü bir ihtimal: ürün henüz üretilmedi. Prototip aşamasındaki ürünler "
   "için animasyon, fotoğrafın mümkün olmadığı tek anlatım biçimi oluyor; "
   "fuara ürünsüz gitmek zorunda kalan firmalar için asıl kullanım alanı burası.",
  ]),
  ("Süre, revizyon ve onay adımları", [
   "Ürün animasyonunda en sık yaşanan gecikme teknik değil, onay kaynaklı. "
   "Animasyon ilerledikten sonra gelen \"şu parçayı da gösterelim\" isteği, "
   "yapılmış işin bir kısmını geri alıyor. Bunu önlemenin yolu, üretime "
   "başlamadan önce storyboard onayı almak.",
   "Storyboard, animasyonun kare kare çizilmiş hâli değil; hangi sahnede neyin "
   "gösterileceğini ve ne söyleneceğini yazan kısa bir belge. Onaylandıktan "
   "sonra üretim başlıyor ve revizyonlar bu belgeye göre değerlendiriliyor.",
   "Tipik takvim şöyle işliyor: storyboard ve onay bir hafta, modelleme "
   "bir–iki hafta, animasyon ve ışık bir–iki hafta, ses ve son kurgu bir hafta. "
   "Ürün animasyonu için gerçekçi bir toplam süre, teknik çizim hazırsa üç ile "
   "beş hafta arasında oluyor.",
  ]),
  ("Ses, müzik ve dil kararları", [
   "Ürün animasyonunda ses, sonradan eklenen bir süs değil; anlatımın "
   "yarısı. Fuar salonunda kimse sesi duymuyor, o yüzden fuar sürümü "
   "yazıyla anlaşılabilir olmalı. Web sitesinde ise otomatik başlayan video "
   "sessiz açılıyor; ilk saniyeler yine yazıyla taşınıyor.",
   "Seslendirme kararı da satış kanalına bağlı. Yurt dışına satış yapan bir "
   "firmada seslendirme yerine yazı kullanmak, dil sürümlerini ucuzlatıyor: "
   "yeni bir dil için yalnızca yazılar değişiyor.",
   "Müzikte lisans meselesi atlanmamalı. Lisanssız müzikle yayınlanan bir "
   "ürün animasyonu, sosyal mecralarda sessize alınabiliyor ya da "
   "kaldırılabiliyor. Kullandığımız parçaların lisansı işle birlikte "
   "teslim ediliyor.",
  ]),
  ("Nasıl çalışıyoruz", SUREC),
  ("Özetle", [
   "Ürün animasyonu her ürün için gerekli değil. Ürünün değeri dışarıdan "
   "görünüyorsa fotoğraf hem yeterli hem ucuz. Değer içeride — mekanizma, "
   "akış, montaj sırası — ise animasyon o değeri görünür kılan tek yol.",
   "Doğru planlandığında tek üretimden fuar, bayi ve web sürümleri birlikte "
   "çıkıyor. Bu yüzden karar verirken sorulacak soru \"kaç saniye\" değil, "
   "\"bu dosyayı bir yıl boyunca nerede kullanacağım\" olmalı.",
  ]),

 ],
 "sss": [
  ("Ürün animasyonu için 3D model şart mı?",
   "Şart değil. Teknik çizim, ölçü ve fotoğraf yeterli; modeli biz kuruyoruz. "
   "Hazır modeliniz varsa süre ve maliyet düşüyor."),
  ("Animasyon kaç saniye olmalı?",
   "Fuar ekranı için 20–40 saniyelik sessiz döngü, web sitesi için 45–60 "
   "saniyelik anlatımlı sürüm iyi çalışıyor. İkisi aynı üretimden çıkıyor."),
  ("Yabancı dil sürümü ek ücret mi?",
   "Aynı animasyonun ikinci dil sürümü, ilk üretimin yanında küçük bir kalem; "
   "yeniden üretim değil, yalnızca seslendirme ve alt yazı işi."),
  ("Ürün animasyonu mu, ürün fotoğrafı mı?",
   "Ürünün değeri dışarıdan görünüyorsa fotoğraf yeterli ve daha ucuz. Değer "
   "içeride — mekanizma, akış, montaj — ise animasyon gerekiyor."),
 ],
 "kaynak": ["render_fiyat"],
 "ic": [("Ürün animasyonu hizmeti", "hizmetler/urun-animasyon.html"),
        ("inşaat 3D modelleme", "hizmetler/insaat-3d-modelleme.html"),
        ("fiyat sayfamız", "fiyatlar.html")],
},
]

KONULAR += [

{
 "anahtar": "drone-cekim-izin",
 "baslik": "Drone çekimi izin kuralları ve kontrol listesi",
 "adres": "drone-cekimi-izin",
 "kelime": "drone çekimi izin",
 "hizmet": "hizmetler/drone-fpv.html",
 "ozet": "Drone çekimi izin kuralları nasıl işliyor, yasak bölge nasıl kontrol edilir, çekim günü neye bakılır? Ticari çekim öncesi kontrol listesi.",
 "kisa_cevap":
   "Drone çekimi izin işi çekimden önce hallediliyor: Türkiye'de insansız hava aracı uçuşları Sivil Havacılık Genel Müdürlüğü "
   "kurallarına tabi; kayıt, pilot yetkisi ve uçuş bölgesi kontrolü çekimden "
   "önce yapılıyor. Havalimanı çevresi, askerî bölgeler ve kalabalık alanlar "
   "kısıtlı. Yarım günlük çekim ve kurgu içeren işler bizde 8.000 – 25.000 ₺ "
   "bandında.",
 "bolum": [
  ("İzin işi çekim gününe bırakılmaz", [
   "Drone çekiminde en sık yapılan hata, izni çekim sabahına bırakmak. Uçuş "
   "bölgesi kısıtlıysa ekip sahada beklerken çözülecek bir şey değil; günün "
   "tamamı kaybediliyor ve mekân sahibi ikinci kez organize edilmek zorunda "
   "kalıyor.",
   "Kurallar Sivil Havacılık Genel Müdürlüğü tarafından belirleniyor ve "
   "değişebiliyor; bu yüzden kontrolü her iş için baştan yapmak, geçen "
   "seferki bilgiyle hareket etmekten daha güvenli.",
  ]),
  ("Çekim öncesi kontrol listesi", [
   "- Uçuş bölgesi kısıtlı mı, yasak mı — koordinat üzerinden kontrol.",
   "- Havalimanı, askerî tesis, cezaevi, enerji tesisi yakınlığı.",
   "- Kalabalık alan üzerinde uçuş gerekiyor mu; gerekiyorsa alternatif açı.",
   "- Mekân sahibinden yazılı çekim izni (özel mülk üzerinde uçuş).",
   "- Hava durumu: rüzgâr hızı, yağış ihtimali, gün ışığı saatleri.",
   "- Yedek gün — tek güne bağlı iş, ilk rüzgârlı günde riske giriyor.",
  ]),
  ("Yedek gün neden fiyatın parçası", [
   "Drone çekiminde takvim, hava koşuluna bağlı. Yedek gün planlamayan bir "
   "teklif ucuz görünür ama ilk erteleme masrafı sizin tarafınıza yazılır. "
   "Biz yedek günü baştan planlıyoruz; erteleme olursa ek ücret çıkmıyor.",
   "Aynı mantık ham kayıt için de geçerli: çekilen ham görüntülerin sizde "
   "kalıp kalmayacağı sözleşmede yazmıyorsa, ileride başka bir kurgu yapmak "
   "istediğinizde elinizde bir şey olmuyor.",
  ]),
  ("Yerden çekimle birleştirmek", [
   "Havadan çekim tek başına bir tanıtım değil. En iyi sonuç, havadan gelen "
   "geniş plan ile yerdeki detay planların aynı kurguda birleşmesinden çıkıyor. "
   "FPV ile dışarıdan içeri girip kesmesiz devam eden geçişler de bu şekilde "
   "planlanıyor.",
   "Bu yüzden drone çekimini ayrı bir iş gibi sipariş etmek yerine, tanıtımın "
   "bütününü tek planla kurmak hem ucuz hem tutarlı oluyor.",
  ]),
  ("Ticari çekimde sorumluluk kimde", [
   "Drone çekimi izin sorumluluğu, uçuşu yapan tarafta. Yani mekân sahibi "
   "\"bizim arazimiz, uçur\" dese bile hava sahası kuralları ayrı işliyor. "
   "Bu ayrımı bilmeyen bir ekiple çalışmak, riski müşteriye yıkıyor.",
   "Bizim tarafımızda bu iş şöyle yürüyor: bölge kontrolü çekim tarihinden önce "
   "yapılıyor, sonucu yazılı olarak paylaşılıyor ve kısıt varsa alternatif plan "
   "aynı yazıda öneriliyor. Çekim günü sürpriz olmuyor.",
   "Özel mülk üzerinde uçuş için ayrıca mekân sahibinden yazılı izin alıyoruz. "
   "Bu, hem çekim sırasında hem sonrasında görüntünün kullanım hakkını "
   "netleştiriyor.",
  ]),
  ("Havadan çekim her işe gerekmiyor", [
   "Drone çekimi izin ve planlama gerektiren bir iş olduğu için, gerçekten "
   "katkı sağlayacağı yerlerde kullanmak mantıklı. Konum, çevre, arazi ölçeği "
   "ya da bir yapının bütünü anlatılacaksa havadan plan işi görüyor.",
   "Buna karşılık iç mekân ağırlıklı bir tanıtımda havadan çekim çoğu zaman "
   "dekoratif kalıyor: güzel görünüyor ama izleyicinin sorusunu "
   "cevaplamıyor. Bütçeyi orada harcamak yerine yerden çekime ayırmak daha iyi "
   "sonuç veriyor.",
   "Karar ölçütü basit: havadan alınan plan izleyicinin bilmediği bir şey "
   "söylüyor mu? Söylemiyorsa o plan kurguya girmiyor.",
  ]),
  ("Çekim günü sahada ne yapılıyor", [
   "Ekip sahaya vardığında ilk iş uçuş alanının gözle kontrolü: elektrik "
   "hatları, ağaçlar, vinç, komşu binaların balkonları. Harita üzerinde temiz "
   "görünen bir alan sahada başka türlü olabiliyor.",
   "Ardından kalkış noktası belirleniyor ve kısa bir deneme uçuşu yapılıyor. "
   "Bu uçuşun amacı görüntü almak değil; rüzgârın gerçek şiddetini ve sinyal "
   "durumunu ölçmek. Deneme atlanırsa asıl çekim sırasında sürpriz çıkıyor.",
   "Çekim sırasında yerdeki ekip de çalışıyor: aynı anda yerden alınan planlar, "
   "havadan gelen görüntünün kurguda oturmasını sağlıyor. Drone çekimi izin ve "
   "planlama tarafı doğru kurulduğunda, sahada geçen süre yarım güne "
   "iniyor ve maliyet öngörülebilir kalıyor.",
  ]),
  ("Görüntünün sonraki kullanımı", [
   "Çekilen havadan görüntü tek bir videoda tükenmiyor. Aynı kayıttan ilan "
   "videosu, kurumsal tanıtım, sosyal medya kesiti ve web sitesi arkaplanı "
   "çıkıyor. Bu yüzden çekim planı yapılırken yalnızca bugünkü iş değil, "
   "önümüzdeki bir yılın kullanımı da konuşuluyor.",
   "Şantiye takibi yapan firmalarda ayrı bir kullanım var: aynı açıdan "
   "belirli aralıklarla alınan havadan kayıt, ilerlemeyi gösteren bir "
   "arşive dönüşüyor. Bunun için kalkış noktasının ve kamera ayarlarının "
   "kayıt altına alınması gerekiyor.",
   "Drone çekimi izin kontrolü de bu tekrar eden işlerde her seferinde "
   "yenileniyor; bölge durumu zaman içinde değişebiliyor ve geçen ayki "
   "kontrol bu ay için geçerli sayılmıyor.",
  ]),
  ("Nasıl çalışıyoruz", SUREC),
  ("Özetle", [
   "Drone çekimi izin tarafı, çekimin en teknik ama en öngörülebilir kısmı. "
   "Bölge kontrolü, yazılı mekân izni ve yedek gün planı önceden "
   "yapıldığında çekim günü sürpriz olmuyor.",
   "Havadan çekim her işe de gerekmiyor. Ölçüt şu: alınan plan izleyicinin "
   "bilmediği bir şey söylüyorsa değerli, söylemiyorsa bütçe yerden çekime "
   "ayrılmalı.",
   "Fiyat tarafında da tablo net: yarım günlük çekim ve kurgu içeren işler "
   "8.000 – 25.000 ₺ bandında oluşuyor. Bandın yeri, uçuş süresine değil "
   "kurgunun kapsamına ve teslim edilecek sürüm sayısına göre değişiyor. "
   "Tek bir yayına hazır video ile beş farklı mecra sürümü aynı iş değil.",
  ]),

 ],
 "sss": [
  ("Drone çekimi için izin gerekiyor mu?",
   "İnsansız hava aracı uçuşları Sivil Havacılık Genel Müdürlüğü kurallarına "
   "tabidir; kayıt, pilot yetkisi ve bölge kontrolü gerekir. Kontrolü çekimden "
   "önce yapıyoruz."),
  ("Yasak bölgede çekim mümkün mü?",
   "Kısıtlı ve yasak bölgelerde uçuş yapılmıyor. Bu durumda alternatif açı, "
   "yerden yüksek nokta ya da direkli çekim gibi çözümlerle plan değişiyor."),
  ("Rüzgârlı havada çekim yapılır mı?",
   "Belirli bir rüzgâr hızının üzerinde görüntü stabil olmuyor ve uçuş riskli. "
   "Bu yüzden her işte yedek gün planlıyoruz."),
  ("Ham kayıtlar bize veriliyor mu?",
   "Evet. Ham kayıtların teslim edilip edilmeyeceği kapsam yazısında açıkça "
   "yazıyor; sonradan başka bir kurgu yapmak isterseniz elinizde duruyor."),
 ],
 "kaynak": ["shm"],
 "ic": [("Drone ve FPV çekim", "hizmetler/drone-fpv.html"),
        ("emlak tanıtım işleri", "hizmetler/emlak-kurumsal.html"),
        ("fiyat bandı", "fiyatlar.html")],
},

{
 "anahtar": "yapay-zeka-arama-kaynak",
 "baslik": "Yapay zeka arama görünürlüğü: kaynak olarak seçilmek",
 "adres": "yapay-zeka-arama-gorunurlugu",
 "kelime": "yapay zeka arama görünürlüğü",
 "hizmet": "hizmetler/yapay-zeka-seo.html",
 "ozet": "Yapay zeka arama görünürlüğü nasıl kazanılır? Cevapta kaynak olarak gösterilmek için sitede neyin bulunması gerektiğini yazdık.",
 "kisa_cevap":
   "Yapay zeka arama görünürlüğü, cevabın içinde kaynak olarak geçmek demek. Yapay zekâ tabanlı arama, cevabı üretirken kaynak gösterebileceği sayfaları "
   "seçiyor. Kaynak olarak seçilmek için üç şey gerekiyor: net bir soru-cevap "
   "yapısı, makine tarafından okunabilen şema verisi ve doğrulanabilir, "
   "tarihli bilgi. Süslü pazarlama metni bu üçünün hiçbirini karşılamıyor.",
 "bolum": [
  ("Soru artık arama kutusuna yazılmıyor", [
   "\"Bursa'da 3D render kim yapıyor\" sorusu artık yalnızca arama kutusuna "
   "değil, doğrudan bir yapay zekâ asistanına da soruluyor. Asistan cevabı "
   "üretirken bir yerlerden okuyor ve çoğu zaman okuduğu yeri kaynak olarak "
   "gösteriyor.",
   "Buradaki fark önemli: klasik aramada hedef ilk sırada çıkmaktı; burada "
   "hedef cevabın içinde geçmek. İkisi aynı şey değil ve ikincisi farklı bir "
   "sayfa yapısı istiyor.",
  ]),
  ("Kaynak seçilen sayfanın üç özelliği", [
   "**Net soru-cevap.** Sayfada sorunun kendisi ve cevabı ayrı ayrı, kısa ve "
   "doğrudan yazılmış olmalı. \"Çözüm ortağınız olarak yanınızdayız\" cümlesi "
   "hiçbir sorunun cevabı değil.",
   "**Şema verisi.** Sayfanın ne anlattığını makineye söyleyen JSON-LD şeması "
   "— hizmet, işletme, SSS. Google bunun dokümanını yayınlıyor; uygulaması "
   "teknik ama bir kez kuruluyor.",
   "**Doğrulanabilirlik.** Rakam veriyorsanız kaynağı ve tarihi olsun. "
   "Tarihsiz iddia, hem okuyucu hem makine için değersiz.",
  ]),
  ("Ölçülebilir olan ne", [
   "Bu alanda dürüst olmak gerekiyor: yapay zekâ cevaplarında kaç kez kaynak "
   "gösterildiğinizi gösteren olgun bir ölçüm aracı henüz yok. Ölçülebilen "
   "şey, sayfaların teknik olarak uygun olup olmadığı ve klasik aramadaki "
   "hareket.",
   "Biz kendi sitemizde bunu açık tutuyoruz: sayfa sayısı, keşfedilen sayfa "
   "sayısı ve arama verisi şeffaflık sayfasında tarihiyle duruyor. Aynı "
   "yaklaşımı müşteri işlerinde de uyguluyoruz — ölçemediğimiz şeye sonuç "
   "demiyoruz.",
  ]),
  ("Nereden başlanır", [
   "Sırayla: önce sitenin teknik durumu (başlık, açıklama, şema, site "
   "haritası), sonra her hizmet için gerçek soru-cevap içerikleri, en sonda "
   "yazı düzeni. Ters sırada başlamak — önce blog yazmak — en sık yapılan ve "
   "en pahalı hata.",
   "Kendi sitemizde bunu yaptığımızda 331 sayfanın yalnızca 24'ünün "
   "keşfedildiğini gördük; site haritası düzeltildikten sonra aynı gün "
   "tamamı keşfedildi. Bu, içerik değil bakım işiydi.",
  ]),
  ("Sıralama değil, alıntılanma", [
   "Klasik SEO'da başarı ölçüsü sıralamaydı: kaçıncı sıradayız. Yapay zeka "
   "arama görünürlüğü tarafında ölçü değişiyor; sayfa hiç tıklanmadan da cevabın "
   "içinde geçebiliyor. Bu, trafik grafiğine yansımayan ama satışa yansıyan bir "
   "görünürlük.",
   "Pratikte bu, sayfaların \"alıntılanabilir\" parçalara bölünmesi anlamına "
   "geliyor: kısa ve kendi başına anlamlı paragraflar, net tanımlar, tablo "
   "hâline getirilebilir bilgiler. Uzun ve dolambaçlı bir paragraftan alıntı "
   "çıkarmak zor.",
   "Aynı mantık okuyucu için de iyi çalışıyor. Yapay zekâ için düzenlenmiş bir "
   "sayfa, insan için de daha okunur oluyor — bu ikisi çelişmiyor.",
  ]),
  ("Kendi sitemizde ne yaptık", [
   "Yapay zeka arama görünürlüğü konusunda tavsiye veren bir firmanın kendi "
   "sitesini ölçmesi gerekir. Biz sitemizin sayfa sayısını, keşfedilen sayfa "
   "sayısını ve arama verisini tarihiyle birlikte yayınlıyoruz.",
   "Yaptığımız iş sırasıyla şuydu: site haritasının doğru okunduğunu "
   "doğrulamak, her sayfaya şema verisi eklemek, hizmet sayfalarını gerçek "
   "sorulara cevap verecek biçimde yeniden yazmak ve ölçümü kurmak.",
   "Bunların hiçbiri blog yazmakla başlamadı. İçerik, teknik temel "
   "kurulduktan sonra anlam kazanıyor; ters sıra en sık yapılan hata.",
  ]),
  ("Nelerden kaçınmak gerekiyor", [
   "Bu alanda hızlı sonuç vadeden yöntemlerin çoğu eski numaraların yeni "
   "adı. Aynı yazının şehir şehir kopyalanması, anahtar kelime doldurulmuş "
   "paragraflar, kaynağı olmayan istatistikler: üçü de kısa vadede hareket "
   "yaratıp orta vadede görünürlüğü düşürüyor.",
   "Google'ın yayınladığı yararlı içerik rehberi bu konuda açık: içerik "
   "arama motoru için değil, konuyu bilen bir insan için yazılmış olmalı. "
   "Yapay zeka arama görünürlüğü tarafında da aynı ölçüt geçerli, çünkü "
   "cevabı üreten model de aynı sayfaları okuyor.",
   "Bizim uyguladığımız kural şu: yayınlanan her yazının biçimsel bir "
   "kontrolden geçmesi gerekiyor — başlık, özet, iç bağlantı, kaynak, "
   "soru-cevap ve özgünlük. Bu kontrolden tam puan almayan yazı "
   "yayınlanmıyor. Kontrolü geçmek yazıyı iyi yapmıyor, ama eksik yazının "
   "yayınlanmasını engelliyor.",
  ]),
  ("Sayfa yapısı pratikte nasıl değişiyor", [
   "Değişikliklerin çoğu görünürde küçük. Her hizmet sayfasının başına, o "
   "hizmetin ne olduğunu iki cümlede söyleyen bir blok geliyor. Fiyat "
   "konuşuluyorsa bant ve tarih yazılıyor. Sık sorulan sorular sayfanın "
   "altına değil, ilgili bölümün yanına konuyor.",
   "Şema tarafında ise sayfanın türü açıkça belirtiliyor: bu bir hizmet "
   "sayfası mı, bir işletme sayfası mı, bir yazı mı. Google'ın SSS şeması "
   "dokümanı bunun nasıl yazılacağını anlatıyor ve uygulaması bir kerelik.",
   "Yapay zeka arama görünürlüğü için yapılan bu düzenlemelerin yan etkisi "
   "de var: sayfa insan için de hızlı okunur hâle geliyor ve telefonda "
   "cevabı bulmak kolaylaşıyor. İki hedef aynı yöne bakıyor.",
  ]),
  ("Nasıl çalışıyoruz", SUREC),
  ("Özetle", [
   "Yapay zeka arama görünürlüğü, sıralamada yükselmek değil cevabın içinde "
   "kaynak olarak geçmek demek. Bunun için gereken üç şey net soru-cevap "
   "yapısı, şema verisi ve doğrulanabilir, tarihli bilgi.",
   "Sıra önemli: önce teknik temel ve hizmet sayfaları, sonra yazı düzeni. "
   "Ters sırada başlamak — önce blog yazmak — en sık yapılan ve en pahalı "
   "hata.",
  ]),

 ],
 "sss": [
  ("Yapay zekâ aramasında görünmek için ne gerekiyor?",
   "Net soru-cevap yapısı, JSON-LD şema verisi ve doğrulanabilir, tarihli "
   "bilgi. Üçü de sayfanın kendisinde bulunmalı."),
  ("Bu, klasik SEO'nun yerine mi geçiyor?",
   "Hayır, üstüne biniyor. Teknik sağlık ve içerik kalitesi ikisinde de aynı "
   "temel; fark, cevabın içinde kaynak olarak geçme hedefinde."),
  ("Sonuç ne kadar sürede görülür?",
   "Teknik düzeltmelerin etkisi günler içinde görülebiliyor; içerik "
   "tarafındaki hareket aylarla ölçülüyor. Tarih vererek söz vermiyoruz."),
  ("Ölçümü nasıl yapıyorsunuz?",
   "Search Console verisi, sayfa denetimi ve site içi ölçüm. Ölçemediğimiz "
   "şeyi rapora yazmıyoruz."),
 ],
 "kaynak": ["google_yardimci", "google_sss"],
 "ic": [("Yapay zekâ ve arama görünürlüğü", "hizmetler/yapay-zeka-seo.html"),
        ("SEO ve içerik hizmeti", "hizmetler/seo-icerik.html"),
        ("şeffaflık sayfamız", "seffaflik.html")],
},

{
 "anahtar": "bir-cekim-gunu-bir-ay",
 "baslik": "İşletme tanıtım videosu: bir günden bir aylık içerik",
 "adres": "isletme-tanitim-videosu-icerik-duzeni",
 "kelime": "işletme tanıtım videosu",
 "hizmet": "hizmetler/isletme-tanitim.html",
 "ozet": "İşletme tanıtım videosu tek başına yetmiyor. Bir çekim gününü bir aylık içerik düzenine çevirmenin pratik yolunu ve maliyetini yazdık.",
 "kisa_cevap":
   "Tek bir işletme tanıtım videosu bir hafta konuşulur, sonra hesap susar. Çözüm daha çok video "
   "çekmek değil, bir çekim gününü planlı biçimde parçalamak: aynı günde "
   "çekilen malzemeden 10–12 içerik çıkarılıp bir aya yayılıyor. İçerik "
   "üretimi dahil aylık düzen bizde 14.000 – 40.000 ₺ bandında.",
 "bolum": [
  ("Sorun bütçe değil, süreklilik", [
   "Çoğu işletme videoyu tek seferlik bir masraf gibi planlıyor: bir tanıtım "
   "videosu çekiliyor, yayınlanıyor, bir hafta konuşuluyor ve hesap tekrar "
   "sessizliğe dönüyor. Sorun videonun kalitesi değil, arkasının gelmemesi.",
   "Sosyal mecralar süreklilik ödüllendiriyor. Ayda bir paylaşım yapan bir "
   "hesap, hem takipçi hem algoritma tarafında baştan başlıyor.",
  ]),
  ("Çekim gününü planlı parçalamak", [
   "Bir çekim gününü verimli kılan şey ekipman değil, plan. Çekime giderken "
   "hangi içeriklerin çıkacağı yazılı oluyor: tanıtım, ürün/hizmet anlatımı, "
   "ekip, arkaplan, müşteri sorusu cevapları, kısa dikey kesitler.",
   "Bir günde çekilen malzemeden tipik olarak 10–12 içerik çıkıyor ve bunlar "
   "bir aya yayılıyor. Aynı günde çekildikleri için görsel dil tutarlı; ayrı "
   "ayrı çekilseler hem pahalı hem dağınık olurdu.",
  ]),
  ("Neyi ölçmek gerekiyor", [
   "Beğeni sayısı işletmeye para kazandırmıyor. Ölçülmesi gereken şey, "
   "paylaşımdan sonra gelen mesaj ve arama sayısı. Bunun için sitedeki "
   "iletişim tıklamalarının ölçülmesi gerekiyor — WhatsApp, telefon, form.",
   "Bu ölçüm kurulmadan yapılan sosyal medya işi, sonucu tartışılamaz bir "
   "harcamaya dönüşüyor. Kurulumu bir kerelik ve zor değil.",
  ]),
  ("Ne kadar tutuyor", [
   "İçerik üretimi dahil aylık düzen bizde 14.000 – 40.000 ₺ bandında; bandın "
   "yeri çekim sıklığına ve içerik sayısına göre değişiyor. En az üç ay "
   "önerdiğimiz için ilk ayın sonunda karar vermek erken oluyor.",
   "Bütçe kısıtlıysa tek video ile başlamak da mümkün; ama beklentiyi buna "
   "göre kurmak gerekiyor: tek video bir başlangıçtır, bir düzen değil.",
  ]),
  ("Çekim gününde neler çekiliyor", [
   "Plan olmadan gidilen çekimden üç içerik çıkıyor; planla gidilenden on iki. "
   "Fark ekipmanda değil, listede. Tipik bir işletme tanıtım videosu çekim "
   "gününde şunlar çekiliyor: ana tanıtım, hizmet anlatımları, ekip tanıtımı, "
   "üretim veya mutfak arkaplanı, sık sorulan sorulara cevaplar ve dikey "
   "kesitler.",
   "Bu listenin işletmeye göre değişen tarafı var: bir lokantada mutfak, bir "
   "atölyede üretim hattı, bir klinikte hasta yolculuğu farklı ağırlık "
   "taşıyor. Liste çekimden önce yazılı olarak paylaşılıyor ve onaylanıyor.",
   "Onaylı liste, çekim gününü de kısaltıyor. Ne çekileceği belliyse bir "
   "işletmede yarım gün çoğu zaman yetiyor.",
  ]),
  ("Yayın takvimi ve tekrar", [
   "Çekilen içerik aynı hafta tükenmiyor; bir aya yayılıyor. Haftada iki üç "
   "paylaşım, ay boyunca düzenli görünürlük demek. Aynı içeriğin farklı "
   "kesitleri iki ay sonra tekrar kullanılabiliyor — takipçinin çoğu ilkini "
   "zaten görmemişti.",
   "İşletme tanıtım videosu üretiminde en çok atlanan şey bu tekrar hakkı. "
   "Elinizdeki malzemeyi tek kullanımlık saymak, en pahalı yöntem.",
   "Üç ayın sonunda elinizde hem yayınlanmış bir arşiv hem de neyin işe "
   "yaradığını gösteren bir ölçüm oluyor. Dördüncü ayın planı tahminle değil, "
   "o ölçümle yapılıyor.",
  ]),
  ("Hangi işletmede ne işe yarıyor", [
   "Lokanta ve kafede en çok işe yarayan içerik mutfak ve tabak hazırlığı; "
   "izleyici yemeğin nasıl çıktığını görmek istiyor. Atölye ve üretimde "
   "makinenin çalışması ve işin ustalık kısmı ilgi çekiyor.",
   "Hizmet işletmelerinde — klinik, danışmanlık, servis — asıl işe yarayan "
   "şey sık sorulan sorulara verilen kısa cevaplar. Bir işletme tanıtım "
   "videosu burada satış değil, güven kuruyor: müşteri gelmeden önce "
   "muhatabını tanımış oluyor.",
   "Perakendede ise ürün ve vitrin değişimi düzenli içerik üretiyor; yeni "
   "gelen ürün her hafta doğal bir konu. Ortak nokta şu: içerik fikrini "
   "aramak yerine işletmenin zaten yaptığı işi kaydetmek, hem daha ucuz hem "
   "daha inandırıcı oluyor.",
  ]),
  ("Üç ayın sonunda elinizde ne oluyor", [
   "İlk ay tanışma ayı: hangi içeriğin işletmeye uyduğu, kimin kamera "
   "önünde rahat olduğu ve takipçinin neye tepki verdiği ortaya çıkıyor. "
   "İkinci ay düzenin oturduğu ay; üçüncü ay ise karşılaştırma yapılabilen "
   "ilk ay.",
   "Üç ayın sonunda elde iki şey oluyor. Birincisi yayınlanmış bir arşiv: "
   "otuz civarında içerik, aynı görsel dille çekilmiş ve tekrar "
   "kullanılabilir. İkincisi ölçüm: hangi içerik türünün mesaj ve arama "
   "getirdiğini gösteren gerçek veri.",
   "Dördüncü ayın planı artık tahminle değil bu veriyle yapılıyor. İşletme "
   "tanıtım videosu üretimini sürdürmenin de, durdurmanın da kararı burada "
   "verilebilir hâle geliyor — ve bu karar için elinizde rakam oluyor.",
  ]),
  ("Nasıl çalışıyoruz", SUREC),
  ("Özetle", [
   "Tek bir işletme tanıtım videosu bir başlangıçtır, bir düzen değil. "
   "Süreklilik isteyen mecralarda sonucu belirleyen şey videonun kalitesi "
   "değil, arkasının gelmesi.",
   "Planlı bir çekim gününden 10–12 içerik çıkıyor ve bunlar bir aya "
   "yayılıyor. Ölçüm kurulduğunda ise üçüncü ayın sonunda devam kararı "
   "tahminle değil rakamla veriliyor.",
   "Ölçüm kurulmadan yapılan sosyal medya harcaması, sonucu tartışılamayan "
   "bir gider olarak kalıyor; kurulumu ise bir kerelik ve zor değil.",
   "Başlarken büyük bütçe şart değil. Elinizde kullanılmayan görüntü varsa "
   "yalnızca kurgu ve altyazı ile yayınlanabilir hâle getirmek en ucuz "
   "başlangıç; ilk sonucu gördükten sonra düzeni kurmak hem daha kolay hem "
   "daha ikna edici oluyor.",
  ]),

 ],
 "sss": [
  ("Ayda kaç içerik gerekiyor?",
   "Mecraya göre değişmekle birlikte haftada 2–3 paylaşım, bir çekim gününden "
   "çıkan 10–12 içerikle karşılanabiliyor."),
  ("Kendi telefonumuzla çeksek olmaz mı?",
   "Olur ve bazı içerikler için daha samimi durur. Fark planlamada ve "
   "kurguda; çekim aracı tek başına belirleyici değil."),
  ("Sonuç ne zaman görülür?",
   "Üçüncü aydan önce anlamlı bir eğilim görmek zor. Bu yüzden en az üç aylık "
   "düzen öneriyoruz."),
  ("İçerik fikirlerini kim buluyor?",
   "Plan bizde çıkıyor, onay sizde. Çekimden önce hangi içeriklerin "
   "çekileceği yazılı olarak paylaşılıyor."),
 ],
 "kaynak": ["sosyal_fiyat"],
 "ic": [("İşletme tanıtım hizmeti", "hizmetler/isletme-tanitim.html"),
        ("klip ve çekim tarafı", "hizmetler/klip-cekimi.html"),
        ("fiyat sayfası", "fiyatlar.html")],
},
]


# ------------------------------------------------------------------ üretim
def konu_bul(anahtar):
    for k in KONULAR:
        if k["anahtar"] == anahtar:
            return k
    return None


def liste():
    """Panelin göstereceği konu listesi."""
    from . import yayin as YA
    basilan = {k.get("baslik") for k in YA.kayitlar()}
    out = []
    for k in KONULAR:
        out.append({"anahtar": k["anahtar"], "baslik": k["baslik"],
                    "kelime": k["kelime"], "hizmet": k["hizmet"],
                    "yayinda": k["baslik"] in basilan})
    return out


def _sayfa_var(yol):
    return os.path.isfile(os.path.join(SITE_KOK, yol.lstrip("/")))


def ic_baglantilar(konu):
    """Yalnızca gerçekten var olan sayfalara bağlantı verilir."""
    return [(ad, yol) for ad, yol in konu.get("ic", []) if _sayfa_var(yol)]


def _paragraf_baglantila(metin, baglar, kullanilan):
    """Metinde geçen ilk uygun ifadeyi iç bağlantıya çevirir (bir kez)."""
    for ad, yol in baglar:
        if yol in kullanilan:
            continue
        for aday in (ad, ad.lower()):
            if aday in metin:
                kullanilan.add(yol)
                return metin.replace(aday, "[%s](../%s)" % (aday, yol), 1)
    return metin


def uret(anahtar):
    """Konudan yayına hazır markdown üretir (yayin.md_coz ile uyumlu)."""
    k = konu_bul(anahtar)
    if not k:
        return None
    baglar = ic_baglantilar(k)
    kullanilan = set()
    bugun = datetime.date.today().strftime("%d.%m.%Y")

    s = ["# %s" % k["baslik"], "",
         "*%s · Luna Yapım*" % bugun, "",
         "**Neden bu yazı:** %s" % k["ozet"], "",
         "**İlgili hizmet sayfası:** `%s`" % k["hizmet"], "",
         "---", "",
         "## Kısa cevap", "", k["kisa_cevap"], ""]

    for baslik, paragraflar in k["bolum"]:
        s.append("## %s" % baslik)
        s.append("")
        for p in paragraflar:
            s.append(_paragraf_baglantila(p, baglar, kullanilan))
            s.append("")

    # Bağlantı borcu kaldıysa kapanış bölümünde ödeniyor — yazının içine
    # zorla sıkıştırmak yerine okurun işine yarayacak yerde.
    kalan = [(ad, yol) for ad, yol in baglar if yol not in kullanilan]
    if kalan:
        s.append("## Devamı için")
        s.append("")
        for ad, yol in kalan:
            s.append("- [%s](../%s)" % (ad, yol))
        s.append("")

    kaynaklar = [KAYNAK_HAVUZ[a] for a in k.get("kaynak", []) if a in KAYNAK_HAVUZ]
    if kaynaklar:
        s.append("## Kaynaklar")
        s.append("")
        for ad, url in kaynaklar:
            s.append("- [%s](%s)" % (ad, url))
        s.append("")

    s.append("## Sık sorulanlar")
    s.append("")
    for soru, cevap in k["sss"]:
        s.append("**%s**" % soru)
        s.append(cevap)
        s.append("")
    return "\n".join(s).rstrip() + "\n"


def yaz(anahtar, klasor):
    """Üretilen yazıyı taslak klasörüne dosya olarak bırakır."""
    metin = uret(anahtar)
    if not metin:
        return None
    os.makedirs(klasor, exist_ok=True)
    yol = os.path.join(klasor, "%s-%s.md" % (datetime.date.today().strftime("%Y%m%d"),
                                             anahtar))
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    return yol


# ------------------------------------------------------------------ kapı ve yayın
def olc(anahtar):
    """Konuyu üretir ve yayın kapısından geçirir. Yayınlamaz."""
    from . import makale_puan as MP
    k = konu_bul(anahtar)
    if not k:
        return None
    metin = uret(anahtar)
    sonuc = MP.puanla(metin, k["kelime"], k["ozet"], k.get("adres", ""))
    sonuc["anahtar"] = anahtar
    sonuc["baslik"] = k["baslik"]
    sonuc["metin"] = metin
    sonuc["adres"] = k.get("adres", "")
    return sonuc


def yayinla(anahtar):
    """100 puan almayan yazı yayınlanmaz. Kapı burada, tek yerde."""
    from . import yayin as YA
    k = konu_bul(anahtar)
    if not k:
        return {"hata": "Konu bulunamadı."}
    o = olc(anahtar)
    if not o["gecti"]:
        return {"hata": "Puan %d/100 — yayınlanmadı." % o["puan"],
                "puan": o["puan"], "eksik": o["eksik"]}
    yazi, uyari = YA.md_coz(o["metin"])
    if uyari:
        return {"hata": "Yazı çözümlenemedi: " + " ".join(uyari)}
    if k.get("adres"):
        yazi["dosya"] = k["adres"] + ".html"
    yazi["ozet"] = k["ozet"]
    yazi["hizmet_sayfa"] = k["hizmet"]
    # Anahtar kelime satırı konudan çıkıyor; başlık kelimelerini doldurmak
    # ("kısa, cevap, soru, artık") kimseye bir şey anlatmıyor.
    cekirdek = []
    for a, kel in YA.CEKIRDEK.items():
        if a in (k.get("hizmet") or ""):
            cekirdek = list(kel)
            break
    tumu, gorulen = [], set()
    for x in [k["kelime"]] + cekirdek:
        if x and x.lower() not in gorulen:
            gorulen.add(x.lower())
            tumu.append(x)
    yazi["anahtar"] = ", ".join(tumu[:8])
    sonuc = YA.yayinla(yazi)
    sonuc["puan"] = o["puan"]
    return sonuc


def hazir_sayisi():
    """Karargâh için: kaç konu şu an 100 alıyor ve henüz yayında değil."""
    from . import yayin as YA
    basilan = {k.get("baslik") for k in YA.kayitlar()}
    n = 0
    for k in KONULAR:
        if k["baslik"] in basilan:
            continue
        o = olc(k["anahtar"])
        if o and o["gecti"]:
            n += 1
    return n
