# -*- coding: utf-8 -*-
"""
TRENDSAPHIENS — LunaTrendSaphiens: günün haberleri, analizler, raporlar, sistem.
Ana siteden ayrı tasarım (açık tema, kart akışı), aynı depo: /trend/

Kaynaklar (hepsi zaten üretilmiş, kopya değil):
  · veri/gundem/*.json           → günün haberleri (her madde kendi sayfası)
  · blog/*.html                  → analiz/rehber kartları (blog sayfasına bağlanır)
  · bulten/*.html + veri/bulten  → raporlar (haftalık karne)
  · ORGANLAR (aşağıda)           → "sonuç veren organlarımız" — nasıl yaptığımızı anlatmadan

Kurallar:
  · Uydurma rakam yok; sayı yalnızca kaynakta geçiyorsa yazılır.
  · Piyasa tarafında yatırım tavsiyesi, fiyat hedefi, al/sat yok; risk bloğu her rapor sayfasında.
  · Her sayfa paylaşım çubuğu taşır (X, WhatsApp, bağlantı). X'e otomatik paylaşım: x_paylas.py.
  · SEO kapısı: üretimden sonra seo.denetci çalışır.
"""
import datetime, html, json, os, re, sys, unicodedata

from .ayarlar import SITE_KOK, KOK_DIZIN

AY = ["Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"]
KOK_URL = "https://lunayapim.com/trend/"
ADSENSE = "ca-pub-3059196718190568"

KATEGORI = {
    "gundem":      ("Gündem",       "Günün haberleri, kaynaklı ve tarihli"),
    "aranan":      ("Bugün Aranan", "Türkiye bugün ne aradı — günlük liste"),
    "piyasa":      ("Piyasalar",    "Dolar, euro, altın ve piyasayı okuyan sistemin defteri"),
    "ekran":       ("Dizi & Film",  "Vizyondakiler, yeni bölümler, platform yayınları"),
    "spor":        ("Spor Ekranı",  "Maç hangi kanalda, saat kaçta"),
    "sanat":       ("Sanat",        "Sergi, sahne, konser"),
    "teknoloji":   ("Teknoloji",    "Yapay zekâ, yazılım, üretim araçları"),
    "muhendislik": ("Mühendislik",  "Üretim, enerji, otomotiv, altyapı"),
    "sosyal-medya":("Sosyal Medya", "Platformlar, akımlar, içerik üreticisi"),
    "analiz":      ("Analiz",       "Sektörü okuyan yazılar"),
    "rapor":       ("Rapor",        "Haftalık karneler ve ölçümler"),
    "sehir":       ("Şehir",        "Bursa ve 81 il"),
    "sistem":      ("Sistem",       "Sonuç veren organlarımız"),
}
# geniş bölüm anahtarı (trend_izle.BOLUMLER) → kategori
BOLUM_KAT = {"piyasalar": "piyasa", "ekran": "ekran", "spor": "spor", "sanat": "sanat", "yapay-zeka": "teknoloji",
             "yazilim": "teknoloji", "muhendislik": "muhendislik", "sosyal-medya": "sosyal-medya"}
BOLUM_GORSEL = {"piyasa": "../video/karga-k3", "ekran": "renk-masasi", "spor": "../video/karga-k5", "sanat": "set-isik",
                "teknoloji": "render-istasyonu", "muhendislik": "render-istasyonu", "sosyal-medya": "../video/karga-k2", "aranan": "../video/karga-k6"}
KAT_GIRIS = {
    "gundem": "Her sabah inşaat, konut, emlak, sanayi, turizm ve tanıtım sektörlerinden günün haberleri taranır; işimize dokunanlar seçilir. Her madde kaynağı ve tarihiyle durur, altında tek bir soru cevaplanır: bu bizim için ne demek? Haberi yeniden yazmıyoruz; olgu kaynaktan, analiz bizden. Rakam yalnızca kaynakta geçiyorsa yazılır; tahmin ve projeksiyon bu sayfada yok.",
    "analiz": "Analiz yazıları haberin bir adım ötesi: bir gelişmenin bir inşaat firmasının, bir emlak ofisinin ya da bir üreticinin tanıtım kararını nasıl değiştirdiğini anlatır. Fiyat bantları, teslim süreleri ve kontrol listeleri gerçek işlerden gelir. Uzun yazılar blogda, kısa okumalar burada.",
    "rapor": "Raporlar ölçümdür, yorum değil. Haftalık karne, piyasayı okuyan sistemin yedi günlük sonucunu kazanan ve kaybeden bütün kayıtlarla verir; seçme yapılmaz. Sektör raporları ise TÜİK, sahibindex ve sektör derneklerinin yayınladığı verilerin kısa okumasıdır. Hiçbir rapor yatırım tavsiyesi değildir.",
    "piyasa": "Piyasa bölümü KDA Matrix'in kanıt defterinden beslenir: sistem neye baktı, hangi hatlar sınavı geçti, hangileri elendi. Fiyat hedefi, al-sat önerisi ya da açık pozisyon paylaşılmaz; sonuçlar kapanışta doğrulandıktan sonra yazılır. Kripto ve hisse piyasaları yüksek risk taşır.",
    "sehir": "Şehir bölümü Bursa'dan başlar, 81 ile uzanır: yatırım gündemi, sanayi ve turizm haberleri, ilan ve konut piyasasının yerel görünümü. Her ilin kendi sayfası ana sitede; burada günün gelişmesi ve o ilde ne anlama geldiği yazılır.",
    "teknoloji": "Teknoloji bölümü yapay zekâ ile görsel ve video üretimi, reklam düzenlemeleri, yazılım ve üretim araçlarını izler. Hangi aracın neye yaradığını gerçek kullanımdan anlatırız; etiket zorunluluğu, telif ve gizlilik gibi kuralları da atlamayız.",
}

KAT_IZLEME = {
    "gundem": ("Neyi izliyoruz", "TÜİK konut satış ve yapı ruhsatı verileri, sahibindex ve Endeksa piyasa raporları, kentsel dönüşüm kararları, sanayi üretimi ve ihracat rakamları, fuar takvimi, otel ve turizm yatırımları, mobilya ve dekorasyon sektörü, yapay zekâ ile reklam düzenlemeleri, küçük işletmelerin sosyal medya kullanımı ve Bursa'nın yatırım gündemi. Siyaset, asayiş, spor, magazin ve döviz-borsanın günlük hareketi bu sayfaya girmez.", [("../hizmetler/", "Prodüksiyon hizmetleri"), ("../gundem/", "Gündem arşivi"), ("../blog/", "Blog")]),
    "analiz": ("Nasıl yazıyoruz", "Her analiz bir soruyla başlar: bu gelişme kimin hangi kararını değiştirir? Cevap gerçek bir işten gelir — bir satış ofisinin görsel ihtiyacı, bir emlak ofisinin ilan süresi, bir üreticinin fuar takvimi. Fiyat yazıyorsak sitede yayınlanmış banttır; süre yazıyorsak teslim ettiğimiz işlerin ortalamasıdır. Kaynak göstermeden sayı vermeyiz.", [("../fiyatlar", "Fiyat listesi"), ("../blog/", "Uzun yazılar"), ("../studyo", "Nasıl çalışıyoruz")]),
    "rapor": ("Raporun anatomisi", "Haftalık karne dört bölümden oluşur: sistemin taradığı hareket sayısı, ham isabet oranı (kazanan ve kaybeden bütün sinyaller dahil), sınavı geçen ve elenen hatlar, sistemin dikkatinin kaydığı bölgeler. Bir hat kırk sonuçlanmış sinyal biriktirmeden yayına çıkmaz; elenen hat listeden silinmez, mezarlığa kaldırılır. Sayı, sistemin kendi kaydıdır; insan eli değmez.", [("../bulten/", "Matrix Bülteni"), ("../bulten/00-sistem", "Sistem nasıl çalışıyor"), ("../matrix", "Kanıt defteri")]),
    "piyasa": ("Ne paylaşmıyoruz", "Açık pozisyon, fiyat hedefi, alım-satım önerisi ve \"şu coin patlayacak\" cümlesi bu bölümde yoktur. Hangi hattın hangi sinyali verdiği ancak sonuç kapanışta doğrulandıktan sonra yazılır. Kripto varlık ve hisse piyasaları yüksek risk taşır; yatırdığınız tutarın tamamını kaybedebilirsiniz. Bu bölüm bir araştırma sisteminin şeffaf günlüğüdür, başka bir şey değil.", [("../matrix", "Kanıt defteri"), ("../bulten/", "Haftalık karne"), ("../kosullar", "Koşullar")]),
    "sehir": ("Bursa'dan 81 ile", "Bursa; otomotiv, tekstil ve mobilya sanayisi, Uludağ turizmi ve kentsel dönüşüm projeleriyle bizim sahamız. Diğer 80 il için her ilin kendi sayfası ana sitede: o ilde hangi hizmeti verdiğimiz, yerel sektör yapısı ve teslim takvimi. Buradaki haberler o sayfalara bağlanır; drone çekimi 81 ilin tamamında.", [("../sehir/bursa", "Bursa sayfası"), ("../sehir/", "Tüm iller"), ("../hizmetler/drone-fpv", "Drone çekimi")]),
    "teknoloji": ("Kullandığımız araçlar", "Görsel ve video üretiminde Runway ve Higgsfield, tel kafes ve hareketli grafikte kendi kodumuz, kurgu ve kodlamada ffmpeg; siteyi ve bu yayını Luna Pusula işletir. Yapay zekâ ile üretilen her görsel teslimde işaretlenir. Hangi aracın nerede işe yaradığını ve nerede yaramadığını gerçek denemelerden yazarız.", [("../yapay-zeka/", "Yapay zekâ sayfası"), ("../yazilim", "Yazılım"), ("../studyo", "Stüdyo")]),
}

# hizmet sayfası → kategori, görsel
HIZMET_KAT = {
    "hizmetler/insaat-3d-modelleme.html": ("gundem", "render-istasyonu", "İnşaat"),
    "hizmetler/emlak-kurumsal.html":      ("gundem", "drone-safak", "Emlak"),
    "hizmetler/urun-animasyon.html":      ("teknoloji", "set-isik", "Reklam"),
    "hizmetler/drone-fpv.html":           ("sehir", "drone-safak", "Havadan"),
    "hizmetler/isletme-tanitim.html":     ("gundem", "set-isik", "İşletme"),
    "hizmetler/klip-cekimi.html":         ("gundem", "renk-masasi", "Müzik"),
    "sehir/bursa.html":                   ("sehir", "drone-safak", "Bursa"),
}
GORSEL_KAT = {"gundem": "set-isik", "analiz": "renk-masasi", "rapor": "../video/karga-k5", "piyasa": "../video/karga-k3",
              "sehir": "drone-safak", "teknoloji": "render-istasyonu", "sistem": "../video/karga-k6"}
