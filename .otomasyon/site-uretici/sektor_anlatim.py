# -*- coding: utf-8 -*-
"""Sektöre özel anlatım cümleleri — her ilin kendi sektör listesinden üretilir."""

KURAL = [
 (("otomotiv","yedek parça"), "Otomotiv yan sanayide parçanın montaj sırasını ve dayanım davranışını gösteren animasyon, ana sanayi görüşmelerinde teknik anlatımı kısaltıyor."),
 (("tekstil","iplik","konfeksiyon","kumaş","havlu","battaniye","ev tekstili","dokuma"), "Tekstilde kumaş dokusunu, örgü yapısını ve renk varyantlarını yakın planda gösteren 3D anlatım, numune göndermeden karar verdiriyor."),
 (("mobilya",), "Mobilyada modül seçenekleri ve renk varyantları bir kez modellenip sonsuz varyantta gösteriliyor; her varyant için ayrı fotoğraf çekiminden belirgin şekilde ucuza geliyor."),
 (("makine","otomasyon","imalat","tarım makineleri","değirmen","demiryolu araçları"), "Makine imalatında gövdeyi şeffaflaştırıp içerideki hareketi gösteren kesit animasyonu, teknik satışta müşterinin \"anladım\" dediği an oluyor."),
 (("gıda","süt","peynir","fındık","zeytin","kayısı","meyve","un ","şeker","konserve","bal","çay","fıstık","bisküvi","et ","kaşar","pestil","incir","narenciye","yer fıstığı","ceviz","elma","pirinç","sarımsak","kuru üzüm","yem"), "Gıda üretiminde hammaddeden pakete uzanan süreç animasyonu, zincir market ve ihracat görüşmelerinde izlenebilirlik anlatımını tek karede veriyor."),
 (("mermer","doğal taş","traverten","taş işleme","ahlat taşı"), "Mermer ve doğal taşta damar desenini ve plaka ölçüsünü gerçekçi gösteren 3D vitrin, yurt dışı alıcıya numune öncesi karar verdiriyor."),
 (("seramik","porselen","çini","cam","refrakter","kaolen"), "Seramik ve cam ürünlerde yüzey dokusunu ve uygulama sürecini gösteren animasyon, mimar ve bayi kanalında doğrudan satış aracına dönüşüyor."),
 (("kimya","petrokimya","plastik","boya","lastik","gübre","petrol","rafinaj"), "Kimya ve plastik üretiminde gizlilik nedeniyle çekim yapılamayan bölümler 3D ile anlatılıyor: süreç görünüyor, tesis görünmüyor."),
 (("medikal","laboratuvar","tıbbi"), "Medikal cihazlarda kullanım adımlarını ve hijyen sürecini gösteren animasyon, satış temsilcisi olmadan da doğru anlatımı garanti ediyor."),
 (("savunma","havacılık","raylı"), "Savunma ve havacılık tedarikinde gizlilik sınırları içinde kalan kesit ve montaj animasyonu, ihale sunumlarının standart parçası."),
 (("demir","çelik","metal","döküm","kalıp","haddehane","çelik kapı","bakırcılık"), "Demir-çelik ve metal işlemede tesis ölçeğini ve süreç akışını gösteren animasyon, yatırımcı ve ihale sunumlarında kullanılıyor."),
 (("madencilik","kömür","bor","krom","bakır","tuz","enerji","jeotermal"), "Madencilik ve enerji yatırımlarında saha ölçeğini ve galeri yapısını gösteren 3D anlatım, izin ve yatırımcı süreçlerini hızlandırıyor."),
 (("tarım","seracılık","pamuk","bağcılık","şarap","hayvancılık","arıcılık","fidancılık","süs bitki"), "Tarım ve hayvancılıkta üretim döngüsünü anlatan animasyon, coğrafi işaretli ürünü taklitten ayıran en somut materyal."),
 (("turizm","otel","konaklama","termal"), "Turizm tesislerinde henüz yapılmamış bölümleri 3D ile tamamlayıp mevcut kısımları gerçek çekimle birleştiriyoruz."),
 (("lojistik","liman","sınır ticareti"), "Lojistik ve liman hizmetlerinde fiziksel ürün yok; süreç animasyonu taşıma, gümrük ve depolama akışını müşteriye tek videoda anlatıyor."),
 (("yazılım","teknoloji","fintek"), "Yazılım ve teknoloji şirketlerinde arayüz ve veri akışını izometrik sahnelerle anlatan süreç animasyonu, demo toplantısını kısaltıyor."),
 (("inşaat malzemesi","çimento","tuğla","kiremit","yalıtım"), "İnşaat malzemesinde uygulama adımlarını ve katman kesitini gösteren animasyon, usta ve mimar kanalında doğrudan işe yarıyor."),
 (("orman","kereste","kâğıt","ahşap","baston"), "Orman ürünlerinde malzemenin işlenme adımlarını ve son ürün varyantlarını gösteren animasyon, ihracat kataloğunun yerini alıyor."),
 (("deri",), "Deri üretiminde yüzey dokusunu ve işleme adımlarını gösteren makro animasyon, butik markalaşmayı destekliyor."),
 (("halı","kilim"), "Halı ve kilimde deseni ve dokuyu yakın planda gösteren 3D vitrin, online satışta fotoğrafın anlatamadığını anlatıyor."),
 (("tekne","yat","tersane"), "Tekne ve yat imalatında iç yerleşimi ve donanımı gösteren 3D tur, yurt dışı alıcıya tekneyi görmeden karar verdiriyor."),
 (("elektronik","beyaz eşya","kablo"), "Elektronik ve beyaz eşyada iç yapıyı gösteren kesit animasyonu, teknik satışta en etkili araç."),
 (("ambalaj",), "Ambalaj üretiminde kalıp, baskı ve montaj adımlarını gösteren animasyon, marka müşterisine kapasiteyi anlatmanın en hızlı yolu."),
 (("el sanatları","telkâri","gümüş","çömlek","oltu taşı","gül"), "El sanatları ve yüksek katma değerli küçük üründe makro 3D anlatım, online pazarda fiyatı meşrulaştıran şey oluyor."),
 (("balıkçılık","su ürünleri"), "Su ürünlerinde avlanmadan soğuk zincire uzanan süreç videosu, tazelik iddiasını görünür kılıyor."),
]

