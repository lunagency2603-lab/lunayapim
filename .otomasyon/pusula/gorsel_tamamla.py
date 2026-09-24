# -*- coding: utf-8 -*-
"""
GÖRSEL TAMAMLA — görseli olmayan yazılara serbest lisanslı kapak bulur.

Neden ayrı bir modül: konu.py yazıyı yazarken görseli de indiriyor, ama elle
yazılan (kaynak_tur "elle") kayıtlarda bu adım atlanıyor ve sayfa bölümün
yedek görseliyle kalıyor — aynı karga karesi onlarca kartta tekrar ediyor.

Ağ ister: kullanıcının sanal makinesinde ağ yok, GitHub Actions'ta var.
Bu yüzden günlük iş akışına bir adım olarak bağlandı; ağ yoksa sessizce geçer.

Kaynak ve lisans kuralları gorsel_bul.py'nin kendisinde: yalnız Wikimedia
Commons ve Openverse, yalnız ticari kullanıma açık lisanslar, künye sayfada.
"""
import glob, io, json, os, re, sys

from .ayarlar import KOK_DIZIN

# Bölüme göre ek arama ipucu — terim tek başına görsel vermiyorsa.
KAT_IPUCU = {
    "burc": "constellation star map",
    "spor": "stadium football match",
    "ekran": "television studio",
    "muzik": "concert stage music",
    "edebiyat": "books library",
    "sanat": "art exhibition gallery",
    "teknoloji": "computer technology",
    "muhendislik": "factory industry",
    "sosyal-medya": "smartphone social media",
    "haber": "city hall public building",
    "piyasa": "stock exchange finance",
}

# Burçlar için takımyıldızın kendi adı en iyi sonucu veriyor.
BURC_SORGU = {
    "koc": ["Aries constellation map", "Aries constellation"],
    "boga": ["Taurus constellation map", "Pleiades star cluster"],
    "ikizler": ["Gemini constellation map", "Gemini constellation"],
    "yengec": ["Cancer constellation map", "Beehive Cluster"],
    "aslan": ["Leo constellation map", "Regulus star"],
    "basak": ["Virgo constellation map", "Spica star"],
    "terazi": ["Libra constellation map", "Libra constellation"],
    "akrep": ["Scorpius constellation map", "Antares"],
    "yay": ["Sagittarius constellation map", "Sagittarius constellation"],
    "oglak": ["Capricornus constellation map", "Capricornus constellation"],
    "kova": ["Aquarius constellation map", "Aquarius constellation"],
    "balik": ["Pisces constellation map", "Pisces constellation"],
}


def _sorgular(kayit):
    terim = (kayit.get("terim") or "").strip()
    kat = kayit.get("kat") or ""
    slug = kayit.get("slug") or ""
    if kat == "burc":
        for k, v in BURC_SORGU.items():
            if slug.startswith(k + "-"):
                return v
    s = []
    if terim:
        s.append(terim)
    baslik = (kayit.get("yazi") or {}).get("baslik") or ""
    if baslik:
        s.append(re.split(r"[:?—]", baslik)[0].strip())
    if kat in KAT_IPUCU:
        s.append(KAT_IPUCU[kat])
    return [x for x in s if x][:4]


def calistir(log=print):
    try:
        from . import gorsel_bul as GB
    except Exception as ex:
        log("gorsel_bul yok: %s" % ex)
        return {"bakilan": 0, "bulunan": 0}
    dizin = os.path.join(KOK_DIZIN, "veri", "konu")
    bakilan = bulunan = 0
    for yol in sorted(glob.glob(os.path.join(dizin, "20??-??-??", "*.json"))):
        try:
            k = json.load(io.open(yol, encoding="utf-8"))
        except Exception:
            continue
        if k.get("gorsel"):
            continue
        bakilan += 1
        try:
            g = GB.bul(_sorgular(k), k.get("slug") or os.path.basename(yol)[:-5], k.get("kat"))
        except Exception as ex:
            log("  %s: %s" % (k.get("slug"), ex))
            continue
        if g and g.get("dosya"):
            k["gorsel"] = g
            json.dump(k, io.open(yol, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            bulunan += 1
            log("  %-44s %s · %s" % (k.get("slug", "")[:44], g.get("lisans", "?"), (g.get("yazar") or "")[:30]))
    r = rehber_kapaklari(GB, log)
    return {"bakilan": bakilan, "bulunan": bulunan, "rehber": r}


# 23.09.2026 — rehber yazıları (trend_rehber.py) stüdyo fotoğrafıyla yayındaydı.
REHBER_SORGU = {
    "dolar-kac-tl-tcmb-kuru-banka-kuru-neden-farkli": ["Turkish lira US dollar banknotes", "Turkish lira banknotes", "currency exchange office"],
    "gram-altin-nasil-hesaplanir-ons-dolar": ["gold bullion bars", "gold coins", "gold bar"],
    "mac-hangi-kanalda-yayinci-nasil-bulunur": ["football match television broadcast", "football stadium crowd"],
    "vizyona-giren-filmler-ne-zaman-aciklanir-nereden-bakilir": ["cinema auditorium", "movie theater"],
    "google-trends-bugun-en-cok-aranan-listesi-nasil-okunur": ["search engine laptop screen", "laptop keyboard"],
    "enflasyon-verisi-ne-zaman-aciklanir-tuik-takvimi": ["supermarket prices shelf", "Turkish Statistical Institute"],
    "yapay-zeka-ile-uretilmis-gorsel-nasil-anlasilir-etiket": ["artificial intelligence art", "neural network visualization"],
    "isletme-sosyal-medya-haftalik-paylasim-takvimi": ["smartphone social media", "planner calendar desk"],
    "sergi-konser-tiyatro-takvimi-nereden-takip-edilir": ["theatre stage audience", "concert hall audience"],
}


def rehber_kapaklari(GB, log=print):
    yol = os.path.join(KOK_DIZIN, "veri", "trend", "rehber-gorsel.json")
    try:
        d = json.load(io.open(yol, encoding="utf-8"))
    except Exception:
        d = {}
    bulunan = 0
    for slug, sorgu in REHBER_SORGU.items():
        if (d.get(slug) or {}).get("dosya"):
            continue
        try:
            g = GB.bul(sorgu, "rehber-" + slug[:60])
        except Exception as ex:
            log("  rehber %s: %s" % (slug, ex)); continue
        if g and g.get("dosya"):
            d[slug] = g; bulunan += 1
            log("  rehber %-40s %s" % (slug[:40], g.get("lisans", "?")))
    if bulunan:
        os.makedirs(os.path.dirname(yol), exist_ok=True)
        json.dump(d, io.open(yol, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return bulunan


if __name__ == "__main__":
    print(json.dumps(calistir(), ensure_ascii=False))
