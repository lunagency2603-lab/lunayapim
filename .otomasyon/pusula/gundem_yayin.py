# -*- coding: utf-8 -*-
"""
GÜNDEM YAYINI — günün sektör haberlerini Luna'nın diliyle siteye basar.

Akış:
  gundem.tara()  → puanlı haber listesi (Google Haberler RSS, kendi makinende)
  sec()          → sektör çeşitliliği gözeterek 3–6 madde
  sayi_yaz()     → /gundem/YYYY-MM-DD.html  (günün sayısı)
  hub_yaz()      → /gundem/index.html        (tüm sayılar)
  sitemap + menü + SEO kapısı

Kurallar:
  · Her madde kaynağını, kaynağın tarihini ve bağlantısını gösterir.
  · Haberi kopyalamıyoruz; 2–3 cümle olgu + "bizim için ne demek" açısı.
  · Uydurma rakam yok: sayı yalnızca kaynakta geçiyorsa yazılır.
  · SEO kapısı zorunlu — 100 altı sayı yayınlanmaz.
  · Yazı yapay zekâ kalıbı taşımasın: kısa cümle, somut sayı, tek fikir.
"""
import datetime, html, json, os, re, sys

from .ayarlar import SITE_KOK, KOK_DIZIN

HIZMET_AD = {
    "hizmetler/insaat-3d-modelleme.html": ("İnşaat 3D modelleme", "../hizmetler/insaat-3d-modelleme"),
    "hizmetler/emlak-kurumsal.html":      ("Emlak videosu", "../hizmetler/emlak-kurumsal"),
    "hizmetler/urun-animasyon.html":      ("Ürün animasyonu", "../hizmetler/urun-animasyon"),
    "hizmetler/drone-fpv.html":           ("Drone çekimi", "../hizmetler/drone-fpv"),
    "hizmetler/isletme-tanitim.html":     ("İşletme tanıtımı", "../hizmetler/isletme-tanitim"),
    "hizmetler/klip-cekimi.html":         ("Klip çekimi", "../hizmetler/klip-cekimi"),
    "sehir/bursa.html":                   ("Bursa", "../sehir/bursa"),
}

# Sektör görselleri (dergi düzeni): hizmet sayfası → (sektör, kicker, görsel, alt)
SEKTOR = {
    "hizmetler/insaat-3d-modelleme.html": ("İnşaat", "Konut · proje · render", "render-istasyonu", "Render istasyonu: tel kafes modelden fotogerçekçi kareye"),
    "hizmetler/emlak-kurumsal.html":      ("Emlak", "İlan · portföy · video", "drone-safak", "Şafakta çatı kenarında sinema dronu, arkada şehir"),
    "hizmetler/urun-animasyon.html":      ("Reklam", "Ürün · animasyon · etiket", "set-isik", "Boş set: kamera, tek sert ışık, sis"),
    "hizmetler/drone-fpv.html":           ("Havadan", "Drone · saha · 81 il", "drone-safak", "Şafakta çatı kenarında sinema dronu"),
    "hizmetler/isletme-tanitim.html":     ("İşletme", "Tanıtım filmi · sosyal medya", "set-isik", "Boş set: kamera ve ışık"),
    "hizmetler/klip-cekimi.html":         ("Müzik", "Klip · sahne · gece", "renk-masasi", "Renk masası: iki monitörde karga silueti"),
    "sehir/bursa.html":                   ("Bursa", "Yatırım · sanayi · şehir", "drone-safak", "Bursa: şafakta şehir"),
}
def _sektor(m):
    return SEKTOR.get(m.get("hizmet") or "", ("Sektör", "Gündem", "renk-masasi", "Renk masası"))

def _kart_gorsel(m, boy="k"):
    sek, kick, gor, alt = _sektor(m)
    return '<img src="../assets/studyo/%s%s.jpg" alt="%s" loading="lazy" width="800" height="447">' % (gor, "-k" if boy == "k" else "", _e(alt))

def _madde_ozet(m, n=190):
    o = (m.get("olgu") or "").strip()
    return o if len(o) <= n else o[:n].rsplit(" ", 1)[0] + "…"

AY = ["Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"]


def _e(x):
    return html.escape(x or "", quote=True)


def _tr_tarih(iso):
    y, a, g = iso.split("-")
    return "%d %s %s" % (int(g), AY[int(a) - 1], y)


