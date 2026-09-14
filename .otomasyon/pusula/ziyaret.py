# -*- coding: utf-8 -*-
"""
ZİYARET RAPORU — günlük kaç kişi, hangi sayfa, kaç kişi butona bastı.

Search Console hattıyla aynı mantık: API yerine DIŞA AKTARIM okuyoruz.

Nereden alınır:
  GA4        → Raporlar → istediğin rapor → sağ üstteki paylaş/indir → "Dosya indir (CSV)"
  Cloudflare → Web Analytics → Site → sağ üstteki indirme simgesi (CSV)

Neyi çıkarır:
  · günlük ziyaretçi ve oturum eğrisi
  · en çok bakılan sayfalar
  · buton tıklamaları: WhatsApp, telefon, e-posta, form (olcum.js bunları olay
    olarak gönderiyor: whatsapp_tikla, telefon_tikla, eposta_tikla, form_gonder)
  · dönüşüm oranı: kaç ziyaretçiden kaçı iletişim eylemi yaptı

GA4'ün CSV'si başına "# " ile başlayan yorum satırları koyuyor ve tabloyu ondan
sonra veriyor; okuyucu bunu atlıyor.
"""
import csv, io, os, re, json, zipfile, datetime

# olcum.js'in gönderdiği olaylar → insanca ad
OLAY_AD = {
    "whatsapp_tikla": "WhatsApp'a tıkladı",
    "telefon_tikla": "Telefonu tıkladı",
    "eposta_tikla": "E-postayı tıkladı",
    "form_gonder": "Formu gönderdi",
}
ILETISIM_OLAYLARI = tuple(OLAY_AD)

_KUCUK = str.maketrans({"İ": "i", "I": "ı", "Ğ": "ğ", "Ü": "ü", "Ş": "ş", "Ö": "ö", "Ç": "ç"})


def _sade(x):
    return (x or "").replace("﻿", "").strip().translate(_KUCUK).lower()


def _sayi(x):
    if x is None:
        return None
    s = str(x).strip().replace("%", "").replace("\xa0", "")
    if not s or s in ("-", "—"):
        return None
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".") if s.rfind(",") > s.rfind(".") else s.replace(",", "")
    elif "," in s:
        s = s.replace(",", ".") if len(s.split(",")[-1]) <= 2 else s.replace(",", "")
    elif re.fullmatch(r"\d{1,3}(\.\d{3})+", s):
        s = s.replace(".", "")
    try:
        return float(s)
    except ValueError:
        return None


# ---------------------------------------------------------------- sütun eşleme
BOYUT = {
    "tarih":  ("tarih", "date", "gün", "day", "nth day"),
    "sayfa":  ("sayfa yolu", "page path", "sayfa başlığı", "page title", "sayfa", "path", "url"),
    "olay":   ("olay adı", "event name", "olay", "event"),
    "kaynak": ("kaynak", "source", "ortam", "medium", "kanal", "channel", "yönlendiren", "referrer"),
    "ulke":   ("ülke", "country"),
    "cihaz":  ("cihaz", "device"),
}
OLCUM = {
    "kullanici": ("toplam kullanıcı", "kullanıcı", "users", "total users", "active users",
                  "ziyaretçi", "visitors", "tekil ziyaretçi", "unique visitors"),
    "oturum":    ("oturum", "sessions", "session"),
    "goruntuleme": ("görüntüleme", "views", "pageviews", "sayfa görüntüleme", "page views",
                    "ekran görüntüleme"),
    "olay_sayisi": ("olay sayısı", "event count", "olay"),
    "sure":      ("ortalama etkileşim süresi", "average engagement time", "ortalama süre"),
}


def _basliklari_coz(basliklar):
    b = [_sade(x) for x in basliklar]
    boyut_i, olcum_i = {}, {}
    for ad, izler in BOYUT.items():
        for i, x in enumerate(b):
            if i in boyut_i.values() or i in olcum_i.values():
                continue
            if any(iz in x for iz in izler):
                boyut_i[ad] = i
                break
    for ad, izler in OLCUM.items():
        for i, x in enumerate(b):
            if i in boyut_i.values() or i in olcum_i.values():
                continue
            if any(iz in x for iz in izler):
                olcum_i[ad] = i
                break
    return boyut_i, olcum_i


