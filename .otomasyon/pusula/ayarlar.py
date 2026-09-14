# -*- coding: utf-8 -*-
"""
Luna Pusula — ayarlar.
Buradaki sayılar VARSAYIMDIR ve değiştirilebilir. Her biri raporda
"varsayım" olarak gösterilir; uydurulmuş kesinlik satmıyoruz.
"""
import os, json

# Yollar paketin bulunduğu klasöre görelidir; nereye kopyalarsan orada çalışır.
KOK_DIZIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AYAR_DOSYA = os.path.join(KOK_DIZIN, "ayarlar.json")


def _ozel_oku():
    try:
        with open(AYAR_DOSYA, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


_OZEL = _ozel_oku()

# ---------------------------------------------------------------- anahtarlar
# Panelden girilen değer önce gelir, sonra ortam değişkeni.
# Google Places API (New) anahtarı. Yoksa OpenStreetMap'e düşer (ücretsiz).
GOOGLE_ANAHTAR = (_OZEL.get("google_anahtar") or os.environ.get("GOOGLE_MAPS_API_KEY", "")).strip()
# PageSpeed Insights anahtarı (opsiyonel; anahtarsız da günde birkaç yüz istek çalışır)
PAGESPEED_ANAHTAR = (_OZEL.get("pagespeed_anahtar") or os.environ.get("PAGESPEED_API_KEY", "")).strip()

# ---------------------------------------------------------------- firma
FIRMA = {
    "ad": "Luna Yapım",
    "telefon": "+905411602603",
    "wa": "905411602603",
    "eposta": _OZEL.get("eposta", ""),
    "site": "https://lunayapim.com",
    "imza": _OZEL.get("imza", "Luna Yapım"),
}
FIRMA.update(_OZEL.get("firma", {}))

# ---------------------------------------------------------------- e-posta gönderimi (isteğe bağlı)
SMTP = {"sunucu": "", "kapi": 587, "kullanici": "", "sifre": "", "gonderen": ""}
SMTP.update(_OZEL.get("smtp", {}))

# ---------------------------------------------------------------- okuma sayacı (site tıklanmaları)
# Cloudflare Pages'te PANEL_ANAHTARI olarak girdiğin değerin aynısı. Panel bununla
# https://lunayapim.com/api/okuma adresinden günlük okuma sayılarını çekiyor.
OKUMA_ANAHTAR = (_OZEL.get("okuma_anahtar") or os.environ.get("LUNA_OKUMA_ANAHTAR", "")).strip()

# ---------------------------------------------------------------- Telegram (isteğe bağlı)
# jeton  : @BotFather'dan alınan bot anahtarı
# sohbet : mesajın gideceği sohbet kimliği (kendi hesabın ya da bir grup)
TELEGRAM = {"jeton": "", "sohbet": "", "sessiz": False}
TELEGRAM.update(_OZEL.get("telegram", {}))
if not TELEGRAM["jeton"]:
    TELEGRAM["jeton"] = os.environ.get("LUNA_TG_JETON", "").strip()
if not TELEGRAM["sohbet"]:
    TELEGRAM["sohbet"] = os.environ.get("LUNA_TG_SOHBET", "").strip()

VT_YOLU   = os.environ.get("PUSULA_DB")    or os.path.join(KOK_DIZIN, "pusula.db")
CIKTI     = os.environ.get("PUSULA_CIKTI") or os.path.join(KOK_DIZIN, "cikti")

# ---------------------------------------------------------------- hedefleme
# Luna Yapım'ın satabildiği hizmetlere göre avlanacak işletme türleri.
SEKTORLER = {
    "insaat": {
        "ad": "İnşaat / Müteahhit",
        "aramalar": ["inşaat firması", "müteahhit", "yapı şirketi", "konut projesi"],
        "osm": ['"office"="construction_company"', '"craft"="builder"'],
        "hizmet": "insaat-3d-modelleme",
        "teklif": "İnşaat 3D modelleme + proje tanıtım animasyonu",
    },
    "emlak": {
        "ad": "Emlak Ofisi",
        "aramalar": ["emlak ofisi", "gayrimenkul danışmanlığı", "emlakçı"],
        "osm": ['"office"="estate_agent"'],
        "hizmet": "emlak-video",
        "teklif": "Emlak video çekimi + portföy paketi",
    },
    "mimarlik": {
        "ad": "Mimarlık Ofisi",
        "aramalar": ["mimarlık ofisi", "mimar", "iç mimarlık"],
        "osm": ['"office"="architect"'],
        "hizmet": "insaat-3d-modelleme",
        "teklif": "Mimari görselleştirme + sunum animasyonu",
    },
    "sanayi": {
        "ad": "Üretici / Sanayi",
        "aramalar": ["makine imalat", "fabrika", "sanayi üretim", "metal işleme"],
        "osm": ['"man_made"="works"', '"industrial"="factory"'],
        "hizmet": "urun-animasyon",
        "teklif": "3D ürün animasyonu + fuar videosu",
    },
    "mobilya": {
        "ad": "Mobilya / Showroom",
        "aramalar": ["mobilya mağazası", "mobilya imalat", "showroom"],
        "osm": ['"shop"="furniture"'],
        "hizmet": "urun-animasyon",
        "teklif": "Ürün 3D vitrin + varyant animasyonu",
    },
    "otel": {
        "ad": "Otel / Turizm Tesisi",
        "aramalar": ["otel", "termal otel", "butik otel", "tatil köyü"],
        "osm": ['"tourism"="hotel"'],
        "hizmet": "emlak-video",
        "teklif": "Tesis tanıtım filmi + drone çekim",
    },
    "isletme": {
        "ad": "Kafe / Restoran / Yerel İşletme",
        "aramalar": ["restoran", "kafe", "güzellik salonu", "spor salonu"],
        "osm": ['"amenity"="restaurant"', '"amenity"="cafe"'],
        "hizmet": "isletme-tanitim",
        "teklif": "Sosyal medya içerik paketi",
    },
}

# ---------------------------------------------------------------- eksik ağırlıkları
# Her eksiğin "görünürlük skoru"ndan düşürdüğü puan (toplam 100).
EKSIK_AGIRLIK = {
    "site_yok":            22,   # hiç web sitesi yok
    "site_bozuk":          18,   # site var ama açılmıyor
    "https_yok":            6,
    "mobil_uyumsuz":        9,
    "yavas":                8,   # PageSpeed mobil < 50
    "baslik_zayif":         5,   # <title> yok/çok kısa/genel
    "aciklama_yok":         4,   # meta description yok
    "sema_yok":             5,   # LocalBusiness JSON-LD yok
    "video_yok":           12,   # sitede veya profilde video yok
    "gorsel_az":            7,   # Google profilinde az fotoğraf
    "yorum_az":             6,   # yorum sayısı düşük
    "puan_dusuk":           4,   # 4.0 altı puan
    "sosyal_yok":           5,   # Instagram/Facebook bağlantısı yok
    "telefon_yok":          3,
    "adres_yok":            2,

    # --- derin katman: dönüşüm (ziyaretçi geldi, ne oldu?)
    "cta_yok":              8,
    "whatsapp_yok":         6,
    "tel_tiklanmaz":        4,
    "form_yok":             4,
    "fiyat_sinyali_yok":    3,
    "harita_link_yok":      2,
    # --- derin katman: güven
    "referans_yok":         7,
    "yorum_gomulu_yok":     4,
    "ekip_yok":             3,
    "belge_yok":            2,
    "iletisim_sayfasi_yok": 3,
    "sss_yok":              2,
    # --- derin katman: içerik
    "icerik_sig":           6,
    "hizmet_sayfasi_yok":   5,
    "blog_yok":             3,
    "gorsel_alt_yok":       2,
    "ic_baglanti_az":       2,
    # --- derin katman: teknik
    "h1_yok":               3,
    "h1_coklu":             1,
    "canonical_yok":        2,
    "og_yok":               3,
    "favicon_yok":          1,
    "dil_etiketi_yok":      1,
    "eski_icerik":          2,
    "robots_yok":           1,
    "sitemap_yok":          2,
    "agir_sayfa":           2,
    # --- sosyal katman
    "sosyal_hicyok":        6,
    "sosyal_site_baglantisi_yok": 2,
}

# ---------------------------------------------------------------- eşikler
ESIK = {
    "gorsel_az":   10,     # Google profilinde bu sayıdan az fotoğraf → eksik
    "yorum_az":    25,     # bu sayıdan az yorum → eksik
    "puan_dusuk":  4.0,
    "pagespeed_yavas": 50,
    "sicak_skor":  65,     # bu skorun ALTINDAKİ işletme = sıcak aday (çok eksiği var)
}

# ---------------------------------------------------------------- kazanç modeli
# TÜMÜ VARSAYIMDIR. Raporda "varsayım" olarak işaretlenir.
# Mantık: eksikler kapandığında yerel arama görünürlüğü ve dönüşüm artar.
MODEL = {
    # aylık organik/harita görüntülenmesi tahmini için taban (yorum sayısına göre ölçekler)
    "goruntulenme_taban": 120,
    "goruntulenme_yorum_carpani": 14,     # her yorum ~ bu kadar aylık görüntülenme sinyali
    "goruntulenme_tavan": 12000,

    # eksik kapatıldığında görüntülenmeye etkisi (çarpan)
    "etki": {
        "site_yok":      1.55,
        "site_bozuk":    1.45,
        "https_yok":     1.04,
        "mobil_uyumsuz": 1.18,
        "yavas":         1.12,
        "baslik_zayif":  1.10,
        "aciklama_yok":  1.05,
        "sema_yok":      1.12,
        "video_yok":     1.25,
        "gorsel_az":     1.15,
        "yorum_az":      1.20,
        "puan_dusuk":    1.08,
        "sosyal_yok":    1.07,
        "telefon_yok":   1.03,
        "adres_yok":     1.02,
    },
    # görüntülenmeden iletişime dönüşüm oranı (mevcut / iyileştirilmiş)
    "donusum_mevcut":    0.018,
    "donusum_iyilesmis": 0.032,
    # iletişimden işe dönüşüm
    "kapanis_orani":     0.18,
    # sektör başına ortalama iş büyüklüğü (TL) — kullanıcı kendi rakamıyla değiştirir
    "ortalama_is": {
        "insaat": 45000, "emlak": 9000, "mimarlik": 30000, "sanayi": 38000,
        "mobilya": 18000, "otel": 25000, "isletme": 7000,
    },
    # toplam çarpan tavanı — modelin abartmasını engeller
    "carpan_tavani": 3.2,
}

ILLER = ["Adana","Adıyaman","Afyonkarahisar","Ağrı","Aksaray","Amasya","Ankara","Antalya","Ardahan",
 "Artvin","Aydın","Balıkesir","Bartın","Batman","Bayburt","Bilecik","Bingöl","Bitlis","Bolu","Burdur",
 "Bursa","Çanakkale","Çankırı","Çorum","Denizli","Diyarbakır","Düzce","Edirne","Elazığ","Erzincan",
 "Erzurum","Eskişehir","Gaziantep","Giresun","Gümüşhane","Hakkari","Hatay","Iğdır","Isparta","İstanbul",
 "İzmir","Kahramanmaraş","Karabük","Karaman","Kars","Kastamonu","Kayseri","Kırıkkale","Kırklareli",
 "Kırşehir","Kilis","Kocaeli","Konya","Kütahya","Malatya","Manisa","Mardin","Mersin","Muğla","Muş",
 "Nevşehir","Niğde","Ordu","Osmaniye","Rize","Sakarya","Samsun","Siirt","Sinop","Sivas","Şanlıurfa",
 "Şırnak","Tekirdağ","Tokat","Trabzon","Tunceli","Uşak","Van","Yalova","Yozgat","Zonguldak"]

# Sitenin yerel klasörü — "hiç görünmeyen sayfa" tespiti için taranıyor.
# Bilinen yerlere bakar; bulamazsa ayarlar.json'daki "site_kok" kullanılır.
def _site_kok_bul():
    adaylar = [
        os.path.expanduser("~/Documents/GitHub/lunayapim"),
        os.path.expanduser("~/GitHub/lunayapim"),
        os.path.expanduser("~/Documents/lunayapim"),
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__)))), "GitHub", "lunayapim"),
    ]
    for a in adaylar:
        if os.path.isfile(os.path.join(a, "sitemap.xml")):
            return a
    return adaylar[0]


