# -*- coding: utf-8 -*-
"""
TREND İZLEME — Türkiye'de bugün en çok aranan + geniş yelpaze haber akışı (TrendSaphiens için).

Kaynaklar (anahtarsız, kalıcı):
  · Google Trends günlük RSS (TR):  https://trends.google.com/trending/rss?geo=TR
      → başlık, yaklaşık arama hacmi, bağlı haber (başlık, kaynak, adres)
  · Google Haberler RSS (konu başına sorgu) — gundem.rss_cek ile aynı yol

Çıktı: veri/trend/YYYY-MM-DD.json
  {"tarih": ..., "aranan": [{"baslik", "hacim", "haber_baslik", "haber_url", "haber_kaynak", "bolum"}],
   "bolumler": {"ekran": [{"baslik","url","kaynak","tarih","ozet"}], ...}}

Kural: kaynağı (adres + ad + tarih) olmayan madde yazılmaz. Bizim eklediğimiz tek şey
çerçeve cümlesidir ("neden arandı / nereye bakılır"); haber metni kopyalanmaz.
"""
import datetime, html, json, os, re, urllib.parse
import xml.etree.ElementTree as ET

from .ayarlar import KOK_DIZIN
from .gundem import rss_cek, GOOGLE_HABER
from .kaynaklar.agir import getir

TRENDS_RSS = "https://trends.google.com/trending/rss?geo=TR"

# Geniş yelpaze — TrendSaphiens bölümleri (anahtar, sorgu, bölüm başlığı, çerçeve)
BOLUMLER = [
    ("piyasalar", 'dolar OR "gram altın" OR borsa OR faiz when:1d', "Piyasalar",
     "Günün rakamı ve nedeni; yorum değil, kaynaklı özet. Yatırım tavsiyesi değildir."),
    ("ekran", '"vizyona giren" OR "bu hafta vizyonda" OR "yeni dizi" OR "dizi final" when:7d', "Dizi & Film",
     "Bu hafta ne izlenir: vizyona girenler, yeni bölümler, platform yayınları."),
    ("spor", '"hangi kanalda" OR "milli maç" OR derbi OR "maç saat kaçta" when:3d', "Spor Ekranı",
     "Maç hangi kanalda, saat kaçta — yayıncı bilgisi kaynağıyla."),
    ("sanat", 'sergi OR bienal OR "sanat galerisi" OR "tiyatro oyunu" OR konser when:7d', "Sanat",
     "Sergi, sahne ve konser takvimi; şehirde ne var."),
    ("yapay-zeka", '"yapay zeka" OR ChatGPT OR Claude OR Gemini OR Runway when:3d', "Yapay Zekâ",
     "Yeni model, yeni araç, yeni kural — ne işe yarar, ne değişir."),
    ("yazilim", 'yazılım OR uygulama OR siber OR "veri ihlali" when:3d', "Yazılım",
     "Ürün, güncelleme ve güvenlik haberleri; kullanıcıya dokunan tarafı."),
    ("muhendislik", 'mühendislik OR "yerli üretim" OR robot OR otomotiv OR enerji when:7d', "Mühendislik",
     "Üretim, enerji, otomotiv ve altyapıda günün gelişmesi."),
    ("sosyal-medya", 'TikTok OR Instagram OR YouTube OR "sosyal medya" when:3d', "Sosyal Medya",
     "Platform değişiklikleri, akımlar ve içerik üreticisine etkisi."),
]
# Google Trends başlığını bölüme eşlemek için anahtar kelimeler
BOLUM_ANAHTAR = {
    "piyasalar": ("dolar", "euro", "altın", "borsa", "faiz", "bist", "kur", "bitcoin", "kripto"),
    "spor": ("maç", "galatasaray", "fenerbahçe", "beşiktaş", "trabzonspor", "milli", "lig", "kupa", "transfer", "derbi", "nba", "euroleague", "voleybol"),
    "ekran": ("dizi", "film", "netflix", "disney", "vizyon", "bölüm", "fragman", "oyuncu", "survivor", "yarışma"),
    "sanat": ("konser", "sergi", "tiyatro", "festival", "albüm", "şarkı"),
    "yapay-zeka": ("yapay zeka", "chatgpt", "gemini", "claude", "openai", "runway"),
    "yazilim": ("uygulama", "güncelleme", "iphone", "android", "whatsapp", "siber", "hack"),
    "muhendislik": ("togg", "tesla", "uydu", "roket", "elektrik", "deprem", "köprü", "tünel"),
    "sosyal-medya": ("tiktok", "instagram", "youtube", "twitter", "x ", "influencer"),
}


