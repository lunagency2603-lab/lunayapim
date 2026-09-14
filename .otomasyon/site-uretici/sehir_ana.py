# -*- coding: utf-8 -*-
"""Genel il sayfası üreticisi (henüz sayfası olmayan iller için)."""
import os, sys
from sehirler import SEHIRLER, SEHIR_INDEKS
from kabuk import head, FOOTER
from uretici import (HEDEF, KOK, e, j, ilce_metni, ekip_cumlesi, video_bolumu,
                     sss_blok, cta, SUREC, liste)
import json

def yerel_blok(c, e, ad, ek):
    """İl için gerçekten elimizde olan yerel bilgiden bölüm kurar.

    Veri yoksa o başlık HİÇ basılmaz — boş paragraf ya da uydurma cümle yok.
    Elimizde mekân/kültür notu olmayan iller için, sahip olduğumuz alanlardan
    (coğrafya, sektörler, komşu iller, hangi ekip gidiyor) doğru olan bir
    planlama bölümü kuruluyor."""
    p = []
    mekan = (c.get("mekan") or "").strip()
    kultur = (c.get("kultur") or "").strip()
    isletme = (c.get("isletme_notu") or "").strip()
    dugun = (c.get("dugun_notu") or "").strip()
    cog = (c.get("cografya") or "").strip()

    if mekan or cog:
        p.append("<h2>%s%s çekim mekânları</h2>" % (e(ad), ek))
        if mekan:
            p.append("<p>%s</p>" % e(mekan))
        if cog:
            p.append("<p><strong>Havadan:</strong> %s</p>" % e(cog))

    alt = []
    if kultur:
        alt.append("<p><strong>Klip ve sahne:</strong> %s</p>" % e(kultur))
    if isletme:
        alt.append("<p><strong>İşletme içeriği:</strong> %s</p>" % e(isletme))
    if dugun:
        alt.append("<p><strong>Düğün ve etkinlik:</strong> %s</p>" % e(dugun))

    if not alt:
        # Yerel not yazılmamış iller: elimizdeki doğrulanabilir alanlardan kur.
        sek = [x for x in (c.get("sektorler") or [])][:3]
        komsu = [SEHIR_INDEKS[k]["ad"] for k in (c.get("komsu") or [])
                 if k in SEHIR_INDEKS][:3]
        if sek:
            alt.append("<p><strong>Talebi ne belirliyor:</strong> %s%s en çok iş "
                       "%s alanlarından geliyor; çekim planını da bu sektörlerin "
                       "kendi takvimi belirliyor.</p>"
                       % (e(ad), ek, e(", ".join(sek).lower())))
        if komsu:
            alt.append("<p><strong>Aynı güne iki iş:</strong> %s ile birlikte %s "
                       "yönünde de çalışıyoruz. İki iş aynı güne denk gelirse "
                       "ulaşım gideri bölünüyor, ikisi de ucuzluyor.</p>"
                       % (e(ad), e(", ".join(komsu[:-1]) + " ve " + komsu[-1]
                                     if len(komsu) > 1 else komsu[0])))
        if (c.get("ekip") or "") == "ortak":
            alt.append("<p><strong>Kim geliyor:</strong> Modelleme ve animasyon "
                       "tarafı uzaktan yürüyor. Kamera veya drone gereken işlerde "
                       "%s%s çözüm ortağımızla çalışıyoruz; yönetmenlik, kurgu ve "
                       "renk yine bizde kalıyor.</p>" % (e(ad), ek))
        else:
            alt.append("<p><strong>Kim geliyor:</strong> %s%s kendi ekibimizle "
                       "sahaya çıkıyoruz — çeken de, kurgulayan da aynı kişi.</p>"
                       % (e(ad), ek))

    if alt:
        p.append("<h2>%s%s çekim planı nasıl kuruluyor</h2>" % (e(ad), ek))
        p.extend(alt)
    return "\n    ".join(p)


