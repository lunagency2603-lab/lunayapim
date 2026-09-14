# -*- coding: utf-8 -*-
"""
Luna Yapım — şehir × hizmet SEO sayfası üreticisi.
Kullanım:  python3 uretici.py            (hepsini üretir)
           python3 uretici.py bursa      (tek il)
Çıktı:     ~/Documents/GitHub/lunayapim/sehir/{il}-{hizmet}.html
"""
import os, sys, re, json, html
import yerel_analiz as YA
from sehirler import SEHIRLER, SEHIR_INDEKS, KADEME1, KADEME2, KADEME3
from kabuk import head, FOOTER
from cesit import cesitlendir, yerel_blok, varyant
from sektor_anlatim import sektor_bloku, uc_ihtiyac

HEDEF = os.path.expanduser("~/Documents/GitHub/lunayapim/sehir")
if not os.path.isdir(HEDEF):
    HEDEF = os.path.expanduser("~/mnt/Documents/GitHub/lunayapim/sehir")
KOK = "https://lunayapim.com"
TEL = "+905411602603"

def e(x): return html.escape(x, quote=True)
def j(x): return json.dumps(x, ensure_ascii=False)

def kisa_baslik(x, azami=68):
    """Google başlıkta ~65 karakter gösteriyor; taşan başlığı kırpar."""
    x = re.sub(r"\s+", " ", x).strip()
    return x if len(x) <= azami else x[:azami - 1].rstrip(" ,·—|") + "…"


def meta_desc(temel, ek=""):
    """160 karakteri aşmayan meta açıklama. Ek cümle ancak sığarsa eklenir."""
    t = re.sub(r"\s+", " ", temel).strip()
    ek = re.sub(r"\s+", " ", ek).strip()
    if ek and len(t) + 1 + len(ek) <= 160:
        t = t + " " + ek
    if len(t) > 160:
        t = t[:157].rsplit(" ", 1)[0].rstrip(" ,.;:") + "..."
    return t


def ilk_ilceler(c, n=3):
    i = c["ilceler"][:n]
    return ", ".join(i[:-1]) + " ve " + i[-1] if len(i) > 1 else i[0]


def liste(xs):
    return "".join("<li>%s</li>" % x for x in xs)

def ilce_metni(c):
    i = c["ilceler"]
    if len(i) > 2:
        return ", ".join(i[:-1]) + " ve " + i[-1]
    return " ve ".join(i)

def ekip_cumlesi(c):
    if c["ekip"] == "kendi":
        return ("%s%s kendi ekibimizle çalışıyoruz; çekim ve keşif için aynı gün yola çıkabiliyoruz."
                % (c["ad"], c["ek"]))
    return ("%s%s modelleme ve animasyon işini tamamen uzaktan yürütüyoruz; yerinde çekim gerektiğinde "
            "Bursa'daki ekibimiz veya bölgedeki çözüm ortağımızla programa alıyoruz." % (c["ad"], c["ek"]))

def sema_bloklari(c, hizmet, baslik, aciklama, url, sss):
    b = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Ana Sayfa","item":KOK+"/"},
        {"@type":"ListItem","position":2,"name":"İller","item":KOK+"/sehir/"},
        {"@type":"ListItem","position":3,"name":c["ad"],"item":KOK+"/sehir/%s.html"%c["slug"]},
        {"@type":"ListItem","position":4,"name":baslik,"item":url}]}
    s = {"@context":"https://schema.org","@type":"Service",
        "serviceType":hizmet["sema_tur"],"name":baslik,"description":aciklama,"url":url,
        "category":hizmet["kategori"],
        "provider":{"@type":"LocalBusiness","name":"Luna Yapım",
            "image":KOK+"/assets/og-image.png","telephone":TEL,"priceRange":"$$",
            "address":{"@type":"PostalAddress","addressLocality":"Bursa","addressRegion":"Bursa","addressCountry":"TR"},
            "url":KOK},
        "areaServed":{"@type":"City","name":c["ad"],"containedInPlace":{"@type":"Country","name":"Türkiye"}},
        "audience":{"@type":"BusinessAudience","audienceType":hizmet["kitle"]}}
    f = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in sss]}
    return "\n".join('<script type="application/ld+json">\n%s\n</script>' % j(x) for x in (b,s,f))

