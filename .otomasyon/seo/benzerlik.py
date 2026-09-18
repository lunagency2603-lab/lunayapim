# -*- coding: utf-8 -*-
"""
Benzerlik (doorway/spam riski) analizi.
Sayfa gövdelerini 5 kelimelik parçalara ("shingle") bölüp Jaccard benzerliği hesaplar.
  > %70  : Google için birbirinin kopyası sayılabilir  → KIRMIZI
  %50-70 : şablon ağır basıyor                         → SARI
  < %50  : sağlıklı                                    → YEŞİL
Ayrıca her sayfanın "özgün metin oranını" (yalnızca o sayfada geçen parçalar) verir.
"""
import os, re, html, glob, collections, itertools, sys

SITE = os.path.expanduser("~/Documents/GitHub/lunayapim")
if not os.path.isdir(SITE): SITE = os.path.expanduser("~/mnt/Documents/GitHub/lunayapim")
N = 5

BETIK = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.S | re.I)
ETIKET = re.compile(r"<[^>]+>")
BASLIK_ALT = re.compile(r"<(header|footer|nav)[^>]*>.*?</\1>", re.S | re.I)

def govde(s):
    s = BETIK.sub(" ", s)
    s = BASLIK_ALT.sub(" ", s)          # ortak header/footer/nav sayılmasın
    s = ETIKET.sub(" ", s)
    s = html.unescape(s).lower()
    s = re.sub(r"[^\wçğıöşü ]+", " ", s, flags=re.UNICODE)
    return [w for w in s.split() if len(w) > 1]

def parcalar(kelimeler, n=N):
    return set(tuple(kelimeler[i:i+n]) for i in range(max(0, len(kelimeler)-n+1)))

def jaccard(a, b):
    if not a or not b: return 0.0
    k = len(a & b)
    return k / float(len(a | b))

def grupla(f):
    b = os.path.basename(f)
    d = os.path.dirname(f)
    if d == "sehir":
        if b == "index.html": return "sehir-index"
        for h in ("insaat-3d-modelleme","emlak-video","urun-animasyon","klip-cekimi",
                  "drone-cekimi","dugun-cekimi","isletme-tanitim"):
            if b.endswith("-" + h + ".html"): return "sehir:" + h
        return "sehir:genel"
    return d or "kok"

def calistir():
    eski = os.getcwd(); os.chdir(SITE)
    dosyalar = [f for f in sorted(glob.glob("**/*.html", recursive=True)) if not f.startswith("onizleme/")]
    P = {}
    for f in dosyalar:
        P[f] = parcalar(govde(open(f, encoding="utf-8").read()))
    # özgünlük: kaç parça yalnızca bu sayfada geçiyor
    sayac = collections.Counter()
    for f, p in P.items():
        for x in p: sayac[x] += 1
    ozgun = {f: (sum(1 for x in p if sayac[x] == 1) / float(len(p)) if p else 0) for f, p in P.items()}

    gruplar = collections.defaultdict(list)
    for f in dosyalar: gruplar[grupla(f)].append(f)

    rapor = []
    en_yuksek = []
    for g, fs in sorted(gruplar.items()):
        if len(fs) < 2:
            rapor.append((g, len(fs), None, None, None)); continue
        deger = []
        for a, b in itertools.combinations(fs, 2):
            deger.append((jaccard(P[a], P[b]), a, b))
        deger.sort(reverse=True)
        ort = sum(d[0] for d in deger) / len(deger)
        rapor.append((g, len(fs), ort, deger[0][0], deger[0][1:]))
        en_yuksek += deger[:3]
    en_yuksek.sort(reverse=True)
    os.chdir(eski)
    return dosyalar, rapor, en_yuksek, ozgun

if __name__ == "__main__":
    dosyalar, rapor, en_yuksek, ozgun = calistir()
    print("Sayfa: %d | parça uzunluğu: %d kelime\n" % (len(dosyalar), N))
    print("%-26s %5s %10s %10s" % ("GRUP", "ADET", "ORT.BENZ", "EN YÜKSEK"))
    for g, n, ort, enb, cift in rapor:
        if ort is None:
            print("%-26s %5d %10s %10s" % (g, n, "—", "—")); continue
        isaret = "KIRMIZI" if enb > .70 else ("SARI" if enb > .50 else "")
        print("%-26s %5d %9.1f%% %9.1f%%  %s" % (g, n, ort*100, enb*100, isaret))
    print("\nEn benzer 8 çift:")
    for d, a, b in en_yuksek[:8]:
        print("  %5.1f%%  %s  ↔  %s" % (d*100, a, b))
    ort_ozgun = sum(ozgun.values())/len(ozgun)
    print("\nOrtalama özgün metin oranı: %%%.1f" % (ort_ozgun*100))
    dusuk = sorted(ozgun.items(), key=lambda x: x[1])[:6]
    print("En düşük özgünlük:")
    for f, o in dusuk: print("  %%%.1f  %s" % (o*100, f))
