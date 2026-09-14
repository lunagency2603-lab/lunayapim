# -*- coding: utf-8 -*-
"""
KAYNAK ÖZETİ — Google Haberler bağlantısını yayıncının gerçek adresine çözer, sayfadan
kısa ve kaynaklı bir özet çıkarır (og:description + ilk paragraflar). Haber sayfası
yalnız bu özet gerçekten varsa yazılır; yoksa madde gündem sayısında bağlantı olarak
kalır, ayrı sayfa açılmaz (ince sayfa yok).

Alıntı sınırı: en çok iki kısa parça (olgu + ek), toplam ~700 karakter; kaynak adı ve
bağlantısı her zaman yanında. Haber yeniden yazılmaz.
Sadece standart kütüphane. İnternet ister (Mac'te çalışır); önbellek veri/ham/ozet/.
"""
import base64, hashlib, html as H, json, os, re, urllib.parse, urllib.request
from .ayarlar import KOK_DIZIN, KULLANICI_AJANI
from .kaynaklar.agir import getir

ONBELLEK = os.path.join(KOK_DIZIN, "veri", "ham", "ozet")
ASGARI = 240          # olgu bu uzunluğun altındaysa haber sayfası açılmaz

def _temiz(t):
    t = H.unescape(re.sub(r"<[^>]+>", " ", t or ""))
    return re.sub(r"\s+", " ", t).strip()

def _cumle_kes(t, azami):
    t = _temiz(t)
    if len(t) <= azami:
        return t
    kes = t[:azami]
    for ayrac in (". ", "! ", "? ", "; "):
        i = kes.rfind(ayrac)
        if i > azami * 0.55:
            return kes[:i + 1].strip()
    return kes.rsplit(" ", 1)[0].rstrip(",;:") + "…"

# ---------------------------------------------------------------- google haberler çözümü
def _gn_kimlik(url):
    m = re.search(r"news\.google\.com/(?:rss/)?articles/([^/?#]+)", url or "")
    return m.group(1) if m else None

def _gn_eski_coz(kimlik):
    """2024 öncesi biçim: base64 içinde düz adres."""
    try:
        ham = base64.urlsafe_b64decode(kimlik + "=" * (-len(kimlik) % 4))
        m = re.search(rb"https?://[^\x00-\x1f\x7f-\xff\"'<> ]+", ham)
        if m:
            u = m.group(0).decode("utf-8", "ignore")
            if "google." not in u:
                return u
    except Exception:
        pass
    return None

def _gn_yeni_coz(kimlik):
    """2024+ biçim: sayfadaki imza/zaman ile batchexecute çağrısı."""
    kod, sayfa, _ = getir("https://news.google.com/articles/" + kimlik, zaman_asimi=15)
    if kod != 200 or not sayfa:
        return None
    sg = re.search(r'data-n-a-sg="([^"]+)"', sayfa); ts = re.search(r'data-n-a-ts="([^"]+)"', sayfa)
    if not (sg and ts):
        m = re.search(r'<a[^>]+href="(https?://(?!(?:www\.)?google\.)[^"]+)"', sayfa)
        return m.group(1) if m else None
    yuk = ["Fbv4je", '["garturlreq",[["X","X",["X","X"],null,null,1,1,"TR:tr",null,1,null,null,null,null,null,0,1],"X","X",1,[1,1,1],1,1,null,0,0,null,0],"%s",%s,"%s"]' % (kimlik, ts.group(1), sg.group(1))]
    veri = "f.req=" + urllib.parse.quote(json.dumps([[yuk]]))
    istek = urllib.request.Request("https://news.google.com/_/DotsSplashUi/data/batchexecute", data=veri.encode("utf-8"),
                                   headers={"User-Agent": KULLANICI_AJANI, "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"})
    try:
        with urllib.request.urlopen(istek, timeout=15) as c:
            metin = c.read().decode("utf-8", "replace")
        parca = metin.split("\n\n")[1]
        dis = json.loads(parca)
        ic = json.loads(dis[0][2])
        u = ic[1]
        return u if isinstance(u, str) and u.startswith("http") else None
    except Exception:
        return None

def gercek_adres(url):
    k = _gn_kimlik(url)
    if not k:
        return url
    return _gn_eski_coz(k) or _gn_yeni_coz(k) or url

