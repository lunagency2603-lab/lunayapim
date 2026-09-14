# -*- coding: utf-8 -*-
"""
Çeşitlendirme katmanı.
Aynı şablonun 300 sayfada birebir tekrar etmesi Google'ın "doorway page"
tanımına girer. Bu modül, her ilin slug'ından türeyen sabit bir sayı ile
başlıkları, geçiş cümlelerini ve bölüm sırasını değiştirir — böylece her
sayfa aynı bilgiyi farklı bir metinle verir.
"""
import hashlib, re

def varyant(slug, n, tuz=""):
    h = hashlib.md5((slug + "|" + tuz).encode("utf-8")).hexdigest()
    return int(h[:8], 16) % n

# --- başlık ve kalıp alternatifleri (aynı anlam, farklı cümle) ---
ALTERNATIF = {
 "Ne teslim ediyoruz": ["Ne teslim ediyoruz", "Elinize ne geçiyor", "Teslim listesi"],
 "Süreç": ["Süreç", "İşin akışı", "Nasıl ilerliyoruz"],
 "sık sorulan sorular": ["sık sorulan sorular", "en çok sorulanlar", "merak edilenler"],
 "Paketler": ["Paketler", "Çalışma paketleri", "Nasıl paketliyoruz"],
 "Oynatmak için bir işin üzerine dokun.":
   ["Oynatmak için bir işin üzerine dokun.",
    "Bir işe dokunun, oynasın.",
    "Örnekleri buradan izleyebilirsiniz."],
 "İlgili sayfalar": ["İlgili sayfalar", "Yakından ilgili işler", "Bunlara da bakın"],
 "hangi ilçelerde çalışıyoruz": ["hangi ilçelerde çalışıyoruz", "nerelere gidiyoruz", "hangi ilçeleri kapsıyoruz"],
 "diğer hizmetlerimiz": ["diğer hizmetlerimiz", "başka neler yapıyoruz", "verdiğimiz diğer hizmetler"],
 "için teklif al": ["için teklif al", "için fiyat iste", "için teklif isteyin"],
}

# --- açılış geçiş cümleleri (her ilde farklı bir giriş tonu) ---
GIRIS = [
 "Şehri tanımadan iş yapmıyoruz; aşağıdaki her satır {ad} için yazıldı.",
 "Aynı işi her ilde aynı şekilde yapmıyoruz — {ad}'ın kendi dinamiği var.",
 "Bu sayfadaki her şey {ad} için ayrı düşünüldü, başka ilden kopyalanmadı.",
 "{ad} özelinde ne yaptığımızı ve neden böyle yaptığımızı aşağıda anlattık.",
 "Bir şehirde işe yarayan anlatım diğerinde yaramıyor; {ad} için olan bu.",
]

def cesitlendir(govde, c):
    """Üretilen HTML'i ilin slug'ına göre çeşitlendirir."""
    slug = c["slug"]
    for kanonik, secenekler in ALTERNATIF.items():
        i = varyant(slug, len(secenekler), kanonik)
        if secenekler[i] != kanonik:
            govde = govde.replace(kanonik, secenekler[i])
    return govde

def giris_cumlesi(c):
    return GIRIS[varyant(c["slug"], len(GIRIS), "giris")].format(ad=c["ad"])