HIZMET_ADLARI = [
 ("insaat-3d-modelleme", "%s İnşaat 3D Modelleme", "Mimari render, proje animasyonu, sanal tur", 1),
 ("emlak-video",         "%s Emlak Video Çekimi",  "İlan, portföy ve proje videosu", 1),
 ("urun-animasyon",      "%s Ürün Animasyonu",     "Makine, üretim hattı ve hizmet anlatımı", 1),
 ("klip-cekimi",         "%s Klip Çekimi",         "Müzik klibi ve marka klibi", 2),
 ("drone-cekimi",        "%s Drone Çekimi",        "Havadan 4K ve FPV planlar", 2),
 ("dugun-cekimi",        "%s Düğün Çekimi",        "Sinematik düğün ve etkinlik filmi", 2),
 ("isletme-tanitim",     "%s İşletme Tanıtım",     "Sosyal medya için düzenli içerik", 2),
]

def sayfa_var(c, anahtar):
    """Bu il için o hizmetin ayrı sayfası üretiliyor mu?"""
    if c["kademe"] == 1: return True
    if c["kademe"] == 2: return anahtar in ("insaat-3d-modelleme","emlak-video","urun-animasyon")
    return False

def ilgili_blok(c, aktif):
    ic = []
    for anahtar, kalip, aciklama, _ in HIZMET_ADLARI:
        if anahtar == aktif: continue
        if sayfa_var(c, anahtar):
            ic.append('<a href="%s-%s"><b>%s</b><span>%s</span></a>'
                      % (c["slug"], anahtar, e(kalip % c["ad"]), aciklama))
    ic.append('<a href="%s"><b>%s — tüm hizmetler</b><span>Şehir sayfasına dön</span></a>'
              % (c["slug"], e(c["ad"])))
    komsular = [k for k in c["komsu"] if k in SEHIR_INDEKS and sayfa_var(SEHIR_INDEKS[k], aktif)][:3]
    for k in komsular:
        ko = SEHIR_INDEKS[k]
        ic.append('<a href="%s-%s"><b>%s</b><span>Komşu ilde aynı hizmet</span></a>' % (k, aktif, e(ko["ad"])))
    if len(ic) < 4:
        for k in c["komsu"][:2]:
            if k in SEHIR_INDEKS:
                ic.append('<a href="%s"><b>%s</b><span>Komşu il sayfası</span></a>' % (k, e(SEHIR_INDEKS[k]["ad"])))
    return '<div class="ilgili">\n      ' + "\n      ".join(ic) + '\n    </div>'

def yerel_plan(c, hizmet_adi="çekim"):
    """Her il-hizmet sayfasına, o İLE ÖZGÜ planlama bölümü.

    Üç bilgi de sehirler.py'de o il için yazılı: hangi ekip gidiyor, hangi
    komşu illerle aynı güne iş konuyor, hangi ilçeler kapsamda.
    Uydurma yok; veri yoksa o satır basılmıyor.

    Neden gerekli: aynı hizmetin 46 il sayfası birbirinin kopyasıysa Google
    hepsini tek sayfanın varyantı sayıp eliyor. Bu blok her ilde farklı."""
    ad, ek = c["ad"], c["ek"]
    p = []
    komsu = [SEHIR_INDEKS[k]["ad"] for k in (c.get("komsu") or [])
             if k in SEHIR_INDEKS][:3]
    ilce = (c.get("ilceler") or [])[:4]
    sek = (c.get("sektorler") or [])[:3]

    if ilce:
        p.append("<p><strong>Kapsam:</strong> %s%s %s dahil ilin tamamında %s "
                 "yapıyoruz; ilçeye gitmek için ek ücret çıkarmıyoruz.</p>"
                 % (e(ad), ek, e(", ".join(ilce)), e(hizmet_adi)))
    if sek:
        p.append("<p><strong>Talep nereden geliyor:</strong> %s%s işin büyük kısmı "
                 "%s tarafından geliyor; planı da bu sektörlerin kendi takvimi "
                 "belirliyor.</p>" % (e(ad), ek, e(", ".join(sek).lower())))
    if komsu:
        kb = ", ".join(komsu[:-1]) + " ve " + komsu[-1] if len(komsu) > 1 else komsu[0]
        p.append("<p><strong>Aynı güne iki iş:</strong> %s yönünde de çalışıyoruz. "
                 "İki iş aynı güne denk gelirse ulaşım gideri bölünüyor — ikisi de "
                 "ucuza geliyor.</p>" % e(kb))
    if (c.get("ekip") or "") == "ortak":
        p.append("<p><strong>Kim geliyor:</strong> Kurgu, renk ve yönetmenlik bizde; "
                 "kamera gereken günlerde %s%s çözüm ortağımızla çalışıyoruz.</p>"
                 % (e(ad), ek))
    else:
        p.append("<p><strong>Kim geliyor:</strong> %s%s kendi ekibimizle çıkıyoruz — "
                 "çeken de kurgulayan da aynı kişi.</p>" % (e(ad), ek))
    if not p:
        return ""
    return ("<h2>%s%s nasıl çalışıyoruz</h2>\n    " % (e(ad), ek)) + "\n    ".join(p)