# ---------------------------------------------------------------- yayıncı sayfası
def _meta(sayfa, ad):
    m = re.search(r'<meta[^>]+(?:property|name)=["\']%s["\'][^>]+content=["\']([^"\']+)["\']' % re.escape(ad), sayfa, re.I) or \
        re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:property|name)=["\']%s["\']' % re.escape(ad), sayfa, re.I)
    return H.unescape(m.group(1)).strip() if m else ""

def _paragraflar(sayfa, en_az=60, adet=6):
    govde = re.search(r"<article[^>]*>(.*?)</article>", sayfa, re.S | re.I)
    kaynak = govde.group(1) if govde else sayfa
    kaynak = re.sub(r"<(script|style|nav|footer|header|aside)[^>]*>.*?</\1>", " ", kaynak, flags=re.S | re.I)
    ps = []
    for m in re.finditer(r"<p[^>]*>(.*?)</p>", kaynak, re.S | re.I):
        t = _temiz(m.group(1))
        if len(t) >= en_az and not re.search(r"©|çerez|cookie|abone ol|tıklayın", t, re.I) and t not in ps:
            ps.append(t)
        if len(ps) >= adet:
            break
    return ps

def sayfa_ozeti(url):
    """{adres, baslik, olgu, ek, tarih} — bulunamazsa olgu boş."""
    os.makedirs(ONBELLEK, exist_ok=True)
    anahtar = hashlib.sha1((url or "").encode("utf-8")).hexdigest()[:16]
    yol = os.path.join(ONBELLEK, anahtar + ".json")
    if os.path.exists(yol):
        try:
            return json.load(open(yol, encoding="utf-8"))
        except Exception:
            pass
    adres = gercek_adres(url)
    sonuc = {"adres": adres, "baslik": "", "olgu": "", "ek": "", "tarih": ""}
    kod, sayfa, son = getir(adres, zaman_asimi=20, basliklar={"Accept": "text/html"})
    if kod == 200 and sayfa:
        if son and "google." not in son:
            sonuc["adres"] = son
        sonuc["baslik"] = _meta(sayfa, "og:title") or _temiz(re.search(r"<title>(.*?)</title>", sayfa, re.S | re.I).group(1) if re.search(r"<title>", sayfa, re.I) else "")
        sonuc["tarih"] = _meta(sayfa, "article:published_time") or _meta(sayfa, "datePublished")
        desc = _meta(sayfa, "og:description") or _meta(sayfa, "description")
        ps = _paragraflar(sayfa)
        # olgu: açıklama + ilk paragrafın birleşimi, tekrarsız; ek: sonraki 1-2 paragraf
        olgu = desc.rstrip("…. ")
        for p in ps:
            if p[:60] in olgu:
                continue
            if len(olgu) < 200:
                olgu = (olgu + " " + p).strip() if olgu else p
            else:
                break
        sonuc["olgu"] = _cumle_kes(olgu, 380)
        kalan = [p for p in ps if p[:60] not in sonuc["olgu"]]
        sonuc["ek"] = _cumle_kes(" ".join(kalan[:2]), 330) if kalan else ""
    json.dump(sonuc, open(yol, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return sonuc

def zenginlestir(h):
    """gundem.tara() maddesini yerinde zenginleştirir: gerçek adres, kaynaklı özet, ek parça."""
    try:
        s = sayfa_ozeti(h.get("adres", ""))
    except Exception:
        return h
    if s.get("adres") and "google." not in s["adres"]:
        h["adres"] = s["adres"]
    baslik = _temiz(h.get("baslik", ""))
    if len(s.get("olgu", "")) >= ASGARI and s["olgu"][:80] != baslik[:80]:
        h["ozet"] = s["olgu"]; h["ek"] = s.get("ek", "")
    if s.get("tarih") and not h.get("tarih"):
        h["tarih"] = s["tarih"]
    return h

def yeterli(m):
    """Haber sayfası açmaya değer mi: gerçek, kaynaklı bir olgu paragrafı var mı?"""
    if isinstance(m.get("yazi"), dict) and m["yazi"].get("bolumler") and not m["yazi"].get("hata"):
        return True
    olgu = _temiz(m.get("olgu", "")); baslik = _temiz(m.get("baslik", ""))
    return len(olgu) >= ASGARI and olgu[:80] != baslik[:80]
