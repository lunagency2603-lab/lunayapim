# -*- coding: utf-8 -*-
"""
FARK KATMANI — "herkesin yaptığı" ile "bizim yaptığımız" arasındaki mesafe.

Amaç övünmek değil. Teklifi okuyan işletme sahibi daha önce en az bir ajansla
çalışmış ya da teklif almıştır. O tecrübeyi hatırlatıp yanına farkı koyuyoruz.
Her satır somut ve doğrulanabilir olmalı — "daha kaliteliyiz" gibi bir cümle
buraya giremez.

Ayrıca ÇALIŞMA MODELİ burada tanımlı: aylık düzen mi, tek iş mi.
"""

# ------------------------------------------------------------------ genel fark
# (sıradan yaklaşım, bizim yaklaşımımız, bunun ölçülebilir sonucu)
GENEL = [
    ("Teklif gelmeden önce firmayı kimse incelemez; fiyat listesi gönderilir.",
     "Teklifi açtığınızda sitenizde ve profilinizde ne bulduğumuz, hangi adreste "
     "ve hangi saatte baktığımızla birlikte yazılı duruyor.",
     "Neyi neden yapacağımızı tartışıyoruz; fiyatı değil işi konuşuyoruz."),

    ("Video teslim edilir, iş biter. Nerede kullanılacağı müşterinin problemi olur.",
     "Aynı çekimden yatay, kare ve dikey sürüm birlikte çıkar; altyazılı ve altyazısız, "
     "kapak görselleriyle beraber.",
     "İlan sitesi, Reels, fuar ekranı ve WhatsApp için ayrı ayrı çekim ücreti ödemiyorsunuz."),

    ("Görüntü ham hâliyle 'renk düzeltmesi yapıldı' diye verilir.",
     "Renk, ses ve ritim ayrı ayrı çalışılır; ilk üç saniye ayrıca kurgulanır.",
     "İzlenme süresi ilk üç saniyede belli olur — asıl fark orada oluşuyor."),

    ("Sosyal medya ajansı içerik üretir, prodüksiyon ekibi video çeker; ikisi birbirini beklemez.",
     "Çekim, kurgu, tasarım ve yayın planı aynı ekipte; çekim günü zaten içerik takvimine göre planlanır.",
     "Tek çekim gününden bir aylık içerik çıkıyor, koordinasyon kaybı olmuyor."),

    ("Yazılım tarafı 'bizim işimiz değil' denip dışarı verilir.",
     "Kendi ürünlerimizi kendimiz yazıyoruz; sipariş, stok, form, otomasyon tarafı da bize açık.",
     "Videodan gelen talebin nereye düştüğü de bizim sorunumuz — sadece görüntü teslim etmiyoruz."),

    ("Rakamlar yuvarlanır: 'ciroyu ikiye katlıyoruz'.",
     "Tahmin ettiğimiz her rakamın yanında varsayımı yazılı; ilk ay ölçüm ayı olarak kullanılıyor.",
     "Abartılmış vaat yerine ölçülebilir bir başlangıç; rakam tutmazsa devam etmiyorsunuz."),
]


