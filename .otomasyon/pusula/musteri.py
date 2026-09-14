# -*- coding: utf-8 -*-
"""
Müşteri dosyası üretici.
Seçilen aday için tek klasörde yedi şey çıkarır:
  analiz.html    → firmaya gösterilecek görünürlük analizi (demo sunumu)
  is-emri.md     → ekibin eline geçecek iç iş emri
  teklif.html    → müşteriye gönderilecek teklif sayfası
  mesajlar.md    → WhatsApp açılış + iki takip + e-posta metni
  sosyal-demo.html → sosyal medya eksikleri + sektöre özel demo kurgu + referanslar
  cekim-plani.svg  → sektöre özel örnek çekim planı (storyboard)
  strateji.html    → 90 günlük pazarlama stratejisi (kanal, içerik, yol haritası, bütçe, KPI)
Ayrıca WhatsApp bağlantısını ve e-posta gövdesini panele döner.
"""
import os, re, json, html, unicodedata, datetime, urllib.parse

from .ayarlar import CIKTI, SEKTORLER, FIRMA, SMTP
from .puanlama import (ETIKET, COZUM, oncelikli_eksikler, bizim_eksikler, sicak_mi,
                       karne, en_zayif_grup)
from .hedefkitle import HIZMETLER, SEKTOR_HIZMET
from .demo import demo_uret, PLAN
from . import iletisim as IL
from . import piyasa as PY
from . import deger as DG
from . import veritabani as vt
from . import sosyal as SO
from . import demo_sosyal as DS
from . import fark as FK
from . import referans as RF
from . import ornek as OR
from . import strateji as SR
from . import onizleme as ON
from . import gom as GM
from . import ulasim as UL

DOSYA_KOK = os.path.join(CIKTI, "musteri")


# ---------------------------------------------------------------- yardımcılar
def slugla(x, azami=48):
    from .sosyal import TR_HARF
    d = unicodedata.normalize("NFKD", (x or "").translate(TR_HARF)).encode("ascii", "ignore").decode()
    d = re.sub(r"-{2,}", "-", "".join(c if c.isalnum() else "-" for c in d.lower())).strip("-")
    return d[:azami] or "musteri"


def telefon_normalize(t):
    """TR numarasını 90XXXXXXXXXX biçimine getirir; çeviremezse None."""
    if not t:
        return None
    r = re.sub(r"\D", "", t)
    if r.startswith("00"):
        r = r[2:]
    if len(r) == 10 and r.startswith("5"):
        r = "90" + r
    elif len(r) == 11 and r.startswith("0"):
        r = "90" + r[1:]
    elif len(r) == 12 and r.startswith("90"):
        pass
    elif len(r) == 13 and r.startswith("090"):
        r = r[1:]
    else:
        return r if 11 <= len(r) <= 15 else None
    return r


def wa_link(telefon, metin):
    n = telefon_normalize(telefon)
    taban = "https://wa.me/%s" % n if n else "https://wa.me/"
    return taban + "?text=" + urllib.parse.quote(metin)


def mailto_link(adres, konu, govde):
    return "mailto:%s?subject=%s&body=%s" % (
        urllib.parse.quote(adres or ""), urllib.parse.quote(konu), urllib.parse.quote(govde))


# ---------------------------------------------------------------- zenginleştirme
# ÖNEMLİ: SQLite tek yazıcı kaldırır. Ağ işi (site gezme, sosyal doğrulama) saniyeler
# sürdüğü için veritabanı bağlantısı o süre boyunca AÇIK TUTULMAZ. İş ikiye ayrıldı:
#   arastir(aday)  → sadece ağ; veritabanına dokunmaz, paralel çalıştırılabilir
#   yaz(b, ...)    → sadece yazma; tek bağlantıda, tek iş parçacığında çalışır
def arastir(aday):
    """Ağ tarafı: firmanın sitesini gezer, sosyal hesapları eşleştirir.
    Veritabanına DOKUNMAZ — bu yüzden iş parçacıklarında paralel çağrılabilir."""
    bulgu = {"id": aday["id"], "ad": aday["ad"], "hata": None, "gezilen": [],
             "kanallar": [], "kisiler": [], "epostalar": [], "telefonlar": [],
             "sosyal_ad": [], "sosyal_denetim": None, "sosyal_skor": None,
             "sosyal_hata": None}

    tel_bilgi = []
    if aday.get("telefon"):
        t = IL.telefon_tipi(aday["telefon"])
        t["kaynak"] = "harita profili"
        tel_bilgi.append(t)
        bulgu["kanallar"].append(("telefon", t["normal"] or aday["telefon"],
                                  "harita profili", 1, t["aciklama"]))
        if t["wa"]:
            bulgu["kanallar"].append(("whatsapp", t["normal"], "harita profili (cep hattı)", 0,
                                      "numaranın WhatsApp'ta kayıtlı olduğu ancak mesaj atınca kesinleşir"))

    k = IL.site_kesif(aday.get("site"))
    bulgu["gezilen"] = k["gezilen"]
    if k["hata"]:
        bulgu["hata"] = k["hata"]
    else:
        for e in k["epostalar"]:
            bulgu["kanallar"].append(("eposta", e["deger"], e["kaynak"], 1, None))
            bulgu["epostalar"].append(e["deger"])
        for t in k["telefonlar"]:
            if not t["normal"]:
                continue
            bulgu["kanallar"].append(("telefon", t["normal"], t.get("kaynak"), 1, t["aciklama"]))
            if t["wa"]:
                bulgu["kanallar"].append(("whatsapp", t["normal"], t.get("kaynak"), 0,
                                          "sitede yayınlanan cep hattı"))
            if not any(x["normal"] == t["normal"] for x in tel_bilgi):
                tel_bilgi.append(t)
        for ad, sv in k["sosyal"].items():
            bulgu["kanallar"].append((ad, sv["url"], sv["kaynak"], 0, None))
            bulgu["sosyal_ad"].append(ad)
        bulgu["kisiler"] = k["kisiler"]

    bulgu["telefonlar"] = tel_bilgi

    # sosyal denetim: kanalları veritabanından değil, elimizdeki listeden veriyoruz
    try:
        eldeki = [{"tur": t2, "deger": d2, "kaynak": kk} for t2, d2, kk, _dg, _n in bulgu["kanallar"]]
        sd = SO.sosyal_denetle(aday["ad"], aday.get("sektor") or "isletme", eldeki,
                               sehir=aday.get("sehir") or "")
        bulgu["sosyal_denetim"] = sd
        bulgu["sosyal_skor"] = SO.sosyal_skor(sd)
        bulgu["sosyal_ad"] = sorted(set(bulgu["sosyal_ad"]) | set(sd["hesaplar"].keys()))
    except Exception as ex:
        bulgu["sosyal_hata"] = "%s: %s" % (type(ex).__name__, ex)

    return bulgu


