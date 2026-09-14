# -*- coding: utf-8 -*-
"""Teklif raporunu TEK DOSYA hâline getirir: görseller ve video içine gömülür.

Neden: teklif WhatsApp'tan ya da e-postayla tek dosya gidiyor. Görseller ayrı
dosya olarak kalırsa alıcıda kırık görünür. Gömülü hâlde her yerde açılır.
"""
import base64, os, re, sys


def veri_uri(yol, tur):
    with open(yol, "rb") as f:
        return "data:%s;base64,%s" % (tur, base64.b64encode(f.read()).decode("ascii"))


def gom(html_yolu, klasor, cikti=None):
    s = open(html_yolu, encoding="utf-8").read()

    # görseller: küçültülmüş jpg sürümü varsa onu kullan
    for ad in re.findall(r'src="([^"]+\.png)"', s):
        kucuk = os.path.join(klasor, "_g_" + ad.replace(".png", ".jpg"))
        tam = kucuk if os.path.exists(kucuk) else os.path.join(klasor, ad)
        if not os.path.exists(tam):
            continue
        tur = "image/jpeg" if tam.endswith(".jpg") else "image/png"
        s = s.replace('src="%s"' % ad, 'src="%s"' % veri_uri(tam, tur))

    # video: küçük sürüm varsa onu göm
    for ad in re.findall(r'src="([^"]+\.mp4)"', s):
        kucuk = os.path.join(klasor, "_kucuk.mp4")
        tam = kucuk if os.path.exists(kucuk) else os.path.join(klasor, ad)
        if not os.path.exists(tam):
            continue
        s = s.replace('src="%s"' % ad, 'src="%s"' % veri_uri(tam, "video/mp4"))

    # poster niteliği de gömülsün
    for ad in re.findall(r'poster="([^"]+\.png)"', s):
        kucuk = os.path.join(klasor, "_g_" + ad.replace(".png", ".jpg"))
        tam = kucuk if os.path.exists(kucuk) else os.path.join(klasor, ad)
        if os.path.exists(tam):
            tur = "image/jpeg" if tam.endswith(".jpg") else "image/png"
            s = s.replace('poster="%s"' % ad, 'poster="%s"' % veri_uri(tam, tur))

    cikti = cikti or html_yolu.replace(".html", "-tek-dosya.html")
    open(cikti, "w", encoding="utf-8").write(s)
    return cikti, os.path.getsize(cikti)


if __name__ == "__main__":
    k = sys.argv[1] if len(sys.argv) > 1 else "."
    print(gom(os.path.join(k, "teklif.html"), k))
