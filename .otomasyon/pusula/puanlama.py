# -*- coding: utf-8 -*-
"""Görünürlük skoru — 100'den eksiklerin ağırlığı düşülür."""
from .ayarlar import EKSIK_AGIRLIK, ESIK

ETIKET = {
 "site_yok":"Web sitesi yok",
 "site_bozuk":"Site açılmıyor / erişilemiyor",
 "https_yok":"HTTPS (güvenli bağlantı) yok",
 "mobil_uyumsuz":"Mobil uyumlu değil",
 "yavas":"Mobilde yavaş açılıyor",
 "baslik_zayif":"Sayfa başlığı zayıf / genel",
 "aciklama_yok":"Meta açıklama yok",
 "sema_yok":"İşletme şeması (JSON-LD) yok",
 "video_yok":"Hiç video yok",
 "gorsel_az":"Harita profilinde az fotoğraf",
 "yorum_az":"Yorum sayısı düşük",
 "puan_dusuk":"Ortalama puan düşük",
 "sosyal_yok":"Sosyal medya bağlantısı yok",
 "telefon_yok":"Telefon bilgisi eksik",
 "adres_yok":"Adres bilgisi eksik",

 # --- derin katman: dönüşüm
 "cta_yok":"Eylem çağrısı yok (ne yapacağı söylenmiyor)",
 "tel_tiklanmaz":"Telefon tıklanabilir değil",
 "whatsapp_yok":"Sitede WhatsApp butonu yok",
 "form_yok":"İletişim formu yok",
 "harita_link_yok":"Yol tarifi bağlantısı yok",
 "fiyat_sinyali_yok":"Hiçbir fiyat sinyali yok",
 # --- derin katman: güven
 "referans_yok":"Yapılmış iş / referans bölümü yok",
 "yorum_gomulu_yok":"Sitede müşteri yorumu yok",
 "ekip_yok":"Hakkımızda / ekip bölümü yok",
 "belge_yok":"Sertifika, üyelik veya ödül gösterilmemiş",
 "iletisim_sayfasi_yok":"Ayrı iletişim sayfası yok",
 "sss_yok":"Sık sorulan sorular yok",
 # --- derin katman: içerik
 "icerik_sig":"Ana sayfa içeriği çok sığ",
 "hizmet_sayfasi_yok":"Hizmetlerin ayrı sayfası yok",
 "blog_yok":"Blog / taze içerik yok",
 "gorsel_alt_yok":"Görsellerde alt metni yok",
 "ic_baglanti_az":"İç bağlantı çok az",
 # --- derin katman: teknik
 "h1_yok":"Ana başlık (H1) yok",
 "h1_coklu":"Birden fazla H1",
 "canonical_yok":"Canonical etiketi yok",
 "og_yok":"Paylaşım kartı (Open Graph) yok",
 "favicon_yok":"Favicon yok",
 "dil_etiketi_yok":"Dil etiketi yok",
 "eski_icerik":"Telif yılı eski — site terk edilmiş görünüyor",
 "robots_yok":"robots.txt yok",
 "sitemap_yok":"Site haritası yok",
 "agir_sayfa":"Ana sayfa çok ağır",
 # --- sosyal katman (sosyal.py üretir)
 "sosyal_hicyok":"Hiç sosyal medya hesabı yok",
 "sosyal_site_baglantisi_yok":"Hesaplar var, siteden bağlantı verilmemiş",
}