def _kabuk():
    sys.path.insert(0, os.path.join(KOK_DIZIN, "site-uretici"))
    import kabuk
    return kabuk


def _menu_duzelt(bas, aktif):
    """Kabuk şablonu İller'i aktif basıyor ve Gündem/Bülten bağlantısını zaten içeriyor.
    Bu sayfada: İller sadeleşsin, kendi bağlantımız aktif olsun, çift ekleme olmasın."""
    bas = bas.replace('<a href="./" style="opacity:1;color:var(--kirmizi)">İller</a>',
                      '<a href="../sehir/">İller</a>')
    if aktif == "gundem":
        bas = bas.replace('<a href="../gundem/">Gündem</a>',
                          '<a href="./" style="opacity:1;color:var(--kirmizi)">Gündem</a>')
    elif aktif == "bulten":
        bas = bas.replace('<a href="../bulten/">Bülten</a>',
                          '<a href="./" style="opacity:1;color:var(--kirmizi)">Bülten</a>')
    return bas


def _sema(baslik, aciklama, url, maddeler, tarih):
    kaynaklar = [{"@type": "CreativeWork", "name": m["kaynak_ad"], "url": m["kaynak_url"]}
                 for m in maddeler if m.get("kaynak_url")]
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": baslik, "description": aciklama, "url": url,
         "datePublished": tarih, "dateModified": tarih, "inLanguage": "tr",
         "author": {"@type": "Organization", "name": "Luna Yapım", "url": "https://lunayapim.com/"},
         "publisher": {"@type": "Organization", "name": "Luna Yapım",
                       "logo": {"@type": "ImageObject", "url": "https://lunayapim.com/assets/luna-logo.png"}},
         "citation": kaynaklar},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": "https://lunayapim.com/"},
            {"@type": "ListItem", "position": 2, "name": "Gündem", "item": "https://lunayapim.com/gundem/"},
            {"@type": "ListItem", "position": 3, "name": baslik, "item": url}]},
    ]}, ensure_ascii=False) + '</script>' 


# ---------------------------------------------------------------- seçim
def sec(haberler, en_az=3, en_cok=6):
    """Puanı yüksek, sektörü çeşitli maddeler. Aynı konudan en çok iki."""
    sayac, ci = {}, []
    for h in sorted(haberler, key=lambda x: -x.get("puan", 0)):
        k = h.get("konu")
        if sayac.get(k, 0) >= 2:
            continue
        sayac[k] = sayac.get(k, 0) + 1
        ci.append(h)
        if len(ci) >= en_cok:
            break
    return ci if len(ci) >= en_az else ci


def madde_kur(baslik, kaynak_ad, kaynak_url, kaynak_tarih, olgu, aci, hizmet, ek="", aci_soru="", hizmet_soz="", yazi=None):
    """Elle ya da taramadan gelen tek maddeyi standart biçime sokar.
    olgu: kaynaktan kısa alıntı; ek: ikinci kısa parça; aci: bizim okumamız (paragraf);
    aci_soru: analiz başlığı (soru); hizmet_soz: hizmet bağlantısı cümlesi."""
    ad, yol = HIZMET_AD.get(hizmet, ("Hizmetlerimiz", "../hizmetler/"))
    return {"baslik": baslik, "kaynak_ad": kaynak_ad, "kaynak_url": kaynak_url,
            "kaynak_tarih": kaynak_tarih, "olgu": olgu, "ek": ek or "", "aci": aci,
            "aci_soru": aci_soru or "", "hizmet_soz": hizmet_soz or "", "yazi": yazi,
            "hizmet_ad": ad, "hizmet_yol": yol, "hizmet": hizmet}


def taramadan_madde(h):
    """gundem.tara() çıktısını maddeye çevirir. Analiz paragrafı ACILAR kalıbının
    gerekçesi + hizmet cümlesi; soru başlığı kalıptan. Olgu kaynak_ozet ile dolduysa
    gerçek alıntıdır, dolmadıysa haber sayfası açılmaz (trend.yayinla kapısı)."""
    a = h.get("aci") or {}
    soz = a.get("bizim_soz") or ""
    gerekce = (a.get("gerekce") or "").strip()
    analiz = (gerekce + (" Bizim tarafımız: " + soz[:1].lower() + soz[1:] + ".") if gerekce and soz else (gerekce or soz)).strip()
    return madde_kur(h["baslik"], h.get("kaynak") or "Kaynak", h["adres"],
                     h.get("tarih") or "", h.get("ozet") or "",
                     analiz, h.get("hizmet_sayfa") or "",
                     ek=h.get("ek") or "", aci_soru=a.get("baslik") or "", hizmet_soz=soz)


