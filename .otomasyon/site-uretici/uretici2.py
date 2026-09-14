# -*- coding: utf-8 -*-
"""Ek hizmet sayfaları (klip, drone, düğün, işletme) + zengin genel il sayfası."""
import os, json
from sehirler import SEHIRLER, SEHIR_INDEKS
from kabuk import head, FOOTER
from cesit import varyant, giris_cumlesi
from sektor_anlatim import icerik_fikirleri
import yerel_analiz as YA
from uretici import (yerel_plan, KOK, e, j, liste, ilce_metni, ekip_cumlesi, sema_bloklari,
                     kisa_baslik, meta_desc, ilk_ilceler,
                     ilgili_blok, sayfa_var, HIZMET_ADLARI, SUREC, cta,
                     video_bolumu, sss_blok)


def _kabuk(c, slug, baslik_seo, aciklama, anahtar, semalar, h1, lede, govde,
           video_etiketi, video_baslik, sss, aktif, cta_baslik, cta_alt, crumb):
    url = "%s/sehir/%s.html" % (KOK, slug)
    g = head(e(baslik_seo), e(aciklama), e(anahtar), url, semalar)
    g += """<div class="page-hero">
  <img class="karga-buyuk" src="../assets/karga.png" alt="">
  <div class="wrap">
    <div class="crumbs"><a href="../">Ana Sayfa</a> · <a href="./">İller</a> · <a href="{slug0}">{ad}</a> · {crumb}</div>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
    <div class="btnlar">
      <a class="btn btn-dolu" href="https://wa.me/905411602603">{ad} için teklif al</a>
      <a class="btn btn-cizgi" href="#surec">Nasıl çalışıyor?</a>
    </div>
  </div>
</div>

{govde}
""".format(slug0=c["slug"], ad=e(c["ad"]), crumb=crumb, h1=h1, lede=lede, govde=govde)
    g += video_bolumu(video_etiketi, video_baslik)
    g += """<section>
  <div class="wrap prose">
    <h2>{ad} — sık sorulan sorular</h2>
    {sss}

    <h2>{ad}{ek} diğer hizmetlerimiz</h2>
    {ilgili}

    <p style="margin-top:30px"><a href="https://wa.me/905411602603" class="btn btn-dolu">{ad} için teklif al</a></p>
  </div>
</section>

""".format(ad=e(c["ad"]), ek=c["ek"], sss=sss_blok(sss), ilgili=ilgili_blok(c, aktif))
    g += cta(c, cta_baslik, cta_alt)
    g += FOOTER
    return slug + ".html", g


