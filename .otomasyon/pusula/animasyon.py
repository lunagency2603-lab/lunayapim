# -*- coding: utf-8 -*-
"""
HİZMET TANITIM ANİMASYONLARI — v2 (ARTIK KULLANILMIYOR)

Bu SVG sürümü yerini gerçek videoya bıraktı: ../video-uretici/ altında sahne
motoru duruyor, çıktılar assets/video/ içinde. Burası sayfaya gömme işini
video olarak yapıyor; SVG üretimi tarihsel olarak duruyor.

ESKİ AÇIKLAMA

İlk sürüm çubuk adam kalmıştı: kutular ve çizgiler, içi boş. Galzura
animasyonunun dili farklı ve doğru olan o:

  • solda bölüm numarası (06 / 13) + ince kural çizgisi
  • altında büyük başlık, altında iki satırlık gri açıklama
  • sağda GERÇEK ARAYÜZ KURGUSU — kartlar, rozetler, ilerleme çubukları,
    isimler, tarihler, rakamlar. Soyut şekil değil, bakınca "bu bir ekran"
    dediğin şey.
  • altta bölüm sayacı

Bu dosya o dili Luna paletiyle (mürekkep / kemik / vermilyon) yeniden kuruyor.
Her animasyon 2-3 bölümden geçiyor, bölümler çapraz geçişle değişiyor.

Video değil, SVG: 8-20 KB, anında açılıyor, metni arama motoru okuyabiliyor,
prefers-reduced-motion'da duruyor.
"""
import os

MUREKKEP = "#14110f"
PANEL    = "#1a1715"
PANEL2   = "#12100f"
KEMIK    = "#efe7dd"
KIRMIZI  = "#e8452c"
GRI      = "#8a8079"
CIZGI    = "#2a2724"
YESIL    = "#8fce8f"
SARI     = "#d8a13a"

G, Y = 640, 340          # tuval
BOLUM_SURE = 4.6         # her bölüm kaç saniye durur


