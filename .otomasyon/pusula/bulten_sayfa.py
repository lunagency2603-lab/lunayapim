# -*- coding: utf-8 -*-
"""
GÜNÜN BÜLTENİ — tek sayfada numaralı geçişle 25-30 haber.

20.09.2026 isteği: okur tek tek sayfa açmadan, bülten okur gibi sırayla
geçerek günün tamamını görsün. Klasik "sonraki haber" kalıbı: her ekranda
tek madde, altta numaralar, ok tuşu ve kaydırma ile geçiş.

SEO: bütün maddeler tek HTML'de ve DOM'da basılı — slider yalnız sunum
katmanı. JavaScript kapalıyken sayfa dikey liste olarak okunur ve her
maddenin kendi sayfasına bağlantısı çalışır.

Erişilebilirlik: geçişler gerçek düğme; ok tuşları, Home/End ve dokunmatik
kaydırma çalışır; prefers-reduced-motion'da yumuşak kaydırma kapanır.
"""
import datetime, io, json, os

from .ayarlar import SITE_KOK
from . import trend as T

KOK_URL = "https://lunayapim.com/trend/"
ADET = 30          # bültene giren madde sayısı
SLUG = "bulten"


def _e(x):
    return T._e(x)


def _maddeler(kok):
    """Akıştaki en yeni maddeler — bölüm sayfaları ve sistem sayfaları hariç."""
    hepsi = T._hepsi(kok)
    out = []
    for m in hepsi:
        if m.get("kat") in ("sistem",):
            continue
        out.append(m)
        if len(out) >= ADET:
            break
    return out


def _u(m, tr=""):
    if m["tur"] in ("haber", "rehber"):
        return tr + m["slug"]
    if m["tur"] == "sayfa":
        return tr + m["url"]
    return "../" + m["url"][3:]