def hizmet_baglari(c, e):
    """Yalnızca gerçekten üretilmiş il-hizmet sayfalarına bağlanır.

    Kademe 2 ve 3 illerinde her hizmetin ayrı sayfası yok; olmayan sayfaya
    bağlanmak kırık bağlantı demek. Var olanı il sayfasına, olmayanı genel
    hizmet sayfasına yönlendiriyoruz."""
    slug = c["slug"]
    kalemler = [
        ("insaat-3d-modelleme", "İnşaat 3D Modelleme", "../hizmetler/insaat-3d-modelleme"),
        ("emlak-video",         "Emlak Video Çekimi",  "../hizmetler/emlak-kurumsal"),
        ("urun-animasyon",      "3D Ürün Animasyonu",  "../hizmetler/urun-animasyon"),
        ("klip-cekimi",         "Klip Çekimi",         "../hizmetler/klip-cekimi"),
        ("drone-cekimi",        "Drone & FPV Çekim",   "../hizmetler/drone-fpv"),
        ("isletme-tanitim",     "İşletme Tanıtım",     "../hizmetler/isletme-tanitim"),
    ]
    ci = []
    for ek_, ad_, yedek in kalemler:
        yol = os.path.join(HEDEF, "%s-%s.html" % (slug, ek_))
        hedef = "%s-%s" % (slug, ek_) if os.path.exists(yol) else yedek
        ci.append('<a href="%s"><b>%s</b></a>' % (hedef, e(ad_)))
    return "".join(ci)


