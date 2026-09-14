# -*- coding: utf-8 -*-
"""
YEREL ANALİZ — her il-hizmet sayfası için, o ilin GERÇEK verisinden kurulan
hizmete özel analiz bölümü.

İlke: geçmiş iş uydurmuyoruz ("Edirne'de şu projeyi çektik" YOK). Yaptığımız
şey, sehirler.py'de o il için yazılmış pazar/coğrafya/sanayi verisini o
hizmetin gözüyle okumak: "Bu ilde bu hizmet neyi göstermeli, neden, kime."
Bir prodüksiyon şirketinin teklif öncesi yaptığı analiz tam olarak budur.

Her hizmetin kendi alan seçimi var (drone → coğrafya+sanayi, emlak → emlak+
ilçe, ...) ki aynı ilin farklı sayfaları birbirini tekrar etmesin. Çerçeve
cümleleri il adından türeyen sabit seçimle 3 sürüm arasında dönüyor; içerik
her ilde zaten farklı olduğu için sonuç kelime düzeyinde de ayrışıyor.
"""
import hashlib, html

from sehirler import SEHIR_INDEKS


def _e(x):
    return html.escape(x or "", quote=True)


def _sec(il, anahtar, n):
    h = hashlib.md5(("%s|%s" % (il, anahtar)).encode("utf-8")).hexdigest()
    return int(h[:8], 16) % n


def _ilce(c, n=3):
    return (c.get("ilceler") or [])[:n]


def _komsu(c, n=3):
    return [SEHIR_INDEKS[k]["ad"] for k in (c.get("komsu") or []) if k in SEHIR_INDEKS][:n]


def _liste(xs):
    xs = [x for x in xs if x]
    if not xs:
        return ""
    if len(xs) == 1:
        return xs[0]
    return ", ".join(xs[:-1]) + " ve " + xs[-1]


def _sektor(c, n=3):
    return [s.lower() for s in (c.get("sektorler") or [])[:n]]


def _ekip_cumle(c, ad, ek, is_):
    if (c.get("ekip") or "") == "ortak":
        return ("%s%s %s için kamera gereken günlerde yerel çözüm ortağımızla, "
                "kurgu-renk-yönetmenlik tarafında kendi ekibimizle çalışıyoruz."
                % (ad, ek, is_))
    return ("%s%s %s için kendi ekibimizle sahaya çıkıyoruz; çeken de "
            "kurgulayan da aynı masa." % (ad, ek, is_))


# ---------------------------------------------------------------- hizmetler
def insaat3d(c):
    ad, ek = c["ad"], c["ek"]
    il = c["slug"]
    p = []
    ins = (c.get("insaat") or "").strip()
    cog = (c.get("cografya") or "").strip()
    ilce = _ilce(c)
    kom = _komsu(c)

    if ins:
        v = _sec(il, "i1", 3)
        p.append([
            "<p><strong>%s%s konut pazarı:</strong> %s</p>" % (_e(ad), ek, _e(ins)),
            "<p>%s Bu tablo 3D görselleştirmenin %s%s neyi göstermesi gerektiğini de "
            "belirliyor.</p>" % (_e(ins), _e(ad), ek),
            "<p>%s%s proje tanıtımına başlamadan önce şuna bakıyoruz. %s</p>"
            % (_e(ad), ek, _e(ins)),
        ][v])
    if cog:
        v = _sec(il, "i2", 3)
        p.append([
            "<p><strong>Çevre modeli:</strong> %s Render'da arsanın çevresini de bu "
            "gerçek dokuyla kuruyoruz; alıcı projeyi boşlukta değil, tanıdığı yerde "
            "görüyor.</p>" % _e(cog),
            "<p>%s Yerleşim maketinde ve dış cephe render'ında bu çevreyi olduğu gibi "
            "modelliyoruz — komşu yapılar, yol kotu, manzara açısı.</p>" % _e(cog),
            "<p>Arsa çevresi %s%s şöyle: %s Simülasyonda güneş açısını ve manzarayı "
            "bu gerçek konuma göre hesaplıyoruz.</p>" % (_e(ad), ek, _e(cog)),
        ][v])
    if ilce:
        p.append("<p><strong>Nerede:</strong> %s hattındaki projelerde çalışıyoruz; "
                 "modelleme uzaktan yürüdüğü için ilçe farkı süreyi değiştirmiyor. "
                 "%s</p>" % (_e(_liste(ilce)), _e(_ekip_cumle(c, ad, ek, "şantiye çekimi"))))
    if kom:
        p.append("<p>%s yönündeki projelerle aynı keşif gününe alınabiliyor; drone "
                 "gereken işlerde ulaşım gideri bölünüyor.</p>" % _e(_liste(kom)))
    return "\n    ".join(p)


