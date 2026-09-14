# -*- coding: utf-8 -*-
"""
ÖRNEK ÇALIŞMA GÖRSELİ ÜRETİCİ

Firmaya "sizin işiniz için ne çekeriz" sorusunun görsel cevabı: sektöre özel
bir storyboard sayfası. Her kare, o sektörde gerçekten çekilecek planın
kendisi — çekim ölçeği, kamera hareketi, ne duyulacağı ve ekranda ne yazacağı.

SVG üretiliyor: tek dosya, ölçeklenebilir, e-postaya eklenebiliyor, yazdırılınca
bozulmuyor. Fotoğraf uydurmuyoruz — bu bir çekim planıdır, sahte bir iş değil.
"""
import html

# ---------------------------------------------------------------- storyboard
# (kare başlığı, plan ölçeği, kamera, sahnede ne var, ekranda ne yazar, ses)
PLANLAR = {
"produksiyon": [
 ("Kamera arkası", "Genel", "Sabit", "Kurulum anı: ışık, tripod, ekip", "ÇEKİM GÜNÜ", "Ortam sesi"),
 ("Kadraj kararı", "Yakın", "Sabit", "Monitörde kadraj, elle işaret", "Neden bu açı", "Konuşma"),
 ("Öncesi", "Genel", "Sabit", "Ham görüntü, düzeltilmemiş", "ÖNCE", "Sessiz"),
 ("Sonrası", "Genel", "Aynı kadraj", "Renk ve kurgu sonrası", "SONRA", "Müzik girer"),
 ("3D devreye giriyor", "Grafik", "Model dönüyor", "Kameranın giremediği yer modelleniyor", "3D", "Vurgu"),
 ("Çoklu format", "Bölünmüş ekran", "Sabit", "Aynı iş yatay/kare/dikey yan yana", "Tek çekim, üç sürüm", "—"),
 ("Teslim", "Grafik", "Sabit", "Dosya listesi ve iletişim", "TESLİM · WhatsApp", "Müzik biter"),
],
"insaat": [
 ("Açılış", "Geniş / havadan", "Drone yavaş alçalarak",
  "Şantiyenin bütünü, arkada şehir silueti", "PROJE ADI · BURSA", "Tek enstrüman, sakin"),
 ("Ölçek", "Genel", "Sabit, yavaş kaydırma",
  "Vinç ve yükselen blok; insan figürü ölçek versin", "12 kat · 96 daire", "Şantiye sesi kısık"),
 ("Malzeme", "Yakın (makro)", "Sabit, sığ alan derinliği",
  "Cephe kaplaması, doğrama profili, zemin dokusu", "Cephe: kompozit panel", "Sessiz, sadece doku"),
 ("İçeri giriş", "Öznel / tek plan", "Gimbal, kesintisiz yürüyüş",
  "Daire kapısından girip salona, oradan balkona", "3+1 · 145 m²", "Adım sesi + ambiyans"),
 ("Manzara kanıtı", "Genel", "Balkondan dışa doğru çevrinme",
  "Pencereden gerçek manzara, kat numarası köşede", "8. kat · güneybatı", "Rüzgâr"),
 ("Söz–teslim", "Bölünmüş ekran", "Sabit",
  "Solda render, sağda aynı açıdan teslim edilmiş hali", "Söz verilen / teslim edilen", "Vurgu sesi"),
 ("Kapanış", "Havadan çıkış", "Drone yükselerek uzaklaşır",
  "Bina ve çevresi; logo ve iletişim", "İLETİŞİM · WhatsApp", "Müzik biter"),
],
"emlak": [
 ("Kapı", "Yakın", "Sabit", "Anahtar kapıyı açıyor", "Nilüfer · 3+1", "Anahtar sesi"),
 ("İlk izlenim", "Öznel tek plan", "Gimbal, kapıdan salona", "Kesintisiz giriş", "145 m² brüt", "Ambiyans"),
 ("Salon", "Genel", "Yavaş yatay kaydırma", "Doğal ışıkta salon", "Güney cephe", "Sessiz"),
 ("Mutfak detayı", "Yakın", "Sabit", "Tezgâh, dolap içi, ankastre", "Ankastre dahil", "—"),
 ("Manzara", "Genel", "Balkondan çevrinme", "Pencereden gerçek görüntü", "8. kat", "Rüzgâr"),
 ("Konum", "Havadan", "Drone yukarı", "Binadan okula/metroya yürüyüş hattı", "Metro 6 dk yürüme", "Müzik"),
 ("Danışman", "Orta", "Sabit, göz hizası", "Danışman kısa konuşma", "Ara: 0500 000 00 00", "Doğrudan ses"),
],
"mimarlik": [
 ("Konsept", "Grafik", "—", "Eskiz çizgisinden modele geçiş", "Konsept → uygulama", "Sessiz"),
 ("Kütle", "Genel / 3D", "Yörünge hareketi", "Bina kütlesi çevresinde dönüş", "Kütle ve yerleşim", "Tek nota"),
 ("Malzeme", "Makro / 3D", "Yavaş kaydırma", "Doku örnekleri yakın plan", "Beton · ahşap · cam", "—"),
 ("İç mekân", "Öznel / 3D", "Kamera içeride yürüyor", "Işığın gün içinde değişimi", "09:00 → 18:00", "Ambiyans"),
 ("Kesit", "Grafik", "Kesit açılıyor", "Bina kesiti ve kat ilişkileri", "Kesit A-A", "Vurgu"),
 ("Çevre", "Havadan / 3D", "Yükselerek uzaklaşma", "Yapı ve çevresi", "Vaziyet planı", "Müzik biter"),
],
"sanayi": [
 ("Tesis", "Geniş", "Havadan alçalma", "Fabrika dıştan", "ÜRETİM TESİSİ", "Sakin müzik"),
 ("Hat", "Genel", "Yavaş kaydırma", "Çalışan üretim hattı", "Günlük kapasite", "Makine sesi"),
 ("İnsan", "Orta", "Sabit", "Operatör işini yaparken", "20 yıllık ekip", "Ambiyans"),
 ("Kesit animasyon", "Grafik / 3D", "Makine yarı saydam", "İçeride ne olduğu görünür hâle gelir",
  "Çalışma prensibi", "Vurgu sesi"),
 ("Akış", "Grafik / 3D", "Ok ve renkli akış", "Hammadde → ürün yolu", "Hammadde → ürün", "—"),
 ("Kalite", "Makro", "Sabit", "Ölçüm ve kontrol anı", "±0,02 mm tolerans", "Sessiz"),
 ("İhracat", "Genel", "Sabit", "Paketleme ve sevkiyat", "EXPORT · EN/DE altyazı", "Müzik"),
],
"mobilya": [
 ("Ürün", "Genel", "Yörünge", "Ürün mekân içinde", "Model adı", "Sakin"),
 ("Doku", "Makro", "Yavaş kaydırma", "Kumaş, ahşap damarı, dikiş", "Kumaş: keten", "—"),
 ("Mekanizma", "Yakın", "Sabit", "Açılma/kapanma hareketi", "Tek elle açılır", "Mekanizma sesi"),
 ("Varyant", "Grafik / 3D", "Renk geçişleri", "Aynı sahnede renk seçenekleri", "6 renk seçeneği", "—"),
 ("Ölçek", "Orta", "Sabit", "İnsan ürünün yanında", "210 × 90 cm", "Ambiyans"),
 ("Mekânda", "Genel", "Yavaş kaydırma", "Kurulu oda görüntüsü", "Şimdi mağazada", "Müzik biter"),
],
"otel": [
 ("Varış", "Havadan", "Drone yaklaşır", "Tesis ve çevresi", "TESİS ADI", "Sakin müzik"),
 ("Lobi", "Öznel", "Gimbal, girişten içeri", "Kesintisiz giriş", "—", "Ambiyans"),
 ("Oda", "Genel", "Yavaş kaydırma", "Gerçek ölçüde oda", "Deniz manzaralı · 32 m²", "Sessiz"),
 ("Detay", "Makro", "Sabit", "Nevresim, banyo amenity, kahvaltı tabağı", "Detaylar", "—"),
 ("Manzara", "Genel", "Balkondan çevrinme", "Gerçek manzara, saat bilgisiyle", "Gün batımı · 19:40", "Rüzgâr"),
 ("Sosyal alan", "Genel", "Kaydırma", "Havuz/restoran, insanlı", "Akşam programı", "Kalabalık uğultusu"),
 ("Rezervasyon", "Grafik", "Sabit", "İletişim ve rezervasyon", "Doğrudan rezervasyon", "Müzik biter"),
],
"isletme": [
 ("Dışarıdan", "Genel", "Sabit", "İşletme cephesi, tabela okunur", "İŞLETME ADI · BURSA", "Sokak sesi"),
 ("İçeri", "Öznel", "Gimbal, kapıdan içeri", "Kesintisiz giriş", "—", "Ambiyans"),
 ("İş başında", "Orta", "Sabit", "İşin yapıldığı an", "Nasıl yapılıyor", "Doğrudan ses"),
 ("Detay", "Makro", "Sabit", "İşin en iyi göründüğü detay", "Detay", "—"),
 ("İnsan", "Orta", "Sabit, göz hizası", "Sahibi/ustası kısa konuşma", "12 yıldır buradayız", "Doğrudan ses"),
 ("Çağrı", "Grafik", "Sabit", "Adres, saat, iletişim", "Yol tarifi · WhatsApp", "Müzik biter"),
],
}

