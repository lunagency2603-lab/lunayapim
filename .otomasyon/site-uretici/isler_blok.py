# -*- coding: utf-8 -*-
"""
İŞ BLOĞU — hizmet sayfalarına "bu alandaki işimiz" kanıtı (13.10.2026)

Sahibinin sözü: "yaptığımız her şeyi gerçek iş olarak sayfalara koy; koymak zorunda
değilsek müşteri ismini gizle." Buradaki her kayıt gerçekten yapılmış ve kontrol
edilmiş bir iştir; rakamlar ölçülmüş değerlerdir (kaynak: Search Console dışa
aktarımı, PageSpeed, Meta/Google Ads CSV, kendi üretim kayıtlarımız). Uydurma
kayıt eklenmez; müşteri adı yalnız yayında olan ve adı zaten açık işlerde geçer,
reklam/analiz işlerinde firma tanınmaz.

İki parça üretir:
  kartlar(ids)  → .uv-izgara içinde görselli kartlar (luna.css'teki .uv bileşeni)
  rakamlar(ids) → .vk-rakam ölçü kutuları (yeni; luna.css v27)
  blok(slug)    → sayfaya göre ikisini birleştirir: SAYFA sözlüğünden okur

Kullanım: sektor_sayfalari / sektor_dijital / ajans_hizmetleri / yeni_hizmetler
_govde içinden `from isler_blok import blok` → blok("insaat-3d-villa")
Yollar hizmetler/ altındaki sayfalara göre ("../assets/…").
"""
from uretici import e

