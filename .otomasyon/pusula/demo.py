# -*- coding: utf-8 -*-
"""
Otomatik demo üreteci.
Her aday için tek dosyalık, kendi kendine yeten bir HTML sunum çıkarır:
  · şu anki durum   · tespit edilen eksikler   · eksikler kapanırsa tahmin
  · Luna Yapım'ın önerdiği iş planı   · iletişim
Ayrıca WhatsApp'a yapıştırılabilir kısa bir açılış mesajı üretir.
"""
import os, re, html, json, datetime
from .ayarlar import CIKTI, SEKTORLER
from . import fark as FK
from . import ornek as OR
from . import referans as RF
from .puanlama import karne, en_zayif_grup, GRUP,  ETIKET, COZUM, oncelikli_eksikler, bizim_eksikler, sicak_mi

def _e(x): return html.escape(str(x if x is not None else ""), quote=True)

PLAN = {
 "insaat-3d-modelleme": [
   ("Mimari model", "Projenin 3D modeli: yapı, arsa, çevre ve peyzaj ölçülü kurulur."),
   ("Render seti", "Dış cephe görselleri — gündüz, gün batımı ve gece ışık senaryosu."),
   ("Tanıtım animasyonu", "60–90 saniyelik kamera hareketli proje filmi, müzik ve grafiklerle."),
   ("İç mekân + sanal tur", "Daire tipi başına iç görseller ve 360° gezinti."),
   ("Yayın paketi", "İlan sitesi, web ve sosyal medya için yatay/dikey/kare kesimler."),
 ],
 "emlak-video": [
   ("Keşif", "Mülkün ışık saati ve çekim rotası belirlenir."),
   ("Çekim günü", "İçeriden akıcı kamera, dışarıdan drone; fotoğraflar aynı gün."),
   ("Kurgu", "Ritim kurgusu, renk düzenleme, altyazı ve müzik."),
   ("Yayın paketi", "İlan sitesi sürümü + dikey/kare sosyal medya kesimleri."),
   ("Portföy aboneliği", "Aylık sabit fiyatla düzenli mülk çekimi."),
 ],
 "urun-animasyon": [
   ("Ürün brifingi", "Teknik resim / CAD / fotoğraf toplanır, hedef kitle netleşir."),
   ("Senaryo", "Hangi özellik hangi saniyede anlatılacak, kare kare planlanır."),
   ("3D modelleme", "Ürün ölçülü modellenir; malzeme ve mekanizma kurulur."),
   ("Animasyon", "Çalışma prensibi, kesit ve patlatılmış görünüm."),
   ("Çok dilli teslim", "Fuar döngüsü, web sürümü, sosyal kesimler, yabancı dil seslendirme."),
 ],
 "isletme-tanitim": [
   ("İçerik planı", "Aylık çekim takvimi ve konu listesi."),
   ("Çekim günü", "Mekân, ürün ve ekip görüntüleri tek seferde toplanır."),
   ("Kurgu", "Reels formatında kısa videolar, altyazılı."),
   ("Yayın", "Haftalık paylaşım için hazır teslim."),
   ("Ölçüm", "Etkileşim takibi ve bir sonraki ayın planı."),
 ],
}