SITE_KOK = _site_kok_bul()

KULLANICI_AJANI = "LunaPusula/1.0 (+https://lunayapim.com)"
ISTEK_ZAMAN_ASIMI = 12


# ============================================================
#  Panelden ayar okuma / yazma
# ============================================================
def izinli_epostalar():
    """
    Cloudflare Access arkasından girmesine izin verilen e-posta adresleri.
    Access zaten kapıda duruyor; bu liste ikinci kilit — Access yanlış
    yapılandırılırsa panel yine de herkese açılmasın diye.
    """
    v = _ozel_oku().get("uzak_epostalar") or []
    if isinstance(v, str):
        v = [x.strip() for x in v.replace(";", ",").split(",")]
    return {str(x).strip().lower() for x in v if str(x).strip()}


def ayarlari_getir():
    """Panelin gösterdiği ayar sözlüğü."""
    return {
        "google_anahtar": GOOGLE_ANAHTAR,
        "pagespeed_anahtar": PAGESPEED_ANAHTAR,
        "eposta": FIRMA.get("eposta", ""),
        "imza": FIRMA.get("imza", ""),
        "smtp": dict(SMTP),
        "okuma_anahtar": OKUMA_ANAHTAR,
        "runway_anahtar": (_OZEL.get("runway_anahtar") or ""),
        "yazar_anahtar": (_OZEL.get("yazar_anahtar") or ""),
        "yazar_model": (_OZEL.get("yazar_model") or ""),
        "telegram": {"jeton": TELEGRAM["jeton"], "sohbet": TELEGRAM["sohbet"],
                     "sessiz": TELEGRAM["sessiz"]},
        "esik": dict(ESIK),
        "model": {
            "donusum_mevcut": MODEL["donusum_mevcut"],
            "donusum_iyilesmis": MODEL["donusum_iyilesmis"],
            "kapanis_orani": MODEL["kapanis_orani"],
            "carpan_tavani": MODEL["carpan_tavani"],
            "ortalama_is": dict(MODEL["ortalama_is"]),
        },
        "uzak_epostalar": sorted(izinli_epostalar()),
        "kaynak": "Google Places" if GOOGLE_ANAHTAR else "OpenStreetMap (anahtarsız)",
        "ayar_dosyasi": AYAR_DOSYA,
    }


