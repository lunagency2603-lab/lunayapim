# -*- coding: utf-8 -*-
"""
ANA HİZMET SAYFASI → İL SAYFALARI BAĞLANTI BLOĞU

Bulgu (02.09): 7 ana hizmet sayfasının hiçbiri kendi il sayfalarına bağlanmıyordu.
250 il-hizmet sayfası yalnızca site haritasından keşfediliyor, otorite taşıyan
ana sayfalardan hiç pay almıyordu. Google'da 37–88. sırada kalmamızın en
somut yapısal sebebi buydu.

Bu modül her ana hizmet sayfasına "İllere göre …" bloğu ekler: o hizmetin
gerçekten var olan il sayfalarına bağlantı. Olmayan sayfaya bağlanmaz.
Etkisiz tekrarlanabilir — ikinci çalıştırma bloğu yeniler, çoğaltmaz.
"""
import glob, html, io, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sehirler import SEHIR_INDEKS

# ana sayfa dosyası → (il sayfası eki, blok başlığı)
ESLEME = {
    "drone-fpv":            ("drone-cekimi",        "İllere göre drone çekimi"),
    "emlak-kurumsal":       ("emlak-video",         "İllere göre emlak video çekimi"),
    "insaat-3d-modelleme":  ("insaat-3d-modelleme", "İllere göre inşaat 3D modelleme"),
    "urun-animasyon":       ("urun-animasyon",      "İllere göre ürün animasyonu"),
    "klip-cekimi":          ("klip-cekimi",         "İllere göre klip çekimi"),
    "dugun-etkinlik":       ("dugun-cekimi",        "İllere göre düğün çekimi"),
    "isletme-tanitim":      ("isletme-tanitim",     "İllere göre işletme tanıtım videosu"),
}

BAS = "<!-- il-baglari -->"
SON = "<!-- /il-baglari -->"


def blok(kok, ek, baslik):
    iller = []
    for slug, c in SEHIR_INDEKS.items():
        if os.path.exists(os.path.join(kok, "sehir", "%s-%s.html" % (slug, ek))):
            iller.append((c["ad"], slug))
    iller.sort(key=lambda x: x[0].lower().replace("ç","c").replace("ğ","g").replace("ı","i")
                                .replace("ö","o").replace("ş","s").replace("ü","u"))
    if not iller:
        return ""
    ci = "".join('<a href="../sehir/%s-%s">%s</a>' % (slug, ek, html.escape(ad))
                 for ad, slug in iller)
    return ('%s\n<section>\n  <div class="wrap">\n'
            '    <div class="bas"><span class="no">◎</span><div><h2>%s</h2>\n'
            '      <p class="aciklama">%d ilde ayrı sayfa — her biri o ilin pazarına, '
            'ilçelerine ve coğrafyasına göre yazıldı. Diğer iller için '
            '<a href="../sehir/">il sayfalarına</a> bakın.</p></div></div>\n'
            '    <div class="iller">%s</div>\n  </div>\n</section>\n%s\n'
            % (BAS, html.escape(baslik), len(iller), ci, SON))


def calistir(kok):
    n = 0
    for ad, (ek, baslik) in ESLEME.items():
        y = os.path.join(kok, "hizmetler", ad + ".html")
        if not os.path.exists(y):
            continue
        s = io.open(y, encoding="utf-8").read()
        s = re.sub(re.escape(BAS) + r"[\s\S]*?" + re.escape(SON) + r"\n?", "", s)
        b = blok(kok, ek, baslik)
        if not b:
            continue
        if '<section class="cta">' in s:
            s = s.replace('<section class="cta">', b + '<section class="cta">', 1)
        else:
            s = s.replace("</main>", b + "</main>", 1)
        io.open(y, "w", encoding="utf-8").write(s)
        n += 1
    return {"guncellenen_hizmet_sayfasi": n}


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from pusula.ayarlar import SITE_KOK
    print(calistir(SITE_KOK))
