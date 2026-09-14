# -*- coding: utf-8 -*-
"""
MATRIX BÜLTENİ — KDA Matrix'in halka açık, abonelikli yayını.

Ne: Sistemin haftalık karnesi ve sistemi anlatan içerik. Kaynak, sistemin
KENDİ çıktısı (matrix panelinin yazdığı JSON). Rakam yalnızca sistem
yazdıysa yazılır.

Ne DEĞİL: yatırım tavsiyesi, al-sat sinyali, fiyat hedefi. matrix.html'deki
risk bildirimi burada da geçerli ve her sayfada görünür.

Sayfalar:
  /bulten/            → bülteni anlatan sayfa + abonelik formu (SEO girişi)
  /bulten/YYYY-WW     → haftalık sayı (veri/bulten/YYYY-WW.json'dan)
  /bulten/00-sistem   → 0. sayı: sistem nasıl çalışıyor (verisiz, kalıcı)
"""
import datetime, html, json, os, sys

from .ayarlar import SITE_KOK, KOK_DIZIN


def _e(x):
    return html.escape(x or "", quote=True)


def _kabuk():
    sys.path.insert(0, os.path.join(KOK_DIZIN, "site-uretici"))
    import kabuk
    return kabuk


RISK = """<div class="bl-risk">
  <span class="etk">Risk bildirimi</span>
  <p>Matrix Bülteni bir <strong>bilgi ürünüdür</strong>. Burada paylaşılan hiçbir içerik yatırım
    danışmanlığı, yatırım tavsiyesi ya da alım-satım önerisi değildir. Kripto varlık ve hisse
    piyasaları yüksek risk taşır; yatırdığınız tutarın tamamını kaybedebilirsiniz. Geçmiş
    performans gelecek için gösterge değildir, hiçbir kazanç vaat edilmez. Bültende geçen her
    sayı sistemin kendi ölçümüdür; kazanan ve kaybeden bütün sonuçlar dahildir.</p>
</div>"""

FORM = """<div class="bl-abone" id="abone">
  <span class="etk">Abone ol — ücretsiz</span>
  <h2>Haftalık karne e-postana <i>gelsin</i>.</h2>
  <p>Her hafta bir e-posta: sistem neye baktı, hangi hatlar sınavı geçti, hangileri elendi.
    Reklam yok, spam yok; tek tıkla çıkabilirsin.</p>
  <form id="bl-form" autocomplete="off">
    <div class="bl-satir">
      <input type="email" id="bl-eposta" placeholder="e-posta adresin" required maxlength="120">
      <button type="submit">Abone ol</button>
    </div>
    <label class="bl-onay"><input type="checkbox" id="bl-onay" required>
      İçeriğin yatırım tavsiyesi olmadığını anladım; 18 yaşından büyüğüm; e-posta adresimin
      yalnızca bu bülten için saklanmasını kabul ediyorum. <a href="../kosullar">Koşullar</a></label>
    <p id="bl-sonuc" class="bl-sonuc" aria-live="polite"></p>
  </form>
</div>
<script>
(function(){
  var f=document.getElementById("bl-form"); if(!f) return;
  f.addEventListener("submit",async function(ev){
    ev.preventDefault();
    var s=document.getElementById("bl-sonuc"), e=document.getElementById("bl-eposta").value.trim(),
        o=document.getElementById("bl-onay").checked;
    s.textContent="Kaydediliyor…";
    try{
      var r=await fetch("/api/abone",{method:"POST",headers:{"Content-Type":"application/json"},
        body:JSON.stringify({eposta:e,onay:o,kaynak:location.pathname})});
      var d=await r.json();
      s.textContent=d.mesaj||d.hata||"Bir şey ters gitti.";
      if(d.ok){ f.reset(); try{ if(window.gtag) gtag("event","bulten_abone"); }catch(x){} }
    }catch(x){ s.textContent="Bağlantı kurulamadı; biraz sonra tekrar dene."; }
  });
})();
</script>"""


