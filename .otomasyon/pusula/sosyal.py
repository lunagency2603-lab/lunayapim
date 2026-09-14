# -*- coding: utf-8 -*-
"""
SOSYAL MEDYA TESPİTİ VE EŞLEŞTİRME

Firmanın sosyal hesaplarını bulur, gerçekten o firmaya ait olup olmadığını ad
benzerliğiyle puanlar, hesabın açık olup olmadığını doğrular ve sektöre göre
hangi platformun eksik olduğunu çıkarır.

DÜRÜSTLÜK NOTU: Takipçi sayısı, paylaşım sıklığı ve etkileşim gibi veriler
platformların herkese açık sayfalarından güvenilir biçimde okunamıyor (Instagram
giriş duvarı arkasında, diğerleri sık sık değişiyor). Okunabilirse okunur ve
"teyitli" işaretlenir; okunamazsa "teyit edilemedi" denir ve panelde elle
girilebilecek bir alan bırakılır. Uydurma rakam üretmiyoruz.
"""
import re, html, unicodedata, datetime, urllib.parse
from .kaynaklar.agir import getir
from . import sosyal_saglik as SG

PLATFORM = {
 "instagram": {"ad": "Instagram", "url": "https://instagram.com/%s"},
 "facebook":  {"ad": "Facebook",  "url": "https://facebook.com/%s"},
 "linkedin":  {"ad": "LinkedIn",  "url": "https://linkedin.com/company/%s"},
 "youtube":   {"ad": "YouTube",   "url": "https://youtube.com/@%s"},
 "tiktok":    {"ad": "TikTok",    "url": "https://tiktok.com/@%s"},
 "x":         {"ad": "X",         "url": "https://x.com/%s"},
}

# Sektöre göre hangi platform gerçekten işe yarıyor (agirlik: eksikse ne kadar önemli)
SEKTOR_PLATFORM = {
 "produksiyon": [("instagram", 3, "Görsel iş yapan bir ekibin vitrini burası; potansiyel müşteri işi görmeden aramıyor."),
                 ("youtube", 3, "Uzun işlerin kalıcı adresi; teklif ekine bağlantı olarak giriyor ve yıllarca çalışıyor."),
                 ("linkedin", 2, "Müteahhit, fabrika ve otel tarafındaki karar verici burada; B2B iş buradan geliyor."),
                 ("tiktok", 1, "Erişim tarafı; asıl işi Instagram'a ve siteye trafik taşımak.")],
 "insaat":   [("instagram", 3, "Proje görselleri ve şantiye ilerlemesi burada takip ediliyor; alıcı projeyi ilk buradan görüyor."),
              ("youtube", 2, "Proje tanıtım filmi ve sanal turun kalıcı adresi; ilanlardan ve siteden buraya bağlanılıyor."),
              ("linkedin", 2, "Yatırımcı, tedarikçi ve kurumsal alıcı tarafı LinkedIn'den bakıyor.")],
 "emlak":    [("instagram", 3, "Portföy videosu ve mülk turları en çok buradan yayılıyor; danışman kimliği burada kuruluyor."),
              ("youtube", 2, "Uzun mülk turları ve sanal turlar için; ilan sitesine link verilebiliyor."),
              ("tiktok", 1, "Genç alıcı ve kiracı kitlesi için hızlı mülk turları.")],
 "mimarlik": [("instagram", 3, "Mimari görsel işi tamamen görsel; portföy burada dolaşıyor."),
              ("linkedin", 2, "İşveren ve müteahhit tarafı LinkedIn'den referans bakıyor."),
              ("youtube", 1, "Proje animasyonlarının kalıcı arşivi.")],
 "sanayi":   [("linkedin", 3, "B2B alıcı, ihracat müşterisi ve tedarik zinciri LinkedIn'de; kurumsal güven buradan kuruluyor."),
              ("youtube", 3, "Ürün çalışma videosu ve fabrika turu; fuar öncesi müşteri buradan inceliyor."),
              ("instagram", 1, "İşveren markası ve fuar anları için ikincil kanal.")],
 "mobilya":  [("instagram", 3, "Ürün ve mekân görseli doğrudan satışa dönüyor; koleksiyon burada gösteriliyor."),
              ("youtube", 2, "Montaj, varyant ve showroom turu videoları."),
              ("tiktok", 2, "Ev dekorasyonu içeriği bu platformda çok hızlı yayılıyor.")],
 "otel":     [("instagram", 3, "Rezervasyon kararının büyük kısmı burada görülen görselle veriliyor."),
              ("youtube", 2, "Tesis turu ve çevre videoları; acente ve doğrudan rezervasyon için."),
              ("facebook", 1, "Yurt dışı ve orta yaş üstü misafir kitlesi hâlâ burada.")],
 "isletme":  [("instagram", 3, "Yerel işletmede tercih kararı çoğunlukla Instagram'da veriliyor."),
              ("facebook", 2, "Mahalle grupları ve yerel arama trafiği için."),
              ("tiktok", 2, "Yeni müşteri keşfi için en hızlı büyüyen kanal.")],
}
HIZMET_SOZCUK = {
 "produksiyon": ("video", "prodüksiyon", "3d", "animasyon", "çekim", "drone", "render", "kurgu"),
 "insaat": ("inşaat", "müteahhit", "konut", "proje", "yapı", "daire", "şantiye"),
 "emlak": ("emlak", "gayrimenkul", "danışman", "portföy", "satılık", "kiralık"),
 "mimarlik": ("mimar", "mimarlık", "tasarım", "proje", "iç mimari"),
 "sanayi": ("üretim", "sanayi", "makine", "fabrika", "imalat", "ihracat"),
 "mobilya": ("mobilya", "tasarım", "ahşap", "koltuk", "dekorasyon"),
 "otel": ("otel", "tesis", "konaklama", "rezervasyon", "butik"),
 "isletme": ("hizmet", "işletme", "mağaza", "atölye", "servis"),
}

