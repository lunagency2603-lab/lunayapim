# -*- coding: utf-8 -*-
"""
TrendSaphiens ana sayfası (vitrin), editör paneli, yazar sayfası ve yayın ilkeleri (12.10.2026).

Ana sayfa düzeni Onedio incelemesinden: tek kronolojik akış yerine kutular —
güncel konular · manşet · trend + günün anketi + hızlı erişim · testler ·
bölüm satırları · en çok okunanlar · editör bandı · tam arşiv (yetim sayfa kalmasın).
"""
import datetime, html, json

from . import bicim as BC, editor as ED

SIRA = ["ekran", "spor", "muzik", "burc", "haber", "teknoloji", "sanat", "edebiyat", "sosyal-medya", "piyasa"]
HIZLI = [("dolar-kac-tl-bugun", "💵", "Dolar kaç TL?", "TCMB kuru, her gün"),
         ("gram-altin-nasil-hesaplanir-ons-dolar", "🪙", "Gram altın", "Hesap ve güncel fiyat"),
         ("yukselen-burc-hesaplama", "🌅", "Yükselen burç", "Doğum saatine göre"),
         ("burc-uyumu", "💞", "Burç uyumu", "12 burcun eşleşmesi"),
         ("yas-hesaplama", "🎂", "Yaş hesaplama", "Yıl, ay, gün"),
         ("yuzde-hesaplama", "➗", "Yüzde hesaplama", "Oran ve değişim")]


def _e(x):
    return html.escape(str(x or ""), quote=True)


def _yazi(hepsi):
    from .trend import YAZI_TURLERI, GORUNUR
    return [m for m in hepsi if m["tur"] in YAZI_TURLERI and m.get("slug") and m.get("kat") in GORUNUR]


def _mk(m, sinif, h="h3", tekrar_mi=None):
    from .trend import KATEGORI, _tr_tarih
    return ('<a class="v-mk %s" href="%s">%s<div class="v-mk-metin"><small>%s · %s</small><%s>%s</%s></div></a>'
            % (sinif, _e(m["slug"]), BC.kapak_html(m, "../", tekrar_mi), _e(KATEGORI.get(m.get("kat"), ("",))[0]),
               _e(_tr_tarih(m["tarih"][:10])), h, _e(m["baslik"]), h))


