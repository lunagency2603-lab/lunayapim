# -*- coding: utf-8 -*-
"""
Luna Pusula paneli — yerel admin arayüzü.
  python3 -m pusula.panel      → tarayıcıda açar (http://127.0.0.1:8765)
Sadece bu bilgisayardan erişilir; dışarı açık değildir.
Terminal gerekmez: tarama dahil tüm komutlar panelden çalışır.
"""
import json, os, re, secrets, threading, webbrowser, urllib.parse, datetime, html
from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer

from . import veritabani as vt
from . import telgraf as TG
from . import asistan_panel as AP
from . import uretim as UR
from . import ayarlar as A
from . import gorev as G
from . import akis as AK
from . import musteri as M
from . import piyasa as PY
from . import sosyal as SO
from . import arama as AR
from . import gundem as GU
from . import gundem_yayin as GY
from . import yayin as YA
from . import indexnow as IN
from . import depo as DP
from . import ziyaret as ZY
from . import saglik as SL
from . import talep as TL
from . import kilavuz as KL
from . import karargah as KG
from . import makale as MK
from . import sorgu as SG
from . import yapay_zeka as YZ
from . import ag as AG
from . import uzak as UZ
from . import iletisim as IL
from .ayarlar import SEKTORLER, CIKTI, ILLER, SITE_KOK
from .hedefkitle import HIZMETLER
from .puanlama import sicak_mi, ETIKET
from .panel_html import SAYFA

KAPI = int(os.environ.get("PUSULA_KAPI", "8765"))

# Ağ kipi: açıkken panel yerel ağa açılır ve erişim anahtarı zorunlu olur.
# Kendiliğinden açılmıyor — Panel-Ag.command ya da PUSULA_AG=1 gerekiyor.
AG_KIPI = os.environ.get("PUSULA_AG", "").strip() in ("1", "acik", "açık", "true")

# Tünel kipi: panel Cloudflare üzerinden internete açık. Tünel açıkken
# "bu bilgisayar serbest" muafiyeti KALKAR — tünelin trafiği de localhost'tan
# geldiği için o muafiyet bırakılsa bütün internet serbest kalırdı.
UZAK_KIPI = os.environ.get("PUSULA_UZAK", "").strip() in ("1", "acik", "açık", "true")


# ---------------------------------------------------------------- veri
def adaylari_getir(b):
    liste = []
    for r in vt.son_denetimler(b):
        eks = json.loads(r["eksikler"])
        t = vt.son_tahmin(b, r["id"])
        td = json.loads(t["detay"]) if t else {}
        d = b.execute("SELECT dosya FROM demolar WHERE aday_id=? ORDER BY id DESC LIMIT 1", (r["id"],)).fetchone()
        tm = b.execute("SELECT durum, tarih FROM temas WHERE aday_id=? ORDER BY id DESC LIMIT 1", (r["id"],)).fetchone()
        klasor = os.path.join(M.DOSYA_KOK, "%s-%s" % (r["id"], M.slugla(r["ad"])))
        tel = IL.telefon_tipi(r["telefon"]) if r["telefon"] else None
        kanal_sayilari = dict(b.execute(
            "SELECT tur, COUNT(*) FROM kanallar WHERE aday_id=? GROUP BY tur", (r["id"],)).fetchall())
        kisi_n = b.execute("SELECT COUNT(*) FROM kisiler WHERE aday_id=?", (r["id"],)).fetchone()[0]
        liste.append({
            "id": r["id"], "ad": r["ad"], "sektor": r["sektor"],
            "sektor_ad": SEKTORLER.get(r["sektor"], {}).get("ad", r["sektor"] or ""),
            "sehir": r["sehir"] or "", "ilce": r["ilce"] or "",
            "telefon": r["telefon"] or "", "site": r["site"] or "",
            "puan": r["puan"], "yorum": r["yorum_sayisi"] or 0, "foto": r["fotograf_sayisi"] or 0,
            "skor": r["skor"], "sicak": sicak_mi(r["skor"]), "eksik": len(eks),
            "eksikler": [ETIKET.get(k, k) for k in eks],
            "ek_gelir": td.get("ek_gelir", 0),
            "demo": os.path.basename(d["dosya"]) if d else None,
            "temas": tm["durum"] if tm else None,
            "temas_tarih": (tm["tarih"][:10] if tm else None),
            "dosya": os.path.isdir(klasor),
            "durum": (r["durum"] if "durum" in r.keys() else None) or "yeni",
            "eposta": (r["eposta"] if "eposta" in r.keys() else None) or "",
            "zengin": bool(r["zengin"] if "zengin" in r.keys() else 0),
            "tel_tip": tel["tip"] if tel else None,
            # profildeki numara sabit olsa bile sitede cep hattı bulunmuş olabilir
            "wa_uygun": bool(kanal_sayilari.get("whatsapp")) or (bool(tel["wa"]) if tel else False),
            "tel_aciklama": ("sitede cep hattı bulundu — WhatsApp açık"
                             if kanal_sayilari.get("whatsapp")
                             else (tel["aciklama"] if tel else "numara yok")),
            "kisi_sayisi": kisi_n,
            "kanal_sayilari": kanal_sayilari,
            "sosyal_skor": (r["sosyal_skor"] if "sosyal_skor" in r.keys() else None),
            "sosyal_hesap": len([t for t in kanal_sayilari if t in SO.PLATFORM]),
        })
    return liste


def veri():
    b = vt.baglan()
    adaylar = adaylari_getir(b)
    isler = [dict(x) for x in b.execute("SELECT * FROM isler ORDER BY id DESC").fetchall()]
    ist = vt.istatistik(b)
    temaslar = vt.temaslar_getir(b, limit=120)
    takip = vt.takip_gerekenler(b)
    b.close()
    return {"hizmetler": HIZMETLER, "adaylar": adaylar, "isler": isler,
            "istatistik": ist, "asamalar": vt.ASAMALAR, "asama_ad": vt.ASAMA_AD,
            "durumlar": vt.DURUMLAR, "durum_ad": vt.DURUM_AD,
            "temaslar": temaslar, "takip": takip,
            "iller": ILLER,
            "sektorler": [{"anahtar": k, "ad": v["ad"], "teklif": v["teklif"]} for k, v in SEKTORLER.items()],
            "kaynak": "Google Places" if A.GOOGLE_ANAHTAR else "OpenStreetMap (anahtarsız)",
            "mesgul": G.mesgul(), "gorevler": G.durum()}


# Kimlik doğrulama kapısı izleri — bunlar 200 + HTML döner ama İÇERİK DEĞİLDİR.
# (İlk sürüm bunu kaçırdı ve Cloudflare Access giriş sayfasını "indekslenebilir
#  içerik" sanıp yanlış uyarı verdi.)
KAPI_IZLERI = (
    ("cloudflare access", "Cloudflare Access (Zero Trust) giriş kapısı"),
    ("cf-access", "Cloudflare Access"),
    ("sign in ・", "oturum açma sayfası"),
    ("sign in ·", "oturum açma sayfası"),
    ("<title>sign in", "oturum açma sayfası"),
    ("oturum aç", "oturum açma sayfası"),
    ("giriş yap", "oturum açma sayfası"),
    ("unauthorized", "yetkisiz erişim sayfası"),
    ("authentication required", "kimlik doğrulama gerekiyor"),
    ("login", "oturum açma sayfası"),
)


def _kapi_mi(k):
    """Yanıt gerçek içerik mi, yoksa bir giriş/koruma kapısı mı?"""
    metin = ((k.get("ilk") or "") + " " + (k.get("tur") or "")).lower()
    for iz, ad in KAPI_IZLERI:
        if iz in metin:
            return ad
    return None


