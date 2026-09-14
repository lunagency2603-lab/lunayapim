# -*- coding: utf-8 -*-
"""
GELEN TALEP ÇÖZÜMLEYİCİ — özelleştirilmiş iş taleplerine hazır yanıt.

Bir müşteri "3 dakikalık AI kısa film istiyorum, karakter tutarlılığı şart,
senaryo hazır" yazdığında; hangi hizmet, hangi bandın neresi, hangi kalemler
fiyatı yukarı çekiyor ve hangi dürüst sınırı baştan söylememiz gerektiği
belli olsun diye yazıldı.

Uydurma yapmıyor: her hizmetin bandı, kapsamı ve referans cevabı sitedeki
hizmet sayfasıyla birebir aynı. Referansı olmayan hizmette "referansımız yok"
diyor ve yerine test/prova öneriyor.

Kullanım:
    from pusula import talep
    r = talep.coz(gelen_mesaj)          # sınıflandırma + bant + gerekçe
    m = talep.taslak(gelen_mesaj)       # kısa + uzun yanıt metni
"""
import re, json, datetime

# ------------------------------------------------------------ türkçe küçültme
_KUCUK = str.maketrans("ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZQWX",
                       "abcçdefgğhıijklmnoöprsştuüvyzqwx")


def _kucuk(s):
    return (s or "").translate(_KUCUK).lower()


def _var(metin, kelimeler):
    """Kelimelerden en az biri metinde geçiyor mu (küçültülmüş karşılaştırma)."""
    k = _kucuk(metin)
    return [x for x in kelimeler if _kucuk(x) in k]


