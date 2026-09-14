# -*- coding: utf-8 -*-
"""
Luna Pusula — komut satırı.

  python3 -m pusula.cli tara   --sehir Bursa --sektor insaat [--adet 60]
  python3 -m pusula.cli denetle --sehir Bursa [--hizli] [--adet 50]
  python3 -m pusula.cli hesapla --sehir Bursa
  python3 -m pusula.cli demo    --sehir Bursa [--adet 20] [--sadece-sicak]
  python3 -m pusula.cli rapor   --sehir Bursa
  python3 -m pusula.cli tumu    --sehir Bursa --sektor insaat      (hepsi sırayla)
  python3 -m pusula.cli liste   --sehir Bursa
"""
import argparse, json, sys, os, time
from concurrent.futures import ThreadPoolExecutor

from . import veritabani as vt
from .ayarlar import SEKTORLER, CIKTI
from . import ayarlar
from .kaynaklar import google_places, osm
from .tespit import eksikleri_bul
from .puanlama import skorla, sicak_mi, ETIKET
from .tahmin import hesapla as tahmin_hesapla
from .demo import demo_uret
from . import rapor as rapor_mod


def komut_tara(a):
    b = vt.baglan()
    sektorler = [a.sektor] if a.sektor else list(SEKTORLER)
    yeni = toplam = 0
    for sk in sektorler:
        if sk not in SEKTORLER:
            print("  ! bilinmeyen sektör:", sk); continue
        tanim = SEKTORLER[sk]
        bulunan = []
        if ayarlar.GOOGLE_ANAHTAR:
            for sorgu in tanim["aramalar"]:
                bulunan += google_places.ara(sorgu, a.sehir, azami=a.adet)
                time.sleep(0.4)
        else:
            bulunan = osm.ara(tanim["osm"], a.sehir, azami=a.adet)
        gorulen = set()
        for k in bulunan:
            if not k["ad"] or k["kaynak_id"] in gorulen: continue
            gorulen.add(k["kaynak_id"])
            k["sektor"] = sk; k["sehir"] = a.sehir
            k.setdefault("ilce", "")
            toplam += 1
            if vt.aday_ekle(b, k): yeni += 1
        print("  %-28s %3d bulundu" % (tanim["ad"], len(gorulen)))
    b.commit()
    kaynak = "Google Places" if ayarlar.GOOGLE_ANAHTAR else "OpenStreetMap (anahtar yok)"
    print("→ %s | toplam %d kayıt, %d yeni" % (kaynak, toplam, yeni))
    if not ayarlar.GOOGLE_ANAHTAR:
        print("  ipucu: GOOGLE_MAPS_API_KEY tanımlarsan puan/yorum/fotoğraf verisi de gelir.")


def komut_denetle(a):
    b = vt.baglan()
    q = "SELECT * FROM adaylar"; p = []
    k = []
    if a.sehir:  k.append("sehir=?");  p.append(a.sehir)
    if a.sektor: k.append("sektor=?"); p.append(a.sektor)
    if k: q += " WHERE " + " AND ".join(k)
    q += " ORDER BY id"
    if a.adet: q += " LIMIT %d" % a.adet
    adaylar = [dict(r) for r in b.execute(q, p).fetchall()]
    if not adaylar:
        print("  aday yok — önce 'tara' çalıştır."); return

    def is_(ad):
        try:
            eks, det = eksikleri_bul(ad, hizli=a.hizli)
            return ad, eks, det
        except Exception as ex:
            return ad, ["site_bozuk"], {"hata": str(ex)[:120]}

    print("  %d aday denetleniyor%s..." % (len(adaylar), " (hızlı)" if a.hizli else ""))
    with ThreadPoolExecutor(max_workers=6) as h:
        for i, (ad, eks, det) in enumerate(h.map(is_, adaylar), 1):
            s = skorla(eks)
            vt.denetim_kaydet(b, ad["id"], s, eks, det)
            isaret = "SICAK" if sicak_mi(s) else "     "
            print("   %3d/%d  %-34s skor %3d  %s  (%d eksik)" %
                  (i, len(adaylar), ad["ad"][:34], s, isaret, len(eks)))
            if i % 10 == 0: b.commit()
    b.commit()
    print("→ denetim bitti")