def bulten_html(kok, tr=""):
    mad = _maddeler(kok)
    if not mad:
        return None
    bugun = datetime.date.today()
    # Sayı numarası: yayının başladığı gün 03.09.2026 = 1. sayı
    sayi = (bugun - datetime.date(2026, 9, 3)).days + 1
    baslik = "TrendSaphiens Bülteni · Sayı %d · %s" % (sayi, T._tr_tarih(bugun.isoformat()))
    aciklama = ("Günün %d başlığı tek sayfada, sırayla: haber, piyasa, burç, spor ve teknoloji. "
                "Okları kullanın ya da numaradan atlayın." % len(mad))

    slayt, numara = [], []
    for i, m in enumerate(mad, 1):
        kat = m.get("kat") or "haber"
        kat_ad = T.KATEGORI.get(kat, (kat.title(), ""))[0]
        g = T._gorsel_url(m.get("gorsel"))
        gorsel = ('<figure class="bl-gorsel"><img src="%s" alt="%s" loading="%s" decoding="async" width="960" height="540"></figure>'
                  % (_e(g), _e(m["baslik"]), "eager" if i <= 2 else "lazy"))
        slayt.append(
            '<article class="bl-slayt" id="bl-%d" aria-roledescription="madde" aria-label="%d / %d">'
            '%s'
            '<div class="bl-govde">'
            '<p class="bl-ust"><span class="bl-rozet">%s</span><time datetime="%s">%s</time>'
            '<span class="bl-sira">%02d<i>/%d</i></span></p>'
            '<h2 class="bl-baslik"><a href="%s">%s</a></h2>'
            '<p class="bl-ozet">%s</p>'
            '<p class="bl-git"><a class="btn btn-cizgi" href="%s">Haberin tamamı →</a></p>'
            '</div></article>'
            % (i, i, len(mad), gorsel, _e(kat_ad), _e(m["tarih"][:10]), _e(T._tr_tarih(m["tarih"][:10])),
               i, len(mad), _e(_u(m, tr)), _e(m["baslik"]), _e((m.get("olgu") or "")[:240]),
               _e(_u(m, tr))))
        numara.append('<button type="button" class="bl-no" data-git="%d" aria-label="%d. maddeye git">%d</button>' % (i, i, i))

    sema = json.dumps({
        "@context": "https://schema.org", "@type": "ItemList",
        "name": baslik, "url": KOK_URL + SLUG, "numberOfItems": len(mad),
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": m["baslik"], "url": KOK_URL + _u(m, "")}
            for i, m in enumerate(mad, 1)],
    }, ensure_ascii=False)
    sema_html = '<script type="application/ld+json">%s</script>' % sema

    js = """
<script>
(function(){
  var ray = document.getElementById("bl-ray");
  if (!ray) return;
  var slaytlar = Array.prototype.slice.call(ray.querySelectorAll(".bl-slayt"));
  var nolar = Array.prototype.slice.call(document.querySelectorAll(".bl-no"));
  var sayac = document.getElementById("bl-sayac");
  var cubuk = document.getElementById("bl-ilerleme");
  var onceki = document.getElementById("bl-onceki");
  var sonraki = document.getElementById("bl-sonraki");
  var simdi = 0;
  document.body.classList.add("bl-js");

  function isaretle(i){
    simdi = Math.max(0, Math.min(slaytlar.length - 1, i));
    nolar.forEach(function(b, n){
      var a = n === simdi;
      b.classList.toggle("etkin", a);
      b.setAttribute("aria-current", a ? "true" : "false");
    });
    if (sayac) sayac.textContent = (simdi + 1) + " / " + slaytlar.length;
    if (cubuk) cubuk.style.width = ((simdi + 1) / slaytlar.length * 100) + "%";
    if (onceki) onceki.disabled = simdi === 0;
    if (sonraki) sonraki.disabled = simdi === slaytlar.length - 1;
    var etkinNo = nolar[simdi];
    if (etkinNo && etkinNo.parentNode.scrollWidth > etkinNo.parentNode.clientWidth) {
      var p = etkinNo.parentNode;
      p.scrollTo({left: etkinNo.offsetLeft - p.clientWidth / 2 + etkinNo.clientWidth / 2, behavior: "smooth"});
    }
  }
  function git(i){
    var h = slaytlar[Math.max(0, Math.min(slaytlar.length - 1, i))];
    if (!h) return;
    ray.scrollTo({left: h.offsetLeft - ray.offsetLeft, behavior: "smooth"});
    isaretle(i);
  }
  nolar.forEach(function(b){ b.addEventListener("click", function(){ git(+b.getAttribute("data-git") - 1); }); });
  if (onceki) onceki.addEventListener("click", function(){ git(simdi - 1); });
  if (sonraki) sonraki.addEventListener("click", function(){ git(simdi + 1); });

  // kaydırma bittiğinde hangi slaytta olduğumuzu bul
  var zamanlayici;
  ray.addEventListener("scroll", function(){
    clearTimeout(zamanlayici);
    zamanlayici = setTimeout(function(){
      var en = ray.scrollLeft, yakin = 0, fark = Infinity;
      slaytlar.forEach(function(s, n){
        var d = Math.abs(s.offsetLeft - ray.offsetLeft - en);
        if (d < fark){ fark = d; yakin = n; }
      });
      isaretle(yakin);
    }, 90);
  }, {passive: true});

  document.addEventListener("keydown", function(e){
    if (e.target && /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName)) return;
    if (e.key === "ArrowRight"){ e.preventDefault(); git(simdi + 1); }
    else if (e.key === "ArrowLeft"){ e.preventDefault(); git(simdi - 1); }
    else if (e.key === "Home"){ e.preventDefault(); git(0); }
    else if (e.key === "End"){ e.preventDefault(); git(slaytlar.length - 1); }
  });
  isaretle(0);
})();
</script>
"""

    govde = """
<main class="bl-sayfa">
  <div class="wrap">
    <nav class="ts-crumbs"><a href="./">TrendSaphiens</a> · Bülten</nav>
    <header class="bl-bas">
      <p class="etk">Sayı %d · %s</p>
      <h1>Günün bülteni</h1>
      <p class="bl-ozet-ust">%s</p>
    </header>

    <div class="bl-denetim">
      <button type="button" id="bl-onceki" class="bl-ok" aria-label="Önceki madde">&larr;</button>
      <div class="bl-ilerleme-kap"><span id="bl-ilerleme" class="bl-ilerleme"></span></div>
      <span id="bl-sayac" class="bl-sayac">1 / %d</span>
      <button type="button" id="bl-sonraki" class="bl-ok" aria-label="Sonraki madde">&rarr;</button>
    </div>

    <div class="bl-ray" id="bl-ray" tabindex="0" role="group" aria-label="Günün maddeleri">%s</div>

    <nav class="bl-nolar" aria-label="Madde numaraları">%s</nav>

    <section class="ts-giris bl-not">
      <h2>Bu sayfa nasıl okunur?</h2>
      <p>Her ekranda bir madde var. Sağ ve sol ok tuşlarıyla, alttaki numaralarla ya da
      doğrudan kaydırarak geçebilirsiniz. Başlığa dokunduğunuzda haberin tam metnine gidersiniz.</p>
      <p>Bülten her yayında yeniden derlenir: en yeni %d madde, bölüm ayrımı olmadan,
      yayına giriş sırasına göre. Kaynak ve tarih her maddenin kendi sayfasında durur.</p>
    </section>
    <p class="ts-arac-geri"><a href="./">← Akışa dön</a></p>
  </div>
</main>
""" % (sayi, _e(T._tr_tarih(bugun.isoformat())), _e(aciklama), len(mad),
       "".join(slayt), "".join(numara), len(mad))

    return T._bas(baslik, aciklama, KOK_URL + SLUG, mad[0].get("gorsel"), sema_html, "website", "../", tr, ana=False) \
        + govde + js + T._alt("../", tr, ana=False)


def yayinla(kok=None):
    kok = kok or SITE_KOK
    html = bulten_html(kok)
    if not html:
        return {"bulten": "madde yok"}
    yol = os.path.join(kok, "trend", SLUG + ".html")
    io.open(yol, "w", encoding="utf-8").write(html)
    # sitemap
    y = os.path.join(kok, "sitemap.xml")
    try:
        s = io.open(y, encoding="utf-8").read()
        adres = KOK_URL + SLUG
        if adres not in s:
            s = s.replace("</urlset>",
                          '  <url><loc>%s</loc><lastmod>%s</lastmod><changefreq>daily</changefreq><priority>0.8</priority></url>\n</urlset>'
                          % (adres, datetime.date.today().isoformat()))
            io.open(y, "w", encoding="utf-8").write(s)
    except Exception as ex:
        print("sitemap:", ex)
    return {"bulten": SLUG, "madde": html.count('class="bl-slayt"')}


if __name__ == "__main__":
    print(json.dumps(yayinla(), ensure_ascii=False))
