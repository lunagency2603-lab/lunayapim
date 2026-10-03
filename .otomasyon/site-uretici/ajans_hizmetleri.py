# -*- coding: utf-8 -*-
"""Ajans tarafı hizmet sayfaları: reklam yönetimi, sosyal medya, pazar araştırması.

DÜRÜSTLÜK KURALI (yeni_hizmetler.py'deki ile aynı): yalnız GERÇEKTEN yaptığımız iş
yazılır. Buradaki her sayı, devraldığımız hesaplarda ve kendi sitelerimizde ölçülmüş
gerçek sayıdır; müşteri adı, sektörü ve tanınmasına yol açacak ayrıntı YAZILMAZ.
Her sayfada "Neyi yapmıyoruz" bölümü zorunludur.
"""
import os

from kabuk import head, FOOTER
from uretici import KOK, e, j, sss_blok, cta, kisa_baslik, meta_desc
from yeni_hizmetler import _hizmet_kabugu, _surec, _paketler


# ══════════════════════════════════════════════════ REKLAM YÖNETİMİ + DENETİM
def reklam_yonetimi():
    """Google Ads + Meta reklam yönetimi; giriş kapısı reklam denetimi.

    Dayanak: devraldığımız bir hesapta 30 günlük harcamanın tamamı tek tek
    okundu; platformun kendi CSV dışa aktarımıyla yaş, bölge, yerleşim ve
    reklam kırılımları çıkarıldı. Rakamlar oradan; firma tanınmayacak şekilde
    oran ve yöntem düzeyinde yazıldı.
    """
    dosya = "reklam-yonetimi.html"
    ad = "Reklam Yönetimi — Google Ads ve Meta"
    aciklama = ("Google Ads ve Meta reklam yönetimi: önce hesap denetimi, sonra kurulum. "
                "Gerçek sonucun maliyetini ölçeriz, tıklamanın değil. Bütçe ve kapsam "
                "yazılı, karşılaştırma tablosu açık.")
    anahtar = ("reklam yönetimi, google ads yönetimi, meta reklam yönetimi, "
               "facebook reklam ajansı, instagram reklam yönetimi, reklam denetimi, "
               "google ads ajansı, reklam hesabı analizi, dönüşüm takibi kurulumu, "
               "reklam bütçesi optimizasyonu")
    sss = [
      ("Reklam yönetimi ücreti nasıl belirleniyor?",
       "Aylık sabit bedel alıyoruz, reklam harcamanızın yüzdesini değil. Yüzde usulü, "
       "ajansın bütçeyi büyütmekte çıkarı olması demek; biz tam tersini savunduğumuz "
       "durumlarda da aynı parayı kazanmak istiyoruz. Bedel hesabın büyüklüğüne ve kaç "
       "platform yönettiğimize göre değişiyor, teklifte tek rakam olarak yazılı oluyor."),
      ("Önce denetim şart mı, doğrudan kampanya kuramaz mısınız?",
       "Kurabiliriz ama önermiyoruz. Çalışan bir hesapta ilk iş, paranın nereye gittiğini "
       "görmek. Denetim bir haftada bitiyor ve çıktısı yazılı bir rapor oluyor; rapordan "
       "sonra devam etmezseniz rapor yine sizde kalır."),
      ("Mevcut ajansımla çalışıyorum, hesabı kapatmam mı gerekiyor?",
       "Hayır. Denetim için görüntüleme yetkisi yeterli. Devir konuşulursa ilkemiz "
       "“erişim değil sahiplik”: reklam hesabı, sayfa, veri kümesi ve ölçüm "
       "varlıkları sizin tüzel kişiliğinizde olur, ajansın değil."),
      ("Ne kadar bütçeyle başlanabilir?",
       "Yönetim bedelinin kendini çıkarması için bir alt sınır var; bütçeniz onun altındaysa "
       "bunu söylüyoruz ve reklam yerine hangi işin daha çok getireceğini anlatıyoruz. "
       "Küçük bütçede çoğu zaman doğru cevap reklam değil, sitenin dönüşüm oranı oluyor."),
      ("Kaç günde sonuç görürüm?",
       "Kurulumdan sonra ilk okunabilir veri 7. günde, ilk karar 13–14. günde çıkıyor. "
       "Daha erken konuşulan her şey gürültü. Kampanyayı sonuç gelmedi diye kapatmıyoruz; "
       "önce neden gelmediğini buluyoruz."),
      ("Sonuç garantisi veriyor musunuz?",
       "Hayır. Garanti veren bir kurulum yok; veren varsa ya sonucu kendisi tanımlıyor ya da "
       "ölçüyü seçiyor. Bizim verdiğimiz söz, başlangıç tablosunu yazıp aynı ölçülerle "
       "karşılaştırmak ve kötüleşen bir kalemi size biz söylemek."),
      ("Hangi platformlarda çalışıyorsunuz?",
       "Google Ads (arama, performans maks., YouTube) ve Meta (Facebook, Instagram). "
       "Daha önce kurmadığımız bir platformu kurmadığımızı baştan söylüyoruz."),
    ]
    g = ['<section><div class="wrap prose">']
    g.append("<p>Reklam hesaplarının çoğu iyi yönetiliyor gibi görünür. Rapor dolu, maliyet "
             "düşük, grafikler yukarı bakar. Sorun genellikle bir yerde gizlenir: hesap "
             "yanlış soruyu ucuza cevaplar.</p>")

    g.append("<h2>Bir denetimde ne çıkıyor</h2>")
    g.append("<p>Devraldığımız bir hesapta 30 günlük harcamanın tamamını tek tek okuduk. "
             "Panelde “aramalar” kalemi ucuz görünüyordu. Ama aynı platformun "
             "raporunda, aramanın 20 saniyeyi ve 60 saniyeyi geçip geçmediğini gösteren iki "
             "sütun daha vardı — kimse açmamıştı. Açtığımızda, konuşmaya dönüşen bir arama "
             "için gerçek maliyet, raporlanan maliyetin <strong>altı katından fazlaydı</strong>.</p>")
    g.append("<p>Aynı okuma dört şeyi daha gösterdi:</p>")
    g.append("<ul>"
             "<li>Fiyat bilgisi yanlış yazılmış iki reklam, bir ayın harcamasının "
             "<strong>dörtte birini</strong> tüketmişti. İnsanlar arıyor, doğru fiyatı "
             "duyuyor, kapatıyordu — o kampanyanın 20 saniyeyi geçen arama oranı hesabın "
             "en düşüğüydü.</li>"
             "<li>Bir kampanya ay boyunca beş haneli bir bütçe harcayıp <strong>tek bir iş "
             "sonucu</strong> üretmemişti; ölçtüğü şey profil ziyaretiydi.</li>"
             "<li>Sitede 76.000 sayfa görüntülemeye karşılık ölçüm kodunun gördüğü talep "
             "sayısı <strong>6</strong>'ydı. Yani algoritma “kim satın alır”ı "
             "değil, “kim düğmeye basar”ı öğreniyordu.</li>"
             "<li>Siteyi ziyaret edenlere yeniden ulaşmak için kurulmuş <strong>tek bir "
             "kitle yoktu</strong>. O havuz geriye dönük dolmuyor; kurulmadığı her gün "
             "kaybediliyor.</li>"
             "</ul>")
    g.append("<p>Hiçbiri gizli bir bilgi değildi. Hepsi hesabın kendi ekranında duruyordu.</p>")

    g.append("<h2>Nasıl ölçüyoruz</h2>")
    g.append("<p>Reklam panelleri tabloyu ekrana sığdığı kadar gösterir; ekrandan okunan "
             "sayı eksik olur. Biz platformun kendi dışa aktarımını alıp satırların tamamını "
             "okuyoruz. Sonra dört kırılıma bakıyoruz: <strong>yaş</strong>, "
             "<strong>bölge</strong>, <strong>yerleşim</strong> ve <strong>reklam</strong>.</p>")
    g.append("<p>Bu kırılımlar genellikle birbiriyle çelişir, ve asıl bilgi oradadır. "
             "Bir hesapta en ucuz aramayı üreten yaş grubu, konuşmaya dönüşme oranına "
             "bakıldığında <strong>en pahalı</strong> gruptu — ucuz arıyor, hemen kapatıyordu. "
             "Yerleşimler arasındaki fark dört kattan fazlaydı ve en pahalı yerleşim bütçe "
             "aldığı hâlde sıfır arama üretmişti. Videolu reklamlar durağan görsellere göre "
             "belirgin şekilde ucuza çalışıyordu; üretilen video sayısı ise sıfırdı.</p>")

    g.append("<h2>Süreç</h2></div><div class=\"wrap\">")
    g.append(_surec([
        ("Denetim", "Görüntüleme yetkisiyle 30 günün tamamı okunur. Bütçeye dokunulmaz."),
        ("Rapor", "Nerede ne kaybediliyor, hangi ölçü yanlış — yazılı, sayılarla."),
        ("Başlangıç tablosu", "Bugünün değerleri kayda geçer; sonradan tartışma olmasın."),
        ("Kurulum", "Yapı, kitle, yerleşim ve ölçüm yeniden kurulur. Çalışan reklam, "
                    "yerine geçecek kanıtlanmadan kapatılmaz."),
        ("7. ve 14. gün", "Arama terimleri ve ilk karar. Kötüleşen kalemi biz söyleriz."),
    ]))
    g.append('</div><div class="wrap prose">')

    g.append("<h2>Paketler</h2>")
    g.append(_paketler([
        ("Reklam denetimi", "Tek seferlik", [
            "30 günlük harcamanın tamamı okunur",
            "Yaş, bölge, yerleşim ve reklam kırılımı",
            "Gerçek sonuç maliyeti hesabı",
            "Yazılı rapor — devam etmeseniz de sizde kalır"]),
        ("Tek platform yönetimi", "Aylık", [
            "Google Ads ya da Meta",
            "Yapı, kitle ve ölçüm kurulumu",
            "Yeniden hedefleme kitleleri",
            "Aylık karşılaştırma tablosu"]),
        ("İki platform + içerik", "Aylık", [
            "Google Ads ve Meta birlikte",
            "Reklam için dikey video üretimi",
            "Her kampanyada en az üç yaratıcı testi",
            "Aylık rapor ve bütçe önerisi"]),
    ]))

    g.append("<h2>Ölçüyü biz seçmiyoruz</h2>")
    g.append("<p>İşin başında tek bir soruyu birlikte cevaplıyoruz: <em>sizin için sonuç "
             "nedir?</em> Telefonun çalması mı, 60 saniyeyi geçen bir görüşme mi, formun "
             "dolması mı, mağazaya gelinmesi mi. Cevap neyse rapor onun üzerine kuruluyor. "
             "Tıklama ve gösterim raporda yer alır ama başarı ölçüsü olmaz.</p>")

    g.append("<h2>Neyi yapmıyoruz</h2>")
    g.append("<p>Hesabı görmeden rakam vermiyoruz — “maliyeti yarıya indiririz” "
             "cümlesi hesabın içini görmeden kurulamaz. Harcamanın yüzdesi üzerinden "
             "ücretlendirme yapmıyoruz. Çalışan bir kampanyayı, yerine koyacağımız şey "
             "kanıtlanmadan kapatmıyoruz. Doğruluğunu teyit etmediğimiz fiyat ve vaadi "
             "reklama koymuyoruz. Bütçeniz yönetim bedelini çıkarmıyorsa bunu size "
             "söylüyoruz; iş almak için susmuyoruz.</p>")
    g.append("<p>Bir şeyi daha yapmıyoruz: bütçeyi düşürüp sonucu da düşürerek bunu tasarruf "
             "diye sunmak. Yarı bütçeyle iki kat sonuç medya satın almada olmuyor. "
             "Katlama genellikle medyanın dışında — sitenin dönüşüm oranında, cevaplanmayan "
             "mesajlarda ve hiç üretilmemiş içerikte — duruyor.</p>")

    g.append("<h2>Fiyat</h2>")
    g.append("<p>Denetim tek seferlik ve sabit bedelli. Yönetim aylık; bedeli hesabın "
             "büyüklüğüne ve platform sayısına göre değişiyor. Reklam bütçesi size ait ve "
             "doğrudan platforma ödenir — bizim üstümüzden geçmez. Hangi aralıkta "
             "olduğunuzu ilk görüşmede söylüyoruz; diğer hizmetlerin bantları "
             "<a href=\"../fiyatlar\">fiyat sayfamızda</a> açık yazılı.</p>")
    g.append("</div></section>")
    g.append('<section><div class="wrap prose"><h2>Sık sorulan sorular</h2>%s</div></section>'
             % sss_blok(sss))
    g.append(cta({"slug": "reklam-yonetimi"},
                 "Önce hesabı <i>okuyalım</i>, sonra konuşalım.",
                 "Görüntüleme yetkisi yeterli. Bir haftada nerede kaybettiğinizi yazılı olarak görün."))
    return dosya, _hizmet_kabugu(
        dosya, ad + " | Luna Yapım", aciklama, anahtar,
        "Reklam yönetimi ve <i>reklam denetimi</i>",
        "Google Ads ve Meta. Önce hesabı okuyoruz, sonra kuruyoruz — ve gerçek sonucun "
        "maliyetini ölçüyoruz, tıklamanın değil.",
        "\n".join(g), ad, sss)