# <title> için kısa alt başlık (70 karakter sınırı)
KAT_KISA = {
    "aranan": "Türkiye bugün ne aradı", "piyasa": "Dolar, euro, altın bugün", "ekran": "Vizyon, dizi, platform",
    "spor": "Maç hangi kanalda", "sanat": "Sergi, sahne, konser", "teknoloji": "Yapay zekâ ve yazılım",
    "muhendislik": "Üretim, enerji, altyapı", "sosyal-medya": "Platformlar ve akımlar", "gundem": "Günün haberleri",
    "analiz": "Sektörü okuyan yazılar", "rapor": "Haftalık karneler", "sehir": "Bursa ve 81 il", "sistem": "Sonuç veren organlar",
}
# Bölümün çalışma düzeni — sayfada "Ne zaman, nasıl güncellenir" bloğu (takvim.py ile uyumlu)
KAT_DUZEN = {
    "aranan": ("Ne zaman, nasıl güncellenir", "Liste her sabah Google Trends'in Türkiye beslemesinden alınır ve gün içinde bir kez daha yenilenir. Her başlığın altında Google'ın bağladığı haberin kaynağı ve adresi durur; kaynağı olmayan başlık listeye girmez. Günün sayfası tarihle arşivlenir, böylece 'geçen hafta ne aranmıştı' sorusunun cevabı da burada kalır. Sık aranan kalıcı sorular — dolar kaç TL, maç hangi kanalda, bu hafta vizyonda ne var — kendi bölümlerine yönlendirilir; bu sayfa günün anlık merakını tutar."),
    "ekran": ("Ne zaman, nasıl güncellenir", "Vizyon listesi cuma sabahı çıkar; yeni dizi ve platform yayınları hafta içinde eklenir. Her madde dağıtımcı ya da yayıncı haberinin kaynağına bağlanır; süre, tür ve nerede izlendiği yazılır, puan verilmez. Afiş ve fragman yayıncıya aittir, buraya alınmaz; görsel yalnızca bizim çektiğimiz ya da ürettiğimiz kareler olur. Bir yapım şirketi olarak eklediğimiz katman şu: bir sahnenin nasıl çekildiğini, hangi ışıkla kurulduğunu arada yazarız."),
    "spor": ("Ne zaman, nasıl güncellenir", "Hafta sonu maçları cumartesi ve pazar sabahı, hafta içi maçlar oynandığı gün listelenir; her satırda yayıncı kanal, saat ve haberin kaynağı vardır. Yayın hakları sezon içinde değişebildiği için maddede tarih durur ve eski sayfa güncellenmez, yenisi açılır. Skor, tahmin ve bahis içeriği yoktur; amaç doğru ekranı bulmanızdır. Millî maç ve derbi günleri takvimde önceden işaretlenir."),
    "sanat": ("Ne zaman, nasıl güncellenir", "Haftanın sergi, sahne ve konser takvimi cuma öğleden sonra çıkar; şehir bazlı ekler hafta içinde gelir. Her madde mekânın ya da organizatörün duyurusuna bağlanır; tarih, mekân ve bilet bilgisi yazılır, yorum yazılmaz. Bizim tarafımızdan gelen katman: sergi ve sahne ışığı, konser kaydı ve mekân çekimi bizim işimiz; bir etkinliği nasıl belgelediğimizi arada anlatırız. Bursa'daki galeriler, devlet tiyatrosu ve konser mekânları ile İstanbul'un büyük sergileri birlikte izlenir; ücretsiz etkinlikler ayrıca işaretlenir ki hafta sonu planı yapan okur tek bakışta görsün."),
    "muhendislik": ("Ne zaman, nasıl güncellenir", "Üretim, enerji, otomotiv ve altyapı haberleri her sabah taranır; seçilen maddeler kaynağıyla listelenir. Teknik rakam yalnızca haberde geçiyorsa yazılır; tahmin ve abartı yoktur. Fabrika ve tesis tanıtımı bizim iş alanımız olduğu için bu bölüm ayrıca 'bir tesis nasıl çekilir, bir üretim hattı nasıl anlatılır' yazılarıyla beslenir. Bursa'nın otomotiv, tekstil ve makine sanayisi bu bölümün doğal odağıdır; organize sanayi bölgelerinden gelen duyurular ve yerli üretim haberleri öne alınır, ihale ve teşvik haberlerinde resmî kaynak aranır."),
    "sosyal-medya": ("Ne zaman, nasıl güncellenir", "Platform değişiklikleri ve akımlar her sabah taranır; küçük işletmeyi ilgilendiren maddeler öne alınır. Her madde platformun kendi duyurusuna ya da haberin kaynağına bağlanır. Sosyal medya yönetimi bizim hizmetimiz olduğu için burada gerçekten söyleyecek sözümüz var: bir değişikliğin işletme hesabına ne yaptığını, ne yapılması gerektiğini kısa ve kaynaklı yazarız. Algoritma söylentileri ile platformun resmî duyurusu ayrı tutulur; söylenti, kaynağı yazılarak ve öyle olduğu belirtilerek girer. Reklamda yapay zekâ etiketi gibi mevzuat değişiklikleri de burada, resmî metnine bağlanarak duyurulur."),
}
# Sık sorulanlar — bölüm sayfasında FAQ bloğu + FAQPage şeması (arayanın sorduğu biçimde)
KAT_SSS = {
    "aranan": [("Liste kimin listesi?", "Google Trends'in Türkiye için yayınladığı günlük listedir; biz sıralamayı değiştirmeyiz, yalnızca her başlığın yanına kaynağını ve bir cümlelik çerçeveyi ekleriz."),
               ("Dünkü liste nerede?", "Her gün ayrı sayfa olarak arşivlenir; bölüm sayfasındaki akıştan tarihe göre geçilir."),
               ("Neden bazı başlıklar yok?", "Google'ın bir haber bağlamadığı ya da kaynağı belirsiz başlıkları yayınlamayız; kaynaksız madde bu sitede yoktur.")],
    "ekran": [("Bu hafta vizyona giren filmler ne zaman yayınlanır?", "Cuma sabahı; dağıtımcı listeleri ve yayıncı haberleri kaynağıyla eklenir."),
              ("Dizi önerisi nasıl seçiliyor?", "Beğeniyle değil ölçütle: tür, süre, nerede yayında ve kaynağı. Puan vermeyiz."),
              ("Fragman ve afiş neden yok?", "Yayıncının telifidir; sayfada yalnızca bizim çektiğimiz ya da ürettiğimiz görseller bulunur.")],
    "spor": [("Maç hangi kanalda bilgisi nereden geliyor?", "Yayıncı kuruluşun ya da haber kaynağının duyurusundan; her satırda kaynak adresi ve tarih durur."),
             ("Derbi ve millî maç günleri nasıl takip edilir?", "Takvim kutusunda önceden işaretlenir; maç günü sayfa sabah yenilenir."),
             ("Skor ve tahmin var mı?", "Yok. Bu bölüm yalnızca doğru ekranı ve saati bulmanız içindir; bahis içeriği barındırmaz.")],
    "sanat": [("Sergi ve konser listesi hangi şehirleri kapsar?", "Öncelik Bursa ve büyük şehirler; kaynaklı duyuru olan her etkinlik girebilir."),
              ("Bilet bilgisi güncel mi?", "Maddede duyurunun tarihi yazar; bilet ve saat için organizatörün bağlantısına gidilir."),
              ("Etkinliğimizi nasıl ekletiriz?", "Duyurunuzun adresini iletişim sayfasından gönderin; kaynaklı ve tarihli olması yeter.")],
    "muhendislik": [("Hangi haberler seçiliyor?", "Üretim, enerji, otomotiv ve altyapıda o günün gelişmesi; teknik rakam yalnızca haberde geçiyorsa yazılır."),
                    ("Kaynak olarak neye güveniyorsunuz?", "Kurumun kendi duyurusu ve ulusal haber kaynakları; her maddede adres durur."),
                    ("Fabrika tanıtımı ile bağlantısı ne?", "Tesis ve üretim hattı çekimi bizim işimiz; bir tesisin nasıl anlatıldığını arada yazarız.")],
    "sosyal-medya": [("Platform değişiklikleri ne sıklıkla güncellenir?", "Her sabah taranır; işletme hesabını etkileyen değişiklik aynı gün girer."),
                     ("Akımları nasıl seçiyorsunuz?", "Kaynaklı ve tarihli olanları; yalnızca 'viral' diye yazılmış maddeyi almayız."),
                     ("Küçük işletme için ne anlama geldiğini kim yazıyor?", "Sosyal medya yönetimi hizmetimizin içinden, iki kişilik ekibimiz; kısa, kaynaklı ve deneyimden.")],
}
KAT_GIRIS_EK = {
    "aranan": "Her sabah Google Trends'in Türkiye listesini alır, her başlığın yanına Google'ın bağladığı haberi (kaynak ve adres) koyarız. Bizim eklediğimiz tek şey bir cümlelik çerçeve: neden arandı, nereye bakılır. Liste Google'ındır, sıralama Google'ındır; biz okunur hâle getiririz.",
    "ekran": "Vizyona girenler, yeni bölümler ve platform yayınları; her madde kaynağıyla. Öneri yazarken beğeniyi değil ölçütü söyleriz: tür, süre, nerede yayında. Fragman ve afiş yayıncıya aittir, buraya alınmaz.",
    "spor": "Maç hangi kanalda, saat kaçta: yayıncı bilgisi her zaman kaynağıyla verilir; yayın hakları değişebildiği için maddede tarih durur. Skor ve yorum yok; ekranı bulmanız için varız.",
    "sanat": "Sergi, tiyatro, konser ve festival: tarih, mekân, kaynak. Kendi işimizden gelen katman ise şu: sahne ışığı, renk ve kamera bizim de mesleğimiz; bir sergiyi nasıl çekeriz, bir konseri nasıl kaydederiz — arada yazarız.",
    "muhendislik": "Üretim, enerji, otomotiv ve altyapı haberleri; yerli üretim ve büyük projelerde günün gelişmesi. Teknik ayrıntıya kaynağıyla gireriz; abartı yok.",
    "sosyal-medya": "Platform değişiklikleri, akımlar ve içerik üreticisine etkisi. Küçük işletme için ne demek — bizim işimiz olduğu için burada gerçekten söyleyecek sözümüz var.",
}

# Sonuç veren organlar — ne yaptığı bir cümle, nasıl yaptığı yok.
ORGANLAR = [
    ("Gözcü",     "Piyasayı ve siteyi kesintisiz izler; sapmayı ilk o görür."),
    ("Aday",      "Yeni okuma hatlarını kuluçkaya alır; kanıt biriktirmeden sahaya çıkarmaz."),
    ("Rejim",     "Piyasanın hangi mevsimde olduğunu söyler; sistem vitesini ona göre değiştirir."),
    ("Beyin",     "Hatların puanını tutar, terfi ve tenzil kararını verir."),
    ("İcra",      "Kararı uygular; dalga, boyut ve zaman kurallarına uyar."),
    ("Bekçi",     "Her şeyi durdurabilen tek organ; kilit, kill-switch ve gece nöbeti onda."),
    ("Ekspertiz", "Sistemi kendi kendine denetler; mantık hatasını yayına çıkmadan yakalar."),
    ("Teyit",     "Sonucu kapanışta doğrular; kazandığını da kaybettiğini de yazar."),
    ("Pusula",    "Bu siteyi işletir: denetim, gündem, teklif, üretim, tıklanma."),
    ("Asistan",   "Sorulara sitenin kendi metninden cevap verir; bilmediğinde uydurmaz."),
]
ILKELER = [
    ("Kanıtsız terfi yok", "Bir hat, otuz sonuçlanmış karar biriktirmeden sahaya çıkmaz."),
    ("Hatasını saklayamayan sistem", "Kaybeden sonuç da deftere yazılır; karne seçme yapmaz."),
    ("İtiraz hakkı", "Mühendis hakem olarak itiraz edebilir; şiir sayıya çevrilir."),
    ("Mezarlık", "Çalışmayan fikirler silinmez, mezarlığa kaldırılır; geri dönmek için yeni kanıt gerekir."),
]


