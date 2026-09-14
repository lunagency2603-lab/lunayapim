# -*- coding: utf-8 -*-
"""Panel arayüzü — tek dosya HTML/CSS/JS. Veri /api/* uçlarından gelir."""

SAYFA = r"""<!DOCTYPE html>
<html lang="tr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Luna Pusula — Üretim Fabrikası</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,800&family=Manrope:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{--ink:#0A0A0C;--ink2:#131317;--ink3:#1a1a20;--bone:#EFEDE8;--kirmizi:#E8452C;
--yesil:#3BA55C;--sari:#E0A32E;--gri:#8C8A84;--cizgi:rgba(239,237,232,.13)}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--ink);color:var(--bone);font-family:"Manrope",system-ui,-apple-system,sans-serif;
font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}
h1,h2,h3{font-family:"Bricolage Grotesque","Manrope",sans-serif;font-weight:800;letter-spacing:-.03em;line-height:1.05}
.etk{font-family:"Space Mono",ui-monospace,monospace;font-size:10px;letter-spacing:.2em;text-transform:uppercase}
a{color:var(--kirmizi);text-decoration:none}
header{position:sticky;top:0;z-index:50;background:rgba(10,10,12,.94);backdrop-filter:blur(14px);
border-bottom:1px solid var(--cizgi)}
.hbar{max-width:1560px;margin:0 auto;padding:13px 24px;display:flex;align-items:center;gap:20px;flex-wrap:wrap}
.logo{font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:17px;letter-spacing:-.02em}
.logo span{color:var(--kirmizi)}
nav{display:flex;gap:3px;flex-wrap:wrap;margin-left:auto}
nav button{background:none;border:1px solid transparent;color:var(--bone);opacity:.62;cursor:pointer;
font-family:inherit;font-size:14px;font-weight:600;padding:8px 14px;border-radius:2px;transition:.16s}
nav button:hover{opacity:1}
nav button.aktif{opacity:1;color:var(--kirmizi);border-color:var(--kirmizi)}
.durumlambasi{display:flex;align-items:center;gap:7px;font-family:"Space Mono",monospace;font-size:10px;
letter-spacing:.14em;text-transform:uppercase;color:var(--gri)}
.nokta{width:8px;height:8px;border-radius:50%;background:var(--gri)}
.nokta.calisiyor{background:var(--kirmizi);animation:nb 1s infinite}
@keyframes nb{50%{opacity:.25}}
main{max-width:1560px;margin:0 auto;padding:28px 24px 90px}
.sayfa{display:none}.sayfa.aktif{display:block}
.baslik h2{font-size:29px}
.altbaslik{color:var(--gri);font-size:14.5px;margin:6px 0 24px;max-width:86ch}

.izgara{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px}
.kart{background:var(--ink2);border:1px solid var(--cizgi);border-radius:4px;padding:22px 20px;
cursor:pointer;transition:.2s;position:relative;overflow:hidden}
.kart:hover{border-color:var(--kirmizi);transform:translateY(-2px)}
.kart::before{content:"";position:absolute;left:0;top:0;height:3px;width:0;background:var(--kirmizi);transition:width .35s}
.kart:hover::before{width:100%}
.kart h3{font-size:20px;margin:8px 0 6px}
.kart .kisa{color:var(--gri);font-size:14px;margin-bottom:14px}
.kart .mini{display:flex;gap:14px;flex-wrap:wrap;font-size:12.5px;color:var(--gri);
border-top:1px solid var(--cizgi);padding-top:12px}
.kart .mini b{color:var(--bone);display:block;font-size:13px}

.perde{position:fixed;inset:0;background:rgba(4,4,6,.72);z-index:80;display:none}
.perde.acik{display:block}
.cekmece{position:fixed;top:0;right:0;bottom:0;width:min(780px,96vw);background:var(--ink);
border-left:1px solid var(--cizgi);z-index:90;overflow-y:auto;transform:translateX(100%);
transition:transform .28s cubic-bezier(.2,.8,.3,1)}
.cekmece.acik{transform:none}
.cekmece .ic{padding:28px 30px 70px}
.kapat{position:absolute;top:16px;right:20px;background:none;border:0;color:var(--bone);font-size:26px;cursor:pointer;z-index:2}
.blok{margin-top:24px}
.blok>.etk{color:var(--kirmizi);display:block;margin-bottom:10px}
.blok ul{list-style:none}
.blok li{padding:7px 0 7px 20px;position:relative;color:rgba(239,237,232,.82);font-size:14.5px;
border-bottom:1px solid rgba(239,237,232,.06)}
.blok li::before{content:"›";position:absolute;left:0;color:var(--kirmizi)}
.mesaj{background:var(--ink2);border-left:3px solid var(--kirmizi);padding:15px 17px;font-size:14.5px;
color:rgba(239,237,232,.86);border-radius:0 3px 3px 0;white-space:pre-wrap}
.itiraz{border:1px solid var(--cizgi);border-radius:3px;padding:13px 15px;margin-bottom:9px}
.itiraz b{display:block;color:var(--kirmizi);font-size:14px;margin-bottom:5px}
.itiraz p{font-size:14px;color:rgba(239,237,232,.78)}
.satir{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1px;background:var(--cizgi);
border:1px solid var(--cizgi);margin-top:14px}
.satir div{background:var(--ink);padding:13px 15px}
.satir .etk{color:var(--gri);display:block;margin-bottom:5px}
.satir b{font-size:14.5px}

.arac{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px;align-items:center}
label.k{display:flex;align-items:center;gap:7px;font-size:13.5px;color:rgba(239,237,232,.8);cursor:pointer;
border:1px solid var(--cizgi);padding:8px 12px;border-radius:2px}
label.k input{accent-color:var(--kirmizi)}
select,input[type=text],input[type=number],input[type=date],input[type=password],input[type=email],textarea{
background:var(--ink2);border:1px solid var(--cizgi);color:var(--bone);padding:9px 12px;border-radius:2px;
font-family:inherit;font-size:14px}
textarea{width:100%;min-height:90px;resize:vertical;line-height:1.5}
.dug{background:var(--kirmizi);border:0;color:#fff;padding:9px 16px;border-radius:2px;
font-family:inherit;font-weight:600;font-size:14px;cursor:pointer;
display:inline-block;text-decoration:none;line-height:1.2;text-align:center}
.dug.sade{background:transparent;border:1px solid var(--cizgi);color:var(--bone)}
.dug.mini{padding:5px 10px;font-size:12.5px}
.dug:disabled{opacity:.4;cursor:not-allowed}
button.dug:hover:not(:disabled){opacity:.9}
table{width:100%;border-collapse:collapse;font-size:14px}
th,td{text-align:left;padding:10px 11px;border-bottom:1px solid var(--cizgi);vertical-align:middle}
th{font-family:"Space Mono",ui-monospace,monospace;font-size:9.5px;letter-spacing:.16em;
text-transform:uppercase;color:var(--kirmizi);white-space:nowrap;cursor:pointer;user-select:none}
tr:hover td{background:rgba(239,237,232,.03)}
tr.secili td{background:rgba(232,69,44,.08)}
.rz{display:inline-block;font-family:"Space Mono",ui-monospace,monospace;font-size:9px;letter-spacing:.12em;
text-transform:uppercase;padding:3px 8px;border-radius:2px;border:1px solid var(--cizgi);color:var(--gri)}
.rz.sicak{border-color:var(--kirmizi);color:var(--kirmizi)}
.rz.ok{border-color:var(--yesil);color:var(--yesil)}
.skorc{font-weight:700}
small{color:var(--gri)}

.konsol{background:#050506;border:1px solid var(--cizgi);border-radius:4px;padding:16px 18px;
font-family:"Space Mono",ui-monospace,monospace;font-size:12.5px;line-height:1.65;color:#cfcdc8;
max-height:420px;overflow-y:auto;white-space:pre-wrap;word-break:break-word}
.konsol .y{color:var(--kirmizi)}
.konsol .b{color:var(--yesil)}
.ilerleme{height:5px;background:rgba(239,237,232,.08);border-radius:99px;overflow:hidden;margin:12px 0}
.ilerleme i{display:block;height:100%;background:var(--kirmizi);transition:width .3s}

.huni{max-width:760px}
.hbas{display:flex;justify-content:space-between;font-size:14px;margin-bottom:5px}
.hcubuk{height:34px;background:rgba(239,237,232,.07);border-radius:3px;overflow:hidden;margin-bottom:16px}
.hcubuk i{display:flex;align-items:center;height:100%;padding-left:12px;font-size:12.5px;font-weight:700;
color:#fff;background:linear-gradient(90deg,var(--kirmizi),#b8341f)}

.pano{display:grid;grid-template-columns:repeat(7,minmax(180px,1fr));gap:10px;overflow-x:auto;padding-bottom:10px}
.sut{background:var(--ink2);border:1px solid var(--cizgi);border-radius:4px;padding:12px;min-height:180px}
.sut>.etk{display:flex;justify-content:space-between;color:var(--gri);margin-bottom:10px}
.is{background:var(--ink3);border:1px solid var(--cizgi);border-radius:3px;padding:11px 12px;margin-bottom:8px}
.is b{display:block;font-size:13.5px;margin-bottom:3px}
.is small{display:block;font-size:11.5px}
.is .tas{display:flex;gap:4px;margin-top:8px}
.is .tas button{flex:1;background:transparent;border:1px solid var(--cizgi);color:var(--gri);
border-radius:2px;cursor:pointer;font-size:11px;padding:3px}
.is .tas button:hover{border-color:var(--kirmizi);color:var(--kirmizi)}

.kutular{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:1px;
background:var(--cizgi);border:1px solid var(--cizgi);margin-bottom:26px}
.kutu{background:var(--ink);padding:19px 17px}
.kutu-yazi{width:100%;background:#12100f;color:var(--bone);border:1px solid #2a2724;
  border-radius:6px;padding:9px;font:inherit;resize:vertical}
.mk-s{display:flex;justify-content:space-between;gap:12px;align-items:center;
  padding:11px 0;border-top:1px solid #221f1d}
.mk-s:first-child{border-top:none}
.mk-s b{font-size:14.5px}
.mk-s .kel{color:var(--gri);font:11px/1.4 "Space Mono",monospace}
.mk-m{display:flex;gap:10px;padding:9px 0;border-top:1px solid #221f1d;align-items:flex-start}
.mk-m:first-child{border-top:none}
.mk-m .im{flex:0 0 18px;font-weight:700}
.mk-m .ok{color:#8fce8f} .mk-m .yok{color:var(--kirmizi)}
.mk-m .ne{color:var(--gri);font-size:12.5px}
.mk-m .ya{color:var(--bone);font-size:12.5px;opacity:.85;margin-top:3px}
.mk-m .ya::before{content:"→ ";color:var(--kirmizi)}
.rz{display:inline-block;padding:2px 7px;border-radius:4px;font:10px/1.6 "Space Mono",monospace;
  background:#2a2724;color:var(--gri)}
.kg-u{display:flex;gap:12px;padding:13px 0;border-top:1px solid #221f1d;align-items:flex-start}
.kg-u:first-child{border-top:none}
.kg-nokta{flex:0 0 9px;height:9px;border-radius:50%;margin-top:6px}
.kg-kritik{background:var(--kirmizi)} .kg-onemli{background:#d8a13a} .kg-bilgi{background:#5a7f9c}
.kg-u b{display:block;font-size:15px;margin-bottom:2px}
.kg-u .sebep{color:var(--gri);font-size:13.5px;line-height:1.55}
.kg-u .adim{color:var(--bone);font-size:13px;margin-top:5px;opacity:.85}
.kg-u .adim::before{content:"→ ";color:var(--kirmizi)}
.kg-is{display:flex;justify-content:space-between;gap:12px;padding:11px 0;
  border-top:1px solid #221f1d;align-items:center}
.kg-is:first-child{border-top:none}
.kg-gec{color:var(--kirmizi);font:11px/1 "Space Mono",monospace;letter-spacing:.06em}
.anlat{border:1px solid #2a2724;border-left:3px solid var(--kirmizi);
  border-radius:8px;background:#1a1715;margin:0 0 20px}
.anlat>summary{cursor:pointer;padding:13px 16px;list-style:none;display:flex;
  align-items:center;gap:9px;font-size:14px;color:var(--bone)}
.anlat>summary::-webkit-details-marker{display:none}
.anlat>summary::before{content:"›";color:var(--kirmizi);font-size:19px;line-height:1;
  transition:transform .15s;display:inline-block}
.anlat[open]>summary::before{transform:rotate(90deg)}
.anlat .ic{padding:0 16px 16px 32px}
.anlat .amac{color:var(--bone);font-size:14.5px;margin:0 0 14px;line-height:1.65}
.anlat ol{margin:0;padding-left:19px;color:var(--gri);font-size:14px;line-height:1.7}
.anlat ol li{margin-bottom:5px}
.anlat .sonra{margin:14px 0 0;padding:11px 13px;background:#12100f;border-radius:6px;
  color:var(--gri);font-size:13.5px}
.anlat .sonra b{color:var(--bone)}
.anlat .ipucu{margin:10px 0 0;color:#8a8079;font-size:13px;font-style:italic}
.surec-adim{display:flex;gap:14px;padding:14px 0;border-top:1px solid #221f1d}
.surec-adim:first-child{border-top:none}
.surec-no{flex:0 0 28px;height:28px;border-radius:50%;background:#2a2724;color:var(--bone);
  display:grid;place-items:center;font-size:13px;font-weight:700}
.surec-nerede{font:11px/1 "Space Mono",monospace;color:var(--kirmizi);letter-spacing:.06em}
.kl-adim{display:flex;gap:12px;padding:12px 0;border-top:1px solid #221f1d}
.kl-adim:first-child{border-top:none}
.kl-no{flex:0 0 26px;height:26px;border-radius:50%;background:var(--kirmizi);color:#fff;
  display:grid;place-items:center;font-size:13px;font-weight:700}
.kl-not{color:var(--gri);font-size:13px;margin-top:4px;display:block}
.kl-ornek{border:1px solid #2a2724;border-radius:8px;padding:14px;margin-bottom:12px}
.kl-ornek pre{white-space:pre-wrap;background:#12100f;border-radius:6px;padding:12px;
  font:inherit;color:var(--bone);margin:8px 0 0}
.kl-rozet{font:11px/1 "Space Mono",monospace;letter-spacing:.08em;padding:4px 8px;border-radius:4px}
.kutu .etk{color:var(--gri);display:block;margin-bottom:8px}
.kutu .buyuk{font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:29px;line-height:1}
.cift{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:22px}
.cbar{display:flex;align-items:center;gap:10px;margin-bottom:7px;font-size:13.5px}
.cbar span:first-child{width:130px;flex-shrink:0;color:rgba(239,237,232,.85)}
.cbar .c{flex:1;height:16px;background:rgba(239,237,232,.07);border-radius:2px;overflow:hidden}
.cbar .c i{display:block;height:100%;background:var(--kirmizi)}
.cbar span:last-child{width:44px;text-align:right;color:var(--gri);font-family:"Space Mono",monospace;font-size:12px}
.bos{color:var(--gri);padding:30px 0;font-style:italic}
.alan{margin-bottom:16px}
.alan label{display:block;font-size:12.5px;color:var(--gri);margin-bottom:5px}
.alan input,.alan select{width:100%}
.dortlu{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}
.uyari{border-left:3px solid var(--sari);background:rgba(224,163,46,.08);padding:13px 15px;
font-size:13.5px;color:rgba(239,237,232,.82);margin:14px 0;border-radius:0 3px 3px 0}
.tost{position:fixed;left:50%;bottom:26px;transform:translateX(-50%);background:var(--ink2);
border:1px solid var(--kirmizi);color:var(--bone);padding:12px 20px;border-radius:3px;z-index:120;
font-size:14px;display:none;max-width:80vw}
.tost.gor{display:block}
@media(max-width:900px){.pano{grid-template-columns:repeat(7,200px)}}
</style></head><body>

<header><div class="hbar">
  <div class="logo">LUNA <span>PUSULA</span></div>
  <div class="durumlambasi"><span class="nokta" id="lamba"></span><span id="lamba-yazi">hazır</span></div>
  <nav>
    <button data-s="karargah" class="aktif">Karargâh</button>
    <button data-s="tarama">Tarama</button>
    <button data-s="fabrika">Hedef Kitle</button>
    <button data-s="adaylar">Adaylar</button>
    <button data-s="raf">Raf</button>
    <button data-s="piyasa">Piyasa</button>
    <button data-s="huni">Huni</button>
    <button data-s="uretim">Üretim</button>
    <button data-s="arama">Arama</button>
    <button data-s="gundem">Gündem</button>
    <button data-s="sorgu">Arama Gündemi</button>
    <button data-s="makale">Makale</button>
    <button data-s="talep">Talep</button>
    <button data-s="kilavuz">Kılavuz</button>
    <button data-s="istatistik">İstatistik</button>
    <button data-s="ayarlar">Ayarlar</button>
  </nav>
</div></header>

<main>
  <!-- ================= KARARGÂH ================= -->
  <section class="sayfa aktif" id="s-karargah">
    <div class="baslik"><h2>Karargâh</h2>
      <span id="kg-zaman" style="color:var(--gri);font-size:13px;align-self:center"></span></div>
    <p class="altbaslik">Sabah ilk bakılacak yer. Ne durumdayız, neyi unutuyoruz,
      bugün ne yapılacak — üçü de burada.</p>

    <div class="kart" style="margin-bottom:16px" id="kg-okuma">
      <div style="display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap">
        <span class="etk">Site tıklanmaları · gerçek okuma</span>
        <span style="color:var(--gri);font-size:12.5px">15 sn + %25 kaydırma = 1 okuma · çerezsiz</span>
      </div>
      <div id="ok-ozet" class="kutular" style="margin-top:10px"></div>
      <div id="ok-grafik" style="margin-top:12px"></div>
      <div id="ok-sayfa" style="margin-top:12px;font-size:13px"></div>
    </div>

    <div id="kg-durum" class="kutular"></div>

    <div class="kart" style="margin-top:20px">
      <span class="etk">Dikkat isteyenler</span>
      <div id="kg-uyari" style="margin-top:8px"></div>
    </div>

    <div class="kart" style="margin-top:18px">
      <span class="etk">Bugün yapılacaklar</span>
      <div id="kg-bugun" style="margin-top:8px"></div>
    </div>

    <div class="kart" style="margin-top:18px">
      <span class="etk">Hızlı işlem</span>
      <div class="arac" style="margin-top:10px;flex-wrap:wrap">
        <button class="dug" onclick="karargahYenile()">Durumu yenile</button>
        <button class="dug sade" onclick="saglikOlc();gitSekme('arama')">Siteyi tara</button>
        <button class="dug sade" onclick="gitSekme('raf')">Rafı aç</button>
        <button class="dug sade" onclick="gitSekme('gundem')">Gündeme bak</button>
        <button class="dug sade" onclick="gitSekme('talep')">Gelen talebi yanıtla</button>
      </div>
    </div>
  </section>

  <!-- ================= TARAMA ================= -->
  <section class="sayfa" id="s-tarama">
    <div class="baslik"><h2>Tarama</h2></div>
    <p class="altbaslik">Şehri ve sektörü seç, başlat. Aday bulma, eksik tespiti, kazanç hesabı, demo üretimi
       ve rapor sırayla çalışır — terminal açmana gerek yok.</p>

    <div class="dortlu" style="max-width:1100px">
      <div class="alan"><label>Şehir</label><select id="t-sehir"></select></div>
      <div class="alan"><label>Sektör</label><select id="t-sektor"></select></div>
      <div class="alan"><label>Sektör başına azami aday (0 = sınırsız)</label>
        <input type="number" id="t-adet" value="40" min="0" max="200"></div>
      <div class="alan"><label>Ortalama iş bedeli (₺, boş = varsayılan)</label>
        <input type="number" id="t-ois" placeholder="örn. 45000"></div>
    </div>

    <div class="arac" style="margin-top:6px">
      <label class="k"><input type="checkbox" id="t-hizli" checked> Hızlı mod (site hız testi atlanır)</label>
      <label class="k"><input type="checkbox" id="t-sicak"> Demo yalnızca sıcak adaylara</label>
    </div>
    <div class="arac">
      <span class="etk" style="color:var(--gri);align-self:center;margin-right:4px">Adımlar</span>
      <label class="k"><input type="checkbox" class="adim" value="tara" checked> Bul</label>
      <label class="k"><input type="checkbox" class="adim" value="denetle" checked> Denetle</label>
      <label class="k"><input type="checkbox" class="adim" value="zenginlestir" checked> Araştır</label>
      <label class="k"><input type="checkbox" class="adim" value="hesapla" checked> Hesapla</label>
      <label class="k"><input type="checkbox" class="adim" value="demo" checked> Demo</label>
      <label class="k"><input type="checkbox" class="adim" value="rapor" checked> Rapor</label>
      <button class="dug" id="t-basla" onclick="akisBaslat()">Taramayı başlat</button>
      <span id="t-kaynak" class="etk" style="color:var(--gri);align-self:center"></span>
    </div>

    <div class="baslik" style="margin-top:18px"><h3>Bağlantıyla ekle</h3></div>
    <p class="altbaslik">Taramada çıkmayan ya da Haritalar'da olup aramaya yakalanmayan firma: web sitesini ya da Google Haritalar
       bağlantısını yapıştır. Aday olarak kaydedilir, Haritalar'da eşleşirse puan/yorum/fotoğraf çekilir, eksik tespiti,
       kazanç tahmini ve demo aynı adımda üretilir. Sektör boşsa siteden tahmin edilir.</p>
    <div class="dortlu" style="max-width:1100px">
      <div class="alan"><label>Web sitesi</label><input id="e-site" placeholder="https://firma.com"></div>
      <div class="alan"><label>Google Haritalar bağlantısı (isteğe bağlı)</label><input id="e-harita" placeholder="https://maps.app.goo.gl/… ya da /maps/place/…"></div>
      <div class="alan"><label>Firma adı (boş = siteden)</label><input id="e-ad"></div>
      <div class="alan"><label>Sektör (boş = tahmin)</label><select id="e-sektor"><option value="">— tahmin et —</option></select></div>
    </div>
    <div class="arac"><button class="dug" onclick="elleEkle()">Ekle ve analiz et</button></div>

    <div id="t-ilerleme" style="display:none">
      <div class="ilerleme"><i id="t-cubuk" style="width:0"></i></div>
      <div style="display:flex;justify-content:space-between;font-size:13px;color:var(--gri);margin-bottom:10px">
        <span id="t-adim">—</span><span id="t-gecen"></span>
      </div>
    </div>
    <div class="konsol" id="t-konsol">Hazır. Şehir seçip “Taramayı başlat”a bas.</div>

    <h3 style="font-size:18px;margin:26px 0 10px">Son görevler</h3>
    <div class='tablo-kaydir'><table><thead><tr><th>#</th><th>Görev</th><th>Durum</th><th>Adım</th><th>Süre</th><th></th></tr></thead>
      <tbody id="gorev-govde"></tbody></table></div>
  </section>

  <!-- ================= HEDEF KİTLE ================= -->
  <section class="sayfa" id="s-fabrika">
    <div class="baslik"><h2>Hedef kitle fabrikası</h2></div>
    <p class="altbaslik">Her hizmet için kimi arıyoruz, nereden tanırız, ne deriz, hangi itiraz gelir.
       Karta tıkla, tam dosya açılsın.</p>
    <div class="izgara" id="hizmet-izgara"></div>
  </section>

  <!-- ================= ADAYLAR ================= -->
  <section class="sayfa" id="s-adaylar">
    <div class="baslik"><h2>Aday havuzu</h2></div>
    <p class="altbaslik">Skoru düşük olan = eksiği çok olan = sıcak aday. Satıra tıkla, dosyasını aç;
       seçip toplu müşteri dosyası çıkar.</p>
    <div class="arac">
      <select id="f-sehir"><option value="">Tüm iller</option></select>
      <select id="f-sektor"><option value="">Tüm sektörler</option></select>
      <select id="f-durum"><option value="">Hepsi</option><option value="sicak">Sadece sıcak</option>
        <option value="temassiz">Temas edilmemiş</option><option value="demolu">Demosu olan</option>
        <option value="dosyali">Dosyası çıkmış</option>
        <option value="wa">WhatsApp'a uygun</option><option value="mail">Sadece e-posta/sabit</option>
        <option value="arastirilmadi">Araştırılmamış</option></select>
      <input type="text" id="f-ara" placeholder="İsimde ara...">
      <span id="aday-sayi" class="etk" style="color:var(--gri);margin-left:auto"></span>
    </div>
    <div class="arac" id="toplu" style="display:none">
      <span class="etk" style="color:var(--kirmizi);align-self:center"><b id="secili-sayi">0</b> seçili</span>
      <button class="dug" onclick="dosyaCikar()">Müşteri dosyası çıkar</button>
      <button class="dug sade" onclick="arastir()">İletişim araştır</button>
      <button class="dug sade" onclick="topluTemas()">Temas kaydı düş</button>
      <button class="dug sade" onclick="topluDurum()">Durum değiştir</button>
      <button class="dug sade" onclick="secimTemizle()">Seçimi temizle</button>
    </div>
    <div class='tablo-kaydir'><table><thead><tr>
      <th style="width:34px"><input type="checkbox" id="hepsi" onclick="hepsiSec(this)"></th>
      <th data-sirala="ad">İşletme</th><th data-sirala="sektor_ad">Sektör</th><th data-sirala="sehir">İl</th>
      <th data-sirala="skor">Skor</th><th data-sirala="eksik">Eksik</th>
      <th data-sirala="ek_gelir">Tahmini ek ciro</th><th>Kanal</th><th>Kişi</th><th data-sirala="sosyal_skor">Sosyal</th><th data-sirala="durum">Durum</th><th>İşlem</th>
    </tr></thead><tbody id="aday-govde"></tbody></table></div>
  </section>

  <!-- ================= RAF ================= -->
  <section class="sayfa" id="s-raf">
    <div class="baslik"><h2>Raf</h2></div>
    <p class="altbaslik">Her firma bir durumda duruyor. Aranan, mesaj atılan, mail gönderilen ve
       cevap veren herkes burada kayıtlı — hiçbir şey akılda tutulmuyor.</p>
    <h3 style="font-size:18px;margin:6px 0 10px">Bugün takip edilecekler</h3>
    <div class='tablo-kaydir'><table><thead><tr><th>Firma</th><th>İl</th><th>Son temas</th><th>Sonraki adım</th><th>Tarih</th><th></th></tr></thead>
      <tbody id="takip-govde"></tbody></table></div>
    <h3 style="font-size:18px;margin:28px 0 10px">Durum panosu</h3>
    <div class="pano" id="raf-pano" style="grid-template-columns:repeat(9,minmax(160px,1fr))"></div>
    <h3 style="font-size:18px;margin:28px 0 10px">Temas günlüğü</h3>
    <div class='tablo-kaydir'><table><thead><tr><th>Tarih</th><th>Firma</th><th>Yön</th><th>Kanal</th><th>Sonuç</th><th>Kişi</th><th>Kim yaptı</th><th>Not</th></tr></thead>
      <tbody id="temas-govde"></tbody></table></div>
  </section>

  <!-- ================= PİYASA ================= -->
  <section class="sayfa" id="s-piyasa">
    <div class="baslik"><h2>Piyasa</h2></div>
    <p class="altbaslik">Hangi işin piyasada ne ettiğini bilmeden teklif vermek, ya para bırakmak
       ya işi kaçırmak demek. Aşağıdaki aralıklar yayınlanmış ajans listelerinden derlendi —
       canlı veri değil, çapa. Duyduğun gerçek rakip teklifleri kaydettikçe sistem kendi
       ortalamasını hesaplar ve o öne çıkar.</p>
    <div class="arac">
      <select id="p-sehir"><option value="">Türkiye geneli</option></select>
      <span id="p-derleme" class="etk" style="color:var(--gri);align-self:center"></span>
    </div>
    <div id="piyasa-liste"></div>
    <h3 style="font-size:18px;margin:28px 0 10px">Duyduğun rakip teklifi kaydet</h3>
    <div class="arac">
      <select id="r-hizmet"></select>
      <input type="text" id="r-sehir" placeholder="İl" style="width:120px">
      <input type="number" id="r-tutar" placeholder="Tutar (₺)" style="width:150px">
      <input type="text" id="r-kaynak" placeholder="Kimden duydun / kaynak" style="width:220px">
      <button class="dug" onclick="rakipEkle()">Kaydet</button>
    </div>
    <div class='tablo-kaydir'><table><thead><tr><th>Tarih</th><th>Hizmet</th><th>İl</th><th>Tutar</th><th>Kaynak</th></tr></thead>
      <tbody id="rakip-govde"></tbody></table></div>
    <h3 style="font-size:18px;margin:28px 0 10px">Kaynaklar</h3>
    <ul id="piyasa-kaynak" style="list-style:none;font-size:13.5px"></ul>
  </section>

  <!-- ================= HUNİ ================= -->
  <section class="sayfa" id="s-huni">
    <div class="baslik"><h2>Satış hunisi</h2></div>
    <p class="altbaslik">Bulunandan kazanılan işe. Her adımdaki düşüş nerede kan kaybettiğini gösterir.</p>
    <div class="huni" id="huni"></div>
  </section>

  <!-- ================= ÜRETİM ================= -->
  <section class="sayfa" id="s-uretim">
    <div class="baslik"><h2>Üretim panosu</h2></div>
    <p class="altbaslik">Kazanılan işin teklif aşamasından teslime kadar takibi.</p>
    <div class="arac">
      <input type="text" id="i-musteri" placeholder="Müşteri adı">
      <select id="i-hizmet"></select>
      <input type="text" id="i-sehir" placeholder="İl" style="width:120px">
      <input type="number" id="i-bedel" placeholder="Bedel (₺)" style="width:140px">
      <input type="date" id="i-teslim">
      <button class="dug" onclick="isEkle()">İş ekle</button>
    </div>
    <div class="pano" id="pano"></div>
  </section>

  <!-- ================= KILAVUZ ================= -->
  <section class="sayfa" id="s-kilavuz">
    <div class="baslik"><h2>Kılavuz</h2></div>
    <p class="altbaslik">Sistem ne yapıyor, biz ne yapıyoruz, hangi sırayla.
      Takıldığın yerde aşağıdaki formu doldur — Claude'a yapıştırılacak
      düzgün bir talep metni çıkar.</p>

    <div class="kart">
      <span class="etk">Sen kimsin</span>
      <p style="color:var(--gri);font-size:14px;margin:8px 0 12px">
        İki kişi kullandığınız için her temas ve iş kaydının yanında kimin yaptığı
        yazılıyor. Bu isim sadece bu tarayıcıda saklanıyor.</p>
      <div class="arac">
        <input type="text" id="kl-ben" placeholder="Adın" style="max-width:220px">
        <button class="dug" onclick="kimimKaydet()">Kaydet</button>
        <span id="kl-ben-durum" style="color:var(--gri);font-size:13px"></span>
      </div>
    </div>

    <div class="kart" style="margin-top:18px">
      <span class="etk">Süreç — bir firma baştan sona nasıl ilerliyor</span>
      <p style="color:var(--gri);font-size:14px;margin:8px 0 14px">
        Sistemin tamamı tek bir zincir. Her sayfa bu zincirin bir halkası;
        hangi sayfada olduğunu unutursan buraya bak.</p>
      <div id="kl-surec"></div>

    <div class="kart" style="margin-top:18px">
      <span class="etk">İlk gün</span>
      <div id="kl-baslangic" style="margin-top:10px"></div>
    </div>

    <div class="kart" style="margin-top:18px">
      <span class="etk">Ritim — ne zaman ne yapılır</span>
      <div id="kl-ritim" style="margin-top:10px"></div>
    </div>

    <div class="kart" style="margin-top:18px">
      <span class="etk">Hangi sekme ne işe yarar</span>
      <div id="kl-sekmeler" style="margin-top:10px"></div>
    </div>

    <div class="kart" style="margin-top:18px">
      <span class="etk">Sık karşılaşılanlar</span>
      <div id="kl-sorunlar" style="margin-top:10px"></div>
    </div>

    <div class="kart" style="margin-top:18px">
      <span class="etk">Eksik gördüğün şeyi Claude'a nasıl anlatırsın</span>
      <div id="kl-kural" style="margin-top:10px"></div>

      <div style="border-top:1px solid #2a2724;margin-top:20px;padding-top:18px">
        <h4 style="margin:0 0 10px">Talep yaz</h4>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
          <div class="alan"><label>Hangi sekme</label>
            <select id="kl-sekme"></select></div>
          <div class="alan"><label>Tek cümlelik başlık</label>
            <input type="text" id="kl-baslik" placeholder="Aday listesinde en zayıf firmayı önce görmek"></div>
        </div>
        <div class="alan" style="margin-top:10px"><label>Ne yapmak istedin</label>
          <textarea id="kl-niyet" rows="2" class="kutu-yazi"></textarea></div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:10px">
          <div class="alan"><label>Ne bekliyordun</label>
            <textarea id="kl-beklenen" rows="2" class="kutu-yazi"></textarea></div>
          <div class="alan"><label>Ne oldu</label>
            <textarea id="kl-olan" rows="2" class="kutu-yazi"></textarea></div>
        </div>
        <div class="alan" style="margin-top:10px"><label>Hata satırı (varsa — olduğu gibi yapıştır)</label>
          <textarea id="kl-hata" rows="3" class="kutu-yazi"
            placeholder="Ekrandaki kırmızı yazı ya da terminal penceresindeki son satırlar"></textarea></div>
        <div class="arac" style="margin-top:12px;align-items:flex-end">
          <div class="alan" style="max-width:200px"><label>Aciliyet</label>
            <select id="kl-aciliyet">
              <option>Acil değil</option><option>Bu hafta</option>
              <option>Acil — iş bekliyor</option></select></div>
          <button class="dug" onclick="talepMetniUret()">Metni oluştur</button>
        </div>
        <div id="kl-metin-kutu" style="margin-top:14px"></div>
      </div>
    </div>

    <div class="kart" style="margin-top:18px">
      <span class="etk">Örnekler</span>
      <div id="kl-ornek" style="margin-top:10px"></div>
    </div>

    <div class="kart" style="margin-top:18px">
      <span class="etk">Değişmeyen kurallar</span>
      <p style="color:var(--gri);font-size:14px;margin:8px 0 12px">
        Bunlar keyfi tercih değil; her biri bir sebepten kondu. Değiştirmek
        istersen sebebini birlikte konuşalım.</p>
      <div id="kl-ilke"></div>
    </div>

    <div class="kart" style="margin-top:18px">
      <span class="etk">İkinci bilgisayar</span>
      <div id="kl-ag" style="margin-top:8px"></div>
    </div>

    <div class="kart" style="margin-top:18px">
      <span class="etk">Uzaktan erişim — farklı ağdaysanız</span>
      <p style="color:var(--gri);font-size:14px;margin:8px 0 14px">
        Yukarıdaki ağ kipi yalnızca aynı Wi-Fi içinde çalışır. Farklı ev ya da
        şehirdeyseniz yol Cloudflare tüneli: panel yine bu bilgisayarda çalışır,
        dışarıya tek bir <b>https</b> adresi açılır. Modemde port açmak,
        IP ezberlemek yok.</p>
      <div id="kl-uzak"></div>
    </div>

    </div>
  </section>

  <!-- ================= TALEP ================= -->
  <section class="sayfa" id="s-talep">
    <div class="baslik"><h2>Gelen talep · hazır yanıt</h2></div>
    <p class="altbaslik">Müşteriden gelen mesajı olduğu gibi yapıştır. Hangi hizmet olduğunu,
      fiyatın bandın neresine oturduğunu ve neden orada olduğunu çıkarıp; WhatsApp ve e-posta
      için iki ayrı yanıt taslağı yazar. Rakamlar hizmet sayfalarındaki bantlarla aynı —
      uydurma fiyat üretmez.</p>

    <div class="kart">
      <div class="alan"><label>Gelen mesaj</label>
        <textarea id="tl-metin" rows="7" placeholder="Müşterinin mesajını buraya yapıştır…"
          style="width:100%;background:#12100f;color:var(--bone);border:1px solid #2a2724;
                 border-radius:6px;padding:10px;font:inherit"></textarea></div>
      <div class="arac" style="margin-top:10px">
        <button class="dug" onclick="talepCoz()">Yanıt taslağı üret</button>
        <button class="dug sade" onclick="talepKaydet()">Taslağı dosyaya yaz</button>
      </div>
      <div id="tl-durum" style="margin-top:12px"></div>
      <div id="tl-sonuc"></div>
    </div>

    <div class="kart" style="margin-top:18px">
      <span class="etk">Hizmet bantları</span>
      <p style="color:var(--gri);font-size:14px;margin:8px 0 12px">
        Yanıtlarda kullanılan bantlar. Bir bandı değiştirirsen <b>hem sitedeki hizmet
        sayfasını hem de <code>pusula/talep.py</code>'yi</b> birlikte güncelle — ikisi
        aynı rakamı söylemek zorunda.</p>
      <div id="tl-hizmetler"></div>
    </div>
  </section>

  <!-- ================= İSTATİSTİK ================= -->
  <!-- ================= ARAMA ================= -->
  <section class="sayfa" id="s-arama">
    <div class="baslik"><h2>Arama performansı</h2></div>
    <p class="altbaslik">Google Search Console → <b>Performans</b> → sağ üstteki <b>Dışa aktar</b> →
      <b>CSV indir</b>. İnen ZIP'i olduğu gibi buraya bırak. Hangi şehirde kaç tıklanma aldığımızı,
      hangi sayfanın gösterim alıp tıklanmadığını ve hiç görünmeyen sayfaları çıkarır.</p>

    <div class="kart">
      <div class="arac" style="align-items:flex-end">
        <div class="alan" style="max-width:250px"><label>Dönem etiketi (isteğe bağlı)</label>
          <input type="text" id="ar-donem" placeholder="Son 3 ay"></div>
        <div class="alan" style="max-width:320px"><label>Search Console dosyası (.zip / .csv)</label>
          <input type="file" id="ar-dosya" accept=".zip,.csv,.tsv"></div>
        <button class="dug" onclick="aramaYukle()">Oku</button>
        <button class="dug sade" onclick="aramaGecmis()">Geçmiş yüklemeler</button>
      </div>
      <div id="ar-durum" style="margin-top:12px"></div>
    </div>

    <div id="ar-sonuc"></div>

    <div class="kart" style="margin-top:22px">
      <span class="etk">Ziyaretçi ve buton tıklaması</span>
      <p style="color:var(--gri);font-size:14px;margin:8px 0 12px">
        Günde kaç kişi girdi, hangi sayfaya baktı, kaç kişi <b>WhatsApp / telefon / form</b>
        butonuna bastı. GA4 → Raporlar → sağ üstten <b>Dosya indir (CSV)</b>;
        Cloudflare → Web Analytics → indirme simgesi. İnen dosyayı olduğu gibi bırak.
        <br><small>Not: buton tıklamaları <code>assets/olcum.js</code> tarafından olay olarak
        gönderiliyor — Ayarlar'da GA4 kimliği girilmemişse bu satırlar boş gelir.</small></p>
      <div class="arac" style="align-items:flex-end">
        <div class="alan" style="max-width:220px"><label>Dönem etiketi</label>
          <input type="text" id="zy-donem" placeholder="Son 28 gün"></div>
        <div class="alan" style="max-width:320px"><label>GA4 / Cloudflare dosyası</label>
          <input type="file" id="zy-dosya" accept=".zip,.csv,.tsv"></div>
        <button class="dug" onclick="ziyaretYukle()">Oku</button>
        <button class="dug sade" onclick="ziyaretGecmis()">Geçmiş</button>
      </div>
      <div id="zy-durum" style="margin-top:12px"></div>
      <div id="zy-sonuc"></div>
    </div>

    <div class="kart" style="margin-top:18px">
      <span class="etk">Site sağlığı — günlük SEO taraması</span>
      <p style="color:var(--gri);font-size:14px;margin:8px 0 12px">
        Sitenin tamamı kategori kategori denetleniyor: ana sayfalar, hizmet sayfaları,
        şehir sayfaları ve blog. Sonuç günlüğe yazılıyor; bir önceki ölçümle farkı da
        gösteriliyor.</p>
      <div class="arac">
        <button class="dug" onclick="saglikOlc()">Şimdi tara</button>
        <button class="dug sade" onclick="saglikGecmis()">Günlüğü aç</button>
      </div>
      <div id="sg-sonuc" style="margin-top:12px"></div>
    </div>

    <div class="kart" style="margin-top:18px">
      <span class="etk">Alt alan adı kontrolü</span>
      <p style="color:var(--gri);font-size:14px;margin:8px 0 12px">
        <b>kda.lunayapim.com</b> ana sitenin SEO'suna zarar veriyor mu? Bu testi senin makinen
        çalıştırır — alt alan adı indekslenebilir sayfa mı yoksa sadece API mi döndürüyor,
        robots.txt taramayı kapatmış mı diye bakar.</p>
      <div class="arac">
        <div class="alan" style="max-width:280px"><label>Alt alan adı</label>
          <input type="text" id="ar-alan" value="kda.lunayapim.com"></div>
        <button class="dug sade" onclick="altalanTest()">Kontrol et</button>
      </div>
      <div id="ar-altalan" style="margin-top:12px"></div>
    </div>
  </section>


  <!-- ================= ARAMA GÜNDEMİ ================= -->
  <section class="sayfa" id="s-sorgu">
    <div class="baslik"><h2>Arama Gündemi</h2>
      <span id="sg-zaman" style="color:var(--gri);font-size:13px;align-self:center"></span></div>
    <p class="altbaslik">İnsanlar bugün ne arıyor? Günde bir kez derle, siteye bas.</p>

    <details class="anlat"><summary>Bu sayfa ne yapıyor?</summary>
      <p><b>Amaç:</b> içerik planını tahminle değil, gerçek aramayla yapmak.
        Hangi soruyu kaç kişi sorduğunu bilmeden doğru sayfayı yazamayız.</p>
      <p><b>Kaynak:</b> ikisi de ücretsiz ve anahtarsız.
        1) <b>Google otomatik tamamlama</b> — arama kutusuna bir kelime yazınca çıkan
        öneriler. Bu liste sıklık sırasına göre gelir, yani tahmin değil ölçüm.
        2) <b>Google Trends TR</b> — o gün yükselen aramalar.</p>
      <p><b>Süreç:</b> 1) <b>Derle</b> — tohum kelimeler soru ekleri ve harflerle
        genişletilir, çıkan sorgular kendi hizmet sözlüğümüzle puanlanır, bize
        değmeyen atılır. 2) <b>Siteye bas</b> — <code>/yapay-zeka/</code> sayfası
        yenilenir. 3) Öneri listesindeki bir sorgu yazıya değerse Makale sekmesine
        geçip 100 puan kapısından geçir.</p>
      <p><b>Dürüstlük:</b> otomatik tamamlama arama <i>sayısı</i> vermez, <i>sıra</i>
        verir. Sitede de sıra yazıyor; hacim uydurmuyoruz.</p>
    </details>

    <div class="kart">
      <div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center">
        <button class="dug" onclick="sgDerle()">Bugünü derle</button>
        <button class="dug sade" onclick="sgYayinla()">Siteye bas</button>
        <button class="dug sade" onclick="sgTest()">Kaynakları sına</button>
        <span id="sg-durum" style="color:var(--gri);font-size:13px"></span>
      </div>
      <div id="sg-test" style="margin-top:12px"></div>
    </div>

    <div class="kart" style="margin-top:18px">
      <span class="etk">Yazıya değer sorgular</span>
      <div id="sg-oneri" style="margin-top:10px">Yükleniyor…</div>
    </div>

    <div class="kart" style="margin-top:18px">
      <span class="etk">Bugünün derlemesi</span>
      <div id="sg-liste" style="margin-top:10px">Yükleniyor…</div>
    </div>
  </section>

  <!-- ================= MAKALE ================= -->
  <section class="sayfa" id="s-makale">
    <div class="baslik"><h2>Makale</h2></div>
    <p class="altbaslik">Yazıyı sistem üretiyor, kapıyı sistem tutuyor.
      100 puan almayan yazı yayınlanamıyor — düğme kapalı kalıyor.</p>

    <details class="anlat"><summary>Bu sayfa ne yapıyor?</summary>
      <p><b>Amaç:</b> sitenin arama tarafındaki yüzeyini büyütmek. Hizmet
        sayfaları "biz ne yapıyoruz" diyor; makaleler müşterinin sorduğu
        soruya cevap veriyor. Aranan şey çoğu zaman ikincisi.</p>
      <p><b>Süreç:</b> 1) Konuyu seç. 2) <b>Üret ve puanla</b> — yazı çıkıyor,
        yanında 100 üzerinden karnesi. 3) Eksik varsa ne yapılacağı yazıyor.
        4) 100 olunca <b>Yayınla</b> açılıyor; yazı siteye basılıyor, blog
        indeksi ve site haritası güncelleniyor. 5) GitHub Desktop → Commit →
        Push origin ile yayına gidiyor.</p>
      <p><b>Kural:</b> uydurma rakam yok, kaynaksız iddia yok, aynı yazının
        şehir kopyası yok. Üçü de kapının maddeleri arasında.</p>
    </details>

    <div class="kart">
      <span class="etk">Konular</span>
      <div id="mk-liste" style="margin-top:10px">Yükleniyor…</div>
    </div>

    <div class="kart" style="margin-top:18px" id="mk-sonuc-kart" hidden>
      <div class="baslik" style="margin-bottom:6px">
        <h3 id="mk-baslik" style="font-size:18px;margin:0"></h3>
        <span id="mk-puan" class="buyuk" style="font-size:26px"></span></div>
      <div id="mk-karne"></div>
      <div class="arac" style="margin-top:14px;flex-wrap:wrap">
        <button class="dug" id="mk-yayinla" onclick="makaleYayinla()" disabled>Yayınla</button>
        <button class="dug sade" onclick="document.getElementById('mk-metin').hidden=!document.getElementById('mk-metin').hidden">Yazıyı göster / gizle</button>
      </div>
      <pre id="mk-metin" hidden style="white-space:pre-wrap;margin-top:12px;
        background:#12100f;border:1px solid #221f1d;border-radius:8px;padding:14px;
        font:13px/1.65 Manrope,sans-serif;color:var(--bone);max-height:420px;overflow:auto"></pre>
    </div>
  </section>

  <!-- ================= GÜNDEM ================= -->
  <section class="sayfa" id="s-gundem">
    <div class="baslik"><h2>Gündem → içerik</h2></div>
    <p class="altbaslik">Günün haberlerinden <b>bizim gerçekten söyleyecek sözümüz olanları</b> bulur.
      Trend kovalamıyoruz: haber bizim işimizle kesişmiyorsa yazı önerilmiyor. Her öneri için
      neden o yazının yazılacağı ve hangi hizmet sayfasına bağlanacağı yazılı geliyor.</p>

    <div class="kart">
      <div class="arac" style="align-items:flex-end">
        <div class="alan" style="max-width:190px"><label>En düşük ilgi puanı</label>
          <input type="number" id="gu-asgari" value="40" min="0" max="100"></div>
        <div class="alan" style="max-width:190px"><label>Konu başına haber</label>
          <input type="number" id="gu-adet" value="12" min="3" max="30"></div>
        <button class="dug" onclick="gundemTara()">Gündemi tara</button>
        <button class="dug sade" onclick="gundemKaynak()">Kaynak testi</button>
      </div>
      <div id="gu-durum" style="margin-top:12px"></div>
    </div>

    <div id="gu-liste"></div>
    <div id="gu-taslak"></div>

    <div class="kart" style="margin-top:22px">
      <span class="etk">Yayına al</span>
      <p style="color:var(--gri);font-size:14px;margin:8px 0 12px">
        Taslağın metnini yazdıktan sonra buradan tek tuşla siteye basıyoruz:
        <b>blog/&lt;yazı&gt;.html</b> + blog indeksi + sitemap.xml birlikte güncelleniyor.
        Sayfa diğer 326 sayfayla aynı şablondan çıkıyor — h1/h2 hiyerarşisi, canonical,
        OG etiketleri, Article + FAQPage + BreadcrumbList şemaları hazır geliyor.</p>
      <div class="arac">
        <button class="dug sade" onclick="taslakListe()">Taslakları getir</button>
        <label style="display:flex;align-items:center;gap:7px;font-size:14px;color:var(--gri)">
          <input type="checkbox" id="ya-bildir" checked> yayınlayınca arama motorlarına bildir</label>
      </div>
      <div id="ya-liste" style="margin-top:12px"></div>
      <div id="ya-sonuc"></div>
    </div>

    <div class="kart" style="margin-top:18px">
      <span class="etk">Depo durumu — GitHub Desktop takıldıysa</span>
      <p style="color:var(--gri);font-size:14px;margin:8px 0 12px">
        "A lock file already exists in the repository" hatası, yarıda kesilmiş bir git
        işleminden kalan <code>.git/index.lock</code> dosyasından geliyor. Çalışan bir git
        süreci varsa dokunmuyoruz; yoksa kilidi kaldırıyoruz.</p>
      <div class="arac">
        <button class="dug sade" onclick="depoDurum()">Depoyu kontrol et</button>
        <button class="dug" onclick="depoKilit(false)">Kilidi çöz</button>
      </div>
      <div id="ya-depo" style="margin-top:12px"></div>
    </div>

    <div class="kart" style="margin-top:18px">
      <span class="etk">Arama motoruna bildirim (IndexNow)</span>
      <p style="color:var(--gri);font-size:14px;margin:8px 0 12px">
        Google'ın eski sitemap ping ucu 2023'te kapatıldı. IndexNow açık protokol:
        Bing, Yandex, Seznam ve Naver destekliyor. Google tarafında yol sitemap —
        her yayında lastmod'u güncelliyoruz, Search Console'daki sitemap zaten taranıyor.</p>
      <div class="arac">
        <button class="dug sade" onclick="inDurum()">Durum</button>
        <button class="dug sade" onclick="inAnahtar()">Anahtar üret</button>
        <button class="dug sade" onclick="inBildir()">Ana sayfa + blogu bildir</button>
      </div>
      <div id="ya-index" style="margin-top:12px"></div>
    </div>
  </section>

  <section class="sayfa" id="s-istatistik">
    <div class="baslik"><h2>İstatistik</h2></div>
    <p class="altbaslik">Ham sayılar. Yorum yok — rakamı sen okuyacaksın.</p>
    <div class="kutular" id="ist-kutular"></div>
    <div class="cift">
      <div><h3 style="font-size:19px;margin-bottom:14px">İl dağılımı</h3><div id="ist-sehir"></div></div>
      <div><h3 style="font-size:19px;margin-bottom:14px">Sektör dağılımı</h3><div id="ist-sektor"></div></div>
      <div><h3 style="font-size:19px;margin-bottom:14px">Görünürlük skoru kuşakları</h3><div id="ist-skor"></div></div>
      <div><h3 style="font-size:19px;margin-bottom:14px">Üretim aşamaları</h3><div id="ist-asama"></div></div>
    </div>
    <h3 style="font-size:19px;margin:30px 0 12px">Dışa aktar</h3>
    <div class="arac">
      <button class="dug sade" onclick="arsivCikar()">Arşiv sayfası üret (tek dosya HTML)</button>
      <span id="arsiv-sonuc" style="align-self:center;font-size:13.5px;color:var(--gri)"></span>
    </div>
  </section>

  <!-- ================= AYARLAR ================= -->
  <section class="sayfa" id="s-ayarlar">
    <div class="baslik"><h2>Ayarlar</h2></div>
    <p class="altbaslik">Buradaki her şey <code>ayarlar.json</code> dosyasına yazılır ve bilgisayarından çıkmaz.</p>

    <h3 style="font-size:18px;margin:20px 0 10px">Veri kaynağı</h3>
    <div class="dortlu" style="max-width:900px">
      <div class="alan"><label>Google Maps / Places API anahtarı</label>
        <input type="password" id="a-google" placeholder="AIza..."></div>
      <div class="alan"><label>PageSpeed Insights anahtarı (isteğe bağlı)</label>
        <input type="password" id="a-pagespeed" placeholder="AIza..."></div>
    </div>
    <div class="arac" style="margin-top:-4px;margin-bottom:14px">
      <button class="dug sade" onclick="anahtarTest()">Anahtarı test et</button>
      <span id="anahtar-sonuc" style="align-self:center;font-size:13.5px;color:var(--gri)"></span>
    </div>
    <div class="uyari">Google anahtarı olmadan OpenStreetMap kullanılır: isim, adres ve site gelir ama
      <strong>puan, yorum ve fotoğraf sayısı gelmez</strong> — skorlar bu yüzden daha kaba çıkar.
      Anahtarı girip kaydettiğinde bir sonraki tarama Google Places'ten çalışır.</div>

    <h3 style="font-size:18px;margin:24px 0 10px">Firma ve iletişim</h3>
    <div class="dortlu" style="max-width:900px">
      <div class="alan"><label>Mesajlarda kullanılacak imza</label><input type="text" id="a-imza"></div>
      <div class="alan"><label>E-posta adresin</label><input type="email" id="a-eposta"></div>
    </div>

    <h3 style="font-size:18px;margin:24px 0 10px">E-posta gönderimi (isteğe bağlı)</h3>
    <div class="dortlu" style="max-width:1100px">
      <div class="alan"><label>SMTP sunucu</label><input type="text" id="a-smtp-sunucu" placeholder="smtp.gmail.com"></div>
      <div class="alan"><label>Kapı</label><input type="number" id="a-smtp-kapi" value="587"></div>
      <div class="alan"><label>Kullanıcı</label><input type="text" id="a-smtp-kullanici"></div>
      <div class="alan"><label>Şifre / uygulama şifresi</label><input type="password" id="a-smtp-sifre"></div>
    </div>

    <h3 style="font-size:18px;margin:24px 0 10px">Site tıklanmaları (okuma sayacı)</h3>
    <p class="ip" style="max-width:1100px;margin:0 0 10px">
      Cloudflare Pages → lunayapim → Settings → Functions: <b>KV namespace binding</b> adı
      <code>OKUMA</code> (yeni bir KV alanı oluştur), <b>Environment variable</b>
      <code>PANEL_ANAHTARI</code> = uzun rastgele bir metin. Aynı metni buraya yapıştır.
      Push sonrası sayaç çalışmaya başlar; Karargâh'ta görünür.
    </p>
    <div class="dortlu" style="max-width:1100px">
      <div class="alan"><label>PANEL_ANAHTARI</label><input type="password" id="a-okuma-anahtar" placeholder="Cloudflare'deki değerin aynısı"></div>
      <div class="alan"><label>&nbsp;</label><button class="dugme" onclick="okumaYukle(true)">Sayacı sına</button></div>
    </div>
    <div id="ok-sina" class="ip" style="margin:6px 0 0"></div>
    <h3 style="margin-top:22px">Yazar (TrendSaphiens haber-analiz yazıları)</h3>
    <p class="ip">Gündem maddeleri kaynak olgularından, <code>cikti/yazim-rehberi.md</code> kurallarıyla yazılır; her yazı intihal
      denetiminden geçer. Anahtar boşsa yazı yazılmaz, sayfa "kaynak alıntısı + okuma" biçiminde kalır. Anahtar: console.anthropic.com → API keys.</p>
    <div class="dortlu" style="max-width:1100px">
      <div class="alan"><label>Anthropic API anahtarı</label><input type="password" id="a-yazar-anahtar" placeholder="sk-ant-…"></div>
      <div class="alan"><label>Model</label><input id="a-yazar-model" placeholder="claude-sonnet-4-5"></div>
    </div>

    <h3 style="font-size:18px;margin:24px 0 10px">Üretim (Runway API)</h3>
    <p class="ip" style="max-width:1100px;margin:0 0 10px">
      Runway → Settings → API → anahtar. Girilince video/görsel üretimi panelden ve asistandan
      yapılır; tarayıcıya gerek kalmaz. Her üretim önce kredi tahmini gösterir, onaysız gitmez.
      API kredisi ile uygulama kredisi ayrı ürünlerdir; ilk gerçek üretimden sonra tahmin tablosu düzeltilir.
    </p>
    <div class="dortlu" style="max-width:1100px">
      <div class="alan"><label>Runway API anahtarı</label><input type="password" id="a-runway" placeholder="key_…"></div>
    </div>

    <h3 style="font-size:18px;margin:24px 0 10px">Telegram (teklif paketi telefona düşsün)</h3>
    <p class="ip" style="max-width:1100px;margin:0 0 10px">
      Telegram&#39;da <b>@BotFather</b>&#39;a <code>/newbot</code> yaz, çıkan jetonu buraya yapıştır.
      Sonra kendi botuna bir kez <code>/start</code> yaz. Sohbet kimliğini öğrenmek için
      <b>@userinfobot</b>&#39;a yaz — verdiği Id buraya gelecek. Bot yalnızca sana yazar,
      kimseye kendiliğinden mesaj atmaz.
    </p>
    <div class="dortlu" style="max-width:1100px">
      <div class="alan"><label>Bot jetonu</label><input type="password" id="a-tg-jeton" placeholder="123456:AA..."></div>
      <div class="alan"><label>Sohbet kimliği</label><input type="text" id="a-tg-sohbet" placeholder="123456789"></div>
      <div class="alan"><label>Sessiz gönder</label><select id="a-tg-sessiz"><option value="0">Hayır</option><option value="1">Evet</option></select></div>
      <div class="alan"><label>&nbsp;</label><button class="dugme" onclick="tgSina()">Bağlantıyı sına</button></div>
    </div>
    <div id="tg-sonuc" class="ip" style="margin:6px 0 0"></div>

    <h3 style="font-size:18px;margin:24px 0 10px">Eşikler</h3>
    <div class="dortlu" style="max-width:1100px">
      <div class="alan"><label>Sıcak aday skor eşiği</label><input type="number" id="a-sicak"></div>
      <div class="alan"><label>Az fotoğraf sayılır (altı)</label><input type="number" id="a-foto"></div>
      <div class="alan"><label>Az yorum sayılır (altı)</label><input type="number" id="a-yorum"></div>
      <div class="alan"><label>Düşük puan sayılır (altı)</label><input type="number" step="0.1" id="a-puan"></div>
    </div>

    <h3 style="font-size:18px;margin:24px 0 10px">Kazanç modeli varsayımları</h3>
    <div class="dortlu" style="max-width:1100px">
      <div class="alan"><label>Mevcut dönüşüm oranı (%)</label><input type="number" step="0.1" id="a-d1"></div>
      <div class="alan"><label>İyileştirilmiş dönüşüm (%)</label><input type="number" step="0.1" id="a-d2"></div>
      <div class="alan"><label>İletişimden işe dönüşüm (%)</label><input type="number" step="0.1" id="a-d3"></div>
      <div class="alan"><label>Çarpan tavanı</label><input type="number" step="0.1" id="a-tavan"></div>
    </div>
    <div class="uyari">Bu oranlar tahmin modelini besler. Gerçek veriniz oldukça buraya girin —
      demo sunumlarındaki rakamlar da o an güncellenir. Model bir tahmindir, garanti değildir.</div>

    <h3 style="font-size:18px;margin:24px 0 10px">Sektör başına ortalama iş bedeli (₺)</h3>
    <div class="dortlu" style="max-width:1100px" id="a-ois"></div>

    <div class="arac" style="margin-top:22px">
      <button class="dug" onclick="ayarKaydet()">Ayarları kaydet</button>
      <span id="ayar-sonuc" style="align-self:center;font-size:13.5px;color:var(--gri)"></span>
    </div>

    <h3 style="font-size:18px;margin:30px 0 10px">Site ölçümü</h3>
    <p style="color:var(--gri);font-size:14px;max-width:70ch;margin-bottom:14px">
      Sitede şu an sadece Google Ads dönüşüm etiketi var; kaç kişi geldiği, nereden geldiği
      ve hangi sayfada durduğu ölçülmüyor. Aşağıya kimliği yapıştır, <b>Ölçümü kaydet</b> de —
      <code>assets/olcum.js</code> dosyasına biz yazıyoruz, senin dosya düzenlemene gerek yok.
      Yazdıktan sonra siteyi yayınlaman gerekiyor.</p>
    <div class="ikili" style="max-width:900px">
      <div class="alan"><label>GA4 ölçüm kimliği</label>
        <input type="text" id="a-ga4" placeholder="G-XXXXXXXXXX">
        <small style="color:var(--gri);font-size:12px;margin-top:5px;display:block">
          analytics.google.com → Yönetici (sol altta dişli) → Veri akışları → akışı seç →
          sağ üstteki <b>Ölçüm Kimliği</b>. G- ile başlar.</small></div>
      <div class="alan"><label>Cloudflare Web Analytics token (isteğe bağlı)</label>
        <input type="text" id="a-cf" placeholder="a1b2c3d4…">
        <small style="color:var(--gri);font-size:12px;margin-top:5px;display:block">
          Cloudflare → Analytics &amp; Logs → Web Analytics → siteyi ekle → verilen koddaki
          <b>token</b> değeri. Çerezsiz ve ücretsiz; GA4 ile birlikte de çalışır.</small></div>
    </div>
    <div class="arac" style="margin-top:14px">
      <button class="dug" onclick="olcumKaydet()">Ölçümü kaydet</button>
      <button class="dug sade" onclick="olcumOku()">Mevcut değeri getir</button>
      <span id="olcum-sonuc" style="align-self:center;font-size:13.5px;color:var(--gri)"></span>
    </div>

    <h3 style="font-size:18px;margin:26px 0 10px">Dosya konumları</h3>
    <table style="max-width:900px"><tbody>
      <tr><th style="cursor:default">Veritabanı</th><td><small id="a-vt">—</small></td></tr>
      <tr><th style="cursor:default">Çıktı klasörü</th><td><small id="a-cikti">—</small></td></tr>
      <tr><th style="cursor:default">Ayar dosyası</th><td><small id="a-ayardosya">—</small></td></tr>
    </tbody></table></div>
    <p style="color:var(--gri);font-size:13px;margin-top:10px">Yedeklemek için veritabanı dosyasını kopyalaman yeterli.</p>
  </section>
</main>

<div class="perde" id="perde" onclick="cekmeceKapat()"></div>
<div class="cekmece" id="cekmece"><button class="kapat" onclick="cekmeceKapat()">✕</button>
  <div class="ic" id="cekmece-ic"></div></div>
<div class="tost" id="tost"></div>

<script>
let V={hizmetler:{},adaylar:[],istatistik:{},isler:[],asamalar:[],asama_ad:{},iller:[],sektorler:[]};
let AY={}, sira={alan:"skor",yon:1}, secili=new Set(), aktifGorev=null, logIndex=0, anket=null;

const bicim=n=>(n===null||n===undefined||n==="")?"—":Number(n).toLocaleString("tr-TR");
const kacir=s=>String(s===null||s===undefined?"":s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
function tost(m,sure){const t=document.getElementById("tost");t.textContent=m;t.classList.add("gor");
  clearTimeout(t._z);t._z=setTimeout(()=>t.classList.remove("gor"),sure||3200);}

async function jget(u){const r=await fetch(u);return r.json();}
async function jpost(u,g){
  // Her yazma isteğine kim yaptığını ekliyoruz — iki kişi kullanıyor.
  const kim=(function(){try{return localStorage.getItem("pusula_kullanici")||"";}catch(e){return "";}})();
  const bas={"Content-Type":"application/json"};
  if(kim)bas["X-Pusula-Kullanici"]=kim;
  const r=await fetch(u,{method:"POST",headers:bas,body:JSON.stringify(g||{})});return r.json();}

// İlk açılışta isim sorulur; iptal edilirse bir daha sorulmaz, Kılavuz'dan girilir.
function ilkAcilisIsim(){
  let k="";try{k=localStorage.getItem("pusula_kullanici")||"";}catch(e){return;}
  if(k)return;
  try{if(localStorage.getItem("pusula_isim_soruldu"))return;}catch(e){}
  const el=document.createElement("div");
  el.style.cssText="position:fixed;left:0;right:0;bottom:0;z-index:99;background:#1a1715;"+
    "border-top:1px solid var(--kirmizi);padding:14px 20px;display:flex;gap:12px;align-items:center;flex-wrap:wrap";
  el.innerHTML=`<span style="font-size:14px">Panele hoş geldin. Adını yazarsan her temas ve iş
      kaydının yanında kimin yaptığı görünür.</span>
    <input type="text" id="ilk-ad" placeholder="Adın" style="max-width:180px">
    <button class="dug" id="ilk-kaydet">Kaydet</button>
    <button class="dug sade" id="ilk-gec">Şimdi değil</button>`;
  document.body.appendChild(el);
  el.querySelector("#ilk-kaydet").onclick=function(){
    const a=(el.querySelector("#ilk-ad").value||"").trim();
    try{if(a)localStorage.setItem("pusula_kullanici",a);
        localStorage.setItem("pusula_isim_soruldu","1");}catch(e){}
    el.remove();if(a)tost("Kayıtlar "+a+" adına düşecek.");};
  el.querySelector("#ilk-gec").onclick=function(){
    try{localStorage.setItem("pusula_isim_soruldu","1");}catch(e){}
    el.remove();};
}

async function yukle(){
  V=await jget("/api/veri");
  cizHizmetler();doldurFiltre();cizAdaylar();cizHuni();cizPano();cizIstatistik();cizGorevler();cizRaf();
  document.getElementById("t-kaynak").textContent="kaynak: "+V.kaynak;
  lamba(V.mesgul);
}
function lamba(c){
  document.getElementById("lamba").className="nokta"+(c?" calisiyor":"");
  document.getElementById("lamba-yazi").textContent=c?"çalışıyor":"hazır";
  document.getElementById("t-basla").disabled=!!c;
}

/* ---------------- TARAMA ---------------- */
function tarayiciDoldur(){
  const s=document.getElementById("t-sehir");
  s.innerHTML=V.iller.map(i=>`<option${i==="Bursa"?" selected":""}>${kacir(i)}</option>`).join("");
  document.getElementById("t-sektor").innerHTML='<option value="">Tüm sektörler</option>'+
    V.sektorler.map(x=>`<option value="${x.anahtar}">${kacir(x.ad)}</option>`).join("");
  const es=document.getElementById("e-sektor"); if(es) es.innerHTML='<option value="">— tahmin et —</option>'+
    V.sektorler.map(x=>`<option value="${x.anahtar}">${kacir(x.ad)}</option>`).join("");
}
async function akisBaslat(){
  const adimlar=[...document.querySelectorAll(".adim:checked")].map(x=>x.value);
  if(!adimlar.length){tost("En az bir adım seç.");return;}
  const g={sehir:document.getElementById("t-sehir").value,
    sektor:document.getElementById("t-sektor").value||null,
    adet:parseInt(document.getElementById("t-adet").value)||0,
    hizli:document.getElementById("t-hizli").checked,
    sadece_sicak:document.getElementById("t-sicak").checked,
    ortalama_is:parseInt(document.getElementById("t-ois").value)||null,
    adimlar:adimlar};
  const y=await jpost("/api/akis",g);
  if(y.hata){tost(y.hata,5000);return;}
  aktifGorev=y.gorev;logIndex=0;
  document.getElementById("t-konsol").textContent="";
  document.getElementById("t-ilerleme").style.display="block";
  lamba(true);izle();
}
async function elleEkle(){
  const g={site:document.getElementById("e-site").value.trim(),harita:document.getElementById("e-harita").value.trim(),
    ad:document.getElementById("e-ad").value.trim(),sektor:document.getElementById("e-sektor").value||null,
    sehir:document.getElementById("t-sehir").value};
  if(!g.site&&!g.harita){tost("Site ya da Haritalar bağlantısı gir.",4000);return;}
  const y=await jpost("/api/ekle",g);
  if(y.hata){tost(y.hata,5000);return;}
  aktifGorev=y.gorev;logIndex=0;
  document.getElementById("t-konsol").textContent="";
  document.getElementById("t-ilerleme").style.display="block";
  lamba(true);izle();
}
function izle(){
  clearInterval(anket);
  anket=setInterval(async()=>{
    if(!aktifGorev)return;
    const g=await jget("/api/gorev?id="+aktifGorev+"&from="+logIndex);
    if(g.hata)return;
    if(g.log&&g.log.length){
      const k=document.getElementById("t-konsol");
      g.log.forEach(s=>{
        const d=document.createElement("div");
        if(s.startsWith("──")||s.startsWith("▸"))d.className="y";
        if(s.startsWith("✓")||s.startsWith("→"))d.className="b";
        d.textContent=s;k.appendChild(d);
      });
      logIndex=g.log_uzunluk;k.scrollTop=k.scrollHeight;
    }
    document.getElementById("t-adim").textContent=g.adim||"—";
    document.getElementById("t-gecen").textContent=g.gecen+" sn";
    document.getElementById("t-cubuk").style.width=
      (g.toplam_adim?Math.round(100*g.adim_no/g.toplam_adim):0)+"%";
    if(g.durum==="bitti"||g.durum==="hata"){
      clearInterval(anket);aktifGorev=null;lamba(false);
      tost(g.durum==="bitti"?"Tarama bitti.":"Görev hata verdi — konsola bak.",5000);
      yukle();
    }
  },900);
}
function cizGorevler(){
  const g=V.gorevler||[];
  document.getElementById("gorev-govde").innerHTML=g.length?g.map(x=>
    `<tr><td>${x.id}</td><td>${kacir(x.ad)}</td>
     <td><span class="rz ${x.durum==="calisiyor"?"sicak":(x.durum==="bitti"?"ok":"")}">${x.durum}</span></td>
     <td><small>${kacir(x.adim||x.hata||"—")}</small></td><td>${x.gecen} sn</td>
     <td><button class="dug sade mini" onclick="gorevAc(${x.id})">logu aç</button></td></tr>`).join("")
    :`<tr><td colspan="6" class="bos">Henüz görev yok.</td></tr>`;
}
async function gorevAc(id){
  const g=await jget("/api/gorev?id="+id);
  document.getElementById("cekmece-ic").innerHTML=
    `<span class="etk" style="color:var(--kirmizi)">Görev ${g.id}</span>
     <h2 style="font-size:24px;margin:8px 0 4px">${kacir(g.ad)}</h2>
     <p style="color:var(--gri)">${g.durum} · ${g.gecen} sn${g.hata?" · "+kacir(g.hata):""}</p>
     <div class="konsol" style="margin-top:18px;max-height:none">${g.log.map(kacir).join("\n")}</div>`;
  cekmeceAc();
}

/* ---------------- HEDEF KİTLE ---------------- */
function cizHizmetler(){
  document.getElementById("hizmet-izgara").innerHTML=Object.entries(V.hizmetler).map(([a,h])=>`
    <div class="kart" onclick="hizmetAc('${a}')">
      <span class="etk" style="color:var(--kirmizi)">${kacir(a)}</span>
      <h3>${kacir(h.ad)}</h3><p class="kisa">${kacir(h.kisa)}</p>
      <div class="mini"><div><b>${h.kim.length}</b>hedef profil</div>
        <div><b>${h.sinyal.length}</b>arama sinyali</div>
        <div><b>${h.itirazlar.length}</b>itiraz cevabı</div></div>
    </div>`).join("");
}
function hizmetAc(a){
  const h=V.hizmetler[a],li=x=>`<ul>${x.map(i=>`<li>${kacir(i)}</li>`).join("")}</ul>`;
  document.getElementById("cekmece-ic").innerHTML=`
    <span class="etk" style="color:var(--kirmizi)">Hedef kitle dosyası</span>
    <h2 style="font-size:27px;margin:9px 0 6px">${kacir(h.ad)}</h2>
    <p style="color:var(--gri)">${kacir(h.kisa)} · <a href="https://lunayapim.com/${h.sayfa}" target="_blank">hizmet sayfası ↗</a></p>
    <div class="satir">
      <div><span class="etk">Bütçe</span><b>${kacir(h.butce)}</b></div>
      <div><span class="etk">Satış döngüsü</span><b>${kacir(h.dongu)}</b></div>
      <div><span class="etk">Mevsim</span><b>${kacir(h.mevsim)}</b></div>
    </div>
    <div class="blok"><span class="etk">Kimi arıyoruz</span>${li(h.kim)}</div>
    <div class="blok"><span class="etk">Hangi unvan</span>${li(h.unvan)}</div>
    <div class="blok"><span class="etk">Arama sinyalleri — bunu görürsen aday</span>${li(h.sinyal)}</div>
    <div class="blok"><span class="etk">Nerede bulunur</span>${li(h.nerede)}</div>
    <div class="blok"><span class="etk">Neyin acısını çekiyor</span>${li(h.aci)}</div>
    <div class="blok"><span class="etk">Açılış mesajı</span><div class="mesaj">${kacir(h.acilis)}</div></div>
    <div class="blok"><span class="etk">Kanal</span>${li(h.kanal)}</div>
    <div class="blok"><span class="etk">Takip ritmi</span><div class="mesaj">${kacir(h.ritim)}</div></div>
    <div class="blok"><span class="etk">İtirazlar ve cevapları</span>
      ${h.itirazlar.map(p=>`<div class="itiraz"><b>${kacir(p[0])}</b><p>${kacir(p[1])}</p></div>`).join("")}</div>
    <div class="blok"><span class="etk">Yanında götürülecek kanıt</span>${li(h.kanit)}</div>
    <div class="blok"><span class="etk">Çapraz satış</span>${li(h.capraz.map(c=>V.hizmetler[c]?V.hizmetler[c].ad:c))}</div>`;
  cekmeceAc();
}
function cekmeceAc(){document.getElementById("cekmece").classList.add("acik");
  document.getElementById("perde").classList.add("acik");}
function cekmeceKapat(){document.getElementById("cekmece").classList.remove("acik");
  document.getElementById("perde").classList.remove("acik");}
document.addEventListener("keydown",e=>{if(e.key==="Escape")cekmeceKapat();});

/* ---------------- ADAYLAR ---------------- */
function doldurFiltre(){
  const iller=[...new Set(V.adaylar.map(a=>a.sehir).filter(Boolean))].sort();
  const sek=[...new Set(V.adaylar.map(a=>a.sektor_ad).filter(Boolean))].sort();
  document.getElementById("f-sehir").innerHTML='<option value="">Tüm iller</option>'+iller.map(i=>`<option>${kacir(i)}</option>`).join("");
  document.getElementById("f-sektor").innerHTML='<option value="">Tüm sektörler</option>'+sek.map(i=>`<option>${kacir(i)}</option>`).join("");
  document.getElementById("i-hizmet").innerHTML=Object.entries(V.hizmetler).map(([a,h])=>`<option value="${a}">${kacir(h.ad)}</option>`).join("");
  if(!document.getElementById("t-sehir").options.length)tarayiciDoldur();
  const ps=document.getElementById("p-sehir");
  if(ps&&ps.options.length<2)ps.innerHTML='<option value="">Türkiye geneli</option>'+
    (V.iller||[]).map(i=>`<option>${kacir(i)}</option>`).join("");
  const rh=document.getElementById("r-hizmet");
  if(rh&&!rh.options.length)rh.innerHTML=Object.entries(V.hizmetler).map(([a,x])=>`<option value="${a}">${kacir(x.ad)}</option>`).join("");
}
function suzulmus(){
  const se=document.getElementById("f-sehir").value,sk=document.getElementById("f-sektor").value;
  const du=document.getElementById("f-durum").value,ar=document.getElementById("f-ara").value.toLocaleLowerCase("tr");
  let l=V.adaylar.filter(a=>(!se||a.sehir===se)&&(!sk||a.sektor_ad===sk)&&(!ar||a.ad.toLocaleLowerCase("tr").includes(ar)));
  if(du==="sicak")l=l.filter(a=>a.sicak);
  if(du==="temassiz")l=l.filter(a=>!a.temas);
  if(du==="demolu")l=l.filter(a=>a.demo);
  if(du==="dosyali")l=l.filter(a=>a.dosya);
  if(du==="wa")l=l.filter(a=>a.wa_uygun);
  if(du==="mail")l=l.filter(a=>!a.wa_uygun);
  if(du==="arastirilmadi")l=l.filter(a=>!a.zengin);
  l.sort((x,y)=>{const a=x[sira.alan],b=y[sira.alan];
    if(typeof a==="string")return sira.yon*String(a).localeCompare(String(b),"tr");
    return sira.yon*((a||0)-(b||0));});
  return l;
}
function cizAdaylar(){
  const l=suzulmus();
  document.getElementById("aday-sayi").textContent=l.length+" aday · "+l.filter(a=>a.sicak).length+" sıcak";
  document.getElementById("aday-govde").innerHTML=l.length?l.map(a=>`
    <tr class="${secili.has(a.id)?"secili":""}">
      <td><input type="checkbox" ${secili.has(a.id)?"checked":""} onclick="event.stopPropagation();secToggle(${a.id})"></td>
      <td onclick="adayAc(${a.id})" style="cursor:pointer"><b>${kacir(a.ad)}</b>${a.ilce?'<br><small>'+kacir(a.ilce)+'</small>':''}</td>
      <td><small>${kacir(a.sektor_ad)}</small></td><td>${kacir(a.sehir)}</td>
      <td class="skorc" style="color:${a.sicak?'var(--kirmizi)':'var(--bone)'}">${a.skor}</td>
      <td>${a.eksik}</td><td>${bicim(a.ek_gelir)} ₺</td>
      <td>${kanalRozet(a)}</td>
      <td>${a.kisi_sayisi?('<span class="rz ok">'+a.kisi_sayisi+' kişi</span>'):(a.zengin?'<small>—</small>':'<small style="color:var(--sari)">araştırılmadı</small>')}</td>
      <td>${a.sosyal_skor===null||a.sosyal_skor===undefined?'<small style="color:var(--sari)">—</small>'
        :`<span class="rz ${a.sosyal_skor>=65?'ok':(a.sosyal_skor>=35?'':'')}" style="${a.sosyal_skor>=65?'':(a.sosyal_skor>=35?'border-color:var(--sari);color:var(--sari)':'border-color:var(--kirmizi);color:var(--kirmizi)')}" title="sosyal medya gücü">${a.sosyal_skor}</span>`}</td>
      <td><span class="rz ${a.durum==='kazanildi'?'ok':(a.durum==='kayip'||a.durum==='uygun_degil'?'':'sicak')}">${kacir((V.durum_ad||{})[a.durum]||a.durum)}</span></td>
      <td style="white-space:nowrap">
        <button class="dug sade mini" onclick="event.stopPropagation();adayAc(${a.id})">aç</button>
        ${a.wa_uygun?`<button class="dug sade mini" onclick="event.stopPropagation();waAc(${a.id})">wa</button>`:""}
      </td></tr>`).join("")
    :`<tr><td colspan="11" class="bos">Aday yok. <b>Tarama</b> sekmesinden şehir seçip başlat.</td></tr>`;
  document.getElementById("secili-sayi").textContent=secili.size;
  document.getElementById("toplu").style.display=secili.size?"flex":"none";
}
["f-sehir","f-sektor","f-durum"].forEach(i=>document.getElementById(i).addEventListener("change",cizAdaylar));
document.getElementById("f-ara").addEventListener("input",cizAdaylar);
document.getElementById("p-sehir").addEventListener("change",piyasaYukle);
document.querySelectorAll("th[data-sirala]").forEach(t=>t.addEventListener("click",()=>{
  const a=t.dataset.sirala;sira.yon=(sira.alan===a)?-sira.yon:1;sira.alan=a;cizAdaylar();}));
function kanalRozet(a){
  if(a.wa_uygun) return '<span class="rz ok" title="'+kacir(a.tel_aciklama)+'">WhatsApp</span>';
  if(a.eposta)   return '<span class="rz" title="'+kacir(a.eposta)+'">e-posta</span>';
  if(a.telefon)  return '<span class="rz" style="border-color:var(--sari);color:var(--sari)" title="'+kacir(a.tel_aciklama)+'">sabit hat</span>';
  return '<span class="rz" style="opacity:.5">kanal yok</span>';
}
function secToggle(id){secili.has(id)?secili.delete(id):secili.add(id);cizAdaylar();}
function hepsiSec(el){const l=suzulmus();if(el.checked)l.forEach(a=>secili.add(a.id));else secili.clear();cizAdaylar();}
function secimTemizle(){secili.clear();document.getElementById("hepsi").checked=false;cizAdaylar();}

async function adayAc(id){
  const a=V.adaylar.find(x=>x.id===id);if(!a)return;
  const d=await jget("/api/aday?id="+id);
  if(d.hata){tost(d.hata);return;}
  const kanal=d.kanallar||[],kisi=d.kisiler||[],tem=d.temaslar||[];
  const grup=t=>kanal.filter(k=>k.tur===t);
  const kanalSatir=k=>`<li><b>${kacir(k.deger)}</b>${k.not_?' <small>· '+kacir(k.not_)+'</small>':''}
    <br><small>kaynak: ${k.kaynak?('<a href="'+kacir(k.kaynak)+'" target="_blank">'+kacir(k.kaynak)+' ↗</a>'):'—'}</small></li>`;
  const p=d.piyasa;
  document.getElementById("cekmece-ic").innerHTML=`
    <span class="etk" style="color:var(--kirmizi)">${kacir(a.sektor_ad)} · ${kacir(a.sehir)}${a.ilce?" · "+kacir(a.ilce):""}</span>
    <h2 style="font-size:25px;margin:9px 0 6px">${kacir(a.ad)}</h2>
    <p style="color:var(--gri)">${a.site?'<a href="'+kacir(a.site)+'" target="_blank">'+kacir(a.site)+' ↗</a>':"sitesi yok"}
      · <span class="rz ${a.durum==='kazanildi'?'ok':'sicak'}">${kacir((V.durum_ad||{})[a.durum]||a.durum)}</span></p>
    <div class="satir">
      <div><span class="etk">Skor</span><b style="color:${a.sicak?'var(--kirmizi)':'var(--bone)'}">${a.skor}/100</b></div>
      <div><span class="etk">Eksik</span><b>${a.eksik}</b></div>
      <div><span class="etk">Harita</span><b>${a.puan||"—"} · ${a.yorum} yorum · ${a.foto} foto</b></div>
      <div><span class="etk">Tahmini ek ciro</span><b>${bicim(a.ek_gelir)} ₺/ay</b></div>
    </div>

    <div class="blok"><span class="etk">Nasıl ulaşacağız</span>
      <div class="mesaj"><b>${kacir(a.tel_aciklama)}</b><br>
        ${a.wa_uygun?"WhatsApp birincil kanal.":(a.eposta?"Cep hattı yok — e-posta yolu kullanılacak.":"Cep hattı ve e-posta yok — sabit hattan aranmalı.")}</div>
      <ul style="margin-top:12px">
        ${grup("telefon").map(kanalSatir).join("")||"<li><small>telefon bulunamadı</small></li>"}
        ${grup("eposta").map(kanalSatir).join("")||"<li><small>e-posta bulunamadı</small></li>"}
      </ul>
      ${["instagram","facebook","linkedin","x","youtube","tiktok"].filter(t=>grup(t).length).length?
        `<div style="margin-top:10px"><span class="etk" style="color:var(--gri)">Sosyal hesaplar</span>
         <ul>${["instagram","facebook","linkedin","x","youtube","tiktok"].flatMap(t=>grup(t)).map(k=>
           `<li><a href="${kacir(k.deger)}" target="_blank">${kacir(k.tur)} ↗</a>
            <br><small>kaynak: ${kacir(k.kaynak||"—")}</small></li>`).join("")}</ul></div>`:""}
      ${a.zengin?"":'<div class="uyari" style="margin-top:12px">Bu firma henüz araştırılmadı. Aşağıdaki düğmeyle sitesini gezip iletişim ve yetkili bilgisi toplayabilirsin.</div>'}
      <div class="arac" style="margin-top:12px">
        <button class="dug sade" onclick="araştırTek(${a.id})">İletişim araştır</button>
      </div>
    </div>

    <div class="blok"><span class="etk">Yayınlanmış yetkililer</span>
      ${kisi.length?`<ul>${kisi.map(k=>`<li><b>${kacir(k.isim)}</b> — ${kacir(k.unvan||"")}
        <br><small>kaynak: <a href="${kacir(k.kaynak||"#")}" target="_blank">${kacir(k.kaynak||"—")}</a></small></li>`).join("")}</ul>`
        :`<p style="color:var(--gri);font-size:14px">Firmanın kendi sitesinde yayınlanmış isim/ünvan bulunamadı.
           LinkedIn ve sosyal platformların içine girip kişi kazımıyoruz — bu hem o platformların
           şartlarına aykırı hem KVKK açısından riskli. Aşağıdaki bağlantılardan elle bakabilirsin.</p>`}
      <div style="margin-top:12px">${Object.entries(d.arama||{}).map(([ad,u])=>
        `<a class="dug sade mini" style="text-decoration:none;display:inline-block;margin:0 6px 6px 0" href="${u}" target="_blank">${kacir(ad)} ↗</a>`).join("")}</div>
    </div>

    <div class="blok"><span class="etk">Kanıtlı eksikler</span>
      <ul>${(d.eksikler||[]).map(e=>`<li><b>${kacir(e.ad)}</b>
        ${e.kanit?`<div style="margin-top:5px;font-size:13px;color:var(--gri);line-height:1.5">
          <b style="color:rgba(239,237,232,.72)">Ne kontrol ettik:</b> ${kacir(e.kanit.kontrol)}<br>
          <b style="color:rgba(239,237,232,.72)">Ne bulduk:</b> ${kacir(e.kanit.bulgu)}<br>
          <span style="font-family:'Space Mono',monospace;font-size:10.5px;color:#6f6d68">kaynak: ${kacir(e.kanit.kaynak)} · ${kacir(e.kanit.zaman)}</span></div>`:""}
        </li>`).join("")}</ul></div>

    ${(()=>{const so=d.sosyal;if(!so)return `<div class="blok"><span class="etk">Sosyal medya</span>
      <p style="color:var(--gri);font-size:13.5px">Sosyal medya denetimi henüz yapılmadı —
      yukarıdaki <b>İletişim araştır</b> düğmesi hesapları eşleştirip eksikleri çıkarır.</p></div>`;
      const hes=Object.values(so.hesaplar||{}),eks=so.eksikler||[];
      const renk=so.skor>=65?"var(--yesil)":(so.skor>=35?"var(--sari)":"var(--kirmizi)");
      return `<div class="blok"><span class="etk">Sosyal medya · ${kacir(so.zaman||"")}</span>
      <div class="satir">
        <div><span class="etk">Sosyal güç</span><b style="color:${renk}">${so.skor}/100</b></div>
        <div><span class="etk">Bulunan hesap</span><b>${hes.length}</b></div>
        <div><span class="etk">Sosyal eksik</span><b>${eks.length}</b></div>
      </div>
      ${hes.length?`<ul style="margin-top:12px">${hes.map(h=>`<li>
        <b>${kacir(h.ad)}</b> — <a href="${kacir(h.url)}" target="_blank">@${kacir(h.kullanici)} ↗</a>
        <span class="rz" style="margin-left:6px">${kacir(h.eslesme_yorum||"")}</span>
        ${h.acik===false?'<span class="rz" style="border-color:var(--kirmizi);color:var(--kirmizi)">açılmıyor</span>':""}
        <br><small>${kacir(h.nasil||"")}${h.teyit?" · "+kacir(h.teyit):""}</small></li>`).join("")}</ul>`
       :`<div class="uyari" style="margin-top:12px">Doğrulanabilen hesap bulunamadı.</div>`}
      ${eks.length?`<div style="margin-top:12px"><span class="etk" style="color:var(--gri)">Kanıtlı sosyal eksikler</span>
        <ul>${eks.map(e=>`<li><b>${kacir(e.baslik)}</b>
          <div style="margin-top:5px;font-size:13px;color:var(--gri);line-height:1.5">
          <b style="color:rgba(239,237,232,.72)">Ne kontrol ettik:</b> ${kacir(e.kanit.kontrol)}<br>
          <b style="color:rgba(239,237,232,.72)">Ne bulduk:</b> ${kacir(e.kanit.bulgu)}<br>
          <span style="font-family:'Space Mono',monospace;font-size:10.5px;color:#6f6d68">kaynak: ${kacir(e.kanit.kaynak)} · ${kacir(e.kanit.zaman)}</span></div>
        </li>`).join("")}</ul></div>`:""}
      ${(d.sosyal_plan||[]).length?`<div style="margin-top:12px"><span class="etk" style="color:var(--gri)">Bu sektörde yapabileceklerimiz</span>
        <ul>${d.sosyal_plan.map(f=>`<li><b>${kacir(f.baslik)}</b> <small>· ${kacir(f.format_ad)}</small><br><small>${kacir(f.kanca)}</small></li>`).join("")}</ul></div>`:""}
      <div style="margin-top:14px;border-top:1px solid var(--cizgi);padding-top:12px">
        <span class="etk" style="color:var(--gri)">Etkileşim oranı — rakamları profilden elle gir</span>
        <p style="font-size:12.5px;color:var(--gri);margin:6px 0 9px">
          Takipçi ve son 5-10 gönderinin ortalama beğeni+yorumu. Platform API'si olmadan
          bu veri alınamıyor; elle girilen rakam öyle işaretleniyor.</p>
        <div class="arac">
          <div class="alan" style="max-width:130px"><label>Platform</label>
            <select id="et-platform">
              <option value="instagram">Instagram</option><option value="youtube">YouTube</option>
              <option value="linkedin">LinkedIn</option><option value="tiktok">TikTok</option>
              <option value="facebook">Facebook</option></select></div>
          <div class="alan" style="max-width:110px"><label>Takipçi</label>
            <input type="number" id="et-takipci" placeholder="2400"></div>
          <div class="alan" style="max-width:130px"><label>Ort. etkileşim</label>
            <input type="number" id="et-etkilesim" placeholder="42"></div>
          <div class="alan" style="max-width:120px"><label>Aylık paylaşım</label>
            <input type="number" id="et-tempo" placeholder="4"></div>
          <button class="dug sade" onclick="etkilesimHesapla(${a.id},'${kacir(a.sektor)}')">Hesapla</button>
        </div>
        <div id="et-sonuc" style="margin-top:10px"></div>
      </div>
      ${d.sosyal_demo?`<div class="arac" style="margin-top:12px">
        <a class="dug" style="text-decoration:none" href="/cikti/${encodeURI(d.sosyal_demo)}" target="_blank">Sosyal medya demosunu aç ↗</a></div>`
       :`<p style="color:var(--gri);font-size:13px;margin-top:10px">Demo sayfası müşteri dosyası çıkarılınca üretilir.</p>`}
      </div>`;})()}

    ${p?`<div class="blok"><span class="etk">Piyasa — ${kacir(p.ad)}</span>
      <div class="satir">
        <div><span class="etk">${kacir(p.sehir||"Türkiye")} aralığı</span><b>${bicim(p.alt)} – ${bicim(p.ust)} ₺</b></div>
        <div><span class="etk">Orta nokta</span><b>${bicim(p.orta)} ₺</b></div>
        <div><span class="etk">Önerilen teklif</span><b style="color:var(--kirmizi)">${bicim(d.onerilen_bedel)} ₺</b></div>
      </div>
      ${p.kendi_veri?`<p style="color:var(--yesil);font-size:13.5px;margin-top:10px">Kendi kaydettiğin ${p.kendi_veri.adet} rakip teklif ortalaması: ${bicim(p.kendi_veri.ortalama)} ₺</p>`:""}
      <p style="color:var(--gri);font-size:13px;margin-top:8px">${kacir(p.not)}</p></div>`:""}

    <div class="blok"><span class="etk">Müşteri dosyası</span>
      <div class="alan" style="max-width:300px"><label>Teklif bedeli (₺) — boş bırakırsan önerilen kullanılır</label>
        <input type="number" id="d-bedel" placeholder="${d.onerilen_bedel||""}"></div>
      <label style="display:flex;gap:8px;align-items:center;font-size:13.5px;margin:8px 0">
        <input type="checkbox" id="d-telegram" checked> Hazır olunca <b>Telegram&#39;a</b> gönder
        (metin + görseller + film + belgeler)</label>
      <div class="arac">
        <button class="dug" onclick="dosyaCikar(${a.id})">Dosyayı çıkar</button>
        ${a.dosya?`<button class="dug sade" onclick="dosyaAc(${a.id})">Analizi aç</button>`:""}
        <button class="dug sade" onclick="temasEt(${a.id})">Temas kaydı</button>
      </div>
      <div id="d-sonuc"></div></div>

    ${tem.length?`<div class="blok"><span class="etk">Temas geçmişi</span>
      <ul>${tem.map(t=>`<li>${kacir((t.tarih||"").slice(0,16))} · ${t.yon==="gelen"?"← gelen":"→ giden"}
        · ${kacir(t.kanal||"")} · <b>${kacir(t.durum||"")}</b>
        ${t.sonraki_tarih?`<br><small>sonraki: ${kacir(t.sonraki_adim||"")} (${kacir(t.sonraki_tarih)})</small>`:""}
        ${t.not_?`<br><small>${kacir(t.not_)}</small>`:""}</li>`).join("")}</ul></div>`:""}`;
  cekmeceAc();
}

/* ---------------- ZİYARET RAPORU ---------------- */
async function ziyaretYukle(){
  const f=document.getElementById("zy-dosya").files[0];
  const d=document.getElementById("zy-durum");
  if(!f){d.innerHTML='<div class="uyari">Önce dosyayı seç.</div>';return;}
  d.innerHTML='<div class="mesaj">Okunuyor…</div>';
  const b64=await new Promise((ok,hata)=>{const r=new FileReader();
    r.onload=()=>ok(String(r.result).split(",")[1]);r.onerror=hata;r.readAsDataURL(f);});
  const y=await jpost("/api/ziyaret-yukle",{ad:f.name,veri:b64,
    donem:document.getElementById("zy-donem").value||""});
  if(y.hata){d.innerHTML='<div class="uyari">'+kacir(y.hata)+'</div>';return;}
  d.innerHTML='<div class="mesaj" style="border-color:var(--yesil)">Okundu: '+
    kacir((y.tablo||[]).join(", "))+'</div>';
  ziyaretCiz(y);
}
function ziyaretCiz(y){
  const h=document.getElementById("zy-sonuc"); const t=y.toplam||{};
  const gun=y.gun||[]; const enb=Math.max(1,...gun.map(g=>g.kullanici||0));
  let g="";
  g+=`<div class="kutular" style="margin-top:14px">
    ${arKutu("Günlük ortalama",t.gunluk_ortalama??"—","kişi/gün")}
    ${arKutu("Toplam ziyaretçi",bicim(t.kullanici||0),(y.gun_sayisi||0)+" günde")}
    ${arKutu("Sayfa görüntüleme",bicim(t.goruntuleme||0),"kişi başı "+(t.sayfa_basi??"—"))}
    ${arKutu("İletişim eylemi",bicim(y.iletisim_toplam||0),y.donusum!=null?("dönüşüm %"+y.donusum):"olay verisi yok")}
  </div>`;
  if((y.yorum||[]).length)
    g+='<div class="mesaj" style="margin-top:12px">'+y.yorum.map(kacir).join("<br>")+'</div>';

  if(gun.length){
    g+=`<div class="kart" style="margin-top:16px"><span class="etk">Günlük ziyaretçi</span>
      <div style="display:flex;align-items:flex-end;gap:4px;height:120px;margin-top:14px">
      ${gun.map(x=>`<div title="${kacir(x.tarih)}: ${x.kullanici} kişi" style="flex:1;height:100%;
        display:flex;flex-direction:column;justify-content:flex-end;align-items:center;gap:4px">
        <span style="font-size:10px;color:var(--gri)">${x.kullanici}</span>
        <i style="display:block;width:100%;background:var(--kirmizi);border-radius:2px 2px 0 0;min-height:3px;
           height:${Math.max(4,Math.round(100*(x.kullanici||0)/enb))}%"></i></div>`).join("")}
      </div>
      <div style="display:flex;gap:4px;margin-top:6px">
      ${gun.map(x=>`<span style="flex:1;text-align:center;font-size:9.5px;color:#6f6d68;
        font-family:'Space Mono',monospace">${kacir((x.tarih||"").slice(5))}</span>`).join("")}
      </div></div>`;
  }
  if((y.iletisim||[]).length){
    g+=`<div class="kart" style="margin-top:16px"><span class="etk">Butona basanlar</span>
      <table style="margin-top:10px"><thead><tr><th>Eylem</th><th class="sag">Kaç kez</th></tr></thead><tbody>
      ${y.iletisim.map(i=>`<tr><td><b>${kacir(i.ad)}</b></td><td class="sag">${i.adet}</td></tr>`).join("")}
      </tbody></table></div>`;
  }
  if((y.sayfa||[]).length){
    g+=`<div class="kart" style="margin-top:16px"><span class="etk">En çok bakılan sayfalar</span>
      <table style="margin-top:10px"><thead><tr><th>Sayfa</th><th class="sag">Görüntüleme</th>
      <th class="sag">Kişi</th></tr></thead><tbody>
      ${y.sayfa.slice(0,20).map(s=>`<tr><td>${kacir(s.yol)}</td>
        <td class="sag">${bicim(s.goruntuleme)}</td><td class="sag">${bicim(s.kullanici)}</td></tr>`).join("")}
      </tbody></table></div>`;
  }
  if((y.kaynak||[]).length){
    g+=`<div class="kart" style="margin-top:16px"><span class="etk">Nereden geldiler</span>
      <table style="margin-top:10px"><thead><tr><th>Kaynak</th><th class="sag">Kişi</th></tr></thead><tbody>
      ${y.kaynak.slice(0,12).map(k=>`<tr><td>${kacir(k.ad)}</td><td class="sag">${bicim(k.kullanici)}</td></tr>`).join("")}
      </tbody></table></div>`;
  }
  h.innerHTML=g;
}
async function ziyaretGecmis(){
  const y=await jget("/api/ziyaret"); const d=document.getElementById("zy-durum");
  if(!y.liste||!y.liste.length){d.innerHTML='<div class="uyari">Henüz yükleme yok.</div>';return;}
  d.innerHTML='<table style="margin-top:10px"><thead><tr><th>Tarih</th><th>Dönem</th>'+
    '<th class="sag">Kişi</th><th class="sag">Görüntüleme</th><th class="sag">İletişim</th><th></th></tr></thead><tbody>'+
    y.liste.map(x=>`<tr><td>${kacir((x.yuklendi||"").slice(0,16))}</td><td>${kacir(x.donem||"—")}</td>
      <td class="sag">${bicim(x.kullanici||0)}</td><td class="sag">${bicim(x.goruntuleme||0)}</td>
      <td class="sag">${x.iletisim||0}</td>
      <td><button class="dug sade mini" onclick="ziyaretAc(${x.id})">aç</button></td></tr>`).join("")+
    '</tbody></table></div>';
  if(y.kayit&&y.kayit.ozet) ziyaretCiz(y.kayit.ozet);
}
async function ziyaretAc(id){
  const y=await jget("/api/ziyaret?id="+id);
  if(y.kayit&&y.kayit.ozet) ziyaretCiz(y.kayit.ozet);
}

/* ---------------- SİTE SAĞLIĞI ---------------- */
async function saglikOlc(){
  const h=document.getElementById("sg-sonuc");
  h.innerHTML='<div class="mesaj">331 sayfa taranıyor…</div>';
  const y=await jpost("/api/saglik",{olc:true});
  if(y.sorun){h.innerHTML='<div class="uyari">'+kacir(y.sorun)+'</div>';return;}
  saglikCiz(y);
}
function saglikCiz(y){
  const h=document.getElementById("sg-sonuc");
  const renk=v=>v>=99?"var(--yesil)":(v>=90?"var(--sari)":"var(--kirmizi)");
  const d=y.degisim;
  const ok=(n,ters)=>n===0?'<span style="color:var(--gri)">değişmedi</span>':
    `<span style="color:${(ters?n<0:n>0)?'var(--yesil)':'var(--kirmizi)'}">${n>0?"+":""}${n}</span>`;
  let g=`<div class="kutular">
    ${arKutu("SEO uygunluk","%"+y.oran, d?("önceki: %"+(y.oran-d.oran).toFixed(1)):"ilk ölçüm")}
    ${arKutu("Taranan sayfa",bicim(y.sayfa), d?("değişim "+(d.sayfa>0?"+":"")+d.sayfa):"")}
    ${arKutu("Hata",y.hata, d?ok(d.hata,true):"")}
    ${arKutu("Uyarı",y.uyari, d?ok(d.uyari,true):"")}
  </div>
  <table style="margin-top:14px"><thead><tr><th>Kategori</th><th class="sag">Sayfa</th>
    <th class="sag">Hata</th><th class="sag">Uyarı</th><th class="sag">Uygunluk</th></tr></thead><tbody>
    ${(y.kategori||[]).map(k=>`<tr><td><b>${kacir(k.ad)}</b></td><td class="sag">${k.sayfa}</td>
      <td class="sag">${k.hata}</td><td class="sag">${k.uyari}</td>
      <td class="sag" style="color:${renk(k.oran)}">%${k.oran}</td></tr>`).join("")}
  </tbody></table></div>`;
  if((y.kod||[]).length){
    g+=`<div style="margin-top:14px"><span class="etk" style="color:var(--gri)">Bulgu türleri</span>
      <table style="margin-top:8px"><tbody>
      ${y.kod.slice(0,8).map(x=>`<tr><td><span class="rz" style="${x.tur==='HATA'?'border-color:var(--kirmizi);color:var(--kirmizi)':''}">${kacir(x.tur)}</span> ${kacir(x.kod)}</td>
        <td class="sag">${x.adet}</td></tr>`).join("")}
      </tbody></table></div>`;
  }
  const orn=(y.kategori||[]).flatMap(k=>k.ornek||[]).slice(0,10);
  if(orn.length){
    g+=`<div style="margin-top:14px"><span class="etk" style="color:var(--gri)">Örnek bulgular</span>
      <table style="margin-top:8px"><tbody>
      ${orn.map(o=>`<tr><td><small>${kacir(o.sayfa)}</small></td><td><small>${kacir(o.mesaj)}</small></td></tr>`).join("")}
      </tbody></table></div>`;
  }
  if((y.gecmis||[]).length>1){
    const gc=y.gecmis; const enb=100;
    g+=`<div class="kart" style="margin-top:16px"><span class="etk">Günlük seyir</span>
      <div style="display:flex;align-items:flex-end;gap:3px;height:90px;margin-top:12px">
      ${gc.map(x=>`<div title="${kacir(x.tarih)}: %${x.oran}" style="flex:1;height:100%;
        display:flex;flex-direction:column;justify-content:flex-end"><i style="display:block;width:100%;
        background:${renk(x.oran)};border-radius:2px 2px 0 0;min-height:3px;
        height:${Math.max(4,Math.round(100*x.oran/enb))}%"></i></div>`).join("")}
      </div></div>`;
  }
  h.innerHTML=g;
}
async function saglikGecmis(){
  const y=await jpost("/api/saglik",{});
  const gc=y.gecmis||[]; const h=document.getElementById("sg-sonuc");
  if(!gc.length){h.innerHTML='<div class="uyari">Henüz ölçüm yok. "Şimdi tara" ile başla.</div>';return;}
  h.innerHTML='<div class="tablo-kaydir"><table><thead><tr><th>Tarih</th><th class="sag">Sayfa</th><th class="sag">Hata</th>'+
    '<th class="sag">Uyarı</th><th class="sag">Uygunluk</th></tr></thead><tbody>'+
    gc.slice().reverse().map(x=>`<tr><td>${kacir(x.tarih)}</td><td class="sag">${x.sayfa}</td>
      <td class="sag">${x.hata}</td><td class="sag">${x.uyari}</td><td class="sag">%${x.oran}</td></tr>`).join("")+
    '</tbody></table></div>';
}

/* ---------------- YAYIN / DEPO / INDEXNOW ---------------- */
async function taslakListe(){
  const h=document.getElementById("ya-liste");
  const y=await jpost("/api/yayin-taslaklar",{});
  const t=y.taslak||[];
  if(!t.length){h.innerHTML='<div class="uyari">Henüz taslak yok. Önce gündemi tarayıp taslak çıkar.</div>';return;}
  h.innerHTML='<div class="tablo-kaydir"><table><thead><tr><th>Taslak</th><th class="sag">Dolu bölüm</th><th class="sag">SSS</th><th>Durum</th><th></th></tr></thead><tbody>'+
    t.map(x=>`<tr><td><b>${kacir(x.baslik||x.dosya)}</b><br><small>${kacir(x.dosya)}</small>
      ${x.uyari.length?'<br><small style="color:var(--sari)">'+x.uyari.map(kacir).join('<br>')+'</small>':''}</td>
      <td class="sag">${x.dolu_bolum}</td><td class="sag">${x.sss}</td>
      <td><span class="rz ${x.hazir?'ok':''}" style="${x.hazir?'':'border-color:var(--sari);color:var(--sari)'}">${x.hazir?"hazır":"eksik"}</span></td>
      <td><button class="dug ${x.hazir?'':'sade'} mini" onclick="yayinla(${JSON.stringify(x.yol).replace(/"/g,'&quot;')})">Yayınla</button></td></tr>`).join("")+
    '</tbody></table></div>';
}
async function yayinla(yol){
  const s=document.getElementById("ya-sonuc");
  s.innerHTML='<div class="mesaj" style="margin-top:12px">Yayınlanıyor…</div>';
  const y=await jpost("/api/yayinla",{yol:yol,bildir:document.getElementById("ya-bildir").checked});
  if(y.hata){s.innerHTML='<div class="uyari" style="margin-top:12px"><b>'+kacir(y.hata)+'</b>'+
    ((y.uyari||[]).length?'<ul>'+y.uyari.map(u=>'<li>'+kacir(u)+'</li>').join("")+'</ul>':'')+'</div>';return;}
  const ix=y.indexnow;
  s.innerHTML=`<div class="mesaj" style="margin-top:12px;border-color:var(--yesil)">
    <b>Yayınlandı:</b> blog/${kacir(y.dosya)} · ${y.kelime} kelime · blogda toplam ${y.yazi_sayisi} yazı<br>
    <small>Adres: ${kacir(y.url)} · sitemap.xml güncellendi</small>
    ${(y.uyari||[]).length?'<div style="margin-top:9px;color:var(--sari)">'+y.uyari.map(kacir).join('<br>')+'</div>':''}
    ${ix?`<div style="margin-top:9px"><b>IndexNow:</b> ${ix.gonderilen||0} adres · `+
      ((ix.sonuc||[]).map(r=>kacir(r.uc)+" "+r.durum).join(" · ")||kacir(ix.hata||""))+`</div>`:""}
    <div style="margin-top:10px;color:var(--gri)">Sıradaki adım: GitHub Desktop'tan yayınla —
      dosya bilgisayarında hazır ama siteye ancak push'tan sonra çıkıyor.</div></div>`;
  taslakListe();
}
async function depoDurum(){
  const h=document.getElementById("ya-depo");
  const d=await jpost("/api/depo",{islem:"durum"});
  if(d.hata){h.innerHTML='<div class="uyari">'+kacir(d.hata)+'</div>';return;}
  const kilit=(d.kilit||[]).length;
  h.innerHTML=`<div class="satir">
      <div><span class="etk">Dal</span><b>${kacir(d.dal||"—")}</b></div>
      <div><span class="etk">Bekleyen değişiklik</span><b>${d.degisiklik}</b>
        <small style="color:var(--gri)">${d.degisen} değişen · ${d.yeni} yeni</small></div>
      <div><span class="etk">Kilit</span><b style="color:${kilit?'var(--kirmizi)':'var(--yesil)'}">${kilit?kilit+" adet":"yok"}</b></div>
      <div><span class="etk">Çalışan git</span><b>${(d.surec||[]).length?kacir(d.surec.join(", ")):"yok"}</b></div>
    </div>
    ${d.son_islem?'<p style="color:var(--gri);font-size:13px;margin-top:10px">son işlem: '+kacir(d.son_islem)+'</p>':''}
    ${kilit?'<table style="margin-top:12px"><thead><tr><th>Kilit</th><th>Oluşma</th><th class="sag">Yaş</th><th class="sag">Boyut</th></tr></thead><tbody>'+
      d.kilit.map(k=>`<tr><td>${kacir(k.ad)}</td><td>${kacir(k.zaman)}</td>
        <td class="sag">${k.yas_dk} dk</td><td class="sag">${k.bayt} B</td></tr>`).join("")+'</tbody></table></div>':''}`;
}
async function depoKilit(zorla){
  const h=document.getElementById("ya-depo");
  const d=await jpost("/api/depo",{islem:"kilit-coz",zorla:!!zorla});
  const iyi=(d.kaldirilan||[]).length>0;
  h.innerHTML=`<div class="mesaj" style="border-color:${iyi?'var(--yesil)':'var(--sari)'}">
    ${kacir(d.mesaj||"")}
    ${(d.kaldirilan||[]).length?'<br><small>'+d.kaldirilan.map(k=>kacir(k.ad)+" ("+kacir(k.nasil)+")").join(", ")+'</small>':''}
    ${d.yarim_nesne?'<br><small>'+d.yarim_nesne+' yarım nesne temizlendi</small>':''}
    ${(d.atlanan||[]).length&&!zorla?'<div class="arac" style="margin-top:10px"><button class="dug sade mini" onclick="depoKilit(true)">Yine de zorla</button></div>':''}
  </div>`;
  setTimeout(depoDurum,400);
}
async function inDurum(){
  const h=document.getElementById("ya-index");
  const d=await jpost("/api/indexnow",{islem:"durum"});
  h.innerHTML=`<div class="mesaj" style="border-color:${d.kurulu?'var(--yesil)':'var(--sari)'}">
    <b>${d.kurulu?"Anahtar kurulu":"Anahtar yok"}</b>${d.dosya?" · "+kacir(d.dosya):""}<br>
    <small>${kacir(d.not)}</small>
    ${d.adres?'<br><small>adres: '+kacir(d.adres)+'</small>':''}</div>`;
}
async function inAnahtar(){
  const d=await jpost("/api/indexnow",{islem:"anahtar"});
  document.getElementById("ya-index").innerHTML=
    `<div class="mesaj" style="border-color:var(--yesil)"><b>${d.yeni?"Anahtar üretildi":"Anahtar zaten vardı"}</b><br>
     <small>${kacir(d.anahtar)}.txt site köküne yazıldı. Siteyi yayınladıktan sonra bildirim çalışır.</small></div>`;
}
async function inBildir(){
  const h=document.getElementById("ya-index");
  h.innerHTML='<div class="mesaj">Bildiriliyor…</div>';
  const d=await jpost("/api/indexnow",{islem:"bildir"});
  if(d.hata){h.innerHTML='<div class="uyari">'+kacir(d.hata)+'</div>';return;}
  h.innerHTML=`<div class="mesaj"><b>${d.gonderilen} adres bildirildi</b><br>`+
    (d.sonuc||[]).map(r=>`<small>${kacir(r.uc)}: ${r.durum} — ${kacir(r.not)}</small>`).join("<br>")+
    `<br><small style="color:var(--gri)">anahtar: ${kacir(d.anahtar_adresi||"")}</small></div>`;
}

/* ---------------- GÜNDEM ---------------- */
let GUNDEM=[];
async function gundemTara(){
  const d=document.getElementById("gu-durum");
  d.innerHTML='<div class="mesaj">Gündem taranıyor — 10 konu, birkaç saniye…</div>';
  const y=await jpost("/api/gundem",{asgari:document.getElementById("gu-asgari").value,
                                     adet:document.getElementById("gu-adet").value});
  if(y.hata){d.innerHTML='<div class="uyari">'+kacir(y.hata)+
    '<br><small>İnternet bağlantısı gerekiyor. Kaynak testi ile kontrol et.</small></div>';return;}
  GUNDEM=y.liste||[];
  if(!GUNDEM.length){d.innerHTML='<div class="uyari">'+kacir(y.not||"Uygun haber çıkmadı.")+'</div>';
    document.getElementById("gu-liste").innerHTML="";return;}
  d.innerHTML='<div class="mesaj" style="border-color:var(--yesil)">'+GUNDEM.length+
    ' haberde yazacak sözümüz var.</div>';
  gundemCiz();
}
function gundemCiz(){
  document.getElementById("gu-liste").innerHTML=GUNDEM.map((h,i)=>{
    const renk=h.puan>=65?"var(--yesil)":(h.puan>=50?"var(--sari)":"var(--gri)");
    return `<div class="kart" style="margin-top:14px">
      <div style="display:flex;gap:16px;align-items:flex-start;flex-wrap:wrap">
        <div style="flex:1;min-width:280px">
          <span class="etk" style="color:${renk}">İlgi ${h.puan}/100 · ${kacir(h.aci.ad)}</span>
          <h3 style="font-size:19px;margin:7px 0 4px">${kacir(h.aci.baslik)}</h3>
          <p style="color:var(--gri);font-size:13.5px;line-height:1.6">${kacir(h.aci.gerekce)}</p>
          <p style="font-size:12.5px;margin-top:9px">
            <span style="color:#6f6d68">tetikleyen haber:</span>
            <a href="${kacir(h.adres)}" target="_blank">${kacir(h.baslik)} ↗</a>
            ${h.kaynak?'<span style="color:#6f6d68"> · '+kacir(h.kaynak)+'</span>':''}</p>
          <p style="font-size:12.5px;color:#6f6d68;margin-top:5px">
            bağlanacak sayfa: ${kacir(h.aci.hizmet_sayfa||"—")}
            ${h.il?' · yerel bağ: '+kacir(h.il):''}</p>
          <p style="font-size:11.5px;color:#6f6d68;margin-top:5px;font-family:'Space Mono',monospace">
            ${(h.gerekce||[]).map(kacir).join(" · ")}</p>
        </div>
        <div style="display:flex;flex-direction:column;gap:8px">
          <label style="font-size:13px;display:flex;gap:6px;align-items:center">
            <input type="checkbox" data-gu-sec="${i}"> Günün sayısına al</label>
          <button class="dug sade" onclick="gundemTaslak(${i})">Taslak çıkar</button>
        </div>
      </div>
      <div data-gu-metin="${i}" hidden style="margin-top:12px;display:grid;gap:8px">
        <textarea data-gu-olgu="${i}" rows="3" placeholder="Olgu: haberde geçen rakam ve gerçekler (2–3 cümle, uydurma yok)" style="width:100%"></textarea>
        <textarea data-gu-aci="${i}" rows="2" placeholder="Bizim için ne demek: tek açı, tek cümle-iki cümle" style="width:100%">${kacir((h.aci&&h.aci.bizim_soz)||"")}</textarea>
      </div></div>`;}).join("")+
    `<div class="arac" style="margin-top:16px">
      <button class="dug" onclick="gundemYayinla()">Seçilenleri günün sayısı olarak siteye yayınla</button>
      <span style="color:var(--gri);font-size:13px">SEO kapısından geçmeyen sayı yayınlanmaz.</span>
    </div><div id="gu-yayin"></div>`;
  document.querySelectorAll("[data-gu-sec]").forEach(k=>k.addEventListener("change",e=>{
    const m=document.querySelector('[data-gu-metin="'+e.target.dataset.guSec+'"]'); if(m) m.hidden=!e.target.checked;}));
}
async function gundemYayinla(){
  const sec=[...document.querySelectorAll("[data-gu-sec]:checked")].map(k=>parseInt(k.dataset.guSec));
  if(!sec.length){tost("Haber seçilmedi.");return;}
  const haberler=sec.map(i=>{const h=Object.assign({},GUNDEM[i]);
    h.olgu=(document.querySelector('[data-gu-olgu="'+i+'"]')||{}).value||"";
    h.aci_metin=(document.querySelector('[data-gu-aci="'+i+'"]')||{}).value||"";
    h.hizmet_sayfa=(h.aci&&h.aci.hizmet_sayfa)||h.hizmet_sayfa; return h;});
  const eksik=haberler.filter(h=>!h.olgu.trim());
  if(eksik.length){tost("Seçilen her habere olgu cümlesi yaz — kaynaktaki rakam ve gerçekler.",6000);return;}
  const y=document.getElementById("gu-yayin");
  y.innerHTML='<div class="mesaj">Yayınlanıyor, SEO kapısı çalışıyor…</div>';
  const r=await jpost("/api/gundem-yayinla",{haberler:haberler});
  if(r.hata){y.innerHTML='<div class="uyari">'+kacir(r.hata)+'</div>';return;}
  y.innerHTML=`<div class="mesaj" style="border-color:var(--yesil)"><b>${r.madde} madde yayınlandı</b> → ${kacir(r.sayfa||"")}
    <br><small>Menüye eklenen sayfa: ${r.menu_eklenen} · Kapı: ${kacir(JSON.stringify(r.kapi||"—"))}</small>
    <br><small>Şimdi: GitHub Desktop → Commit → Push.</small></div>`;
}
async function gundemTaslak(i){
  const h=GUNDEM[i]; const t=document.getElementById("gu-taslak");
  t.innerHTML='<div class="mesaj" style="margin-top:14px">Taslak hazırlanıyor…</div>';
  const y=await jpost("/api/gundem-taslak",{haber:h});
  if(y.hata){t.innerHTML='<div class="uyari">'+kacir(y.hata)+'</div>';return;}
  t.innerHTML=`<div class="kart" style="margin-top:18px">
    <span class="etk">Yazı taslağı</span>
    <p style="color:var(--gri);font-size:13.5px;margin:8px 0 12px">
      Dosya: <a href="/cikti/${encodeURI(y.yol)}" target="_blank">${kacir(y.yol)} ↗</a>
      · Bölüm başlıkları ve ne yazılacağı hazır; metni sen yazıyorsun.
      Yayına almak için <code>site-uretici/blog.py</code> içindeki YAZILAR listesine ekle.</p>
    <pre style="background:var(--ink);border:1px solid var(--cizgi);border-radius:4px;padding:18px;
      max-height:420px;overflow:auto;font-size:12.5px;line-height:1.65;white-space:pre-wrap">${kacir(y.metin)}</pre>
    <div class="arac" style="margin-top:12px">
      <button class="dug sade" onclick="kopyala(${JSON.stringify(y.metin).replace(/"/g,'&quot;')})">Taslağı kopyala</button>
      <button class="dug sade" onclick="kopyala(${JSON.stringify(y.sosyal.govde).replace(/"/g,'&quot;')})">Sosyal metni kopyala</button>
    </div>
    <div class="mesaj" style="margin-top:14px"><b>Sosyal kesit (${kacir(y.sosyal["biçim"])})</b><br>
      ${kacir(y.sosyal.govde)}<br><small style="color:var(--gri)">${kacir(y.sosyal.not)}</small></div>
  </div>`;
  t.scrollIntoView({behavior:"smooth",block:"start"});
}
async function gundemKaynak(){
  const d=document.getElementById("gu-durum");
  d.innerHTML='<div class="mesaj">Kaynaklar deneniyor…</div>';
  const y=await jget("/api/gundem-kaynak");
  const k=y.kaynak||[];
  const calisan=k.filter(x=>x.haber>0).length;
  d.innerHTML=`<div class="mesaj" style="border-color:${calisan?'var(--yesil)':'var(--kirmizi)'}">
    ${calisan}/${k.length} konu veri döndü${calisan?"":" — internet bağlantısını kontrol et"}</div>
    <table style="margin-top:10px"><thead><tr><th>Konu</th><th class="sag">Haber</th><th>Not</th></tr></thead><tbody>
    ${k.map(x=>`<tr><td>${kacir(x.konu)}</td><td class="sag">${x.haber}</td>
      <td><small>${kacir(x.hata||(x.haber?"tamam":"veri yok"))}</small></td></tr>`).join("")}
    </tbody></table></div>`;
}

/* ---------------- ARAMA PERFORMANSI ---------------- */
function arKutu(b,d,r){return `<div class="kutu"><span class="etk">${b}</span><b style="font-size:26px;display:block;margin-top:4px">${d}</b>${r?`<small style="color:var(--gri)">${r}</small>`:""}</div>`;}

async function aramaYukle(){
  const f=document.getElementById("ar-dosya").files[0];
  const d=document.getElementById("ar-durum");
  if(!f){d.innerHTML='<div class="uyari">Önce dosyayı seç.</div>';return;}
  d.innerHTML='<div class="mesaj">Okunuyor…</div>';
  const b64=await new Promise((ok,hata)=>{const r=new FileReader();
    r.onload=()=>ok(String(r.result).split(",")[1]);r.onerror=hata;r.readAsDataURL(f);});
  const y=await jpost("/api/arama-yukle",{ad:f.name,veri:b64,
    donem:document.getElementById("ar-donem").value||""});
  if(y.hata){d.innerHTML='<div class="uyari">'+kacir(y.hata)+'</div>';return;}
  d.innerHTML='<div class="mesaj" style="border-color:var(--yesil)">Okundu: '+
    kacir(y.bulunan_tablo.join(", "))+(y.site_tarandi?" · site klasörü tarandı":"")+'</div>';
  aramaCiz(y);
}

function aramaCiz(y){
  const h=document.getElementById("ar-sonuc"); const sp=y.sayfa, sq=y.sorgu;
  if(!sp&&!sq){h.innerHTML='<div class="uyari">Dosyada sayfa/sorgu tablosu yok.</div>';return;}
  let g="";
  if(sp){
    const t=sp.toplam;
    g+=`<div class="kart"><span class="etk">Toplam · ${kacir(y.kaynak)}</span>
      <div class="kutular" style="margin-top:12px">
        ${arKutu("Tıklanma",bicim(t.tiklama))}
        ${arKutu("Gösterim",bicim(t.gosterim))}
        ${arKutu("Ortalama TO","%"+(t.gosterim?(100*t.tiklama/t.gosterim).toFixed(2):"0"))}
        ${arKutu("Veri gelen sayfa",bicim(t.sayfa), t.gorunmeyen?bicim(t.gorunmeyen)+" sayfa hiç görünmemiş":"")}
      </div></div>`;

    g+=`<div class="kart" style="margin-top:18px"><span class="etk">Şehir kırılımı — hangi ilde kaç tıklanma</span>
      <table style="margin-top:12px"><thead><tr><th>Şehir</th><th class="sag">Tıklanma</th>
      <th class="sag">Gösterim</th><th class="sag">TO</th><th class="sag">Ort. konum</th><th class="sag">Sayfa</th></tr></thead><tbody>
      ${(sp.il||[]).map(x=>`<tr><td><b>${kacir(x.ad)}</b></td>
        <td class="sag" style="color:${x.tiklama?'var(--bone)':'var(--kirmizi)'}">${x.tiklama}</td>
        <td class="sag">${bicim(x.gosterim)}</td><td class="sag">%${x.to}</td>
        <td class="sag">${x.konum==null?"—":x.konum}</td><td class="sag">${x.sayfa}</td></tr>`).join("")
        ||'<tr><td colspan="6" class="bos">Şehir sayfası verisi yok</td></tr>'}
      </tbody></table></div>`;

    g+=`<div class="kart" style="margin-top:18px"><span class="etk">Hizmet kırılımı</span>
      <table style="margin-top:12px"><thead><tr><th>Hizmet</th><th class="sag">Tıklanma</th>
      <th class="sag">Gösterim</th><th class="sag">Ort. konum</th></tr></thead><tbody>
      ${(sp.hizmet||[]).map(x=>`<tr><td>${kacir(x.ad||"—")}</td><td class="sag">${x.tiklama}</td>
        <td class="sag">${bicim(x.gosterim)}</td><td class="sag">${x.konum==null?"—":x.konum}</td></tr>`).join("")}
      </tbody></table></div>`;

    const liste=(b,ac,arr,renk)=>`<div class="kart" style="margin-top:18px">
      <span class="etk" style="color:${renk}">${b}</span>
      <p style="color:var(--gri);font-size:13.5px;margin:8px 0 10px">${ac}</p>
      ${arr.length?`<div class="tablo-kaydir"><table><thead><tr><th>Sayfa</th><th class="sag">Gösterim</th>
        <th class="sag">Tık</th><th class="sag">Konum</th></tr></thead><tbody>
        ${arr.map(x=>`<tr><td><a href="https://lunayapim.com${kacir(x.yol)}" target="_blank">${kacir(x.yol)}</a>
          ${x.il?'<br><small>'+kacir(x.il)+(x.hizmet?" · "+kacir(x.hizmet):"")+'</small>':""}</td>
          <td class="sag">${bicim(x.gosterim)}</td><td class="sag">${x.tiklama}</td>
          <td class="sag">${x.konum==null?"—":x.konum}</td></tr>`).join("")}
        </tbody></table></div>`:'<p class="bos">Bu listede sayfa yok.</p>'}</div>`;

    g+=liste("Kapıda kaybediyoruz","Gösterim alıyor ama hiç tıklanmıyor. Başlık ve açıklama metni işini yapmıyor demektir — en hızlı kazanç burada.",sp.kapida||[],"var(--kirmizi)");
    g+=liste("İkinci sayfa — itilecek olanlar","Konum 11–20 arası. Birkaç iç bağlantı ve içerik takviyesiyle ilk sayfaya taşınabilecek sayfalar.",sp.ikinci_sayfa||[],"var(--sari)");
    g+=liste("İlk sayfada, zirveye yakın","Konum 3–10 arası. Küçük iyileştirmeyle ilk üçe girebilir.",sp.yakin||[],"var(--yesil)");

    if((sp.olu||[]).length){
      g+=`<div class="kart" style="margin-top:18px"><span class="etk">Hiç görünmeyen sayfalar (${sp.olu.length})</span>
        <p style="color:var(--gri);font-size:13.5px;margin:8px 0 10px">Sitede yayında ama bu dönemde
          tek gösterim bile almamış. Yeni sayfalarda normaldir; eskiyorsa iç bağlantı ve içerik gerekiyor.</p>
        <div style="max-height:280px;overflow:auto"><div class='tablo-kaydir'><table><tbody>
        ${sp.olu.map(x=>`<tr><td>${kacir(x.yol)}</td><td><small>${kacir(x.il||"")}</small></td></tr>`).join("")}
        </tbody></table></div></div>`;
    }
  }
  if(sq){
    g+=`<div class="kart" style="margin-top:18px"><span class="etk">Sorgular — yerel niyet payı %${sq.yerel_pay}</span>
      <p style="color:var(--gri);font-size:13.5px;margin:8px 0 12px">İçinde şehir adı geçen sorguların
        gösterimdeki payı. Yerel iş için bu oranın yükselmesini istiyoruz.</p>
      <div class="satir">
        <div><span class="etk">Şehirli sorgu</span><b>${sq.yerel.length}</b></div>
        <div><span class="etk">Genel sorgu</span><b>${sq.genel.length}</b></div>
      </div>
      <table style="margin-top:14px"><thead><tr><th>Sorgu</th><th>Şehir</th><th class="sag">Tık</th>
        <th class="sag">Gösterim</th><th class="sag">Konum</th></tr></thead><tbody>
        ${sq.yerel.slice(0,25).map(x=>`<tr><td>${kacir(x.sorgu)}</td><td><small>${kacir(x.il)}</small></td>
          <td class="sag">${x.tiklama}</td><td class="sag">${bicim(x.gosterim)}</td>
          <td class="sag">${x.konum==null?"—":x.konum}</td></tr>`).join("")}
      </tbody></table></div>`;
  }
  h.innerHTML=g;
}

async function aramaGecmis(){
  const y=await jget("/api/arama");
  const d=document.getElementById("ar-durum");
  if(!y.liste||!y.liste.length){d.innerHTML='<div class="uyari">Henüz yükleme yok.</div>';return;}
  d.innerHTML='<table style="margin-top:10px"><thead><tr><th>Tarih</th><th>Dönem</th><th>Dosya</th>'+
    '<th class="sag">Tık</th><th class="sag">Gösterim</th><th></th></tr></thead><tbody>'+
    y.liste.map(x=>`<tr><td>${kacir((x.yuklendi||"").slice(0,16))}</td><td>${kacir(x.donem||"—")}</td>
      <td><small>${kacir(x.kaynak||"")}</small></td><td class="sag">${x.tiklama||0}</td>
      <td class="sag">${bicim(x.gosterim||0)}</td>
      <td><button class="dug sade mini" onclick="aramaAc(${x.id})">aç</button></td></tr>`).join("")+
    '</tbody></table></div>';
  if(y.kayit&&y.kayit.ozet) aramaCiz(y.kayit.ozet);
}
async function aramaAc(id){
  const y=await jget("/api/arama?id="+id);
  if(y.kayit&&y.kayit.ozet) aramaCiz(y.kayit.ozet);
}

async function altalanTest(){
  const h=document.getElementById("ar-altalan");
  h.innerHTML='<div class="mesaj">Kontrol ediliyor…</div>';
  const y=await jpost("/api/altalan-test",{alan:document.getElementById("ar-alan").value});
  if(y.hata){h.innerHTML='<div class="uyari">'+kacir(y.hata)+'</div>';return;}
  const renk={iyi:"var(--yesil)",dikkat:"var(--sari)",bilinmiyor:"var(--gri)",bilgi:"var(--gri)"};
  h.innerHTML=(y.yorum||[]).map(([d,m])=>
      `<div class="mesaj" style="border-color:${renk[d]||'var(--cizgi)'};margin-bottom:8px">
       <b style="color:${renk[d]||'var(--bone)'}">${d.toUpperCase()}</b> — ${kacir(m)}</div>`).join("")+
    '<table style="margin-top:12px"><thead><tr><th>Kontrol</th><th>Durum</th><th>Tür</th><th>Not</th></tr></thead><tbody>'+
    (y.kontrol||[]).map(k=>`<tr><td>${kacir(k.ad)}</td><td>${k.durum||"—"}</td>
      <td><small>${kacir(k.tur||"")}</small></td>
      <td><small>${kacir(k.hata||((k.ilk||"").slice(0,90)))}</small></td></tr>`).join("")+
    '</tbody></table></div>';
}

async function etkilesimHesapla(id, sektor){
  const h=document.getElementById("et-sonuc");
  const y=await jpost("/api/etkilesim",{aday_id:id,sektor:sektor,
    platform:document.getElementById("et-platform").value,
    takipci:document.getElementById("et-takipci").value,
    etkilesim:document.getElementById("et-etkilesim").value,
    aylik_paylasim:document.getElementById("et-tempo").value});
  if(y.hata){h.innerHTML='<div class="uyari">'+kacir(y.hata)+'</div>';return;}
  const renk={iyi:"var(--yesil)",normal:"var(--sari)",zayif:"var(--kirmizi)",kotu:"var(--kirmizi)"}[y.seviye];
  h.innerHTML=`<div class="mesaj" style="border-color:${renk}">
    <b style="color:${renk};font-size:19px">%${y.oran}</b> etkileşim oranı — <b>${kacir(y.seviye)}</b><br>
    <small>${kacir(y.yorum)}</small><br>
    <small style="color:var(--gri)">sektör kıyası: zayıf &lt;%${y.kiyas.zayif} · normal %${y.kiyas.normal} · iyi &gt;%${y.kiyas.iyi}
      · iyi banda çıkmak için gönderi başına ~${y.hedef_etkilesim} etkileşim gerekiyor</small>
    ${y.tempo?`<br><small style="color:var(--gri)">tempo: <b>${kacir(y.tempo.seviye)}</b> — ${kacir(y.tempo.yorum)}</small>`:""}
    <br><small style="color:#6f6d68;font-family:'Space Mono',monospace;font-size:10.5px">kaynak: ${kacir(y.kaynak)} · ${kacir(y.zaman)}</small>
  </div>`;
}

async function araştırTek(id){
  const y=await jpost("/api/zenginlestir",{ids:[id]});
  if(y.hata){tost(y.hata,5000);return;}
  tost("Araştırma başladı, birkaç saniye…",4000);
  aktifGorev=y.gorev;logIndex=0;
  const bekle=setInterval(async()=>{
    const g=await jget("/api/gorev?id="+y.gorev);
    if(g.durum==="bitti"||g.durum==="hata"){clearInterval(bekle);aktifGorev=null;
      await yukle();adayAc(id);tost("Araştırma bitti.");}
  },1200);
}

async function dosyaCikar(tekId){
  const ids=tekId?[tekId]:[...secili];
  if(!ids.length){tost("Aday seçilmedi.");return;}
  const be=document.getElementById("d-bedel");
  const bedel=be&&be.value?parseInt(be.value):null;
  tost("Dosya üretiliyor…",9000);
  const tgKutu=document.getElementById("d-telegram");
  const tg=tgKutu?tgKutu.checked:false;
  const y=await jpost("/api/dosya-toplu",{ids:ids,bedel:bedel,telegram:tg});
  if(y.hata){tost(y.hata,5000);return;}
  const s=y.sonuc||[];
  let tgNot="";
  (s||[]).forEach(r=>{if(r.telegram){
    if((r.telegram.hata||[]).length)tgNot=" · Telegram: "+r.telegram.hata[0];
    else tgNot=" · Telegram'a gönderildi ("+(r.telegram.gonderilen||[]).length+" parça)";}});
  tost(s.length+" müşteri dosyası hazır."+tgNot,6000);
  const hedef=document.getElementById("d-sonuc");
  if(hedef&&s.length===1){
    const r=s[0];
    const wa=r.wa_numara;
    hedef.innerHTML=`
      <div class="mesaj" style="margin-top:12px">
        <b>${kacir(r.hizmet_ad)}</b> · teklif ${bicim(r.bedel)} ₺
        ${r.deger?`<br><small>müşteriye giden değer ${kacir(r.deger.toplam_tl)} — aradaki fark ${kacir(r.deger.kazanc_tl||"—")} (${r.deger.oran||"—"}x)</small>`:""}
        <br><br>
        <a href="/cikti/${encodeURI(r.analiz)}" target="_blank">analiz.html ↗</a> ·
        <a href="/cikti/${encodeURI(r.teklif)}" target="_blank">teklif.html ↗</a> ·
        <a href="/cikti/${encodeURI(r.is_emri)}" target="_blank">iş emri ↗</a> ·
        <a href="/cikti/${encodeURI(r.mesajlar)}" target="_blank">mesajlar ↗</a>
        ${r.sosyal_demo?` · <a href="/cikti/${encodeURI(r.sosyal_demo)}" target="_blank" style="color:var(--kirmizi)">sosyal demo ↗</a>`:""}
        ${r.cekim_plani?` · <a href="/cikti/${encodeURI(r.cekim_plani)}" target="_blank" style="color:var(--kirmizi)">çekim planı ↗</a>`:""}
        ${r.strateji?` · <a href="/cikti/${encodeURI(r.strateji)}" target="_blank" style="color:var(--kirmizi)"><b>strateji ↗</b></a>`:""}
      </div>
      <div class="blok"><span class="etk">Önerilen kanal: ${kacir((r.kanal||{}).kanal||"?")}</span>
        <p style="color:var(--gri);font-size:13.5px;margin-bottom:10px">${kacir((r.kanal||{}).gerekce||"")}</p>
        ${wa?`<div class="mesaj">${kacir(r.mesaj.whatsapp)}</div>
          <div class="arac" style="margin-top:10px">
            <a class="dug" style="text-decoration:none" href="${r.wa}" target="_blank" onclick="temasOtomatik(${r.id},'whatsapp')">WhatsApp'ta aç</a>
            <button class="dug sade" onclick="kopyala(${JSON.stringify(r.mesaj.whatsapp).replace(/"/g,'&quot;')})">Kopyala</button>
          </div>`:""}
        ${(r.epostalar||[]).length?`<div style="margin-top:14px">
          <span class="etk" style="color:var(--gri)">E-posta · ${kacir(r.epostalar[0])}</span>
          <div class="mesaj" style="margin-top:8px;max-height:220px;overflow:auto">${kacir(r.mesaj.eposta_govde)}</div>
          <div class="arac" style="margin-top:10px">
            <a class="dug" style="text-decoration:none" href="${r.mailto}" onclick="temasOtomatik(${r.id},'eposta')">Mail uygulamasında aç</a>
            <button class="dug sade" onclick="epostaGonder(${r.id},'${kacir(r.epostalar[0])}')">Panelden gönder (SMTP)</button>
            <button class="dug sade" onclick="kopyala(${JSON.stringify(r.mesaj.eposta_govde).replace(/"/g,'&quot;')})">Kopyala</button>
          </div></div>`:""}
        ${!wa&&!(r.epostalar||[]).length?`<div style="margin-top:14px">
          <span class="etk" style="color:var(--sari)">Sadece sabit hat — aranmalı</span>
          <div class="mesaj" style="margin-top:8px">${kacir(r.mesaj.telefon)}</div>
          <div class="arac" style="margin-top:10px">
            <button class="dug sade" onclick="kopyala(${JSON.stringify(r.mesaj.telefon).replace(/"/g,'&quot;')})">Konuşma metnini kopyala</button>
            <button class="dug sade" onclick="temasEt(${r.id})">Aradım, kaydet</button>
          </div></div>`:""}
      </div>`;
  }
  yukle();
}
async function temasOtomatik(id,kanal){
  await jpost("/api/temas",{aday_id:id,kanal:kanal,
    durum:kanal==="whatsapp"?"mesaj atildi":"eposta gonderildi",
    sonraki_adim:"takip mesajı",sonraki_tarih:new Date(Date.now()+3*864e5).toISOString().slice(0,10)});
  setTimeout(yukle,600);
}
async function epostaGonder(id,alici){
  const a=prompt("Alıcı e-posta:",alici||"");if(!a)return;
  tost("Gönderiliyor…",6000);
  const y=await jpost("/api/eposta",{aday_id:id,alici:a});
  tost(y.ok?"E-posta gönderildi.":("Gönderilemedi — "+(y.mesaj||"")),6000);
  yukle();
}
// ---------------------------------------------------------------- gelen talep
function tlPara(n){return (n||0).toLocaleString("tr-TR")+" \u20ba";}
async function talepCoz(kaydet){
  const m=(document.getElementById("tl-metin").value||"").trim();
  if(m.length<15){tost("Mesaj çok kısa.");return;}
  document.getElementById("tl-durum").innerHTML='<span class="gri">Çözümleniyor…</span>';
  const y=await jpost("/api/talep",{metin:m,kaydet:!!kaydet});
  if(y.sorun||y.hata){document.getElementById("tl-durum").innerHTML=
    '<div class="uyari">'+(y.sorun||y.hata)+'</div>';document.getElementById("tl-sonuc").innerHTML="";return;}
  const c=y.cozum, a=c.daraltilmis[0], u=c.daraltilmis[1];
  document.getElementById("tl-durum").innerHTML = y.yol
    ? '<div class="basari">Taslak yazıldı: <code>'+y.yol+'</code></div>' : '';
  document.getElementById("tl-sonuc").innerHTML=`
    <div class="kutular" style="margin-top:14px">
      <div class="kutu"><span class="etk">Eşleşen hizmet</span>
        <b style="font-size:19px;display:block;line-height:1.25">${c.ad}</b>
        <small style="color:var(--gri)">eşleşme güveni: ${c.guven}</small></div>
      <div class="kutu"><span class="etk">Bu talep için</span>
        <b class="buyuk" style="display:block;font-size:24px">${tlPara(a)} – ${tlPara(u)}</b>
        <small style="color:var(--gri)">${c.aylik?"aylık düzen":"proje bedeli"}</small></div>
      <div class="kutu"><span class="etk">Genel bandımız</span>
        <b class="buyuk" style="display:block;font-size:24px">${tlPara(c.band[0])} – ${tlPara(c.band[1])}</b>
        <small style="color:var(--gri)">hizmet sayfasındaki aralık</small></div>
      <div class="kutu"><span class="etk">Süre</span>
        <b class="buyuk" style="display:block;font-size:24px">${c.sure}</b>
        <small style="color:var(--gri)">tipik teslim</small></div>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:16px">
      <div><h4 style="margin:0 0 6px">Fiyatı ne belirledi</h4>
        <ul style="margin:0;padding-left:18px;color:var(--gri);font-size:14px">
          ${(c.gerekce||[]).map(g=>`<li><b style="color:${g.yon==="+"?"var(--kirmizi)":"#7aa87a"}">${g.yon}</b> ${g.aciklama}</li>`).join("")||"<li>Belirgin bir kalem yok — bandın ortası.</li>"}
        </ul>
        <h4 style="margin:14px 0 6px">Müşteri ne kadar hazır</h4>
        <ul style="margin:0;padding-left:18px;color:var(--gri);font-size:14px">
          ${(c.hazirlik||[]).map(x=>`<li>${x}</li>`).join("")||"<li>Belirgin hazırlık işareti yok.</li>"}
        </ul></div>
      <div><h4 style="margin:0 0 6px">Baştan söylenecek sınır</h4>
        <p style="color:var(--gri);font-size:14px;margin:0">${c.sinir}</p>
        <h4 style="margin:14px 0 6px">Önerilecek ilk adım</h4>
        <p style="color:var(--gri);font-size:14px;margin:0"><b>${c.kapi[0]}</b> — ${c.kapi[1]}</p>
        <h4 style="margin:14px 0 6px">Bize gereken bilgiler</h4>
        <ul style="margin:0;padding-left:18px;color:var(--gri);font-size:14px">
          ${(c.gerekli||[]).map(x=>`<li>${x}</li>`).join("")}</ul></div>
    </div>
    <div style="margin-top:18px">
      <h4 style="margin:0 0 6px">WhatsApp yanıtı
        <button class="dug sade" style="margin-left:8px" onclick="kopyala(document.getElementById('tl-kisa').innerText)">Kopyala</button></h4>
      <pre id="tl-kisa" style="white-space:pre-wrap;background:#12100f;border:1px solid #2a2724;
        border-radius:6px;padding:14px;font:inherit;color:var(--bone);margin:0">${(y.kisa||"").replace(/</g,"&lt;")}</pre>
      <h4 style="margin:16px 0 6px">E-posta yanıtı
        <button class="dug sade" style="margin-left:8px" onclick="kopyala(document.getElementById('tl-uzun').innerText)">Kopyala</button></h4>
      <pre id="tl-uzun" style="white-space:pre-wrap;background:#12100f;border:1px solid #2a2724;
        border-radius:6px;padding:14px;font:inherit;color:var(--bone);margin:0">${(y.uzun||"").replace(/</g,"&lt;")}</pre>
    </div>`;
}
function talepKaydet(){return talepCoz(true);}
async function talepHizmetler(){
  const y=await jpost("/api/talep",{liste:true});
  if(!y.liste)return;
  document.getElementById("tl-hizmetler").innerHTML=`<table class="tab"><thead><tr>
    <th>Hizmet</th><th>Band</th><th>Model</th><th>Yayınlanabilir referans</th><th>Sayfa</th></tr></thead><tbody>
    ${y.liste.map(h=>`<tr><td>${h.ad}</td><td>${tlPara(h.band[0])} – ${tlPara(h.band[1])}</td>
      <td>${h.aylik?"aylık":"proje"}</td>
      <td>${h.referansli?"var":'<span style="color:var(--kirmizi)">yok — test/prova öneriliyor</span>'}</td>
      <td><code>${h.sayfa}</code></td></tr>`).join("")}</tbody></table></div>`;
}

// ---------------------------------------------------------------- karargâh
function gitSekme(ad){
  const d=document.querySelector('nav button[data-s="'+ad+'"]');
  if(d) d.click();
}
async function karargahYenile(){
  const k=await jget("/api/karargah"); if(!k||!k.durum)return;
  document.getElementById("kg-zaman").textContent=k.zaman;

  const renk={yesil:"#8fce8f",sari:"#d8a13a",kirmizi:"var(--kirmizi)",gri:"var(--gri)"};
  document.getElementById("kg-durum").innerHTML=k.durum.map(d=>
    `<div class="kutu"><span class="etk">${d.ad}</span>
      <b class="buyuk" style="display:block;font-size:26px;color:${renk[d.renk]||"var(--bone)"}">${d.deger}</b>
      <small style="color:var(--gri)">${d.alt}</small></div>`).join("");

  const u=k.uyari||[];
  document.getElementById("kg-uyari").innerHTML = u.length
    ? u.map(x=>`<div class="kg-u"><span class="kg-nokta kg-${x.onem}"></span><div style="flex:1">
        <b>${x.baslik}</b>
        <div class="sebep">${x.sebep}</div>
        <div class="adim">${x.adim}</div></div>
        ${x.sekme?`<button class="dug sade mini" onclick="gitSekme('${x.sekme}')">Aç</button>`:""}
      </div>`).join("")
    : `<p style="color:#8fce8f;margin:6px 0">Bekleyen bir şey yok. Nadir bir gün.</p>`;

  const bg=k.bugun||[];
  document.getElementById("kg-bugun").innerHTML = bg.length
    ? bg.map(x=>`<div class="kg-is"><div>
        <b>${x.ad}</b>
        <div style="color:var(--gri);font-size:13px">${x["not"]}</div></div>
        <div style="text-align:right;white-space:nowrap">
          ${x.gecikti?'<div class="kg-gec">GECİKTİ</div>':''}
          <div style="color:var(--gri);font-size:12px">${x.tarih||""}</div></div>
      </div>`).join("")
    : `<p style="color:var(--gri);margin:6px 0">Bugün söz verilmiş bir takip yok.</p>`;
}

// ---------------------------------------------------------------- makale
let mkSecili="";
async function makaleListe(){
  const d=await jget("/api/makaleler"); const k=(d&&d.konular)||[];
  document.getElementById("mk-liste").innerHTML = k.map(x=>
    `<div class="mk-s"><div><b>${x.baslik}</b>
      <div class="kel">${x.kelime}</div></div>
      <div style="white-space:nowrap">
      ${x.yayinda?'<span class="rz">yayında</span> ':''}
      <button class="dug sade mini" onclick="makaleOlc('${x.anahtar}')">Üret ve puanla</button>
      </div></div>`).join("") || "<p style='color:var(--gri)'>Konu yok.</p>";
}
async function makaleOlc(a){
  mkSecili=a;
  const kart=document.getElementById("mk-sonuc-kart");
  kart.hidden=false; document.getElementById("mk-karne").innerHTML="Ölçülüyor…";
  document.getElementById("mk-puan").textContent="";
  const o=await jpost("/api/makale-olc",{anahtar:a});
  if(!o||o.hata){document.getElementById("mk-karne").textContent=(o&&o.hata)||"hata";return;}
  document.getElementById("mk-baslik").textContent=o.baslik;
  const p=document.getElementById("mk-puan");
  p.textContent=o.puan+" / 100";
  p.style.color=o.gecti?"#8fce8f":"var(--kirmizi)";
  document.getElementById("mk-metin").textContent=o.metin;
  document.getElementById("mk-karne").innerHTML=
    `<p style="color:var(--gri);font-size:13px;margin:2px 0 10px">${o.kelime_sayisi} kelime</p>`
    + o.maddeler.map(m=>`<div class="mk-m">
        <span class="im ${m.tam?'ok':'yok'}">${m.tam?'✓':'✕'}</span>
        <div style="flex:1"><b>${m.ad}</b> <span class="rz">${m.puan}/${m.agirlik}</span>
          <div class="ne">${m.neden}</div>
          ${m.tam?'':'<div class="ya">'+m.nasil+'</div>'}</div></div>`).join("");
  const d=document.getElementById("mk-yayinla");
  d.disabled=!o.gecti;
  d.textContent=o.gecti?"Yayınla":"Yayınlanamaz — 100 değil";
}
async function makaleYayinla(){
  if(!mkSecili)return;
  const d=document.getElementById("mk-yayinla");
  d.disabled=true; d.textContent="Yayınlanıyor…";
  const r=await jpost("/api/makale-yayinla",{anahtar:mkSecili});
  if(r&&r.hata){ d.textContent="Yayınlanmadı"; alert(r.hata); return; }
  d.textContent="Yayınlandı";
  alert("Yazı siteye basıldı:\n"+(r.url||"")+"\n\nYayına gitmesi için GitHub Desktop → Commit → Push origin.");
  makaleListe(); karargahYenile();
}

// -------------------------------------------------- sayfa başı anlatım kutuları
let ANLATIM=null;
function anlatKutusu(anahtar,d){
  const acik=(function(){try{return localStorage.getItem("pusula_anlat_"+anahtar)!=="kapali";}
                         catch(e){return true;}})();
  return `<details class="anlat" ${acik?"open":""} data-a="${anahtar}">
    <summary>Bu sayfada ne yapıyoruz?</summary>
    <div class="ic">
      <p class="amac">${d.amac}</p>
      <ol>${d.adim.map(x=>`<li>${x}</li>`).join("")}</ol>
      <p class="sonra"><b>Sonra ne oluyor:</b> ${d.sonra}</p>
      ${d.ipucu?`<p class="ipucu">${d.ipucu}</p>`:""}
    </div></details>`;
}
function anlatimlariYerlestir(sayfa){
  if(!sayfa)return;
  Object.keys(sayfa).forEach(function(k){
    const b=document.getElementById("s-"+k);
    if(!b || b.querySelector(".anlat"))return;
    const alt=b.querySelector(".altbaslik")||b.querySelector(".baslik");
    if(!alt)return;
    alt.insertAdjacentHTML("afterend", anlatKutusu(k, sayfa[k]));
  });
  document.querySelectorAll("details.anlat").forEach(function(d){
    d.addEventListener("toggle",function(){
      try{localStorage.setItem("pusula_anlat_"+d.dataset.a, d.open?"acik":"kapali");}catch(e){}
    });
  });
}
async function anlatimYukle(){
  if(ANLATIM)return ANLATIM;
  ANLATIM=await jget("/api/kilavuz");
  anlatimlariYerlestir(ANLATIM.sayfa);
  return ANLATIM;
}

// ---------------------------------------------------------------- uzaktan erişim
async function uzakYukle(){
  const u=await jpost("/api/uzak",{});
  const k=document.getElementById("kl-uzak"); if(!k)return;
  let h="";

  if(!u.uzak_kipi){
    h+=`<div class="uyari" style="margin-bottom:14px">Panel şu an uzaktan erişim kipinde
      değil. Luna Pusula klasöründe <b>Panel-Uzak.command</b> dosyasına çift tıkla,
      sonra buraya dön.</div>`;
  }

  h+=`<div class="kutular" style="margin-bottom:16px">
    <div class="kutu"><span class="etk">Giriş PIN'i</span>
      <b class="buyuk" style="display:block;font-size:26px;letter-spacing:.12em">${u.pin||"—"}</b>
      <small style="color:var(--gri)">eşine bunu söyle — uzun adres yok</small></div>
    <div class="kutu"><span class="etk">cloudflared</span>
      <b style="font-size:18px;display:block">${u.kurulu?"kurulu":"kurulu değil"}</b>
      <small style="color:var(--gri)">${u.surum||"tüneli açan program"}</small></div>
    <div class="kutu"><span class="etk">Tünel</span>
      <b style="font-size:18px;display:block;color:${u.calisiyor?"#8fce8f":"var(--gri)"}">
        ${u.calisiyor?"açık":"kapalı"}</b>
      <small style="color:var(--gri)">${u.calisiyor?"adres aşağıda":"başlatılmadı"}</small></div>
  </div>`;

  if(!u.kurulu){
    h+=`<div class="kart" style="background:#12100f;margin-bottom:16px">
      <b>Önce cloudflared kurulmalı</b>
      <p style="color:var(--gri);font-size:14px;margin:6px 0 10px">
        Terminal'i aç, şunu yapıştır ve Enter'a bas. Bir kez yapılıyor.</p>
      <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
        <code id="kl-brew" style="flex:1;min-width:220px;background:#0d0b0a;border:1px solid #2a2724;
          border-radius:6px;padding:10px">${u.kurulum.brew}</code>
        <button class="dug sade" onclick="kopyala(document.getElementById('kl-brew').innerText)">Kopyala</button>
      </div>
      <span class="kl-not">↳ ${u.kurulum["not"]}</span></div>`;
  }

  if(u.calisiyor && u.adres){
    const wa="https://wa.me/?text="+encodeURIComponent(
      "Luna Pusula paneli:\n"+u.adres+"\n\nAçılan ekrana şu PIN'i gir: "+(u.pin||""));
    h+=`<div class="kart" style="background:#12100f;margin-bottom:16px">
      <span class="etk">Hazır adres</span>
      <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:8px">
        <code id="kl-uzak-adres" style="flex:1;min-width:260px;background:#0d0b0a;
          border:1px solid #2a2724;border-radius:6px;padding:10px;word-break:break-all">${u.adres}</code>
        <button class="dug sade" onclick="kopyala(document.getElementById('kl-uzak-adres').innerText)">Kopyala</button>
      </div>
      <div class="arac" style="margin-top:12px">
        <a class="dug" style="text-decoration:none" href="${wa}" target="_blank">WhatsApp'tan gönder</a>
        <button class="dug sade" onclick="uzakDurdur()">Tüneli kapat</button>
      </div>
      <p style="color:var(--gri);font-size:13px;margin:12px 0 0">
        Bu adres <b>geçici</b>: panel ya da tünel kapanınca ölür, her başlatmada değişir.
        Kalıcı adres için aşağıdaki altı adımı bir kez yap.</p></div>`;
  } else if(u.kurulu){
    h+=`<div class="arac" style="margin-bottom:16px">
      <button class="dug" onclick="uzakBaslat(this)">Tüneli başlat</button>
      <span style="color:var(--gri);font-size:13px;align-self:center">
        Adres birkaç saniyede geliyor.</span></div>`;
  }

  h+=`<details class="anlat" style="border-left-color:#2a2724;margin-top:18px">
    <summary>Kalıcı adres kurulumu — bir kez yapılan adımlar</summary>
    <div class="ic">
    <p style="color:var(--gri);font-size:14px;margin:0 0 14px">
      Kurulum tamamlandıysa buraya bakmana gerek yok. Tüneli her gün açmak için
      Luna Pusula klasöründeki <b>Tunel.command</b> dosyasına çift tıklaman yeterli.
      Aşağıdakiler yeni bir bilgisayarda kurulum gerekirse diye duruyor.</p>
    ${(u.adimlar||[]).map((a,i)=>`
      <div class="kl-adim"><div class="kl-no">${i+1}</div><div style="flex:1">
        <b>${a.baslik}</b>
        ${a.komut?`<div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:6px 0 4px">
          <code id="kl-k${i}" style="flex:1;min-width:240px;background:#12100f;border:1px solid #2a2724;
            border-radius:6px;padding:9px;word-break:break-all">${a.komut}</code>
          <button class="dug sade mini" onclick="kopyala(document.getElementById('kl-k${i}').innerText)">Kopyala</button>
        </div>`:""}
        <span class="kl-not">↳ ${a.aciklama}</span></div></div>`).join("")}
    <div style="background:#12100f;border:1px solid #2a2724;border-radius:8px;padding:14px;margin-top:16px">
      <b>7. Access'te izin verdiğin e-postaları buraya da yaz</b>
      <p style="color:var(--gri);font-size:13.5px;margin:6px 0 10px">
        Panel bunları ikinci kilit olarak kontrol ediyor: Access yanlış yapılandırılırsa
        panel yine de herkese açılmasın diye. Bu liste doluyken ve Access arkasından
        girildiğinde PIN sorulmuyor. Virgülle ayır.</p>
      <div class="arac">
        <input type="text" id="kl-eposta" style="flex:1;min-width:260px"
          placeholder="sen@lunayapim.com, esin@ornek.com"
          value="${(u.epostalar||[]).join(", ")}">
        <button class="dug" onclick="uzakEposta()">Kaydet</button>
      </div>
      <span class="kl-not">↳ Şu an tanımlı: ${(u.epostalar&&u.epostalar.length)?u.epostalar.join(", "):"yok"}</span>
    </div>
  </div></details>`;
  k.innerHTML=h;
}
async function uzakBaslat(d){
  if(d){d.disabled=true;d.textContent="Tünel açılıyor…";}
  const r=await jpost("/api/uzak",{baslat:true});
  if(!r.ok){
    tost(r.sorun||"Tünel açılamadı.");
    if(d){d.disabled=false;d.textContent="Tüneli başlat";}
  }
  uzakYukle();
}
async function uzakDurdur(){ await jpost("/api/uzak",{durdur:true}); uzakYukle(); }
async function uzakEposta(){
  const v=(document.getElementById("kl-eposta").value||"").trim();
  await jpost("/api/uzak",{epostalar:v});
  tost(v?"E-posta listesi kaydedildi.":"Liste boşaltıldı — Access arkasından da PIN sorulacak.");
  uzakYukle();
}

// ---------------------------------------------------------------- kılavuz
function benKimim(){try{return localStorage.getItem("pusula_kullanici")||"";}catch(e){return "";}}
function kimimKaydet(){
  const a=(document.getElementById("kl-ben").value||"").trim();
  try{localStorage.setItem("pusula_kullanici",a);}catch(e){}
  document.getElementById("kl-ben-durum").textContent=a?("Kayıtlar "+a+" adına düşecek."):"İsim boş.";
}
async function kilavuzYukle(){
  const d=await anlatimYukle(); if(!d||!d.sekmeler)return;
  const sr=document.getElementById("kl-surec");
  if(sr) sr.innerHTML=(d.surec||[]).map((x,i)=>
    `<div class="surec-adim"><div class="surec-no">${i+1}</div><div>
       <b>${x.asama}</b> <span class="surec-nerede">${x.nerede}</span>
       <div style="color:var(--gri);font-size:14px;margin-top:3px">${x.metin}</div></div></div>`).join("");
  document.getElementById("kl-ben").value=benKimim();
  if(benKimim())document.getElementById("kl-ben-durum").textContent="Kayıtlar "+benKimim()+" adına düşüyor.";

  document.getElementById("kl-baslangic").innerHTML=d.baslangic.map((x,i)=>
    `<div class="kl-adim"><div class="kl-no">${i+1}</div><div><b>${x.baslik}</b>
     <div style="color:var(--gri);font-size:14px;margin-top:3px">${x.metin}</div>
     <span class="kl-not">↳ ${x["not"]}</span></div></div>`).join("");

  document.getElementById("kl-ritim").innerHTML=d.ritim.map(x=>
    `<div style="margin-bottom:16px"><b style="color:var(--kirmizi)">${x.baslik}</b>
     <ul style="margin:6px 0 0;padding-left:18px;color:var(--gri);font-size:14px">
     ${x.maddeler.map(m=>`<li style="margin-bottom:4px">${m}</li>`).join("")}</ul></div>`).join("");

  document.getElementById("kl-sekmeler").innerHTML=`<table class="tab"><thead><tr>
    <th>Sekme</th><th>Ne yapar</th><th>Ne zaman</th></tr></thead><tbody>
    ${d.sekmeler.map(x=>`<tr><td><b>${x.ad}</b></td><td>${x.ne}</td>
      <td style="color:var(--gri)">${x.ne_zaman}</td></tr>`).join("")}</tbody></table></div>`;

  document.getElementById("kl-sorunlar").innerHTML=d.sorunlar.map(x=>
    `<div style="padding:11px 0;border-top:1px solid #221f1d"><b>${x.baslik}</b>
     <div style="color:var(--gri);font-size:14px;margin-top:3px">${x.cozum}</div></div>`).join("");

  document.getElementById("kl-kural").innerHTML=`<ul style="margin:0;padding-left:18px;
    color:var(--gri);font-size:14px">${d.talep_kurali.map(x=>
    `<li style="margin-bottom:6px"><b style="color:var(--bone)">${x.baslik}</b> — ${x.metin}</li>`).join("")}</ul>`;

  document.getElementById("kl-ornek").innerHTML=d.ornek.map(o=>
    `<div class="kl-ornek"><span class="kl-rozet" style="background:${o.iyi?"#1f3a1f":"#3a1f1f"};
       color:${o.iyi?"#8fce8f":"#e8907c"}">${o.iyi?"BÖYLE YAZ":"BÖYLE YAZMA"}</span>
     <b style="margin-left:8px">${o.baslik}</b>
     <pre>${(o.metin||"").replace(/</g,"&lt;")}</pre>
     <div style="color:var(--gri);font-size:13px;margin-top:8px">↳ ${o.neden}</div></div>`).join("");

  document.getElementById("kl-ilke").innerHTML=d.ilkeler.map(x=>
    `<div style="padding:11px 0;border-top:1px solid #221f1d"><b>${x.baslik}</b>
     <div style="color:var(--gri);font-size:14px;margin-top:3px">${x.metin}</div></div>`).join("");

  const sc=document.getElementById("kl-sekme");
  sc.innerHTML=d.sekmeler.map(x=>`<option>${x.ad}</option>`).join("")+"<option>Genel</option>";

  uzakYukle();
  const a=await jget("/api/ag");
  const kutu=document.getElementById("kl-ag");
  if(!a || !a.acik){
    kutu.innerHTML=`<p style="color:var(--gri);font-size:14px;margin:0">Ağ kipi <b>kapalı</b> —
      panele şu an sadece bu bilgisayardan girilebiliyor. İkinci bilgisayarı bağlamak için
      Luna Pusula klasöründeki <b>Panel-Ag.command</b> dosyasına çift tıkla; bağlantı burada
      ve o pencerede görünür.</p>`;
  } else {
    const ilk=(a.adresler&&a.adresler[0])?a.adresler[0].url:(a.adres||"");
    const wa="https://wa.me/?text="+encodeURIComponent(
      "Luna Pusula paneli — bu bağlantıya tıkla, açılır:\n"+ilk+
      "\n\n(Aynı ev/ofis ağındayken çalışır. Şifre girmene gerek yok.)");
    kutu.innerHTML=
      (a.ag_var?"":`<div class="uyari" style="margin-bottom:12px">Yerel ağ adresi okunamadı —
         bilgisayar ağa bağlı değil gibi görünüyor. Wi-Fi'yi kontrol edip Panel-Ag.command
         penceresini kapatıp yeniden aç.</div>`)+
      `<p style="color:var(--gri);font-size:14px;margin:0 0 12px">Ağ kipi <b style="color:#8fce8f">açık</b>.
        Aşağıdaki bağlantıyı gönder — karşı taraf tıklayınca panel açılır.
        <b>Anahtarı elle girmesine gerek yok</b>, adresin içinde.</p>`+
      (a.adresler||[]).map((x,i)=>
        `<div style="margin-bottom:12px">
           <div class="etk" style="margin-bottom:5px">${x.ad}${i===0?" — bunu gönder":""}</div>
           <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
             <code id="kl-adr-${i}" style="flex:1;min-width:260px;background:#12100f;
               border:1px solid #2a2724;border-radius:6px;padding:10px;
               word-break:break-all">${x.url}</code>
             <button class="dug sade" onclick="kopyala(document.getElementById('kl-adr-${i}').innerText)">Kopyala</button>
           </div>
           <span class="kl-not">↳ ${x["not"]}</span>
         </div>`).join("")+
      `<div class="arac" style="margin-top:14px">
         <a class="dug" style="text-decoration:none" href="${wa}" target="_blank">WhatsApp'tan gönder</a>
         <a class="dug sade" style="text-decoration:none"
            href="mailto:?subject=${encodeURIComponent("Luna Pusula paneli")}&body=${encodeURIComponent("Bu bağlantıya tıkla, panel açılır:\n"+ilk)}">E-posta ile gönder</a>
       </div>
       <p style="color:var(--gri);font-size:13px;margin:12px 0 0">
         Bu adres yalnızca aynı ev/ofis ağı içinden açılır — internetten erişilemez,
         o yüzden bağlantıyı WhatsApp'tan göndermek sakıncalı değil.
         Veritabanı bu bilgisayarda duruyor; diğeri sadece tarayıcıyla bağlanıyor.</p>`;
  }
}
async function talepMetniUret(){
  const v=i=>(document.getElementById(i).value||"").trim();
  if(!v("kl-baslik")&&!v("kl-olan")){tost("En azından başlığı ve ne olduğunu yaz.");return;}
  const y=await jpost("/api/talep-metni",{sekme:v("kl-sekme"),baslik:v("kl-baslik"),
    niyet:v("kl-niyet"),beklenen:v("kl-beklenen"),olan:v("kl-olan"),hata:v("kl-hata"),
    aciliyet:v("kl-aciliyet"),kim:benKimim()});
  document.getElementById("kl-metin-kutu").innerHTML=
    `<div class="basari" style="margin-bottom:10px">Metin hazır — kopyalayıp Claude'a yapıştır.</div>
     <pre id="kl-metin" style="white-space:pre-wrap;background:#12100f;border:1px solid #2a2724;
       border-radius:6px;padding:14px;font:inherit;color:var(--bone);margin:0">${(y.metin||"").replace(/</g,"&lt;")}</pre>
     <button class="dug" style="margin-top:10px"
       onclick="kopyala(document.getElementById('kl-metin').innerText)">Kopyala</button>`;
}

function kopyala(m){navigator.clipboard.writeText(m).then(()=>tost("Kopyalandı."));}
async function dosyaAc(id){
  const a=V.adaylar.find(x=>x.id===id);
  window.open("/cikti/musteri/"+id+"-"+slug(a.ad)+"/analiz.html","_blank");
}
function slug(x){return (x||"").normalize("NFKD").replace(/[̀-ͯ]/g,"")
  .toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/-{2,}/g,"-").replace(/^-|-$/g,"").slice(0,48)||"musteri";}
async function waAc(id){
  const y=await jpost("/api/dosya",{aday_id:id});
  const r=(y.sonuc||[])[0];
  if(!r){tost("Dosya üretilemedi.");return;}
  if(!r.wa_numara){tost("Cep hattı yok — mesaj kopyalandı, e-posta yolunu kullan.");kopyala(r.mesaj.whatsapp);return;}
  window.open(r.wa,"_blank");
  await temasOtomatik(id,"whatsapp");
}
async function temasEt(id){
  const kanal=prompt("Kanal (whatsapp / telefon / eposta / ziyaret):","telefon");if(!kanal)return;
  const durum=prompt("Sonuç:\nmesaj atildi / arandi ulasilamadi / arandi gorusuldu / gorusuldu /\nteklif verildi / ilgilenmiyor / uygun degil / kazanildi","arandi gorusuldu");if(!durum)return;
  const kisi=prompt("Kiminle konuşuldu? (boş geçilebilir)","")||null;
  const notu=prompt("Not (boş geçilebilir)","")||null;
  const tarih=prompt("Sonraki takip tarihi (YYYY-AA-GG, boş geçilebilir)",
    new Date(Date.now()+3*864e5).toISOString().slice(0,10))||null;
  await jpost("/api/temas",{aday_id:id,kanal:kanal,durum:durum,kisi:kisi,not:notu,
    sonraki_adim:tarih?"takip":null,sonraki_tarih:tarih});
  yukle();tost("Temas kaydedildi.");
}
async function topluTemas(){
  const kanal=prompt("Kanal:","whatsapp");if(!kanal)return;
  const durum=prompt("Sonuç:","mesaj atildi");if(!durum)return;
  const tarih=prompt("Sonraki takip tarihi (YYYY-AA-GG)",
    new Date(Date.now()+3*864e5).toISOString().slice(0,10))||null;
  await jpost("/api/temas",{ids:[...secili],kanal:kanal,durum:durum,
    sonraki_adim:tarih?"takip":null,sonraki_tarih:tarih});
  secimTemizle();yukle();tost("Temas kayıtları düşüldü.");
}

async function arastir(){
  const ids=[...secili];
  if(!ids.length){tost("Aday seçilmedi.");return;}
  const y=await jpost("/api/zenginlestir",{ids:ids});
  if(y.hata){tost(y.hata,5000);return;}
  aktifGorev=y.gorev;logIndex=0;
  document.getElementById("t-konsol").textContent="";
  document.getElementById("t-ilerleme").style.display="block";
  document.querySelector('nav button[data-s="karargah"]').click();
  okumaYukle(false);
  karargahYenile();
  ilkAcilisIsim();
  anlatimYukle();
  lamba(true);izle();
}
async function topluDurum(){
  const d=prompt("Yeni durum ("+(V.durumlar||[]).join(" / ")+"):","temas");
  if(!d)return;
  await jpost("/api/durum",{ids:[...secili],durum:d});
  secimTemizle();yukle();tost("Durum güncellendi.");
}

/* ---------------- RAF ---------------- */
function cizRaf(){
  const t=V.takip||[];
  document.getElementById("takip-govde").innerHTML=t.length?t.map(x=>
    `<tr><td><b>${kacir(x.firma)}</b></td><td>${kacir(x.sehir||"—")}</td>
     <td><small>${kacir(x.kanal||"")} · ${kacir(x.durum||"")}</small></td>
     <td>${kacir(x.sonraki_adim||"—")}</td>
     <td><span class="rz sicak">${kacir(x.sonraki_tarih||"")}</span></td>
     <td><button class="dug sade mini" onclick="adayAc(${x.aday_id})">aç</button></td></tr>`).join("")
    :`<tr><td colspan="6" class="bos">Bugün takip edilecek kimse yok.</td></tr>`;

  const say={};(V.adaylar||[]).forEach(a=>{say[a.durum]=(say[a.durum]||0)+1;});
  document.getElementById("raf-pano").innerHTML=(V.durumlar||[]).map(d=>{
    const l=(V.adaylar||[]).filter(a=>a.durum===d);
    const ciro=l.reduce((s,a)=>s+(a.ek_gelir||0),0);
    return `<div class="sut"><span class="etk">${kacir((V.durum_ad||{})[d]||d)}<span>${l.length}</span></span>
      ${ciro?`<div style="font-family:'Space Mono',monospace;font-size:11px;color:var(--kirmizi);margin-bottom:8px">${bicim(ciro)} ₺</div>`:""}
      ${l.slice(0,12).map(a=>`<div class="is" style="cursor:pointer" onclick="adayAc(${a.id})">
        <b>${kacir(a.ad)}</b><small>${kacir(a.sehir)} · skor ${a.skor}</small></div>`).join("")||'<small style="color:var(--gri)">—</small>'}
      ${l.length>12?`<small style="color:var(--gri)">+${l.length-12} tane daha</small>`:""}</div>`;}).join("");

  const g=V.temaslar||[];
  document.getElementById("temas-govde").innerHTML=g.length?g.map(x=>
    `<tr><td><small>${kacir((x.tarih||"").slice(0,16))}</small></td><td>${kacir(x.firma)}</td>
     <td><small>${x.yon==="gelen"?"← gelen":"→ giden"}</small></td>
     <td><small>${kacir(x.kanal||"")}</small></td><td>${kacir(x.durum||"")}</td>
     <td><small>${kacir(x.kisi||"—")}</small></td>
     <td><small>${kacir(x.kullanici||"—")}</small></td>
     <td><small>${kacir(x.not_||"—")}</small></td></tr>`).join("")
    :`<tr><td colspan="8" class="bos">Henüz temas kaydı yok.</td></tr>`;
}

/* ---------------- PİYASA ---------------- */
let PZ=null;
async function piyasaYukle(){
  const s=document.getElementById("p-sehir").value;
  PZ=await jget("/api/piyasa"+(s?("?sehir="+encodeURIComponent(s)):""));
  document.getElementById("p-derleme").textContent="derleme: "+PZ.derleme;
  const r=PZ.referans;
  document.getElementById("piyasa-liste").innerHTML=Object.entries(r).map(([k,v])=>`
    <div style="border:1px solid var(--cizgi);border-radius:4px;padding:20px;margin-bottom:14px">
      <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;align-items:baseline">
        <h3 style="font-size:19px">${kacir(v.ad)}</h3>
        <div style="font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:22px">
          ${bicim(v.alt)} – ${bicim(v.ust)} ₺ <small style="font-size:12px;color:var(--gri)">/ ${kacir(v.birim)}</small></div>
      </div>
      <div style="font-size:13px;color:var(--gri);margin-top:4px">
        orta nokta ${bicim(v.orta)} ₺ · şehir çarpanı ${v.carpan}
        ${v.kendi_veri?` · <span style="color:var(--yesil)">senin kaydın: ${v.kendi_veri.adet} teklif, ortalama ${bicim(v.kendi_veri.ortalama)} ₺</span>`:""}</div>
      <table style="margin-top:12px"><tr><th>Referans kalem</th><th class="sag">Piyasa</th><th>Kaynak</th></tr>
        ${v.kalemler.map(k2=>`<tr><td>${kacir(k2[0])}</td><td style="text-align:right;white-space:nowrap">${kacir(k2[1])}</td><td><small>${kacir(k2[2])}</small></td></tr>`).join("")}</table></div>
      <p style="font-size:13px;color:var(--gri);margin-top:10px">${kacir(v.not)}</p>
    </div>`).join("");
  document.getElementById("rakip-govde").innerHTML=(PZ.rakip||[]).length?PZ.rakip.map(x=>
    `<tr><td><small>${kacir((x.tarih||"").slice(0,10))}</small></td>
     <td>${kacir((V.hizmetler[x.hizmet]||{}).ad||x.hizmet)}</td><td>${kacir(x.sehir||"—")}</td>
     <td>${bicim(x.tutar)} ₺</td><td><small>${kacir(x.kaynak||"—")}</small></td></tr>`).join("")
    :`<tr><td colspan="5" class="bos">Henüz rakip teklif kaydı yok. Duyduğun her rakamı buraya girersen ortalama gerçeğe yaklaşır.</td></tr>`;
  document.getElementById("piyasa-kaynak").innerHTML=(PZ.kaynaklar||[]).map(k2=>
    `<li style="padding:5px 0"><a href="${k2[1]}" target="_blank">${kacir(k2[0])} ↗</a></li>`).join("");
}
async function rakipEkle(){
  const t=parseFloat(document.getElementById("r-tutar").value);
  if(!t){tost("Tutar gerekli.");return;}
  await jpost("/api/rakip-teklif",{hizmet:document.getElementById("r-hizmet").value,
    tutar:t,sehir:document.getElementById("r-sehir").value,
    kaynak:document.getElementById("r-kaynak").value});
  document.getElementById("r-tutar").value="";document.getElementById("r-kaynak").value="";
  piyasaYukle();tost("Kaydedildi — ortalama güncellendi.");
}

/* ---------------- HUNİ / ÜRETİM / İSTATİSTİK ---------------- */
function cizHuni(){
  const i=V.istatistik,adim=[["Bulunan aday",i.aday],["Denetlenen",i.denetlenen],["Demo üretilen",i.demo],
    ["Temas kurulan",i.temas],["Açılan iş",i.is],["Kazanılan iş",i.kazanilan]];
  const enb=Math.max(...adim.map(a=>a[1]),1);
  document.getElementById("huni").innerHTML=adim.map((a,n)=>{
    const onc=n?adim[n-1][1]:a[1],oran=onc?Math.round(100*a[1]/onc):100;
    return `<div class="hbas"><b>${a[0]}</b><span>${bicim(a[1])}${n?` <small>· bir öncekinin %${oran}'i</small>`:""}</span></div>
    <div class="hcubuk"><i style="width:${Math.max(2,100*a[1]/enb)}%">${a[1]||""}</i></div>`;}).join("");
}
function cizPano(){
  document.getElementById("pano").innerHTML=V.asamalar.map(as=>{
    const l=V.isler.filter(i=>i.asama===as),top=l.reduce((t,i)=>t+(i.bedel||0),0);
    return `<div class="sut"><span class="etk">${kacir(V.asama_ad[as]||as)}<span>${l.length}</span></span>
      ${top?`<div style="font-family:'Space Mono',monospace;font-size:11px;color:var(--kirmizi);margin-bottom:8px">${bicim(top)} ₺</div>`:""}
      ${l.map(i=>`<div class="is"><b>${kacir(i.musteri)}</b>
        <small>${kacir(V.hizmetler[i.hizmet]?V.hizmetler[i.hizmet].ad:i.hizmet)}</small>
        <small>${i.bedel?bicim(i.bedel)+" ₺":""}${i.teslim_tarihi?" · "+kacir(i.teslim_tarihi):""}</small>
        <div class="tas"><button onclick="tasi(${i.id},-1)">←</button><button onclick="tasi(${i.id},1)">→</button></div>
      </div>`).join("")||'<small style="color:var(--gri)">—</small>'}</div>`;}).join("");
}
async function tasi(id,yon){
  const i=V.isler.find(x=>x.id===id);if(!i)return;
  let n=Math.max(0,Math.min(V.asamalar.length-1,V.asamalar.indexOf(i.asama)+yon));
  await jpost("/api/is-asama",{id:id,asama:V.asamalar[n]});yukle();
}
async function isEkle(){
  const m=document.getElementById("i-musteri").value.trim();
  if(!m){tost("Müşteri adı gerekli.");return;}
  await jpost("/api/is",{musteri:m,hizmet:document.getElementById("i-hizmet").value,
    sehir:document.getElementById("i-sehir").value,
    bedel:parseFloat(document.getElementById("i-bedel").value)||null,
    teslim:document.getElementById("i-teslim").value||null});
  document.getElementById("i-musteri").value="";document.getElementById("i-bedel").value="";
  yukle();tost("İş eklendi.");
}
function cizIstatistik(){
  const i=V.istatistik;
  document.getElementById("ist-kutular").innerHTML=[["Aday","aday"],["Denetlenen","denetlenen"],
    ["Demo","demo"],["Temas","temas"],["Açık iş","is"],["Kazanılan","kazanilan"]].map(k=>
    `<div class="kutu"><span class="etk">${k[0]}</span><div class="buyuk">${bicim(i[k[1]])}</div></div>`).join("")
    +`<div class="kutu"><span class="etk">Kazanılan ciro</span><div class="buyuk">${bicim(i.ciro)} ₺</div></div>`
    +`<div class="kutu"><span class="etk">Açık ciro</span><div class="buyuk">${bicim(i.acik_ciro)} ₺</div></div>`;
  const cub=(el,veri,ad,deg)=>{const enb=Math.max(...veri.map(v=>v[deg]),1);
    document.getElementById(el).innerHTML=veri.length?veri.map(v=>
      `<div class="cbar"><span>${kacir(v[ad]||"—")}</span><div class="c"><i style="width:${100*v[deg]/enb}%"></i></div><span>${v[deg]}</span></div>`).join("")
      :'<p class="bos">Veri yok</p>';};
  cub("ist-sehir",i.sehirler||[],"sehir","adet");
  cub("ist-sektor",i.sektorler||[],"sektor","adet");
  cub("ist-skor",i.skor_dagilim||[],"kusak","adet");
  cub("ist-asama",(i.asamalar||[]).map(a=>({asama:V.asama_ad[a.asama]||a.asama,adet:a.adet})),"asama","adet");
}
async function arsivCikar(){
  const y=await jpost("/api/arsiv",{});
  document.getElementById("arsiv-sonuc").innerHTML=
    `hazır: <a href="/cikti/${encodeURI(y.rel)}" target="_blank">${kacir(y.rel)} ↗</a>`;
  tost("Arşiv üretildi.");
}

/* ---------------- AYARLAR ---------------- */
async function ayarYukle(){
  AY=await jget("/api/ayarlar");
  const s=(id,v)=>{const e=document.getElementById(id);if(e)e.value=(v===null||v===undefined)?"":v;};
  s("a-google",AY.google_anahtar);s("a-pagespeed",AY.pagespeed_anahtar);
  s("a-imza",AY.imza);s("a-eposta",AY.eposta);
  s("a-smtp-sunucu",AY.smtp.sunucu);s("a-smtp-kapi",AY.smtp.kapi);
  s("a-smtp-kullanici",AY.smtp.kullanici);s("a-smtp-sifre",AY.smtp.sifre);
  var tg=AY.telegram||{};s("a-tg-jeton",tg.jeton||"");s("a-tg-sohbet",tg.sohbet||"");
  s("a-okuma-anahtar",AY.okuma_anahtar||"");s("a-runway",AY.runway_anahtar||"");s("a-yazar-anahtar",AY.yazar_anahtar||"");s("a-yazar-model",AY.yazar_model||"");
  var ss=document.getElementById("a-tg-sessiz");if(ss)ss.value=tg.sessiz?"1":"0";
  s("a-sicak",AY.esik.sicak_skor);s("a-foto",AY.esik.gorsel_az);
  s("a-yorum",AY.esik.yorum_az);s("a-puan",AY.esik.puan_dusuk);
  s("a-d1",(AY.model.donusum_mevcut*100).toFixed(1));
  s("a-d2",(AY.model.donusum_iyilesmis*100).toFixed(1));
  s("a-d3",(AY.model.kapanis_orani*100).toFixed(1));
  s("a-tavan",AY.model.carpan_tavani);
  const y=(id,v)=>{const e=document.getElementById(id);if(e)e.textContent=v||"—";};
  y("a-vt",AY.vt_yolu);y("a-cikti",AY.cikti);y("a-ayardosya",AY.ayar_dosyasi);
  document.getElementById("a-ois").innerHTML=Object.entries(AY.model.ortalama_is).map(([k,v])=>
    `<div class="alan"><label>${kacir((V.sektorler.find(x=>x.anahtar===k)||{}).ad||k)}</label>
     <input type="number" data-ois="${k}" value="${v}"></div>`).join("");
}
async function anahtarTest(){
  const e=document.getElementById("anahtar-sonuc");
  e.textContent="test ediliyor…";e.style.color="var(--gri)";
  const y=await jpost("/api/anahtar-test",{});
  if(y.ok){
    e.style.color="var(--yesil)";
    e.innerHTML="✓ "+kacir(y.mesaj)+(y.ornek&&y.ornek.length?
      ' <small>· örnek: '+kacir(y.ornek[0].ad)+' ('+(y.ornek[0].yorum||0)+' yorum)</small>':'');
  }else{
    e.style.color="var(--kirmizi)";
    e.innerHTML="✕ "+kacir(y.mesaj)+(y.detay?'<br><small>'+kacir(y.detay.slice(0,220))+'</small>':'');
  }
}
async function olcumOku(){
  const d=await jpost("/api/olcum",{});
  document.getElementById("a-ga4").value=d.ga4||"";
  document.getElementById("a-cf").value=d.cloudflare||"";
  document.getElementById("olcum-sonuc").textContent =
    d.var ? ((d.ga4||d.cloudflare) ? "ölçüm kurulu" : "henüz boş") : "assets/olcum.js bulunamadı";
}
async function olcumKaydet(){
  const c=document.getElementById("olcum-sonuc");
  c.textContent="kaydediliyor…";
  const d=await jpost("/api/olcum",{kaydet:true,
    ga4:document.getElementById("a-ga4").value,
    cloudflare:document.getElementById("a-cf").value});
  if(d.hata){c.style.color="var(--kirmizi)";c.textContent=d.hata;return;}
  c.style.color="var(--yesil)";
  c.textContent=d.not+((d.uyari||[]).length?" · "+d.uyari.join(" "):"");
}

async function okumaYukle(sina){
  const oz=document.getElementById("ok-ozet"), gr=document.getElementById("ok-grafik"),
        sp=document.getElementById("ok-sayfa"), sn=document.getElementById("ok-sina");
  if(sina){ await ayarKaydet(true); if(sn) sn.textContent="Sınanıyor…"; }
  const d=await jget("/api/okuma");
  if(d.hata){
    if(oz) oz.innerHTML='<div class="k" style="grid-column:1/-1;color:var(--gri)">'+kacir(d.hata)+'</div>';
    if(sn) sn.innerHTML='<b style="color:#c00">✕ </b>'+kacir(d.hata); return;}
  const g=(d.gunler||[]); const bugun=g[0]?g[0].okuma:0;
  const y7=g.slice(0,7).reduce((a,b)=>a+b.okuma,0), y30=g.reduce((a,b)=>a+b.okuma,0);
  if(oz) oz.innerHTML=`<div class="k"><span>Bugün</span><b>${bugun}</b></div>
    <div class="k"><span>Son 7 gün</span><b>${y7}</b></div>
    <div class="k"><span>Son 30 gün</span><b>${y30}</b></div>
    <div class="k"><span>Günlük ort. (30)</span><b>${(y30/Math.max(1,g.length)).toFixed(1)}</b></div>`;
  const en=Math.max(1,...g.map(x=>x.okuma));
  if(gr) gr.innerHTML='<div style="display:flex;gap:3px;align-items:flex-end;height:64px">'+
    g.slice().reverse().map(x=>`<div title="${x.gun}: ${x.okuma}" style="flex:1;background:${x.okuma?'var(--kirmizi)':'var(--cizgi)'};height:${Math.max(2,Math.round(62*x.okuma/en))}px;border-radius:2px 2px 0 0"></div>`).join("")+'</div>';
  if(sp){
    const s1=(d.sayfa||[]).slice(0,10).map(x=>`<tr><td>${kacir(x.ad)}</td><td class="sag">${x.n}</td></tr>`).join("");
    const s2=(d.kaynak||[]).slice(0,6).map(x=>`<tr><td>${kacir(x.ad)}</td><td class="sag">${x.n}</td></tr>`).join("");
    sp.innerHTML=`<div class="ikili"><div><span class="etk">En çok okunan (7 gün)</span><table>${s1||'<tr><td style="color:var(--gri)">henüz veri yok</td></tr>'}</table></div>
      <div><span class="etk">Nereden geldiler (7 gün)</span><table>${s2||'<tr><td style="color:var(--gri)">henüz veri yok</td></tr>'}</table></div></div>`;}
  if(sn) sn.innerHTML='<b style="color:#1a7f37">✓ </b>Sayaç bağlı — bugün '+bugun+' okuma.';
}
async function tgSina(){
  const k=document.getElementById("tg-sonuc");
  if(k)k.textContent="Sınanıyor…";
  await ayarKaydet(true);
  const y=await jpost("/api/telgraf-sina",{});
  if(k)k.innerHTML=(y.ok?"<b style=\'color:#1a7f37\'>✓ </b>":"<b style=\'color:#c00\'>✕ </b>")+kacir(y.mesaj||"");
}
async function ayarKaydet(sessiz){
  const g=id=>document.getElementById(id).value;
  const ois={};document.querySelectorAll("[data-ois]").forEach(e=>ois[e.dataset.ois]=parseInt(e.value)||0);
  const y=await jpost("/api/ayarlar",{
    google_anahtar:g("a-google"),pagespeed_anahtar:g("a-pagespeed"),
    imza:g("a-imza"),eposta:g("a-eposta"),
    smtp:{sunucu:g("a-smtp-sunucu"),kapi:parseInt(g("a-smtp-kapi"))||587,
          kullanici:g("a-smtp-kullanici"),sifre:g("a-smtp-sifre")},
    okuma_anahtar:g("a-okuma-anahtar"),runway_anahtar:g("a-runway"),yazar_anahtar:g("a-yazar-anahtar"),yazar_model:g("a-yazar-model"),
    telegram:{jeton:g("a-tg-jeton"),sohbet:g("a-tg-sohbet"),
              sessiz:(document.getElementById("a-tg-sessiz")||{}).value==="1"},
    esik:{sicak_skor:parseInt(g("a-sicak")),gorsel_az:parseInt(g("a-foto")),
          yorum_az:parseInt(g("a-yorum")),puan_dusuk:parseFloat(g("a-puan"))},
    model:{donusum_mevcut:parseFloat(g("a-d1"))/100,donusum_iyilesmis:parseFloat(g("a-d2"))/100,
           kapanis_orani:parseFloat(g("a-d3"))/100,carpan_tavani:parseFloat(g("a-tavan")),
           ortalama_is:ois}});
  AY=y;
  document.getElementById("ayar-sonuc").textContent="kaydedildi · kaynak: "+y.kaynak;
  if(!sessiz){tost("Ayarlar kaydedildi.");yukle();}
}

/* ---------------- gezinme ---------------- */
document.querySelectorAll("nav button").forEach(b=>b.addEventListener("click",()=>{
  if(b.dataset.s==="talep" && !document.getElementById("tl-hizmetler").innerHTML) talepHizmetler();
  if(b.dataset.s==="kilavuz" && !document.getElementById("kl-sekmeler").innerHTML) kilavuzYukle();
  if(b.dataset.s==="karargah") karargahYenile();
  if(b.dataset.s==="makale" && !mkSecili) makaleListe();
  document.querySelectorAll("nav button").forEach(x=>x.classList.remove("aktif"));
  document.querySelectorAll(".sayfa").forEach(x=>x.classList.remove("aktif"));
  b.classList.add("aktif");document.getElementById("s-"+b.dataset.s).classList.add("aktif");
  if(b.dataset.s==="ayarlar"){ayarYukle();olcumOku();}
  if(b.dataset.s==="piyasa")piyasaYukle();
  if(b.dataset.s==="gundem"){depoDurum();inDurum();taslakListe();}
  if(b.dataset.s==="sorgu")sgYukle();
}));
yukle().then(()=>{tarayiciDoldur();});
setInterval(()=>{if(!aktifGorev)jget("/api/veri").then(v=>{V.gorevler=v.gorevler;lamba(v.mesgul);cizGorevler();});},6000);

/* ---------------- Arama Gündemi ---------------- */
function sgYaz(k, s){ var e = document.getElementById(k); if(e) e.innerHTML = s; }
function sgKac(x){ return String(x==null?"":x).replace(/&/g,"&amp;").replace(/</g,"&lt;"); }

function sgYukle(){
  fetch("/api/sorgular").then(r=>r.json()).then(function(d){
    var p = d.paket || {};
    document.getElementById("sg-zaman").textContent =
      p.tarih ? ("son derleme: " + p.tarih + " · " + (p.adet||0) + " sorgu") : "henüz derlenmedi";

    var o = d.oneri || [];
    sgYaz("sg-oneri", o.length ? ("<table class='tbl'><thead><tr><th>Sorgu</th>"+
      "<th>Hizmet</th><th>Puan</th></tr></thead><tbody>" +
      o.map(function(s){ return "<tr><td><b>"+sgKac(s.sorgu)+"</b></td><td>"+
        sgKac(s.etiket)+"</td><td>"+s.puan+"</td></tr>"; }).join("") +
      "</tbody></table></div><p class='ipucu'>Bunların sitede karşılığı yok. Yazıya "+
      "dönüştürmek için Makale sekmesine geç.</p>")
      : "<p class='ipucu'>Önce derle.</p>");

    var l = (p.sorgular || []).slice(0, 60);
    sgYaz("sg-liste", l.length ? ("<table class='tbl'><thead><tr><th>#</th><th>Sorgu</th>"+
      "<th>Hizmet</th><th>Kaynak</th><th>Sıra</th><th>Puan</th></tr></thead><tbody>" +
      l.map(function(s,i){ return "<tr><td>"+(i+1)+"</td><td>"+sgKac(s.sorgu)+"</td><td>"+
        sgKac(s.etiket)+"</td><td>"+sgKac(s.kaynak)+"</td><td>"+
        (s.kaynak==="trend" ? "—" : (s.sira+1))+"</td><td>"+s.puan+"</td></tr>"; }).join("") +
      "</tbody></table></div>") : "<p class='ipucu'>Önce derle.</p>");

    if(p.hata && p.hata.length)
      document.getElementById("sg-durum").textContent = "uyarı: " + p.hata.join(" · ");
  }).catch(function(){ sgYaz("sg-liste","<p class='ipucu'>Liste alınamadı.</p>"); });
}

function sgDerle(){
  var d = document.getElementById("sg-durum");
  d.textContent = "derleniyor… (bir iki dakika sürebilir)";
  fetch("/api/sorgu-derle", {method:"POST", headers:{"Content-Type":"application/json"}, body:"{}"})
    .then(r=>r.json()).then(function(x){
      d.textContent = x.hata ? ("HATA: " + x.hata) : (x.adet + " sorgu derlendi · " + x.tarih);
      sgYukle();
    }).catch(function(){ d.textContent = "HATA: istek gitmedi."; });
}

function sgYayinla(){
  var d = document.getElementById("sg-durum");
  d.textContent = "sayfa basılıyor…";
  fetch("/api/yz-yayinla", {method:"POST", headers:{"Content-Type":"application/json"}, body:"{}"})
    .then(r=>r.json()).then(function(x){
      d.textContent = x.hata ? ("HATA: " + x.hata)
        : ("yapay-zeka/index.html yenilendi (" + x.adet + " sorgu). GitHub Desktop → Commit → Push.");
    }).catch(function(){ d.textContent = "HATA: istek gitmedi."; });
}

function sgTest(){
  sgYaz("sg-test", "<p class='ipucu'>Sınanıyor…</p>");
  fetch("/api/sorgu-test", {method:"POST", headers:{"Content-Type":"application/json"}, body:"{}"})
    .then(r=>r.json()).then(function(x){
      if(x.hata){ sgYaz("sg-test", "<p class='ipucu'>HATA: "+sgKac(x.hata)+"</p>"); return; }
      sgYaz("sg-test", "<table class='tbl'><thead><tr><th>Kaynak</th><th>Sonuç</th>"+
        "<th>Örnek</th></tr></thead><tbody>" + x.sonuc.map(function(s){
          return "<tr><td>"+sgKac(s.kaynak)+"</td><td>"+(s.adet? s.adet+" kayıt":"<b>cevap yok</b>")+
                 "</td><td>"+sgKac((s.ornek||[]).join(" · "))+"</td></tr>"; }).join("") +
        "</tbody></table></div>");
    });
}

</script>
<div id="pa" class="pa">
  <button class="pa-dug" id="pa-dug" aria-expanded="false" aria-controls="pa-kutu">◆ Pusula Asistan</button>
  <div class="pa-kutu" id="pa-kutu" hidden role="dialog" aria-label="Pusula Asistan">
    <div class="pa-bas"><b>Pusula Asistan</b><span>veritabanı · karargâh · kılavuz</span>
      <button class="pa-kapa" id="pa-kapa" aria-label="Kapat">&times;</button></div>
    <div class="pa-govde" id="pa-govde"></div>
    <form class="pa-alt" id="pa-form" autocomplete="off">
      <input id="pa-giris" type="text" placeholder="kaç aday var · sıcak adaylar · [firma] için teklif üret · gündemi tara" maxlength="160">
      <button type="submit">→</button></form>
  </div>
</div>
<style>
.pa{position:fixed;right:18px;bottom:18px;z-index:200;font-family:inherit}
.pa-dug{background:var(--kirmizi);color:#fff;border:0;border-radius:999px;padding:11px 16px;font:inherit;font-weight:700;cursor:pointer;box-shadow:0 10px 28px rgba(0,0,0,.35)}
.pa-kutu{position:absolute;right:0;bottom:52px;width:min(420px,calc(100vw - 36px));max-height:min(560px,calc(100vh - 110px));display:flex;flex-direction:column;background:var(--ink-2,#131317);border:1px solid var(--cizgi);border-radius:14px;overflow:hidden;box-shadow:0 24px 60px rgba(0,0,0,.5)}
.pa-kutu[hidden]{display:none!important}
.pa-bas{display:flex;gap:10px;align-items:baseline;padding:12px 14px;border-bottom:1px solid var(--cizgi)}
.pa-bas span{font-size:11px;color:var(--gri);letter-spacing:.08em;text-transform:uppercase}
.pa-kapa{margin-left:auto;background:none;border:0;color:var(--gri);font-size:20px;cursor:pointer}
.pa-govde{padding:12px 14px;overflow:auto;flex:1;font-size:13.5px;line-height:1.6}
.pa-ben{background:var(--kirmizi);color:#fff;padding:7px 11px;border-radius:10px 10px 3px 10px;margin:0 0 10px auto;width:fit-content;max-width:88%}
.pa-c{border:1px solid var(--cizgi);border-radius:10px 10px 10px 3px;padding:10px 12px;margin-bottom:10px;background:rgba(255,255,255,.03)}
.pa-c .dug{margin-top:8px}
.pa-alt{display:flex;gap:8px;padding:10px 12px;border-top:1px solid var(--cizgi)}
.pa-alt input{flex:1;min-width:0;padding:9px 11px;border-radius:8px;border:1px solid var(--cizgi);background:rgba(255,255,255,.05);color:inherit;font:inherit}
.pa-alt button{background:var(--kirmizi);color:#fff;border:0;border-radius:8px;width:40px;font-size:18px;cursor:pointer}
</style>
<script>
(function(){
  const dug=document.getElementById("pa-dug"), kutu=document.getElementById("pa-kutu"),
        gov=document.getElementById("pa-govde"), giris=document.getElementById("pa-giris");
  let acik=false;
  function ac(){acik=true;kutu.hidden=false;dug.setAttribute("aria-expanded","true");
    if(!gov.innerHTML) gov.innerHTML='<div class="pa-c">Merhaba. Veritabanı, karargâh ve kılavuzdan cevap veriyorum; teklif üretme ve gündem tarama gibi işleri de başlatabilirim — ama her zaman önce sorarım.</div>';
    setTimeout(()=>giris.focus(),50);}
  function kapat(){acik=false;kutu.hidden=true;dug.setAttribute("aria-expanded","false");}
  dug.addEventListener("click",()=>acik?kapat():ac());
  document.getElementById("pa-kapa").addEventListener("click",kapat);
  document.addEventListener("keydown",e=>{if(e.key==="Escape"&&acik)kapat();});
  document.getElementById("pa-form").addEventListener("submit",async e=>{
    e.preventDefault(); const q=giris.value.trim(); if(!q) return; giris.value="";
    gov.insertAdjacentHTML("beforeend",'<div class="pa-ben">'+kacir(q)+'</div><div class="pa-c" id="pa-bekle">Bakıyorum…</div>');
    gov.scrollTop=gov.scrollHeight;
    const r=await jpost("/api/asistan",{soru:q});
    const b=document.getElementById("pa-bekle"); b.removeAttribute("id");
    let h=r.cevap||"Bir şey ters gitti.";
    if(r.eylem){ const ey=r.eylem;
      h+='<br><button class="dug" onclick="paEylem('+JSON.stringify(ey).replace(/"/g,"&quot;")+',this)">'+kacir(ey.etiket||"Yap")+'</button>'; }
    b.innerHTML=h; gov.scrollTop=gov.scrollHeight;
  });
  window.paEylem=async function(ey,btn){
    btn.disabled=true; btn.textContent="Çalışıyor…";
    try{
      if(ey.tur==="dosya"){ const y=await jpost("/api/dosya",{aday_id:ey.aday_id,telegram:true}); const r=(y.sonuc||[])[0];
        btn.outerHTML=r?('<div class="pa-c">Teklif hazır: <a href="/cikti/'+encodeURI(r.teklif_tek||r.teklif)+'" target="_blank">raporu aç ↗</a>'+
          (r.telegram?(' · Telegram: '+((r.telegram.hata||[]).length?kacir(r.telegram.hata[0]):(r.telegram.gonderilen||[]).length+" parça gitti")):"")+'</div>'):'<div class="pa-c">Üretilemedi.</div>';
      } else if(ey.tur==="gundem"){ gitSekme("gundem"); await gundemTara(); btn.outerHTML='<div class="pa-c">Gündem sekmesinde liste hazır.</div>';
      } else if(ey.tur==="okuma"){ gitSekme("karargah"); await okumaYukle(false); btn.outerHTML='<div class="pa-c">Karargâh\'ta tıklanma kutusu güncellendi.</div>';
      } else if(ey.tur==="karga"){ const y=await jpost("/api/uretim",{karga:true,onay:true});
        if(y.hata){ btn.outerHTML='<div class="pa-c">Hata: '+kacir(y.hata)+'</div>'; }
        else { btn.outerHTML='<div class="pa-c">'+(y.sonuc||[]).map(r=>'• '+kacir(r.ad)+': '+(r.site?('hazır → '+kacir(r.site.mp4.split("/").pop())+' ('+r.site.boyut_kb+' KB)'):(r.mesaj||r.yol))).join('<br>')+'</div>'; }
      } else { btn.outerHTML='<div class="pa-c">Bu eylemi henüz bilmiyorum.</div>'; }
    }catch(x){ btn.outerHTML='<div class="pa-c">Hata: '+kacir(String(x))+'</div>'; }
  };
})();
</script>
</body></html>"""