# ------------------------------------------------------------------ sektöre özel fark
SEKTOR = {
"produksiyon": [
 ("Ajans işi alır, prodüksiyonu dışarı verir; iki ekip birbirini bekler.",
  "Çekim, kurgu, 3D ve yazılım aynı ekipte; koordinasyon kaybı yok.",
  "Teslim süresi kısalıyor, revizyon aynı gün dönebiliyor."),
 ("Portfolyo 'güzel işler' olarak gösterilir; müşteri kendi işini göremez.",
  "Referanslar sektöre eşlenmiş; her işin yanında 'sizin işinizle ilgisi şu' yazıyor.",
  "Müşteri kendi projesinin nasıl çıkacağını görüyor, hayal etmek zorunda kalmıyor."),
],
"insaat": [
 ("Maket fotoğrafı ve render, projeyi anlatmak için yeterli sayılır.",
  "Aynı açıdan haftalık çekimle şantiye ilerlemesi biriktiriliyor; teslimde render ile "
  "gerçek yan yana konuyor.",
  "Alıcıya 'söz verilen ile teslim edilen aynı' diyebileceğiniz tek kanıt bu."),
 ("Daire, metrekare ve kat planıyla anlatılır.",
  "Kapıdan girip balkona çıkan kesintisiz tek plan çekim; pencereden gerçek manzara, kat numarasıyla.",
  "Satış ofisindeki 'manzara nasıl' tartışması videoda bitiyor."),
 ("Proje tanıtımı bir kere çekilir, sonuna kadar aynı video kullanılır.",
  "Etaplara bölünmüş içerik: kaba inşaat, cephe, iç mekân, teslim — her aşama kendi videosu.",
  "Proje boyunca anlatacak yeni şeyiniz oluyor; ilan da sosyal medya da tazeleniyor."),
],
"emlak": [
 ("Telefonla dikey video çekilir, ilana yüklenir.",
  "Gimbal ile akıcı tur, doğru saatte doğal ışık, dikey ve yatay sürüm birlikte.",
  "Aynı portföy, aynı fiyat — ilan sayfasında geçirilen süre farkı buradan çıkıyor."),
 ("Her ilan için ayrı ajans işi ayrı fiyattır.",
  "Aylık düzende çalışırsak portföy başına maliyet düşer; çekim günü toplu planlanır.",
  "Portföyünüz büyüdükçe birim maliyetiniz azalıyor."),
 ("Danışmanın kendisi hiç görünmez.",
  "Danışman tanıtımı ve 'bölgeyi anlatan' içerik ayrıca çekilir.",
  "Emlakta insan seçiliyor; portföy sonra geliyor."),
],
"mimarlik": [
 ("Sunum, PDF üzerinde render ve plan olarak yapılır.",
  "Sunum videosu: kamera projenin içinde geziyor, malzeme ve ışık gerçek saatine göre.",
  "Jüri ve yatırımcı sunumunda anlatım süresi kısalıyor, karar hızlanıyor."),
 ("Görselleştirme dışarıdan alınır, revizyon uzun sürer.",
  "Modelleme, ışık ve kurgu aynı ekipte; revizyon aynı gün dönebiliyor.",
  "Teslim tarihine yetişme riski azalıyor."),
],
"sanayi": [
 ("Makine, fabrikada olduğu gibi çekilir; içeride ne olduğu görünmez.",
  "Dışı gerçek çekim, içi animasyon: kesit, akış ve çalışma prensibi görünür hâle gelir.",
  "Fuarda ve ihracat görüşmesinde tercüman gerektirmeyen tek anlatım biçimi."),
 ("Katalog yeterli sayılır.",
  "Aynı animasyondan İngilizce/Almanca altyazılı sürüm ve kısa sosyal kesitler çıkar.",
  "Tek üretim, birden çok pazarda kullanılıyor — Galzura işinde tam olarak bunu yaptık."),
 ("Üretim durdurulur, çekim yapılır.",
  "Hat çalışırken çekim planı kuruyoruz; ışığı biz getiriyoruz.",
  "Üretim kaybı olmadan çekim tamamlanıyor."),
],
"mobilya": [
 ("Ürün beyaz fonda fotoğraflanır.",
  "Ürün gerçek bir mekâna yerleştirilir; mekân yoksa 3D olarak kurulur.",
  "Alıcı ürünü kendi evinde hayal edebiliyor; sepete atma kararı orada veriliyor."),
 ("Her renk/kumaş seçeneği için ayrı çekim yapılır.",
  "Bir kere modellenir, tüm varyantlar aynı sahneden çıkar.",
  "Yeni varyant eklemek yeni çekim değil, birkaç saatlik render işi."),
],
"otel": [
 ("Sezon başında bir kere çekilir, tüm yıl aynı görsel kullanılır.",
  "Sezon dışı görünmesi gereken sahneler 3D ile üretiliyor; gerçek çekim doğru ışıkta yapılıyor.",
  "Ocak ayında yaz rezervasyonu için elinizde yaz görseli oluyor."),
 ("Oda fotoğrafları geniş açıyla şişirilir.",
  "Gerçek ölçüde çekim + kat planı animasyonu.",
  "Yerinde hayal kırıklığı azalıyor; kötü yorum oradan çıkıyor."),
],
"isletme": [
 ("Tanıtım videosu çekilir, siteye konur, unutulur.",
  "Bir çekim gününden bir aylık içerik: uzun video, kısa kesitler, kapak görselleri, story kareleri.",
  "Aynı bütçe, dört haftalık görünürlük."),
 ("İçerik 'trend' üzerine kurulur.",
  "İçerik işin kendisinden çıkar: nasıl yapıldığı, kimin yaptığı, neyin neden öyle olduğu.",
  "Trend geçer, iş anlatımı kalıcıdır — ve müşteri asıl ona güveniyor."),
],
}