def _e(x):
    return html.escape(x or "", quote=True)


def _slug(t):
    t = unicodedata.normalize("NFKD", t.replace("ı", "i").replace("İ", "i").replace("ğ", "g").replace("Ğ", "g")
                              .replace("ş", "s").replace("Ş", "s").replace("ç", "c").replace("Ç", "c")
                              .replace("ö", "o").replace("Ö", "o").replace("ü", "u").replace("Ü", "u"))
    t = "".join(c for c in t if not unicodedata.combining(c)).lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t[:70].rstrip("-")


def _tr_tarih(iso):
    y, a, g = iso.split("-")
    return "%d %s %s" % (int(g), AY[int(a) - 1], y)


def _okuma_sure(metin):
    k = len(re.findall(r"\w+", metin or ""))
    return max(1, round(k / 180))


def _gorsel(ad, alt, boy="k", on="../"):
    if ad.startswith("../video/"):
        return '<img src="%sassets/video/%s.jpg" alt="%s" loading="lazy" width="1280" height="720">' % (on, ad[9:], _e(alt))
    return '<img src="%sassets/studyo/%s%s.jpg" alt="%s" loading="lazy" width="800" height="447">' % (on, ad, "-k" if boy == "k" else "", _e(alt))


# ---------------------------------------------------------------- kabuk (kendi tasarımı)
def _bas(baslik, aciklama, url, gorsel=None, sema=None, tur="website", on="../", tr=""):
    og = ("https://lunayapim.com/assets/studyo/%s.jpg" % gorsel) if gorsel and not gorsel.startswith("../video/") else \
         ("https://lunayapim.com/assets/video/%s.jpg" % gorsel[9:]) if gorsel else "https://lunayapim.com/assets/og-image.png"
    return """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-18288531900"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'AW-18288531900');
</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=%s" crossorigin="anonymous"></script>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%s</title>
<meta name="description" content="%s">
<meta name="keywords" content="trendsaphiens, günün haberleri, sektör analizi, piyasa raporu, bursa, yapay zekâ, inşaat, emlak">
<link rel="canonical" href="%s">
<meta property="og:site_name" content="LunaTrendSaphiens">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:type" content="%s">
<meta property="og:url" content="%s">
<meta property="og:image" content="%s">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="%s">
<link rel="icon" type="image/x-icon" href="{on}assets/favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="{on}assets/favicon-32.png">
<link rel="apple-touch-icon" sizes="180x180" href="{on}assets/favicon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,800&family=Manrope:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{on}assets/luna.css">
%s
</head>
<body class="ts-tema">
<header class="ts-ust">
  <div class="wrap ts-ust-ic">
    <a class="ts-marka" href="{trk}">Luna<b>Trend</b>Saphiens</a>
    <nav class="ts-nav">%s</nav>
    <div class="ts-ust-sag"><a href="{on}" class="ts-ana">Luna Yapım</a><a href="#abone" class="ts-abone-dug">Abone ol</a></div>
  </div>
</header>
""".replace("{on}", on).replace("{trk}", tr or "./").replace("{tr}", tr) % (ADSENSE, _e(baslik), _e(aciklama), url, _e(baslik), _e(aciklama), tur, url, og, og, sema or "",
       "".join('<a href="%s%s/">%s</a>' % (tr, k, v[0]) for k, v in KATEGORI.items()))


def _alt(on="../", tr=""):
    return ("""
<footer class="ts-alt">
  <div class="wrap">
    <div class="ts-alt-izgara">
      <div><a class="ts-marka" href="{trk}">Luna<b>Trend</b>Saphiens</a>
        <p>Günün haberleri, analizler ve raporlar. Her madde kaynaklı; rakam yalnızca kaynakta varsa yazılır. Piyasa tarafı yatırım tavsiyesi değildir.</p></div>
      <div><h4>Bölümler</h4>%s</div>
      <div><h4>Luna Yapım</h4><a href="{on}">Ana site</a><a href="{on}yazilim">Yazılım</a><a href="{on}hizmetler/">Prodüksiyon</a><a href="{on}studyo">Stüdyo</a><a href="{on}matrix">KDA Matrix</a></div>
      <div><h4>Kurumsal</h4><a href="{on}iletisim">İletişim</a><a href="{on}gizlilik">Gizlilik ve çerezler</a><a href="{on}kosullar">Koşullar</a><a href="{on}seffaflik">Şeffaflık</a></div>
    </div>
    <div class="ts-alt-satir"><span>© <span id="yil"></span> Luna Yapım · Bursa</span><span>LunaTrendSaphiens bir Luna Yapım yayınıdır</span></div>
  </div>
</footer>
<script>document.getElementById("yil").textContent=new Date().getFullYear();</script>
<script src="{on}assets/olcum.js"></script>
<script src="{on}assets/okuma.js" defer></script>
<script src="{on}assets/sahne.js?v=1" defer></script>
</body>
</html>""".replace("{on}", on).replace("{trk}", tr or "./").replace("{tr}", tr)) % "".join('<a href="%s%s/">%s</a>' % (tr, k, v[0]) for k, v in KATEGORI.items())


def _paylas(url, baslik):
    u = html.escape(url, quote=True); b = html.escape(baslik, quote=True)
    return ('<div class="ts-paylas"><span class="etk">Paylaş</span>'
            '<a href="https://twitter.com/intent/tweet?text=%s&url=%s" target="_blank" rel="noopener">X</a>'
            '<a href="https://wa.me/?text=%s%%20%s" target="_blank" rel="noopener">WhatsApp</a>'
            '<button type="button" data-kopyala="%s">Bağlantı</button></div>'
            % (b.replace(" ", "%20"), u, b.replace(" ", "%20"), u, u))


def _abone(on="../"):
    return """<div class="ts-abone" id="abone">
  <span class="etk">Ücretsiz bülten</span>
  <h3>Günün özeti ve haftalık karne, e-postana.</h3>
  <form id="bl-form" autocomplete="off">
    <div class="bl-satir"><input type="email" id="bl-eposta" placeholder="e-posta adresin" required maxlength="120"><button type="submit">Abone ol</button></div>
    <label class="bl-onay"><input type="checkbox" id="bl-onay" required> Piyasa içeriğinin yatırım tavsiyesi olmadığını anladım; 18 yaşından büyüğüm; e-postam yalnızca bu bülten için saklansın. <a href="%skosullar">Koşullar</a></label>
    <p id="bl-sonuc" class="bl-sonuc" aria-live="polite"></p>
  </form>
</div>
<script>
(function(){var f=document.getElementById("bl-form");if(!f)return;f.addEventListener("submit",async function(ev){ev.preventDefault();var e=document.getElementById("bl-eposta").value.trim(),s=document.getElementById("bl-sonuc");if(!document.getElementById("bl-onay").checked){s.textContent="Onay kutusunu işaretle.";return}s.textContent="Kaydediliyor…";try{var r=await fetch("/api/abone",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({eposta:e,onay:true,kaynak:"trend"})});s.textContent=r.ok?"Tamam — ilk sayı Pazartesi.":"Olmadı; daha sonra tekrar dene."}catch(x){s.textContent="Bağlantı yok; daha sonra tekrar dene."}});})();
</script>""" % on

RISK = """<div class="bl-risk"><span class="etk">Risk bildirimi</span>
  <p>Piyasa içeriği bir <strong>bilgi ürünüdür</strong>; yatırım danışmanlığı, tavsiyesi ya da alım-satım önerisi değildir. Kripto varlık ve hisse piyasaları yüksek risk taşır; geçmiş performans gelecek için gösterge değildir, hiçbir kazanç vaat edilmez.</p></div>"""

# AdSense birimleri (hesap: ca-pub-3059196718190568). Onay gelene kadar boş kalır; onaydan sonra kendiliğinden dolar.
REKLAM_YAZI_ICI = "1717189115"   # "TrendSaphiens yazı içi" — in-article, fluid
REKLAM_AKIS = "1154811288"       # "TrendSaphiens akış" — display, responsive
REKLAM = ('<div class="ts-reklam"><ins class="adsbygoogle" style="display:block;text-align:center" data-ad-layout="in-article" data-ad-format="fluid" '
          'data-ad-client="ca-pub-%s" data-ad-slot="%s"></ins><script>(adsbygoogle=window.adsbygoogle||[]).push({});</script></div>' % (ADSENSE.replace("ca-pub-", ""), REKLAM_YAZI_ICI))
REKLAM_YAN = ('<div class="ts-reklam"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-%s" data-ad-slot="%s" data-ad-format="auto" '
              'data-full-width-responsive="true"></ins><script>(adsbygoogle=window.adsbygoogle||[]).push({});</script></div>' % (ADSENSE.replace("ca-pub-", ""), REKLAM_AKIS))


# ---------------------------------------------------------------- kaynaklar
def _gundem_maddeleri():
    d = os.path.join(KOK_DIZIN, "veri", "gundem")
    ci = []
    if not os.path.isdir(d):
        return ci
    for f in sorted(os.listdir(d), reverse=True):
        if not re.match(r"\d{4}-\d{2}-\d{2}\.json$", f):
            continue
        tarih = f[:-5]
        try:
            ham = json.load(open(os.path.join(d, f), encoding="utf-8"))
        except Exception:
            continue
        for i, m in enumerate(ham, 1):
            # İNCE SAYFA KAPISI: kaynaklı gerçek bir olgu paragrafı yoksa ayrı haber sayfası açılmaz;
            # madde gündem sayısında kaynağa bağlantı olarak kalır.
            try:
                from .kaynak_ozet import yeterli
                if not yeterli(m):
                    continue
            except Exception:
                pass
            kat, gor, sek = HIZMET_KAT.get(m.get("hizmet", ""), ("gundem", "set-isik", "Sektör"))
            ci.append({"tur": "haber", "tarih": tarih, "sira": i, "baslik": m["baslik"], "olgu": m.get("olgu", ""),
                       "ek": m.get("ek", ""), "aci_soru": m.get("aci_soru", ""), "hizmet_soz": m.get("hizmet_soz", ""), "yazi": m.get("yazi") if isinstance(m.get("yazi"), dict) and not m["yazi"].get("hata") else None,
                       "aci": m.get("aci", ""), "kaynak_ad": m.get("kaynak_ad", ""), "kaynak_url": m.get("kaynak_url", ""),
                       "kaynak_tarih": m.get("kaynak_tarih", ""), "hizmet": m.get("hizmet", ""),
                       "kat": kat, "gorsel": gor, "sektor": sek,
                       "slug": _slug(m["baslik"]) or ("haber-%s-%d" % (tarih, i)),
                       "gundem_url": "../gundem/%s#m%d" % (tarih, i)})
    return ci