def _sema(baslik, aciklama, url, tur="WebPage"):
    return '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@graph": [
            {"@type": tur, "name": baslik, "headline": baslik, "description": aciklama, "url": url,
             "inLanguage": "tr", "isPartOf": {"@type": "WebSite", "name": "Luna Yapım", "url": "https://lunayapim.com/"},
             "publisher": {"@type": "Organization", "name": "Luna Yapım"}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": "https://lunayapim.com/"},
                {"@type": "ListItem", "position": 2, "name": "Matrix Bülteni", "item": "https://lunayapim.com/bulten/"}]}
        ]}, ensure_ascii=False) + '</script>'


def _bas(K, baslik, aciklama, url, tur="WebPage"):
    b = K.head(_e(baslik), _e(aciklama), _e("matrix bülteni, kda matrix, otonom piyasa araştırma, kripto analiz sistemi, haftalık piyasa karnesi"), url, _sema(baslik, aciklama, url, tur))
    b = b.replace('<a href="./" style="opacity:1;color:var(--kirmizi)">İller</a>', '<a href="../sehir/">İller</a>')
    return b.replace('<a href="../bulten/">Bülten</a>', '<a href="./" style="opacity:1;color:var(--kirmizi)">Bülten</a>')


def giris_html():
    K = _kabuk()
    baslik = "Matrix Bülteni — piyasayı okuyan sistemin karnesi | Luna Yapım"
    aciklama = ("KDA Matrix her gün binlerce fiyat hareketini tarar ve hatlarını puanlar. Haftalık karne: "
                "sınavı geçen hatlar, sistemin baktığı yerler. Yatırım tavsiyesi değildir.")
    url = "https://lunayapim.com/bulten/"
    # yayınlanmış sayılar (kapak ve arşiv için)
    vd = os.path.join(KOK_DIZIN, "veri", "bulten")
    haftalar = sorted(f[:-5] for f in os.listdir(vd) if f.endswith(".json")) if os.path.isdir(vd) else []
    son = haftalar[-1] if haftalar else None
    kapak_sayi = son or "00"
    kapak_baslik = "Haftanın karnesi" if son else "Sistem nasıl çalışıyor"
    kapak_yol = son or "00-sistem"
    arsiv = "".join('<a class="bl-sayi" href="%s"><span class="etk">Sayı %s</span><b>Haftanın karnesi</b><span>Sınavı geçenler, elenenler, dikkat haritası</span></a>' % (_e(h), _e(h)) for h in reversed(haftalar))
    arsiv = '<a class="bl-sayi" href="00-sistem"><span class="etk">Sayı 00</span><b>Sistem nasıl çalışıyor</b><span>Hatlar, kuluçka, 40 sinyal kuralı, karne</span></a>' + arsiv
    govde = """
<div class="dg-mast">
  <div class="wrap">
    <div class="crumbs"><a href="../">Ana Sayfa</a> · Matrix Bülteni</div>
    <div class="dg-mast-satir">
      <span class="dg-marka">Matrix Bülteni<small>Luna Yapım · piyasayı okuyan sistemin karnesi</small></span>
      <div class="dg-tarih"><b>Haftalık</b><span>Pazartesi sabahı · ücretsiz · reklamsız</span></div>
      <nav class="dg-sek"><a href="00-sistem">Sistem</a><a href="../matrix">Kanıt defteri</a><a href="../yazilim">Yazılım</a><a href="#abone">Abone ol</a></nav>
    </div>
  </div>
</div>

<section class="bl-kapak wrap">
  <div class="bl-kapak-kart gor">
    <div class="ust"><span>Matrix Bülteni</span><span>Kripto · Hisse</span></div>
    <div><div class="sayi">Sayı <i>%s</i></div><h3 style="margin-top:18px">%s</h3></div>
    <img class="karga" src="../assets/karga.png" alt="">
    <div class="alt"><span>Ölçüm, yorum değil</span><a href="%s" style="color:var(--kirmizi);text-decoration:none">Oku →</a></div>
  </div>
  <div class="bl-kapak-metin">
    <p class="etk" style="color:var(--kirmizi);margin-bottom:14px">Otonom araştırma · haftalık karne</p>
    <h1 class="gor">Piyasayı okuyan bir sistemin <i style="font-style:normal;color:var(--kirmizi)">karnesi</i>.</h1>
    <p class="lede gor" data-gecik="1">İnsan yorumu değil, ölçüm. KDA Matrix her gün binlerce fiyat hareketini tarıyor, kendi okuma hatlarını puanlıyor ve sonucu — kazanan, kaybeden, hepsi — olduğu gibi yazıyor. Bülten, o defterin haftalık özeti.</p>
    <div class="btnlar gor" data-gecik="2">
      <a class="btn btn-dolu" href="#abone">Ücretsiz abone ol</a>
      <a class="btn btn-cizgi" href="00-sistem">Sistem nasıl çalışıyor</a>
    </div>
  </div>
</section>

<section class="acik">
  <div class="wrap">
    <div class="bas"><span class="no">01</span><div><h2>Her hafta ne geliyor</h2>
      <p class="aciklama">Tek e-posta, dört bölüm. Hepsi sistemin kendi çıktısından.</p></div></div>
    <div class="uc">
      <div class="hiz"><h3>Haftanın karnesi</h3><p>Yayındaki okuma hatlarının 7 günlük isabet ölçümü.
        Ham sayı: kazanan ve kaybeden bütün sinyaller dahil, seçme yok.</p></div>
      <div class="hiz"><h3>Sınavı geçenler ve elenenler</h3><p>Kuluçkadaki her hat 40 sonuçlanmış sinyal
        tamamlamadan yayına çıkmıyor. Bu hafta kim terfi etti, kim düştü.</p></div>
      <div class="hiz"><h3>Sistem neye baktı</h3><p>Haftanın en çok taranan bölgeleri ve sistemin
        dikkatinin nereye kaydığı. Yorum değil, dikkat haritası.</p></div>
      <div class="hiz"><h3>Mutfaktan</h3><p>Sistemi nasıl kurduğumuz, hangi hatayı bulup düzelttiğimiz.
        Yazılımın kendisini merak edenler için.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">%s</div>
</section>

<section class="acik">
  <div class="wrap">
    <div class="bas"><span class="no">02</span><div><h2>Sayılar</h2>
      <p class="aciklama">Yayınlanan her sayı burada kalır; e-postayı kaçıran siteden okur.</p></div></div>
    <div class="bl-sayilar">%s</div>
  </div>
</section>

<section>
  <div class="wrap prose">
    <h2>Bu bülten kimin için</h2>
    <p>Piyasayı takip eden ama "uzman yorumu" formatından yorulmuş herkes için. Sistem ne dediyse
      o yazılıyor; beğenmediğimiz sonucu saklamıyoruz, çünkü saklarsak karne anlamını yitirir.
      Yazılımla ilgilenenler için ayrıca bir katman var: bu sistemi iki kişilik bir ekip, kendi
      araçlarıyla kurdu ve her hafta bir parçasını anlatıyor.</p>
    <h2>Bu bülten ne değil</h2>
    <p>Al-sat önerisi değil. Fiyat hedefi vermiyor. "Şu coin patlayacak" demiyor. Hangi hattın
      hangi sinyali verdiğini sonuçlandıktan sonra yazıyor; açık pozisyon paylaşmıyor.
      Kısacası: bir araştırma sisteminin şeffaf günlüğü.</p>
    <h2>Sistemi merak edenler için</h2>
    <p>KDA Matrix, Luna Yapım'ın otonom piyasa araştırma ürünü. Aynı mühendisliği müşterilerimiz
      için de kuruyoruz: piyasayı tarayan sistemler, içerik üretim hatları, e-ticaret otomasyonu.
      <a href="../yazilim">Yazılım tarafımıza</a> ve <a href="../matrix">Matrix'in canlı kanıt
      defterine</a> bakabilirsiniz.</p>
  </div>
</section>

<section class="acik">
  <div class="wrap">%s</div>
</section>
""" % (_e(kapak_sayi), _e(kapak_baslik), _e(kapak_yol), FORM, arsiv, RISK)
    return _bas(K, baslik, aciklama, url) + govde + K.FOOTER.replace("</body>", '<script src="../assets/sahne.js?v=1" defer></script>\n</body>', 1)


