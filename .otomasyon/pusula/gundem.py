# -*- coding: utf-8 -*-
"""
GÜNDEM TAKİBİ — günün haberlerinden Luna'nın gerçekten söyleyecek sözü olanları bulur.

Amaç trend kovalamak değil. Gündemdeki bir gelişme ile bizim işimizin kesiştiği
yerde yazı yazmak; kesişmiyorsa yazmamak. Zorlama bağ kuran içerik hem okuyucuyu
kaçırıyor hem de Google'ın "yararsız içerik" değerlendirmesine takılıyor.

Kaynak: Google Haberler RSS. Tek uç nokta, anahtarsız, Türkçe sorgu destekli ve
kalıcı. Kendi RSS adreslerini de KAYNAK listesine ekleyebilirsin.

İnternet gerektirir — panel kendi makinende çalıştığı için orada sorun olmaz.
"""
import re, html, json, os, datetime, urllib.parse
import xml.etree.ElementTree as ET

from .kaynaklar.agir import getir

GOOGLE_HABER = ("https://news.google.com/rss/search"
                "?q=%s&hl=tr&gl=TR&ceid=TR:tr")


# ------------------------------------------------------------------ konu haritası
# (anahtar, arama sorgusu, hizmet sayfası, bizim bu konuda söyleyecek sözümüz)
KONULAR = [
 ("insaat", 'inşaat OR "konut projesi" OR müteahhit when:7d',
  "hizmetler/insaat-3d-modelleme.html",
  "Proje tanıtımı, şantiye ilerleme çekimi ve maketten önce 3D görselleştirme"),
 ("konut_satis", '"konut satış" OR "konut kredisi" OR "konut fiyatları" when:7d',
  "hizmetler/emlak-kurumsal.html",
  "İlan performansı, emlak videosu ve alıcının karar süreci"),
 ("emlak", 'emlak OR gayrimenkul OR "kira artışı" when:7d',
  "hizmetler/emlak-kurumsal.html",
  "Portföy tanıtımı, danışman görünürlüğü ve videolu ilan"),
 ("kentsel_donusum", '"kentsel dönüşüm" OR "riskli yapı" OR "yarısı bizden" when:14d',
  "hizmetler/insaat-3d-modelleme.html",
  "Hak sahibine projeyi anlatmak: dönüşüm öncesi/sonrası görselleştirme"),
 ("sanayi", 'sanayi OR ihracat OR "üretim tesisi" OR fuar when:7d',
  "hizmetler/urun-animasyon.html",
  "Makine ve süreç animasyonu, çok dilli tanıtım, fuar ekranı içeriği"),
 ("turizm", 'turizm OR otel OR "rezervasyon" OR "tatil sezonu" when:7d',
  "hizmetler/drone-fpv.html",
  "Tesis tanıtımı, sezon dışı görsel üretimi ve doğrudan rezervasyon"),
 ("mobilya", 'mobilya OR "ev tekstili" OR dekorasyon fuarı when:14d',
  "hizmetler/urun-animasyon.html",
  "Ürün görselleştirme, varyant üretimi ve mekâna yerleştirme"),
 ("bursa", 'Bursa yatırım OR Bursa proje OR Bursa sanayi when:7d',
  "sehir/bursa.html",
  "Bursa'daki iş ve yatırım gündemi — yerel görünürlük"),
 ("yapay_zeka_gorsel", '"yapay zeka" görsel OR video üretimi when:14d',
  "hizmetler/urun-animasyon.html",
  "Yapay zekâ ile üretilen görselin nerede işe yaradığı, nerede yaramadığı"),
 ("sosyal_medya", '"sosyal medya" işletme OR Instagram esnaf OR Reels when:14d',
  "hizmetler/isletme-tanitim.html",
  "Küçük işletmede içerik üretimi ve ölçülebilir sonuç"),
]