def _blog_yazilari(kok):
    y = os.path.join(kok, "blog", "index.html")
    ci = []
    if not os.path.exists(y):
        return ci
    s = open(y, encoding="utf-8").read()
    for m in re.finditer(r'<a class="urun" href="([^"]+)"[^>]*>.*?<span class="rom">([^<]*)</span>\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>', s, re.S):
        href, tarih, bas, oz = m.groups()
        bas = re.sub(r"<[^>]+>", "", bas); oz = re.sub(r"<[^>]+>", "", oz)
        kat = "teknoloji" if re.search(r"yapay zek|arama", bas, re.I) else "analiz"
        gor = "render-istasyonu" if "3d" in bas.lower() else "drone-safak" if "drone" in bas.lower() or "emlak" in bas.lower() else "set-isik"
        ci.append({"tur": "blog", "tarih": tarih.strip() if re.match(r"\d{4}-\d{2}-\d{2}", tarih.strip()) else "2026-08-31",
                   "baslik": html.unescape(bas.strip()), "olgu": html.unescape(oz.strip()), "kat": kat, "gorsel": gor,
                   "url": "../blog/%s" % href, "slug": None})
    return ci


def _bulten_sayilari(kok):
    d = os.path.join(kok, "bulten")
    ci = [{"tur": "rapor", "tarih": "2026-09-02", "baslik": "Matrix Bülteni Sayı 00: piyasayı okuyan sistem nasıl çalışıyor",
           "olgu": "Hatlar, kuluçka, otuz karar kuralı ve haftalık karne — sistemin kendi diliyle.", "kat": "rapor",
           "gorsel": "../video/karga-k5", "url": "../bulten/00-sistem", "slug": None}]
    vd = os.path.join(KOK_DIZIN, "veri", "bulten")
    if os.path.isdir(vd):
        for f in sorted(os.listdir(vd), reverse=True):
            if f.endswith(".json"):
                h = f[:-5]
                ci.insert(0, {"tur": "rapor", "tarih": datetime.date.today().isoformat(), "baslik": "Haftanın karnesi · Sayı %s" % h,
                              "olgu": "Sınavı geçen ve elenen hatlar, sistemin baktığı yerler. Ölçüm, yorum değil.", "kat": "rapor",
                              "gorsel": "../video/karga-k3", "url": "../bulten/%s" % h, "slug": None})
    return ci


# ---------------------------------------------------------------- kartlar
def _kart(m, buyuk=False, on="../", tr=""):
    kat_ad = KATEGORI.get(m["kat"], ("Gündem",))[0]
    if m["tur"] in ("haber", "rehber"):
        url = tr + m["slug"]
    elif m["tur"] == "sayfa":
        url = tr + m["url"]
    else:
        url = on + m["url"][3:]   # "../blog/x" → kök önekiyle
    sure = _okuma_sure((m.get("olgu") or "") + (m.get("aci") or ""))
    return """<a class="ts-kart%s gor" href="%s">
      <div class="ts-kart-gorsel">%s<span class="ts-chip">%s</span></div>
      <div class="ts-kart-metin">
        <span class="ts-meta">%s · %d dk</span>
        <h3>%s</h3>
        <p>%s</p>
      </div>
    </a>""" % (" ts-kart-buyuk" if buyuk else "", _e(url), _gorsel(m["gorsel"], m["baslik"], "b" if buyuk else "k", on),
               _e(kat_ad), _e(_tr_tarih(m["tarih"])), sure, _e(m["baslik"]), _e((m.get("olgu") or "")[:220].rsplit(" ", 1)[0] + ("…" if len(m.get("olgu") or "") > 220 else "")))


def _gunluk_sayfalar():
    """trend_izle ve piyasa_gunluk verisinden akışa girecek günlük sayfalar."""
    ci = []
    try:
        from . import trend_izle as TI, piyasa_gunluk as PG
    except Exception:
        return ci
    for v in TI.hepsi():
        t = v.get("tarih"); ar = v.get("aranan") or []
        if ar:
            ilk = ", ".join(a["baslik"] for a in ar[:5])
            ci.append({"tur": "sayfa", "tarih": t, "kat": "aranan", "gorsel": BOLUM_GORSEL["aranan"],
                       "baslik": "Türkiye bugün ne aradı? %s" % _tr_tarih(t),
                       "olgu": "Günün en çok aranan %d başlığı: %s… Her biri Google'ın bağladığı haberle." % (len(ar), ilk),
                       "url": "aranan/%s" % t})
        for b, liste in (v.get("bolumler") or {}).items():
            kat = BOLUM_KAT.get(b)
            if not kat or not liste:
                continue
            ad = KATEGORI[kat][0]
            ci.append({"tur": "sayfa", "tarih": t, "kat": kat, "gorsel": BOLUM_GORSEL.get(kat, "set-isik"),
                       "baslik": "%s · %s: %s" % (ad, _tr_tarih(t), liste[0]["baslik"][:70]),
                       "olgu": " · ".join(x["baslik"][:60] for x in liste[1:4]) or liste[0].get("ozet", ""),
                       "url": "%s/%s" % (kat, t)})
    for v in PG.hepsi():
        t = v.get("tarih"); k = (v.get("tcmb") or {}).get("kurlar", {})
        usd = _tl(k.get("USD", {}).get("satis", "")); eur = _tl(k.get("EUR", {}).get("satis", ""))
        ga = ((v.get("altin") or {}).get("gram-altin") or {}).get("satis", "")
        ozet = "TCMB satış: dolar %s, euro %s%s. Kaynaklı, yatırım tavsiyesi değildir." % (usd or "—", eur or "—", (", gram altın %s" % ga) if ga else "")
        ci.append({"tur": "sayfa", "tarih": t, "kat": "piyasa", "gorsel": BOLUM_GORSEL["piyasa"],
                   "baslik": "Dolar, euro ve altın bugün · %s" % _tr_tarih(t), "olgu": ozet, "url": "piyasa/%s" % t})
    return ci


def _rehberler():
    try:
        from . import trend_rehber as TRH
    except Exception:
        return []
    out = []
    for r in TRH.hepsi():
        out.append({"tur": "rehber", "tarih": r["tarih"], "sira": 0, "kat": r["kat"], "gorsel": r["gorsel"], "baslik": r["baslik"],
                    "olgu": r["ozet"], "slug": r["slug"], "rehber": r})
    return out


def _diskteki_gun_sayfalari(kok, mevcut):
    """Diskte duran ama veri listesinden dusmus gun sayfalarini da akisa kat.

    Neden: bir gunun bolum verisi sonraki kosuda bosalirsa (kaynak o gun o bolumu
    vermezse) sayfa diskte kalir ama hicbir yerden baglanmaz — yetim sayfa olur
    (14.09.2026: 7 sayfa). Sayfa zaten sitemap'te; basligi kendi <title>'indan
    okunur. Etkisiz tekrarlanabilir.
    """
    import glob as _g
    ek = []
    var = set(m.get("url") for m in mevcut)
    for kat in list(KATEGORI.keys()) + ["aranan", "piyasa"]:
        d = os.path.join(kok, "trend", kat)
        if not os.path.isdir(d):
            continue
        for yol in sorted(_g.glob(os.path.join(d, "20??-??-??.html"))):
            t = os.path.basename(yol)[:-5]
            url = "%s/%s" % (kat, t)
            if url in var:
                continue
            try:
                ham = open(yol, encoding="utf-8").read(6000)
            except Exception:
                continue
            m = re.search(r"<title>(.*?)</title>", ham, re.S)
            baslik = re.sub(r"\s+", " ", m.group(1)).split("|")[0].strip() if m else url
            m2 = re.search(r'name="description" content="([^"]*)"', ham)
            ozet = (m2.group(1) if m2 else "").strip()
            ek.append({"tur": "sayfa", "tarih": t, "kat": kat if kat in KATEGORI else "piyasa",
                       "gorsel": BOLUM_GORSEL.get(kat, "set-isik"), "baslik": baslik,
                       "olgu": ozet or "Bu gunun basliklari, kaynagiyla.", "url": url})
    return ek


def _hepsi(kok):
    h = _gundem_maddeleri() + _blog_yazilari(kok) + _bulten_sayilari(kok) + _gunluk_sayfalar() + _rehberler()
    try:
        h += _diskteki_gun_sayfalari(kok, h)
    except Exception as ex:
        print("diskteki gun sayfalari:", ex)
    h.sort(key=lambda x: (x["tarih"], -x.get("sira", 0)), reverse=True)
    return h


# ---------------------------------------------------------------- sayfalar
def _tl(x, hane=2):
    """TCMB'nin '48.2943' biçimini Türkçe '48,29'a çevirir; zaten Türkçe biçimdeyse ('6.880,35') dokunmaz."""
    x = (x or "").strip()
    if re.match(r"^\d+\.\d+$", x):
        try:
            return ("{:,.%df}" % hane).format(float(x)).replace(",", "X").replace(".", ",").replace("X", ".")
        except ValueError:
            return x
    return x


def _takvim_kutu(on="../", tr=""):
    """Bugün / bu hafta çok aranacaklar — takvim.py'den; sabit kayıtlar kaynaklı."""
    try:
        from . import takvim as TK
    except Exception:
        return ""
    bugun = datetime.date.today()
    satir = []
    for g, liste in TK.hafta(bugun, 7):
        if g == bugun:
            secim = liste[:4]
        else:
            secim = [k for k in liste if k.get("kural") not in ("hergun", "isgunu")][:2]
        for k in secim:
            etiket = "Bugün" if g == bugun else TK.GUN[g.weekday()]
            satir.append('<li><span class="ts-tk-gun">%s%s</span><b>%s</b><small>%s</small></li>' % (
                _e(etiket), (" · " + _e(k["saat"])) if k["saat"] else "", _e(k["ad"]), _e(k["sorgu"])))
    if not satir:
        return ""
    return '<div class="ts-kutu ts-takvim"><h2 class="etk">Takvim · bu hafta aranacaklar</h2><ul>%s</ul><p class="ts-not">Her iş günü 15:30 TCMB kurları, her sabah altın fiyatı; tarihi belli konular ilgili sayfada kaynağıyla yenilenir.</p></div>' % "".join(satir[:9])


def _rehber_kutu(tr=""):
    """Kalici rehberler: her akis sayfasindan baglanir (yoksa 9 rehber yetim kalirdi)."""
    try:
        from . import trend_rehber as TR
        rl = TR.hepsi()
    except Exception:
        return ""
    if not rl:
        return ""
    sat = "".join('<li><a href="%s%s">%s</a></li>' % (tr, _e(r["slug"]), _e(r["baslik"])) for r in rl[:9])
    return ('<div class="ts-kutu ts-rehber"><h2 class="etk">Kalici rehberler</h2><ul class="ts-rehber-liste">%s</ul>'
            '<p class="ts-not">Gunu gecmeyen sorular: nereye bakilir, nasil okunur.</p></div>') % sat


def _rakam_kutu(on="../", tr=""):
    """Günün rakamı: TCMB satış + gram altın — yalnız veri varsa, kaynak adıyla."""
    try:
        from . import piyasa_gunluk as PG
        v = PG.son()
    except Exception:
        v = None
    if not v:
        return ""
    k = (v.get("tcmb") or {}).get("kurlar", {}); al = v.get("altin") or {}
    hucre = []
    for kod, ad in (("USD", "Dolar"), ("EUR", "Euro"), ("GBP", "Sterlin")):
        x = k.get(kod, {}).get("satis")
        if x:
            hucre.append('<div><span>%s</span><b>%s</b><i>TL · TCMB satış</i></div>' % (ad, _e(_tl(x))))
    if al.get("gram-altin", {}).get("satis"):
        hucre.append('<div><span>Gram altın</span><b>%s</b><i>TL · truncgil</i></div>' % _e(al["gram-altin"]["satis"]))
    if not hucre:
        return ""
    return ('<div class="ts-kutu ts-rakam"><h2 class="etk">Günün rakamı · %s</h2><div class="ts-rakam-izgara">%s</div>'
            '<a class="ts-daha" href="%spiyasa/%s">Tam tablo ve kaynak →</a><p class="ts-not">Yatırım tavsiyesi değildir.</p></div>') % (
            _e(_tr_tarih(v["tarih"])), "".join(hucre), tr, _e(v["tarih"]))