# --------------------------------------------------------------- İŞ KAYITLARI
IS = {
"aktas-3b": dict(
    baslik="Aktaş Prefabrik — 3B ev tasarlayıcı", rom="Prefabrik ev üreticisi · Sakarya",
    etiket="Canlı", gorsel="video/aktas-3b-tasarlayici.jpg",
    alt="Aktaş Prefabrik 3B ev tasarlayıcısı: çift katlı 3+1 model, dış görünüm",
    href="../isler/aktas-prefabrik-3b-ev-tasarlayici", ok="İşi incele →",
    metin="Firmanın 40 modelinin ölçülü kat planı tarayıcıda eve dönüşüyor. Ziyaretçi kat, oda "
          "düzeni, cephe, çatı ve terası seçiyor; evin içinde yürüyor, gece görünümüne geçiyor. "
          "Yanında seçime en yakın model ve liste fiyatı.",
    rakam=[("40", "model, gerçek kat planından"), ("321", "oda ölçüsüyle kuruldu"),
           ("100", "mobil hız puanı (Lighthouse)")]),
"aktas-montaj": dict(
    baslik="Aktaş Prefabrik — 3B montaj filmi", rom="Prefabrik ev üreticisi · Sakarya",
    etiket="Video", gorsel="video/aktas-montaj.jpg",
    alt="3B montaj filminden kare: teslim edilmiş prefabrik ev",
    href="../isler/aktas-prefabrik-3b-montaj-filmi", ok="Filmi izle →",
    metin="Arsadan teslime yedi aşama 4K karelerle modellendi ve tek kadrajda birbirine "
          "bağlandı; ev kendi kendine kuruluyor. Tasarlayıcıyla aynı 3B modelden üretildi.",
    rakam=[("7", "aşama: arsa → teslim"), ("4K", "kare çözünürlüğü"), ("10 sn", "açılış filmi")]),
"aktas-site": dict(
    baslik="Aktaş Prefabrik — web sitesi, SEO ve ölçüm", rom="Prefabrik ev üreticisi · Sakarya",
    etiket="Canlı", gorsel="web/aktas-site.jpg",
    alt="aktasprefabrikev.com ana sayfası: fabrika görüntüsü ve model vitrini",
    href="seo-ornegi-aktas-prefabrik", ok="Ölçülen sonuçlar →",
    metin="WordPress'ten statik yapıya taşındı; 380'den fazla sayfa, Türkçe-İngilizce-Almanca. "
          "Mobil hız 72'den 100'e; 28 günde aramadan gelen tıklama üç katına çıktı. Telefon, "
          "WhatsApp ve form ayrı ayrı sayılıyor.",
    rakam=[("72 → 100", "mobil PageSpeed"), ("×3", "28 günde organik tıklama (203 → 616)"),
           ("380+", "sayfa · 3 dil")]),
"ata-kumas": dict(
    baslik="Ata Kumaş — vitrin, sanal mağaza, yönetim paneli", rom="Kumaş toptancısı · Bursa",
    etiket="Canlı", gorsel="video/atakumas-sanal-magaza.jpg",
    alt="Ata Kumaş sanal mağazası: duvarlarda asılı kumaşlar, koridor görünümü",
    href="../isler/ata-kumas-sanal-magaza-ve-manken", ok="İşi incele →",
    metin="Trendyol kataloğu siteye taşındı; müşteri mağazanın içinde geziyor, kumaşı kadın ve "
          "erkek mankenin üzerinde görüyor. Satış, stok ve maliyet paneli; depodan Telegram'a "
          "atılan fotoğraf onayla ürün oluyor.",
    rakam=[("31", "ürün, 27 kumaş dokusu"), ("3B", "mağaza turu + manken"),
           ("0 ₺", "aylık sunucu gideri")]),
"galzura": dict(
    baslik="Galzura — tanıtım animasyonu ve site", rom="Filo yönetim yazılımı · Avusturya",
    etiket="Video", gorsel="video/ornek-galzura.jpg",
    alt="Galzura tanıtım animasyonundan kare: canlı araç takip ekranı",
    href="../isler/galzura-tanitim-animasyonu", ok="Animasyonu izle →",
    metin="Lojistik firmalarına satılan filo yazılımı için 1 dakikalık tanıtım animasyonu; "
          "Türkçe ve Almanca seslendirme, yatay ve dikey sürüm. galzura.com'un bakımı ve "
          "pazarlaması da bizde.",
    rakam=[("TR · DE", "iki dil, tek kurgu"), ("13", "ürün ekranı sahnesi"), ("16:9 + 9:16", "site ve sosyal sürüm")]),
"cm": dict(
    baslik="CM Vorarlberg — konut projesi 3D animasyonu", rom="Konut geliştiricisi · Avusturya",
    etiket="Video", gorsel="video/ornek-cm.jpg",
    alt="CM Vorarlberg konut projesi 3D animasyonundan dış cephe karesi",
    href="../isler/cm-vorarlberg-konut-projesi-3d-animasyon", ok="Animasyonu izle →",
    metin="Projenin dış cephesi modellenip render edildi; yapının çevresinde dolaşan tek plan "
          "ve marka kapanışı. Satış ofisi açılmadan projenin görünür hâle gelmesi için.",
    rakam=None),
"bgk": dict(
    baslik="Buhar geri kazanım sistemi — teknik eğitim animasyonu", rom="Akaryakıt sektörü · demo",
    etiket="Video", gorsel="video/bgk-egitim-demo.jpg",
    alt="BGK eğitim animasyonundan kare: tank kesiti ve buhar hattı",
    href="../isler/buhar-geri-kazanim-egitim-animasyonu", ok="Animasyonu izle →",
    metin="Faz I ve Faz II çalışma ilkesi 30 saniyede: tanker boşaltımı, tank kesitinde seviye, "
          "dispenser içindeki akış. Bir petrol şirketinin eğitim talebi için hazırlanan demo.",
    rakam=None),
"yade": dict(
    baslik="YADE × Vogue — 3D animasyon klip", rom="Kendi maskotumuz · müzik klibi",
    etiket="Video", gorsel="video/yade-vogue.jpg",
    alt="YADE karakteri: bazalt sütunlar arasında siyah tüylü ejderha",
    href="../isler/yade-vogue-3d-animasyon-klip", ok="Klibi izle →",
    metin="Kliplerimizin sanatçısı olarak tasarladığımız YADE karakteri: silüet, malzeme ve "
          "hareket dili önce kâğıtta, sonra Blender'da. 2:40'lık klip beş dünyada geçiyor; "
          "kurgu şarkının vuruşlarına göre biçildi.",
    rakam=[("2:40", "klip süresi"), ("5", "dünya, hepsi 3B"), ("4K", "teslim")]),
"karga": dict(
    baslik="Karga — Luna Yapım'ın kendi karakteri", rom="Marka karakteri · 6 bölümlük seri",
    etiket="Video", gorsel="video/karga-k1.jpg",
    alt="Karga serisinden kare: dalda karga silüeti, altın saat",
    href="../studyo", ok="Seriyi izle →",
    metin="Logodaki karga altı kısa bölümde canlandırıldı; ana sayfamızın açılış filmi bu "
          "seriden. Dikey sürümleri sosyal medya için hazır, karakter her bölümde aynı.",
    rakam=None),
"evliya": dict(
    baslik="Evliya Çelebi Soruyor — 1. bölüm", rom="Yapay zekâ kısa film · sokak röportajı formatı",
    etiket="Video", gorsel="video/evliya-soruyor-b1.jpg",
    alt="Evliya Çelebi Soruyor: mikrofonlu Evliya Çelebi Bursa sokağında",
    href="../isler/evliya-celebi-soruyor-1-bolum", ok="Bölümü izle →",
    metin="Karakter sayfaları, Türkçe seslendirme ve telaffuz denetimiyle 23 saniyelik dikey "
          "bölüm. Kamu malı karakterler, gerçek hayattan bir sahne hissi; seri formatı.",
    rakam=None),
"pusula": dict(
    baslik="Luna Pusula — hedef kitle ve teklif hattı", rom="Kendi yazılımımız · satış altyapısı",
    etiket="Yazılım", gorsel="urun/pusula.jpg",
    alt="Luna Pusula paneli: aday firma listesi ve puanlar",
    href="../yazilim", ok="Yazılımı gör →",
    metin="Firmaları kendi yayınladıkları sayfalardan bulur, eksiklerini kanıtla ölçer, "
          "puanlar; arama listesi, takip tarihi ve teklif belgesi tek panelde. Son hedef "
          "listesi: 56 firma, bir gecede.",
    rakam=[("56", "firma puanlanıp sıralandı"), ("2 iş günü", "sonra otomatik takip"),
           ("0", "satın alınan veri — hepsi açık kaynak")]),
"trendyol": dict(
    baslik="Trendyol otomasyonu — fotoğraftan ürün", rom="Kendi yazılımımız · pazaryeri",
    etiket="Yazılım", gorsel="urun/trendyol.jpg",
    alt="Trendyol otomasyonu: ürün fotoğrafından açıklama ve görsel üretimi",
    href="../yazilim", ok="Yazılımı gör →",
    metin="Ürün fotoğrafından açıklama, çoklu görsel ve barkod üretip Satıcı API ile mağazaya "
          "yüklüyor. Ata Kumaş'ta aynı hat Telegram botuyla depodan siteye çalışıyor.",
    rakam=None),
"trendsaphiens": dict(
    baslik="TrendSaphiens — kendi yayınımız", rom="Günlük yayın · editör onaylı",
    etiket="Canlı", gorsel="urun/trendsaphiens.jpg",
    alt="TrendSaphiens ana sayfası",
    href="seo-ornegi-trendsaphiens", ok="Örneği gör →",
    metin="Günlük veri toplayan, yazan ve editör onayından sonra yayınlayan sistem; yeni alan "
          "adında ilk haftaların dizin yolculuğu açık yazılı.",
    rakam=None),
}