VARSAYILAN = "%s alanında üreten firmalar için ürünü ve süreci anlatan 3D animasyon, fuar ve ihracat görüşmelerinde tercümandan hızlı iş görüyor."

def sektor_cumlesi(sektor):
    s = sektor.lower()
    for anahtarlar, cumle in KURAL:
        if any(a in s for a in anahtarlar):
            return cumle
    return VARSAYILAN % sektor

def sektor_bloku(c):
    """İlin kendi sektör listesinden, tekrar etmeyen anlatım cümleleri."""
    gorulen, satir = set(), []
    for sek in c["sektorler"]:
        cu = sektor_cumlesi(sek)
        if cu in gorulen: continue
        gorulen.add(cu)
        satir.append("<li><strong>%s</strong> — %s</li>" % (sek, cu))
    return "<ul>\n      %s\n    </ul>" % "\n      ".join(satir)


# ============================================================
#  İl bazlı "üç ihtiyaç" — sektör karışımına göre değişir
# ============================================================
IHTIYAC = [
 (("otomotiv","makine","otomasyon","metal","döküm","kalıp","demir","çelik","haddehane","elektronik","kablo","beyaz eşya"),
  "Teknik satışta ürünün içini gösterememek — kesit animasyonu bu boşluğu kapatıyor."),
 (("tekstil","iplik","konfeksiyon","kumaş","havlu","battaniye","deri","halı","kilim","dokuma","mobilya","ev tekstili"),
  "Renk ve varyant çeşidini her seferinde yeniden çekmek zorunda kalmak — 3D modelde varyant üretmek dakikalar sürüyor."),
 (("gıda","süt","peynir","zeytin","fındık","kayısı","meyve","şeker","konserve","bal","çay","fıstık","bisküvi","un ","et ","narenciye","ceviz","incir","kaşar","pestil","elma","pirinç","sarımsak","yem","kuru üzüm"),
  "Zincir market ve ihracat müşterisine izlenebilirliği anlatmak — hammaddeden pakete süreç videosu bunu tek seferde yapıyor."),
 (("mermer","doğal taş","traverten","seramik","porselen","çini","cam","refrakter","çimento","tuğla","kiremit","inşaat malzemesi","taş işleme","kaolen"),
  "Malzemenin uygulandığında nasıl duracağını gösterememek — uygulama ve doku animasyonu mimar kanalını açıyor."),
 (("kimya","petrokimya","plastik","boya","lastik","gübre","petrol","rafinaj","madencilik","kömür","bor","krom","bakır","enerji","jeotermal","tuz"),
  "Gizlilik ve iş güvenliği nedeniyle üretim hattını çekememek — 3D ile süreç anlatılıyor, tesis görünmüyor."),
 (("savunma","havacılık","raylı","medikal","laboratuvar","tıbbi"),
  "Ürünü ihale ve denetim sunumunda anlatmak — montaj ve kullanım animasyonu bunu standart hale getiriyor."),
 (("lojistik","liman","sınır ticareti","yazılım","teknoloji","fintek","turizm","otel","konaklama","termal"),
  "Fiziksel ürünün olmaması — hizmetin kendisi süreç animasyonuyla somutlaşıyor."),
 (("tarım","tarım makineleri","hayvancılık","arıcılık","seracılık","pamuk","bağcılık","şarap","fidancılık","süs bitki","balıkçılık","su ürünleri","değirmen"),
  "Ürünün sahada nasıl çalıştığını ya da nasıl yetiştiğini göstermek — mevsim beklemeden animasyonla anlatılabiliyor."),
 (("ambalaj","orman","kereste","kâğıt","ahşap","tekne","yat","tersane","el sanatları","telkâri","gümüş","çömlek","gül","baston","oltu taşı","bakırcılık"),
  "Küçük detayın ve işçiliğin fotoğrafta kaybolması — makro 3D anlatım işçiliği görünür kılıyor."),
]