def _t(x):
    return html.unescape(re.sub(r"<[^>]+>", "", x or "")).strip()


def trendler(azami=25):
    """Google Trends günlük TR listesi; bağlı haberle birlikte."""
    try:
        kod, ham, _ = getir(TRENDS_RSS, zaman_asimi=20)
    except Exception:
        return []
    if kod != 200 or not ham:
        return []
    try:
        kok = ET.fromstring(ham.encode("utf-8", "ignore"))
    except ET.ParseError:
        return []
    ns = {"ht": "https://trends.google.com/trending/rss"}
    ci = []
    for it in kok.iter("item"):
        baslik = _t(it.findtext("title"))
        if not baslik:
            continue
        hacim = _t(it.findtext("ht:approx_traffic", default="", namespaces=ns))
        haber = it.find("ht:news_item", ns)
        hb = hu = hk = ""
        if haber is not None:
            hb = _t(haber.findtext("ht:news_item_title", default="", namespaces=ns))
            hu = _t(haber.findtext("ht:news_item_url", default="", namespaces=ns))
            hk = _t(haber.findtext("ht:news_item_source", default="", namespaces=ns))
        resim = _t(it.findtext("ht:picture", default="", namespaces=ns))
        ci.append({"baslik": baslik, "hacim": hacim, "haber_baslik": hb, "haber_url": hu, "haber_kaynak": hk,
                   "resim": resim, "bolum": bolum_bul(baslik + " " + hb)})
        if len(ci) >= azami:
            break
    return ci


def bolum_bul(metin):
    m = (metin or "").lower()
    for b, anahtarlar in BOLUM_ANAHTAR.items():
        if any(a in m for a in anahtarlar):
            return b
    return "gundem"


def bolum_haberleri(azami=10):
    """Her geniş bölüm için Google Haberler'den kaynaklı başlıklar."""
    out = {}
    for anahtar, sorgu, ad, cerceve in BOLUMLER:
        liste = []
        try:
            for h in rss_cek(GOOGLE_HABER % urllib.parse.quote(sorgu), azami * 2):
                if not h.get("adres") or not h.get("baslik"):
                    continue
                imza = re.sub(r"\W+", " ", h["baslik"].lower())[:60]
                if any(re.sub(r"\W+", " ", x["baslik"].lower())[:60] == imza for x in liste):
                    continue
                liste.append({"baslik": h["baslik"], "url": h["adres"], "kaynak": h.get("kaynak") or "",
                              "tarih": h.get("tarih") or "", "ozet": (h.get("ozet") or "")[:240]})
                if len(liste) >= azami:
                    break
        except Exception:
            pass
        out[anahtar] = liste
    return out


def gunluk_uret(tarih=None):
    """Günün trend + bölüm dosyasını yazar; eskisi varsa üstüne yazar."""
    tarih = tarih or datetime.date.today().isoformat()
    d = os.path.join(KOK_DIZIN, "veri", "trend"); os.makedirs(d, exist_ok=True)
    veri = {"tarih": tarih, "aranan": trendler(), "bolumler": bolum_haberleri()}
    json.dump(veri, open(os.path.join(d, tarih + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return {"tarih": tarih, "aranan": len(veri["aranan"]), "bolum": {k: len(v) for k, v in veri["bolumler"].items()}}


def son(tarih=None):
    d = os.path.join(KOK_DIZIN, "veri", "trend")
    if not os.path.isdir(d):
        return None
    ds = sorted(f for f in os.listdir(d) if re.match(r"\d{4}-\d{2}-\d{2}\.json$", f))
    if not ds:
        return None
    f = (tarih + ".json") if tarih and (tarih + ".json") in ds else ds[-1]
    try:
        return json.load(open(os.path.join(d, f), encoding="utf-8"))
    except Exception:
        return None


def hepsi():
    d = os.path.join(KOK_DIZIN, "veri", "trend")
    if not os.path.isdir(d):
        return []
    out = []
    for f in sorted(os.listdir(d)):
        if re.match(r"\d{4}-\d{2}-\d{2}\.json$", f):
            try:
                out.append(json.load(open(os.path.join(d, f), encoding="utf-8")))
            except Exception:
                pass
    return out