# ------------------------------------------------------------------- hizmetler
# band: (alt, üst) TL. Sitedeki hizmet sayfasıyla aynı olmak zorunda.
HIZMET = {
 "ai_kisa_film": {
  "ad": "AI kısa film ve karakter tutarlılığı",
  "sayfa": "/hizmetler/ai-kisa-film.html",
  "band": (120000, 400000),
  "sure": "3–5 hafta",
  "anahtar": ["ai kısa film", "yapay zeka film", "karakter tutarlılığı",
              "character consistency", "face consistency", "kısa film",
              "hikaye filmi", "hikâye filmi", "image-to-video", "sinematik"],
  "kapsam": ["AI üretim", "kurgu ve renk", "müzik ve ses tasarımı",
             "post-prodüksiyon", "altyazılı/altyazısız sürüm",
             "yatay + kare + dikey teslim", "iki tur revizyon"],
  "fark": ("Genelde fotoğraf hareket ettirilir ve klipler arka arkaya dizilir. "
           "Biz sahne kuruyoruz: plan ölçeği, kamera hareketi, bakış yönü ve "
           "sahne içi eylem — karakter kimliği sahneler boyunca sabit."),
  "sinir": ("Karakter tutarlılığı yüksek oranda sağlanıyor ama %100 değil. "
            "En iyi sonuç yakın ve orta planlarda çıkıyor; aşırı geniş planlar, "
            "hızlı hareket ve kalabalık sahneler zorlandığımız yerler."),
  "kapi": ("karakter testi", "Kendi fotoğraflarınızla üç plan ölçeğinde "
           "(yakın, orta, genel) test kareleri üretiyoruz. Onaylamadan film "
           "üretimine geçmiyoruz; devam ederseniz bedeli film fiyatından düşülüyor."),
  "referans": None,   # gerçek kişi yüzünden yayınlanmış işimiz yok
  "referans_yok": ("Gerçek kişilerin yüzünden üretilmiş, yayınlanmış bir referans "
                   "filmimiz yok — bu işler kişisel olduğu için müşterilerimiz "
                   "yayınlanmasını istemiyor, biz de izinsiz paylaşmıyoruz. "
                   "Sizin filminiz için de aynı kural geçerli olacak."),
  "en_yakin": ("Karga serisi", "tamamen üretilmiş bir karakterin açılış, geçiş, "
               "makro göz, kanat açılışı ve kapanış olmak üzere birden çok sahnede "
               "aynı kimlikle korunduğu bir seri — tüy dokusu, göz içi kırılma ve "
               "ışık her sahnede tutarlı"),
  "gerekli": ["Senaryo ve sahne akışı",
              "Kişi başına 15–20+ fotoğraf (farklı açı, ışık ve mümkünse farklı yıllar)",
              "Mekân referansları",
              "Müzik yönü (tempo, tür, varsa örnek parça)",
              "Öncelikli teslim formatı (yatay / kare / dikey — hepsini veriyoruz)",
              "Fotoğraftaki kişilerin rızası (sözleşmede yazılı yer alıyor)"],
 },
 "urun_animasyon": {
  "ad": "Ürün animasyonu",
  "sayfa": "/hizmetler/urun-animasyon.html",
  "band": (35000, 140000),
  "sure": "2–4 hafta",
  "anahtar": ["ürün animasyon", "ürün tanıtım", "3d ürün", "anlatım animasyonu",
              "explainer", "reklam animasyonu"],
  "kapsam": ["3D modelleme veya AI üretim", "animasyon", "kurgu ve renk",
             "seslendirme/müzik", "çok dilli sürüm", "yatay + dikey teslim"],
  "fark": ("Genelde tek bir yatay video teslim edilir. Biz tek üretimden "
           "dil ve format sürümlerini birlikte çıkarıyoruz — ikinci mecra için "
           "işi baştan yaptırmıyorsunuz."),
  "sinir": ("Ürünün gerçek dokusu ve ölçüsü kritikse teknik çizim veya iyi "
            "fotoğraf gerekiyor; elimizde yoksa benzerlik düşer."),
  "kapi": ("stil karesi", "Üretime geçmeden tek bir kare üzerinde ışık, renk ve "
           "kamera dilini onaylıyoruz."),
  "referans": ("Galzura", "TR ve DE seslendirmeli anlatım animasyonu; aynı "
               "üretimden yatay ve dikey sürümler çıkarıldı"),
  "gerekli": ["Ürün görselleri veya 3D/teknik çizim", "Anlatılacak mesaj",
              "Dil ve format listesi", "Marka renk ve font bilgisi"],
 },
 "insaat_3d": {
  "ad": "İnşaat 3D modelleme ve görselleştirme",
  "sayfa": "/hizmetler/insaat-3d-modelleme.html",
  "band": (40000, 250000),
  "sure": "2–6 hafta",
  "anahtar": ["3d modelleme", "mimari görselleştirme", "render", "maket",
              "proje tanıtım", "inşaat", "konut projesi", "iç mekan"],
  "kapsam": ["3D model", "dış/iç mekân render", "animasyon turu",
             "gündüz/gece varyantı", "yüksek çözünürlük teslim"],
  "fark": ("Genelde tek açı render verilir. Biz projeyi modelleyip aynı "
           "modelden satış için gereken tüm açıları, kat planlarını ve "
           "animasyon turunu çıkarıyoruz."),
  "sinir": ("Mimari proje dosyası eksikse model tahmine dayanır; bunu "
            "teslimden önce söylüyoruz."),
  "kapi": ("tek açı denemesi", "Bir açıyı modelleyip render alıyoruz; "
           "kalite ve stil onaylanmadan tüm projeye geçmiyoruz."),
  "referans": None,
  "referans_yok": ("Bu kategoride yayınlanabilir referansımızı iş sahiplerinin "
                   "izniyle sınırlı tutuyoruz."),
  "en_yakin": ("İşler sayfası", "prodüksiyon ve 3D işlerimiz"),
  "gerekli": ["Mimari proje (dwg/pdf)", "Malzeme ve renk kararları",
              "İstenen açı sayısı", "Teslim tarihi"],
 },
 "klip": {
  "ad": "Klip ve tanıtım çekimi",
  "sayfa": "/hizmetler/klip-cekimi.html",
  "band": (25000, 150000),
  "sure": "1–3 hafta",
  "anahtar": ["klip çekimi", "müzik klibi", "tanıtım filmi", "reklam filmi",
              "çekim", "video çekimi", "işletme tanıtım"],
  "kapsam": ["çekim planı", "çekim günü", "kurgu ve renk", "müzik/ses",
             "sosyal medya sürümleri"],
  "fark": ("Genelde çekilir ve kurgulanır. Biz çekim planını önce çıkarıyoruz — "
           "hangi plan neyi anlatacak, çekim günü belli oluyor."),
  "sinir": "Hava ve mekân izni takvimi etkileyebiliyor; yedek gün planlıyoruz.",
  "kapi": ("çekim planı", "Çekimden önce sahne sahne planı yazılı veriyoruz."),
  "referans": ("Kısa film ve klip işlerimiz", "kurgu, ışık ve ritim tarafını gösteriyor"),
  "gerekli": ["Mekân ve tarih", "Anlatılacak hikâye veya mesaj",
              "Süre ve teslim formatları"],
 },
 "drone": {
  "ad": "Drone ve FPV çekim",
  "sayfa": "/hizmetler/drone-fpv.html",
  "band": (15000, 80000),
  "sure": "1–2 hafta",
  "anahtar": ["drone", "fpv", "havadan çekim", "hava çekimi"],
  "kapsam": ["uçuş planı", "çekim", "kurgu ve renk", "ham kayıt teslimi"],
  "fark": ("Genelde tek geniş plan alınır. Biz FPV ile iç mekâna giren, "
           "tek planda bina turu yapan geçişler kuruyoruz."),
  "sinir": "Uçuşa yasak bölge ve izin gerektiren alanlar önceden kontrol ediliyor.",
  "kapi": ("uçuş planı", "Lokasyonu ve izin durumunu çekimden önce netleştiriyoruz."),
  "referans": ("Prodüksiyon işlerimiz", "havadan ve FPV planlarımız"),
  "gerekli": ["Lokasyon", "Tarih", "İstenen plan tipleri"],
 },
 "seo": {
  "ad": "SEO ve içerik",
  "sayfa": "/hizmetler/seo-icerik.html",
  "band": (8000, 45000),
  "sure": "aylık düzen",
  "aylik": True,
  "anahtar": ["seo", "google", "arama", "içerik", "blog", "sıralama",
              "organik", "search console"],
  "kapsam": ["teknik denetim", "sayfa yapısı ve şema", "içerik planı",
             "aylık ölçüm raporu", "Search Console takibi"],
  "fark": ("Genelde anahtar kelime listesi ve blog yazısı verilir. Biz önce "
           "teknik denetimden geçiriyoruz — sayfalar taranabilir değilse "
           "içerik para kaybı."),
  "sinir": ("SEO'da ilk sonuç 2–3 ayda görünür; ilk aydan sıralama sözü veren "
            "kimseye inanmayın."),
  "kapi": ("ücretsiz denetim", "Sitenizi kendi denetçimizden geçirip bulduğumuz "
           "eksikleri liste hâlinde veriyoruz — çalışmasak da sizde kalıyor."),
  "referans": ("Kendi sitemiz", "331 sayfa, 0 hata, 0 uyarı — ölçümü ve açık "
               "eksiklerimizi şeffaflık sayfasında yayınlıyoruz"),
  "gerekli": ["Site adresi", "Search Console erişimi veya dışa aktarım dosyası",
              "Hedef şehir/hizmet listesi"],
 },
 "ai_seo": {
  "ad": "Yapay zekâ SEO (AI arama görünürlüğü)",
  "sayfa": "/hizmetler/yapay-zeka-seo.html",
  "band": (10000, 55000),
  "sure": "aylık düzen",
  "aylik": True,
  "anahtar": ["yapay zeka seo", "ai seo", "chatgpt", "gemini", "yapay zekaya",
              "llm", "aeo", "geo", "yapay zeka arama"],
  "kapsam": ["yapılandırılmış veri (JSON-LD)", "soru-cevap içerik yapısı",
             "kaynak gösterilebilirlik", "AI yanıtlarında görünürlük takibi"],
  "fark": ("Genelde klasik SEO yapılır ve AI aramaları görmezden gelinir. "
           "Biz sayfaları yapay zekânın alıntılayabileceği şekilde kuruyoruz: "
           "net soru-cevap yapısı, şema ve doğrulanabilir kaynak."),
  "sinir": ("AI yanıtlarında görünürlük garanti edilemez; ölçümü de klasik "
            "sıralama kadar net değil. Ne ölçebildiğimizi baştan söylüyoruz."),
  "kapi": ("görünürlük testi", "Sektörünüzün sorularını yapay zekâya sorup "
           "şu an kimin çıktığını gösteriyoruz."),
  "referans": ("Kendi sitemiz", "şema, soru-cevap yapısı ve şeffaf ölçüm"),
  "gerekli": ["Site adresi", "Sektör ve hedef sorular", "Rakip listesi"],
 },
 "yazilim": {
  "ad": "Yazılım ve otonom sistem",
  "sayfa": "/yazilim.html",
  "band": (60000, 500000),
  "sure": "değişken",
  "anahtar": ["yazılım", "panel", "otomasyon", "sistem", "uygulama", "crm",
              "bot", "entegrasyon", "web sitesi"],
  "kapsam": ["ihtiyaç çözümlemesi", "geliştirme", "kurulum", "eğitim", "bakım"],
  "fark": ("Genelde hazır paket satılır ve iş akışınız pakete uydurulur. "
           "Biz kendi ürünlerimizi yazan bir ekibiz; sizin akışınıza göre "
           "yazıyoruz."),
  "sinir": "Kapsam netleşmeden fiyat vermiyoruz; ilk görüşme kapsam çıkarmak için.",
  "kapi": ("kapsam görüşmesi", "Bir görüşmede ne yapacağını yazılı çıkarıyoruz."),
  "referans": ("Luna Pusula", "kendi geliştirdiğimiz saha/üretim sistemi"),
  "gerekli": ["Mevcut akışın tarifi", "Kullanıcı sayısı", "Entegrasyon ihtiyaçları"],
 },
}


