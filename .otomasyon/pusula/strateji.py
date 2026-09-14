# -*- coding: utf-8 -*-
"""
PAZARLAMA STRATEJİSİ — adayın verisinden tam bir strateji belgesi çıkarır.

Bu bir şablon doldurma değil. Belge, o firma için toplanan gerçek bulgulardan
kuruluyor: karne notları, kanıtlı eksikler, sosyal denetim, harita profili,
sektör ve şehir. Aynı sektörden iki firma farklı belge alıyor, çünkü zayıf
oldukları yer farklı.

Belgenin omurgası:
  1. Bugün nerede duruyoruz      — beş başlıkta karne, kanıtla
  2. Kime satıyoruz              — katmanlı hedef kitle, satın alma tetikleyicisi
  3. Nerede konumlanıyoruz       — rakibin söylemediği, bizim söyleyebileceğimiz
  4. Hangi kanal, neden          — kanal dağılımı ve gerekçesi (moda değil, sebep)
  5. Ne anlatacağız              — içerik sütunları ve her birinin işi
  6. 30 / 60 / 90 gün            — sırayla ne yapılacak
  7. Huni matematiği             — kaç görüntülenme kaç işe dönüyor (varsayımlı)
  8. Bütçe dağılımı              — para nereye, hangi oranla
  9. Ne ölçeceğiz                — KPI, hedef, ölçüm yeri, ölçüm sıklığı
 10. Riskler                     — ne ters gidebilir, önlemi ne

Rakamların tamamı VARSAYIM olarak işaretleniyor. Uydurma kesinlik satmıyoruz.
"""
import datetime

from .ayarlar import SEKTORLER, MODEL
from .puanlama import karne, en_zayif_grup, ETIKET, GRUP_KISA
from . import fark as FK
from . import sosyal as SO
from .ayarlar import FIRMA
from . import strateji_html as SH