def yerel_blok(c, odak="genel"):
    """
    Her sayfaya giren, tamamen o ile özgü 'yerel unsurlar' bölümü.
    odak: sayfanın hizmetine göre vurguyu değiştirir.
    """
    ad, ek = c["ad"], c["ek"]
    ilce = c["ilceler"]
    ilce_metni = ", ".join(ilce[:-1]) + " ve " + ilce[-1] if len(ilce) > 1 else ilce[0]
    sek = c["sektorler"]

    satirlar = ['<h2>%s%s yerel unsurlar</h2>' % (ad, ek),
                '<p>%s</p>' % giris_cumlesi(c)]

    if odak in ("insaat", "emlak", "genel"):
        satirlar.append('<h3>Yapı ve gayrimenkul dokusu</h3><p>%s</p>' % c["insaat"])
    if odak in ("emlak", "genel"):
        satirlar.append('<p>%s</p>' % c["emlak"])
    if odak in ("urun", "genel"):
        satirlar.append('<h3>Üretim profili</h3><p>%s</p>' % c["sanayi"])
    if odak in ("drone", "klip", "dugun", "genel", "insaat", "emlak"):
        satirlar.append('<h3>Coğrafya ve çekim koşulları</h3><p>%s</p>' % c["cografya"])
    if odak in ("klip", "dugun") and c.get("kultur"):
        satirlar.append('<h3>Yerel kültür ve sahne</h3><p>%s</p>' % c["kultur"])
    if odak in ("klip", "dugun", "drone") and c.get("mekan"):
        satirlar.append('<h3>Çekim mekânları</h3><p>%s%s sık kullandığımız mekânlar: %s.</p>'
                        % (ad, ek, c["mekan"]))
    if odak == "isletme" and c.get("isletme_notu"):
        satirlar.append('<h3>Yerel işletme ortamı</h3><p>%s</p>' % c["isletme_notu"])
    if odak == "dugun" and c.get("dugun_notu"):
        satirlar.append('<h3>Düğün geleneği</h3><p>%s</p>' % c["dugun_notu"])

    satirlar.append('<h3>Kapsadığımız ilçeler</h3><p>%s dahil ilin tamamında çalışıyoruz.</p>' % ilce_metni)
    satirlar.append('<h3>Öne çıkan sektörler</h3><ul>%s</ul>'
                    % "".join("<li>%s</li>" % x for x in sek))
    return "\n    ".join(satirlar)


