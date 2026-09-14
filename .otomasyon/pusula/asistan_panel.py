# -*- coding: utf-8 -*-
"""
PUSULA ASİSTANI — panelin içinden konuşan yardımcı.

Dış API yok. Üç kaynağı var:
  1. Veritabanı  — adaylar, temaslar, kişiler (sayım, arama, sıcak liste)
  2. Karargâh    — bugünün durumu, uyarılar, yapılacaklar
  3. Kılavuz     — hangi sekme ne işe yarıyor, sorun çözümleri

Ve eylem yapabiliyor: teklif üret, gündemi tara, Telegram'a gönder, tıklanmayı
getir. Eylem her zaman önce "şunu yapayım mı?" der; onaysız dosya üretmez.

Uydurmaz: cevabı veriden kuramıyorsa "bunu bilmiyorum, şu sekmeye bak" der.
"""
import re, unicodedata

from . import veritabani as vt


def _sade(x):
    x = (x or "").lower()
    for a, b in (("ı","i"),("ğ","g"),("ü","u"),("ş","s"),("ö","o"),("ç","c"),("â","a")):
        x = x.replace(a, b)
    x = unicodedata.normalize("NFKD", x)
    x = "".join(c for c in x if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]+", " ", x).strip()


def _iceriyor(s, *kel):
    return any(k in s for k in kel)


# ---------------------------------------------------------------- veri yardımcıları
SKOR_SQL = """(SELECT d.skor FROM denetimler d WHERE d.aday_id = a.id ORDER BY d.tarih DESC LIMIT 1)"""


def _sayim(b):
    from .ayarlar import ESIK
    q = lambda sql, p=(): b.execute(sql, p).fetchone()[0]
    esik = ESIK.get("sicak_skor", 60)
    return {
        "aday": q("SELECT COUNT(*) FROM adaylar"),
        "sicak": q("SELECT COUNT(*) FROM adaylar a WHERE COALESCE(%s,0) >= ?" % SKOR_SQL, (esik,)),
        "temas": q("SELECT COUNT(*) FROM temas"),
        "temas_firma": q("SELECT COUNT(DISTINCT aday_id) FROM temas"),
        "kisi": q("SELECT COUNT(*) FROM kisiler"),
        "kanal": q("SELECT COUNT(*) FROM kanallar"),
    }


def _sutun(b, tablo, ad):
    return any(r[1] == ad for r in b.execute("PRAGMA table_info(%s)" % tablo))


def _aday_bul(b, metin, n=5):
    """Türkçe harf duyarsız arama: 'iy yapi' → 'İy Yapı 16'."""
    hedef = _sade(metin)
    if len(hedef) < 2:
        return []
    ci = []
    for r in b.execute("SELECT a.id, a.ad, a.sektor, a.sehir, a.telefon, a.site, a.puan, %s AS skor "
                       "FROM adaylar a" % SKOR_SQL):
        if hedef in _sade(r["ad"]):
            ci.append(dict(r))
    ci.sort(key=lambda x: -(x.get("skor") or 0))
    return ci[:n]


def _sicaklar(b, n=8):
    return [dict(r) for r in b.execute(
        "SELECT a.id, a.ad, a.sektor, a.sehir, %s AS skor FROM adaylar a "
        "WHERE %s IS NOT NULL ORDER BY skor DESC LIMIT ?" % (SKOR_SQL, SKOR_SQL), (n,))]


def _sektor_dagilim(b):
    return [(r[0] or "—", r[1]) for r in b.execute(
        "SELECT sektor, COUNT(*) FROM adaylar GROUP BY sektor ORDER BY 2 DESC LIMIT 8")]


def _sehir_dagilim(b):
    return [(r[0] or "—", r[1]) for r in b.execute(
        "SELECT sehir, COUNT(*) FROM adaylar GROUP BY sehir ORDER BY 2 DESC LIMIT 8")]