SUREC = """<div class="surec">
      <div class="adim"><span class="n">01</span><h3>%s</h3><p>%s</p></div>
      <div class="adim"><span class="n">02</span><h3>%s</h3><p>%s</p></div>
      <div class="adim"><span class="n">03</span><h3>%s</h3><p>%s</p></div>
      <div class="adim"><span class="n">04</span><h3>%s</h3><p>%s</p></div>
    </div>"""

def cta(c, baslik, alt):
    return """<section class="cta">
  <img class="karga-buyuk" src="../assets/karga.png" alt="">
  <div class="wrap">
    <p class="etk">İletişim</p>
    <h2>%s</h2>
    <p>%s</p>
    <div class="btnlar">
      <a href="https://wa.me/905411602603" class="btn btn-koyu">WhatsApp'tan Yaz</a>
      <a href="tel:+905411602603" class="btn btn-cizgi" style="border-color:rgba(255,255,255,.5);color:#fff">Ara · 0541 160 26 03</a>
    </div>
  </div>
</section>

""" % (baslik, alt)

def video_bolumu(etiket, baslik):
    return """<section class="acik" data-video-bolum>
  <div class="wrap">
    <div class="bas"><span class="no">▶</span><div><h2>%s</h2>
      <p class="aciklama">Oynatmak için bir işin üzerine dokun.</p></div></div>
    <div class="isler" data-video="%s"></div>
  </div>
</section>

""" % (baslik, etiket)

def sonlandir(govde, c, odak):
    """Her sayfaya ile özgü 'yerel unsurlar' bölümünü ekler ve metni çeşitlendirir."""
    blok = ('<section class="acik">\n  <div class="wrap prose">\n    %s\n  </div>\n</section>\n\n'
            % yerel_blok(c, odak))
    isaret = '<section class="acik" data-video-bolum>'
    if isaret in govde:
        govde = govde.replace(isaret, blok + isaret, 1)
    else:
        govde = govde.replace('<section class="cta">', blok + '<section class="cta">', 1)
    return cesitlendir(govde, c)


def sss_blok(sss):
    p = ['<div class="sss">']
    for i,(q,a) in enumerate(sss):
        acik = " open" if i == 0 else ""
        p.append('      <details%s><summary>%s</summary>\n        <div class="cvp"><p>%s</p></div></details>' % (acik, e(q), e(a)))
    p.append('    </div>')
    return "\n".join(p)