# --------------------------------------------------------------- fiyat etkenleri
# Her etken bandın neresinde durduğumuzu belirliyor. agirlik: 0..1 arası itiş.
ETKEN = [
 ("sure_uzun",  0.25, ["3 dakika", "3 dk", "üç dakika", "4 dakika", "5 dakika",
                       "uzun metraj", "10 dakika"],
  "Süre uzun — sahne sayısı doğrudan artıyor"),
 ("sure_kisa", -0.25, ["30 saniye", "15 saniye", "60 saniye", "1 dakika",
                       "kısa reklam", "bir dakika"],
  "Süre kısa — sahne sayısı sınırlı"),
 ("cok_karakter", 0.18, ["çift", "iki kişi", "aile", "karakterler", "oyuncular",
                         "üç kişi", "kalabalık"],
  "Birden fazla karakter — her biri ayrı kimlik ve ayrı test turu"),
 ("zaman_atlamasi", 0.18, ["farklı yıllar", "yıllara", "çocukluk", "gençlik",
                           "yaş", "geçmiş", "dönem", "eski fotoğraf"],
  "Yıllara yayılan yaş değişimi — her dönem ek test turu"),
 ("cok_mekan", 0.12, ["mekân referans", "mekan referans", "farklı mekan",
                      "farklı mekân", "lokasyon", "birden çok yer"],
  "Mekân çeşitliliği — tek mekânlı işten belirgin farkı var"),
 ("ses_tam", 0.08, ["ses tasarımı", "müzik", "seslendirme", "diyalog",
                    "dublaj", "ortam sesi"],
  "Tam ses tasarımı — sadece hazır müzik değil"),
 ("cok_dil", 0.12, ["çok dilli", "ingilizce", "almanca", "arapça", "iki dil",
                    "yabancı dil"],
  "Çok dilli sürüm"),
 ("acil", 0.15, ["acil", "en kısa sürede", "bu hafta", "yetişmesi", "deadline",
                 "hemen"],
  "Sıkışık takvim — üretim paralelleştiriliyor"),
 ("yuksek_kalite", 0.07, ["sinema", "sinematik", "yüksek kalite", "profesyonel",
                          "reklam kalitesi", "gerçek film"],
  "Sinema düzeyi beklentisi — plan çeşitliliği ve post yükü artıyor"),
 ("hazir_senaryo", -0.08, ["senaryo hazır", "senaryo ve sahne akışı hazır",
                           "sahne akışı hazır", "metin hazır"],
  "Senaryo hazır — yazım aşaması bizde değil"),
 ("hazir_referans", -0.06, ["fotoğrafı mevcut", "fotoğraflar mevcut",
                            "elimde", "referanslar hazır", "görseller mevcut"],
  "Referans malzeme hazır — toplama süresi yok"),
]

