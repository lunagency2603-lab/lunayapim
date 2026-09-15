# -*- coding: utf-8 -*-
"""
Eksik tespitinin DOĞRULUK KAPISI.

Sorun: derin.py ve tespit.py bulgularını sunucudan gelen ham HTML'den çıkarıyor.
Site JavaScript ile çiziliyorsa (Wix, Squarespace, React/Vue/Angular tek sayfa
uygulaması) ham HTML boş bir kabuktur. O zaman "WhatsApp yok, form yok, referans
yok, H1 yok" gibi onlarca bulgu YANLIŞ düşer. Bu raporu firmaya gönderirsek
firma kendi sitesini açar, hepsini yerinde görür ve bize bir daha inanmaz.

Bu modül üç şey yapar:
  1. Sayfanın sunucuda mı istemcide mi çizildiğini tespit eder.
  2. Her eksik koduna kesinlik verir: kesin / muhtemel / doğrulanamadı.
  3. Teklife yalnızca KESİN bulguların girmesini sağlar.

Hiçbir bulguyu uydurmaz; emin olamadığını eksik saymaz, ayrı listeye koyar.
"""
import re

# ---------------------------------------------------------------- render tespiti

# Ham HTML'de görülürse sayfanın gövdesi tarayıcıda çiziliyor demektir.
ISTEMCI_IMZA = (
    ('<div id="root"></div>',        "React kök düğümü boş"),
    ("<div id=\"root\"></div>",      "React kök düğümü boş"),
    ('<div id="app"></div>',         "Vue kök düğümü boş"),
    ("data-reactroot",               "React"),
    ("ng-app",                       "AngularJS"),
    ("ng-version=",                  "Angular"),
    ("__NEXT_DATA__",                "Next.js"),
    ("__NUXT__",                     "Nuxt"),
    ("wix-warmup-data",              "Wix"),
    ("_wixCssImports",               "Wix"),
    ("static.parastorage.com",       "Wix"),
    ("Static.SQUARESPACE_CONTEXT",   "Squarespace"),
    ("window.__INITIAL_STATE__",     "istemci tarafı durum aktarımı"),
    ("id=\"__nuxt\"",                "Nuxt"),
    ("data-svelte",                  "Svelte"),
)

# Sunucuda kabuk basıp içeriğin bir kısmını tarayıcıda dolduran çatılar
# (Lovable/TanStack Start, Remix vb.). Ham HTML'de metin bol görünse de
# iletişim/menü gibi bloklar sonradan gelir → en az "karma" sayılır.
# 15.09.2026 mugellocafe.com: ham HTML'de adres/harita/menü yoktu, tarayıcıda vardı.
KARMA_IMZA = (
    ("$tsr-stream-barrier",          "TanStack Start"),
    ("__tsr_router__",               "TanStack Router"),
    ("window.__remixcontext",        "Remix"),
    (".supabase.co/rest/v1",         "Supabase istemci sorgusu"),
    ("/__l5e/",                      "Lovable"),
)

# Bu kodlar sayfanın nasıl çizildiğinden BAĞIMSIZ olarak doğrulanabilir:
# HTTP katmanı, dosya varlığı, harita profili verisi, ölçülen performans.
KESIN_KODLAR = {
    "site_yok", "site_bozuk", "https_yok", "sertifika_gecersiz",
    "yavas", "robots_yok", "sitemap_yok", "agir_sayfa",
    "gorsel_az", "yorum_az", "puan_dusuk", "telefon_yok", "adres_yok",
}

# <head> içinde duran etiketler. Wix/Squarespace bunları sunucuda basar, saf
# React uygulamaları basmaz ama Google JS çalıştırıp görebilir → "muhtemel".
BAS_KODLARI = {
    "baslik_zayif", "aciklama_yok", "canonical_yok", "og_yok",
    "favicon_yok", "dil_etiketi_yok", "mobil_uyumsuz",
}


def _gorunur_metin(govde):
    g = re.sub(r"<(script|style|noscript|svg|template)[^>]*>.*?</\1>", " ",
               govde or "", flags=re.S | re.I)
    g = re.sub(r"<[^>]+>", " ", g)
    g = re.sub(r"&[a-z]+;|&#\d+;", " ", g)
    return re.sub(r"\s+", " ", g).strip()


