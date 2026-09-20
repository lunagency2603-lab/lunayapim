# -*- coding: utf-8 -*-
"""
BAĞIMSIZ DENETİM — yayını bizim ölçümüzle değil, dışarıdakiyle ölçer.

20.09.2026 gerekçesi: seo/denetci.py depodaki dosyalara bakar. Dosya doğru ama
canlı yanlış olabilir — 20.09'da tam bu oldu: hakkımızda/iletişim/gizlilik/koşullar
sayfaları depoda vardı, canlıda ana sayfaya düşüyordu. Kendi denetimimiz bunu
göremez; çünkü dosya yerindeydi.

Bu modül üç bağımsız kaynaktan ölçer:
  1) CANLI TARAMA   — site haritasındaki her adres gerçekten 200 mü dönüyor,
                      yönlendiriliyor mu, iç bağlantıların hedefi yaşıyor mu.
  2) PageSpeed      — Google'ın kendi Lighthouse ölçümü (performans, erişilebilirlik,
                      en iyi uygulamalar, SEO). PSI_ANAHTAR tanımlıysa kotası geniştir.
  3) W3C doğrulayıcı— HTML standart hataları (validator.w3.org/nu).

Çıktı: veri/denetim-dis.json  →  /denetim sayfası bunu basar.
Ağ ister; bu yüzden GitHub Actions'ta çalışır, Mac'te değil.
"""
import datetime, json, os, re, socket, sys, time
import urllib.error, urllib.parse, urllib.request

from .ayarlar import SITE_KOK, KOK_DIZIN

SITE = "https://trendsaphiens.com"
AJAN = "LunaTrendSaphiensDenetim/1.0 (+https://trendsaphiens.com/denetim)"
OLCULEN = ["/", "/bulten", "/hakkimizda", "/yukselen-burc-hesaplama"]
ZAMAN_ASIMI = 45
CIKTI = os.path.join(KOK_DIZIN, "veri", "denetim-dis.json")


def _iste(url, yontem="GET", zaman=ZAMAN_ASIMI):
    r = urllib.request.Request(url, method=yontem, headers={"User-Agent": AJAN,
                                                            "Accept-Language": "tr,en;q=0.8"})
    return urllib.request.urlopen(r, timeout=zaman)


# ------------------------------------------------------------------ 1) canlı tarama
def canli_tarama():
    """Site haritasındaki her adres + sayfalardaki iç bağlantılar."""
    sonuc = {"tarih": datetime.datetime.now().isoformat(timespec="seconds"),
             "adres": 0, "iyi": 0, "sorun": []}
    try:
        harita = _iste(SITE + "/sitemap.xml").read().decode("utf-8", "replace")
    except Exception as ex:
        sonuc["sorun"].append({"adres": "/sitemap.xml", "durum": "okunamadı: %s" % ex})
        return sonuc
    adresler = re.findall(r"<loc>([^<]+)</loc>", harita)
    baglar = set()
    for a in adresler:
        sonuc["adres"] += 1
        try:
            y = _iste(a)
            govde = y.read().decode("utf-8", "replace")
            son = y.geturl()
            if y.status != 200:
                sonuc["sorun"].append({"adres": a, "durum": "HTTP %d" % y.status})
            elif son.rstrip("/") != a.rstrip("/"):
                sonuc["sorun"].append({"adres": a, "durum": "yönlendirildi → %s" % son})
            else:
                sonuc["iyi"] += 1
            for h in re.findall(r'href="([^"#?]+)"', govde):
                if h.startswith(("mailto:", "tel:", "javascript:", "data:")):
                    continue
                u = urllib.parse.urljoin(a, h)
                if u.startswith(SITE) and u not in adresler:
                    baglar.add(u)
        except urllib.error.HTTPError as ex:
            sonuc["sorun"].append({"adres": a, "durum": "HTTP %d" % ex.code})
        except Exception as ex:
            sonuc["sorun"].append({"adres": a, "durum": str(ex)[:80]})
    # site haritasında olmayan ama sayfalardan bağlanan adresler
    sonuc["bagli_adres"] = len(baglar)
    for u in sorted(baglar):
        try:
            y = _iste(u, "GET")
            son = y.geturl()
            y.read(1)
            if y.status != 200:
                sonuc["sorun"].append({"adres": u, "durum": "HTTP %d (bağlantı hedefi)" % y.status})
            elif son.rstrip("/") != u.rstrip("/"):
                sonuc["sorun"].append({"adres": u, "durum": "yönlendirildi → %s" % son})
        except urllib.error.HTTPError as ex:
            sonuc["sorun"].append({"adres": u, "durum": "HTTP %d (bağlantı hedefi)" % ex.code})
        except Exception as ex:
            sonuc["sorun"].append({"adres": u, "durum": str(ex)[:80]})
    return sonuc