# ============================================================
#  PARAGRAF VARYANTLARI
#  Şablonun en uzun ortak paragrafları her ilde farklı yazılır.
#  Aynı bilgi, farklı cümle — böylece sayfalar birbirinin kopyası olmuyor.
# ============================================================
PARAGRAF = {

# --- ürün animasyonu ---
"Her ürün kameraya gelmez. Kimi çok büyüktür, kimi çalışırken içi görünmez, kimi henüz üretilmemiştir, kimi de zaten fiziksel değildir. 3D modelleme ve animasyon tam olarak kameranın yapamadığını yapar: ürünü havada döndürür, ortadan ikiye keser, içindeki akışı renklendirir, montajını adım adım söker ve tekrar takar.": [
 "Her ürün kameraya gelmez. Kimi çok büyüktür, kimi çalışırken içi görünmez, kimi henüz üretilmemiştir, kimi de zaten fiziksel değildir. 3D modelleme ve animasyon tam olarak kameranın yapamadığını yapar: ürünü havada döndürür, ortadan ikiye keser, içindeki akışı renklendirir, montajını adım adım söker ve tekrar takar.",
 "Bir ürünü fotoğraflamak onu anlatmaya çoğu zaman yetmiyor. Makine çalışırken içi görünmüyor, tesis çok büyük olduğu için kadraja sığmıyor, yeni model henüz üretim bandına inmemiş oluyor. 3D animasyon bu noktada devreye giriyor: gövdeyi saydamlaştırıyor, akışı renklendiriyor, parçaları havada ayırıp yeniden birleştiriyor.",
 "Satışta asıl soru ürünün nasıl göründüğü değil, nasıl çalıştığı. Kamera bunu çoğu zaman gösteremiyor — ya ürün kapalı, ya çok büyük, ya da henüz ortada yok. 3D animasyon ürünü istediğiniz açıdan döndürüyor, kesitini alıyor, içindeki hareketi görünür kılıyor ve montajını adım adım anlatıyor.",
],

# --- emlak ---
"Bir ilanda on fotoğraf yerine bir dakikalık iyi bir video, alıcının kararını belirgin şekilde hızlandırır. Videonun asıl faydası ise ayak izini azaltmasıdır: alıcı gelmeden önce mülkü gezmiş olur, yerinde gezmeye gelen kişi daha nitelikli olur.": [
 "Bir ilanda on fotoğraf yerine bir dakikalık iyi bir video, alıcının kararını belirgin şekilde hızlandırır. Videonun asıl faydası ise ayak izini azaltmasıdır: alıcı gelmeden önce mülkü gezmiş olur, yerinde gezmeye gelen kişi daha nitelikli olur.",
 "Videolu ilanın en görünür faydası tıklanma, en değerli faydası ise eleme. Alıcı mülkü gelmeden gezmiş oluyor; yerinde görmeye gelen kişi gerçekten ilgilenen kişi oluyor. Danışman açısından bu, günde üç boş gezdirme yerine bir ciddi görüşme demek.",
 "İlan sitelerinde on fotoğrafın anlattığını iyi kurgulanmış altmış saniye çok daha net anlatıyor. Asıl kazanç ise zaman: mülkü uzaktan gezen alıcı, gezmeye geldiğinde kararının yarısını çoktan vermiş oluyor.",
],

# --- inşaat 3D ---
"Luna Yapım olarak {ad}{ek} bu iki ihtiyacın ikisine de aynı araçla cevap veriyoruz": [
 "Luna Yapım olarak {ad}{ek} bu iki ihtiyacın ikisine de aynı araçla cevap veriyoruz",
 "Bu iki farklı ihtiyaca {ad}{ek} tek bir yöntemle karşılık veriyoruz",
 "{ad}{ek} her iki durumda da izlediğimiz yol aynı",
],

# --- drone ---
"Havadan tek plan bir açılış, bir mekânın konumunu, ölçeğini ve çevresini anlatmanın en hızlı yolu. FPV ile ise kapıdan girip odaları gezen, sonra bahçeye çıkıp yukarı yükselen kesintisiz planlar çekiyoruz — az sayıda ekibin yapabildiği bir iş.": [
 "Havadan tek plan bir açılış, bir mekânın konumunu, ölçeğini ve çevresini anlatmanın en hızlı yolu. FPV ile ise kapıdan girip odaları gezen, sonra bahçeye çıkıp yukarı yükselen kesintisiz planlar çekiyoruz — az sayıda ekibin yapabildiği bir iş.",
 "Bir mekânın nerede olduğunu, ne kadar büyük olduğunu ve çevresinde ne bulunduğunu anlatmanın en kısa yolu tek bir havadan plan. FPV ise bunun tersini yapıyor: içeri giriyor, dar alanlardan geçiyor ve kesmeden dışarı çıkıyor. İkincisini yapabilen ekip sayısı çok az.",
 "Yerden çekilen görüntü mekânı gösterir, havadan çekilen görüntü konumu anlatır. FPV drone ise ikisini tek planda birleştiriyor: kapıdan giren, odaları gezen ve bahçeden yukarı yükselen kesintisiz bir hareket. Bu, çoğu ekibin denemekten kaçındığı bir çekim.",
],

# --- klip ---
"İyi bir klip şarkıyı tekrar etmez, ona bir dünya kurar. Luna Yapım'ın kısa film ve sinematografi geçmişi klip tarafında doğrudan işe yarıyor: hikâye kuran, oyuncu yöneten ve ışığı bilen aynı ekip FPV drone'u da uçuruyor.": [
 "İyi bir klip şarkıyı tekrar etmez, ona bir dünya kurar. Luna Yapım'ın kısa film ve sinematografi geçmişi klip tarafında doğrudan işe yarıyor: hikâye kuran, oyuncu yöneten ve ışığı bilen aynı ekip FPV drone'u da uçuruyor.",
 "Klip, şarkının görüntüyle tekrarı değil; ona bir mekân, bir ışık ve bir duygu vermesi. Kısa film tarafından gelen bir ekip olduğumuz için işe kameranın nereye konacağından değil, parçanın neyi anlattığından başlıyoruz — ve aynı ekip gün içinde FPV drone'u da uçuruyor.",
 "Bir klibi akılda kalıcı yapan şey şarkıyı görselleştirmesi değil, ona ait bir dünya kurması. Senaryo, oyuncu yönetimi, ışık ve kurgu aynı masada konuşulduğu için klip üç ayrı taşerona bölünmeden tek bir kafadan çıkıyor.",
],

# --- düğün ---
"Düğün videosu bir gün sonra değil, on yıl sonra izlenmek için çekilir. Biz de o yüzden düğünü olay sırasına göre kaydetmiyor, kısa bir film gibi kurguluyoruz: hazırlık, karşılaşma, tören ve gecenin kendi ritmi.": [
 "Düğün videosu bir gün sonra değil, on yıl sonra izlenmek için çekilir. Biz de o yüzden düğünü olay sırasına göre kaydetmiyor, kısa bir film gibi kurguluyoruz: hazırlık, karşılaşma, tören ve gecenin kendi ritmi.",
 "Düğün videosunun ömrü uzun; asıl izlenme zamanı ertesi hafta değil, yıllar sonrası. Bu yüzden günü baştan sona kaydetmek yerine bir kısa film gibi kurguluyoruz — hazırlığın telaşı, karşılaşma anı, törenin sessizliği ve gecenin kendi ritmi.",
 "İyi bir düğün filmi olayları sırayla göstermez, günün duygusunu taşır. Kameranın nerede duracağından çok neyi bekleyeceğine karar veriyoruz; kurguda da günü olay listesi gibi değil, hikâye gibi diziyoruz.",
],

# --- işletme ---
"Küçük bir işletmenin en büyük sorunu içerik üretmeye vakit bulamamak. Biz ayda bir gün geliyor, dört haftalık içeriği tek seferde çekiyoruz; siz sadece yayınlıyorsunuz.": [
 "Küçük bir işletmenin en büyük sorunu içerik üretmeye vakit bulamamak. Biz ayda bir gün geliyor, dört haftalık içeriği tek seferde çekiyoruz; siz sadece yayınlıyorsunuz.",
 "Yerel işletmelerde sorun içerik fikri değil, zaman. Servis açıkken kimse video çekmeye vakit bulamıyor. Bu yüzden ayda bir gün geliyoruz ve dört haftalık içeriği tek seferde topluyoruz — sizin işiniz sadece yayınlamak.",
 "İşletme sahibinin gününde sosyal medyaya ayrılacak yer genelde kalmıyor. Çözüm her gün biraz çekmek değil, ayda bir gün düzgün çekmek: tek çekimden dört haftalık akış çıkarıyoruz, takvimiyle birlikte teslim ediyoruz.",
],
}

