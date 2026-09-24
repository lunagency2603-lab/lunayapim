# -*- coding: utf-8 -*-
"""
YERELLEŞTİRME — il × hizmet sayfalarındaki ORTAK hizmet metnini inceltir,
ilin kendi verisinden gelen bölümü kalınlaştırır.

Neden (14.09.2026): 332 il sayfasının her biri aynı hizmet anlatımını taşıyordu.
Ölçüm: drone sayfalarında 472 kelimenin 163'ü (%34), 3D'de %30, ürün animasyonunda
daha fazlası 46 sayfada BİREBİR aynıydı. Bu, hem Google'ın "ölçekli içerik"
tanımına yaklaşıyor hem de AdSense'in "düşük değerli içerik" değerlendirmesini
besliyordu.

Yaklaşım — eş anlamlı kelime oyunu (spun content) DEĞİL:
  1. Her sayfada aynı olan hizmet anlatımı (süreç adımları, teslim formatları,
     fiyatın uzun açıklaması) il sayfasından ÇIKARILIR; bunlar zaten hizmet
     sayfasında tek ve kanonik hâlde duruyor — oraya bağlanır.
  2. Yerine ilin KENDİ verisinden (ilçeler, komşu iller, sektör listesi, mekân
     ve ekip bilgisi) üretilen, gerçekten o ile ait iki bölüm eklenir.
  3. Sonuç: ortak kelime düşer, ile özel kelime artar; iki il sayfası birbirine
     benzemeyi bırakır çünkü içerikleri gerçekten farklıdır.

Etkisiz tekrarlanabilir: işaretlenmiş bölümleri (data-yerel) ikinci kez eklemez.
"""
import collections, hashlib, html, os, re

from sehirler import SEHIRLER, SEHIR_INDEKS

HIZMET_SAYFA = {
    "drone-cekimi": ("drone-fpv", "drone çekimi"),
    "emlak-video": ("emlak-kurumsal", "emlak videosu"),
    "insaat-3d-modelleme": ("insaat-3d-modelleme", "inşaat 3D modelleme"),
    "urun-animasyon": ("urun-animasyon", "ürün animasyonu"),
    "klip-cekimi": ("klip-cekimi", "klip çekimi"),
    "dugun-cekimi": ("dugun-etkinlik", "düğün çekimi"),
    "isletme-tanitim": ("isletme-tanitim", "işletme tanıtımı"),
}


def _e(x):
    return html.escape(x or "", quote=True)


def _v(slug, anahtar, n):
    """İl+bağlam'dan türeyen sabit seçim: aynı cümle kalıbı her ilde tekrarlanmasın."""
    h = hashlib.md5(("%s|%s" % (slug, anahtar)).encode("utf-8")).hexdigest()
    return int(h[:8], 16) % n


def _liste(xs):
    xs = [x for x in xs if x]
    if not xs:
        return ""
    if len(xs) == 1:
        return xs[0]
    return ", ".join(xs[:-1]) + " ve " + xs[-1]


def _komsu_adlari(c, n=3):
    return [SEHIR_INDEKS[k]["ad"] for k in (c.get("komsu") or []) if k in SEHIR_INDEKS][:n]


# ------------------------------------------------------------------ 1) ortak metni incelt
def _surec_sil(s, hizmet_slug, ad, ek):
    """Dört adımlık süreç bloğu her ilde aynı — hizmet sayfasına bağla, sayfadan çıkar."""
    hs, hiz_ad = HIZMET_SAYFA[hizmet_slug]
    kal = ['<p class="ts-not">Adım adım işleyiş ve teslim listesi <a href="../hizmetler/%s#surec">%s sayfasında</a>.</p>',
           '<p class="ts-not">İşleyişin tamamı <a href="../hizmetler/%s#surec">%s sayfasında</a>.</p>',
           '<p class="ts-not">Keşiften teslime adımlar <a href="../hizmetler/%s#surec">%s sayfasında</a> yazılı.</p>',
           '<p class="ts-not">Süreç ve teslim biçimleri <a href="../hizmetler/%s#surec">%s sayfasında</a>.</p>']
    yeni = kal[_v(ad, "surec", len(kal))] % (hs, _e(hiz_ad))
    return re.sub(r'<div class="surec">.*?</div>\s*</div>\s*</section>',
                  yeni + "\n  </div>\n</section>", s, count=1, flags=re.S)


