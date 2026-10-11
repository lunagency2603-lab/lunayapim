# -*- coding: utf-8 -*-
"""
YEREL ÖZGÜN SAYFA YAZICI — 11.10.2026

yerel_icerik.py'deki elle yazılmış il metnini, sayfanın mevcut kabuğuna
(head, menü, fiyat bölümü, iş vitrini, "diğer hizmetler", CTA, altbilgi)
yerleştirir. Adres, başlık ve canonical değişmez; gövde tamamen yenilenir.
Sayfa <!-- yerel-ozgun:v1 --> ve il-sabit işaretini taşır; otomatik yeniden
yazıcılar dokunmaz.
Kullanım: python3 yerel_ozgun.py <site kökü> [slug ...]
"""
import html, io, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from yerel_icerik import SAYFA

ISARET = "<!-- yerel-ozgun:v1 -->"


def _e(x):
    return html.escape(x, quote=True)


def _sss_html(sss):
    p = ['<div class="sss">']
    for i, (q, a) in enumerate(sss):
        p.append('<details%s><summary>%s</summary>\n  <div class="cvp"><p>%s</p></div></details>'
                 % (" open" if i == 0 else "", _e(q), _e(a)))
    p.append("</div>")
    return "\n".join(p)


def _kaynak_html(kaynak):
    if not kaynak:
        return ""
    li = " · ".join('<a href="%s" rel="noopener">%s</a>' % (_e(u), _e(t)) for t, u in kaynak)
    return '<p class="kaynak"><small>Kaynaklar: %s</small></p>' % li


def yaz(kok, slug):
    v = SAYFA[slug]
    y = os.path.join(kok, "sehir", slug + ".html")
    s = io.open(y, encoding="utf-8").read()
    # mevcut kabuk parçaları
    i_hero = s.index('<div class="page-hero">')
    i_foot = s.index("<footer")
    bas, govde, son = s[:i_hero], s[i_hero:i_foot], s[i_foot:]
    m_crumb = re.search(r'<div class="crumbs">.*?</div>', govde, re.S)
    m_h1 = re.search(r"<h1>.*?</h1>", govde, re.S)
    m_btn = re.search(r'<div class="btnlar">.*?</div>', govde, re.S)
    m_vid = re.search(r'<section class="acik" data-video-bolum.*?</section>', govde, re.S)
    m_fiyat = re.search(r'<!-- arama:fiyat -->.*?(?=<h2>)', govde, re.S)
    m_ilgili = re.search(r'<h2>[^<]*diğer hizmetlerimiz</h2>\s*<div class="ilgili">.*?</div>', govde, re.S)
    m_cta = re.search(r'(<section class="cta.*|<section class="kirmizi.*|<div class="cta.*)', govde, re.S)
    if not (m_crumb and m_h1):
        raise SystemExit("kabuk parçası bulunamadı: %s" % slug)
    il_ad = re.sub(r"<[^>]+>", "", m_h1.group(0)).split("'")[0].split("’")[0].strip()
    # ilk bölüm başlığını aranan ifadeyle hizala
    hero = ('<div class="page-hero">\n  <img class="karga-buyuk" src="../assets/karga.png" alt="">\n'
            '  <div class="wrap">\n    %s\n    %s\n    <p class="lede">%s</p>\n    %s\n  </div>\n</div>\n'
            % (m_crumb.group(0), m_h1.group(0), _e(v["lede"]), m_btn.group(0) if m_btn else ""))
    bol = []
    for baslik, metin in v["bolum"]:
        bol.append("    <h2>%s</h2>\n    %s\n" % (_e(baslik), metin))
    if slug.endswith("drone-cekimi"):
        bol.append('    <p><strong>Yetki:</strong> SHGM\'ye kayıtlı İHA ile ve lisanslı pilotla uçuyoruz; uçuşu taşerona vermiyoruz.</p>\n')
    yeni = [hero, "\n<section>\n  <div class=\"wrap prose\">\n", "\n".join(bol),
            _kaynak_html(v.get("kaynak")), "\n  </div>\n</section>\n\n"]
    if m_vid:
        yeni.append(m_vid.group(0) + "\n\n")
    yeni.append('<section>\n  <div class="wrap prose">\n    ')
    if m_fiyat:
        yeni.append(m_fiyat.group(0).rstrip() + "\n\n")
    yeni.append("    <h2>%s — sık sorulan sorular</h2>\n%s\n\n" % (_e(il_ad), _sss_html(v["sss"])))
    if m_ilgili:
        yeni.append("    " + m_ilgili.group(0) + "\n")
    yeni.append("  </div>\n</section>\n")
    if m_cta:
        yeni.append(m_cta.group(0))
    govde2 = "".join(yeni)
    # FAQPage şeması: yeni SSS ile değiştir
    faq = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q,
           "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in v["sss"]]}

    def _faq_degis(mm):
        try:
            d = json.loads(mm.group(1))
        except Exception:
            return mm.group(0)
        def _yenile(o):
            if isinstance(o, dict) and o.get("@type") == "FAQPage":
                o2 = dict(faq); o2["@context"] = o.get("@context", "https://schema.org") if "@context" in o else None
                if o2["@context"] is None: del o2["@context"]
                return o2
            if isinstance(o, dict) and "@graph" in o:
                o["@graph"] = [_yenile(x) for x in o["@graph"]]
            return o
        d = _yenile(d)
        return '<script type="application/ld+json">%s</script>' % json.dumps(d, ensure_ascii=False)
    bas = re.sub(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', _faq_degis, bas, flags=re.S)
    # meta açıklama: yeni giriş cümlesiyle (≤158)
    ac = v["lede"] if len(v["lede"]) <= 158 else v["lede"][:v["lede"].rfind(" ", 0, 155)] + "…"
    bas = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda mm: mm.group(1) + _e(ac) + mm.group(2), bas, 1)
    bas = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda mm: mm.group(1) + _e(ac) + mm.group(2), bas, 1)
    if ISARET not in bas:
        bas = bas.replace("<body", ISARET + "\n<body", 1)
    io.open(y, "w", encoding="utf-8").write(bas + govde2 + son)
    # fiyat şeması, kesik başlık ve sitemap tarihi (yerel_seo.py)
    from yerel_seo import calistir as _seo
    _seo(kok, None, [slug])
    return slug


if __name__ == "__main__":
    kok = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    hedef = sys.argv[2:] or list(SAYFA)
    print([yaz(kok, s) for s in hedef])