COZUM = {
 "site_yok":"Tek sayfalık hızlı tanıtım sitesi + iletişim akışı",
 "site_bozuk":"Siteyi ayağa kaldırma veya yenisiyle değiştirme",
 "https_yok":"SSL sertifikası ve yönlendirme kurulumu",
 "mobil_uyumsuz":"Mobil öncelikli yeniden düzen",
 "yavas":"Görsel/kod optimizasyonu, önbellek",
 "baslik_zayif":"Aramaya uygun başlık ve sayfa yapısı",
 "aciklama_yok":"Her sayfaya özgün meta açıklama",
 "sema_yok":"LocalBusiness JSON-LD şeması",
 "video_yok":"Tanıtım videosu / 3D animasyon üretimi",
 "gorsel_az":"Profesyonel fotoğraf çekimi ve profile yükleme",
 "yorum_az":"Yorum toplama akışı (QR, SMS, karekod masa kartı)",
 "puan_dusuk":"Yorum yanıtlama ve memnuniyet akışı",
 "sosyal_yok":"Sosyal hesap açılışı + düzenli içerik",
 "telefon_yok":"Harita profilinde iletişim tamamlama",
 "adres_yok":"Harita profilinde adres tamamlama",

 "cta_yok":"Her sayfaya tek ve net bir eylem çağrısı; video sonunda da aynı çağrı",
 "tel_tiklanmaz":"Numarayı tel: bağlantısına çevirme + sabit arama butonu",
 "whatsapp_yok":"Hazır mesajla açılan WhatsApp butonu (mobilde sabit)",
 "form_yok":"Kısa iletişim formu — 3 alan, mesai dışı talep yakalar",
 "harita_link_yok":"Yol tarifi butonu ve gömülü harita",
 "fiyat_sinyali_yok":"Paket/aralık sayfası — bütçe elemesi ziyaretçide olsun",
 "referans_yok":"Referans galerisi: proje videosu + öncesi/sonrası + künye",
 "yorum_gomulu_yok":"Müşteri görüşü çekimi (30 sn video) + siteye yerleştirme",
 "ekip_yok":"Ekip portre çekimi + hakkımızda sayfası",
 "belge_yok":"Belge/sertifika görselleştirme ve güven şeridi",
 "iletisim_sayfasi_yok":"İletişim sayfası + LocalBusiness şeması + harita",
 "sss_yok":"SSS bölümü + FAQPage şeması (aramada soru kutusuna çıkar)",
 "icerik_sig":"Hizmet anlatım metinleri ve sayfa mimarisi",
 "hizmet_sayfasi_yok":"Her hizmete ayrı sayfa + kendi videosu",
 "blog_yok":"Aylık içerik takvimi — yazı + görsel + kısa video",
 "gorsel_alt_yok":"Tüm görsellere açıklayıcı alt metni",
 "ic_baglanti_az":"İç bağlantı mimarisi ve gezinme düzeni",
 "h1_yok":"Sayfa başlık hiyerarşisi kurulumu",
 "h1_coklu":"Başlık hiyerarşisini tekilleştirme",
 "canonical_yok":"Canonical ve yönlendirme düzeni",
 "og_yok":"Paylaşım kartı görseli + OG/Twitter etiketleri",
 "favicon_yok":"Favicon seti (32/180/192/512)",
 "dil_etiketi_yok":"Dil ve karakter kümesi etiketleri",
 "eski_icerik":"İçerik tazeleme ve düzenli güncelleme akışı",
 "robots_yok":"robots.txt ve tarama yönergeleri",
 "sitemap_yok":"Otomatik güncellenen sitemap.xml",
 "agir_sayfa":"Görsel/kod optimizasyonu ve önbellek",
 "sosyal_hicyok":"Sosyal hesap kurulumu + ilk ay içerik üretimi",
 "sosyal_site_baglantisi_yok":"Site–sosyal bağlantı ve sameAs şeması",
}

# Luna Yapım'ın hangi eksiği doğrudan çözebildiği
BIZIM_ISIMIZ = {"video_yok","gorsel_az","site_yok","site_bozuk","mobil_uyumsuz",
                "yavas","baslik_zayif","aciklama_yok","sema_yok","sosyal_yok",
                "cta_yok","tel_tiklanmaz","whatsapp_yok","form_yok","harita_link_yok",
                "fiyat_sinyali_yok","referans_yok","yorum_gomulu_yok","ekip_yok",
                "belge_yok","iletisim_sayfasi_yok","sss_yok","icerik_sig",
                "hizmet_sayfasi_yok","blog_yok","gorsel_alt_yok","ic_baglanti_az",
                "h1_yok","h1_coklu","canonical_yok","og_yok","favicon_yok",
                "dil_etiketi_yok","eski_icerik","robots_yok","sitemap_yok","agir_sayfa",
                "sosyal_hicyok","sosyal_site_baglantisi_yok"}

# Eksikleri konu başlığına göre gruplar — analiz ve teklifte bölüm bölüm gösterilir
GRUP = {
 "donusum": ("Ziyaretçi ne yapacağını biliyor mu",
   ["cta_yok","tel_tiklanmaz","whatsapp_yok","form_yok","harita_link_yok",
    "fiyat_sinyali_yok","telefon_yok","adres_yok"]),
 "guven": ("Bu firmaya güvenilir mi",
   ["referans_yok","yorum_gomulu_yok","ekip_yok","belge_yok","iletisim_sayfasi_yok",
    "yorum_az","puan_dusuk"]),
 "gorunurluk": ("Arandığında bulunuyor mu",
   ["site_yok","site_bozuk","baslik_zayif","aciklama_yok","sema_yok","sss_yok",
    "icerik_sig","hizmet_sayfasi_yok","blog_yok","ic_baglanti_az","canonical_yok",
    "sitemap_yok","robots_yok","gorsel_alt_yok","dil_etiketi_yok"]),
 "gorsel": ("Gördüğünde ikna oluyor mu",
   ["video_yok","gorsel_az","og_yok","favicon_yok","sosyal_yok","sosyal_hicyok",
    "sosyal_site_baglantisi_yok"]),
 "teknik": ("Teknik altyapı",
   ["https_yok","mobil_uyumsuz","yavas","h1_yok","h1_coklu","agir_sayfa","eski_icerik"]),
}