def _fiyat_kisalt(s):
    """Fiyat paragrafının il-bağımsız uzun kuyruğunu kısalt (bant kalır, açıklama fiyat sayfasında)."""
    return s.replace(
        ' Rakamlar <a href="../fiyatlar">fiyat sayfamızdaki</a> bantla aynı; işi anlattığınızda aynı gün '
        'net bir aralık veriyoruz, sürpriz kalem çıkarmıyoruz.',
        ' Aynı bant <a href="../fiyatlar">fiyat sayfamızda</a> da yazılı.')


def _sss_incelt(s, ad, hizmet):
    """İl adı geçmeyen soru-cevaplar il sayfasından çıkar.

    Bunlar hizmetin kendisine ait cevaplar (paket içeriği, teslim süresi, dosya
    biçimi) ve 46 il sayfasında birebir aynıydı. Kanonik yerleri hizmet sayfası;
    il sayfasında yalnız o ile ait sorular kalır, gerisi için bağlantı verilir.
    """
    hs, hiz_ad = HIZMET_SAYFA[hizmet]
    parcalar = list(re.finditer(r'<details[^>]*>\s*<summary>(.*?)</summary>\s*<div class="cvp">(.*?)</div></details>', s, re.S))
    kok = ad.split("'")[0].lower()
    silindi = 0
    for m in parcalar:
        govde = re.sub(r"<[^>]+>", " ", m.group(1) + " " + m.group(2)).lower()
        cevap = re.sub(r"<[^>]+>", " ", m.group(2)).lower()
        if kok in cevap:
            continue                      # cevabın içinde il geçiyorsa yerel sayılır, kalsın
        if "data-sss-yerel" in m.group(0):
            continue                      # bizim ürettiğimiz yerel soru
        s = s.replace(m.group(0), "", 1); silindi += 1
    if silindi and "sss-devam" not in s:
        kal = ['<p class="ts-not sss-devam">Diğer sorular <a href="../hizmetler/%s#sss">%s sayfasında</a>.</p>',
               '<p class="ts-not sss-devam">Hizmete ait sorular <a href="../hizmetler/%s#sss">%s sayfasında</a>.</p>',
               '<p class="ts-not sss-devam">Kalan sorular <a href="../hizmetler/%s#sss">%s sayfasında</a>.</p>']
        s = s.replace('</div>\n\n    <h2>', '</div>\n    ' + (kal[_v(ad, "sssnot", len(kal))] % (hs, _e(hiz_ad))) + '\n\n    <h2>', 1)
    return s


# ------------------------------------------------------------------ 2) ile özel bölüm ekle
EK_ALAN = {
    "insaat-3d-modelleme": "konut",
    "emlak-video": "portfoy",
    "urun-animasyon": "uretim",
    "drone-cekimi": "saha",
    "klip-cekimi": "mekan",
    "dugun-cekimi": "mekan",
    "isletme-tanitim": "musteri",
}


