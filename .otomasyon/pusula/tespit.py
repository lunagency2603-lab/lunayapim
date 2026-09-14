# -*- coding: utf-8 -*-
"""
Eksik tespiti — bir işletmenin dijital görünürlüğünde NE EKSİK, onu bulur.
Sadece kamuya açık bilgiye bakar: web sitesinin kendisi ve harita profili verisi.
"""
import re, json
from .kaynaklar.agir import getir, json_getir
from .ayarlar import ESIK
from . import ayarlar
from . import derin as DR
from . import dogrulama as DG

VIDEO_IZLERI = ("youtube.com/embed", "youtu.be/", "player.vimeo", "<video",
                "wistia", "dailymotion", ".mp4")
SOSYAL_IZLERI = ("instagram.com", "facebook.com", "linkedin.com", "tiktok.com", "x.com/", "twitter.com")

def _site_normalize(u):
    if not u: return None
    u = u.strip()
    if not u.startswith("http"): u = "https://" + u
    return u

def site_denetle(url):
    """Web sitesini indirip yapısal eksikleri çıkarır."""
    d = {"site_url": url, "ulasildi": False, "https": False, "durum": 0,
         "baslik": "", "aciklama": "", "sema": False, "viewport": False,
         "video": False, "sosyal": [], "h1": 0, "boyut_kb": 0, "og": False,
         "render": None, "sertifika": None}
    url = _site_normalize(url)
    if not url: return d
    kod, govde, son = getir(url, dogrula_ssl=True)
    d["sertifika"] = "gecerli" if kod else None
    if kod == 0:
        kod, govde, son = getir(url, dogrula_ssl=False)
        if kod:
            # doğrulamasız istekle açıldı → sertifika zinciri bozuk
            d["sertifika"] = "gecersiz"
    d["durum"] = kod
    if kod == 0 or kod >= 400 or not govde:
        return d
    d["ulasildi"] = True
    d["https"] = son.startswith("https://")
    d["boyut_kb"] = round(len(govde.encode("utf-8", "ignore")) / 1024, 1)
    alt = govde.lower()

    m = re.search(r"<title[^>]*>(.*?)</title>", govde, re.S | re.I)
    if m: d["baslik"] = re.sub(r"\s+", " ", m.group(1)).strip()[:200]
    m = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', govde, re.S | re.I)
    if m: d["aciklama"] = re.sub(r"\s+", " ", m.group(1)).strip()[:400]

    d["viewport"] = 'name="viewport"' in alt or "name='viewport'" in alt
    d["og"] = 'property="og:' in alt
    d["h1"] = len(re.findall(r"<h1[\s>]", alt))
    d["render"] = DG.render_tipi(govde)
    d["video"] = any(i in alt for i in VIDEO_IZLERI) or DG.video_var_mi(govde)
    d["sosyal"] = sorted({s for s in SOSYAL_IZLERI if s in alt} | set(DG.sosyal_ek(govde)))

    for blok in re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', govde, re.S | re.I):
        try:
            v = json.loads(blok)
        except Exception:
            continue
        metin = json.dumps(v, ensure_ascii=False)
        if any(t in metin for t in ("LocalBusiness", "Organization", "RealEstateAgent",
                                    "HomeAndConstructionBusiness", "Store", "Restaurant")):
            d["sema"] = True
    if not d["sema"] and DG.sema_var_mi(govde):
        d["sema"] = True
    return d

def pagespeed(url, strateji="mobile"):
    """PageSpeed Insights skoru (0-100). Ulaşılamazsa None."""
    if not url: return None
    u = ("https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
         "?url=%s&strategy=%s&category=performance" % (url, strateji))
    if ayarlar.PAGESPEED_ANAHTAR: u += "&key=" + ayarlar.PAGESPEED_ANAHTAR
    y = json_getir(u)
    try:
        return int(round(y["lighthouseResult"]["categories"]["performance"]["score"] * 100))
    except Exception:
        return None

