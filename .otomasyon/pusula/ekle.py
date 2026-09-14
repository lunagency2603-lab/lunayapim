# -*- coding: utf-8 -*-
"""
ELLE FİRMA EKLEME — taramada çıkmayan (ya da Google Haritalar'da olup aramaya yakalanmayan) bir firmayı
web sitesi ya da Haritalar bağlantısıyla aday listesine alır ve tek adımda tam analizden geçirir:
aday kaydı → (Places eşleşmesi varsa puan/yorum/fotoğraf) → eksik tespiti → skor → kazanç tahmini → demo.

Kullanım:
  CLI:   pusula ekle --site https://firma.com [--ad "Firma"] [--sehir Bursa] [--sektor insaat]
                     [--harita "https://maps.app.goo.gl/..."] [--telefon ...]
  Panel: Adaylar → "Bağlantıyla ekle" → POST /api/ekle {site, ad, sehir, sektor, harita, telefon}
Kaynak "elle"; kaynak_id "elle:<alan adı>". Aynı alan adı ikinci kez eklenirse kayıt güncellenir.
"""
import json, re, urllib.parse, html as H
from . import veritabani as vt, ayarlar
from .ayarlar import SEKTORLER
from .kaynaklar import google_places
from .kaynaklar.agir import getir
from .tespit import eksikleri_bul
from .puanlama import skorla, sicak_mi
from .tahmin import hesapla as tahmin_hesapla
from .demo import demo_uret

# sektör tahmini: site metnindeki anahtar kelimeler (SEKTORLER.aramalar + ek ipuçları)
IPUCU = {
    "insaat": ["inşaat", "müteahhit", "konut projesi", "yapı", "şantiye", "daire", "villa projesi"],
    "emlak": ["emlak", "gayrimenkul", "satılık", "kiralık", "danışman"],
    "mimarlik": ["mimarlık", "mimari", "iç mimar", "proje tasarım", "restorasyon"],
    "sanayi": ["sanayi", "üretim", "fabrika", "makine", "imalat", "ihracat", "otomotiv", "tekstil"],
    "mobilya": ["mobilya", "koltuk", "yatak odası", "dekorasyon", "ev tekstili"],
    "otel": ["otel", "hotel", "konaklama", "rezervasyon", "butik otel", "tatil"],
    "isletme": ["restoran", "kafe", "cafe", "kuaför", "güzellik", "salon", "mağaza", "klinik", "spor salonu"],
}

def _alan(site):
    u = site.strip()
    if not re.match(r"^https?://", u, re.I):
        u = "https://" + u
    p = urllib.parse.urlparse(u)
    return u, (p.hostname or "").lower().replace("www.", "")

def _harita_adi(harita):
    """Google Haritalar bağlantısından yer adı (…/maps/place/Ad+Soyad/…)."""
    m = re.search(r"/maps/place/([^/@?]+)", harita or "")
    return urllib.parse.unquote_plus(m.group(1)).strip() if m else ""

def _site_bilgi(url):
    """Ana sayfadan başlık, açıklama ve düz metin (sektör tahmini için)."""
    kod, sayfa, son = getir(url, zaman_asimi=20, basliklar={"Accept": "text/html"})
    if kod != 200 or not sayfa:
        return {"kod": kod, "baslik": "", "metin": ""}
    baslik = re.search(r"<title>(.*?)</title>", sayfa, re.S | re.I)
    metin = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", sayfa, flags=re.S | re.I)
    metin = H.unescape(re.sub(r"<[^>]+>", " ", metin))
    return {"kod": kod, "son": son, "baslik": H.unescape(baslik.group(1)).strip() if baslik else "",
            "metin": re.sub(r"\s+", " ", metin)[:20000].lower()}

def sektor_tahmin(metin):
    puan = {}
    for sk, kelimeler in IPUCU.items():
        puan[sk] = sum(metin.count(k) for k in kelimeler)
    en = max(puan, key=puan.get)
    return (en if puan[en] > 0 else "isletme"), puan

def _ad_temizle(baslik):
    b = re.split(r"\s[|\-–—:]\s", baslik or "")[0].strip()
    return b[:80]

