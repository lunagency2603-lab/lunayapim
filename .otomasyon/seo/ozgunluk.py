# -*- coding: utf-8 -*-
"""
ÖZGÜNLÜK DENETÇİSİ — "yapay zekâ yazmış" izlerini ve iç tekrarı arar.

Dürüstlük notu, en başta: **Hiçbir dedektör kesin değildir.** Ne bu, ne
piyasadaki ücretli olanlar. Burada yaptığımız şey, makine metninde
istatistiksel olarak daha sık görülen kalıpları saymak. Yüksek puan
"yapay zekâ yazdı" demek değil; "bu metin kalıplaşmış, insan editörü
görmemiş" demek. Zaten düzeltmemiz gereken de tam olarak bu.

Üç katman:
  1. İÇ TEKRAR    — kendi sayfalarımız birbirini kopyalıyor mu (5'li n-gram)
  2. KALIP        — yapay zekâ metninde şişen bağlaçlar, boş pekiştirmeler,
                    edilgen yığılması, üçlü liste tiki
  3. RİTİM        — cümle uzunluğu değişkenliği (düşük değişkenlik = makine)

Çıktı: sayfa başına 0–100 puan ve DÜZELTİLECEK CÜMLELERİN kendisi.
Genel laf etmiyor; "şu cümleyi değiştir" diyor.
"""
import os, re, json, math, unicodedata
from collections import Counter

ETIKET_SIL = re.compile(r"<(script|style|noscript|svg|template)[^>]*>.*?</\1>", re.S | re.I)
ETIKET = re.compile(r"<[^>]+>")

# --- yapay zekâ metninde şişen kalıplar (Türkçe) ------------------------------
# Her biri: (desen, ceza, öneri)
KALIPLAR = [
    (r"(?:^|[.!?…]\s+)Ayrıca,?\s",       3, "cümle başında 'Ayrıca' — cümleyi öncekine bağla ya da at"),
    (r"\bbununla birlikte\b",           3, "'ama' ya da 'yine de' yaz"),
    (r"\bbu bağlamda\b",                4, "at — hiçbir şey eklemiyor"),
    (r"\bbu doğrultuda\b",              4, "at"),
    (r"\bsonuç olarak\b",               3, "at; sonucu zaten yazıyorsun"),
    (r"\bgenel olarak\b",               3, "at ya da somut sayı ver"),
    (r"\bunutulmamalıdır\b",            4, "kime söylüyorsun? doğrudan yaz"),
    (r"\bönemli bir rol oynamaktadır\b",5, "ne yaptığını yaz"),
    (r"\bbüyük önem taşı(r|maktadır)\b",5, "neden önemli, onu yaz"),
    (r"\bdikkat çekmektedir\b",         4, "kim dikkat ediyor? somutlaştır"),
    (r"\böne çıkmaktadır\b",            4, "somutlaştır"),
    (r"\bson derece\b",                 3, "at"),
    (r"\boldukça (?:iyi|önemli|etkili|başarılı|yüksek)\b", 3, "ölç ya da at"),
    (r"\bgünümüzde\b",                  3, "tarih ver ya da at"),
    (r"\bgiderek artan\b",              3, "ne kadar arttı? sayı ver"),
    (r"\bçeşitli avantajlar\b",         4, "hangi avantaj? say"),
    (r"\bihtiyaçlarınıza yönelik\b",    3, "hangi ihtiyaç? yaz"),
    (r"\bprofesyonel bir şekilde\b",    4, "nasıl? somut adım yaz"),
    (r"\btitizlikle\b",                 3, "ne yaptığını yaz"),
    (r"\bmaksimum verim\b",             4, "ölç"),
    (r"\bsizler için\b",                2, "'size' yeter"),
    (r"\bhizmet vermekteyiz\b",         3, "'yapıyoruz' yaz"),
    (r"\bsağlamaktadır\b",              2, "'sağlıyor' yaz"),
    (r"\bgerçekleştirilmektedir\b",     4, "kim yapıyor? etken yaz"),
    (r"\bsunulmaktadır\b",              3, "etken yaz"),
]