VARSAYILAN_PLATFORM = SEKTOR_PLATFORM["isletme"]


# ---------------------------------------------------------------- ad eşleştirme
# Sadece hukuki ek ve doldurma kelimeler atılır. "inşaat", "yapı", "mobilya" gibi
# sektör kelimeleri çoğu zaman kullanıcı adının parçası olduğu için ATILMAZ.
SIRA_DISI = {"as", "ltd", "sti", "san", "tic", "ve", "co", "com", "net", "tr",
             "official", "resmi", "anonim", "limited", "sirketi", "sirket"}


# Türkçe harfler NFKD ile düzgün çözülmüyor (ı hiç çözülmüyor) — elle eşleyelim
TR_HARF = str.maketrans({
    "ı": "i", "İ": "i", "I": "i", "ğ": "g", "Ğ": "g", "ş": "s", "Ş": "s",
    "ö": "o", "Ö": "o", "ü": "u", "Ü": "u", "ç": "c", "Ç": "c", "â": "a", "î": "i", "û": "u",
})


def tr_sade(x):
    d = (x or "").translate(TR_HARF)
    return unicodedata.normalize("NFKD", d).encode("ascii", "ignore").decode().lower()


def _sadelestir(x):
    return re.sub(r"[^a-z0-9]", "", tr_sade(x))


def _kelimeler(x):
    ham = [k for k in re.split(r"[^a-z0-9]+", tr_sade(x)) if k and len(k) > 2]
    suzulmus = [k for k in ham if k not in SIRA_DISI]
    return suzulmus or ham


def eslesme_puani(firma, kullanici):
    """0–100. Hesabın gerçekten bu firmaya ait olma ihtimali."""
    f, k = _sadelestir(firma), _sadelestir(kullanici)
    if not f or not k:
        return 0
    if f == k:
        return 100
    if f in k or k in f:
        return 88
    fk, kk = set(_kelimeler(firma)), set(_kelimeler(kullanici))
    if not fk:
        return 30
    ortak = fk & kk
    if ortak:
        return int(60 + 30 * len(ortak) / float(len(fk)))
    # baş harf/ kısaltma denemesi
    bas = "".join(w[0] for w in _kelimeler(firma))
    if bas and (bas == k or bas in k):
        return 62
    ortak_harf = len(set(f) & set(k)) / float(len(set(f) | set(k)) or 1)
    return int(ortak_harf * 45)


def eslesme_yorumu(p):
    if p >= 85:  return "kesin eşleşme"
    if p >= 65:  return "büyük ihtimalle aynı firma"
    if p >= 45:  return "şüpheli — elle doğrulanmalı"
    return "eşleşmiyor — başka bir hesap olabilir"


