# -*- coding: utf-8 -*-
"""
DEĞER YIĞINI — "biz ne katıyoruz" sorusunun somut cevabı.

Her hizmet için: teslim edilen kalemler, her kalemin piyasada ayrı ayrı alınsa
ne tutacağı, ve o kalemin işe ne yaradığı. Toplam değer teklifin üstünde çıktığı
sürece teklif kendini savunur. Uydurma rakam yok — kalem fiyatları piyasa.py'deki
derlenmiş aralıklardan geliyor.

Ayrıca: risk tersine çevirme (müşterinin kaybetme ihtimalini sıfırlayan madde),
ilk 30 günde ne olacağı, ve reddetmeyi zorlaştıran dürüst gerekçeler.
"""

# hizmet -> [(kalem, piyasa_degeri, ne_ise_yarar)]
YIGIN = {
"insaat-3d-modelleme": [
 ("6–8 dış cephe render görseli", 150000,
  "İlan sitesinde ve broşürde doğrudan kullanılır; alıcı projeyi bitmiş görür."),
 ("60–90 sn proje tanıtım animasyonu", 135000,
  "Satış ofisinde ve reklamda çalışır; anlatma yükünü ekipten alır."),
 ("Daire tipi başına iç mekân görselleri", 60000,
  "Alıcı metrekareyi rakam değil, içinde durduğu oda olarak görür."),
 ("Kuşbakışı yerleşim ve vaziyet maketi", 25000,
  "Hangi blok hangi manzaraya bakıyor, tek karede belli olur."),
 ("360° sanal tur", 20000,
  "Şehir dışı ve yurt dışı alıcı gelmeden karar verir."),
 ("Yatay / dikey / kare kesimler", 15000,
  "Aynı işten ilan sitesi, web ve sosyal medya sürümü çıkar; ayrıca ücret ödemezsin."),
],
"emlak-video": [
 ("Mülk başına tam tur videosu", 25000,
  "İlan listede öne çıkar, gelen alıcı daha nitelikli olur."),
 ("Drone ile konum ve çevre açılışı", 12000,
  "Konumun avantajı tek planda anlaşılır — arsa ve site ilanlarında belirleyici."),
 ("Havadan ve içeriden fotoğraf seti", 35000,
  "İlanda ve broşürde videodan daha uzun ömürlü kullanılır."),
 ("İlan sitesi + sosyal medya kesimleri", 12000,
  "Sahibinden'de ayrı, Instagram'da ayrı sürüm; tek çekimden ikisi de çıkar."),
 ("Dijital mobilyalama (boş mülkte)", 15000,
  "Boş daire soğuk durmaz; alıcı evi döşenmiş halde görür."),
],
"urun-animasyon": [
 ("Ürünün 3D modeli (sizde kalır)", 50000,
  "Bir kez yapılır; her yeni renk, modül ve versiyonda sıfırdan çekim yapmazsınız."),
 ("Çalışma prensibi / kesit animasyonu", 90000,
  "Kapalı gövdenin içini gösterir — teknik satışta 'anladım' dedirten şey budur."),
 ("Patlatılmış görünüm ve montaj", 40000,
  "Bayi eğitimi, kurulum kılavuzu ve yedek parça anlatımı tek videoya iner."),
 ("Fuar için sessiz döngü sürümü", 20000,
  "Standda tercümandan hızlı iş görür, ziyaretçi durmasa da anlatım tamamlanır."),
 ("Çok dilli seslendirme + altyazı", 25000,
  "Aynı animasyon İngilizce/Almanca/Arapça'ya çevrilir; ihracat kapısı açılır."),
],
"klip-cekimi": [
 ("Konsept ve storyboard", 20000,
  "Çekime plansız gidilmez; bütçe doğru sahneye harcanır."),
 ("Çekim günü (ekip + ekipman)", 60000,
  "Sinema kamerası, ışık ekibi ve FPV drone tek ekipten — koordinasyon derdi yok."),
 ("Sinematik renk düzenleme", 25000,
  "Kliplerde asıl fark burada oluşur; ham görüntüyle arasındaki mesafe budur."),
 ("Dikey kesimler ve teaser'lar", 18000,
  "Lansman haftasının içerik takvimi aynı çekimden çıkar."),
 ("Kamera arkası ve fotoğraf", 15000,
  "Klip sonrası üç hafta paylaşılacak malzeme hazır olur."),
],
"drone-cekimi": [
 ("Havadan 4K çekim + kurgu", 15000,
  "Konum, ölçek ve çevre tek planda anlaşılır."),
 ("Yüksek çözünürlüklü hava fotoğrafları", 10000,
  "İlanda ve baskıda videodan uzun ömürlü."),
 ("İzin takibi ve uçuş planı", 6000,
  "SHGM tarafını siz takip etmezsiniz; kapalı bölgede alternatif plan çıkar."),
 ("Aylık şantiye serisi (abonelik)", 25000,
  "Yatırımcıya düzenli rapor; teslimde projenin yükselişini gösteren tek film."),
],
"dugun-cekimi": [
 ("İki kamera + drone, tam gün", 55000,
  "Anı kaçırmayan çoklu açı; tek kamerayla çekilen düğünle arasındaki fark burada."),
 ("Ertesi gün teaser", 12000,
  "Paylaşım sıcakken elinizde hazır video olur."),
 ("8–12 dakikalık sinematik tam film", 25000,
  "Olay listesi değil, günün duygusunu taşıyan bir film."),
 ("Dış çekim ve save the date", 18000,
  "Düğün öncesi içerik ve davetiye materyali."),
],
"isletme-tanitim": [
 ("Aylık tek çekim günü", 20000,
  "Dört haftalık içerik tek seferde toplanır; siz uğraşmazsınız."),
 ("8–12 altyazılı dikey video", 18000,
  "Yayına hazır gelir; düzenleme derdi yok."),
 ("20–30 fotoğraf (menü / ürün / mekân)", 12000,
  "Google profili ve ilanlar aynı setten beslenir."),
 ("Google işletme profili düzenlemesi", 8000,
  "Haritada bulunurluğu doğrudan etkiler — çoğu müşteri oradan geliyor."),
 ("İçerik takvimi ve aylık ölçüm", 6000,
  "Ne zaman ne yayınlanacağı belli; ay sonunda işe yarayıp yaramadığı ölçülür."),
],
}

