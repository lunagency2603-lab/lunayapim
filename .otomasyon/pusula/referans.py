# -*- coding: utf-8 -*-
"""
REFERANS KÜTÜĞÜ — Luna Yapım'ın gerçekten yapmış olduğu işler.

Buradaki her kayıt elimizde duran bir çalışmadır. Uydurma proje, uydurma
müşteri, uydurma rakam yok. Müşteriye gösterilen her referans buradan gelir;
teklif, analiz ve sosyal demo aynı kütüğü okur.

Alanlar:
  anahtar   → kod adı
  ad        → işin gösterilen adı
  tur       → ne tür iş (kısa film, reklam, animasyon, klip...)
  ne_yaptik → teknik olarak ne yapıldı (müşterinin "bunu bana da yapar mısın" demesi için)
  neden     → bu iş neyi kanıtlıyor (yetenek iddiası değil, kanıt cümlesi)
  video     → YouTube kimliği (varsa)
  kare      → yerel kare görselinin dosya adı (site/assets/referans altında)
  sektor    → hangi sektörlere gösterilebilir
  vurgu     → o sektörde bu işin öne çıkan tarafı
"""

# ------------------------------------------------------------------ kütük
ISLER = [
    {
        "anahtar": "galzura",
        "ad": "Galzura — Filo ve Personel Yönetimi Tanıtımı",
        "tur": "Ürün / yazılım tanıtım animasyonu",
        "ne_yaptik": "Yazılım arayüzünün ekran kaydı değil, yeniden kurgulanmış animasyonu: "
                     "arayüz elemanları tek tek hareket ediyor, anlatım altyazıyla ilerliyor. "
                     "65 saniye, iki dil (TR/DE), iki format (16:9 ve 9:16).",
        "neden": "Ekranda geçen bir yazılımı, yazılımı hiç görmemiş birine anlatmak en zor iştir. "
                 "Bu iş onun kanıtı: aynı içerik hem yatay hem dikey, hem Türkçe hem Almanca "
                 "çıktı — tek çekimden çok sürüm meselesini biz laf olsun diye söylemiyoruz.",
        "video": "",
        "kare": ["galzura-1.jpg", "galzura-2.jpg", "galzura-3.jpg"],
        "dikey_kare": "galzura-dikey.jpg",
        "sektor": ["sanayi", "isletme", "mobilya", "emlak", "insaat", "mimarlik"],
        "vurgu": {
            "insaat": "Bir projeyi, projeyi hiç görmemiş birine 60 saniyede anlatmak: "
                      "etaplar, kat planı, teslim takvimi. Yazılımda yaptığımız iş buydu, "
                      "konut projesinde de aynısı yapılıyor.",
            "mimarlik": "Sunum videosu tam olarak bu yapıda kuruluyor — anlatım altyazıyla "
                        "ilerliyor, izleyici hiçbir yerde kaybolmuyor.",
            "sanayi": "Makine ve süreç anlatımı da tam olarak bu mantıkla yapılıyor: "
                      "görünmeyeni görünür kılmak.",
            "isletme": "Hizmetinizi anlatan bir video, hizmeti hiç duymamış birine "
                       "60 saniyede anlatabilmeli. Örneği burada.",
            "mobilya": "Ürünün nasıl çalıştığını/açıldığını anlatan animasyon aynı yöntemle çıkıyor.",
            "emlak": "Aynı işin dikey sürümü de teslim edildi — ilan sitesi ve Reels için ayrı çekim yok.",
        },
    },
    {
        "anahtar": "karga",
        "ad": "Karga — Marka Açılış ve 3D Karakter Serisi",
        "tur": "3D modelleme, ışık ve doku çalışması",
        "ne_yaptik": "Tamamen üretilmiş bir sahne: karakter modeli, tüy dokusu, göz içi kırılma, "
                     "kanlı ay arkasında hacimsel ışık. Açılış, geçiş, makro göz, kanat açılışı "
                     "ve kapanış olarak ayrı ayrı kurgulanabilir parçalar hâlinde.",
        "neden": "Bu sahnenin hiçbir yerinde kamera yok — hepsi modellenip ışıklandırıldı. "
                 "Bir binanın, bir dairenin veya bir ürünün 'henüz yokken' fotogerçekçi "
                 "görünmesi tam olarak bu iştir.",
        "video": "",
        "kare": ["karga-acilis.jpg", "karga-goz.jpg", "karga-kanat.jpg", "karga-tuy.jpg"],
        "sektor": ["insaat", "mimarlik", "emlak", "sanayi", "mobilya", "otel", "isletme"],
        "vurgu": {
            "insaat": "Henüz temeli atılmamış bloğun akşam ışığında nasıl görüneceği "
                      "bu teknikle çıkıyor. Render sattığımızı söylemiyoruz, gösteriyoruz.",
            "mimarlik": "Malzeme, doku ve ışık kontrolü burada görülüyor — sunum kalitesinin sınırı bu.",
            "emlak": "Manzara ve saat ışığı simülasyonu aynı motorla yapılıyor.",
            "otel": "Oda ve genel alanların 'akşam hâli' böyle üretiliyor; sezon dışı çekim beklemiyorsunuz.",
            "mobilya": "Ürünün kumaş/ahşap dokusu bu detayda çıkıyor.",
            "sanayi": "Metal, cam ve yansıma çalışması makine görselleştirmesinin temelidir.",
            "isletme": "Marka açılış animasyonunuz da bu kalitede üretilebilir.",
        },
    },
    {"anahtar": "kisa-film", "ad": "Kısa Film", "tur": "Kısa film",
     "ne_yaptik": "Hikâye kurgusu, ışık yönetimi ve oyuncu yönetimiyle çekilmiş kısa film.",
     "neden": "Reklam filmi ile kısa film arasındaki fark ritimdir. Ritmi kuran ekip, "
              "60 saniyelik tanıtımda da izleyiciyi sonuna kadar tutar.",
     "video": "TjUTFk9LZSs", "kare": [], "sektor": ["isletme", "otel", "emlak", "insaat", "mimarlik"],
     "vurgu": {"insaat": "Şantiye çekimi teknik bir iş değil, anlatım işidir. Ritmi kuran ekip, "
                         "iki dakikalık proje tanıtımında izleyiciyi sonuna kadar tutar.",
               "mimarlik": "Mekânı hikâyeyle anlatmak — sunumun ikna eden kısmı burasıdır."}},
    {"anahtar": "sinematografi", "ad": "Sinematografi Çalışması", "tur": "Sinematografi",
     "ne_yaptik": "Kamera hareketi ve renk dili çalışması; gimbal ve klasik kamera bir arada.",
     "neden": "Aynı mekân, kötü çekilince sıradan; doğru çekilince pahalı görünür. "
              "Aradaki fark burada duruyor.",
     "video": "aV6_WSjJcnU", "kare": [],
     "sektor": ["otel", "emlak", "isletme", "mimarlik", "insaat", "mobilya", "sanayi"],
     "vurgu": {"insaat": "Aynı bina, kötü çekilince beton yığını; doğru saatte ve doğru "
                         "hareketle çekilince satılabilir bir proje. Fark bu çalışmada görünüyor.",
               "mobilya": "Ürün çekiminde kamera hareketi ve renk dili aynı yerden geliyor.",
               "sanayi": "Tesis çekiminde ışık ve hareket kontrolü bu çalışmadaki gibi kuruluyor."}},
    {"anahtar": "uretim-reklam", "ad": "Üretim Tesisi Reklam Filmi", "tur": "Reklam filmi",
     "ne_yaptik": "Üretim tesisinde çekim ve kurgu — hat, insan ve ürün aynı filmde.",
     "neden": "Fabrika çekimi zordur: ışık kötü, alan dar, hat durmaz. Bu iş, "
              "çalışan bir tesiste çekim yapabildiğimizin kanıtı.",
     "video": "kRc1KAWI-_o", "kare": [], "sektor": ["sanayi", "mobilya", "isletme", "insaat"],
     "vurgu": {"sanayi": "Üretiminizi durdurmadan çekim yapıyoruz — bu filmde de öyle oldu.",
               "insaat": "Çalışan bir tesiste çekim ile çalışan bir şantiyede çekim aynı iştir: "
                         "iş durmaz, ışık kötüdür, alan tehlikelidir. Bunu yapabildiğimizin kanıtı."}},
    {"anahtar": "siir-klibi", "ad": "Şiir Klibi", "tur": "Klip",
     "ne_yaptik": "Atmosfer ve ritim kurgusu; metin ile görüntünün eşlenmesi.",
     "neden": "Sözü olan işi görüntüyle taşımak — marka hikâyesi anlatımının ta kendisi.",
     "video": "DuMsRUDUYc8", "kare": [], "sektor": ["isletme", "otel"], "vurgu": {}},
    {"anahtar": "kisa-film-klip", "ad": "Kısa Film / Klip", "tur": "Kısa film",
     "ne_yaptik": "Düşük bütçeyle sinematik görüntü: ışık ve yer seçimiyle çözülen prodüksiyon.",
     "neden": "Bütçe küçükse iş kötü olmak zorunda değil. Nerede harcanacağını bilmek yeterli.",
     "video": "CV6kVVBuxxM", "kare": [], "sektor": ["isletme", "emlak"], "vurgu": {}},
    {"anahtar": "dugun-klibi", "ad": "Düğün Klibi", "tur": "Etkinlik",
     "ne_yaptik": "Tek günde çok kameralı çekim ve aynı hafta teslim.",
     "neden": "Tekrarı olmayan bir günü kaçırmadan çekmek, planlama işidir. "
              "Etkinlik ve açılış çekimleri de aynı disiplinle yürüyor.",
     "video": "YGYCJZPC1cA", "kare": [], "sektor": ["otel", "isletme"],
     "vurgu": {"otel": "Otelinizdeki organizasyonlar da aynı çok kameralı düzenle çekiliyor."}},
    {"anahtar": "opener", "ad": "Video Opener", "tur": "Marka açılış animasyonu",
     "ne_yaptik": "Logo ve marka açılış animasyonu — tüm videolarınızın başına giren imza.",
     "neden": "Beş saniyelik açılış, markayı hatırlatan en ucuz tekrardır. Bir kere üretilir, "
              "her videoda çalışır.",
     "video": "itxSC873O_U", "kare": [], "sektor": ["insaat", "emlak", "sanayi", "mobilya",
                                                    "otel", "isletme", "mimarlik"],
     "vurgu": {}},
]


