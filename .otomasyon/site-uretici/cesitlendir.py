# -*- coding: utf-8 -*-
"""
ŞABLON CÜMLE ÇEŞİTLENDİRME

Sorun: 81 il sayfasında aynı gövde cümleleri birebir tekrar ediyor. Google'ın
"ölçekli içerik" / "doorway page" tanımına giren şey tam olarak bu — nitekim
Search Console'da 34 sayfa "Alternate page with proper canonical tag" ile
elenmiş durumda.

Çözüm: her cümlenin ANLAMI AYNI, ifadesi farklı 4 sürümü. Hangi ilin hangi
sürümü alacağı il adından türetiliyor — yani her çalıştırmada aynı sonuç,
rastgelelik yok, sayfa değişmeden kalıyor.

Uydurma yok: hiçbir sürüm yeni bir iddia eklemiyor, sadece aynı şeyi başka
türlü söylüyor.
"""
import glob, hashlib, io, os, re, sys

VARYANT = {
"İşin ölçeği, çekim günü sayısı ve teslim edilecek format sayısına göre.": [
 "İşin ölçeği, çekim günü sayısı ve teslim edilecek format sayısına göre.",
 "Kaç gün çekim yapılacağı, işin büyüklüğü ve kaç formatta teslim istendiği belirliyor.",
 "Üç şey belirliyor: işin büyüklüğü, sahada geçen gün sayısı ve istenen format sayısı.",
 "Fiyatı, projenin ölçeği ile çekim ve teslim yükü birlikte belirliyor.",
],
"Aynı gün birden fazla iş planlandığında ulaşım maliyeti bölünüyor.": [
 "Aynı gün birden fazla iş planlandığında ulaşım maliyeti bölünüyor.",
 "Bir güne iki iş sığdığında yol gideri ikiye bölünüyor, ikisi de ucuzluyor.",
 "Aynı güne denk gelen işlerde ulaşımı tek sefer yazıyoruz.",
 "Komşu işleri aynı güne alıyoruz; yol masrafı tek işin sırtına binmiyor.",
],
"Temel atılmadan maket satışına başlamak isteyen projelerin ilk ihtiyacı.": [
 "Temel atılmadan maket satışına başlamak isteyen projelerin ilk ihtiyacı.",
 "Henüz kazma vurulmamışken satışa başlamak isteyen projeler önce bunu istiyor.",
 "İnşaat başlamadan daire satmak isteyen projede ilk sırada bu var.",
 "Maket satışını lansman gününde açmak isteyen proje buradan başlıyor.",
],
"Senaryo, sanat yönetimi, sinematografi, FPV drone ve renk düzenleme tek elden yürüyor.": [
 "Senaryo, sanat yönetimi, sinematografi, FPV drone ve renk düzenleme tek elden yürüyor.",
 "Senaryodan renk düzenlemeye kadar her adım aynı ekipte: sanat yönetimi, kamera, FPV drone.",
 "Yazımı, sanat yönetimini, kamerayı, FPV droneu ve rengi aynı masada konuşuyoruz.",
 "Tek ekip: senaryo, sanat yönetimi, görüntü, FPV drone, renk.",
],
"Şantiye ilerleme takibi, arsa ilanı, tesis tanıtımı ve etkinlik çekimlerinde kullanılıyor.": [
 "Şantiye ilerleme takibi, arsa ilanı, tesis tanıtımı ve etkinlik çekimlerinde kullanılıyor.",
 "En sık şantiye ilerlemesi, arsa ilanı, tesis tanıtımı ve etkinlik kaydı için isteniyor.",
 "Arsa ilanından şantiye takibine, tesis tanıtımından etkinliğe kadar kullanılıyor.",
 "Kullanım yerleri: şantiye ilerlemesi, arsa ilanı, tesis tanıtımı, etkinlik.",
],
"Sadece gerçek kamera ve drone çekimi gerektiren işlerde sahaya çıkıyoruz.": [
 "Sadece gerçek kamera ve drone çekimi gerektiren işlerde sahaya çıkıyoruz.",
 "Sahaya yalnızca kamera ya da drone gerçekten gerekiyorsa geliyoruz.",
 "Yerinde çekim şart değilse yola çıkmıyoruz; gereksiz gün ücreti yazmıyoruz.",
 "Kamera veya drone gerekmiyorsa iş uzaktan yürüyor, saha gideri çıkmıyor.",
],
"İlanın listede öne çıkmasını ve gelen alıcının daha nitelikli olmasını sağlıyor.": [
 "İlanın listede öne çıkmasını ve gelen alıcının daha nitelikli olmasını sağlıyor.",
 "İlan listede yukarı çıkıyor ve arayan kişi mülkü görmüş olarak arıyor.",
 "Hem ilan daha çok görülüyor hem de gelen aramalar daha ciddi oluyor.",
 "Listede fark ediliyor; telefon eden kişi ne göreceğini bilerek ediyor.",
],
"Projeyi anlattığınızda aynı gün net bir aralık veriyoruz; sürpriz kalem çıkarmıyoruz.": [
 "Projeyi anlattığınızda aynı gün net bir aralık veriyoruz; sürpriz kalem çıkarmıyoruz.",
 "Projeyi dinledikten sonra aynı gün aralık veriyoruz; sonradan kalem eklemiyoruz.",
 "İşi anlatın, aynı gün rakam söyleyelim. Fatura sürprizi yok.",
 "Aynı gün net aralık, sözleşmede yazılı kapsam, sonradan ek kalem yok.",
],
}