def yaz(b, aday, bulgu):
    """Yazma tarafı: tek bağlantı, tek iş parçacığı. Ağ beklemesi yok."""
    aid = aday["id"]
    for tur, deger, kaynak, dogrulandi, not_ in bulgu["kanallar"]:
        if deger:
            vt.kanal_ekle(b, aid, tur, deger, kaynak, dogrulandi, not_)
    for kisi in bulgu["kisiler"]:
        vt.kisi_ekle(b, aid, kisi["isim"], kisi["unvan"], kaynak=kisi["kaynak"])
    if bulgu["sosyal_denetim"] is not None:
        vt.sosyal_kaydet(b, aid, bulgu["sosyal_denetim"], bulgu["sosyal_skor"])

    tel_bilgi = bulgu["telefonlar"]
    karar = IL.kanal_onerisi(tel_bilgi, bulgu["epostalar"])
    ilk_eposta = bulgu["epostalar"][0] if bulgu["epostalar"] else None
    mobil = next((t for t in tel_bilgi if t["wa"]), None)
    b.execute("""UPDATE adaylar SET eposta=COALESCE(?,eposta), telefon_tipi=?, wa_uygun=?, zengin=1,
                 durum=CASE WHEN COALESCE(durum,'yeni')='yeni' THEN 'arastirildi' ELSE durum END
                 WHERE id=?""",
              (ilk_eposta, (tel_bilgi[0]["tip"] if tel_bilgi else None),
               1 if mobil else 0, aid))

    sd = bulgu["sosyal_denetim"] or {}
    return {"id": aid, "ad": aday["ad"], "eposta": bulgu["epostalar"],
            "kisi": len(bulgu["kisiler"]), "sosyal": bulgu["sosyal_ad"],
            "telefonlar": tel_bilgi, "kanal": karar, "hata": bulgu["hata"],
            "gezilen": bulgu["gezilen"], "sosyal_denetim": bulgu["sosyal_denetim"],
            "sosyal_skor": bulgu["sosyal_skor"], "sosyal_eksik": len(sd.get("eksikler", [])),
            "sosyal_hata": bulgu["sosyal_hata"]}


def zenginlestir(b, aday):
    """Tek adayı sırayla araştırıp yazar (panel tek tek çağırırken kullanılıyor)."""
    return yaz(b, aday, arastir(aday))


# ---------------------------------------------------------------- bedel önerisi
# Sadece ÖNERİ; panelde değiştirilebiliyor ve teklifte "aralık" olarak sunuluyor.
ONERI = {
 "insaat-3d-modelleme": (65000, 185000, "proje ölçeğine göre"),
 "emlak-video":         (9000,  28000,  "mülk sayısına göre / aylık pakette daha düşük"),
 "urun-animasyon":      (38000, 120000, "ürün sayısı ve dil sayısına göre"),
 "klip-cekimi":         (45000, 140000, "mekân ve çekim günü sayısına göre"),
 "drone-cekimi":        (12000, 45000,  "tek çekim / aylık seri"),
 "dugun-cekimi":        (28000, 75000,  "pakete göre"),
 "isletme-tanitim":     (12000, 30000,  "aylık paket"),
}


def hizmet_anahtari(aday):
    return SEKTOR_HIZMET.get(aday.get("sektor"), "isletme-tanitim")


def bedel_onerisi(anahtar):
    a, b, notu = ONERI.get(anahtar, (15000, 45000, ""))
    return {"alt": a, "ust": b, "not": notu}


def _tl(x):
    try:
        return "{:,}".format(int(round(float(x)))).replace(",", ".") + " ₺"
    except Exception:
        return "—"