# ------------------------------------------------------------------ yardımcı
def _k(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _bol(metin, en):
    """Uzun başlığı kelime sınırından ikiye böler."""
    if len(metin) <= en:
        return [metin]
    kel, satir, sonuc = metin.split(), "", []
    for k in kel:
        if satir and len(satir) + 1 + len(k) > en:
            sonuc.append(satir); satir = k
        else:
            satir = (satir + " " + k).strip()
    sonuc.append(satir)
    return sonuc


def _gorunurluk(sira, toplam, ic):
    """Bölümü sırası gelince gösterip sonra saklayan sarmalayıcı."""
    top = toplam * BOLUM_SURE
    bas, bit = sira * BOLUM_SURE, (sira + 1) * BOLUM_SURE
    return ('<g opacity="0">'
            '<animate attributeName="opacity" '
            'values="0;1;1;0;0" keyTimes="0;%.4f;%.4f;%.4f;1" dur="%.1fs" '
            'repeatCount="indefinite"/>%s</g>'
            % (max(0.001, (bas + 0.35) / top), (bit - 0.55) / top,
               (bit - 0.2) / top, top, ic))


def _girisli(ic, gecikme, sira, toplam, kayma=10):
    """Bölüm içindeki öge: aşağıdan hafifçe yükselerek gelir."""
    top = toplam * BOLUM_SURE
    b = sira * BOLUM_SURE + gecikme
    return ('<g opacity="0" transform="translate(0,%d)">'
            '<animate attributeName="opacity" values="0;0;1;1" '
            'keyTimes="0;%.4f;%.4f;1" dur="%.1fs" repeatCount="indefinite"/>'
            '<animateTransform attributeName="transform" type="translate" '
            'values="0 %d;0 %d;0 0;0 0" keyTimes="0;%.4f;%.4f;1" '
            'dur="%.1fs" repeatCount="indefinite"/>%s</g>'
            % (kayma, b / top, (b + 0.45) / top, top,
               kayma, kayma, b / top, (b + 0.45) / top, top, ic))


# ------------------------------------------------------------------ parçalar
def _dagit(n, w):
    """n adet w genişlikteki ögeyi sağ sütuna eşit aralıkla dağıtır."""
    if n <= 1:
        return [SAG]
    bos = (SAG_G - n * w) / float(n - 1)
    return [int(round(SAG + i * (w + bos))) for i in range(n)]


def _sol(no, toplam, baslik, alt1, alt2, sira):
    """Galzura'daki sol sütun: numara, kural, başlık, iki satır açıklama."""
    g = []
    g.append('<text x="46" y="112" font-family="Bricolage Grotesque,Manrope,sans-serif" '
             'font-size="15" fill="%s">%02d</text>' % (KIRMIZI, no))
    g.append('<line x1="70" y1="107" x2="106" y2="107" stroke="%s" stroke-width="1"/>' % CIZGI)
    # Başlık sol sütuna sığmalı: 16 karakteri geçerse boşluktan ikiye bölünüyor.
    satirlar, y = _bol(baslik, 16), 152
    for st in satirlar[:2]:
        g.append('<text x="46" y="%d" font-family="Bricolage Grotesque,Manrope,sans-serif" '
                 'font-weight="800" font-size="23" fill="%s">%s</text>'
                 % (y, KEMIK, _k(st)))
        y += 28
    y += 6
    for alt in (alt1, alt2):
        if alt:
            g.append('<text x="46" y="%d" font-family="Manrope,sans-serif" font-size="13" '
                     'fill="%s">%s</text>' % (y, GRI, _k(alt)))
            y += 19
    return _girisli("".join(g), 0.15, sira, toplam, 8)


def _kart(x, y, w, h, baslik="", rozet=None, satir=0, alt="", vurgu=False):
    """Galzura'daki içerik kartı: rozet, başlık, gri satırlar, alt bilgi."""
    g = ['<rect x="%d" y="%d" width="%d" height="%d" rx="8" fill="%s" stroke="%s" '
         'stroke-width="1"/>' % (x, y, w, h, PANEL2, KIRMIZI if vurgu else CIZGI)]
    iy = y + 26
    bx, bg = x + 14, 0
    if rozet:
        et, rk = rozet
        bg = 8 + len(et) * 7
        g.append('<rect x="%d" y="%d" width="%d" height="18" rx="4" fill="%s" '
                 'opacity=".22"/>' % (bx, iy - 13, bg, rk))
        g.append('<text x="%d" y="%d" font-family="Space Mono,monospace" font-size="9" '
                 'font-weight="700" fill="%s">%s</text>' % (bx + 6, iy, rk, _k(et)))
    sinir = y + h - (30 if alt else 10)
    if baslik:
        # Rozetin altına sığmıyorsa başlık rozetin yanına geçiyor; kart alçak
        # diye başlık kaybolmuyor, alt bilgi çizgisine de binmiyor.
        yan = bool(rozet) and (iy + 26) > sinir
        tx = bx + bg + 10 if yan else bx
        ty = iy + (26 if (rozet and not yan) else 0)
        en = max(6, int((x + w - 14 - tx) / 6.5))
        satirlar = _bol(str(baslik), en)[:2]
        for si, st in enumerate(satirlar):
            if ty > sinir:
                break
            g.append('<text x="%d" y="%d" font-family="Manrope,sans-serif" font-size="12.5" '
                     'fill="%s">%s</text>' % (tx, ty, KEMIK, _k(st)))
            ty += 16
        iy = max(iy + 26, ty) if not yan else max(iy + 26, ty)
    elif rozet:
        iy += 26
    # Alt bilgi çizgisine çarpmadan kaç satır sığıyorsa o kadar.
    tavan = (y + h - (32 if alt else 12)) - iy
    satir = max(0, min(satir, int(tavan // 11)))
    for i in range(satir):
        gen = w - 28 - (i % 3) * 22
        g.append('<rect x="%d" y="%d" width="%d" height="5" rx="2.5" fill="%s" '
                 'opacity="%.2f"/>' % (x + 14, iy, gen, GRI, 0.45 - i * 0.045))
        iy += 11
    if alt:
        g.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s"/>'
                 % (x + 14, y + h - 26, x + w - 14, y + h - 26, CIZGI))
        g.append('<text x="%d" y="%d" font-family="Manrope,sans-serif" font-size="9.5" '
                 'fill="%s">%s</text>' % (x + 14, y + h - 12, GRI, _k(alt)))
    return "".join(g)


def _satir_kart(x, y, w, ad, sag, oran, rakam=None, sonuk=False):
    """Galzura'daki performans satırı: avatar, ad, çubuk, sağ etiket, rakam."""
    o = ".38" if sonuk else "1"
    renk = KIRMIZI if not sonuk else GRI
    # Sağdaki büyük rakam ne kadar yer kaplıyorsa etiket o kadar geri çekiliyor;
    # kalan yere sığmayan etiket kısaltılıyor. Çakışma böyle bitiyor.
    rk_g = 0 if rakam is None else int(len(str(rakam)) * 12) + 16
    ad_g = int(len(str(ad)) * 6.7)
    et_bit = w - 16 - rk_g
    bosluk = et_bit - (50 + ad_g + 12)
    et = str(sag or "")
    if bosluk < 24:
        et = ""
    else:
        maks = int(bosluk / 5.4)
        if len(et) > maks:
            et = et[:max(1, maks - 1)].rstrip() + "\u2026"
    g = ['<g opacity="%s">' % o,
         '<rect x="%d" y="%d" width="%d" height="52" rx="8" fill="%s" stroke="%s"/>'
         % (x, y, w, PANEL2, CIZGI),
         '<circle cx="%d" cy="%d" r="13" fill="none" stroke="%s"/>'
         % (x + 26, y + 26, renk),
         '<text x="%d" y="%d" font-family="Manrope,sans-serif" font-size="11" '
         'text-anchor="middle" fill="%s">%s</text>' % (x + 26, y + 30, renk, _k(ad[:1])),
         '<text x="%d" y="%d" font-family="Manrope,sans-serif" font-size="12.5" '
         'fill="%s">%s</text>' % (x + 50, y + 22, KEMIK, _k(ad))]
    if et:
        g.append('<text x="%d" y="%d" font-family="Manrope,sans-serif" font-size="10" '
                 'text-anchor="end" fill="%s">%s</text>'
                 % (x + et_bit, y + 22, GRI, _k(et)))
    cw = max(40, w - 62 - rk_g - 12)
    g.append('<rect x="%d" y="%d" width="%d" height="5" rx="2.5" fill="%s" opacity=".3"/>'
             % (x + 50, y + 32, cw, GRI))
    if oran > 0:
        g.append('<rect x="%d" y="%d" width="0" height="5" rx="2.5" fill="%s">'
                 '<animate attributeName="width" values="0;%d" dur="1.1s" '
                 'begin="0.3s" fill="freeze"/></rect>'
                 % (x + 50, y + 32, KIRMIZI, int(cw * oran)))
    if rakam is not None:
        g.append('<text x="%d" y="%d" font-family="Bricolage Grotesque,sans-serif" '
                 'font-weight="800" font-size="22" text-anchor="end" fill="%s">%s</text>'
                 % (x + w - 16, y + 34, renk, _k(rakam)))
    g.append("</g>")
    return "".join(g)


def _serp(x, y, w, baslik, adres, aciklama, ilk=False, cizgi=0):
    """Arama sonucu satırı kurgusu."""
    g = []
    if ilk:
        g.append('<rect x="%d" y="%d" width="%d" height="58" rx="6" fill="%s" '
                 'opacity=".10"/>' % (x - 8, y - 16, w + 16, KIRMIZI))
    g.append('<text x="%d" y="%d" font-family="Manrope,sans-serif" font-size="9.5" '
             'fill="%s">%s</text>' % (x, y - 2, GRI, _k(adres)))
    g.append('<text x="%d" y="%d" font-family="Manrope,sans-serif" font-size="13" '
             'fill="%s">%s</text>' % (x, y + 16, KIRMIZI if ilk else KEMIK, _k(baslik)))
    if aciklama:
        g.append('<text x="%d" y="%d" font-family="Manrope,sans-serif" font-size="10" '
                 'fill="%s">%s</text>' % (x, y + 32, GRI, _k(aciklama)))
    for i in range(cizgi):
        g.append('<rect x="%d" y="%d" width="%d" height="4.5" rx="2.2" fill="%s" '
                 'opacity=".26"/>' % (x, y + 26 + i * 10, w - 30 - i * 46, GRI))
    return "".join(g)


def _kare(x, y, w, h, etiket="", isaret=False):
    """Video/plan karesi. Ortadaki işaret boş daire değil, görsel simgesi."""
    g = ['<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="%s" stroke="%s"/>'
         % (x, y, w, h, PANEL2, CIZGI)]
    gw = max(16, int(min(w, h) * 0.46))
    gh = max(12, int(gw * 0.74))
    gx, gy = x + (w - gw) // 2, y + (h - gh) // 2 - (5 if etiket else 0)
    if isaret:
        g.append('<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="none" '
                 'stroke="%s" stroke-width="1.2" opacity=".9"/>' % (gx, gy, gw, gh, YESIL))
        g.append('<path d="M%d %d l%d %d l%d %d" fill="none" stroke="%s" '
                 'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
                 % (gx + gw // 4, gy + gh // 2, gw // 6, gh // 4, gw // 2, -gh // 2, YESIL))
    else:
        g.append('<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="none" '
                 'stroke="%s" stroke-width="1.2"/>' % (gx, gy, gw, gh, GRI))
        g.append('<circle cx="%d" cy="%d" r="%d" fill="%s" opacity=".75"/>'
                 % (gx + gw - gw // 4, gy + gh // 3, max(1, gw // 10), GRI))
        g.append('<path d="M%d %d l%d %d l%d %d l%d %d" fill="none" stroke="%s" '
                 'stroke-width="1.4" stroke-linejoin="round" opacity=".8"/>'
                 % (gx + 3, gy + gh - 4, gw // 4, -gh // 3, gw // 5, gh // 5,
                    gw // 3, -gh // 2, GRI))
    if etiket:
        # Etiket kareye sığmıyorsa önce küçülüyor, sonra kısalıyor. Taşma yok.
        en = max(6.0, float(w - 10))
        punto = 8.5
        if len(etiket) * 5.0 > en:
            punto = max(6.4, en / (len(etiket) * 0.59))
        maks = int(en / (punto * 0.59))
        et = etiket if len(etiket) <= maks else etiket[:max(1, maks - 1)].rstrip() + "\u2026"
        g.append('<text x="%d" y="%d" font-family="Space Mono,monospace" font-size="%.1f" '
                 'text-anchor="middle" fill="%s">%s</text>'
                 % (x + w // 2, y + h - 9, punto, GRI, _k(et)))
    return "".join(g)


def _sayac(sira, toplam, ad):
    return ('<text x="46" y="316" font-family="Space Mono,monospace" font-size="9.5" '
            'letter-spacing="2" fill="%s" opacity=".5">%02d / %02d — %s</text>'
            % (GRI, sira + 1, toplam, ad.upper()))


# ------------------------------------------------------------------ bölümler
SAG = 306          # sağ sütunun sol kenarı (sol sütun 46-286 arası)
SAG_G = 300        # sağ sütun genişliği

HIZMET = {

 "insaat-3d-modelleme": ("İNŞAAT 3D", [
   ("Proje bitmeden", "Kat planı ve teknik çizim geliyor;", "biz onu satılabilir görsele çeviriyoruz.",
    lambda: _kart(SAG, 96, SAG_G, 150, "Blok A — kat planı", ("DWG", SARI), 4,
                  "teslim alındı · 06.07.2026")),
   ("Render seti", "Dış cephe, iç mekân, gece — hepsi", "aynı modelden çıkıyor.",
    lambda: ((lambda x: _kare(x[0], 96, 96, 74, "dış cephe") +
                        _kare(x[1], 96, 96, 74, "iç mekân") +
                        _kare(x[2], 96, 96, 74, "gece"))(_dagit(3, 96)) +
             _kart(SAG, 184, SAG_G, 62, "6–10 görsel + 45 sn animasyon", None, 1,
                   "tek modelden, ek ücret yok"))),
   ("Satış başlıyor", "İlan, katalog ve sosyal medya", "aynı setten besleniyor.",
    lambda: (_satir_kart(SAG, 100, SAG_G, "İlan görüntülenme", "ilk hafta", 0.82, "3.4x") +
             _satir_kart(SAG, 162, SAG_G, "Randevu talebi", "ilk hafta", 0.55, "2.1x") +
             _kart(SAG, 224, SAG_G, 34, None, None, 0,
                   "rakamlar örnektir — sizinki ölçülerek yazılır"))),
 ]),

 "urun-animasyon": ("ÜRÜN ANİMASYONU", [
   ("Ürünü anlatmak zor", "Fotoğraf içini göstermiyor,", "katalog kimse okumuyor.",
    lambda: ((lambda x: _kart(x[0], 96, 142, 116, "ürün-01.jpg", ("JPG", GRI), 3, "durağan") +
                        _kart(x[1], 96, 142, 116, "katalog.pdf", ("PDF", GRI), 4, "18 sayfa"))(_dagit(2, 142)))),
   ("Kesit ve akış", "Modeli açıyoruz: içeride ne var,", "nasıl çalışıyor, neden önemli.",
    lambda: ((lambda x: _kare(x[0], 96, 92, 76, "dış görünüm") + _kare(x[1], 96, 92, 76, "kesit", True) +
                        _kare(x[2], 96, 92, 76, "çalışma"))(_dagit(3, 92)) +
             _satir_kart(SAG, 186, SAG_G, "Anlatım süresi", "hedef", 0.6, "60 sn"))),
   ("Tek üretim, çok sürüm", "Aynı animasyondan dil ve format", "sürümleri birlikte çıkıyor.",
    lambda: ((lambda x: _kart(x[0], 92, 90, 92, "TR", ("SES", KIRMIZI), 0, "yatay") +
                        _kart(x[1], 92, 90, 92, "EN", ("SES", KIRMIZI), 0, "kare") +
                        _kart(x[2], 92, 90, 92, "DE", ("SES", KIRMIZI), 0, "dikey"))(_dagit(3, 90)) +
             _kart(SAG, 198, SAG_G, 58, "Fuar · site · sosyal medya · bayi sunumu",
                   None, 0, "tek üretimden hepsi"))),
 ]),

 "klip-cekimi": ("KLİP ÇEKİMİ", [
   ("Önce plan", "Çekim gününe hangi planların", "çekileceği yazılı gidiyor.",
    lambda: _kart(SAG, 96, SAG_G, 150, "Çekim planı — 24 plan", ("PDF", SARI), 5,
                  "onaylandı · çekimden 3 gün önce")),
   ("Çekim ve kurgu", "Ritim kurguda kuruluyor;", "renk ve ses ayrı ayrı çalışılıyor.",
    lambda: ("".join(_kare(x, 100, 52, 46, "", i == 2) for i, x in enumerate(_dagit(5, 52))) +
             _satir_kart(SAG, 160, SAG_G, "Kurgu", "ritim ve tempo", 0.78, None) +
             _satir_kart(SAG, 214, SAG_G, "Renk + ses", "tek palet", 0.62, None))),
   ("Üç format birden", "Yatay, kare ve dikey aynı", "çekimden çıkıyor.",
    lambda: (_kare(SAG, 96, 132, 86, "16:9 · YouTube") + _kare(SAG + 145, 96, 86, 86, "1:1 · feed") +
             _kare(SAG + 244, 96, 56, 86, "9:16") +
             _kart(SAG, 200, SAG_G, 50, "İkinci mecra için yeniden çekim yok",
                   None, 0, ""))),
 ]),

 "drone-fpv": ("DRONE & FPV", [
   ("Yerden görünmeyen", "Bina, arazi ve şantiye yerden", "anlatılamıyor.",
    lambda: (_kart(SAG, 96, SAG_G, 92, "Yer seviyesi çekim", None, 3,
                   "sınırlı açı") +
             _kart(SAG, 200, SAG_G, 46, "Ölçek ve konum görünmüyor", None, 1, ""))),
   ("Tek planda geçiş", "FPV ile dışarıdan içeri, sonra", "tepeye — kesme yok.",
    lambda: ('<path d="M%d 176 C %d 176, %d 104, %d 122 S %d 168, %d 112" '
             'fill="none" stroke="%s" stroke-width="2" stroke-linecap="round" '
             'stroke-dasharray="400" stroke-dashoffset="400">'
             '<animate attributeName="stroke-dashoffset" values="400;0" dur="2.2s" '
             'begin="0.3s" fill="freeze"/></path>'
             % (SAG + 12, SAG + 70, SAG + 96, SAG + 158, SAG + 226, SAG + 288, KIRMIZI) +
             '<circle r="4.5" fill="%s"><animateMotion dur="2.2s" begin="0.3s" '
             'fill="freeze" path="M%d 176 C %d 176, %d 104, %d 122 S %d 168, %d 112"/>'
             '</circle>' % (KIRMIZI, SAG + 12, SAG + 70, SAG + 96, SAG + 158,
                            SAG + 226, SAG + 288) +
             '<text x="%d" y="%d" font-family="Space Mono,monospace" font-size="9" '
             'fill="%s">dış cephe</text>' % (SAG + 4, 196, GRI) +
             '<text x="%d" y="%d" font-family="Space Mono,monospace" font-size="9" '
             'text-anchor="middle" fill="%s">iç mekân</text>' % (SAG + 150, 96, GRI) +
             '<text x="%d" y="%d" font-family="Space Mono,monospace" font-size="9" '
             'text-anchor="end" fill="%s">tepe</text>' % (SAG + SAG_G, 134, GRI) +
             _kart(SAG, 210, SAG_G, 46, "Tek çekim · kesmesiz geçiş", None, 0, ""))),
   ("İzin ve güvenlik", "Uçuşa yasak bölge çekimden", "önce kontrol ediliyor.",
    lambda: (_satir_kart(SAG, 100, SAG_G, "Bölge kontrolü", "yapıldı", 1.0, "✓") +
             _satir_kart(SAG, 158, SAG_G, "Yedek gün", "planlandı", 1.0, "✓") +
             _satir_kart(SAG, 216, SAG_G, "Ham kayıt", "teslim", 0.0, None, True))),
 ]),

 "emlak-kurumsal": ("EMLAK & KURUMSAL", [
   ("İlan fotoğrafı yetmiyor", "Alıcı mekânı gezemeyince", "randevuya gelmiyor.",
    lambda: ("".join(_kare(x, 100, 68, 60, "foto %d" % (i + 1)) for i, x in enumerate(_dagit(4, 68))) +
             _kart(SAG, 176, SAG_G, 70, "Ölçü, akış ve ışık anlaşılmıyor", None, 2, ""))),
   ("Video tur", "Girişten çıkışa tek akış;", "mekân gerçekten geziliyor.",
    lambda: (_kare(SAG, 96, SAG_G, 118, "") +
             '<polygon points="%d,150 %d,178 %d,164" fill="%s"/>'
             % (SAG + 158, SAG + 158, SAG + 186, KIRMIZI) +
             _satir_kart(SAG, 226, SAG_G, "Portföy başına tur", "aylık paket", 0.7, None))),
   ("Talep artıyor", "Aynı çekimden ilan, sosyal", "medya ve sunum çıkıyor.",
    lambda: (_satir_kart(SAG, 100, SAG_G, "İlan görüntülenme", "video eklendikten sonra",
                         0.85, "↑") +
             _satir_kart(SAG, 158, SAG_G, "Mesaj / arama", "aynı dönem", 0.6, "↑") +
             _kart(SAG, 216, SAG_G, 40, None, None, 0,
                   "yön göstergesidir — sizinki ölçülerek yazılır"))),
 ]),

 "dugun-etkinlik": ("DÜĞÜN & ETKİNLİK", [
   ("Gün bir kez yaşanıyor", "Telefon kayıtları dağınık,", "kimse baştan sona izlemiyor.",
    lambda: ("".join(_kare(_dagit(4, 68)[i % 4], 100 + (i // 4) * 66, 68, 56, "") for i in range(8)))),
   ("Kurgu", "Saatlerce görüntü üç dakikaya", "iniyor — hikâye sırasıyla.",
    lambda: ("".join(_kare(x, 100, 52, 46, "", i == 1) for i, x in enumerate(_dagit(5, 52))) +
             _satir_kart(SAG, 160, SAG_G, "Kurgu ritmi", "3 dakika", 0.75, None) +
             _satir_kart(SAG, 214, SAG_G, "Müzik ve ses", "sahneye göre", 0.55, None))),
   ("Ömür boyu kalan", "Uzun film, kısa sürüm ve", "sosyal medya kesitleri.",
    lambda: (_kare(SAG, 96, 132, 86, "film · 3 dk") + _kare(SAG + 145, 96, 86, 86, "özet · 60 sn") +
             _kare(SAG + 244, 96, 56, 86, "Reels") +
             _kart(SAG, 200, SAG_G, 50, "Master dosya sizde kalıyor", None, 0, ""))),
 ]),

 "isletme-tanitim": ("İŞLETME TANITIM", [
   ("Ayda bir hatırlanmak", "Tek video bir hafta konuşulur,", "sonra sessizlik.",
    lambda: (_satir_kart(SAG, 100, SAG_G, "Ocak — 1 paylaşım", "sonra ara", 0.2, None) +
             _satir_kart(SAG, 158, SAG_G, "Şubat", "paylaşım yok", 0.0, None, True) +
             _satir_kart(SAG, 216, SAG_G, "Mart", "paylaşım yok", 0.0, None, True))),
   ("Bir çekim günü", "Bir günde çekilen malzeme", "bir aya yayılıyor.",
    lambda: (_kart(SAG, 96, SAG_G, 74, "Çekim günü — 1 gün", ("PLAN", KIRMIZI), 2,
                   "12 içerik çıkacak") +
             "".join(_kare(x, 182, 52, 46, "") for x in _dagit(5, 52)))),
   ("Süren görünürlük", "Her hafta yeni içerik;", "hesap durmuyor.",
    lambda: ("".join(_kare(_dagit(5, 52)[i % 5], 96 + (i // 5) * 56, 52, 46,
                           "", i in (0, 3, 6, 9)) for i in range(10)) +
             _kart(SAG, 214, SAG_G, 42, "Aylık düzen — en az 3 ay önerilir",
                   None, 1, ""))),
 ]),

 "seo-icerik": ("SEO VE İÇERİK", [
   ("Sayfa var, görünürlük yok", "331 sayfamız vardı; Google", "yalnızca 24'ünü biliyordu.",
    lambda: (_kart(SAG, 96, SAG_G, 84, "Site haritası", ("XML", SARI), 2,
                   "son okuma: 5 Temmuz") +
             _satir_kart(SAG, 192, SAG_G, "Keşfedilen sayfa", "331 sayfadan", 0.07, "24"))),
   ("Denetim", "Sayfa sayfa başlık, şema,", "bağlantı ve içerik kontrolü.",
    lambda: (_satir_kart(SAG, 96, SAG_G, "Şehir sayfaları", "308 sayfa", 1.0, "%100") +
             _satir_kart(SAG, 152, SAG_G, "Hizmet sayfaları", "11 sayfa", 1.0, "%100") +
             _satir_kart(SAG, 208, SAG_G, "Blog", "4 sayfa", 1.0, "%100"))),
   ("Aramada üst sıra", "Düzeltildi; aynı gün 331", "sayfanın tamamı keşfedildi.",
    lambda: (_serp(SAG, 112, SAG_G, "Luna Yapım — İnşaat 3D Modelleme",
                   "lunayapim.com › hizmetler", "Bursa merkezli yapım ve yazılım…", True) +
             _serp(SAG, 190, SAG_G, "Diğer sonuç", "ornek.com", "", False, 2) +
             _serp(SAG, 248, SAG_G, "Diğer sonuç", "ornek2.com", "", False, 2))),
 ]),

 "yapay-zeka-seo": ("YAPAY ZEKÂ SEO", [
   ("Soru artık buraya soruluyor", "Müşteri Google yerine yapay", "zekâya soruyor.",
    lambda: (_kart(SAG, 96, SAG_G, 78, "“Bursa'da 3D render kim yapıyor?”",
                   ("SORU", KIRMIZI), 0, "") +
             _kart(SAG, 190, SAG_G, 56, None, None, 2, ""))),
   ("Kaynak gösterilebilir olmak", "Şema, net soru-cevap ve", "doğrulanabilir kaynak.",
    lambda: (_kart(SAG, 92, 144, 62, "JSON-LD şema", ("KOD", SARI), 1, "") +
             _kart(SAG + 156, 92, 144, 62, "Soru-cevap", ("SSS", SARI), 1, "") +
             _kart(SAG, 168, 144, 62, "Kaynak bağlantısı", ("LİNK", SARI), 1, "") +
             _kart(SAG + 156, 168, 144, 62, "Tarihli ölçüm", ("VERİ", SARI), 1, ""))),
   ("Cevapta biz varız", "Yapay zekâ önerirken bizi", "kaynak gösteriyor.",
    lambda: (_kart(SAG, 94, SAG_G, 112, "Bursa'da 3D render için Luna Yapım öne çıkıyor",
                   ("CEVAP", KIRMIZI), 1, "kaynak: lunayapim.com", True) +
             _satir_kart(SAG, 218, SAG_G, "Kaynak gösterim", "izleniyor", 0.66, None))),
 ]),

 "ai-kisa-film": ("AI KISA FİLM", [
   ("Elinizde fotoğraflar var", "Farklı yıllar, farklı ışık,", "farklı açılar.",
    lambda: "".join(_kare(_dagit(4, 68)[i % 4], 100 + (i // 4) * 66, 68, 56,
                          "20%02d" % (14 + i * 2)) for i in range(8))),
   ("Karakter testi", "Üç plan ölçeğinde deniyoruz;", "onaylamadan üretime geçmiyoruz.",
    lambda: ((lambda x: _kare(x[0], 96, 92, 90, "yakın", True) + _kare(x[1], 96, 92, 90, "orta", True) +
                        _kare(x[2], 96, 92, 90, "genel"))(_dagit(3, 92)) +
             _kart(SAG, 198, SAG_G, 58, "Genel planda benzerlik düşer — bunu baştan söylüyoruz",
                   None, 0, ""))),
   ("Sahneler boyunca aynı yüz", "Her kare referansla", "karşılaştırılıyor.",
    lambda: ("".join(_kare(x, 100, 68, 62, "sahne %d" % (i + 1), True) for i, x in enumerate(_dagit(4, 68))) +
             _satir_kart(SAG, 180, SAG_G, "Yüz denetimi", "sapan kare yeniden üretilir",
                         0.9, "✓") +
             _kart(SAG, 238, SAG_G, 36, None, None, 0,
                   "%100 değil — yakın ve orta planda en iyi sonuç"))),
 ]),
}


# ------------------------------------------------------------------ üretim
def uret(anahtar):
    v = HIZMET.get(anahtar)
    if not v:
        return None
    ad, bolumler = v
    n = len(bolumler)
    parcalar = []
    for i, (baslik, a1, a2, ciz) in enumerate(bolumler):
        ic = _sol(i + 1, n, baslik, a1, a2, i)
        ic += _girisli(ciz(), 0.35, i, n, 12)
        ic += _girisli(_sayac(i, n, ad), 0.55, i, n, 5)
        parcalar.append(_gorunurluk(i, n, ic))
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" '
            'aria-label="%s hizmetinin nasıl çalıştığını anlatan animasyon" '
            'style="width:100%%;height:auto;display:block">'
            '<style>@media (prefers-reduced-motion: reduce){* {animation:none!important;'
            'opacity:1!important}}</style>'
            '<rect width="%d" height="%d" fill="%s"/>'
            '<rect x="10" y="10" width="%d" height="%d" rx="10" fill="%s" stroke="%s"/>'
            '%s</svg>'
            % (G, Y, _k(ad), G, Y, MUREKKEP, G - 20, Y - 20, PANEL, CIZGI,
               "".join(parcalar)))


def hepsini_yaz(site_kok):
    klasor = os.path.join(site_kok, "assets", "animasyon")
    os.makedirs(klasor, exist_ok=True)
    out = []
    for a in HIZMET:
        s = uret(a)
        with open(os.path.join(klasor, a + ".svg"), "w", encoding="utf-8") as f:
            f.write(s)
        out.append((a, len(s)))
    return out


def sayfaya_ekle(html, anahtar, kok=""):
    """Hizmet sayfasına tanıtım videosunu gömer.

    Video ekrana girmeden indirilmiyor (preload="none" + video.js), "hareketi
    azalt" ayarı açıksa hiç oynamıyor; afiş karesi kalıyor.
    """
    if anahtar not in HIZMET or 'class="hizmet-animasyon"' in html:
        return html, False
    i = html.find('class="page-hero"')
    if i < 0:
        return html, False
    j = html.find("<section", i)
    if j < 0:
        return html, False
    blok = ('\n<div class="wrap hizmet-animasyon" style="margin:28px auto 0">\n'
            '  <video data-luna muted loop playsinline preload="none"\n'
            '         poster="%sassets/video/%s.jpg"\n'
            '         style="width:100%%;height:auto;border-radius:10px;display:block"\n'
            '         aria-label="%s — nasıl çalıştığını anlatan kısa tanıtım videosu">\n'
            '    <source src="%sassets/video/%s.webm" type="video/webm">\n'
            '    <source src="%sassets/video/%s.mp4" type="video/mp4">\n'
            '  </video>\n</div>\n'
            % (kok, anahtar, _k(HIZMET[anahtar][0]), kok, anahtar, kok, anahtar))
    return html[:j] + blok + html[j:], True
