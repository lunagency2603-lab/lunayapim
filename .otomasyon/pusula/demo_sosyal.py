# -*- coding: utf-8 -*-
"""
SOSYAL MEDYA DEMO SAYFASI

Bir aday için: mevcut sosyal durumu (kanıtıyla), sektörüne uygun içerik planı,
o planın nasıl görüneceğini gösteren EKRAN KURGULARI, çalışmanın olası sonucu
(sebepleriyle, hesap yöntemi verilmeden) ve Luna Yapım'ın görsel üretim referansları.

Ekran kurguları GERÇEK EKRAN GÖRÜNTÜSÜ DEĞİLDİR ve sayfada böyle işaretlenir —
firmanın hesabından alınmış gibi gösterilmez.
"""
import os, html, datetime
from .ayarlar import CIKTI, SEKTORLER, FIRMA
from . import sosyal as S
from . import referans as RF
from . import fark as FK

# Luna Yapım'ın yayındaki işleri — referans bölümünde thumbnail'leriyle gösterilir
# Referanslar artık pusula/referans.py kütüğünden geliyor — tek kaynak.
# Sektöre göre seçiliyor ve her işin o sektördeki vurgusu yazılıyor.
def _referanslar(sektor, adet=6):
    return [{"ad": i["ad"], "tur": i["tur"], "vurgu": RF.vurgu(i, sektor),
             "gorsel": RF.gorsel_url(i), "baglanti": RF.baglanti(i),
             "kare": RF.tum_kareler(i)}
            for i in RF.sektor_icin(sektor, adet)]


HIZMET_SAYFA = {
 "insaat":   ("İnşaat 3D Modelleme", "hizmetler/insaat-3d-modelleme.html"),
 "emlak":    ("Emlak Video Çekimi", "hizmetler/emlak-kurumsal.html"),
 "mimarlik": ("Mimari Görselleştirme", "hizmetler/insaat-3d-modelleme.html"),
 "sanayi":   ("Ürün & Hizmet Animasyonu", "hizmetler/urun-animasyon.html"),
 "mobilya":  ("Ürün Animasyonu", "hizmetler/urun-animasyon.html"),
 "otel":     ("Tanıtım Filmi & Drone", "hizmetler/drone-fpv.html"),
 "isletme":  ("İşletme Tanıtım & Sosyal Medya", "hizmetler/isletme-tanitim.html"),
}

# Format -> kurgu görselinin rengi/etiketi
FORMAT_STIL = {
 "reels":    ("#E8452C", "▶ REELS"),
 "carousel": ("#3BA55C", "❯ KAYDIR"),
 "tekli":    ("#8C8A84", "◻ GÖRSEL"),
 "story":    ("#E0A32E", "◔ STORY"),
 "uzun":     ("#4A7BC8", "▶ UZUN"),
}


def _e(x):
    return html.escape(str(x if x is not None else ""), quote=True)


