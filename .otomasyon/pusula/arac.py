# -*- coding: utf-8 -*-
"""
ARAÇ SAYFALARI — TrendSaphiens'in "vakit geçirten" bölümü.

20.09.2026 kararı: okur her gün haber için gelmez; hesaplayan, deneyen, sonucu
paylaşılan sayfalar için de gelir. Bu modül onları üretir:

  /yukselen-burc-hesaplama   doğum tarihi + saati + ili → yükselen burç (saf JS)
  /burc-uyumu                12×12 uyum tablosu, geleneksel astroloji yorumu
  /yas-hesaplama             iki tarih arası gün/ay/yıl
  /vucut-kitle-indeksi       VKİ + DSÖ aralıkları
  /yuzde-hesaplama           dört yüzde sorusu tek sayfada
  /oruntu-oyunu              10 soruluk örüntü/mantık oyunu

İLKELER
  · Hesap TARAYICIDA yapılır; doğum tarihi, boy, kilo hiçbir sunucuya gitmez.
    Bu sayfada açıkça yazılır — hem doğru hem ayırt edici.
  · Her sayfada aracın yanında İNDEKSLENEBİLİR metin var: Google aracı değil,
    metni sıralar. Yöntem anlatılır, kaynak verilir.
  · Dürüstlük: astroloji kişilik ölçmez; örüntü oyunu IQ testi DEĞİLDİR ve puan
    vermez; VKİ tıbbi tanı değildir. Bu notlar sayfanın görünen yerinde durur.
  · Dış kütüphane yok, çerez yok, veri toplama yok.

Yükselen hesabı: Meeus'un Julian Day ve GMST bağıntıları + standart ASC formülü
(tan ASC = cos(RAMC) / −(sin ε · tan φ + cos ε · sin RAMC)) ve kadran düzeltmesi.
Saat dilimi tarayıcının IANA verisinden okunur (Türkiye 2016'ya kadar yaz saati
uyguluyordu; elle kodlamak yanlış yükselen üretir).
"""
import io, json, os

from .ayarlar import SITE_KOK
from . import trend as T

KOK_URL = "https://lunayapim.com/trend/"
# Sayfa sürümü: Cloudflare dağıtımı bir dosyayı atlarsa bu damga değişince yeniden yüklenir.
SURUM = "2026-09-20-2"

# 81 il — merkez koordinatları (ondalık derece, doğu boylamı pozitif).
# Yükselen için il merkezi yeterli: ilçe farkı ASC'yi tipik olarak 0,1°'den az oynatır.
ILLER = {
    "Adana": (37.00, 35.32), "Adıyaman": (37.76, 38.28), "Afyonkarahisar": (38.76, 30.54),
    "Ağrı": (39.72, 43.05), "Aksaray": (38.37, 34.03), "Amasya": (40.65, 35.83),
    "Ankara": (39.93, 32.86), "Antalya": (36.90, 30.69), "Ardahan": (41.11, 42.70),
    "Artvin": (41.18, 41.82), "Aydın": (37.84, 27.84), "Balıkesir": (39.65, 27.89),
    "Bartın": (41.64, 32.34), "Batman": (37.88, 41.13), "Bayburt": (40.26, 40.23),
    "Bilecik": (40.14, 29.98), "Bingöl": (38.89, 40.50), "Bitlis": (38.40, 42.11),
    "Bolu": (40.74, 31.61), "Burdur": (37.72, 30.29), "Bursa": (40.19, 29.06),
    "Çanakkale": (40.15, 26.41), "Çankırı": (40.60, 33.62), "Çorum": (40.55, 34.95),
    "Denizli": (37.78, 29.09), "Diyarbakır": (37.91, 40.24), "Düzce": (40.84, 31.16),
    "Edirne": (41.68, 26.56), "Elazığ": (38.68, 39.22), "Erzincan": (39.75, 39.49),
    "Erzurum": (39.90, 41.27), "Eskişehir": (39.78, 30.52), "Gaziantep": (37.07, 37.38),
    "Giresun": (40.91, 38.39), "Gümüşhane": (40.46, 39.48), "Hakkâri": (37.58, 43.74),
    "Hatay": (36.20, 36.16), "Iğdır": (39.92, 44.04), "Isparta": (37.76, 30.55),
    "İstanbul": (41.01, 28.98), "İzmir": (38.42, 27.14), "Kahramanmaraş": (37.58, 36.93),
    "Karabük": (41.20, 32.62), "Karaman": (37.18, 33.22), "Kars": (40.60, 43.10),
    "Kastamonu": (41.39, 33.78), "Kayseri": (38.73, 35.49), "Kilis": (36.72, 37.12),
    "Kırıkkale": (39.85, 33.52), "Kırklareli": (41.73, 27.22), "Kırşehir": (39.15, 34.16),
    "Kocaeli": (40.77, 29.92), "Konya": (37.87, 32.48), "Kütahya": (39.42, 29.98),
    "Malatya": (38.36, 38.31), "Manisa": (38.62, 27.43), "Mardin": (37.31, 40.74),
    "Mersin": (36.81, 34.64), "Muğla": (37.22, 28.36), "Muş": (38.73, 41.49),
    "Nevşehir": (38.62, 34.71), "Niğde": (37.97, 34.68), "Ordu": (40.98, 37.88),
    "Osmaniye": (37.07, 36.25), "Rize": (41.02, 40.52), "Sakarya": (40.78, 30.40),
    "Samsun": (41.29, 36.33), "Siirt": (37.93, 41.94), "Sinop": (42.03, 35.15),
    "Sivas": (39.75, 37.02), "Şanlıurfa": (37.16, 38.80), "Şırnak": (37.52, 42.46),
    "Tekirdağ": (40.98, 27.51), "Tokat": (40.31, 36.55), "Trabzon": (41.00, 39.72),
    "Tunceli": (39.11, 39.55), "Uşak": (38.67, 29.41), "Van": (38.49, 43.38),
    "Yalova": (40.65, 29.28), "Yozgat": (39.82, 34.81), "Zonguldak": (41.46, 31.79),
}

BURCLAR = [
    ("Koç", "koc"), ("Boğa", "boga"), ("İkizler", "ikizler"), ("Yengeç", "yengec"),
    ("Aslan", "aslan"), ("Başak", "basak"), ("Terazi", "terazi"), ("Akrep", "akrep"),
    ("Yay", "yay"), ("Oğlak", "oglak"), ("Kova", "kova"), ("Balık", "balik"),
]

# Geleneksel element uyumu — astroloji yorumu, bilimsel iddia değil.
ELEMENT = {"koc": "ates", "aslan": "ates", "yay": "ates",
           "boga": "toprak", "basak": "toprak", "oglak": "toprak",
           "ikizler": "hava", "terazi": "hava", "kova": "hava",
           "yengec": "su", "akrep": "su", "balik": "su"}
ELEMENT_AD = {"ates": "Ateş", "toprak": "Toprak", "hava": "Hava", "su": "Su"}


def _e(x):
    return T._e(x)


