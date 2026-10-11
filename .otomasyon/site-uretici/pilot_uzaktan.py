# -*- coding: utf-8 -*-
"""
UZAKTAN TESLİM EDİLEN HİZMETLER — PİLOT İL DÜZENİ (11.10.2026)

Karar (sahibinin, 11.10.2026): yerinde çekim gerektirmeyen işlerde (3D modelleme,
ürün animasyonu) 81 il için ayrı sayfa tutulmaz. Bu sayfalar aynı hizmeti il adını
değiştirerek anlatıyordu; Google'ın "şehirlere göre çoğaltılmış sayfa" tanımına
giriyor ve 46 sayfanın yarısını Google hiç taramıyordu.

Düzen: pilot iller (aşağıda) kalır ve her biri o ilin sanayi/proje verisiyle
özgünleşir; diğer illerin adresleri ana hizmet sayfasına 301 ile bağlanır,
sitedeki bütün iç bağlantılar doğrudan ana sayfaya çevrilir.

Bu modül: (1) pilot dışı dosyaları siler, (2) yönlendirme defterine yazar,
(3) iç bağlantıları çevirir. Etkisiz tekrarlanabilir.
Üreticiler (uretici*.py, sektor_sayfalari.py) yeni sayfa açarken PILOT'a bakmalı.
"""
import glob, io, json, os, re, sys

PILOT = ("istanbul", "ankara", "izmir", "bursa", "kocaeli")
UZAKTAN = {
    "insaat-3d-modelleme": "/hizmetler/insaat-3d-modelleme",
    "urun-animasyon": "/hizmetler/urun-animasyon",
}


def pilot_mi(il_slug):
    return il_slug in PILOT


def _defterler(kok):
    yollar = [os.path.join(kok, ".otomasyon", "veri", "yonlendirme.json")]
    pus = os.path.expanduser("~/mnt/luna-pusula/veri/yonlendirme.json")
    if os.path.exists(pus):
        yollar.append(pus)
    return yollar


def calistir(kok, sil=True):
    kaldir = {}   # /sehir/x-hizmet -> hedef
    for ek, hedef in UZAKTAN.items():
        for y in glob.glob(os.path.join(kok, "sehir", "*-%s.html" % ek)):
            il = os.path.basename(y)[: -len("-%s.html" % ek)]
            if il in PILOT:
                continue
            kaldir["/sehir/%s-%s" % (il, ek)] = hedef
            if sil:
                os.remove(y)
    # yönlendirme defterleri
    for d in _defterler(kok):
        try:
            defter = json.load(open(d, encoding="utf-8"))
        except Exception as ex:
            print("defter okunamadı, dokunulmadı:", d, ex)
            continue
        defter.update(kaldir)
        json.dump(defter, open(d, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
    # _redirects: tam adres satırları jokerlerden önce
    r = os.path.join(kok, "_redirects")
    satir = io.open(r, encoding="utf-8").read().split("\n")
    var = {l.split()[0] for l in satir if l.strip() and not l.startswith("#")}
    yeni = ["%s  %s  301" % (a, h) for a, h in sorted(kaldir.items()) if a not in var]
    bas = [l for l in satir if l.startswith("#")]
    govde = [l for l in satir if l.strip() and not l.startswith("#")]
    io.open(r, "w", encoding="utf-8").write("\n".join(bas + yeni + govde) + "\n")
    # iç bağlantılar: pilot dışı her uzaktan-hizmet il adresi ana hizmet sayfasına
    desen = re.compile(r'href="((?:https://lunayapim\.com)?(?:\.\./|/)?(?:sehir/)?)([a-z]+(?:-[a-z]+)*?)-(%s)(\.html)?(#[^"]*)?"'
                       % "|".join(re.escape(k) for k in UZAKTAN))
    n = 0
    for y in glob.glob(os.path.join(kok, "**", "*.html"), recursive=True):
        p = os.path.relpath(y, kok)
        if p.startswith(("trend/", "onizleme/", "assets/")):
            continue
        s = io.open(y, encoding="utf-8").read()
        derin = p.count("/")
        on = "../" * derin

        def _cevir(m):
            onek, il, ek = m.group(1), m.group(2), m.group(3)
            sehir_ici = ("sehir/" in onek) or (p.startswith("sehir/") and onek == "")
            if not sehir_ici or il in PILOT:
                return m.group(0)
            return 'href="%s%s%s"' % (on, UZAKTAN[ek].lstrip("/"), m.group(5) or "")
        s2 = desen.sub(_cevir, s)
        if s2 != s:
            io.open(y, "w", encoding="utf-8").write(s2)
            n += 1
    return {"yonlendirilen": len(kaldir), "baglanti_degisen_sayfa": n}


if __name__ == "__main__":
    kok = sys.argv[1] if len(sys.argv) > 1 else "."
    print(calistir(os.path.abspath(kok)))
