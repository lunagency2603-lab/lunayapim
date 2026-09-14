# -*- coding: utf-8 -*-
"""
İNDEKS DENETİMİ — Google'ın sitemizi nasıl gördüğünü defterleyen ve
indekslenmeyi ENGELLEYEBİLECEK repo tarafı sebepleri her turda arayan modül.

İki parça:
  1) SC_KAYIT — Search Console'dan ELLE okunan, tarihli sayılar. API bağlı
     değil; o yüzden her satırın yanında okunduğu tarih var. Rakamı
     güzelleştirmiyoruz, ne görüldüyse o yazıyor.
  2) repo_denetimi() — internet gerektirmeyen, kaynak dosyalardan bakılan
     kontroller. Amaç: "Google neden indekslemiyor" sorusunun BİZDEN
     kaynaklanan cevaplarını (hayalet adres, uzantılı bağlantı, site
     haritası tutarsızlığı, robots kapsamı) aynı gün yakalamak.

Kullanım:  python3 -m pusula.indeks        (ya da  pusula indeks)
"""
import io, json, os, re, datetime

from .ayarlar import KOK_DIZIN, SITE_KOK

KOK = "https://lunayapim.com"
KAYIT_DOSYA = os.path.join(KOK_DIZIN, "veri", "indeks-kayit.json")

# ------------------------------------------------------------------ 1) Search Console defteri
# (tarih, indeksli, indekssiz, {sebep: adet}, not)
SC_KAYIT = [
 {"tarih": "2026-08-31", "indeksli": 27, "indekssiz": 63, "sebep": {},
  "not": "Site haritası 5 Temmuz'dan beri okunmamıştı; yeniden gönderildi."},
 {"tarih": "2026-09-03", "indeksli": 195, "indekssiz": None, "sebep": {},
  "not": "Site haritası okundu, keşfedilen sayfa 365."},
 {"tarih": "2026-09-14", "indeksli": 266, "indekssiz": 398,
  "sebep": {
    "Yönlendirmeli sayfa (eski .html adresleri)": 187,
    "Kanonik etiketi doğru olan alternatif sayfa (/api/ hayalet adresleri)": 36,
    "robots.txt ile engellendi": 2,
    "Tarandı - şu an indekslenmedi": 17,
    "Keşfedildi - şu an indekslenmedi": 156,
  },
  "not": ("Site haritasında 460 adres var, 266'sı dizinde. Engelleyici teknik hata YOK: "
          "187 yönlendirme eski uzantılı adreslerin temiz adrese taşınması (istenen davranış), "
          "36 hayalet /api/ adresi artık robots ile kapalı. Gerçek darboğaz 156 sayfanın "
          "keşfedildiği hâlde henüz TARANMAMASI — tarama bütçesi, sayfa yaşı ve dış bağlantı yokluğu."),
  },
]


def son_kayit():
    d = list(SC_KAYIT)
    try:
        if os.path.exists(KAYIT_DOSYA):
            d += json.load(io.open(KAYIT_DOSYA, encoding="utf-8"))
    except Exception:
        pass
    d.sort(key=lambda k: k.get("tarih", ""))
    return d[-1] if d else {}