# ---------------------------------------------------------------- mesajlar
def mesajlar_uret(aday, eksikler, tahmin, anahtar, kisiler=None, kanal=None, detay=None):
    """Kanala göre üç ayrı metin: WhatsApp, e-posta, telefon açılışı."""
    ad = aday["ad"]
    imza = FIRMA.get("imza") or FIRMA["ad"]
    kisiler = kisiler or []
    kanit = (detay or {}).get("kanit", {})
    onc = oncelikli_eksikler(eksikler, 2)

    def kanit_cumle(k):
        kn = kanit.get(k)
        if not kn:
            return ETIKET.get(k, "").lower()
        return "%s (%s)" % (ETIKET.get(k, k).lower(), kn["bulgu"].lower())

    e1 = kanit_cumle(onc[0]) if onc else ""
    e2 = kanit_cumle(onc[1]) if len(onc) > 1 else ""
    ikili = e1 + ((", ayrıca " + e2) if e2 else "")
    yetkili = next((k for k in kisiler if k.get("isim")), None)
    hitap = ("Sayın %s" % yetkili["isim"]) if yetkili else "Merhaba"
    deger = DG.deger_cumlesi(anahtar, tahmin, eksikler)

    # --- karne: konuşmaya en zayıf başlıktan giriyoruz
    kn = karne(eksikler)
    zayif = en_zayif_grup(eksikler)

    def _kucult(x):
        """Cümle ortasına giren parçanın ilk harfini küçültür."""
        x = (x or "").strip()
        return (x[0].lower() + x[1:]) if x else x

    # kanıtı en zayıf grubun içinden seç — konuşma tutarlı olsun
    zayif_kodlar = oncelikli_eksikler(zayif.get("kodlar") or eksikler, 2)
    z1 = zayif_kodlar[0] if zayif_kodlar else (onc[0] if onc else None)
    zayif_bulgu = ((kanit.get(z1) or {}).get("bulgu")
                   or (ETIKET.get(z1, "") if z1 else "birkaç başlıkta kolay kazanç var"))
    sektor_k = aday.get("sektor") or "isletme"
    fark_c = (FK.farklar(sektor_k, 1) or [{}])[0]
    plan_c = (SO.icerik_plani(sektor_k, 1) or [{}])[0]
    ref_c = (RF.sektor_icin(sektor_k, 1) or [None])[0]

    # --- WhatsApp: tek somut bulgu + tek somut fikir + kolay cevap
    #     Amaç satmak değil, cevap almak. Onun için tek soru soruyoruz.
    wa = ("{hitap}, {imza}'dan yazıyorum — Bursa'da video ve 3D üretiyoruz.\n\n"
          "{ad}'ı internette aradık. En zayıf taraf şu: {zayif_ad} ({zayif_skor}/100). "
          "Somut örnek: {bulgu}\n\n"
          "Sizin sektörünüzde en çok işe yarayan şey şu: {fikir} — {kanca}.\n\n"
          "Ne bulduğumuzu kaynaklarıyla yazdığımız tek sayfalık bir analiz ve sizin için "
          "hazırladığımız çekim planı var. Göndereyim mi? (Ücretsiz, karşılığında bir şey istemiyorum.)"
          ).format(hitap=hitap, imza=imza, ad=ad,
                   zayif_ad=zayif.get("kisa", zayif["baslik"]), zayif_skor=zayif["skor"],
                   bulgu=zayif_bulgu,
                   fikir=plan_c.get("baslik", "kısa video"),
                   kanca=plan_c.get("kanca", "işin kendisini gösteren içerik"))

    # --- Telefon açılışı (sabit hat)
    telefon = ("{hitap}, ben {imza}'dan arıyorum, Bursa'dan. İki dakikanızı alacağım.\n\n"
               "{ad} için internetteki görünürlüğünüze baktık. En zayıf başlık {zayif_ad}; "
               "100 üzerinden {zayif_skor} çıktı. Örneğin: {bulgu}\n\n"
               "Şunu söylemek için aradım: {sektorde} genelde {siradan} Bizde ise {bizde}\n\n"
               "Ne bulduğumuzu kaynaklarıyla yazdık, bir de sizin için çekim planı hazırladık. "
               "WhatsApp'tan mı göndereyim, mail mi daha rahat?").format(
                   hitap=hitap, imza=imza, ad=ad,
                   zayif_ad=zayif.get("kisa", zayif["baslik"]), zayif_skor=zayif["skor"],
                   bulgu=zayif_bulgu,
                   sektorde="sizin sektörünüzde",
                   siradan=_kucult(fark_c.get("sıradan", "iş bir kere çekilip bırakılıyor.")),
                   bizde=_kucult(fark_c.get("bizde", "aynı çekimden birden çok sürüm çıkarıyoruz.")))

    # --- E-posta (uzun, kanıtlı)
    konu = "%s — dijital görünürlük analizi (%d başlıkta eksik)" % (ad, len(eksikler))
    kanit_satirlari = []
    for k in oncelikli_eksikler(eksikler, 4):
        kn = kanit.get(k)
        if kn:
            kanit_satirlari.append("  · %s\n      ne baktık: %s\n      ne bulduk: %s\n      kaynak: %s"
                                   % (ETIKET.get(k, k), kn["kontrol"], kn["bulgu"], kn["kaynak"]))
        else:
            kanit_satirlari.append("  · %s" % ETIKET.get(k, k))

    govde = """{hitap},

{imza} olarak {ad} için herkese açık bilgiler üzerinden bir görünürlük analizi çıkardık.
Hiçbir özel veri kullanmadık; baktığımız her şey sizin kendi sitenizde ve harita profilinizde
zaten yayında.

Öne çıkan bulgular:
{bulgular}

Toplam {n} başlıkta eksik göründü; bunların {b} tanesi doğrudan bizim çözdüğümüz işler.

Modelimize göre bu eksikler kapatıldığında aylık görüntülenme {g1} seviyesinden {g2} seviyesine,
aylık iletişim {i1} seviyesinden {i2} seviyesine çıkabiliyor. Bu rakamlar bir tahmindir,
garanti değildir — sizin gerçek verinizle çalıştırdığımızda çok daha isabetli oluyor.

Ne katıyoruz: {deger}

Neden biz: {fark_siradan}
Bizde ise: {fark_bizde}
Sonuç olarak: {fark_sonuc}

Nasıl çalışırız: {model_c}

Ekte dört dosya var:
  · analiz.html      — bulduklarımız, kaynaklarıyla birlikte
  · cekim-plani.svg  — sizin işiniz için hazırladığımız çekim planı (kare kare)
  · sosyal-demo.html — sosyal medya tarafı ve örnek kurgular
  · teklif.html      — önerdiğimiz çalışma, kapsamı ve bedeli

Çekim planını özellikle bir bakın: hazır bir görsel değil, sizin için yazılmış gerçek bir
plan. Beğenmezseniz de elinizde kalsın, kendi ekibinizle uygulayabilirsiniz.

15 dakikalık kısa bir görüşmede üzerinden geçelim mi? Uygun olduğunuz bir saat söyleyin,
ben arayayım.

İyi çalışmalar,
{imza}
{tel} · {site}""".format(
        hitap=hitap, imza=imza, ad=ad, bulgular="\n".join(kanit_satirlari),
        n=len(eksikler), b=len(bizim_eksikler(eksikler)), deger=deger,
        g1=tahmin.get("mevcut_goruntulenme"), g2=tahmin.get("hedef_goruntulenme"),
        i1=tahmin.get("mevcut_iletisim"), i2=tahmin.get("hedef_iletisim"),
        tel=FIRMA["telefon"], site=FIRMA["site"],
        fark_siradan=fark_c.get("sıradan", ""), fark_bizde=fark_c.get("bizde", ""),
        fark_sonuc=fark_c.get("sonuc", ""), model_c=FK.model_cumlesi(sektor_k))

    takip1 = ("{hitap}, geçen hafta {ad} için hazırladığımız görünürlük analizini paylaşmıştım. "
              "Bakabildiniz mi? Sorularınız olursa 10 dakikada hepsini konuşabiliriz.").format(hitap=hitap, ad=ad)
    takip2 = ("{hitap}, {ad} için hazırladığımız çalışma hâlâ masamızda. Şu an gündeminizde değilse "
              "sorun değil, uygun bir zamanda tekrar yazayım. Analiz sizde kalsın — içindeki maddelerin "
              "birkaçını kendi ekibinizle de uygulayabilirsiniz.").format(hitap=hitap, ad=ad)

    return {"acilis": wa, "whatsapp": wa, "telefon": telefon,
            "takip1": takip1, "takip2": takip2,
            "eposta_konu": konu, "eposta_govde": govde,
            "hitap": hitap, "yetkili": (yetkili["isim"] if yetkili else None),
            "onerilen_kanal": (kanal or {}).get("kanal")}


