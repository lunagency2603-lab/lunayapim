# -*- coding: utf-8 -*-
"""
KARARGÂH — panelin açılış ekranı.

Panel on üç sekmeye büyüdü ve her sekme bir araç. Ama sabah panelı açan
kişinin ilk sorusu "hangi aracı kullanayım" değil: **bugün ne yapmam
gerekiyor?**

Bu katman o soruyu cevaplıyor. Üç bölüm:

  DURUM    — sitenin, aramanın, satışın o anki hâli. Tek bakışta.
  UYARI    — bekleyen, unutulan, yarıda kalmış işler. Öncelik sırasında.
  BUGÜN    — bugün elle yapılacak somut işler (takipler, hazır taslaklar).

Kural: uyarı üretmek kolay, doğru uyarı üretmek zor. Buradaki her uyarının
bir SEBEBİ ve bir SONRAKİ ADIMI var. "Bir şeyler eksik" diyen satır yok.
"""
import os, json, datetime

from .ayarlar import CIKTI, SITE_KOK


ONEM = {"kritik": 0, "onemli": 1, "bilgi": 2}


def _tarih(g):
    try:
        return datetime.date.fromisoformat(str(g)[:10])
    except Exception:
        return None


# ------------------------------------------------------------------ durum
def _site_durumu():
    from . import saglik as SL
    try:
        g = SL.gunluk_oku()
        son = g[-1] if g else None
    except Exception:
        son = None
    if not son:
        return {"ad": "Site sağlığı", "deger": "—", "alt": "henüz ölçülmedi",
                "renk": "gri"}
    fark = ""
    if len(g) >= 2:
        d = round(son["oran"] - g[-2]["oran"], 1)
        if d:
            fark = " (%+.1f)" % d
    return {"ad": "Site sağlığı", "deger": "%%%s%s" % (son["oran"], fark),
            "alt": "%d sayfa · %d hata · %d uyarı" % (son["sayfa"], son["hata"], son["uyari"]),
            "renk": "yesil" if son["hata"] == 0 and son["uyari"] == 0 else
                    ("sari" if son["hata"] == 0 else "kirmizi")}


def _yayin_durumu():
    from . import depo as DP
    d = DP.durum()
    if d.get("hata") or not d.get("depo_mu"):
        return {"ad": "Yayın", "deger": "—", "alt": "depo okunamadı", "renk": "gri"}
    bekleyen = int(d.get("degisiklik") or 0)
    if bekleyen:
        return {"ad": "Yayın", "deger": "%d dosya" % bekleyen,
                "alt": "kaydedilmemiş değişiklik var", "renk": "sari"}
    return {"ad": "Yayın", "deger": "güncel", "alt": d.get("son_islem") or "—",
            "renk": "yesil"}


def _arama_durumu():
    from . import veritabani as vt
    try:
        b = vt.baglan()
        r = b.execute("SELECT tiklama, gosterim, yuklendi FROM arama_kayit "
                      "ORDER BY id DESC LIMIT 1").fetchone()
        b.close()
    except Exception:
        r = None
    if not r:
        return {"ad": "Arama", "deger": "—", "alt": "veri yüklenmedi", "renk": "gri"}
    return {"ad": "Arama", "deger": "%s tık" % (r["tiklama"] or 0),
            "alt": "%s gösterim · %s" % (r["gosterim"] or 0, str(r["yuklendi"])[:10]),
            "renk": "gri"}


def _satis_durumu():
    from . import veritabani as vt
    try:
        b = vt.baglan()
        i = vt.istatistik(b)
        takip = len(vt.takip_gerekenler(b))
        b.close()
    except Exception:
        return {"ad": "Satış", "deger": "—", "alt": "okunamadı", "renk": "gri"}
    return {"ad": "Bugün takip", "deger": str(takip),
            "alt": "%d aday · %d temas · %d iş" % (i.get("aday", 0), i.get("temas", 0),
                                                   i.get("is", 0)),
            "renk": "kirmizi" if takip else "yesil"}


def durum():
    return [_site_durumu(), _yayin_durumu(), _arama_durumu(), _satis_durumu()]


# ------------------------------------------------------------------ uyarılar
def _u(onem, baslik, sebep, adim, sekme=""):
    return {"onem": onem, "baslik": baslik, "sebep": sebep, "adim": adim, "sekme": sekme}