# ============================================================ KLİP
def sayfa_klip(c):
    ad, ek = c["ad"], c["ek"]
    slug = "%s-klip-cekimi" % c["slug"]
    baslik = kisa_baslik("%s Klip Çekimi ve Müzik Videosu | Luna Yapım" % ad)
    aciklama = meta_desc(
        "%s%s klip çekimi: müzik klibi, marka klibi ve sanatçı tanıtım videosu. Senaryo, sinematografi ve FPV drone tek elden." % (ad, ek),
        "%s ve tüm ilçeler." % ilk_ilceler(c))
    anahtar = ("%s klip çekimi, %s müzik klibi, %s marka klibi, %s video klip fiyatları, %s klip prodüksiyon, "
        "%s sanatçı tanıtım videosu, %s lyric video, %s sinematik klip" % tuple([ad.lower()]*8))
    sss = [
     ("%s%s klip çekimi için mekân bulma işini siz mi yapıyorsunuz?" % (ad, ek),
      "Evet. %s Mekân izinleri, oyuncu ve figüran koordinasyonu, ekipman planlaması bize ait." % (
          "%s%s sık kullandığımız mekânlar: %s." % (ad, ek, c.get("mekan","şehir merkezi ve çevresi")))),
     ("%s%s çekime kendi ekibinizle mi geliyorsunuz?" % (ad, ek), ekip_cumlesi(c)),
     ("Şarkı henüz yayınlanmadı, klibi önceden çekebilir miyiz?",
      "Evet, en doğrusu da budur. Mikslenmiş bir demo yeterli. Klip ve şarkı aynı gün yayına girecek şekilde planlıyor, teaser ve dikey kesimleri lansman öncesi teslim ediyoruz."),
     ("Bütçemiz kısıtlı, yine de iyi bir klip çıkar mı?",
      "Tek mekân paketiyle başlıyoruz. %s Doğru mekân seçildiğinde küçük bütçeyle büyük görünen iş çıkıyor." % c["cografya"]),
     ("Dikey ve teaser sürüm veriyor musunuz?",
      "Evet. YouTube için yatay tam sürüm, Reels ve TikTok için dikey kesimler, 15–30 saniyelik teaser'lar ve istenirse lyric sürüm teslim ediliyor."),
    ]
    hizmet = {"sema_tur":"Klip Çekimi ve Müzik Videosu Prodüksiyonu","kategori":["Müzik","Prodüksiyon","Reklam"],
              "kitle":"%s'daki müzisyenler, sanatçılar, menajerlik firmaları ve markalar" % ad}
    semalar = sema_bloklari(c, hizmet, "%s Klip Çekimi" % ad, aciklama, "%s/sehir/%s.html" % (KOK, slug), sss)

    govde = """<section>
  <div class="wrap prose">
    {yerel_analiz}

    <p>{kultur}</p>
    <p>İyi bir klip şarkıyı tekrar etmez, ona bir dünya kurar. Luna Yapım'ın kısa film ve sinematografi geçmişi klip tarafında doğrudan işe yarıyor: hikâye kuran, oyuncu yöneten ve ışığı bilen aynı ekip FPV drone'u da uçuruyor. {ekip}</p>

    <div class="rozetler">
      <span class="rozet">Müzik Klibi</span><span class="rozet">Marka Klibi</span>
      <span class="rozet">Lyric Video</span><span class="rozet">FPV Drone</span>
      <span class="rozet">Sinematik Renk</span><span class="rozet">Dikey Kesimler</span>
    </div>

    <h2>{ad}{ek} klip çekiminde ne yapıyoruz</h2>
    <ul>
      <li><strong>Müzik klibi</strong> — performans, hikâye ya da ikisinin karışımı</li>
      <li><strong>Marka klibi</strong> — ürünü değil markanın duygusunu anlatan müzik odaklı iş</li>
      <li><strong>Sanatçı tanıtım videosu</strong> — menajerlik ve plak şirketi sunumları için</li>
      <li><strong>Lyric ve teaser sürümleri</strong> — lansman haftasının içerik takvimi</li>
    </ul>

    <h2 id="surec">Süreç</h2>
  </div>
  <div class="wrap">
    {surec}
  </div>
  <div class="wrap prose">
    <div class="kutu"><span class="etk">Lansman aklı</span>
      <p>Çekim gününde ana klip için gereken karelerin dışında ekstra malzeme de topluyoruz: kamera arkası,
         dikey performans planları, fotoğraf. Klip yayınlandıktan sonraki üç hafta boyunca paylaşılacak içerik hazır oluyor.</p></div>
  </div>
</section>

""".format(yerel_analiz=YA.blok(c, "klip"), kultur=e(c.get("kultur", "%s%s yerel müzik sahnesi klip üretimi için canlı bir zemin sunuyor." % (ad, ek))),
           ekip=e(ekip_cumlesi(c)), ad=e(ad), ek=ek,
           surec=SUREC % ("Şarkıyı dinleriz","Demo bile olsa parçayı dinleyip referansları konuşuyoruz.",
                          "Konsept","Sahne sahne plan, mekân önerisi, kostüm ve sanat yönetimi.",
                          "Çekim günü","Sinema kamerası, ışık ekibi ve FPV drone birlikte sahada.",
                          "Lansman paketi","Yatay sürüm, dikey kesimler, teaser, kapak ve kamera arkası."))

    return _kabuk(c, slug, baslik, aciklama, anahtar, semalar,
        "{ad}{ek} <i>klip</i> çekimi".format(ad=e(ad), ek=ek),
        "Müzik klibi, marka klibi ve sanatçı tanıtım videosu — senaryodan renk düzenlemeye kadar tek elden.",
        govde, "klip", "Klip işlerimizden", sss, "klip-cekimi",
        "Şarkını <i>gönder</i>, konseptini konuşalım.",
        "Parçayı dinleyip {ad}{ek} nasıl bir klip çıkabileceğini aynı gün söyleyelim.".format(ad=e(ad), ek=ek),
        "Klip Çekimi")


# ============================================================ DRONE
SEKTOR_KULLANIM = {
    "gıda": "üretim tesisinin ölçeğini ve lojistik bağlantısını havadan göstermek",
    "tarım": "arazi sınırlarını, sulama hattını ve ürün desenini tek karede vermek",
    "tekstil": "fabrika kampüsünü ve sevkiyat alanını yabancı alıcıya anlatmak",
    "makine": "tesis yerleşimini ve üretim akışının fiziksel düzenini göstermek",
    "mobilya": "üretim tesisi ve showroom ilişkisini tek planda kurmak",
    "enerji": "santral, hat ve saha yatırımının ölçeğini belgelemek",
    "lojistik": "depo, liman ve yol bağlantısını konumuyla birlikte göstermek",
    "turizm": "tesisin sahille, manzarayla ve çevresiyle ilişkisini kurmak",
    "otel": "tesisin konumunu ve çevresini rezervasyon sitesine uygun çekmek",
    "maden": "saha genişliğini ve ulaşım hattını belgelemek",
    "mermer": "ocak sahasını ve nakliye hattını göstermek",
    "seracılık": "sera alanının ölçeğini ve düzenini havadan vermek",
    "hayvancılık": "işletme alanının düzenini ve kapasitesini göstermek",
    "inşaat": "şantiye ilerlemesini aylık seri ile belgelemek",
    "plastik": "üretim tesisinin ölçeğini ve yerleşimini göstermek",
    "kimya": "tesis yerleşimini ve güvenlik mesafelerini belgelemek",
    "demir": "tesis ve stok sahasının ölçeğini göstermek",
    "cam": "üretim kampüsünü ve sevkiyat düzenini anlatmak",
    "deri": "üretim tesisini ve organize sanayi konumunu göstermek",
    "ayakkabı": "üretim tesisini ve showroom bağlantısını göstermek",
    "kağıt": "tesis ölçeğini ve lojistik bağlantısını göstermek",
    "balıkçılık": "kıyı tesisini ve üretim sahasını havadan vermek",
    "çay": "üretim sahasını ve fabrika bağlantısını göstermek",
    "fındık": "bahçe alanını ve işleme tesisini birlikte göstermek",
    "zeytin": "bahçe ve işletme ilişkisini tek planda kurmak",
    "üzüm": "bağ alanını ve tesis bağlantısını göstermek",
    "petrol": "saha yatırımını ve hat bağlantısını belgelemek",
    "savunma": "tesis kampüsünü ve yerleşimini belgelemek",
    "otomotiv": "üretim kampüsünü ve yan sanayi bağlantısını göstermek",
}


