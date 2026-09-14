# -*- coding: utf-8 -*-
"""
SİTE SAĞLIĞI — kategori kırılımlı SEO denetimi ve günlük takip.

seo/denetci.py tüm siteyi tek sayı olarak ölçüyordu. Bu katman aynı denetimi
BÖLÜM BÖLÜM çalıştırıyor (ana sayfalar, hizmetler, şehir sayfaları, blog),
sonucu tarihe yazıyor ve zaman içindeki değişimi gösteriyor.

Böylece "sitemiz iyi mi" sorusu yerine "hangi bölüm iyi, hangisi geriliyor"
sorusunu cevaplayabiliyoruz — ve şeffaflık sayfası bu ölçümden besleniyor.
"""
import os, sys, re, json, datetime, importlib.util

from .ayarlar import SITE_KOK, CIKTI


KATEGORI = [
 ("ana",      "Ana sayfalar",   lambda y: "/" not in y.strip("/")),
 ("hizmet",   "Hizmet sayfaları", lambda y: y.startswith("/hizmetler/")),
 ("sehir",    "Şehir sayfaları",  lambda y: y.startswith("/sehir/")),
 ("blog",     "Blog",             lambda y: y.startswith("/blog/")),
]


def _denetci():
    """seo/denetci.py'yi modül olarak yükler."""
    kok = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    yol = os.path.join(kok, "seo", "denetci.py")
    if not os.path.isfile(yol):
        return None
    spec = importlib.util.spec_from_file_location("_denetci", yol)
    m = importlib.util.module_from_spec(spec)
    eski = os.getcwd()
    try:
        os.chdir(os.path.dirname(yol))
        spec.loader.exec_module(m)
    finally:
        os.chdir(eski)
    return m


def _kategori(yol):
    y = "/" + yol.lstrip("/")
    for anahtar, _ad, kural in KATEGORI:
        try:
            if kural(y):
                return anahtar
        except Exception:
            pass
    return "diger"


def olc():
    """
    Tüm siteyi denetler, kategori kırılımı çıkarır.
    Döner: {zaman, sayfa, hata, uyari, oran, kategori:[...], kod:[...]}
    """
    d = _denetci()
    if not d:
        return {"sorun": "seo/denetci.py bulunamadı."}
    sl, bulgu, genel = d.denetle()
    hata, uyari, kod = d.ozet(sl, bulgu, genel)

    # kategori bazında topla
    kat = {}
    for f in sl:
        rel = os.path.relpath(f, SITE_KOK) if os.path.isabs(str(f)) else str(f)
        k = _kategori(rel.replace(os.sep, "/"))
        c = kat.setdefault(k, {"sayfa": 0, "hata": 0, "uyari": 0, "ornek": []})
        c["sayfa"] += 1
        for s, kod_, mesaj in bulgu.get(f, []):
            if s.upper().startswith("HATA"):
                c["hata"] += 1
            else:
                c["uyari"] += 1
            if len(c["ornek"]) < 4:
                c["ornek"].append({"sayfa": rel, "tur": s, "kod": kod_, "mesaj": mesaj})

    kategori = []
    ad_map = {a: ad for a, ad, _ in KATEGORI}
    ad_map["diger"] = "Diğer"
    for anahtar, c in kat.items():
        n = c["sayfa"] or 1
        oran = 100.0 if (c["hata"] == 0 and c["uyari"] == 0) else max(
            0.0, 100 - (c["hata"] * 100.0 / n) - (c["uyari"] * 25.0 / n))
        kategori.append({"anahtar": anahtar, "ad": ad_map.get(anahtar, anahtar),
                         "sayfa": c["sayfa"], "hata": c["hata"], "uyari": c["uyari"],
                         "oran": round(oran, 1), "ornek": c["ornek"]})
    kategori.sort(key=lambda x: -x["sayfa"])

    n = len(sl) or 1
    oran = 100.0 if (hata == 0 and uyari == 0) else max(
        0.0, 100 - (hata * 100.0 / n) - (uyari * 25.0 / n))

    return {
        "zaman": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
        "tarih": datetime.date.today().isoformat(),
        "sayfa": len(sl), "hata": hata, "uyari": uyari, "oran": round(oran, 1),
        "kategori": kategori,
        "kod": [{"tur": s, "kod": k, "adet": v} for (s, k), v in
                sorted(kod.items(), key=lambda x: -x[1])][:20],
        "kontrol_sayisi": 20,
    }


# ------------------------------------------------------------------ günlük kayıt
def _defter():
    return os.path.join(CIKTI, "saglik-gunlugu.json")