# talebin ne kadar ciddi/hazır olduğunu gösteren işaretler
HAZIRLIK = [
 ("Senaryo hazır", ["senaryo hazır", "sahne akışı hazır", "metin hazır"]),
 ("Referans malzeme mevcut", ["fotoğraf", "referans", "görsel", "mevcut"]),
 ("Bütçe sorusu net", ["ne kadar", "fiyat", "maliyet", "bütçe", "tutar"]),
 ("Referans işi görmek istiyor", ["örnek", "referans paylaş", "daha önce yaptığınız",
                                  "çalışma örneği", "portfolyo"]),
 ("Takvim belirtilmiş", ["tarih", "ne zaman", "süre", "teslim", "hafta", "ay"]),
]


def _tespit_hizmet(metin):
    """Metne en çok uyan hizmeti bulur. Döner: (anahtar, skor, eslesen)."""
    k = _kucuk(metin)
    en = (None, 0, [])
    for anahtar, h in HIZMET.items():
        es = [a for a in h["anahtar"] if _kucuk(a) in k]
        # daha uzun anahtar daha güçlü sinyal
        skor = sum(len(a.split()) + 1 for a in es)
        if skor > en[1]:
            en = (anahtar, skor, es)
    return en


def _band_daralt(band, itis):
    """
    Genel bandı, tespit edilen etkenlere göre daraltır.
    itis 0 → bandın alt üçte biri, 1 → üst üçte biri.
    Formül müşteriye gösterilmiyor; gerekçeler gösteriliyor.
    """
    alt, ust = band
    genislik = ust - alt
    orta = alt + genislik * max(0.0, min(1.0, itis))
    yari = genislik * 0.15          # daraltılmış bandın yarı genişliği
    a = max(alt, orta - yari)
    u = min(ust, orta + yari)
    yuvarla = 10000 if genislik > 100000 else 5000
    a = int(round(a / yuvarla) * yuvarla)
    u = int(round(u / yuvarla) * yuvarla)
    if u <= a:
        u = a + yuvarla
    return (a, u)


