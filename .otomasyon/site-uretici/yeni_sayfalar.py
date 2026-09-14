# -*- coding: utf-8 -*-
"""
YENİ SAYFALAR — fiyat konumlandırması, şeffaflık, SEO hizmetleri, AI kısa film.

Sitenin kendi kabuğunu (kabuk.head + FOOTER) kullanıyor; başlık hiyerarşisi,
canonical, OG etiketleri ve şemalar diğer sayfalarla birebir aynı çıkıyor.
"""
import os, json, html, datetime

from kabuk import head, FOOTER
from uretici import HEDEF, KOK, e, j, sss_blok, cta, video_bolumu, kisa_baslik, meta_desc

SITE = os.path.dirname(HEDEF)          # .../lunayapim
BUGUN = datetime.date.today().strftime("%Y-%m-%d")


def _sema(tur, **k):
    d = {"@context": "https://schema.org", "@type": tur}
    d.update(k)
    return d


def _kabuk(dosya, baslik_seo, aciklama, anahtar, semalar, h1, lede, govde, kok=""):
    url = "%s/%s" % (KOK, dosya)
    s = "\n".join('<script type="application/ld+json">\n%s\n</script>' % j(x) for x in semalar)
    g = head(e(kisa_baslik(baslik_seo)), e(meta_desc(aciklama)), e(anahtar), url, s)
    g += """<div class="page-hero">
  <img class="karga-buyuk" src="%sassets/karga.png" alt="">
  <div class="wrap">
    <div class="crumbs"><a href="%sindex">Ana Sayfa</a> · %s</div>
    <h1>%s</h1>
    <p class="lede">%s</p>
  </div>
</div>

""" % (kok, kok, e(baslik_seo.split("|")[0].strip()[:40]), h1, e(lede))
    g += govde
    g += FOOTER
    if kok == "":
        # kabuk alt klasör varsayıyor; kök sayfada ../ önekini kaldırıyoruz
        g = g.replace('"../assets/', '"assets/').replace("'../assets/", "'assets/")
        g = g.replace('href="../', 'href="').replace('src="../', 'src="')
    return g


# ══════════════════════════════════════════════════════════════════ FİYATLAR
# Pazarlama imzası. Ucuzluk iddiası değil — MEKANİZMA anlatımı.
IMZA = "Ucuz değil — aracısız."
IMZA_ALT = ("Fiyat farkımız indirimden gelmiyor. Aradan çıkardığımız her halkadan geliyor.")

NEDEN = [
 ("Aracı yok", "aracisiz",
  "Çekim, kurgu, 3D ve yazılım aynı ekipte. Ajansların çoğu işi alıp prodüksiyonu dışarı "
  "veriyor; her aracı kendi payını ekliyor ve iş üç el değiştirene kadar fiyat iki katına çıkıyor.",
  "Sizin ödediğiniz para işi yapan ekibe gidiyor, aracıya değil."),
 ("Ekip sürekli çalışıyor", "surekli",
  "Boş geçen ay yok. Sürekli üretim yapan bir ekipte ekipman, yazılım ve sabit giderler "
  "aya yayılıyor; iş başına düşen maliyet, ayda iki iş alan bir ekibinkinden belirgin düşük.",
  "Aynı ekipman ve aynı ekip, iş başına daha az maliyetle çalışıyor."),
 ("Tekrar eden işi yazılım yapıyor", "otomasyon",
  "Format çıkarma, altyazı, teslim paketi hazırlama, dosya adlandırma — bunları kendi "
  "yazdığımız araçlar yapıyor. Aynı işi elle yapan ekip o saatleri size faturalıyor.",
  "Kurgucunun zamanı asıl işe gidiyor; saat ücreti aynı ama harcanan saat az."),
 ("Tek çekimden çok çıktı", "coklu",
  "Bir çekim gününden yatay, kare ve dikey sürümler, kısa kesitler ve kapak görselleri "
  "birlikte çıkıyor. Piyasada her format ayrı kalem olarak fiyatlanıyor.",
  "Dört ayrı iş için dört ayrı ücret ödemiyorsunuz."),
]