def vitrin_html(kok, hepsi):
    from . import trend as T
    tm = T._tekrar_mi
    yazi = _yazi(hepsi)
    # manşet: önce görseli olan ya da biçim içerikleri öne çıkar; aynı içerik iki kutuda tekrar etmez
    kullanildi = set()

    def al(liste, n):
        out = []
        for m in liste:
            if m["slug"] in kullanildi:
                continue
            out.append(m); kullanildi.add(m["slug"])
            if len(out) >= n:
                break
        return out

    haber_turu = [m for m in yazi if m.get("bicim") not in ("test", "bilgi", "anket")]
    manset = al(sorted(haber_turu, key=lambda m: (m["tarih"][:10], BC.gorsel_var(m, tm)), reverse=True)[:6], 3)

    def etiket(m):
        t = (m.get("terim") or m["baslik"]).split(":")[0].strip()
        return t if len(t) <= 34 else t[:34].rsplit(" ", 1)[0]
    konular = "".join('<a href="%s">%s</a>' % (_e(m["slug"]), _e(etiket(m))) for m in yazi[:10])
    trend = "".join('<li><a href="%s"><span>%02d</span><b>%s</b><small>%s</small></a></li>'
                    % (_e(m["slug"]), i, _e(m["baslik"]), _e(T.KATEGORI.get(m.get("kat"), ("",))[0]))
                    for i, m in enumerate([m for m in haber_turu if m["slug"] not in kullanildi][:6], 1))
    anketler = [m for m in yazi if m.get("bicim") == "anket"]
    anket_kutu = ('<div class="v-kutu"><h2>Günün anketi</h2>%s<p style="margin:10px 0 0;font-size:13px"><a href="%s">Anketin hikâyesi →</a></p></div>'
                  % (BC.anket_kutu_html(anketler[0]["veri"]), _e(anketler[0]["slug"]))) if anketler else BC.populer_html(hepsi, "")
    hizli = '<div class="v-kutu"><h2>Hızlı erişim</h2><div class="v-hizli">%s</div></div>' % "".join(
        '<a href="%s"><i aria-hidden="true">%s</i><b>%s</b><small>%s</small></a>' % (s, i, _e(a), _e(o)) for s, i, a, o in HIZLI)

    par = []
    par.append('<div class="wrap"><div class="v-konular" role="navigation" aria-label="Güncel konular"><span>Gündemde</span>%s</div></div>' % konular)
    if manset:
        par.append('<div class="wrap"><section class="v-manset" aria-label="Manşet">%s<div class="v-manset-yan">%s</div></section></div>'
                   % (_mk(manset[0], "v-manset-ana", "h2", tm), "".join(_mk(m, "", "h3", tm) for m in manset[1:3])))
    par.append('<div class="wrap"><section class="v-uclu"><div class="v-kutu"><h2>Son eklenenler</h2><ol class="v-sirali">%s</ol></div>%s%s</section></div>'
               % (trend, anket_kutu, hizli))
    testler = [m for m in yazi if m.get("bicim") in ("test", "bilgi")]
    if testler:
        par.append('<div class="wrap"><section class="v-bant" style="--kr:var(--k-test)"><div class="v-bant-bas"><h2>Testler</h2><span style="font-size:13px;color:var(--gri-2)">Kişilik ve bilgi testleri — sonuçlar sayfada, kayıt yok</span></div>'
                   '<div class="v-izgara">%s</div></section></div>' % "".join(BC.kart_html(m, "../", "", tm) for m in testler[:4]))
        kullanildi.update(m["slug"] for m in testler[:4])
    par.append('<div class="wrap">%s</div>' % T.REKLAM_YAN)
    for kat in SIRA:
        if kat not in T.GORUNUR:
            continue
        liste = [m for m in yazi if m.get("kat") == kat and m["slug"] not in kullanildi and m.get("bicim") not in ("test", "bilgi")][:4]
        if len(liste) < 2:
            continue
        kullanildi.update(m["slug"] for m in liste)
        ad, alt = T.KATEGORI[kat]
        yan = "".join('<a href="%s">%s<b>%s</b></a>' % (_e(m["slug"]), BC.kapak_html(m, "../", tm, etiket=False), _e(m["baslik"])) for m in liste[1:])
        par.append('<div class="wrap"><section class="v-bant" style="--kr:var(--k-%s)"><div class="v-bant-bas"><h2>%s</h2><a href="%s/">Tümü →</a></div>'
                   '<div class="v-kat">%s<div class="v-kat-liste">%s</div></div></section></div>'
                   % (kat, _e(ad), kat, BC.kart_html(liste[0], "../", "", tm), yan))
    par.append('<div class="wrap"><section class="v-bant"><div class="v-uclu v-ikili">%s%s</div></section></div>'
               % (BC.populer_html(hepsi, ""), T._rehber_kutu("").replace("ts-kutu ts-rehber", "v-kutu ts-rehber")))
    par.append('<div class="wrap"><section class="v-editor"><span class="ts-imza-harf" style="width:56px;height:56px;font-size:17px;background:#fff;color:var(--ink)">PC</span>'
               '<div><b>%s</b> · <span style="color:#CFCBC2">%s</span><p>Yayına çıkan her liste, test ve haberi okuyup kaynaklarını kontrol ederek yayına alır. '
               'Hata gördüğünde yazman yeterli; düzeltme yazının içinde tarihiyle belirtilir.</p></div><a href="yayin-ilkeleri">Yayın ilkelerimiz →</a></section></div>'
               % (_e(ED.EDITOR["ad"]), _e(ED.EDITOR["unvan"])))
    kalan = [m for m in yazi if m["slug"] not in kullanildi]
    if kalan:
        par.append('<div class="wrap"><section class="v-bant"><div class="v-bant-bas"><h2>Tüm yazılar</h2></div><ul class="ts-tumu-liste">%s</ul></section></div>'
                   % "".join('<li><a href="%s">%s</a><time datetime="%s">%s</time></li>' % (_e(m["slug"]), _e(m["baslik"]), _e(m["tarih"][:10]), _e(T._tr_tarih(m["tarih"][:10])))
                             for m in kalan))
    baslik = "TrendSaphiens — gündem, testler, listeler ve rehberler"
    aciklama = "Türkiye'nin aradığı konular kaynaklarıyla: dizi-film, spor, müzik ve burç yazıları, kişilik ve bilgi testleri, anketler, günün kurları ve hesaplama araçları."
    sema = '<script type="application/ld+json">%s</script>' % json.dumps({"@context": "https://schema.org", "@type": "WebSite",
        "name": "TrendSaphiens", "url": T.KOK_URL, "description": aciklama,
        "publisher": {"@type": "Organization", "name": "Luna Yapım", "url": "https://lunayapim.com/"}}, ensure_ascii=False)
    h1 = '<h1 class="ts-gizli" style="position:absolute;left:-9999px">TrendSaphiens — gündem, testler ve rehberler</h1>'
    return T._bas(baslik, aciklama, T.KOK_URL, manset[0]["gorsel"] if manset and BC.gorsel_var(manset[0], tm) else None, sema, "website", "../", "") \
        + h1 + "\n".join(par) + T._alt("../", "")