# ---------------------------------------------------------------- iş emri
def is_emri_uret(aday, eksikler, detay, tahmin, anahtar, bedel=None,
                 kisiler=None, kanallar=None, kanal=None, piyasa=None, dpaket=None,
                 sosyal=None):
    h = HIZMETLER.get(anahtar, {})
    adimlar = PLAN.get(anahtar, PLAN["isletme-tanitim"])
    biz = bizim_eksikler(eksikler)
    kanit = (detay or {}).get("kanit", {})
    site = (detay.get("site") or {}).get("site_url") or "yok"
    oneri = bedel_onerisi(anahtar)
    kisiler = kisiler or []
    kanallar = kanallar or []
    satir = []
    a = satir.append

    a("# İŞ EMRİ — %s" % aday["ad"])
    a("")
    a("| Alan | Değer |")
    a("|---|---|")
    a("| Sektör | %s |" % SEKTORLER.get(aday.get("sektor"), {}).get("ad", aday.get("sektor") or ""))
    a("| Şehir / ilçe | %s %s |" % (aday.get("sehir") or "", aday.get("ilce") or ""))
    a("| Web sitesi | %s |" % site)
    a("| Harita puanı | %s (%s yorum, %s fotoğraf) |" % (
        aday.get("puan") or "—", aday.get("yorum_sayisi") or 0, aday.get("fotograf_sayisi") or 0))
    a("| Görünürlük skoru | %s / 100 %s |" % (aday.get("skor"),
        "· SICAK ADAY" if sicak_mi(aday.get("skor") or 100) else ""))
    a("| Önerilen hizmet | %s |" % h.get("ad", anahtar))
    a("| Bedel | %s |" % (_tl(bedel) if bedel else "%s – %s (%s)" % (
        _tl(oneri["alt"]), _tl(oneri["ust"]), oneri["not"])))
    a("| Hazırlandı | %s |" % datetime.date.today().strftime("%d.%m.%Y"))
    a("")

    # --- iletişim
    a("## Kime, hangi kanaldan gidilecek")
    if kanal:
        a("**Önerilen kanal: %s** — %s" % (kanal.get("kanal", "?").upper(), kanal.get("gerekce", "")))
        if kanal.get("hedef"):
            a("Hedef: `%s`" % kanal["hedef"])
    a("")
    if kisiler:
        a("| Kişi | Ünvan | Kaynak |")
        a("|---|---|---|")
        for k in kisiler:
            a("| %s | %s | %s |" % (k.get("isim") or "—", k.get("unvan") or "—", k.get("kaynak") or "—"))
    else:
        a("*Sitede yayınlanmış yetkili ismi bulunamadı. İş emrinin sonundaki arama bağlantılarından*")
        a("*elle bakabilirsin — otomatik kişi kazıma yapmıyoruz.*")
    a("")
    if kanallar:
        a("| Kanal | Değer | Kaynak | Teyit |")
        a("|---|---|---|---|")
        for k in kanallar:
            a("| %s | %s | %s | %s |" % (k["tur"], k["deger"], k.get("kaynak") or "—",
                                         "doğrulandı" if k.get("dogrulandi") else "—"))
        a("")

    # --- kanıtlı eksikler
    a("## Tespit edilen eksikler (%d) — kanıtlı" % len(eksikler))
    a("")
    for k in eksikler:
        isaret = " **← bizim işimiz**" if k in biz else ""
        a("### %s%s" % (ETIKET.get(k, k), isaret))
        kn = kanit.get(k)
        if kn:
            a("- **Ne kontrol ettik:** %s" % kn["kontrol"])
            a("- **Ne bulduk:** %s" % kn["bulgu"])
            a("- **Kaynak:** %s · %s" % (kn["kaynak"], kn["zaman"]))
        a("- **Çözüm:** %s" % COZUM.get(k, "—"))
        a("")

    # --- tahmin
    a("## Tahmin (model çıktısı — garanti değil)")
    a("- Aylık görüntülenme: %s → %s (%%%s)" % (tahmin.get("mevcut_goruntulenme"),
      tahmin.get("hedef_goruntulenme"), tahmin.get("goruntulenme_artis_yuzde")))
    a("- Aylık iletişim: %s → %s" % (tahmin.get("mevcut_iletisim"), tahmin.get("hedef_iletisim")))
    a("- Aylık kazanılan iş: %s → %s" % (tahmin.get("mevcut_is"), tahmin.get("hedef_is")))
    a("- Aylık ek ciro tahmini: %s" % _tl(tahmin.get("ek_gelir")))
    a("")
    a("### Önce hangisini yapalım")
    for i, t in enumerate((tahmin.get("tekil_katki") or [])[:4], 1):
        a("%d. %s — tek başına +%s aylık iletişim" % (i, ETIKET.get(t["eksik"], t["eksik"]),
                                                      t["tek_basina_ek_iletisim"]))
    a("")

    # --- piyasa
    if piyasa:
        r = piyasa["referans"] if "referans" in piyasa else piyasa
        a("## Piyasa karşılaştırması")
        a("- %s için %s piyasası: **%s – %s** (orta nokta %s)" % (
            r["ad"], r.get("sehir") or "Türkiye", _tl(r["alt"]), _tl(r["ust"]), _tl(r["orta"])))
        if r.get("kendi_veri"):
            kv = r["kendi_veri"]
            a("- Kendi kaydettiğin %d rakip teklif ortalaması: **%s**" % (kv["adet"], _tl(kv["ortalama"])))
        if piyasa.get("yer"):
            a("- Bizim teklif (%s) piyasanın **%s** bandında (orta noktadan %%%s)" % (
                _tl(piyasa["teklif"]), piyasa["yer"], piyasa["fark_yuzde"]))
            a("- %s" % piyasa["yorum"])
        a("- Referans kalemleri:")
        for ad_k, tutar, kaynak in r["kalemler"]:
            a("  - %s: %s *(%s)*" % (ad_k, tutar, kaynak))
        a("- *%s*" % r["not"])
        a("")

    # --- değer yığını
    if dpaket:
        a("## Değer yığını — müşteriye ne anlatacağız")
        a("")
        a("| Kalem | Ayrı alınsa | Ne işe yarar |")
        a("|---|---|---|")
        for k in dpaket["yigin"]["kalemler"]:
            a("| %s%s | %s | %s |" % (k["ad"], " ★" if k["vurgu"] else "", k["deger_tl"], k["fayda"]))
        a("| **TOPLAM** | **%s** | |" % dpaket["yigin"]["toplam_tl"])
        if dpaket.get("teklif"):
            a("")
            a("Teklif **%s** → müşterinin eline geçen fark **%s** (%sx)." % (
                _tl(dpaket["teklif"]), dpaket["kazanc_tl"], dpaket.get("oran")))
        a("")
        a("**Risk tersine çevirme:** %s" % dpaket["risk"])
        a("")
        a("### İlk 30 gün")
        for ne_zaman, ne in dpaket["takvim"]:
            a("- **%s** — %s" % (ne_zaman, ne))
        a("")

    # --- satış notları
    if h:
        a("## Satış notları")
        a("- **Acı noktası:** %s" % (h.get("aci") or [""])[0])
        a("- **Kanal:** %s" % ", ".join(h.get("kanal", [])[:2]))
        a("- **Takip ritmi:** %s" % h.get("ritim", ""))
        a("- **Beklenen itiraz:** %s" % (h.get("itirazlar") or [("", "")])[0][0])
        a("  - *Cevap:* %s" % (h.get("itirazlar") or [("", "")])[0][1])
        a("- **Yanında götür:** %s" % ", ".join(h.get("kanit", [])))
        a("")

    # --- sosyal medya
    if sosyal and sosyal.get("eksikler") is not None:
        a("## Sosyal medya durumu (sosyal-demo.html ile birlikte gider)")
        a("- **Sosyal güç:** %d/100" % SO.sosyal_skor(sosyal))
        if sosyal.get("hesaplar"):
            for pl, hh in sosyal["hesaplar"].items():
                a("- **%s** — @%s (%s) · %s" % (hh.get("ad", pl), hh.get("kullanici", ""),
                                                hh.get("eslesme_yorum", ""), hh.get("nasil", "")))
                a("  - %s" % hh.get("url", ""))
        else:
            a("- Doğrulanabilen hesap yok — sıfırdan kurulum.")
        if sosyal["eksikler"]:
            a("")
            a("| Sosyal eksik | Ne kontrol ettik | Ne bulduk |")
            a("|---|---|---|")
            for e in sosyal["eksikler"]:
                kk = e["kanit"]
                a("| %s | %s | %s |" % (e["baslik"], kk["kontrol"], kk["bulgu"].replace("|", "/")))
        plan = SO.icerik_plani(aday.get("sektor") or "isletme", 6)
        tempo = SO.TEMPO.get(aday.get("sektor") or "isletme", SO.TEMPO["isletme"])
        a("")
        a("**Aylık tempo önerisi:** " + " · ".join(
            "%s %s" % (v, SO.FORMAT_AD.get(k2, k2).lower()) for k2, v in tempo.items() if v))
        a("")
        a("**Çekim listesi (ilk ay):**")
        for f in plan:
            a("- [ ] **%s** (%s) — %s" % (f["baslik"], f["format_ad"], f["kanca"]))
        a("")

    # --- elle bakılacak yerler
    a("## Elle bakılacak yerler (otomatik kazıma yok)")
    for ad_b, url in IL.arama_baglantilari(aday["ad"], aday.get("sehir")).items():
        a("- [%s](%s)" % (ad_b, url))
    a("")
    a("---")
    a("*Luna Pusula tarafından otomatik üretildi. Bulgular firmanın kendi sitesinden ve "
      "harita profilinden, kaynak adresleriyle birlikte alınmıştır. Fiyat referansları "
      "%s tarihinde derlenen yayınlanmış ajans listelerinden gelir.*" % PY.DERLEME_TARIHI)
    return "\n".join(satir)