# ---------------------------------------------------------------- beklenen sonuç
# Sebepli anlatım. Hesaplama yöntemi paylaşılmaz — sadece ne olacağı ve NEDEN.
BEKLENEN = {
 "insaat": [
  ("Proje sorusu geliyor", "Şantiye ilerlemesi ve daire turu düzenli görününce, satış ofisini aramadan önce "
   "mesajdan soru soran alıcı sayısı artıyor. Soru gelen yerde satış konuşması başlıyor."),
  ("Gelen alıcı daha hazır", "Videoyu izleyip gelen kişi kat planını, manzarayı ve konumu zaten görmüş oluyor; "
   "satış ekibi anlatmakla değil, kapatmakla uğraşıyor."),
  ("Şehir dışı alıcıya erişim", "İlanı görmeyen ama akışta karşılaşan alıcı ortaya çıkıyor. "
   "İnşaatta alıcının önemli kısmı başka şehirden geliyor ve onlara ancak buradan ulaşılıyor."),
  ("Fiyat itirazı azalıyor", "Malzeme yakın planı ve render-teslim karşılaştırması, kalite iddiasını "
   "sözle değil görüntüyle kanıtlıyor; pazarlık masasında konum güçleniyor."),
 ],
 "emlak": [
  ("Boş gezdirme azalıyor", "Mülkü videoda gezen alıcı, uygun değilse zaten aramıyor. "
   "Randevuya gelen kişi gerçekten ilgilenen kişi oluyor."),
  ("Portföy toplamak kolaylaşıyor", "Mülkünü satacak kişi, ofisin ilanları nasıl sunduğuna bakıyor. "
   "Videolu ilan gören mal sahibi 'benimkini de bu ofis satsın' diyor."),
  ("İlan daha uzun inceleniyor", "Videolu ilanda ziyaretçi sayfada daha çok kalıyor; "
   "ilan sitelerinin sıralaması bundan etkileniyor."),
  ("Danışman tanınır oluyor", "Emlakta güven kişiye kurulur. Yüzü ve sesi tanınan danışmana "
   "doğrudan mesaj gelmeye başlıyor."),
 ],
 "mimarlik": [
  ("Meslektaş ağı iş getiriyor", "Detay ve süreç içerikleri meslektaşlar tarafından paylaşılıyor; "
   "işlerin önemli kısmı bu ağdan geliyor."),
  ("İşveren süreci anlıyor", "Eskizden render'a giden içerik, mimarlık hizmetinin neden bir bedeli "
   "olduğunu anlatıyor; fiyat konuşması kolaylaşıyor."),
  ("Portföy her an hazır", "Sunum istendiğinde dosya hazırlamak yerine hesabın linki veriliyor."),
 ],
 "sanayi": [
  ("İhracat müşterisi tesisi görmüş oluyor", "Yurt dışı alıcı fabrikayı ziyaret edemiyor. "
   "Üretim videosu ziyaretin yerini tutuyor ve ilk güveni kuruyor."),
  ("Fuar öncesi randevu geliyor", "Fuardan haftalar önce paylaşılan ürün ve stand içeriği, "
   "standa gelmeden randevu isteyen müşteri yaratıyor."),
  ("Teknik anlatım kısalıyor", "Kesit animasyonunu izlemiş müşteriyle yapılan görüşme, "
   "sıfırdan anlatılan görüşmeden çok daha kısa ve sonuca yakın oluyor."),
  ("Nitelikli eleman başvurusu", "İşveren markası görünen fabrikaya başvuru artıyor; "
   "bu, sanayide beklenmedik ama en çok geri dönüş alınan etkilerden biri."),
 ],
 "mobilya": [
  ("Varyant sorusu bitiyor", "Renk ve kumaş seçenekleri görünce müşteri mağazaya karar vermiş geliyor."),
  ("Kurulum endişesi kalkıyor", "Montaj videosu, satın almayı engelleyen en yaygın tereddüdü ortadan kaldırıyor."),
  ("Mağazaya trafik", "Showroom turu içeriği yerel erişimde en yüksek dönüşen tür."),
 ],
 "otel": [
  ("Doğrudan rezervasyon artıyor", "Acente üzerinden değil, doğrudan mesajdan gelen rezervasyon "
   "komisyon ödemeden ciroya dönüyor."),
  ("Sezon dışı doluluk", "Çevre ve deneyim içerikleri, tesisin sadece yaz aylarında değil "
   "yıl boyu akılda kalmasını sağlıyor."),
  ("Fiyat sorgusu azalıyor", "Oda ve kahvaltı görselleri beklentiyi doğru kuruyor; "
   "misafir fiyatı gördüğü değere göre değerlendiriyor."),
 ],
 "isletme": [
  ("Haritada üst sıraya çıkıyor", "Düzenli ve taze görsel, işletme profilinin bulunurluğunu artırıyor. "
   "Yerel işletmede müşterinin büyük kısmı haritadan geliyor."),
  ("Yeni müşteri keşfi", "Dikey video, mahalle dışındaki insana ulaşan tek ucuz kanal."),
  ("'Buradan gördüm' diyen müşteri", "İçerik yayınlandıktan sonra gelen müşterinin bunu söylemesi, "
   "kanalın çalıştığının en somut kanıtı oluyor."),
  ("Sadık müşteri bağı", "Ekibi ve arkadaki emeği gören müşteri geri geliyor; "
   "yerel işletmede asıl kâr tekrar eden müşteride."),
 ],
}


def olasi_sonuc(sektor):
    return BEKLENEN.get(sektor) or BEKLENEN["isletme"]