# ══════════════════════════════════════════════════════ SOSYAL MEDYA YÖNETİMİ
def sosyal_medya():
    """İçerik üreterek yapılan sosyal medya yönetimi — ajans tarafı değil, kamera tarafı."""
    dosya = "sosyal-medya-yonetimi.html"
    ad = "Sosyal Medya Yönetimi ve Dikey Video Üretimi"
    aciklama = ("Sosyal medya yönetimi: içeriği biz çekiyoruz. Dikey video, paylaşım "
                "takvimi, gelen kutusu düzeni ve reklamla uyumlu yaratıcı üretimi. "
                "Takipçi sayısı değil, iş sonucu konuşuyoruz.")
    anahtar = ("sosyal medya yönetimi, instagram yönetimi, reels üretimi, dikey video, "
               "sosyal medya içerik üretimi, kurumsal sosyal medya ajansı, "
               "sosyal medya paylaşım takvimi, tiktok içerik üretimi")
    sss = [
      ("İçeriği siz mi çekiyorsunuz, ben mi göndereceğim?",
       "Biz çekiyoruz. Asıl işimiz kamera; sosyal medya yönetimini de içerik üretebildiğimiz "
       "için veriyoruz. Saha çekimlerini 81 ilde çözüm ortaklarımızla yapıyoruz, kurgu, renk "
       "ve 3B Bursa'daki ekipte. Elinizde kullanılabilir malzeme varsa onu da değerlendiriyoruz."),
      ("Ayda kaç paylaşım yapılıyor?",
       "Pakete göre değişiyor ama sayıyı hedef olarak koymuyoruz. Haftada üç iyi dikey video, "
       "haftada on dolgu paylaşımından fazla iş getiriyor. Takvimi birlikte kuruyoruz ve "
       "takvimde ne varsa o çekiliyor."),
      ("Takipçi sayımı artırır mısınız?",
       "Takipçi satın almıyoruz ve takipçi sayısı sözü vermiyoruz. Yüz binin üzerinde "
       "takipçisi olan bir hesapta görüntülemelerin yalnız yüzde üçünün takipçilerden "
       "geldiğini ölçtük — yani erişimin neredeyse tamamı satın alınıyordu. Takipçi, "
       "doğru içeriğin yan ürünü oluyor; hedefi olmuyor."),
      ("Yorum ve mesajlara siz mi bakıyorsunuz?",
       "Evet, paketin kapsamındaysa. Bu çoğu hesapta en ucuz kazanç: devraldığımız bir "
       "gelen kutusunda cevaplanmamış yirmi mesaj vardı ve içlerinde doğrudan satın alma "
       "ve bayilik talepleri çıktı. Reklam bütçesi artırmadan önce kapatılacak delik orası."),
      ("Hangi platformlarda çalışıyorsunuz?",
       "Instagram, Facebook, YouTube ve TikTok. Hepsini birden açmayı önermiyoruz; "
       "müşterinizin olduğu yerde iyi olmak, dört yerde vasat olmaktan iyi."),
      ("Reklamla ilişkisi ne?",
       "Ürettiğimiz dikey videolar aynı zamanda reklam yaratıcısı oluyor. Ölçtüğümüz bir "
       "hesapta videolu reklamlar durağan görsellere göre belirgin şekilde ucuza sonuç "
       "üretiyordu ve o hesapta hiç video üretilmiyordu. "
       "<a href=\"reklam-yonetimi\">Reklam yönetimi</a> hizmetiyle birlikte alındığında "
       "aynı çekimden hem paylaşım hem reklam çıkıyor."),
      ("Sözleşme süresi var mı?",
       "Üç ay öneriyoruz, çünkü ilk ay çekim ve kurulumla geçiyor; ama süreyle bağlamıyoruz. "
       "Ayrılırsanız üretilen tüm ham ve kurgulu malzeme sizde kalır."),
    ]
    g = ['<section><div class="wrap prose">']
    g.append("<p>Sosyal medya yönetimi çoğu yerde “paylaşım yapma” işi olarak "
             "satılıyor. Oysa hesabın tıkandığı yer neredeyse hiç takvim değil; "
             "<strong>çekilecek malzemenin olmaması</strong>.</p>")

    g.append("<h2>Ölçtüğümüz üç şey</h2>")
    g.append("<p>Bir hesabı devraldığımızda önce şuna bakıyoruz:</p>")
    g.append("<ul>"
             "<li><strong>Erişiminizin ne kadarı sizin?</strong> Yüz binin üzerinde takipçisi "
             "olan bir hesapta görüntülemelerin %2,6'sı takipçilerden geliyordu. Geri kalanı "
             "reklamla satın alınmıştı. Reklam durduğunda erişim de duruyor demektir.</li>"
             "<li><strong>Geçen hafta kaç paylaşım yapıldı?</strong> Aynı hesapta cevap "
             "sıfırdı — ne video ne gönderi. Platform bunu kendi panelinde uyarı olarak "
             "yazıyordu.</li>"
             "<li><strong>Gelen kutusunda ne birikti?</strong> Yirmi okunmamış mesaj, "
             "içlerinde doğrudan talepler. Bu, reklam bütçesinden önce kapatılacak delik.</li>"
             "</ul>")

    g.append("<h2>İçeriği üretiyoruz, yönetmiyoruz</h2>")
    g.append("<p>Fark burada. Elinizdeki malzemeyi takvime dizmek yönetim değil, arşivi "
             "tüketmektir. Biz kamerayla geliyoruz: tesis, üretim, teslim, ekip, ürün. "
             "Tek çekim gününden haftalarca içerik çıkıyor çünkü plan çekimden önce yapılıyor.</p>")
    g.append("<p>Dikey video standardımız sabit: 1080×1920, 15–25 saniye, yazının kesilmeyeceği "
             "güvenli alan, yakılmış altyazı (sesi kapalı izleniyor), telifsiz müzik. "
             "Her konsept en az üç varyantla üretiliyor — biri tutmazsa diğeri test edilsin diye. "
             "Reklamda kullanılan her fiyat ve vaat, yayına girmeden önce sizin kendi "
             "kaynağınızdan doğrulanıyor.</p>")

    g.append("<h2>Süreç</h2></div><div class=\"wrap\">")
    g.append(_surec([
        ("Hesap okuması", "Erişim nereden geliyor, ne paylaşılmış, gelen kutusunda ne var."),
        ("Konsept ve takvim", "Altı konsept, her birine üç varyant. Takvim yazılı."),
        ("Çekim günü", "Tek günde planın tamamı. Saha ortağı + Bursa ekibi."),
        ("Kurgu ve yayın", "Dikey kurgu, altyazı, kapak. Takvime göre yayına girer."),
        ("Aylık okuma", "Neyin tuttuğu, neyin tutmadığı ve bir sonraki ayın planı."),
    ]))
    g.append('</div><div class="wrap prose">')

    g.append("<h2>Paketler</h2>")
    g.append(_paketler([
        ("Yayın düzeni", "Aylık", [
            "Takvim, metin ve kapak tasarımı",
            "Elinizdeki malzemeden kurgu",
            "Gelen kutusu ve yorum takibi",
            "Aylık okuma raporu"]),
        ("Üretimli yönetim", "Aylık", [
            "Ayda bir çekim günü",
            "Dikey video üretimi ve altyazı",
            "Takvim, yayın ve gelen kutusu",
            "Reklamda kullanılabilir yaratıcı seti"]),
        ("Üretim + reklam", "Aylık", [
            "Üretimli yönetimin tamamı",
            "Google Ads ve Meta yönetimi",
            "Her kampanyada üç yaratıcı testi",
            "Tek rapor: organik ve reklam birlikte"]),
    ]))

    g.append("<h2>Neyi yapmıyoruz</h2>")
    g.append("<p>Takipçi ve etkileşim satın almıyoruz. Takipçi sayısı sözü vermiyoruz. "
             "Stok görseli sizin tesisinizmiş gibi paylaşmıyoruz. Doğrulamadığımız fiyatı "
             "ve vaadi yayınlamıyoruz. Haftalık paylaşım sayısını başarı ölçüsü olarak "
             "raporlamıyoruz — o sayı yükselirken iş sonucunun düştüğü hesaplar gördük. "
             "Bir de şunu yapmıyoruz: her platformu birden açıp hepsini yarım bırakmak.</p>")

    g.append("<h2>Fiyat</h2>")
    g.append("<p>Aylık bedel; çekim günü sayısına, platform sayısına ve gelen kutusunun "
             "yoğunluğuna göre değişiyor. Tek fiyat vermek doğru olmuyor çünkü ayda bir çekim "
             "günü olan bir işletmeyle haftalık çekim gereken bir işletme aynı iş değil. "
             "Hangi aralıkta olduğunuzu ilk görüşmede söylüyoruz; bantlar "
             "<a href=\"../fiyatlar\">fiyat sayfamızda</a>.</p>")
    g.append("</div></section>")
    g.append('<section><div class="wrap prose"><h2>Sık sorulan sorular</h2>%s</div></section>'
             % sss_blok(sss))
    g.append(cta({"slug": "sosyal-medya-yonetimi"},
                 "Hesabınızın <i>kendi</i> erişimi ne kadar?",
                 "Bir bakışta söyleyelim: erişiminiz nereden geliyor, gelen kutunuzda ne bekliyor."))
    return dosya, _hizmet_kabugu(
        dosya, ad + " | Luna Yapım", aciklama, anahtar,
        "Sosyal medya yönetimi — <i>içeriği biz çekiyoruz</i>",
        "Takvim doldurmak değil, çekilecek malzemeyi üretmek. Dikey video, yayın düzeni "
        "ve gelen kutusu; takipçi sayısı değil iş sonucu.",
        "\n".join(g), ad, sss)