# ============================================================
#  1) İNŞAAT 3D MODELLEME
# ============================================================
def sayfa_insaat3d(c):
    ad, ek, icin = c["ad"], c["ek"], c["icin"]
    slug = "%s-insaat-3d-modelleme" % c["slug"]
    url = "%s/sehir/%s.html" % (KOK, slug)
    baslik_seo = kisa_baslik("%s İnşaat 3D Modelleme ve Mimari Render | Luna Yapım" % ad)
    aciklama = meta_desc(
        "%s%s inşaat 3D modelleme: mimari render, proje tanıtım animasyonu, iç mekân görselleştirme ve 360° sanal tur." % (ad, ek),
        "%s ve tüm ilçeler." % ilk_ilceler(c))
    anahtar = ("%s inşaat 3d modelleme, %s mimari görselleştirme, %s 3d render, %s proje tanıtım animasyonu, "
        "%s konut projesi 3d, %s villa render, %s mimari animasyon, %s 3d maket" %
        (ad.lower(), ad.lower(), ad.lower(), ad.lower(), ad.lower(), ad.lower(), ad.lower(), ad.lower()))

    sss = [
     ("%s%s hangi projelerde 3D modelleme yapıyorsunuz?" % (ad, ek),
      "Konut projesi, villa, site yerleşimi, ticari yapı, fabrika ve kentsel dönüşüm projelerinde çalışıyoruz. %s başta olmak üzere ilin tüm ilçelerindeki projeler için modelleme yapıyoruz." % ilce_metni(c)),
     ("%s%s yerinde gelmeniz gerekiyor mu?" % (ad, ek),
      ekip_cumlesi(c) + " 3D modelleme tarafı için yerinde bulunmamız şart değil; mimari proje ve arsa bilgisi yeterli."),
     ("Mimari projemiz DWG değil, PDF. Sorun olur mu?",
      "Olmaz. PDF proje, kat planı ve cephe görselleriyle de model kurabiliyoruz. DWG veya 3D dosya verdiğinizde süreç kısalıyor ve maliyet düşüyor."),
     ("Teslim süresi ne kadar?",
      "Tek blok bir projede modelleme ve render 10–15 iş günü, çok bloklu site yerleşimlerinde 3–5 hafta. Lansman tarihi sabitse önce render görsellerini teslim edip animasyonu arkadan yetiştiriyoruz."),
     ("Şantiyenin havadan görüntüsüyle 3D modeli birleştirebilir misiniz?",
      "Evet. %s Arsanın veya devam eden şantiyenin drone çekimini yapıp 3D modeli gerçek çevreye yerleştiriyoruz." % c["cografya"]),
    ]
    hizmet = {"sema_tur":"İnşaat 3D Modelleme ve Mimari Görselleştirme",
              "kategori":["İnşaat","Gayrimenkul","Mimarlık"],
              "kitle":"%s'daki inşaat firmaları, müteahhitler, mimarlık ofisleri ve gayrimenkul geliştiriciler" % ad}

    g = head(e(baslik_seo), e(aciklama), e(anahtar), url,
             sema_bloklari(c, hizmet, "%s İnşaat 3D Modelleme" % ad, aciklama, url, sss))

    g += """<div class="page-hero">
  <img class="karga-buyuk" src="../assets/karga.png" alt="">
  <div class="wrap">
    <div class="crumbs"><a href="../">Ana Sayfa</a> · <a href="./">İller</a> · <a href="{slug0}">{ad}</a> · İnşaat 3D Modelleme</div>
    <h1>{ad}{ek} inşaat <i>3D modelleme</i></h1>
    <p class="lede">{ad}{ek} konut projesi, villa, site ve ticari yapı için mimari render, proje tanıtım animasyonu, iç mekân görselleştirme ve 360° sanal tur.</p>
    <div class="btnlar">
      <a class="btn btn-dolu" href="https://wa.me/905411602603">{ad} için teklif al</a>
      <a class="btn btn-cizgi" href="#surec">Nasıl çalışıyor?</a>
    </div>
  </div>
</div>

<section>
  <div class="wrap prose">
    {yerel_analiz}

    <p>Luna Yapım olarak {ad}{ek} bu iki ihtiyacın ikisine de aynı araçla cevap veriyoruz: mimari projeyi alıp gerçek malzeme dokularıyla modelliyor, arsanın gerçek konumuna ve gerçek güneş açısına oturtuyor, sonra bunu satış ofisinde, ilan sitelerinde ve sosyal medyada kullanabileceğiniz video ve görsellere çeviriyoruz. {ekip}</p>

    <div class="rozetler">
      <span class="rozet">Mimari Render</span>
      <span class="rozet">Proje Animasyonu</span>
      <span class="rozet">İç Mekân 3D</span>
      <span class="rozet">Yerleşim Maketi</span>
      <span class="rozet">Sanal Tur</span>
      <span class="rozet">Şantiye Simülasyonu</span>
    </div>

    <h2>{ad}{ek} hangi ilçelerde çalışıyoruz</h2>
    <p>{ilceler} dahil ilin tamamında proje kabul ediyoruz. Modelleme tamamen uzaktan yürüdüğü için ilçe farkı süreyi değiştirmiyor; yalnızca drone ve gerçek çekim gerektiren işlerde keşif planlaması yapıyoruz.</p>


    <p>Ne teslim ettiğimizin tam listesi, teslim formatları ve örnek çalışma <a href="../hizmetler/insaat-3d-modelleme">inşaat 3D modelleme sayfasında</a>.</p>

    <h2 id="surec">{ad} projeniz nasıl ilerliyor</h2>
  </div>

  <div class="wrap">
    {surec}
  </div>

</section>

""".format(yerel_analiz=YA.blok(c, "insaat3d"), ad=e(ad), ek=ek, slug0=c["slug"], insaat=e(c["insaat"]), ekip=e(ekip_cumlesi(c)),
           ilceler=e(ilce_metni(c)), cografya=e(c["cografya"]),
           surec=SUREC % ("Proje ve hedef","Mimari proje, malzeme listesi ve satış hedefi alınıyor.",
                          "Modelleme","Yapı, arsa, çevre ve peyzaj ölçülü modelleniyor.",
                          "Ön izleme","Taslak render ve kamera hareketi onayınıza sunuluyor.",
                          "Teslim","Yüksek çözünürlüklü çıktı, çoklu format ve sanal tur."))

    g += video_bolumu("insaat-3d", "3D modelleme işlerimizden")
    g += """<section>
  <div class="wrap prose">
    <h2>{ad} — sık sorulan sorular</h2>
    {sss}

    <h2>{ad}{ek} diğer hizmetlerimiz</h2>
    {ilgili}

    <p style="margin-top:30px"><a href="../hizmetler/insaat-3d-modelleme" class="btn btn-cizgi">Hizmetin tüm detayları</a>
      <a href="https://wa.me/905411602603" class="btn btn-dolu">{ad} için teklif al</a></p>
  </div>
</section>

""".format(ad=e(ad), ek=ek, sss=sss_blok(sss), ilgili=ilgili_blok(c,"insaat-3d-modelleme"))
    g += cta(c, "%s%s projenizi <i>görünür</i> yapalım." % (e(ad), ek),
                "Mimari projeni gönder; kaç günde ve neye mal olacağını aynı gün söyleyelim.")
    g += FOOTER
    return slug + ".html", g