def _yerel_bolum(c, hizmet_slug):
    ad, ek = c["ad"], c["ek"]
    ilceler = c.get("ilceler") or []
    sektorler = c.get("sektorler") or []
    komsu = _komsu_adlari(c)
    ekip_ortak = (c.get("ekip") or "") == "ortak"
    mekan = (c.get("mekan") or "").split(",")
    mekan = [m.strip() for m in mekan if m.strip()]
    tur = EK_ALAN[hizmet_slug]
    p = []

    # a) ilçe/işin nereden geldiği — her ilde farklı ilçe adları ve farklı sektör karışımı
    if ilceler:
        if tur == "konut":
            p.append("%s%s iş genellikle %s hattından geliyor: yeni parselin nerede açıldığı, "
                     "hangi ilçede kaç katlı yapıldığı ve arsanın hangi yöne baktığı modelin "
                     "ışık kurgusunu doğrudan değiştiriyor. %s"
                     % (_e(ad), _e(ek), _e(_liste(ilceler[:4])),
                        _e("Talep %s tarafından da geliyor; aynı keşif gününe birleştirilebiliyor." % _liste(komsu)) if komsu else ""))
        elif tur == "portfoy":
            p.append("Portföyün ağırlığı %s tarafında toplanıyor. İlan videosunda ilçe farkı "
                     "önemli: merkeze yakın daire ile şehir dışındaki müstakil mülk aynı anlatımla "
                     "satılmıyor, ilkinde yürüyüş rotası, ikincisinde arazi ve yol bağlantısı "
                     "belirleyici oluyor." % _e(_liste(ilceler[:4])))
        elif tur == "uretim":
            p.append("Üretim %s hattında yoğunlaşıyor; %s gibi kalemler ilin dışına satış yapan "
                     "firmaların ağırlıkta olduğunu gösteriyor. Bu, animasyonun çoğunlukla tek dilde "
                     "değil, fuar ve ihracat sürümüyle birlikte istendiği anlamına geliyor."
                     % (_e(_liste(ilceler[:4])), _e(_liste([s.lower() for s in sektorler[:3]]))))
        elif tur == "saha":
            p.append("Uçuş planı %s%s ilçeden ilçeye değişiyor: %s aynı gün içinde sıralanabiliyor, "
                     "ama rüzgâr ve yerleşim kısıtı her noktada ayrı kontrol ediliyor. Keşifte "
                     "hangi noktadan kalkılacağını ve alternatif saati birlikte belirliyoruz."
                     % (_e(ad), _e(ek), _e(_liste(ilceler[:3]))))
        elif tur == "mekan":
            p.append("Çekim noktaları %s çevresine dağılıyor; %s%s tanınan mekânlar (%s) "
                     "izleyicide anında yer duygusu kuruyor, bu da videonun yerel paylaşımını artırıyor."
                     % (_e(_liste(ilceler[:3])), _e(ad), _e(ek), _e(_liste(mekan[:3]) or "şehir merkezi")))
        else:
            p.append("Müşteri trafiği %s hattında toplanıyor. İşletme içeriğinde ilçe farkı doğrudan "
                     "kurguya yansıyor: merkezdeki bir mekânda yoğun saat, çeperdeki bir işletmede "
                     "ulaşım ve otopark anlatımı öne çıkıyor." % _e(_liste(ilceler[:4])))

    # b) ekip ve yol — komşu iller gerçek veriden, uydurma iş yok
    if komsu:
        v = _v(c["slug"], "ekip", 4)
        if ekip_ortak:
            kaliplar = [
                "Kamera gereken gün %s hattındaki çözüm ortağımızla sahaya çıkıyoruz; kurgu, renk ve "
                "yönetmenlik Bursa'daki masamızda kalıyor.",
                "Sahada %s tarafındaki ortağımızla, masada kendi ekibimizle çalışıyoruz — çeken ve "
                "kurgulayan farklı, karar veren aynı.",
                "Çekim günü için %s bölgesindeki ortağımızı programlıyoruz; dosya aynı akşam bize geçiyor, "
                "kurgu Bursa'da yapılıyor.",
                "%s yönünde çalışan ortağımızla aynı ekipman listesini kullanıyoruz; bu, iki ayrı ilde "
                "çekilen işin aynı görünmesini sağlıyor.",
            ]
        else:
            kaliplar = [
                "Sahaya kendi ekibimizle çıkıyoruz; %s tarafındaki işlerle aynı haftaya denk gelirse "
                "program tek yol planında birleşiyor.",
                "Çekimi de kurguyu da biz yapıyoruz; %s yönünde aynı hafta iş varsa yol tek seferde planlanıyor.",
                "Ekip kendi ekipmanıyla geliyor; %s hattındaki işlerle birleştiğinde keşif günü ortaklaşıyor.",
                "İşi baştan sona aynı ekip yürütüyor; %s tarafıyla aynı takvime düşen işler tek çıkışta toplanıyor.",
            ]
        p.append(kaliplar[v] % _e(_liste(komsu)))

    if not p:
        return ""
    basliklar = ["%s%s bu iş nereden geliyor", "%s%s sahanın hâli", "%s%s işin coğrafyası", "%s%s talep nerede toplanıyor"]
    bas = basliklar[_v(c["slug"], "baslik" + hizmet_slug, len(basliklar))] % (_e(ad), _e(ek))
    return ('\n<section data-yerel="%s">\n  <div class="wrap prose">\n    <h2>%s</h2>\n    %s\n  </div>\n</section>\n'
            % (hizmet_slug, bas, "\n    ".join("<p>%s</p>" % x for x in p)))