# Neyi ucuza getirmiyoruz — asıl güveni bu bölüm veriyor.
KISMIYORUZ = [
 ("Çekim günü sayısı", "Bir günde bitmeyecek işi bir güne sıkıştırmıyoruz. Sıkıştırılan "
  "çekim, kurguda telafi edilemiyor."),
 ("Işık", "Işık kiralamak pahalı ama görüntünün pahalı görünmesini sağlayan tek kalem o. "
  "Buradan kısmak, bütün işi ucuz gösteriyor."),
 ("Ses", "İzleyici kötü görüntüye dayanıyor, kötü sese dayanmıyor. Yaka mikrofonu ve "
  "ortam sesi her işte var."),
 ("Renk", "Renk düzeltmesi 'filtre atmak' değil. Bu aşama atlandığında görüntü ham kalıyor "
  "ve fark hemen anlaşılıyor."),
 ("Revizyon hakkı", "İki tur revizyon fiyata dahil. 'Revizyon ek ücret' yazan teklif, "
  "işi baştan doğru yapmayacağını söylüyor demektir."),
]

FIYAT_TABLO = [
 ("İnşaat 3D modelleme", "Dış cephe render seti (6–10 görsel)", "45.000 – 250.000 ₺",
  "Blok sayısı, daire tipi, ışık senaryosu"),
 ("Proje tanıtım animasyonu", "60–90 sn, kurgu ve ses dahil", "90.000 – 180.000 ₺",
  "Süre, sahne sayısı, gerçek çekimle birleşim"),
 ("Ürün / makine animasyonu", "45–60 sn, kesit ve akış anlatımı", "80.000 – 160.000 ₺",
  "Model karmaşıklığı, dil sayısı"),
 ("Emlak video çekimi", "Portföy başına tur videosu", "2.500 – 12.000 ₺",
  "Mülk büyüklüğü, drone, aylık paket"),
 ("Kurumsal tanıtım filmi", "2–3 dk, çok mekânlı", "35.000 – 140.000 ₺",
  "Çekim günü, oyuncu, mekân sayısı"),
 ("Sosyal medya aylık üretim", "Aylık içerik paketi", "8.000 – 120.000 ₺/ay",
  "İçerik adedi, çekim günü, platform sayısı"),
 ("AI kısa film", "Karakter tutarlılığı olan kurgu film", "120.000 – 400.000 ₺",
  "Süre, sahne sayısı, karakter sayısı, tutarlılık zorluğu"),
]


# Piyasada YAYINLANMIŞ fiyat listeleriyle kıyas. Kural: rakip firma adı üzerinden
# "onlar pahalı" denmiyor; yayınlanmış, tarihli ve bağlantısı verilen listelerle
# kendi bandımız yan yana konuyor. Karşılaştırma ancak nesnel ve doğrulanabilir
# olursa dürüst olur — okuyan kaynağa tıklayıp kontrol edebilmeli.
PIYASA_KIYAS = [
 ("İnşaat 3D modelleme / mimari görselleştirme",
  "90.000 – 180.000 ₺", "45.000 – 150.000 ₺",
  "Tek blok için render seti + kısa animasyon"),
 ("3D ürün animasyonu (sinematik)",
  "50.000 – 120.000 ₺", "40.000 – 95.000 ₺",
  "Modelleme + animasyon + ses tasarımı"),
 ("Kurumsal / emlak tanıtım filmi",
  "35.000 – 65.000 ₺", "25.000 – 55.000 ₺",
  "Çekim + kurgu + renk + sosyal sürümler"),
 ("Reklam / marka filmi",
  "50.000 – 120.000 ₺", "35.000 – 100.000 ₺",
  "Senaryolu, çok planlı çekim"),
 ("Drone çekim (tek iş)",
  "25.000 – 50.000 ₺", "10.000 – 25.000 ₺",
  "Yarım günlük çekim + kurgu"),
 ("İşletme / sosyal medya (aylık)",
  "28.000 – 55.000 ₺", "14.000 – 40.000 ₺",
  "İçerik üretimi dahil aylık düzen"),
]