# ═══════════════════════════════════════════ PAZAR ARAŞTIRMASI + SATIŞ OTOMASYONU
def pazar_arastirmasi():
    """Hedef kitle bulma, veri toplama, teklif gönderme altyapısı — kendi yazdığımız hat."""
    dosya = "pazar-arastirmasi-otomasyon.html"
    ad = "Pazar Araştırması ve Satış Otomasyonu"
    aciklama = ("Hedef kitlenizi bulan, aday firmaları ölçen ve teklif gönderimini "
                "otomatikleştiren altyapı. Kendi yazdığımız hat; kiraladığımız araç değil. "
                "KVKK ve ticari ileti kurallarına uygun.")
    anahtar = ("pazar araştırması, satış otomasyonu, potansiyel müşteri bulma, "
               "lead generation, b2b müşteri listesi, rakip analizi, arama hacmi analizi, "
               "otomatik teklif gönderme, crm otomasyonu, veri toplama yazılımı")
    sss = [
      ("Bu bir hazır araç mı, yoksa yazılım mı yazıyorsunuz?",
       "Yazılım yazıyoruz. Hat bizim: aday firma bulma, eksik tespiti, puanlama, rapor ve "
       "teklif üretimi tek akışta çalışıyor. Bunu önce kendi satışımız için kurduk ve hâlâ "
       "kendimiz kullanıyoruz; size kurduğumuz da aynı hat oluyor."),
      ("Hangi verileri topluyorsunuz?",
       "Firmaların kamuya açık dijital izini: web sitesi, sayfa hızı, eksik etiketler, "
       "video olup olmaması, işletme profili, sosyal hesaplar ve arama görünürlüğü. "
       "Kişisel veri kazımıyoruz; hedefimiz kişi değil firma."),
      ("Toplu e-posta ve mesaj göndermek yasal mı?",
       "Tacir ve esnafa ticari elektronik ileti göndermek için önceden onay aranmıyor; ancak "
       "iletişim adreslerinin İleti Yönetim Sistemi'ne kaydedilmesi ve her iletide ret "
       "hakkının açık tutulması gerekiyor. Kurduğumuz akış buna göre çalışıyor: ret gelen "
       "adres aynı gün listeden düşüyor. Tüketiciye yönelik gönderimde önceden onay şart ve "
       "o tarafta onaysız gönderim kurmuyoruz."),
      ("Ne kadar sürede liste çıkıyor?",
       "Sektör ve bölge belliyse ilk liste birkaç gün içinde çıkıyor. Asıl zaman listeyi "
       "temizlemekte ve puanlamada geçiyor; ham liste işe yaramıyor, sıralanmış liste yarıyor."),
      ("Bize teslim ettikten sonra kullanabilir miyiz?",
       "Evet. Hat sizin sunucunuzda ya da bilgisayarınızda çalışacak şekilde kuruluyor ve "
       "kaynak kod sizde kalıyor. Aylık bakım isteğe bağlı."),
      ("Pazar araştırması kısmında tam olarak ne veriyorsunuz?",
       "İnsanların ne aradığını, hangi aramalarda göründüğünüz hâlde tıklanmadığınızı, "
       "rakiplerin hangi sorularda önde olduğunu ve hiç sayfası olmayan talep kümelerini. "
       "Çıktı, yazılacak sayfaların listesi oluyor — tahmin değil, ölçülmüş eksik."),
    ]
    g = ['<section><div class="wrap prose">']
    g.append("<p>Satışın en pahalı kısmı, kime gideceğini bilmemek. Çoğu firma bu soruyu "
             "sezgiyle cevaplıyor ve listeyi elle topluyor; haftalar gidiyor, liste "
             "eskiyor.</p>")

    g.append("<h2>Üç parçası var</h2>")
    g.append("<ul>"
             "<li><strong>Aday bulma.</strong> Sektör ve bölge verdiğinizde firmaları "
             "topluyoruz; isim, iletişim ve dijital iz birlikte geliyor.</li>"
             "<li><strong>Eksik tespiti ve puanlama.</strong> Her firmanın sitesi ölçülüyor: "
             "hız, eksik etiket, video var mı, işletme profili doğru mu, arama görünürlüğü ne. "
             "Puan, kimin size ihtiyacı olduğunu sıralıyor.</li>"
             "<li><strong>Teklif üretimi.</strong> Yüksek puanlı aday için firmaya özel rapor "
             "ve teklif çıkıyor; gönderim takibi aynı hatta.</li>"
             "</ul>")
    g.append("<p>Bu üçü bir arada olmayınca işe yaramıyor. Ham liste satış yapmıyor; "
             "<em>sıralanmış</em> liste yapıyor.</p>")

    g.append("<h2>Pazar araştırması tarafı</h2>")
    g.append("<p>İkinci kullanım alanı kendi pazarınızı okumak. Devraldığımız bir sitede "
             "arama verisini dışa aktardık: 931 sorgunun <strong>380'i gösterim alıyor, "
             "tık almıyordu</strong>. Yani insanlar o konuyu arıyor, siteyi görüyor, "
             "tıklamıyordu. İçlerinde iki talep kümesinin karşılığı olan <em>hiçbir sayfa "
             "yoktu</em>; o sayfalar yazıldı.</p>")
    g.append("<p>Bunun tahminle bulunması mümkün değil. Arama verisi, otomatik tamamlama ve "
             "rakiplerin sıralandığı sorular birlikte okununca eksikler listeye dönüşüyor: "
             "hangi sayfa yazılacak, hangi başlık değişecek, hangi soruya cevap verilmemiş.</p>")

    g.append("<h2>Süreç</h2></div><div class=\"wrap\">")
    g.append(_surec([
        ("Hedef tanımı", "Kime satıyorsunuz, hangi bölgede, hangi büyüklükte."),
        ("İlk liste", "Aday firmalar toplanır; liste ham hâliyle size gösterilir."),
        ("Ölçüm ve puan", "Her aday ölçülür, puanlanır ve sıralanır."),
        ("Teklif akışı", "Rapor ve teklif şablonu kurulur; ret yönetimi dahil."),
        ("Devir", "Hat sizde çalışır hâlde kalır; kaynak kod teslim edilir."),
    ]))
    g.append('</div><div class="wrap prose">')

    g.append("<h2>Paketler</h2>")
    g.append(_paketler([
        ("Pazar raporu", "Tek seferlik", [
            "Arama verisi ve rakip okuması",
            "Gösterim alıp tık almayan sorgular",
            "Karşılığı olmayan talep kümeleri",
            "Yazılacak sayfa listesi"]),
        ("Aday listesi", "Tek seferlik", [
            "Sektör ve bölgeye göre firma listesi",
            "Dijital iz ölçümü ve puanlama",
            "Sıralanmış, temizlenmiş liste"]),
        ("Çalışan hat", "Kurulum + isteğe bağlı bakım", [
            "Aday bulma, ölçme, puanlama",
            "Firmaya özel rapor ve teklif üretimi",
            "Ret yönetimi ve kayıt",
            "Kaynak kod sizde kalır"]),
    ]))

    g.append("<h2>Neyi yapmıyoruz</h2>")
    g.append("<p>Kişisel veri kazımıyoruz ve satın alınmış hazır listelerle çalışmıyoruz. "
             "Tüketiciye onaysız ticari ileti gönderen bir akış kurmuyoruz. Ret hakkını "
             "gizleyen, çıkışı zorlaştıran şablon yazmıyoruz. Sosyal ağların kullanım "
             "şartlarını ihlal eden otomasyon kurmuyoruz. Ve “garantili müşteri” "
             "sözü vermiyoruz — hat doğru adayı bulur, satışı siz yaparsınız.</p>")

    g.append("<h2>Fiyat</h2>")
    g.append("<p>Pazar raporu ve aday listesi tek seferlik, kapsamına göre fiyatlanıyor. "
             "Çalışan hat kurulum bedeli + isteğe bağlı aylık bakım. Sektörünüzü ve hedef "
             "bölgenizi yazın, aynı gün net bir aralık verelim; bantlar "
             "<a href=\"../fiyatlar\">fiyat sayfamızda</a>.</p>")
    g.append("</div></section>")
    g.append('<section><div class="wrap prose"><h2>Sık sorulan sorular</h2>%s</div></section>'
             % sss_blok(sss))
    g.append(cta({"slug": "pazar-arastirmasi-otomasyon"},
                 "Kime satacağınızı <i>tahmin</i> etmeyin.",
                 "Sektörünüzü ve bölgenizi yazın; ilk aday listesinin neye benzeyeceğini gösterelim."))
    return dosya, _hizmet_kabugu(
        dosya, ad + " | Luna Yapım", aciklama, anahtar,
        "Pazar araştırması ve <i>satış otomasyonu</i>",
        "Hedef kitlenizi bulan, aday firmaları ölçüp sıralayan ve teklif gönderimini "
        "otomatikleştiren altyapı — kendi yazdığımız hat.",
        "\n".join(g), ad, sss)


SAYFALAR = [reklam_yonetimi, sosyal_medya, pazar_arastirmasi]


def yayinla(kok):
    d = os.path.join(kok, "hizmetler")
    os.makedirs(d, exist_ok=True)
    yazilan = []
    for f in SAYFALAR:
        dosya, html = f()
        with open(os.path.join(d, dosya), "w", encoding="utf-8") as y:
            y.write(html)
        yazilan.append(dosya)
    return {"ajans_hizmetleri": len(yazilan), "dosyalar": yazilan}


if __name__ == "__main__":
    import sys
    print(yayinla(sys.argv[1] if len(sys.argv) > 1 else "."))