# ---------------------------------------------------------------- hesap doğrulama
OG_ACIKLAMA = re.compile(r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\'](.*?)["\']', re.S | re.I)
OG_BASLIK = re.compile(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\'](.*?)["\']', re.S | re.I)
SAYI_TAKIP = re.compile(r"([\d.,]+\s*[KMBkmb]?)\s*(?:Followers|takipçi|Takipçi|abone|subscribers)", re.I)
SAYI_GONDERI = re.compile(r"([\d.,]+\s*[KMBkmb]?)\s*(?:Posts|gönderi|Gönderi|video)", re.I)


def hesap_dogrula(url):
    """
    Hesap açık mı? Açıksa herkese açık üstveriden okunabileni al.
    Okunamayan alanlar None kalır — uydurulmaz.
    """
    d = {"url": url, "acik": None, "durum": 0, "baslik": None,
         "takipci": None, "gonderi": None, "teyit": "teyit edilemedi"}
    kod, govde, _ = getir(url, zaman_asimi=8)
    d["durum"] = kod
    if kod in (200, 999):          # LinkedIn bot trafiğine 999 döner
        d["acik"] = True
    elif kod in (404, 410):
        d["acik"] = False
        d["teyit"] = "hesap bulunamadı (%s)" % kod
        return d
    else:
        d["teyit"] = "doğrulanamadı (durum %s)" % (kod or "bağlantı yok")
        return d

    m = OG_BASLIK.search(govde or "")
    if m:
        d["baslik"] = html.unescape(m.group(1))[:120]
    a = OG_ACIKLAMA.search(govde or "")
    if a:
        metin = html.unescape(a.group(1))
        t = SAYI_TAKIP.search(metin)
        g = SAYI_GONDERI.search(metin)
        if t:
            d["takipci"] = t.group(1).strip()
        if g:
            d["gonderi"] = g.group(1).strip()
        if t or g:
            d["teyit"] = "sayfanın herkese açık üstverisinden okundu"
        else:
            d["teyit"] = "hesap açık; takipçi/gönderi verisi sayfada yayınlanmıyor"
    else:
        d["teyit"] = "hesap açık; üstveri okunamadı"
    return d


def tahmin_kullanici(firma):
    """Firma adından olası kullanıcı adları — doğrulanacak adaylar."""
    k = _kelimeler(firma)
    if not k:
        return []
    birlesik = "".join(k)
    adaylar = [birlesik, ".".join(k), "_".join(k)]
    if len(k) > 1:
        adaylar.append(k[0] + k[1])
    adaylar.append(k[0])
    gorulen, cikti = set(), []
    for a in adaylar:
        if 3 <= len(a) <= 30 and a not in gorulen:
            gorulen.add(a); cikti.append(a)
    return cikti[:4]