PIYASA_KAYNAK = [
 ("Video prodüksiyon ve tanıtım filmi fiyatları 2026",
  "https://www.medyabox.com.tr/tanitim-filmi-fiyatlari"),
 ("2026 yılı render fiyatları",
  "https://www.allrender.net/post/2026-yili-render-fiyatlari"),
 ("Sosyal medya yönetimi fiyat rehberi 2026",
  "https://kreativty.com/blog/sosyal-medya-yonetimi-ne-kadar-tutar-2026-fiyat-rehberi"),
]
PIYASA_TARIH = "25.08.2026"

# Bütçesi kısıtlı olan da bir yerden başlayabilsin diye. Rakamlar gerçek —
# bu kapsamda gerçekten yapabildiğimiz işler.
GIRIS_BANDI = [
 ("Tek video ile başla", "12.000 ₺'den",
  "Bir ürün, bir mekân ya da bir hizmet. Çekim + kurgu + yatay/kare/dikey teslim. "
  "İşe yaradığını görürsen devam ederiz."),
 ("Elindeki görüntüyü kurtar", "6.000 ₺'den",
  "Çekilmiş ama kullanılmayan görüntülerin var mı? Kurgu, renk, altyazı ve "
  "sosyal medya sürümleriyle yayınlanabilir hâle getiriyoruz."),
 ("Tek sayfa, tek render", "10.000 ₺'den",
  "Projenin tek bir açısı ya da tek bir iç mekânı. Satışa başlamak için çoğu zaman yeterli."),
]