def akis_html(kok, kat=None):
    hepsi = _hepsi(kok)
    if kat:
        hepsi = [m for m in hepsi if m["kat"] == kat]
    on, tr = ("../../", "../") if kat else ("../", "")
    ad, alt_baslik = KATEGORI.get(kat, ("Akış", "Günün haberleri, analizler, raporlar"))
    baslik = ("%s — %s | TrendSaphiens" % (ad, KAT_KISA.get(kat, alt_baslik))) if kat else "LunaTrendSaphiens — günün haberleri, analizler, raporlar"
    if len(baslik) > 68:
        baslik = "%s | LunaTrendSaphiens" % ad
    aciklama = (alt_baslik + ". Her madde kaynaklı ve tarihli; rakam yalnızca kaynakta varsa yazılır. Luna Yapım'ın günlük yayını: haber, analiz, rapor.")[:158]
    url = KOK_URL + ((kat + "/") if kat else "")
    sema = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "CollectionPage", "name": baslik, "url": url,
            "description": aciklama, "isPartOf": {"@type": "WebSite", "name": "LunaTrendSaphiens", "url": KOK_URL},
            "publisher": {"@type": "Organization", "name": "Luna Yapım", "url": "https://lunayapim.com/"}}, ensure_ascii=False) + "</script>"
    man = hepsi[0] if hepsi else None
    kartlar = "".join(_kart(m, False, on, tr) for m in hepsi[1:13])
    def _u(m):
        return tr + m["slug"] if m["tur"] in ("haber", "rehber") else (tr + m["url"] if m["tur"] == "sayfa" else on + m["url"][3:])
    trend = "".join('<li><a href="%s"><span>%02d</span>%s</a></li>' % (_e(_u(m)), i, _e(m["baslik"])) for i, m in enumerate(hepsi[:6], 1))
    govde = """
<section class="ts-manset">
  <div class="wrap">
    <div class="ts-mast"><h1>%s</h1><p>%s</p></div>
    %s
  </div>
</section>
<section class="ts-govde">
  <div class="wrap ts-izgara">
    <div class="ts-akis">
      <div class="ts-bas"><h2 class="etk">%s</h2><span class="ts-sayi">%d yazı</span></div>
      <div class="ts-kartlar">%s</div>
      %s
      <div class="ts-giris"><h2>Bu bölüm nasıl çalışır</h2><p>%s</p></div>
      %s
    </div>
    <aside class="ts-yan">
      <div class="ts-kutu"><h2 class="etk">Trend</h2><ol class="ts-trend">%s</ol></div>
      %s
      %s
      %s
      %s
      <div class="ts-kutu ts-sistem"><span class="etk">Sistem</span><h3>Sonuç veren organlarımız</h3><p>Gözcü, Aday, Rejim, Beyin, İcra, Bekçi… Bu yayını ve piyasa defterini işleten organlar.</p><a class="btn btn-cizgi" href="%ssistem/">Tanış →</a></div>
      %s
    </aside>
  </div>
</section>
""" % (_e(ad if kat else "Bugün ne oldu, ne anlama geliyor?"), _e(alt_baslik if kat else "Sektör haberleri, analizler ve piyasayı okuyan sistemin raporları — kaynaklı, kısa, günlük."),
       (_kart(man, True, on, tr) if man else ""), _e("Akış" if not kat else ad), len(hepsi), kartlar, REKLAM_YAN,
       _e(KAT_GIRIS.get(kat) or KAT_GIRIS_EK.get(kat) or (KAT_GIRIS["gundem"] + " " + KAT_GIRIS["rapor"])),
       ('<div class="ts-giris"><h2>%s</h2><p>%s</p><p class="ts-baglar">%s</p></div>' % (_e(KAT_IZLEME[kat][0]), _e(KAT_IZLEME[kat][1]),
        " · ".join('<a href="%s%s">%s</a>' % (on, h[3:], _e(t)) for h, t in KAT_IZLEME[kat][2])) +
        '<div class="ts-giris"><h2>Neden bir yapım şirketi yayın tutuyor</h2><p>Çünkü işimiz sektörün nabzına bağlı. Konut satışı düştüğünde satış ofisinin görsele ihtiyacı artıyor; kira talebi yükseldiğinde ilan videosu fark yaratıyor; reklamda yapay zekâ etiketi zorunlu olunca gerçek çekimin değeri değişiyor. Bunları izlemeyen bir yapım şirketi müşterisine yalnızca kamera satar; biz neyin neden işe yaradığını da anlatmak istiyoruz. LunaTrendSaphiens bu yüzden var: her sabah günün haberleri seçilir, haftada bir piyasa defterinin karnesi çıkar, öne çıkan konu blogda derinleşir. Bütün yayını iki kişilik bir stüdyonun kendi yazdığı sistem işletir; sayfaların SEO kapısından geçtiğini de o denetler. Okuduğunuz bir maddeyle ilgili işiniz varsa altındaki hizmet bağlantısından o sayfaya geçebilir ya da bize yazabilirsiniz.</p></div>') if kat in KAT_IZLEME else "",
       trend, _rakam_kutu(on, tr), _takvim_kutu(on, tr), _abone(on), _rehber_kutu(tr), tr, REKLAM_YAN)
    ek = ""
    if kat in KAT_DUZEN:
        ek += '      <div class="ts-giris"><h2>%s</h2><p>%s</p></div>\n' % (_e(KAT_DUZEN[kat][0]), _e(KAT_DUZEN[kat][1]))
    if kat in KAT_SSS:
        ek += '      <div class="ts-giris ts-sss"><h2>Sık sorulanlar</h2>%s</div>\n' % "".join("<h3>%s</h3><p>%s</p>" % (_e(q), _e(a)) for q, a in KAT_SSS[kat])
        sema += '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in KAT_SSS[kat]]}, ensure_ascii=False) + "</script>"
    # Kart izgarasina sigmayan maddeler: tarihli tam liste. Kartlar yalniz 12 madde
    # gosterdigi icin eski gun sayfalari hicbir yerden baglanmiyordu (yetim sayfa).
    kalan = hepsi[13:]
    if kalan:
        sat = []
        for m in kalan:
            sat.append('<li><a href="%s">%s</a><time datetime="%s">%s</time></li>'
                       % (_e(_u(m)), _e(m["baslik"]), _e(m["tarih"][:10]), _e(_tr_tarih(m["tarih"][:10]))))
        ek += ('      <div class="ts-giris ts-tumu"><h2>Bu bölümün tüm arşivi</h2>'
               '<p>Kartlara sigmayan %d madde, yeniden eskiye.</p><ul class="ts-tumu-liste">%s</ul></div>\n'
               % (len(kalan), "".join(sat)))
    if ek:
        govde = govde.replace('    </div>\n    <aside class="ts-yan">', ek + '    </div>\n    <aside class="ts-yan">', 1)
    return _bas(baslik, aciklama, url, man["gorsel"] if man else None, sema, "website", on, tr) + govde + _alt(on, tr)


def _makale_govde(m, yz, hizmet_ad):
    """Yazı (yazar.py) varsa tam makale; yoksa kaynak alıntısı + bizim okumamız."""
    kt = _e(m.get("kaynak_tarih") or _tr_tarih(m["tarih"]))
    if yz:
        h = ['<p class="ts-giris">%s</p>' % _e(yz.get("giris", ""))]
        for b in yz.get("bolumler", []):
            h.append("<h2>%s</h2>" % _e(b.get("h2", "")))
            h += ["<p>%s</p>" % _e(p) for p in b.get("paragraflar", []) if p]
        a = yz.get("alinti") or {}
        if a.get("metin"):
            h.append('<blockquote class="ts-olgu"><p>“%s”</p><cite>— <a href="%s" rel="nofollow noopener" target="_blank">%s</a>, %s</cite></blockquote>'
                     % (_e(a["metin"].strip("“”\"")), _e(m["kaynak_url"]), _e(a.get("kaynak") or m["kaynak_ad"]), kt))
        if yz.get("ne_yapmali"):
            h.append('<div class="ts-analiz"><h2 class="etk">Ne yapmalı</h2><ol>%s</ol><a href="%s">%s →</a></div>'
                     % ("".join("<li>%s</li>" % _e(x) for x in yz["ne_yapmali"]), _e(hizmet_ad[1]), _e(hizmet_ad[0])))
        if yz.get("sss"):
            h.append('<section class="ts-sss"><h2>Sık sorulan sorular</h2>%s</section>'
                     % "".join("<h3>%s</h3><p>%s</p>" % (_e(q.get("soru", "")), _e(q.get("cevap", ""))) for q in yz["sss"]))
        h.append('<p class="ts-not">Kaynak: <a href="%s" rel="nofollow noopener" target="_blank">%s</a>, %s. Yazı bu kaynağın olgularından Luna Yapım tarafından yazılmıştır; intihal denetimi: kaynakla örtüşme %%%.1f.</p>'
                 % (_e(m["kaynak_url"]), _e(m["kaynak_ad"]), kt, 100 * float((yz.get("intihal") or {}).get("kapsama", 0))))
        return "\n      ".join(h)
    return ("""<h2 class="etk">Kaynak ne diyor</h2>
      <blockquote class="ts-olgu"><p>%s</p>%s<cite>— <a href="%s" rel="nofollow noopener" target="_blank">%s</a>, %s</cite></blockquote>
      <div class="ts-analiz"><h2 class="etk">Bizim okumamız</h2>%s<p>%s</p>%s<a href="%s">%s →</a></div>"""
      % (_e(m["olgu"]), ("<p>%s</p>" % _e(m["ek"])) if m.get("ek") else "", _e(m["kaynak_url"]), _e(m["kaynak_ad"]), kt,
         ("<h3>%s</h3>" % _e(m["aci_soru"])) if m.get("aci_soru") else "", _e(m["aci"]),
         ("<p class=\"ts-hizmet-soz\">Bizim tarafımız: %s.</p>" % _e(m["hizmet_soz"].rstrip("."))) if m.get("hizmet_soz") and m["hizmet_soz"].strip() not in m["aci"] else "",
         _e(hizmet_ad[1]), _e(hizmet_ad[0])))