SABLON = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{ad} · Luna Yapım Görünürlük Analizi</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,800&family=Manrope:wght@400;500;600&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{{--ink:#0A0A0C;--ink2:#131317;--bone:#EFEDE8;--kirmizi:#E8452C;--gri:#8C8A84;--cizgi:rgba(239,237,232,.13)}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--ink);color:var(--bone);font-family:"Manrope",system-ui,-apple-system,"Segoe UI",sans-serif;
line-height:1.6;-webkit-font-smoothing:antialiased}}
.wrap{{max-width:980px;margin:0 auto;padding:0 26px}}
h1,h2,h3{{font-family:"Bricolage Grotesque","Manrope",sans-serif;font-weight:800;letter-spacing:-.03em;line-height:1.03}}
.etk{{font-family:"Space Mono",ui-monospace,monospace;font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--kirmizi)}}
header{{border-bottom:1px solid var(--cizgi);padding:18px 0}}
.mrk{{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap}}
.mrk b{{font-family:"Bricolage Grotesque",sans-serif;font-size:17px}}
.kapak{{padding:74px 0 56px;border-bottom:1px solid var(--cizgi);background:linear-gradient(180deg,var(--ink2),var(--ink))}}
.kapak h1{{font-size:clamp(32px,5.6vw,58px);margin:16px 0 18px;max-width:20ch}}
.kapak p{{color:rgba(239,237,232,.72);max-width:62ch;font-size:17px}}
section{{padding:56px 0;border-bottom:1px solid var(--cizgi)}}
section h2{{font-size:clamp(24px,3.6vw,36px);margin-bottom:10px}}
.alt{{color:var(--gri);margin-bottom:26px;max-width:64ch}}
.skor{{display:flex;align-items:center;gap:26px;flex-wrap:wrap;margin:26px 0}}
.halka{{width:132px;height:132px;border-radius:50%;display:grid;place-items:center;
background:conic-gradient(var(--kirmizi) calc({skor}*1%),rgba(239,237,232,.10) 0);position:relative;flex-shrink:0}}
.halka::after{{content:"";position:absolute;inset:11px;border-radius:50%;background:var(--ink)}}
.halka span{{position:relative;z-index:1;font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:36px}}
.skor .yan b{{display:block;font-size:19px;margin-bottom:4px}}
.skor .yan p{{color:var(--gri);font-size:15px;max-width:44ch}}
table{{width:100%;border-collapse:collapse;font-size:15px;margin-top:8px}}
th,td{{text-align:left;padding:12px 12px;border-bottom:1px solid var(--cizgi);vertical-align:top}}
th{{font-family:"Space Mono",ui-monospace,monospace;font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--kirmizi)}}
td.k{{color:rgba(239,237,232,.9);width:34%}}
td.c{{color:var(--gri)}}
.rozet{{display:inline-block;font-family:"Space Mono",ui-monospace,monospace;font-size:9.5px;letter-spacing:.14em;
text-transform:uppercase;border:1px solid var(--cizgi);padding:4px 9px;border-radius:2px;color:var(--gri)}}
.rozet.biz{{border-color:var(--kirmizi);color:var(--kirmizi)}}
.kutular{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:1px;background:var(--cizgi);
border:1px solid var(--cizgi);margin:22px 0}}
.kutu{{background:var(--ink);padding:22px 20px}}
.kutu .etk{{display:block;margin-bottom:10px;color:var(--gri)}}
.kutu .buyuk{{font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:30px;line-height:1}}
.kutu .fark{{color:var(--kirmizi);font-size:13px;margin-top:6px;font-family:"Space Mono",ui-monospace,monospace}}
.bar{{height:9px;background:rgba(239,237,232,.10);border-radius:99px;overflow:hidden;margin-top:9px}}
.bar i{{display:block;height:100%;background:var(--kirmizi)}}
.adimlar{{counter-reset:a}}
.adim{{display:grid;grid-template-columns:52px 1fr;gap:16px;padding:16px 0;border-bottom:1px solid var(--cizgi)}}
.adim .n{{font-family:"Space Mono",ui-monospace,monospace;font-size:11px;color:var(--kirmizi);padding-top:5px}}
.adim b{{font-size:17px;display:block;margin-bottom:3px}}
.adim p{{color:var(--gri);font-size:15px}}
.cta{{background:var(--kirmizi);color:#fff;padding:56px 0}}
.cta h2{{font-size:clamp(26px,4.2vw,40px);max-width:18ch}}
.cta p{{margin-top:12px;max-width:52ch;color:rgba(255,255,255,.9)}}
.btn{{display:inline-block;margin-top:22px;margin-right:10px;background:var(--ink);color:var(--bone);
padding:14px 24px;border-radius:2px;text-decoration:none;font-weight:600;font-size:15px}}
.btn.cizgi{{background:transparent;border:1px solid rgba(255,255,255,.55);color:#fff}}
footer{{padding:30px 0;color:var(--gri);font-size:12.5px;display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap}}
.uyari{{border-left:3px solid var(--kirmizi);background:rgba(232,69,44,.07);padding:16px 18px;margin-top:22px;
font-size:14px;color:rgba(239,237,232,.78)}}
.kanit{{margin-top:9px;padding:10px 12px;background:rgba(239,237,232,.04);border-left:2px solid var(--gri);
border-radius:0 3px 3px 0;font-size:12.8px;color:var(--gri);line-height:1.55}}
.kanit b{{color:rgba(239,237,232,.72);font-weight:600}}
.kanit .kaynak{{display:block;margin-top:5px;font-family:"Space Mono",ui-monospace,monospace;font-size:10.5px;
letter-spacing:.06em;color:#6f6d68}}
@media(max-width:640px){{.adim{{grid-template-columns:36px 1fr}}}}
/* ---- grup karnesi ---- */
.karne{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px;margin-top:20px}}
.karne-kutu{{border:1px solid var(--cizgi);border-radius:5px;padding:18px 18px 16px}}
.karne-kutu.zayif{{border-color:var(--kirmizi);box-shadow:0 0 0 1px rgba(232,69,44,.2)}}
.karne-kutu .etk{{display:block;line-height:1.5;min-height:2.6em;color:var(--gri)}}
.karne-skor{{font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:40px;
line-height:1;margin:8px 0 10px;letter-spacing:-.04em}}
.karne-cubuk{{height:4px;background:rgba(239,237,232,.1);border-radius:99px;overflow:hidden}}
.karne-cubuk i{{display:block;height:100%;border-radius:99px}}
.karne-kutu small{{display:block;margin-top:9px;font-size:12px;color:var(--gri);line-height:1.45}}
/* ---- fark ---- */
.fark{{display:grid;gap:2px;margin-top:20px;border:1px solid var(--cizgi);border-radius:5px;overflow:hidden}}
.fark-satir{{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--cizgi)}}
@media(max-width:760px){{.fark-satir{{grid-template-columns:1fr}}}}
.fark-satir>div{{background:var(--ink);padding:19px 21px}}
.fark-satir .sol{{color:var(--gri)}}
.fark-satir .sag{{border-left:2px solid var(--kirmizi)}}
.fark-et{{font-family:"Space Mono",monospace;font-size:9.5px;letter-spacing:.18em;
text-transform:uppercase;display:block;margin-bottom:9px}}
.fark-satir .sol .fark-et{{color:#6f6d68}}
.fark-satir .sag .fark-et{{color:var(--kirmizi)}}
.fark-sonuc{{grid-column:1/-1;background:rgba(232,69,44,.07);padding:12px 21px;font-size:13.5px}}
/* ---- calisma modeli ---- */
.modeller{{display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));gap:18px;margin-top:20px}}
.model{{border:1px solid var(--cizgi);border-radius:5px;padding:25px}}
.model.one{{border-color:var(--kirmizi);box-shadow:0 0 0 1px rgba(232,69,44,.2)}}
.model h3{{font-size:20px;margin-bottom:5px}}
.model .rozet{{display:inline-block;font-family:"Space Mono",monospace;font-size:9.5px;
letter-spacing:.16em;text-transform:uppercase;border:1px solid var(--cizgi);border-radius:99px;
padding:4px 10px;color:var(--gri);margin-bottom:14px}}
.model .kime{{color:var(--gri);font-size:14px;line-height:1.6;margin-bottom:15px}}
.model ol{{margin:0 0 14px 18px}}
.model ol li{{font-size:14px;line-height:1.6;margin-bottom:5px}}
.model dl{{display:grid;grid-template-columns:auto 1fr;gap:6px 14px;font-size:13.5px;
border-top:1px solid var(--cizgi);padding-top:13px}}
.model dt{{font-family:"Space Mono",monospace;font-size:9.5px;letter-spacing:.14em;
text-transform:uppercase;color:var(--kirmizi);padding-top:3px}}
.model dd{{color:rgba(239,237,232,.82)}}
/* ---- referans ---- */
.ref{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin-top:20px}}
.ref-kart{{display:flex;flex-direction:column;border:1px solid var(--cizgi);border-radius:5px;
overflow:hidden;text-decoration:none;color:inherit;transition:.16s}}
.ref-kart:hover{{border-color:var(--kirmizi)}}
.ref .kapak{{display:block;width:100%;aspect-ratio:16/9;background-size:cover;background-position:center;
background-color:#15151a;position:relative}}
.ref .kapak::after{{content:"";position:absolute;inset:0}}
.ref .bilgi{{padding:14px 16px;flex:1}}
.ref .bilgi b{{display:block;font-size:14.5px;line-height:1.35}}
.ref .bilgi small{{color:var(--gri);font-size:11.5px}}
.plan{{margin-top:22px;border:1px solid var(--cizgi);border-radius:5px;overflow-x:auto;
background:#0A0A0C}}
.plan svg{{display:block;min-width:900px;max-width:100%;height:auto}}
.ref .bilgi p{{font-size:12.5px;line-height:1.55;color:var(--gri);margin-top:9px;
border-top:1px solid var(--cizgi);padding-top:9px}}
</style>
</head>
<body>
"""

# Sosyal eksiğin koduna göre ne yapacağımız — genel cümle yerine somut iş
_SOSYAL_COZUM = {
 "instagram": "Instagram kurulumu + aylık reels/carousel üretimi (şantiye, ürün, mekân)",
 "youtube": "YouTube kanalı + uzun tanıtım videosu; ilanlardan ve siteden buraya bağlantı",
 "linkedin": "LinkedIn şirket sayfası + kurumsal alıcıya yönelik içerik",
 "tiktok": "TikTok hesabı + dikey kısa içerik üretimi",
 "facebook": "Facebook sayfası + harita/işletme bilgisiyle eşleştirme",
 "x": "X hesabı + duyuru akışı",
}


def _sosyal_cozum(kod, sektor):
    k = (kod or "")
    for p_, c in _SOSYAL_COZUM.items():
        if p_ in k:
            if k.endswith("_olu") or "_olu_" in k:
                return "Ölü bağlantının düzeltilmesi + hesabın yeniden ayağa kaldırılması"
            if "eslesmiyor" in k:
                return "Hesap adının marka adıyla hizalanması ve profil düzeni"
            if k.startswith("bio_"):
                return "Profil düzeni: açıklama, siteye bağlantı, iletişim ve kapak görseli"
            return c
    if k == "sosyal_hicyok":
        return "Sıfırdan kurulum: hesaplar, profil düzeni ve ilk ay içerik üretimi"
    if k == "sosyal_site_baglantisi_yok":
        return "Siteden hesaplara bağlantı + JSON-LD sameAs alanı"
    if k == "sosyal_ad_tutarsiz":
        return "Kullanıcı adlarının tek marka adında birleştirilmesi"
    if k == "sosyal_tek_yonlu_bag":
        return "Profil açıklamasına siteye bağlantı eklenmesi"
    if k.startswith("bio_"):
        return "Profil düzeni: açıklama, siteye bağlantı, iletişim ve kapak görseli"
    return COZUM.get(k, "Sosyal medya kurulumu ve içerik üretimi")


def _sosyal_bolum(sosyal, sektor):
    """Sosyal denetim bulgularını rapora giren bölüme çevirir."""
    if not sosyal or "eksikler" not in sosyal:
        return ""
    from . import sosyal as SO
    hesaplar = sosyal.get("hesaplar") or {}
    eksik = sosyal.get("eksikler") or []
    skor = SO.sosyal_skor(sosyal)
    renk = "#E8452C" if skor < 45 else ("#E0A32E" if skor < 75 else "#3BA55C")

    kart = []
    for p_, h in hesaplar.items():
        sg = h.get("saglik") or {}
        satir = []
        if h.get("eslesme_yorum"):
            satir.append("eşleşme: %s" % h["eslesme_yorum"])
        if sg.get("takipci") is not None:
            satir.append("takipçi: %s" % "{:,}".format(sg["takipci"]).replace(",", "."))
        if sg.get("gonderi") is not None:
            satir.append("gönderi: %s" % sg["gonderi"])
        if sg.get("okunabilirlik") and sg["okunabilirlik"] != "açık":
            satir.append("profil sayfası okunamadı")
        kart.append('<div class="kutu"><span class="etk">%s</span>'
                    '<div class="buyuk" style="font-size:19px">@%s</div>'
                    '<div class="fark">%s</div></div>'
                    % (_e(h.get("ad", p_)), _e(h.get("kullanici", "")),
                       _e(" · ".join(satir) or "hesap bulundu")))
    if not kart:
        kart.append('<div class="kutu"><span class="etk">Bulunan hesap</span>'
                    '<div class="buyuk" style="font-size:19px">yok</div>'
                    '<div class="fark">Sektörünüzde işe yarayan platformların '
                    'hiçbirinde doğrulanabilen hesap yok</div></div>')

    satirlar = []
    for e in eksik[:10]:
        k = e.get("kanit") or {}
        satirlar.append('<tr><td class="k">%s<div class="kanit">'
                        '<b>Ne kontrol ettik:</b> %s<br><b>Ne bulduk:</b> %s'
                        '<span class="kaynak">kaynak: %s · %s</span></div></td>'
                        '<td class="c">%s</td></tr>'
                        % (_e(e.get("baslik", "")), _e(k.get("kontrol", "")),
                           _e(k.get("bulgu", "")), _e(k.get("kaynak", "")),
                           _e(k.get("zaman", "")), _e(_sosyal_cozum(e.get("kod", ""), sektor))))

    tut = (sosyal.get("tutarlilik") or {}).get("not", "")
    kars = (sosyal.get("karsiliklilik") or {}).get("not", "")
    notlar = " ".join(x for x in (tut, kars) if x)

    return ('<section><div class="wrap"><h2>Sosyal medya durumu</h2>'
            '<p class="alt">Hesapları firma adıyla eşleştirdik, açık olup olmadığını ve '
            'profilin tamamlanmışlığını kontrol ettik. Platformların içine girip veri '
            'kazımıyoruz — bakılan her şey herkese açık profil sayfasından.</p>'
            '<div class="skor"><div class="halka" style="border-color:%s">'
            '<span style="color:%s">%d</span></div>'
            '<div class="yan"><b>Sosyal medya gücü</b><p>Sektörünüzde işe yarayan '
            'platformların ağırlığına göre hesaplandı; eksik ve sorunlu hesaplar düşüldü.</p></div></div>'
            '<div class="kutular" style="margin-top:24px">%s</div>'
            '%s'
            '<h3 style="margin-top:32px;font-size:20px">Kanıtlı sosyal eksikler</h3>'
            '<table style="margin-top:12px"><tr><th>Eksik</th><th>Çözüm</th></tr>%s</table></div>'
            '</div></section>'
            % (renk, renk, skor, "".join(kart),
               ('<div class="uyari" style="margin-top:18px">%s</div>' % _e(notlar)) if notlar else "",
               "".join(satirlar) or '<tr><td colspan="2">Belirgin bir sosyal eksik bulunamadı.</td></tr>'))


def demo_uret(aday, eksikler, detay, tahmin, klasor=None, cekim_plani=None,
              sosyal=None, strateji=None):
    ad = aday["ad"]
    sektor = aday["sektor"]
    sk = SEKTORLER.get(sektor, {})
    hizmet = sk.get("hizmet", "isletme-tanitim")
    skor = tahmin.get("_skor", 0)
    biz = bizim_eksikler(eksikler)
    klasor = klasor or os.path.join(CIKTI, "demo")
    os.makedirs(klasor, exist_ok=True)

    kanitlar = (detay or {}).get("kanit", {})
    satirlar = []
    for k in sorted(eksikler, key=lambda x: -(0 if x not in ETIKET else 1)):
        bizim = ' <span class="rozet biz">Luna çözüyor</span>' if k in biz else ''
        kn = kanitlar.get(k)
        kanit_html = ""
        if kn:
            kanit_html = ('<div class="kanit"><b>Ne kontrol ettik:</b> %s<br>'
                          '<b>Ne bulduk:</b> %s<br><span class="kaynak">kaynak: %s · %s</span></div>'
                          % (_e(kn.get("kontrol")), _e(kn.get("bulgu")),
                             _e(kn.get("kaynak")), _e(kn.get("zaman"))))
        satirlar.append('<tr><td class="k">%s%s%s</td><td class="c">%s</td></tr>'
                        % (_e(ETIKET.get(k, k)), bizim, kanit_html, _e(COZUM.get(k, "—"))))

    tekil = []
    en_buyuk = max([t["tek_basina_ek_iletisim"] for t in tahmin["tekil_katki"]] or [1])
    for t in tahmin["tekil_katki"][:6]:
        oran = int(round(100 * t["tek_basina_ek_iletisim"] / en_buyuk)) if en_buyuk else 0
        tekil.append('<tr><td class="k">%s</td><td class="c">+%s aylık iletişim<div class="bar"><i style="width:%d%%"></i></div></td></tr>'
                     % (_e(ETIKET.get(t["eksik"], t["eksik"])), t["tek_basina_ek_iletisim"], oran))

    adimlar = []
    for i, (b, p) in enumerate(PLAN.get(hizmet, PLAN["isletme-tanitim"]), 1):
        adimlar.append('<div class="adim"><span class="n">%02d</span><div><b>%s</b><p>%s</p></div></div>' % (i, _e(b), _e(p)))

    # --- grup karnesi: hangi başlıkta kaç puan
    kn = karne(eksikler)
    zayif = en_zayif_grup(eksikler)
    karne_html = "".join(
      '<div class="karne-kutu%s"><span class="etk">%s</span>'
      '<div class="karne-skor" style="color:%s">%d</div>'
      '<div class="karne-cubuk"><i style="width:%d%%;background:%s"></i></div>'
      '<small>%s</small></div>'
      % (" zayif" if g == zayif["anahtar"] else "", _e(v["baslik"]),
         ("#E8452C" if v["skor"] < 45 else "#E0A32E" if v["skor"] < 75 else "#3BA55C"),
         v["skor"], v["skor"],
         ("#E8452C" if v["skor"] < 45 else "#E0A32E" if v["skor"] < 75 else "#3BA55C"),
         _e(v["not"] or ("%d başlık eksik" % len(v["kodlar"]) if v["kodlar"] else "eksik yok")))
      for g, v in kn.items())

    # --- fark katmanı
    fark_html = "".join(
      '<div class="fark-satir"><div class="sol"><span class="fark-et">Genelde böyle yapılır</span>%s</div>'
      '<div class="sag"><span class="fark-et">Bizde böyle</span>%s</div>'
      '<div class="fark-sonuc"><b>Sonuç:</b> %s</div></div>'
      % (_e(f["sıradan"]), _e(f["bizde"]), _e(f["sonuc"]))
      for f in FK.farklar(sektor, 4))

    # --- çalışma modeli
    md = FK.model(sektor)
    def _mk(anahtar):
        m = md[anahtar]; one = (anahtar == md["onerilen"])
        return ('<div class="model%s"><h3>%s</h3><span class="rozet"%s>%s</span>'
                '<p class="kime">%s</p><ol>%s</ol>'
                '<dl><dt>Süre</dt><dd>%s</dd><dt>Ödeme</dt><dd>%s</dd><dt>Artısı</dt><dd>%s</dd></dl></div>'
                % (" one" if one else "", _e(m["ad"]),
                   ' style="border-color:#E8452C;color:#E8452C"' if one else "",
                   "size önerdiğimiz" if one else "diğer yol", _e(m["kime"]),
                   "".join("<li>%s</li>" % _e(x) for x in m["nasil"]),
                   _e(m["sure"]), _e(m["odeme"]), _e(m["avantaj"])))
    model_html = _mk(md["onerilen"]) + _mk("aylik" if md["onerilen"] == "proje" else "proje")

    # --- sektöre eşlenmiş referanslar
    ref_html = "".join(
      ('<a class="ref-kart" href="%s" target="_blank" rel="noopener">' % _e(RF.baglanti(i))
       if RF.baglanti(i) else '<div class="ref-kart">') +
      ('<span class="kapak" style="background-image:linear-gradient(180deg,rgba(0,0,0,.1),'
       'rgba(0,0,0,.45)),url(%s)"></span>' % _e(RF.gorsel_url(i)) if RF.gorsel_url(i)
       else '<span class="kapak"></span>') +
      '<div class="bilgi"><b>%s</b><small>%s</small><p>%s</p></div>' % (
          _e(i["ad"]), _e(i["tur"]), _e(RF.vurgu(i, sektor))) +
      ("</a>" if RF.baglanti(i) else "</div>")
      for i in RF.sektor_icin(sektor, 4))

    # --- örnek çekim planı (sektöre özel storyboard, sayfaya gömülü)
    plan_bolumu = ""
    try:
        svg = OR.storyboard(sektor or "isletme", ad, aday.get("sehir") or "")
        plan_bolumu = ('<section><div class="wrap">'
                       '<h2>Sizin için ne çekeriz</h2>'
                       '<p class="alt">Aşağıdaki, %s için hazırladığımız çekim planıdır. '
                       'Her kare gerçekten çekilecek plandır: ölçeği, kamera hareketi, ekranda ne '
                       'yazacağı ve ne duyulacağı yazılı. Hazır görsel değil — yapılacak işin kendisi.</p>'
                       '<div class="plan">%s</div></div></section>' % (_e(ad), svg))
    except Exception:
        plan_bolumu = ""

    # --- sosyal medya bölümü (raporun içinde, kanıtlı)
    sosyal_bolumu = ""
    try:
        sosyal_bolumu = _sosyal_bolum(sosyal, sektor)
    except Exception:
        sosyal_bolumu = ""

    strateji_bolumu = ""
    if strateji:
        strateji_bolumu = (
            '<section><div class="wrap"><h2>90 günlük plan</h2>'
            '<p class="alt">Bu analizin devamı olarak, size özel bir pazarlama stratejisi '
            'belgesi hazırladık: hangi kanal ve neden, ne anlatacağız, 30/60/90 gün sırası, '
            'huni matematiği, bütçe dağılımı ve ne ölçeceğimiz.</p>'
            '<div class="kutular">%s</div>'
            '<p class="alt" style="margin-top:16px">Ayrı dosya: <b>strateji.html</b></p>'
            '</div></section>'
            % "".join('<div class="kutu"><span class="etk">%s</span>'
                      '<div class="buyuk" style="font-size:26px">%s</div>'
                      '<div class="fark">%s</div></div>'
                      % (_e(y["donem"]), _e(y["baslik"]), _e("%d adım" % len(y["adim"])))
                      for y in strateji["yol"]))

    site = (detay.get("site") or {}).get("site_url")
    durum_satirlari = [
        ("Web sitesi", site or "Yok"),
        ("Harita puanı", ("%.1f" % aday["puan"]) if aday["puan"] else "—"),
        ("Yorum sayısı", aday["yorum_sayisi"] or 0),
        ("Profil fotoğrafı", aday["fotograf_sayisi"] or 0),
        ("Sitede video", "Var" if (detay.get("site") or {}).get("video") else "Yok"),
        ("İşletme şeması", "Var" if (detay.get("site") or {}).get("sema") else "Yok"),
    ]
    if detay.get("pagespeed_mobil") is not None:
        durum_satirlari.append(("Mobil hız skoru", "%s / 100" % detay["pagespeed_mobil"]))

    g = SABLON.format(ad=_e(ad), skor=skor)
    g += """<header><div class="wrap mrk"><b>LUNA YAPIM</b><span class="etk">Görünürlük Analizi · {tarih}</span></div></header>

<div class="kapak"><div class="wrap">
  <p class="etk">{sektor_ad} · {sehir}</p>
  <h1>{ad} bugün internette ne kadar görünüyor?</h1>
  <p>Bu sayfa, herkese açık bilgiler üzerinden yapılmış bir durum tespitidir. Hiçbir özel veri kullanılmadı.
     Aşağıda mevcut durum, tespit edilen eksikler ve bu eksikler kapatıldığında modelin öngördüğü değişim var.</p>
</div></div>

<section><div class="wrap">
  <h2>Bugünkü tablo</h2>
  <p class="alt">Görünürlük skoru, işletmenin dijitalde bulunabilirliğini 100 üzerinden özetler.</p>
  <div class="skor">
    <div class="halka"><span>{skor}</span></div>
    <div class="yan"><b>{yorum}</b><p>{yorum_alt}</p></div>
  </div>
  <h3 style="margin-top:36px;font-size:20px">Beş başlıkta karneniz</h3>
  <p class="alt">Tek bir puan yerine, paranın nerede kaybedildiğini gösteren beş ayrı not.
     En düşük olan başlıktan başlıyoruz.</p>
  <div class="karne">{karne}</div>
  <table style="margin-top:30px"><tr><th>Ölçüm</th><th>Durum</th></tr>{durum}</table></div>
</div></section>

<section><div class="wrap">
  <h2>Tespit edilen eksikler</h2>
  <p class="alt">{eksik_sayisi} başlık bulundu. Her satırın altında <strong>ne kontrol ettiğimiz ve ne bulduğumuz</strong>
     kaynağıyla birlikte yazıyor — hiçbiri tahmin değil, hepsi doğrulanabilir.</p>
  <div class='tablo-kaydir'><table><tr><th>Eksik</th><th>Çözüm</th></tr>{eksikler}</table></div>
</div></section>

<section><div class="wrap">
  <h2>Eksikler kapanırsa</h2>
  <p class="alt">Aşağıdaki rakamlar bir <strong>modelleme tahminidir</strong>, garanti değildir. Amaç, hangi işin ne kadar
     fark yaratacağını büyüklük mertebesiyle göstermek.</p>
  <div class="kutular">
    <div class="kutu"><span class="etk">Aylık görüntülenme</span><div class="buyuk">{hedef_g}</div>
      <div class="fark">şu an {mevcut_g} · %{artis} artış</div></div>
    <div class="kutu"><span class="etk">Aylık iletişim</span><div class="buyuk">{hedef_i}</div>
      <div class="fark">şu an {mevcut_i}</div></div>
    <div class="kutu"><span class="etk">Aylık kazanılan iş</span><div class="buyuk">{hedef_is}</div>
      <div class="fark">şu an {mevcut_is}</div></div>
    <div class="kutu"><span class="etk">Aylık ek ciro (tahmini)</span><div class="buyuk">{ek_gelir}</div>
      <div class="fark">ort. iş büyüklüğü {ort_is} TL varsayımıyla</div></div>
  </div>
  <h3 style="margin-top:34px;font-size:20px">Önce hangisini yapalım?</h3>
  <table style="margin-top:12px"><tr><th>İş</th><th>Tek başına etkisi</th></tr>{tekil}</table></div>
  <div class="uyari">Model varsayımları: mevcut dönüşüm %{d1}, iyileştirilmiş dönüşüm %{d2}, iletişimden işe dönüşüm %{d3}.
    Bu oranlar Luna Pusula ayar dosyasından değiştirilebilir; işletmenin kendi rakamları girildiğinde tahmin gerçeğe yaklaşır.</div>
</div></section>

<section><div class="wrap">
  <h2>Önerimiz: {teklif}</h2>
  <p class="alt">Eksiklerin en ağır olanı görünürlük tarafında. Aşağıdaki plan, {ad} için doğrudan uygulanabilir.</p>
  <div class="adimlar">{adimlar}</div>
</div></section>

<section><div class="wrap">
  <h2>Herkesin yaptığı şey, bir de bizim yaptığımız</h2>
  <p class="alt">Daha önce teklif aldıysanız sol sütun tanıdık gelecek.</p>
  <div class="fark">{fark}</div>
</div></section>

<section><div class="wrap">
  <h2>Nasıl çalışırız — iki yol var</h2>
  <p class="alt">{model_cumle}</p>
  <div class="modeller">{model}</div>
</div></section>

{sosyal_bolumu}

{plan_bolumu}

{strateji_bolumu}

<section><div class="wrap">
  <h2>Sizin sektörünüzde yaptığımız işler</h2>
  <p class="alt">Aşağıdakiler elimizde duran çalışmalardan. Her birinin yanında,
     sizin işinizle ilgisinin ne olduğu yazıyor.</p>
  <div class="ref">{referans}</div>
</div></section>

<div class="cta"><div class="wrap">
  <p class="etk" style="color:rgba(255,255,255,.75)">İletişim</p>
  <h2>Bu analizi birlikte konuşalım.</h2>
  <p>Rakamları kendi verinizle güncelleyelim, sizin için ne anlama geldiğini beraber çıkaralım.</p>
  <a class="btn" href="https://wa.me/905411602603">WhatsApp'tan yaz</a>
  <a class="btn cizgi" href="tel:+905411602603">0541 160 26 03</a>
</div></div>

<footer><div class="wrap mrk"><span>Luna Yapım · lunayapim.com · Bursa</span>
<span>Bu sayfa Luna Pusula ile otomatik üretildi · {tarih}</span></div></footer>
</body></html>
""".format(
      tarih=datetime.date.today().strftime("%d.%m.%Y"),
      sektor_ad=_e(sk.get("ad", sektor or "İşletme")), sehir=_e(aday["sehir"] or ""),
      ad=_e(ad), skor=skor,
      yorum=("Çok sayıda eksik var" if skor < 55 else "Orta seviyede" if skor < 75 else "İyi durumda"),
      yorum_alt=("Bu tablodaki her eksik, sizi arayabilecek birinin sizi bulamaması demek."
                 if skor < 55 else "Temel işler yerinde; birkaç adımla belirgin fark alınabilir."),
      durum="".join('<tr><td class="k">%s</td><td class="c">%s</td></tr>' % (_e(a), _e(b)) for a, b in durum_satirlari),
      eksik_sayisi=len(eksikler), eksikler="".join(satirlar),
      hedef_g="{:,}".format(tahmin["hedef_goruntulenme"]).replace(",", "."),
      mevcut_g="{:,}".format(tahmin["mevcut_goruntulenme"]).replace(",", "."),
      artis=tahmin["goruntulenme_artis_yuzde"],
      hedef_i=tahmin["hedef_iletisim"], mevcut_i=tahmin["mevcut_iletisim"],
      hedef_is=tahmin["hedef_is"], mevcut_is=tahmin["mevcut_is"],
      ek_gelir="{:,} TL".format(tahmin["ek_gelir"]).replace(",", "."),
      ort_is="{:,}".format(tahmin["ortalama_is"]).replace(",", "."),
      tekil="".join(tekil),
      d1=round(tahmin["varsayimlar"]["donusum_mevcut"] * 100, 1),
      d2=round(tahmin["varsayimlar"]["donusum_iyilesmis"] * 100, 1),
      d3=round(tahmin["varsayimlar"]["kapanis_orani"] * 100, 1),
      teklif=_e(sk.get("teklif", "Tanıtım videosu")),
      adimlar="".join(adimlar),
      karne=karne_html, fark=fark_html, model=model_html, referans=ref_html,
      plan_bolumu=plan_bolumu, sosyal_bolumu=sosyal_bolumu,
      strateji_bolumu=strateji_bolumu,
      model_cumle=_e(FK.model_cumlesi(sektor)))

    import unicodedata
    duz = unicodedata.normalize("NFKD", ad).encode("ascii", "ignore").decode()
    guvenli = re.sub(r"-{2,}", "-", "".join(ch if ch.isalnum() else "-" for ch in duz.lower())).strip("-")[:60] or "aday"
    dosya = os.path.join(klasor, "%s-%s.html" % (aday["id"], guvenli))
    open(dosya, "w", encoding="utf-8").write(g)

    onc = oncelikli_eksikler(eksikler, 2)
    mesaj = ("Merhaba, Luna Yapım'dan {kim}. {ad} için internetteki görünürlüğünüze baktık — "
             "{e1}{e2} gibi başlıklarda kolay kazanç görünüyor. Ne yaptığımızı ve rakamların ne anlama "
             "geldiğini gösteren kısa bir sayfa hazırladım, göndereyim mi?").format(
                kim="ekibimiz", ad=ad,
                e1=ETIKET.get(onc[0], "") if onc else "",
                e2=(" ve " + ETIKET.get(onc[1], "").lower()) if len(onc) > 1 else "")
    return dosya, mesaj