EDILGEN = re.compile(r"\w+(maktadır|mektedir|ılmaktadır|ilmektedir|ulmaktadır|ünmektedir)\b")
UCLU = re.compile(r"\b\w+,\s+\w+\s+ve\s+\w+\b")


GOVDE_DISI = re.compile(r"<(header|footer|nav)\b[^>]*>.*?</\1>", re.S | re.I)


def duz(g):
    g = ETIKET_SIL.sub(" ", g or "")
    # Menü, üst ve alt bilgi HER sayfada aynı — benzerliği yapay şişiriyor.
    # Karşılaştırma yalnızca sayfanın kendi gövdesi üzerinden yapılmalı.
    g = GOVDE_DISI.sub(" ", g)
    g = ETIKET.sub(" ", g)
    g = re.sub(r"&[a-z]+;|&#\d+;", " ", g)
    return re.sub(r"\s+", " ", g).strip()


def cumleler(m):
    p = re.split(r"(?<=[.!?…])\s+", m or "")
    return [c.strip() for c in p if len(c.strip()) > 25]


def sadelestir(x):
    x = (x or "").lower()
    for a, b in (("ı", "i"), ("ğ", "g"), ("ü", "u"), ("ş", "s"), ("ö", "o"), ("ç", "c")):
        x = x.replace(a, b)
    x = unicodedata.normalize("NFKD", x)
    x = "".join(c for c in x if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]+", " ", x)


def ngram(m, n=5):
    k = sadelestir(m).split()
    return {" ".join(k[i:i + n]) for i in range(max(0, len(k) - n + 1))}


# ---------------------------------------------------------------- katman 2 ve 3
def kalip_bul(metin):
    """Yapay zekâ kalıplarını ve nerede geçtiğini döner."""
    bulgular = []
    for desen, ceza, oneri in KALIPLAR:
        for m in re.finditer(desen, metin, re.I):
            bas = max(0, m.start() - 60)
            bulgular.append({
                "kalip": m.group(0), "ceza": ceza, "oneri": oneri,
                "baglam": "…" + metin[bas:m.end() + 60].strip() + "…",
            })
    return bulgular


def ritim(cs):
    """Cümle uzunluğu değişkenliği. Düşük = makine ritmi."""
    if len(cs) < 5:
        return None, None
    u = [len(c.split()) for c in cs]
    ort = sum(u) / len(u)
    sap = math.sqrt(sum((x - ort) ** 2 for x in u) / len(u))
    return round(ort, 1), round(sap / ort, 3) if ort else None


def sayfa_puan(metin):
    """0–100. 100 = temiz. Düşükse metin kalıplaşmış demektir."""
    cs = cumleler(metin)
    kelime = len(metin.split())
    if kelime < 120:
        return None
    ceza = 0.0
    kalip = kalip_bul(metin)
    ceza += sum(k["ceza"] for k in kalip)

    ed = len(EDILGEN.findall(metin))
    ed_oran = ed / max(1, len(cs))
    if ed_oran > 0.25:
        ceza += (ed_oran - 0.25) * 60

    uc = len(UCLU.findall(metin))
    uc_oran = uc / max(1, len(cs))
    if uc_oran > 0.18:
        ceza += (uc_oran - 0.18) * 50

    ort, degisken = ritim(cs)
    if degisken is not None and degisken < 0.34:
        ceza += (0.34 - degisken) * 90       # tekdüze ritim

    # aynı kelimeyle başlayan cümleler
    baslar = Counter(sadelestir(c).split()[0] for c in cs if sadelestir(c).split())
    tekrar = sum(v - 1 for v in baslar.values() if v > 2)
    ceza += tekrar * 1.5

    puan = max(0, 100 - ceza * (100.0 / max(60.0, kelime / 6.0)))
    return {
        "puan": round(min(100, puan), 1),
        "kelime": kelime, "cumle": len(cs),
        "ort_uzunluk": ort, "ritim_degiskenlik": degisken,
        "edilgen": ed, "uclu_liste": uc,
        "tekrar_cumle_basi": tekrar,
        "kalip": kalip,
    }