# Bizim sözlüğümüz — haberin bize gerçekten değip değmediğini buradan ölçüyoruz.
BIZIM_SOZLUK = {
 3: ("3d", "render", "görselleştirme", "animasyon", "maket", "tanıtım filmi", "drone",
     "video", "sanal tur", "görsel", "prodüksiyon", "reklam filmi", "içerik üretimi"),
 2: ("proje", "konut", "daire", "satış ofisi", "ilan", "portföy", "fuar", "tanıtım",
     "pazarlama", "marka", "sosyal medya", "instagram", "yapay zeka", "kentsel dönüşüm",
     "showroom", "katalog", "ihracat", "otel", "tesis", "mağaza",
     "konut satış", "satış", "alıcı", "müşteri", "rezervasyon", "lansman",
     "satış ofisi", "web sitesi", "görünürlük", "tanıtım filmi"),
 1: ("inşaat", "emlak", "gayrimenkul", "sanayi", "üretim", "turizm", "mobilya",
     "müteahhit", "yatırım", "işletme", "esnaf", "bursa"),
}
# Bunlar geçiyorsa haber bizim işimizle ilgili değildir — eliyoruz.
ELEME = ("cinayet", "kaza", "deprem can kaybı", "tutuklandı", "gözaltı", "yaralandı",
         "vefat", "cenaze", "iddianame", "operasyonu düzenlendi", "yangında öldü",
         "hükümlü", "terör", "silahlı",
         # doğrulama/teyit haberleri ve galeri-magazin kalıpları: sektör gündemi değil
         "doğruluk payı", "teyit", "mı gösteriyor", "mi gösteriyor", "mu gösteriyor", "mü gösteriyor",
         "iddia edildi", "sahte mi", "gerçek mi", "burç", "magazin",
         # 15.09.2026: asayiş/skandal kalıpları eklendi — "Çanakkale'de skandal olay…"
         # gibi bir haber gündem defterine düşmüştü. Bunlar sektör gündemi değil.
         "skandal", "yakalandı", "fuhuş", "taciz", "istismar", "şüpheli", "gözaltına",
         "cinsel", "kavga", "bıçak", "ölü bulundu", "intihar", "dolandırıcı", "kumar")


def spam_baslik(baslik):
    """SEO çöpü başlıkları eler: emoji yığını, büyük harf bağırması, tekrar eden kalıp.

    15.09.2026: "TOKİ İSTANBUL KİRALIK KONUT 2026 📌 TOKİ İstanbul…" gibi başlıklar
    içerik çiftlikleri tarafından üretiliyor; kaynak olarak alınmaya değmez.
    """
    b = (baslik or "").strip()
    if not b:
        return True
    harf = [c for c in b if c.isalpha()]
    if harf and sum(1 for c in harf if c.isupper()) / len(harf) > 0.6:
        return True                                  # başlığın çoğu BÜYÜK HARF
    if sum(1 for c in b if ord(c) > 0x2190) >= 1:
        return True                                  # emoji / sembol var
    kelime = [k for k in _kucuk(b).split() if len(k) > 3]
    if kelime and len(set(kelime)) / len(kelime) < 0.6:
        return True                                  # aynı kelimeler tekrarlanıyor
    return False

TR_KUCUK = str.maketrans({"İ": "i", "I": "ı", "Ğ": "ğ", "Ü": "ü", "Ş": "ş", "Ö": "ö", "Ç": "ç"})


def _kucuk(x):
    return (x or "").translate(TR_KUCUK).lower()


def _temiz(x):
    x = re.sub(r"<[^>]+>", " ", x or "")
    return re.sub(r"\s+", " ", html.unescape(x)).strip()


# ------------------------------------------------------------------ çekme
def rss_cek(url, azami=25):
    """RSS/Atom okur. Döner: [{baslik, adres, kaynak, tarih, ozet}]"""
    kod, govde, _ = getir(url, zaman_asimi=15)
    if kod != 200 or not govde:
        return []
    try:
        kok = ET.fromstring(govde.encode("utf-8", "ignore"))
    except ET.ParseError:
        return []
    cikti = []
    for it in kok.iter():
        if not it.tag.endswith("item") and not it.tag.endswith("entry"):
            continue
        d = {"baslik": "", "adres": "", "kaynak": "", "tarih": "", "ozet": ""}
        for c in it:
            t = c.tag.split("}")[-1]
            if t == "title":
                d["baslik"] = _temiz(c.text)
            elif t == "link":
                d["adres"] = (c.text or c.attrib.get("href") or "").strip()
            elif t == "source":
                d["kaynak"] = _temiz(c.text)
            elif t in ("pubDate", "published", "updated"):
                d["tarih"] = (c.text or "").strip()
            elif t in ("description", "summary", "content"):
                d["ozet"] = _temiz(c.text)[:400]
        if d["baslik"] and d["adres"]:
            cikti.append(d)
        if len(cikti) >= azami:
            break
    return cikti


def konu_cek(konu, azami=15):
    anahtar, sorgu, sayfa, soz = konu
    url = GOOGLE_HABER % urllib.parse.quote(sorgu)
    for h in rss_cek(url, azami):
        h["konu"] = anahtar
        h["hizmet_sayfa"] = sayfa
        h["bizim_soz"] = soz
        yield h