def csv_oku(metin):
    """GA4/Cloudflare CSV'sini satır sözlüklerine çevirir. Yorum satırlarını atlar."""
    satirlar = [s for s in metin.splitlines() if s.strip()]
    # GA4 başa "# " ile yorum koyuyor
    satirlar = [s for s in satirlar if not s.lstrip().startswith("#")]
    if len(satirlar) < 2:
        return [], {}, {}
    metin2 = "\n".join(satirlar)
    ilk = satirlar[0]
    ayrac = "\t" if "\t" in ilk else (";" if ilk.count(";") > ilk.count(",") else ",")
    r = list(csv.reader(io.StringIO(metin2), delimiter=ayrac))
    if len(r) < 2:
        return [], {}, {}
    boyut_i, olcum_i = _basliklari_coz(r[0])
    if not olcum_i:
        return [], {}, {}
    cikti = []
    for s in r[1:]:
        if not s or all(not x.strip() for x in s):
            continue
        d = {}
        for ad, i in boyut_i.items():
            d[ad] = s[i].strip() if i < len(s) else ""
        for ad, i in olcum_i.items():
            d[ad] = _sayi(s[i]) if i < len(s) else None
        if any(v for v in d.values()):
            cikti.append(d)
    return cikti, boyut_i, olcum_i


def dosya_oku(yol):
    """ZIP ya da tek CSV. Döner: [{tur, satir, boyut, olcum}]"""
    tablolar = []

    def _coz(ad, ham):
        for kod in ("utf-8-sig", "utf-8", "cp1254", "latin-1"):
            try:
                metin = ham.decode(kod)
                break
            except UnicodeDecodeError:
                continue
        else:
            return
        satir, boyut, olcum = csv_oku(metin)
        if satir:
            tablolar.append({"ad": ad, "satir": satir, "boyut": boyut, "olcum": olcum})

    if zipfile.is_zipfile(yol):
        with zipfile.ZipFile(yol) as z:
            for ad in z.namelist():
                if ad.lower().endswith((".csv", ".tsv")):
                    _coz(os.path.basename(ad), z.read(ad))
    else:
        with open(yol, "rb") as f:
            _coz(os.path.basename(yol), f.read())
    return tablolar


# ---------------------------------------------------------------- analiz
def _tarih_duzelt(x):
    """'20260826' / '2026-08-26' / '26.08.2026' → '2026-08-26'."""
    s = str(x or "").strip()
    if re.fullmatch(r"\d{8}", s):
        return "%s-%s-%s" % (s[:4], s[4:6], s[6:])
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return s
    m = re.fullmatch(r"(\d{2})[./](\d{2})[./](\d{4})", s)
    if m:
        return "%s-%s-%s" % (m.group(3), m.group(2), m.group(1))
    return s