def gunluk_oku():
    y = _defter()
    if not os.path.isfile(y):
        return []
    try:
        with open(y, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def gunluk_yaz(kayit):
    """Günde bir kayıt tutuyor; aynı gün tekrar ölçülürse üzerine yazıyor."""
    g = [x for x in gunluk_oku() if x.get("tarih") != kayit["tarih"]]
    g.append({k: kayit[k] for k in ("tarih", "zaman", "sayfa", "hata", "uyari", "oran")}
             | {"kategori": [{kk: k2[kk] for kk in ("anahtar", "ad", "sayfa", "hata", "uyari", "oran")}
                             for k2 in kayit["kategori"]]})
    g.sort(key=lambda x: x["tarih"])
    g = g[-180:]
    os.makedirs(os.path.dirname(_defter()), exist_ok=True)
    with open(_defter(), "w", encoding="utf-8") as f:
        json.dump(g, f, ensure_ascii=False, indent=1)
    return g


def olc_ve_kaydet():
    r = olc()
    if r.get("sorun"):
        return r
    gecmis = gunluk_yaz(r)
    r["gecmis"] = gecmis[-30:]
    if len(gecmis) >= 2:
        onceki = gecmis[-2]
        r["degisim"] = {
            "oran": round(r["oran"] - onceki["oran"], 1),
            "sayfa": r["sayfa"] - onceki["sayfa"],
            "hata": r["hata"] - onceki["hata"],
            "uyari": r["uyari"] - onceki["uyari"],
            "onceki_tarih": onceki["tarih"],
        }
    return r


# ------------------------------------------------------------------ şeffaflık verisi
# Kendi sitemizde bulup düzelttiğimiz eksikler. Elle tutulan bir defter —
# her madde gerçekten yapılmış bir iş.
GUNLUK_KAYIT = [
 ("Sitede hiç sosyal medya bağlantısı yoktu",
  "assets/sosyal.js eklendi: alt bilgi, iletişim sayfası ve JSON-LD sameAs alanı", "25.08.2026"),
 ("JSON-LD şemasında sameAs alanı yoktu",
  "Sosyal hesaplar şemaya bağlanacak şekilde kuruldu", "25.08.2026"),
 ("İletişim formu yoktu — mesai dışı talep kayboluyordu",
  "Statik HTML form eklendi; WhatsApp ve e-postaya tek mesaj olarak gidiyor", "25.08.2026"),
 ("İç sayfaların stil tanımları eksikti, sayfalar biçimsiz açılıyordu",
  "assets/luna.css tamamlandı (page-hero, crumbs, lede, prose ve tablo stilleri)", "25.08.2026"),
 ("385 SEO uyarısı vardı (başlık uzunluğu, meta açıklama, şema, ince içerik)",
  "Tamamı giderildi; başlıklar kısaltıldı, açıklamalar yazıldı, şemalar eklendi", "25.08.2026"),
 ("Analiz raporlarında charset etiketi yoktu; Türkçe karakterler bozuk gidiyordu",
  "Doctype, charset ve body etiketleri eklendi", "26.08.2026"),
 ("Sitede analitik yoktu — sadece reklam dönüşüm etiketi vardı",
  "assets/olcum.js eklendi; GA4/Cloudflare ve buton tıklama olayları", "26.08.2026"),
 ("PROJE_DURUM.md ve README.md yayına açıktı",
  "robots.txt ile tarama dışı bırakıldı", "26.08.2026"),
 ("Fiyat sayfası yoktu; ziyaretçi bütçe elemesi yapamıyordu",
  "fiyatlar.html eklendi: aralıklar, fiyatı ne belirlediği ve neyi kısmadığımız", "26.08.2026"),
 ("Ölçüm kodu iki kez yükleniyordu (reklam etiketi zaten yüklüyordu)",
  "Tek yüklemeye indirildi — 331 sayfada gereksiz bir dosya inişi kalktı", "30.08.2026"),
 ("Sosyal hesapları şemaya bağlayan kod iç içe şemayı göremiyordu; "
  "81 şehir sayfasında 'bu hesaplar bize ait' bilgisi hiç eklenmiyordu",
  "Şema ağacı baştan sona geziliyor; harita bağlantısı da aynı yoldan ekleniyor", "30.08.2026"),
 ("Sosyal bağlantı şeridi 331 sayfanın sadece 14'ünde vardı",
  "316 sayfaya eklendi; sayfa üreticisi de aynı şekilde güncellendi", "30.08.2026"),
 ("Ana sayfa kendini yalnızca Organization olarak tanıtıyordu — yerel arama sinyali yoktu",
  "ProfessionalService tipine geçildi, hizmet verilen iller şemaya yazıldı", "30.08.2026"),
 ("Sitede hiçbir e-posta bağlantısı yoktu; sadece WhatsApp ve telefon vardı",
  "330 sayfanın alt bilgisine, iletişim sayfasına ve şemaya e-posta eklendi", "31.08.2026"),
 ("Google site haritamızı 5 Temmuz'dan beri okumamıştı; 331 sayfanın sadece 24'ünü biliyordu",
  "Site haritası yeniden gönderildi, aynı gün okundu — keşfedilen sayfa 24'ten 331'e çıktı",
  "31.08.2026"),
 ("Google'ın hangi sayfamızı neden dizine almadığına sadece elle bakılıyordu",
  "İndeks denetimi günlük kontrole eklendi (pusula/indeks.py): canonical, .html'e giden "
  "iç bağlantı, karşılığı olmayan /api/ adresi, site haritası ↔ dosya eşleşmesi ve "
  "haritadaki noindex her turda taranıyor; Search Console okumaları tarihli deftere yazılıyor",
  "14.09.2026"),
 ("376 sayfadaki menü bağlantısı hâlâ eski uzantılı adrese gidiyordu "
  "(index.html#urunler gibi, toplam 421 bağlantı); her tıklama ve her tarama "
  "önce yönlendirmeye düşüyordu — Google bu adresleri 'yönlendirilmiş' diye dizin dışı tutuyor",
  "Bağlantılar doğrudan hedefe çevrildi; üretici de çapa/sorgu ekli adresleri "
  "artık uzantısız basıyor — site içinde .html'e giden tek bağlantı kalmadı", "14.09.2026"),
 ("Menüdeki 'İller' bağlantısı 12 sayfada kendi klasörünü gösteriyordu "
  "(blog sayfalarında /blog/, fiyat ve şeffaflık sayfasında ana sayfa)",
  "12 sayfada /sehir/ adresine çevrildi, ortak kabuk da düzeltildi", "14.09.2026"),
 ("Sitede karşılığı olmayan /api/ adresleri sayfa koduna gömülüydü; Google bunları "
  "adres sanıp tarıyordu (36 hayalet adres dizin raporuna düştü)",
  "robots.txt /api/ dizinini taramaya kapattı; denetim artık karşılıksız her /api/ "
  "adresini robots kaydıyla birlikte kontrol ediyor", "14.09.2026"),
]


# Aramada nerede olduğumuz. Search Console'dan ELLE okunan, tarihli ölçümler —
# otomatik çekilemiyor, o yüzden her satırın yanında okunduğu tarih yazıyor.
# Rakamı güzelleştirmiyoruz; başlangıç neyse o yazıyor.
ARAMA_KANIT = {
 "tarih": "14.09.2026",
 "kaynak": "Google Search Console (sc-domain:lunayapim.com)",
 "satir": [
   ("Site haritasındaki sayfa", "460", "hepsinin dosyası yerinde"),
   ("Google'ın dizinine girmiş sayfa", "266", "31.08'de 27'ydi"),
   ("Dizine girmemiş adres", "398", "225'i eski/otomatik adres, 173'ü gerçek sayfa"),
   ("Taranmayı bekleyen sayfa", "156", "keşfedildi ama henüz taranmadı"),
 ],
 "not": ("Rakamları düzeltmiyoruz. İki haftada dizindeki sayfa 27'den 266'ya çıktı. "
         "Dizine girmemiş 398 adresin 187'si sitenin eski uzantılı adresleri (yeni temiz "
         "adrese yönleniyor, olması gereken bu), 38'i robots ile kapattığımız yönetim/servis "
         "adresleri. Geriye kalan asıl darboğaz: 156 sayfayı Google biliyor ama henüz "
         "taramadı. Bu bizim düzeltebileceğimiz bir hata değil; tarama sırası, sayfa yaşı "
         "ve dışarıdan gelen bağlantı sayısıyla ilgili. Haftalık takip ediyoruz."),
}


ACIK_EKSIK = [
 "Müşteri sözleri henüz yayında değil — yazılı onay alınan görüşler eklenecek "
 "(uydurma yorum koymuyoruz, bu yüzden bölüm şu an gizli).",
 "Harita profilinde fotoğraf sayımız az; profesyonel çekim planlandı.",
 "Yol tarifi bağlantısı eklenmedi — Google Haritalar işletme kaydı sürüyor.",
 "156 sayfamızı Google keşfetti ama henüz taramadı; 17 sayfa tarandı ve dizine "
 "alınmadı. Teknik engel yok (14.09 denetimi: 0 hata) — sayfa yaşı ve dış bağlantı "
 "azlığı. Haftalık ölçüp bu sayfada yazıyoruz.",
 "Sitenin eski uzantılı adresleri (187 adet .html) hâlâ Google'ın dizin raporunda "
 "'yönlendirilmiş' görünüyor. Yönlendirme doğru çalışıyor, zamanla listeden düşecek; "
 "doğrulama istemiyoruz çünkü düzeltilecek bir hata değil.",
 "Sosyal medya hesaplarımız henüz açık değil — kullanıcı adları belirlenince "
 "site bağlantıları ve şema otomatik devreye giriyor.",
]


def seffaflik_verisi():
    """Şeffaflık sayfasını besleyen ölçüm + defter."""
    r = olc()
    if r.get("sorun"):
        return r
    return {
        "zaman": r["zaman"],
        "kontrol_sayisi": r["kontrol_sayisi"],
        "kutular": [
            ("Yayındaki sayfa", "{:,}".format(r["sayfa"]).replace(",", "."), "denetimden geçen"),
            ("SEO uygunluk", "%%%s" % r["oran"], "kendi denetçimizle ölçüldü"),
            ("Hata", str(r["hata"]), "engelleyici bulgu"),
            ("Uyarı", str(r["uyari"]), "iyileştirme fırsatı"),
        ],
        "kategori": r["kategori"],
        "gunluk": GUNLUK_KAYIT,
        "acik_eksik": ACIK_EKSIK,
        "arama": ARAMA_KANIT,
    }