def emlak(c):
    ad, ek = c["ad"], c["ek"]
    il = c["slug"]
    p = []
    em = (c.get("emlak") or "").strip()
    cog = (c.get("cografya") or "").strip()
    ilce = _ilce(c, 4)
    kom = _komsu(c)
    if em:
        v = _sec(il, "e1", 3)
        p.append([
            "<p><strong>%s%s portföy nasıl:</strong> %s</p>" % (_e(ad), ek, _e(em)),
            "<p>%s Emlak videosunun %s%s hangi soruya cevap vermesi gerektiği "
            "buradan çıkıyor.</p>" % (_e(em), _e(ad), ek),
            "<p>%s%s ilan videosu planlarken ilk baktığımız şey pazarın kendisi. %s</p>"
            % (_e(ad), ek, _e(em)),
        ][v])
    if cog:
        v = _sec(il, "e2", 2)
        p.append([
            "<p><strong>Açılış planı:</strong> %s Mülkün konumunu bu gerçek çevreyle "
            "birlikte gösteriyoruz — alıcının ilk sorusu 'nerede' ve 'neye bakıyor'.</p>" % _e(cog),
            "<p>Havadan açılışta %s%s elimizde şu var: %s Mülk bu çevrenin içinde "
            "gösterildiğinde ilan listede ayrışıyor.</p>" % (_e(ad), ek, _e(cog)),
        ][v])
    if ilce:
        p.append("<p><strong>Kapsam:</strong> %s dahil ilin tamamı. Aynı güne birden "
                 "fazla mülk sığdırıldığında ulaşım tek kez yazılıyor; portföyü toplu "
                 "çekmek mülk başına maliyeti düşürüyor.</p>" % _e(_liste(ilce)))
    if kom:
        p.append("<p>%s hattındaki ofislerle ortak çekim günü planlanabiliyor. %s</p>"
                 % (_e(_liste(kom)), _e(_ekip_cumle(c, ad, ek, "emlak çekimi"))))
    return "\n    ".join(p)


def urun(c):
    ad, ek = c["ad"], c["ek"]
    il = c["slug"]
    p = []
    san = (c.get("sanayi") or "").strip()
    sek = _sektor(c, 4)
    kom = _komsu(c)
    if san:
        v = _sec(il, "u1", 3)
        p.append([
            "<p><strong>%s sanayisi ne üretiyor:</strong> %s</p>" % (_e(ad), _e(san)),
            "<p>%s Ürün animasyonunun %s%s hangi üreticiye, neyi anlatması gerektiği "
            "bu tablodan çıkıyor.</p>" % (_e(san), _e(ad), ek),
            "<p>%s%s animasyon planlarken sanayinin kendisinden başlıyoruz. %s</p>"
            % (_e(ad), ek, _e(san)),
        ][v])
    if sek:
        p.append("<p><strong>Hangi ürün, hangi anlatım:</strong> %s%s öne çıkan %s "
                 "üreticileri için sırasıyla çalışma prensibi, kesit anlatım ve üretim "
                 "hattı animasyonu en çok işe yarayan üç biçim. Fuar ve ihracat sunumu "
                 "için çok dilli altyazı aynı projeden çıkıyor.</p>"
                 % (_e(ad), ek, _e(_liste(sek))))
    p.append("<p><strong>Uzaktan:</strong> Ürün animasyonu için %s%s bulunmamız "
             "gerekmiyor; teknik çizim, CAD dosyası ya da ürün fotoğrafı yeterli. "
             "Gerçek çekimle birleştirilecekse tesise bir gün geliyoruz.</p>" % (_e(ad), ek))
    if kom:
        p.append("<p>%s yönündeki üreticilerle aynı tesis ziyaretine birleştirilebiliyor.</p>"
                 % _e(_liste(kom)))
    return "\n    ".join(p)