# ---------------------------------------------------------------- katman 1
def ic_tekrar(sayfalar, esik=0.28):
    """Sayfa çiftleri arasında n-gram örtüşmesi. Yüksekse kendimizi kopyalıyoruz."""
    gramlar = {y: ngram(m) for y, m in sayfalar.items() if len(m.split()) > 150}
    adlar = sorted(gramlar)
    ciftler = []
    for i in range(len(adlar)):
        for j in range(i + 1, len(adlar)):
            a, b = gramlar[adlar[i]], gramlar[adlar[j]]
            if not a or not b:
                continue
            ortak = len(a & b)
            if not ortak:
                continue
            j_ = ortak / len(a | b)
            if j_ >= esik:
                ciftler.append({"a": adlar[i], "b": adlar[j], "benzerlik": round(j_, 3)})
    ciftler.sort(key=lambda x: -x["benzerlik"])
    return ciftler


def kalip_cumleler(sayfalar, en_az=8):
    """Çok sayıda sayfada birebir tekrar eden cümleler (şablon kokusu)."""
    sayac = Counter()
    nerede = {}
    for y, m in sayfalar.items():
        for c in set(cumleler(m)):
            a = sadelestir(c)[:150]
            if len(a) < 60:
                continue
            sayac[a] += 1
            nerede.setdefault(a, c)
    return [{"cumle": nerede[a][:170], "sayfa": n}
            for a, n in sayac.most_common(40) if n >= en_az]


# ---------------------------------------------------------------- çalıştır
def tara(kok, azami=None):
    sayfalar = {}
    for d, altlar, dosyalar in os.walk(kok):
        altlar[:] = [x for x in altlar if x not in ("assets", ".git", ".github", "node_modules")]
        for f in sorted(dosyalar):
            if not f.endswith(".html"):
                continue
            y = os.path.relpath(os.path.join(d, f), kok)
            try:
                sayfalar[y] = duz(open(os.path.join(d, f), encoding="utf-8").read())
            except Exception:
                pass
            if azami and len(sayfalar) >= azami:
                break
    return sayfalar


def rapor(kok, azami=None):
    sayfalar = tara(kok, azami)
    puanlar = {}
    for y, m in sayfalar.items():
        p = sayfa_puan(m)
        if p:
            puanlar[y] = p
    dusuk = sorted(puanlar.items(), key=lambda kv: kv[1]["puan"])[:25]
    kalip_toplam = Counter()
    for p in puanlar.values():
        for k in p["kalip"]:
            kalip_toplam[k["kalip"].lower()] += 1
    return {
        "sayfa": len(puanlar),
        "ortalama": round(sum(p["puan"] for p in puanlar.values()) / max(1, len(puanlar)), 1),
        "en_dusuk": [{"sayfa": y, "puan": p["puan"], "kalip": len(p["kalip"]),
                      "ritim": p["ritim_degiskenlik"], "edilgen": p["edilgen"]}
                     for y, p in dusuk],
        "en_sik_kalip": kalip_toplam.most_common(15),
        "ic_tekrar": ic_tekrar(sayfalar),
        "sablon_cumle": kalip_cumleler(sayfalar),
        "_puanlar": puanlar,
    }


if __name__ == "__main__":
    import sys
    from pusula.ayarlar import SITE_KOK
    r = rapor(sys.argv[1] if len(sys.argv) > 1 else SITE_KOK)
    r.pop("_puanlar", None)
    print(json.dumps(r, ensure_ascii=False, indent=2)[:6000])