def kullanim_listesi(c, e, ad, ek):
    """İlin KENDİ sektörlerinden, o ile özgü kullanım listesi kurar.

    Eskiden bu liste 81 ilde birebir aynıydı; artık ilin sektör verisinden
    türüyor. Sektör eşleşmezse o satır yazılmıyor — uydurma yok."""
    ci = []
    for sek in (c.get("sektorler") or [])[:5]:
        alt = sek.lower()
        for anahtar, is_ in SEKTOR_KULLANIM.items():
            if anahtar in alt:
                ci.append("<li><strong>%s</strong> — %s</li>" % (e(sek), e(is_)))
                break
    ilce = (c.get("ilceler") or [])[:2]
    if ilce:
        ci.append("<li><strong>Şantiye ilerleme takibi</strong> — %s hattındaki "
                  "projelerde aylık seri ve teslim filmi</li>"
                  % e(" ve ".join(ilce)))
    ci.append("<li><strong>Arsa ve arazi ilanı</strong> — sınır, yol bağlantısı ve "
              "topografyanın tek karede gösterimi</li>")
    ci.append('<li><strong>Emlak projeleri</strong> — <a href="%s-emlak-video">'
              '%s%s emlak video çekimi</a> ile birlikte</li>' % (c["slug"], e(ad), ek))
    return "".join(ci)


def yerel_talep(c, e, ad, ek, tur):
    """İlin kendi verisinden, o hizmete BAĞLI yerel talep bölümü.

    Uydurma yok: yalnızca sehirler.py'de o il için yazılmış alanlar kullanılıyor.
    Alan yoksa o satır hiç basılmıyor."""
    satir = []
    # ÖNEMLİ: her hizmet sayfası ilin FARKLI bir alanını kullanır.
    # Aynı ilin dört sayfası aynı paragrafı basarsa Google onları birbirinin
    # kopyası sayıp eliyor ("Alternate page with proper canonical tag").
    # Bu yüzden alan paylaşımı sabit:
    #   drone → sanayi   | emlak-video → emlak | insaat-3d → insaat
    #   klip  → kultur   | dugun → dugun_notu  | isletme → isletme_notu
    if tur == "drone":
        if c.get("sanayi"):
            satir.append(("Tesis ve sanayi", c["sanayi"]))
    if not satir:
        return ""
    p = ["<h2>%s%s havadan çekim talebini ne besliyor</h2>" % (e(ad), ek)]
    for bas, metin in satir:
        p.append("<p><strong>%s:</strong> %s</p>" % (e(bas), e(metin)))
    return "\n    ".join(p)


