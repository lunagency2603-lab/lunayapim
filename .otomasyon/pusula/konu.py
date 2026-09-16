# -*- coding: utf-8 -*-
"""
KONU FABRİKASI — Türkiye'nin çok aradığı her konu için kendi yazdığımız, tekil sayfa.

Akış (her turda, 16.09.2026):
  1. Aday: günün Google Trends listesi (veri/trend/<gün>.json → "aranan") + her geniş bölümün
     (müzik, edebiyat, spor, dizi-film, sanat, teknoloji, haber…) en yeni başlığı.
  2. Olgu: konu Google Haberler'de aranır; en az İKİ farklı yayıncının sayfasından olgu paragrafı
     çıkarılır (kaynak_ozet). İki bağımsız kaynak yoksa sayfa AÇILMAZ — tek kaynaklı özet yazı olmaz.
  3. Yazı: yazar.py (Anthropic) arayanın sorusunu cevaplayan açıklayıcı haber yazar; intihal kapısı
     bütün kaynak metinlerine karşı çalışır. Geçmeyen atılır, defterde görünür.
  4. Görsel: gorsel_bul — Wikimedia Commons / Openverse, yalnız serbest lisans; künye sayfada basılır.
     Bulunamazsa bölümün kendi görseli kullanılır. Görsel ÜRETİLMEZ.
  5. Kayıt: veri/konu/<gün>/<slug>.json → trend.py her yayında bunları haber sayfası olarak basar.

Kapılar:
  · Hassas konu (ölüm, suç, kaza, saldırı, hastalık…) otomatik yazılmaz — insan kararı ister.
  · Aynı konu 7 gün içinde ikinci kez yazılmaz.
  · Tur başına üst sınır (KONU_AZAMI, varsayılan 4) — maliyet ve kalite için.
Sadece standart kütüphane (Pillow varsa görsel küçültülür).
"""
import datetime, json, os, re, unicodedata, urllib.parse

from .ayarlar import KOK_DIZIN, SITE_KOK
from . import yazar as YZ

DIZIN = os.path.join(KOK_DIZIN, "veri", "konu")
KAYIT_DIZIN = os.path.join(DIZIN, "_dizin.json")
TEKRAR_GUN = 7

# trend_izle bölüm anahtarı → TrendSaphiens kategorisi
KAT = {"piyasalar": "piyasa", "ekran": "ekran", "spor": "spor", "sanat": "sanat", "yapay-zeka": "teknoloji",
       "yazilim": "teknoloji", "muhendislik": "muhendislik", "sosyal-medya": "sosyal-medya",
       "muzik": "muzik", "edebiyat": "edebiyat", "haber": "haber", "gundem": "haber"}

HASSAS = re.compile(
    r"\b(öldü|ölü|ölüm|ölen|hayatını kaybet|vefat|cenaze|cinayet|öldür|intihar|tecavüz|taciz|istismar|"
    r"kaza(?:da|sı|sında|yla|lar)?\b|yaralı|saldırı|terör|patlama|bıçak|silahlı|tutukla|gözaltı|firari|"
    r"kayıp çocuk|kaçırıl|hastaneye kaldır|kanser|salgın|zehirlen)", re.I)