def _paragraf_cesitle(govde, c):
    slug = c["slug"]
    for kanonik, secenekler in PARAGRAF.items():
        k = kanonik.format(ad=c["ad"], ek=c["ek"]) if "{ad}" in kanonik else kanonik
        if k not in govde:
            continue
        i = varyant(slug, len(secenekler), kanonik[:24])
        if i:
            yeni = secenekler[i]
            yeni = yeni.format(ad=c["ad"], ek=c["ek"]) if "{ad}" in yeni else yeni
            govde = govde.replace(k, yeni)
    return govde

_eski_cesitlendir = cesitlendir
def cesitlendir(govde, c):
    govde = _paragraf_cesitle(govde, c)
    return _eski_cesitlendir(govde, c)


# --- ürün animasyonu: karar tablosu ve kullanım listesi varyantları ---
_TABLO_A = """<div class='tablo-kaydir'><table>
      <tr><th>Durum</th><th>Önerimiz</th></tr>
      <tr><td>Ürün var, taşınabilir, güzel görünüyor</td><td>Gerçek çekim + kısa 3D detay</td></tr>
      <tr><td>Ürün çalışırken içi görünmüyor</td><td>Kesit animasyonu</td></tr>
      <tr><td>Ürün çok büyük veya sahada sabit</td><td>Drone çekimi + 3D birleşim</td></tr>
      <tr><td>Ürün henüz üretilmedi</td><td>Tamamen 3D</td></tr>
      <tr><td>Fiziksel ürün yok, hizmet var</td><td>Süreç animasyonu</td></tr>
      <tr><td>Tesiste gizlilik kuralı var</td><td>3D — hattı göstermeden süreci anlatır</td></tr>
    </table></div>"""