def fiyatlar():
    dosya = "fiyatlar.html"
    semalar = [
      _sema("BreadcrumbList", itemListElement=[
        {"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": KOK + "/"},
        {"@type": "ListItem", "position": 2, "name": "Fiyatlar", "item": "%s/%s" % (KOK, dosya)}]),
      _sema("FAQPage", mainEntity=[
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FIYAT_SSS]),
    ]
    g = ['<section><div class="wrap prose">']
    g.append('<div class="kutu"><h2 style="margin-bottom:8px">%s</h2><p>%s</p></div>'
             % (e(IMZA), e(IMZA_ALT)))
    g.append("<h2>Fiyat farkı nereden geliyor</h2>")
    g.append("<p>Bir işin fiyatı iki şeyden oluşuyor: yapılan işin kendisi ve o işe eklenen "
             "halkalar. Biz ikincisini azaltıyoruz, birincisini değil. Aşağıda dört mekanizma "
             "var; hepsi doğrulanabilir, hiçbiri indirim değil.</p>")
    g.append('<div class="surec">')
    for i, (bas, _slug, ne, sonuc) in enumerate(NEDEN, 1):
        g.append('<div class="adim"><span class="n">%02d</span><div><b>%s</b><p>%s</p>'
                 '<p style="color:var(--kirmizi);font-size:14px;margin-top:6px">→ %s</p></div></div>'
                 % (i, e(bas), e(ne), e(sonuc)))
    g.append("</div>")

    g.append("<h2>Neyi ucuza getirmiyoruz</h2>")
    g.append("<p>Fiyatı aşağı çekmenin kolay yolu kaliteyi düşürmek. Bunu yapmıyoruz ve "
             "hangi kalemlerden kısmadığımızı açıkça yazıyoruz — bir teklifi kıyaslarken "
             "bu listeye bakın, ucuz teklifin nereden ucuzladığını buradan anlarsınız.</p>")
    g.append("<div class='tablo-kaydir'><table><tr><th>Kalem</th><th>Neden kısmıyoruz</th></tr>")
    for k, n in KISMIYORUZ:
        g.append("<tr><td><strong>%s</strong></td><td>%s</td></tr>" % (e(k), e(n)))
    g.append("</table></div>")

    g.append("<h2>Fiyat aralıkları</h2>")
    g.append("<p>Aşağıdakiler <strong>başlangıç aralıklarıdır</strong>, liste fiyatı değil. "
             "Aynı başlık altında çok farklı işler olabiliyor; bu yüzden aralığı belirleyen "
             "kalemi de yanına yazdık. Teklifte tek bir rakam ve kapsamı yazılı veriyoruz.</p>")
    g.append('<div class=\"tablo-kaydir\"><table><tr><th>Hizmet</th><th>Kapsam</th><th>Aralık</th><th>Fiyatı ne belirliyor</th></tr>')
    for h, kaps, ara, belirleyen in FIYAT_TABLO:
        g.append("<tr><td><strong>%s</strong></td><td>%s</td>"
                 "<td style='white-space:nowrap;color:var(--kirmizi)'>%s</td><td>%s</td></tr>"
                 % (e(h), e(kaps), e(ara), e(belirleyen)))
    g.append("</table></div>")

    g.append("<h2>Piyasa ne diyor, biz ne diyoruz</h2>")
    g.append("<p>Aşağıdaki soldaki sütun bizim uydurduğumuz bir rakam değil: "
             "sektörde <strong>yayınlanmış fiyat listelerinden</strong> derlendi ve "
             "kaynakları tablonun altında duruyor. İsteyen tıklayıp kontrol edebilir. "
             "Rakip firma adı üzerinden \u201conlar pahalı\u201d demiyoruz \u2014 "
             "herkesin görebileceği listelerle kendi bandımızı yan yana koyuyoruz.</p>")
    g.append('<div class=\"tablo-kaydir\"><table><tr><th>İş</th><th class="sag">Yayınlanmış piyasa</th>'
             '<th class="sag">Luna Yapım</th><th>Kapsam</th></tr>')
    for is_, piy, biz, kaps in PIYASA_KIYAS:
        g.append("<tr><td><strong>%s</strong></td>"
                 "<td class='sag' style='white-space:nowrap;color:var(--gri)'>%s</td>"
                 "<td class='sag' style='white-space:nowrap;color:var(--kirmizi)'>"
                 "<strong>%s</strong></td><td>%s</td></tr>"
                 % (e(is_), e(piy), e(biz), e(kaps)))
    g.append("</table></div>")
    g.append('<p style="color:var(--gri);font-size:14px;margin-top:12px">'
             'Piyasa sütunu %s tarihinde şu yayınlanmış listelerden derlendi: %s. '
             'Listeler değişebilir; bu sayfayı derleme tarihiyle birlikte yayınlıyoruz ki '
             'ne zamana ait olduğu belli olsun.</p>'
             % (e(PIYASA_TARIH),
                " · ".join('<a href="%s" rel="nofollow noopener" target="_blank">%s</a>'
                           % (u, e(ad)) for ad, u in PIYASA_KAYNAK)))
    g.append('<div class="kutu"><p><strong>Neden aşağıdayız:</strong> ucuz malzeme ya da '
             'acemi ekiple değil. Çekimi de kurguyu da 3D\'yi de yazılımı da aynı ekip '
             'yapıyor; taşeron, aracı ajans ve komisyon kalemi yok. Aradan çıkan her halka '
             'fiyattan düşüyor \u2014 işten değil.</p></div>')

    g.append("<h2>Bütçen küçükse de başlayabiliriz</h2>")
    g.append("<p>Yukarıdaki rakamlar tam kapsamlı işler için. Ama her işletmenin ilk adımı "
             "büyük olmak zorunda değil. Aşağıdakiler gerçekten yaptığımız, küçük bütçeyle "
             "başlanabilecek işler \u2014 sonuç işe yararsa büyütürüz.</p>")
    g.append('<div class="paketler">')
    for ad, bedel, aciklama in GIRIS_BANDI:
        g.append('<div class="paket"><h3>%s</h3>'
                 '<p style="color:var(--kirmizi);font-weight:700;font-size:19px;margin:2px 0 8px">%s</p>'
                 '<p>%s</p></div>' % (e(ad), e(bedel), e(aciklama)))
    g.append("</div>")
    g.append("<p>Bütçeni söyle, işi ona göre kurgulayalım. \u201cBu para yetmez\u201d "
             "demek yerine <strong>o bütçeyle ne yapılabileceğini</strong> yazıyoruz; "
             "olmuyorsa da açıkça olmuyor diyoruz.</p>")

    g.append("<h2>İki çalışma biçimi</h2>")
    g.append('<div class="paketler">')
    for ad, kime, sure, odeme, arti in (
        ("Proje bazlı", "Net bir işi var, bir kere çekilecek, uzun süre kullanılacak",
         "1–4 hafta", "%50 başlangıç + %50 teslim",
         "Tek seferlik bütçe; sonuç sizde kalıyor, istediğiniz yerde kullanıyorsunuz"),
        ("Aylık düzen", "Görünürlüğün sürmesi gerekiyor: portföy, devam eden proje, işletme",
         "Aylık, en az 3 ay önerilir", "Ay başında aylık bedel",
         "Birim maliyet belirgin düşük; ekip işinizi öğrendikçe çıkan iş iyileşiyor")):
        g.append('<div class="paket"><h3>%s</h3><p>%s</p>'
                 '<ul><li><strong>Süre:</strong> %s</li><li><strong>Ödeme:</strong> %s</li>'
                 '<li><strong>Artısı:</strong> %s</li></ul></div>'
                 % (e(ad), e(kime), e(sure), e(odeme), e(arti)))
    g.append("</div>")

    g.append("<h2>Teklif nasıl çıkıyor</h2>")
    g.append("<p>Teklif göndermeden önce sitenizi ve harita profilinizi inceliyoruz. "
             "Teklifin içinde ne bulduğumuz, hangi adreste ve hangi saatte baktığımız yazılı "
             "oluyor. Böylece fiyatı değil, <strong>yapılacak işi</strong> konuşuyoruz. "
             "Bu inceleme ücretsiz ve karşılığında bir şey istemiyoruz — beğenmezseniz "
             "elinizde kalıyor, kendi ekibinizle de uygulayabilirsiniz.</p>")
    g.append("<h2>Sık sorulan sorular</h2>")
    g.append(sss_blok(FIYAT_SSS))
    g.append("</div></section>\n")
    g.append(cta({"slug": "fiyatlar"}, "Kapsamı <i>netleştirelim</i>.",
                 "İşi anlatın; aralığı ve süresini aynı gün söyleyelim."))

    return dosya, _kabuk(
        dosya, "Fiyatlar ve Çalışma Biçimi | Luna Yapım",
        "Video, 3D ve sosyal medya üretiminde fiyatı ne belirliyor, neden daha uygun ve "
        "hangi kalemlerden kısmıyoruz. Aralıklar ve iki çalışma biçimi.",
        "video prodüksiyon fiyatları, 3d modelleme fiyat, tanıtım filmi maliyeti, "
        "emlak videosu fiyatı, sosyal medya aylık paket, ai kısa film fiyat",
        semalar,
        "Fiyatlar: <i>ucuz değil</i>, aracısız",
        "Fiyat farkımızın nereden geldiğini ve hangi kalemlerden kısmadığımızı açıkça "
        "yazıyoruz. Aşağıdaki aralıklar başlangıç noktası; teklifte tek rakam ve kapsamı olur.",
        "\n".join(g))