# ------------------------------------------------------------------ 3) ikinci tur: lede, liste, SSS
ODAK_ALAN = {
    "insaat-3d-modelleme": "insaat", "emlak-video": "emlak", "urun-animasyon": "sanayi",
    "drone-cekimi": "cografya", "klip-cekimi": "kultur", "dugun-cekimi": "dugun_notu",
    "isletme-tanitim": "isletme_notu",
}
ODAK_IS = {
    "insaat-3d-modelleme": "mimari render ve proje animasyonu",
    "emlak-video": "ilan ve portföy videosu",
    "urun-animasyon": "3D ürün ve süreç animasyonu",
    "drone-cekimi": "havadan görüntü ve FPV çekim",
    "klip-cekimi": "klip çekimi ve kurgusu",
    "dugun-cekimi": "düğün ve etkinlik çekimi",
    "isletme-tanitim": "işletme tanıtımı ve aylık içerik",
}


def _ilk_cumle(t, en_az=40):
    t = (t or "").strip()
    if not t:
        return ""
    for i, ch in enumerate(t):
        if ch in ".!?" and i >= en_az:
            return t[:i + 1].strip()
    return t[:220].strip()


def _lede_yerel(s, c, hizmet):
    """Kahraman bölümündeki tanıtım cümlesi her ilde aynıydı; ilin kendi verisinden kuruyoruz.

    Analiz bölümü alanın İLK cümlesini kullanıyor; burada tekrar olmasın diye
    ikinci cümleyi, yoksa mekân/sektör verisini alıyoruz.
    """
    alan = ODAK_ALAN[hizmet]
    tam = (c.get(alan) or "").strip()
    ilk = _ilk_cumle(tam)
    kalan = tam[len(ilk):].strip()
    olgu = _ilk_cumle(kalan) if len(kalan.split()) > 8 else ""
    if not olgu:
        mek = [x.strip() for x in (c.get("mekan") or "").split(",") if x.strip()]
        sek = [x for x in (c.get("sektorler") or [])][:3]
        if mek:
            # 23.09.2026: "çalışırken sık döndüğümüz yerler" her ilde tekrarlanan bir deneyim
            # iddiasıydı; yerine iddiasız, yine yerel bir tanım.
            olgu = "%s%s çekim planında öne çıkan yerler: %s." % (_e(c["ad"]), _e(c["ek"]), _e(_liste(mek[:3])))
        elif sek:
            olgu = "%s%s üretim %s üzerinde yoğunlaşıyor." % (_e(c["ad"]), _e(c["ek"]), _e(_liste([x.lower() for x in sek])))
    if not olgu:
        return s
    ad, ek_ = c["ad"], c["ek"]
    kal = ["%s %s işini buna göre kuruyoruz.",
           "%s Bu tablo %s planını doğrudan belirliyor.",
           "%s %s işinde neyi göstereceğimiz buradan çıkıyor.",
           "%s %s işinin çerçevesi bu."]
    is_ = _e(ODAK_IS[hizmet])
    yeni = kal[_v(c["slug"], "lede" + hizmet, len(kal))] % (olgu, is_)
    yeni = re.sub(r"(?<=[.!?]) +([a-zçğıöşü])", lambda m: " " + m.group(1).upper(), yeni)
    return re.sub(r'<p class="lede">.*?</p>', '<p class="lede">%s</p>' % yeni, s, count=1, flags=re.S)