# --------------------------------------------------------------- SAYFA → BLOK
SAYFA = {
"insaat-3d-modelleme": dict(baslik="Bu alandaki işlerimiz", kartlar=["aktas-3b", "aktas-montaj", "cm"],
    aciklama="Üçü de teslim edilmiş iş; ilki şu an yayında, tıklayıp deneyebilirsiniz."),
"insaat-3d-konut-projesi": dict(baslik="Konut projelerinde yaptıklarımız", kartlar=["aktas-3b", "cm", "aktas-montaj"],
    aciklama="Kat planından kurulan ev, dış cephe animasyonu ve montaj filmi — üçü de gerçek proje."),
"insaat-3d-villa": dict(baslik="Villa ve müstakil evde yaptıklarımız", kartlar=["aktas-3b", "aktas-montaj", "cm"],
    aciklama="Müstakil evde alıcı önce kendi evini görmek istiyor; tasarlayıcı tam bunun için kuruldu."),
"insaat-3d-otel": dict(baslik="Aynı motorla yaptıklarımız", kartlar=["aktas-3b", "cm"],
    aciklama="Otel projesi için ayrı örneğimiz henüz yok; konut tarafında kurduğumuz iş akışı aynı."),
"insaat-3d-ticari-avm": dict(baslik="Aynı motorla yaptıklarımız", kartlar=["cm", "aktas-3b"],
    aciklama="Ticari yapı için ayrı örneğimiz henüz yok; dış cephe animasyonu ve 3B gezinti aynı araçlarla kuruluyor."),
"insaat-3d-kentsel-donusum": dict(baslik="Aynı motorla yaptıklarımız", kartlar=["aktas-3b", "aktas-montaj"],
    aciklama="Hak sahibine daireyi göstermek için kurduğumuz araç, prefabrik evde çalışan tasarlayıcının kendisi."),
"sanal-tur": dict(baslik="Yayında olan iki sanal tur", kartlar=["aktas-3b", "ata-kumas"],
    aciklama="İkisi de canlı; tıklayıp içinde gezebilirsiniz. Telefonda da çalışıyor."),
"sanal-showroom": dict(baslik="Yayında olan showroom işlerimiz", kartlar=["ata-kumas", "aktas-3b"],
    aciklama="Bir kumaş mağazası ve bir prefabrik ev üreticisi; ikisi de şu an müşterilerine açık."),
"sanal-showroom-ev-tekstili-kumas": dict(baslik="Kumaşta yaptığımız iş", kartlar=["ata-kumas"],
    aciklama="Aynı mağazanın kataloğu pazaryerinden siteye, siteden mankenin üzerine taşındı."),
"sanal-showroom-konut-projesi": dict(baslik="Konutta yaptığımız iş", kartlar=["aktas-3b", "aktas-montaj"],
    aciklama="Alıcı daireyi değil, kendi seçimlerini görüyor; satış ofisine bu seçimle geliyor."),
"sanal-showroom-mobilya": dict(baslik="Aynı motorla kurduğumuz vitrinler", kartlar=["ata-kumas", "aktas-3b"],
    aciklama="Mobilya için ayrı örneğimiz henüz yok; kumaş dokusunu mankene giydiren ve evi odadan kuran iki iş aynı altyapıda."),
"sanal-showroom-otomotiv-galerisi": dict(baslik="Aynı motorla kurduğumuz vitrinler", kartlar=["aktas-3b", "ata-kumas"],
    aciklama="Oto galeri için ayrı örneğimiz henüz yok; 3B gezinti ve ürün döndürme aynı altyapıyla kuruluyor."),
"sanal-showroom-seramik-banyo": dict(baslik="Aynı motorla kurduğumuz vitrinler", kartlar=["aktas-3b", "ata-kumas"],
    aciklama="Seramik için ayrı örneğimiz henüz yok; tasarlayıcıdaki zemin ve fayans seçimi aynı mantıkla çalışıyor."),
"sanal-showroom-aydinlatma": dict(baslik="Aynı motorla kurduğumuz vitrinler", kartlar=["aktas-3b", "ata-kumas"],
    aciklama="Aydınlatma için ayrı örneğimiz henüz yok; tasarlayıcının gece görünümü ışığı sahnede gösteriyor."),
"urun-animasyon": dict(baslik="Ürün ve sistem animasyonlarımız", kartlar=["bgk", "galzura", "yade"],
    aciklama="Teknik eğitim, yazılım tanıtımı ve karakter animasyonu — üçü de bizim kurgumuz."),
"urun-animasyon-makine-imalati": dict(baslik="Teknik anlatımda yaptıklarımız", kartlar=["bgk", "galzura"],
    aciklama="Kapalı bir sistemin içini kesitle anlatmak: buhar hattı için yaptığımızı makine için de yapıyoruz."),
"urun-animasyon-insaat-malzemesi": dict(baslik="Yapı ürünlerinde yaptıklarımız", kartlar=["aktas-montaj", "aktas-3b"],
    aciklama="Panel, iskelet ve çatının nasıl birleştiği montaj filminde; malzeme seçimi tasarlayıcıda."),
"urun-animasyon-mobilya": dict(baslik="Aynı araçlarla yaptıklarımız", kartlar=["ata-kumas", "yade"],
    aciklama="Kumaşı 3B mankene giydiren vitrin ve karakter animasyonu aynı modelleme hattından çıkıyor."),
"urun-animasyon-ambalaj": dict(baslik="Aynı araçlarla yaptıklarımız", kartlar=["bgk", "galzura"],
    aciklama="Ambalaj için ayrı örneğimiz henüz yok; kesit ve süreç anlatımını iki işte görebilirsiniz."),
"urun-animasyon-medikal": dict(baslik="Aynı araçlarla yaptıklarımız", kartlar=["bgk", "galzura"],
    aciklama="Medikal için ayrı örneğimiz henüz yok; kullanım adımlarını sırayla anlatan kurgu BGK işindeki gibi."),
"urun-animasyon-gida": dict(baslik="Aynı araçlarla yaptıklarımız", kartlar=["bgk", "galzura"],
    aciklama="Gıda için ayrı örneğimiz henüz yok; üretim hattı anlatımı aynı kurguyla kuruluyor."),
"urun-animasyon-otomotiv-yan-sanayi": dict(baslik="Aynı araçlarla yaptıklarımız", kartlar=["bgk", "galzura"],
    aciklama="Otomotiv için ayrı örneğimiz henüz yok; parça ve akış anlatımı BGK animasyonundaki yöntemle."),
"urun-animasyon-tarim-makineleri": dict(baslik="Aynı araçlarla yaptıklarımız", kartlar=["bgk", "galzura"],
    aciklama="Tarım makinesi için ayrı örneğimiz henüz yok; çalışma ilkesi anlatımı aynı."),
"animasyon-teknik-egitim-isg": dict(baslik="Teknik eğitimde yaptığımız iş", kartlar=["bgk", "galzura"],
    aciklama="Eğitim animasyonunda her adım aynı sırayla, her izleyicide aynı; BGK demosu tam bu kurgu."),
"animasyon-enerji-isi-sistemleri": dict(baslik="Enerji sistemlerinde yaptığımız iş", kartlar=["bgk", "aktas-montaj"],
    aciklama="Buhar geri kazanım hattı için hazırladığımız animasyon; akış yönü ve çalışma ilkesi tek videoda."),
"animasyon-maskot-karakter": dict(baslik="Tasarladığımız karakterler", kartlar=["yade", "karga", "evliya"],
    aciklama="Üçü de bizim: bir ejderha, bir karga ve bir sokak röportajı kadrosu."),
"web-sitesi-tasarimi": dict(baslik="Müşteri işleri", kartlar=["aktas-3b", "ata-kumas", "aktas-site"],
    aciklama="Üçü de çalışır hâlde; tıklayıp açabilirsiniz."),
"web-sitesi-insaat-ve-yapi-firmalari": dict(baslik="İnşaatta yaptığımız iş", kartlar=["aktas-site", "aktas-3b", "aktas-montaj"],
    aciklama="Site, tasarlayıcı ve açılış filmi aynı firma için; rakamlar ölçüldü."),
"web-sitesi-uretici-firmalar": dict(baslik="Üreticilerde yaptığımız iş", kartlar=["ata-kumas", "galzura", "aktas-site"],
    aciklama="Kumaş toptancısı, yazılım üreticisi ve prefabrik ev üreticisi — üçü de yayında."),
"web-sitesi-saglik-denetimi": dict(baslik="Denetimle başlayan işler", kartlar=["aktas-site", "trendsaphiens"],
    aciklama="Önce ölçtük, sonra düzelttik; rakamlar örnek sayfalarında açık."),
"seo-icerik": dict(baslik="SEO'da ölçülmüş işler", kartlar=["aktas-site", "trendsaphiens"],
    aciklama="Kendi sitemizin dizin yolculuğu da örnek sayfasında."),
"yapay-zeka-seo": dict(baslik="Yapay zekâ aramasına hazırladığımız siteler", kartlar=["aktas-site", "trendsaphiens"],
    aciklama="Yapılandırılmış veri, llms.txt ve firma varlığı — ikisinde de kurulu."),
"e-ticaret": dict(baslik="E-ticarette yaptıklarımız", kartlar=["ata-kumas", "trendyol"],
    aciklama="Pazaryerinden siteye taşınan katalog ve fotoğraftan ürün yükleyen hat."),
"pazar-arastirmasi-otomasyon": dict(baslik="Kendi hattımız", kartlar=["pusula", "trendyol"],
    aciklama="Önce kendi satışımız için yazdık; aynı hattı müşteriye kuruyoruz."),
"reklam-yonetimi": dict(baslik="Reklamla birlikte ürettiklerimiz", kartlar=["aktas-site", "aktas-3b"],
    aciklama="Reklam bütçesinin gittiği site ve o sitedeki dönüşüm aracı — ikisi de bizim işimiz."),
"sosyal-medya-yonetimi": dict(baslik="Sosyal medya için ürettiklerimiz", kartlar=["yade", "karga", "evliya"],
    aciklama="Firma arşivinden kurgu Reels'ler aşağıda; karakterli içerikler burada."),
"isletme-tanitim": dict(baslik="İşletmeler için yaptıklarımız", kartlar=["aktas-site", "ata-kumas"],
    aciklama="Tanıtım filmiyle birlikte sitenin ve vitrinin de kurulduğu iki iş."),
"drone-fpv": dict(baslik="Havadan görüntünün gittiği yer", kartlar=["aktas-site", "cm"],
    aciklama="Drone çekimini tek başına değil, gideceği site ve projeyle birlikte planlıyoruz."),
"ai-kisa-film": dict(baslik="Yapay zekâ ile ürettiklerimiz", kartlar=["evliya", "yade", "karga"],
    aciklama="Karakter tutarlılığı ve Türkçe seslendirme — üç işte de çözüldü."),
}