def render_tipi(govde):
    """
    Döner: {"tip": sunucu|karma|istemci, "imza": [...], "kelime": n, "oran": 0-1}

    tip="istemci" → gövde bulguları GÜVENİLMEZ.
    tip="karma"   → imza var ama metin de var; bulgular muhtemel.
    tip="sunucu"  → ham HTML gerçek içeriği taşıyor; bulgular kesin.
    """
    d = {"tip": "sunucu", "imza": [], "kelime": 0, "oran": 0.0}
    if not govde:
        d["tip"] = "istemci"
        d["imza"] = ["gövde boş"]
        return d
    alt = govde.lower()
    for iz, ad in ISTEMCI_IMZA:
        if iz.lower() in alt and ad not in d["imza"]:
            d["imza"].append(ad)
    metin = _gorunur_metin(govde)
    d["kelime"] = len(metin.split())
    d["oran"] = round(len(metin) / max(1, len(govde)), 4)

    # Karar: az metin + imza → istemci. Bol metin → imza olsa da sunucu basmış.
    if d["kelime"] < 60:
        d["tip"] = "istemci"
    elif d["imza"] and d["kelime"] < 250:
        d["tip"] = "istemci"
    elif d["imza"]:
        d["tip"] = "karma"
    if d["tip"] == "sunucu":
        karma = [ad for iz, ad in KARMA_IMZA if iz in alt]
        if karma:
            d["imza"] += karma
            d["tip"] = "karma"
    return d


def kesinlik(kod, render):
    """Bir eksik kodunun bu sayfada ne kadar güvenilir olduğunu söyler."""
    if kod in KESIN_KODLAR:
        return "kesin"
    tip = (render or {}).get("tip", "sunucu")
    if tip == "sunucu":
        return "kesin"
    if tip == "karma":
        return "kesin" if kod in BAS_KODLARI else "muhtemel"
    # istemci
    return "muhtemel" if kod in BAS_KODLARI else "dogrulanamadi"


ACIKLAMA = {
    "kesin": "Sunucudan gelen sayfada doğrudan ölçüldü.",
    "muhtemel": "Ham sayfada görünmüyor; tarayıcıda sonradan eklenmiş olabilir. "
                "Teklife koymadan önce siteyi elle açıp bakılmalı.",
    "dogrulanamadi": "Site içeriğini tarayıcıda çiziyor. Ham sayfadan okunamadı — "
                     "eksik SAYILMADI.",
}


def suz(eksikler, kanit, render):
    """
    Eksik listesini kesinliğe göre üçe ayırır ve her kanıta kesinlik damgası basar.
    Döner: {"kesin": [...], "muhtemel": [...], "dogrulanamadi": [...]}
    """
    kova = {"kesin": [], "muhtemel": [], "dogrulanamadi": []}
    for kod in eksikler:
        k = kesinlik(kod, render)
        kova[k].append(kod)
        if kod in (kanit or {}):
            kanit[kod]["kesinlik"] = k
            kanit[kod]["kesinlik_notu"] = ACIKLAMA[k]
    for a in kova:
        kova[a] = sorted(set(kova[a]))
    return kova


# ---------------------------------------------------------------- tamamlayıcı okumalar
# Ham HTML'den okunabilen ama tespit.py'nin kaçırdığı işaretler.
# Bunlar YANLIŞ POZİTİFİ azaltır: "yok" demeden önce ikinci kez bakar.

MIKROVERI = re.compile(r'itemtype\s*=\s*["\']https?://schema\.org/', re.I)
RDFA = re.compile(r'typeof\s*=\s*["\'](?:schema:)?(?:LocalBusiness|Organization)', re.I)

VIDEO_EK = ("youtube.com/watch", "youtube-nocookie.com", "youtube.com/shorts",
            "vimeo.com/", "data-src", "video/mp4", "jwplayer", "brightcove",
            "cloudflarestream", "iframe.mediadelivery", "streamable.com")

SOSYAL_EK = ("youtube.com/@", "youtube.com/channel", "youtube.com/c/",
             "pinterest.com/", "wa.me/", "t.me/", "behance.net/", "vimeo.com/")


def sema_var_mi(govde):
    """JSON-LD dışındaki şema biçimlerini de sayar (mikroveri, RDFa)."""
    if not govde:
        return False
    return bool(MIKROVERI.search(govde) or RDFA.search(govde))


def video_var_mi(govde):
    if not govde:
        return False
    alt = govde.lower()
    return any(i in alt for i in VIDEO_EK)


def sosyal_ek(govde):
    if not govde:
        return []
    alt = govde.lower()
    return sorted({i for i in SOSYAL_EK if i in alt})


def ozet(render, kova):
    """Rapora yazılacak tek cümlelik durum."""
    tip = render.get("tip")
    if tip == "sunucu":
        return "Site sunucudan tam sayfa gönderiyor; bulguların tamamı doğrudan ölçüldü."
    imza = ", ".join(render.get("imza") or []) or "içerik JS ile yükleniyor"
    if tip == "karma":
        return ("Site kısmen tarayıcıda çiziliyor (%s). Gövde bulguları ikinci "
                "kontrolden geçirildi." % imza)
    return ("Site içeriğini tarayıcıda çiziyor (%s). Ham sayfadan okunamayan %d başlık "
            "eksik SAYILMADI — yalnızca doğrudan ölçülen %d bulgu raporlandı."
            % (imza, len(kova["dogrulanamadi"]), len(kova["kesin"])))