_TABLO_B = """<div class='tablo-kaydir'><table>
      <tr><th>Elinizdeki durum</th><th>Uygun yöntem</th></tr>
      <tr><td>Numune elde, taşınabiliyor ve fotojenik</td><td>Stüdyo çekimi, detaylarda kısa 3D</td></tr>
      <tr><td>Mekanizma kapalı gövdenin içinde</td><td>Şeffaflaştırma ve kesit</td></tr>
      <tr><td>Ekipman sahada sabit ya da kadraja sığmıyor</td><td>Havadan çekim ve 3D birleşim</td></tr>
      <tr><td>Model henüz üretim bandına inmedi</td><td>Baştan sona 3D</td></tr>
      <tr><td>Sattığınız şey bir hizmet</td><td>İzometrik süreç anlatımı</td></tr>
      <tr><td>Üretim hattı görüntülenemiyor</td><td>3D — akış anlatılır, tesis gizli kalır</td></tr>
    </table></div>"""

_TABLO_C = """<div class='tablo-kaydir'><table>
      <tr><th>Soru</th><th>Cevap</th></tr>
      <tr><td>Ürünü kameranın önüne koyabiliyor musunuz?</td><td>Evet ise gerçek çekim, detayda 3D</td></tr>
      <tr><td>Anlatmak istediğiniz şey içeride mi oluyor?</td><td>Kesit ve şeffaflaştırma</td></tr>
      <tr><td>Ürün bir binadan büyük mü?</td><td>Drone + 3D birleşimi</td></tr>
      <tr><td>Ürün henüz var mı?</td><td>Yoksa tamamen 3D</td></tr>
      <tr><td>Elle tutulur bir ürün var mı?</td><td>Yoksa süreç animasyonu</td></tr>
      <tr><td>Hattı çekmenize izin veriliyor mu?</td><td>Verilmiyorsa 3D anlatım</td></tr>
    </table></div>"""

_LISTE_A = """<li><strong>Fuar standı</strong> — sessiz döngü sürümü, ekranda sürekli dönen anlatım</li>
      <li><strong>İhracat görüşmesi</strong> — çok dilli sürüm, dil bariyerini aşan görsel anlatım</li>
      <li><strong>Teklif dosyası</strong> — teklife eklenen bağlantı, ürünü satış temsilcisi olmadan anlatıyor</li>
      <li><strong>Bayi ve satış ekibi eğitimi</strong> — montaj ve kullanım anlatımı</li>
      <li><strong>Web sitesi ve sosyal medya</strong> — ürün sayfası videosu, reklam kesimleri</li>
      <li><strong>İhale ve yatırımcı sunumu</strong> — tesis kapasitesinin görsel anlatımı</li>"""

_LISTE_B = """<li><strong>Fuarda</strong> — standdaki ekranda sessiz dönen sürüm, tercümandan hızlı iş görüyor</li>
      <li><strong>Yurt dışı görüşmelerinde</strong> — İngilizce, Almanca veya Arapça seslendirilmiş sürüm</li>
      <li><strong>Tekliflerin ekinde</strong> — bağlantıyı açan müşteri ürünü kendi kendine anlıyor</li>
      <li><strong>Bayi eğitiminde</strong> — montaj, kurulum ve bakım adımları tek videoda</li>
      <li><strong>Ürün sayfasında</strong> — sitede kalış süresini uzatan asıl içerik</li>
      <li><strong>Yatırımcı ve ihale sunumunda</strong> — kapasitenin ve sürecin görsel kanıtı</li>"""

_LISTE_C = """<li><strong>Stand ekranı</strong> — ziyaretçi durmadan da anlatımın tamamını görüyor</li>
      <li><strong>İhracat dosyası</strong> — çok dilli sürüm, katalogdan çok daha fazla izleniyor</li>
      <li><strong>Satış görüşmesi</strong> — temsilcinin yirmi dakikada anlattığını doksan saniyede veriyor</li>
      <li><strong>Bayi ve servis ağı</strong> — kurulum ve yedek parça anlatımı standartlaşıyor</li>
      <li><strong>Dijital reklam</strong> — aynı animasyondan çıkan kısa kesimler</li>
      <li><strong>Kurumsal sunum</strong> — tesis ve kapasite anlatımı</li>"""