# ------------------------------------------------------------------ 2) PageSpeed
def pagespeed(adresler=None, kip="mobile"):
    anahtar = os.environ.get("PSI_ANAHTAR", "")
    out = []
    for yol in (adresler or OLCULEN):
        u = ("https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=%s&strategy=%s"
             "&category=performance&category=accessibility&category=best-practices&category=seo"
             % (urllib.parse.quote(SITE + yol, safe=""), kip))
        if anahtar:
            u += "&key=" + anahtar
        try:
            d = json.loads(_iste(u, zaman=120).read().decode("utf-8"))
            lr = d["lighthouseResult"]
            puan = {k: int(round((v.get("score") or 0) * 100)) for k, v in lr["categories"].items()}
            olcum = {}
            for ad, kimlik in (("FCP", "first-contentful-paint"), ("LCP", "largest-contentful-paint"),
                               ("TBT", "total-blocking-time"), ("CLS", "cumulative-layout-shift")):
                try:
                    olcum[ad] = lr["audits"][kimlik]["displayValue"]
                except Exception:
                    pass
            out.append({"yol": yol, "kip": kip, "puan": puan, "olcum": olcum})
        except Exception as ex:
            out.append({"yol": yol, "kip": kip, "hata": str(ex)[:120]})
        time.sleep(2)
    return out


# ------------------------------------------------------------------ 3) W3C doğrulayıcı
def w3c(adresler=None):
    out = []
    for yol in (adresler or OLCULEN[:3]):
        u = ("https://validator.w3.org/nu/?out=json&doc=%s"
             % urllib.parse.quote(SITE + yol, safe=""))
        try:
            d = json.loads(_iste(u, zaman=90).read().decode("utf-8"))
            ileti = d.get("messages", [])
            hata = [m for m in ileti if m.get("type") == "error"]
            uyari = [m for m in ileti if m.get("type") != "error"]
            out.append({"yol": yol, "hata": len(hata), "uyari": len(uyari),
                        "ornek": [m.get("message", "")[:140] for m in hata[:5]]})
        except Exception as ex:
            out.append({"yol": yol, "hata_mesaji": str(ex)[:120]})
        time.sleep(2)
    return out


def calistir(yaz=True):
    rapor = {"tarih": datetime.datetime.now().isoformat(timespec="seconds"),
             "site": SITE, "canli": canli_tarama()}
    rapor["pagespeed"] = pagespeed(kip="mobile")
    rapor["w3c"] = w3c()
    rapor["ozet"] = ozet(rapor)
    if yaz:
        os.makedirs(os.path.dirname(CIKTI), exist_ok=True)
        with open(CIKTI, "w", encoding="utf-8") as f:
            json.dump(rapor, f, ensure_ascii=False, indent=1)
    return rapor


def ozet(r):
    c = r.get("canli", {})
    psi = [p for p in r.get("pagespeed", []) if "puan" in p]
    ort = {}
    if psi:
        for k in ("performance", "accessibility", "best-practices", "seo"):
            d = [p["puan"].get(k) for p in psi if p["puan"].get(k) is not None]
            if d:
                ort[k] = int(round(sum(d) / len(d)))
    w = sum(x.get("hata", 0) for x in r.get("w3c", []) if isinstance(x.get("hata"), int))
    return {"adres": c.get("adres", 0), "canli_sorun": len(c.get("sorun", [])),
            "psi_ortalama": ort, "w3c_hata": w}


if __name__ == "__main__":
    r = calistir()
    o = r["ozet"]
    print(json.dumps(o, ensure_ascii=False))
    for s in r["canli"]["sorun"][:25]:
        print("  SORUN", s["adres"], "—", s["durum"])
    # canlıda sorun varsa koşu kırmızı dönsün: sessizce bozulmasın
    sys.exit(1 if o["canli_sorun"] else 0)