KONU_SISTEM = """Sen TrendSaphiens'in (trendsaphiens.com — Luna Yapım'ın haber ve analiz yayını) editörüsün.
Türkiye'de bugün çok aranan bir konuyu, arama kutusuna o kelimeyi yazıp gelen okurun sorusunu doğrudan
cevaplayan ÖZGÜN bir açıklayıcı haber yazısına çevirirsin. Türkçe, sade, gazete dili; ünlem yok,
"şok", "olay", "dev", "muhteşem" gibi sözcük yok.

KURALLAR (ihlal edersen yazı çöpe gider):
1. YALNIZ verilen olguları kullan. Olgularda olmayan rakam, tarih, isim, kurum, skor, oran, alıntı YAZMA.
   Genel arka plan bilgisi verirsen rakamsız ve "genel olarak" diye işaretle.
2. Kaynak cümlelerini kopyalama, yeniden sözcüklerle de yazma. Farklı kaynakların olgularını birleştir,
   kendi sıranla, kendi cümlenle anlat. Tek doğrudan alıntıya izin var: en çok bir cümle, "alinti" alanında.
3. Kaynaklar çelişiyorsa bunu açıkça yaz ve hangisinin ne dediğini kaynak adıyla belirt.
4. İlk paragraf ("giris") arayanın sorusunu iki cümlede cevaplar: ne oldu, neden şimdi konuşuluyor.
5. Bölümler (3-4): "Ne oldu?" · "Neden bu kadar arandı?" · "Bilinenler ve henüz bilinmeyenler"
   (olgularda olmayanı "henüz açıklanmadı" diye yaz, tahmin etme) · isteğe bağlı "Sırada ne var?"
   (yalnız olgularda tarih/adım varsa). H2'leri okurun soracağı biçimde, konunun adını geçirerek yaz.
6. Siyasi konularda taraf tutma, değerlendirme yapma; açıklamaları sahibine atfet ("... açıkladı").
7. Kişiler hakkında olgularda olmayan hiçbir iddia, niteleme ya da yorum yok.
8. Başlık: konunun aranan kelimesini içerir, ≤ 70 karakter, soru olabilir, tıklama tuzağı yok.
9. Uzunluk 420–650 kelime. Paragraf ≤ 60 kelime.
10. "izle": okurun konuyu takip etmek için bakacağı 3 somut yer ya da adım (resmî duyuru kanalı, yayın
    saati, bilet/başvuru sayfasının ADI — adres uydurma). Olgularda dayanağı yoksa genel ama doğru yaz.
11. Yalnız JSON döndür, başka hiçbir şey yazma. Şema:
{"baslik": str, "meta": str (120-155 karakter), "giris": str,
 "bolumler": [{"h2": str, "paragraflar": [str, ...]}, ...],
 "alinti": {"metin": str, "kaynak": str} | null,
 "izle": [str, str, str],
 "sss": [{"soru": str, "cevap": str}, {"soru": str, "cevap": str}, {"soru": str, "cevap": str}]}"""


def _norm(t):
    t = (t or "").replace("ı", "i").replace("İ", "i")
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def _slug(t):
    return re.sub(r"\s+", "-", _norm(t))[:70].rstrip("-")


def _dizin():
    try:
        return json.load(open(KAYIT_DIZIN, encoding="utf-8"))
    except Exception:
        return {}