# Her hizmet için risk tersine çevirme — müşterinin kaybetme ihtimalini sıfırlayan madde
RISK_TERSI = {
"insaat-3d-modelleme":
  "İlk taslak render'ı beğenmezseniz ödeme yok, dosyayı kapatırız. Onaydan sonraki iki "
  "revizyon turu fiyata dahil.",
"emlak-video":
  "İlk mülkü çekelim; videoyu beğenmezseniz ücret almayız. Aylık pakete ancak ilk işten "
  "sonra karar verirsiniz.",
"urun-animasyon":
  "Storyboard onayınızdan önce hiçbir ödeme almıyoruz. Onaylamazsanız iş başlamaz, "
  "kimse bir şey kaybetmez.",
"klip-cekimi":
  "Konsepti beğenmezseniz çekime çıkmayız ve ödeme almayız. Çekim sonrası ilk kurguda "
  "iki revizyon dahil.",
"drone-cekimi":
  "Hava nedeniyle uçulamazsa erteleme ücreti yok. Çekimi beğenmezseniz ücret almıyoruz.",
"dugun-cekimi":
  "Kapora dışında ödeme teslimde. Teaser'ı beğenmezseniz tam filmi teslim etmeden önce "
  "birlikte yeniden kurgularız.",
"isletme-tanitim":
  "İlk ay deneme. Ay sonunda gelen aramayı ve harita görüntülenmesini birlikte sayarız; "
  "rakam ikna etmezse devam etmezsiniz.",
}

