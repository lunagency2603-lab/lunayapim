# -*- coding: utf-8 -*-
"""
YAZAR — gündem maddesinden intihalsiz, kaynaklı haber-analiz yazısı.

Yöntem cikti/yazim-rehberi.md §3: kaynaktan yalnız OLGULAR gelir (kaynak_ozet), iskelet arayanın
sorusundan kurulur, metin bizim; tek kısa alıntı; "Bizim tarafımız" ve "Ne yapmalı" bölümleri zorunlu.
Yazan model: Anthropic Messages API (anahtar Panel → Ayarlar → Yazar; ayarlar.json "yazar_anahtar",
model "yazar_model"). Anahtar yoksa hiçbir şey yazılmaz — sayfa "kaynak alıntısı + okuma" biçiminde kalır.
Her yazı intihal denetiminden (pusula/intihal.py) geçer; geçmeyen atılır, log'a düşer.
Sadece standart kütüphane.
"""
import json, os, re, urllib.request, urllib.error
from .ayarlar import _OZEL, KOK_DIZIN
from . import intihal

API = "https://api.anthropic.com/v1/messages"
VARSAYILAN_MODEL = "claude-sonnet-4-5"

def anahtar():
    return (_OZEL.get("yazar_anahtar") or os.environ.get("ANTHROPIC_API_KEY", "")).strip()

def model():
    return (_OZEL.get("yazar_model") or VARSAYILAN_MODEL).strip()

# fiyat bantları: fiyatlar.html "Luna Yapım" sütunuyla aynı
FIYAT = {
    "hizmetler/insaat-3d-modelleme.html": "İnşaat 3D modelleme / mimari görselleştirme 45.000 – 150.000 ₺ (tek blok render seti + kısa animasyon)",
    "hizmetler/emlak-kurumsal.html": "Emlak video çekimi 2.500 – 12.000 ₺ (portföy başına); kurumsal tanıtım filmi 25.000 – 55.000 ₺",
    "hizmetler/urun-animasyon.html": "3D ürün animasyonu 40.000 – 95.000 ₺ (modelleme + animasyon + ses)",
    "hizmetler/drone-fpv.html": "Drone çekimi (tek iş) 10.000 – 25.000 ₺ (yarım gün çekim + kurgu)",
    "hizmetler/isletme-tanitim.html": "İşletme / sosyal medya aylık üretim 14.000 – 40.000 ₺; tanıtım filmi 25.000 – 55.000 ₺",
    "hizmetler/klip-cekimi.html": "Klip çekimi 35.000 – 100.000 ₺ (senaryolu, çok planlı)",
}

SISTEM = """Sen Luna Yapım'ın (Bursa, iki kişilik prodüksiyon + yazılım stüdyosu) yazı editörüsün. Türkçe, profesyonel,
abartısız, gazete dili; ünlem yok, "dev", "muhteşem" gibi sıfatlar yok. Bir sektör haberinden, o sektördeki
işletmelere yönelik kısa bir HABER-ANALİZ yazısı yazarsın.

KURALLAR (ihlal edersen yazı çöpe gider):
1. YALNIZ verilen olguları kullan. Verilmeyen hiçbir rakam, tarih, isim, kurum, oran yazma. Genel bilgi
   ekleyeceksen "genel olarak", "sektörde yaygın uygulama" gibi işaretle ve rakam verme.
2. Kaynak cümlelerini kopyalama, yeniden sözcüklerle de yazma. Olguyu kendi cümlenle, kendi sıranla anlat.
   Kaynağın cümle yapısını izleme. Tek doğrudan alıntıya izin var: en çok bir cümle, "alinti" alanında.
3. Rakamlar kaynakta geçtiği gibi (6.445 m², %17, 123.603) — yuvarlama yok, tahmin yok.
4. "Bizim tarafımız" bölümü Luna Yapım'ın deneyimi ve verilen fiyat bandıyla yazılır; ekip kalabalığı ima etme
   (iki kişilik stüdyo), müşteri adı uydurma, "yüzlerce proje" gibi iddia yok. Yatırım tavsiyesi yok.
5. "Ne yapmalı" okuyucuya (o sektördeki işletme sahibine) 3 somut adım; her adım bir cümle.
6. Başlık: olgu + rakam varsa rakam; soru başlığı olabilir; ≤ 70 karakter; tıklama tuzağı yok.
7. Uzunluk 450–700 kelime. Paragraf ≤ 60 kelime. H2'ler soru ya da aranan kalıp ("… ne anlama geliyor").
8. Yalnız JSON döndür, başka hiçbir şey yazma. Şema:
{"baslik": str, "meta": str (110-150 karakter), "giris": str (2 cümle),
 "bolumler": [{"h2": str, "paragraflar": [str, ...]}, ...] (3-4 bölüm: Ne oldu / Kimi etkiler / Bizim tarafımız / isteğe bağlı Rakamlar),
 "alinti": {"metin": str, "kaynak": str} | null,
 "ne_yapmali": [str, str, str],
 "sss": [{"soru": str, "cevap": str}, {"soru": str, "cevap": str}]}"""