# ---------------------------------------------------------------- teklif sayfası
TEKLIF = """<!DOCTYPE html><html lang="tr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>@AD@ — Teklif · Luna Yapım</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,800&family=Manrope:wght@400;500;600&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{--ink:#0A0A0C;--ink2:#131317;--bone:#EFEDE8;--kirmizi:#E8452C;--yesil:#3BA55C;--gri:#8C8A84;--cizgi:rgba(239,237,232,.13)}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--ink);color:var(--bone);font-family:"Manrope",system-ui,sans-serif;line-height:1.6}
.wrap{max-width:940px;margin:0 auto;padding:0 26px}
h1,h2,h3{font-family:"Bricolage Grotesque","Manrope",sans-serif;font-weight:800;letter-spacing:-.03em;line-height:1.05}
.etk{font-family:"Space Mono",ui-monospace,monospace;font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:var(--kirmizi)}
header{border-bottom:1px solid var(--cizgi);padding:18px 0}
.mrk{display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap}
.mrk b{font-family:"Bricolage Grotesque",sans-serif;font-size:17px}
.kapak{padding:60px 0 44px;border-bottom:1px solid var(--cizgi);background:linear-gradient(180deg,var(--ink2),var(--ink))}
.kapak h1{font-size:clamp(28px,4.6vw,46px);margin:14px 0 16px}
.kapak p{color:rgba(239,237,232,.76);max-width:62ch}
section{padding:44px 0;border-bottom:1px solid var(--cizgi)}
section h2{font-size:clamp(22px,3.2vw,31px);margin-bottom:14px}
section h3{font-size:18px;margin:24px 0 10px}
ul{list-style:none}
li{padding:8px 0 8px 22px;position:relative;color:rgba(239,237,232,.82)}
li::before{content:"\2192";position:absolute;left:0;color:var(--kirmizi)}
table{width:100%;border-collapse:collapse;font-size:14.5px;margin-top:10px}
th,td{text-align:left;padding:11px 12px;border-bottom:1px solid var(--cizgi);vertical-align:top}
th{font-family:"Space Mono",monospace;font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--kirmizi)}
td{color:rgba(239,237,232,.8)}
td.sag,th.sag{text-align:right;white-space:nowrap}
tr.top td{border-top:2px solid var(--kirmizi);font-weight:700;color:var(--bone)}
.adim{display:grid;grid-template-columns:48px 1fr;gap:14px;padding:13px 0;border-bottom:1px solid var(--cizgi)}
.adim .n{font-family:"Space Mono",monospace;font-size:11px;color:var(--kirmizi);padding-top:4px}
.adim b{display:block;font-size:16px;margin-bottom:3px}
.adim p{color:var(--gri);font-size:14.5px}
.bedel{background:var(--ink2);border:1px solid var(--kirmizi);border-radius:4px;padding:26px;margin-top:18px}
.bedel .buyuk{font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:36px;line-height:1.1}
.bedel small{color:var(--gri);display:block;margin-top:8px;font-size:13.5px}
.kazanc{display:inline-block;margin-top:14px;border:1px solid var(--yesil);color:var(--yesil);
padding:8px 14px;border-radius:2px;font-family:"Space Mono",monospace;font-size:12px;letter-spacing:.1em}
.risk{border-left:3px solid var(--yesil);background:rgba(59,165,92,.08);padding:16px 18px;
margin-top:18px;border-radius:0 3px 3px 0}
.risk b{color:var(--yesil)}
.uyari{border-left:3px solid var(--kirmizi);background:rgba(232,69,44,.07);padding:14px 16px;margin-top:18px;font-size:14px;color:rgba(239,237,232,.78)}
.kanit{font-size:12.6px;color:var(--gri);margin-top:6px;line-height:1.5}
.kanit code{font-family:"Space Mono",monospace;font-size:11.5px;color:#a9a7a2}
.cta{background:var(--kirmizi);color:#fff;padding:44px 0}
.cta h2{max-width:20ch}
.btn{display:inline-block;margin-top:18px;margin-right:10px;background:var(--ink);color:var(--bone);
padding:13px 22px;border-radius:2px;text-decoration:none;font-weight:600}
.btn.c{background:transparent;border:1px solid rgba(255,255,255,.55);color:#fff}
footer{padding:26px 0;color:var(--gri);font-size:12.5px}
</style></head><body>
<header><div class="wrap mrk"><b>LUNA YAPIM</b><span class="etk">Teklif · @TARIH@</span></div></header>
<div class="kapak"><div class="wrap">
  <p class="etk">@SEKTOR@ · @SEHIR@</p>
  <h1>@AD@ için önerimiz</h1>
  <p>@GIRIS@</p>
</div></div>

<section><div class="wrap">
  <h2>Ne bulduk</h2>
  <p style="color:rgba(239,237,232,.8);max-width:64ch">Aşağıdaki her satır, sizin kendi sitenizde ve
     harita profilinizde <strong>bugün yayında olan</strong> duruma bakılarak yazıldı. Hiçbiri tahmin değil;
     ne kontrol ettiğimiz ve ne bulduğumuz kaynağıyla birlikte yazılı.</p>
  <div class='tablo-kaydir'><table><tr><th>Eksik</th><th>Ne kontrol ettik / ne bulduk</th></tr>@BULGULAR@</table></div>
</div></section>

<section><div class="wrap">
  <h2>Eksikler kapanırsa</h2>
  <div class='tablo-kaydir'><table><tr><th>Şu an</th><th>Çalışma sonrası (tahmin)</th></tr>
    <tr><td>Aylık görüntülenme: @G1@</td><td>@G2@ (%@ARTIS@)</td></tr>
    <tr><td>Aylık iletişim: @I1@</td><td>@I2@</td></tr>
    <tr><td>Aylık kazanılan iş: @IS1@</td><td>@IS2@</td></tr>
  </table></div>
  <div class="uyari">Bu rakamlar bir modelleme tahminidir, garanti değildir. Kendi verilerinizi
    paylaşırsanız modeli sizin gerçek rakamlarınızla yeniden çalıştırırız.</div>
</div></section>

<section><div class="wrap">
  <h2>@HIZMET@</h2>
  @ADIMLAR@
</div></section>

<section><div class="wrap">
  <h2>Ne alıyorsunuz, ayrı ayrı ne tutar</h2>
  <p style="color:rgba(239,237,232,.8);max-width:64ch">Aşağıdaki kalemleri tek tek, farklı yerlerden
     almaya kalksanız ödeyeceğiniz tutarlar. Fiyatlar yayınlanmış ajans listelerinden derlenmiştir.</p>
  <div class='tablo-kaydir'><table>
    <tr><th>Kalem</th><th class="sag">Ayrı alınsa</th><th>Ne işe yarar</th></tr>
    @YIGIN@
    <tr class="top"><td>Toplam</td><td class="sag">@YIGIN_TOPLAM@</td><td></td></tr>
  </table></div>
  @KAZANC@
</div></section>

<section><div class="wrap">
  <h2>Piyasa neresi</h2>
  @PIYASA@
</div></section>

<section><div class="wrap">
  <h2>Kapsam ve bedel</h2>
  <ul>@TESLIM@</ul>
  <div class="bedel">
    <span class="etk">Bedel</span>
    <div class="buyuk">@BEDEL@</div>
    <small>@BEDEL_NOT@ · Ödeme: başlangıçta ön ödeme, teslimde kalan. Teklif 30 gün geçerlidir.</small>
  </div>
  <div class="risk"><b>Riski biz alıyoruz.</b><br>@RISK@</div>
</div></section>

<section><div class="wrap">
  <h2>İlk 30 gün</h2>
  @TAKVIM@
</div></section>

<div class="cta"><div class="wrap">
  <p class="etk" style="color:rgba(255,255,255,.75)">Sıradaki adım</p>
  <h2>15 dakikalık bir görüşmede üzerinden geçelim.</h2>
  <a class="btn" href="https://wa.me/@WA@">WhatsApp'tan yaz</a>
  <a class="btn c" href="tel:@TEL@">@TEL@</a>
</div></div>
<footer><div class="wrap mrk"><span>Luna Yapım · lunayapim.com · Bursa</span><span>@TARIH@</span></div></footer>
</body></html>"""