def _liste_yerel(s, c, hizmet):
    """"Nerede kullanılıyor" listesine ilin kendi sektör ve ilçe verisinden iki madde ekler,
    iki genel maddeyi çıkarır. Madde sayısı aynı kalır; içerik ile bağlanır."""
    m = re.search(r'(<h2[^>]*>[^<]*kullan[^<]*</h2>\s*)<ul>(.*?)</ul>', s, re.S | re.I)
    if not m:
        return s
    maddeler = re.findall(r"<li>.*?</li>", m.group(2), re.S)
    if len(maddeler) < 4:
        return s
    sekt = [x for x in (c.get("sektorler") or [])][:2]
    ilce = (c.get("ilceler") or [])[:2]
    yerel = []
    if sekt:
        k1 = ["<li><strong>%s alıcısına</strong> — %s ağırlıklı bir ilde en çok istenen iş</li>",
              "<li><strong>%s tarafı</strong> — %s üreten firmaların ilk sorduğu anlatım</li>",
              "<li><strong>%s müşterisi</strong> — %s hattındaki firmalarda öne çıkan kullanım</li>",
              "<li><strong>%s kanalı</strong> — %s işi yapan firmaların satış aracı</li>"]
        yerel.append(k1[_v(c["slug"], "liste1", len(k1))] % (_e(sekt[0]), _e(", ".join(x.lower() for x in sekt))))
    if ilce:
        k2 = ["<li><strong>%s çevresi</strong> — aynı güne sığdırılan çoklu nokta</li>",
              "<li><strong>%s hattı</strong> — tek çekim gününde birden fazla durak</li>",
              "<li><strong>%s bölgesi</strong> — program tek güne toplanıyor</li>",
              "<li><strong>%s tarafı</strong> — noktalar aynı güne diziliyor</li>"]
        yerel.append(k2[_v(c["slug"], "liste2", len(k2))] % _e(", ".join(ilce)))
    if not yerel:
        return s
    kalan = maddeler[:max(2, len(maddeler) - len(yerel))]
    yeni = "<ul>\n      %s\n    </ul>" % "\n      ".join(kalan + yerel)
    return s[:m.start(2) - 4] + yeni + s[m.end(2) + 5:]


def _sss_yerel(s, c, hizmet):
    """İle özel iki soru-cevap ekler (ilçe, komşu il, sektör verisinden; uydurma iş yok)."""
    if "data-sss-yerel" in s:
        return s
    ad, ek_ = c["ad"], c["ek"]
    ilce = _liste((c.get("ilceler") or [])[:3])
    komsu = _liste(_komsu_adlari(c))
    sekt = _liste([x.lower() for x in (c.get("sektorler") or [])[:3]])
    ortak = (c.get("ekip") or "") == "ortak"
    sorular = []
    if ilce:
        kal = ["%s başta olmak üzere ilin tamamına geliyoruz; uzak ilçelerde tek iş yerine aynı bölgedeki işleri bir güne topluyoruz.",
               "İlin tamamına geliyoruz, yoğunluk %s tarafında. Tek iş için uzun yol çıkıyorsa programı aynı bölgedeki başka işle birleştiriyoruz.",
               "%s dahil her ilçeye çıkıyoruz; mesafe uzunsa keşif ve çekimi aynı güne sıkıştırıyoruz.",
               "%s dahil ilin her yerine geliyoruz; uzak nokta için günü başka işle birleştirmeyi öneriyoruz."]
        sorular.append(("%s%s hangi ilçelere geliyorsunuz?" % (_e(ad), _e(ek_)),
                        kal[_v(c["slug"], "sssilce", len(kal))] % _e(ilce)))
    if komsu:
        kal2 = ["Evet. %s yönündeki işlerle aynı haftaya denk gelirse tek yol planında birleştiriyoruz.",
                "Alıyoruz. %s tarafındaki işler aynı takvime düşerse yol tek seferde planlanıyor.",
                "Evet — %s hattındaki işlerle aynı hafta içindeyse program ortaklaşıyor.",
                "Çalışıyoruz. %s yönüyle aynı haftaya denk gelen işler tek çıkışta toplanıyor."]
        sorular.append(("%s dışından da iş alıyor musunuz?" % _e(ad),
                        kal2[_v(c["slug"], "ssskomsu", len(kal2))] % _e(komsu) + " %s"
                        % ("Kamera gereken günlerde bölgedeki çözüm ortağımızla, kurgu ve renkte kendi ekibimizle çalışıyoruz."
                           if ortak else "Ekibimiz sahaya kendisi çıkıyor.")))
    elif sekt:
        sorular.append(("%s%s hangi sektörlerle çalışıyorsunuz?" % (_e(ad), _e(ek_)),
                        "İlin üretim profiline uygun olarak %s başta olmak üzere her sektörle çalışıyoruz." % _e(sekt)))
    if not sorular:
        return s
    blok = "".join('<details data-sss-yerel><summary>%s</summary><div class="cvp"><p>%s</p></div></details>'
                   % (q, a) for q, a in sorular[:2])
    return re.sub(r'(<div class="sss">)', r"\1" + blok, s, count=1)