def ayarlari_kaydet(yeni):
    """Paneldan gelen ayarları ayarlar.json'a yazar ve bellekteki değerleri tazeler."""
    global GOOGLE_ANAHTAR, PAGESPEED_ANAHTAR, _OZEL
    mevcut = _ozel_oku()

    for a in ("google_anahtar", "pagespeed_anahtar", "eposta", "imza", "okuma_anahtar", "runway_anahtar", "yazar_anahtar", "yazar_model"):
        if a in yeni:
            mevcut[a] = (yeni[a] or "").strip()
    if "smtp" in yeni and isinstance(yeni["smtp"], dict):
        m = mevcut.get("smtp", {}); m.update(yeni["smtp"]); mevcut["smtp"] = m
    if "telegram" in yeni and isinstance(yeni["telegram"], dict):
        m = mevcut.get("telegram", {}); m.update(yeni["telegram"]); mevcut["telegram"] = m
    if "x" in yeni and isinstance(yeni["x"], dict):
        m = mevcut.get("x", {}); m.update({k: (v.strip() if isinstance(v, str) else v) for k, v in yeni["x"].items()}); mevcut["x"] = m
    if "esik" in yeni and isinstance(yeni["esik"], dict):
        m = mevcut.get("esik", {}); m.update(yeni["esik"]); mevcut["esik"] = m
    if "model" in yeni and isinstance(yeni["model"], dict):
        m = mevcut.get("model", {}); m.update(yeni["model"]); mevcut["model"] = m
    if "uzak_epostalar" in yeni:
        v = yeni["uzak_epostalar"]
        if isinstance(v, str):
            v = [x.strip() for x in v.replace(";", ",").replace("\n", ",").split(",")]
        mevcut["uzak_epostalar"] = [str(x).strip().lower() for x in (v or []) if str(x).strip()]

    with open(AYAR_DOSYA, "w", encoding="utf-8") as f:
        json.dump(mevcut, f, ensure_ascii=False, indent=2)

    _OZEL = mevcut
    GOOGLE_ANAHTAR = (mevcut.get("google_anahtar") or os.environ.get("GOOGLE_MAPS_API_KEY", "")).strip()
    PAGESPEED_ANAHTAR = (mevcut.get("pagespeed_anahtar") or os.environ.get("PAGESPEED_API_KEY", "")).strip()
    FIRMA["eposta"] = mevcut.get("eposta", FIRMA.get("eposta", ""))
    FIRMA["imza"] = mevcut.get("imza", FIRMA.get("imza", ""))
    SMTP.update(mevcut.get("smtp", {}))
    TELEGRAM.update(mevcut.get("telegram", {}))
    global OKUMA_ANAHTAR
    OKUMA_ANAHTAR = (mevcut.get("okuma_anahtar") or "").strip()
    ESIK.update({k: v for k, v in mevcut.get("esik", {}).items() if k in ESIK})
    for k, v in mevcut.get("model", {}).items():
        if k == "ortalama_is" and isinstance(v, dict):
            MODEL["ortalama_is"].update(v)
        elif k in MODEL:
            MODEL[k] = v
    return ayarlari_getir()


# başlangıçta json'daki eşik/model değerlerini uygula
ESIK.update({k: v for k, v in _OZEL.get("esik", {}).items() if k in ESIK})
for _k, _v in _OZEL.get("model", {}).items():
    if _k == "ortalama_is" and isinstance(_v, dict):
        MODEL["ortalama_is"].update(_v)
    elif _k in MODEL:
        MODEL[_k] = _v
