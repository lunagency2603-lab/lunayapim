# -*- coding: utf-8 -*-
"""
MALİYET VE FİYAT DENETİMİ

Üç rakamı yan yana koyar ve tutarsızlığı söyler:
  1) BİZİM MALİYETİMİZ   — emek + ulaşım + abonelik + genel gider payı
  2) SİTEDE YAYINLADIĞIMIZ BAND — hizmet sayfalarından canlı okunur (uydurulmaz)
  3) PİYASA BANDI        — piyasa.py'deki kaynaklı derleme

Sonra üç soruyu cevaplar:
  · Piyasanın altında mıyız?
  · Maliyetin üstünde miyiz? (alt banttan iş alırsak zarar var mı)
  · Sitede yazan fiyatla panelin önerdiği fiyat aynı mı?

MALİYET GİRDİLERİ VARSAYIMDIR. Gerçek rakamları GIRDI sözlüğüne yaz —
hesap otomatik yeniden çıkar. Uydurma yapmamak için her varsayımın yanında
nereden geldiği duruyor.
"""
import os, re, json, datetime

from . import piyasa
from .ayarlar import SITE_KOK

# ------------------------------------------------------------------ girdiler
# Hepsi DÜZENLENEBİLİR varsayımdır. Kendi rakamlarını yaz.
GIRDI = {
 "ekip_kisi":         2,        # varsayım: iki kişilik çekirdek ekip
 "aylik_sabit_tl":    45000,    # varsayım: yazılım abonelikleri + ofis + iletişim
 "amortisman_ay_tl":  12000,    # varsayım: kamera, drone, ışık, bilgisayar aylık payı
 "ay_calisma_saat":   320,      # varsayım: 2 kişi × ~160 saat
 "cekim_gun_ek_tl":   3500,     # varsayım: çekim günü ek gideri (yemek, sarf, sigorta payı)
 "km_basi_tl":        14,       # varsayım: yakıt + aşınma
 "muzik_lisans_tl":   1200,     # varsayım: iş başına lisanslı müzik
 "usd_try":           42.0,     # varsayım: panelden güncelle
 "genel_gider_yuzde": 12,       # muhasebe, banka, tahsilat riski
 "hedef_kar_yuzde":   45,       # hedeflenen brüt kâr
}

# Emek tahminleri — sitede YAYINLADIĞIMIZ teslim taahhütlerine dayanıyor.
# (kaynak: hizmet sayfalarındaki "ne veriyoruz" maddeleri)
EMEK = {
 "insaat-3d-modelleme": {"ad": "İnşaat 3D modelleme",
   "hazirlik_saat": 8, "cekim_gun": 0, "yapim_saat": 60, "revizyon_saat": 12,
   "km": 0, "ai_usd": 12, "taseron_tl": 0,
   "dayanak": "6–10 görsel + 45 sn animasyon, 5–10 iş günü teslim"},
 "emlak-video": {"ad": "Emlak / kurumsal video",
   "hazirlik_saat": 4, "cekim_gun": 1, "yapim_saat": 16, "revizyon_saat": 4,
   "km": 60, "ai_usd": 0, "taseron_tl": 0,
   "dayanak": "çekimden sonra 3–7 iş günü, portal + sosyal iki sürüm"},
 "urun-animasyon": {"ad": "3D ürün / hizmet animasyonu",
   "hazirlik_saat": 10, "cekim_gun": 0, "yapim_saat": 80, "revizyon_saat": 16,
   "km": 0, "ai_usd": 18, "taseron_tl": 0,
   "dayanak": "teknik çizim hazırsa 3–5 hafta, TR/EN/DE sürümler"},
 "klip-cekimi": {"ad": "Klip çekimi",
   "hazirlik_saat": 14, "cekim_gun": 1, "yapim_saat": 34, "revizyon_saat": 8,
   "km": 80, "ai_usd": 6, "taseron_tl": 0,
   "dayanak": "24 plan, tek çekim günü, üç format, renk + ses ayrı"},
 "drone-cekimi": {"ad": "Drone / FPV çekim",
   "hazirlik_saat": 3, "cekim_gun": 1, "yapim_saat": 8, "revizyon_saat": 2,
   "km": 70, "ai_usd": 0, "taseron_tl": 0,
   "dayanak": "izin takibi bizde, yedek gün ek ücretsiz"},
 "dugun-cekimi": {"ad": "Düğün / etkinlik",
   "hazirlik_saat": 5, "cekim_gun": 1, "yapim_saat": 30, "revizyon_saat": 5,
   "km": 90, "ai_usd": 0, "taseron_tl": 6000,
   "dayanak": "çok kamera, uzun film + kısa sürüm + sosyal kesitler, ham kayıt teslim"},
 "isletme-tanitim": {"ad": "İşletme tanıtım (aylık)",
   "hazirlik_saat": 4, "cekim_gun": 1, "yapim_saat": 20, "revizyon_saat": 4,
   "km": 50, "ai_usd": 4, "taseron_tl": 0,
   "dayanak": "tek çekim gününden 10–12 içerik, aylık ölçüm"},
}