FIYAT_SSS = [
 ("Neden liste fiyatı yayınlamıyorsunuz?",
  "Aynı başlık altında on kat fark olabiliyor: tek blok bir proje ile çok bloklu bir site "
  "aynı iş değil. Liste fiyatı ya fazla ödetir ya da işi eksik yaptırır. Onun yerine aralığı "
  "ve fiyatı neyin belirlediğini yayınlıyoruz."),
 ("Daha uygun fiyat kaliteden mi kısıyorsunuz?",
  "Hayır, ve hangi kalemlerden kısmadığımızı sayfada listeledik: çekim günü, ışık, ses, renk "
  "ve revizyon hakkı. Fark aradan çıkardığımız aracılardan, sürekli çalışan bir ekibin "
  "maliyet avantajından ve tekrar eden işleri yazılımla yapmamızdan geliyor."),
 ("Ödeme nasıl yapılıyor?",
  "Proje bazlı işlerde başlangıçta %50, teslimde %50. Aylık düzende ay başında aylık bedel. "
  "Uzun projelerde aşamalara bölüyoruz; tutarlar teklifte yazılı oluyor."),
 ("Teklif sonrası fiyat değişir mi?",
  "Kapsam değişmedikçe değişmiyor. Kapsam büyürse farkı önceden yazılı bildiriyoruz; "
  "iş bittikten sonra sürpriz kalem çıkmıyor."),
 ("Küçük bütçeyle başlanabilir mi?",
  "Evet. Bütçe kısıtlıysa hangi kalemin en çok işe yarayacağını söylüyoruz ve oradan "
  "başlıyoruz. Gerekmeyen işi 'gerekmiyor' diye söylemek de bizim işimiz."),
]


