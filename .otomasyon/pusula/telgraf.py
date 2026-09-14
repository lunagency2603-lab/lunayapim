# -*- coding: utf-8 -*-
"""
Telegram köprüsü — teklif üretilince her şeyi tek seferde telefona düşürür.

Neden Telegram: WhatsApp'ın resmî olmayan otomasyonu hesap kapattırır. Telegram
bot API'si resmî, ücretsiz, sınırsız ve dosya boyutu 50 MB'a kadar serbest.
Teklif paketi (metin + görseller + video + belgeler) buradan telefona düşer,
sen okur, beğenirsen kopyalayıp müşteriye WhatsApp'tan kendin gönderirsin.

Kimseye kendiliğinden mesaj ATMAZ. Yalnızca senin sohbetine gönderir.
Sadece Python standart kütüphanesi kullanır.
"""
import json, mimetypes, os, ssl, urllib.request, urllib.error, uuid

from .ayarlar import TELEGRAM

API = "https://api.telegram.org/bot%s/%s"
AZAMI_METIN = 4096
AZAMI_ALTYAZI = 1024
AZAMI_DOSYA = 49 * 1024 * 1024


# ---------------------------------------------------------------- alt katman
def hazir():
    """(hazir_mi, sebep)"""
    if not TELEGRAM.get("jeton"):
        return False, "Telegram bot jetonu girilmemiş (Ayarlar → Telegram)."
    if not TELEGRAM.get("sohbet"):
        return False, "Telegram sohbet kimliği girilmemiş (Ayarlar → Telegram)."
    return True, ""


def _coklu_govde(alanlar, dosyalar):
    """multipart/form-data gövdesi kurar (kütüphane yok, elle)."""
    sinir = "----luna" + uuid.uuid4().hex
    ci = []
    for ad, deger in alanlar.items():
        if deger is None:
            continue
        ci.append(("--" + sinir).encode())
        ci.append(('Content-Disposition: form-data; name="%s"' % ad).encode())
        ci.append(b"")
        ci.append(str(deger).encode("utf-8"))
    for ad, yol in dosyalar.items():
        tur = mimetypes.guess_type(yol)[0] or "application/octet-stream"
        with open(yol, "rb") as f:
            ham = f.read()
        ci.append(("--" + sinir).encode())
        ci.append(('Content-Disposition: form-data; name="%s"; filename="%s"'
                   % (ad, os.path.basename(yol))).encode("utf-8"))
        ci.append(("Content-Type: " + tur).encode())
        ci.append(b"")
        ci.append(ham)
    ci.append(("--" + sinir + "--").encode())
    ci.append(b"")
    return b"\r\n".join(ci), "multipart/form-data; boundary=" + sinir