# Panelin teklifte önerdiği band (musteri.ONERI ile aynı kalmalı)
PANEL_BAND = {
 "insaat-3d-modelleme": (65000, 185000),
 "emlak-video":         (9000, 28000),
 "urun-animasyon":      (38000, 120000),
 "klip-cekimi":         (45000, 140000),
 "drone-cekimi":        (12000, 45000),
 "dugun-cekimi":        (28000, 75000),
 "isletme-tanitim":     (12000, 30000),
}

# hizmet anahtarı -> site sayfası (band buradan CANLI okunur)
SITE_SAYFA = {
 "insaat-3d-modelleme": "hizmetler/insaat-3d-modelleme.html",
 "emlak-video":         "hizmetler/emlak-kurumsal.html",
 "urun-animasyon":      "hizmetler/urun-animasyon.html",
 "klip-cekimi":         "hizmetler/klip-cekimi.html",
 "drone-cekimi":        "hizmetler/drone-fpv.html",
 "isletme-tanitim":     "hizmetler/isletme-tanitim.html",
 "dugun-cekimi":        "hizmetler/dugun-etkinlik.html",
}

_BAND = re.compile(r"(\d{1,3})\s*[–-]\s*(\d{1,3})\s*bin\s*₺")


def site_bandi(hizmet, kok=None):
    """Sitede yayınlanmış bandı sayfadan okur. Yoksa None — uydurmaz."""
    kok = kok or SITE_KOK
    yol = SITE_SAYFA.get(hizmet)
    if not kok or not yol:
        return None
    tam = os.path.join(kok, yol)
    if not os.path.exists(tam):
        return None
    try:
        s = open(tam, encoding="utf-8").read()
    except Exception:
        return None
    m = _BAND.search(s)
    if not m:
        return None
    return (int(m.group(1)) * 1000, int(m.group(2)) * 1000)


# ------------------------------------------------------------------ maliyet
def saatlik():
    """Yüklenmiş saatlik maliyet: sabit gider + amortisman / çalışma saati."""
    g = GIRDI
    return (g["aylik_sabit_tl"] + g["amortisman_ay_tl"]) / max(1, g["ay_calisma_saat"])


def maliyet(hizmet):
    """Bir işin bize maliyeti — kalem kalem."""
    e = EMEK.get(hizmet)
    if not e:
        return None
    g = GIRDI
    sa = saatlik()
    saat = e["hazirlik_saat"] + e["yapim_saat"] + e["revizyon_saat"]
    emek = saat * sa
    cekim = e["cekim_gun"] * g["cekim_gun_ek_tl"]
    yol = e["km"] * g["km_basi_tl"]
    ai = e["ai_usd"] * g["usd_try"]
    muzik = g["muzik_lisans_tl"] if e["cekim_gun"] or hizmet in ("urun-animasyon", "insaat-3d-modelleme") else 0
    taseron = e["taseron_tl"]
    dogrudan = emek + cekim + yol + ai + muzik + taseron
    genel = dogrudan * g["genel_gider_yuzde"] / 100.0
    toplam = dogrudan + genel
    return {
        "hizmet": hizmet, "ad": e["ad"], "saat": saat, "saatlik": round(sa),
        "kalemler": [
            ("Emek (%d saat × %d ₺)" % (saat, round(sa)), round(emek)),
            ("Çekim günü gideri (%d gün)" % e["cekim_gun"], round(cekim)),
            ("Ulaşım (%d km)" % e["km"], round(yol)),
            ("Yapay zekâ / bulut (%d $)" % e["ai_usd"], round(ai)),
            ("Müzik lisansı", round(muzik)),
            ("Taşeron / ek ekip", round(taseron)),
            ("Genel gider payı (%%%d)" % g["genel_gider_yuzde"], round(genel)),
        ],
        "dogrudan": round(dogrudan), "toplam": round(toplam),
        "asgari_fiyat": round(toplam / (1 - g["hedef_kar_yuzde"] / 100.0)),
        "dayanak": e["dayanak"],
    }