PARAGRAF[_TABLO_A] = [_TABLO_A, _TABLO_B, _TABLO_C]
PARAGRAF[_LISTE_A] = [_LISTE_A, _LISTE_B, _LISTE_C]


# --- inşaat 3D ve emlak: teslim listesi varyantları ---
_INS_A = """<li>Dış cephe render görselleri (gündüz / gün batımı / gece)</li>
      <li>60–120 saniyelik proje tanıtım animasyonu</li>
      <li>Daire tipi başına mobilyalı iç mekân görselleri</li>
      <li>Kuşbakışı yerleşim ve vaziyet planı maketi</li>
      <li>İnşaat aşama simülasyonu</li>
      <li>360° sanal tur bağlantısı</li>
      <li>Yatay, dikey ve kare video kesimleri</li>
    """
_INS_B = """<li>Üç ayrı ışık senaryosunda yüksek çözünürlüklü cephe görselleri</li>
      <li>Kamera hareketli proje filmi (bir ila iki dakika)</li>
      <li>Her daire tipi için döşenmiş iç mekân kareleri</li>
      <li>Blokları, otoparkı ve sosyal alanı gösteren kuşbakışı maket</li>
      <li>Kazıdan teslime hızlandırılmış inşaat simülasyonu</li>
      <li>Telefondan gezilebilen 360° sanal tur</li>
      <li>İlan sitesi, web ve sosyal medya için ayrı kurgular</li>
    """
_INS_C = """<li>Baskı ve web çözünürlüğünde dış cephe render seti</li>
      <li>Müzikli ve grafikli proje tanıtım animasyonu</li>
      <li>Mobilyalı daire tipi görselleri (1+1'den 4+1'e)</li>
      <li>Peyzajı ve yürüyüş yollarını gösteren vaziyet maketi</li>
      <li>Aşama aşama şantiye ilerleme animasyonu</li>
      <li>Web sitesine gömülebilen sanal tur</li>
      <li>Üç formatta (16:9, 9:16, 1:1) video teslimi</li>
    """
_EML_A = """<li>İlan siteleri için kısa versiyon (Sahibinden, Emlakjet, Hepsiemlak uyumlu)</li>
      <li>Web sitesi ve sunum için tam tanıtım filmi</li>
      <li>Sosyal medya için dikey ve kare kesimler</li>
      <li>Havadan ve içeriden yüksek çözünürlüklü fotoğraflar</li>
      <li>İstenirse 360° sanal tur bağlantısı</li>
      <li>İstenirse altyazı, seslendirme ve çok dilli sürüm</li>
    """
_EML_B = """<li>İlan sitelerine uygun 60–90 saniyelik kısa sürüm</li>
      <li>Web sitesi ve müşteri sunumu için tam film</li>
      <li>Reels ve TikTok için dikey, akış için kare kesim</li>
      <li>Drone ve iç mekân fotoğrafları (baskı çözünürlüğünde)</li>
      <li>Talep edilirse gezilebilir 360° sanal tur</li>
      <li>Talep edilirse yabancı dilde seslendirme ve altyazı</li>
    """
_EML_C = """<li>Portala yüklenmeye hazır kısa ilan videosu</li>
      <li>Ofis sunumu ve web sitesi için uzun sürüm</li>
      <li>Dikey ve kare sosyal medya kesimleri</li>
      <li>Havadan konum fotoğrafı ve iç mekân kareleri</li>
      <li>Sanal tur bağlantısı (isteğe bağlı)</li>
      <li>Yurt dışı alıcı için çok dilli sürüm (isteğe bağlı)</li>
    """
PARAGRAF[_INS_A] = [_INS_A, _INS_B, _INS_C]
PARAGRAF[_EML_A] = [_EML_A, _EML_B, _EML_C]
