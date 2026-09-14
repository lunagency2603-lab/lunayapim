# -*- coding: utf-8 -*-
"""
ARAMA GÜNDEMİ — insanların gerçekten ne arattığını günlük derler.

Neden bu iki kaynak: ikisi de anahtarsız, ücretsiz ve kalıcı.

  1) Google otomatik tamamlama
     Arama kutusuna bir kelime yazan insanın gördüğü öneri listesi. Bu liste
     tahmin değil, o kelimeyle başlayan aramaların gerçek sıklık sırası.
     Tohum kelimeyi soru ekleri ve harflerle genişletince tek bir hizmetten
     yüzlerce gerçek sorgu çıkıyor.

  2) Google Trends günlük RSS
     O gün Türkiye'de yükselen aramalar. Gündemi buradan okuyoruz.

Toplanan her sorgu kendi hizmet sözlüğümüzle puanlanıyor; bize değmeyen
atılıyor. Amaç trend kovalamak değil, bizim gerçekten cevap verebileceğimiz
soruyu bulmak.

İnternet gerektirir — panel kendi makinende çalıştığı için orada sorun olmaz.
"""
import json, os, re, html, datetime, urllib.parse
import xml.etree.ElementTree as ET

from .kaynaklar.agir import getir
from . import ayarlar

TAMAMLA = ("https://suggestqueries.google.com/complete/search"
           "?client=firefox&hl=tr&gl=tr&q=%s")
TRENDS = "https://trends.google.com/trending/rss?geo=%s"

VERI_KLASOR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "veri", "sorgular")

# --------------------------------------------------------------- tohum kelimeler
# (tohum, hizmet sayfası, kısa etiket)
TOHUMLAR = [
 ("3d modelleme",            "hizmetler/insaat-3d-modelleme", "3D Modelleme"),
 ("mimari render",           "hizmetler/insaat-3d-modelleme", "3D Modelleme"),
 ("konut projesi tanıtım",   "hizmetler/insaat-3d-modelleme", "3D Modelleme"),
 ("3d ürün animasyonu",      "hizmetler/urun-animasyon",      "Ürün Animasyonu"),
 ("makine tanıtım videosu",  "hizmetler/urun-animasyon",      "Ürün Animasyonu"),
 ("emlak videosu",           "hizmetler/emlak-kurumsal",      "Emlak ve Kurumsal"),
 ("tanıtım filmi",           "hizmetler/emlak-kurumsal",      "Emlak ve Kurumsal"),
 ("drone çekim",             "hizmetler/drone-fpv",           "Drone ve FPV"),
 ("fpv drone video",         "hizmetler/drone-fpv",           "Drone ve FPV"),
 ("düğün videosu",           "hizmetler/dugun-etkinlik",      "Düğün ve Etkinlik"),
 ("klip çekimi",             "hizmetler/klip-cekimi",         "Klip Çekimi"),
 ("reklam filmi",            "hizmetler/isletme-tanitim",     "İşletme Tanıtım"),
 ("sosyal medya videosu",    "hizmetler/isletme-tanitim",     "İşletme Tanıtım"),
 ("yapay zeka video",        "hizmetler/ai-kisa-film",        "Yapay Zekâ Kısa Film"),
 ("yapay zeka reklam",       "hizmetler/ai-kisa-film",        "Yapay Zekâ Kısa Film"),
 ("seo nedir",               "hizmetler/seo-icerik",          "SEO ve İçerik"),
 ("yapay zeka seo",          "hizmetler/yapay-zeka-seo",      "Yapay Zekâ ve Arama"),
 ("chatgpt arama",           "hizmetler/yapay-zeka-seo",      "Yapay Zekâ ve Arama"),
]

# Tohumu genişleten ekler. Soru ekleri niyet taşır, harfler kuyruğu açar.
EKLER = ["", " nasıl", " ne kadar", " fiyat", " fiyatları", " nedir", " en iyi",
         " hangi", " neden", " örnek", " ücretsiz", " programı", " firması",
         " bursa", " istanbul", " a", " b", " f", " k", " m", " s", " y"]

# Sorgunun bize değip değmediğini ölçen sözlük (gundem.py ile aynı mantık).
DEGER = {
 3: ("3d", "render", "görselleştirme", "animasyon", "maket", "tanıtım filmi",
     "drone", "fpv", "klip", "sanal tur", "prodüksiyon", "reklam filmi",
     "video çekim", "montaj", "kurgu", "storyboard"),
 2: ("video", "görsel", "proje", "konut", "daire", "ilan", "portföy", "fuar",
     "tanıtım", "pazarlama", "marka", "sosyal medya", "instagram", "reels",
     "yapay zeka", "kentsel dönüşüm", "showroom", "katalog", "web sitesi",
     "seo", "arama", "chatgpt", "içerik", "düğün", "etkinlik"),
 1: ("inşaat", "emlak", "gayrimenkul", "sanayi", "üretim", "turizm", "mobilya",
     "müteahhit", "yatırım", "işletme", "esnaf", "bursa", "fiyat", "ücret",
     "firma", "ajans", "stüdyo"),
}
# Bunlar geçiyorsa iş sorgusu değil — eliyoruz.
ELEME = ("indir", "torrent", "crack", "apk", "bedava izle", "full izle", "hile",
         "porn", "bahis", "iddaa", "casino", "kumar", "hd izle", "dizi izle")