# ---------------------------------------------------------------- yazım
def sayi_html(tarih, maddeler, aranan=None, komsu=None):
    """Günün sayısı — dergi düzeni: manşet + akış + yan sütun. komsu = (onceki, sonraki) tarih."""
    K = _kabuk()
    tr = _tr_tarih(tarih)
    baslik = "Gündem · %s — sektörlerimizde bugün ne oldu" % tr
    aciklama = ("%s: inşaat, emlak, sanayi ve tanıtım sektörlerinden günün gelişmeleri ve "
                "Luna Yapım için ne anlama geldiği. Kaynaklı, tarihli." % tr)[:160]
    url = "https://lunayapim.com/gundem/%s" % tarih
    anahtar = "sektör gündemi, inşaat haberleri, emlak haberleri, sanayi haberleri, tanıtım filmi, drone, 3d modelleme"

    bas = K.head(_e(baslik), _e(aciklama), _e(anahtar), url,
                 _sema(baslik, aciklama, url, maddeler, tarih))
    bas = _menu_duzelt(bas, "gundem")
    if maddeler:
        bas = bas.replace('content="https://lunayapim.com/assets/og-image.png"',
                          'content="https://lunayapim.com/assets/studyo/%s.jpg"' % _sektor(maddeler[0])[2])

    onceki, sonraki = (komsu or (None, None))
    gez = '<div class="dg-gez">%s<span>Sayı · %s</span>%s</div>' % (
        ('<a href="%s">← %s</a>' % (onceki, _tr_tarih(onceki))) if onceki else '<span></span>',
        tr,
        ('<a href="%s">%s →</a>' % (sonraki, _tr_tarih(sonraki))) if sonraki else '<a href="./">Tüm sayılar →</a>')

    # manşet
    man = ""
    if maddeler:
        m = maddeler[0]; sek, kick, gor, alt = _sektor(m)
        man = """
    <article class="dg-lead gm" id="m1">
      <div class="dg-lead-gorsel">%s<span class="dg-chip">%s</span></div>
      <div class="dg-lead-metin">
        <p class="dg-kicker">%s</p>
        <h2>%s</h2>
        <p class="gm-olgu">%s</p>
        <div class="dg-nedemek"><b>Bizim için ne demek</b><p>%s</p><a href="%s">%s →</a></div>
        <p class="gm-kaynak">Kaynak: <a href="%s" rel="nofollow noopener" target="_blank">%s</a>%s</p>
      </div>
    </article>""" % (_kart_gorsel(m, "b"), _e(sek), _e(kick), _e(m["baslik"]), _e(m["olgu"]), _e(m["aci"]),
                     _e(m["hizmet_yol"]), _e(m["hizmet_ad"]), _e(m["kaynak_url"]), _e(m["kaynak_ad"]),
                     (" · " + _e(m["kaynak_tarih"])) if m.get("kaynak_tarih") else "")
    # akış
    akis = []
    for i, m in enumerate(maddeler[1:], 2):
        sek, kick, gor, alt = _sektor(m)
        akis.append("""
    <article class="dg-madde gm" id="m%d">
      <div class="dg-madde-ust"><span class="gm-no">%02d</span><span class="dg-chip">%s</span><span class="dg-kicker">%s</span></div>
      <div class="dg-madde-govde">
        <div class="dg-madde-gorsel">%s</div>
        <div>
          <h2>%s</h2>
          <p class="gm-olgu">%s</p>
          <div class="dg-nedemek"><b>Bizim için ne demek</b><p>%s</p><a href="%s">%s →</a></div>
          <p class="gm-kaynak">Kaynak: <a href="%s" rel="nofollow noopener" target="_blank">%s</a>%s</p>
        </div>
      </div>
    </article>""" % (i, i, _e(sek), _e(kick), _kart_gorsel(m), _e(m["baslik"]), _e(m["olgu"]), _e(m["aci"]),
                     _e(m["hizmet_yol"]), _e(m["hizmet_ad"]), _e(m["kaynak_url"]), _e(m["kaynak_ad"]),
                     (" · " + _e(m["kaynak_tarih"])) if m.get("kaynak_tarih") else ""))
    # yan sütun
    toc = "".join('<li><a href="#m%d"><span>%02d</span>%s</a></li>' % (i, i, _e(m["baslik"])) for i, m in enumerate(maddeler, 1))
    aranan_html = ""
    if aranan:
        aranan_html = ('<div class="dg-kutu"><span class="etk">Bugün en çok aranan</span>'
                       '<ol class="gm-aranan">%s</ol><p class="dg-not">Google otomatik tamamlama, günün sırası. Hacim değil sıra.</p></div>'
                       % "".join("<li>%s</li>" % _e(x) for x in aranan[:8]))
    yan = """
    <aside class="dg-yan">
      <div class="dg-kutu"><span class="etk">Bu sayıda</span><ol class="dg-toc">%s</ol></div>
      %s
      <div class="dg-kutu dg-abone"><span class="etk">Matrix Bülteni</span><p>Piyasayı okuyan sistemin haftalık karnesi, e-postana. Ücretsiz.</p><a class="btn btn-dolu" href="../bulten/#abone">Abone ol</a></div>
      <div class="dg-kutu"><span class="etk">Gündemi işe çevir</span><p>Sektörünüzdeki gelişmeyi tanıtıma dönüştürelim; aynı gün net aralık.</p><a class="btn btn-cizgi" href="https://wa.me/905411602603">WhatsApp'tan yaz</a></div>
    </aside>""" % (toc, aranan_html)

    govde = """
<div class="dg-mast">
  <div class="wrap">
    <div class="crumbs"><a href="../">Ana Sayfa</a> · <a href="./">Gündem</a> · %s</div>
    <div class="dg-mast-satir">
      <a class="dg-marka" href="./">Gündem<small>Luna Yapım · sektör günlüğü</small></a>
      <div class="dg-tarih"><b>%s</b><span>%d madde · kaynaklı, tarihli</span></div>
      <nav class="dg-sek"><a href="../hizmetler/insaat-3d-modelleme">İnşaat</a><a href="../hizmetler/emlak-kurumsal">Emlak</a><a href="../hizmetler/isletme-tanitim">Reklam</a><a href="../yazilim">Yazılım</a><a href="../sehir/bursa">Bursa</a></nav>
    </div>
    %s
  </div>
</div>
<h1 class="dg-h1">Sektörlerimizde bugün — %s</h1>

<section class="dg-govde">
  <div class="wrap dg-izgara">
    <div class="dg-ana">%s%s</div>
    %s
  </div>
</section>

<section class="cta">
  <div class="wrap">
    <span class="etk">Gündemi işe çevirelim</span>
    <h2>Sektörünüzdeki gelişmeyi <i>tanıtıma</i> dönüştürelim.</h2>
    <p>Haberi okumak bir şey, ondan iş çıkarmak başka. Projenizi anlatın; aynı gün net bir aralık verelim.</p>
    <div class="btnlar">
      <a href="https://wa.me/905411602603" class="btn btn-dolu" style="background:#fff;color:var(--kirmizi)">WhatsApp'tan yaz</a>
      <a href="../iletisim" class="btn btn-cizgi" style="border-color:rgba(255,255,255,.5);color:#fff">İletişim</a>
    </div>
  </div>
</section>
""" % (tr, tr, len(maddeler), gez, tr, man, "".join(akis), yan)
    return baslik, bas + govde + K.FOOTER