# --------------------------------------------------------------- ÜRETİM
def _kart(k, on):
    v = IS[k]
    dis = v["href"].startswith("http")
    return ('<a class="uv" href="%s"%s><span class="uv-gorsel">'
            '<img src="%sassets/%s" width="800" height="500" loading="lazy" alt="%s">'
            '<i class="uv-yz">%s</i></span><span class="uv-metin"><span class="rom">%s</span>'
            '<h3>%s</h3><p>%s</p><span class="ok">%s</span></span></a>'
            % (v["href"] if dis or v["href"].startswith("../") else v["href"],
               ' rel="noopener" target="_blank"' if dis else "",
               on, v["gorsel"], e(v["alt"]), e(v["etiket"]), e(v["rom"]),
               e(v["baslik"]), e(v["metin"]), e(v["ok"])))


def kartlar(ids, on="../"):
    return '<div class="uv-izgara">%s</div>' % "".join(_kart(k, on) for k in ids if k in IS)


def rakamlar(ids):
    """Kartlardaki ölçülmüş rakamlar tek şeritte — ilk kartın rakamları öncelikli."""
    r = []
    for k in ids:
        for sayi, etiket in (IS.get(k, {}).get("rakam") or []):
            if len(r) < 4:
                r.append((sayi, etiket))
    if not r:
        return ""
    return '<div class="vk-rakam">%s</div>' % "".join(
        '<div class="vk"><b>%s</b><span>%s</span></div>' % (e(s), e(t)) for s, t in r)


def blok(slug, on="../", rakam=True):
    v = SAYFA.get(slug)
    if not v:
        return ""
    ids = [k for k in v["kartlar"] if k in IS]
    return ('<section class="acik" data-is-blok>\n  <div class="wrap">\n'
            '    <div class="bas"><span class="no">✓</span><div><h2>%s</h2>'
            '<p class="aciklama">%s</p></div></div>\n    %s\n    %s\n  </div>\n</section>\n'
            % (e(v["baslik"]), e(v["aciklama"]), rakamlar(ids) if rakam else "", kartlar(ids, on)))


def gorseller():
    """Denetim için: kullanılan görsellerin assets altındaki yolları."""
    return sorted({v["gorsel"] for v in IS.values()})
