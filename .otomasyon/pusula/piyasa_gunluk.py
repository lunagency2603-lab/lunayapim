# -*- coding: utf-8 -*-
"""
PİYASA GÜNLÜK — "Dolar kaç TL, euro kaç TL, gram altın kaç TL" sayfası için veri.

Kaynaklar:
  · TCMB günlük kur tablosu (resmî):  https://www.tcmb.gov.tr/kurlar/today.xml
      USD, EUR, GBP alış/satış (döviz alış-satış), tarih ve bülten no.
  · Altın: truncgil today.json (anahtarsız, ücretsiz; kaynak adı sayfada yazılır)
      https://finans.truncgil.com/today.json  → "gram-altin", "ceyrek-altin", "ons"

Kurallar: rakam yalnızca kaynaktan; kaynağın kendi zaman damgası sayfada; yorum, hedef,
tavsiye yok. Kaynak cevap vermezse o satır boş kalır ("—"), uydurulmaz.

Çıktı: veri/piyasa/YYYY-MM-DD.json
"""
import datetime, json, os, re
import xml.etree.ElementTree as ET

from .ayarlar import KOK_DIZIN
from .kaynaklar.agir import getir

TCMB = "https://www.tcmb.gov.tr/kurlar/today.xml"
ALTIN = "https://finans.truncgil.com/today.json"


def tcmb():
    try:
        kod, ham, _ = getir(TCMB, zaman_asimi=20)
    except Exception:
        return None
    if kod != 200 or not ham:
        return None
    try:
        kok = ET.fromstring(ham.encode("utf-8", "ignore"))
    except ET.ParseError:
        return None
    out = {"tarih": kok.attrib.get("Tarih", ""), "bulten": kok.attrib.get("Bulten_No", ""), "kurlar": {}}
    for c in kok.findall("Currency"):
        kodu = c.attrib.get("CurrencyCode")
        if kodu in ("USD", "EUR", "GBP", "CHF", "JPY"):
            def f(t):
                v = (c.findtext(t) or "").strip()
                return v if v else ""
            out["kurlar"][kodu] = {"alis": f("ForexBuying"), "satis": f("ForexSelling"),
                                   "efektif_alis": f("BanknoteBuying"), "efektif_satis": f("BanknoteSelling"),
                                   "ad": (c.findtext("Isim") or "").strip()}
    return out


def altin():
    try:
        kod, ham, _ = getir(ALTIN, zaman_asimi=20)
    except Exception:
        return None
    if kod != 200 or not ham:
        return None
    try:
        d = json.loads(ham)
    except Exception:
        return None
    out = {"guncelleme": d.get("Update_Date") or d.get("update_date") or ""}
    for anahtar, ad in (("gram-altin", "Gram altın"), ("ceyrek-altin", "Çeyrek altın"), ("yarim-altin", "Yarım altın"),
                        ("tam-altin", "Tam altın"), ("ons", "Ons altın (USD)"), ("gumus", "Gümüş")):
        v = d.get(anahtar) or d.get(anahtar.replace("-", "_")) or {}
        if isinstance(v, dict) and (v.get("Alış") or v.get("Satış") or v.get("Alis") or v.get("Satis")):
            out[anahtar] = {"ad": ad, "alis": str(v.get("Alış") or v.get("Alis") or ""), "satis": str(v.get("Satış") or v.get("Satis") or ""),
                            "degisim": str(v.get("Değişim") or v.get("Degisim") or "")}
    return out


def _dolu(v):
    """Kayit gercekten veri tasiyor mu? (tcmb kurlari ya da altin satiri)"""
    if not isinstance(v, dict):
        return False
    k = (v.get("tcmb") or {}).get("kurlar") or {}
    a = v.get("altin") or {}
    return bool(k) or bool(a)


def gunluk_uret(tarih=None):
    tarih = tarih or datetime.date.today().isoformat()
    d = os.path.join(KOK_DIZIN, "veri", "piyasa"); os.makedirs(d, exist_ok=True)
    veri = {"tarih": tarih, "tcmb": tcmb(), "altin": altin(), "alindi": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}
    if not _dolu(veri):
        # Ag yoksa bos kayit YAZILMAZ: bos kayit sayfasi uretilmeyen bir gune baglanti dogurur (kirik bag -> SEO kapisi -> push yok).
        yol = os.path.join(d, tarih + ".json")
        if os.path.exists(yol):
            try: os.remove(yol)
            except Exception: pass
        return {"tarih": tarih, "tcmb": False, "altin": False, "kayit": False}
    json.dump(veri, open(os.path.join(d, tarih + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return {"tarih": tarih, "tcmb": bool(veri["tcmb"]), "altin": bool(veri["altin"] and len(veri["altin"]) > 1), "kayit": True}


def son():
    d = os.path.join(KOK_DIZIN, "veri", "piyasa")
    if not os.path.isdir(d):
        return None
    ds = sorted(f for f in os.listdir(d) if re.match(r"\d{4}-\d{2}-\d{2}\.json$", f))
    if not ds:
        return None
    for f in reversed(ds):
        try:
            v = json.load(open(os.path.join(d, f), encoding="utf-8"))
        except Exception:
            continue
        if _dolu(v):
            return v
    return None


def hepsi():
    d = os.path.join(KOK_DIZIN, "veri", "piyasa")
    if not os.path.isdir(d):
        return []
    out = []
    for f in sorted(os.listdir(d)):
        if re.match(r"\d{4}-\d{2}-\d{2}\.json$", f):
            try:
                v = json.load(open(os.path.join(d, f), encoding="utf-8"))
            except Exception:
                continue
            if _dolu(v):
                out.append(v)
    return out