def coz(metin):
    """
    Gelen talebi çözümler.
    Döner: {hizmet, ad, sayfa, band, daraltilmis, gerekce[], hazirlik[],
            eksik_bilgi[], sinir, kapi, referans}
    """
    anahtar, skor, eslesen = _tespit_hizmet(metin)
    if not anahtar:
        return {"hizmet": None,
                "sorun": "Talebin hangi hizmete ait olduğu anlaşılamadı. "
                         "Hizmeti elle seçip taslağı öyle üretin."}
    h = HIZMET[anahtar]

    # Etkenler doğrusal toplanmıyor: altı kalem işaretlendi diye iş
    # otomatik tavana yapışmasın. Toplam doyuma ulaşarak bandın içinde
    # yer buluyor — üst uç gerçekten istisnai işler için ayrılı kalıyor.
    net, gerekce = 0.0, []
    for ad, agirlik, kelimeler, aciklama in ETKEN:
        if _var(metin, kelimeler):
            net += agirlik
            gerekce.append({"etken": ad, "yon": "+" if agirlik > 0 else "−",
                            "aciklama": aciklama})
    itis = 0.40 + (net / (1.0 + abs(net))) * 0.45
    itis = max(0.05, min(0.95, itis))

    hazirlik = [ad for ad, kelimeler in HAZIRLIK if _var(metin, kelimeler)]
    eksik = [g for g in h["gerekli"]
             if not _var(metin, [g.split("(")[0].split("—")[0].strip()[:12]])]

    return {
        "hizmet": anahtar,
        "ad": h["ad"],
        "sayfa": h["sayfa"],
        "aylik": bool(h.get("aylik")),
        "band": h["band"],
        "daraltilmis": _band_daralt(h["band"], itis),
        "sure": h["sure"],
        "kapsam": h["kapsam"],
        "fark": h["fark"],
        "sinir": h["sinir"],
        "kapi": h["kapi"],
        "referans": h.get("referans"),
        "referans_yok": h.get("referans_yok"),
        "en_yakin": h.get("en_yakin"),
        "gerekli": h["gerekli"],
        "eksik_bilgi": eksik,
        "gerekce": gerekce,
        "hazirlik": hazirlik,
        "eslesen": eslesen,
        "guven": "yüksek" if skor >= 5 else ("orta" if skor >= 3 else "düşük"),
    }