TR_KUCUK = str.maketrans({"İ": "i", "I": "ı", "Ğ": "ğ", "Ü": "ü", "Ş": "ş",
                          "Ö": "ö", "Ç": "ç"})


def _kucuk(x):
    return (x or "").translate(TR_KUCUK).lower()


def _temiz(x):
    return re.sub(r"\s+", " ", html.unescape(x or "")).strip()


# --------------------------------------------------------------- kaynaklar
def oneriler(tohum):
    """Bir kelime için Google'ın önerdiği aramalar. Sıra = gerçek sıklık sırası."""
    kod, govde, _ = getir(TAMAMLA % urllib.parse.quote(tohum))
    if kod != 200 or not govde:
        return []
    try:
        veri = json.loads(govde)
    except Exception:
        return []
    if not isinstance(veri, list) or len(veri) < 2 or not isinstance(veri[1], list):
        return []
    return [_temiz(x) for x in veri[1] if isinstance(x, str)]


def genislet(tohum, ekler=None):
    """Tohumu eklerle genişletip tüm önerileri toplar. Sıra bilgisi korunur."""
    cikti = {}
    for ek in (ekler if ekler is not None else EKLER):
        for sira, s in enumerate(oneriler(tohum + ek)):
            k = _kucuk(s)
            if k not in cikti or sira < cikti[k][1]:
                cikti[k] = (s, sira)
    return [v[0] for v in sorted(cikti.values(), key=lambda v: v[1])]


def trendler(geo="TR"):
    """O gün yükselen aramalar. (baslik, yaklasik_hacim, haber_basligi) listesi."""
    kod, govde, _ = getir(TRENDS % geo)
    if kod != 200 or not govde:
        return []
    try:
        kok = ET.fromstring(govde.encode("utf-8"))
    except Exception:
        return []
    cikti = []
    for it in kok.iter("item"):
        bas = _temiz((it.findtext("title") or ""))
        if not bas:
            continue
        hacim = ""
        haber = ""
        for c in it:
            etiket = c.tag.split("}")[-1]
            if etiket == "approx_traffic":
                hacim = _temiz(c.text)
            elif etiket == "news_item" and not haber:
                for cc in c:
                    if cc.tag.split("}")[-1] == "news_item_title":
                        haber = _temiz(cc.text)
        cikti.append({"sorgu": bas, "hacim": hacim, "haber": haber})
    return cikti


# --------------------------------------------------------------- puanlama
def puanla(sorgu):
    """0–10 arası değer puanı. 0 = bize değmiyor."""
    k = _kucuk(sorgu)
    if any(e in k for e in ELEME):
        return 0
    puan = 0
    for agirlik, kelimeler in DEGER.items():
        for kelime in kelimeler:
            if kelime in k:
                puan += agirlik
                break
    # niyet ekleri: para veya karar sinyali taşıyan sorgu daha değerli
    if re.search(r"\b(fiyat|ücret|kaç para|ne kadar|maliyet|teklif)\b", k):
        puan += 3
    if re.search(r"\b(firma|ajans|stüdyo|şirket|yapan|kim)\b", k):
        puan += 2
    if re.search(r"\b(nasıl|nedir|neden|hangi|örnek)\b", k):
        puan += 1
    return min(10, puan)


def hizmet_bul(sorgu):
    """Sorguyu en yakın hizmet sayfasıyla eşler."""
    k = _kucuk(sorgu)
    en_iyi, en_puan = None, 0
    for tohum, sayfa, etiket in TOHUMLAR:
        ortak = len([p for p in _kucuk(tohum).split() if p and p in k])
        if ortak > en_puan:
            en_iyi, en_puan = (sayfa, etiket), ortak
    return en_iyi or ("hizmetler/index", "Prodüksiyon")