def teklif_uret(aday, eksikler, tahmin, anahtar, bedel=None, detay=None,
                piyasa=None, dpaket=None):
    h = HIZMETLER.get(anahtar, {})
    adimlar = PLAN.get(anahtar, PLAN["isletme-tanitim"])
    oneri = bedel_onerisi(anahtar)
    kanit = (detay or {}).get("kanit", {})
    teslim = {
     "insaat-3d-modelleme": ["Dış cephe render seti (gündüz / gün batımı / gece)",
        "60–90 sn proje tanıtım animasyonu", "Daire tipi başına iç mekân görselleri",
        "Kuşbakışı yerleşim maketi", "Yatay, dikey ve kare video kesimleri", "İki tur revizyon"],
     "emlak-video": ["İlan sitesi için kısa sürüm", "Web ve sunum için tam film",
        "Dikey ve kare sosyal medya kesimleri", "Havadan ve içeriden fotoğraflar",
        "İstenirse 360° sanal tur", "İki tur revizyon"],
     "urun-animasyon": ["Ürün 3D modelleme (model sizde kalır)", "Çalışma prensibi / kesit animasyonu",
        "Fuar için sessiz döngü sürümü", "Yatay, dikey ve kare kesimler",
        "Türkçe seslendirme (ek dil opsiyonel)", "İki tur revizyon"],
     "klip-cekimi": ["Konsept ve storyboard", "Çekim günü (ekip + ekipman)",
        "Sinematik renk düzenleme", "YouTube sürümü + dikey kesimler", "Teaser", "İki tur revizyon"],
     "drone-cekimi": ["Havadan 4K video", "Yüksek çözünürlüklü hava fotoğrafları",
        "Dikey ve kare kesimler", "İzin takibi", "Kurgu ve renk düzenleme"],
     "dugun-cekimi": ["İki kamera + drone", "Hazırlıktan geceye tam gün çekim",
        "Ertesi gün teaser", "8–12 dakikalık tam film", "Dikey kesimler"],
     "isletme-tanitim": ["Aylık tek çekim günü", "8–12 altyazılı kısa dikey video",
        "20–30 fotoğraf", "Google işletme profili düzenlemesi", "İçerik takvimi", "Aylık ölçüm"],
    }.get(anahtar, ["Çekim", "Kurgu", "Çoklu format teslim"])

    giris = ("%s için hazırladığımız görünürlük analizinin ardından, en hızlı sonuç verecek çalışmayı "
             "aşağıda topladık. Kapsam ve bedel nettir; sonradan kalem eklenmez." % aday["ad"])

    # bulgular tablosu
    bulgular = []
    for k in eksikler:
        kn = kanit.get(k)
        icerik = "—"
        if kn:
            icerik = ("<b>Kontrol:</b> %s<div class='kanit'><b>Bulgu:</b> %s<br>"
                      "<code>kaynak: %s · %s</code></div>"
                      % (html.escape(kn["kontrol"]), html.escape(kn["bulgu"]),
                         html.escape(str(kn["kaynak"])), html.escape(kn["zaman"])))
        bulgular.append("<tr><td><strong>%s</strong></td><td>%s</td></tr>"
                        % (html.escape(ETIKET.get(k, k)), icerik))

    # değer yığını
    yigin_satir, yigin_toplam, kazanc_html = "", "—", ""
    if dpaket:
        yigin_satir = "".join(
            "<tr><td>%s%s</td><td class='sag'>%s</td><td>%s</td></tr>"
            % (html.escape(k["ad"]), " ★" if k["vurgu"] else "", k["deger_tl"], html.escape(k["fayda"]))
            for k in dpaket["yigin"]["kalemler"])
        yigin_toplam = dpaket["yigin"]["toplam_tl"]
        if dpaket.get("teklif") and dpaket.get("kazanc", 0) > 0:
            kazanc_html = ("<span class='kazanc'>Teklif %s → aradaki fark %s · %sx değer</span>"
                           % (_tl(dpaket["teklif"]), dpaket["kazanc_tl"], dpaket.get("oran")))

    # piyasa bloğu
    piyasa_html = "<p style='color:var(--gri)'>Piyasa referansı bulunamadı.</p>"
    if piyasa:
        r = piyasa.get("referans", piyasa)
        kalem = "".join("<tr><td>%s</td><td class='sag'>%s</td><td><small>%s</small></td></tr>"
                        % (html.escape(a2), html.escape(t2), html.escape(k2))
                        for a2, t2, k2 in r["kalemler"])
        konum_c = ""
        if piyasa.get("yer"):
            konum_c = ("<p style='margin-top:14px'>Bu teklif, %s piyasasının <strong>%s</strong> bandında "
                       "duruyor (orta nokta %s).</p>" % (html.escape(r.get("sehir") or "Türkiye"),
                                                          html.escape(piyasa["yer"]), _tl(r["orta"])))
        piyasa_html = ("<p style='color:rgba(239,237,232,.8);max-width:64ch'>%s için %s piyasasında "
                       "yayınlanmış aralık: <strong>%s – %s</strong>.</p>%s"
                       "<div class='tablo-kaydir'><table><tr><th>Referans kalem</th><th class='sag'>Piyasa</th><th>Kaynak</th></tr>%s</table></div>"
                       "<div class='uyari'>%s<br><br>Fiyat referansları %s tarihinde yayınlanmış ajans "
                       "listelerinden derlenmiştir; canlı piyasa verisi değildir.</div>"
                       % (html.escape(r["ad"]), html.escape(r.get("sehir") or "Türkiye"),
                          _tl(r["alt"]), _tl(r["ust"]), konum_c, kalem,
                          html.escape(r["not"]), PY.DERLEME_TARIHI))

    takvim_html = ""
    if dpaket and dpaket.get("takvim"):
        takvim_html = "".join(
            "<div class='adim'><span class='n'>%s</span><div><b>%s</b><p>%s</p></div></div>"
            % ("●", html.escape(a3), html.escape(b3)) for a3, b3 in dpaket["takvim"])

    g = TEKLIF
    yer = {
      "@AD@": html.escape(aday["ad"]),
      "@SEKTOR@": html.escape(SEKTORLER.get(aday.get("sektor"), {}).get("ad", aday.get("sektor") or "")),
      "@SEHIR@": html.escape(aday.get("sehir") or ""),
      "@TARIH@": datetime.date.today().strftime("%d.%m.%Y"),
      "@GIRIS@": html.escape(giris),
      "@BULGULAR@": "".join(bulgular),
      "@G1@": str(tahmin.get("mevcut_goruntulenme", "—")),
      "@G2@": str(tahmin.get("hedef_goruntulenme", "—")),
      "@ARTIS@": str(tahmin.get("goruntulenme_artis_yuzde", "—")),
      "@I1@": str(tahmin.get("mevcut_iletisim", "—")),
      "@I2@": str(tahmin.get("hedef_iletisim", "—")),
      "@IS1@": str(tahmin.get("mevcut_is", "—")),
      "@IS2@": str(tahmin.get("hedef_is", "—")),
      "@HIZMET@": html.escape(h.get("ad", anahtar)),
      "@ADIMLAR@": "".join('<div class="adim"><span class="n">%02d</span><div><b>%s</b><p>%s</p></div></div>'
                           % (i, html.escape(b4), html.escape(p4)) for i, (b4, p4) in enumerate(adimlar, 1)),
      "@YIGIN@": yigin_satir,
      "@YIGIN_TOPLAM@": yigin_toplam,
      "@KAZANC@": kazanc_html,
      "@PIYASA@": piyasa_html,
      "@TESLIM@": "".join("<li>%s</li>" % html.escape(x) for x in teslim),
      "@BEDEL@": _tl(bedel) if bedel else "%s – %s" % (_tl(oneri["alt"]), _tl(oneri["ust"])),
      "@BEDEL_NOT@": html.escape("" if bedel else oneri["not"] or "kapsama göre"),
      "@RISK@": html.escape((dpaket or {}).get("risk", "")),
      "@TAKVIM@": takvim_html,
      "@WA@": FIRMA["wa"],
      "@TEL@": FIRMA["telefon"],
    }
    for k2, v2 in yer.items():
        g = g.replace(k2, v2)
    return g