# ---------------------------------------------------------------- ana tespit
def sosyal_denetle(firma, sektor, bulunan_kanallar, tahmin_et=True, azami_deneme=6,
                   sehir=""):
    """
    bulunan_kanallar: [{tur, deger, kaynak}] — site keşfinden gelenler.
    Döner: {hesaplar, eksikler, oncelik, zaman}
    """
    zaman = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    beklenen = SEKTOR_PLATFORM.get(sektor, VARSAYILAN_PLATFORM)
    beklenen_map = {p: (a, n) for p, a, n in beklenen}

    hesaplar, eksikler = {}, []
    deneme = 0

    # 1) sitede bağlantısı bulunanlar
    for k in bulunan_kanallar:
        t = k.get("tur")
        if t not in PLATFORM:
            continue
        url = k.get("deger")
        kullanici = url.rstrip("/").split("/")[-1].lstrip("@")
        puan = eslesme_puani(firma, kullanici)
        kayit = {"platform": t, "ad": PLATFORM[t]["ad"], "url": url, "kullanici": kullanici,
                 "kaynak": k.get("kaynak"), "nasil": "firmanın kendi sitesinde bağlantısı var",
                 "eslesme": puan, "eslesme_yorum": eslesme_yorumu(puan)}
        if deneme < azami_deneme:
            kayit.update(hesap_dogrula(url)); deneme += 1
            # sayfa sağlığı: bio, bağlantı, görsel, yayınlanmış sayılar
            try:
                kayit["saglik"] = SG.profil_saglik(
                    url, firma, sehir, HIZMET_SOZCUK.get(sektor, ()))
            except Exception as ex:
                kayit["saglik"] = {"hata": "%s: %s" % (type(ex).__name__, ex)}
        hesaplar[t] = kayit

    # 2) beklenen ama bulunamayan platformlarda kullanıcı adı tahmini
    if tahmin_et:
        for p, agirlik, neden in beklenen:
            if p in hesaplar or deneme >= azami_deneme:
                continue
            for kul in tahmin_kullanici(firma):
                if deneme >= azami_deneme:
                    break
                url = PLATFORM[p]["url"] % kul
                d = hesap_dogrula(url); deneme += 1
                if d["acik"]:
                    puan = eslesme_puani(firma, kul)
                    if puan < 45:
                        continue
                    try:
                        d["saglik"] = SG.profil_saglik(url, firma, sehir,
                                                       HIZMET_SOZCUK.get(sektor, ()))
                    except Exception:
                        pass
                    hesaplar[p] = dict(d, platform=p, ad=PLATFORM[p]["ad"], kullanici=kul,
                                       kaynak="ad tahminiyle bulundu, açık olduğu doğrulandı",
                                       nasil="firma adından türetilip doğrulandı",
                                       eslesme=puan, eslesme_yorum=eslesme_yorumu(puan))
                    break

    # 3) eksikleri çıkar
    def ekle(kod, baslik, kontrol, bulgu, kaynak, agirlik):
        eksikler.append({"kod": kod, "baslik": baslik, "agirlik": agirlik,
                         "kanit": {"kontrol": kontrol, "bulgu": bulgu,
                                   "kaynak": kaynak, "zaman": zaman}})

    if not hesaplar:
        ekle("sosyal_hicyok", "Hiç sosyal medya hesabı bulunamadı",
             "Firmanın sitesindeki bağlantılar ve firma adından türetilen kullanıcı adları",
             "Hiçbir platformda doğrulanabilen hesap bulunamadı",
             "site + platform doğrulaması", 3)

    for p, agirlik, neden in beklenen:
        if p not in hesaplar:
            ekle("sosyal_%s_yok" % p, "%s hesabı yok" % PLATFORM[p]["ad"],
                 "%s üzerinde firma adıyla eşleşen hesap" % PLATFORM[p]["ad"],
                 "Bulunamadı — bu sektörde %s" % neden[0].lower() + neden[1:],
                 "%s araması" % PLATFORM[p]["ad"], agirlik)
        else:
            h = hesaplar[p]
            if h.get("acik") is False:
                ekle("sosyal_%s_olu" % p, "%s hesabı açılmıyor" % PLATFORM[p]["ad"],
                     "Sitede verilen %s bağlantısı" % PLATFORM[p]["ad"],
                     "Bağlantı çalışmıyor (durum %s) — sitede ölü link duruyor" % h.get("durum"),
                     h.get("kaynak") or h["url"], agirlik)
            if h.get("eslesme", 100) < 45:
                ekle("sosyal_%s_eslesmiyor" % p, "%s hesabı firma adıyla uyuşmuyor" % PLATFORM[p]["ad"],
                     "Hesap adı ile firma adı karşılaştırması",
                     "Hesap adı '%s' — firma adıyla eşleşme zayıf, başka bir hesap olabilir" % h.get("kullanici"),
                     h["url"], 1)

    site_baglanti = any(k.get("tur") in PLATFORM for k in bulunan_kanallar)
    if hesaplar and not site_baglanti:
        ekle("sosyal_site_baglantisi_yok", "Sitede sosyal medya bağlantısı yok",
             "Firmanın sitesindeki sosyal medya bağlantıları",
             "Hesaplar var ama siteden bağlantı verilmemiş — ziyaretçi hesapları bulamıyor",
             "firma sitesi", 2)

    # --- profil sağlığı eksikleri (bio, bağlantı, görsel)
    for p, h in hesaplar.items():
        for e in ((h.get("saglik") or {}).get("eksik") or []):
            eksikler.append({"kod": e["kod"] + "_" + p, "baslik": e["baslik"],
                             "agirlik": e.get("agirlik", 1),
                             "kanit": {"kontrol": e["kontrol"], "bulgu": e["bulgu"],
                                       "kaynak": e["kaynak"], "zaman": e["zaman"]}})

    # --- kullanıcı adı tutarlılığı
    tut = SG.kullanici_tutarliligi(hesaplar)
    if tut.get("tutarli") is False:
        ekle("sosyal_ad_tutarsiz", "Platformlarda farklı kullanıcı adları",
             "Bulunan hesapların kullanıcı adlarının karşılaştırılması",
             tut["not"], "profil sayfaları", 2)

    # --- site ↔ hesap karşılıklılığı
    kars = SG.karsiliklilik(hesaplar, bulunan_kanallar)
    if kars.get("okunamayan"):
        # Bilmediğimizi eksik diye yazmıyoruz; not olarak geçiyoruz.
        kars["not"] = ("Şu hesapların profil sayfası okunamadı (giriş duvarı ya da ağ): %s. "
                       "Bio'daki bağlantı ve profil bütünlüğü için panelden elle bakılabilir."
                       % ", ".join(PLATFORM.get(p, {}).get("ad", p) for p in kars["okunamayan"]))
    if kars["tek_yonlu"]:
        ekle("sosyal_tek_yonlu_bag", "Hesaptan siteye bağlantı yok",
             "Profil açıklamasındaki (bio) bağlantı alanı",
             "Şu hesaplarda siteye bağlantı yok: %s. Sosyalden gelen ilgili kişi "
             "siteye geçemiyor, satın alma sayfasına ulaşamıyor."
             % ", ".join(PLATFORM.get(p, {}).get("ad", p) for p in kars["tek_yonlu"]),
             "profil sayfaları", 2)

    eksikler.sort(key=lambda e: -e["agirlik"])
    return {"hesaplar": hesaplar, "eksikler": eksikler, "beklenen": beklenen,
            "zaman": zaman, "denenen_istek": deneme,
            "tutarlilik": tut, "karsiliklilik": kars}