def haber_html(m, komsular):
    yz = m.get("yazi") if isinstance(m.get("yazi"), dict) else None
    baslik = (yz or {}).get("baslik") or m["baslik"]
    kisa = baslik if len(baslik) <= 52 else baslik[:52].rsplit(" ", 1)[0].rstrip(",;:—-") + "…"
    url = KOK_URL + m["slug"]
    kat_ad = KATEGORI[m["kat"]][0]
    aciklama = ((yz or {}).get("meta") or m.get("olgu") or "").strip()
    if len(aciklama) < 110:   # SEO kapısı: description ≥110; olgu kısa kalınca kaynak ve bölüm bağlamı eklenir
        ek = " Kaynak: %s. %s bölümü, LunaTrendSaphiens — Luna Yapım'ın üretim tarafından okuması ve bağlam." % (m.get("kaynak_ad") or "haber", kat_ad)
        if aciklama and aciklama[-1] not in ".!?…": aciklama += "."
        aciklama = (aciklama + ek).strip()
        if len(aciklama) < 110: aciklama = baslik + ". " + aciklama
    aciklama = aciklama[:158]
    if len(aciklama) == 158: aciklama = aciklama.rsplit(" ", 1)[0].rstrip(",;:—-") + "…"
    sema = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "NewsArticle", "headline": baslik, "description": aciklama, "url": url, "datePublished": m["tarih"], "dateModified": m["tarih"],
         "inLanguage": "tr", "articleSection": kat_ad,
         "image": "https://lunayapim.com/assets/studyo/%s.jpg" % m["gorsel"] if not m["gorsel"].startswith("../video/") else "https://lunayapim.com/assets/video/%s.jpg" % m["gorsel"][9:],
         "author": {"@type": "Organization", "name": "Luna Yapım", "url": "https://lunayapim.com/"},
         "publisher": {"@type": "Organization", "name": "LunaTrendSaphiens", "url": KOK_URL, "logo": {"@type": "ImageObject", "url": "https://lunayapim.com/assets/luna-logo.png"}},
         "citation": [{"@type": "CreativeWork", "name": m["kaynak_ad"], "url": m["kaynak_url"]}] if m.get("kaynak_url") else []},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "LunaTrendSaphiens", "item": KOK_URL},
            {"@type": "ListItem", "position": 2, "name": kat_ad, "item": KOK_URL + m["kat"] + "/"},
            {"@type": "ListItem", "position": 3, "name": baslik, "item": url}]}] + ([
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q.get("soru", ""), "acceptedAnswer": {"@type": "Answer", "text": q.get("cevap", "")}}
                                          for q in yz.get("sss", []) if q.get("soru")]}] if yz and yz.get("sss") else [])}, ensure_ascii=False) + "</script>"
    hizmet_ad = {"hizmetler/insaat-3d-modelleme.html": ("İnşaat 3D modelleme", "../hizmetler/insaat-3d-modelleme"),
                 "hizmetler/emlak-kurumsal.html": ("Emlak videosu", "../hizmetler/emlak-kurumsal"),
                 "hizmetler/urun-animasyon.html": ("Ürün animasyonu", "../hizmetler/urun-animasyon"),
                 "hizmetler/drone-fpv.html": ("Drone çekimi", "../hizmetler/drone-fpv"),
                 "hizmetler/isletme-tanitim.html": ("İşletme tanıtımı", "../hizmetler/isletme-tanitim"),
                 "hizmetler/klip-cekimi.html": ("Klip çekimi", "../hizmetler/klip-cekimi"),
                 "sehir/bursa.html": ("Bursa", "../sehir/bursa")}.get(m.get("hizmet", ""), ("Hizmetlerimiz", "../hizmetler/"))
    sure = _okuma_sure(m.get("olgu", "") + m.get("ek", "") + m.get("aci", ""))
    komsu_kart = "".join(_kart(k, False, "../", "") for k in komsular[:3])
    govde = """
<article class="ts-yazi">
  <div class="wrap ts-yazi-izgara">
    <div class="ts-yazi-ana">
      <div class="crumbs"><a href="./">LunaTrendSaphiens</a> · <a href="%s/">%s</a> · %s</div>
      <span class="ts-chip">%s</span>
      <h1>%s</h1>
      <p class="ts-yazi-meta">%s · %d dk okuma · Kaynak: <a href="%s" rel="nofollow noopener" target="_blank">%s</a>%s</p>
      <div class="ts-yazi-gorsel">%s</div>
      %s
      %s
      %s
      <footer class="ts-baglam">
        <p><strong>Olgu ve okuma ayrı.</strong> Alıntı kaynağın sözü; rakam yalnızca kaynakta geçiyorsa yazılır. "Bizim okumamız" bu gelişmenin tanıtım, görsel ve yatırım kararına etkisi üzerine yorumumuzdur. Kaynak: %s, %s. Bölüm: %s. Bu madde <a href="%s">Gündem</a> sayısından.</p>
      </footer>
    </div>
    <aside class="ts-yan">
      %s
      <nav class="ts-kutu" aria-label="Devamı"><h2 class="etk">Devamı</h2><div class="ts-kartlar ts-kartlar-dar">%s</div></nav>
    </aside>
  </div>
</article>
""" % (m["kat"], _e(kat_ad), _e(_tr_tarih(m["tarih"])), _e(m["sektor"]), _e(baslik), _e(_tr_tarih(m["tarih"])), sure,
       _e(m["kaynak_url"]), _e(m["kaynak_ad"]), (" · " + _e(m["kaynak_tarih"])) if m.get("kaynak_tarih") else "",
       _gorsel(m["gorsel"], baslik, "b"), _paylas(url, baslik),
       _makale_govde(m, yz, hizmet_ad),
       REKLAM, _e(m["kaynak_ad"]), _e(m.get("kaynak_tarih") or _tr_tarih(m["tarih"])), _e(kat_ad),
       _e(m["gundem_url"]), _abone("../"), komsu_kart)
    return _bas(kisa + " | TrendSaphiens", aciklama, url, m["gorsel"], sema, "article") + govde + _alt("../", "")


def rehber_html(m, komsular):
    r = m["rehber"]; baslik = r["baslik"]; url = KOK_URL + r["slug"]; kat_ad = KATEGORI[r["kat"]][0]
    kisa = baslik if len(baslik) <= 52 else baslik[:52].rsplit(" ", 1)[0].rstrip(",;:—-") + "…"
    aciklama = r["ozet"][:158]
    govde_metin = " ".join(p for _, p in r["bolumler"])
    sema = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": baslik, "description": aciklama, "url": url, "datePublished": r["tarih"], "dateModified": r["tarih"],
         "inLanguage": "tr", "articleSection": kat_ad, "image": "https://lunayapim.com/assets/studyo/%s.jpg" % r["gorsel"],
         "author": {"@type": "Organization", "name": "Luna Yapım", "url": "https://lunayapim.com/"},
         "publisher": {"@type": "Organization", "name": "LunaTrendSaphiens", "url": KOK_URL, "logo": {"@type": "ImageObject", "url": "https://lunayapim.com/assets/luna-logo.png"}},
         "citation": [{"@type": "CreativeWork", "name": a, "url": u} for a, u in r.get("kaynaklar", [])]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in r.get("sss", [])]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "LunaTrendSaphiens", "item": KOK_URL},
            {"@type": "ListItem", "position": 2, "name": kat_ad, "item": KOK_URL + r["kat"] + "/"},
            {"@type": "ListItem", "position": 3, "name": baslik, "item": url}]}]}, ensure_ascii=False) + "</script>"
    bolumler = "".join("<h2>%s</h2><p>%s</p>" % (_e(h), _e(p)) for h, p in r["bolumler"])
    # reklam: ikinci bölümden sonra
    parcalar = ["<h2>%s</h2><p>%s</p>" % (_e(h), _e(p)) for h, p in r["bolumler"]]
    if len(parcalar) > 2:
        parcalar.insert(2, REKLAM)
    bolumler = "".join(parcalar)
    sss = "".join("<h3>%s</h3><p>%s</p>" % (_e(q), _e(a)) for q, a in r.get("sss", []))
    kaynaklar = "".join('<li><a href="%s" rel="nofollow noopener" target="_blank">%s</a></li>' % (_e(u), _e(a)) for a, u in r.get("kaynaklar", []))
    risk = RISK if r["kat"] == "piyasa" else ""
    komsu_kart = "".join(_kart(k, False, "../", "") for k in komsular[:3])
    govde = """
<article class="ts-yazi">
  <div class="wrap ts-yazi-izgara">
    <div class="ts-yazi-ana">
      <div class="crumbs"><a href="./">LunaTrendSaphiens</a> · <a href="%s/">%s</a> · Rehber</div>
      <span class="ts-chip">Rehber</span>
      <h1>%s</h1>
      <p class="ts-yazi-meta">%s · %d dk okuma · kalıcı yazı, gerektikçe güncellenir</p>
      <div class="ts-yazi-gorsel">%s</div>
      %s
      <p class="ts-olgu">%s</p>
      <div class="ts-rehber">%s</div>
      <div class="ts-baglam ts-sss"><h2>Sık sorulanlar</h2>%s</div>
      <div class="ts-baglam"><h2>Kaynaklar</h2><ul class="ts-kaynaklar">%s</ul><p class="ts-not">Tarih ve kural bilgisi yalnızca kurumun kendi yayınına dayanır; bir kural değiştiğinde yazı güncellenir ve güncelleme tarihi değişir.</p></div>
      %s
    </div>
    <aside class="ts-yan">
      %s
      %s
      <div class="ts-kutu"><h2 class="etk">Devamı</h2><div class="ts-kartlar ts-kartlar-dar">%s</div></div>
    </aside>
  </div>
</article>
""" % (r["kat"], _e(kat_ad), _e(baslik), _e(_tr_tarih(r["tarih"])), _okuma_sure(govde_metin), _gorsel(r["gorsel"], baslik, "b"), _paylas(url, baslik),
       _e(r["ozet"]), bolumler, sss, kaynaklar, risk, _takvim_kutu("../", ""), _abone("../"), komsu_kart)
    return _bas(kisa + " | TrendSaphiens", aciklama, url, r["gorsel"], sema, "article") + govde + _alt("../", "")


def sistem_html():
    on, tr = "../../", "../"
    baslik = "Sonuç veren organlarımız — LunaTrendSaphiens"
    aciklama = "Bu yayını ve piyasa defterini işleten organlar: Gözcü, Aday, Rejim, Beyin, İcra, Bekçi, Ekspertiz, Teyit, Pusula, Asistan. Ne yaptıkları; nasıl yaptıkları değil."
    url = KOK_URL + "sistem/"
    organ = "".join('<div class="ts-organ gor"><b>%s</b><p>%s</p></div>' % (_e(a), _e(b)) for a, b in ORGANLAR)
    ilke = "".join('<div class="ts-ilke"><b>%s</b><p>%s</p></div>' % (_e(a), _e(b)) for a, b in ILKELER)
    govde = """
<section class="ts-manset ts-manset-sistem">
  <div class="wrap">
    <div class="crumbs"><a href="../">LunaTrendSaphiens</a> · Sistem</div>
    <div class="ts-mast"><h1>Sonuç veren organlarımız</h1><p>Bu yayın bir kişinin sabah rutini değil; birbirini denetleyen organların işi. Ne yaptıklarını yazıyoruz, nasıl yaptıklarını değil.</p></div>
    <div class="ts-organlar">%s</div>
  </div>
</section>
<section class="ts-govde"><div class="wrap ts-izgara">
  <div class="ts-akis">
    <div class="ts-bas"><h2 class="etk">İlkeler</h2></div>
    <div class="ts-ilkeler">%s</div>
    <div class="ts-giris"><h2>Bu organlar ne üretir</h2><p>Her sabah günün haberleri seçilir ve bu yayına basılır; her hafta piyasa defterinin karnesi çıkar; her ay sitenin bütün sayfaları yeniden denetlenir. Aday firmalar için eksik listesi ve kanıtlı teklif üretilir, Telegram'a düşer. Bir organ tek başına karar vermez: Aday'ın önerdiğini Beyin puanlar, Teyit doğrular, Bekçi gerektiğinde durdurur. Sonuçlar kanıt defterinde ve haftalık karnede herkese açık durur.</p><p>Bu organların hiçbiri tek başına yayın yapmaz. Bir haber önce Pusula'nın tarayıcısından geçer, kaynak ve tarih doğrulanır, sonra Asistan'ın dizinine girer; bir piyasa sonucu önce Teyit'ten, sonra karneden geçer. İnsan eli iki yerde vardır: seçimde ve itirazda. Gerisi organların işidir ve her adım deftere yazılır.</p></div>
    <div class="ts-analiz" style="margin-top:28px"><h2 class="etk">Neden anlatmıyoruz</h2><p>Bir sistemin değeri sonuçlarındadır; sonuçlar kanıt defterinde ve haftalık karnede duruyor. Organların içi ticari sırrımız — ama defter herkese açık.</p><a href="%smatrix">Kanıt defteri →</a></div>
    %s
  </div>
  <aside class="ts-yan">%s<div class="ts-kutu"><span class="etk">Yazılım</span><p>Aynı organ mantığını müşteriler için de kuruyoruz: tarayan, puanlayan, raporlayan sistemler.</p><a class="btn btn-cizgi" href="%syazilim">Yazılım →</a></div></aside>
</div></section>
""" % (organ, ilke, on, RISK, _abone(on), on)
    sema = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "AboutPage", "name": baslik, "url": url, "description": aciklama,
            "isPartOf": {"@type": "WebSite", "name": "LunaTrendSaphiens", "url": KOK_URL}, "publisher": {"@type": "Organization", "name": "Luna Yapım", "url": "https://lunayapim.com/"}}, ensure_ascii=False) + "</script>"
    return _bas(baslik, aciklama, url, "../video/karga-k6", sema, "website", on, tr) + govde + _alt(on, tr)