# --------------------------------------------------------------- toplama
def topla(tohumlar=None, asgari_puan=4, tohum_basi=40, trend_dahil=True):
    """Tüm tohumları gezer, puanlar, sıralı ve tekilleştirilmiş liste döner."""
    liste = tohumlar if tohumlar is not None else TOHUMLAR
    bulunan = {}
    hata = []

    for tohum, sayfa, etiket in liste:
        try:
            sonuc = genislet(tohum)
        except Exception as ex:
            hata.append("%s: %s" % (tohum, ex))
            continue
        if not sonuc:
            hata.append("%s: kaynak cevap vermedi" % tohum)
            continue
        alindi = 0
        for sira, s in enumerate(sonuc):
            if alindi >= tohum_basi:
                break
            p = puanla(s)
            if p < asgari_puan:
                continue
            k = _kucuk(s)
            if k in bulunan:
                bulunan[k]["tohum"].append(tohum)
                continue
            bulunan[k] = {"sorgu": s, "puan": p, "sira": sira,
                          "hizmet": sayfa, "etiket": etiket, "tohum": [tohum],
                          "kaynak": "tamamlama"}
            alindi += 1

    if trend_dahil:
        try:
            for t in trendler():
                p = puanla(t["sorgu"])
                if p < asgari_puan:
                    continue
                k = _kucuk(t["sorgu"])
                if k in bulunan:
                    bulunan[k]["kaynak"] = "tamamlama+trend"
                    bulunan[k]["hacim"] = t.get("hacim", "")
                    continue
                sayfa, etiket = hizmet_bul(t["sorgu"])
                bulunan[k] = {"sorgu": t["sorgu"], "puan": p, "sira": 0,
                              "hizmet": sayfa, "etiket": etiket, "tohum": [],
                              "kaynak": "trend", "hacim": t.get("hacim", ""),
                              "haber": t.get("haber", "")}
        except Exception as ex:
            hata.append("trend: %s" % ex)

    sirali = sorted(bulunan.values(), key=lambda d: (-d["puan"], d["sira"]))
    return {"tarih": datetime.date.today().isoformat(),
            "adet": len(sirali), "sorgular": sirali, "hata": hata}


# --------------------------------------------------------------- kayıt
def _yol(tarih=None):
    t = tarih or datetime.date.today().isoformat()
    return os.path.join(VERI_KLASOR, t + ".json")


def kaydet(paket):
    os.makedirs(VERI_KLASOR, exist_ok=True)
    yol = _yol(paket.get("tarih"))
    with open(yol, "w", encoding="utf-8") as f:
        json.dump(paket, f, ensure_ascii=False, indent=1)
    return yol


def oku(tarih=None):
    yol = _yol(tarih)
    if not os.path.exists(yol):
        return None
    try:
        with open(yol, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def gunler(azami=30):
    if not os.path.isdir(VERI_KLASOR):
        return []
    g = sorted((x[:-5] for x in os.listdir(VERI_KLASOR) if x.endswith(".json")),
               reverse=True)
    return g[:azami]


def gunluk(yenile=False):
    """Bugünün derlemesi. Dosya varsa onu okur; yoksa (ya da yenile=True) toplar."""
    if not yenile:
        var = oku()
        if var:
            return var
    paket = topla()
    if paket["sorgular"]:
        kaydet(paket)
    return paket


def yukselenler(gun=7, azami=12):
    """Son N günde yeni çıkan ya da sırası yükselen sorgular."""
    g = gunler(gun)
    if len(g) < 2:
        p = oku(g[0]) if g else None
        return (p or {}).get("sorgular", [])[:azami]
    yeni = oku(g[0]) or {"sorgular": []}
    eski = {}
    for t in g[1:]:
        p = oku(t) or {"sorgular": []}
        for s in p["sorgular"]:
            eski.setdefault(_kucuk(s["sorgu"]), s["sira"])
    cikti = []
    for s in yeni["sorgular"]:
        k = _kucuk(s["sorgu"])
        if k not in eski:
            s = dict(s); s["durum"] = "yeni"
            cikti.append(s)
        elif s["sira"] < eski[k] - 2:
            s = dict(s); s["durum"] = "yükseliyor"; s["onceki"] = eski[k]
            cikti.append(s)
    return cikti[:azami]


def konu_onerileri(azami=8):
    """Yazıya dönüştürülmeye değer, sitede karşılığı olmayan sorgular."""
    p = gunluk()
    kok = ayarlar.SITE_KOK
    yazilmis = set()
    blog = os.path.join(kok, "blog") if kok else None
    if blog and os.path.isdir(blog):
        for ad in os.listdir(blog):
            if ad.endswith(".html"):
                yazilmis.add(_kucuk(ad[:-5].replace("-", " ")))
    cikti = []
    for s in p.get("sorgular", []):
        k = _kucuk(s["sorgu"])
        if any(k in y or y in k for y in yazilmis):
            continue
        cikti.append(s)
        if len(cikti) >= azami:
            break
    return cikti


def kaynak_testi():
    """Panelde 'kaynaklar çalışıyor mu' düğmesi için."""
    sonuc = []
    o = oneriler("3d modelleme")
    sonuc.append(("Google otomatik tamamlama", len(o), o[:3]))
    t = trendler()
    sonuc.append(("Google Trends TR", len(t), [x["sorgu"] for x in t[:3]]))
    return sonuc