def sayfa_drone(c):
    ad, ek = c["ad"], c["ek"]
    slug = "%s-drone-cekimi" % c["slug"]
    baslik = kisa_baslik("%s Drone Çekimi — Havadan Görüntü ve 4K Video | Luna Yapım" % ad)
    aciklama = meta_desc(
        "%s%s drone çekimi: şantiye, arsa, tesis, otel ve etkinlik için havadan 4K görüntü ve FPV tek plan mekân turu." % (ad, ek),
        "%s ve tüm ilçeler." % ilk_ilceler(c))
    anahtar = ("%s drone çekimi, %s havadan çekim, %s fpv çekim, %s şantiye drone, %s emlak drone çekimi, "
        "%s tanıtım videosu, %s hava fotoğrafı, %s drone fiyatları" % tuple([ad.lower()]*8))
    sss = [
     ("%s%s drone uçuşu için izin gerekiyor mu?" % (ad, ek),
      "Yerleşim ve uçuş kısıtı olan bölgelerde gerekli izinleri biz takip ediyoruz. Uçuş planını keşif sırasında belirliyoruz."),
     ("%s%s hangi işler için drone çekimi yapıyorsunuz?" % (ad, ek),
      "Şantiye ilerleme takibi, arsa ve arazi ilanı, fabrika ve tesis tanıtımı, otel ve turizm tesisi, etkinlik ve festival, emlak projeleri."),
     ("Şantiyede aylık çekim ne işe yarıyor?",
      "Her ay aynı açıdan çekilen görüntüler yatırımcıya düzenli ilerleme raporu oluyor; teslimde ise elinizde projenin sıfırdan yükselişini gösteren tek bir zaman atlamalı film kalıyor."),
     ("Kendi drone'umuz var, sadece kurgu yaptırabilir miyiz?",
      "Evet. Çektiğiniz ham görüntüyü alıp kurgu, renk düzenleme ve ses tarafını biz yapıyoruz. Çoğu işte fark tam olarak burada oluşuyor."),
     ("%s%s çekim koşulları nasıl?" % (ad, ek), c["cografya"]),
    ]
    hizmet = {"sema_tur":"Drone ve FPV Video Çekimi","kategori":["Prodüksiyon","İnşaat","Gayrimenkul","Turizm"],
              "kitle":"%s'daki inşaat firmaları, emlak ofisleri, oteller, sanayi tesisleri ve etkinlik organizatörleri" % ad}
    semalar = sema_bloklari(c, hizmet, "%s Drone Çekimi" % ad, aciklama, "%s/sehir/%s.html" % (KOK, slug), sss)

    govde = """<section>
  <div class="wrap prose">
    {yerel_analiz}
    <p>Havadan tek plan bir açılış, bir mekânın konumunu, ölçeğini ve çevresini anlatmanın en hızlı yolu. FPV ile ise kapıdan girip odaları gezen, sonra bahçeye çıkıp yukarı yükselen kesintisiz planlar çekiyoruz — az sayıda ekibin yapabildiği bir iş. {ekip}</p>

    <div class="rozetler">
      <span class="rozet">Havadan 4K</span><span class="rozet">FPV Tek Plan</span>
      <span class="rozet">Şantiye İlerleme</span><span class="rozet">Zaman Atlamalı</span>
      <span class="rozet">Hava Fotoğrafı</span><span class="rozet">Gece Çekimi</span>
    </div>

    {yerel_talep}
    <h2>{ad}{ek} en çok hangi işlerde kullanılıyor</h2>
    <ul>{kullanim}</ul>

    <h2 id="surec">Süreç</h2>
  </div>
  <div class="wrap">
    {surec}
  </div>
</section>

""".format(yerel_analiz=YA.blok(c, "drone"), cografya=e(c["cografya"]), ekip=e(ekip_cumlesi(c)), ad=e(ad), ek=ek, slug0=c["slug"],
           yerel_talep=yerel_talep(c, e, ad, ek, "drone"),
           kullanim=kullanim_listesi(c, e, ad, ek),
           surec=SUREC % ("Keşif ve izin","Uçuş kısıtı kontrolü, saha ve ışık saati planı.",
                          "Uçuş","Havadan 4K ve gereken yerde FPV tek plan çekim.",
                          "Kurgu ve renk","Ritim kurgusu, renk düzenleme, müzik ve grafik.",
                          "Teslim","Yatay, dikey ve kare kesimler; yüksek çözünürlüklü hava fotoğrafları."))

    return _kabuk(c, slug, baslik, aciklama, anahtar, semalar,
        "{ad}{ek} <i>drone</i> çekimi".format(ad=e(ad), ek=ek),
        "Şantiye, arsa, tesis, otel ve etkinlik için havadan 4K görüntü ve FPV tek plan mekân turu.",
        govde, "drone", "Drone ve FPV işlerimizden", sss, "drone-cekimi",
        "{ad}{ek} <i>havalanalım</i>.".format(ad=e(ad), ek=ek),
        "Sahayı ve tarihi yaz; uçuş iznini ve planı biz çıkaralım.",
        "Drone Çekimi")


