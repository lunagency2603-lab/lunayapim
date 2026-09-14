# -*- coding: utf-8 -*-
"""
TAKVİM — Türkiye'de düzenli olarak çok aranan, tarihi önceden belli konular.
TrendSaphiens her sabah "bugün / bu hafta ne aranacak" kutusunu buradan kurar ve
X paylaşım sırasını buna göre düzenler.

İki tür kayıt:
  · KURAL   : tekrar eden (her iş günü, her cuma, her ay 3'ü…) — tarih hesaplanır.
  · SABİT   : tek tarihli (derbi, milli maç, faiz kararı, bayram…) — veri/takvim.json'dan
              okunur; her kaydın resmî kaynağı (url) ZORUNLU, kaynaksız kayıt listelenmez.
              Panelden ya da elle eklenir; biz tarih uydurmayız.

Her kayıt: {"ad", "tarih", "saat", "kat", "sorgu" (Google'da aranan biçim), "kaynak", "kaynak_url", "sayfa"}
"sayfa": TrendSaphiens'te hangi günlük sayfaya bağlanır (piyasa/<t>, ekran/<t>, spor/<t>…).
"""
import calendar, datetime, json, os

from .ayarlar import KOK_DIZIN

SABIT_DOSYA = os.path.join(KOK_DIZIN, "veri", "takvim.json")

# (ad, kural, saat, kat, sorgu, kaynak, kaynak_url)
# kural: "isgunu" | "hergun" | "cuma" | "cumartesi" | "pazar" | "ay:3" (ayın 3'ü; hafta sonuna gelirse sonraki iş günü)
KURAL = [
    ("TCMB gösterge kurları", "isgunu", "15:30", "piyasa", "dolar kaç tl, euro kaç tl", "TCMB", "https://www.tcmb.gov.tr/kurlar/today.xml"),
    ("Gram altın fiyatı", "hergun", "09:00", "piyasa", "gram altın kaç tl, çeyrek altın", "truncgil finans", "https://finans.truncgil.com/"),
    ("Vizyona giren filmler", "cuma", "10:00", "ekran", "bu hafta vizyona giren filmler", "Google Haberler", "https://news.google.com/rss/search?q=%22vizyona+giren%22&hl=tr&gl=TR&ceid=TR:tr"),
    ("Hafta sonu maçları — hangi kanalda", "cumartesi", "09:00", "spor", "maç hangi kanalda, saat kaçta", "Google Haberler", "https://news.google.com/rss/search?q=%22hangi+kanalda%22+ma%C3%A7&hl=tr&gl=TR&ceid=TR:tr"),
    ("Pazar maçları — hangi kanalda", "pazar", "09:00", "spor", "derbi hangi kanalda", "Google Haberler", "https://news.google.com/rss/search?q=derbi+%22hangi+kanalda%22&hl=tr&gl=TR&ceid=TR:tr"),
    ("TÜİK enflasyon verisi", "ay:3", "10:00", "piyasa", "enflasyon açıklandı mı, tüfe", "TÜİK", "https://data.tuik.gov.tr/"),
    ("Haftanın dizileri ve platform yayınları", "cuma", "12:00", "ekran", "yeni dizi, netflix bu hafta", "Google Haberler", "https://news.google.com/rss/search?q=%22yeni+dizi%22+OR+%22yeni+sezon%22&hl=tr&gl=TR&ceid=TR:tr"),
    ("Sanat takvimi — sergi, konser, sahne", "cuma", "14:00", "sanat", "bu hafta sonu ne yapılır, sergi", "Google Haberler", "https://news.google.com/rss/search?q=sergi+OR+konser+OR+tiyatro&hl=tr&gl=TR&ceid=TR:tr"),
]

GUN = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
_HAFTA = {"pazartesi": 0, "sali": 1, "carsamba": 2, "persembe": 3, "cuma": 4, "cumartesi": 5, "pazar": 6}


def _kural_uyar(kural, gun):
    if kural == "hergun":
        return True
    if kural == "isgunu":
        return gun.weekday() < 5
    if kural in _HAFTA:
        return gun.weekday() == _HAFTA[kural]
    if kural.startswith("ay:"):
        n = int(kural[3:])
        d = datetime.date(gun.year, gun.month, min(n, calendar.monthrange(gun.year, gun.month)[1]))
        while d.weekday() >= 5:
            d += datetime.timedelta(days=1)
        return d == gun
    return False


def sabitler():
    """veri/takvim.json — kaynaklı tek tarihli kayıtlar. Kaynaksız olan atlanır."""
    try:
        liste = json.load(open(SABIT_DOSYA, encoding="utf-8"))
    except Exception:
        return []
    out = []
    for k in liste if isinstance(liste, list) else []:
        if not (k.get("ad") and k.get("tarih") and k.get("kaynak_url")):
            continue
        out.append({"ad": k["ad"], "tarih": k["tarih"], "saat": k.get("saat", ""), "kat": k.get("kat", "gundem"),
                    "sorgu": k.get("sorgu", ""), "kaynak": k.get("kaynak", ""), "kaynak_url": k["kaynak_url"], "sabit": True})
    return out


def gun(tarih=None):
    """O günün kayıtları (kural + sabit), saate göre sıralı."""
    t = datetime.date.fromisoformat(tarih) if isinstance(tarih, str) else (tarih or datetime.date.today())
    out = []
    for ad, kural, saat, kat, sorgu, kaynak, url in KURAL:
        if _kural_uyar(kural, t):
            out.append({"ad": ad, "tarih": t.isoformat(), "saat": saat, "kat": kat, "sorgu": sorgu, "kaynak": kaynak, "kaynak_url": url, "sabit": False, "kural": kural})
    out += [s for s in sabitler() if s["tarih"] == t.isoformat()]
    for k in out:
        k["sayfa"] = "%s/%s" % (k["kat"], t.isoformat()) if k["kat"] in ("piyasa", "ekran", "spor", "sanat", "teknoloji", "muhendislik", "sosyal-medya") else "aranan/%s" % t.isoformat()
    return sorted(out, key=lambda k: k["saat"] or "99")


def hafta(tarih=None, gun_sayisi=7):
    t = datetime.date.fromisoformat(tarih) if isinstance(tarih, str) else (tarih or datetime.date.today())
    return [(t + datetime.timedelta(days=i), gun(t + datetime.timedelta(days=i))) for i in range(gun_sayisi)]


def paylasim_sirasi(tarih=None):
    """X için günün sırası: saat → (metin, sayfa). Metin kısa; rakam yok (rakam sayfada, kaynaklı)."""
    out = []
    for k in gun(tarih):
        out.append({"saat": k["saat"], "metin": "%s — %s" % (k["ad"], k["sorgu"]), "sayfa": k["sayfa"]})
    return out