# ------------------------------------------------------------------ hedef kitle katmanları
# Her sektörde üç katman: şimdi alacak / araştıran / farkında olmayan.
# Strateji bu üçünü aynı anda değil, SIRAYLA hedefliyor.
KATMAN = {
"produksiyon": [
 ("Şimdi iş verecek", "Projesi/lansmanı var, tarih belli, ekip arıyor",
  "Bu ekip bu işi daha önce yapmış mı, teslim ediyor mu", "Sektöre eşlenmiş referans + çekim planı"),
 ("Araştıran", "İhtiyacı fark etmiş, fiyat ve kapsam öğreniyor",
  "Ne kadar tutar, ne kadar sürer, neye karar vermem gerekiyor",
  "Fiyatı neyin belirlediğini anlatan içerik + paket sayfası"),
 ("Farkında olmayan", "Video/3D'yi masraf sayıyor, işine yarayacağını görmemiş",
  "Aynı işi yapanlar bununla ne kazanıyor",
  "Öncesi/sonrası kanıt içerikleri + sektörel örnek"),
],
"insaat": [
 ("Şimdi alacak", "Bütçesi hazır, bölge seçmiş, iki-üç proje arasında karşılaştırıyor",
  "Manzara, kat, teslim tarihi ve komşu proje kıyası", "Proje tanıtım videosu + daire içi tur"),
 ("Araştıran", "Taşınmayı düşünüyor, hangi bölge diye bakıyor, aciliyeti yok",
  "Bölge gelişimi, ulaşım, okul, yatırım getirisi", "Bölge anlatım içeriği + ilerleme kaydı"),
 ("Farkında olmayan", "Yatırım arayan, gayrimenkulü seçenek olarak görmemiş",
  "Alternatif yatırımlara göre kıyas, kira getirisi", "Rakamlı kısa içerik + hesap örneği"),
],
"emlak": [
 ("Şimdi alacak", "Kredi onayı almış ya da nakdi hazır, bu ay bakıyor",
  "Portföyün gerçek hâli, fiyatın neden o olduğu", "Her portföye video + tek plan tur"),
 ("Araştıran", "Fiyat izliyor, bölge karşılaştırıyor",
  "Bölge fiyat hareketi, hangi mahalle neden", "Bölge raporu içeriği + danışman görünürlüğü"),
 ("Mal sahibi", "Satmak/kiralamak istiyor, hangi ofise vereceğine karar vermemiş",
  "Bu ofis benim evimi nasıl pazarlayacak", "Yapılmış iş vitrini — portföy tanıtım örnekleri"),
],
"mimarlik": [
 ("İşveren", "Projesi olan, ofis seçen kurumsal ya da bireysel yatırımcı",
  "Bu ofis anlatabiliyor mu, teslim ediyor mu", "Sunum videosu + tamamlanmış iş dosyası"),
 ("Müteahhit ortağı", "Sürekli iş verecek yapı firması",
  "Hız, revizyon disiplini, uyum", "Süreç anlatımı + teslim disiplini içeriği"),
 ("Meslek çevresi", "Yarışma, iş birliği, tedarikçi ağı",
  "İşin kalitesi ve dili", "Detay ve malzeme içerikleri"),
],
"sanayi": [
 ("Alım yapan", "İhtiyacı belirlenmiş, teklif topluyor",
  "Makine ne yapıyor, kapasitesi ne, servis nasıl", "Kesit animasyonu + kapasite anlatımı"),
 ("İhracat kanalı", "Yurt dışı distribütör/temsilci",
  "Ürünü kendi dilinde anlatabilme", "Çok dilli altyazılı anlatım videosu"),
 ("Fuar ziyaretçisi", "Standın önünden geçen, üç saniyede karar veren",
  "Ekranda ne dönüyor", "Sessiz izlenebilen döngü videosu"),
],
"mobilya": [
 ("Nihai tüketici", "Evine ürün arıyor, görselden karar veriyor",
  "Ürün evimde nasıl durur, ölçüsü uyar mı", "Mekâna yerleştirilmiş görsel + ölçek videosu"),
 ("Bayi / proje", "Toplu alım yapan, katalog isteyen",
  "Varyant çeşitliliği, teslim süresi", "Varyant görselleri + üretim kapasitesi anlatımı"),
 ("İç mimar", "Projesine ürün seçen",
  "Teknik çizim, malzeme, doku", "Malzeme makro çekimleri + teknik dosya"),
],
"otel": [
 ("Doğrudan rezervasyon", "Tesisi biliyor, acenteye komisyon vermek istemiyor",
  "Doğrudan almanın avantajı", "Tesis turu + doğrudan rezervasyon çağrısı"),
 ("Karar aşamasında", "Üç-beş tesis arasında seçiyor",
  "Oda gerçekte nasıl, manzara doğru mu", "Gerçek ölçekli oda videosu + manzara kanıtı"),
 ("Grup / kurumsal", "Toplantı, düğün, organizasyon arıyor",
  "Kapasite, salon, teknik altyapı", "Etkinlik alanı turu + geçmiş organizasyon"),
],
"isletme": [
 ("Yakındaki müşteri", "Şu an ihtiyacı var, haritadan arıyor",
  "Açık mı, nerede, ne kadar", "Harita profili + kısa tanıtım videosu"),
 ("Tekrar gelen", "Bir kere geldi, hatırlatılması gerekiyor",
  "Yeni ne var", "Düzenli içerik + kampanya duyurusu"),
 ("Hiç duymamış", "Aynı şehirde ama işletmeyi bilmiyor",
  "Bu iş neden farklı", "İşin yapılışını gösteren içerik"),
],
}