def sistem_html():
    """0. sayı — sistemin kendisi. Veri gerektirmez, kalıcı."""
    K = _kabuk()
    baslik = "Sayı 0 — KDA Matrix nasıl çalışıyor | Matrix Bülteni"
    aciklama = ("Otonom piyasa araştırma sisteminin mantığı: okuma hatları, kuluçka sınavı, 40 sinyal eşiği, "
                "ham isabet ölçümü ve neden hiçbir sonucu saklamadığımız.")
    url = "https://lunayapim.com/bulten/00-sistem"
    govde = """
<div class="page-hero">
  <img class="karga-buyuk" src="../assets/karga.png" alt="">
  <div class="wrap">
    <div class="crumbs"><a href="../">Ana Sayfa</a> · <a href="./">Matrix Bülteni</a> · Sayı 0</div>
    <p class="etk" style="color:var(--kirmizi);margin-bottom:18px">Sayı 0 · Sistem</p>
    <h1>KDA Matrix <i>nasıl</i> çalışıyor</h1>
    <p class="lede">Bülteni okumadan önce sistemi anlamak gerekiyor. Bu sayı veri içermiyor; yalnızca
      mantığı anlatıyor. Bir kez okunur, sonra karneler anlamlanır.</p>
  </div>
</div>

<section>
  <div class="wrap prose">
    <h2>Tek göz yerine ordu</h2>
    <p>Sistem piyasaya tek bir yöntemle bakmıyor. Her biri ayrı bir okuma yöntemi olan çok sayıda
      "hat" var; her hat aynı fiyat hareketini kendi kuralıyla yorumluyor. Hatların adları gerçek,
      tarifleri mahrem — sistemin gücü tek bir sihirli formülde değil, birbirinden bağımsız çok
      sayıda gözün aynı anda bakmasında.</p>

    <h2>Kuluçka ve 40 sinyal sınavı</h2>
    <p>Yeni geliştirilen bir hat doğrudan yayına çıkmıyor. Önce kuluçkaya giriyor ve
      <strong>40 sonuçlanmış sinyal</strong> tamamlayana kadar performansı yayınlanmıyor; yalnızca
      ilerlemesi görünüyor. Eşiği geçtiğinde ölçülen sonucu artıdaysa yayına terfi ediyor, değilse
      eleniyor. Yani bültende gördüğünüz her hat bu sınavdan geçmiş demek.</p>

    <h2>Ham isabet: seçme yok</h2>
    <p>İsabet oranı kazanan ve kaybeden bütün sinyaller dahil hesaplanıyor. Kötü haftayı
      saklamıyoruz, iyi haftayı büyütmüyoruz. Bunun tek sebebi dürüstlük değil; seçilmiş sonuç
      gösteren bir karne, sistemin gerçekten çalışıp çalışmadığını bize de söylemez.</p>

    <h2>Neden halka açık</h2>
    <p>Bir araştırma sisteminin en zor kısmı kendi kendini kandırmamak. Sonuçları olduğu gibi
      dışarıya yazmak bizi disipline ediyor. Bülten bu defterin haftalık özeti; canlı hâli
      <a href="../matrix">Matrix'in kanıt defterinde</a>.</p>

    <h2>Bülten neyi asla yapmaz</h2>
    <p>Açık pozisyon paylaşmaz, fiyat hedefi vermez, "al" ya da "sat" demez. Sonuçlanmış sinyalleri
      sonuçlandıktan sonra, ölçümüyle birlikte yazar. Bu bir bilgi ürünüdür; aşağıdaki risk
      bildirimi her sayıda tekrar edilir.</p>
  </div>
</section>

<section class="acik"><div class="wrap">%s</div></section>
<section><div class="wrap">%s</div></section>
""" % (FORM, RISK)
    return _bas(K, baslik, aciklama, url, "Article") + govde + K.FOOTER


