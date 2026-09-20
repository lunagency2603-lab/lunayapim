# -*- coding: utf-8 -*-
"""
KURUMSAL SAYFALAR — trendsaphiens.com'un kendi künyesi.

20.09.2026: AdSense başvurusu öncesi yapılan denetimde çıktı — yayının kendi
alan adında gizlilik politikası, iletişim, hakkında ve kullanım koşulları
sayfaları yoktu (hepsi 404). Bu sayfalar lunayapim.com'da var ama
trendsaphiens.com kökünden sunulmuyor.

AdSense programı, başvuran sitede gizlilik politikası, açık iletişim yolu ve
yayıncının kim olduğunu anlatan bir sayfa arar. Reklam vermeye çalışan ama
künyesi olmayan site "düşük değerli içerik" sayılır.

Metinler TrendSaphiens'e özeldir: ne topladığımız, neyi toplamadığımız,
hangi üçüncü tarafların çerez kullandığı ve yayın ilkeleri açıkça yazılır.
"""
import datetime, io, json, os

from .ayarlar import SITE_KOK
from . import trend as T

KOK_URL = "https://lunayapim.com/trend/"
EPOSTA = "lunagency2603@gmail.com"
YAYINCI = "Luna Yapım"
SEHIR = "Bursa"


def _e(x):
    return T._e(x)


