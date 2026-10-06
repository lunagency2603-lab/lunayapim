# -*- coding: utf-8 -*-
"""Web sitesi tasarımı ve yaratıcı site eklentileri hizmet sayfası (06.10.2026).

Gerekçe: sitede web tasarımı hizmeti hiç anlatılmıyordu (yalnız yazılım sayfasında
"Web & entegrasyon" başlığı vardı); SEO sayfaları da yalnız ana sayfa alt bilgisinden
ve "Prodüksiyon" etiketli hizmetler dizininden açılıyordu.

DÜRÜSTLÜK KURALI (yeni_hizmetler.py ile aynı): yalnız gerçekten yaptığımız ve şu an
bu sitede çalışan iş yazılır. Müşteri adı, sektörü ve tanınmasına yol açacak ayrıntı
YAZILMAZ. "Neyi yapmıyoruz" bölümü zorunlu. Fiyat bandı yok: kapsama göre teklif.
"""
import os

from uretici import sss_blok, cta
from yeni_hizmetler import _hizmet_kabugu, _surec, _paketler


def web_sitesi_tasarimi():
    dosya = "web-sitesi-tasarimi.html"
    ad = "Web Sitesi Tasarımı ve Yaratıcı Site Eklentileri"
    aciklama = ("Web sitesi tasarımı: hızlı, ölçülen ve aramaya hazır siteler. Mevcut "
                "sitenize tasarım stüdyosu, site asistanı, canlı sahne gibi çalışan eklentiler.")
    anahtar = ("web sitesi tasarımı, web tasarım, kurumsal web sitesi, bursa web tasarım, "
               "web sitesi yaptırmak, site eklentisi, ürün tasarım aracı, site asistanı, "
               "wordpress taşıma, statik site, seo uyumlu web sitesi")
    sss = [
      ("Hangi altyapıyı kullanıyorsunuz?",
       "Tanıtım sitelerinin çoğu için statik yapı: sayfalar önceden üretilir ve dağıtım "
       "ağından sunulur. Hızlı açılır, veritabanı ve eklenti güncellemesi gerektirmez. "
       "İçeriği sık değiştiren bir ekibiniz varsa düzenleme yöntemini baştan birlikte seçiyoruz."),
      ("Mevcut sitemi değiştirmeden eklenti koyabilir misiniz?",
       "Çoğu durumda evet. Tasarım stüdyosu, site asistanı, kaydırıcı ve sahneler sayfaya bir "
       "betik ve bir yer tutucu olarak eklenir; sitenizin geri kalanına dokunulmaz. Önce "
       "altyapınıza bakıp olup olmayacağını yazılı olarak söylüyoruz."),
      ("Site asistanı bir yapay zekâ hizmetine mi bağlı?",
       "Bu sitedeki değil: cevaplar sitenin kendi metinlerinden çıkıyor, soru tarayıcıdan "
       "dışarı gitmiyor, aylık ücreti yok. Dış bir dil modeline bağlanması istenirse maliyeti "
       "ve verinin nereye gittiği ayrıca konuşulur."),
      ("Google'da ilk sayfaya çıkar mıyım?",
       "Söz vermiyoruz. Teknik altyapıyı eksiksiz kuruyor, yayından sonra Arama Konsolu'ndan "
       "dizin ve tıklamayı okuyoruz. Rekabetli aramalarda sıralamayı belirleyenlerin bir kısmı "
       "— başka sitelerden gelen bağlantılar, işletme profili, yorumlar — sitenin dışında; "
       "bunları da açıkça yazıyoruz. Kendi sitemizin rakamları "
       "<a href=\"seo-ornegi-lunayapim\">SEO örneği</a> sayfasında."),
      ("Site kimin adına olur?",
       "Sizin. Alan adı, barındırma, Arama Konsolu ve Analytics hesapları sizin adınıza açılır, "
       "bize yetki verilir. Kaynak dosyalar teslimde sizde kalır; ayrıldığınızda site sizinle gider."),
      ("Metinleri siz mi yazıyorsunuz?",
       "İsterseniz evet. İşinizi sizden dinleyip sizin rakamlarınızla yazıyoruz; doğrulayamadığımız "
       "iddia sitede yer almıyor. Görsel ve video tarafı da aynı ekipte: "
       "<a href=\"urun-animasyon\">ürün animasyonu</a>, <a href=\"drone-fpv\">drone çekimi</a>, "
       "<a href=\"isletme-tanitim\">tanıtım videosu</a>."),
    ]

    g = ['<section><div class="wrap prose">']
    g.append("<p>Çoğu firma sitesi kartvizitin dijital hâli: açılıyor, okunuyor, kapanıyor. "
             "Biz siteyi iki işe göre kuruyoruz — <strong>aranınca bulunmak</strong> ve "
             "<strong>ziyaretçiyi bir adım ileri taşımak</strong>: mesaj, arama, teklif.</p>")

    g.append("<h2>İlk örnek: okuduğunuz site</h2>")
    g.append("<p>lunayapim.com'u sıfırdan biz yazdık. Beş yüzü aşkın sayfası var ve her yayından "
             "önce otomatik bir denetimden geçiyor; hata veren sürüm yayına çıkmıyor. Google "
             "dizinindeki yolculuğunu rakamlarıyla <a href=\"seo-ornegi-lunayapim\">SEO örneği</a> "
             "sayfasında yazdık. İkinci örnek <a href=\"https://trendsaphiens.com/\">trendsaphiens.com</a>: "
             "her gün kendi yazdığımız sistemle güncellenen bir haber ve veri sitesi; yeni alan "
             "adındaki ilk haftaları <a href=\"seo-ornegi-trendsaphiens\">burada</a>.</p>")

    g.append("<h2>Müşteri işleri</h2>")
    g.append("<p>Kendi sitelerimizde denediğimiz parçaları müşterilerimiz için de kuruyoruz. "
             "Üçü de çalışır hâlde; tıklayıp açabilirsiniz.</p>")
    g.append('</div><div class="wrap"><div class="uv-izgara">')
    for href, gorsel, alt, etiket, rom, baslik, metin, ok in [
        ("https://aktasprefabrikev.com/ev-tasarla/", "aktas-ev-tasarlayici.jpg",
         "Aktaş Prefabrik 3B ev tasarlayıcısı: tek katlı 2+1 model ve seçim paneli",
         "Canlı", "i · Prefabrik ev üreticisi", "Aktaş Prefabrik — 3B ev tasarlayıcı",
         "Ziyaretçi kat sayısını, oda düzenini, cepheyi, çatıyı ve terası seçiyor; ev "
         "tarayıcıda firmanın ölçülü plan çizimlerinden kuruluyor. İçinde yürünüyor, gece "
         "görünümüne geçiliyor, seçime en yakın model ve liste fiyatı yanda çıkıyor. Sitenin "
         "tamamını da WordPress'ten statik yapıya biz taşıdık.", "Tasarlayıcıyı aç →"),
        ("../onizleme/ata-kumas/", "ata-kumas-vitrin.jpg",
         "Ata Kumaş vitrin sitesinin açılış görüntüsü: desenli kumaşlar",
         "Tasarım önizlemesi", "ii · Kumaş mağazası", "Ata Kumaş — vitrin ve sanal mağaza",
         "Bursa'daki kumaş mağazasının Trendyol ürünleri kartela düzeninde. Sanal mağaza "
         "turu ve kumaşı kadın ve erkek 3B mankenin üzerinde gösteren podyum; satın alma "
         "doğrudan Trendyol'daki ürüne bağlanıyor.", "Vitrini aç →"),
        ("../isler/yade-vogue-3d-animasyon-klip", "../video/yade-vogue.jpg",
         "YADE × Vogue klibinden kare: siyah ejderha YADE, bazalt sütunlar arasında",
         "Klip", "iii · Müzik klibi", "YADE × Vogue — 3D animasyon klip",
         "gustosound'un Vogue parçası için 2:40'lık klip. Beş dünya Blender'da 3D olarak "
         "kuruldu, kurgu şarkının vuruşlarına göre biçildi; karakter yakın planları yapay "
         "zekâ desteğiyle üretildi.", "Klibi izle →"),
    ]:
        src = gorsel if gorsel.startswith("../") else "web/" + gorsel
        g.append('<a class="uv gor" href="%s"%s><span class="uv-gorsel">'
                 '<img src="../assets/%s" width="800" height="450" loading="lazy" alt="%s">'
                 '<i class="uv-yz">%s</i></span><span class="uv-metin"><span class="rom">%s</span>'
                 '<h3>%s</h3><p>%s</p><span class="ok">%s</span></span></a>'
                 % (href, ' rel="noopener" target="_blank"' if href.startswith("http") else "",
                    src.replace("../video/", "video/"), alt, etiket, rom, baslik, metin, ok))
    g.append('</div></div><div class="wrap prose">')

    g.append("<h2>Sitenize ekleyebileceğimiz yaratıcı parçalar</h2>")
    g.append("<p>Aşağıdakilerin hepsini kendimiz yazdık ve hepsi şu an bu sitede çalışıyor — "
             "tıklayıp deneyebilirsiniz. Çoğu bir dış hizmete bağlı değil; sunucu, anahtar ya da "
             "aylık abonelik gerektirmiyor.</p>")
    g.append("<ul>"
             "<li><strong>Ürün tasarım stüdyosu.</strong> Ziyaretçi ürünü ve rengini seçer, kendi "
             "yazısını ya da görselini yerleştirir, sonucu ürünün üzerinde görür; sipariş tek "
             "mesajla gelir. Dosya hiçbir sunucuya yüklenmez. "
             "<a href=\"baskili-tisort\">Baskılı tişört sayfasında deneyin</a>.</li>"
             "<li><strong>Site asistanı.</strong> Ziyaretçinin sorusunu sitenin kendi metinlerinden "
             "cevaplar, kaynak sayfayı bağlar, bilmediğinde uydurmaz ve WhatsApp'a devreder. "
             "Cevaplanamayan sorular ölçüme düşer; sitede hangi bilginin eksik olduğunu böyle "
             "görüyoruz.</li>"
             "<li><strong>Teklif ve plan aracı.</strong> Hizmeti seçen ziyaretçiye sitedeki fiyat "
             "tablosundan bant gösterir, çalışma takvimini takvim dosyası olarak verir. Kesin "
             "teklif yine insandan çıkar.</li>"
             "<li><strong>Derinlikli sahneler.</strong> Kaydırdıkça katmanları farklı hızda kayan "
             "fon (<a href=\"../\">ana sayfamızın</a> arkasındaki sisli orman ve karga) ve "
             "tarayıcıda canlı dönen tel kafes bina modeli "
             "(<a href=\"../studyo\">stüdyo sayfası</a>).</li>"
             "<li><strong>Öncesi/sonrası kaydırıcı.</strong> Ham görüntü ile işlenmiş hâli aynı "
             "karede; <a href=\"../studyo\">stüdyo sayfasında</a>.</li>"
             "<li><strong>Sinematik video girişi.</strong> Sayfa başında sırayla oynayan klipler, "
             "bölüm sayacı ve ilerleme çubuğu.</li>"
             "<li><strong>Kendini güncelleyen sayfalar.</strong> Kur, altın gibi her gün değişen "
             "verinin kaynağından alınıp tarihli sayfaya dönüşmesi — TrendSaphiens'in piyasa "
             "sayfaları böyle çalışıyor.</li>"
             "<li><strong>Pazaryeri bağlantısı.</strong> Trendyol Satıcı API ile ürün yükleme; "
             "ayrıntısı <a href=\"e-ticaret\">e-ticaret</a> sayfasında.</li>"
             "</ul>")
    g.append("<p>Hareketli her parça, ziyaretçinin “hareketi azalt” tercihine uyar ve sayfanın "
             "açılmasını engellemeden yüklenir. Efekt, sitenin hızından pay almamalı.</p>")

    g.append("<h2>Bir sitede neye bakıyoruz</h2>")
    g.append("<ul>"
             "<li><strong>Hız.</strong> Sayfa ağırlığı, görsel boyutları, mobilde açılış.</li>"
             "<li><strong>Aranınca bulunmak.</strong> Başlık, açıklama, yapılandırılmış veri, site "
             "haritası ve dizin durumu. SEO tarafı aynı ekipte: "
             "<a href=\"seo-icerik\">SEO ve içerik hizmeti</a>.</li>"
             "<li><strong>Ölçüm.</strong> WhatsApp, telefon, form ve e-posta tıklamaları ayrı ayrı "
             "ölçülür. Reklam açılırsa algoritma doğru şeyi öğrensin diye.</li>"
             "<li><strong>Yapay zekâ aramaları.</strong> Asistanların siteyi doğru okuyabilmesi için "
             "düz metin harita ve açık künye: <a href=\"yapay-zeka-seo\">yapay zekâ destekli SEO</a>.</li>"
             "</ul>")

    g.append("<h2>Süreç</h2></div><div class=\"wrap\">")
    g.append(_surec([
        ("Okuma", "Siteniz varsa hız, dizin ve ölçüm durumu okunur; yoksa sizin işinizde "
                  "aranan sayfalar çıkarılır."),
        ("Plan", "Sayfa listesi, her sayfanın karşılayacağı arama ve ziyaretçiden beklenen "
                 "adım — yazılı."),
        ("Tasarım ve yazım", "Metinler sizin işinizden yazılır; şablon cümle ve dolgu sayfa yok."),
        ("Kurulum ve ölçüm", "Alan adı, barındırma ve ölçüm hesapları sizin adınıza; her ölçüm "
                             "olayı denenerek açılır."),
        ("Yayın ve ilk okuma", "Arama Konsolu'na gönderim, ilk hafta dizin ve tıklama okuması."),
    ]))
    g.append('</div><div class="wrap prose">')

    g.append("<h2>Paketler</h2>")
    g.append(_paketler([
        ("Tanıtım sitesi", "Tek seferlik", [
            "Hizmet sayfaları ve iletişim",
            "Mobil öncelikli, hızlı yapı",
            "Yapılandırılmış veri ve site haritası",
            "WhatsApp, telefon ve form ölçümü"]),
        ("Yaratıcı eklenti", "Mevcut sitenize", [
            "Stüdyo, asistan, sahne ya da kaydırıcı",
            "Sitenizin tasarımına uyarlanır",
            "Çoğu tek betik ve veri dosyası",
            "Ölçüm olayıyla birlikte teslim"]),
        ("Site ve bakım", "Kurulum + aylık", [
            "Tanıtım sitesi paketindekiler",
            "Aylık dizin ve hız okuması",
            "Sayfa ve içerik ekleme",
            "Aylık rapor"]),
    ]))

    g.append("<h2>Eski sitenizi taşımak</h2>")
    g.append("<p>WordPress ya da hazır panel kullanan bir siteyi statik yapıya taşıyabiliyoruz. "
             "Eklenti güncellemesi, veritabanı ve güvenlik yaması yükü ortadan kalkar, sayfalar "
             "daha hızlı açılır. Eski adresler kalıcı yönlendirmeyle yenilerine bağlanır; aramadaki "
             "geçmiş kaybolmaz. İçeriği sık değiştiriyorsanız düzenleme ihtiyacını taşımadan önce "
             "konuşuyoruz — her site için statik yapı doğru cevap değil.</p>")

    g.append("<h2>Neyi yapmıyoruz</h2>")
    g.append("<p>Hazır temayı satıp “özel tasarım” demiyoruz. Alan adını, barındırmayı ya da "
             "ölçüm hesaplarını kendi adımıza açmıyoruz. Sayfa sayısını şişirmek için birbirinin "
             "kopyası sayfalar üretmiyoruz; arama motorları bunu cezalandırıyor. “İlk sırada "
             "çıkarırız” garantisi vermiyoruz — sıralamayı arama motoru belirliyor, biz ölçüyü ve "
             "yapılacak işi yazılı veriyoruz. Siteyi ağırlaştıran, ölçülmemiş efekt koymuyoruz.</p>")

    g.append("<h2>Fiyat</h2>")
    g.append("<p>Tanıtım sitesi tek seferlik; sayfa sayısına ve eklentilere göre fiyatlanıyor. "
             "Eklentiler ayrı ayrı da alınabiliyor. Ne istediğinizi ya da mevcut sitenizin adresini "
             "yazın, aynı gün net bir aralık verelim; diğer hizmetlerin bantları "
             "<a href=\"../fiyatlar\">fiyat sayfamızda</a>.</p>")
    g.append("</div></section>")
    g.append('<section><div class="wrap prose"><h2>Sık sorulan sorular</h2>%s</div></section>'
             % sss_blok(sss))
    g.append(cta({"slug": "web-sitesi-tasarimi"},
                 "Sitenizi <i>çalışan</i> hâle getirelim.",
                 "Adresinizi ya da ne istediğinizi yazın; neye bakacağımızı ve hangi eklentinin "
                 "işinize yarayacağını aynı gün söyleyelim."))
    return dosya, _hizmet_kabugu(
        dosya, "Web Sitesi Tasarımı ve Site Eklentileri | Luna Yapım", aciklama, anahtar,
        "Web sitesi tasarımı ve <i>yaratıcı eklentiler</i>",
        "Sitenizi sıfırdan kuruyoruz ya da mevcut sitenize ziyaretçinin kullandığı, ölçülen "
        "parçalar ekliyoruz. Örneklerin hepsi şu an bu sitede çalışıyor.",
        "\n".join(g), ad, sss)


def yayinla(kok):
    d = os.path.join(kok, "hizmetler")
    dosya, html = web_sitesi_tasarimi()
    with open(os.path.join(d, dosya), "w", encoding="utf-8") as y:
        y.write(html)
    return {"web_tasarim": dosya}


if __name__ == "__main__":
    import sys
    print(yayinla(sys.argv[1] if len(sys.argv) > 1 else "."))
