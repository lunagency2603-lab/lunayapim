# -*- coding: utf-8 -*-
"""
TrendSaphiens içerik biçimleri ve vitrin bileşenleri (12.10.2026).

Biçimler (veri/icerik/<slug>.json):
  liste  — numaralı maddeler; her maddede başlık, 2-4 cümle, isteğe bağlı resmî YouTube klibi
  test   — kişilik testi; 5-8 soru, 3-4 şık, 3-6 sonuç (her şık bir sonuca puan verir)
  bilgi  — bilgi testi; doğru cevap + açıklama, yüzdeye göre derece
  anket  — tek soru, 2-8 seçenek, bağlam paragrafları

Ortak alanlar: tur, slug, tarih, kat, baslik, meta, giris, kapak{emoji}, kaynaklar[{ad,url?}],
  isteğe bağlı: guncelleme, editor_notu.
Bütün soru, şık ve sonuç metinleri sayfada düz HTML olarak basılır (JS kapalıyken de okunur).
"""
import glob, html, json, os, re

from .ayarlar import KOK_DIZIN
from . import editor as ED

DIZIN = os.path.join(KOK_DIZIN, "veri", "icerik")
BICIM_AD = {"liste": "Liste", "test": "Test", "bilgi": "Bilgi testi", "anket": "Anket"}
KAT_EMOJI = {"haber": "📰", "ekran": "🎬", "spor": "⚽", "muzik": "🎧", "burc": "🔮", "teknoloji": "💡",
             "piyasa": "💱", "sanat": "🎨", "edebiyat": "📚", "sosyal-medya": "📱", "gundem": "🗞️",
             "aranan": "🔎", "muhendislik": "⚙️"}
BICIM_EMOJI = {"test": "🧩", "bilgi": "🧠", "anket": "📊", "liste": "📋"}
TEPKILER = [("begen", "👍", "Beğendim"), ("gul", "😂", "Güldüm"), ("sasir", "😮", "Şaşırdım"),
            ("uzul", "😢", "Üzüldüm"), ("kiz", "😠", "Kızdım"), ("dusun", "🤔", "Düşündürdü")]


def _e(x):
    return html.escape(str(x or ""), quote=True)


def _yt_id(x):
    m = re.search(r"(?:v=|youtu\.be/|embed/)?([A-Za-z0-9_-]{11})", str(x or ""))
    return m.group(1) if m else ""