# ============================================================ DÜĞÜN
def sayfa_dugun(c):
    ad, ek = c["ad"], c["ek"]
    slug = "%s-dugun-cekimi" % c["slug"]
    baslik = kisa_baslik("%s Düğün Çekimi ve Sinematik Video | Luna Yapım" % ad)
    aciklama = meta_desc(
        "%s%s düğün çekimi: nişan, kına ve düğün için sinematik kısa film, dış çekim, drone ve aynı gün teaser." % (ad, ek),
        "%s ve tüm ilçeler." % ilk_ilceler(c))
    anahtar = ("%s düğün çekimi, %s düğün videosu, %s nişan çekimi, %s kına çekimi, %s sinematik düğün klibi, "
        "%s düğün drone çekimi, %s dış çekim, %s etkinlik videosu" % tuple([ad.lower()]*8))
    sss = [
     ("%s%s dış çekim için nereleri öneriyorsunuz?" % (ad, ek),
      "%s%s en çok kullandığımız mekânlar: %s. Çekim rotasını gün ışığına göre birlikte planlıyoruz."
      % (ad, ek, c.get("mekan", "şehir merkezi ve çevresindeki doğal alanlar"))),
     ("%s%s düğün geleneği çekimi nasıl etkiliyor?" % (ad, ek),
      c.get("dugun_notu", "Yerel düğün düzenine göre kamera planını ve ekip sayısını ayarlıyoruz.")),
     ("Kaç kişilik ekiple geliyorsunuz?",
      "Standart düğünde iki kamera ve bir drone operatörü; kalabalık ve çok mekânlı düğünlerde üç kamera. %s" % ekip_cumlesi(c)),
     ("Aynı gün teaser veriyor musunuz?",
      "Evet. Düğünün ertesi günü paylaşılabilecek 60–90 saniyelik bir teaser çıkarıyoruz; tam film 3–5 hafta sonra teslim ediliyor."),
     ("Fotoğrafçımız var, sadece video alabilir miyiz?",
      "Tabii. Fotoğraf ekibinizle aynı sette sorunsuz çalışıyoruz; çekim öncesi kısa bir koordinasyon görüşmesi yapıyoruz."),
    ]
    hizmet = {"sema_tur":"Düğün ve Etkinlik Video Çekimi","kategori":["Düğün","Etkinlik","Prodüksiyon"],
              "kitle":"%s'daki çiftler, aileler, organizasyon firmaları ve düğün mekânları" % ad}
    semalar = sema_bloklari(c, hizmet, "%s Düğün Çekimi" % ad, aciklama, "%s/sehir/%s.html" % (KOK, slug), sss)

    govde = """<section>
  <div class="wrap prose">
    {yerel_analiz}

    <p>{dugun}</p>
    <p>Düğün videosu bir gün sonra değil, on yıl sonra izlenmek için çekilir. Biz de o yüzden düğünü olay sırasına göre kaydetmiyor, kısa bir film gibi kurguluyoruz: hazırlık, karşılaşma, tören ve gecenin kendi ritmi. {ekip}</p>

    <div class="rozetler">
      <span class="rozet">Sinematik Kurgu</span><span class="rozet">Çift Kamera</span>
      <span class="rozet">Drone Çekimi</span><span class="rozet">Aynı Gün Teaser</span>
      <span class="rozet">Dış Çekim</span><span class="rozet">Nişan &amp; Kına</span>
    </div>

    <h2>{ad}{ek} neleri çekiyoruz</h2>
    <ul>
      <li><strong>Düğün günü</strong> — hazırlıktan gecenin sonuna kadar tam gün</li>
      <li><strong>Nişan, söz ve kına</strong> — ayrı prodüksiyon ya da paket içinde</li>
      <li><strong>Dış çekim</strong> — şehrin en iyi ışık saatinde, seçilmiş mekânlarda</li>
      <li><strong>Save the date</strong> — düğün öncesi kısa tanıtım filmi</li>
      <li><strong>Kurumsal etkinlik</strong> — açılış, lansman, gala ve kongre</li>
      <li><strong>Mekân tanıtımı</strong> — düğün salonu ve kır düğünü mekânları için</li>
    </ul>

    <h2 id="surec">Süreç</h2>
  </div>
  <div class="wrap">
    {surec}
  </div>
  <div class="wrap prose">
    <div class="kutu"><span class="etk">Mekân ve organizasyon firmalarına</span>
      <p>{ad}{ek} düğün salonu, kır düğünü mekânı ve organizasyon firmalarıyla ortaklık kuruyoruz:
         çiftlere video tarafını biz veriyoruz, aynı çekimden mekânınızın tanıtım filmi de çıkıyor.</p></div>
  </div>
</section>

""".format(yerel_analiz=YA.blok(c, "dugun"), dugun=e(c.get("dugun_notu", "%s%s düğün geleneği ve mekân çeşitliliği çekim planını doğrudan belirliyor." % (ad, ek))),
           ekip=e(ekip_cumlesi(c)), ad=e(ad), ek=ek,
           surec=SUREC % ("Tanışma","Tarihi, mekânı ve beklentiyi konuşuyoruz; takvim ayrılıyor.",
                          "Plan","Gün akışı, dış çekim rotası ve ışık saatleri belirleniyor.",
                          "Çekim günü","İki kamera ve drone; hazırlıktan gecenin sonuna kadar.",
                          "Teslim","Ertesi gün teaser, 3–5 hafta içinde tam film ve ham arşiv."))

    return _kabuk(c, slug, baslik, aciklama, anahtar, semalar,
        "{ad}{ek} <i>düğün</i> çekimi".format(ad=e(ad), ek=ek),
        "Sinematik düğün filmi, nişan ve kına çekimi, dış çekim ve drone — aynı gün teaser ile.",
        govde, "dugun", "Düğün ve etkinlik işlerimizden", sss, "dugun-cekimi",
        "Tarihinizi <i>ayıralım</i>.",
        "Düğün tarihinizi yazın; takvimimizi ve paketleri aynı gün paylaşalım.",
        "Düğün Çekimi")