def sayi_html(hafta, veri):
    """Haftalık sayı — veri: matrix panelinin yazdığı JSON.
    Beklenen alanlar (hepsi isteğe bağlı; olmayan yazılmaz):
      taranan, isabet, aktif_hat, terfi:[{ad,isabet,sinyal}], elenen:[{ad}],
      bolgeler:[{ad,pay}], mutfak:"metin", not:"metin"                        """
    K = _kabuk()
    baslik = "Sayı %s — haftanın karnesi | Matrix Bülteni" % hafta
    aciklama = "KDA Matrix'in %s haftası: sistemin ölçülen karnesi, sınavı geçen ve elenen hatlar, dikkat haritası. Yatırım tavsiyesi değildir." % hafta
    url = "https://lunayapim.com/bulten/%s" % hafta
    p = []
    kut = []
    for ad, k in (("Taranan hareket", "taranan"), ("Ham isabet", "isabet"), ("Aktif hat", "aktif_hat")):
        if veri.get(k) is not None:
            kut.append('<div class="mtr-k"><b>%s</b><span class="mtr-e">%s</span></div>' % (_e(str(veri[k])), _e(ad)))
    if kut:
        p.append('<h2>Haftanın karnesi</h2><div class="mtr-sayac">%s</div>' % "".join(kut))
    if veri.get("terfi"):
        p.append("<h2>Sınavı geçenler</h2><ul>%s</ul>" % "".join(
            "<li><strong>%s</strong> — %s sonuçlanmış sinyal, ham isabet %s</li>"
            % (_e(t.get("ad")), _e(str(t.get("sinyal", "—"))), _e(str(t.get("isabet", "—")))) for t in veri["terfi"]))
    if veri.get("elenen"):
        p.append("<h2>Elenenler</h2><p>%s</p>" % _e(", ".join(t.get("ad", "") for t in veri["elenen"])))
    if veri.get("bolgeler"):
        p.append("<h2>Sistem neye baktı</h2><ul>%s</ul>" % "".join(
            "<li>%s — %s</li>" % (_e(b.get("ad")), _e(str(b.get("pay", "")))) for b in veri["bolgeler"]))
    if veri.get("mutfak"):
        p.append("<h2>Mutfaktan</h2><p>%s</p>" % _e(veri["mutfak"]))
    if veri.get("not"):
        p.append("<p class=\"ilk-not\">%s</p>" % _e(veri["not"]))
    govde = """
<div class="page-hero">
  <img class="karga-buyuk" src="../assets/karga.png" alt="">
  <div class="wrap">
    <div class="crumbs"><a href="../">Ana Sayfa</a> · <a href="./">Matrix Bülteni</a> · Sayı %s</div>
    <p class="etk" style="color:var(--kirmizi);margin-bottom:18px">Sayı %s</p>
    <h1>Haftanın <i>karnesi</i></h1>
    <p class="lede">Sistemin kendi ölçümü; kazanan ve kaybeden bütün sonuçlar dahil.</p>
  </div>
</div>
<section><div class="wrap prose">%s</div></section>
<section class="acik"><div class="wrap">%s</div></section>
<section><div class="wrap">%s</div></section>
""" % (_e(hafta), _e(hafta), "\n    ".join(p), FORM, RISK)
    return _bas(K, baslik, aciklama, url, "Article") + govde + K.FOOTER


