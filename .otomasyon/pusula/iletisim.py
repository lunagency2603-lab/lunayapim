# -*- coding: utf-8 -*-
"""
İletişim ve yönetici keşfi.

NE YAPAR: Firmanın KENDİ web sitesini gezer (ana sayfa + iletişim/hakkımızda/ekip
sayfaları), orada YAYINLANMIŞ e-posta, telefon, sosyal hesap ve isim-ünvan
bilgilerini toplar. Her bulgu, bulunduğu sayfanın adresiyle birlikte kaydedilir —
"teyitli" derken kastedilen bu: kaynağı tıklayıp kendin görebilirsin.

NE YAPMAZ: LinkedIn, Instagram gibi platformların içine girip kişi profili
kazımaz. Bu hem o platformların kullanım şartlarına aykırı hem de KVKK açısından
riskli. Bunun yerine firmanın doğrulanmış sosyal hesap adreslerini ve elle
açabileceğin hazır arama bağlantılarını üretir.
"""
import re, html, urllib.parse, datetime
from .kaynaklar.agir import getir

# ---------------------------------------------------------------- telefon
# Türkiye numara planı
MOBIL_ONEK = ("50", "51", "52", "53", "54", "55", "56")     # 5xx
KISA = ("444",)
UCRETSIZ = ("800",)
SABIT_UCRETLI = ("850",)

ALAN_KODU_IL = {
 "212":"İstanbul (Avrupa)","216":"İstanbul (Anadolu)","222":"Eskişehir","224":"Bursa","226":"Yalova",
 "228":"Bilecik","232":"İzmir","236":"Manisa","242":"Antalya","246":"Isparta","248":"Burdur",
 "252":"Muğla","256":"Aydın","258":"Denizli","262":"Kocaeli","264":"Sakarya","266":"Balıkesir",
 "272":"Afyonkarahisar","274":"Kütahya","276":"Uşak","282":"Tekirdağ","284":"Edirne","286":"Çanakkale",
 "288":"Kırklareli","312":"Ankara","318":"Kırıkkale","322":"Adana","324":"Mersin","326":"Hatay",
 "328":"Osmaniye","332":"Konya","338":"Karaman","342":"Gaziantep","344":"Kahramanmaraş","346":"Sivas",
 "348":"Kilis","352":"Kayseri","354":"Yozgat","356":"Tokat","358":"Amasya","362":"Samsun","364":"Çorum",
 "366":"Kastamonu","368":"Sinop","370":"Karabük","372":"Zonguldak","374":"Bolu","376":"Çankırı",
 "378":"Bartın","380":"Düzce","382":"Aksaray","384":"Nevşehir","386":"Kırşehir","388":"Niğde",
 "412":"Diyarbakır","414":"Şanlıurfa","416":"Adıyaman","422":"Malatya","424":"Elazığ","426":"Bingöl",
 "428":"Tunceli","432":"Van","434":"Bitlis","436":"Muş","438":"Hakkâri","442":"Erzurum","446":"Erzincan",
 "452":"Ordu","454":"Giresun","456":"Gümüşhane","458":"Bayburt","462":"Trabzon","464":"Rize",
 "466":"Artvin","472":"Ağrı","474":"Kars","476":"Iğdır","478":"Ardahan","482":"Mardin","484":"Siirt",
 "486":"Şırnak","488":"Batman",
}