# ============================================================ İŞLETME
def sayfa_isletme(c):
    ad, ek = c["ad"], c["ek"]
    slug = "%s-isletme-tanitim" % c["slug"]
    baslik = kisa_baslik("%s Tanıtım Filmi ve İşletme Videosu | Luna Yapım" % ad)
    aciklama = meta_desc(
        "%s%s işletme tanıtım videosu: kafe, restoran, mağaza ve salonlar için aylık Reels paketi, ürün çekimi ve Google profili." % (ad, ek),
        "")
    anahtar = ("%s işletme tanıtım videosu, %s sosyal medya ajansı, %s reels çekimi, %s restoran tanıtım videosu, "
        "%s kafe çekimi, %s ürün çekimi, %s içerik üretimi, %s google işletme fotoğrafı" % tuple([ad.lower()]*8))
    sss = [
     ("%s%s hangi işletmelerle çalışıyorsunuz?" % (ad, ek),
      "Kafe ve restoran, mağaza ve butik, güzellik salonu ve kuaför, spor salonu, klinik, oto servis gibi yerel hizmet işletmeleri. %s dahil ilin her ilçesinde çalışıyoruz." % ilce_metni(c)),
     ("%s%s yerel rekabet nasıl?" % (ad, ek),
      c.get("isletme_notu", "Yerel işletme rekabeti giderek görselleşiyor; haritada ve sosyal medyada görünmeyen işletme tercih listesinin dışında kalıyor.")),
     ("Ayda kaç içerik çıkıyor?",
      "Standart pakette tek çekim gününden 8–12 kısa video ve 20–30 fotoğraf çıkarıyoruz; bu dört haftalık paylaşım demek. İçerik takvimini de birlikte teslim ediyoruz."),
     ("Google işletme profilimizi de düzenliyor musunuz?",
      "Fotoğrafları çekip yüklüyoruz, kategori ve bilgi alanlarını düzenliyoruz. Profildeki fotoğraf sayısı ve tazeliği haritada bulunurluğu doğrudan etkiliyor."),
     ("Sosyal medya bize müşteri getirmiyor, neden denemeliyiz?",
      "Getirmiyorsa içerik yanlış olabilir. Bir ay deneyip gelen aramaları ve 'buradan gördüm' diyen müşteriyi sayalım; işe yaramazsa devam etmeyin."),
    ]
    hizmet = {"sema_tur":"İşletme Tanıtım Videosu ve Sosyal Medya İçerik Üretimi",
              "kategori":["Pazarlama","Reklam","Yerel işletme"],
              "kitle":"%s'daki kafe, restoran, mağaza, salon ve yerel hizmet işletmeleri" % ad}
    semalar = sema_bloklari(c, hizmet, "%s İşletme Tanıtım" % ad, aciklama, "%s/sehir/%s.html" % (KOK, slug), sss)

    govde = """<section>
  <div class="wrap prose">
    {yerel_analiz}

    <p>{isletme}</p>
    <p>Küçük bir işletmenin en büyük sorunu içerik üretmeye vakit bulamamak. Biz ayda bir gün geliyor, dört haftalık içeriği tek seferde çekiyoruz; siz sadece yayınlıyorsunuz. {ekip}</p>

    <div class="rozetler">
      <span class="rozet">Aylık Reels Paketi</span><span class="rozet">Ürün Çekimi</span>
      <span class="rozet">Mekân Tanıtımı</span><span class="rozet">Google Profil Fotoğrafı</span>
      <span class="rozet">İçerik Takvimi</span><span class="rozet">Altyazılı Kısa Video</span>
    </div>

    <h2>{ad}{ek} aylık pakette ne var</h2>
    <ul>
      <li><strong>Tek çekim günü</strong> — mekân, ürün ve ekip görüntüleri bir arada</li>
      <li><strong>8–12 kısa dikey video</strong> — altyazılı, yayına hazır</li>
      <li><strong>20–30 fotoğraf</strong> — menü, ürün ve mekân</li>
      <li><strong>Google işletme profili</strong> — fotoğraf yükleme ve bilgi düzenleme</li>
      <li><strong>İçerik takvimi</strong> — hangi gün ne yayınlanacak</li>
      <li><strong>Aylık ölçüm</strong> — etkileşim takibi ve bir sonraki ayın planı</li>
    </ul>

    <h2>{ad} için içerik fikirleri</h2>
    <p>Aşağıdakiler {ad}{ek} çalıştığımız işletmelerde en çok tutan içerik türleri. İlk ayın takvimini
       genelde bunlardan üçünü seçerek kuruyoruz.</p>
    <ul>{fikirler}</ul>

    <h2 id="surec">Süreç</h2>
  </div>
  <div class="wrap">
    {surec}
  </div>
  <div class="wrap prose">
    <div class="kutu"><span class="etk">Ölçelim, sonra karar verin</span>
      <p>İlk ay bir deneme paketiyle başlıyoruz. Ay sonunda gelen arama sayısını, harita görüntülenmesini ve
         "sosyal medyadan gördüm" diyen müşteriyi birlikte sayıyoruz. Rakam ikna etmezse devam etmiyorsunuz.</p></div>
  </div>
</section>

""".format(yerel_analiz=YA.blok(c, "isletme"), fikirler="".join("<li>%s</li>" % x for x in icerik_fikirleri(c)),
           isletme=e(c.get("isletme_notu", "%s%s yerel işletme rekabeti giderek görselleşiyor; haritada ve sosyal medyada görünmeyen işletme tercih listesinin dışında kalıyor." % (ad, ek))),
           ekip=e(ekip_cumlesi(c)), ad=e(ad), ek=ek,
           surec=SUREC % ("İçerik planı","Ayın konu listesi ve çekim takvimi birlikte belirleniyor.",
                          "Çekim günü","Mekân, ürün ve ekip görüntüleri tek seferde toplanıyor.",
                          "Kurgu","Reels formatında altyazılı kısa videolar ve fotoğraf seçkisi.",
                          "Yayın ve ölçüm","Takvimle teslim; ay sonunda etkileşim değerlendirmesi."))

    return _kabuk(c, slug, baslik, aciklama, anahtar, semalar,
        "{ad}{ek} <i>işletme tanıtım</i> videosu".format(ad=e(ad), ek=ek),
        "Kafe, restoran, mağaza ve yerel işletmeler için aylık içerik paketi: kısa video, fotoğraf ve Google profili.",
        govde, "isletme", "İşletme tanıtım işlerimizden", sss, "isletme-tanitim",
        "Bir ay <i>deneyelim</i>.",
        "İşletmenizi anlatın; ilk ay ne çıkacağını ve maliyetini aynı gün söyleyelim.",
        "İşletme Tanıtım")