def sayfa_sehir(c):
    ad, ek = c["ad"], c["ek"]
    slug = c["slug"]
    url = "%s/sehir/%s.html" % (KOK, slug)
    baslik_seo = "%s Tanıtım Filmi, Drone Çekimi ve 3D Modelleme — Luna Yapım" % ad
    if len(baslik_seo) > 70:      # uzun il adları (Afyonkarahisar, Kahramanmaraş) sığsın
        baslik_seo = "%s Tanıtım Filmi, Drone ve 3D Modelleme — Luna Yapım" % ad
    # Google arama sonucunda 165 karakterden sonrası kesiliyor — sığdır.
    aciklama = ("%s%s kurumsal tanıtım filmi, drone çekimi, inşaat 3D modelleme, "
                "emlak videosu ve ürün animasyonu. Tüm ilçeler. Luna Yapım." % (ad, ek))
    if len(aciklama) > 165:
        aciklama = ("%s%s video çekimi, drone, 3D modelleme ve emlak tanıtım "
                    "videosu. Luna Yapım." % (ad, ek))
    anahtar = ("%s video çekimi, %s drone çekimi, %s tanıtım filmi, %s inşaat 3d modelleme, %s emlak video, "
        "%s ürün animasyonu, %s klip çekimi, %s prodüksiyon" % tuple([ad.lower()]*8))

    sss = [
     ("%s%s hangi hizmetleri veriyorsunuz?" % (ad, ek),
      "İnşaat 3D modelleme ve mimari görselleştirme, emlak ve kurumsal tanıtım videosu, 3D ürün animasyonu, klip çekimi, drone ve FPV çekim ile işletme tanıtım videosu."),
     ("%s%s kendi ekibinizle mi geliyorsunuz?" % (ad, ek), ekip_cumlesi(c)),
     ("Modelleme ve animasyon için %s%s bulunmanız gerekiyor mu?" % (ad, ek),
      "Hayır. 3D modelleme, mimari görselleştirme ve ürün animasyonu tamamen uzaktan yürüyor. Sadece gerçek kamera ve drone çekimi gerektiren işlerde sahaya çıkıyoruz."),
    ]
    semalar = "\n".join('<script type="application/ld+json">\n%s\n</script>' % j(x) for x in (
      {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Ana Sayfa","item":KOK+"/"},
        {"@type":"ListItem","position":2,"name":"İller","item":KOK+"/sehir/"},
        {"@type":"ListItem","position":3,"name":ad,"item":url}]},
      {"@context":"https://schema.org","@type":"LocalBusiness","name":"Luna Yapım",
       "description":aciklama,"url":url,"image":KOK+"/assets/og-image.png","telephone":"+905411602603",
       "priceRange":"$$",
       "address":{"@type":"PostalAddress","addressLocality":"Bursa","addressRegion":"Bursa","addressCountry":"TR"},
       "areaServed":{"@type":"City","name":ad,"containedInPlace":{"@type":"Country","name":"Türkiye"}}},
      {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in sss]}))

    g = head(e(baslik_seo), e(aciklama), e(anahtar), url, semalar)
    g += """<div class="page-hero">
  <img class="karga-buyuk" src="../assets/karga.png" alt="">
  <div class="wrap">
    <div class="crumbs"><a href="../">Ana Sayfa</a> · <a href="./">İller</a> · {ad}</div>
    <h1>{ad}{ek} tanıtım filmi, drone ve <i>3D modelleme</i></h1>
    <p class="lede">İnşaat 3D modelleme, emlak tanıtım videosu, ürün animasyonu, klip çekimi ve drone prodüksiyonu — {ad}{ek} tek ekipten.</p>
    <div class="btnlar">
      <a class="btn btn-dolu" href="https://wa.me/905411602603">{ad} için teklif al</a>
      <a class="btn btn-cizgi" href="#hizmetler">Hizmetler</a>
    </div>
  </div>
</div>

<section>
  <div class="wrap prose">
    <p class="ilk-not">{ekip}</p>

    {yerel}
    <h2>{ad} pazarında ne oluyor</h2>
    <p><strong>İnşaat:</strong> {insaat}</p>
    <p><strong>Gayrimenkul:</strong> {emlak}</p>
    <p><strong>Sanayi:</strong> {sanayi}</p>

    <h2>{ad}{ek} hangi ilçelerde</h2>
    <p>{ilceler} dahil ilin tamamında çalışıyoruz.</p>

    <h2>{ad}{ek} öne çıkan sektörler</h2>
    <ul>{sektorler}</ul>

    <h2 id="hizmetler">{ad}{ek} hizmetlerimiz</h2>
    <div class="ilgili ilgili-sik">{hizmet_baglari}</div>
  </div>
</section>

""".format(ad=e(ad), ek=ek, slug=slug, ekip=e(ekip_cumlesi(c)), insaat=e(c["insaat"]),
           emlak=e(c["emlak"]), sanayi=e(c["sanayi"]), cografya=e(c["cografya"]),
           ilceler=e(ilce_metni(c)), sektorler=liste(c["sektorler"]),
           yerel=yerel_blok(c, e, ad, ek), hizmet_baglari=hizmet_baglari(c, e))

    g += video_bolumu("isler", "İşlerimizden")
    komsu = [k for k in c["komsu"] if k in SEHIR_INDEKS][:4]
    kb = "".join('<a href="%s">%s</a>' % (k, e(SEHIR_INDEKS[k]["ad"])) for k in komsu)
    g += """<section>
  <div class="wrap prose">
    <h2>{ad} — sık sorulan sorular</h2>
    {sss}

    <h2>Yakın iller</h2>
  </div>
  <div class="wrap"><div class="iller">{komsu}<a href="./" style="border-color:var(--kirmizi);color:var(--kirmizi)">Tüm iller →</a></div></div>
</section>

""".format(ad=e(ad), sss=sss_blok(sss), komsu=kb)
    g += cta(c, "{ad}{ek} işe <i>hazırız</i>.".format(ad=e(ad), ek=ek),
                "Projeni anlat, {ad} için sana özel teklif çıkaralım.".format(ad=e(ad)))
    g += FOOTER
    return slug + ".html", g

if __name__ == "__main__":
    n = 0
    for c in SEHIRLER:
        yol = os.path.join(HEDEF, c["slug"] + ".html")
        if os.path.exists(yol):
            continue
        adi, icerik = sayfa_sehir(c)
        open(os.path.join(HEDEF, adi), "w", encoding="utf-8").write(icerik)
        print("yeni:", adi); n += 1
    print("%d yeni il sayfası" % n)