def telefon_tipi(ham):
    """Numarayı sınıflandırır. WhatsApp yalnızca mobil hatlarda çalışır."""
    d = {"ham": ham or "", "normal": None, "tip": "bilinmiyor", "wa": False, "aciklama": "", "il": None}
    if not ham:
        d["aciklama"] = "numara yok"
        return d
    r = re.sub(r"\D", "", str(ham))
    if r.startswith("00"): r = r[2:]
    if r.startswith("90") and len(r) >= 12: r = r[2:]
    if r.startswith("0"): r = r[1:]

    if len(r) == 7 and r[:3] in KISA:
        d.update(tip="kisa", aciklama="444'lü kısa numara — WhatsApp desteklemez")
        d["normal"] = "0" + r
        return d
    if len(r) != 10:
        d["aciklama"] = "numara biçimi çözülemedi (%d hane)" % len(r)
        return d

    d["normal"] = "90" + r
    onek3, onek2 = r[:3], r[:2]
    if onek2 in MOBIL_ONEK:
        d.update(tip="mobil", wa=True, aciklama="cep hattı — WhatsApp denenebilir")
    elif onek3 in UCRETSIZ:
        d.update(tip="ucretsiz", aciklama="800'lü ücretsiz hat — WhatsApp yok")
    elif onek3 in SABIT_UCRETLI:
        d.update(tip="sabit-ucretli", aciklama="850'li işletme hattı — WhatsApp genelde yok")
    elif onek3 in ALAN_KODU_IL:
        d.update(tip="sabit", il=ALAN_KODU_IL[onek3],
                 aciklama="%s sabit hattı — WhatsApp yok, e-posta yolu kullanılmalı" % ALAN_KODU_IL[onek3])
    else:
        d["aciklama"] = "tanınmayan önek (%s)" % onek3
    return d


def kanal_onerisi(telefonlar, epostalar):
    """Hangi kanaldan gidilecek — sırayla WhatsApp, telefon, e-posta."""
    mobil = [t for t in telefonlar if t["wa"]]
    sabit = [t for t in telefonlar if t["tip"] in ("sabit", "sabit-ucretli", "kisa", "ucretsiz")]
    if mobil:
        return {"kanal": "whatsapp", "hedef": mobil[0]["normal"],
                "gerekce": "cep hattı bulundu — WhatsApp birincil kanal"}
    if epostalar:
        return {"kanal": "eposta", "hedef": epostalar[0],
                "gerekce": "cep hattı yok, sabit hat var" if sabit else "yalnızca e-posta bulundu"}
    if sabit:
        return {"kanal": "telefon", "hedef": sabit[0]["normal"],
                "gerekce": "sadece sabit hat var — aranmalı, mesaj gitmez"}
    return {"kanal": "yok", "hedef": None, "gerekce": "hiçbir iletişim kanalı bulunamadı"}


# ---------------------------------------------------------------- site keşfi
EPOSTA = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
TEL = re.compile(r"(?:\+?90[\s\-.]?)?(?:\(?0?\d{3}\)?[\s\-.]?)\d{3}[\s\-.]?\d{2}[\s\-.]?\d{2}")
KOTU_EPOSTA = ("example.com", "domain.com", "sentry.io", "wixpress", "godaddy",
               ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", "@2x", "u003e")

SOSYAL = {
 "instagram": r"instagram\.com/([A-Za-z0-9_.]+)",
 "facebook":  r"facebook\.com/([A-Za-z0-9_.\-]+)",
 "linkedin":  r"linkedin\.com/(?:company|in)/([A-Za-z0-9_.\-%]+)",
 "x":         r"(?:twitter|x)\.com/([A-Za-z0-9_]+)",
 "youtube":   r"youtube\.com/(?:@|c/|channel/|user/)([A-Za-z0-9_.\-]+)",
 "tiktok":    r"tiktok\.com/@([A-Za-z0-9_.]+)",
}
SOSYAL_ATLA = {"instagram": {"p", "explore", "reel", "reels", "accounts"},
               "facebook": {"sharer", "share", "plugins", "tr", "profile.php", "dialog"},
               "x": {"intent", "share", "home", "search"},
               "linkedin": {"shareArticle", "sharing", "feed"}}

UNVANLAR = ["Yönetim Kurulu Başkanı", "Yönetim Kurulu Üyesi", "Genel Müdür Yardımcısı", "Genel Müdür",
            "Genel Koordinatör", "Fabrika Müdürü", "İşletme Müdürü", "Satış Müdürü", "Satış Direktörü",
            "Pazarlama Müdürü", "İhracat Müdürü", "İhracat Sorumlusu", "Proje Müdürü", "Şantiye Şefi",
            "Teknik Müdür", "Mali İşler Müdürü", "İnsan Kaynakları Müdürü", "Bölge Müdürü",
            "Kurucu Ortak", "Kurucu", "Şirket Müdürü", "Müdür", "Direktör", "Koordinatör",
            "CEO", "CTO", "CFO", "COO", "Genel Sekreter", "Mimar", "İç Mimar", "Baş Mimar",
            "Gayrimenkul Danışmanı", "Broker", "Şef", "Sorumlu", "Yönetici"]
UNVAN_RX = re.compile("(" + "|".join(re.escape(u) for u in UNVANLAR) + ")")
ISIM_RX = re.compile(r"((?:[A-ZÇĞİÖŞÜ][a-zçğıöşü]{1,}\.?\s){1,3}[A-ZÇĞİÖŞÜ][A-ZÇĞİÖŞÜa-zçğıöşü]{1,})")

ARANAN_YOLLAR = ["", "/iletisim", "/iletisim.html", "/contact", "/hakkimizda", "/hakkimizda.html",
                 "/kurumsal", "/about", "/ekip", "/ekibimiz", "/yonetim", "/team", "/biz-kimiz",
                 "/insan-kaynaklari", "/kurumsal/yonetim", "/hakkinda"]

ETIKET = re.compile(r"<[^>]+>")
BETIK = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.S | re.I)