# ------------------------------------------------------------------ puanlama
def puanla(haber, iller=()):
    """0-100: bu haberde bizim söyleyecek sözümüz var mı?"""
    metin = _kucuk(haber["baslik"] + " " + haber.get("ozet", ""))
    if any(e in metin for e in ELEME):
        return 0, ["konu dışı (olay/asayiş haberi)"]
    if spam_baslik(haber.get("baslik")):
        return 0, ["başlık SEO çöpü kalıbında (büyük harf/emoji/tekrar)"]

    # Haber zaten bizim konu sorgumuzdan geldiyse ve o konunun tanımlı bir yazı
    # açısı varsa, sıfırdan başlamıyoruz — konu eşleşmesi tek başına bir sinyal.
    puan, gerekce = 0, []
    if haber.get("konu") in ACILAR:
        puan += 4
        gerekce.append("tanımlı konumuz (%s) (+4)" % haber["konu"])
    for agirlik, kelimeler in BIZIM_SOZLUK.items():
        vuran = [k for k in kelimeler if k in metin]
        if vuran:
            puan += agirlik * min(len(vuran), 3)
            gerekce.append("%s (%d puan)" % (", ".join(vuran[:3]), agirlik * min(len(vuran), 3)))

    # şehir adı geçiyorsa yerel içerik üretilebilir
    sehir = next((il for il in iller if _kucuk(il) in metin), None)
    if sehir:
        puan += 3
        gerekce.append("şehir adı geçiyor: %s (+3)" % sehir)
        haber["il"] = sehir

    # başlıkta soru varsa okuyucu zaten cevap arıyor
    if "?" in haber["baslik"]:
        puan += 2
        gerekce.append("başlık soru soruyor (+2)")

    return min(100, int(puan * 4.5)), gerekce


# ------------------------------------------------------------------ açı önerisi
# Haberin türüne göre "biz ne yazarız" kalıbı. Kalıp habere zorla uydurulmaz;
# uymuyorsa yazı önerilmez.
ACILAR = {
"insaat": [
 ("Proje tanıtımı", "{konu} gündemdeyken alıcı projeyi neye bakarak seçiyor?",
  "Gündemdeki gelişme alıcının kafasını karıştırıyor. Karar verirken elinde ne olduğu belirleyici: "
  "maket fotoğrafı mı, içinde yürünen bir video mu."),
 ("Şantiye ilerlemesi", "Devam eden projede alıcıya güven nasıl verilir?",
  "Haber piyasadaki belirsizliği artırdığında ilk sorulan soru 'bu proje bitecek mi' oluyor. "
  "Haftalık ilerleme çekimi bu sorunun tek somut cevabı."),
],
"konut_satis": [
 ("İlan performansı", "Satışların {yon} bir dönemde ilan neye göre tıklanıyor?",
  "Talep değiştiğinde ilanlar arasındaki fark büyüyor. Aynı daire, aynı fiyat — "
  "farkı yaratan görsel ve videonun kalitesi."),
],
"emlak": [
 ("Portföy tanıtımı", "Danışman portföyünü nasıl daha hızlı satar?",
  "Piyasa haberleri alıcıyı beklemeye itiyor. Bekleyen alıcıyı harekete geçiren şey, "
  "mülkü gitmeden gezebilmesi."),
],
"kentsel_donusum": [
 ("Hak sahibine anlatım", "Dönüşümde hak sahibi neye ikna oluyor?",
  "Kentsel dönüşümde en zor kısım anlaşma. Hak sahibi rakamı değil, sonucu göremediği "
  "için tereddüt ediyor — öncesi/sonrası görselleştirme tam olarak bunu çözüyor."),
],
"sanayi": [
 ("Fuar ve ihracat", "Fuarda standın önünde kim duruyor?",
  "Fuarda katalog kimse okumuyor; ekranda dönen bir anlatım duruyor. "
  "Makinenin içinde ne olduğunu gösteren animasyon dil bariyerini de kaldırıyor."),
 ("Süreç anlatımı", "Görünmeyen üretim nasıl anlatılır?",
  "Üretim süreci karmaşıklaştıkça anlatmak zorlaşıyor. Kesit animasyonu, "
  "tesisi gezdirmeden anlatmanın yolu."),
],
"turizm": [
 ("Sezon hazırlığı", "Sezon açılmadan tesis nasıl doldurulur?",
  "Rezervasyon sezondan önce alınıyor ama görsel sezonda çekiliyor — arada kalan boşluk "
  "3D ve doğru planlama ile kapanıyor."),
],
"mobilya": [
 ("Ürün görselleştirme", "Ürün beyaz fonda mı, mekânda mı satılır?",
  "Alıcı ürünü kendi evinde hayal edemezse satın almıyor. Mekâna yerleştirme "
  "bunu çözen en ucuz yöntem."),
],
"bursa": [
 ("Yerel gündem", "Bursa'da {konu} — yerel işletme ne yapmalı?",
  "Yerel bir gelişme yerel aramaları hareketlendiriyor. O dönemde görünür olan kazanıyor."),
],
"yapay_zeka_gorsel": [
 ("Nerede işe yarar", "Yapay zekâ görseli nerede işe yarıyor, nerede yaramıyor?",
  "Dürüst cevap: fikir aşamasında ve varyasyonda çok işe yarıyor; teslim edilecek "
  "gerçek mekân/ürün görselinde yaramıyor. Bunu söyleyen az, bu yüzden değerli."),
],
"sosyal_medya": [
 ("Ölçülebilir içerik", "İçerik üretiyoruz ama müşteri gelmiyor — neden?",
  "Beğeni ile arama arasında bağ kurulmuyor. Ölçülecek şey beğeni değil, "
  "'buradan gördüm' diyen müşteri sayısı."),
],
}