def sosyal_skor(sonuc):
    """0–100: sosyal medya varlığının gücü."""
    beklenen = sonuc.get("beklenen") or VARSAYILAN_PLATFORM
    toplam = sum(a for _, a, _ in beklenen) or 1
    kayip = sum(e["agirlik"] for e in sonuc["eksikler"] if e["kod"].endswith("_yok") or e["kod"] == "sosyal_hicyok")
    ceza = sum(1 for e in sonuc["eksikler"] if e["kod"].endswith(("_olu", "_eslesmiyor")))
    return max(0, min(100, int(round(100 * (1 - min(1.0, kayip / float(toplam))) - ceza * 6))))


# ============================================================
#  SEKTÖRE ÖZEL İÇERİK PLANI
#  Her fikir: başlık · format · kanca · neden işe yarıyor
#  Formatlar: reels (dikey video), carousel (kaydırmalı), tekli (tek görsel),
#             story (24 saat), uzun (YouTube), canli (yayın)
# ============================================================
FORMAT_AD = {"reels": "Reels / dikey video", "carousel": "Kaydırmalı görsel seti",
             "tekli": "Tek görsel", "story": "Story", "uzun": "Uzun video (YouTube)",
             "canli": "Canlı yayın"}

PLAN = {
"produksiyon": [
 ("Öncesi / sonrası", "carousel", "Solda ham görüntü, sağda teslim edilen kare",
  "Aradaki farkı anlatmanın en hızlı yolu; fiyat itirazını da buradan karşılıyorsun."),
 ("Çekim günü kamera arkası", "reels", "Kurulum, ışık, monitör başı karar anı",
  "İşin nasıl yapıldığını gören müşteri fiyatı sorgulamıyor."),
 ("Tek çekim, üç sürüm", "carousel", "Aynı iş yatay, kare ve dikey olarak yan yana",
  "Rakiplerin çoğu ayrı ayrı ücretlendiriyor; bu görsel tek başına ayrıştırıyor."),
 ("Kameranın giremediği yer", "reels", "Gerçek çekimden 3D'ye geçiş anı",
  "3D ile çekimi aynı ekipte yaptığımızın kanıtı."),
 ("Sektör anlatımı", "tekli", "İnşaatta / sanayide / otelde ne işe yarıyor",
  "Farkında olmayan tarafı içeri çeken tek içerik türü."),
 ("Ekip", "reels", "Kim çekiyor, kim kurguyor, kim modelliyor",
  "Görsel işte insan seçiliyor; tanıdıklık iş getiriyor."),
 ("Teslim paketi", "carousel", "Bir işte teslim edilen dosyaların tamamı",
  "Kapsam belirsizliğini bitiriyor; teklif aşamasını kısaltıyor."),
],
"insaat": [
 ("Şantiyede bir ay", "reels", "Aynı açıdan çekilmiş 4 kare, 15 saniyede yükselen bina",
  "İlerleme videosu güven veriyor; alıcı 'bu iş gerçekten yürüyor' diyor. Aynı içerik yatırımcı raporu olarak da kullanılıyor."),
 ("Daire içinde tek plan tur", "reels", "Kapıdan girip balkona çıkan kesintisiz çekim",
  "Metrekare rakamı hiç kimseye bir şey anlatmıyor; içinde yürünen oda anlatıyor."),
 ("Manzara kanıtı", "reels", "Dairenin penceresinden gerçek manzara, kat numarasıyla",
  "En çok sorulan soru bu. Cevabı videoyla verildiğinde satış ofisindeki tartışma bitiyor."),
 ("3D render → gerçek teslim", "carousel", "Solda render, sağda teslim edilmiş hali",
  "Söz verilen ile teslim edilenin aynı olduğunu gösteren en güçlü kanıt; rakiplerin çoğu bunu yapamıyor."),
 ("Kat planı anlatımı", "carousel", "Plan üzerinde ok ve notlarla oda oda gezinti",
  "Plan okumayı bilmeyen alıcı, planı anladığı an karar sürecine giriyor."),
 ("Malzeme yakın planı", "tekli", "Cephe kaplaması, doğrama, zemin dokusunun makro görüntüsü",
  "Kalite iddiası sözle değil dokuyla anlatılır; fiyat itirazını buradan karşılıyorsun."),
 ("Ustanın anlattığı 30 saniye", "reels", "Şantiye şefi tek bir teknik detayı anlatıyor",
  "İnsan yüzü olan içerik güven kuruyor; kurumsal dil yerine saha dili çalışıyor."),
 ("Bölge anlatımı", "reels", "Projeden okula/metroya kadar yürüyüş çekimi",
  "Konum avantajı harita ekran görüntüsüyle değil, yürüyerek anlatılınca inandırıcı oluyor."),
 ("Teslim günü", "reels", "Anahtar teslimi anı, aile kadrajda",
  "Sosyal kanıt. Bir sonraki alıcının 'burada insanlar gerçekten oturuyor' demesini sağlıyor."),
 ("Sık sorulan soru serisi", "carousel", "Tek soru, net cevap, marka rengi",
  "Satış ekibinin telefonda tekrar tekrar anlattığı şeyi bir kez üretip sonsuz kez kullanıyorsun."),
],
"emlak": [
 ("60 saniyede ev turu", "reels", "Girişten balkona akıcı tek plan, altyazılı temel bilgiler",
  "İlanı gezmeden önce izleyen alıcı, gezmeye geldiğinde kararının yarısını vermiş oluyor."),
 ("Konum yürüyüşü", "reels", "Evden en yakın markete/okula kadar yürüyüş",
  "Alıcının ikinci sorusu her zaman konum. Haritayla değil, adımla anlatınca ikna oluyor."),
 ("Bu evi kim alır", "tekli", "Tek görsel + 'kim için uygun' notu",
  "Yanlış alıcıyı eleyerek gelen aramanın kalitesini yükseltiyor; boş gezdirme azalıyor."),
 ("Fiyat neden bu", "carousel", "Bölge kıyaslaması, metrekare, kat, cephe",
  "Fiyat itirazını pazarlık masasında değil, ilan aşamasında karşılıyorsun."),
 ("Boş daire → döşenmiş hali", "carousel", "Dijital mobilyalama öncesi/sonrası",
  "Boş mekân soğuk durur; döşenmiş hali alıcıya kendini o evde hayal ettirir."),
 ("Satıldı", "reels", "Anahtar teslim anı, kısa ve sade",
  "Sosyal kanıt; portföy sahibi de bunu görüp 'benim evi de bu ofis satsın' diyor."),
 ("Danışmanın yüzü", "reels", "Bir emlak ipucu, doğrudan kameraya",
  "Emlakta güven kişiye kurulur, ofise değil. Yüz görünmeyen hesap portföy toplayamıyor."),
 ("Bölge raporu", "carousel", "Mahallenin bu ayki ortalama fiyatı ve hareketi",
  "Uzmanlık algısı yaratıyor; satıcı mülkünü sana emanet etmek için bunu arıyor."),
 ("Drone açılışı", "reels", "Havadan yaklaşan tek plan, sonra binaya iniş",
  "İlk 3 saniyede durdurma gücü en yüksek format; kaydırmayı kesiyor."),
],
"mimarlik": [
 ("Eskizden render'a", "carousel", "El çizimi → 3D → gerçek fotoğraf",
  "Süreci gösteren içerik, işin arkasındaki emeği görünür kılıyor; fiyat pazarlığını yumuşatıyor."),
 ("Detay yakın planı", "tekli", "Bir birleşim detayı, sade kadraj",
  "Meslektaş ve müteahhit kitlesi bu tür içeriği paylaşıyor; iş buradan geliyor."),
 ("Proje turu", "reels", "3D animasyondan 30 saniyelik kesit",
  "İşveren adayı animasyonu görünce 'benim projemi de böyle anlat' diyor."),
 ("Malzeme paleti", "carousel", "Projede kullanılan malzemelerin yan yana görüntüsü",
  "Estetik dil kurar; hesabın kimliğini belirginleştirir."),
 ("Önce/sonra", "carousel", "Tadilat öncesi ve sonrası aynı açı",
  "En yüksek etkileşimi alan mimari içerik türü; paylaşılma oranı yüksek."),
 ("Şantiye ziyareti", "reels", "Uygulamada bir detayın kontrolü",
  "Mimarın sadece çizmediğini, işi takip ettiğini gösteriyor — işveren güveni buradan geliyor."),
],
"sanayi": [
 ("Makine çalışırken", "reels", "Üretim hattından 15 saniyelik ritmik kesit",
  "Sanayide en çok izlenen içerik makinenin gerçekten çalıştığı an; ihracat müşterisi bunu arıyor."),
 ("Ürünün içi", "reels", "3D kesit animasyonu — kapalı gövde şeffaflaşıyor",
  "Teknik satışta müşterinin 'anladım' dediği an burası; tercümana ihtiyaç kalmıyor."),
 ("Fabrika turu", "uzun", "Hammaddeden paketlemeye tek çekim",
  "Yurt dışı müşteri tesisi göremiyor; bu video ziyaretin yerini tutuyor ve güven kuruyor."),
 ("Fuar hazırlığı ve stand", "reels", "Kurulum ve stand anları",
  "Fuar öncesi görünürlük randevu getiriyor; fuar sonrası da hatırlatma malzemesi oluyor."),
 ("Kalite kontrol anı", "tekli", "Ölçüm yapılırken çekilmiş net kare",
  "Kalite iddiası sertifika logosuyla değil, ölçüm yapan elle inandırıcı oluyor."),
 ("Sayılarla kapasite", "carousel", "Aylık üretim, hat sayısı, ihracat ülkesi",
  "B2B alıcı önce kapasiteye bakıyor; bu bilgi LinkedIn'de doğrudan teklif çağrısı getiriyor."),
 ("Montaj adım adım", "carousel", "Patlatılmış görünümden montaja",
  "Bayi ve servis ağı için eğitim malzemesi; aynı içerik satış argümanı olarak da çalışıyor."),
 ("Ekipten bir yüz", "reels", "Ustabaşı işini anlatıyor",
  "İşveren markası kuruyor; nitelikli eleman bulmayı da kolaylaştırıyor."),
],
"mobilya": [
 ("Tek üründen 6 varyant", "carousel", "Aynı model, farklı kumaş ve renk",
  "3D modelden üretildiği için her varyant için ayrı çekim maliyeti yok; müşteri seçeneği görünce sepete giriyor."),
 ("Mekâna yerleşim", "reels", "Ürün boş odaya yerleşiyor, oda dolu hale geliyor",
  "Müşteri ürünü kendi evinde hayal edemiyor; bu içerik o boşluğu dolduruyor."),
 ("Montaj hızlandırılmış", "reels", "Kutudan çıkıştan kuruluma 20 saniye",
  "En büyük satın alma engeli 'kurulumu zor mu' sorusu; video onu ortadan kaldırıyor."),
 ("Malzeme yakın planı", "tekli", "Kumaş dokusu, ahşap damarı makro",
  "Online satışta dokunamayan müşteri için tek kalite kanıtı bu."),
 ("Showroom turu", "reels", "Mağaza içinde akıcı gezinti",
  "Mağazaya trafik çekmenin en doğrudan yolu; yerel erişim yüksek."),
 ("Ölçü ve kullanım", "carousel", "Ürün ölçüleri ve hangi mekâna uyduğu",
  "İade oranını düşürüyor; müşteri doğru ürünü seçiyor."),
],
"otel": [
 ("Odaya giriş anı", "reels", "Kapı açılıyor, manzara ortaya çıkıyor",
  "Rezervasyon kararı çoğunlukla bu üç saniyede veriliyor."),
 ("Sabah kahvaltısı", "reels", "Servis ve masa detayları, doğal ışık",
  "Otel seçiminde ikinci karar noktası kahvaltı; görselle anlatılınca fiyat sorgusu azalıyor."),
 ("Tesisten çevreye", "reels", "Havadan tesis, sonra çevredeki gezilecek yer",
  "Misafir sadece oteli değil tatili satın alıyor; çevre anlatımı doluluk süresini uzatıyor."),
 ("Bir günlük program", "carousel", "Sabahtan akşama misafir günü",
  "Tereddüt eden misafire 'burada ne yapacağım' sorusunun cevabını veriyor."),
 ("Personelden bir yüz", "reels", "Şef ya da resepsiyon, kısa selam",
  "Sıcaklık algısı kuruyor; özellikle butik tesislerde tercih sebebi."),
 ("Misafir yorumundan içeriğe", "tekli", "Gerçek yorum alıntısı, tesis görseli üstünde",
  "Sosyal kanıt; yorum sayfada kalmak yerine akışta dolaşıyor."),
],
"isletme": [
 ("Günün hazırlığı", "reels", "Açılıştan önceki 30 saniye, ışıklar yanıyor",
  "Mekânın temizliği ve düzeni sözle değil görüntüyle anlatılıyor; ilk ziyaret kararını bu belirliyor."),
 ("Ürün yakın planı", "reels", "Yavaş çekim, doğal ışık, ses açık",
  "Yiyecek/ürün içeriğinde ses ve doku iştah açıyor; en yüksek kaydetme oranı burada."),
 ("Ekipten bir yüz", "reels", "Çalışan kendini tanıtıyor",
  "Yerel işletmede müşteri mekâna değil insana bağlanıyor."),
 ("Müşteri anı", "story", "İzinli çekilmiş kısa an, etiketli",
  "Sosyal kanıt; etiketlenen müşteri kendi çevresine yayıyor, erişim organik büyüyor."),
 ("Menü/hizmet tanıtımı", "carousel", "Her kartta bir ürün, fiyat ve öne çıkan not",
  "En çok kaydedilen içerik türü; müşteri gelmeden ne alacağına karar veriyor."),
 ("Arkada ne oluyor", "reels", "Hazırlık süreci, mutfak veya atölye",
  "Şeffaflık güven kuruyor; hijyen ve kalite algısını sözsüz veriyor."),
 ("Yeni ürün duyurusu", "reels", "İlk 1 saniyede ürün ekranda",
  "Duyuru içeriği en hızlı dönüşen tür; aynı gün ciroya yansıyor."),
 ("Yol tarifi", "reels", "Bilinen bir noktadan işletmeye yürüyüş",
  "Yerel keşfi kolaylaştırıyor; haritada bulunamayan işletme için kritik."),
],
}


