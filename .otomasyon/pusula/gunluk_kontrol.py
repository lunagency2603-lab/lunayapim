# -*- coding: utf-8 -*-
"""
GÜNLÜK KONTROL — her turun sonunda canlı siteyi ve indeksi denetler, özet çıkarır, Telegram'a bildirir.
Amaç: otomasyon sessizce durduğunda (04–07.09'da olduğu gibi) aynı gün haber vermek.

Kontroller (Mac'te, internetle):
  1. Canlı sayfalar: ana sayfa, /trend/, günün piyasa/aranan/gündem sayfaları → 200 mü, gerçekten var mı
     (yumuşak 404 tuzağı: ana sayfa 200 döndürebilir → başlık kontrolü).
  2. sitemap.xml canlıda okunuyor mu, bugünün adresleri içinde mi, kaç URL.
  3. Depo: yayınlanmamış değişiklik var mı (push başarısız olduysa burada görünür).
  4. Yerel SEO kapısı sonucu (log'dan) ve son yazar/kaynak özeti satırları.
  5. İndeks denetimi (pusula/indeks.py): Google'ın indekslemesini engelleyebilecek
     repo tarafı sebepler — canonical, .html bağlantı, hayalet /api/ adresi,
     site haritası ↔ disk eşleşmesi, sitemap'te noindex — + son Search Console okuması.
Çıktı: veri/gunluk-kontrol.json (son 60 gün) + otomasyon.log'a özet + Telegram (jeton varsa).
"""
import datetime, io, json, os, re, subprocess, sys
from .ayarlar import KOK_DIZIN, SITE_KOK
from .kaynaklar.agir import getir

KOK = "https://lunayapim.com"

def _sayfa(url, beklenen_baslik=None):
    kod, govde, son = getir(url, zaman_asimi=20, basliklar={"Accept": "text/html"})
    baslik = (re.search(r"<title>(.*?)</title>", govde or "", re.S) or [None, ""])[1] if govde else ""
    anasayfa = "Luna Yapım — İnşaat 3D" in (baslik or "")
    var = kod == 200 and (not beklenen_baslik or (beklenen_baslik in (govde or ""))) and not (anasayfa and not url.rstrip("/").endswith("lunayapim.com"))
    return {"url": url.replace(KOK, ""), "kod": kod, "var": bool(var), "baslik": (baslik or "").strip()[:70]}

def _sitemap():
    kod, s, _ = getir(KOK + "/sitemap.xml", zaman_asimi=20)
    urls = re.findall(r"<loc>([^<]+)</loc>", s or "")
    return kod, urls

def _depo():
    S = SITE_KOK
    try:
        out = subprocess.run(["git", "--no-optional-locks", "status", "--porcelain"], cwd=S, capture_output=True, text=True, timeout=30).stdout
        yerel = len([l for l in out.splitlines() if l.strip()])
        ahead = subprocess.run(["git", "--no-optional-locks", "rev-list", "--count", "@{u}..HEAD"], cwd=S, capture_output=True, text=True, timeout=30).stdout.strip()
        return {"bekleyen_dosya": yerel, "push_bekleyen_kayit": int(ahead or 0)}
    except Exception as ex:
        return {"hata": str(ex)[:120]}