def _gunluk_kabuk(baslik, aciklama, url, kat, gorsel, govde, sema_tur="Article", tarih=None):
    """Bölüm günlükleri için ortak kabuk — /trend/<kat>/<tarih>.html (on=../../, tr=../)."""
    on, tr = "../../", "../"
    sema = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": sema_tur, "headline": baslik, "description": aciklama, "url": url, "inLanguage": "tr",
         "datePublished": tarih or datetime.date.today().isoformat(), "dateModified": tarih or datetime.date.today().isoformat(),
         "author": {"@type": "Organization", "name": "Luna Yapım", "url": "https://lunayapim.com/"},
         "publisher": {"@type": "Organization", "name": "LunaTrendSaphiens", "url": KOK_URL, "logo": {"@type": "ImageObject", "url": "https://lunayapim.com/assets/luna-logo.png"}}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "LunaTrendSaphiens", "item": KOK_URL},
            {"@type": "ListItem", "position": 2, "name": KATEGORI[kat][0], "item": KOK_URL + kat + "/"},
            {"@type": "ListItem", "position": 3, "name": baslik, "item": url}]}]}, ensure_ascii=False) + "</script>"
    return _bas(baslik, aciklama, url, gorsel, sema, "article", on, tr) + govde + _alt(on, tr)


def aranan_html(v, kok):
    t = v["tarih"]; ar = v.get("aranan") or []
    baslik = "Türkiye bugün ne aradı? %s | TrendSaphiens" % _tr_tarih(t)
    aciklama = ("Google Trends Türkiye listesi, %s: günün en çok aranan %d başlığı, her birinin yanında Google'ın bağladığı haber ve kaynağı. Neden arandı, nereye bakılır." % (_tr_tarih(t), len(ar)))[:158]
    url = KOK_URL + "aranan/" + t
    sat = []
    for i, a in enumerate(ar, 1):
        kat = BOLUM_KAT.get(a.get("bolum"), a.get("bolum") if a.get("bolum") in KATEGORI else "gundem")
        hab = ('<p class="ts-aranan-haber">%s — <a href="%s" rel="nofollow noopener" target="_blank">%s</a></p>'
               % (_e(a.get("haber_baslik")), _e(a.get("haber_url")), _e(a.get("haber_kaynak") or "kaynak"))) if a.get("haber_url") else '<p class="ts-aranan-haber ts-not">Google bu başlığa haber bağlamadı; yalnız arama var.</p>'
        sat.append('<li class="ts-aranan"><span class="ts-aranan-no">%02d</span><div><h2>%s</h2><p class="ts-meta">%s · <a href="../%s/">%s</a></p>%s</div></li>'
                   % (i, _e(a["baslik"]), _e(("yaklaşık " + a["hacim"] + " arama") if a.get("hacim") else "hacim belirtilmedi"), kat, _e(KATEGORI.get(kat, ("Gündem",))[0]), hab))
    govde = """
<article class="ts-yazi"><div class="wrap ts-yazi-izgara">
  <div class="ts-yazi-ana">
    <div class="crumbs"><a href="../">LunaTrendSaphiens</a> · <a href="./">Bugün Aranan</a> · %s</div>
    <span class="ts-chip">Günün listesi</span>
    <h1>Türkiye bugün ne aradı?</h1>
    <p class="ts-yazi-meta">%s · Google Trends Türkiye · %d başlık</p>
    %s
    <p class="ts-olgu">Liste ve sıralama Google'ındır; her başlığın yanında Google'ın bağladığı haber ve kaynağı durur. Bizim eklediğimiz, hangi bölümde okunacağı. Rakam yalnızca Google'ın verdiği yaklaşık hacimdir.</p>
    <ol class="ts-aranan-liste">%s</ol>
    %s
    <div class="ts-baglam"><h2>Bu liste nasıl okunmalı</h2><p><strong>Hacim yaklaşık değerdir.</strong> Google "yaklaşık 20 bin+" gibi bir eşik verir; kesin sayı değildir. <strong>Haber bağlantısı Google'ındır.</strong> Biz seçmedik; Google o aramaya en çok tıklanan haberi bağlar. <strong>Bölüm bizimdir.</strong> Başlığı hangi bölümde okuyacağınızı biz eşleriz; yanılırsak düzeltiriz.</p></div>
  </div>
  <aside class="ts-yan">%s%s%s<div class="ts-kutu"><h2 class="etk">Önceki günler</h2><p><a href="./">Bugün Aranan arşivi →</a></p></div></aside>
</div></article>
""" % (_e(_tr_tarih(t)), _e(_tr_tarih(t)), len(ar), _paylas(url, "Türkiye bugün ne aradı? " + _tr_tarih(t)), "".join(sat), REKLAM, _rakam_kutu("../../", "../"), _takvim_kutu("../../", "../"), _abone("../../"))
    return _gunluk_kabuk(baslik, aciklama, url, "aranan", BOLUM_GORSEL["aranan"], govde, "ItemList", t)


def bolum_gunluk_html(kat, t, liste, cerceve):
    ad = KATEGORI[kat][0]
    baslik = "%s · %s | TrendSaphiens" % (ad, _tr_tarih(t))
    aciklama = ("%s, %s: %s" % (ad, _tr_tarih(t), " · ".join(x["baslik"][:50] for x in liste[:3])))[:158]
    url = KOK_URL + kat + "/" + t
    sat = "".join('<li class="ts-aranan"><span class="ts-aranan-no">%02d</span><div><h2>%s</h2>%s<p class="ts-aranan-haber">Kaynak: <a href="%s" rel="nofollow noopener" target="_blank">%s</a>%s</p></div></li>'
                  % (i, _e(x["baslik"]), ('<p class="ts-olgu" style="font-size:15.5px">%s</p>' % _e(x["ozet"])) if x.get("ozet") else "",
                     _e(x["url"]), _e(x.get("kaynak") or "haber"), (" · " + _e(x["tarih"][:16])) if x.get("tarih") else "")
                  for i, x in enumerate(liste, 1))
    govde = """
<article class="ts-yazi"><div class="wrap ts-yazi-izgara">
  <div class="ts-yazi-ana">
    <div class="crumbs"><a href="../">LunaTrendSaphiens</a> · <a href="./">%s</a> · %s</div>
    <span class="ts-chip">%s</span>
    <h1>%s: bugün ne var?</h1>
    <p class="ts-yazi-meta">%s · %d madde · kaynaklı</p>
    %s
    <p class="ts-olgu">%s</p>
    <ol class="ts-aranan-liste">%s</ol>
    %s
    <div class="ts-baglam"><h2>Nasıl derliyoruz</h2><p>Bu liste Google Haberler'de son günlerin %s başlıklarından derlenir; her madde kaynağı ve tarihiyle durur, haber metni kopyalanmaz. Sıralama yayın saatine göredir, önem sırası değildir. Yanlış ya da eksik bir madde görürseniz yazın; düzeltir, düzelttiğimizi yazarız.</p></div>
  </div>
  <aside class="ts-yan">%s%s%s<div class="ts-kutu"><h2 class="etk">Arşiv</h2><p><a href="./">%s arşivi →</a></p></div></aside>
</div></article>
""" % (_e(ad), _e(_tr_tarih(t)), _e(ad), _e(ad), _e(_tr_tarih(t)), len(liste), _paylas(url, "%s · %s" % (ad, _tr_tarih(t))), _e(cerceve), sat, REKLAM, _e(ad.lower()), _rakam_kutu("../../", "../"), _takvim_kutu("../../", "../"), _abone("../../"), _e(ad))
    return _gunluk_kabuk(baslik, aciklama, url, kat, BOLUM_GORSEL.get(kat, "set-isik"), govde, "ItemList", t)


def _piyasa_sorular(tc, al):
    """Arayanın sorduğu biçimde kısa, kaynaklı cevaplar: 'Dolar kaç TL?' — rakam yalnız veri varsa."""
    k = tc.get("kurlar", {}); tarih = tc.get("tarih") or ""
    sat = []
    for kod, ad in (("USD", "Dolar"), ("EUR", "Euro"), ("GBP", "Sterlin")):
        x = k.get(kod, {})
        if x.get("satis"):
            sat.append("<h3>%s kaç TL?</h3><p>TCMB'nin %s tarihli tablosunda %s döviz alış %s TL, döviz satış %s TL. Bankalar ve döviz büroları kendi makasını uygular; bu rakam gösterge kurudur.</p>" % (ad, _e(tarih), ad.lower(), _e(_tl(x.get("alis")) or "—"), _e(_tl(x["satis"]))))
    for anahtar, ad in (("gram-altin", "Gram altın"), ("ceyrek-altin", "Çeyrek altın"), ("tam-altin", "Tam altın")):
        x = al.get(anahtar) or {}
        if isinstance(x, dict) and x.get("satis"):
            d = (" Güne göre değişim %s." % _e(x["degisim"])) if x.get("degisim") else ""
            sat.append("<h3>%s kaç TL?</h3><p>Beslemenin %s güncellemesinde %s alış %s TL, satış %s TL.%s Kuyumcuda işçilik ve makas eklenir.</p>" % (ad, _e(al.get("guncelleme") or "—"), ad.lower(), _e(x.get("alis") or "—"), _e(x["satis"]), d))
    if not sat:
        return ""
    return '<div class="ts-baglam ts-sss"><h2>Kısa cevaplar</h2>%s</div>' % "".join(sat)