def _metin(g):
    g = BETIK.sub(" ", g)
    g = re.sub(r"<br\s*/?>|</p>|</div>|</li>|</h[1-6]>", "\n", g, flags=re.I)
    g = ETIKET.sub(" ", g)
    return re.sub(r"[ \t]+", " ", html.unescape(g))


def _kok(url):
    p = urllib.parse.urlparse(url if url.startswith("http") else "https://" + url)
    return "%s://%s" % (p.scheme, p.netloc), p.netloc


def _temiz_eposta(e):
    e = e.strip().strip(".").lower()
    if any(k in e for k in KOTU_EPOSTA): return None
    if len(e) > 90: return None
    return e


def site_kesif(site, azami_sayfa=6):
    """
    Firmanın kendi sitesinden iletişim bilgisi ve yayınlanmış kişi/ünvan toplar.
    Döner: {epostalar, telefonlar, sosyal, kisiler, gezilen, hata}
    """
    sonuc = {"epostalar": [], "telefonlar": [], "sosyal": {}, "kisiler": [],
             "gezilen": [], "hata": None,
             "zaman": datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}
    if not site:
        sonuc["hata"] = "site adresi yok"
        return sonuc
    kok, alan = _kok(site)

    # ana sayfadan iç bağlantıları topla
    kod, govde, _ = getir(kok)
    if kod == 0 or not govde:
        kod, govde, _ = getir(kok, dogrula_ssl=False)
    if kod == 0 or not govde:
        sonuc["hata"] = "siteye ulaşılamadı"
        return sonuc

    adaylar = [kok]
    for m in re.finditer(r'href="([^"]+)"', govde):
        u = m.group(1)
        if u.startswith("#") or u.startswith("mailto:") or u.startswith("tel:"): continue
        tam = urllib.parse.urljoin(kok, u)
        if alan not in tam: continue
        yol = urllib.parse.urlparse(tam).path.lower()
        if any(a and a.strip("/") in yol for a in ARANAN_YOLLAR if a):
            if tam not in adaylar: adaylar.append(tam)
    for y in ARANAN_YOLLAR[1:]:
        t = kok + y
        if t not in adaylar: adaylar.append(t)
    adaylar = adaylar[:azami_sayfa + 6]

    gorulen_eposta, gorulen_tel, gorulen_kisi = {}, {}, {}
    gezildi = 0
    for u in adaylar:
        if gezildi >= azami_sayfa: break
        if u == kok:
            g = govde
        else:
            k, g, _ = getir(u)
            if k != 200 or not g: continue
        gezildi += 1
        sonuc["gezilen"].append(u)

        for e in EPOSTA.findall(g):
            t = _temiz_eposta(e)
            if t and t not in gorulen_eposta:
                gorulen_eposta[t] = u
        m = _metin(g)
        for t in TEL.findall(m):
            bilgi = telefon_tipi(t)
            if bilgi["normal"] and bilgi["normal"] not in gorulen_tel:
                bilgi["kaynak"] = u
                gorulen_tel[bilgi["normal"]] = bilgi
        for ad, rx in SOSYAL.items():
            for h in re.findall(rx, g, re.I):
                if h.lower() in SOSYAL_ATLA.get(ad, set()): continue
                if ad not in sonuc["sosyal"]:
                    sonuc["sosyal"][ad] = {"kullanici": h, "kaynak": u,
                                           "url": _sosyal_url(ad, h), "dogrulandi": False}
        # kişi + ünvan
        for satir in m.split("\n"):
            s = satir.strip()
            if not (8 < len(s) < 160): continue
            um = UNVAN_RX.search(s)
            if not um: continue
            unvan = um.group(1)
            oncesi, sonrasi = s[:um.start()].strip(" ,-–—|:"), s[um.end():].strip(" ,-–—|:")
            isim = None
            for parca in (oncesi[-60:], sonrasi[:60]):
                im = ISIM_RX.search(parca)
                if im:
                    aday_isim = im.group(1).strip()
                    if UNVAN_RX.search(aday_isim): continue
                    if 5 <= len(aday_isim) <= 45 and len(aday_isim.split()) >= 2:
                        isim = aday_isim; break
            if isim and (isim, unvan) not in gorulen_kisi:
                gorulen_kisi[(isim, unvan)] = u

    sonuc["epostalar"] = [{"deger": e, "kaynak": k} for e, k in gorulen_eposta.items()]
    sonuc["telefonlar"] = list(gorulen_tel.values())
    sonuc["kisiler"] = [{"isim": i, "unvan": u, "kaynak": k} for (i, u), k in gorulen_kisi.items()]
    return sonuc