def _sayfa(slug, baslik, meta, h1, ozet, govde, sema=None, sss=None):
    """Araç sayfası kabuğu — trend.py'nin başlık/altbilgi kalıbını kullanır."""
    url = KOK_URL + slug
    semalar = []
    semalar.append(json.dumps({
        "@context": "https://schema.org", "@type": "WebApplication", "name": baslik,
        "url": url, "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "Web", "description": meta,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "TRY"},
        "publisher": {"@type": "Organization", "name": "Luna Yapım", "url": "https://lunayapim.com/"},
    }, ensure_ascii=False))
    semalar.append(json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "TrendSaphiens", "item": KOK_URL},
            {"@type": "ListItem", "position": 2, "name": "Araçlar", "item": KOK_URL + "araclar"},
            {"@type": "ListItem", "position": 3, "name": h1, "item": url}]}, ensure_ascii=False))
    if sss:
        semalar.append(json.dumps({
            "@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in sss]}, ensure_ascii=False))
    sema_html = "".join('<script type="application/ld+json">%s</script>' % x for x in semalar)
    sss_html = ""
    if sss:
        sss_html = ('<section class="ts-giris ts-sss"><h2>Sık sorulanlar</h2>%s</section>'
                    % "".join("<h3>%s</h3><p>%s</p>" % (_e(q), _e(a)) for q, a in sss))
    govde_html = """
<main class="ts-arac-sayfa">
  <div class="wrap">
    <nav class="ts-crumbs"><a href="./">TrendSaphiens</a> · <a href="araclar">Araçlar</a></nav>
    <h1>%s</h1>
    <p class="ts-arac-ozet">%s</p>
    %s
    %s
    <p class="ts-not ts-gizlilik">Hesap tarayıcınızda yapılır: girdiğiniz bilgiler hiçbir sunucuya gönderilmez, kaydedilmez.</p>
    <p class="ts-arac-geri"><a href="araclar">← Tüm araçlar</a></p>
    <!-- surum: {SURUM} -->
  </div>
</main>
""".replace("{SURUM}", SURUM) % (_e(h1), _e(ozet), govde, sss_html)
    return T._bas(baslik, meta, url, None, sema_html, "website", "../", "") + govde_html + T._alt("../", "")


# ───────────────────────────────────────────────────────── yükselen burç

YUKSELEN_JS = """
<script>
(function(){
  var IL = %s;
  var Z = ["Koç","Boğa","İkizler","Yengeç","Aslan","Başak","Terazi","Akrep","Yay","Oğlak","Kova","Balık"];
  var ZS = ["koc","boga","ikizler","yengec","aslan","basak","terazi","akrep","yay","oglak","kova","balik"];
  var R = Math.PI/180, D = 180/Math.PI;
  var mod = function(x){ x = x %% 360; return x < 0 ? x + 360 : x; };

  // Yerel saat → UTC kayması: tarayıcının IANA verisi (Türkiye'de 2016'ya kadar yaz saati vardı)
  function ofsetDk(y, ay, g, sa, dk){
    try {
      var d = new Date(Date.UTC(y, ay-1, g, sa, dk));
      var f = new Intl.DateTimeFormat("en-US", {timeZone:"Europe/Istanbul", timeZoneName:"longOffset"});
      var p = f.formatToParts(d).find(function(x){ return x.type === "timeZoneName"; });
      var m = p && p.value.match(/GMT([+-])(\\d{1,2})(?::(\\d{2}))?/);
      if (!m) return 180;
      var s = m[1] === "-" ? -1 : 1;
      return s * (parseInt(m[2],10)*60 + (m[3] ? parseInt(m[3],10) : 0));
    } catch(e){ return 180; }
  }

  function julian(y, ay, g, saatKesri){
    if (ay <= 2){ y -= 1; ay += 12; }
    var A = Math.floor(y/100), B = 2 - A + Math.floor(A/4);
    return Math.floor(365.25*(y+4716)) + Math.floor(30.6001*(ay+1)) + g + saatKesri/24 + B - 1524.5;
  }

  function hesapla(y, ay, g, sa, dk, enlem, boylam){
    var ofs = ofsetDk(y, ay, g, sa, dk);
    var utcDk = sa*60 + dk - ofs;              // yerel → UTC
    var gun = g, kesir = utcDk/60;
    while (kesir < 0){ kesir += 24; gun -= 1; }
    while (kesir >= 24){ kesir -= 24; gun += 1; }
    var JD = julian(y, ay, gun, kesir);
    var Tt = (JD - 2451545.0)/36525;
    var GMST = mod(280.46061837 + 360.98564736629*(JD - 2451545.0) + 0.000387933*Tt*Tt - Tt*Tt*Tt/38710000);
    var RAMC = mod(GMST + boylam);
    var eps = (23.4392911 - 0.0130042*Tt - 0.00000016*Tt*Tt + 0.000000504*Tt*Tt*Tt) * R;
    var ramc = RAMC * R, fi = enlem * R;
    var MC = mod(Math.atan2(Math.sin(ramc), Math.cos(ramc)*Math.cos(eps)) * D);
    var ASC = mod(Math.atan2(Math.cos(ramc), -(Math.sin(eps)*Math.tan(fi) + Math.cos(eps)*Math.sin(ramc))) * D);
    if (mod(ASC - MC) > 180) ASC = mod(ASC + 180);
    return {asc: ASC, mc: MC, ofset: ofs};
  }

  var f = document.getElementById("yuk-form");
  if (!f) return;
  var sec = document.getElementById("yuk-il");
  Object.keys(IL).sort(function(a,b){ return a.localeCompare(b,"tr"); }).forEach(function(ad){
    var o = document.createElement("option"); o.value = ad; o.textContent = ad;
    if (ad === "İstanbul") o.selected = true;
    sec.appendChild(o);
  });

  f.addEventListener("submit", function(ev){
    ev.preventDefault();
    var cikti = document.getElementById("yuk-sonuc");
    var t = (document.getElementById("yuk-tarih").value || "").split("-");
    var s = (document.getElementById("yuk-saat").value || "").split(":");
    if (t.length !== 3 || s.length < 2){
      cikti.innerHTML = "<p class='ts-uyari'>Doğum tarihini ve saatini giriniz.</p>"; return;
    }
    var y = +t[0], ay = +t[1], g = +t[2], sa = +s[0], dk = +s[1];
    if (!(y >= 1900 && y <= 2100)){
      cikti.innerHTML = "<p class='ts-uyari'>Yıl 1900-2100 aralığında olmalı.</p>"; return;
    }
    var k = IL[sec.value] || IL["İstanbul"];
    var r = hesapla(y, ay, g, sa, dk, k[0], k[1]);
    var i = Math.floor(r.asc/30), derece = r.asc %% 30;
    var mci = Math.floor(r.mc/30);
    cikti.innerHTML =
      '<div class="ts-sonuc-kart"><span class="etk">Yükselen burcunuz</span>' +
      '<strong class="ts-sonuc-buyuk">' + Z[i] + '</strong>' +
      '<p>Yükselen derecesi: ' + Z[i] + ' burcunun ' + derece.toFixed(1).replace(".", ",") + '. derecesi. ' +
      'Göğün ortası (MC): ' + Z[mci] + '.</p>' +
      '<p class="ts-not">Hesap ' + sec.value + ' koordinatlarıyla ve o tarihteki ' +
      (r.ofset/60).toString().replace(".", ",") + ' saatlik yerel saat farkıyla yapıldı.</p><p class="yuk-bag"></p></div>';
    var bag = document.createElement("a");
    bag.className = "btn btn-cizgi";
    bag.setAttribute("href", ZS[i] + "-burcu-ozellikleri");
    bag.textContent = Z[i] + " burcunun özellikleri →";
    var yer = cikti.querySelector(".yuk-bag");
    if (yer) yer.appendChild(bag);
    cikti.scrollIntoView({behavior: "smooth", block: "nearest"});
  });
})();
</script>
"""


def yukselen_html():
    form = """
<form id="yuk-form" class="ts-arac-kutu" autocomplete="off">
  <div class="ts-alanlar">
    <label>Doğum tarihi<input type="date" id="yuk-tarih" required min="1900-01-01" max="2100-12-31"></label>
    <label>Doğum saati<input type="time" id="yuk-saat" required></label>
    <label>Doğum ili<select id="yuk-il"></select></label>
  </div>
  <button type="submit" class="btn">Yükselenimi hesapla</button>
</form>
<div id="yuk-sonuc" aria-live="polite"></div>
""" + (YUKSELEN_JS % json.dumps(ILLER, ensure_ascii=False))
    anlatim = """
<section class="ts-giris">
  <h2>Yükselen burç nedir?</h2>
  <p>Yükselen, doğduğunuz anda doğu ufkunda yükselmekte olan zodyak burcudur. Güneş burcu doğum
  gününüze bağlıdır; yükselen ise doğum <em>saatinize</em> ve <em>yerinize</em> bağlıdır.</p>
  <p>Gökyüzü yaklaşık 24 saatte bir tam tur attığı için yükselen ortalama iki saatte bir değişir.
  Dört dakikalık bir saat hatası sonucu yaklaşık bir derece kaydırır; burç sınırına yakın
  doğumlarda bu fark burcu değiştirebilir.</p>
  <h2>Hesap nasıl yapılıyor?</h2>
  <p>Sayfa önce doğum anını evrensel zamana çevirir. Türkiye 8 Eylül 2016'ya kadar yaz saati
  uyguluyordu; bu yüzden saat farkı sabit alınmaz, tarayıcınızın saat dilimi veritabanından o
  tarihe ait gerçek fark okunur.</p>
  <p>Ardından Julian gün sayısı ve Greenwich yıldız zamanı hesaplanır, doğum ilinin boylamı
  eklenerek yerel yıldız zamanı bulunur. Ufuk ile ekliptiğin kesiştiği nokta, ekliptik eğikliği
  ve enlem kullanılarak çözülür. Sonuç, yükselenin hangi burçta ve kaçıncı derecede olduğudur.</p>
  <h2>Doğum saatimi bilmiyorsam?</h2>
  <p>Yükselen saat olmadan hesaplanamaz. Doğum saati nüfus kayıt örneğinde ya da doğum belgesinde
  yer alır; e-Devlet üzerinden nüfus kayıt örneği alınabilir. Yaklaşık bir saat girerseniz sonuç
  da yaklaşık olur.</p>
  <h2>Yükselen ile güneş burcu arasındaki fark</h2>
  <p>Güneş burcu, doğduğunuz gün Güneş'in hangi zodyak diliminde olduğunu söyler. Aynı gün doğan
  herkesin güneş burcu aynıdır. Yükselen ise saat ve yere bağlı olduğu için aynı gün doğan iki
  kişide farklı çıkabilir.</p>
  <p>Astroloji geleneğinde güneş burcu temel eğilimi, yükselen ise kişinin dışarıya dönük yüzünü
  anlatır diye yorumlanır. Bu ayrımın kişilik araştırmalarında bir karşılığı yoktur; geleneğin
  kendi açıklamasıdır.</p>
  <h2>Göğün ortası (MC) nedir?</h2>
  <p>Sonuçta yükselenle birlikte göğün ortası da verilir. MC, doğum anında tam tepe noktasından
  geçen ekliptik derecesidir. Astrolojide meslek ve toplumsal görünürlükle ilişkilendirilir.</p>
  <h2>Hesap ne kadar hassas?</h2>
  <p>Kullanılan bağıntılar astronomi literatürünün standart yaklaşımlarıdır ve yükseleni derece
  düzeyinde verir. Doğruluğu sınırlayan şey formül değil, girdiğiniz doğum saatinin kesinliğidir.
  İl merkezi koordinatı kullanıldığı için aynı ildeki ilçe farkı sonucu pratikte değiştirmez.</p>
</section>
<p class="ts-not ts-durust">Astroloji bir inanç ve kültür alanıdır; kişiliği ölçen ya da geleceği
bildiren bilimsel bir yöntem değildir. Buradaki hesap gökyüzünün o andaki konumunu doğru şekilde
bulur — bu konumun insan karakteriyle ilişkisi astrolojinin kendi yorumudur.</p>
"""
    sss = [
        ("Yükselen burç nasıl hesaplanır?", "Doğum tarihi, saati ve yerinin koordinatları kullanılarak, doğum anında doğu ufkunda yükselen zodyak derecesi bulunur. Hesap yıldız zamanı, ekliptik eğikliği ve enlem üzerinden yapılır."),
        ("Yükselen kaç saatte bir değişir?", "Ortalama iki saatte bir. Yıl içinde ve enleme göre bu süre bir miktar değişir."),
        ("Doğum saatim yanlışsa ne olur?", "Dört dakikalık hata yaklaşık bir derecelik kayma yaratır. Burç sınırına yakın doğumlarda yükselen komşu burca kayabilir."),
        ("Bilgilerim kaydediliyor mu?", "Hayır. Hesap tarayıcınızda çalışır; doğum tarihi, saati ve iliniz hiçbir sunucuya gönderilmez."),
    ]
    return _sayfa(
        "yukselen-burc-hesaplama",
        "Yükselen Burç Hesaplama — doğum saatine göre | TrendSaphiens",
        "Doğum tarihi, saati ve iline göre yükselen burcunuzu hesaplayın. Hesap tarayıcınızda yapılır, bilgileriniz hiçbir yere gönderilmez.",
        "Yükselen burç hesaplama",
        "Doğum tarihinizi, saatinizi ve ilinizi girin; yükselen burcunuz ve derecesi anında çıksın.",
        form + anlatim, sss=sss)


# ───────────────────────────────────────────────────────── burç uyumu

def uyumu_html():
    # Geleneksel yorum: aynı element ve tamamlayıcı element yüksek, kare/karşıt açılar zorlu sayılır.
    def puan(a, b):
        ea, eb = ELEMENT[a], ELEMENT[b]
        if a == b:
            return 4, "Aynı burç: benzerlik rahatlık verir, aynı körlükler de paylaşılır."
        if ea == eb:
            return 5, "Aynı element: astrolojide en akıcı eşleşme sayılır."
        if {ea, eb} in ({"ates", "hava"}, {"toprak", "su"}):
            return 4, "Tamamlayıcı elementler: geleneksel yorumda birbirini besler."
        return 2, "Farklı element grupları: uyum için karşılıklı çaba beklenir."

    satir = []
    for ad, s in BURCLAR:
        hucre = []
        for ad2, s2 in BURCLAR:
            p, _ = puan(s, s2)
            hucre.append('<td class="p%d" title="%s – %s"><span>%d</span></td>' % (p, _e(ad), _e(ad2), p))
        satir.append('<tr><th scope="row"><a href="%s-burcu-ozellikleri">%s</a></th>%s</tr>'
                     % (s, _e(ad), "".join(hucre)))
    tablo = ('<div class="ts-tablo-sar"><table class="ts-uyum"><caption>Geleneksel astroloji yorumuna göre '
             'element uyumu — 5 en akıcı, 2 en çok çaba isteyen</caption><thead><tr><th></th>%s</tr></thead>'
             '<tbody>%s</tbody></table></div>'
             % ("".join('<th scope="col"><abbr title="%s">%s</abbr></th>' % (_e(a), _e(a[:2])) for a, _s in BURCLAR),
                "".join(satir)))
    anlatim = """
<section class="ts-giris">
  <h2>Burç uyumu neye göre hesaplanır?</h2>
  <p>Astrolojide uyum, iki burcun zodyak çemberi üzerindeki açısına ve elementlerine bakılarak
  yorumlanır. Dört element vardır: ateş, toprak, hava ve su.</p>
  <p>Aynı elementten iki burç geleneksel yorumda en akıcı eşleşme sayılır. Ateş ile hava, toprak
  ile su ise birbirini tamamlayıcı kabul edilir. Farklı gruplardan gelen eşleşmeler zorlu değil,
  daha çok karşılıklı çaba isteyen eşleşmeler olarak anlatılır.</p>
  <h2>Dört element ve burçları</h2>
  <p>Ateş grubunda Koç, Aslan ve Yay; toprak grubunda Boğa, Başak ve Oğlak; hava grubunda
  İkizler, Terazi ve Kova; su grubunda Yengeç, Akrep ve Balık bulunur. Her grupta üç burç
  vardır ve bunlar çember üzerinde birbirinden 120 derece aralıkla durur.</p>
  <p>Geleneksel yorumda bu 120 derecelik açı uyumlu, 90 derecelik açı ise gerilimli sayılır.
  Tablodaki renkler bu açı mantığının sadeleştirilmiş hâlidir.</p>
  <h2>Aynı burçtan iki kişi</h2>
  <p>Tabloda aynı burç eşleşmeleri en yüksek puanı almaz. Astroloji metinlerinde bunun nedeni
  şöyle anlatılır: benzerlik anlaşmayı kolaylaştırır ama aynı zayıf noktaların iki kişide birden
  bulunması dengeleyici bir taraf bırakmaz.</p>
  <h2>Bu tablo ne kadar ciddiye alınmalı?</h2>
  <p>Tablo, astroloji geleneğinin kendi kurallarını düzenli biçimde gösterir. İki insanın
  anlaşmasını belirleyen şeyin doğum ayı olduğuna dair bir bulgu yoktur. Eşleşmeyi merak
  etmek eğlencelidir; karar vermek için kullanmak başka bir şeydir.</p>
  <p>Astrolojiyle ilgilenenler de yalnız güneş burcuna bakmanın geleneğin en kaba hâli olduğunu
  söyler; yükselen ve diğer gezegen konumları hesaba katılmadan yapılan uyum yorumu, o gelenek
  içinde bile eksik sayılır.</p>
</section>
<p class="ts-not ts-durust">Astroloji kişiliği ya da ilişki başarısını ölçmez. Bu sayfa
astrolojinin kendi yorum geleneğini aktarır.</p>
"""
    sss = [
        ("Hangi burçlar birbiriyle uyumlu sayılır?", "Geleneksel yorumda aynı elementten burçlar (ateş-ateş, su-su gibi) ve tamamlayıcı elementler (ateş-hava, toprak-su) uyumlu kabul edilir."),
        ("Burç uyumu ilişkinin geleceğini gösterir mi?", "Hayır. Astroloji bir kültür ve inanç alanıdır; ilişki uyumunu ölçen bilimsel bir yöntem değildir."),
        ("Yükselen burç uyumu etkiler mi?", "Astrolojide yükselen ve diğer gezegen konumları da yoruma katılır. Yalnız güneş burcuna bakmak geleneğin en basit hâlidir."),
    ]
    return _sayfa(
        "burc-uyumu",
        "Burç Uyumu Tablosu — 12 burcun eşleşmesi | TrendSaphiens",
        "Hangi burç hangisiyle uyumlu sayılır? 12 burcun element ve açı yorumuna göre hazırlanmış uyum tablosu ve açıklaması.",
        "Burç uyumu tablosu",
        "On iki burcun birbiriyle eşleşmesi, astrolojinin kendi element kurallarına göre tek tabloda.",
        tablo + anlatim, sss=sss)


# ───────────────────────────────────────────────────────── hesaplayıcılar

HESAP_JS = """
<script>
(function(){
  function el(id){ return document.getElementById(id); }
  function yaz(id, html){ var c = el(id); if (c) c.innerHTML = html; }
  function vir(x){ return String(x).replace(".", ","); }

  var yf = el("yas-form");
  if (yf) yf.addEventListener("submit", function(e){
    e.preventDefault();
    var d = el("yas-dogum").value, h = el("yas-hedef").value || new Date().toISOString().slice(0,10);
    if (!d) return yaz("yas-sonuc", "<p class='ts-uyari'>Doğum tarihini giriniz.</p>");
    var a = new Date(d + "T00:00:00"), b = new Date(h + "T00:00:00");
    if (b < a) return yaz("yas-sonuc", "<p class='ts-uyari'>Hedef tarih doğum tarihinden önce olamaz.</p>");
    var y = b.getFullYear() - a.getFullYear(), ay = b.getMonth() - a.getMonth(), g = b.getDate() - a.getDate();
    if (g < 0){ ay -= 1; g += new Date(b.getFullYear(), b.getMonth(), 0).getDate(); }
    if (ay < 0){ y -= 1; ay += 12; }
    var gun = Math.round((b - a)/86400000);
    var sonraki = new Date(b.getFullYear(), a.getMonth(), a.getDate());
    if (sonraki < b) sonraki = new Date(b.getFullYear()+1, a.getMonth(), a.getDate());
    var kalan = Math.round((sonraki - b)/86400000);
    yaz("yas-sonuc", "<div class='ts-sonuc-kart'><span class='etk'>Yaşınız</span>" +
      "<strong class='ts-sonuc-buyuk'>" + y + " yıl " + ay + " ay " + g + " gün</strong>" +
      "<p>Toplam " + gun.toLocaleString("tr-TR") + " gün · yaklaşık " + Math.floor(gun/7).toLocaleString("tr-TR") + " hafta.</p>" +
      "<p>Bir sonraki doğum gününe " + kalan + " gün var.</p></div>");
  });

  var vf = el("vki-form");
  if (vf) vf.addEventListener("submit", function(e){
    e.preventDefault();
    var boy = parseFloat(el("vki-boy").value), kilo = parseFloat(el("vki-kilo").value);
    if (!(boy > 0 && kilo > 0)) return yaz("vki-sonuc", "<p class='ts-uyari'>Boy ve kiloyu giriniz.</p>");
    if (boy > 3) boy = boy/100;
    if (boy < 0.6 || boy > 2.6 || kilo < 15 || kilo > 400)
      return yaz("vki-sonuc", "<p class='ts-uyari'>Girilen değerler beklenen aralığın dışında.</p>");
    var v = kilo/(boy*boy), ad;
    if (v < 18.5) ad = "zayıf"; else if (v < 25) ad = "normal";
    else if (v < 30) ad = "fazla kilolu"; else if (v < 35) ad = "1. derece obez";
    else if (v < 40) ad = "2. derece obez"; else ad = "3. derece obez";
    yaz("vki-sonuc", "<div class='ts-sonuc-kart'><span class='etk'>Vücut kitle indeksiniz</span>" +
      "<strong class='ts-sonuc-buyuk'>" + vir(v.toFixed(1)) + "</strong>" +
      "<p>Dünya Sağlık Örgütü sınıflamasında <b>" + ad + "</b> aralığına denk geliyor.</p>" +
      "<p class='ts-not'>VKİ kas ve yağ ayrımı yapmaz; sporcularda ve yaşlılarda yanıltabilir. Tanı değildir.</p></div>");
  });

  var pf = el("yuzde-form");
  if (pf) pf.addEventListener("submit", function(e){
    e.preventDefault();
    var t = el("yuzde-tur").value, a = parseFloat(el("yuzde-a").value), b = parseFloat(el("yuzde-b").value);
    if (isNaN(a) || isNaN(b)) return yaz("yuzde-sonuc", "<p class='ts-uyari'>İki sayıyı da giriniz.</p>");
    var s = "", n;
    if (t === "kaci"){ n = a*b/100; s = vir(a) + " sayısının %" + vir(b) + "'i = <b>" + vir(+n.toFixed(4)) + "</b>"; }
    else if (t === "oran"){ if (b === 0) return yaz("yuzde-sonuc", "<p class='ts-uyari'>İkinci sayı sıfır olamaz.</p>");
      n = a/b*100; s = vir(a) + " sayısı " + vir(b) + " sayısının <b>%" + vir(+n.toFixed(2)) + "</b>'idir"; }
    else if (t === "artis"){ if (a === 0) return yaz("yuzde-sonuc", "<p class='ts-uyari'>İlk sayı sıfır olamaz.</p>");
      n = (b-a)/Math.abs(a)*100; s = vir(a) + " → " + vir(b) + " değişimi <b>%" + vir(+n.toFixed(2)) + "</b> " + (n >= 0 ? "artış" : "azalış"); }
    else { n = a + a*b/100; s = vir(a) + " sayısına %" + vir(b) + " eklenince <b>" + vir(+n.toFixed(4)) + "</b>"; }
    yaz("yuzde-sonuc", "<div class='ts-sonuc-kart'><p class='ts-sonuc-orta'>" + s + "</p></div>");
  });
})();
</script>
"""


def yas_html():
    form = """
<form id="yas-form" class="ts-arac-kutu" autocomplete="off">
  <div class="ts-alanlar">
    <label>Doğum tarihi<input type="date" id="yas-dogum" required></label>
    <label>Hangi tarihteki yaş<input type="date" id="yas-hedef"></label>
  </div>
  <button type="submit" class="btn">Yaşı hesapla</button>
</form>
<div id="yas-sonuc" aria-live="polite"></div>
""" + HESAP_JS
    anlatim = """
<section class="ts-giris">
  <h2>Yaş nasıl hesaplanır?</h2>
  <p>Yaş, doğum tarihinden bugüne geçen tam yıl sayısıdır. Doğum günü henüz gelmediyse o yıl
  sayılmaz — bu yüzden hesap yalnız yılları çıkarmakla yapılmaz.</p>
  <p>Araç ayrıca kalan ay ve günü, toplam gün sayısını ve bir sonraki doğum gününe kaç gün
  kaldığını verir. İkinci tarihi boş bırakırsanız bugüne göre hesaplanır; belirli bir tarihteki
  yaşı öğrenmek için ikinci alanı doldurun.</p>
  <h2>Artık yıllar hesaba katılıyor mu?</h2>
  <p>Evet. Gün farkı takvim üzerinden hesaplandığı için 29 Şubat içeren yıllar kendiliğinden
  doğru sayılır.</p>
  <h2>29 Şubat'ta doğanlar</h2>
  <p>Dört yılda bir gelen bu tarihte doğanların yaşı, artık olmayan yıllarda 28 Şubat ya da
  1 Mart üzerinden sayılır. Türkiye'de nüfus kayıtlarında doğum tarihi olduğu gibi durur; yaş
  hesabı takvim yılına göre işler.</p>
  <h2>Yaş hesabı nerelerde gerekir?</h2>
  <p>Okula başlama, ehliyet, askerlik, sigorta ve bazı başvurularda yaş belirli bir tarihteki
  duruma göre değerlendirilir. Bu yüzden araçta ikinci tarih alanı var: başvuru tarihini yazıp
  o gündeki yaşınızı görebilirsiniz.</p>
  <h2>Toplam gün ve hafta ne işe yarar?</h2>
  <p>Bebeklerde gelişim haftayla, yetişkinlerde bazı sağlık takipleri günle izlenir. Araç
  toplam gün ve yaklaşık hafta sayısını da verdiği için bu hesapları ayrıca yapmak gerekmez.</p>
  <h2>Yaş ile burç aynı anda değişmez</h2>
  <p>Doğum günü yaşı bir artırır ama burcu değiştirmez; burç doğum tarihine sabitlidir. Burç
  sınırına yakın günlerde doğanlar için tarih aralıkları yıldan yıla bir gün oynayabilir,
  çünkü mevsim dönümleri her yıl tam aynı saatte gerçekleşmez.</p>
  <h2>İki tarih arasını hesaplamak</h2>
  <p>Araç yalnız yaş için değil, herhangi iki tarih arasındaki süre için de kullanılabilir. İlk
  alana başlangıç, ikinci alana bitiş tarihini yazmanız yeterli: aradaki yıl, ay, gün ve toplam
  gün sayısı aynı biçimde çıkar.</p>
</section>
"""
    sss = [
        ("Yaş hesaplama nasıl yapılır?", "Doğum tarihi ile hedef tarih arasındaki tam yıl sayısı bulunur; doğum günü o yıl içinde henüz gelmemişse bir yıl eksilir. Kalan süre ay ve gün olarak verilir."),
        ("Belirli bir tarihteki yaşımı öğrenebilir miyim?", "Evet, ikinci alana o tarihi yazın. Boş bırakırsanız bugüne göre hesaplanır."),
        ("Artık yıl sonucu etkiler mi?", "Gün sayısı takvim üzerinden hesaplandığı için artık yıllar otomatik olarak doğru sayılır."),
    ]
    return _sayfa("yas-hesaplama", "Yaş Hesaplama — doğum tarihine göre tam yaş | TrendSaphiens",
                  "Doğum tarihinizi girin; yıl, ay ve gün olarak tam yaşınızı, toplam gün sayısını ve doğum gününüze kalan süreyi görün.",
                  "Yaş hesaplama", "Doğum tarihinden bugüne kaç yıl, ay ve gün geçtiğini tam olarak hesaplayın.",
                  form + anlatim, sss=sss)


def vki_html():
    form = """
<form id="vki-form" class="ts-arac-kutu" autocomplete="off">
  <div class="ts-alanlar">
    <label>Boy (cm)<input type="number" id="vki-boy" min="60" max="260" step="0.1" required placeholder="175"></label>
    <label>Kilo (kg)<input type="number" id="vki-kilo" min="15" max="400" step="0.1" required placeholder="70"></label>
  </div>
  <button type="submit" class="btn">VKİ hesapla</button>
</form>
<div id="vki-sonuc" aria-live="polite"></div>
""" + HESAP_JS
    anlatim = """
<section class="ts-giris">
  <h2>Vücut kitle indeksi nedir?</h2>
  <p>Vücut kitle indeksi (VKİ), kilonun boyun karesine bölünmesiyle bulunan bir orandır:
  kilogram bölü metre kare. Dünya Sağlık Örgütü bu oranı toplum düzeyinde kilo dağılımını
  izlemek için kullanır.</p>
  <h2>Aralıklar ne anlama geliyor?</h2>
  <p>18,5 altı zayıf, 18,5–24,9 normal, 25–29,9 fazla kilolu, 30 ve üzeri obez olarak
  sınıflandırılır. Obezite ayrıca üç dereceye ayrılır.</p>
  <h2>VKİ neyi ölçmez?</h2>
  <p>VKİ kas ile yağı ayırt etmez. Düzenli antrenman yapan biri yüksek kas kütlesi yüzünden
  "fazla kilolu" çıkabilir; yaşlılarda kas kaybı nedeniyle tersi olabilir. Çocuklarda ve
  gebelikte yetişkin aralıkları kullanılmaz.</p>
  <p>Yağın nerede toplandığını da göstermez. Aynı VKİ değerine sahip iki kişiden bel çevresi
  geniş olanın metabolik riski daha yüksek kabul edilir; bu yüzden sağlık değerlendirmesinde
  bel çevresi ölçümü VKİ'nin yanında kullanılır.</p>
  <h2>Nereden geliyor bu formül?</h2>
  <p>Oran, 19. yüzyılda Belçikalı istatistikçi Adolphe Quetelet tarafından toplumdaki kilo
  dağılımını tanımlamak için önerildi. Uzun süre "Quetelet indeksi" diye anıldı. Yani başından
  beri toplum ölçeğinde bir araç; bireyi teşhis etmek için tasarlanmadı.</p>
  <h2>Sayıyı gördükten sonra ne yapmalı?</h2>
  <p>Tek bir ölçüm bir durum değil, bir başlangıç noktasıdır. Değer aralık dışındaysa doğru adım
  internetten diyet aramak değil, hekime ya da diyetisyene danışmaktır. Aralık içindeyse de
  düzenli hareket ve dengeli beslenme tavsiyesi değişmez.</p>
</section>
<p class="ts-not ts-durust">Bu hesap bir tarama aracıdır, tıbbi tanı değildir. Kilonuzla ilgili
bir kaygınız varsa değerlendirmeyi hekiminiz yapmalıdır.</p>
"""
    sss = [
        ("VKİ nasıl hesaplanır?", "Kilo (kg) bölü boyun karesi (m²). Örneğin 70 kilo ve 1,75 metre için 70 / (1,75 × 1,75) = 22,9."),
        ("Normal VKİ aralığı nedir?", "Dünya Sağlık Örgütü sınıflamasında yetişkinler için 18,5 ile 24,9 arası normal kabul edilir."),
        ("VKİ sporcularda doğru sonuç verir mi?", "Vermeyebilir. VKİ kas ve yağ ayrımı yapmadığı için yüksek kas kütlesi olan kişilerde olduğundan yüksek çıkar."),
    ]
    return _sayfa("vucut-kitle-indeksi", "VKİ Hesaplama — vücut kitle indeksi | TrendSaphiens",
                  "Boy ve kilonuzu girin, vücut kitle indeksinizi ve Dünya Sağlık Örgütü sınıflamasındaki karşılığını görün. Tanı değildir.",
                  "Vücut kitle indeksi hesaplama",
                  "Boy ve kilodan VKİ değerinizi hesaplayın, aralıkların ne anlama geldiğini okuyun.",
                  form + anlatim, sss=sss)


def yuzde_html():
    form = """
<form id="yuzde-form" class="ts-arac-kutu" autocomplete="off">
  <div class="ts-alanlar">
    <label>Soru türü<select id="yuzde-tur">
      <option value="kaci">A sayısının yüzde B'si kaç?</option>
      <option value="oran">A, B'nin yüzde kaçı?</option>
      <option value="artis">A'dan B'ye yüzde kaç değişti?</option>
      <option value="ekle">A'ya yüzde B eklenirse?</option>
    </select></label>
    <label>A sayısı<input type="number" id="yuzde-a" step="any" required placeholder="250"></label>
    <label>B sayısı<input type="number" id="yuzde-b" step="any" required placeholder="18"></label>
  </div>
  <button type="submit" class="btn">Hesapla</button>
</form>
<div id="yuzde-sonuc" aria-live="polite"></div>
""" + HESAP_JS
    anlatim = """
<section class="ts-giris">
  <h2>Yüzde hesaplama kuralları</h2>
  <p>Yüzde, yüz birimlik bir bütünün kaç biriminden söz edildiğini gösterir. Bir sayının yüzde
  kaçı sorusunda sayı yüzde oranıyla çarpılıp yüze bölünür.</p>
  <p>Yüzde değişim sorusunda ise iki değer arasındaki fark, başlangıç değerine bölünür. Zam,
  indirim ve artış hesapları bu kuralla yapılır. Başlangıç değeri sıfırsa yüzde değişim
  tanımsızdır.</p>
  <h2>Sık yapılan hata: yüzde ekleme ve çıkarma simetrik değildir</h2>
  <p>Bir fiyata yüzde 20 zam yapıp sonra yüzde 20 indirim uygularsanız başlangıç fiyatına
  dönmezsiniz. 100 lira yüzde 20 zamla 120 olur; 120'nin yüzde 20 indirimi 96'dır.</p>
  <h2>Yüzde puan ile yüzde aynı şey değil</h2>
  <p>Bir oran yüzde 20'den yüzde 25'e çıktığında "5 puan arttı" denir. Bunu "yüzde 5 arttı" diye
  söylemek yanlıştır, çünkü göreli artış yüzde 25'tir. Haberlerde faiz ve işsizlik oranları
  anlatılırken bu ayrım sık karışır.</p>
  <h2>Ardışık indirimler toplanmaz</h2>
  <p>Yüzde 30 indirimin üstüne yüzde 20 daha indirim, yüzde 50 indirim demek değildir. İkinci
  indirim, ilkinden sonra kalan tutara uygulanır: 100 lira önce 70'e, sonra 56'ya iner. Toplam
  indirim yüzde 44'tür.</p>
  <h2>KDV dahil fiyattan KDV'yi ayırmak</h2>
  <p>Yüzde 20 KDV dahil 120 liralık bir üründe KDV tutarı 20 liradır, 24 değil. Dahil fiyattan
  vergiyi bulmak için tutar 1,20'ye bölünür ve çıkan sonuç fiyattan çıkarılır.</p>
</section>
"""
    sss = [
        ("Bir sayının yüzde kaçı nasıl bulunur?", "Sayı, yüzde oranıyla çarpılır ve yüze bölünür. 250 sayısının yüzde 18'i: 250 × 18 / 100 = 45."),
        ("Yüzde değişim nasıl hesaplanır?", "Yeni değerden eski değer çıkarılır, sonuç eski değere bölünüp yüzle çarpılır."),
        ("Yüzde 20 zam sonrası yüzde 20 indirim başa döndürür mü?", "Hayır. Zam ve indirim farklı tabanlar üzerinden hesaplandığı için sonuç başlangıçtan düşük çıkar."),
    ]
    return _sayfa("yuzde-hesaplama", "Yüzde Hesaplama — oran, artış ve indirim | TrendSaphiens",
                  "Bir sayının yüzde kaçı, yüzde değişim, zam ve indirim hesapları tek sayfada. Kurallar ve sık yapılan hata örnekleriyle.",
                  "Yüzde hesaplama",
                  "Dört farklı yüzde sorusunu tek araçta çözün: yüzdesi, oranı, değişimi ve eklemeli hâli.",
                  form + anlatim, sss=sss)


# ───────────────────────────────────────────────────────── örüntü oyunu

SORULAR = [
    ("2, 4, 8, 16, ? — sıradaki sayı nedir?", ["24", "32", "30", "64"], 1,
     "Her adımda sayı ikiyle çarpılıyor: 16 × 2 = 32."),
    ("3, 6, 11, 18, ? — sıradaki sayı nedir?", ["27", "25", "29", "24"], 0,
     "Eklenen fark her adımda ikişer artıyor: +3, +5, +7, +9 → 18 + 9 = 27."),
    ("Bütün güller çiçektir. Bazı çiçekler hızlı solar. Buradan kesin olarak ne çıkar?",
     ["Bazı güller hızlı solar", "Bütün güller hızlı solar", "Hiçbir gül hızlı solmaz", "Kesin bir sonuç çıkmaz"], 3,
     "Hızlı solan çiçeklerin güller olup olmadığı bilinmiyor; öncüller kesin sonuç vermiyor."),
    ("Bir küpün her yüzü boyanıp 27 eşit küçük küpe ayrılıyor. Kaç küçük küpün hiçbir yüzü boyalı değildir?",
     ["1", "6", "8", "12"], 0, "Yalnız tam ortadaki küp dışarıya hiç değmez."),
    ("A, B'den uzun. C, A'dan uzun. D, B'den kısa. En uzun kim?", ["A", "B", "C", "D"], 2,
     "C > A > B > D sıralaması kuruluyor."),
    ("1, 1, 2, 3, 5, 8, ? — sıradaki sayı nedir?", ["11", "12", "13", "15"], 2,
     "Her sayı kendinden önceki ikisinin toplamı: 5 + 8 = 13."),
    ("Saat 15.20'de akrep ile yelkovan arasındaki açı kaç derecedir?", ["20", "30", "50", "70"], 0,
     "Yelkovan 20 dakikada 20 × 6 = 120°. Akrep saat 3 konumunda 90°, üstüne 20 × 0,5 = 10° ekler, 100° olur. Aradaki açı 120 − 100 = 20°."),
    ("Bir işi 4 işçi 6 günde bitiriyor. Aynı hızda 3 işçi kaç günde bitirir?", ["7", "8", "9", "12"], 1,
     "Toplam iş 24 işçi-gün; 24 / 3 = 8 gün."),
    ("KİTAP → PATİK ilişkisi nedir?", ["Eş anlam", "Harflerin tersten dizilişi", "Zıt anlam", "Hece değişimi"], 1,
     "KİTAP sözcüğünün harfleri tersten okunduğunda PATİK elde edilir."),
    ("81, 64, 49, 36, ? — sıradaki sayı nedir?", ["25", "28", "24", "30"], 0,
     "Sayılar sırayla 9², 8², 7², 6² — sıradaki 5² = 25."),
]


def oyun_html():
    veri = json.dumps([{"s": q, "c": ch, "d": d, "a": ac} for q, ch, d, ac in SORULAR], ensure_ascii=False)
    js = """
<script>
(function(){
  var S = %s, i = 0, dogru = 0, cevaplar = [];
  var kutu = document.getElementById("oyun-kutu");
  if (!kutu) return;
  function ciz(){
    if (i >= S.length) return bitir();
    var q = S[i];
    kutu.innerHTML = '<p class="ts-oyun-sayac">Soru ' + (i+1) + ' / ' + S.length + '</p>' +
      '<h2 class="ts-oyun-soru">' + q.s + '</h2>' +
      '<div class="ts-oyun-secenek">' + q.c.map(function(c, n){
        return '<button type="button" data-n="' + n + '">' + c + '</button>'; }).join("") + '</div>';
    Array.prototype.forEach.call(kutu.querySelectorAll("button"), function(b){
      b.addEventListener("click", function(){
        var n = +b.getAttribute("data-n"), q = S[i];
        cevaplar.push({s: q.s, verilen: q.c[n], dogru: q.c[q.d], aciklama: q.a, oldu: n === q.d});
        if (n === q.d) dogru++;
        i++; ciz();
      });
    });
  }
  function bitir(){
    var yorum = dogru >= 9 ? "Örüntüleri çok hızlı yakaladınız."
              : dogru >= 7 ? "Sayı ve mantık sorularında rahatsınız."
              : dogru >= 4 ? "Bir kısmını çözdünüz; açıklamalara bakmak iyi gelir."
              : "Bu tur zorlandınız. Açıklamalar yöntemi gösteriyor.";
    kutu.innerHTML = '<div class="ts-sonuc-kart"><span class="etk">Sonuç</span>' +
      '<strong class="ts-sonuc-buyuk">' + dogru + ' / ' + S.length + '</strong><p>' + yorum + '</p>' +
      '<p class="ts-not">Bu bir zekâ testi değildir ve IQ puanı vermez. On soruluk bir örüntü oyunudur.</p></div>' +
      '<div class="ts-oyun-dokum"><h2>Cevaplar ve açıklamaları</h2>' +
      cevaplar.map(function(c){
        return '<div class="' + (c.oldu ? "ok" : "yanlis") + '"><p class="s">' + c.s + '</p>' +
               '<p class="v">Verdiğiniz: ' + c.verilen + (c.oldu ? "" : " · Doğrusu: " + c.dogru) + '</p>' +
               '<p class="a">' + c.aciklama + '</p></div>'; }).join("") + '</div>' +
      '<p><button type="button" class="btn" id="oyun-tekrar">Yeniden dene</button></p>';
    var t = document.getElementById("oyun-tekrar");
    if (t) t.addEventListener("click", function(){ i = 0; dogru = 0; cevaplar = []; ciz(); });
  }
  ciz();
})();
</script>
""" % veri
    anlatim = """
<section class="ts-giris">
  <h2>Bu oyun neyi ölçer, neyi ölçmez?</h2>
  <p>Buradaki on soru sayı dizileri, mantık çıkarımı ve uzamsal düşünme üzerine kurulu. Doğru
  sayınız bu tür soruları o an ne kadar hızlı çözdüğünüzü gösterir.</p>
  <p>Zekâ ölçümü bundan başka bir şeydir. Gerçek zekâ testleri uzman gözetiminde, standart
  koşullarda, yaş grubuna göre normlanmış maddelerle uygulanır ve tek oturumda sonuç
  üretmez. İnternette IQ puanı veren sayfaların verdiği sayı bir ölçüm değil, bir süstür.</p>
  <h2>Soruları kim hazırladı?</h2>
  <p>Sorular TrendSaphiens için yazıldı; her birinin çözümü sonuç ekranında adım adım
  açıklanıyor. Amaç puan vermek değil, yöntemi göstermek.</p>
  <h2>Sayı dizilerinde ne aranır?</h2>
  <p>Bir dizide önce ardışık terimlerin farkına bakılır. Fark sabitse dizi aritmetiktir. Fark
  düzenli olarak büyüyorsa ikinci fark alınır. Oran sabitse dizi geometriktir. Bu üç kontrol
  çoğu soruyu çözer.</p>
  <p>Çözülmüyorsa sayıların kare, küp ya da asal olup olmadığına bakılır. Bu oyundaki 81, 64, 49
  dizisi tam kareler; 1, 1, 2, 3, 5 dizisi ise her terimin önceki ikisinin toplamı olduğu
  Fibonacci dizisidir.</p>
  <h2>Mantık sorularında en sık yapılan hata</h2>
  <p>"Bütün A'lar B'dir" ile "bütün B'ler A'dır" aynı şey değildir. Öncüller kesin sonuç
  vermiyorsa doğru cevap çoğu zaman "kesin bir sonuç çıkmaz" olur. Sezgiye uyan cevap ile
  öncüllerin izin verdiği cevap her zaman aynı olmaz.</p>
  <h2>Süre tutmuyoruz, neden?</h2>
  <p>Zaman baskısı doğru sayısını düşürür ama düşünme biçimini göstermez. Buradaki amaç sıralama
  değil, soruyu çözdükten sonra yöntemi görmek. Bu yüzden geri sayım yok; takılırsanız
  bırakıp sonra dönebilirsiniz.</p>
  <h2>Bu tür sorular geliştirilebilir mi?</h2>
  <p>Örüntü sorularında pratikle gelişme olur: aynı kalıplar tekrar ettiği için çözüm yolları
  tanıdık gelmeye başlar. Bunun genel zihinsel yetenekleri artırdığına dair güçlü bir kanıt
  yoktur; gelişen şey çoğunlukla o soru tipindeki beceridir.</p>
</section>
<p class="ts-not ts-durust">Bu sayfa eğlence ve pratik amaçlıdır. IQ ölçmez, zekâ tanısı koymaz,
sonucu hiçbir yere kaydetmez.</p>
"""
    sss = [
        ("Bu bir IQ testi mi?", "Hayır. On soruluk bir örüntü ve mantık oyunudur; IQ puanı vermez. Gerçek zekâ testleri uzman gözetiminde ve normlanmış maddelerle uygulanır."),
        ("Sonucum kaydediliyor mu?", "Hayır. Sorular ve sonuç tarayıcınızda kalır, hiçbir sunucuya gönderilmez."),
        ("Soruların çözümünü görebilir miyim?", "Evet. Oyun bittiğinde her sorunun doğru cevabı ve çözüm açıklaması listelenir."),
    ]
    return _sayfa("oruntu-oyunu", "Örüntü ve Mantık Oyunu — 10 soru | TrendSaphiens",
                  "Sayı dizileri, mantık çıkarımı ve uzamsal düşünme üzerine on soru. Her sorunun çözümü açıklamalı. IQ testi değildir.",
                  "Örüntü ve mantık oyunu",
                  "On soru, her birinin çözümü açıklamalı. Puan değil yöntem veren bir oyun.",
                  '<div id="oyun-kutu" class="ts-arac-kutu ts-oyun"></div>' + js + anlatim, sss=sss)


# ───────────────────────────────────────────────────────── araç dizini

ARACLAR = [
    ("yukselen-burc-hesaplama", "Yükselen burç hesaplama", "Doğum tarihi, saati ve iline göre yükselen burcunuz ve derecesi.", "Burç"),
    ("burc-uyumu", "Burç uyumu tablosu", "On iki burcun eşleşmesi, astrolojinin element kurallarına göre.", "Burç"),
    ("yas-hesaplama", "Yaş hesaplama", "Yıl, ay, gün olarak tam yaş ve doğum gününe kalan süre.", "Günlük"),
    ("vucut-kitle-indeksi", "Vücut kitle indeksi", "Boy ve kilodan VKİ ve Dünya Sağlık Örgütü aralıkları.", "Sağlık"),
    ("yuzde-hesaplama", "Yüzde hesaplama", "Yüzdesi, oranı, değişimi ve eklemeli hâli tek araçta.", "Günlük"),
    ("oruntu-oyunu", "Örüntü ve mantık oyunu", "On soru, çözümleri açıklamalı. IQ testi değildir.", "Oyun"),
]


def dizin_html():
    kart = "".join(
        '<li><a href="%s"><span class="ts-arac-rozet">%s</span><strong>%s</strong><em>%s</em></a></li>'
        % (s, _e(rozet), _e(ad), _e(ozet)) for s, ad, ozet, rozet in ARACLAR)
    govde = ('<ul class="ts-arac-izgara">%s</ul>' % kart) + """
<section class="ts-giris">
  <h2>Bu araçlar nasıl çalışıyor?</h2>
  <p>Hepsi tarayıcınızın içinde çalışır. Girdiğiniz doğum tarihi, boy, kilo ya da cevaplar
  hiçbir sunucuya gönderilmez, kaydedilmez; sayfayı kapattığınızda hiçbir iz kalmaz.</p>
  <p>Her aracın yanında yöntemin anlatımı var: hangi formül kullanıldığı, hangi durumda
  yanıltabileceği ve neyi ölçmediği yazılı. Sonucu güzelleştirmiyoruz.</p>
  <h2>Neden bazı araçları yapmıyoruz?</h2>
  <p>Emeklilik, kıdem tazminatı ve bedelli askerlik hesaplayıcıları bilerek listede yok. Bu
  hesaplar mevzuata bağlı, sık değişiyor ve yanlış sonuç kullanıcının işten ayrılma gibi geri
  dönülmez bir kararını etkileyebiliyor. Böyle konularda doğru adres kurumun kendi resmî
  aracıdır.</p>
  <p>Kredi taksit hesabı da aynı nedenle beklemede: vergiler ve masraflar hariç tutulduğunda
  çıkan rakam gerçek ödemeden düşük görünüyor, bu da yanıltıcı oluyor.</p>
  <h2>Sırada ne var?</h2>
  <p>Bölüm büyüdükçe doğum haritası çıkarma, gün farkı hesaplama ve kelime oyunu eklenecek.
  Ölçüt aynı kalacak: sonucu doğru veren, yöntemini açıklayan ve veriyi toplamayan araçlar.</p>
  <h2>Araçlar neden reklamsız çalışıyor?</h2>
  <p>Hesaplama sayfalarında en çok şikâyet edilen şey, sonucun reklam arasında kaybolmasıdır.
  Burada araç sayfanın en üstünde durur, sonuç doğrudan altında çıkar. Açıklama metni sonucun
  altındadır; okumak isteyen okur, istemeyen sonucu alıp gider.</p>
  <h2>Mobilde de aynı şekilde çalışır</h2>
  <p>Araçların tamamı telefonda tek sütuna iner, klavye tipi alana göre açılır: tarih alanında
  takvim, sayı alanında sayı tuşları gelir. Hesap için internet bağlantısı gerekmez; sayfa bir
  kez açıldıktan sonra çevrimdışı da çalışır.</p>
</section>
"""
    return _sayfa("araclar", "Araçlar — hesaplama ve oyunlar | TrendSaphiens",
                  "Yükselen burç, burç uyumu, yaş, vücut kitle indeksi ve yüzde hesaplama ile örüntü oyunu. Hepsi tarayıcıda çalışır.",
                  "Araçlar", "Hesaplayan, deneyen, sonucu anında veren sayfalar — hepsi tarayıcınızda.",
                  govde)


def yayinla(kok=None):
    kok = kok or SITE_KOK
    d = os.path.join(kok, "trend")
    os.makedirs(d, exist_ok=True)
    uretilen = [
        ("yukselen-burc-hesaplama", yukselen_html()),
        ("burc-uyumu", uyumu_html()),
        ("yas-hesaplama", yas_html()),
        ("vucut-kitle-indeksi", vki_html()),
        ("yuzde-hesaplama", yuzde_html()),
        ("oruntu-oyunu", oyun_html()),
        ("araclar", dizin_html()),
    ]
    for slug, html in uretilen:
        io.open(os.path.join(d, slug + ".html"), "w", encoding="utf-8").write(html)
    # sitemap
    y = os.path.join(kok, "sitemap.xml")
    try:
        s = io.open(y, encoding="utf-8").read()
        ek = []
        import datetime
        bugun = datetime.date.today().isoformat()
        for slug, _h in uretilen:
            adres = KOK_URL + slug
            if adres not in s:
                ek.append('  <url><loc>%s</loc><lastmod>%s</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>'
                          % (adres, bugun))
        if ek:
            s = s.replace("</urlset>", "\n".join(ek) + "\n</urlset>")
            io.open(y, "w", encoding="utf-8").write(s)
    except Exception as ex:
        print("sitemap:", ex)
    return {"arac": len(uretilen), "adresler": [s for s, _h in uretilen]}


if __name__ == "__main__":
    print(json.dumps(yayinla(), ensure_ascii=False, indent=1))