SEKTOR_AD = {"produksiyon": "Prodüksiyon / Ajans", "insaat": "İnşaat / Müteahhit", "emlak": "Emlak", "mimarlik": "Mimarlık",
             "sanayi": "Sanayi / Üretim", "mobilya": "Mobilya / Ürün",
             "otel": "Otel / Turizm", "isletme": "İşletme"}


def _e(x):
    return html.escape(str(x if x is not None else ""), quote=True)


def _sar(metin, uzunluk):
    """Metni satırlara böler (SVG'de otomatik sarma yok)."""
    kelime, satir, cikti = metin.split(), "", []
    for k in kelime:
        deneme = (satir + " " + k).strip()
        if len(deneme) > uzunluk and satir:
            cikti.append(satir); satir = k
        else:
            satir = deneme
    if satir:
        cikti.append(satir)
    return cikti


def storyboard(sektor, firma_adi="", sehir=""):
    """Sektöre özel çekim planını SVG storyboard olarak üretir."""
    planlar = PLANLAR.get(sektor, PLANLAR["isletme"])
    sektor_ad = SEKTOR_AD.get(sektor, "İşletme")

    SUT, KARE_G, KARE_Y = 3, 300, 176
    BOSLUK, IC_Y = 26, 132
    satir_sayisi = (len(planlar) + SUT - 1) // SUT
    hucre_y = KARE_Y + IC_Y
    G = SUT * KARE_G + (SUT - 1) * BOSLUK + 72
    UST = 148
    Y = UST + satir_sayisi * hucre_y + (satir_sayisi - 1) * BOSLUK + 74

    p = []
    p.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
             'viewBox="0 0 %d %d" font-family="Manrope, Helvetica, Arial, sans-serif">' % (G, Y, G, Y))
    p.append('<defs>'
             '<linearGradient id="kare" x1="0" y1="0" x2="1" y2="1">'
             '<stop offset="0" stop-color="#1d1116"/><stop offset="1" stop-color="#0c0c10"/></linearGradient>'
             '<linearGradient id="ust" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#131317"/><stop offset="1" stop-color="#0A0A0C"/></linearGradient>'
             '</defs>')
    p.append('<rect width="%d" height="%d" fill="#0A0A0C"/>' % (G, Y))
    p.append('<rect width="%d" height="%d" fill="url(#ust)"/>' % (G, UST))
    p.append('<line x1="0" y1="%d" x2="%d" y2="%d" stroke="#EFEDE8" stroke-opacity=".13"/>' % (UST, G, UST))

    # başlık
    p.append('<text x="36" y="46" fill="#E8452C" font-family="monospace" font-size="11" '
             'letter-spacing="3.4">LUNA YAPIM · ÇEKİM PLANI</text>')
    baslik = ("%s için çekim planı" % firma_adi) if firma_adi else "%s çekim planı" % sektor_ad
    p.append('<text x="36" y="86" fill="#EFEDE8" font-size="27" font-weight="700" '
             'letter-spacing="-.6">%s</text>' % _e(baslik[:52]))
    alt = "%s%s · %d kare · tek çekim günü" % (sektor_ad, (" · " + sehir) if sehir else "", len(planlar))
    p.append('<text x="36" y="116" fill="#8C8A84" font-size="13.5">%s</text>' % _e(alt))
    p.append('<text x="%d" y="86" fill="#8C8A84" font-size="12" text-anchor="end">'
             'Bu bir çekim planıdır — hazır görsel değil.</text>' % (G - 36))

    for i, (kare_ad, olcek, kamera, sahne, ekran, ses) in enumerate(planlar):
        sut, sat = i % SUT, i // SUT
        x = 36 + sut * (KARE_G + BOSLUK)
        y = UST + 34 + sat * (hucre_y + BOSLUK)

        # kare çerçevesi
        p.append('<rect x="%d" y="%d" width="%d" height="%d" rx="4" fill="url(#kare)" '
                 'stroke="#EFEDE8" stroke-opacity=".14"/>' % (x, y, KARE_G, KARE_Y))
        # kadraj yardım çizgileri (üçler kuralı)
        for ç in (1, 2):
            p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#EFEDE8" stroke-opacity=".07"/>'
                     % (x + KARE_G * ç / 3, y, x + KARE_G * ç / 3, y + KARE_Y))
            p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#EFEDE8" stroke-opacity=".07"/>'
                     % (x, y + KARE_Y * ç / 3, x + KARE_G, y + KARE_Y * ç / 3))
        # kare numarası
        p.append('<rect x="%d" y="%d" width="34" height="21" rx="2" fill="#E8452C"/>' % (x, y))
        p.append('<text x="%d" y="%d" fill="#fff" font-family="monospace" font-size="11" '
                 'text-anchor="middle" font-weight="700">%02d</text>' % (x + 17, y + 15, i + 1))
        # plan ölçeği rozeti
        p.append('<text x="%d" y="%d" fill="#EFEDE8" fill-opacity=".55" font-family="monospace" '
                 'font-size="9.5" letter-spacing="1.6" text-anchor="end">%s</text>'
                 % (x + KARE_G - 10, y + 16, _e(olcek.upper())))
        # sahnede ne var
        for j, satir in enumerate(_sar(sahne, 30)[:3]):
            p.append('<text x="%d" y="%d" fill="#EFEDE8" fill-opacity=".82" font-size="12.5">%s</text>'
                     % (x + 14, y + KARE_Y - 54 + j * 17, _e(satir)))
        # ekranda yazan (altyazı kutusu)
        if ekran and ekran != "—":
            gen = min(KARE_G - 28, 9 + len(ekran) * 6.4)
            p.append('<rect x="%d" y="%d" width="%d" height="20" rx="2" fill="#000" fill-opacity=".62"/>'
                     % (x + 14, y + KARE_Y - 30, gen))
            p.append('<text x="%d" y="%d" fill="#EFEDE8" font-family="monospace" font-size="10">%s</text>'
                     % (x + 20, y + KARE_Y - 16, _e(ekran[:34])))

        # kare altı künye
        ay = y + KARE_Y + 20
        p.append('<text x="%d" y="%d" fill="#EFEDE8" font-size="14.5" font-weight="700">%s</text>'
                 % (x, ay, _e(kare_ad)))
        for etiket, deger, dy in (("KAMERA", kamera, 22), ("SES", ses, 0)):
            if not deger or deger == "—":
                continue
            ay += dy if dy else 22
            p.append('<text x="%d" y="%d" fill="#E8452C" font-family="monospace" font-size="8.5" '
                     'letter-spacing="1.4">%s</text>' % (x, ay, etiket))
            for j, satir in enumerate(_sar(deger, 34)[:2]):
                p.append('<text x="%d" y="%d" fill="#8C8A84" font-size="12">%s</text>'
                         % (x, ay + 15 + j * 14, _e(satir)))
            ay += 15 + (len(_sar(deger, 34)[:2]) - 1) * 14

    # alt bilgi
    p.append('<line x1="36" y1="%d" x2="%d" y2="%d" stroke="#EFEDE8" stroke-opacity=".13"/>'
             % (Y - 46, G - 36, Y - 46))
    p.append('<text x="36" y="%d" fill="#8C8A84" font-size="12">'
             'Luna Yapım · lunayapim.com · Bu plan tek çekim gününde tamamlanacak şekilde kurulmuştur.</text>'
             % (Y - 22))
    p.append('</svg>')
    return "\n".join(p)


def yaz(sektor, yol, firma_adi="", sehir=""):
    g = storyboard(sektor, firma_adi, sehir)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(g)
    return yol