# ------------------------------------------------------------------ veri
def hepsi():
    out = []
    for f in sorted(glob.glob(os.path.join(DIZIN, "*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception as ex:
            print("biçim okunamadı %s: %s" % (f, ex))
            continue
        if d.get("tur") not in BICIM_AD or not d.get("slug") or not d.get("baslik"):
            continue
        out.append(d)
    return out


def akis_maddeleri():
    """trend._hepsi() için kart sözlükleri."""
    ci = []
    for d in hepsi():
        ci.append({"tur": "bicim", "bicim": d["tur"], "tarih": d["tarih"], "sira": 0, "kat": d.get("kat", "haber"),
                   "baslik": d["baslik"], "olgu": d.get("meta") or d.get("giris", ""), "slug": d["slug"],
                   "gorsel": None, "kapak": d.get("kapak") or {}, "veri": d,
                   "sektor": BICIM_AD[d["tur"]], "aci": " ".join(_metinler(d))})
    return ci


def _metinler(d):
    """Sayfada okunan bütün metin (kelime sayısı ve okuma süresi için)."""
    t = []

    def ekle(x):
        if isinstance(x, str):
            t.append(x)
        elif isinstance(x, list):
            for y in x:
                ekle(y)
        elif isinstance(x, dict):
            for k in ("baslik", "metin", "soru", "aciklama", "secenekler"):
                if k in x:
                    ekle(x[k] if k != "secenekler" or not x[k] or isinstance(x[k][0], str) else [c.get("metin") for c in x[k]])
    ekle(d.get("giris")); ekle(d.get("maddeler", [])); ekle(d.get("sorular", []))
    ekle(list((d.get("sonuclar") or {}).values())); ekle(d.get("derece", [])); ekle(d.get("baglam", []))
    ekle(d.get("kapanis", [])); ekle(d.get("soru")); ekle(d.get("secenekler", []) if d.get("tur") == "anket" else [])
    return [x for x in t if x]


def kelime(d):
    return len(re.findall(r"\w+", " ".join(_metinler(d))))


# ------------------------------------------------------------------ kapak ve kart
def gorsel_var(m, tekrar_mi=None):
    g = str(m.get("gorsel") or "")
    if not g.startswith("ts:"):
        return False
    return not (tekrar_mi and tekrar_mi(m))


def kapak_html(m, on="../", tekrar_mi=None, etiket=True):
    kat = m.get("kat") or "haber"
    bic = m.get("bicim")
    renk = "var(--k-%s)" % (bic if bic in ("test", "bilgi", "anket") else kat)
    tur = ('<span class="v-tur%s">%s</span>' % (" test" if bic in ("test", "bilgi") else "", BICIM_AD[bic])) if bic and etiket else ""
    if gorsel_var(m, tekrar_mi):
        return ('<div class="v-kapak gorselli">%s<img src="%sassets/ts/%s" alt="%s" loading="lazy" width="960" height="540"></div>'
                % (tur, on, _e(m["gorsel"][3:]), _e(m.get("baslik"))))
    emoji = (m.get("kapak") or {}).get("emoji") or BICIM_EMOJI.get(bic) or KAT_EMOJI.get(kat, "✦")
    from .trend import KATEGORI
    return ('<div class="v-kapak" style="--kr:%s">%s<i aria-hidden="true">%s</i><em>%s</em></div>'
            % (renk, tur, emoji, _e(KATEGORI.get(kat, ("",))[0])))


def kart_html(m, on="../", tr="", tekrar_mi=None, ozet=True):
    from .trend import KATEGORI, _tr_tarih
    url = tr + m["slug"] if m.get("slug") else tr + m.get("url", "")
    bic = m.get("bicim")
    cta = '<span class="v-cta">%s →</span>' % ("Testi çöz" if bic in ("test", "bilgi") else "Oy ver") if bic in ("test", "bilgi", "anket") else ""
    alt = '<span class="v-kart-alt"><span>%s</span></span>' % _e(_tr_tarih(m["tarih"][:10])) if not cta else cta
    return ('<a class="v-kart%s" href="%s">%s<div class="v-kart-metin"><small>%s</small><h3>%s</h3>%s%s</div></a>'
            % (" test" if bic in ("test", "bilgi") else "", _e(url), kapak_html(m, on, tekrar_mi),
               _e(KATEGORI.get(m.get("kat"), ("Gündem",))[0]), _e(m["baslik"]),
               ('<p>%s</p>' % _e(_kisa(m.get("olgu"), 120))) if ozet else "", alt))


def _kisa(t, n):
    t = re.sub(r"\s+", " ", str(t or "")).strip()
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + "…"


# ------------------------------------------------------------------ ortak modüller
def tepki_html():
    return ('<section class="ts-tepki" data-tepki><h2>Bu içeriğe tepkin ne?</h2><div class="ts-tepki-izgara">%s</div></section>'
            % "".join('<button type="button" data-t="%s" aria-label="%s"><span>%s</span><small>%s</small><b>0</b></button>'
                      % (k, a, e, a) for k, e, a in TEPKILER))


def ilgili_html(m, havuz, on="../", tr="", tekrar_mi=None, n=3):
    """3 ilgili kart: aynı bölümden 2 yazı + 1 test (Onedio'da okuru tutan düzen)."""
    aday = [k for k in havuz if k is not m and k.get("slug") != m.get("slug") and k.get("tur") in ("haber", "rehber", "bicim")]
    ayni = [k for k in aday if k.get("kat") == m.get("kat") and k.get("bicim") not in ("test", "bilgi")]
    testler = [k for k in aday if k.get("bicim") in ("test", "bilgi")]
    sec = ayni[:n - 1] + testler[:1]
    for k in aday:
        if len(sec) >= n:
            break
        if k not in sec:
            sec.append(k)
    if not sec:
        return ""
    return ('<section class="ts-ilgili"><h2>Bunlar da ilgini çekebilir</h2><div class="v-izgara v-izgara-3">%s</div></section>'
            % "".join(kart_html(k, on, tr, tekrar_mi, ozet=False) for k in sec[:n]))


def populer_html(havuz, tr="", baslik="En çok okunanlar"):
    """Sunucu tarafında son 6 yazı basılır; okuma sayacından veri gelince JS gerçek listeyle değiştirir."""
    from .trend import KATEGORI
    yedek = [k for k in havuz if k.get("tur") in ("haber", "rehber", "bicim")][:6]
    sat = "".join('<li><a href="%s%s"><span>%02d</span><b>%s</b><small>%s</small></a></li>'
                  % (tr, _e(k["slug"]), i, _e(k["baslik"]), _e(KATEGORI.get(k.get("kat"), ("",))[0]))
                  for i, k in enumerate(yedek, 1))
    return ('<div class="v-kutu ts-populer" data-populer data-dizin="%sbaslik-dizin.json" data-on="%s"><h2>%s</h2><ol class="v-sirali">%s</ol></div>'
            % (tr, tr, _e(baslik), sat))


def anket_kutu_html(d):
    sec = d.get("secenekler", [])
    return ('<div class="ts-anket" data-anket="%s"><h3>%s</h3>%s<span class="ts-anket-toplam">Oy vermek için bir seçeneğe dokun</span></div>'
            % (_e(d["slug"]), _e(d.get("soru") or d["baslik"]),
               "".join('<button type="button" class="ts-anket-sec"><span>%s</span><span class="ts-anket-oran">%%0</span></button>' % _e(s) for s in sec)))


def yt_html(yid, baslik=""):
    yid = _yt_id(yid)
    if not yid:
        return ""
    # Hafif oynatıcı: önce kapak, tıklayınca youtube-nocookie iframe'i (sayfa hızı ve gizlilik)
    return ('<button type="button" class="ts-yt" style="background-image:url(https://i.ytimg.com/vi/%s/hqdefault.jpg)" '
            'onclick="this.innerHTML=\'<iframe src=&quot;https://www.youtube-nocookie.com/embed/%s?autoplay=1&quot; allow=&quot;autoplay; encrypted-media; picture-in-picture&quot; allowfullscreen title=&quot;%s&quot;></iframe>\';this.onclick=null" '
            'aria-label="%s videosunu oynat"><span>YouTube · resmî kanal</span></button>' % (yid, yid, _e(baslik), _e(baslik)))


# ------------------------------------------------------------------ biçim gövdeleri
def _paragraflar(x):
    if isinstance(x, list):
        return "".join("<p>%s</p>" % _e(p) for p in x if p)
    return "<p>%s</p>" % _e(x) if x else ""


def govde_liste(d):
    h = []
    for i, m in enumerate(d.get("maddeler", []), 1):
        h.append('<section class="ts-madde" id="m%d"><h2><span>%d.</span>%s</h2>' % (i, i, _e(m.get("baslik"))))
        if m.get("bilgi"):
            h.append('<p class="ts-madde-bilgi">%s</p>' % _e(m["bilgi"]))
        if m.get("youtube"):
            h.append(yt_html(m["youtube"], m.get("baslik")))
        h.append(_paragraflar(m.get("metin")))
        h.append("</section>")
    if d.get("kapanis"):
        h.append('<div class="ts-analiz">%s</div>' % _paragraflar(d["kapanis"]))
    return "".join(h)


def govde_test(d):
    sonuclar = d.get("sonuclar", {})
    h = ['<div class="ts-test" data-test>']
    for i, s in enumerate(d.get("sorular", []), 1):
        ad = "s%d" % i
        h.append('<fieldset class="ts-soru"><h2><span>%d.</span>%s</h2><div class="ts-siklar">%s</div></fieldset>'
                 % (i, _e(s["soru"]), "".join('<label><input type="radio" name="%s" value="%s"> %s</label>' % (ad, _e(c["sonuc"]), _e(c["metin"]))
                                             for c in s.get("secenekler", []))))
    h.append('<button type="button" class="ts-test-bitir" disabled>Sonucumu göster</button>')
    h.append('<div class="ts-test-sonuc" hidden aria-live="polite">')
    for k, v in sonuclar.items():
        h.append('<div data-sonuc="%s" hidden id="sonuc-%s"><span class="ts-sonuc-emoji">%s</span><span class="etk">Senin sonucun</span><h2>%s</h2>%s</div>'
                 % (_e(k), _e(k), _e(v.get("emoji", "✦")), _e(v["baslik"]), _paragraflar(v.get("metin"))))
    h.append('<button type="button" class="ts-test-tekrar">Testi yeniden çöz</button></div></div>')
    h.append('<details class="ts-tum-sonuclar"><summary>Bu testin bütün sonuçları</summary>%s</details>'
             % "".join("<h3>%s %s</h3>%s" % (_e(v.get("emoji", "")), _e(v["baslik"]), _paragraflar(v.get("metin"))) for v in sonuclar.values()))
    return "".join(h)


def govde_bilgi(d):
    h = ['<div class="ts-test" data-bilgi>']
    for i, s in enumerate(d.get("sorular", []), 1):
        ad = "b%d" % i
        h.append('<fieldset class="ts-soru" data-dogru="%d"><h2><span>%d.</span>%s</h2><div class="ts-siklar">%s</div>'
                 '<p class="ts-aciklama" hidden><b>Doğru cevap: %s.</b> %s</p></fieldset>'
                 % (int(s["dogru"]), i, _e(s["soru"]),
                    "".join('<label><input type="radio" name="%s" value="%d"> %s</label>' % (ad, j, _e(c)) for j, c in enumerate(s["secenekler"])),
                    _e(s["secenekler"][int(s["dogru"])]), _e(s.get("aciklama", ""))))
    h.append('<div class="ts-test-sonuc" hidden aria-live="polite"><span class="etk">Skorun</span><div class="ts-skor">0</div>')
    for dr in sorted(d.get("derece", []), key=lambda x: x["min"]):
        h.append('<div data-min="%d" hidden><h2>%s</h2>%s</div>' % (int(dr["min"]), _e(dr["baslik"]), _paragraflar(dr.get("metin"))))
    h.append("</div></div>")
    return "".join(h)


def govde_anket(d):
    return ('<div class="v-kutu" style="margin:22px 0">%s</div>%s'
            % (anket_kutu_html(d), "".join("<p>%s</p>" % _e(p) for p in d.get("baglam", []))))


GOVDE = {"liste": govde_liste, "test": govde_test, "bilgi": govde_bilgi, "anket": govde_anket}


def sayfa_html(d, havuz, tekrar_mi=None, taslak=False):
    """Bir biçim içeriğinin tam sayfası (trend._bas/_alt kabuğuyla)."""
    from . import trend as T
    m = [k for k in akis_maddeleri() if k["slug"] == d["slug"]][0]
    url = T.KOK_URL + ("taslak/" if taslak else "") + d["slug"]
    on, tr = ("../../", "../") if taslak else ("../", "")
    kat_ad = T.KATEGORI.get(d.get("kat"), ("Gündem",))[0]
    onayli = d["slug"] in ED.onaylar()
    yazar = ED.kisi_sema() if onayli else {"@type": "Organization", "name": "TrendSaphiens", "url": T.KOK_URL}
    sema = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": d["baslik"], "description": d.get("meta", ""), "url": url,
         "datePublished": d["tarih"], "dateModified": d.get("guncelleme") or d["tarih"], "inLanguage": "tr",
         "articleSection": kat_ad, "author": yazar,
         "publisher": {"@type": "Organization", "name": "TrendSaphiens", "url": T.KOK_URL,
                       "logo": {"@type": "ImageObject", "url": "https://lunayapim.com/assets/luna-logo.png"}}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "TrendSaphiens", "item": T.KOK_URL},
            {"@type": "ListItem", "position": 2, "name": kat_ad, "item": T.KOK_URL + d.get("kat", "haber") + "/"},
            {"@type": "ListItem", "position": 3, "name": d["baslik"], "item": url}]}]}
    sema_html = '<script type="application/ld+json">%s</script>' % json.dumps(sema, ensure_ascii=False)
    kaynak = d.get("kaynaklar") or []
    kaynak_html = ('<div class="ts-baglam"><h2>Kaynaklar</h2><ul class="ts-kaynaklar">%s</ul></div>'
                   % "".join("<li>%s%s</li>" % (_e(k["ad"]), (" — " + _e(k["not"])) if k.get("not") else "") for k in kaynak)) if kaynak else ""
    not_html = ('<p class="ts-not">%s</p>' % _e(d["editor_notu"])) if d.get("editor_notu") else ""
    govde = """
%s<article class="ts-yazi">
  <div class="wrap ts-yazi-izgara">
    <div class="ts-yazi-ana">
      <div class="crumbs"><a href="%s">TrendSaphiens</a> · <a href="%s%s/">%s</a> · %s</div>
      <span class="ts-chip">%s</span>
      <h1>%s</h1>
      <p class="ts-yazi-meta">%s · %d dk</p>
      %s
      <div class="ts-yazi-gorsel">%s</div>
      %s
      <p class="ts-giris">%s</p>
      %s
      %s
      %s
      %s
      %s
      %s
      %s
    </div>
    <aside class="ts-yan">
      %s
    </aside>
  </div>
</article>
""" % ('<div class="ts-taslak-serit">TASLAK — editör onayı bekliyor. Bu sayfa arama motorlarına kapalıdır.</div>' if taslak else "",
       tr or "./", tr, d.get("kat", "haber"), _e(kat_ad), _e(BICIM_AD[d["tur"]]),
       _e(BICIM_AD[d["tur"]]), _e(d["baslik"]), _e(T._tr_tarih(d["tarih"])), max(1, round(kelime(d) / 180)),
       ED.imza_html(d["slug"], tr), kapak_html(m, on, tekrar_mi, etiket=False), T._paylas(url, d["baslik"]),
       _e(d.get("giris", "")), GOVDE[d["tur"]](d), not_html, kaynak_html,
       ED.editor_kutu_html(d["slug"], tr), tepki_html(), ilgili_html(m, havuz, on, tr, tekrar_mi),
       ("" if taslak else T.REKLAM) if onayli else "",
       populer_html(havuz, tr))
    h = T._bas(T._sayfa_basligi(d["baslik"]), d.get("meta", ""), url, None, sema_html, "article", on, tr) + govde + T._alt(on, tr)
    h = h.replace("</head>", '<meta name="ts-editor" content="%s">\n</head>'
                  % ("onayli" if onayli else ("taslak" if taslak else "inceleme")), 1)
    if taslak:
        h = h.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n' + T.NOINDEX, 1)
    return h