def uc_ihtiyac(c):
    secilen, gorulen = [], set()
    for sek in c["sektorler"]:
        s = sek.lower()
        for anahtarlar, cumle in IHTIYAC:
            if any(a in s for a in anahtarlar) and cumle not in gorulen:
                gorulen.add(cumle); secilen.append(cumle)
                break
        if len(secilen) == 3:
            break
    while len(secilen) < 3:
        for _, cumle in IHTIYAC:
            if cumle not in gorulen:
                gorulen.add(cumle); secilen.append(cumle); break
        else:
            break
    return secilen


# ============================================================
#  İşletme tarafı — ile göre içerik fikirleri
# ============================================================
FIKIR = [
 (("gastronomi","gıda","zeytin","bal","peynir","süt","çay","fındık","fıstık","kayısı","incir","meyve","narenciye","şarap","bağcılık","et "),
  "Yerel ürünün mutfakta kullanıldığı kısa video — şehirle kurulan bağ en çok paylaşılan içerik türü."),
 (("turizm","otel","konaklama","termal"),
  "Ziyaretçiye dönük \"şehirde 24 saat\" formatı — işletmenizi turistin gününün içine yerleştiriyor."),
 (("tekstil","mobilya","halı","kilim","deri","el sanatları","çömlek","telkâri","gümüş","bakırcılık"),
  "Üretim ve el işçiliği anları — arkada olan biteni göstermek satın alma kararını hızlandırıyor."),
 (("otomotiv","makine","metal","demir","çelik","madencilik","kimya","plastik","enerji","lojistik","liman","kömür"),
  "Vardiya saatlerine göre kurgulanmış içerik takvimi — sanayi çalışanının gününe denk gelen paylaşım en yüksek etkileşimi alıyor."),
 (("tarım","hayvancılık","seracılık","arıcılık","balıkçılık","su ürünleri","fidancılık","pamuk","süs bitki"),
  "Mevsim döngüsüne bağlı içerik — hasat, sezon açılışı ve ürün değişimi doğal bir takvim veriyor."),
 (("üniversite","yazılım","teknoloji","savunma","havacılık","medikal","eğitim"),
  "Genç ve öğrenci kitleye dönük kısa, hızlı tempolu dikey içerik — fiyat ve atmosfer vurgusu öne çıkıyor."),
]
VARSAYILAN_FIKIR = [
 "Mekânın günün farklı saatlerindeki hâli — sabah, öğle ve akşam üç ayrı atmosfer, üç ayrı içerik.",
 "Ekibin işini yaparken çekildiği kısa videolar — insan yüzü gören içerik güven kuruyor.",
 "Müşteri yorumlarının görsele dönüştürülmesi — yazılı yorumdan çok daha fazla izleniyor.",
]

def icerik_fikirleri(c):
    secilen, gorulen = [], set()
    for sek in c["sektorler"]:
        s = sek.lower()
        for anahtarlar, cumle in FIKIR:
            if any(a in s for a in anahtarlar) and cumle not in gorulen:
                gorulen.add(cumle); secilen.append(cumle); break
    if c.get("mekan"):
        ilk = c["mekan"].split(",")[0].strip()
        secilen.append("Şehrin tanınan bir noktasıyla kurulan içerik — örneğin %s çevresinde çekilen kısa bir tanıtım, yerel izleyicide anında karşılık buluyor." % ilk)
    for f in VARSAYILAN_FIKIR:
        if len(secilen) >= 5: break
        if f not in gorulen: gorulen.add(f); secilen.append(f)
    return secilen[:5]