# ---------------------------------------------------------------- ana üretici
def dosya_uret(aday, eksikler, detay, tahmin, bedel=None, anahtar=None, b=None):
    """Aday için tam müşteri dosyasını üretir, yolları ve iletişim kararını döner."""
    anahtar = anahtar or hizmet_anahtari(aday)
    sehir = aday.get("sehir")
    klasor = os.path.join(DOSYA_KOK, "%s-%s" % (aday["id"], slugla(aday["ad"])))
    os.makedirs(klasor, exist_ok=True)

    # --- iletişim bilgileri
    kisiler, kanallar = [], []
    if b is not None:
        kisiler = vt.kisiler_getir(b, aday["id"])
        kanallar = vt.kanallar_getir(b, aday["id"])
    tel_listesi = [IL.telefon_tipi(k["deger"]) for k in kanallar if k["tur"] == "telefon"]
    if not tel_listesi and aday.get("telefon"):
        tel_listesi = [IL.telefon_tipi(aday["telefon"])]
    epostalar = [k["deger"] for k in kanallar if k["tur"] == "eposta"]
    if not epostalar and aday.get("eposta"):
        epostalar = [aday["eposta"]]
    kanal = IL.kanal_onerisi(tel_listesi, epostalar)
    # sektörün karar yapısına göre ulaşım planı (varsayım → ölçüm)
    bulunan = set()
    if any(t.get("wa") for t in tel_listesi): bulunan.add("whatsapp")
    if tel_listesi: bulunan.add("telefon")
    if epostalar: bulunan.add("eposta")
    if (aday.get("adres") or "").strip(): bulunan.add("ziyaret")
    ulasim_plani = UL.oneri(aday.get("sektor"), bulunan, b)
    kanal["sektor_sira"] = ulasim_plani["sira"]
    kanal["saat"] = ulasim_plani["saat"]
    kanal["kacin"] = ulasim_plani["kacin"]
    kanal["karar"] = ulasim_plani["karar"]
    kanal["kanca"] = ulasim_plani["kanca"]
    kanal["plan_kaynak"] = ulasim_plani["kaynak"]

    # --- piyasa ve değer
    if not bedel:
        bedel = PY.oneri(anahtar, sehir, b)
    piyasa = PY.konum(anahtar, bedel, sehir, b) or {"referans": PY.referans(anahtar, sehir, b)}
    dpaket = DG.paket(anahtar, bedel, eksikler, sehir)

    # --- sosyal medya (denetim + demo sayfası)
    sosyal_demo, sosyal_sonuc = None, None
    try:
        if b is not None:
            sosyal_sonuc = vt.sosyal_getir(b, aday["id"])
        if sosyal_sonuc is None:
            sosyal_sonuc = SO.sosyal_denetle(aday["ad"], aday.get("sektor") or "isletme",
                                             kanallar, tahmin_et=False,
                                             sehir=aday.get("sehir") or "")
            if b is not None:
                vt.sosyal_kaydet(b, aday["id"], sosyal_sonuc, SO.sosyal_skor(sosyal_sonuc))
        sosyal_demo, _ = DS.uret(aday, sosyal_sonuc, klasor=klasor)
    except Exception as ex:
        sosyal_demo = None
        sosyal_sonuc = {"hata": "%s: %s" % (type(ex).__name__, ex)}

    # --- örnek çalışma görseli (sektöre özel çekim planı)
    cekim_plani = None
    try:
        cekim_plani = OR.yaz(aday.get("sektor") or "isletme",
                             os.path.join(klasor, "cekim-plani.svg"),
                             aday["ad"], sehir or "")
    except Exception:
        cekim_plani = None

    # --- pazarlama stratejisi
    strateji_yol, strateji = None, None
    try:
        strateji_yol, strateji = SR.yaz(aday, eksikler, detay, tahmin, klasor,
                                        sosyal_sonuc, bedel)
    except Exception as ex:
        strateji_yol = None
        detay.setdefault("_hata", {})["strateji"] = "%s: %s" % (type(ex).__name__, ex)

    # --- analiz
    t = dict(tahmin)
    t["_skor"] = aday.get("skor", 0)
    analiz, _ = demo_uret(aday, eksikler, detay, t, klasor=klasor,
                          sosyal=sosyal_sonuc, strateji=strateji)
    if os.path.basename(analiz) != "analiz.html":
        hedef = os.path.join(klasor, "analiz.html")
        os.replace(analiz, hedef)
        analiz = hedef

    # --- iş emri
    is_emri = os.path.join(klasor, "is-emri.md")
    open(is_emri, "w", encoding="utf-8").write(
        is_emri_uret(aday, eksikler, detay, tahmin, anahtar, bedel,
                     kisiler, kanallar, kanal, piyasa, dpaket, sosyal_sonuc))

    # --- teklif
    teklif = os.path.join(klasor, "teklif.html")
    open(teklif, "w", encoding="utf-8").write(
        teklif_uret(aday, eksikler, tahmin, anahtar, bedel, detay, piyasa, dpaket))

    # --- firmaya özel önizleme paketi (poster, film, site/sosyal/aşama/kalite taslakları)
    onizleme_paket = {}
    try:
        onizleme_paket = ON.paket(aday["ad"], aday.get("site") or "", klasor,
                                  hizmet=anahtar, eksik_kodlari=eksikler,
                                  telefon=aday.get("telefon"))
    except Exception as ex:
        onizleme_paket = {"not": ["Önizleme üretilemedi: %s: %s" % (type(ex).__name__, ex)]}

    # --- teklifin tek dosyalık sürümü (görseller ve video gömülü)
    teklif_tek = None
    try:
        teklif_tek, _boy = GM.gom(teklif, klasor)
    except Exception as ex:
        detay.setdefault("_hata", {})["gom"] = "%s: %s" % (type(ex).__name__, ex)

    # --- mesajlar
    m = mesajlar_uret(aday, eksikler, tahmin, anahtar, kisiler, kanal, detay)
    mesaj_yolu = os.path.join(klasor, "mesajlar.md")
    kanal_notu = "**Önerilen kanal: %s** — %s\n\n" % (kanal["kanal"].upper(), kanal["gerekce"])
    open(mesaj_yolu, "w", encoding="utf-8").write(
        "# MESAJLAR — %s\n\n%s## WhatsApp açılış%s\n%s\n\n## Telefon açılışı (sabit hat için)\n%s\n\n"
        "## 1. takip (3. gün)\n%s\n\n## 2. takip (10. gün)\n%s\n\n"
        "## E-posta\n**Konu:** %s\n\n```\n%s\n```\n"
        % (aday["ad"], kanal_notu,
           "" if kanal["kanal"] == "whatsapp" else " *(cep hattı yok — bu kanal kapalı)*",
           m["whatsapp"], m["telefon"], m["takip1"], m["takip2"],
           m["eposta_konu"], m["eposta_govde"]))

    wa_numara = next((t2["normal"] for t2 in tel_listesi if t2["wa"]), None)
    return {
        "klasor": klasor,
        "analiz": analiz, "is_emri": is_emri, "teklif": teklif, "mesajlar": mesaj_yolu,
        "teklif_tek": teklif_tek,
        "onizleme": onizleme_paket,
        "sosyal_demo": sosyal_demo,
        "cekim_plani": cekim_plani,
        "strateji": strateji_yol,
        "sosyal": {"skor": SO.sosyal_skor(sosyal_sonuc) if sosyal_sonuc and "eksikler" in sosyal_sonuc else None,
                   "hesaplar": list((sosyal_sonuc or {}).get("hesaplar", {}).keys()),
                   "eksik": len((sosyal_sonuc or {}).get("eksikler", []))},
        "hizmet": anahtar, "hizmet_ad": HIZMETLER.get(anahtar, {}).get("ad", anahtar),
        "wa": wa_link(wa_numara, m["whatsapp"]) if wa_numara else None,
        "wa_numara": wa_numara,
        "mailto": mailto_link(epostalar[0], m["eposta_konu"], m["eposta_govde"]) if epostalar else None,
        "epostalar": epostalar,
        "telefonlar": tel_listesi,
        "kanal": kanal,
        "ulasim": ulasim_plani,
        "kisiler": kisiler,
        "kanallar": kanallar,
        "mesaj": m,
        "bedel": bedel,
        "bedel_oneri": bedel_onerisi(anahtar),
        "piyasa": piyasa,
        "deger": {"toplam": dpaket["yigin"]["toplam"], "toplam_tl": dpaket["yigin"]["toplam_tl"],
                  "kazanc_tl": dpaket.get("kazanc_tl"), "oran": dpaket.get("oran"),
                  "risk": dpaket["risk"]},
        "arama": IL.arama_baglantilari(aday["ad"], sehir),
    }