def karsilastir(hizmet, kok=None):
    """Maliyet, site bandı, panel bandı ve piyasa bandını yan yana koyar."""
    m = maliyet(hizmet)
    if not m:
        return None
    p = piyasa.PIYASA.get(hizmet, {})
    piy = (p.get("alt"), p.get("ust")) if p else (None, None)
    site = site_bandi(hizmet, kok)
    panel = PANEL_BAND.get(hizmet)
    uyari = []

    if panel and piy[0] is not None:
        if panel[0] > piy[0]:
            uyari.append("Panel alt bandı (%s) piyasa alt bandının (%s) ÜSTÜNDE — "
                         "en ucuz teklifte rakip daha ucuz görünüyor."
                         % (_tl(panel[0]), _tl(piy[0])))
        if panel[1] > piy[1]:
            uyari.append("Panel üst bandı (%s) piyasa üst bandını (%s) AŞIYOR."
                         % (_tl(panel[1]), _tl(piy[1])))
    if site and panel:
        if abs(site[0] - panel[0]) > max(2000, site[0] * 0.10):
            uyari.append("Sitede yazan alt fiyat (%s) ile panelin önerdiği alt fiyat (%s) "
                         "TUTMUYOR — müşteri ikisini de görüyor."
                         % (_tl(site[0]), _tl(panel[0])))
        if abs(site[1] - panel[1]) > max(2000, site[1] * 0.10):
            uyari.append("Sitede yazan üst fiyat (%s) ile panelin önerdiği üst fiyat (%s) "
                         "TUTMUYOR." % (_tl(site[1]), _tl(panel[1])))
    if site and site[0] < m["asgari_fiyat"]:
        uyari.append("Sitedeki alt fiyat (%s) hedef kârlı asgari fiyatın (%s) ALTINDA — "
                     "o banttan iş alırsak kâr hedefin altına düşüyor."
                     % (_tl(site[0]), _tl(m["asgari_fiyat"])))
    if site and site[0] < m["toplam"]:
        uyari.append("DİKKAT: sitedeki alt fiyat (%s) maliyetin (%s) altında — zarar."
                     % (_tl(site[0]), _tl(m["toplam"])))

    def marj(fiyat):
        if not fiyat:
            return None
        return round((fiyat - m["toplam"]) / fiyat * 100)

    return {
        "hizmet": hizmet, "ad": m["ad"], "maliyet": m["toplam"],
        "asgari_fiyat": m["asgari_fiyat"],
        "site": site, "panel": panel, "piyasa": piy,
        "marj_site_alt": marj(site[0]) if site else None,
        "marj_site_ust": marj(site[1]) if site else None,
        "piyasa_altinda_mi": (bool(site) and piy[1] is not None and site[1] <= piy[1]
                              and site[0] <= piy[0] * 1.05),
        "uyari": uyari, "detay": m,
    }


def _tl(x):
    try:
        return "{:,}".format(int(round(float(x)))).replace(",", ".") + " ₺"
    except Exception:
        return "—"


def tablo(kok=None):
    return [karsilastir(h, kok) for h in EMEK]


def rapor(kok=None):
    """Okunur metin raporu."""
    sat = ["# Maliyet ve fiyat denetimi",
           "", "Tarih: %s" % datetime.date.today().strftime("%d.%m.%Y"),
           "Piyasa derlemesi: %s (kaynaklar piyasa.py içinde)" % piyasa.DERLEME_TARIHI,
           "", "Saatlik yüklenmiş maliyet: **%s** "
           "(aylık sabit %s + amortisman %s ÷ %d saat)"
           % (_tl(saatlik()), _tl(GIRDI["aylik_sabit_tl"]),
              _tl(GIRDI["amortisman_ay_tl"]), GIRDI["ay_calisma_saat"]),
           "", "> Maliyet girdileri VARSAYIMDIR. `maliyet.GIRDI` içinden düzelt.", ""]
    sat.append("| Hizmet | Maliyet | Asgari fiyat (%%%d kâr) | Sitede | Panel | Piyasa | Alt marj |"
               % GIRDI["hedef_kar_yuzde"])
    sat.append("|---|---|---|---|---|---|---|")
    for k in tablo(kok):
        if not k:
            continue
        sat.append("| %s | %s | %s | %s | %s | %s | %s |" % (
            k["ad"], _tl(k["maliyet"]), _tl(k["asgari_fiyat"]),
            "%s–%s" % (_tl(k["site"][0]), _tl(k["site"][1])) if k["site"] else "—",
            "%s–%s" % (_tl(k["panel"][0]), _tl(k["panel"][1])) if k["panel"] else "—",
            "%s–%s" % (_tl(k["piyasa"][0]), _tl(k["piyasa"][1])) if k["piyasa"][0] else "—",
            ("%%%d" % k["marj_site_alt"]) if k["marj_site_alt"] is not None else "—"))
    sat += ["", "## Uyarılar", ""]
    var = False
    for k in tablo(kok):
        if k and k["uyari"]:
            var = True
            sat.append("**%s**" % k["ad"])
            for u in k["uyari"]:
                sat.append("- %s" % u)
            sat.append("")
    if not var:
        sat.append("Uyarı yok — bantlar tutarlı ve piyasanın altında.")
    sat += ["", "## Kalem kalem maliyet", ""]
    for h in EMEK:
        m = maliyet(h)
        sat.append("### %s" % m["ad"])
        sat.append("_Dayanak: %s_" % m["dayanak"])
        sat.append("")
        for ad, tut in m["kalemler"]:
            if tut:
                sat.append("- %s → %s" % (ad, _tl(tut)))
        sat.append("- **Toplam maliyet → %s**" % _tl(m["toplam"]))
        sat.append("- Hedef kârla asgari satış → **%s**" % _tl(m["asgari_fiyat"]))
        sat.append("")
    return "\n".join(sat)