# ============================================================ GENEL İL SAYFASI
HIZMET_ANLATIM = [
 ("insaat-3d-modelleme", "İnşaat 3D modelleme ve mimari görselleştirme", "hizmetler/insaat-3d-modelleme.html",
  "Konut projesi, villa, site ve ticari yapı için mimari render, proje tanıtım animasyonu, iç mekân "
  "görselleştirme, yerleşim maketi ve 360° sanal tur. Temel atılmadan maket satışına başlamak isteyen "
  "projelerin ilk ihtiyacı."),
 ("emlak-video", "Emlak video çekimi ve gayrimenkul tanıtımı", "hizmetler/emlak-kurumsal.html",
  "Villa, daire, konut projesi, arsa ve ticari mülk için drone destekli ilan videosu, sanal tur ve "
  "profesyonel fotoğraf. İlanın listede öne çıkmasını ve gelen alıcının daha nitelikli olmasını sağlıyor."),
 ("urun-animasyon", "3D ürün ve hizmet animasyonu", "hizmetler/urun-animasyon.html",
  "Ürünü 3D modelleyip videoya çeviriyoruz: çalışma prensibi, kesit anlatım, patlatılmış görünüm, "
  "üretim hattı ve fiziksel ürünü olmayan hizmetler için süreç animasyonu. Fuar ve ihracatta çalışıyor."),
 ("klip-cekimi", "Klip çekimi", "hizmetler/klip-cekimi.html",
  "Müzik klibi, marka klibi ve sanatçı tanıtım videosu. Senaryo, sanat yönetimi, sinematografi, "
  "FPV drone ve renk düzenleme tek elden yürüyor."),
 ("drone-cekimi", "Drone ve FPV çekim", "hizmetler/drone-fpv.html",
  "Havadan 4K görüntü ve FPV ile tek nefeste akan mekân turları. Şantiye ilerleme takibi, arsa ilanı, "
  "tesis tanıtımı ve etkinlik çekimlerinde kullanılıyor."),
 ("dugun-cekimi", "Düğün ve etkinlik çekimi", "hizmetler/dugun-etkinlik.html",
  "Sinematik düğün filmi, nişan ve kına çekimi, dış çekim ve kurumsal etkinlik videosu. "
  "Ertesi gün paylaşılabilecek teaser ile birlikte."),
 ("isletme-tanitim", "İşletme tanıtım ve sosyal medya", "hizmetler/isletme-tanitim.html",
  "Kafe, restoran, mağaza, salon ve yerel hizmet işletmeleri için aylık içerik paketi: kısa dikey video, "
  "fotoğraf, Google işletme profili ve içerik takvimi."),
]

def _yerel_vurgu(c, anahtar):
    if anahtar == "insaat-3d-modelleme": return c["insaat"]
    if anahtar == "emlak-video":         return c["emlak"]
    if anahtar == "urun-animasyon":      return c["sanayi"]
    if anahtar == "drone-cekimi":        return c["cografya"]
    if anahtar == "klip-cekimi":
        return c.get("kultur") or ("%s%s çekim mekânı çeşitliliği klip prodüksiyonunda maliyeti düşürüyor." % (c["ad"], c["ek"]))
    if anahtar == "dugun-cekimi":
        return c.get("dugun_notu") or ("%s%s düğün düzenine göre kamera planını ve ekip sayısını ayarlıyoruz." % (c["ad"], c["ek"]))
    if anahtar == "isletme-tanitim":
        return c.get("isletme_notu") or ("%s%s yerel işletmelerde görünürlük giderek tercih sebebine dönüşüyor." % (c["ad"], c["ek"]))
    return ""