# ---------------------------------------------------------------- e-posta
def eposta_gonder(alici, konu, govde, ekler=None):
    """SMTP ayarlıysa gönderir. (sunucu, kullanıcı, şifre ayarlar.json'dan)"""
    import smtplib, ssl
    from email.message import EmailMessage
    if not SMTP.get("sunucu") or not SMTP.get("kullanici"):
        return False, "SMTP ayarlı değil — Ayarlar sekmesinden doldurun."
    if not alici:
        return False, "Alıcı e-posta adresi yok."
    m = EmailMessage()
    m["From"] = SMTP.get("gonderen") or SMTP["kullanici"]
    m["To"] = alici
    m["Subject"] = konu
    m.set_content(govde)
    for yol in (ekler or []):
        try:
            with open(yol, "rb") as f:
                m.add_attachment(f.read(), maintype="text", subtype="html",
                                 filename=os.path.basename(yol))
        except Exception:
            pass
    try:
        ctx = ssl.create_default_context()
        with smtplib.SMTP(SMTP["sunucu"], int(SMTP.get("kapi") or 587), timeout=25) as s:
            s.starttls(context=ctx)
            s.login(SMTP["kullanici"], SMTP["sifre"])
            s.send_message(m)
        return True, "gönderildi"
    except Exception as ex:
        return False, "%s: %s" % (type(ex).__name__, ex)