# ============================================================
#  2) EMLAK VİDEO ÇEKİMİ
# ============================================================
def sayfa_emlak(c):
    ad, ek = c["ad"], c["ek"]
    slug = "%s-emlak-video" % c["slug"]
    url = "%s/sehir/%s.html" % (KOK, slug)
    baslik_seo = kisa_baslik("%s Emlak Videosu ve Kurumsal Tanıtım Filmi | Luna Yapım" % ad)
    aciklama = meta_desc(
        "%s%s emlak video çekimi: villa, daire, konut projesi, arsa ve ticari mülk için drone destekli ilan videosu ve sanal tur." % (ad, ek),
        "%s ve tüm ilçeler." % ilk_ilceler(c))
    anahtar = ("%s emlak video çekimi, %s gayrimenkul video, %s villa tanıtım videosu, %s emlak drone çekimi, "
        "%s konut projesi tanıtım filmi, %s arsa çekimi, %s emlak fotoğraf, %s ilan videosu" %
        tuple([ad.lower()]*8))

    sss = [
     ("%s%s hangi mülkleri çekiyorsunuz?" % (ad, ek),
      "Villa, daire, rezidans, konut projesi, site, arsa, tarım arazisi, depo, dükkân ve fabrika binası. %s dahil ilin her ilçesinde çekim yapıyoruz." % ilce_metni(c)),
     ("%s%s çekim ne kadar sürüyor, ne zaman teslim ediliyor?" % (ad, ek),
      "Tek daire veya villa yarım gün, konut projesi ve site bir gün sürüyor. Kurgu ve renk düzenlemesiyle birlikte teslim genellikle çekimden 5–7 iş günü sonra."),
     ("Drone çekimi için izin gerekiyor mu?",
      "Yerleşim ve uçuş kısıtı olan bölgelerde gerekli izinleri biz takip ediyoruz. %s Uçuş planını keşif sırasında belirliyoruz." % c["cografya"]),
     ("Emlak ofisi olarak sürekli çalışabilir miyiz?",
      "Evet. Portföyünü düzenli çeken ofisler için aylık paket kuruyoruz: ay içinde belirli sayıda mülk çekimi, sabit fiyat ve öncelikli takvim."),
     ("Boş daireyi nasıl çekiyorsunuz?",
      "Geniş açı, doğru ışık saati ve akıcı kamera hareketiyle. İstenirse dijital mobilyalama uyguluyoruz: boş odaya 3D mobilya yerleştirip mekânın nasıl kullanılacağını gösteriyoruz."),
    ]
    hizmet = {"sema_tur":"Emlak Video Çekimi ve Gayrimenkul Tanıtım Filmi",
              "kategori":["Gayrimenkul","İnşaat","Pazarlama"],
              "kitle":"%s'daki emlak ofisleri, gayrimenkul danışmanları, müteahhitler ve site yönetimleri" % ad}

    g = head(e(baslik_seo), e(aciklama), e(anahtar), url,
             sema_bloklari(c, hizmet, "%s Emlak Video Çekimi" % ad, aciklama, url, sss))

    g += """<div class="page-hero">
  <img class="karga-buyuk" src="../assets/karga.png" alt="">
  <div class="wrap">
    <div class="crumbs"><a href="../">Ana Sayfa</a> · <a href="./">İller</a> · <a href="{slug0}">{ad}</a> · Emlak Video</div>
    <h1>{ad}{ek} <i>emlak video</i> çekimi</h1>
    <p class="lede">Villa, daire, konut projesi, arsa ve ticari mülk için drone destekli ilan videosu, sanal tur ve fotoğraf. İlanınız listede farklı bir yerde dursun.</p>
    <div class="btnlar">
      <a class="btn btn-dolu" href="https://wa.me/905411602603">{ad} için teklif al</a>
      <a class="btn btn-cizgi" href="#surec">Nasıl çalışıyor?</a>
    </div>
  </div>
</div>

<section>
  <div class="wrap prose">
    {yerel_analiz}

    <p>Bir ilanda on fotoğraf yerine bir dakikalık iyi bir video, alıcının kararını belirgin şekilde hızlandırır. Videonun asıl faydası ise ayak izini azaltmasıdır: alıcı gelmeden önce mülkü gezmiş olur, yerinde gezmeye gelen kişi daha nitelikli olur. {ekip}</p>

    <div class="rozetler">
      <span class="rozet">Villa &amp; Daire</span>
      <span class="rozet">Konut Projesi</span>
      <span class="rozet">Arsa &amp; Arazi</span>
      <span class="rozet">Ticari Mülk</span>
      <span class="rozet">Drone Destekli</span>
      <span class="rozet">Sanal Tur</span>
      <span class="rozet">İlan Fotoğrafı</span>
    </div>

    <h2>{ad}{ek} hangi ilçelerde çekim yapıyoruz</h2>
    <p>{ilceler} dahil ilin tamamında çekim yapıyoruz. Aynı gün içinde birden fazla mülk çekimi planladığınızda ulaşım maliyeti bölünüyor; bu yüzden portföyü toplu çekmek her zaman daha ekonomik.</p>


    <p>Teslim formatlarının tamamı (ilan sitesi, web, sosyal medya sürümleri) <a href="../hizmetler/emlak-kurumsal">emlak video sayfasında</a>.</p>

    <h2 id="surec">{ad}{ek} çekim nasıl ilerliyor</h2>
  </div>

  <div class="wrap">
    {surec}
  </div>

</section>

""".format(yerel_analiz=YA.blok(c, "emlak"), ad=e(ad), ek=ek, slug0=c["slug"], emlak=e(c["emlak"]), ekip=e(ekip_cumlesi(c)),
           ilceler=e(ilce_metni(c)), cografya=e(c["cografya"]),
           surec=SUREC % ("Keşif","Mülkü ve ışık saatini konuşuyoruz; yürüyüş rotasını belirliyoruz.",
                          "Çekim günü","İçeriden akıcı kamera, dışarıdan drone; fotoğraflar aynı gün.",
                          "Kurgu ve renk","Ritim kurgusu, renk düzenleme, altyazı ve müzik.",
                          "Çoklu format","İlan sitesi, web ve sosyal medya sürümleri birlikte teslim."))

    g += video_bolumu("emlak", "Emlak ve kurumsal işlerimizden")
    g += """<section>
  <div class="wrap prose">
    <h2>{ad} — sık sorulan sorular</h2>
    {sss}

    <h2>{ad}{ek} diğer hizmetlerimiz</h2>
    {ilgili}

    <p style="margin-top:30px"><a href="../hizmetler/emlak-kurumsal" class="btn btn-cizgi">Hizmetin tüm detayları</a>
      <a href="https://wa.me/905411602603" class="btn btn-dolu">{ad} için teklif al</a></p>
  </div>
</section>

""".format(ad=e(ad), ek=ek, sss=sss_blok(sss), ilgili=ilgili_blok(c,"emlak-video"))
    g += cta(c, "{ad}{ek} çekime <i>hazırız</i>.".format(ad=e(ad), ek=ek),
                "Mülkün adresini ve ne zaman çekilmesini istediğini yaz; takvimi aynı gün çıkaralım.")
    g += FOOTER
    return slug + ".html", g