# ---------------------------------------------------------------- sayfa
SABLON = """<!DOCTYPE html><html lang="tr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>@AD@ — Sosyal Medya Çalışması · Luna Yapım</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,800&family=Manrope:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{--ink:#0A0A0C;--ink2:#131317;--ink3:#1b1b21;--bone:#EFEDE8;--kirmizi:#E8452C;
--yesil:#3BA55C;--sari:#E0A32E;--gri:#8C8A84;--cizgi:rgba(239,237,232,.13)}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--ink);color:var(--bone);font-family:"Manrope",system-ui,sans-serif;line-height:1.6}
.wrap{max-width:1060px;margin:0 auto;padding:0 26px}
h1,h2,h3{font-family:"Bricolage Grotesque","Manrope",sans-serif;font-weight:800;letter-spacing:-.03em;line-height:1.06}
.etk{font-family:"Space Mono",ui-monospace,monospace;font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:var(--kirmizi)}
header{border-bottom:1px solid var(--cizgi);padding:18px 0}
.mrk{display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap}
.mrk b{font-family:"Bricolage Grotesque",sans-serif;font-size:17px}
.kapak{padding:58px 0 42px;border-bottom:1px solid var(--cizgi);background:linear-gradient(180deg,var(--ink2),var(--ink))}
.kapak h1{font-size:clamp(27px,4.4vw,44px);margin:13px 0 15px}
.kapak p{color:rgba(239,237,232,.76);max-width:62ch}
section{padding:44px 0;border-bottom:1px solid var(--cizgi)}
section h2{font-size:clamp(21px,3vw,30px);margin-bottom:12px}
section h3{font-size:17px;margin:22px 0 10px}
.alt{color:var(--gri);max-width:66ch;margin-bottom:20px;font-size:14.5px}
ul{list-style:none}
li{padding:8px 0 8px 22px;position:relative;color:rgba(239,237,232,.82)}
li::before{content:"\\2192";position:absolute;left:0;color:var(--kirmizi)}
table{width:100%;border-collapse:collapse;font-size:14.5px;margin-top:10px}
th,td{text-align:left;padding:11px 12px;border-bottom:1px solid var(--cizgi);vertical-align:top}
th{font-family:"Space Mono",monospace;font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--kirmizi)}
td{color:rgba(239,237,232,.8)}
.kanit{margin-top:7px;padding:9px 11px;background:rgba(239,237,232,.04);border-left:2px solid var(--gri);
border-radius:0 3px 3px 0;font-size:12.6px;color:var(--gri);line-height:1.5}
.kanit b{color:rgba(239,237,232,.72)}
.kanit .kaynak{display:block;margin-top:4px;font-family:"Space Mono",monospace;font-size:10.5px;color:#6f6d68}
.rozet{display:inline-block;font-family:"Space Mono",monospace;font-size:9.5px;letter-spacing:.12em;
text-transform:uppercase;padding:3px 9px;border-radius:2px;border:1px solid var(--cizgi);color:var(--gri)}
.rozet.iyi{border-color:var(--yesil);color:var(--yesil)}
.rozet.kotu{border-color:var(--kirmizi);color:var(--kirmizi)}
.rozet.orta{border-color:var(--sari);color:var(--sari)}
.hesaplar{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin-top:16px}
.hesap{border:1px solid var(--cizgi);border-radius:4px;padding:16px 18px}
.hesap b{display:block;font-size:16px;margin-bottom:4px}
.hesap small{color:var(--gri);font-size:12.5px;display:block;line-height:1.5}

/* ---- ekran kurguları ---- */
.kurgular{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:26px;margin-top:22px;align-items:start;justify-items:center}
.telefon{background:#050506;border:8px solid #1c1c22;border-radius:26px;padding:0;overflow:hidden;
box-shadow:0 18px 44px rgba(0,0,0,.5);width:100%;max-width:296px;height:524px;margin:0 auto;
display:flex;flex-direction:column}
.tbar{height:26px;background:#0d0d11;display:flex;align-items:center;justify-content:center}
.tbar i{width:52px;height:5px;background:#2a2a31;border-radius:99px;display:block}
.profil{padding:16px 14px 10px;border-bottom:1px solid rgba(255,255,255,.07)}
.pust{display:flex;gap:14px;align-items:center}
.avatar{width:56px;height:56px;border-radius:50%;background:linear-gradient(135deg,#E8452C,#7a2216);
display:grid;place-items:center;font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:20px;color:#fff;flex-shrink:0}
.psay{display:flex;gap:16px;flex:1;text-align:center}
.psay div{flex:1}
.psay b{display:block;font-size:14px}
.psay span{font-size:10px;color:var(--gri)}
.pad{margin-top:10px;font-size:13px;font-weight:700}
.pbio{font-size:11.5px;color:var(--gri);line-height:1.45;margin-top:3px}
.izgara{display:grid;grid-template-columns:repeat(3,1fr);gap:2px;background:rgba(255,255,255,.06);
flex:1;min-height:0}
.kare{min-height:0;background:var(--ink3);position:relative;display:flex;align-items:flex-end;padding:7px;overflow:hidden}
.kare::before{content:"";position:absolute;inset:0;background:
linear-gradient(135deg,rgba(232,69,44,.16),rgba(255,255,255,.02) 60%)}
.kare span{position:relative;font-size:8.6px;line-height:1.25;color:rgba(239,237,232,.92);font-weight:600;
text-shadow:0 1px 3px rgba(0,0,0,.7)}
.kare i{position:absolute;top:6px;right:7px;font-style:normal;font-family:"Space Mono",monospace;
font-size:7px;letter-spacing:.06em;padding:2px 4px;border-radius:2px;background:rgba(0,0,0,.55)}
/* reels kurgusu */
.reels{position:relative;flex:1;min-height:0;background:linear-gradient(160deg,#241014,#0a0a0c 60%);
display:flex;flex-direction:column;justify-content:flex-end;padding:14px}
.reels .kanca{font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:19px;line-height:1.12;
text-shadow:0 2px 10px rgba(0,0,0,.8);margin-bottom:8px}
.reels .altyazi{font-size:11px;background:rgba(0,0,0,.6);padding:4px 7px;border-radius:3px;
align-self:flex-start;max-width:92%}
.reels .ust{position:absolute;top:12px;left:14px;font-family:"Space Mono",monospace;font-size:9px;
letter-spacing:.12em;color:rgba(255,255,255,.75)}
.reels .yan{position:absolute;right:10px;bottom:70px;display:flex;flex-direction:column;gap:12px;
align-items:center;font-size:9px;color:rgba(255,255,255,.8)}
.reels .yan em{font-style:normal;display:block;text-align:center;font-size:14px}
.kurgu-not{font-size:11.5px;color:var(--gri);text-align:center;margin-top:10px;line-height:1.5}
.kurgu-baslik{font-family:"Space Mono",monospace;font-size:10px;letter-spacing:.16em;text-transform:uppercase;
color:var(--kirmizi);text-align:center;margin-bottom:10px}
.uyari{border-left:3px solid var(--sari);background:rgba(224,163,46,.08);padding:14px 16px;
margin-top:18px;font-size:13.5px;color:rgba(239,237,232,.82);border-radius:0 3px 3px 0}
.plan{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px;margin-top:18px}
.fikir{border:1px solid var(--cizgi);border-radius:4px;padding:16px 18px}
.fikir b{display:block;font-size:16px;margin:6px 0 6px}
.fikir .kanca{font-size:13.5px;color:rgba(239,237,232,.8)}
.fikir .neden{font-size:13px;color:var(--gri);margin-top:8px;padding-top:8px;border-top:1px solid var(--cizgi)}
.sonuc{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px;margin-top:16px}
.sonuc div{border:1px solid var(--cizgi);border-left:3px solid var(--yesil);border-radius:0 4px 4px 0;padding:15px 17px}
.sonuc b{display:block;font-size:16px;margin-bottom:6px;color:var(--yesil)}
.sonuc p{font-size:13.5px;color:rgba(239,237,232,.78)}
.ref{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-top:18px}
.ref a{display:block;text-decoration:none;color:inherit;border:1px solid var(--cizgi);border-radius:4px;overflow:hidden;
transition:border-color .2s,transform .2s}
.ref a:hover{border-color:var(--kirmizi);transform:translateY(-2px)}
.ref .kapak{width:100%;aspect-ratio:16/9;display:block;background-size:cover;background-position:center;
background-color:#15151a;background-image:linear-gradient(135deg,rgba(232,69,44,.22),rgba(21,21,26,.9) 65%);
position:relative}
.ref .kapak::after{content:"▶";position:absolute;inset:0;display:grid;place-items:center;
font-size:26px;color:rgba(255,255,255,.62);text-shadow:0 2px 12px rgba(0,0,0,.7)}
.ref a,.ref .ref-kart{display:flex;flex-direction:column;text-decoration:none;color:inherit;
border:1px solid var(--cizgi);border-radius:4px;overflow:hidden;transition:.16s}
.ref .ref-kart:hover,.ref a:hover{border-color:var(--kirmizi)}
.fark{display:grid;gap:2px;margin-top:20px;border:1px solid var(--cizgi);border-radius:5px;overflow:hidden}
.fark-satir{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--cizgi)}
@media(max-width:760px){.fark-satir{grid-template-columns:1fr}}
.fark-satir>div{background:var(--ink);padding:20px 22px}
.fark-satir .sol{color:var(--gri)}
.fark-satir .sag{border-left:2px solid var(--kirmizi)}
.fark-et{font-family:"Space Mono",monospace;font-size:9.5px;letter-spacing:.18em;
text-transform:uppercase;display:block;margin-bottom:9px}
.fark-satir .sol .fark-et{color:#6f6d68}
.fark-satir .sag .fark-et{color:var(--kirmizi)}
.fark-sonuc{grid-column:1/-1;background:rgba(232,69,44,.07);padding:13px 22px;
font-size:13.5px;color:rgba(239,237,232,.8)}
.modeller{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:18px;margin-top:20px}
.model{border:1px solid var(--cizgi);border-radius:5px;padding:26px}
.model.one{border-color:var(--kirmizi);box-shadow:0 0 0 1px rgba(232,69,44,.22)}
.model h3{font-size:21px;margin-bottom:4px}
.model .rozet{margin-bottom:14px}
.model .kime{color:var(--gri);font-size:14px;line-height:1.6;margin-bottom:16px}
.model ol{margin:0 0 16px 18px;padding:0}
.model ol li{font-size:14px;line-height:1.6;margin-bottom:6px}
.model dl{display:grid;grid-template-columns:auto 1fr;gap:6px 14px;font-size:13.5px;margin-top:14px;
border-top:1px solid var(--cizgi);padding-top:14px}
.model dt{font-family:"Space Mono",monospace;font-size:9.5px;letter-spacing:.14em;
text-transform:uppercase;color:var(--kirmizi);padding-top:3px}
.model dd{margin:0;color:rgba(239,237,232,.82)}
.ref-vurgu{font-size:12.5px;line-height:1.55;color:var(--gri);margin-top:9px;
border-top:1px solid var(--cizgi);padding-top:9px}
.ref .bilgi{flex:1}
.ref .bilgi{padding:12px 14px}
.ref b{display:block;font-size:14.5px}
.ref small{color:var(--gri);font-size:12px}
.cta{background:var(--kirmizi);color:#fff;padding:42px 0}
.cta h2{max-width:22ch}
.btn{display:inline-block;margin-top:16px;margin-right:10px;background:var(--ink);color:var(--bone);
padding:13px 22px;border-radius:2px;text-decoration:none;font-weight:600}
.btn.c{background:transparent;border:1px solid rgba(255,255,255,.55);color:#fff}
footer{padding:24px 0;color:var(--gri);font-size:12.5px}
@media(max-width:640px){.kurgular{grid-template-columns:1fr}}
</style></head><body>
<header><div class="wrap mrk"><b>LUNA YAPIM</b><span class="etk">Sosyal Medya Çalışması · @TARIH@</span></div></header>

<div class="kapak"><div class="wrap">
  <p class="etk">@SEKTOR@ · @SEHIR@</p>
  <h1>@AD@ sosyal medyada bugün ne durumda, ne olabilir</h1>
  <p>Aşağıdaki tespitler herkese açık bilgilerden çıkarıldı; her satırın altında ne kontrol
     ettiğimiz ve nerede bulduğumuz yazıyor. Sonrasında sizin sektörünüzde ne çalıştığını,
     nasıl görüneceğini ve bunun ne işe yarayacağını anlattık.</p>
</div></div>

<section><div class="wrap">
  <h2>Bugünkü tablo</h2>
  <p class="alt">Sektörünüzde işe yarayan platformlara baktık: hangisi var, hangisi yok,
     var olan gerçekten sizin mi.</p>
  @HESAPLAR@
  <h3>Tespit edilenler</h3>
  <div class='tablo-kaydir'><table><tr><th>Eksik</th><th>Ne kontrol ettik / ne bulduk</th></tr>@EKSIKLER@</table></div>
</div></section>

<section><div class="wrap">
  <h2>Sizin sektörünüzde ne çalışıyor</h2>
  <p class="alt">Aşağıdakiler @SEKTOR_SADE@ tarafında en çok sonuç veren içerik türleri.
     Her birinin yanında neden işe yaradığını yazdık — moda olduğu için değil, işi olduğu için.</p>
  <div class="plan">@PLAN@</div>
  <h3>Aylık tempo önerisi</h3>
  <p class="alt">@TEMPO@</p>
</div></section>

<section><div class="wrap">
  <h2>Nasıl görünecek</h2>
  <p class="alt">Aşağıdakiler, yukarıdaki planın uygulandığında hesabınızda nasıl duracağını
     gösteren kurgulardır.</p>
  <div class="kurgular">
    <div>
      <div class="kurgu-baslik">Profil görünümü</div>
      <div class="telefon">
        <div class="tbar"><i></i></div>
        <div class="profil">
          <div class="pust">
            <div class="avatar">@BASHARF@</div>
            <div class="psay">
              <div><b>@GONDERI@</b><span>gönderi</span></div>
              <div><b>—</b><span>takipçi</span></div>
              <div><b>—</b><span>takip</span></div>
            </div>
          </div>
          <div class="pad">@AD@</div>
          <div class="pbio">@BIO@</div>
        </div>
        <div class="izgara">@IZGARA@</div>
      </div>
      <p class="kurgu-not">Kareler yukarıdaki içerik planından geliyor.<br>Takipçi sayısı boş bırakıldı — uydurma rakam koymuyoruz.</p>
    </div>
    <div>
      <div class="kurgu-baslik">Dikey video (Reels)</div>
      <div class="telefon">
        <div class="tbar"><i></i></div>
        <div class="reels">
          <div class="ust">@AD_KISA@ · @REELS_ETIKET@</div>
          <div class="yan"><span><em>♡</em>beğeni</span><span><em>💬</em>yorum</span><span><em>↗</em>paylaş</span></div>
          <div class="kanca">@REELS_KANCA@</div>
          <div class="altyazi">@REELS_ALT@</div>
        </div>
      </div>
      <p class="kurgu-not">İlk 3 saniyede kanca, altta altyazı.<br>Sesi kapalı izleyen için altyazı şart.</p>
    </div>
    <div>
      <div class="kurgu-baslik">Kaydırmalı görsel seti</div>
      <div class="telefon">
        <div class="tbar"><i></i></div>
        <div class="izgara" style="grid-template-columns:1fr">@CAROUSEL@</div>
      </div>
      <p class="kurgu-not">Kaydırdıkça anlatım ilerliyor.<br>En çok kaydedilen format bu.</p>
    </div>
  </div>
  <div class="uyari"><b>Bunlar örnek kurgudur.</b> Hesabınızdan alınmış ekran görüntüsü değildir;
    planın uygulandığında nasıl duracağını göstermek için Luna Yapım tarafından hazırlanmıştır.
    Gerçek çekim yapıldığında görseller sizin mekânınız, ürününüz ve ekibinizden olacak.</div>
</div></section>

<section><div class="wrap">
  <h2>Bizimle çalışırsanız ne değişir</h2>
  <p class="alt">Rakam vaadi vermiyoruz. Aşağıdakiler, bu çalışmanın sizin sektörünüzde
     hangi somut sonuçları neden ürettiğidir.</p>
  <div class="sonuc">@SONUC@</div>
  <div class="uyari">Ne kadar sürede olur? İlk fark genelde ikinci ayda görülüyor, çünkü
    hem içerik birikmesi hem de kanalın sizi tanıması zaman alıyor. İlk ayı ölçüm ayı olarak
    kullanıyoruz: gelen arama, harita görüntülenmesi ve "buradan gördüm" diyen müşteri sayılıyor.
    Rakam ikna etmezse devam etmiyorsunuz.</div>
</div></section>

<section><div class="wrap">
  <h2>Herkesin yaptığı şey, bir de bizim yaptığımız</h2>
  <p class="alt">Daha önce teklif aldıysanız aşağıdaki sol sütun tanıdık gelecek.
     Sağ sütun, aynı işi neden farklı yaptığımız.</p>
  <div class="fark">@FARK@</div>
</div></section>

<section><div class="wrap">
  <h2>Nasıl çalışırız — iki yol var</h2>
  <p class="alt">@MODEL_CUMLE@</p>
  <div class="modeller">@MODEL@</div>
</div></section>

<section><div class="wrap">
  <h2>Görsel üretimde bizim işimiz</h2>
  <p class="alt">Sosyal medya içeriğini reklam ajansı gözüyle değil, kamera arkasından
     gelen bir ekip olarak üretiyoruz. Aşağıdakiler yayında olan işlerimizden —
     üzerine dokunup izleyebilirsiniz.</p>
  <div class="ref">@REFERANS@</div>
  <h3>Bu işte ne yapıyoruz</h3>
  <ul>
    <li><b>Çekim</b> — sinema kamerası, ışık seti, gimbal ve FPV/klasik drone; hepsi aynı ekipte</li>
    <li><b>3D ve animasyon</b> — kameranın gösteremediği yerde modelleme devreye giriyor</li>
    <li><b>Kurgu ve renk</b> — asıl fark burada oluşuyor; ham görüntüyle arasındaki mesafe bu</li>
    <li><b>Çoklu format</b> — tek çekimden dikey, kare ve yatay sürümler; ayrıca ücret yok</li>
    <li><b>Altyazı ve grafik</b> — sesi kapalı izleyen için; izlenme süresini doğrudan etkiliyor</li>
  </ul>
  <p class="alt" style="margin-top:14px">Detaylı hizmet sayfası:
    <a href="https://lunayapim.com/@HIZMET_YOL@" style="color:var(--kirmizi)">@HIZMET_AD@ ↗</a></p>
</div></section>

<div class="cta"><div class="wrap">
  <p class="etk" style="color:rgba(255,255,255,.75)">Sıradaki adım</p>
  <h2>İlk ayı birlikte deneyelim, rakama bakalım.</h2>
  <a class="btn" href="https://wa.me/@WA@">WhatsApp'tan yaz</a>
  <a class="btn c" href="tel:@TEL@">@TEL@</a>
</div></div>
<footer><div class="wrap mrk"><span>Luna Yapım · lunayapim.com · Bursa</span><span>@TARIH@</span></div></footer>
</body></html>"""