def icerik_plani(sektor, adet=8):
    ham = PLAN.get(sektor) or PLAN["isletme"]
    return [{"baslik": b, "format": f, "format_ad": FORMAT_AD.get(f, f), "kanca": k, "neden": n}
            for b, f, k, n in ham[:adet]]


# Sektöre göre önerilen aylık üretim temposu
TEMPO = {
 "produksiyon": {"reels": 8, "carousel": 4, "tekli": 2, "story": 12, "uzun": 2},
 "insaat":   {"reels": 6, "carousel": 3, "tekli": 3, "story": 12, "uzun": 1},
 "emlak":    {"reels": 8, "carousel": 4, "tekli": 4, "story": 16, "uzun": 1},
 "mimarlik": {"reels": 4, "carousel": 4, "tekli": 6, "story": 8,  "uzun": 1},
 "sanayi":   {"reels": 5, "carousel": 3, "tekli": 3, "story": 6,  "uzun": 1},
 "mobilya":  {"reels": 8, "carousel": 4, "tekli": 6, "story": 12, "uzun": 1},
 "otel":     {"reels": 10, "carousel": 3, "tekli": 5, "story": 20, "uzun": 1},
 "isletme":  {"reels": 8, "carousel": 3, "tekli": 4, "story": 16, "uzun": 0},
}