def AR_altalan_yorum(kontrol):
    """Alt alan adının ana siteye SEO açısından zarar verip vermediğini yorumlar."""
    ana = next((k for k in kontrol if k["ad"] == "ana sayfa"), {})
    rob = next((k for k in kontrol if k["ad"] == "robots.txt"), {})
    y = []
    durum = ana.get("durum") or 0
    tur = (ana.get("tur") or "").lower()
    ilk = (ana.get("ilk") or "").lstrip().lower()
    kapi = _kapi_mi(ana)
    rob_kapi = _kapi_mi(rob)

    if durum == 0:
        y.append(("bilinmiyor", "Alt alan adına ulaşılamadı — kapalı olabilir. "
                                "Kapalıysa Google da indeksleyemez; zararsızdır."))
    elif kapi:
        y.append(("iyi",
                  "Alt alan adı %s arkasında. Gelen her istek — Googlebot dahil — giriş "
                  "sayfasını görüyor; arkadaki hiçbir içerik dışarı çıkmıyor. "
                  "Ana sitenin SEO'suna ZARARI YOK." % kapi))
        y.append(("dikkat",
                  "Tek kalan risk: giriş sayfasının kendisi 200 döndüğü için Google onu "
                  "ince bir sayfa olarak indeksleyip marka aramanda gösterebilir. "
                  "Kesin çözüm: Cloudflare → Rules → Transform Rules → Modify Response "
                  "Header → kda.lunayapim.com için 'X-Robots-Tag: noindex, nofollow' ekle. "
                  "Access'in arkasına robots.txt koyamazsın; başlık yöntemi bunu aşar."))
    elif durum >= 400:
        y.append(("iyi", "Ana sayfa %s dönüyor — Google indekslenecek sayfa bulamaz, "
                         "ana siteye etkisi yok." % durum))
    elif "html" not in tur and ("{" in ilk[:5] or "json" in tur):
        y.append(("iyi", "Ana sayfa HTML değil, API yanıtı (%s) dönüyor. Google bunu "
                         "normalde indekslemez; ana siteye zarar vermez." % tur))
    elif "html" in tur:
        y.append(("dikkat", "Alt alan adı indekslenebilir HTML sayfa dönüyor (%d bayt). "
                            "Alt alan adları Google için AYRI SİTEDİR; ana sitenin sıralamasını "
                            "doğrudan düşürmez ama marka aramasında zayıf bir sonuç olarak "
                            "çıkabilir. robots ile engelle ya da noindex ekle."
                  % ana.get("uzunluk", 0)))
    else:
        y.append(("bilgi", "Ana sayfa %s / %s döndü." % (durum, tur or "tür yok")))

    # robots.txt yorumu — kapı arkasındaysa robots.txt zaten okunamıyor demektir
    if rob_kapi:
        y.append(("bilgi", "robots.txt de giriş kapısının arkasında (%s). Bu beklenen "
                           "durumdur; Google robots.txt okuyamadığı için siteyi taramaya "
                           "çalışır, kapıya çarpar ve içeriğe ulaşamaz. Yapılacak bir şey yok — "
                           "yukarıdaki X-Robots-Tag yeterli." % rob_kapi))
    elif rob.get("durum") == 200:
        metin = (rob.get("ilk") or "").lower()
        if "disallow: /" in metin and "disallow: /a" not in metin:
            y.append(("iyi", "robots.txt tüm taramayı kapatmış — istenen davranış bu."))
        else:
            y.append(("dikkat", "robots.txt var ama taramayı kapatmıyor. API alt alan adında "
                                "'User-agent: *' + 'Disallow: /' olması en temizi."))
    elif rob.get("durum", 0) >= 400 or rob.get("durum") == 0:
        y.append(("dikkat", "robots.txt yok. API alt alan adına 'Disallow: /' içeren bir "
                            "robots.txt koymak, oraya hiç bakılmamasını garanti eder."))

    # X-Robots-Tag zaten var mı
    basliklar = {k.lower(): v for k, v in (ana.get("basliklar") or {}).items()}
    if "noindex" in (basliklar.get("x-robots-tag") or "").lower():
        y = [("iyi", "X-Robots-Tag: noindex zaten ayarlı — bu alt alan adı için "
                     "yapılacak başka bir şey yok.")] + [x for x in y if x[0] != "dikkat"]
    return y


def _aday_paketi(b, aday_id):
    r = b.execute("""SELECT a.*, d.skor, d.eksikler, d.detay FROM adaylar a
                     JOIN denetimler d ON d.id=(SELECT id FROM denetimler WHERE aday_id=a.id ORDER BY id DESC LIMIT 1)
                     WHERE a.id=?""", (aday_id,)).fetchone()
    if not r:
        return None
    aday = dict(r)
    eksikler = json.loads(r["eksikler"])
    detay = json.loads(r["detay"])
    t = vt.son_tahmin(b, aday_id)
    if t:
        tahmin = json.loads(t["detay"])
    else:
        from .tahmin import hesapla
        tahmin = hesapla(r, eksikler)
    return aday, eksikler, detay, tahmin


# ---------------------------------------------------------------- arşiv
def arsiv_uret():
    d = veri()
    yol = os.path.join(CIKTI, "pusula-arsiv-%s.html" % datetime.date.today().strftime("%Y%m%d"))
    g = """<!DOCTYPE html><html lang="tr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Luna Pusula — Arşiv %s</title><style>
body{background:#0A0A0C;color:#EFEDE8;font-family:system-ui,-apple-system,sans-serif;margin:0;padding:32px 20px}
h1{font-size:24px;margin:0 0 4px}p.a{color:#8C8A84;font-size:14px;margin:0 0 22px}
h2{font-size:18px;margin:28px 0 10px}
table{width:100%%;max-width:1200px;border-collapse:collapse;font-size:14px}
th,td{text-align:left;padding:10px 11px;border-bottom:1px solid rgba(239,237,232,.12)}
th{font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:#E8452C}
tr.s td:nth-child(3){color:#E8452C;font-weight:700}
.k{display:inline-block;border:1px solid rgba(239,237,232,.15);border-radius:3px;padding:12px 16px;margin:0 8px 8px 0}
.k b{display:block;font-size:22px}.k span{font-size:11px;color:#8C8A84;letter-spacing:.14em;text-transform:uppercase}
</style></head><body>
<h1>Luna Pusula — arşiv</h1><p class="a">%s · salt okunur anlık görüntü</p>
""" % (datetime.date.today().strftime("%d.%m.%Y"), datetime.datetime.now().strftime("%d.%m.%Y %H:%M"))
    i = d["istatistik"]
    for etk, anahtar in [("Aday", "aday"), ("Denetlenen", "denetlenen"), ("Demo", "demo"),
                         ("Temas", "temas"), ("Açık iş", "is"), ("Kazanılan", "kazanilan")]:
        g += '<div class="k"><span>%s</span><b>%s</b></div>' % (etk, i.get(anahtar, 0))
    g += '<div class="k"><span>Kazanılan ciro</span><b>%s ₺</b></div>' % "{:,}".format(int(i.get("ciro") or 0)).replace(",", ".")
    g += "<h2>Adaylar (%d)</h2><div class='tablo-kaydir'><table><tr><th>#</th><th>İşletme</th><th>Skor</th><th>Eksik</th><th>Sektör</th><th>İl</th><th>Telefon</th><th>Temas</th></tr>" % len(d["adaylar"])
    for a in d["adaylar"]:
        g += "<tr class='%s'><td>%d</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
            "s" if a["sicak"] else "", a["id"], html.escape(a["ad"]), a["skor"], a["eksik"],
            html.escape(a["sektor_ad"]), html.escape(a["sehir"]), html.escape(a["telefon"] or "—"),
            html.escape(a["temas"] or "—"))
    g += "</table></div>"
    if d["isler"]:
        g += "<h2>İşler (%d)</h2><div class='tablo-kaydir'><table><tr><th>Müşteri</th><th>Hizmet</th><th>Aşama</th><th>Bedel</th><th>Teslim</th></tr>" % len(d["isler"])
        for x in d["isler"]:
            g += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                html.escape(x["musteri"]), html.escape(HIZMETLER.get(x["hizmet"], {}).get("ad", x["hizmet"] or "")),
                vt.ASAMA_AD.get(x["asama"], x["asama"]),
                "{:,}".format(int(x["bedel"] or 0)).replace(",", ".") + " ₺" if x["bedel"] else "—",
                x["teslim_tarihi"] or "—")
        g += "</table></div>"
    g += "</body></html>"
    os.makedirs(CIKTI, exist_ok=True)
    open(yol, "w", encoding="utf-8").write(g)
    return yol