# ------------------------------------------------------------------ sorgular
def sektor_icin(sektor, adet=6):
    """O sektöre gösterilecek referanslar — vurgusu olanlar önce."""
    uygun = [i for i in ISLER if sektor in i["sektor"]]
    uygun.sort(key=lambda i: (0 if i.get("vurgu", {}).get(sektor) else 1,
                              0 if (i["kare"] or i["video"]) else 1))
    if not uygun:
        uygun = [i for i in ISLER if "isletme" in i["sektor"]]
    return uygun[:adet]


def vurgu(is_, sektor):
    """Bu işin o sektördeki öne çıkan tarafı; yoksa genel gerekçe."""
    return (is_.get("vurgu", {}) or {}).get(sektor) or is_["neden"]


def gorsel_url(is_, kok="https://lunayapim.com/assets/referans/"):
    """İlk gösterilecek görselin adresi: yerel kare varsa o, yoksa YouTube kapağı."""
    if is_["kare"]:
        return kok + is_["kare"][0]
    if is_["video"]:
        return "https://i.ytimg.com/vi/%s/hqdefault.jpg" % is_["video"]
    return None


def tum_kareler(is_, kok="https://lunayapim.com/assets/referans/"):
    return [kok + k for k in is_["kare"]]


def baglanti(is_):
    return ("https://www.youtube.com/watch?v=%s" % is_["video"]) if is_["video"] else None


def ozet(sektor):
    """Panelde ve iş emrinde kullanılacak kısa özet."""
    l = sektor_icin(sektor)
    return {"adet": len(l),
            "isler": [{"ad": i["ad"], "tur": i["tur"], "vurgu": vurgu(i, sektor),
                       "gorsel": gorsel_url(i), "baglanti": baglanti(i)} for i in l]}


# ------------------------------------------------------------------ kanıt sayıları
def envanter():
    """Elimizde ne var — abartmadan."""
    videolu = [i for i in ISLER if i["video"]]
    kareli = [i for i in ISLER if i["kare"]]
    return {
        "toplam_is": len(ISLER),
        "yayindaki_video": len(videolu),
        "kare_gorsel": sum(len(i["kare"]) for i in kareli),
        "kapsanan_sektor": sorted({s for i in ISLER for s in i["sektor"]}),
    }