def aci_uret(haber):
    """Habere uygun yazı açısı. Uygun kalıp yoksa None."""
    kaliplar = ACILAR.get(haber.get("konu"))
    if not kaliplar:
        return None
    # başlıktan konuyu çıkar (kaba ama işe yarıyor)
    konu_kelime = haber["baslik"].split("—")[0].split("|")[0].strip()
    # Başlıkta şehir adı zaten varsa kalıptaki şehirle iki kez yazılmasın
    il = haber.get("il")
    if il:
        konu_kelime = re.sub(r"^%s['\u2019]?[a-zçğıöşü]*\s+" % re.escape(il),
                             "", konu_kelime, flags=re.I).strip()
    konu_kelime = (konu_kelime[:1].lower() + konu_kelime[1:]) if konu_kelime else konu_kelime
    if len(konu_kelime) > 60:
        konu_kelime = konu_kelime[:57] + "…"
    metin = _kucuk(haber["baslik"])
    yon = "yavaşladığı" if any(k in metin for k in ("düştü", "geriledi", "azaldı", "yavaşla")) \
          else "hareketlendiği" if any(k in metin for k in ("arttı", "yükseldi", "rekor", "canlan")) \
          else "değiştiği"
    ad, soru, gerekce = kaliplar[hash(haber["adres"]) % len(kaliplar)]
    return {
        "ad": ad,
        "baslik": soru.format(konu=konu_kelime, yon=yon),
        "gerekce": gerekce,
        "hizmet_sayfa": haber.get("hizmet_sayfa"),
        "bizim_soz": haber.get("bizim_soz"),
    }


# ------------------------------------------------------------------ tarama
def tara(iller=(), asgari_puan=40, konu_basi=12):
    """Tüm konuları tarar, puanlar, açı önerir. Döner: sıralı liste."""
    gorulen, cikti = set(), []
    for konu in KONULAR:
        try:
            haberler = list(konu_cek(konu, konu_basi))
        except Exception:
            continue
        for h in haberler:
            anahtar = _kucuk(h["baslik"])[:80]
            if anahtar in gorulen:
                continue
            gorulen.add(anahtar)
            puan, gerekce = puanla(h, iller)
            if puan < asgari_puan:
                continue
            aci = aci_uret(h)
            if not aci:
                continue
            cikti.append({**h, "puan": puan, "gerekce": gerekce, "aci": aci})
    cikti.sort(key=lambda x: -x["puan"])
    return cikti


def kaynak_testi():
    """Hangi konu sorgusu veri dönüyor — ağ sorunu mu, sorgu sorunu mu ayırt eder."""
    sonuc = []
    for anahtar, sorgu, _, _ in KONULAR:
        try:
            n = len(rss_cek(GOOGLE_HABER % urllib.parse.quote(sorgu), 5))
        except Exception as ex:
            n, hata = 0, "%s" % type(ex).__name__
        else:
            hata = None
        sonuc.append({"konu": anahtar, "haber": n, "hata": hata})
    return sonuc