def _son_sayi_maddeleri(kok):
    """En yeni sayının maddelerini veri/gundem/YYYY-MM-DD.json dosyasından okur."""
    d = os.path.join(KOK_DIZIN, "veri", "gundem")
    if not os.path.isdir(d):
        return None, []
    ds = sorted(f for f in os.listdir(d) if re.match(r"\d{4}-\d{2}-\d{2}\.json$", f))
    if not ds:
        return None, []
    tarih = ds[-1][:-5]
    try:
        ham = json.load(open(os.path.join(d, ds[-1]), encoding="utf-8"))
    except Exception:
        return tarih, []
    return tarih, [madde_kur(m["baslik"], m.get("kaynak_ad", ""), m.get("kaynak_url", ""), m.get("kaynak_tarih", ""),
                            m.get("olgu", ""), m.get("aci", ""), m.get("hizmet", ""))
                   for m in ham]


def hub_html(sayilar):
    K = _kabuk()
    baslik = "Gündem — sektörlerimizde her gün ne oluyor | Luna Yapım"
    aciklama = ("İnşaat, emlak, sanayi ve tanıtım sektörlerinden günlük gelişmeler; her madde "
                "kaynaklı ve tarihli, altında Luna Yapım için ne anlama geldiği.")
    url = "https://lunayapim.com/gundem/"
    sema = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "CollectionPage",
                       "name": baslik, "url": url, "description": aciklama,
                       "isPartOf": {"@type": "WebSite", "name": "Luna Yapım", "url": "https://lunayapim.com/"}},
                      ensure_ascii=False) + '</script>'
    bas = K.head(_e(baslik), _e(aciklama), _e("sektör gündemi, günlük haber, inşaat, emlak, sanayi"), url, sema)
    bas = _menu_duzelt(bas, "gundem")

    son_tarih, son = _son_sayi_maddeleri(None)
    # manşet + ikincil kartlar (en yeni sayıdan)
    manset, ikincil = "", ""
    if son:
        m = son[0]; sek, kick, gor, alt = _sektor(m)
        manset = """
      <a class="dg-lead dg-lead-link" href="%s#m1">
        <div class="dg-lead-gorsel">%s<span class="dg-chip">%s</span></div>
        <div class="dg-lead-metin">
          <p class="dg-kicker">%s · %s</p>
          <h2>%s</h2>
          <p class="gm-olgu">%s</p>
          <p class="dg-devam">Sayıyı oku →</p>
        </div>
      </a>""" % (son_tarih, _kart_gorsel(m, "b"), _e(sek), _e(_tr_tarih(son_tarih)), _e(kick), _e(m["baslik"]), _e(_madde_ozet(m, 220)))
        kart = []
        for i, m in enumerate(son[1:4], 2):
            sek, kick, gor, alt = _sektor(m)
            kart.append('<a class="dg-kart" href="%s#m%d"><div class="dg-kart-gorsel">%s</div><span class="dg-chip">%s</span><h3>%s</h3><p>%s</p></a>'
                        % (son_tarih, i, _kart_gorsel(m), _e(sek), _e(m["baslik"]), _e(_madde_ozet(m, 130))))
        ikincil = '<div class="dg-kartlar">%s</div>' % "".join(kart)

    arsiv = "".join(
        '<a class="gm-kart" href="%s"><span class="etk">%s</span><b>%s</b><span>%d madde</span></a>'
        % (s["tarih"], _e(_tr_tarih(s["tarih"])), _e(s["baslik"]), s["madde"])
        for s in sorted(sayilar, key=lambda x: x["tarih"], reverse=True))
    bugun = _tr_tarih(son_tarih) if son_tarih else _tr_tarih(datetime.date.today().isoformat())

    govde = """
<div class="dg-mast">
  <div class="wrap">
    <div class="crumbs"><a href="../">Ana Sayfa</a> · Gündem</div>
    <div class="dg-mast-satir">
      <span class="dg-marka">Gündem<small>Luna Yapım · sektör günlüğü</small></span>
      <div class="dg-tarih"><b>%s</b><span>%d sayı · her gün bir sayı</span></div>
      <nav class="dg-sek"><a href="../hizmetler/insaat-3d-modelleme">İnşaat</a><a href="../hizmetler/emlak-kurumsal">Emlak</a><a href="../hizmetler/isletme-tanitim">Reklam</a><a href="../yazilim">Yazılım</a><a href="../sehir/bursa">Bursa</a></nav>
    </div>
  </div>
</div>
<h1 class="dg-h1">Sektörlerimizde her gün ne oluyor</h1>

<section class="dg-govde">
  <div class="wrap dg-izgara">
    <div class="dg-ana">%s%s</div>
    <aside class="dg-yan">
      <div class="dg-kutu"><span class="etk">Nasıl seçiyoruz</span><p>Her sabah inşaat, konut, emlak, sanayi, turizm, mobilya, yapay zekâ düzenlemeleri ve Bursa gündemi taranır. İki soru: işimize dokunuyor mu, dokunuyorsa ne söyleyebiliriz? Rakam yalnızca kaynakta varsa yazılır.</p></div>
      <div class="dg-kutu dg-abone"><span class="etk">Matrix Bülteni</span><p>Piyasayı okuyan sistemin haftalık karnesi, e-postana. Ücretsiz, reklamsız.</p><a class="btn btn-dolu" href="../bulten/#abone">Abone ol</a></div>
      <div class="dg-kutu"><span class="etk">Derinleşen konular</span><p>Burada öne çıkan başlık ertesi hafta blogda uzun yazıya dönüşür.</p><a class="btn btn-cizgi" href="../blog/">Blog</a></div>
    </aside>
  </div>
</section>

<section class="acik"><div class="wrap">
  <div class="bas"><span class="no">◆</span><div><h2>Arşiv</h2>
    <p class="aciklama">Her gün bir sayı. En yenisi üstte.</p></div></div>
  <div class="gm-kartlar">%s</div>
</div></section>

<section><div class="wrap prose">
  <h2>Neden bir prodüksiyon şirketi gündem tutuyor</h2>
  <p>Çünkü işimiz sektörün nabzına bağlı. Konut satışı düştüğünde satış ofisinin görsele
    ihtiyacı artıyor, kira talebi yükseldiğinde ilan videosu fark yaratıyor, reklamda yapay zekâ
    etiketi zorunlu olunca gerçek çekimin değeri değişiyor. Bunları takip etmeyen bir yapım şirketi
    müşterisine yalnızca kamera satar; biz neyin neden işe yaradığını da anlatmak istiyoruz.</p>
  <h2>Hangi başlıkları izliyoruz</h2>
  <p>İnşaat ve konut projeleri, TÜİK konut satış verisi, kira ve satılık piyasa raporları,
    kentsel dönüşüm, sanayi üretimi ve ihracat, fuar takvimi, turizm ve otel yatırımları,
    mobilya ve dekorasyon, yapay zekâ ile görsel ve video üretimine dair düzenlemeler, küçük
    işletmelerin sosyal medya kullanımı ve Bursa'nın yatırım gündemi. Siyaset, asayiş, spor, magazin,
    döviz ve borsanın günlük hareketi bu sayfaya girmiyor; bizim işimizle kesişmiyor.</p>
  <h2>Yazılar neden kısa</h2>
  <p>Haberi yeniden yazmıyoruz; kaynağı zaten bağlıyoruz. Bizim eklediğimiz şey iki üç cümlelik
    olgu özeti ve tek bir açı: bu gelişme bir inşaat firmasının, bir emlak ofisinin, bir
    üreticinin tanıtım kararını nasıl etkiler. Rakam kaynakta yoksa biz de yazmıyoruz — tahmin,
    projeksiyon ya da "uzmanlara göre" cümlesi bu sayfada yok. Bir maddeyle ilgili işiniz varsa
    altındaki hizmet bağlantısından o sayfaya geçebilir, ya da <a href="../iletisim">bize yazabilirsiniz</a>.</p>
</div></section>
""" % (bugun, len(sayilar), manset, ikincil, arsiv)
    return bas + govde + K.FOOTER