def sayfa_sehir(c):
    ad, ek, slug = c["ad"], c["ek"], c["slug"]
    url = "%s/sehir/%s.html" % (KOK, slug)
    baslik = kisa_baslik("%s Video Çekimi, Drone ve 3D Modelleme | Luna Yapım" % ad)
    aciklama = meta_desc(
        "%s%s video prodüksiyonu: inşaat 3D modelleme, emlak videosu, ürün animasyonu, klip, drone ve düğün çekimi." % (ad, ek),
        "%s ve tüm ilçeler." % ilk_ilceler(c))
    anahtar = ("%s video çekimi, %s drone çekimi, %s tanıtım filmi, %s inşaat 3d modelleme, %s emlak video, "
        "%s ürün animasyonu, %s klip çekimi, %s prodüksiyon şirketi" % tuple([ad.lower()]*8))

    sss = [
     ("%s%s hangi hizmetleri veriyorsunuz?" % (ad, ek),
      "İnşaat 3D modelleme ve mimari görselleştirme, emlak ve kurumsal tanıtım videosu, 3D ürün animasyonu, "
      "klip çekimi, drone ve FPV çekim, düğün ve etkinlik çekimi ile işletme tanıtım videosu — yedi ana hizmet."),
     ("%s%s kendi ekibinizle mi geliyorsunuz?" % (ad, ek), ekip_cumlesi(c)),
     ("Modelleme ve animasyon için %s%s bulunmanız gerekiyor mu?" % (ad, ek),
      "Hayır. 3D modelleme, mimari görselleştirme ve ürün animasyonu tamamen uzaktan yürüyor; projeyi "
      "gönderdiğiniz her ilde çalışabiliyoruz. Sadece gerçek kamera ve drone çekimi gerektiren işlerde sahaya çıkıyoruz."),
     ("%s%s hangi ilçelere gidiyorsunuz?" % (ad, ek),
      "%s dahil ilin tamamına gidiyoruz. Aynı gün birden fazla iş planlandığında ulaşım maliyeti bölünüyor." % ilce_metni(c)),
     ("Fiyatlarınız nasıl belirleniyor?",
      "İşin ölçeği, çekim günü sayısı ve teslim edilecek format sayısına göre. Projeyi anlattığınızda "
      "aynı gün net bir aralık veriyoruz; sürpriz kalem çıkarmıyoruz."),
    ]

    semalar = "\n".join('<script type="application/ld+json">\n%s\n</script>' % j(x) for x in (
      {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Ana Sayfa","item":KOK+"/"},
        {"@type":"ListItem","position":2,"name":"İller","item":KOK+"/sehir/"},
        {"@type":"ListItem","position":3,"name":ad,"item":url}]},
      {"@context":"https://schema.org","@type":"LocalBusiness","name":"Luna Yapım","description":aciklama,
       "url":url,"image":KOK+"/assets/og-image.png","telephone":"+905411602603","priceRange":"$$",
       "address":{"@type":"PostalAddress","addressLocality":"Bursa","addressRegion":"Bursa","addressCountry":"TR"},
       "areaServed":{"@type":"City","name":ad,"containedInPlace":{"@type":"Country","name":"Türkiye"}},
       "knowsAbout":[x[1] for x in HIZMET_ANLATIM],
       "hasOfferCatalog":{"@type":"OfferCatalog","name":"%s hizmetleri" % ad,"itemListElement":[
          {"@type":"Offer","itemOffered":{"@type":"Service","name":"%s %s" % (ad, x[1]),
           "url":(("%s/sehir/%s-%s.html" % (KOK, slug, x[0])) if sayfa_var(c, x[0]) else "%s/%s" % (KOK, x[2]))}}
          for x in HIZMET_ANLATIM]}},
      {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in sss]}))

    g = head(e(baslik), e(aciklama), e(anahtar), url, semalar)
    g += """<div class="page-hero">
  <img class="karga-buyuk" src="../assets/karga.png" alt="">
  <div class="wrap">
    <div class="crumbs"><a href="../">Ana Sayfa</a> · <a href="./">İller</a> · {ad}</div>
    <h1>{ad}{ek} video, drone ve <i>3D modelleme</i></h1>
    <p class="lede">İnşaat 3D modellemeden emlak videosuna, ürün animasyonundan klip çekimine kadar yedi hizmet — {ad}{ek} tek ekipten.</p>
    <div class="btnlar">
      <a class="btn btn-dolu" href="https://wa.me/905411602603">{ad} için teklif al</a>
      <a class="btn btn-cizgi" href="#hizmetler">Hizmetleri gör</a>
    </div>
  </div>
</div>

<section>
  <div class="wrap prose">
    <p>{giris} Luna Yapım Bursa merkezli bir yapım ve yazılım şirketi; modelleme ve animasyon işlerini
       uzaktan, kamera gerektiren işleri ise sahada yürütüyoruz. {ekip}</p>
    <h2 id="hizmetler">{ad}{ek} hizmetlerimiz</h2>
""".format(ad=e(ad), ek=ek, giris=e(giris_cumlesi(c)), ekip=e(ekip_cumlesi(c)))

    for i, (anahtar, hizmet_adi, genel_sayfa, aciklama_h) in enumerate(HIZMET_ANLATIM, 1):
        hedef = ("%s-%s.html" % (slug, anahtar)) if sayfa_var(c, anahtar) else ("../%s" % genel_sayfa)
        etiket = ("%s %s detay sayfası" % (ad, hizmet_adi)) if sayfa_var(c, anahtar) else ("%s hizmet detayı" % hizmet_adi)
        g += """    <h3>{n}. {hizmet}</h3>
    <p>{aciklama}</p>
    <p><strong>{ad} özelinde:</strong> {vurgu}</p>
    <p><a href="{hedef}">{etiket} →</a></p>
""".format(n=i, hizmet=e(hizmet_adi), aciklama=e(aciklama_h), ad=e(ad),
           vurgu=e(_yerel_vurgu(c, anahtar)), hedef=hedef, etiket=e(etiket))

    g += """  </div>
</section>

"""
    g += video_bolumu("isler", "İşlerimizden")

    komsu = [k for k in c["komsu"] if k in SEHIR_INDEKS][:4]
    kb = "".join('<a href="%s">%s</a>' % (k, e(SEHIR_INDEKS[k]["ad"])) for k in komsu)
    ic = []
    for anahtar, kalip, aciklama_i, _ in HIZMET_ADLARI:
        if sayfa_var(c, anahtar):
            ic.append('<a href="%s-%s"><b>%s</b><span>%s</span></a>'
                      % (slug, anahtar, e(kalip % ad), aciklama_i))
    ilgili = ('<div class="ilgili">\n      ' + "\n      ".join(ic) + '\n    </div>') if ic else ""

    g += """<section>
  <div class="wrap prose">
    <h2>{ad} — sık sorulan sorular</h2>
    {sss}
{ilgili_bas}
    <h2>Yakın iller</h2>
  </div>
  <div class="wrap"><div class="iller">{komsu}<a href="./" style="border-color:var(--kirmizi);color:var(--kirmizi)">Tüm iller →</a></div></div>
</section>

""".format(ad=e(ad), sss=sss_blok(sss), komsu=kb,
           ilgili_bas=("\n    <h2>%s%s hizmet sayfalarımız</h2>\n    %s\n" % (e(ad), ek, ilgili)) if ilgili else "")

    g += cta(c, "{ad}{ek} işe <i>hazırız</i>.".format(ad=e(ad), ek=ek),
                "Projeni anlat, {ad} için sana özel teklif çıkaralım. Genelde aynı gün dönüyoruz.".format(ad=e(ad)))
    g += FOOTER
    return slug + ".html", g