# ---------------------------------------------------------------- kılavuz araması
def _kilavuz_ara(soru_s):
    from . import kilavuz as KL
    k = KL.veri()
    aday = []
    for sek in k.get("sekmeler", []):
        metin = _sade("%s %s %s" % (sek.get("ad"), sek.get("ne"), sek.get("ne_zaman")))
        puan = sum(1 for t in soru_s.split() if len(t) > 2 and t in metin)
        if puan:
            aday.append((puan, sek))
    for so in k.get("sorunlar", []):
        metin = _sade(" ".join(str(v) for v in so.values()))
        puan = sum(1 for t in soru_s.split() if len(t) > 2 and t in metin)
        if puan:
            aday.append((puan + 0.5, so))
    aday.sort(key=lambda x: -x[0])
    return [a for _, a in aday[:3]]


# ---------------------------------------------------------------- cevap
def cevapla(soru, b=None):
    """Döner: {"cevap": html, "eylem": {...} | None, "veri": ...}"""
    s = _sade(soru)
    kapat = b is None
    b = b or vt.baglan()
    try:
        # --- eylem niyetleri (onay ister)
        m = re.search(r"(.+?)\s+(?:icin|için)\s+(teklif|dosya)", s)
        if m or _iceriyor(s, "teklif uret", "teklif hazirla", "dosya cikar", "dosyayi cikar"):
            hedef = (m.group(1) if m else re.sub(r"(teklif|dosya|uret|hazirla|cikar|icin).*", "", s)).strip()
            bul = _aday_bul(b, hedef) if hedef else []
            if bul:
                a = bul[0]
                return {"cevap": "<b>%s</b> (%s · %s) için teklif paketi üreteyim mi? Poster, film, "
                                 "site/sosyal/aşama taslakları ve tek dosya rapor çıkar; Telegram açıksa "
                                 "telefona düşer." % (a["ad"], a.get("sektor") or "—", a.get("sehir") or "—"),
                        "eylem": {"tur": "dosya", "aday_id": a["id"], "etiket": "Teklifi üret"}}
            return {"cevap": "Hangi firma için? Adının bir parçasını yaz — adaylarda arayayım.", "eylem": None}

        if _iceriyor(s, "karga", "klip uret", "video uret", "runway"):
            from . import uretim as UR
            p = UR.karga_plani()
            if p["yol"] == "api":
                return {"cevap": "Karga setini üreteyim mi? %d klip × %d sn, %s modeli, tahmini <b>%d kredi</b>. "
                                 "Bittiğinde kodlanıp assets/video'ya girer." % (p["adet"], p["sn"], p["model"], p["kredi"]),
                        "eylem": {"tur": "karga", "etiket": "Üret (%d kredi)" % p["kredi"]}}
            return {"cevap": "Runway API anahtarı girilmemiş; karga seti tarayıcıdan üretilir. Anahtar girilirse "
                             "(Ayarlar → Üretim) 5 klip yaklaşık <b>%d kredi</b> — uygulama içi üretimin yedide biri." % p["kredi"],
                    "eylem": None}

        if _iceriyor(s, "gundemi tara", "gundem tara", "haberleri tara", "bugun ne oldu sektor"):
            return {"cevap": "Sektör gündemini tarayayım mı? 10 konu, birkaç saniye; sonra günün sayısını "
                             "seçip siteye yayınlayabilirsin.",
                    "eylem": {"tur": "gundem", "etiket": "Gündemi tara"}}

        if _iceriyor(s, "tiklanma", "kac kisi okudu", "okunma", "ziyaret"):
            return {"cevap": "Site okuma sayacını getireyim — bugün, 7 gün, 30 gün ve en çok okunan sayfalar.",
                    "eylem": {"tur": "okuma", "etiket": "Tıklanmayı getir"}}

        # --- durum / sayım
        if _iceriyor(s, "kac aday", "aday sayisi", "toplam aday", "ne kadar aday"):
            c = _sayim(b)
            return {"cevap": "<b>%d aday</b> var. %d kişi, %d iletişim kanalı çıkarılmış; "
                             "%d firmayla toplam %d temas kaydı var.%s"
                             % (c["aday"], c["kisi"], c["kanal"], c["temas_firma"], c["temas"],
                                (" Sıcak (skor eşiği üstü): %d." % c["sicak"]) if c["sicak"] is not None else ""),
                    "eylem": None, "veri": c}

        if _iceriyor(s, "sicak", "en iyi aday", "oncelikli", "kimden baslayayim", "kime gideyim"):
            l = _sicaklar(b)
            if not l:
                return {"cevap": "Skor sütunu yok ya da hesaplanmamış — önce <b>Denetle</b> ve <b>Hesapla</b> çalıştır.", "eylem": None}
            return {"cevap": "En sıcak adaylar:<br>" + "<br>".join(
                        "• <b>%s</b> — %s, %s · skor %s" % (a["ad"], a.get("sektor") or "—", a.get("sehir") or "—", a.get("skor"))
                        for a in l), "eylem": None, "veri": l}

        if _iceriyor(s, "sektor dagilim", "hangi sektor", "sektorlere gore"):
            d = _sektor_dagilim(b)
            return {"cevap": "Sektöre göre aday:<br>" + "<br>".join("• %s: %d" % x for x in d), "eylem": None}

        if _iceriyor(s, "sehir dagilim", "hangi sehir", "illere gore", "sehirlere gore"):
            d = _sehir_dagilim(b)
            return {"cevap": "İle göre aday:<br>" + "<br>".join("• %s: %d" % x for x in d), "eylem": None}

        if _iceriyor(s, "bugun ne yap", "bugun", "ne yapmaliyim", "durum ne", "nasil gidiyor", "ozet"):
            from . import karargah as KG
            o = KG.ozet()
            u = o.get("uyari") or []
            p = ["<b>%s</b> — %s" % (x.get("baslik"), x.get("adim")) for x in u[:5]]
            d = ["%s: <b>%s</b> (%s)" % (x.get("ad"), x.get("deger"), x.get("alt")) for x in (o.get("durum") or [])[:4]]
            return {"cevap": "Durum:<br>" + "<br>".join(d) + ("<br><br>Bugün:<br>" + "<br>".join("• " + x for x in p) if p else ""),
                    "eylem": None}

        # --- firma araması
        if _iceriyor(s, "hakkinda", "kimdir", "bilgi ver", "bul", "ara "):
            hedef = re.sub(r"(hakkinda|kimdir|bilgi ver|bul|ara)\b", "", s).strip()
            bul = _aday_bul(b, hedef) if len(hedef) > 2 else []
            if bul:
                return {"cevap": "Bulduklarım:<br>" + "<br>".join(
                    "• <b>%s</b> — %s, %s · tel %s · site %s" % (a["ad"], a.get("sektor") or "—", a.get("sehir") or "—",
                                                                 a.get("telefon") or "—", a.get("site") or "—")
                    for a in bul), "eylem": None, "veri": bul}

        # --- kılavuz
        k = _kilavuz_ara(s)
        if k:
            p = []
            for x in k:
                if "ne" in x:
                    p.append("<b>%s</b> — %s <i>(%s)</i>" % (x.get("ad"), x.get("ne"), x.get("ne_zaman", "")))
                else:
                    bas = x.get("belirti") or x.get("sorun") or x.get("baslik") or x.get("ad") or ""
                    p.append("<b>%s</b> — %s" % (bas, x.get("cozum") or x.get("coz") or x.get("ne") or ""))
            return {"cevap": "Kılavuzdan:<br>" + "<br>".join("• " + x for x in p), "eylem": None}

        return {"cevap": "Bunu veriden cevaplayamadım. Şunları sorabilirsin: <i>kaç aday var · sıcak adaylar · "
                         "bugün ne yapmalıyım · sektör dağılımı · [firma] hakkında · [firma] için teklif üret · "
                         "gündemi tara · tıklanma</i>", "eylem": None}
    finally:
        if kapat:
            b.close()