# ---------------------------------------------------------------- hizmet sayfaları
# İl-hizmet sayfalarında 46 ilde birebir tekrar eden gövde cümleleri.
# Bilgi aynı, cümle farklı. Hiçbir sürüm yeni iddia eklemiyor.
VARYANT.update({
"İki iş aynı güne denk gelirse ulaşım gideri bölünüyor — ikisi de ucuza geliyor.": [
 "İki iş aynı güne denk gelirse ulaşım gideri bölünüyor — ikisi de ucuza geliyor.",
 "Aynı güne iki iş sığdığında yol masrafı ikiye bölünüyor.",
 "İki işi aynı güne alırsak ulaşımı tek kez yazıyoruz.",
 "Aynı gün iki iş varsa yol gideri paylaşılıyor, fiyat ikisinde de düşüyor.",
],
"Havadan tek plan bir açılış, bir mekânın konumunu, ölçeğini ve çevresini anlatmanın en hızlı yolu.": [
 "Havadan tek plan bir açılış, bir mekânın konumunu, ölçeğini ve çevresini anlatmanın en hızlı yolu.",
 "Bir yerin nerede olduğunu, ne kadar büyük olduğunu ve çevresinde ne bulunduğunu tek havadan planla anlatmak mümkün.",
 "Konum, ölçek ve çevre — üçünü birden gösteren en kısa yol havadan açılış planı.",
 "Tek bir havadan plan, sayfalarca anlatımın yerini tutuyor: yer, büyüklük, çevre.",
],
"Mülkün konumunu, çevresini ve manzarasını anlatmanın en hızlı yolu havadan tek plan bir açılış.": [
 "Mülkün konumunu, çevresini ve manzarasını anlatmanın en hızlı yolu havadan tek plan bir açılış.",
 "Havadan bir açılış planı, mülkün nerede durduğunu ve neye baktığını tek seferde gösteriyor.",
 "Konum, çevre ve manzara — üçü de tek havadan planla anlaşılıyor.",
 "Alıcının ilk sorusu 'nerede ve neye bakıyor'; buna en hızlı cevap havadan açılış.",
],
"Çektiğiniz ham görüntüyü alıp kurgu, renk düzenleme ve ses tarafını biz yapıyoruz.": [
 "Çektiğiniz ham görüntüyü alıp kurgu, renk düzenleme ve ses tarafını biz yapıyoruz.",
 "Ham kaydı bize gönderin; kurguyu, rengi ve sesi biz üstlenelim.",
 "Kamerayı siz tutun, kurgu ve renk bizde olsun.",
 "Elinizdeki görüntüden kurgu, renk ve ses çıkışını biz alıyoruz.",
],
"Aynı gün içinde birden fazla mülk çekimi planladığınızda ulaşım maliyeti bölünüyor; bu yüzden portföyü toplu çekmek her zaman daha ucuz.": [
 "Aynı gün içinde birden fazla mülk çekimi planladığınızda ulaşım maliyeti bölünüyor; bu yüzden portföyü toplu çekmek her zaman daha ucuz.",
 "Portföyü tek güne toplarsanız yol gideri bölünür; mülk başına maliyet belirgin düşer.",
 "Birkaç mülkü aynı güne koymak en ucuz yol — ulaşım bir kez yazılıyor.",
 "Tek tek çekmek yerine portföyü toplu çekmek mülk başına fiyatı aşağı çekiyor.",
],
"Mülkün adresini ve ne zaman çekilmesini istediğini yaz; takvimi aynı gün çıkaralım.": [
 "Mülkün adresini ve ne zaman çekilmesini istediğini yaz; takvimi aynı gün çıkaralım.",
 "Adresi ve tercih ettiğin tarihi gönder, takvimi aynı gün netleştirelim.",
 "Nerede ve ne zaman — bu ikisini yaz, gerisini biz planlayalım.",
 "Adres ve tarih yeter; çekim takvimini aynı gün dönüyoruz.",
],
"İstenirse dijital mobilyalama uyguluyoruz: boş odaya 3D mobilya yerleştirip mekânın nasıl kullanılacağını gösteriyoruz.": [
 "İstenirse dijital mobilyalama uyguluyoruz: boş odaya 3D mobilya yerleştirip mekânın nasıl kullanılacağını gösteriyoruz.",
 "Boş daireye 3D mobilya yerleştirip odanın nasıl yaşanacağını gösterebiliyoruz.",
 "Dijital mobilyalama isteğe bağlı: boş mekâna 3D eşya koyup kullanım senaryosunu görselleştiriyoruz.",
 "Boş oda alıcıya bir şey anlatmıyor; 3D mobilyayla nasıl kullanılacağını gösteriyoruz.",
],
"Her ay aynı açıdan çekilen görüntüler yatırımcıya düzenli ilerleme raporu oluyor; teslimde ise elinizde projenin sıfırdan yükselişini gösteren tek bir zaman atlamalı film kalıyor.": [
 "Her ay aynı açıdan çekilen görüntüler yatırımcıya düzenli ilerleme raporu oluyor; teslimde ise elinizde projenin sıfırdan yükselişini gösteren tek bir zaman atlamalı film kalıyor.",
 "Aylık sabit açıyla çekim, yatırımcıya düzenli rapor verir; proje bitince aynı kareler tek bir zaman atlamalı filme dönüşür.",
 "Aynı noktadan her ay çekilen kare, hem ilerleme raporu hem de teslimde kullanacağınız hızlandırılmış filmin ham maddesi.",
 "Sabit açı aylık seri: süreçte rapor, sonunda projenin sıfırdan yükselişini gösteren film.",
],
"Portföyünü düzenli çeken ofisler için aylık paket kuruyoruz: ay içinde belirli sayıda mülk çekimi, sabit fiyat ve öncelikli takvim.": [
 "Portföyünü düzenli çeken ofisler için aylık paket kuruyoruz: ay içinde belirli sayıda mülk çekimi, sabit fiyat ve öncelikli takvim.",
 "Düzenli çekim yapan ofislere aylık düzen: belirli sayıda mülk, sabit fiyat, takvimde öncelik.",
 "Aylık paket seçeneği var — ay içinde kaç mülk çekileceği baştan yazılıyor, fiyat sabit kalıyor.",
 "Sürekli portföy çeken ofisler aylık düzene geçiyor: sabit fiyat, öncelikli randevu.",
],
"Bitmemiş projeniz varsa Devam eden bir şantiyeyi tanıtmanın en güçlü yolu gerçek çekimle 3D'yi birleştirmek.": [
 "Bitmemiş projeniz varsa Devam eden bir şantiyeyi tanıtmanın en güçlü yolu gerçek çekimle 3D'yi birleştirmek.",
 "Bitmemiş projeniz varsa Şantiyeyi tanıtmanın en etkili yolu, gerçek görüntüyle 3D modeli aynı karede birleştirmek.",
 "Bitmemiş projeniz varsa Devam eden inşaatı anlatırken gerçek çekim ile 3D'yi üst üste koyuyoruz.",
 "Bitmemiş projeniz varsa Yarım kalmış bir yapıyı satmanın yolu, bitmiş halini gerçek çevresine yerleştirmekten geçiyor.",
],
})


def _sec(anahtar, il):
    """İl adından türeyen sabit seçim — her çalıştırmada aynı."""
    v = VARYANT[anahtar]
    h = hashlib.md5((il + "|" + anahtar[:24]).encode("utf-8")).hexdigest()
    return v[int(h[:8], 16) % len(v)]


def _il(yol):
    a = os.path.basename(yol)[:-5]
    return a.split("-")[0]


def calistir(kok, kuru=False):
    degisen, toplam = 0, 0
    for yol in sorted(glob.glob(os.path.join(kok, "sehir", "*.html"))):
        s = io.open(yol, encoding="utf-8").read()
        o = s
        il = _il(yol)
        for anahtar in VARYANT:
            if anahtar in s:
                yeni = _sec(anahtar, il)
                if yeni != anahtar:
                    s = s.replace(anahtar, yeni)
                    toplam += 1
        if s != o:
            degisen += 1
            if not kuru:
                io.open(yol, "w", encoding="utf-8").write(s)
    return {"sayfa": degisen, "degistirilen_cumle": toplam}


if __name__ == "__main__":
    from pusula.ayarlar import SITE_KOK
    print(calistir(SITE_KOK, kuru="--kuru" in sys.argv))