# ------------------------------------------------------------------ editör paneli
def panel_html(hepsi, taslaklar):
    from . import trend as T
    from .trend import YAZI_TURLERI
    satir = []
    for m in list(taslaklar) + [m for m in hepsi if m["tur"] in YAZI_TURLERI and m.get("slug")]:
        dr = "taslak" if m in taslaklar else ED.durum(m["slug"], m.get("tarih"))
        url = ("taslak/" if dr == "taslak" else "") + m["slug"]
        tur = BC.BICIM_AD.get(m.get("bicim"), "Haber" if m["tur"] == "haber" else "Rehber")
        satir.append('<div class="ep-satir" data-slug="%s"><span class="ep-durum %s">%s</span><div><a href="%s" target="_blank">%s</a>'
                     '<small>%s · %s · %s</small></div><button class="ep-dug%s" data-islem="%s">%s</button></div>'
                     % (_e(m["slug"]), dr, {"taslak": "Taslak", "inceleme": "İnceleme", "onayli": "Yayında"}[dr], _e(url), _e(m["baslik"]),
                        _e(tur), _e(T.KATEGORI.get(m.get("kat"), ("",))[0]), _e(T._tr_tarih(str(m.get("tarih", ""))[:10])),
                        " geri" if dr == "onayli" else "", "geri" if dr == "onayli" else "onayla",
                        "Onayı geri al" if dr == "onayli" else "Okudum, yayınla"))
    sayi = {k: sum(1 for x in satir if 'ep-durum %s"' % k in x) for k in ("taslak", "inceleme", "onayli")}
    govde = """
<section class="ts-giris" style="max-width:920px;margin:30px auto">
  <span class="etk">Editör paneli</span>
  <h1 style="margin:6px 0 8px">Onay masası</h1>
  <p>%d taslak · %d inceleme bekleyen eski yazı · %d onaylı. Bir yazıyı açıp okuduktan sonra
  <b>Okudum, yayınla</b>'ya bas. Onay bir sonraki yayın turunda (en geç 3 saat) sayfaya imzanla işlenir;
  taslaklar o turda yayına girer. Bu sayfa arama motorlarına kapalıdır.</p>
  <div class="ep-anahtar"><input type="password" id="ep-anahtar" placeholder="Panel anahtarı (bir kez girilir, bu tarayıcıda saklanır)"><button class="ep-dug" id="ep-kaydet">Kaydet</button></div>
  <h2>Kontrol listesi</h2>
  <p class="ts-not">Okurken kontrol listesi: isimler, tarihler ve rakamlar kaynakla aynı mı? Başlık yazının söylediğinden fazlasını vaat ediyor mu? Testlerde her sonuç metni okunaklı mı? Videolar resmî kanaldan mı?</p>
  <h2>İçerikler</h2>
  %s
</section>
<script>
(function(){var A="ts-panel-anahtar",g=document.getElementById("ep-anahtar");try{g.value=localStorage.getItem(A)||""}catch(e){}
document.getElementById("ep-kaydet").onclick=function(){try{localStorage.setItem(A,g.value)}catch(e){}this.textContent="Kaydedildi"};
Array.prototype.forEach.call(document.querySelectorAll(".ep-satir button"),function(b){b.onclick=function(){
var s=b.parentNode.getAttribute("data-slug"),i=b.getAttribute("data-islem");b.disabled=true;b.textContent="Gönderiliyor…";
fetch("/api/onay",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({slug:s,islem:i,anahtar:g.value})})
.then(function(r){return r.json().then(function(d){if(!r.ok)throw d;return d})})
.then(function(d){var e=b.parentNode.querySelector(".ep-durum");if(d.durum==="onayli"){e.className="ep-durum onayli";e.textContent="Onaylandı";b.textContent="Onaylandı — sıradaki turda yayında"}else{e.className="ep-durum inceleme";e.textContent="Geri alındı";b.textContent="Geri alındı"}})
.catch(function(d){b.disabled=false;b.textContent=(d&&d.hata==="yetki yok")?"Anahtar yanlış":"Olmadı, tekrar dene"})}})})();
</script>
""" % (sayi["taslak"], sayi["inceleme"], sayi["onayli"], "".join(satir))
    h = T._bas("Editör paneli: onay masası — TrendSaphiens", "TrendSaphiens editör onay masası: taslaklar, inceleme bekleyen yazılar ve yayındaki içerikler. Arama motorlarına kapalı iç sayfa.",
               T.KOK_URL + "editor", None, '<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebPage","name":"Editör paneli"}</script>', "website", "../", "") + govde + T._alt("../", "")
    return h.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n' + T.NOINDEX, 1)