def kayit_ekle(indeksli, indekssiz=None, sebep=None, not_=""):
    """Search Console'dan okunan yeni bir ölçümü deftere yazar."""
    try:
        eski = json.load(io.open(KAYIT_DOSYA, encoding="utf-8")) if os.path.exists(KAYIT_DOSYA) else []
    except Exception:
        eski = []
    eski.append({"tarih": datetime.date.today().isoformat(), "indeksli": indeksli,
                 "indekssiz": indekssiz, "sebep": sebep or {}, "not": not_})
    os.makedirs(os.path.dirname(KAYIT_DOSYA), exist_ok=True)
    json.dump(eski[-200:], io.open(KAYIT_DOSYA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return eski[-1]


# ------------------------------------------------------------------ 2) repo tarafı kontroller
YOKSAY = ("404.html", "admin.html")          # bilerek site haritası dışında
ATLA_DIZIN = ("/assets", "/functions", "/.git", "/node_modules", "/veri")


def _site_sayfalari():
    out = []
    for r, d, f in os.walk(SITE_KOK):
        rel = r.replace(SITE_KOK, "")
        if any(rel.startswith(a) or ("/" + a.strip("/")) in rel for a in ATLA_DIZIN):
            continue
        for n in f:
            if n.endswith(".html"):
                out.append(os.path.join(r, n).replace(SITE_KOK, "").lstrip("/"))
    return sorted(out)


def _sitemap_yollari():
    p = os.path.join(SITE_KOK, "sitemap.xml")
    if not os.path.exists(p):
        return [], []
    s = io.open(p, encoding="utf-8").read()
    urls = re.findall(r"<loc>([^<]+)</loc>", s)
    yollar = []
    for u in urls:
        y = u.replace(KOK, "").lstrip("/")
        yollar.append((y + "index.html") if (y == "" or y.endswith("/")) else (y + ".html"))
    return urls, yollar


def repo_denetimi():
    """Dönen liste: (seviye, kod, mesaj). seviye: HATA | UYARI | TAMAM"""
    b = []
    def hata(k, m): b.append(("HATA", k, m))
    def uyari(k, m): b.append(("UYARI", k, m))
    def tamam(k, m): b.append(("TAMAM", k, m))

    urls, yollar = _sitemap_yollari()
    sayfalar = _site_sayfalari()

    # a) site haritası ↔ disk eşleşmesi
    if not urls:
        hata("sitemap_yok", "sitemap.xml bulunamadı")
    else:
        eksik = [u for u, y in zip(urls, yollar) if not os.path.exists(os.path.join(SITE_KOK, y))]
        if eksik:
            hata("sitemap_olu_adres", "site haritasında dosyası olmayan %d adres (ilk: %s)" % (len(eksik), eksik[0]))
        else:
            tamam("sitemap_esles", "site haritasındaki %d adresin hepsinin dosyası var" % len(urls))
        disarda = [s for s in sayfalar if s not in set(yollar) and os.path.basename(s) not in YOKSAY]
        if disarda:
            uyari("sitemap_disi", "site haritasında olmayan %d sayfa (ilk: %s)" % (len(disarda), disarda[0]))
        else:
            tamam("sitemap_kapsam", "bilerek dışarıda bırakılanlar hariç her sayfa haritada")

    # b) canonical uzantısız mı — uzantılı canonical = Google'a ikinci bir adres göstermek
    uzantili, canonicalsiz = [], []
    ic_html_bag = []
    ayni_koken_api = set()
    for s in sayfalar:
        try:
            g = io.open(os.path.join(SITE_KOK, s), encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        m = re.search(r'rel="canonical"\s+href="([^"]+)"', g)
        kapali = ("noindex" in g[:4000]) or (os.path.basename(s) in YOKSAY)
        if not m and not kapali:
            canonicalsiz.append(s)
        elif m and m.group(1).endswith(".html"):
            uzantili.append(s)
        # çapa/sorgu ekli olanlar da sayılır: index.html#urunler de yönlendirme üretir
        for h in re.findall(r'href="([^"]*\.html(?:[#?][^"]*)?)"', g):
            if not h.startswith("http") and not h.startswith("//"):
                ic_html_bag.append((s, h))
        for a in re.findall(r'["\'](/api/[a-z0-9_\-]+)', g):
            ayni_koken_api.add(a)

    if canonicalsiz:
        hata("canonical_yok", "%d sayfada canonical yok (ilk: %s)" % (len(canonicalsiz), canonicalsiz[0]))
    if uzantili:
        hata("canonical_uzantili", "%d sayfanın canonical'ı .html ile bitiyor (ilk: %s)" % (len(uzantili), uzantili[0]))
    if not canonicalsiz and not uzantili:
        tamam("canonical", "%d sayfanın canonical'ı uzantısız ve tam" % len(sayfalar))

    if ic_html_bag:
        uyari("ic_uzantili_bag", "%d iç bağlantı hâlâ .html adresine gidiyor (ilk: %s → %s)"
              % (len(ic_html_bag), ic_html_bag[0][0], ic_html_bag[0][1]))
    else:
        tamam("ic_bag", "site içinde .html'e giden bağlantı yok — yönlendirme üretmiyoruz")

    # c) JS içinde aynı kökene /api/ çağrısı var ama Function'ı yok
    #    (Google bu dizeleri adres sanıp tarıyor — /api/vitrin böyle keşfedildi)
    fn = set()
    fdiz = os.path.join(SITE_KOK, "functions", "api")
    if os.path.isdir(fdiz):
        fn = {"/api/" + n[:-3] for n in os.listdir(fdiz) if n.endswith(".js")}
    hayalet = sorted(a for a in ayni_koken_api if a not in fn)
    robots = ""
    rp = os.path.join(SITE_KOK, "robots.txt")
    if os.path.exists(rp):
        robots = io.open(rp, encoding="utf-8").read()
    if hayalet and "Disallow: /api/" not in robots:
        hata("hayalet_api", "karşılığı olmayan /api/ adresleri sayfada geçiyor ve robots kapatmıyor: %s" % ", ".join(hayalet))
    elif hayalet:
        tamam("hayalet_api", "karşılıksız /api/ adresleri var (%s) ama robots.txt taramayı kapatıyor" % ", ".join(hayalet))

    # d) robots kapsamı
    for gerek in ("Disallow: /admin", "Disallow: /api/", "Sitemap: "):
        if gerek not in robots:
            uyari("robots_eksik", "robots.txt'te '%s' satırı yok" % gerek.strip())

    # e) site haritasında noindex sayfa
    noindex = []
    for u, y in zip(urls, yollar):
        p = os.path.join(SITE_KOK, y)
        if os.path.exists(p):
            g = io.open(p, encoding="utf-8", errors="ignore").read(4000)
            if "noindex" in g:
                noindex.append(u)
    if noindex:
        hata("sitemap_noindex", "site haritasında noindex'li %d adres (ilk: %s)" % (len(noindex), noindex[0]))
    else:
        tamam("noindex", "site haritasında noindex'li adres yok")

    return b


def ozet():
    b = repo_denetimi()
    sk = son_kayit()
    urls, _ = _sitemap_yollari()
    hata = [x for x in b if x[0] == "HATA"]
    uyari = [x for x in b if x[0] == "UYARI"]
    kapsam = None
    if sk.get("indeksli") and urls:
        kapsam = round(100.0 * sk["indeksli"] / len(urls), 1)
    return {"bulgu": b, "hata": len(hata), "uyari": len(uyari), "sitemap": len(urls),
            "sc": sk, "kapsam": kapsam,
            "sorunlar": ["indeks: %s" % m for _, _, m in hata]}


def yazdir():
    o = ozet()
    print("İNDEKS DENETİMİ — %s" % datetime.datetime.now().strftime("%d.%m.%Y %H:%M"))
    print("Site haritası: %d adres" % o["sitemap"])
    sk = o["sc"]
    if sk:
        print("Search Console (%s): dizinde %s, dizin dışı %s%s" % (
            sk.get("tarih"), sk.get("indeksli"), sk.get("indekssiz"),
            (" — kapsam %%%s" % o["kapsam"]) if o["kapsam"] else ""))
        for s, a in (sk.get("sebep") or {}).items():
            print("   · %-62s %s" % (s, a))
    print("-" * 72)
    for sev, kod, m in o["bulgu"]:
        print("%-5s %-22s %s" % (sev, kod, m))
    print("-" * 72)
    print("HATA: %d | UYARI: %d" % (o["hata"], o["uyari"]))
    return o


if __name__ == "__main__":
    yazdir()