# Cümle içinde kullanılabilir kısa ad (başlık soru cümlesi olduğu için ayrı tutuluyor)
GRUP_KISA = {
 "donusum": "ziyaretçiyi müşteriye çevirme",
 "guven": "güven verme",
 "gorunurluk": "aramada bulunma",
 "gorsel": "görsel anlatım",
 "teknik": "teknik altyapı",
}


def grupla(eksikler):
    """Eksikleri konu başlıklarına ayırır; hiçbir gruba girmeyenler 'diger'e düşer."""
    kalan = list(eksikler)
    cikti = []
    for anahtar, (baslik, kodlar) in GRUP.items():
        icinde = [k for k in eksikler if k in kodlar]
        if icinde:
            cikti.append({"anahtar": anahtar, "baslik": baslik, "kodlar": icinde})
            kalan = [k for k in kalan if k not in icinde]
    if kalan:
        cikti.append({"anahtar": "diger", "baslik": "Diğer", "kodlar": kalan})
    return cikti

# Grubun genel skordaki ağırlığı (toplamı 1.0). Para nerede kaybediliyorsa orası ağır.
GRUP_AGIRLIK = {"donusum": .28, "guven": .22, "gorunurluk": .24, "gorsel": .16, "teknik": .10}

# Site hiç yoksa/açılmıyorsa site'ye bağlı gruplar ölçülemez — sıfır sayılır.
SITE_BAGIMLI = ("donusum", "guven", "gorunurluk", "teknik")


def karne(eksikler):
    """
    Grup grup not verir. Döner: {grup: {baslik, skor, kayip, azami, kodlar}}
    Skor = 100 - o gruptaki eksiklerin ağırlık payı. Böylece kontrol sayısı
    arttıkça skor çökmüyor; her grup kendi içinde ölçülüyor.
    """
    e = set(eksikler)
    sitesiz = bool(e & {"site_yok", "site_bozuk"})
    cikti = {}
    for anahtar, (baslik, kodlar) in GRUP.items():
        azami = sum(EKSIK_AGIRLIK.get(k, 0) for k in kodlar) or 1
        kayip = sum(EKSIK_AGIRLIK.get(k, 0) for k in kodlar if k in e)
        not_ = None
        if sitesiz and anahtar in SITE_BAGIMLI:
            oran = 1.0
            not_ = ("Site olmadığı için bu başlık ölçülemedi — sıfır sayılıyor"
                    if "site_yok" in e else
                    "Site açılmadığı için bu başlık ölçülemedi — sıfır sayılıyor")
        else:
            oran = min(1.0, kayip / float(azami))
        cikti[anahtar] = {"baslik": baslik, "kisa": GRUP_KISA.get(anahtar, baslik),
                          "skor": int(round(100 * (1 - oran))),
                          "kayip": kayip, "azami": azami, "not": not_,
                          "olculemedi": bool(not_),
                          "kodlar": [k for k in kodlar if k in e]}
    return cikti


def skorla(eksikler):
    """Genel görünürlük skoru (0-100) — grup notlarının ağırlıklı ortalaması."""
    k = karne(eksikler)
    toplam = sum(GRUP_AGIRLIK.values()) or 1
    return int(round(sum(k[g]["skor"] * a for g, a in GRUP_AGIRLIK.items()) / toplam))


def en_zayif_grup(eksikler):
    """Konuşmaya nereden başlanacağını söyler."""
    k = karne(eksikler)
    g = min(k.items(), key=lambda x: x[1]["skor"])
    return {"anahtar": g[0], **g[1]}


def sicak_mi(skor):
    return skor < ESIK["sicak_skor"]

def oncelikli_eksikler(eksikler, adet=5):
    """Ağırlığa göre en çok puan kaybettiren eksikler."""
    return sorted(eksikler, key=lambda k: -EKSIK_AGIRLIK.get(k, 0))[:adet]

def bizim_eksikler(eksikler):
    return [k for k in eksikler if k in BIZIM_ISIMIZ]