def uret(aday, sosyal_sonuc, klasor=None):
    sektor = aday.get("sektor") or "isletme"
    sektor_ad = SEKTORLER.get(sektor, {}).get("ad", sektor)
    plan = S.icerik_plani(sektor, 8)
    tempo = S.TEMPO.get(sektor, S.TEMPO["isletme"])
    hesaplar = (sosyal_sonuc or {}).get("hesaplar", {})
    eksikler = (sosyal_sonuc or {}).get("eksikler", [])

    # hesap kartları
    if hesaplar:
        kartlar = []
        for p, h in hesaplar.items():
            sinif = "iyi" if h.get("eslesme", 0) >= 65 else ("orta" if h.get("eslesme", 0) >= 45 else "kotu")
            durum = ("açık" if h.get("acik") else ("açılmıyor" if h.get("acik") is False else "doğrulanamadı"))
            kartlar.append(
              '<div class="hesap"><b>%s</b>'
              '<span class="rozet %s">%s</span> <span class="rozet">%s</span>'
              '<small style="margin-top:8px">@%s</small>'
              '<small>%s</small>'
              '<small style="margin-top:6px">%s</small>'
              '<small><a href="%s" target="_blank" style="color:var(--kirmizi)">hesaba git ↗</a></small></div>'
              % (_e(h.get("ad", p)), sinif, _e(h.get("eslesme_yorum", "")), _e(durum),
                 _e(h.get("kullanici", "")), _e(h.get("nasil", "")), _e(h.get("teyit", "")),
                 _e(h.get("url", "#"))))
        hesap_html = '<div class="hesaplar">%s</div>' % "".join(kartlar)
    else:
        hesap_html = ('<div class="uyari">Sektörünüzde işe yarayan platformların hiçbirinde '
                      'doğrulanabilen bir hesap bulamadık. Bu, en baştan kurulacak demek — '
                      'iyi tarafı, dağınık bir geçmişi toparlamak zorunda kalmıyoruz.</div>')

    eksik_satir = []
    for e in eksikler:
        k = e["kanit"]
        eksik_satir.append(
          "<tr><td><strong>%s</strong></td><td><b>Kontrol:</b> %s"
          "<div class='kanit'><b>Bulgu:</b> %s<span class='kaynak'>kaynak: %s · %s</span></div></td></tr>"
          % (_e(e["baslik"]), _e(k["kontrol"]), _e(k["bulgu"]), _e(k["kaynak"]), _e(k["zaman"])))
    if not eksik_satir:
        eksik_satir.append("<tr><td colspan='2'>Belirgin bir eksik bulunamadı — mevcut hesaplar sağlam.</td></tr>")

    # plan kartları
    plan_html = "".join(
      '<div class="fikir"><span class="rozet" style="border-color:%s;color:%s">%s</span>'
      '<b>%s</b><p class="kanca">%s</p><p class="neden">%s</p></div>'
      % (FORMAT_STIL.get(f["format"], ("#8C8A84", ""))[0],
         FORMAT_STIL.get(f["format"], ("#8C8A84", ""))[0],
         _e(f["format_ad"]), _e(f["baslik"]), _e(f["kanca"]), _e(f["neden"]))
      for f in plan)

    tempo_metin = " · ".join(
      "%s %s" % (v, S.FORMAT_AD.get(k, k).lower()) for k, v in tempo.items() if v)
    tempo_metin += ". Tek çekim gününde toplanır; siz sadece yayınlarsınız."

    # ızgara kareleri (9 adet)
    kareler = []
    for i in range(9):
        f = plan[i % len(plan)]
        renk, etiket = FORMAT_STIL.get(f["format"], ("#8C8A84", "◻"))
        kareler.append(
          '<div class="kare" style="background:linear-gradient(150deg,%s22,#1b1b21 65%%)">'
          '<i style="color:%s">%s</i><span>%s</span></div>'
          % (renk, renk, _e(etiket), _e(f["baslik"])))

    # carousel: 3 kart
    car = []
    cf = next((x for x in plan if x["format"] == "carousel"), plan[0])
    for n, metin in enumerate([cf["baslik"], cf["kanca"], "Detaylı bilgi ve iletişim"], 1):
        car.append('<div class="kare" style="background:linear-gradient(150deg,#3BA55C1f,#1b1b21 65%%)">'
                   '<i style="color:#3BA55C">%d/3</i><span>%s</span></div>' % (n, _e(metin)))

    rf = next((x for x in plan if x["format"] == "reels"), plan[0])

    refler = _referanslar(sektor, 6)
    ref_parca = []
    for r in refler:
        kapak = (('<span class="kapak" style="background-image:linear-gradient(180deg,'
                  'rgba(0,0,0,.10),rgba(0,0,0,.42)),url(%s)" role="img" aria-label="%s"></span>')
                 % (_e(r["gorsel"]), _e(r["ad"])) if r["gorsel"]
                 else '<span class="kapak" role="img" aria-label="%s"></span>' % _e(r["ad"]))
        ic = ('<div class="bilgi"><b>%s</b><small>%s</small>'
              '<p class="ref-vurgu">%s</p></div>'
              % (_e(r["ad"]), _e(r["tur"]), _e(r["vurgu"])))
        if r["baglanti"]:
            ref_parca.append('<a href="%s" target="_blank" rel="noopener">%s%s</a>'
                             % (_e(r["baglanti"]), kapak, ic))
        else:
            ref_parca.append('<div class="ref-kart">%s%s</div>' % (kapak, ic))
    ref_html = "".join(ref_parca)

    fark_html = "".join(
      '<div class="fark-satir">'
      '<div class="sol"><span class="fark-et">Genelde böyle yapılır</span>%s</div>'
      '<div class="sag"><span class="fark-et">Bizde böyle</span>%s</div>'
      '<div class="fark-sonuc"><b>Sonuç:</b> %s</div></div>'
      % (_e(f["sıradan"]), _e(f["bizde"]), _e(f["sonuc"]))
      for f in FK.farklar(sektor, 5))

    md = FK.model(sektor)
    def _model_kart(anahtar):
        m = md[anahtar]
        one = (anahtar == md["onerilen"])
        return ('<div class="model%s"><h3>%s</h3>'
                '<span class="rozet"%s>%s</span>'
                '<p class="kime">%s</p><ol>%s</ol>'
                '<dl><dt>Süre</dt><dd>%s</dd><dt>Ödeme</dt><dd>%s</dd>'
                '<dt>Artısı</dt><dd>%s</dd><dt>Dikkat</dt><dd>%s</dd></dl></div>'
                % (" one" if one else "", _e(m["ad"]),
                   ' style="border-color:var(--kirmizi);color:var(--kirmizi)"' if one else "",
                   "size önerdiğimiz" if one else "diğer yol",
                   _e(m["kime"]),
                   "".join("<li>%s</li>" % _e(x) for x in m["nasil"]),
                   _e(m["sure"]), _e(m["odeme"]), _e(m["avantaj"]), _e(m["dikkat"])))
    model_html = _model_kart(md["onerilen"]) + _model_kart(
        "aylik" if md["onerilen"] == "proje" else "proje")

    sonuc_html = "".join(
      '<div><b>%s</b><p>%s</p></div>' % (_e(b), _e(n)) for b, n in olasi_sonuc(sektor))

    hizmet_ad, hizmet_yol = HIZMET_SAYFA.get(sektor, HIZMET_SAYFA["isletme"])
    bio = "%s · %s%s" % (sektor_ad, aday.get("sehir") or "", 
                          (" / " + aday["ilce"]) if aday.get("ilce") else "")

    g = SABLON
    yer = {
      "@AD@": _e(aday["ad"]),
      "@AD_KISA@": _e((aday["ad"] or "")[:22]),
      "@BASHARF@": _e("".join(w[0] for w in (aday["ad"] or "?").split()[:2]).upper()),
      "@SEKTOR@": _e(sektor_ad),
      "@SEKTOR_SADE@": _e(sektor_ad.split("/")[0].strip().lower()),
      "@SEHIR@": _e(aday.get("sehir") or ""),
      "@TARIH@": datetime.date.today().strftime("%d.%m.%Y"),
      "@HESAPLAR@": hesap_html,
      "@EKSIKLER@": "".join(eksik_satir),
      "@PLAN@": plan_html,
      "@TEMPO@": _e(tempo_metin),
      "@IZGARA@": "".join(kareler),
      "@CAROUSEL@": "".join(car),
      "@GONDERI@": str(sum(v for v in tempo.values() if v)),
      "@BIO@": _e(bio),
      "@REELS_KANCA@": _e(rf["baslik"]),
      "@REELS_ALT@": _e(rf["kanca"][:70]),
      "@REELS_ETIKET@": _e(FORMAT_STIL.get(rf["format"], ("", "REELS"))[1]),
      "@SONUC@": sonuc_html,
      "@FARK@": fark_html,
      "@MODEL@": model_html,
      "@MODEL_CUMLE@": _e(FK.model_cumlesi(sektor)),
      "@REFERANS@": ref_html,
      "@HIZMET_AD@": _e(hizmet_ad),
      "@HIZMET_YOL@": hizmet_yol,
      "@WA@": FIRMA["wa"], "@TEL@": FIRMA["telefon"],
    }
    for k, v in yer.items():
        g = g.replace(k, v)

    if klasor:
        os.makedirs(klasor, exist_ok=True)
        yol = os.path.join(klasor, "sosyal-demo.html")
        open(yol, "w", encoding="utf-8").write(g)
        return yol, g
    return None, g