# ------------------------------------------------------------------ içerik sütunları
# Her sütunun BİR işi var. "İçerik üretelim" değil, "bu içerik şunu çözecek".
SUTUN = {
"produksiyon": [
 ("İş", "Tamamlanmış çalışmalar, öncesi/sonrası, kamera arkası",
  "Yetkinliği kanıtlar — asıl satan sütun", 40),
 ("Nasıl yapılıyor", "Çekim planı, ışık kurulumu, kurgu kararları",
  "Fiyatın neden o olduğunu anlatır, pazarlığı bitirir", 25),
 ("Sektör anlatımı", "İnşaatta/sanayide/otelde ne işe yarıyor",
  "Farkında olmayan tarafı içeri çeker", 20),
 ("Ekip", "Kim çekiyor, kim kurguyor",
  "Görsel işte insan seçilir; tanıdıklık üretir", 15),
],
"insaat": [
 ("Kanıt", "Şantiye ilerlemesi, teslim edilen iş, söz–gerçek kıyası",
  "Projenin biteceğine ikna eder", 35),
 ("Ürün", "Daire içi tur, kat planı anlatımı, manzara", "Alıcının kafasındaki soruyu bitirir", 30),
 ("Bölge", "Ulaşım, okul, gelişim, yatırım değeri", "Henüz bölge seçmemiş alıcıyı çeker", 20),
 ("İnsan", "Ekip, usta, satış danışmanı", "Firmayı tanıdık kılar", 15),
],
"emlak": [
 ("Portföy", "Her ilan için tur videosu", "Doğrudan satış üretir", 40),
 ("Bölge", "Mahalle anlatımı, fiyat hareketi", "Araştıran alıcıyı yakalar", 25),
 ("Danışman", "Yüz, ses, tecrübe", "Emlakta insan seçilir", 20),
 ("Eğitim", "Kredi, tapu, süreç anlatımı", "Güven ve arama trafiği üretir", 15),
],
"mimarlik": [
 ("Proje", "Tamamlanmış iş sunumu", "Yetkinlik kanıtı", 40),
 ("Süreç", "Eskizden teslime yolculuk", "Çalışma disiplinini gösterir", 25),
 ("Detay", "Malzeme, doku, birleşim", "Meslek çevresinde itibar", 20),
 ("Görüş", "Yaklaşım, tercih, eleştiri", "Ayrışma yaratır", 15),
],
"sanayi": [
 ("Ürün", "Makine/ürün anlatımı, kesit animasyonu", "Teklif aşamasını kısaltır", 40),
 ("Kapasite", "Tesis, hat, kalite kontrol", "Büyük alıcıyı ikna eder", 25),
 ("Referans", "Kimler kullanıyor, nerede çalışıyor", "Risk algısını düşürür", 20),
 ("Fuar/etkinlik", "Katılım, lansman, duyuru", "Kanal ve ilişki üretir", 15),
],
"mobilya": [
 ("Ürün mekânda", "Gerçek/3D mekâna yerleştirme", "Satın alma kararını tetikler", 40),
 ("Detay", "Kumaş, ahşap, mekanizma", "Fiyat itirazını karşılar", 25),
 ("Varyant", "Renk, ölçü, seçenekler", "Karar kolaylaştırır", 20),
 ("Üretim", "Nasıl yapıldığı", "Kalite iddiasını kanıtlar", 15),
],
"otel": [
 ("Tesis", "Oda, genel alan, manzara", "Rezervasyon üretir", 40),
 ("Deneyim", "Kahvaltı, aktivite, çevre", "Farkı anlatır", 25),
 ("Misafir", "Gerçek misafir anları ve sözleri", "Güven verir", 20),
 ("Sezon", "Dönemsel duyuru, erken rezervasyon", "Aciliyet yaratır", 15),
],
"isletme": [
 ("İş başında", "İşin yapılışı, ustalık anı", "Kalite iddiasını kanıtlar", 35),
 ("Ürün/hizmet", "Ne sunulduğu, fiyat aralığı", "Elemeyi ziyaretçide yapar", 30),
 ("İnsan", "Sahibi, ekip, hikâye", "Yerelde tanıdıklık üretir", 20),
 ("Müşteri", "Gerçek müşteri sözü", "Güven verir", 15),
],
}


# ------------------------------------------------------------------ konumlandırma
KONUM = {
"produksiyon": ("Prodüksiyon tarafında herkes 'sinematik', 'profesyonel', 'yaratıcı' diyor — "
                "bu kelimelerin hiçbiri ayrıştırmıyor. Luna'nın ayrıştığı yer üç somut şey: "
                "(1) tek çekimden yatay+kare+dikey sürümlerin birlikte teslim edilmesi, "
                "(2) kameranın gösteremediği yerde 3D'nin devreye girmesi — ikisi aynı ekipte, "
                "(3) yazılımı da kendi yazan bir ekip olması: videodan gelen talebin nereye "
                "düştüğü de çözülüyor. Rakiplerin çoğu bu üçünden birini yapabiliyor, üçünü birden değil."),
"insaat": ("Çoğu müteahhit 'kaliteli malzeme, zamanında teslim' diyor — hepsi aynı cümle. "
           "Ayrışma iddiada değil, KANITTA: haftalık ilerleme kaydı tutan ve teslimde "
           "render ile gerçeği yan yana koyan firma, aynı cümleyi kuran on firmadan ayrılıyor."),
"emlak": ("Portföy herkeste benzer, fiyat piyasa belirliyor. Ayrışma danışmanın kendisinde "
          "ve mülkü nasıl gösterdiğinde. Videolu ilan yapan ofis, mal sahibinin gözünde "
          "'evimi daha iyi pazarlar' oluyor — portföy oradan geliyor."),
"mimarlik": ("Görsel kalitesi artık ayrıştırıcı değil, herkes iyi render alıyor. Ayrışma "
             "ANLATIMDA: projeyi jüriye/işverene iki dakikada anlatabilen ofis kazanıyor."),
"sanayi": ("Teknik üstünlük katalogda anlatılamıyor; rakamlar birbirine benziyor. Ayrışma "
           "GÖRÜNMEYENİ GÖSTERMEKTE: makinenin içinde ne olduğunu gösteren firma, "
           "aynı özellikleri listeleyen rakibinden önde başlıyor."),
"mobilya": ("Ürün fotoğrafı herkeste var. Ayrışma BAĞLAMDA: ürünü boş bir fonda değil, "
            "alıcının hayal edebileceği bir mekânda gösteren marka satıyor."),
"otel": ("Fotoğraflar hep en iyi açıdan; misafir buna güvenmiyor. Ayrışma DÜRÜSTLÜKTE: "
         "gerçek ölçekte oda videosu ve doğru saatte manzara, geniş açı şişirmesinden "
         "daha çok rezervasyon getiriyor."),
"isletme": ("Yerelde herkes 'kaliteli hizmet' diyor. Ayrışma İŞİN KENDİSİNİ GÖSTERMEKTE: "
            "nasıl yapıldığını gösteren işletme, iddia eden işletmeden ayrılıyor."),
}


