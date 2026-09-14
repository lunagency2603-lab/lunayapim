# -*- coding: utf-8 -*-
"""Ortak HTML kabuğu — başlık, header, footer, modal."""

GTAG = """<script async src="https://www.googletagmanager.com/gtag/js?id=AW-18288531900"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'AW-18288531900');
</script>"""

HEADER = """<header>
  <div class="wrap hbar">
    <a class="marka" href="../">
      <img src="../assets/karga.png" alt="Luna Yapım">
      <span><b style="display:block">LUNA YAPIM</b><span>YAZILIM &amp; YAPIM</span></span>
    </a>
    <nav>
      <a href="../index.html#urunler">Ürünler</a>
      <a href="../yazilim">Yazılım</a>
      <a href="../hizmetler/">Prodüksiyon</a>
      <a href="../hizmetler/insaat-3d-modelleme">3D Modelleme</a>
      <a href="../isler">İşler</a>
      <a href="./" style="opacity:1;color:var(--kirmizi)">İller</a>
      <a href="../blog/">Blog</a>
      <a href="../trend/">TrendSaphiens</a>
      <a href="../iletisim">İletişim</a>
    </nav>
    <a class="hbtn" href="https://wa.me/905411602603">Teklif Al</a>
  </div>
</header>"""

FOOTER = """<footer>
  <div class="wrap">
    <div class="fgrid">
      <div>
        <div class="fmarka"><img src="../assets/karga.png" alt=""><b>LUNA YAPIM</b></div>
        <p style="color:rgba(239,237,232,.6);font-size:14.5px;max-width:34ch">
          Bursa merkezli yazılım ve yapım şirketi. Kendi ürünlerini yazan, kamerayı da kendi kullanan bir ekip.</p>
      </div>
      <div><h4>Hizmetler</h4>
        <a href="../hizmetler/insaat-3d-modelleme">İnşaat 3D Modelleme</a>
        <a href="../hizmetler/urun-animasyon">Ürün Animasyonu</a>
        <a href="../hizmetler/klip-cekimi">Klip Çekimi</a>
        <a href="../hizmetler/">Tüm prodüksiyon</a>
        <a href="../yazilim">Yazılım</a></div>
      <div><h4>Keşfet</h4>
        <a href="../isler">İşler</a>
        <a href="../blog/">Blog</a>
        <a href="../matrix">KDA Matrix</a>
        <a href="./">Tüm iller</a></div>
      <div><h4>İletişim</h4>
        <a href="https://wa.me/905411602603">WhatsApp</a>
        <a href="tel:+905411602603">0541 160 26 03</a>
        <a href="mailto:lunagency2603@gmail.com">E-posta</a>
        <a href="../iletisim">İletişim sayfası</a>
        <a href="../kosullar">Koşullar</a>
        <span data-sosyal class="sosyal-serit" style="margin-top:12px"></span></div>
    </div>
    <div class="falt">
      <span>© <span id="yil"></span> Luna Yapım · Bursa</span>
      <span>Yazılım · Otonom sistemler · Prodüksiyon</span>
    </div>
  </div>
</footer>

<div class="vmodal" id="vmodal">
  <button class="vkapat" onclick="lunaVideoKapat()" aria-label="Kapat">✕</button>
  <iframe id="vframe" allow="autoplay; encrypted-media" allowfullscreen></iframe>
</div>
<script src="../assets/videolar.js"></script>
<script src="../assets/sosyal.js"></script>
<script src="../assets/olcum.js"></script>
<script src="../assets/asistan.js?v=1" defer></script>
</body>
</html>"""

def head(baslik, aciklama, anahtar, kanonik, semalar):
    return """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
%s
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%s</title>
<meta name="description" content="%s">
<meta name="keywords" content="%s">
<link rel="canonical" href="%s">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:type" content="article">
<meta property="og:url" content="%s">
<meta property="og:image" content="https://lunayapim.com/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://lunayapim.com/assets/og-image.png">
<link rel="icon" type="image/x-icon" href="../assets/favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="../assets/favicon-32.png">
<link rel="apple-touch-icon" sizes="180x180" href="../assets/favicon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,800&family=Manrope:wght@400;500;600&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/luna.css">
%s
</head>
<body>
%s
""" % (GTAG, baslik, aciklama, anahtar, kanonik, baslik, aciklama, kanonik, semalar, HEADER)
