# -*- coding: utf-8 -*-
"""
İNTİHAL DENETİMİ — yazımız kaynak metinle ne kadar örtüşüyor?

Ölçü 1: 6 kelimelik parça (shingle) kapsama oranı — yazıdaki parçaların yüzde kaçı kaynakta da var.
Ölçü 2: en uzun ortak kelime dizisi (alıntı işaretli bölümler hariç tutulur).
Eşik (cikti/yazim-rehberi.md §3.6): kapsama < %5, en uzun dizi < 11 kelime.
Yeniden sözcüklerle yazma (paraphrase) bu ölçülere takılmaz; onu yöntem engeller (olgu listesinden yaz,
kaynağa bakmadan). Bu denetim son kilit: kopyala-yapıştır ve "iki kelime değiştir" kaçağını yakalar.
Kullanım: python3 -m pusula.intihal <yazi.html|txt> <kaynak.txt> [<kaynak2.txt> ...]
"""
import io, re, sys, html as H

N = 6
KAPSAMA_ESIK = 0.05
DIZI_ESIK = 11

def metin(s):
    """HTML ise etiketleri at, alıntı bloklarını (<blockquote>, <q>) ayrı döndür."""
    alintilar = re.findall(r"<(?:blockquote|q)[^>]*>(.*?)</(?:blockquote|q)>", s, re.S | re.I)
    s = re.sub(r"<(?:blockquote|q)[^>]*>.*?</(?:blockquote|q)>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S | re.I)
    s = H.unescape(re.sub(r"<[^>]+>", " ", s))
    return s, [H.unescape(re.sub(r"<[^>]+>", " ", a)) for a in alintilar]

def kelimeler(t):
    t = t.lower().replace("’", "'")
    return re.findall(r"[a-zçğıöşü0-9%]+(?:[.,][0-9]+)*", t)

def parcalar(k, n=N):
    return {tuple(k[i:i + n]) for i in range(max(0, len(k) - n + 1))}

def en_uzun_ortak(a, b):
    """İki kelime listesi arasındaki en uzun ortak ardışık dizi (dinamik programlama, bellek dostu)."""
    if not a or not b:
        return 0, ""
    onceki = [0] * (len(b) + 1); en = 0; son = 0
    for i in range(1, len(a) + 1):
        simdi = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                simdi[j] = onceki[j - 1] + 1
                if simdi[j] > en:
                    en, son = simdi[j], i
        onceki = simdi
    return en, " ".join(a[son - en:son])

def denetle(yazi, kaynaklar):
    """yazi: html/metin; kaynaklar: metin listesi. Döner: {kapsama, en_uzun, dizi, gecti, ...}"""
    y, alintilar = metin(yazi)
    yk = kelimeler(y)
    yp = parcalar(yk)
    kk = []
    for k in kaynaklar:
        kk += kelimeler(metin(k)[0]) + ["§"]
    kp = parcalar(kk)
    ortak = yp & kp
    kapsama = (len(ortak) / len(yp)) if yp else 0.0
    en, dizi = en_uzun_ortak(yk, kk)
    return {"kelime": len(yk), "parca": len(yp), "ortak_parca": len(ortak), "kapsama": round(kapsama, 4),
            "en_uzun": en, "dizi": dizi, "alinti_sayisi": len(alintilar),
            "gecti": kapsama < KAPSAMA_ESIK and en < DIZI_ESIK and len(alintilar) <= 1}

def rapor(r):
    return "kelime %d | ortak 6'lı parça %d/%d (%%%.1f, eşik %%%.0f) | en uzun ortak dizi %d kelime (eşik %d)%s | alıntı %d | %s" % (
        r["kelime"], r["ortak_parca"], r["parca"], r["kapsama"] * 100, KAPSAMA_ESIK * 100, r["en_uzun"], DIZI_ESIK,
        (': "%s"' % r["dizi"]) if r["en_uzun"] >= DIZI_ESIK else "", r["alinti_sayisi"], "GEÇTİ" if r["gecti"] else "GEÇMEDİ")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(2)
    y = io.open(sys.argv[1], encoding="utf-8").read()
    ks = [io.open(p, encoding="utf-8").read() for p in sys.argv[2:]]
    r = denetle(y, ks); print(rapor(r)); sys.exit(0 if r["gecti"] else 1)