# ------------------------------------------------------------------ riskler
RISK = [
 ("İçerik üretilir ama yayınlanmaz", "En sık görülen ölüm sebebi. Çekim yapılır, kurgu biter, "
  "yayın kimsenin işi olmadığı için durur.",
  "Yayın takvimi ay başında yazılı çıkar ve tek bir kişiye zimmetlenir."),
 ("İlk aydan sonuç beklenir", "İki hafta sonra 'işe yaramadı' kararı verilir ve bırakılır.",
  "İlk ay ölçüm ayı olarak konuşulur; kıyas ikinci aydan başlar."),
 ("Beğeni sayısı başarı sanılır", "Erişim artar, telefon çalmaz; kimse fark etmez.",
  "Ölçülen şey beğeni değil: gelen arama, harita görüntülenmesi, 'buradan gördüm' diyen müşteri."),
 ("Her platforma aynı içerik atılır", "Yatay video dikey akışta kenarları boş çıkar, izlenmez.",
  "Tek çekimden platforma göre ayrı sürümler teslim edilir."),
 ("Çekim gününde hazırlık olmaz", "Mekân dağınık, yetkili yok, ürün hazır değil; gün yanar.",
  "Çekimden üç gün önce hazırlık listesi gönderilir ve teyit alınır."),
]


# ------------------------------------------------------------------ üretim
def _pay(sozluk_listesi):
    t = sum(x[3] for x in sozluk_listesi) or 1
    return [(a, b, c, round(100.0 * d / t)) for a, b, c, d in sozluk_listesi]