def _ortak_kes(s, c, hizmet):
    """İl sayfasında tekrar eden HİZMET metnini keser; kanonik yeri hizmet sayfasıdır.

    Kesilenler: rozet şeridi, belge/yetki paragrafı, "ilgili sayfalar" kart açıklamaları,
    sektör listesi girişindeki genel cümle. Hepsi 46 il sayfasında birebir aynıydı.
    """
    hs, hiz_ad = HIZMET_SAYFA[hizmet]
    # rozet şeridi (yalnız etiket yığını, bilgi taşımıyor)
    s = re.sub(r'\s*<div class="rozetler">.*?</div>\s*', "\n", s, count=1, flags=re.S)
    # yetki/belge paragrafı -> tek satır bağlantı
    s = re.sub(r'<h2 id="belgeler">Yetki ve belgeler</h2>\s*<p>.*?</p>',
               '<h2 id="belgeler">Yetki ve belgeler</h2>\n<p class="ts-not">Uçuş belgelerimiz (SHGM kayıtlı araç ve lisanslı pilot) ve '
               'uçuşu taşerona vermeme kuralımız <a href="../hizmetler/%s#belgeler">drone çekimi sayfasında</a> yazılı.</p>' % hs,
               s, count=1, flags=re.S)
    # ilgili kartların açıklama satırları (her ilde aynı)
    s = re.sub(r'(<div class="ilgili">.*?</div>)',
               lambda m: re.sub(r"<span>[^<]*</span>", "", m.group(1)), s, count=1, flags=re.S)
    # sektör listesi girişindeki genel cümle (ayrıca "daha önce modelledik" iddiası taşıyordu)
    s = s.replace("Aşağıdaki sektörlerde daha önce benzer ürünler modelledik; hazır iş akışımız olduğu için hem süre hem "
                  "maliyet düşüyor. Her satır, o sektörde animasyonun en çok neye yaradığını anlatıyor.",
                  "%s%s üretim profili şu satırlardan okunuyor; her satır o sektörde animasyonun neye yaradığını söylüyor."
                  % (_e(c["ad"]), _e(c["ek"])))
    return s


def _bos_baslik_temizle(s):
    """İçeriği kesilince geriye boş kalan H2 başlıklarını kaldırır."""
    s = re.sub(r'<h2[^>]*>[^<]{0,80}</h2>\s*(?=(<h2|</div>|<section|<div class="wrap"))', "", s)
    return s


# ------------------------------------------------------------------ 4) veriye dayalı ortak metin kesici
ELEME_ETIKET = re.compile(r"(?is)<(p|li|details)(\s[^>]*)?>(.*?)</\1>")
KORU = ("fiyat", "₺", "wa.me", "iletisim", "teklif")
ASGARI_KELIME = 430          # SEO kapısı 400; güvenli pay bırakıyoruz
UZUN = 12                    # bu kadar kelimeden uzun ortak blok kesilir


def _duz(x):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()


def _sayfa_kelime(s):
    t = re.sub(r"(?is)<(script|style|nav|header|footer|svg)[^>]*>.*?</\1>", " ", s)
    return len(re.sub(r"(?s)<[^>]+>", " ", t).split())