def _istek(sistem, kullanici, azami=2200):
    veri = json.dumps({"model": model(), "max_tokens": azami, "system": sistem,
                       "messages": [{"role": "user", "content": kullanici}]}).encode("utf-8")
    istek = urllib.request.Request(API, data=veri, headers={
        "x-api-key": anahtar(), "anthropic-version": "2023-06-01", "content-type": "application/json"})
    with urllib.request.urlopen(istek, timeout=90) as c:
        y = json.loads(c.read().decode("utf-8"))
    return "".join(p.get("text", "") for p in y.get("content", []) if p.get("type") == "text")

def _json_ayikla(t):
    t = t.strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t, flags=re.S)
    i, j = t.find("{"), t.rfind("}")
    return json.loads(t[i:j + 1])

def olgu_paketi(m):
    """Yazara giden girdi: kaynak olguları + bizim bağlamımız."""
    return {
        "haber_basligi": m.get("baslik", ""),
        "kaynak": {"ad": m.get("kaynak_ad", ""), "url": m.get("kaynak_url", ""), "tarih": m.get("kaynak_tarih", "")},
        "kaynak_olgulari": [x for x in (m.get("olgu", ""), m.get("ek", "")) if x],
        "hedef_okur": m.get("hizmet_ad", "") + " hizmeti alabilecek işletme sahipleri",
        "bizim_hizmet": m.get("hizmet_ad", ""),
        "bizim_soz": m.get("hizmet_soz") or m.get("aci", ""),
        "fiyat_bandi": FIYAT.get(m.get("hizmet", ""), ""),
        "analiz_sorusu": m.get("aci_soru", ""),
        "surec": "keşif ve teklif aynı gün, çekim/modelleme, kurgu-renk, yatay/dikey/kare teslim; teslimde hangi karenin gerçek çekim hangisinin üretim olduğu yazılı",
    }

def yaz(m):
    """Maddeye 'yazi' ekler (intihal denetimi geçerse). Anahtar yoksa None."""
    if not anahtar():
        return None
    paket = olgu_paketi(m)
    if not paket["kaynak_olgulari"]:
        return None
    metin = _istek(SISTEM, "OLGULAR VE BAĞLAM (JSON):\n" + json.dumps(paket, ensure_ascii=False, indent=1) +
                   "\n\nBu olgulardan rehbere uygun haber-analiz yazısını JSON olarak yaz.")
    try:
        y = _json_ayikla(metin)
    except Exception as ex:
        return {"hata": "json: %s" % ex}
    # intihal: yazının düz metni kaynak olgu metinleriyle karşılaştırılır (alıntı hariç)
    duz = " ".join([y.get("giris", "")] + [p for b in y.get("bolumler", []) for p in b.get("paragraflar", [])] +
                   y.get("ne_yapmali", []) + [s.get("cevap", "") for s in y.get("sss", [])])
    r = intihal.denetle(duz, paket["kaynak_olgulari"])
    y["intihal"] = {"kapsama": r["kapsama"], "en_uzun": r["en_uzun"], "gecti": r["gecti"]}
    kelime = len(re.findall(r"\w+", duz))
    y["kelime"] = kelime
    if not r["gecti"] or kelime < 380:
        y["hata"] = "intihal/uzunluk: %s, %d kelime" % (intihal.rapor(r), kelime)
        return y
    m["yazi"] = y
    return y

def yaz_hepsi(maddeler, log=print):
    n = 0
    for m in maddeler:
        try:
            y = yaz(m)
        except urllib.error.HTTPError as ex:
            log("Yazar API hatası %s: %s" % (ex.code, ex.read()[:200])); break
        except Exception as ex:
            log("Yazar hatası: %s" % ex); continue
        if y is None:
            continue
        if y.get("hata"):
            log("Yazı atıldı (%s): %s" % (m.get("baslik", "")[:50], y["hata"]))
        else:
            n += 1; log("Yazı hazır (%d kelime, örtüşme %%%.1f): %s" % (y["kelime"], y["intihal"]["kapsama"] * 100, y["baslik"]))
    return n