# ------------------------------------------------------------------ çalışma modeli
MODEL = {
"proje": {
  "ad": "Proje bazlı — tek iş",
  "kime": "Elinde net bir iş var: bir proje tanıtımı, bir ürün animasyonu, bir tanıtım filmi. "
          "Bir kere çekilecek, uzun süre kullanılacak.",
  "nasil": [
    "Kısa görüşme ve keşif — ne anlatacağımızı netleştiriyoruz",
    "Yazılı iş emri: çekim listesi, süre, teslim formatları",
    "Çekim / üretim günü",
    "Kurgu ve ilk sürüm",
    "İki revizyon hakkı",
    "Teslim: yatay + kare + dikey, altyazılı ve altyazısız, kapak görselleriyle",
  ],
  "sure": "Kapsamına göre 1–4 hafta",
  "odeme": "Başlangıçta %50, teslimde %50",
  "avantaj": "Tek seferlik bütçe; sonuç elinizde kalıyor, istediğiniz yerde istediğiniz kadar kullanıyorsunuz.",
  "dikkat": "Tek video tek anlatımdır. Sürekli görünürlük istiyorsanız aylık düzen daha doğru.",
},
"aylik": {
  "ad": "Aylık düzen — süreklilik",
  "kime": "Görünürlüğün sürmesi gereken işler: emlak portföyü, devam eden inşaat projesi, "
          "restoran, otel, mağaza, düzenli ürün çıkaran üretici.",
  "nasil": [
    "Ay başında içerik planı — ne çekilecek, ne yayınlanacak, hangi gün",
    "Ayda bir toplu çekim günü (gerektiğinde iki)",
    "Kurgu, tasarım, altyazı ve kapaklar",
    "Yayın takvimine göre teslim — siz sadece yayınlıyorsunuz",
    "Ay sonunda tek sayfalık ölçüm: gelen arama, profil görüntülenmesi, 'buradan gördüm' diyen müşteri",
    "Sonraki ayın planı ölçüme göre güncelleniyor",
  ],
  "sure": "Aylık, en az 3 ay önerilir (ilk ay ölçüm ayıdır)",
  "odeme": "Ay başında aylık bedel",
  "avantaj": "Birim maliyet proje bazlıya göre belirgin şekilde düşük; ekip işinizi öğrendikçe "
             "çekim süresi kısalıyor, çıkan iş iyileşiyor.",
  "dikkat": "İlk ayda büyük rakam beklenmemeli. Ölçüm ayıdır; kıyas ikinci aydan itibaren anlamlı.",
},
}

# Hangi sektörde hangi model daha çok oturuyor (öneri; teklif sırasında değiştirilebilir)
ONERILEN_MODEL = {
    "produksiyon": "aylik",
    "insaat":   "proje",    # proje süresi boyunca etap etap — sonra aylığa geçilebilir
    "emlak":    "aylik",    # portföy sürekli değişiyor
    "mimarlik": "proje",
    "sanayi":   "proje",
    "mobilya":  "aylik",    # sürekli yeni ürün
    "otel":     "aylik",    # sezon boyunca
    "isletme":  "aylik",
}


# ------------------------------------------------------------------ sorgular
def farklar(sektor, adet=5):
    """Sektöre özel farklar önce, sonra genel farklar."""
    l = list(SEKTOR.get(sektor, [])) + list(GENEL)
    return [{"sıradan": a, "bizde": b, "sonuc": c} for a, b, c in l[:adet]]


def model(sektor=None):
    """İki çalışma modeli + o sektörde hangisinin önerildiği."""
    o = ONERILEN_MODEL.get(sektor or "", "proje")
    return {"onerilen": o, "proje": MODEL["proje"], "aylik": MODEL["aylik"]}


def model_cumlesi(sektor):
    o = ONERILEN_MODEL.get(sektor, "proje")
    if o == "aylik":
        return ("Sizin işinizde aylık düzen daha çok oturuyor: anlatacak şey sürekli "
                "yenileniyor, tek video birkaç haftada eskiyor.")
    return ("Sizin işinizde önce proje bazlı tek bir iş mantıklı: ortada net bir "
            "anlatılacak şey var ve uzun süre kullanılacak. Sürekliliğe sonra karar verirsiniz.")