# ══════════════════════════════════════════════════════════════════ ŞEFFAFLIK
def seffaflik(veri):
    """
    Kendi sitemizin gerçek rakamları. veri: denetçiden gelen ölçüm.
    Uydurma rakam yok — ölçülemeyen alan "henüz ölçülmedi" diye yazılıyor.
    """
    dosya = "seffaflik.html"
    semalar = [
      _sema("BreadcrumbList", itemListElement=[
        {"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": KOK + "/"},
        {"@type": "ListItem", "position": 2, "name": "Şeffaflık",
         "item": "%s/%s" % (KOK, dosya)}]),
    ]
    g = ['<section><div class="wrap prose">']
    g.append('<div class="kutu"><p><strong>Neden bu sayfa var:</strong> Müşterilerimize '
             '"sitenizde şu eksik" diyoruz. Aynı denetimi kendimize de uyguluyoruz ve '
             'sonucunu — iyi olsun kötü olsun — burada yayınlıyoruz. Rakamlar aracımızın '
             'ürettiği ölçümlerden geliyor, elle yazılmıyor.</p></div>')

    g.append("<h2>Bugünkü ölçüm</h2>")
    g.append('<div class="rozetler">')
    for etiket, deger, alt in veri["kutular"]:
        g.append('<div class="rozet"><b>%s</b><span>%s</span><small>%s</small></div>'
                 % (e(deger), e(etiket), e(alt)))
    g.append("</div>")
    g.append('<p style="color:var(--gri);font-size:14px;margin-top:14px">Son ölçüm: %s · '
             'Ölçüm aracı: Luna Pusula SEO denetçisi (%d kontrol)</p>'
             % (e(veri["zaman"]), veri["kontrol_sayisi"]))

    g.append("<h2>Kategori kırılımı</h2>")
    g.append("<p>Sitenin her bölümü ayrı ayrı denetleniyor. Aşağıdaki tablo hangi bölümde "
             "kaç sayfa olduğunu ve o bölümün denetimden nasıl geçtiğini gösteriyor.</p>")
    g.append('<div class=\"tablo-kaydir\"><table><tr><th>Bölüm</th><th class="sag">Sayfa</th><th class="sag">Hata</th>'
             '<th class="sag">Uyarı</th><th class="sag">Uygunluk</th></tr>')
    for k in veri["kategori"]:
        g.append('<tr><td><strong>%s</strong></td><td class="sag">%d</td>'
                 '<td class="sag">%d</td><td class="sag">%d</td>'
                 '<td class="sag" style="color:%s">%%%s</td></tr>'
                 % (e(k["ad"]), k["sayfa"], k["hata"], k["uyari"],
                    "var(--yesil)" if k["oran"] >= 99 else
                    ("var(--sari)" if k["oran"] >= 90 else "var(--kirmizi)"), k["oran"]))
    g.append("</table></div>")

    if veri.get("arama"):
        a = veri["arama"]
        g.append("<h2>Aramada bugün neredeyiz</h2>")
        g.append("<p>Yukarıdaki denetim sitenin kendi iç sağlığını ölçüyor. Asıl soru ise "
                 "şu: Google bizi görüyor mu? Aşağıdakiler o sorunun bugünkü cevabı.</p>")
        g.append('<div class=\"tablo-kaydir\"><table><tr><th>Ölçüm</th><th class="sag">Değer</th><th>Not</th></tr>')
        for etiket, deger, not_ in a["satir"]:
            g.append('<tr><td><strong>%s</strong></td>'
                     '<td class="sag" style="white-space:nowrap">%s</td>'
                     '<td style="color:var(--gri)">%s</td></tr>'
                     % (e(etiket), e(deger), e(not_)))
        g.append("</table></div>")
        g.append('<p style="color:var(--gri);font-size:14px;margin-top:10px">'
                 'Okuma tarihi: %s · Kaynak: %s</p>' % (e(a["tarih"]), e(a["kaynak"])))
        g.append('<div class="kutu"><p>%s</p></div>' % e(a["not"]))

    g.append("<h2>Neyi ne zaman düzelttik</h2>")
    g.append("<p>Bu sayfanın asıl işi ilerlemeyi göstermek. Aşağıdakiler kendi sitemizde "
             "bulduğumuz ve düzelttiğimiz eksikler — bulduğumuz gün ve düzelttiğimiz gün "
             "ile birlikte.</p>")
    g.append('<div class=\"tablo-kaydir\"><table><tr><th>Ne bulduk</th><th>Ne yaptık</th><th>Tarih</th></tr>')
    for ne, yapilan, tarih in veri["gunluk"]:
        g.append("<tr><td>%s</td><td>%s</td><td style='white-space:nowrap'>%s</td></tr>"
                 % (e(ne), e(yapilan), e(tarih)))
    g.append("</table></div>")

    if veri.get("acik_eksik"):
        g.append("<h2>Hâlâ eksik olanlar</h2>")
        g.append("<p>Kapanmamış maddeler de burada duruyor. Kendi eksiğini yazmayan bir "
                 "ajansın müşterisinin eksiğini doğru söylemesi beklenemez.</p><ul>")
        for x in veri["acik_eksik"]:
            g.append("<li>%s</li>" % e(x))
        g.append("</ul>")

    g.append("<h2>Nasıl ölçüyoruz</h2>")
    g.append("<p>Ölçüm, müşteri projelerinde kullandığımız aracın aynısı: sayfa sayfa "
             "başlık, açıklama, şema, başlık hiyerarşisi, paylaşım kartı, iç bağlantı, "
             "içerik derinliği ve dönüşüm unsurları kontrol ediliyor. Aynı aracı sizin "
             "sitenizde de çalıştırıp sonucu kaynaklarıyla birlikte veriyoruz.</p>")
    g.append('<p><a href="hizmetler/seo-icerik">SEO ve içerik hizmetimize</a> ya da '
             '<a href="fiyatlar">fiyat sayfamıza</a> bakabilirsiniz.</p>')
    g.append("</div></section>\n")
    g.append(cta({"slug": "seffaflik"}, "Aynı denetimi <i>sizin sitenizde</i> yapalım.",
                 "Ne bulduğumuzu kaynaklarıyla yazıp gönderelim; ücretsiz."))

    return dosya, _kabuk(
        dosya, "Şeffaflık: Kendi Rakamlarımız | Luna Yapım",
        "Müşterilerimize uyguladığımız denetimi kendi sitemize de uyguluyoruz. "
        "Ölçüm sonucu, kategori kırılımı, düzelttiğimiz ve hâlâ açık olan eksikler.",
        "luna yapım şeffaflık, seo denetim sonucu, ajans kendi verisi, site sağlık raporu",
        semalar,
        "Kendi rakamlarımız, <i>olduğu gibi</i>",
        "Müşterilerimize uyguladığımız denetimin aynısını kendimize uyguluyoruz ve "
        "sonucunu burada yayınlıyoruz — düzelttiklerimizi de, hâlâ açık olanları da.",
        "\n".join(g))