# ============================================================
#  3) ÜRÜN & HİZMET ANİMASYONU
# ============================================================
def sayfa_urun(c):
    ad, ek = c["ad"], c["ek"]
    slug = "%s-urun-animasyon" % c["slug"]
    url = "%s/sehir/%s.html" % (KOK, slug)
    baslik_seo = kisa_baslik("%s 3D Ürün Animasyonu ve Tanıtım Videosu | Luna Yapım" % ad)
    aciklama = meta_desc(
        "%s%s 3D ürün animasyonu: makine çalışma prensibi, kesit anlatım, montaj ve üretim hattı videosu." % (ad, ek),
        "Fuar ve ihracat için çok dilli sürüm.")
    anahtar = ("%s 3d ürün animasyonu, %s ürün tanıtım videosu, %s makine animasyonu, %s fabrika tanıtım videosu, "
        "%s üretim hattı animasyonu, %s ürün render, %s fuar videosu, %s tanıtım filmi" % tuple([ad.lower()]*8))

    sektor_liste = liste(c["sektorler"])
    sss = [
     ("%s%s hangi sektörlerde çalışıyorsunuz?" % (ad, ek),
      "İlin üretim profiline uygun olarak %s başta olmak üzere üretim yapan her sektörle çalışıyoruz. Fiziksel ürünü olmayan hizmet şirketleri için de süreç animasyonu üretiyoruz." % ", ".join(c["sektorler"])),
     ("Fabrikamıza gelmeniz gerekiyor mu?",
      ekip_cumlesi(c) + " Animasyon tarafı tamamen uzaktan yürüyor; sadece gerçek üretim görüntüsüyle animasyonu birleştirmek isterseniz tesiste çekim planlıyoruz."),
     ("Ürünümüzün 3D dosyası yok, yine de yapılır mı?",
      "Yapılır. Teknik resim, ölçü listesi veya farklı açılardan net fotoğraflar yeterli. CAD veya STEP dosyası verirseniz süre ve maliyet belirgin şekilde düşüyor."),
     ("Fuar için yetiştirebilir misiniz?",
      "Fuar tarihi sabitse süreci ona göre kuruyoruz. Tek ürün vitrin animasyonu 7–10 iş günü, teknik anlatım animasyonu 2–3 hafta sürüyor. Fuar ekranı için sessiz döngü sürümünü ayrıca teslim ediyoruz."),
     ("İhracat için yabancı dilde sürüm veriyor musunuz?",
      "Evet. Animasyon bir kez üretiliyor, seslendirme ve altyazı istediğiniz kadar dilde ekleniyor. En sık istenenler İngilizce, Almanca, Arapça ve Rusça."),
    ]
    hizmet = {"sema_tur":"3D Ürün ve Hizmet Animasyonu",
              "kategori":["Sanayi","Üretim","Pazarlama"],
              "kitle":"%s'daki üretici firmalar, sanayi kuruluşları ve hizmet şirketleri" % ad}

    g = head(e(baslik_seo), e(aciklama), e(anahtar), url,
             sema_bloklari(c, hizmet, "%s 3D Ürün Animasyonu" % ad, aciklama, url, sss))

    g += """<div class="page-hero">
  <img class="karga-buyuk" src="../assets/karga.png" alt="">
  <div class="wrap">
    <div class="crumbs"><a href="../">Ana Sayfa</a> · <a href="./">İller</a> · <a href="{slug0}">{ad}</a> · Ürün Animasyonu</div>
    <h1>{ad}{ek} <i>3D ürün</i> animasyonu</h1>
    <p class="lede">Ürününüzü 3D modelleyip videoya çeviriyoruz: çalışma prensibi, kesit anlatım, montaj, üretim hattı ve hizmet süreci animasyonu. Fuarda ve ihracatta çalışan video.</p>
    <div class="btnlar">
      <a class="btn btn-dolu" href="https://wa.me/905411602603">{ad} için teklif al</a>
      <a class="btn btn-cizgi" href="#surec">Nasıl çalışıyor?</a>
    </div>
  </div>
</div>

<section>
  <div class="wrap prose">
    {yerel_analiz}

    <p>Her ürün kameraya gelmez. Kimi çok büyüktür, kimi çalışırken içi görünmez, kimi henüz üretilmemiştir, kimi de zaten fiziksel değildir. 3D modelleme ve animasyon tam olarak kameranın yapamadığını yapar: ürünü havada döndürür, ortadan ikiye keser, içindeki akışı renklendirir, montajını adım adım söker ve tekrar takar. {ekip}</p>

    <div class="rozetler">
      <span class="rozet">3D Ürün Modelleme</span>
      <span class="rozet">Çalışma Prensibi</span>
      <span class="rozet">Kesit Animasyon</span>
      <span class="rozet">Patlatılmış Görünüm</span>
      <span class="rozet">Üretim Hattı</span>
      <span class="rozet">Hizmet Süreci</span>
      <span class="rozet">Çok Dilli</span>
    </div>

    <h2>{ad}{ek} sektörünüze göre ne üretiyoruz</h2>
    <p>Aşağıdaki sektörlerde daha önce benzer ürünler modelledik; hazır iş akışımız olduğu için hem süre hem maliyet düşüyor. Her satır, o sektörde animasyonun en çok neye yaradığını anlatıyor.</p>
    {sektorler}

    <h2>{ad} firmalarında en sık karşılaştığımız üç ihtiyaç</h2>
    <p>{ad}{ek} üretim ağırlıklı olarak {ilce_kisa} hattında toplanıyor. Bu bölgedeki firmalarla çalışırken
       tekrar tekrar önümüze çıkan üç başlık şu:</p>
    <ul>{ihtiyaclar}</ul>

    <h2>{ad} firmaları bu videoyu nerede kullanıyor</h2>
    <ul>
      <li><strong>Fuar standı</strong> — sessiz döngü sürümü, ekranda sürekli dönen anlatım</li>
      <li><strong>İhracat görüşmesi</strong> — çok dilli sürüm, dil bariyerini aşan görsel anlatım</li>
      <li><strong>Teklif dosyası</strong> — teklife eklenen bağlantı, ürünü satış temsilcisi olmadan anlatıyor</li>
      <li><strong>Bayi ve satış ekibi eğitimi</strong> — montaj ve kullanım anlatımı</li>
      <li><strong>Web sitesi ve sosyal medya</strong> — ürün sayfası videosu, reklam kesimleri</li>
      <li><strong>İhale ve yatırımcı sunumu</strong> — tesis kapasitesinin görsel anlatımı</li>
    </ul>

    <h2>{ad}{ek} ilçeler ve organize sanayi bölgeleri</h2>
    <p>{ilceler} dahil ilin tamamındaki üretici firmalarla çalışıyoruz. Animasyon üretimi uzaktan yürüdüğü için mesafe bir engel değil; sadece tesiste çekim isteyen işlerde keşif planlıyoruz.</p>

    <h2 id="surec">Süreç</h2>
  </div>

  <div class="wrap">
    {surec}
  </div>

</section>

""".format(yerel_analiz=YA.blok(c, "urun"), ad=e(ad), ek=ek, slug0=c["slug"], sanayi=e(c["sanayi"]), ekip=e(ekip_cumlesi(c)),
           sektorler=sektor_bloku(c), ilceler=e(ilce_metni(c)),
           ilce_kisa=e(ilk_ilceler(c)),
           ihtiyaclar="".join("<li>%s</li>" % x for x in uc_ihtiyac(c)),
           surec=SUREC % ("Ürün brifingi","Teknik resim, CAD ya da fotoğraf; hedef kitle ve kullanım yeri.",
                          "Senaryo","Hangi özellik hangi saniyede anlatılacak, kare kare planlanıyor.",
                          "Modelleme ve animasyon","Ürün ölçülü modelleniyor; taslak sürüm onaya sunuluyor.",
                          "Teslim","Ses, grafik ve çok dilli sürümlerle çoklu format teslim."))

    g += video_bolumu("urun-animasyon", "Animasyon işlerimizden")
    g += """<section>
  <div class="wrap prose">
    <h2>{ad} — sık sorulan sorular</h2>
    {sss}

    <h2>{ad}{ek} diğer hizmetlerimiz</h2>
    {ilgili}

    <p style="margin-top:30px"><a href="../hizmetler/urun-animasyon" class="btn btn-cizgi">Hizmetin tüm detayları</a>
      <a href="https://wa.me/905411602603" class="btn btn-dolu">{ad} için teklif al</a></p>
  </div>
</section>

""".format(ad=e(ad), ek=ek, sss=sss_blok(sss), ilgili=ilgili_blok(c,"urun-animasyon"))
    g += cta(c, "Ürününüzü <i>anlatan</i> videoyu çıkaralım.",
                "Ürünün fotoğrafını ya da teknik resmini gönder; ne yapılabileceğini aynı gün konuşalım.")
    g += FOOTER
    return slug + ".html", g