def _dizin_yaz(d):
    os.makedirs(DIZIN, exist_ok=True)
    json.dump(d, open(KAYIT_DIZIN, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)


def yakin_zamanda_yazildi(terim, bugun=None):
    bugun = bugun or datetime.date.today()
    k = _dizin().get(_norm(terim))
    if not k:
        return False
    try:
        return (bugun - datetime.date.fromisoformat(k["tarih"])).days < TEKRAR_GUN
    except Exception:
        return False


def terim_sayfasi(terim):
    """Bugün Aranan listesinden kendi yazımıza bağlamak için: terim → slug (yoksa None)."""
    k = _dizin().get(_norm(terim))
    return k.get("slug") if k else None


def adaylar(tarih=None):
    """[{terim, hacim, kat, ipucu}] — önce arama listesi (hacme göre), sonra bölüm başlıkları."""
    from . import trend_izle as TI
    v = TI.son(tarih) or {}
    out, gorulen = [], set()

    def _hacim(h):
        m = re.search(r"([\d.]+)", (h or "").replace(",", ""))
        return int(m.group(1).replace(".", "")) if m else 0

    for a in sorted(v.get("aranan") or [], key=lambda x: -_hacim(x.get("hacim"))):
        t = (a.get("baslik") or "").strip()
        if not t or _norm(t) in gorulen:
            continue
        gorulen.add(_norm(t))
        bolum = TI.bolum_bul(t + " " + (a.get("haber_baslik") or ""))
        out.append({"terim": t, "hacim": a.get("hacim") or "", "kat": KAT.get(bolum, "haber"),
                    "ipucu": a.get("haber_baslik") or "", "kaynak_tur": "arama"})
    # geniş bölümlerden: her bölümün en yeni başlığı (arama listesine hiç düşmeyen alanlar da temsil edilsin)
    for bolum, liste in (v.get("bolumler") or {}).items():
        for h in (liste or [])[:1]:
            t = re.sub(r"\s+-\s+[^-]{2,40}$", "", h.get("baslik") or "").strip()   # " - Yayıncı" kuyruğu
            if not t or _norm(t) in gorulen:
                continue
            gorulen.add(_norm(t))
            out.append({"terim": t, "hacim": "", "kat": KAT.get(bolum, "haber"), "ipucu": "", "kaynak_tur": "bolum"})
    return out


def olgular(terim, ipucu="", azami_kaynak=4):
    """Konu için farklı yayıncılardan olgu paragrafları. [{ad, tarih, baslik, olgu}]"""
    from .gundem import rss_cek, GOOGLE_HABER
    from . import kaynak_ozet as KO
    sorgu = '"%s" when:3d' % terim if len(terim) < 60 else terim
    try:
        haberler = rss_cek(GOOGLE_HABER % urllib.parse.quote(sorgu), 12)
    except Exception:
        haberler = []
    if not haberler and ipucu:
        try:
            haberler = rss_cek(GOOGLE_HABER % urllib.parse.quote(ipucu), 8)
        except Exception:
            haberler = []
    out, yayincilar = [], set()
    for h in haberler:
        ad = (h.get("kaynak") or "").strip() or "Haber"
        if _norm(ad) in yayincilar:
            continue
        try:
            s = KO.sayfa_ozeti(h.get("adres", ""))
        except Exception:
            continue
        olgu = (s.get("olgu") or "").strip()
        if len(olgu) < KO.ASGARI:
            continue
        yayincilar.add(_norm(ad))
        out.append({"ad": ad, "tarih": h.get("tarih") or s.get("tarih") or "", "baslik": re.sub(r"\s+-\s+[^-]{2,40}$", "", h.get("baslik", "")),
                    "olgu": olgu, "ek": (s.get("ek") or "").strip()})
        if len(out) >= azami_kaynak:
            break
    return out


def _paket(aday, kaynaklar):
    return {
        "aranan_konu": aday["terim"],
        "arama_hacmi": aday.get("hacim") or "belirtilmedi",
        "bolum": aday["kat"],
        "bugun": datetime.date.today().isoformat(),
        "kaynaklar": [{"yayinci": k["ad"], "tarih": k["tarih"], "haber_basligi": k["baslik"]} for k in kaynaklar],
        "kaynak_olgulari": ["[%s] %s %s" % (k["ad"], k["olgu"], k["ek"]) for k in kaynaklar],
    }


def _kat_ad(kat):
    try:
        from .trend import KATEGORI
        return KATEGORI.get(kat, ("Haber",))[0]
    except Exception:
        return "Haber"


def yaz_konu(aday, log=print):
    """Tek konu: olgu → yazı → görsel → kayıt. Döner: kayıt dict'i ya da None."""
    terim = aday["terim"]
    if HASSAS.search(terim + " " + aday.get("ipucu", "")):
        YZ.kaydet({"olay": "atlandi", "tur": "konu", "baslik": terim, "ayrinti": "hassas konu — otomatik yazılmaz"})
        return None
    kaynaklar = olgular(terim, aday.get("ipucu", ""))
    if len(kaynaklar) < 2:
        YZ.kaydet({"olay": "atlandi", "tur": "konu", "baslik": terim, "ayrinti": "bağımsız kaynak %d (<2)" % len(kaynaklar)})
        return None
    if any(HASSAS.search(k["baslik"]) for k in kaynaklar[:2]):
        YZ.kaydet({"olay": "atlandi", "tur": "konu", "baslik": terim, "ayrinti": "haber başlığı hassas konu"})
        return None
    paket = _paket(aday, kaynaklar)
    m = {"baslik": terim}
    y = YZ.yaz(m, sistem=KONU_SISTEM, paket=paket, asgari_kelime=360,
               istem="Bu olgulardan, '%s' diye arayan okurun sorusunu cevaplayan özgün açıklayıcı haberi JSON olarak yaz." % terim)
    if not y or y.get("hata"):
        YZ.kaydet({"olay": "atildi", "tur": "konu", "baslik": terim, "ayrinti": (y or {}).get("hata", "yazı yok")[:300],
                   "kelime": (y or {}).get("kelime")})
        return None
    tarih = datetime.date.today().isoformat()
    # başlık ve açıklama site genelinde tekil olmalı (SEO kapısı çift title/description'da yayını durdurur)
    eskiler = hepsi()
    if any((k["yazi"].get("baslik") or "").strip().lower() == (y.get("baslik") or "").strip().lower() for k in eskiler):
        y["baslik"] = ("%s (%s)" % (y.get("baslik", terim)[:56], datetime.date.today().strftime("%d.%m")))
    if not y.get("meta") or len(y["meta"]) < 110 or any(k["yazi"].get("meta") == y.get("meta") for k in eskiler):
        y["meta"] = ("%s: %s" % (terim[:1].upper() + terim[1:], y.get("giris") or ""))[:150].rsplit(" ", 1)[0] + "…"
    slug = _slug(y.get("baslik") or terim) or _slug(terim)
    # adres çakışmasın: aynı slug başka bir güne aitse sona tarih eklenir
    mevcut = {k.get("slug") for k in _dizin().values()}
    if slug in mevcut or os.path.exists(os.path.join(SITE_KOK, "trend", slug + ".html")):
        slug = (slug[:58] + "-" + tarih.replace("-", "")).strip("-")
    gorsel = None
    try:
        from . import gorsel_bul as GB
        sorgular = [terim] + ([aday["ipucu"]] if aday.get("ipucu") else [])
        gorsel = GB.bul(sorgular, slug, aday["kat"])
    except Exception as ex:
        log("görsel bulunamadı: %s" % ex)
    kayit = {"tur": "konu", "tarih": tarih, "terim": terim, "hacim": aday.get("hacim", ""), "kat": aday["kat"],
             "kaynak_tur": aday.get("kaynak_tur", ""), "slug": slug, "yazi": y, "gorsel": gorsel,
             "kaynaklar": [{"ad": k["ad"], "tarih": k["tarih"]} for k in kaynaklar], "model": YZ._CALISAN_MODEL}
    d = os.path.join(DIZIN, tarih); os.makedirs(d, exist_ok=True)
    json.dump(kayit, open(os.path.join(d, slug + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    dz = _dizin(); dz[_norm(terim)] = {"slug": slug, "tarih": tarih, "kat": aday["kat"]}; _dizin_yaz(dz)
    YZ.kaydet({"olay": "yazildi", "tur": "konu", "baslik": y.get("baslik", "")[:70], "terim": terim, "kat": aday["kat"],
               "kelime": y.get("kelime"), "kapsama": (y.get("intihal") or {}).get("kapsama"), "kaynak": len(kaynaklar),
               "gorsel": (gorsel or {}).get("kaynak", "bölüm görseli")})
    log("Konu yazıldı: %s (%s, %d kaynak, görsel: %s)" % (y.get("baslik"), _kat_ad(aday["kat"]), len(kaynaklar), (gorsel or {}).get("kaynak", "yok")))
    return kayit


def uret(azami=None, log=print):
    """Bir tur: sırayla adaylara bakar, en çok `azami` yeni sayfa yazar."""
    azami = int(azami or os.environ.get("KONU_AZAMI") or 4)
    if not YZ.anahtar():
        YZ.kaydet({"olay": "tur", "tur": "konu", "anahtar": YZ.anahtar_durumu(), "ayrinti": "anahtar yok — konu yazılmadı"})
        log("Konu: yazar anahtarı yok")
        return {"yazilan": 0, "neden": "anahtar yok"}
    liste = adaylar()
    YZ.kaydet({"olay": "tur", "tur": "konu", "aday": len(liste), "anahtar": YZ.anahtar_durumu(), "model": YZ.model()})
    yazilan, bakilan = [], 0
    for a in liste:
        if len(yazilan) >= azami or bakilan >= azami * 4:
            break
        if yakin_zamanda_yazildi(a["terim"]):
            continue
        bakilan += 1
        try:
            k = yaz_konu(a, log)
        except YZ.YazarHatasi as ex:
            YZ.kaydet({"olay": "api_hatasi", "tur": "konu", "baslik": a["terim"], "kod": ex.kod, "ayrinti": ex.govde[:300]})
            log("Yazar API hatası %s — tur durdu" % ex.kod)
            break
        except Exception as ex:
            YZ.kaydet({"olay": "hata", "tur": "konu", "baslik": a["terim"], "ayrinti": str(ex)[:300]})
            continue
        if k:
            yazilan.append(k["slug"])
    return {"aday": len(liste), "bakilan": bakilan, "yazilan": len(yazilan), "sayfalar": yazilan}


def hepsi():
    """Diskteki bütün konu kayıtları (yeniden eskiye)."""
    out = []
    if not os.path.isdir(DIZIN):
        return out
    for gun in sorted(os.listdir(DIZIN), reverse=True):
        yol = os.path.join(DIZIN, gun)
        if not (os.path.isdir(yol) and re.match(r"\d{4}-\d{2}-\d{2}$", gun)):
            continue
        for f in sorted(os.listdir(yol)):
            if f.endswith(".json"):
                try:
                    k = json.load(open(os.path.join(yol, f), encoding="utf-8"))
                except Exception:
                    continue
                if isinstance(k.get("yazi"), dict) and k["yazi"].get("bolumler") and not k["yazi"].get("hata"):
                    out.append(k)
    return out


if __name__ == "__main__":
    print(json.dumps(uret(), ensure_ascii=False, indent=1))