def _sosyal_url(ad, h):
    return {"instagram": "https://instagram.com/%s",
            "facebook": "https://facebook.com/%s",
            "linkedin": "https://linkedin.com/company/%s",
            "x": "https://x.com/%s",
            "youtube": "https://youtube.com/@%s",
            "tiktok": "https://tiktok.com/@%s"}.get(ad, "%s") % h


def sosyal_dogrula(url):
    """Hesap gerçekten açık mı — sadece durum kodu bakılır, içerik kazınmaz."""
    kod, _, _ = getir(url)
    return kod in (200, 999)     # LinkedIn bot trafiğine 999 döner


def arama_baglantilari(firma, sehir=None):
    """Elle açıp bakman için hazır arama adresleri — otomatik kazıma yok."""
    q = urllib.parse.quote('"%s"%s' % (firma, (" " + sehir) if sehir else ""))
    return {
      "LinkedIn şirket": "https://www.linkedin.com/search/results/companies/?keywords=" + q,
      "LinkedIn yönetici": "https://www.google.com/search?q=" + urllib.parse.quote(
          'site:linkedin.com/in "%s" (müdür OR genel müdür OR kurucu OR sahibi)' % firma),
      "Instagram": "https://www.google.com/search?q=" + urllib.parse.quote(
          'site:instagram.com "%s"' % firma),
      "Google (iletişim)": "https://www.google.com/search?q=" + urllib.parse.quote(
          '"%s" iletişim (e-posta OR mail OR "genel müdür")' % firma),
      "Ticaret sicili": "https://www.google.com/search?q=" + urllib.parse.quote(
          '"%s" ticaret sicil gazetesi' % firma),
    }