def cozumle(tablolar):
    """Tabloları tek rapora çevirir."""
    gunluk, sayfa, olay, kaynak = {}, {}, {}, {}

    for t in tablolar:
        b, o = t["boyut"], t["olcum"]
        for s in t["satir"]:
            kisi = s.get("kullanici") or s.get("oturum") or 0
            gor = s.get("goruntuleme") or 0
            adet = s.get("olay_sayisi") or 0

            if "tarih" in b:
                g = _tarih_duzelt(s.get("tarih"))
                if g:
                    d = gunluk.setdefault(g, {"kullanici": 0, "oturum": 0, "goruntuleme": 0})
                    d["kullanici"] += int(s.get("kullanici") or 0)
                    d["oturum"] += int(s.get("oturum") or 0)
                    d["goruntuleme"] += int(gor)
            if "sayfa" in b and s.get("sayfa"):
                y = s["sayfa"].strip()
                d = sayfa.setdefault(y, {"goruntuleme": 0, "kullanici": 0})
                d["goruntuleme"] += int(gor)
                d["kullanici"] += int(s.get("kullanici") or 0)
            if "olay" in b and s.get("olay"):
                a = s["olay"].strip()
                olay[a] = olay.get(a, 0) + int(adet or gor or kisi or 0)
            if "kaynak" in b and s.get("kaynak"):
                k = s["kaynak"].strip()
                d = kaynak.setdefault(k, {"kullanici": 0, "oturum": 0})
                d["kullanici"] += int(s.get("kullanici") or 0)
                d["oturum"] += int(s.get("oturum") or 0)

    gun_listesi = [{"tarih": g, **v} for g, v in sorted(gunluk.items())]
    toplam_kisi = sum(g["kullanici"] for g in gun_listesi) or sum(
        v["kullanici"] for v in sayfa.values())
    toplam_gor = sum(g["goruntuleme"] for g in gun_listesi) or sum(
        v["goruntuleme"] for v in sayfa.values())

    # iletişim eylemleri
    iletisim = {}
    for a, n in olay.items():
        anahtar = _sade(a).replace(" ", "_")
        for kod in ILETISIM_OLAYLARI:
            if kod in anahtar:
                iletisim[kod] = iletisim.get(kod, 0) + n
    iletisim_toplam = sum(iletisim.values())

    sayfa_listesi = [{"yol": y, **v} for y, v in sayfa.items()]
    sayfa_listesi.sort(key=lambda x: -x["goruntuleme"])

    gun_sayisi = len(gun_listesi) or 1
    return {
        "zaman": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
        "gun": gun_listesi,
        "gun_sayisi": len(gun_listesi),
        "toplam": {
            "kullanici": toplam_kisi,
            "goruntuleme": toplam_gor,
            "gunluk_ortalama": round(toplam_kisi / gun_sayisi, 1),
            "sayfa_basi": round(toplam_gor / max(1, toplam_kisi), 2),
        },
        "sayfa": sayfa_listesi[:60],
        "olay": [{"ad": a, "adet": n} for a, n in sorted(olay.items(), key=lambda x: -x[1])][:30],
        "iletisim": [{"kod": k, "ad": OLAY_AD.get(k, k), "adet": v}
                     for k, v in sorted(iletisim.items(), key=lambda x: -x[1])],
        "iletisim_toplam": iletisim_toplam,
        "donusum": (round(100.0 * iletisim_toplam / toplam_kisi, 2) if toplam_kisi else None),
        "kaynak": [{"ad": a, **v} for a, v in
                   sorted(kaynak.items(), key=lambda x: -x[1]["kullanici"])][:20],
        "tablo": [t["ad"] for t in tablolar],
    }


def ice_aktar(yol):
    t = dosya_oku(yol)
    if not t:
        return {"sorun": ("Dosyada tanınan bir tablo yok. GA4'te Raporlar → rapor → "
                          "sağ üstten 'Dosya indir (CSV)'; Cloudflare'de Web Analytics → "
                          "indirme simgesi. İnen dosyayı olduğu gibi yükleyin.")}
    r = cozumle(t)
    r["kaynak_dosya"] = os.path.basename(yol)
    if not r["gun"] and not r["sayfa"] and not r["olay"]:
        return {"sorun": "Tablo okundu ama içinde gün/sayfa/olay verisi bulunamadı."}
    return r


def yorum(r):
    """Rapordan çıkan sade cümleler — panelde üstte gösteriliyor."""
    c = []
    t = r.get("toplam") or {}
    if r.get("gun"):
        c.append("Günde ortalama %s kişi siteye giriyor." % t.get("gunluk_ortalama"))
        en = max(r["gun"], key=lambda g: g["kullanici"])
        c.append("En yoğun gün %s — %d kişi." % (en["tarih"], en["kullanici"]))
    if r.get("sayfa"):
        ilk = r["sayfa"][0]
        c.append("En çok bakılan sayfa: %s (%d görüntülenme)." % (ilk["yol"], ilk["goruntuleme"]))
    if r.get("iletisim_toplam"):
        c.append("İletişim eylemi: %d kez (WhatsApp, telefon, e-posta, form toplamı)."
                 % r["iletisim_toplam"])
        if r.get("donusum") is not None:
            c.append("Yüz ziyaretçiden %s tanesi iletişim eylemi yapıyor." % r["donusum"])
    elif r.get("olay"):
        c.append("Buton tıklaması olayı bulunamadı. assets/olcum.js yayında mı ve "
                 "GA4 kimliği girildi mi kontrol edin.")
    else:
        c.append("Bu dosyada olay verisi yok. GA4'te Raporlar → Etkileşim → Olaylar "
                 "raporunu ayrıca indirip yükleyin.")
    return c