def drone(c):
    ad, ek = c["ad"], c["ek"]
    il = c["slug"]
    p = []
    cog = (c.get("cografya") or "").strip()
    san = (c.get("sanayi") or "").strip()
    ilce = _ilce(c)
    if cog:
        v = _sec(il, "d1", 3)
        p.append([
            "<p><strong>%s%s havadan ne var:</strong> %s</p>" % (_e(ad), ek, _e(cog)),
            "<p>%s Uçuş planını bu unsurlara göre kuruyoruz — açılış planı, ışık "
            "saati ve irtifa.</p>" % _e(cog),
            "<p>%s%s drone planı yaparken ilk baktığımız şey ne göründüğü. %s</p>"
            % (_e(ad), ek, _e(cog)),
        ][v])
    if san:
        p.append("<p><strong>Tesis ve sanayi:</strong> %s Havadan çekim burada "
                 "tesisin ölçeğini ve lojistik konumunu tek karede anlatıyor.</p>" % _e(san))
    if ilce:
        p.append("<p><strong>Uçuş bölgesi:</strong> %s hattı dahil ilin tamamı. Her "
                 "uçuştan önce bölgenin kısıt durumuna bakıyor, gerekiyorsa izni biz "
                 "alıyoruz; yasak bölgede uçmuyoruz. %s</p>"
                 % (_e(_liste(ilce)), _e(_ekip_cumle(c, ad, ek, "drone çekimi"))))
    return "\n    ".join(p)


def klip(c):
    ad, ek = c["ad"], c["ek"]
    p = []
    kul = (c.get("kultur") or "").strip()
    mek = (c.get("mekan") or "").strip()
    cog = (c.get("cografya") or "").strip()
    if kul:
        p.append("<p><strong>%s%s sahne:</strong> %s</p>" % (_e(ad), ek, _e(kul)))
    if mek:
        p.append("<p><strong>Mekân:</strong> %s%s en çok kullandığımız yerler: %s. "
                 "Rotayı gün ışığına göre kuruyoruz.</p>" % (_e(ad), ek, _e(mek)))
    elif cog:
        p.append("<p><strong>Mekân:</strong> %s Klipte bu dokuyu dış mekân planlarında "
                 "kullanıyoruz.</p>" % _e(cog))
    p.append("<p>%s</p>" % _e(_ekip_cumle(c, ad, ek, "klip çekimi")))
    return "\n    ".join(p)


def dugun(c):
    ad, ek = c["ad"], c["ek"]
    p = []
    dn = (c.get("dugun_notu") or "").strip()
    mek = (c.get("mekan") or "").strip()
    cog = (c.get("cografya") or "").strip()
    ilce = _ilce(c)
    if dn:
        p.append("<p><strong>%s%s düğün düzeni:</strong> %s</p>" % (_e(ad), ek, _e(dn)))
    if mek:
        p.append("<p><strong>Dış çekim:</strong> %s. Saati ve rotayı ışığa göre "
                 "birlikte planlıyoruz.</p>" % _e(mek))
    elif cog:
        p.append("<p><strong>Dış çekim:</strong> %s</p>" % _e(cog))
    if ilce:
        p.append("<p>%s dahil ilin her yerindeki salon ve kır mekânlarına geliyoruz. %s</p>"
                 % (_e(_liste(ilce)), _e(_ekip_cumle(c, ad, ek, "düğün çekimi"))))
    return "\n    ".join(p)


def isletme(c):
    ad, ek = c["ad"], c["ek"]
    p = []
    inot = (c.get("isletme_notu") or "").strip()
    sek = _sektor(c, 3)
    ilce = _ilce(c, 4)
    if inot:
        p.append("<p><strong>%s%s işletme ritmi:</strong> %s</p>" % (_e(ad), ek, _e(inot)))
    if sek:
        p.append("<p><strong>Kim istiyor:</strong> %s%s düzenli içerik ihtiyacı en çok "
                 "%s çevresindeki işletmelerden geliyor; aylık paketi o sektörün yoğun "
                 "saatine göre kuruyoruz.</p>" % (_e(ad), ek, _e(_liste(sek))))
    if ilce:
        p.append("<p><strong>Nerede:</strong> %s başta olmak üzere ilin tamamı. Aynı "
                 "gün birkaç işletme çekildiğinde ulaşım bölünüyor. %s</p>"
                 % (_e(_liste(ilce)), _e(_ekip_cumle(c, ad, ek, "işletme çekimi"))))
    return "\n    ".join(p)


ANALIZ = {"insaat3d": insaat3d, "emlak": emlak, "urun": urun, "drone": drone,
          "klip": klip, "dugun": dugun, "isletme": isletme}


def blok(c, tur, baslik=None):
    f = ANALIZ[tur]
    icerik = f(c)
    if not icerik:
        return ""
    ad, ek = c["ad"], c["ek"]
    baslik = baslik or "%s%s bu iş neye bakıyor" % (_e(ad), ek)
    return "<h2>%s</h2>\n    %s" % (baslik, icerik)