# ---------------------------------------------------------------- dosya işleri
def _sayilar(kok):
    d = os.path.join(kok, "gundem")
    ci = []
    if not os.path.isdir(d):
        return ci
    for f in sorted(os.listdir(d)):
        m = re.match(r"(\d{4}-\d{2}-\d{2})\.html$", f)
        if not m:
            continue
        s = open(os.path.join(d, f), encoding="utf-8").read()
        t = re.search(r"<title>(.*?)</title>", s, re.S)
        ci.append({"tarih": m.group(1), "baslik": re.sub(r"\s+", " ", t.group(1)).split("|")[0].strip() if t else m.group(1),
                   "madde": s.count('class="gm"')})
    return ci


def _sitemap_ekle(kok, adresler):
    y = os.path.join(kok, "sitemap.xml")
    if not os.path.exists(y):
        return
    s = open(y, encoding="utf-8").read()
    bugun = datetime.date.today().isoformat()
    for a in adresler:
        if a not in s:
            s = s.replace("</urlset>", "  <url><loc>%s</loc><lastmod>%s</lastmod><changefreq>daily</changefreq><priority>0.6</priority></url>\n</urlset>" % (a, bugun))
    open(y, "w", encoding="utf-8").write(s)


def _menu_ekle(kok):
    """Tüm sayfaların üst menüsüne Gündem bağlantısı (bir kez)."""
    n = 0
    for d, altlar, dosyalar in os.walk(kok):
        altlar[:] = [a for a in altlar if a not in ("assets", ".git", ".github")]
        for f in dosyalar:
            if not f.endswith(".html") or f == "matrix.html":
                continue
            y = os.path.join(d, f)
            s = open(y, encoding="utf-8").read()
            if 'gundem/' in s and '>Gündem<' in s:
                continue
            on = "../" * os.path.relpath(y, kok).count(os.sep)
            m = re.search(r'<a href="%sblog/"[^>]*>Blog</a>' % re.escape(on), s) or \
                re.search(r'<a href="[^"]*blog/"[^>]*>Blog</a>', s)
            if not m:
                continue
            s = s.replace(m.group(0), m.group(0) + '\n      <a href="%sgundem/">Gündem</a>' % on, 1)
            open(y, "w", encoding="utf-8").write(s); n += 1
    return n