def firma_ekle(site=None, ad=None, sehir=None, sektor=None, harita=None, telefon=None, analiz=True, yaz=print):
    """Döner: {"id", "aday", "yeni", "places", "skor", "eksikler", "demo"}"""
    if not site and not harita:
        raise ValueError("site ya da harita bağlantısı gerekli")
    url, alan = _alan(site) if site else ("", "")
    bilgi = _site_bilgi(url) if url else {"kod": 0, "baslik": "", "metin": ""}
    ad = (ad or "").strip() or _harita_adi(harita) or _ad_temizle(bilgi.get("baslik")) or alan
    sehir = (sehir or "").strip() or "Bursa"
    if not sektor:
        sektor, puan = sektor_tahmin(bilgi.get("metin", "") + " " + ad.lower())
        yaz("  sektör tahmini: %s (%s)" % (SEKTORLER[sektor]["ad"], ", ".join("%s=%d" % (k, v) for k, v in puan.items() if v)))
    if sektor not in SEKTORLER:
        raise ValueError("bilinmeyen sektör: %s (%s)" % (sektor, ", ".join(SEKTORLER)))
    k = {"kaynak": "elle", "kaynak_id": "elle:" + (alan or re.sub(r"\W+", "-", ad.lower())), "ad": ad, "sektor": sektor,
         "sehir": sehir, "ilce": "", "adres": "", "telefon": telefon, "site": url or None,
         "puan": None, "yorum_sayisi": 0, "fotograf_sayisi": 0, "enlem": None, "boylam": None}
    places = None
    # Google Haritalar eşleşmesi: ad + şehir ile Places araması, alan adı ya da ad benzerliğiyle seç
    if ayarlar.GOOGLE_ANAHTAR:
        try:
            for p in google_places.ara(ad, sehir, sayfa_basi=5, azami=5):
                p_alan = _alan(p["site"])[1] if p.get("site") else ""
                if (alan and p_alan == alan) or p["ad"].lower()[:20] == ad.lower()[:20]:
                    places = p; break
        except Exception as ex:
            yaz("  Places araması olmadı: %s" % ex)
    if places:
        for alan_adi in ("adres", "telefon", "puan", "yorum_sayisi", "fotograf_sayisi", "enlem", "boylam", "ilce"):
            if places.get(alan_adi) not in (None, "", 0):
                k[alan_adi] = places[alan_adi]
        k["kaynak_id"] = places["kaynak_id"]; k["kaynak"] = "google"
        if not k["site"] and places.get("site"):
            k["site"] = places["site"]
        yaz("  Haritalar eşleşti: %s · puan %s · %s yorum · %s fotoğraf" % (places["ad"], places.get("puan"), places.get("yorum_sayisi"), places.get("fotograf_sayisi")))
    else:
        yaz("  Haritalar eşleşmesi yok%s — site üzerinden analiz" % ("" if ayarlar.GOOGLE_ANAHTAR else " (Google anahtarı boş)"))
    b = vt.baglan()
    yeni = vt.aday_ekle(b, k); b.commit()
    r = b.execute("SELECT * FROM adaylar WHERE kaynak_id=?", (k["kaynak_id"],)).fetchone()
    aday = dict(r); sonuc = {"id": aday["id"], "aday": aday, "yeni": yeni, "places": bool(places), "site_kodu": bilgi.get("kod")}
    yaz("  aday #%d %s (%s, %s) %s" % (aday["id"], aday["ad"], sehir, SEKTORLER[sektor]["ad"], "yeni" if yeni else "güncellendi"))
    if analiz:
        eks, det = eksikleri_bul(aday)
        skor = skorla(eks); vt.denetim_kaydet(b, aday["id"], skor, eks, det); b.commit()
        satir = [x for x in vt.son_denetimler(b, sehir, sektor) if x["id"] == aday["id"]][0]
        t = tahmin_hesapla(satir, eks); vt.tahmin_kaydet(b, aday["id"], t); t["_skor"] = skor
        dosya, mesaj = demo_uret(satir, eks, det, t); vt.demo_kaydet(b, aday["id"], dosya, mesaj); b.commit()
        sonuc.update({"skor": skor, "sicak": sicak_mi(skor), "eksikler": eks, "detay": det, "tahmin": t, "demo": dosya})
        yaz("  skor %d %s · %d eksik: %s" % (skor, "SICAK" if sicak_mi(skor) else "", len(eks), ", ".join(eks)))
        yaz("  demo → %s" % dosya)
    b.close()
    return sonuc