def _tl(n):
    return "{:,}".format(int(n)).replace(",", ".") + " ₺"


def taslak(metin, hizmet=None):
    """
    Gelen talebe hazır yanıt metni üretir (kısa + uzun).
    Döner: {kisa, uzun, cozum}
    """
    c = coz(metin) if not hizmet else None
    if hizmet:
        h = HIZMET.get(hizmet)
        if not h:
            return {"sorun": "Bilinmeyen hizmet: %s" % hizmet}
        c = coz(metin)
        if c.get("hizmet") != hizmet:
            c = coz(metin + " " + h["anahtar"][0])
    if c.get("sorun"):
        return c

    a, u = c["daraltilmis"]
    ba, bu = c["band"]
    ger = [g["aciklama"] for g in c["gerekce"] if g["yon"] == "+"][:3]

    # ---------------------------------------------------------------- kısa
    k = []
    k.append("Merhaba, talebiniz bize net geldi — tam olarak bu işi yapıyoruz.")
    k.append("")
    if c["aylik"]:
        k.append("Tarif ettiğiniz kapsam bizde **aylık %s – %s** bandına oturuyor "
                 "(genel aralığımız %s – %s)." % (_tl(a), _tl(u), _tl(ba), _tl(bu)))
    else:
        k.append("Tarif ettiğiniz iş bizde **%s – %s** bandına oturuyor "
                 "(genel aralığımız %s – %s)." % (_tl(a), _tl(u), _tl(ba), _tl(bu)))
    if ger:
        k.append("Sizi bu aralığa yerleştiren kalemler: " + "; ".join(ger) + ".")
    k.append("Kapsamı gördükten sonra tek rakam ve yazılı kapsam veriyoruz; "
             "kapsam değişmedikçe fiyat değişmiyor. Süre: %s." % c["sure"])
    k.append("")
    if c["referans"]:
        k.append("Referans olarak **%s**: %s." % (c["referans"][0], c["referans"][1]))
    else:
        k.append(c["referans_yok"])
        if c["en_yakin"]:
            k.append("Gösterebileceğimiz en yakın çalışma **%s**: %s." %
                     (c["en_yakin"][0], c["en_yakin"][1]))
    k.append("")
    k.append("Önerim: önce **%s**. %s" % (c["kapi"][0], c["kapi"][1]))
    k.append("")
    k.append("Detaylar: lunayapim.com%s" % c["sayfa"])

    # ---------------------------------------------------------------- uzun
    u_ = []
    u_.append("Merhaba,")
    u_.append("")
    u_.append("Talebiniz bize net geldi. Aşağıda maliyeti, süreci ve "
              "referans sorunuzun dürüst cevabını yazdım.")
    u_.append("")
    u_.append("### Bütçe")
    u_.append("")
    u_.append("%s için genel bandımız **%s – %s**. Sizin tarifiniz "
              "**%s – %s** aralığına oturuyor." %
              (c["ad"], _tl(ba), _tl(bu), _tl(a), _tl(u)))
    if c["gerekce"]:
        u_.append("")
        u_.append("| Kalem | Etkisi |")
        u_.append("|---|---|")
        for g in c["gerekce"]:
            u_.append("| %s | %s |" % (g["yon"], g["aciklama"]))
    u_.append("")
    u_.append("Bu fiyata dahil olanlar: " + ", ".join(c["kapsam"]) + ".")
    u_.append("")
    u_.append("Kapsam netleştikten sonra **tek rakam ve yazılı kapsam** veriyoruz. "
              "Kapsam değişmedikçe fiyat değişmiyor — ara faturayla artan bir "
              "bütçemiz yok. Süre: **%s**." % c["sure"])
    u_.append("")
    u_.append("### Farkımız")
    u_.append("")
    u_.append(c["fark"])
    u_.append("")
    u_.append("**Dürüst sınır:** " + c["sinir"])
    u_.append("")
    u_.append("### Referans sorunuzun cevabı")
    u_.append("")
    if c["referans"]:
        u_.append("**%s** — %s. Tümü lunayapim.com/isler sayfasında." %
                  (c["referans"][0], c["referans"][1]))
    else:
        u_.append(c["referans_yok"])
        if c["en_yakin"]:
            u_.append("")
            u_.append("Gösterebileceğimiz en yakın çalışma **%s**: %s." %
                      (c["en_yakin"][0], c["en_yakin"][1]))
    u_.append("")
    u_.append("Asıl önerim: başkasının işine bakarak karar vermeyin. "
              "Önce **%s** yapalım — %s" % (c["kapi"][0], c["kapi"][1]))
    u_.append("")
    u_.append("### Başlamak için bize gerekenler")
    u_.append("")
    for g in c["gerekli"]:
        u_.append("- " + g)
    u_.append("")
    u_.append("Saygılarımla,")
    u_.append("**Luna Yapım** · Bursa")
    u_.append("0541 160 26 03 · lunayapim.com%s" % c["sayfa"])

    # WhatsApp kalın yazıyı tek yıldızla yapıyor; markdown çift yıldızı
    # orada olduğu gibi görünür. Kısa sürümü WhatsApp yazımına çeviriyoruz.
    kisa = re.sub(r"\*\*(.+?)\*\*", r"*\1*", "\n".join(k))
    return {"cozum": c, "kisa": kisa, "uzun": "\n".join(u_)}


def kaydet(metin, klasor, ad=None):
    """Taslağı dosyaya yazar, yolu döner."""
    import os
    t = taslak(metin)
    if t.get("sorun"):
        return t
    os.makedirs(klasor, exist_ok=True)
    ad = ad or "%s-%s.md" % (t["cozum"]["hizmet"],
                             datetime.date.today().isoformat())
    yol = os.path.join(klasor, ad)
    with open(yol, "w", encoding="utf-8") as f:
        f.write("# %s — hazır yanıt\n\n" % t["cozum"]["ad"])
        f.write("## Gelen talep\n\n> " + metin.replace("\n", "\n> ") + "\n\n---\n\n")
        f.write("## Kısa yanıt (WhatsApp)\n\n" + t["kisa"] + "\n\n---\n\n")
        f.write("## Uzun yanıt (e-posta)\n\n" + t["uzun"] + "\n")
    t["yol"] = yol
    return t


def hizmet_listesi():
    return [{"anahtar": k, "ad": h["ad"], "sayfa": h["sayfa"],
             "band": h["band"], "aylik": bool(h.get("aylik")),
             "referansli": bool(h.get("referans"))}
            for k, h in HIZMET.items()]