def yayinla(maddeler, tarih=None, aranan=None, kok=None, kapi=True):
    """Günün sayısını yazar, hub'ı yeniler, site haritasına ekler, kapıdan geçirir."""
    kok = kok or SITE_KOK
    tarih = tarih or datetime.date.today().isoformat()
    d = os.path.join(kok, "gundem")
    os.makedirs(d, exist_ok=True)
    mevcut = sorted(set(x["tarih"] for x in _sayilar(kok)) | {tarih})
    k = mevcut.index(tarih)
    komsu = (mevcut[k - 1] if k > 0 else None, mevcut[k + 1] if k + 1 < len(mevcut) else None)
    baslik, h = sayi_html(tarih, maddeler, aranan, komsu)
    yol = os.path.join(d, "%s.html" % tarih)
    open(yol, "w", encoding="utf-8").write(h)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(hub_html(_sayilar(kok)))
    _sitemap_ekle(kok, ["https://lunayapim.com/gundem/", "https://lunayapim.com/gundem/%s" % tarih])
    menu = _menu_ekle(kok)

    # üretim sonrası işlem (uzantısız adres, asistan, sürüm)
    try:
        sys.path.insert(0, os.path.join(KOK_DIZIN, "site-uretici"))
        import sonislem
        sonislem.calistir(kok, desen="gundem/*.html")
    except Exception as ex:
        pass

    sonuc = {"sayfa": yol, "madde": len(maddeler), "menu_eklenen": menu, "kapi": None}
    if kapi:
        try:
            sys.path.insert(0, KOK_DIZIN)
            from seo import denetci
            r = denetci.sayfa_denetle(yol, kok) if hasattr(denetci, "sayfa_denetle") else None
            sonuc["kapi"] = r
        except Exception as ex:
            sonuc["kapi"] = "denetçi çalışmadı: %s" % ex
    return sonuc