# İlk 30 günde ne olacak — somut takvim
OTUZ_GUN = {
"insaat-3d-modelleme": [
 ("1. hafta", "Mimari proje alınır, model kurulur, kamera açıları belirlenir."),
 ("2. hafta", "Taslak render'lar onayınıza sunulur; revizyon burada yapılır."),
 ("3. hafta", "Yüksek çözünürlüklü render seti teslim edilir — ilanları güncelleyebilirsiniz."),
 ("4. hafta", "Tanıtım animasyonu ve çoklu format kesimler teslim."),
],
"emlak-video": [
 ("1–2. gün", "Keşif ve çekim planı; ışık saatine göre takvim."),
 ("3. gün", "Çekim günü — video ve fotoğraflar aynı gün toplanır."),
 ("1. hafta sonu", "İlan sitesi sürümü teslim; ilanı güncelleyebilirsiniz."),
 ("2. hafta", "Sosyal medya kesimleri ve fotoğraf seti teslim."),
],
"urun-animasyon": [
 ("1. hafta", "Ürün brifingi, teknik dosya alımı, senaryo ve storyboard."),
 ("2. hafta", "Storyboard onayı → 3D modelleme başlar."),
 ("3. hafta", "Taslak animasyon onayınıza sunulur."),
 ("4. hafta", "Ses, grafik ve çoklu format teslim — fuara yetişir."),
],
"klip-cekimi": [
 ("1. hafta", "Şarkı dinlenir, konsept ve mekân önerileri çıkar."),
 ("2. hafta", "Konsept onayı, mekân izinleri ve ekip planı."),
 ("3. hafta", "Çekim günü."),
 ("4. hafta", "Kurgu, renk ve lansman paketi teslim."),
],
"drone-cekimi": [
 ("1–3. gün", "Uçuş izni kontrolü ve saha planı."),
 ("1. hafta", "Çekim günü (hava uygun ilk gün)."),
 ("2. hafta", "Kurgu, renk ve fotoğraf teslimi."),
 ("4. hafta", "Aylık seriye geçilirse ikinci çekim."),
],
"dugun-cekimi": [
 ("Rezervasyon", "Tarih takvimde ayrılır, kapora alınır."),
 ("Düğün öncesi", "Gün akışı ve dış çekim rotası planlanır."),
 ("Düğün günü", "İki kamera + drone, hazırlıktan geceye."),
 ("Ertesi gün", "Teaser teslim; tam film 3–5 hafta içinde."),
],
"isletme-tanitim": [
 ("1. hafta", "İçerik planı ve çekim takvimi birlikte kurulur."),
 ("2. hafta", "Çekim günü — dört haftalık malzeme tek seferde."),
 ("3. hafta", "İlk içerikler ve Google profil düzenlemesi teslim."),
 ("4. hafta", "Ay sonu ölçüm: gelen arama, harita görüntülenmesi, etkileşim."),
],
}


def _tl(x):
    return "{:,}".format(int(round(x))).replace(",", ".") + " ₺"


def yigin(hizmet, eksikler=None, sehir_carpani=1.0):
    """Değer yığını + toplam. eksikler verilirse ilgili kalemler işaretlenir."""
    kalemler = YIGIN.get(hizmet, [])
    eksikler = set(eksikler or [])
    ilgi = {
        "video_yok": ("animasyon", "video", "tur", "klip", "çekim", "kesim", "film"),
        "gorsel_az": ("fotoğraf", "render", "görsel"),
        "site_yok": ("kesim", "tur", "fotoğraf"),
        "sosyal_yok": ("kesim", "dikey", "sosyal"),
        "yorum_az": ("google", "profil"),
    }
    anahtarlar = set()
    for e in eksikler:
        anahtarlar |= set(ilgi.get(e, ()))
    cikti, toplam = [], 0
    for ad, deger, fayda in kalemler:
        d = int(round(deger * sehir_carpani))
        toplam += d
        vurgu = any(a in ad.lower() for a in anahtarlar)
        cikti.append({"ad": ad, "deger": d, "deger_tl": _tl(d), "fayda": fayda, "vurgu": vurgu})
    return {"kalemler": cikti, "toplam": toplam, "toplam_tl": _tl(toplam)}


def paket(hizmet, teklif, eksikler=None, sehir=None):
    """Teklifin değer yığınına göre konumu — 'ne kadar kazanıyorsun' anlatımı."""
    from .piyasa import carpan
    y = yigin(hizmet, eksikler, carpan(sehir))
    d = {"yigin": y, "risk": RISK_TERSI.get(hizmet, ""), "takvim": OTUZ_GUN.get(hizmet, [])}
    if teklif:
        t = float(teklif)
        d["teklif"] = int(t)
        d["kazanc"] = int(y["toplam"] - t)
        d["kazanc_tl"] = _tl(max(0, y["toplam"] - t))
        d["oran"] = round(y["toplam"] / t, 1) if t else None
    return d


def deger_cumlesi(hizmet, tahmin, eksikler):
    """Tek cümlede 'biz ne katıyoruz' — mesajlarda ve teklifte kullanılır."""
    kazanc = (tahmin or {}).get("ek_gelir") or 0
    n = len(eksikler or [])
    kalem = len(YIGIN.get(hizmet, []))
    return ("%d başlıktaki eksiği kapatan %d kalemlik bir çalışma; modelimize göre aylık "
            "ek ciro potansiyeli %s." % (n, kalem, _tl(kazanc)))