def ortak_kes_otomatik(kok, esik=0.9):
    """Aynı hizmetin il sayfalarında BİREBİR tekrar eden uzun blokları ölçer ve keser.

    Elle liste tutmuyoruz: hangi paragrafın 46 sayfada aynı olduğunu dosyaların
    kendisinden sayıyoruz. Eşiği geçen ve uzun olan bloklar il sayfasından çıkar,
    kanonik hâli hizmet sayfasında kalır. Fiyat bandı ve iletişim satırları korunur.
    Sayfa ASGARI_KELIME'nin altına inecekse kesme durur.
    """
    d = os.path.join(kok, "sehir")
    aile = collections.defaultdict(list)
    for n in sorted(os.listdir(d)):
        if not n.endswith(".html") or n == "index.html":
            continue
        for h in HIZMET_SAYFA:
            if n[:-5].endswith("-" + h):
                aile[h].append(os.path.join(d, n)); break
    rapor = {}
    for hizmet, dosyalar in aile.items():
        if len(dosyalar) < 5:
            continue
        sayac = collections.Counter()
        for y in dosyalar:
            g = open(y, encoding="utf-8").read()
            for m in set(m.group(0) for m in ELEME_ETIKET.finditer(g)):
                if len(_duz(m).split()) >= UZUN:
                    sayac[m] += 1
        sinir = len(dosyalar) * esik
        ortak = [x for x, n in sayac.items() if n >= sinir]
        ortak.sort(key=lambda x: -len(x))
        kesilen = 0
        for y in dosyalar:
            g = open(y, encoding="utf-8").read(); o = g
            for blok in ortak:
                if blok not in g:
                    continue
                d_ = _duz(blok).lower()
                if any(k in d_ or k in blok.lower() for k in KORU):
                    continue
                aday = g.replace(blok, "", 1)
                if _sayfa_kelime(aday) < ASGARI_KELIME:
                    break
                g = aday; kesilen += 1
            g = _bos_baslik_temizle(g)
            if g != o:
                open(y, "w", encoding="utf-8").write(g)
        rapor[hizmet] = {"ortak_blok": len(ortak), "kesilen": kesilen}
    return rapor

# ------------------------------------------------------------------ çalıştır

# ------------------------------------------------------------------ 5) sayfa içi tekrar temizliği (23.09.2026)
# Ölçüm: 509 il sayfasının 504'ünde aynı cümle/paragraf aynı sayfada iki kez geçiyordu
# (toplam 1.265 tekrar) — ör. drone sayfalarında "Tesis ve sanayi: ..." paragrafı hem
# analiz hem "talebi ne besliyor" bölümünde. Search Console'da 162 "keşfedildi" ve 25
# "tarandı - dizine eklenmedi" sayfanın bir nedeni bu şablon kokusu. Burada yalnız
# SİLİNİR, yeni metin üretilmez: aynı sayfada ikinci kez geçen blok/cümle çıkar.
def _cumleler(t):
    return [x.strip() for x in re.split(r"(?<=[.!?])\s+", t) if x.strip()]


def _nrm(x):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x))).strip().lower()


def ic_tekrar_temizle(s):
    a = s.find("</header>"); b = s.rfind("<footer")
    if a < 0 or b <= a:
        return s, 0
    govde = s[a:b]
    gorulen, silinen = set(), [0]

    def degis(m):
        tag, attr, ic = m.group(1), m.group(2) or "", m.group(3)
        tam = _nrm(ic)
        if len(tam.split()) < 6:
            return m.group(0)
        if tam in gorulen:
            silinen[0] += 1
            return ""
        if "<" not in ic:
            parca = _cumleler(ic)
            kalan = [c for c in parca if not (len(_nrm(c).split()) >= 8 and _nrm(c) in gorulen)]
            for c in kalan:
                if len(_nrm(c).split()) >= 8:
                    gorulen.add(_nrm(c))
            gorulen.add(tam)
            if not kalan:
                silinen[0] += 1
                return ""
            if len(kalan) != len(parca):
                silinen[0] += len(parca) - len(kalan)
                return "<%s%s>%s</%s>" % (tag, attr, " ".join(kalan), tag)
            return m.group(0)
        gorulen.add(tam)
        for c in _cumleler(tam):
            if len(c.split()) >= 8:
                gorulen.add(c)
        return m.group(0)

    yeni = ELEME_ETIKET.sub(degis, govde)
    if not silinen[0]:
        return s, 0
    yeni = _bos_baslik_temizle(yeni)
    t = s[:a] + yeni + s[b:]
    if _sayfa_kelime(t) < ASGARI_KELIME:      # SEO kapısını düşürmesin
        return s, 0
    return t, silinen[0]


GIRIS_HATA = re.compile(r"Aynı işi her ilde aynı şekilde yapmıyoruz — ([^<]{2,30}?)(?:'|&#x27;)ın kendi dinamiği var\.")