def uret(aday, eksikler, detay, tahmin, sosyal=None, bedel=None):
    """Adayın verisinden strateji sözlüğü üretir."""
    sektor = aday.get("sektor") or "isletme"
    sk = SEKTORLER.get(sektor, {})
    kn = karne(eksikler)
    zayif = en_zayif_grup(eksikler)
    sosyal = sosyal or {}
    hesaplar = sosyal.get("hesaplar") or {}
    beklenen = [p for p, _, _ in (sosyal.get("beklenen") or SO.SEKTOR_PLATFORM.get(sektor, []))]
    eksik_platform = [p for p in beklenen if p not in hesaplar]

    # --- kanal dağılımı: eksik platform + sektör ağırlığı
    kanal = []
    for p, agirlik, neden in (sosyal.get("beklenen") or SO.SEKTOR_PLATFORM.get(sektor, [])):
        var = p in hesaplar
        kanal.append({
            "platform": SO.PLATFORM.get(p, {}).get("ad", p),
            "anahtar": p, "oncelik": agirlik, "var": var, "neden": neden,
            "durum": ("var — iyileştirilecek" if var else "yok — kurulacak"),
        })
    kanal.sort(key=lambda k: (k["var"], -k["oncelik"]))

    # --- huni matematiği (varsayım)
    mevcut_g = tahmin.get("mevcut_goruntulenme") or 0
    hedef_g = tahmin.get("hedef_goruntulenme") or 0
    d1 = MODEL["donusum_mevcut"]; d2 = MODEL["donusum_iyilesmis"]; kap = MODEL["kapanis_orani"]
    huni = [
        ("Görüntülenme", mevcut_g, hedef_g, "Arama + harita + sosyal toplamı"),
        ("İletişim", int(mevcut_g * d1), int(hedef_g * d2),
         "Arayan, mesaj atan, yol tarifi isteyen"),
        ("Görüşme", int(mevcut_g * d1 * 0.6), int(hedef_g * d2 * 0.6),
         "Gerçekten konuşulan (varsayım: iletişimin %60'ı)"),
        ("İş", int(mevcut_g * d1 * kap), int(hedef_g * d2 * kap), "Kapanan iş"),
    ]

    # --- 30/60/90
    yol = _yol_haritasi(sektor, zayif, eksikler, eksik_platform, hesaplar)

    # --- bütçe dağılımı
    butce = _butce(sektor, bool(eksik_platform), zayif["anahtar"])

    # --- KPI
    kpi = [
        ("Gelen arama", "Harita profili → 'Aramalar' raporu", "Aylık", "+%40 (3. ay)"),
        ("Harita görüntülenmesi", "Google İşletme Profili istatistikleri", "Aylık", "+%60 (3. ay)"),
        ("Yol tarifi isteği", "Harita profili", "Aylık", "+%30 (3. ay)"),
        ("Site oturumu", "GA4 / Search Console", "Haftalık", "+%50 (3. ay)"),
        ("Sosyal → site tıklaması", "GA4 kaynak raporu", "Haftalık", "İlk ay taban ölçümü"),
        ("'Buradan gördüm' diyen müşteri", "Satış ekibi tek soruyla sorar ve çeteleye yazar",
         "Günlük", "Ayda en az 5 (2. ay)"),
        ("Etkileşim oranı", "Platform istatistikleri", "Aylık", "Sektör ortalaması üstü"),
    ]

    return {
        "firma": aday["ad"], "sehir": aday.get("sehir") or "", "sektor": sektor,
        "sektor_ad": sk.get("ad", sektor),
        "zaman": datetime.datetime.now().strftime("%d.%m.%Y"),
        "karne": kn, "zayif": zayif,
        "konumlandirma": KONUM.get(sektor, KONUM["isletme"]),
        "katman": KATMAN.get(sektor, KATMAN["isletme"]),
        "sutun": _pay(SUTUN.get(sektor, SUTUN["isletme"])),
        "kanal": kanal,
        "eksik_platform": eksik_platform,
        "sosyal_eksik": (sosyal.get("eksikler") or [])[:8],
        "tempo": SO.TEMPO.get(sektor, SO.TEMPO["isletme"]),
        "huni": huni,
        "varsayim": {"donusum_mevcut": d1, "donusum_iyilesmis": d2, "kapanis": kap},
        "yol": yol,
        "butce": butce,
        "kpi": kpi,
        "risk": RISK,
        "fark": FK.farklar(sektor, 3),
        "model": FK.model(sektor),
        "bedel": bedel,
    }


