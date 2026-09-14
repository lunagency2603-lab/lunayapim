# -*- coding: utf-8 -*-
"""sitemap.xml + robots.txt üretici."""
import os, glob, datetime
KOK = "https://lunayapim.com"
SITE = os.path.expanduser("~/Documents/GitHub/lunayapim")
if not os.path.isdir(SITE):
    SITE = os.path.expanduser("~/mnt/Documents/GitHub/lunayapim")

ONCELIK = {"index.html":"1.0","hizmetler/index.html":"0.9","sehir/index.html":"0.9",
           "isler.html":"0.9","yazilim.html":"0.9","iletisim.html":"0.8","blog/index.html":"0.8",
           "matrix.html":"0.7","kosullar.html":"0.4"}

def uret(bugun=None):
    bugun = bugun or datetime.date.today().strftime("%Y-%m-%d")
    eski = os.getcwd(); os.chdir(SITE)
    satir = []
    def ekle(u, p, f="monthly"):
        satir.append('  <url><loc>%s</loc><lastmod>%s</lastmod><changefreq>%s</changefreq><priority>%s</priority></url>'
                     % (u, bugun, f, p))
    ekle(KOK + "/", "1.0", "weekly")
    for f in ["yazilim.html","isler.html","iletisim.html","matrix.html","kosullar.html"]:
        ekle("%s/%s" % (KOK, f), ONCELIK.get(f, "0.7"))
    ekle(KOK + "/hizmetler/", "0.9")
    for f in sorted(glob.glob("hizmetler/*.html")):
        if f.endswith("index.html"): continue
        ekle("%s/%s" % (KOK, f), "0.9")
    ekle(KOK + "/sehir/", "0.9")
    il_ana, il_hiz = [], []
    for f in sorted(glob.glob("sehir/*.html")):
        b = os.path.basename(f)
        if b == "index.html": continue
        (il_hiz if "-" in b else il_ana).append(f)
    for f in il_ana: ekle("%s/%s" % (KOK, f), "0.8")
    for f in il_hiz: ekle("%s/%s" % (KOK, f), "0.7")
    ekle(KOK + "/blog/", "0.8")
    for f in sorted(glob.glob("blog/*.html")):
        if f.endswith("index.html"): continue
        ekle("%s/%s" % (KOK, f), "0.6")

    open("sitemap.xml","w",encoding="utf-8").write(
      '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s\n</urlset>\n'
      % "\n".join(satir))
    open("robots.txt","w",encoding="utf-8").write(
"""User-agent: *
Allow: /
Disallow: /kda.db

Sitemap: https://lunayapim.com/sitemap.xml
""")
    os.chdir(eski)
    return len(satir)

if __name__ == "__main__":
    print("sitemap.xml:", uret(), "URL")