def hepsini_yeniden_yaz(kok=None):
    """Düzen değişince: veri/gundem/*.json'dan bütün sayıları ve ön sayfayı yeniden basar."""
    kok = kok or SITE_KOK
    d = os.path.join(KOK_DIZIN, "veri", "gundem")
    tarihler = sorted(f[:-5] for f in os.listdir(d) if re.match(r"\d{4}-\d{2}-\d{2}\.json$", f)) if os.path.isdir(d) else []
    n = 0
    for k, t in enumerate(tarihler):
        ham = json.load(open(os.path.join(d, t + ".json"), encoding="utf-8"))
        maddeler = [madde_kur(m["baslik"], m.get("kaynak_ad", ""), m.get("kaynak_url", ""), m.get("kaynak_tarih", ""),
                              m.get("olgu", ""), m.get("aci", ""), m.get("hizmet", ""),
                              ek=m.get("ek", ""), aci_soru=m.get("aci_soru", ""), hizmet_soz=m.get("hizmet_soz", ""), yazi=m.get("yazi")) for m in ham]
        komsu = (tarihler[k - 1] if k > 0 else None, tarihler[k + 1] if k + 1 < len(tarihler) else None)
        b, h = sayi_html(t, maddeler, None, komsu)
        open(os.path.join(kok, "gundem", t + ".html"), "w", encoding="utf-8").write(h); n += 1
    open(os.path.join(kok, "gundem", "index.html"), "w", encoding="utf-8").write(hub_html(_sayilar(kok)))
    try:
        sys.path.insert(0, os.path.join(KOK_DIZIN, "site-uretici"))
        import sonislem
        sonislem.calistir(kok, desen="gundem/*.html")
    except Exception:
        pass
    return n