def uyarilar():
    """Her uyarı: ne, neden önemli, sıradaki adım."""
    u = []

    # --- yayına gitmemiş değişiklik
    try:
        from . import depo as DP
        d = DP.durum()
        n = int(d.get("degisiklik") or 0)
        if n:
            u.append(_u("kritik", "%d dosya yayına gitmedi" % n,
                        "Yaptığın değişiklikler bilgisayarında duruyor; ziyaretçi "
                        "hâlâ eski sayfayı görüyor.",
                        "GitHub Desktop → Commit → Push origin"))
        if d.get("kilit"):
            u.append(_u("kritik", "Depo kilitli",
                        "GitHub Desktop işlem yapamıyor.",
                        "Ayarlar → Depo durumu → kilidi çöz", "ayarlar"))
    except Exception:
        pass

    # --- site sağlığı
    try:
        from . import saglik as SL
        g = SL.gunluk_oku()
        if not g:
            u.append(_u("onemli", "Site hiç denetlenmedi",
                        "Sayfalarda hata var mı bilmiyoruz.",
                        "Arama → Site sağlığı → Şimdi tara", "arama"))
        else:
            son = g[-1]
            if son["hata"]:
                u.append(_u("kritik", "%d sayfada hata var" % son["hata"],
                            "Hatalı sayfa aramada geriliyor.",
                            "Arama → Site sağlığı → Şimdi tara", "arama"))
            elif son["uyari"]:
                u.append(_u("onemli", "%d uyarı açık" % son["uyari"],
                            "Engelleyici değil ama iyileştirme fırsatı.",
                            "Arama → Site sağlığı", "arama"))
            gun = _tarih(son["tarih"])
            if gun and (datetime.date.today() - gun).days >= 7:
                u.append(_u("bilgi", "Site bir haftadır denetlenmedi",
                            "Son ölçüm %s." % son["tarih"],
                            "Arama → Site sağlığı → Şimdi tara", "arama"))
    except Exception:
        pass

    # --- ölçüm kimlikleri
    try:
        from . import yayin as YA
        o = YA.olcum_oku() or {}
        if not (o.get("ga4") or "").strip():
            u.append(_u("kritik", "Ziyaretçi ölçümü kapalı",
                        "Kaç kişi geldiğini, kimin iletişime geçtiğini göremiyoruz.",
                        "Ayarlar → Ölçüm → GA4 kimliğini yapıştır", "ayarlar"))
    except Exception:
        pass

    # --- sitedeki boş defterler
    try:
        yorum = os.path.join(SITE_KOK, "assets", "yorumlar.js")
        if os.path.isfile(yorum):
            s = open(yorum, encoding="utf-8").read()
            if '"' not in s.split("LUNA_YORUM", 1)[-1].split("]")[0].replace('""', ""):
                u.append(_u("onemli", "Müşteri sözü yok",
                            "Karnemizde en zayıf başlık güven; onu kapatan tek şey bu.",
                            "Yazılı onay aldığın iki görüşü Claude'a ilet"))
    except Exception:
        pass
    try:
        sos = os.path.join(SITE_KOK, "assets", "sosyal.js")
        if os.path.isfile(sos):
            s = open(sos, encoding="utf-8").read()
            govde = s.split("LUNA_SOSYAL", 1)[-1].split("];")[0]
            if 'kullanici:""' in govde.replace(" ", ""):
                bos = govde.replace(" ", "").count('kullanici:""')
                u.append(_u("onemli", "%d sosyal hesap boş" % bos,
                            "Alt bilgideki bağlantı şeridi ve Google'a "
                            "\"bu hesaplar bize ait\" diyen şema alanı kapalı.",
                            "Hesap açtıkça kullanıcı adını Claude'a ilet"))
            if 'LUNA_HARITA = ""' in s:
                u.append(_u("bilgi", "Yol tarifi bağlantısı yok",
                            "Yerel aramada işe yarayan bir sinyal eksik.",
                            "Google Haritalar kaydı onaylanınca bağlantıyı ilet"))
    except Exception:
        pass

    # --- bekleyen taslaklar
    try:
        from . import yayin as YA
        t = YA.taslak_listesi(os.path.join(CIKTI, "gundem")) or []
        hazir = [x for x in t if not x.get("uyari")]
        if hazir:
            u.append(_u("onemli", "%d yazı yayına hazır" % len(hazir),
                        "Yazılmış ama yayınlanmamış içerik duruyor.",
                        "Gündem → Yayın taslakları", "gundem"))
    except Exception:
        pass

    # --- yayına hazır makale
    try:
        from . import makale as MK
        n = MK.hazir_sayisi()
        if n:
            u.append(_u("onemli", "%d makale yayına hazır" % n,
                        "Yazı üretildi ve 100 puan aldı; yayınlanmayı bekliyor. "
                        "Sitenin arama tarafındaki yüzeyi burada büyüyor.",
                        "Makale → Üret ve puanla → Yayınla", "makale"))
    except Exception:
        pass

    # --- takip edilmesi gerekenler
    try:
        from . import veritabani as vt
        b = vt.baglan()
        tk = vt.takip_gerekenler(b)
        b.close()
        gecmis = 0
        for x in tk:
            g = _tarih(x.get("sonraki_tarih"))
            if g and g < datetime.date.today():
                gecmis += 1
        if gecmis:
            u.append(_u("kritik", "%d firmaya söz verilen gün geçti" % gecmis,
                        "İşi kaybettiren şey genelde kötü teklif değil, unutulan takip.",
                        "Raf → Bugün takip edilecekler", "raf"))
        elif tk:
            u.append(_u("onemli", "%d firma bugün takip edilecek" % len(tk),
                        "Söz verilen gün bugün.",
                        "Raf → Bugün takip edilecekler", "raf"))
    except Exception:
        pass

    u.sort(key=lambda x: ONEM.get(x["onem"], 3))
    return u


# ------------------------------------------------------------------ bugün
def bugun():
    """Bugün elle yapılacak somut işler."""
    isler = []
    try:
        from . import veritabani as vt
        b = vt.baglan()
        for x in vt.takip_gerekenler(b)[:12]:
            g = _tarih(x.get("sonraki_tarih"))
            gec = bool(g and g < datetime.date.today())
            isler.append({"tur": "takip", "ad": x.get("firma") or "—",
                          "not": x.get("sonraki_adim") or "Takip et",
                          "tarih": x.get("sonraki_tarih") or "",
                          "gecikti": gec, "aday_id": x.get("aday_id")})
        b.close()
    except Exception:
        pass
    return isler


def ozet():
    """Panelin karargâh sekmesinin okuduğu tek paket."""
    u = uyarilar()
    return {
        "zaman": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
        "durum": durum(),
        "uyari": u,
        "sayac": {k: sum(1 for x in u if x["onem"] == k)
                  for k in ("kritik", "onemli", "bilgi")},
        "bugun": bugun(),
    }