def yayinla(kok=None):
    kok = kok or SITE_KOK
    d = os.path.join(kok, "bulten"); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(giris_html())
    open(os.path.join(d, "00-sistem.html"), "w", encoding="utf-8").write(sistem_html())
    vd = os.path.join(KOK_DIZIN, "veri", "bulten")
    n = 0
    if os.path.isdir(vd):
        for f in sorted(os.listdir(vd)):
            if f.endswith(".json"):
                hafta = f[:-5]
                veri = json.load(open(os.path.join(vd, f), encoding="utf-8"))
                open(os.path.join(d, hafta + ".html"), "w", encoding="utf-8").write(sayi_html(hafta, veri)); n += 1
    # site haritası
    y = os.path.join(kok, "sitemap.xml")
    if os.path.exists(y):
        s = open(y, encoding="utf-8").read()
        for a in ("https://lunayapim.com/bulten/", "https://lunayapim.com/bulten/00-sistem"):
            if a not in s:
                s = s.replace("</urlset>", "  <url><loc>%s</loc><changefreq>weekly</changefreq><priority>0.7</priority></url>\n</urlset>" % a)
        open(y, "w", encoding="utf-8").write(s)
    try:
        sys.path.insert(0, os.path.join(KOK_DIZIN, "site-uretici"))
        import sonislem; sonislem.calistir(kok, desen="bulten/*.html")
    except Exception:
        pass
    return {"giris": True, "sistem": True, "haftalik_sayi": n}


if __name__ == "__main__":
    print(yayinla())