# ------------------------------------------------------------------ yazar sayfası
def yazar_html(hepsi):
    from . import trend as T
    E = ED.EDITOR
    on, tr = "../../", "../"
    onay = ED.onaylar()
    yazilar = [m for m in hepsi if m.get("slug") in onay]
    kart = "".join(BC.kart_html(m, on, tr, T._tekrar_mi) for m in yazilar[:24])
    url = T.KOK_URL + "yazar/" + E["slug"]
    sema = '<script type="application/ld+json">%s</script>' % json.dumps({"@context": "https://schema.org", "@type": "ProfilePage",
        "url": url, "mainEntity": dict(ED.kisi_sema(), description=E["bio"], worksFor={"@type": "Organization", "name": "TrendSaphiens", "url": T.KOK_URL})},
        ensure_ascii=False)
    govde = """
<section class="ts-giris" style="max-width:920px;margin:30px auto">
  <div class="crumbs"><a href="../">TrendSaphiens</a> · Editör</div>
  <div style="display:flex;gap:18px;align-items:center;margin:14px 0">
    <span class="ts-imza-harf" style="width:72px;height:72px;font-size:22px">PC</span>
    <div><h1 style="margin:0">%s</h1><p style="margin:4px 0 0;color:var(--gri-2)">%s</p></div>
  </div>
  <p>%s</p>
  <h2>Nasıl çalışır?</h2>
  <p>Her yazıyı yayından önce okur ve şu soruları sorar: İsimler, tarihler ve rakamlar kaynakla aynı mı? Başlık yazının
  söylediğinden fazlasını vaat ediyor mu? Okur bu sayfadan başka yerde bulamayacağı bir şey alıyor mu — bir tablo,
  bir karşılaştırma, bir bağlam? Testlerde her sonuç metni ve her soru anlaşılır mı? Bu soruların biri "hayır"
  çıkarsa yazı yayına girmez, düzeltilir.</p>
  <p>Ayrıntılı kurallar <a href="../yayin-ilkeleri">yayın ilkeleri</a> sayfasında. İletişim: <a href="../iletisim">iletişim sayfası</a>.</p>
  <h2>Sorumlu olduğu bölümler</h2>
  <p>%s. Liste, kişilik testi, bilgi testi ve anketlerin soruları ile sonuç metinleri de yayından önce onun
  kontrolünden geçer. Bilgi testlerinde her doğru cevabın açıklaması sayfada durur; kişilik testleri eğlence içindir
  ve sonuçları bir ölçüm gibi sunulmaz.</p>
  <h2>Editör onayından geçen içerikler</h2>
  %s
</section>
""" % (_e(E["ad"]), _e(E["unvan"]), _e(E["bio"]),
       _e(", ".join(T.KATEGORI[k][0] for k in T.KATEGORI if k in T.GORUNUR)),
       ('<div class="v-izgara v-izgara-3">%s</div>' % kart) if kart else "<p>Onaylanan yazılar yayına girdikçe burada listelenir.</p>")
    return T._bas("%s — TrendSaphiens Editörü" % E["ad"], "%s, TrendSaphiens editörü. Yayına aldığı yazılar, listeler, testler ve anketler; içerikleri nasıl kontrol ettiği ve çalışma ilkeleri." % E["ad"], url, None, sema, "profile", on, tr) + govde + T._alt(on, tr)