def komut_zenginlestir(a):
    """Adayların sitesini gezip iletişim ve yetkili bilgisi toplar."""
    from . import musteri as M
    b = vt.baglan()
    q = "SELECT * FROM adaylar"; p = []; k = []
    if a.sehir:  k.append("sehir=?");  p.append(a.sehir)
    if a.sektor: k.append("sektor=?"); p.append(a.sektor)
    if getattr(a, "sadece_yeni", False): k.append("COALESCE(zengin,0)=0")
    if k: q += " WHERE " + " AND ".join(k)
    q += " ORDER BY id"
    if a.adet: q += " LIMIT %d" % a.adet
    adaylar = [dict(r) for r in b.execute(q, p).fetchall()]
    if not adaylar:
        print("  zenginleştirilecek aday yok (hepsi daha önce araştırılmış)."); b.close(); return
    print("  %d aday araştırılıyor..." % len(adaylar))
    # Ağ işi paralel, YAZMA tek bağlantıda ve tek iş parçacığında.
    # (SQLite tek yazıcı kaldırır; her iş parçacığına ayrı bağlantı açmak
    #  "database is locked" hatası veriyordu.)
    with ThreadPoolExecutor(max_workers=4) as h:
        for i, (ad, bulgu) in enumerate(zip(adaylar, h.map(M.arastir, adaylar)), 1):
            ozet = M.yaz(b, ad, bulgu)
            b.commit()
            print("   %3d/%d  %-32s %s" % (
                i, len(adaylar), ozet["ad"][:32],
                ("HATA: " + ozet["hata"]) if ozet["hata"] else
                "%d e-posta · %d kişi · %d sosyal%s · kanal: %s" % (
                    len(ozet["eposta"]), ozet["kisi"], len(ozet["sosyal"]),
                    ("" if ozet["sosyal_skor"] is None else " (güç %d)" % ozet["sosyal_skor"]),
                    ozet["kanal"]["kanal"])))
    b.commit()
    # ana bağlantıda da güncelleme yapılmış olabilir; tekrar oku
    n = b.execute("SELECT COUNT(*) FROM adaylar WHERE zengin=1").fetchone()[0]
    print("→ %d aday zenginleştirildi" % n)
    b.close()


def komut_hesapla(a):
    b = vt.baglan()
    satirlar = vt.son_denetimler(b, a.sehir, a.sektor)
    for r in satirlar:
        eks = json.loads(r["eksikler"])
        t = tahmin_hesapla(r, eks, ortalama_is=a.ortalama_is)
        vt.tahmin_kaydet(b, r["id"], t)
    b.commit()
    print("→ %d aday için tahmin hesaplandı" % len(satirlar))


def komut_demo(a):
    b = vt.baglan()
    satirlar = vt.son_denetimler(b, a.sehir, a.sektor, limit=a.adet)
    n = 0
    for r in satirlar:
        if a.sadece_sicak and not sicak_mi(r["skor"]): continue
        eks = json.loads(r["eksikler"]); det = json.loads(r["detay"])
        t = vt.son_tahmin(b, r["id"])
        t = json.loads(t["detay"]) if t else tahmin_hesapla(r, eks)
        t["_skor"] = r["skor"]
        dosya, mesaj = demo_uret(r, eks, det, t)
        vt.demo_kaydet(b, r["id"], dosya, mesaj)
        n += 1
        print("   %-34s → %s" % (r["ad"][:34], os.path.basename(dosya)))
    b.commit()
    print("→ %d demo üretildi → %s/demo" % (n, CIKTI))


def komut_rapor(a):
    b = vt.baglan()
    satirlar = vt.son_denetimler(b, a.sehir, a.sektor)
    tahminler, demolar = {}, {}
    for r in satirlar:
        t = vt.son_tahmin(b, r["id"])
        if t: tahminler[r["id"]] = json.loads(t["detay"])
        d = b.execute("SELECT dosya FROM demolar WHERE aday_id=? ORDER BY id DESC LIMIT 1", (r["id"],)).fetchone()
        if d: demolar[r["id"]] = d["dosya"]
    c, x = rapor_mod.uret(satirlar, tahminler)
    p = rapor_mod.pano(satirlar, tahminler, demolar)
    print("→ CSV : %s" % c)
    if x: print("→ XLSX: %s" % x)
    print("→ Pano: %s" % p)