def piyasa_html(v):
    t = v["tarih"]; tc = v.get("tcmb") or {}; al = v.get("altin") or {}
    baslik = "Dolar, euro ve altın bugün · %s | TrendSaphiens" % _tr_tarih(t)
    k = tc.get("kurlar", {})
    aciklama = ("%s: TCMB döviz satış — dolar %s TL, euro %s TL%s. Resmî kaynak, yatırım tavsiyesi değildir." % (
        _tr_tarih(t), _tl(k.get("USD", {}).get("satis")) or "—", _tl(k.get("EUR", {}).get("satis")) or "—",
        (", gram altın %s TL" % al["gram-altin"]["satis"]) if al.get("gram-altin") else ""))[:158]
    url = KOK_URL + "piyasa/" + t
    kur_sat = "".join("<tr><td>%s <span class='g'>(%s)</span></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
                      % (_e(kod), _e(x.get("ad", "")), _e(_tl(x.get("alis")) or "—"), _e(_tl(x.get("satis")) or "—"), _e(_tl(x.get("efektif_alis")) or "—"), _e(_tl(x.get("efektif_satis")) or "—"))
                      for kod, x in k.items())
    altin_sat = "".join("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (_e(x["ad"]), _e(x.get("alis") or "—"), _e(x.get("satis") or "—"), _e(x.get("degisim") or "—"))
                        for a, x in al.items() if isinstance(x, dict))
    govde = """
<article class="ts-yazi"><div class="wrap ts-yazi-izgara">
  <div class="ts-yazi-ana">
    <div class="crumbs"><a href="../">LunaTrendSaphiens</a> · <a href="./">Piyasalar</a> · %s</div>
    <span class="ts-chip">Günün rakamı</span>
    <h1>Dolar, euro ve altın bugün</h1>
    <p class="ts-yazi-meta">%s · TCMB bülten %s · alındı %s</p>
    %s
    <h2>TCMB döviz kurları (TL)</h2>
    <div class="tablo-kaydir"><table class="ts-tablo"><thead><tr><th>Para birimi</th><th>Döviz alış</th><th>Döviz satış</th><th>Efektif alış</th><th>Efektif satış</th></tr></thead><tbody>%s</tbody></table></div>
    <p class="ts-not">Kaynak: <a href="https://www.tcmb.gov.tr/kurlar/today.xml" rel="nofollow noopener" target="_blank">TCMB günlük kur tablosu</a>, tarih %s. Bankaların uyguladığı kur farklıdır; bu tablo gösterge niteliğindedir.</p>
    <h2>Altın (TL)</h2>
    <div class="tablo-kaydir"><table class="ts-tablo"><thead><tr><th>Ürün</th><th>Alış</th><th>Satış</th><th>Değişim</th></tr></thead><tbody>%s</tbody></table></div>
    <p class="ts-not">Kaynak: <a href="https://finans.truncgil.com/" rel="nofollow noopener" target="_blank">truncgil finans</a>, güncelleme %s. Kuyumcu fiyatı işçilik ve makasa göre değişir.</p>
    %s
    %s
    <div class="ts-baglam"><h2>Bu sayfa nasıl okunmalı</h2><p><strong>Rakamlar kaynaktan, yorum yok.</strong> Döviz TCMB'nin resmî günlük tablosundan, altın açık bir finans beslemesinden alınır; sayfa her sabah yeniden üretilir ve alınma saati üstte yazar. <strong>Tavsiye değildir.</strong> Bu sayfa alım-satım önerisi, hedef ya da tahmin içermez; hangi rakamın neden değiştiğini merak ediyorsanız günün haberleri Gündem bölümündedir.</p></div>
    %s
  </div>
  <aside class="ts-yan">%s<div class="ts-kutu"><h2 class="etk">Piyasayı okuyan sistem</h2><p>Haftalık karne ve kanıt defteri: sistem neye baktı, hangi hatlar sınavı geçti.</p><a class="btn btn-cizgi" href="../../bulten/">Matrix Bülteni →</a></div></aside>
</div></article>
""" % (_e(_tr_tarih(t)), _e(_tr_tarih(t)), _e(tc.get("bulten") or "—"), _e(v.get("alindi") or ""), _paylas(url, "Dolar, euro ve altın bugün · " + _tr_tarih(t)),
       kur_sat or "<tr><td colspan='5'>TCMB bugün tablo yayınlamadı (tatil ya da erişim yok).</td></tr>", _e(tc.get("tarih") or "—"),
       altin_sat or "<tr><td colspan='4'>Altın beslemesi cevap vermedi; rakam uydurmuyoruz.</td></tr>", _e(al.get("guncelleme") or "—"), REKLAM, _piyasa_sorular(tc, al), RISK, _takvim_kutu("../../", "../") + _abone("../../"))
    return _gunluk_kabuk(baslik, aciklama, url, "piyasa", BOLUM_GORSEL["piyasa"], govde, "Article", t)


# ---------------------------------------------------------------- yayın
def yayinla(kok=None, paylas=False):
    kok = kok or SITE_KOK
    d = os.path.join(kok, "trend"); os.makedirs(d, exist_ok=True)
    for k in KATEGORI:
        os.makedirs(os.path.join(d, k), exist_ok=True)
    hepsi = _hepsi(kok)
    haberler = [m for m in hepsi if m["tur"] == "haber"]
    yeni = []
    for i, m in enumerate(haberler):
        yol = os.path.join(d, m["slug"] + ".html")
        if not os.path.exists(yol):
            yeni.append(m)
        komsu = [k for k in hepsi if k is not m][:3]
        open(yol, "w", encoding="utf-8").write(haber_html(m, komsu))
    # rehberler (kalıcı yazılar)
    rehberler = [m for m in hepsi if m["tur"] == "rehber"]
    for m in rehberler:
        yol = os.path.join(d, m["slug"] + ".html")
        if not os.path.exists(yol):
            yeni.append(m)
        komsu = [k for k in hepsi if k is not m and k["kat"] == m["kat"]][:3] or [k for k in hepsi if k is not m][:3]
        open(yol, "w", encoding="utf-8").write(rehber_html(m, komsu))
    # günlük sayfalar: aranan, bölüm günlükleri, piyasa
    gunluk_adres = []
    try:
        from . import trend_izle as TI, piyasa_gunluk as PG
        for v in TI.hepsi():
            t = v["tarih"]
            if v.get("aranan"):
                open(os.path.join(d, "aranan", t + ".html"), "w", encoding="utf-8").write(aranan_html(v, kok)); gunluk_adres.append(KOK_URL + "aranan/" + t)
            cerceve = {b[0]: b[3] for b in TI.BOLUMLER}
            for b, liste in (v.get("bolumler") or {}).items():
                kat = BOLUM_KAT.get(b)
                if kat and liste:
                    open(os.path.join(d, kat, t + ".html"), "w", encoding="utf-8").write(bolum_gunluk_html(kat, t, liste, cerceve.get(b, ""))); gunluk_adres.append(KOK_URL + kat + "/" + t)
        for v in PG.hepsi():
            if v.get("tcmb") or v.get("altin"):
                open(os.path.join(d, "piyasa", v["tarih"] + ".html"), "w", encoding="utf-8").write(piyasa_html(v)); gunluk_adres.append(KOK_URL + "piyasa/" + v["tarih"])
    except Exception as ex:
        gunluk_adres.append("HATA: %s" % ex)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(akis_html(kok))
    for k in KATEGORI:
        if k == "sistem":
            open(os.path.join(d, k, "index.html"), "w", encoding="utf-8").write(sistem_html())
        else:
            open(os.path.join(d, k, "index.html"), "w", encoding="utf-8").write(akis_html(kok, k))
    # site haritası
    y = os.path.join(kok, "sitemap.xml")
    if os.path.exists(y):
        s = open(y, encoding="utf-8").read()
        adresler = [KOK_URL] + [KOK_URL + k + "/" for k in KATEGORI] + [KOK_URL + m["slug"] for m in haberler + rehberler] + [a for a in gunluk_adres if not a.startswith("HATA")]
        bugun = datetime.date.today().isoformat()
        # artık var olmayan trend/ sayfalarını haritadan düşür (ince sayfa kapısı, slug değişimi)
        def _kalsin(m):
            u = m.group(1)
            if not u.startswith(KOK_URL) or u.endswith("/"):
                return m.group(0)
            return m.group(0) if os.path.exists(os.path.join(kok, u[len("https://lunayapim.com/"):] + ".html")) else ""
        s = re.sub(r"[ \t]*<url><loc>([^<]+)</loc>.*?</url>\n?", _kalsin, s, flags=re.S)
        for a in adresler:
            if ("<loc>%s</loc>" % a) not in s:
                s = s.replace("</urlset>", "  <url><loc>%s</loc><lastmod>%s</lastmod><changefreq>daily</changefreq><priority>0.7</priority></url>\n</urlset>" % (a, bugun))
        open(y, "w", encoding="utf-8").write(s)
    try:
        sys.path.insert(0, os.path.join(KOK_DIZIN, "site-uretici"))
        import sonislem
        sonislem.calistir(kok, desen="trend/**/*.html")
    except Exception:
        pass
    # IndexNow: yeni ve günlük sayfaları Bing/Yandex'e anında bildir (Google sitemap'ten okur). Ağ yoksa sessiz geçer.
    indexnow_sonuc = None
    try:
        from . import indexnow as IN
        bildirilecek = [KOK_URL] + [KOK_URL + m["slug"] for m in yeni] + [a for a in gunluk_adres if not a.startswith("HATA")]
        indexnow_sonuc = IN.bildir(bildirilecek, kok)
        indexnow_sonuc = {"gonderilen": indexnow_sonuc.get("gonderilen"), "sonuc": [(x.get("uc"), x.get("durum")) for x in indexnow_sonuc.get("sonuc", [])]} if isinstance(indexnow_sonuc, dict) else indexnow_sonuc
    except Exception as ex:
        indexnow_sonuc = "bildirilemedi: %s" % ex
    sonuc = {"haber": len(haberler), "rehber": len(rehberler), "yeni": [m["slug"] for m in yeni], "indexnow": indexnow_sonuc, "kategori": len(KATEGORI), "gunluk": len(gunluk_adres), "hata": [a for a in gunluk_adres if a.startswith("HATA")]}
    if paylas:
        try:
            from . import x_paylas
            bugun = datetime.date.today().isoformat()
            gonderiler = [("%s — LunaTrendSaphiens" % m["baslik"], KOK_URL + m["slug"]) for m in yeni[:3]]
            if any(a.endswith("aranan/" + bugun) for a in gunluk_adres):
                gonderiler.append(("Türkiye bugün ne aradı? Günün listesi, kaynaklarıyla — LunaTrendSaphiens", KOK_URL + "aranan/" + bugun))
            if any(a.endswith("piyasa/" + bugun) for a in gunluk_adres):
                gonderiler.append(("Dolar, euro ve altın bugün — TCMB tablosu ve altın, kaynaklı. Yatırım tavsiyesi değildir.", KOK_URL + "piyasa/" + bugun))
            # takvim sırası: bugün aranacak konuların sayfası üretildiyse, saat sırasıyla
            try:
                from . import takvim as TK
                for k in TK.paylasim_sirasi(bugun):
                    adres = KOK_URL + k["sayfa"]
                    if adres in gunluk_adres and not any(u == adres for _, u in gonderiler):
                        gonderiler.append(("%s — kaynaklı günlük sayfa, LunaTrendSaphiens" % k["metin"], adres))
            except Exception:
                pass
            sonuc["x"] = [x_paylas.paylas(m, u) for m, u in gonderiler]
        except Exception as ex:
            sonuc["x"] = "paylaşılamadı: %s" % ex
    return sonuc


if __name__ == "__main__":
    print(yayinla())