def _sayfa(slug, baslik, meta, h1, ozet, govde, sss=None, tur="WebPage"):
    url = KOK_URL + slug
    semalar = [json.dumps({
        "@context": "https://schema.org", "@type": tur, "name": h1, "url": url,
        "description": meta, "inLanguage": "tr-TR",
        "publisher": {"@type": "Organization", "name": YAYINCI, "url": "https://lunayapim.com/",
                      "email": EPOSTA, "address": {"@type": "PostalAddress", "addressLocality": SEHIR,
                                                   "addressCountry": "TR"}},
    }, ensure_ascii=False), json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "TrendSaphiens", "item": KOK_URL},
            {"@type": "ListItem", "position": 2, "name": h1, "item": url}]}, ensure_ascii=False)]
    if sss:
        semalar.append(json.dumps({
            "@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in sss]}, ensure_ascii=False))
    sema_html = "".join('<script type="application/ld+json">%s</script>' % x for x in semalar)
    sss_html = ""
    if sss:
        sss_html = ('<section class="ts-giris ts-sss"><h2>Sık sorulanlar</h2>%s</section>'
                    % "".join("<h3>%s</h3><p>%s</p>" % (_e(q), _e(a)) for q, a in sss))
    ic = """
<main class="ts-arac-sayfa ts-kurumsal">
  <div class="wrap">
    <nav class="ts-crumbs"><a href="./">TrendSaphiens</a></nav>
    <h1>%s</h1>
    <p class="ts-arac-ozet">%s</p>
    %s
    %s
    <p class="ts-not">Son güncelleme: %s</p>
    <p class="ts-arac-geri"><a href="./">← Akışa dön</a></p>
  </div>
</main>
""" % (_e(h1), _e(ozet), govde, sss_html, _e(T._tr_tarih(datetime.date.today().isoformat())))
    return T._bas(baslik, meta, url, None, sema_html, "website", "../", "") + ic + T._alt("../", "")


def hakkimizda_html():
    govde = """
<section class="ts-giris">
  <h2>TrendSaphiens nedir?</h2>
  <p>TrendSaphiens, Bursa merkezli yapım ve yazılım stüdyosu Luna Yapım'ın günlük yayınıdır.
  Türkiye'de o gün çok aranan konuları alır, kaynaklarına bakar ve okurun sorusunu doğrudan
  cevaplayan yazılara çevirir.</p>
  <p>Yayın iki kişilik bir stüdyonun kendi yazdığı sistemle işler: veri toplama, konu seçimi,
  yazım ve yayın adımlarının tamamı bu sistemin içindedir.</p>

  <h2>Yayın ilkelerimiz</h2>
  <p><b>Kaynak gösteririz.</b> Her maddenin dayandığı yayıncı ve tarih sayfanın içinde durur.
  Rakam yalnızca kaynakta varsa yazılır; yuvarlanmaz, güzelleştirilmez.</p>
  <p><b>Kopyalamayız.</b> Yazılar başka bir metnin yeniden ifade edilmiş hâli değildir. Farklı
  kaynakların olguları birleştirilip kendi cümlelerimizle anlatılır; doğrudan alıntı en çok bir
  cümledir ve kaynağıyla verilir.</p>
  <p><b>Bilinmeyeni bilinmiş gibi yazmayız.</b> Bir bilgi açıklanmamışsa sayfada "henüz
  açıklanmadı" diye geçer. Kaynaklar çelişiyorsa hangisinin ne dediği adıyla belirtilir.</p>
  <p><b>Eğlence ile ölçümü ayırırız.</b> Burç sayfalarında astrolojinin kendi yorumunu
  aktarırız ve bunun kişilik ölçen bir yöntem olmadığını her sayfada yazarız. Örüntü oyunu IQ
  puanı vermez. Vücut kitle indeksi hesaplayıcısı tanı koymaz.</p>

  <h2>Hangi bölümler var?</h2>
  <p>Haber, bugün aranan, piyasalar, dizi ve film, spor, burç, müzik, edebiyat, sanat,
  teknoloji, mühendislik ve sosyal medya. Bunlara ek olarak hesaplama araçları ve günün
  bülteni sayfası bulunur.</p>

  <h2>Düzeltme ve geri bildirim</h2>
  <p>Bir yazıda hata gördüğünüzde yazın: düzeltir ve sayfada belirtiriz. İletişim adresimiz
  aşağıdaki iletişim sayfasındadır.</p>

  <h2>Görseller nereden geliyor?</h2>
  <p>Kapak görselleri yalnız serbest lisanslı kaynaklardan alınır: Wikimedia Commons ve
  Openverse. Haber sitelerinin fotoğrafları, afişler ve maç görüntüleri kullanılmaz; bunlar
  yayıncının telifindedir. Her görselin eser adı, üreteni ve lisansı sayfada durur.</p>

  <h2>Yapay zekâ kullanımı</h2>
  <p>Yazıların hazırlanmasında yapay zekâ kullanılır: kaynak taraması, olgu çıkarımı ve
  taslak yazım bu sistemle yapılır. Kaynak seçimi, doğrulama ve yayın kararı insandadır.
  Üretilen görsel kullanıldığında sayfada açıkça belirtilir.</p>

  <h2>Neden bir yapım şirketi yayın tutuyor?</h2>
  <p>Luna Yapım'ın işi sektörün nabzına bağlı. Konut satışı düştüğünde satış ofisinin
  görsele ihtiyacı artar; reklamda yapay zekâ etiketi zorunlu olunca gerçek çekimin değeri
  değişir. Bunları izlemek işimizin parçası; yayın da bu izlemenin okura açılmış hâli.</p>
</section>
"""
    sss = [("TrendSaphiens'i kim yayınlıyor?", "Bursa merkezli Luna Yapım. Yayın, stüdyonun kendi yazdığı sistemle günlük olarak derlenir."),
           ("Yazılar nasıl hazırlanıyor?", "Günün çok aranan konuları belirlenir, en az iki bağımsız yayıncıdan olgular toplanır ve yazı kendi cümlelerimizle yazılır. Kaynaklar sayfanın sonunda listelenir."),
           ("Yayında reklam var mı?", "Evet, Google AdSense üzerinden reklam gösterilebilir. Reklamlar içeriği etkilemez; hangi konunun yazılacağına reklam veren karar vermez.")]
    return _sayfa("hakkimizda", "Hakkımızda — TrendSaphiens yayın künyesi",
                  "TrendSaphiens'i kim yayınlıyor, yazılar nasıl hazırlanıyor, yayın ilkeleri neler? Luna Yapım'ın günlük yayınının künyesi.",
                  "Hakkımızda", "Bu yayını kim çıkarıyor, nasıl çalışıyor ve neye söz veriyor.", govde, sss, "AboutPage")


def iletisim_html():
    govde = """
<section class="ts-giris">
  <h2>Bize nasıl ulaşırsınız?</h2>
  <p>Düzeltme, geri bildirim, telif bildirimi ve reklam soruları için e-posta adresimiz:</p>
  <p class="ts-iletisim-eposta"><a href="mailto:%s">%s</a></p>
  <p>Yayıncı: %s · %s, Türkiye</p>

  <h2>Düzeltme talebi</h2>
  <p>Bir yazıda hatalı bilgi olduğunu düşünüyorsanız sayfanın adresini ve hangi bilginin
  yanlış olduğunu yazın. Kaynağını da eklerseniz daha hızlı sonuçlanır. Doğrulanan
  düzeltmeler sayfanın içinde belirtilir.</p>

  <h2>Telif bildirimi</h2>
  <p>Sayfalarımızdaki görseller yalnız serbest lisanslı kaynaklardan (Wikimedia Commons ve
  Openverse) alınır ve künyesiyle yayımlanır. Size ait bir eserin izinsiz kullanıldığını
  düşünüyorsanız yazın; inceleyip gerekirse kaldırırız.</p>

  <h2>Reklam ve iş birliği</h2>
  <p>Yayında Google AdSense reklamları gösterilir. Doğrudan reklam ve iş birliği talepleri
  için aynı adresten yazabilirsiniz. Haber ve analiz içeriği reklam ilişkisinden bağımsızdır.</p>

  <h2>Konu önerisi</h2>
  <p>Merak ettiğiniz, arattığınızda doğru dürüst cevap bulamadığınız bir konu varsa yazın.
  Günlük konu seçimi çok aranan başlıklardan yapılır, ama okurdan gelen sorular da listeye
  girer. Sorunuzu neden aradığınızı da yazarsanız yazı daha isabetli olur.</p>

  <h2>Kurumsal talepler</h2>
  <p>Luna Yapım aynı zamanda video prodüksiyon, 3D görselleştirme ve yazılım işleri yapar.
  Bu konulardaki talepler için lunayapim.com üzerindeki iletişim sayfasını kullanın; bu adres
  yayının kendisiyle ilgili konular içindir.</p>

  <h2>Yanıt süresi</h2>
  <p>E-postalar iş günlerinde okunur. Düzeltme bildirimleri öncelikli sırada değerlendirilir;
  diğer talepler birkaç gün içinde yanıtlanır.</p>

  <h2>Yazıda adı geçenler için</h2>
  <p>Bir yazıda adınız ya da kurumunuz geçiyorsa ve eksik veya yanlış aktarıldığını
  düşünüyorsanız yazın. Açıklamanızı kaynak göstererek sayfaya ekleriz; gerekiyorsa
  ilgili bölümü yeniden yazarız. Bu talepler için ayrı bir ücret ya da koşul yoktur.</p>
</section>
""" % (EPOSTA, EPOSTA, YAYINCI, SEHIR)
    sss = [("Düzeltme talebim ne kadar sürede sonuçlanır?", "Talepler günlük yayın turunda değerlendirilir. Doğrulanan düzeltme aynı gün sayfaya işlenir."),
           ("Yazılarınızı alıntılayabilir miyim?", "Kaynak göstererek ve bağlantı vererek kısa alıntı yapabilirsiniz. Yazının tamamını kopyalamak için izin isteyin.")]
    return _sayfa("iletisim", "İletişim — TrendSaphiens yayınına ulaşın",
                  "TrendSaphiens'e düzeltme, geri bildirim, telif bildirimi ve reklam konularında nasıl ulaşabileceğinizi anlatan iletişim sayfası.",
                  "İletişim", "Düzeltme, telif ve reklam için doğrudan ulaşın.", govde, sss, "ContactPage")


def gizlilik_html():
    govde = """
<section class="ts-giris">
  <h2>Kısaca</h2>
  <p>Bu yayın üyelik istemez, form doldurtmaz ve sizden kişisel bilgi toplamaz. Hesaplama
  araçlarına girdiğiniz veriler tarayıcınızdan çıkmaz. Ziyaret istatistiği ve reklam için
  üçüncü taraf hizmetler çerez kullanır; ayrıntısı aşağıda.</p>

  <h2>Topladığımız veriler</h2>
  <p><b>Ziyaret istatistiği.</b> Hangi sayfaların kaç kez görüntülendiğini ölçeriz. Bu ölçüm
  sayfa adresini, yaklaşık konumu (ülke/şehir düzeyinde), cihaz türünü ve yönlendiren adresi
  içerir. Adınız, e-postanız ya da kimliğiniz bu kayıtlarda yer almaz.</p>
  <p><b>Okunma sayacı.</b> Bir yazının gerçekten okunup okunmadığını anlamak için sayfada
  geçirilen süreyi ve kaydırma oranını ölçen kendi sayacımız çalışır. Kayıt kişiye bağlı
  değildir; aynı yazının aynı bağlantıdan tekrar sayılmaması için kısa süreli bir teknik
  kilit kullanılır.</p>
  <p><b>Araç sayfaları.</b> Yükselen burç, yaş, vücut kitle indeksi ve yüzde hesaplayıcıları
  ile örüntü oyunu tamamen tarayıcınızda çalışır. Doğum tarihiniz, saatiniz, boy ve kilonuz
  ya da oyun cevaplarınız hiçbir sunucuya gönderilmez, kaydedilmez.</p>

  <h2>Çerezler ve üçüncü taraflar</h2>
  <p><b>Google AdSense.</b> Sayfalarda reklam gösterilir. Google ve iş ortakları, ilgi alanına
  dayalı reklam sunmak için çerez kullanabilir. Reklam kişiselleştirmesini Google'ın reklam
  ayarları sayfasından kapatabilirsiniz.</p>
  <p><b>Google Analytics.</b> Ziyaret istatistiği için kullanılır. IP adresi Google tarafından
  işlenir; ölçüm kimliğe bağlanmaz.</p>
  <p>Çerezleri tarayıcı ayarlarınızdan engelleyebilir ya da silebilirsiniz. Engellediğinizde
  yayının içeriği aynen çalışmaya devam eder.</p>

  <h2>Verilerin paylaşımı</h2>
  <p>Ziyaretçi verilerini satmayız ve pazarlama amacıyla üçüncü taraflara aktarmayız. Yukarıda
  adı geçen ölçüm ve reklam hizmetleri dışında veri paylaşımı yoktur.</p>

  <h2>Haklarınız</h2>
  <p>6698 sayılı Kişisel Verilerin Korunması Kanunu kapsamında, işlenen verilerinizle ilgili
  bilgi talep etme, düzeltilmesini ya da silinmesini isteme haklarınız vardır. Talebinizi
  iletişim sayfasındaki adrese iletebilirsiniz.</p>

  <h2>Değişiklikler</h2>
  <p>Bu metin değiştiğinde sayfanın altındaki güncelleme tarihi yenilenir.</p>
</section>
"""
    sss = [("Hesaplama araçlarına girdiğim bilgiler kaydediliyor mu?", "Hayır. Doğum tarihi, saat, boy, kilo gibi bilgiler tarayıcınızda işlenir ve hiçbir sunucuya gönderilmez."),
           ("Reklam çerezlerini nasıl kapatırım?", "Google'ın reklam ayarları sayfasından kişiselleştirilmiş reklamı kapatabilir, tarayıcı ayarlarından çerezleri tümüyle engelleyebilirsiniz."),
           ("Üyelik ya da form var mı?", "Yayında üyelik yoktur. İsteğe bağlı bülten aboneliği dışında hiçbir form kişisel bilgi toplamaz.")]
    return _sayfa("gizlilik", "Gizlilik ve Çerez Politikası — TrendSaphiens",
                  "TrendSaphiens hangi verileri topluyor, hangi çerezler kullanılıyor, hesaplama araçlarına girilen bilgilere ne oluyor? Açık anlatım.",
                  "Gizlilik ve çerez politikası",
                  "Ne topluyoruz, neyi toplamıyoruz ve hangi üçüncü taraflar devrede.", govde, sss)


def kosullar_html():
    govde = """
<section class="ts-giris">
  <h2>İçeriğin kullanımı</h2>
  <p>Bu yayındaki yazılar Luna Yapım'a aittir. Kaynak göstererek ve bağlantı vererek kısa
  alıntı yapabilirsiniz. Yazının tamamını ya da büyük bölümünü başka bir yerde yayımlamak
  için önceden izin alınması gerekir.</p>
  <p>Sayfalardaki görseller serbest lisanslı kaynaklardan alınır ve her birinin künyesi
  görselin yanında belirtilir. Bu görselleri kullanacaksanız kendi lisans koşullarına
  uymanız gerekir.</p>

  <h2>Bilgilerin doğruluğu</h2>
  <p>Yazılar yayın anında erişilebilen kaynaklara dayanır ve her maddede kaynak belirtilir.
  Kaynaklardaki bilgi sonradan değişebilir; sayfalar geriye dönük olarak her zaman
  güncellenmeyebilir. Tarih bilgisi her sayfanın içinde durur.</p>
  <p>Piyasa sayfalarındaki kur ve altın verileri kaynağından alınmış bilgilerdir, yatırım
  tavsiyesi değildir. Alım satım kararlarınızı bu sayfalara dayanarak vermeyin.</p>
  <p>Sağlıkla ilgili hesaplayıcılar tarama aracıdır, tıbbi tanı ya da tedavi önerisi değildir.
  Astroloji bölümü kültürel ve eğlence amaçlıdır; kişiliği ya da geleceği ölçmez.</p>

  <h2>Dış bağlantılar</h2>
  <p>Yazılarda kaynak yayıncılara bağlantı verilir. Bu sitelerin içeriğinden ve gizlilik
  uygulamalarından sorumlu değiliz.</p>

  <h2>Sorumluluk</h2>
  <p>Yayındaki bilgilerin kullanımından doğan sonuçlardan Luna Yapım sorumlu tutulamaz.
  Hatalı gördüğünüz bilgiyi bildirirseniz inceleyip düzeltiriz.</p>

  <h2>Hesaplama araçları</h2>
  <p>Araç sayfalarındaki hesaplar tarayıcınızda çalışır ve girdiğiniz veriler bize
  ulaşmaz. Sonuçlar bilgilendirme amaçlıdır. Yükselen burç hesabı gökyüzü konumunu doğru
  bulur; bu konumun kişilikle ilişkisi astrolojinin kendi yorumudur ve bilimsel bir iddia
  taşımaz.</p>
  <p>Resmî işlem gerektiren hesapları (emeklilik, tazminat, vergi) bilerek yayınlamıyoruz.
  Bu konularda ilgili kurumun kendi aracını kullanın.</p>

  <h2>Yayının sürekliliği</h2>
  <p>Sayfalar günlük olarak yeniden derlenir. Bir bölümde o gün kaynak bulunamazsa o bölüm
  boş kalabilir; eski sayfalar adresini korur. Yayın durdurulursa mevcut adreslerin
  erişilebilir kalması için gerekli yönlendirmeler yapılır.</p>

  <h2>Bu koşullardaki değişiklikler</h2>
  <p>Koşullar değiştiğinde sayfanın altındaki tarih güncellenir. Değişiklikten sonra yayını
  kullanmaya devam etmeniz güncel koşulları kabul ettiğiniz anlamına gelir.</p>
</section>
"""
    return _sayfa("kosullar", "Kullanım Koşulları — TrendSaphiens",
                  "TrendSaphiens içeriğinin kullanım koşulları: alıntı kuralları, görsel lisansları, bilgilerin doğruluğu ve sorumluluk sınırları.",
                  "Kullanım koşulları", "Alıntı kuralları, lisanslar ve sorumluluk sınırları.", govde)


SAYFALAR = [
    ("hakkimizda", "Hakkımızda", hakkimizda_html),
    ("iletisim", "İletişim", iletisim_html),
    ("gizlilik", "Gizlilik ve çerezler", gizlilik_html),
    ("kosullar", "Kullanım koşulları", kosullar_html),
]


def yayinla(kok=None):
    kok = kok or SITE_KOK
    d = os.path.join(kok, "trend")
    os.makedirs(d, exist_ok=True)
    yazilan = []
    for slug, _ad, fn in SAYFALAR:
        io.open(os.path.join(d, slug + ".html"), "w", encoding="utf-8").write(fn())
        yazilan.append(slug)
    y = os.path.join(kok, "sitemap.xml")
    try:
        s = io.open(y, encoding="utf-8").read()
        bugun = datetime.date.today().isoformat()
        ek = ['  <url><loc>%s%s</loc><lastmod>%s</lastmod><changefreq>yearly</changefreq><priority>0.4</priority></url>'
              % (KOK_URL, slug, bugun) for slug in yazilan if (KOK_URL + slug) not in s]
        if ek:
            s = s.replace("</urlset>", "\n".join(ek) + "\n</urlset>")
            io.open(y, "w", encoding="utf-8").write(s)
    except Exception as ex:
        print("sitemap:", ex)
    return {"kurumsal": yazilan}


if __name__ == "__main__":
    print(json.dumps(yayinla(), ensure_ascii=False))