def ic_tekrar_hepsi(kok):
    d = os.path.join(kok, "sehir")
    rap = {"sayfa": 0, "silinen_blok": 0, "ek_duzeltme": 0}
    for n in sorted(os.listdir(d)):
        if not n.endswith(".html"):
            continue
        yol = os.path.join(d, n)
        s = open(yol, encoding="utf-8").read()
        o = s
        # "Çorum'ın", "Antalya'ın" gibi yanlış ekli giriş cümlesi (cesit.py GIRIS)
        s, k = GIRIS_HATA.subn(r"Aynı işi her ilde aynı şekilde yapmıyoruz; aşağıdaki notlar \1 için.", s)
        rap["ek_duzeltme"] += k
        s, n_sil = ic_tekrar_temizle(s)
        rap["silinen_blok"] += n_sil
        if s != o:
            open(yol, "w", encoding="utf-8").write(s); rap["sayfa"] += 1
    return rap


def calistir(kok):
    d = os.path.join(kok, "sehir")
    if not os.path.isdir(d):
        return {"sehir": "yok"}
    sayac = {"islenen": 0, "surec": 0, "sss": 0, "eklenen": 0}
    for n in sorted(os.listdir(d)):
        if not n.endswith(".html") or n == "index.html":
            continue
        kok_ad = n[:-5]
        if "-" not in kok_ad:
            continue
        slug, hizmet = None, None
        for h in HIZMET_SAYFA:
            if kok_ad.endswith("-" + h):
                slug, hizmet = kok_ad[:-(len(h) + 1)], h
                break
        if not hizmet:
            continue
        c = SEHIR_INDEKS.get(slug)
        if not c:
            continue
        yol = os.path.join(d, n)
        s = open(yol, encoding="utf-8").read()
        o = s
        if '<div class="surec">' in s:
            s = _surec_sil(s, hizmet, c["ad"], c["ek"]); sayac["surec"] += 1
        s = _fiyat_kisalt(s)
        s = _ortak_kes(s, c, hizmet)
        s = _lede_yerel(s, c, hizmet)
        s = _liste_yerel(s, c, hizmet)
        s = _sss_yerel(s, c, hizmet)
        y = _sss_incelt(s, c["ad"], hizmet)
        if y != s:
            sayac["sss"] += 1
            s = y
        s = s.replace("<h2 id=\"surec\">Süreç</h2>", "<h2 id=\"surec\">%s%s işleyiş</h2>" % (_e(c["ad"]), _e(c["ek"])))
        s = s.replace("<h2>Süreç</h2>", "<h2>%s%s işleyiş</h2>" % (_e(c["ad"]), _e(c["ek"])))
        # 23.09.2026: "render fiyatları" / "3d mimari görselleştirme fiyatları" aramalarında
        # fiyat rehberi 60-72. sırada; 81 il sayfasının hiçbiri ona bağlanmıyordu.
        if hizmet == "insaat-3d-modelleme" and "data-fiyat-rehber" not in s:
            k = s.find('<section class="cta">')
            if k > 0:
                s = s[:k] + ('<section data-fiyat-rehber><div class="wrap prose"><p>%s%s 3D render bütçesi '
                             'hazırlıyorsanız <a href="../blog/insaat-3d-modelleme-fiyatlari">3D render ve mimari '
                             'görselleştirme fiyatları</a> rehberinde maliyeti belirleyen altı kalem ve gerçek '
                             'fiyat bandı yazılı.</p></div></section>\n' % (_e(c["ad"]), _e(c["ek"]))) + s[k:]
        if 'data-yerel="%s"' % hizmet not in s:
            blok = _yerel_bolum(c, hizmet)
            if blok:
                i = s.find('<section class="cta">')
                if i < 0:
                    i = s.find("<footer")
                if i > 0:
                    s = s[:i] + blok + s[i:]
                    sayac["eklenen"] += 1
        if s != o:
            open(yol, "w", encoding="utf-8").write(s); sayac["islenen"] += 1
    sayac["ortak_kesim"] = ortak_kes_otomatik(kok)
    sayac["ic_tekrar"] = ic_tekrar_hepsi(kok)
    return sayac


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from pusula.ayarlar import SITE_KOK
    print(calistir(SITE_KOK))