def komut_liste(a):
    b = vt.baglan()
    satirlar = vt.son_denetimler(b, a.sehir, a.sektor, limit=a.adet)
    print("%-4s %-34s %-16s %5s %6s  %s" % ("#","İşletme","Sektör","Skor","Eksik","Durum"))
    for r in satirlar:
        eks = json.loads(r["eksikler"])
        print("%-4d %-34s %-16s %5d %6d  %s" % (
            r["id"], r["ad"][:34], (r["sektor"] or "")[:16], r["skor"], len(eks),
            "SICAK ADAY" if sicak_mi(r["skor"]) else ""))


def komut_tumu(a):
    komut_tara(a); komut_denetle(a); komut_zenginlestir(a); komut_hesapla(a)
    komut_demo(a); komut_rapor(a)


def komut_ekle(a):
    """Taramada çıkmayan firmayı site/harita bağlantısıyla ekle ve tam analizden geçir."""
    from . import ekle as EK
    r = EK.firma_ekle(site=a.site, ad=a.ad, sehir=a.sehir, sektor=a.sektor, harita=a.harita, telefon=a.telefon, analiz=not a.analizsiz)
    print("→ aday #%d hazır%s" % (r["id"], (" · skor %d" % r["skor"]) if "skor" in r else ""))


def komut_gundem_gunluk(a):
    """Günlük otomatik gündem: tara → en iyi 3–6 → siteye yayınla (SEO kapısı dahil).

    launchd / cron ile her sabah çalıştırılır. Olgu cümlesi olarak haberin
    RSS özetini kullanır; açı gundem.ACILAR kalıbından gelir. Yayın kapıdan
    geçmezse dosya yazılır ama rapor "kapı: geçmedi" der — sen bakarsın."""
    from . import gundem as GU, gundem_yayin as GY, sorgu as SG
    from .ayarlar import ILLER
    liste = GU.tara(ILLER, asgari_puan=a.asgari, konu_basi=12)
    sec = GY.sec(liste, en_az=3, en_cok=a.adet)
    if len(sec) < 3:
        print("Yeterli haber yok (%d) — bugün gündem sayısı çıkmadı, zorlamıyoruz. TrendSaphiens yine de yenileniyor." % len(sec))
        topla_gunluk()
        try:
            from . import trend as TR
            from .x_paylas import X
            print("TrendSaphiens:", TR.yayinla(paylas=bool(X.get("otomatik", True))))
        except Exception as ex:
            print("TrendSaphiens yayınlanamadı:", ex)
        return
    # kaynaklı özet: Google Haberler bağlantısı → yayıncı sayfası → kısa alıntı (uydurma yok)
    try:
        from . import kaynak_ozet as KO
        for h in sec:
            KO.zenginlestir(h)
        print("Kaynak özeti:", sum(1 for h in sec if KO.yeterli({"olgu": h.get("ozet", ""), "baslik": h["baslik"]})), "/", len(sec), "madde")
    except Exception as ex:
        print("Kaynak özeti alınamadı:", ex)
    maddeler = [GY.taramadan_madde(h) for h in sec]
    # yazar: anahtar varsa kaynak olgularından intihalsiz haber-analiz yazısı (yoksa alıntı + okuma biçimi)
    try:
        from . import yazar as YZ
        if YZ.anahtar():
            print("Yazar:", YZ.yaz_hepsi(maddeler), "/", len(maddeler), "yazı")
        else:
            print("Yazar: anahtar yok — Panel → Ayarlar → Yazar")
    except Exception as ex:
        print("Yazar çalışmadı:", ex)
    try:
        aranan = [x["sorgu"] for x in (SG.oku() or {}).get("sorgular", [])[:10]]
    except Exception:
        aranan = None
    r = GY.yayinla(maddeler, aranan=aranan, kapi=True)
    print("Günün sayısı:", r["sayfa"], "| madde:", r["madde"], "| kapı:", r["kapi"])
    # gündem JSON'u da yaz (TrendSaphiens ve yeniden yazım bundan beslenir)
    try:
        import json, os, datetime
        from .ayarlar import KOK_DIZIN
        d = os.path.join(KOK_DIZIN, "veri", "gundem"); os.makedirs(d, exist_ok=True)
        t = datetime.date.today().isoformat()
        json.dump(maddeler, open(os.path.join(d, t + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    except Exception as ex:
        print("gündem json yazılamadı:", ex)
    # TrendSaphiens günlük veri: Türkiye'de en çok arananlar + geniş bölümler + TCMB/altın (kaynaklı)
    topla_gunluk()
    # TrendSaphiens: akış + kategori + haber sayfaları; X'e otomatik paylaşım (ayarlar.json → x.otomatik)
    try:
        from . import trend as TR
        from .x_paylas import X
        rt = TR.yayinla(paylas=bool(X.get("otomatik", True)))
        print("TrendSaphiens:", rt)
    except Exception as ex:
        print("TrendSaphiens yayınlanamadı:", ex)


def topla_gunluk():
    """trend_izle + piyasa_gunluk: internet ister; kaynak cevap vermezse satır boş kalır, uydurulmaz."""
    try:
        from . import trend_izle as TI
        print("Trend:", TI.gunluk_uret())
    except Exception as ex:
        print("Trend toplanamadı:", ex)
    try:
        from . import piyasa_gunluk as PG
        print("Piyasa:", PG.gunluk_uret())
    except Exception as ex:
        print("Piyasa toplanamadı:", ex)


def komut_trend(a):
    """TrendSaphiens'i yeniden bas (düzen değişince ya da elle). --topla: önce günün verisini çek."""
    from . import trend as TR
    if a.topla:
        topla_gunluk()
    print(TR.yayinla(paylas=a.paylas))


def main(argv=None):
    p = argparse.ArgumentParser(prog="pusula", description="Luna Pusula — yerel müşteri avcısı")
    alt = p.add_subparsers(dest="komut", required=True)
    def ortak(sp, sektor_gerekli=False):
        sp.add_argument("--sehir", required=True)
        sp.add_argument("--sektor", required=sektor_gerekli, choices=list(SEKTORLER))
        sp.add_argument("--adet", type=int, default=0)
        return sp
    ortak(alt.add_parser("tara", help="işletmeleri bul")).set_defaults(fn=komut_tara)
    se = alt.add_parser("ekle", help="firmayı site/harita bağlantısıyla ekle + analiz")
    se.add_argument("--site"); se.add_argument("--ad"); se.add_argument("--sehir"); se.add_argument("--sektor", choices=list(SEKTORLER))
    se.add_argument("--harita"); se.add_argument("--telefon"); se.add_argument("--analizsiz", action="store_true"); se.set_defaults(fn=komut_ekle)
    st = alt.add_parser("trend", help="TrendSaphiens'i yeniden bas"); st.add_argument("--paylas", action="store_true"); st.add_argument("--topla", action="store_true"); st.set_defaults(fn=komut_trend)
    s = ortak(alt.add_parser("denetle", help="eksikleri tespit et")); s.add_argument("--hizli", action="store_true")
    s.set_defaults(fn=komut_denetle)
    s = ortak(alt.add_parser("zenginlestir", help="iletişim ve yetkili bilgisi topla"))
    s.add_argument("--sadece-yeni", action="store_true", dest="sadece_yeni")
    s.set_defaults(fn=komut_zenginlestir)
    s = ortak(alt.add_parser("hesapla", help="eksikler kapanırsa ne olur")); s.add_argument("--ortalama-is", type=int, default=None, dest="ortalama_is")
    s.set_defaults(fn=komut_hesapla)
    s = ortak(alt.add_parser("demo", help="otomatik demo üret")); s.add_argument("--sadece-sicak", action="store_true", dest="sadece_sicak")
    s.set_defaults(fn=komut_demo)
    ortak(alt.add_parser("rapor", help="Excel/CSV + pano")).set_defaults(fn=komut_rapor)
    ortak(alt.add_parser("liste", help="ekrana liste")).set_defaults(fn=komut_liste)
    s = ortak(alt.add_parser("tumu", help="tara→denetle→hesapla→demo→rapor"), sektor_gerekli=False)
    s.add_argument("--hizli", action="store_true"); s.add_argument("--sadece-sicak", action="store_true", dest="sadece_sicak")
    s.add_argument("--ortalama-is", type=int, default=None, dest="ortalama_is")
    s.set_defaults(fn=komut_tumu)
    s = alt.add_parser("gundem-gunluk", help="günün sektör gündemini siteye yayınla")
    s.add_argument("--asgari", type=int, default=45); s.add_argument("--adet", type=int, default=5)
    s.set_defaults(fn=komut_gundem_gunluk)

    a = p.parse_args(argv)
    for alan, vars_ in (("hizli", False), ("sadece_sicak", False), ("ortalama_is", None),
                        ("adet", 0), ("sadece_yeni", False)):
        if not hasattr(a, alan): setattr(a, alan, vars_)
    if not a.adet and a.komut != "gundem-gunluk": a.adet = 0
    a.fn(a)

if __name__ == "__main__":
    main()