ODAK = {"insaat-3d-modelleme":"insaat", "emlak-video":"emlak", "urun-animasyon":"urun",
        "klip-cekimi":"klip", "drone-cekimi":"drone", "dugun-cekimi":"dugun",
        "isletme-tanitim":"isletme"}


def uret(sec=None):
    """Kademeye göre üretim. uretici2 içindeki ek hizmetler de buradan çağrılır."""
    import uretici2
    cekirdek = [("insaat-3d-modelleme", sayfa_insaat3d),
                ("emlak-video", sayfa_emlak),
                ("urun-animasyon", sayfa_urun)]
    genis = cekirdek + [("klip-cekimi", uretici2.sayfa_klip),
                        ("drone-cekimi", uretici2.sayfa_drone),
                        ("dugun-cekimi", uretici2.sayfa_dugun),
                        ("isletme-tanitim", uretici2.sayfa_isletme)]
    yazilan = []
    for c in SEHIRLER:
        if sec and c["slug"] != sec:
            continue
        # genel il sayfası — her il için
        adi, icerik = uretici2.sayfa_sehir(c)
        icerik = sonlandir(icerik, c, "genel")
        open(os.path.join(HEDEF, adi), "w", encoding="utf-8").write(icerik)
        yazilan.append(adi)

        if c["kademe"] == 3:
            continue
        kume = genis if c["kademe"] == 1 else cekirdek
        for anahtar, fn in kume:
            adi, icerik = fn(c)
            icerik = sonlandir(icerik, c, ODAK[anahtar])
            open(os.path.join(HEDEF, adi), "w", encoding="utf-8").write(icerik)
            yazilan.append(adi)
    return yazilan


if __name__ == "__main__":
    sec = sys.argv[1] if len(sys.argv) > 1 else None
    y = uret(sec)
    print("%d sayfa üretildi → %s" % (len(y), HEDEF))