# ------------------------------------------------------------------ yayın ilkeleri
def ilkeler_html():
    from . import trend as T
    url = T.KOK_URL + "yayin-ilkeleri"
    bolum = [
        ("Bu yayını kim çıkarıyor?",
         ["TrendSaphiens, Bursa merkezli video prodüksiyon stüdyosu Luna Yapım'ın yayınıdır. Yayına çıkan içeriklerden "
          "editörümüz %s sorumludur; yazıların altındaki imza, o yazıyı okuyup onayladığını gösterir." % ED.EDITOR["ad"]]),
        ("İçerik nasıl hazırlanıyor?",
         ["Konular Türkiye'de çok aranan başlıklardan, okur sorularından ve takvimden (vizyon, maç, sınav, ödül) seçilir. "
          "Her haber en az iki bağımsız yayıncının olgularına dayanır; kaynak cümlesi kopyalanmaz, yeniden sözcüklerle de yazılmaz.",
          "Taslağı hazırlarken yazılım araçlarından yararlanıyoruz; ancak hiçbir içerik editör okumadan yayına çıkmaz. "
          "Editör onayı olmayan taslaklar arama motorlarına kapalıdır ve reklam taşımaz."]),
        ("Kopyalanamayan katkı kuralı",
         ["Bir yazının yayına girmesi için okura başka sitede hazır bulamayacağı en az bir şey vermesi gerekir: kendi "
          "derlediğimiz bir tablo ya da karşılaştırma, kendi hesabımız, bir olayın neden önemli olduğunu anlatan bağlam ya da "
          "bilinenle bilinmeyeni ayıran bir döküm. Sadece başka bir haberi özetleyen yazı yayımlanmaz."]),
        ("Doğrulama listesi",
         ["İsimler, tarihler, rakamlar ve alıntılar kaynağına karşı tek tek kontrol edilir. Açıklanmamış bir bilgi tahminle "
          "doldurulmaz, \"henüz açıklanmadı\" diye yazılır. Kaynaklar çelişiyorsa hangisinin ne dediği adıyla belirtilir. "
          "Dizi ve filmlerde resmî olarak duyurulmamış tarih, kadro ya da sezon bilgisi kesinmiş gibi yazılmaz."]),
        ("Başlıklar",
         ["Başlık yazının söylediğinden fazlasını vaat etmez. \"Şok\", \"olay\", \"inanamayacaksınız\" gibi kalıplar "
          "kullanılmaz. Ölüm, suç, kaza ve hastalık haberleri yayının konusu değildir."]),
        ("Testler, listeler ve anketler",
         ["Kişilik testleri eğlence içindir; kişiliği ölçen bilimsel bir yöntem değildir ve sonuçları öyle sunulmaz. "
          "Bilgi testlerinde her doğru cevabın açıklaması sayfada durur. Listelerdeki videolar yalnız sanatçının, yapımcının "
          "ya da yayıncının resmî kanalından gömülür; şarkı sözü, afiş ve albüm kapağı kopyalanmaz. Anket sonuçları "
          "okurların oylarıdır, temsilî bir kamuoyu araştırması değildir."]),
        ("Görseller",
         ["Kapaklarda yalnız serbest lisanslı görseller (künyesiyle) ya da kendi tasarladığımız kapaklar kullanılır. "
          "Konuyla ilgisi olmayan temsilî fotoğraf kullanılmaz."]),
        ("Düzeltme politikası",
         ["Anlamı değiştiren bir hata düzeltildiğinde yazının sonuna tarihli bir \"Düzeltme\" notu eklenir; yazım hataları "
          "notsuz düzeltilir. Bir hata görürseniz iletişim sayfasındaki adrese sayfanın adresini ve doğru bilginin "
          "kaynağını yazmanız yeterli."]),
        ("Reklam ve bağımsızlık",
         ["Sayfalarda Google AdSense reklamları gösterilir. Reklamlar içerikten ayrı alanlarda durur; hangi konunun "
          "yazılacağına ya da bir yazının ne söyleyeceğine reklam veren karar vermez. Kur ve altın bilgileri yatırım "
          "tavsiyesi değildir."]),
    ]
    govde = '<section class="ts-giris" style="max-width:820px;margin:30px auto"><div class="crumbs"><a href="./">TrendSaphiens</a> · Yayın ilkeleri</div><h1>Yayın ilkeleri ve düzeltmeler</h1>%s<p class="ts-not">Son güncelleme: %s</p></section>' % (
        "".join("<h2>%s</h2>%s" % (_e(b), "".join("<p>%s</p>" % _e(p) for p in ps)) for b, ps in bolum), T._tr_tarih(ED.KESIM))
    sema = '<script type="application/ld+json">%s</script>' % json.dumps({"@context": "https://schema.org", "@type": "WebPage",
        "name": "Yayın ilkeleri ve düzeltmeler", "url": url, "publisher": {"@type": "Organization", "name": "TrendSaphiens", "url": T.KOK_URL}}, ensure_ascii=False)
    return T._bas("Yayın ilkeleri ve düzeltmeler — TrendSaphiens", "TrendSaphiens'te içerik nasıl seçilir, nasıl doğrulanır, testler ve anketler nasıl hazırlanır, hatalar nasıl düzeltilir.",
                  url, None, sema, "website", "../", "") + govde + T._alt("../", "")