def _yol_haritasi(sektor, zayif, eksikler, eksik_platform, hesaplar):
    """En zayıf başlıktan başlayan 30/60/90 planı."""
    e = set(eksikler)
    otuz, altmis, doksan = [], [], []

    # 0-30: kanamayı durdur — dönüşüm ve temel görünürlük
    if "cta_yok" in e or "whatsapp_yok" in e or "tel_tiklanmaz" in e:
        otuz.append("Sitede tek ve net bir eylem çağrısı + sabit WhatsApp butonu + "
                    "tıklanabilir telefon (yarım gün iş, en hızlı kazanç)")
    if "form_yok" in e:
        otuz.append("Kısa iletişim formu — mesai dışı gelen talebi yakalar")
    if "sema_yok" in e or "iletisim_sayfasi_yok" in e:
        otuz.append("İşletme şeması (LocalBusiness) ve iletişim sayfası")
    if "gorsel_az" in e:
        otuz.append("Harita profili için profesyonel fotoğraf çekimi ve yükleme")
    if eksik_platform:
        otuz.append("Eksik platformların açılması: %s — profil, bio, bağlantı, kapak"
                    % ", ".join(SO.PLATFORM.get(p, {}).get("ad", p) for p in eksik_platform))
    otuz.append("İlk çekim günü: bir günde bir aylık içerik (uzun video + kısa kesitler + kapaklar)")
    otuz.append("Ölçüm taban çizgisi: mevcut arama, görüntülenme ve 'buradan gördüm' sayısı yazılır")

    # 30-60: birikim
    if "video_yok" in e:
        altmis.append("Ana tanıtım videosunun siteye ve harita profiline yerleştirilmesi")
    if "referans_yok" in e or "yorum_gomulu_yok" in e:
        altmis.append("Referans galerisi ve müşteri sözü çekimi (30 saniyelik video görüş)")
    if "sss_yok" in e or "blog_yok" in e:
        altmis.append("SSS bölümü + ilk iki blog yazısı (aramada soru kutusuna çıkmak için)")
    altmis.append("İkinci çekim günü + ilk ayın ölçümüne göre içerik planının güncellenmesi")
    altmis.append("Yorum toplama akışı: QR kart / SMS hatırlatma (harita puanını taşır)")

    # 60-90: ölçekleme
    if "hizmet_sayfasi_yok" in e or "icerik_sig" in e:
        doksan.append("Her hizmete ayrı sayfa + kendi videosu (arama trafiğini böler ve büyütür)")
    doksan.append("En çok işe yarayan iki içerik biçiminin çoğaltılması, işe yaramayanın bırakılması")
    doksan.append("Ölçüm karşılaştırması: 1. ay tabanı ile 3. ay — devam kararı burada verilir")
    doksan.append("İşe yarayan içeriğe küçük bütçeli reklam desteği (organik kanıtlanmadan reklam yok)")

    return [
        {"donem": "0–30 gün", "baslik": "Kanamayı durdur",
         "amac": "En zayıf başlık: %s. Önce buradaki kaybı kes." % zayif.get("kisa", zayif["baslik"]),
         "adim": otuz},
        {"donem": "30–60 gün", "baslik": "Biriktir",
         "amac": "İçerik ve kanıt birikmeye başlasın; ilk ölçüm okunsun.", "adim": altmis},
        {"donem": "60–90 gün", "baslik": "Ölç ve büyüt",
         "amac": "İşe yarayanı çoğalt, yaramayanı bırak; devam kararını rakama bağla.",
         "adim": doksan},
    ]


def _butce(sektor, platform_eksik, zayif_anahtar):
    """Bütçe dağılımı — para nereye. Toplam 100."""
    d = {"Üretim (çekim + kurgu)": 55, "Site ve teknik düzeltme": 15,
         "Harita ve profil düzeni": 10, "Reklam (test bütçesi)": 10, "Ölçüm ve raporlama": 10}
    if zayif_anahtar in ("gorunurluk", "teknik"):
        d["Site ve teknik düzeltme"] += 10
        d["Üretim (çekim + kurgu)"] -= 10
    if platform_eksik:
        d["Harita ve profil düzeni"] += 5
        d["Reklam (test bütçesi)"] -= 5
    return [{"kalem": k, "yuzde": v,
             "not": _butce_not(k)} for k, v in sorted(d.items(), key=lambda x: -x[1])]


def _butce_not(kalem):
    return {
        "Üretim (çekim + kurgu)": "Asıl değer burada üretiliyor; kısılırsa geri kalanı taşıyacak "
                                  "malzeme kalmıyor.",
        "Site ve teknik düzeltme": "Gelen trafiğin düştüğü yer. Buradaki eksik, üretilen her "
                                   "içeriğin getirisini düşürüyor.",
        "Harita ve profil düzeni": "Yerel işte en ucuz kazanç. Fotoğraf, bilgi, yorum akışı.",
        "Reklam (test bütçesi)": "Organik olarak tuttuğu kanıtlanan içeriğe destek. "
                                 "Kanıtlanmadan reklam verilmiyor.",
        "Ölçüm ve raporlama": "Ölçülmeyen iş tekrar edilemez. Bu kalem kısılırsa "
                              "üç ay sonra neyin işe yaradığı bilinmiyor.",
    }.get(kalem, "")


# ------------------------------------------------------------------ belge
def yaz(aday, eksikler, detay, tahmin, klasor, sosyal=None, bedel=None):
    """Strateji belgesini klasöre yazar; (yol, strateji_sozlugu) döner."""
    import os
    s = uret(aday, eksikler, detay, tahmin, sosyal, bedel)
    yol = os.path.join(klasor, "strateji.html")
    with open(yol, "w", encoding="utf-8") as f:
        f.write(SH.sayfa(s, FIRMA))
    return yol, s