def eksikleri_bul(aday, hizli=False):
    """
    aday: adaylar tablosundan bir satır (dict benzeri).
    döner: (eksik_kodlari, detay_sozlugu)
    detay["kanit"] her eksik için: ne kontrol edildi, ne bulundu, hangi kaynakta, ne zaman.
    """
    import datetime
    zaman = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    eksik, detay = [], {}
    kanit = {}

    def kaydet(kod, kontrol, bulgu, kaynak):
        eksik.append(kod)
        kanit[kod] = {"kontrol": kontrol, "bulgu": bulgu, "kaynak": kaynak, "zaman": zaman}

    site = (aday["site"] or "").strip() if isinstance(aday, dict) or hasattr(aday, "keys") else ""

    harita = "Google/harita işletme profili"
    if not site:
        kaydet("site_yok", "Harita profilinde ve aramada web sitesi alanı",
               "Kayıtlı web sitesi bulunamadı", harita)
        kaydet("video_yok", "Web sitesi ve profilde gömülü video",
               "Site olmadığı için gösterilecek video da yok", harita)
        detay["site"] = {"site_url": None, "ulasildi": False}
    else:
        s = site_denetle(site)
        detay["site"] = s
        kaynak = s.get("site_url") or site
        if not s["ulasildi"]:
            kaydet("site_bozuk", "Siteye HTTP isteği",
                   "Sunucu yanıt vermedi (durum kodu %s)" % (s["durum"] or "bağlantı yok"), kaynak)
        else:
            if s.get("sertifika") == "gecersiz":
                kaydet("sertifika_gecersiz", "SSL sertifikası doğrulaması",
                       "Site yalnızca sertifika doğrulaması kapatıldığında açılıyor — "
                       "tarayıcı ziyaretçiye \u201cbağlantınız gizli değil\u201d uyarısı gösteriyor",
                       kaynak)
            if not s["https"]:
                kaydet("https_yok", "Adresin HTTPS'e yönlenmesi",
                       "Site http:// üzerinden açılıyor, güvenli bağlantıya yönlenmiyor", kaynak)
            if not s["viewport"]:
                kaydet("mobil_uyumsuz", "Kaynak kodda <meta name=\"viewport\">",
                       "Viewport etiketi yok — mobilde masaüstü düzeni açılıyor", kaynak)
            b = s["baslik"]
            if not b or len(b) < 15 or b.lower() in ("ana sayfa", "home", "anasayfa", "index"):
                kaydet("baslik_zayif", "<title> etiketi",
                       ("Başlık boş" if not b else "Başlık: %r (%d karakter — arama sonucunda ne "
                        "sattığını anlatmıyor)" % (b[:60], len(b))), kaynak)
            if not s["aciklama"]:
                kaydet("aciklama_yok", "<meta name=\"description\">",
                       "Açıklama etiketi yok — Google arama sonucunda metni kendi uyduruyor", kaynak)
            if not s["sema"]:
                kaydet("sema_yok", "JSON-LD LocalBusiness/Organization şeması",
                       "İşletme şeması yok — arama motoru adres, telefon ve çalışma saatini "
                       "yapısal olarak okuyamıyor", kaynak)
            if not s["video"]:
                kaydet("video_yok", "Sayfada YouTube/Vimeo/mp4 gömülü video",
                       "Hiç video bulunamadı", kaynak)
            if not s["sosyal"]:
                kaydet("sosyal_yok", "Sayfadaki sosyal medya bağlantıları",
                       "Instagram/Facebook/LinkedIn bağlantısı bulunamadı", kaynak)
            # --- derin katman: dönüşüm, güven, içerik, teknik
            try:
                ds = DR.incele(_site_normalize(site))
                detay["derin"] = ds
                for e in DR.eksikler(ds):
                    kaydet(e["kod"], e["kontrol"], e["bulgu"], e["kaynak"])
            except Exception as ex:
                detay["derin_hata"] = "%s: %s" % (type(ex).__name__, ex)

            if not hizli:
                ps = pagespeed(_site_normalize(site))
                detay["pagespeed_mobil"] = ps
                if ps is not None and ps < ESIK["pagespeed_yavas"]:
                    kaydet("yavas", "Google PageSpeed Insights (mobil)",
                           "Mobil performans skoru %d/100 (eşik %d)" % (ps, ESIK["pagespeed_yavas"]),
                           "PageSpeed Insights")

    foto = aday["fotograf_sayisi"] or 0
    yorum = aday["yorum_sayisi"] or 0
    puan = aday["puan"]
    if foto < ESIK["gorsel_az"]:
        kaydet("gorsel_az", "Harita profilindeki fotoğraf sayısı",
               "%d fotoğraf var (eşik %d)" % (foto, ESIK["gorsel_az"]), harita)
    if yorum < ESIK["yorum_az"]:
        kaydet("yorum_az", "Harita profilindeki yorum sayısı",
               "%d yorum var (eşik %d)" % (yorum, ESIK["yorum_az"]), harita)
    if puan is not None and puan < ESIK["puan_dusuk"]:
        kaydet("puan_dusuk", "Harita profilindeki ortalama puan",
               "%.1f puan (eşik %.1f)" % (puan, ESIK["puan_dusuk"]), harita)
    if not (aday["telefon"] or "").strip():
        kaydet("telefon_yok", "Profildeki telefon alanı", "Telefon numarası kayıtlı değil", harita)
    if not (aday["adres"] or "").strip():
        kaydet("adres_yok", "Profildeki adres alanı", "Adres kayıtlı değil", harita)

    detay["profil"] = {"fotograf": foto, "yorum": yorum, "puan": puan}
    detay["kanit"] = kanit
    detay["denetim_zamani"] = zaman

    # --- DOĞRULUK KAPISI ---------------------------------------------------
    # Site içeriğini tarayıcıda çiziyorsa ham HTML'den okunan gövde bulguları
    # güvenilmez. Onları eksik saymıyoruz; ayrı listeye koyuyoruz ki teklife
    # yanlış bir iddia girmesin.
    render = (detay.get("site") or {}).get("render") or {"tip": "sunucu"}
    tekil = sorted(set(eksik))
    kova = DG.suz(tekil, kanit, render)
    detay["render"] = render
    detay["kesinlik"] = kova
    detay["kesinlik_ozeti"] = DG.ozet(render, kova)
    detay["dogrulanamayan"] = kova["dogrulanamadi"]
    # Dışarıya yalnızca savunabildiğimiz bulgular çıkar.
    return kova["kesin"] + kova["muhtemel"], detay