def calistir(bildir=True):
    bugun = datetime.date.today().isoformat()
    sayfalar = [_sayfa(KOK + "/"), _sayfa(KOK + "/trend/"),
                _sayfa(KOK + "/trend/piyasa/" + bugun, bugun), _sayfa(KOK + "/trend/aranan/" + bugun, bugun),
                _sayfa(KOK + "/gundem/" + bugun, bugun), _sayfa(KOK + "/olmayan-sayfa-kontrol-%s" % bugun)]
    smk, urls = _sitemap()
    bugun_sitemap = [u for u in urls if bugun in u]
    depo = _depo()
    # log'dan son kapı satırı
    L = os.path.join(KOK_DIZIN, "veri", "otomasyon.log")
    son = io.open(L, encoding="utf-8").read()[-6000:] if os.path.exists(L) else ""
    kapi = (re.findall(r"Sayfa: \d+ \| HATA: \d+ \| UYARI: \d+ \| SEO uygunluk: %[\d.,]+", son) or ["kapı satırı yok"])[-1]
    yazar = (re.findall(r"Yazar: [^\n]+|Kaynak özeti: [^\n]+", son) or [])[-2:]
    push = "push tamam" if "push tamam" in son.split("===")[-1] else ("push BAŞARISIZ" if "push BAŞARISIZ" in son.split("===")[-1] else "push yok")
    sorunlar = []
    for p in sayfalar[2:5]:
        if not p["var"]:
            sorunlar.append("bugünün sayfası canlıda yok: %s (HTTP %s)" % (p["url"], p["kod"]))
    if sayfalar[5]["kod"] == 200:
        sorunlar.append("yumuşak 404: olmayan adres 200 dönüyor")
    if smk != 200:
        sorunlar.append("sitemap okunamadı (HTTP %s)" % smk)
    elif not bugun_sitemap:
        sorunlar.append("sitemap'te bugünün adresi yok")
    if depo.get("bekleyen_dosya"):
        sorunlar.append("yayınlanmamış %d dosya (push başarısız?)" % depo["bekleyen_dosya"])
    if depo.get("push_bekleyen_kayit"):
        sorunlar.append("GitHub'a gitmemiş %d kayıt" % depo["push_bekleyen_kayit"])
    if "HATA: 0 | UYARI: 0" not in kapi:
        sorunlar.append("SEO kapısı: " + kapi)
    # yazar anahtarı: yoksa TrendSaphiens hiç haber yayınlamaz (derleme biçimi kaldırıldı)
    try:
        from . import yazar as _yz
        if not _yz.anahtar():
            sorunlar.append("YAZAR ANAHTARI YOK — TrendSaphiens haber yayınlamıyor. "
                            "GitHub → Settings → Secrets → ANTHROPIC_API_KEY girilmeli.")
    except Exception:
        pass
    # indeks denetimi — indekslenmeyi engelleyen bizden kaynaklı sebepler
    try:
        from . import indeks as _indeks
        ind = _indeks.ozet()
        sorunlar += ind["sorunlar"]
    except Exception as ex:
        ind = {"hata": None, "sorunlar": [], "not": str(ex)[:120]}
        sorunlar.append("indeks denetimi çalışmadı: %s" % str(ex)[:80])
    ozet = {"tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "sayfalar": sayfalar, "sitemap_url": len(urls),
            "sitemap_bugun": len(bugun_sitemap), "depo": depo, "kapi": kapi, "yazar": yazar, "push": push,
            "indeks": {"hata": ind.get("hata"), "uyari": ind.get("uyari"), "kapsam": ind.get("kapsam"),
                       "sc": ind.get("sc", {}).get("tarih"), "dizinde": ind.get("sc", {}).get("indeksli")},
            "sorunlar": sorunlar}
    y = os.path.join(KOK_DIZIN, "veri", "gunluk-kontrol.json")
    try:
        eski = json.load(open(y, encoding="utf-8")) if os.path.exists(y) else []
    except Exception:
        eski = []
    json.dump((eski + [ozet])[-120:], open(y, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ind_satir = ("İndeks: dizinde %s / %s adres (%s okuması) · repo kontrolü %d hata" % (
        ozet["indeks"]["dizinde"], len(urls), ozet["indeks"]["sc"], ozet["indeks"]["hata"] or 0)
        if ozet["indeks"]["dizinde"] else "İndeks: kayıt yok")
    metin = ("Luna günlük kontrol %s\n%s\n%s\nSitemap %d URL, bugün %d · %s · %s\n%s" % (
        ozet["tarih"], kapi, ind_satir, len(urls), len(bugun_sitemap), push,
        "; ".join(yazar) or "yazar: —",
        ("SORUN:\n- " + "\n- ".join(sorunlar)) if sorunlar else "Sorun yok — bugünün sayfaları canlıda."))
    print(metin)
    if bildir:
        try:
            from . import telgraf
            ok, neden = telgraf.hazir()
            if ok:
                telgraf.mesaj(("⚠️ " if sorunlar else "✅ ") + metin.replace("<", "&lt;"), bicim="HTML")
        except Exception as ex:
            print("Telegram bildirimi olmadı:", ex)
    return ozet

if __name__ == "__main__":
    calistir()