# ------------------------------------------------------------------ yazı taslağı
ISKELET = [
 ("Neden şimdi", "Haberin ne dediği ve bunun okuyucunun işine ne yaptığı — iki paragraf, "
                 "abartısız. Habere bağlantı ver, kaynağı gizleme."),
 ("Asıl mesele", "Okuyucunun gerçek problemi. Haber sadece kapı; asıl konu burada başlıyor."),
 ("Ne yapılmalı", "Somut, uygulanabilir 4-6 madde. Bizden hizmet almadan da "
                  "uygulanabilecek maddeler koy — güven buradan geliyor."),
 ("Nerede biz varız", "Tek paragraf. Zorlama yok: hangi kısımda gerçekten işe yarıyoruz."),
 ("Rakamla bakış", "Varsa süre/maliyet aralığı ya da tipik sonuç. Uydurma rakam yok; "
                   "veremiyorsan bu bölümü sil."),
]


def taslak(haber, firma="Luna Yapım"):
    """İncelenmeye hazır yazı taslağı (markdown)."""
    a = haber["aci"]
    bugun = datetime.date.today().strftime("%d.%m.%Y")
    s = []
    s.append("# %s" % a["baslik"])
    s.append("")
    s.append("*Taslak · %s · gündem kaynaklı*" % bugun)
    s.append("")
    s.append("**Tetikleyen haber:** [%s](%s)%s" %
             (haber["baslik"], haber["adres"],
              (" — %s" % haber["kaynak"]) if haber.get("kaynak") else ""))
    s.append("")
    s.append("**Neden bu yazı:** %s" % a["gerekce"])
    s.append("")
    s.append("**Bizim bu konudaki işimiz:** %s" % (a.get("bizim_soz") or "—"))
    if haber.get("il"):
        s.append("")
        s.append("**Yerel bağ:** Haberde %s geçiyor — yazının sonunda "
                 "`/sehir/` sayfasına bağlantı ver." % haber["il"])
    s.append("")
    s.append("**İlgili hizmet sayfası:** `%s`" % (a.get("hizmet_sayfa") or "—"))
    s.append("")
    s.append("---")
    s.append("")
    for baslik, ne_yaz in ISKELET:
        s.append("## %s" % baslik)
        s.append("")
        s.append("> %s" % ne_yaz)
        s.append("")
    s.append("## Sık sorulanlar")
    s.append("")
    s.append("> Üç soru yaz. Okuyucunun gerçekten sorduğu sorular olsun; "
             "SSS bölümü aramada soru kutusuna çıkma şansı veriyor.")
    s.append("")
    s.append("---")
    s.append("")
    s.append("### Yayına almadan önce")
    s.append("")
    s.append("- [ ] Haber hâlâ güncel mi (gündem yazısı bir haftada bayatlar)")
    s.append("- [ ] Habere verilen bağlantı çalışıyor mu")
    s.append("- [ ] Uydurma rakam var mı — varsa çıkar")
    s.append("- [ ] En az bir iç bağlantı (hizmet ya da şehir sayfası)")
    s.append("- [ ] Kapak görseli seçildi mi")
    s.append("- [ ] `site-uretici/blog.py` içindeki YAZILAR listesine eklendi mi")
    return "\n".join(s)


def sosyal_kesit(haber):
    """Aynı konudan çıkacak kısa sosyal medya metni."""
    a = haber["aci"]
    return {
        "kanca": a["baslik"],
        "govde": ("%s\n\nBu hafta gündemde: %s\n\nBizim tarafımızdan bakınca: %s"
                  % (a["baslik"], haber["baslik"], a["gerekce"])),
        "biçim": "carousel" if "?" in a["baslik"] else "tekli",
        "not": "Haber bağlantısını gönderi metnine koyma — kapak görseline yaz, "
               "bağlantıyı profildeki adrese bırak.",
    }


def yaz(haber, klasor):
    """Taslağı dosyaya yazar."""
    os.makedirs(klasor, exist_ok=True)
    # Türkçe harfleri ascii karşılığına çevir (yoksa "dönüşümde" → "dnmde" oluyor)
    TR = str.maketrans({"ı": "i", "ğ": "g", "ş": "s", "ö": "o", "ü": "u", "ç": "c",
                        "â": "a", "î": "i", "û": "u"})
    duz = _kucuk(haber["aci"]["baslik"]).translate(TR)
    ad = re.sub(r"[^a-z0-9]+", "-", duz.encode("ascii", "ignore").decode()).strip("-")[:60]
    yol = os.path.join(klasor, "%s-%s.md" % (datetime.date.today().strftime("%Y%m%d"),
                                             ad or "gundem"))
    with open(yol, "w", encoding="utf-8") as f:
        f.write(taslak(haber))
    return yol