# ---------------------------------------------------------------- sunucu
class Sunucu(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def _g(self, kod, tur, govde, ikili=False, cerez=None):
        self.send_response(kod)
        self.send_header("Content-Type", tur)
        self.send_header("Cache-Control", "no-store")
        if cerez:
            self.send_header("Set-Cookie", cerez)
        v = govde if ikili else govde.encode("utf-8")
        self.send_header("Content-Length", str(len(v)))
        self.end_headers()
        try:
            self.wfile.write(v)
        except Exception:
            pass

    def _json(self, veri, kod=200):
        self._g(kod, "application/json; charset=utf-8", json.dumps(veri, ensure_ascii=False))

    # ---------------- yetki (yalnızca ağ kipinde)
    def _tunelden(self):
        return UZ.tunelden_mi(self.headers)

    def _yerelden(self):
        return (self.client_address or [""])[0] in ("127.0.0.1", "::1")

    def _yetkili(self, q=None):
        """
        Kapı kontrolü. Üç kip:
          • Hiçbiri açık değil → panel zaten dışarı kapalı, herkes serbest.
          • Ağ kipi           → bu bilgisayar serbest, dışarıdan gelen anahtar/PIN veriyor.
          • Tünel kipi        → hiç muafiyet yok. Tünelin trafiği de localhost'tan
                                geldiği için muafiyet bırakılsa internet serbest kalırdı.
        """
        if not (AG_KIPI or UZAK_KIPI):
            return True

        # Cloudflare Access arkasındaysa ve izinli e-posta ile girildiyse geçiyor.
        # Bu başlığı yalnızca Cloudflare ekleyebiliyor, o yüzden SADECE tünelden
        # gelen istekte dikkate alınıyor.
        if self._tunelden():
            eposta = UZ.access_epostasi(self.headers)
            if eposta and eposta in A.izinli_epostalar():
                return True
        elif AG_KIPI and not UZAK_KIPI and self._yerelden():
            return True

        dogru = AG.anahtar()
        gelen = ""
        if q:
            gelen = (q.get("anahtar") or [""])[0]
        if not gelen:
            gelen = AG.cerezden(self.headers.get("Cookie"))
        return bool(gelen) and secrets.compare_digest(gelen, dogru)

    def _istek_ip(self):
        """Deneme sınırı için: tünelden geliyorsa gerçek ziyaretçi adresi."""
        return ((self.headers.get("Cf-Connecting-Ip") or "").strip()
                or (self.client_address or ["?"])[0])

    def _kullanici(self, g=None):
        """İsteği kimin yaptığı — panel her yazma isteğine ekliyor."""
        ad = ""
        if isinstance(g, dict):
            ad = (g.get("_kullanici") or "").strip()
        if not ad:
            ad = (self.headers.get("X-Pusula-Kullanici") or "").strip()
        return ad[:40] or None

    # ---------------- PIN ile giriş
    def _giris(self):
        ip = self._istek_ip()
        h = AG.deneme_hakki(ip)
        if h["kalan"] <= 0:
            return self._g(429, "text/html; charset=utf-8", AG.giris_sayfasi(
                "Çok fazla yanlış deneme. %d dakika sonra tekrar dene."
                % max(1, h["bekle"] // 60)))
        try:
            n = int(self.headers.get("Content-Length") or 0)
            veri = urllib.parse.parse_qs(self.rfile.read(n).decode("utf-8"))
        except Exception:
            veri = {}
        girilen = "".join(ch for ch in (veri.get("pin") or [""])[0] if ch.isdigit())
        if girilen and secrets.compare_digest(girilen, AG.pin()):
            AG.deneme_isle(ip, True)
            self.send_response(303)
            self.send_header("Location", "/")
            self.send_header("Set-Cookie", AG.cerez_basligi(AG.anahtar()))
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        AG.deneme_isle(ip, False)
        kalan = AG.deneme_hakki(ip)["kalan"]
        return self._g(401, "text/html; charset=utf-8", AG.giris_sayfasi(
            "PIN yanlış." if girilen else "PIN girilmedi.", kalan))

    # ---------------- GET
    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        y, q = u.path, urllib.parse.parse_qs(u.query)
        if not self._yetkili(q):
            return self._g(401, "text/html; charset=utf-8", AG.giris_sayfasi())
        if y in ("/", "/index.html"):
            ek = None
            if AG_KIPI and (q.get("anahtar") or [""])[0]:
                ek = AG.cerez_basligi(AG.anahtar())   # bir kez yapıştır, tarayıcı hatırlasın
            return self._g(200, "text/html; charset=utf-8", SAYFA, cerez=ek)
        if y == "/api/sorgular":
            paket = SG.oku() or {"tarih": None, "adet": 0, "sorgular": [], "hata": []}
            return self._json({"paket": paket,
                               "yukselen": SG.yukselenler() if paket.get("sorgular") else [],
                               "gunler": SG.gunler(14),
                               "oneri": SG.konu_onerileri() if paket.get("sorgular") else []})
        if y == "/api/makaleler":
            return self._json({"konular": MK.liste()})
        if y == "/api/karargah":
            return self._json(KG.ozet())
        if y == "/api/okuma":
            """Sitedeki okuma sayacını çeker (Cloudflare Pages Function + KV)."""
            if not A.OKUMA_ANAHTAR:
                return self._json({"hata": "Okuma anahtarı girilmemiş (Ayarlar → Site tıklanmaları)."})
            from .kaynaklar.agir import getir
            import json as _j
            kod, govde, _ = getir("https://lunayapim.com/api/okuma?anahtar=%s&gun=30"
                                  % urllib.parse.quote(A.OKUMA_ANAHTAR), zaman_asimi=15)
            if kod != 200 or not govde:
                return self._json({"hata": "Sayaç cevap vermedi (HTTP %s). Cloudflare'de KV bağlaması "
                                           "ve PANEL_ANAHTARI ayarlı mı?" % kod})
            try:
                return self._json(_j.loads(govde))
            except Exception:
                return self._json({"hata": "Sayaç geçersiz cevap verdi."})
        if y == "/api/kilavuz":
            return self._json(KL.veri())
        if y == "/api/ag":
            if not AG_KIPI:
                return self._json({"acik": False, "kapi": KAPI,
                                   "pin": AG.pin_okunakli()})
            adr = AG.adresler(KAPI)
            return self._json({"acik": True, "kapi": KAPI, "adresler": adr,
                               "adres": adr[0]["url"], "ip": AG.yerel_ip(),
                               "ag_var": AG.ag_var_mi(),
                               "pin": AG.pin_okunakli()})
        if y == "/api/veri":
            return self._json(veri())
        if y == "/api/gorevler":
            return self._json(G.durum())
        if y == "/api/gorev":
            g = G.durum(q.get("id", ["0"])[0], int(q.get("from", ["0"])[0]))
            return self._json(g or {"hata": "görev yok"}, 200 if g else 404)
        if y == "/api/piyasa":
            hz = q.get("hizmet", [None])[0]
            sh = q.get("sehir", [None])[0]
            b = vt.baglan()
            if hz:
                d = PY.referans(hz, sh, b)
            else:
                d = {k: PY.referans(k, sh, b) for k in PY.PIYASA}
            rk = [dict(r) for r in b.execute(
                "SELECT * FROM rakip_teklif ORDER BY id DESC LIMIT 60").fetchall()]
            b.close()
            return self._json({"referans": d, "rakip": rk,
                               "kaynaklar": PY.KAYNAKLAR, "derleme": PY.DERLEME_TARIHI})
        if y == "/api/aday":
            b = vt.baglan()
            p = _aday_paketi(b, int(q.get("id", ["0"])[0]))
            if not p:
                b.close(); return self._json({"hata": "aday yok"}, 404)
            aday, eksikler, detay, tahmin = p
            anahtar = M.hizmet_anahtari(aday)
            d = {
              "aday": {k: aday[k] for k in aday.keys()},
              "eksikler": [{"kod": k, "ad": ETIKET.get(k, k),
                            "kanit": (detay.get("kanit") or {}).get(k)} for k in eksikler],
              "tahmin": tahmin,
              "kisiler": vt.kisiler_getir(b, aday["id"]),
              "kanallar": vt.kanallar_getir(b, aday["id"]),
              "temaslar": vt.temaslar_getir(b, aday["id"], 30),
              "piyasa": PY.referans(anahtar, aday["sehir"], b),
              "hizmet": anahtar,
              "hizmet_ad": HIZMETLER.get(anahtar, {}).get("ad", anahtar),
              "arama": IL.arama_baglantilari(aday["ad"], aday["sehir"]),
              "onerilen_bedel": PY.oneri(anahtar, aday["sehir"], b),
              "sosyal": vt.sosyal_getir(b, aday["id"]),
              "sosyal_plan": SO.icerik_plani(aday["sektor"] or "isletme", 4),
            }
            if d["sosyal"]:
                d["sosyal"]["skor"] = SO.sosyal_skor(d["sosyal"])
            d["sosyal_demo"] = (os.path.relpath(
                os.path.join(M.DOSYA_KOK, "%s-%s" % (aday["id"], M.slugla(aday["ad"])),
                             "sosyal-demo.html"), CIKTI)
                if os.path.exists(os.path.join(M.DOSYA_KOK, "%s-%s" % (aday["id"], M.slugla(aday["ad"])),
                                               "sosyal-demo.html")) else None)
            b.close()
            return self._json(d)
        if y == "/api/gundem-kaynak":
            return self._json({"kaynak": GU.kaynak_testi()})
        if y == "/api/ziyaret":
            b = vt.baglan()
            kid = q.get("id", [None])[0]
            d = {"liste": vt.ziyaret_listesi(b),
                 "kayit": vt.ziyaret_getir(b, int(kid) if kid else None)}
            b.close()
            return self._json(d)
        if y == "/api/arama":
            b = vt.baglan()
            kid = q.get("id", [None])[0]
            d = {"liste": vt.arama_listesi(b),
                 "kayit": vt.arama_getir(b, int(kid) if kid else None)}
            b.close()
            return self._json(d)
        if y == "/api/ayarlar":
            a = A.ayarlari_getir()
            a["vt_yolu"] = vt.vt_yolu()
            a["cikti"] = CIKTI
            return self._json(a)
        if y.startswith("/cikti/"):
            rel = urllib.parse.unquote(y[len("/cikti/"):])
            tam = os.path.normpath(os.path.join(CIKTI, rel))
            if not tam.startswith(os.path.normpath(CIKTI)) or not os.path.isfile(tam):
                return self._g(404, "text/plain; charset=utf-8", "bulunamadı")
            tur = ("image/svg+xml; charset=utf-8" if tam.endswith(".svg")
                   else "text/html; charset=utf-8" if tam.endswith(".html")
                   else "text/plain; charset=utf-8" if tam.endswith((".md", ".txt", ".csv"))
                   else "application/octet-stream")
            with open(tam, "rb") as f:
                return self._g(200, tur, f.read(), ikili=True)
        if y.startswith("/demo/"):
            ad = urllib.parse.unquote(y[len("/demo/"):])
            if "/" in ad or ".." in ad:
                return self._g(400, "text/plain", "gecersiz")
            yol = os.path.join(CIKTI, "demo", ad)
            if not os.path.exists(yol):
                return self._g(404, "text/plain; charset=utf-8", "demo bulunamadı")
            with open(yol, "rb") as f:
                return self._g(200, "text/html; charset=utf-8", f.read(), ikili=True)
        return self._g(404, "text/plain", "yok")

    # ---------------- POST
    def do_POST(self):
        # PIN girişi kapının kendisi — yetki kontrolünden önce gelir.
        if urllib.parse.urlparse(self.path).path == "/giris":
            return self._giris()
        if not self._yetkili():
            return self._json({"hata": "Erişim anahtarı gerekli."}, 401)
        n = int(self.headers.get("Content-Length") or 0)
        try:
            g = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return self._json({"hata": "geçersiz json"}, 400)
        y = urllib.parse.urlparse(self.path).path
        try:
            return self._yonlendir(y, g)
        except Exception as ex:
            return self._json({"hata": "%s: %s" % (type(ex).__name__, ex)}, 500)

    def _yonlendir(self, y, g):
        # --- arama gündemi: günün derlemesini çıkar
        if y == "/api/sorgu-derle":
            try:
                paket = SG.topla()
            except Exception as ex:
                return self._json({"hata": "Derleme çalışmadı: %s" % ex}, 500)
            if not paket.get("sorgular"):
                return self._json({"hata": "Kaynaklardan sonuç gelmedi. "
                                           "İnternet bağlantısını kontrol et.",
                                   "ayrinti": paket.get("hata", [])}, 502)
            SG.kaydet(paket)
            return self._json({"tamam": True, "adet": paket["adet"],
                               "tarih": paket["tarih"], "uyari": paket.get("hata", [])})
        # --- arama gündemi: kaynak testi
        if y == "/api/sorgu-test":
            try:
                return self._json({"sonuc": [{"kaynak": a, "adet": b, "ornek": c}
                                             for a, b, c in SG.kaynak_testi()]})
            except Exception as ex:
                return self._json({"hata": str(ex)}, 500)
        # --- arama gündemi: sayfayı siteye bas
        if y == "/api/yz-yayinla":
            try:
                yol, adet = YZ.uret()
            except Exception as ex:
                return self._json({"hata": str(ex)}, 500)
            return self._json({"tamam": True, "yol": yol, "adet": adet})

        # --- makale: üret + puanla (yayınlamaz)
        if y == "/api/makale-olc":
            o = MK.olc((g.get("anahtar") or "").strip())
            return self._json(o or {"hata": "Konu bulunamadı."}, 200 if o else 404)
        # --- makale: yayın kapısı. 100 almayan buradan geçmiyor.
        if y == "/api/makale-yayinla":
            return self._json(MK.yayinla((g.get("anahtar") or "").strip()))

        # --- akış başlat
        if y == "/api/akis":
            if G.mesgul():
                return self._json({"hata": "Zaten çalışan bir görev var, bitmesini bekleyin."}, 409)
            sehir = (g.get("sehir") or "").strip()
            if not sehir:
                return self._json({"hata": "Şehir seçilmedi."}, 400)
            sektor = g.get("sektor") or None
            adimlar = g.get("adimlar") or None
            ad = "%s%s" % (sehir, (" · " + SEKTORLER[sektor]["ad"]) if sektor in SEKTORLER else " · tüm sektörler")
            gv = G.calistir(ad, lambda gg: AK.akis(
                gg, sehir, sektor, int(g.get("adet") or 0), bool(g.get("hizli", True)),
                bool(g.get("sadece_sicak", False)), g.get("ortalama_is"), adimlar), "tarama akışı")
            return self._json({"gorev": gv["id"]})

        # --- zenginleştirme (iletişim + yetkili araştırması)
        # --- elle firma ekleme: site / harita bağlantısıyla aday + tam analiz (arka planda)
        if y == "/api/ekle":
            if G.mesgul():
                return self._json({"hata": "Zaten çalışan bir görev var."}, 409)
            if not (g.get("site") or g.get("harita")):
                return self._json({"hata": "Site ya da Haritalar bağlantısı gerekli."}, 400)

            def is_(gg):
                from . import ekle as EK
                gg["toplam_adim"] = 1; gg["adim_no"] = 1; gg["adim"] = (g.get("site") or g.get("harita"))[:38]
                r = EK.firma_ekle(site=g.get("site"), ad=g.get("ad"), sehir=g.get("sehir"), sektor=g.get("sektor") or None,
                                  harita=g.get("harita"), telefon=g.get("telefon"))
                print("\n✓ Aday #%d hazır — skor %s. Adaylar listesinden aç." % (r["id"], r.get("skor", "—")))
            gv = G.calistir("Bağlantıyla ekle", is_, "elle firma")
            return self._json({"gorev": gv["id"]})

        if y == "/api/zenginlestir":
            if G.mesgul():
                return self._json({"hata": "Zaten çalışan bir görev var."}, 409)
            idler = [int(x) for x in (g.get("ids") or [])]
            sehir = g.get("sehir")

            def is_(gg):
                b2 = vt.baglan()
                if idler:
                    q2 = "SELECT * FROM adaylar WHERE id IN (%s)" % ",".join("?" * len(idler))
                    satir = b2.execute(q2, idler).fetchall()
                else:
                    q2 = "SELECT * FROM adaylar WHERE COALESCE(zengin,0)=0"
                    p2 = []
                    if sehir:
                        q2 += " AND sehir=?"; p2.append(sehir)
                    satir = b2.execute(q2 + " ORDER BY id", p2).fetchall()
                gg["toplam_adim"] = len(satir)
                print("▸ %d aday araştırılıyor" % len(satir))
                for i2, r2 in enumerate(satir, 1):
                    gg["adim_no"] = i2
                    gg["adim"] = r2["ad"][:38]
                    o = M.zenginlestir(b2, dict(r2))
                    print("  %3d/%d  %-34s %s" % (
                        i2, len(satir), r2["ad"][:34],
                        ("HATA: " + o["hata"]) if o["hata"] else
                        "%d e-posta · %d kişi · %d sosyal · kanal: %s" % (
                            len(o["eposta"]), o["kisi"], len(o["sosyal"]), o["kanal"]["kanal"])))
                    b2.commit()
                b2.close()
                print("\n✓ Araştırma bitti.")
            gv = G.calistir("İletişim araştırması", is_, "zenginleştirme")
            return self._json({"gorev": gv["id"]})

        # --- raf: durum değiştir
        if y == "/api/durum":
            b = vt.baglan()
            for i in (g.get("ids") or [g.get("aday_id")]):
                if i: vt.durum_ayarla(b, int(i), g["durum"])
            b.commit(); b.close()
            return self._json({"ok": True})

        # --- rakip teklif kaydı (piyasa öğrenmesi)
        if y == "/api/rakip-teklif":
            b = vt.baglan()
            vt.rakip_teklif_ekle(b, g["hizmet"], g["tutar"], g.get("sehir"),
                                 g.get("kaynak"), g.get("not"))
            b.commit()
            r = PY.referans(g["hizmet"], g.get("sehir"), b)
            b.close()
            return self._json({"ok": True, "referans": r})

        # --- API anahtarı canlı testi
        if y == "/api/anahtar-test":
            import json as _j, urllib.request as _u, ssl as _s
            if not A.GOOGLE_ANAHTAR:
                return self._json({"ok": False, "mesaj": "Google anahtarı boş."})
            govde = {"textQuery": g.get("sorgu") or "inşaat firması Bursa",
                     "languageCode": "tr", "regionCode": "TR", "maxResultCount": 3}
            istek = _u.Request(
                "https://places.googleapis.com/v1/places:searchText",
                data=_j.dumps(govde).encode(),
                headers={"Content-Type": "application/json",
                         "X-Goog-Api-Key": A.GOOGLE_ANAHTAR,
                         "X-Goog-FieldMask": "places.displayName,places.rating,"
                                             "places.userRatingCount,places.websiteUri"})
            try:
                with _u.urlopen(istek, timeout=20, context=_s.create_default_context()) as c:
                    v = _j.loads(c.read().decode())
                ornek = [{"ad": (p.get("displayName") or {}).get("text"),
                          "puan": p.get("rating"), "yorum": p.get("userRatingCount"),
                          "site": p.get("websiteUri")} for p in v.get("places", [])]
                return self._json({"ok": True,
                                   "mesaj": "Anahtar çalışıyor — Places API (New) açık.",
                                   "ornek": ornek})
            except Exception as ex:
                govde_hata = ""
                try:
                    govde_hata = ex.read().decode()[:400]
                except Exception:
                    pass
                kod = getattr(ex, "code", "")
                ipucu = ""
                if kod == 403:
                    ipucu = ("403 — Google Cloud projesinde 'Places API (New)' etkin değil ya da "
                             "anahtara kısıtlama konmuş olabilir.")
                elif kod == 400:
                    ipucu = "400 — istek reddedildi; anahtar biçimi hatalı olabilir."
                elif kod == 429:
                    ipucu = "429 — kota doldu."
                return self._json({"ok": False,
                                   "mesaj": "%s %s %s" % (type(ex).__name__, kod, ipucu).strip(),
                                   "detay": govde_hata})

        # --- arama performansı: Search Console dışa aktarımını yükle
        if y == "/api/arama-yukle":
            import base64, tempfile
            ham = g.get("veri") or ""
            if "," in ham[:200]:
                ham = ham.split(",", 1)[1]
            try:
                bayt = base64.b64decode(ham)
            except Exception:
                return self._json({"hata": "Dosya çözülemedi."}, 400)
            if not bayt:
                return self._json({"hata": "Dosya boş."}, 400)
            uzanti = os.path.splitext(g.get("ad") or "veri.zip")[1] or ".zip"
            gecici = os.path.join(tempfile.gettempdir(), "pusula-arama" + uzanti)
            with open(gecici, "wb") as f:
                f.write(bayt)
            yollar = None
            try:
                if os.path.isdir(SITE_KOK):
                    yollar = AR.site_yollari(SITE_KOK)
            except Exception:
                yollar = None
            sonuc = AR.ice_aktar(gecici, ILLER, yollar)
            try:
                os.remove(gecici)
            except OSError:
                pass
            if sonuc.get("hata"):
                return self._json(sonuc, 400)
            b = vt.baglan()
            kid = vt.arama_kaydet(b, g.get("ad") or sonuc["kaynak"], g.get("donem") or "", sonuc)
            b.commit(); b.close()
            sonuc["id"] = kid
            sonuc["site_tarandi"] = bool(yollar)
            return self._json(sonuc)

        # --- kda.lunayapim.com kontrolü (kullanıcının makinesinden)
        if y == "/api/altalan-test":
            import ssl as _s2, urllib.request as _u2
            alan = (g.get("alan") or "kda.lunayapim.com").strip()
            cikti = {"alan": alan, "kontrol": []}

            def dene(adres, ad):
                try:
                    istek = _u2.Request(adres, headers={"User-Agent": "LunaPusula/1.0"})
                    with _u2.urlopen(istek, timeout=12,
                                     context=_s2.create_default_context()) as c:
                        govde = c.read(200000).decode("utf-8", "replace")
                        return {"ad": ad, "adres": adres, "durum": c.status,
                                "tur": c.headers.get("Content-Type", ""),
                                "uzunluk": len(govde), "ilk": govde[:600],
                                "basliklar": {k: v for k, v in c.headers.items()}}
                except Exception as ex:
                    return {"ad": ad, "adres": adres,
                            "durum": getattr(ex, "code", 0),
                            "hata": "%s: %s" % (type(ex).__name__, ex)}

            for adres, ad in (("https://%s/" % alan, "ana sayfa"),
                              ("https://%s/robots.txt" % alan, "robots.txt"),
                              ("https://%s/sitemap.xml" % alan, "sitemap.xml")):
                cikti["kontrol"].append(dene(adres, ad))
            cikti["yorum"] = AR_altalan_yorum(cikti["kontrol"])
            return self._json(cikti)

        # --- gündem taraması
        if y == "/api/gundem":
            try:
                liste = GU.tara(ILLER, int(g.get("asgari") or 40), int(g.get("adet") or 12))
            except Exception as ex:
                return self._json({"hata": "%s: %s" % (type(ex).__name__, ex)}, 500)
            if not liste:
                return self._json({"liste": [], "not": (
                    "Hiç uygun haber çıkmadı. Ya ağ kapalı ya da bu hafta bizim işimizle "
                    "kesişen bir gündem yok — zorlama yazı yazmıyoruz. "
                    "'Kaynak testi' ile ağ tarafını kontrol edebilirsin.")})
            return self._json({"liste": liste[:40]})

        if y == "/api/gundem-taslak":
            h = g.get("haber") or {}
            if not h.get("aci"):
                return self._json({"hata": "Haber verisi eksik."}, 400)
            klasor = os.path.join(CIKTI, "gundem")
            yol = GU.yaz(h, klasor)
            return self._json({"yol": os.path.relpath(yol, CIKTI),
                               "metin": GU.taslak(h),
                               "sosyal": GU.sosyal_kesit(h)})

        if y == "/api/gundem-yayinla":
            """Seçilen haberleri günün sayısı olarak siteye basar (SEO kapısı dahil)."""
            secilen = g.get("haberler") or []
            if not secilen:
                return self._json({"hata": "Haber seçilmedi."}, 400)
            maddeler = []
            for h in secilen:
                if h.get("olgu") and h.get("aci_metin"):
                    maddeler.append(GY.madde_kur(h["baslik"], h.get("kaynak") or "Kaynak",
                                                 h["adres"], h.get("tarih") or "",
                                                 h["olgu"], h["aci_metin"], h.get("hizmet_sayfa") or ""))
                else:
                    maddeler.append(GY.taramadan_madde(h))
            try:
                aranan = [x["sorgu"] for x in (SG.oku() or {}).get("sorgular", [])[:10]]
            except Exception:
                aranan = None
            r = GY.yayinla(maddeler, aranan=aranan, kapi=True)
            # kayıt: aynı günün maddeleri tekrar üretilebilsin
            import json as _j, datetime as _d
            kd = os.path.join(A.KOK_DIZIN, "veri", "gundem"); os.makedirs(kd, exist_ok=True)
            with open(os.path.join(kd, _d.date.today().isoformat() + ".json"), "w", encoding="utf-8") as f:
                _j.dump([{"baslik": m["baslik"], "kaynak_ad": m["kaynak_ad"], "kaynak_url": m["kaynak_url"],
                          "kaynak_tarih": m["kaynak_tarih"], "olgu": m["olgu"], "aci": m["aci"],
                          "hizmet": next((k for k, v in GY.HIZMET_AD.items() if v[0] == m["hizmet_ad"]), "")}
                         for m in maddeler], f, ensure_ascii=False, indent=1)
            r["sayfa"] = os.path.relpath(r["sayfa"], A.SITE_KOK) if r.get("sayfa") else None
            return self._json(r)

        # --- yayın: taslak listesi / yayınla
        if y == "/api/yayin-taslaklar":
            return self._json({"taslak": YA.taslak_listesi(os.path.join(CIKTI, "gundem"))})

        if y == "/api/yayinla":
            yol = g.get("yol")
            if not yol or not os.path.isfile(yol):
                return self._json({"hata": "Taslak dosyası bulunamadı."}, 400)
            metin = open(yol, encoding="utf-8").read()
            yazi, uyari = YA.md_coz(metin)
            if not yazi["baslik"] or len(yazi["bolumler"]) < 2:
                return self._json({"hata": "Yazı yayına hazır değil.", "uyari": uyari}, 400)
            r = YA.yayinla(yazi)
            r["uyari"] = uyari
            r["kelime"] = len(re.sub(r"<[^>]+>", " ",
                                     " ".join(i for _, i in yazi["bolumler"])).split())
            if r["kelime"] < 400:
                r.setdefault("uyari", []).append(
                    "Yazı %d kelime. Google'ın ciddiye alması için 400+ kelime öneriliyor; "
                    "şu hâliyle 'ince içerik' uyarısı alır." % r["kelime"])
            if g.get("bildir"):
                r["indexnow"] = IN.bildir(r["adresler"])
            return self._json(r)

        # --- IndexNow
        if y == "/api/indexnow":
            islem = g.get("islem") or "durum"
            if islem == "anahtar":
                return self._json(IN.anahtar())
            if islem == "bildir":
                adres = g.get("adresler") or []
                if not adres:
                    adres = ["https://lunayapim.com/", "https://lunayapim.com/blog/"]
                return self._json(IN.bildir(adres))
            return self._json(IN.durum())

        # --- depo (git kilidi)
        if y == "/api/depo":
            islem = g.get("islem") or "durum"
            if islem == "kilit-coz":
                return self._json(DP.kilit_coz(zorla=bool(g.get("zorla"))))
            return self._json(DP.durum())

        # --- ölçüm kimlikleri
        if y == "/api/olcum":
            if g.get("kaydet"):
                return self._json(YA.olcum_yaz(g.get("ga4", ""), g.get("cloudflare", "")))
            return self._json(YA.olcum_oku())

        # --- etkileşim oranı hesabı (rakamlar elle giriliyor)
        if y == "/api/etkilesim":
            from . import sosyal_saglik as SSG
            r = SSG.etkilesim_hesapla(g.get("sektor") or "isletme",
                                     g.get("platform") or "instagram",
                                     g.get("takipci"), g.get("etkilesim"))
            if g.get("aylik_paylasim") not in (None, ""):
                r["tempo"] = SSG.tempo_yorumu(g.get("platform") or "instagram",
                                             g.get("aylik_paylasim"))
            if not r.get("hata") and g.get("aday_id"):
                b = vt.baglan()
                sd = vt.sosyal_getir(b, int(g["aday_id"])) or {}
                sd.setdefault("elle_girilen", []).append(r)
                vt.sosyal_kaydet(b, int(g["aday_id"]), sd, SO.sosyal_skor(sd)
                                 if "eksikler" in sd else None)
                b.commit(); b.close()
            return self._json(r)

        # --- ziyaret raporu (GA4 / Cloudflare dışa aktarımı)
        if y == "/api/ziyaret-yukle":
            import base64, tempfile
            ham = g.get("veri") or ""
            if "," in ham[:200]:
                ham = ham.split(",", 1)[1]
            try:
                bayt = base64.b64decode(ham)
            except Exception:
                return self._json({"hata": "Dosya çözülemedi."}, 400)
            if not bayt:
                return self._json({"hata": "Dosya boş."}, 400)
            uzanti = os.path.splitext(g.get("ad") or "veri.csv")[1] or ".csv"
            gecici = os.path.join(tempfile.gettempdir(), "pusula-ziyaret" + uzanti)
            with open(gecici, "wb") as f:
                f.write(bayt)
            r = ZY.ice_aktar(gecici)
            try:
                os.remove(gecici)
            except OSError:
                pass
            if r.get("sorun"):
                return self._json({"hata": r["sorun"]}, 400)
            r["yorum"] = ZY.yorum(r)
            b = vt.baglan()
            r["id"] = vt.ziyaret_kaydet(b, g.get("ad") or r.get("kaynak_dosya"),
                                        g.get("donem") or "", r)
            b.commit(); b.close()
            return self._json(r)

        # --- site sağlığı (kategori kırılımlı SEO denetimi)
        if y == "/api/saglik":
            if g.get("olc"):
                return self._json(SL.olc_ve_kaydet())
            return self._json({"gecmis": SL.gunluk_oku()[-60:]})

        # --- gelen talep → hazır yanıt taslağı
        if y == "/api/talep":
            if g.get("liste"):
                return self._json({"liste": TL.hizmet_listesi()})
            metin = (g.get("metin") or "").strip()
            if len(metin) < 15:
                return self._json({"sorun": "Mesaj çok kısa."}, 400)
            if g.get("kaydet"):
                t = TL.kaydet(metin, os.path.join(CIKTI, "talepler"))
                if not t.get("sorun"):
                    t["yol"] = os.path.relpath(t["yol"], CIKTI)
            else:
                t = TL.taslak(metin)
            return self._json(t, 400 if t.get("sorun") else 200)

        # --- kılavuz: formdan Claude'a yapıştırılacak talep metni
        if y == "/api/talep-metni":
            return self._json({"metin": KL.talep_metni(
                g.get("sekme"), g.get("baslik"), g.get("niyet"), g.get("beklenen"),
                g.get("olan"), g.get("hata", ""), g.get("aciliyet", ""),
                g.get("kim") or (self._kullanici(g) or ""))})

        # --- uzaktan erişim (Cloudflare tüneli)
        if y == "/api/uzak":
            if g.get("baslat"):
                return self._json(UZ.baslat(KAPI))
            if g.get("durdur"):
                return self._json(UZ.durdur())
            if "epostalar" in g:
                A.ayarlari_kaydet({"uzak_epostalar": g.get("epostalar")})
            return self._json(dict(UZ.durum(KAPI),
                                   adimlar=UZ.kalici_adimlar(kapi=KAPI),
                                   uzak_kipi=UZAK_KIPI,
                                   pin=AG.pin_okunakli(),
                                   epostalar=sorted(A.izinli_epostalar())))

        # --- ayarlar
        if y == "/api/ayarlar":
            a = A.ayarlari_kaydet(g)
            a["vt_yolu"] = vt.vt_yolu()
            a["cikti"] = CIKTI
            return self._json(a)

        # --- müşteri dosyası
        if y in ("/api/dosya", "/api/dosya-toplu"):
            b = vt.baglan()
            idler = [int(x) for x in (g.get("ids") or ([g["aday_id"]] if g.get("aday_id") else []))]
            bedel = g.get("bedel")
            sonuc = []
            for i in idler:
                p = _aday_paketi(b, i)
                if not p:
                    sonuc.append({"id": i, "hata": "aday bulunamadı"}); continue
                aday, eksikler, detay, tahmin = p
                r = M.dosya_uret(aday, eksikler, detay, tahmin, bedel, g.get("hizmet"), b)
                vt.demo_kaydet(b, i, r["analiz"], r["mesaj"]["whatsapp"])
                sonuc.append({
                    "id": i, "ad": aday["ad"], "klasor": r["klasor"],
                    "analiz": os.path.relpath(r["analiz"], CIKTI),
                    "teklif": os.path.relpath(r["teklif"], CIKTI),
                    "is_emri": os.path.relpath(r["is_emri"], CIKTI),
                    "mesajlar": os.path.relpath(r["mesajlar"], CIKTI),
                    "sosyal_demo": (os.path.relpath(r["sosyal_demo"], CIKTI)
                                    if r.get("sosyal_demo") else None),
                    "sosyal": r.get("sosyal"),
                    "cekim_plani": (os.path.relpath(r["cekim_plani"], CIKTI)
                                    if r.get("cekim_plani") else None),
                    "strateji": (os.path.relpath(r["strateji"], CIKTI)
                                 if r.get("strateji") else None),
                    "wa": r["wa"], "wa_numara": r["wa_numara"], "mailto": r["mailto"],
                    "epostalar": r["epostalar"], "kanal": r["kanal"],
                    "kisiler": r["kisiler"], "telefonlar": r["telefonlar"],
                    "hizmet": r["hizmet"], "hizmet_ad": r["hizmet_ad"],
                    "mesaj": r["mesaj"], "bedel": r["bedel"], "bedel_oneri": r["bedel_oneri"],
                    "piyasa": r["piyasa"], "deger": r["deger"], "arama": r["arama"],
                    "teklif_tek": (os.path.relpath(r["teklif_tek"], CIKTI)
                                   if r.get("teklif_tek") else None),
                    "onizleme": {k2: (os.path.relpath(v2, CIKTI) if isinstance(v2, str)
                                      and os.path.exists(v2) else v2)
                                 for k2, v2 in (r.get("onizleme") or {}).items()
                                 if k2 != "gorseller"},
                    "telegram": (TG.teklif_gonder(r, aday, eksikler, detay, tahmin)
                                 if (g.get("telegram") and TG.hazir()[0]) else None),
                })
            b.commit(); b.close()
            return self._json({"sonuc": sonuc})

        # --- telegram
        if y == "/api/asistan":
            return self._json(AP.cevapla(g.get("soru") or ""))

        if y == "/api/uretim-tahmin":
            if g.get("karga"):
                return self._json(UR.karga_plani(g.get("model") or "gen4_turbo", int(g.get("sn") or 5)))
            return self._json(UR.tahmin(g.get("tur") or "video", g.get("arac") or "runway",
                                        g.get("model"), int(g.get("sn") or 5), int(g.get("adet") or 1)))

        if y == "/api/uretim":
            """Kredi harcar — onay=True olmadan çalışmaz."""
            import importlib; importlib.reload(UR)      # anahtar yeni girilmiş olabilir
            try:
                if g.get("karga"):
                    sonuc = []
                    for ad, metin in UR.KARGA:
                        sonuc.append({"ad": ad, **UR.uret("video", metin, ad, "runway",
                                                          int(g.get("sn") or 5), "1280:720",
                                                          g.get("model"), bool(g.get("onay")))})
                    return self._json({"sonuc": sonuc})
                r = UR.uret(g.get("tur") or "video", g.get("metin") or "", g.get("ad") or "uretim",
                            g.get("arac") or "runway", int(g.get("sn") or 5), g.get("oran") or "1280:720",
                            g.get("model"), bool(g.get("onay")), g.get("gorsel_uri"))
                return self._json(r)
            except Exception as ex:
                return self._json({"hata": "%s: %s" % (type(ex).__name__, ex)}, 500)

        if y == "/api/telgraf-sina":
            ok, m = TG.sinama()
            return self._json({"ok": ok, "mesaj": m})

        if y == "/api/telgraf-gonder":
            b = vt.baglan()
            p = _aday_paketi(b, int(g["aday_id"]))
            if not p:
                b.close(); return self._json({"hata": "aday yok"}, 404)
            aday, eksikler, detay, tahmin = p
            r = M.dosya_uret(aday, eksikler, detay, tahmin, g.get("bedel"),
                             g.get("hizmet"), b)
            b.commit(); b.close()
            return self._json(TG.teklif_gonder(r, aday, eksikler, detay, tahmin))

        # --- e-posta
        if y == "/api/eposta":
            b = vt.baglan()
            p = _aday_paketi(b, int(g["aday_id"]))
            if not p:
                b.close(); return self._json({"hata": "aday yok"}, 404)
            aday, eksikler, detay, tahmin = p
            anahtar = g.get("hizmet") or M.hizmet_anahtari(aday)
            m = M.mesajlar_uret(aday, eksikler, tahmin, anahtar)
            klasor = os.path.join(M.DOSYA_KOK, "%s-%s" % (aday["id"], M.slugla(aday["ad"])))
            ekler = [os.path.join(klasor, x) for x in ("analiz.html", "teklif.html")
                     if os.path.exists(os.path.join(klasor, x))]
            ok, mesaj = M.eposta_gonder(g.get("alici"), m["eposta_konu"], m["eposta_govde"], ekler)
            if ok:
                vt.temas_ekle(b, aday["id"], "eposta", "eposta gonderildi")
                b.commit()
            b.close()
            return self._json({"ok": ok, "mesaj": mesaj,
                               "mailto": M.mailto_link(g.get("alici"), m["eposta_konu"], m["eposta_govde"])})

        # --- arşiv
        if y == "/api/arsiv":
            yol = arsiv_uret()
            return self._json({"yol": yol, "rel": os.path.relpath(yol, CIKTI)})

        # --- kayıtlar
        b = vt.baglan()
        try:
            if y == "/api/temas":
                for i in (g.get("ids") or [g.get("aday_id")]):
                    if not i: continue
                    vt.temas_ekle(b, int(i), g.get("kanal", ""), g.get("durum", ""), g.get("not"),
                                  g.get("yon", "giden"), g.get("kisi"),
                                  g.get("sonraki_adim"), g.get("sonraki_tarih"),
                                  self._kullanici(g))
            elif y == "/api/is":
                vt.is_ekle(b, g["musteri"], g.get("hizmet", ""), g.get("sehir"),
                           g.get("aday_id"), g.get("bedel"), g.get("teslim"), g.get("notlar"),
                           self._kullanici(g))
            elif y == "/api/is-asama":
                vt.is_asama(b, int(g["id"]), g["asama"])
            else:
                b.close(); return self._json({"hata": "bilinmeyen uç"}, 404)
            b.commit()
        finally:
            b.close()
        return self._json({"ok": True})


def calistir(kapi=KAPI, ac=True, ag=None, uzak=None):
    global AG_KIPI, UZAK_KIPI
    if ag is not None:
        AG_KIPI = bool(ag)
    if uzak is not None:
        UZAK_KIPI = bool(uzak)

    # Ağ kipinde tüm arayüzlere bağlanıyor; kapalıyken sadece bu bilgisayara.
    # Tünel kipinde dışarı açılmaya gerek yok — cloudflared localhost'a bağlanıyor.
    adres_ic = "0.0.0.0" if AG_KIPI else "127.0.0.1"
    s = ThreadingHTTPServer((adres_ic, kapi), Sunucu)
    url = "http://127.0.0.1:%d/" % kapi
    print("╔══════════════════════════════════════════════╗")
    print("║  LUNA PUSULA — Üretim Fabrikası              ║")
    print("╚══════════════════════════════════════════════╝")
    print("  Panel açık:  %s" % url)
    if AG_KIPI:
        anah = AG.anahtar()
        adr = AG.adresler(kapi, anah)
        print("")
        print("  ── AĞ KİPİ AÇIK ─────────────────────────────")
        print("  İkinci bilgisayar için hazır bağlantı:")
        print("")
        for a in adr:
            print("    %s" % a["url"])
            print("      %s" % a["not"])
            print("")
        if AG.panoya_kopyala(adr[0]["url"]):
            print("  ✓ Bağlantı panoya kopyalandı — WhatsApp'a ya da")
            print("    e-postaya doğrudan yapıştırabilirsin (Cmd+V).")
        else:
            print("  Bağlantıyı yukarıdan seçip kopyala.")
        print("")
        print("  Karşı taraf tıklayınca panel açılır; anahtarı elle")
        print("  girmesi gerekmiyor, adresin içinde. Bir kez açması")
        print("  yeterli — tarayıcı hatırlıyor.")
        if not AG.ag_var_mi():
            print("")
            print("  ! Yerel ağ adresi bulunamadı — bilgisayar ağa bağlı değil")
            print("    gibi görünüyor. Wi-Fi bağlantısını kontrol edip bu")
            print("    pencereyi kapatıp yeniden açın.")
        print("")
        print("  Bu adres yalnızca aynı ev/ofis ağı içinden açılır;")
        print("  internetten erişilemez. Veritabanı BU bilgisayarda.")
        print("  ─────────────────────────────────────────────")
        print("")
    if UZAK_KIPI:
        print("")
        print("  ── UZAKTAN ERİŞİM KİPİ ──────────────────────")
        print("  Panel internete açılmaya hazır. Adresi almak için")
        print("  panelde Kılavuz sekmesi → Uzaktan erişim →")
        print("  'Tüneli başlat' düğmesine bas.")
        print("")
        print("  Giriş PIN'i:  %s" % AG.pin_okunakli())
        print("  Eşine bu PIN'i söylemen yeterli; uzun adres yok.")
        print("")
        print("  Bu kipte panelin kendi tarayıcısı da anahtar istiyor —")
        print("  tünelin trafiği de bu bilgisayardan geldiği için")
        print("  'kendi bilgisayarım serbest' muafiyeti kapalı.")
        print("  ─────────────────────────────────────────────")
        print("")
    print("  Veri kaynağı: %s" % ("Google Places" if A.GOOGLE_ANAHTAR else "OpenStreetMap (anahtarsız)"))
    print("  Kapatmak için bu pencerede Ctrl+C")
    yerel_url = url
    if UZAK_KIPI:
        # Tünel kipinde muafiyet yok; kendi tarayıcısı da anahtarla girsin.
        yerel_url = "http://127.0.0.1:%d/?anahtar=%s" % (kapi, AG.anahtar())
    if ac:
        threading.Timer(0.8, lambda: webbrowser.open(yerel_url)).start()
    try:
        s.serve_forever()
    except KeyboardInterrupt:
        print("\n  panel kapatıldı")
        s.server_close()


if __name__ == "__main__":
    import sys
    calistir(ag=True if "--ag" in sys.argv else None,
             uzak=True if "--uzak" in sys.argv else None,
             ac=("--acma" not in sys.argv))