def cagir(metot, alanlar=None, dosyalar=None, zaman_asimi=90):
    """Telegram API çağrısı. Döner: (basarili, cevap_veya_hata)"""
    tamam, sebep = hazir()
    if not tamam:
        return False, sebep
    alanlar = dict(alanlar or {})
    alanlar.setdefault("chat_id", TELEGRAM["sohbet"])
    if TELEGRAM.get("sessiz"):
        alanlar.setdefault("disable_notification", "true")
    url = API % (TELEGRAM["jeton"], metot)
    try:
        if dosyalar:
            govde, tur = _coklu_govde(alanlar, dosyalar)
            istek = urllib.request.Request(url, data=govde,
                                           headers={"Content-Type": tur})
        else:
            govde = json.dumps(alanlar).encode("utf-8")
            istek = urllib.request.Request(url, data=govde,
                                           headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(istek, timeout=zaman_asimi,
                                    context=ssl.create_default_context()) as c:
            y = json.loads(c.read().decode("utf-8", "ignore"))
        return bool(y.get("ok")), y
    except urllib.error.HTTPError as e:
        try:
            y = json.loads(e.read().decode("utf-8", "ignore"))
            return False, y.get("description") or str(e)
        except Exception:
            return False, "HTTP %s" % e.code
    except Exception as e:
        return False, "%s: %s" % (type(e).__name__, e)


def sinama():
    """Ayarlar doğru mu — bota kim olduğunu sorar, sohbete tek satır atar."""
    ok, y = cagir("getMe")
    if not ok:
        return False, ("Bot jetonu çalışmıyor: %s" % y)
    ad = (y.get("result") or {}).get("username", "?")
    ok2, y2 = mesaj("Luna Pusula bağlandı. Bot: @%s" % ad)
    if not ok2:
        return False, ("Jeton doğru ama sohbete yazılamadı: %s\n"
                       "Sebep genelde: bota Telegram'dan bir kez /start yazılmamış "
                       "ya da sohbet kimliği yanlış." % y2)
    return True, "Bağlandı — bot @%s, sohbete deneme mesajı düştü." % ad


# ---------------------------------------------------------------- gönderim
def _kirp(m, azami):
    m = m or ""
    return m if len(m) <= azami else m[: azami - 20].rstrip() + "\n…(kesildi)"


def mesaj(metin, bicim="HTML", onizleme=False):
    parcalar, kalan = [], metin or ""
    while len(kalan) > AZAMI_METIN:
        kes = kalan.rfind("\n", 0, AZAMI_METIN)
        if kes < 1000:
            kes = AZAMI_METIN
        parcalar.append(kalan[:kes])
        kalan = kalan[kes:]
    parcalar.append(kalan)
    son = (True, None)
    for p in parcalar:
        son = cagir("sendMessage", {"text": p, "parse_mode": bicim,
                                    "disable_web_page_preview": not onizleme})
        if not son[0]:
            return son
    return son


def foto(yol, altyazi=None):
    if not (yol and os.path.exists(yol)):
        return False, "dosya yok: %s" % yol
    return cagir("sendPhoto", {"caption": _kirp(altyazi, AZAMI_ALTYAZI),
                               "parse_mode": "HTML"}, {"photo": yol})


def video(yol, altyazi=None):
    if not (yol and os.path.exists(yol)):
        return False, "dosya yok: %s" % yol
    if os.path.getsize(yol) > AZAMI_DOSYA:
        return belge(yol, altyazi)
    return cagir("sendVideo", {"caption": _kirp(altyazi, AZAMI_ALTYAZI),
                               "parse_mode": "HTML",
                               "supports_streaming": "true"}, {"video": yol})


def belge(yol, altyazi=None):
    if not (yol and os.path.exists(yol)):
        return False, "dosya yok: %s" % yol
    if os.path.getsize(yol) > AZAMI_DOSYA:
        return False, "dosya 50 MB üstü: %s" % os.path.basename(yol)
    return cagir("sendDocument", {"caption": _kirp(altyazi, AZAMI_ALTYAZI),
                                  "parse_mode": "HTML"}, {"document": yol})


def album(yollar, altyazi=None):
    """En çok 10 görseli tek kart olarak gönderir; altyazı ilkine yazılır."""
    yollar = [y for y in (yollar or []) if y and os.path.exists(y)][:10]
    if not yollar:
        return False, "gönderilecek görsel yok"
    if len(yollar) == 1:
        return foto(yollar[0], altyazi)
    ortam, dosyalar = [], {}
    for i, y in enumerate(yollar):
        ad = "g%d" % i
        dosyalar[ad] = y
        p = {"type": "photo", "media": "attach://" + ad}
        if i == 0 and altyazi:
            p["caption"] = _kirp(altyazi, AZAMI_ALTYAZI)
            p["parse_mode"] = "HTML"
        ortam.append(p)
    return cagir("sendMediaGroup", {"media": json.dumps(ortam, ensure_ascii=False)},
                 dosyalar)


# ---------------------------------------------------------------- teklif paketi
def _kacis(x):
    return (str(x or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _eksik_satirlari(eksikler, detay, azami=8):
    """Kanıtıyla ve kesinliğiyle birlikte en önemli eksikler."""
    from .puanlama import ETIKET
    kanit = (detay or {}).get("kanit") or {}
    kesin = set(((detay or {}).get("kesinlik") or {}).get("kesin") or eksikler)
    sirali = [k for k in eksikler if k in kesin] + [k for k in eksikler if k not in kesin]
    satir = []
    for kod in sirali[:azami]:
        ad = ETIKET.get(kod, kod)
        k = kanit.get(kod) or {}
        bulgu = _kacis(k.get("bulgu", ""))[:180]
        damga = "" if kod in kesin else " <i>(elle doğrulanmalı)</i>"
        satir.append("• <b>%s</b>%s\n   <i>%s</i>" % (_kacis(ad), damga, bulgu))
    kalan = len(eksikler) - len(satir)
    if kalan > 0:
        satir.append("• …ve %d başlık daha (raporda)" % kalan)
    return "\n".join(satir)


def teklif_gonder(sonuc, aday, eksikler, detay, tahmin=None):
    """
    Bir teklif paketini olduğu gibi Telegram'a düşürür:
      1) özet kart — firma, kanal, bedel, kanıtlı eksikler
      2) görsel albümü — poster + site/sosyal/aşama/kalite taslakları
      3) film — firmanın kendi görsellerinden üretilen dikey tanıtım
      4) belgeler — tek dosyalık teklif, iş emri, mesajlar
      5) kopyala-yapıştır açılış mesajı

    Döner: {"gonderilen": [...], "hata": [...]}
    """
    tamam, sebep = hazir()
    if not tamam:
        return {"gonderilen": [], "hata": [sebep]}

    giden, hata = [], []
    ad = _kacis(aday.get("ad"))
    sehir = _kacis(aday.get("sehir") or "")
    sektor = _kacis(aday.get("sektor") or "")
    kanal = (sonuc.get("kanal") or {})
    bedel = sonuc.get("bedel")
    site = aday.get("site") or "—"
    ozet = (detay or {}).get("kesinlik_ozeti") or ""
    kesinlik = (detay or {}).get("kesinlik") or {}

    bas = ["<b>TEKLİF HAZIR — %s</b>" % ad]
    alt = " · ".join(x for x in (sektor, sehir) if x)
    if alt:
        bas.append(alt)
    bas.append("Site: %s" % _kacis(site))
    bas.append("")
    bas.append("<b>Kanal:</b> %s — %s" % (_kacis(kanal.get("kanal", "?")).upper(),
                                          _kacis(kanal.get("gerekce", ""))))
    u = sonuc.get("ulasim") or {}
    if u:
        bas.append("<b>Sektör planı</b> (%s): %s" % (_kacis(u.get("kaynak")),
                                                     _kacis(" → ".join(u.get("sira") or []))))
        bas.append("<b>Saat:</b> %s" % _kacis(u.get("saat")))
        bas.append("<b>Kaçın:</b> %s" % _kacis(u.get("kacin")))
        bas.append("<b>Karar veren:</b> %s" % _kacis(u.get("karar")))
        bas.append("<b>Kanca:</b> %s" % _kacis(u.get("kanca")))
    if sonuc.get("wa_numara"):
        bas.append("<b>WhatsApp:</b> +%s" % _kacis(sonuc["wa_numara"]))
    for t in (sonuc.get("telefonlar") or [])[:2]:
        bas.append("<b>Telefon:</b> %s (%s)" % (_kacis(t.get("normal")), _kacis(t.get("tip"))))
    for e in (sonuc.get("epostalar") or [])[:2]:
        bas.append("<b>E-posta:</b> %s" % _kacis(e))
    if bedel:
        bas.append("<b>Önerilen bedel:</b> %s" % _kacis(sonuc.get("bedel_oneri") or bedel))
    bas.append("")
    bas.append("<b>Tespit edilen eksikler (%d)</b>" % len(eksikler))
    if kesinlik:
        bas.append("<i>%d kesin · %d elle doğrulanacak · %d ölçülemedi</i>"
                   % (len(kesinlik.get("kesin", [])), len(kesinlik.get("muhtemel", [])),
                      len(kesinlik.get("dogrulanamadi", []))))
    bas.append(_eksik_satirlari(eksikler, detay))
    if ozet:
        bas.append("")
        bas.append("<i>%s</i>" % _kacis(ozet))

    ok, y = mesaj("\n".join(bas))
    (giden if ok else hata).append("özet" if ok else "özet: %s" % y)

    # --- görseller
    on = sonuc.get("onizleme") or {}
    gorseller = on.get("gorseller") or [g for g in (on.get("poster"),) if g]
    if gorseller:
        ok, y = album(gorseller, "%s için hazırlanan taslaklar — hepsi firmanın kendi "
                                 "malzemesinden üretildi, üzerinde ÖNİZLEME · TASLAK "
                                 "rozeti var." % ad)
        (giden if ok else hata).append("görseller (%d)" % len(gorseller) if ok
                                       else "görseller: %s" % y)
    else:
        hata.append("görsel üretilemedi: " + "; ".join(on.get("not") or ["sebep bilinmiyor"]))

    # --- film
    if on.get("film"):
        ok, y = video(on["film"], "%s — dikey tanıtım önizlemesi (taslak)" % ad)
        (giden if ok else hata).append("film" if ok else "film: %s" % y)

    # --- belgeler
    for anahtar, aciklama in (("teklif_tek", "Teklif raporu (tek dosya, görseller gömülü)"),
                              ("is_emri", "İş emri — üretim planı"),
                              ("mesajlar", "Hazır mesajlar")):
        yol = sonuc.get(anahtar)
        if yol and os.path.exists(yol):
            ok, y = belge(yol, "%s — %s" % (ad, aciklama))
            (giden if ok else hata).append(anahtar if ok else "%s: %s" % (anahtar, y))

    # --- kopyalanacak açılış mesajı (biçimsiz, doğrudan yapıştırılabilsin)
    m = (sonuc.get("mesaj") or {}).get(kanal.get("kanal") if kanal.get("kanal") in
                                       ("whatsapp", "telefon") else "whatsapp")
    if m:
        ok, y = cagir("sendMessage", {"text": "AÇILIŞ MESAJI (kopyala):\n\n" + m,
                                      "disable_web_page_preview": True})
        (giden if ok else hata).append("açılış mesajı" if ok else "açılış: %s" % y)

    return {"gonderilen": giden, "hata": hata}
