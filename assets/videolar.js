/* ============================================================
   LUNA YAPIM — VİDEO DEFTERİ
   ------------------------------------------------------------
   TEK YAPMAN GEREKEN: aşağıdaki listeye YouTube video kimliğini
   yapıştırmak.  Kimlik = adres çubuğundaki v= sonrası kısım.
      https://www.youtube.com/watch?v=TjUTFk9LZSs
                                     └────┬────┘
                                    işte bu kısım

   id boş ("") bırakılırsa o video sitede HİÇ görünmez.
   Bir bölümdeki tüm videolar boşsa o bölüm otomatik gizlenir.
   Yani listeyi şimdiden doldurabilirsin; kimliği yapıştırdığın an yayına girer.

   etiket → videonun hangi sayfalarda çıkacağını belirler:
     isler          → İşler sayfası + ana sayfa (hepsi buraya girer)
     insaat-3d      → hizmetler/insaat-3d-modelleme.html
     urun-animasyon → hizmetler/urun-animasyon.html
     klip           → hizmetler/klip-cekimi.html
     emlak          → hizmetler/emlak-kurumsal.html
     drone          → hizmetler/drone-fpv.html
     dugun          → hizmetler/dugun-etkinlik.html
     isletme        → hizmetler/isletme-tanitim.html
   ============================================================ */

window.LUNA_VIDEOLAR = [

  /* ---------- YAYINDA ---------- */
  { id:"TjUTFk9LZSs", baslik:"Kısa Film",              kat:"Kısa Film",      etiket:["isler"] },
  { id:"aV6_WSjJcnU", baslik:"Sinematografi",          kat:"Sinematografi",  etiket:["isler"] },
  { id:"kRc1KAWI-_o", baslik:"Üretim Reklam Filmi",    kat:"Reklam",         etiket:["isler","isletme"] },
  { id:"YGYCJZPC1cA", baslik:"Düğün Klibi",            kat:"Düğün",          etiket:["isler","dugun"] },
  { id:"DuMsRUDUYc8", baslik:"Şiir Klibi",             kat:"Klip",           etiket:["isler","klip"] },
  { id:"CV6kVVBuxxM", baslik:"Kısa Film / Klip",       kat:"Kısa Film",      etiket:["isler","klip"] },
  { id:"itxSC873O_U", baslik:"Video Opener",           kat:"Opener",         etiket:["isler"] },

  /* ---------- İNŞAAT & MİMARİ 3D MODELLEME (kimlik bekliyor) ---------- */
  { id:"", baslik:"Konut Projesi 3D Tanıtım Animasyonu", kat:"3D Mimari",   etiket:["isler","insaat-3d"] },
  { id:"", baslik:"Villa Dış Cephe Render Animasyonu",   kat:"3D Mimari",   etiket:["isler","insaat-3d"] },
  { id:"", baslik:"İç Mekân Sanal Tur",                  kat:"3D Mimari",   etiket:["isler","insaat-3d"] },
  { id:"", baslik:"Site / Yerleşim Maket Videosu",       kat:"3D Mimari",   etiket:["isler","insaat-3d"] },
  { id:"", baslik:"İnşaat Aşama Simülasyonu",            kat:"3D Mimari",   etiket:["isler","insaat-3d"] },

  /* ---------- ÜRÜN & HİZMET ANİMASYONU (kimlik bekliyor) ---------- */
  { id:"", baslik:"3D Ürün Tanıtım Animasyonu",          kat:"Ürün 3D",     etiket:["isler","urun-animasyon"] },
  { id:"", baslik:"Makine Çalışma Prensibi Animasyonu",  kat:"Ürün 3D",     etiket:["isler","urun-animasyon"] },
  { id:"", baslik:"Üretim Hattı Fabrika Animasyonu",     kat:"Ürün 3D",     etiket:["isler","urun-animasyon"] },
  { id:"", baslik:"Hizmet Anlatım Animasyonu",           kat:"Animasyon",   etiket:["isler","urun-animasyon"] },
  { id:"", baslik:"Ürün Patlatılmış Görünüm (Exploded)", kat:"Ürün 3D",     etiket:["isler","urun-animasyon"] },

  /* ---------- KLİP ÇEKİMİ (kimlik bekliyor) ---------- */
  { id:"", baslik:"Müzik Klibi",                         kat:"Klip",        etiket:["isler","klip"] },
  { id:"", baslik:"Marka Klibi",                         kat:"Klip",        etiket:["isler","klip"] },
  { id:"", baslik:"Sanatçı Tanıtım Klibi",               kat:"Klip",        etiket:["isler","klip"] },

  /* ---------- EMLAK & KURUMSAL (kimlik bekliyor) ---------- */
  { id:"", baslik:"Villa Tanıtım Filmi",                 kat:"Emlak",       etiket:["isler","emlak"] },
  { id:"", baslik:"Konut Projesi Tanıtımı",              kat:"Emlak",       etiket:["isler","emlak"] },
  { id:"", baslik:"Fabrika Kurumsal Tanıtım",            kat:"Kurumsal",    etiket:["isler","emlak"] },

  /* ---------- DRONE & FPV (kimlik bekliyor) ---------- */
  { id:"", baslik:"FPV Tek Plan Mekân Turu",             kat:"FPV",         etiket:["isler","drone"] },
  { id:"", baslik:"Havadan Şantiye İlerleme Çekimi",     kat:"Drone",       etiket:["isler","drone","insaat-3d"] }

];

/* ============================================================
   RENDER — bu kısma dokunmana gerek yok
   ============================================================ */
(function(){
  function kart(v){
    return '<div class="is" data-vid="'+v.id+'">'+
      '<img loading="lazy" src="https://i.ytimg.com/vi/'+v.id+'/hqdefault.jpg" alt="'+v.baslik+'">'+
      '<span class="kat">'+v.kat+'</span>'+
      '<span class="oynat"><span></span></span>'+
      '<h3>'+v.baslik+'</h3></div>';
  }

  function doldur(){
    var liste = window.LUNA_VIDEOLAR || [];
    document.querySelectorAll('[data-video]').forEach(function(kap){
      var etiket = kap.getAttribute('data-video');
      var limit  = parseInt(kap.getAttribute('data-limit')||'0',10);
      var sec = liste.filter(function(v){
        return v.id && v.etiket && v.etiket.indexOf(etiket) !== -1;
      });
      if(limit>0) sec = sec.slice(0,limit);

      if(!sec.length){
        var bolum = kap.closest('[data-video-bolum]') || kap.closest('section');
        if(bolum) bolum.style.display='none'; else kap.style.display='none';
        return;
      }
      kap.innerHTML = sec.map(kart).join('');
    });
    bagla();
  }

  function bagla(){
    document.querySelectorAll('.is').forEach(function(k){
      if(k.dataset.bagli) return;
      k.dataset.bagli='1';
      k.addEventListener('click',function(){
        var v=k.dataset.vid; if(!v) return;
        var f=document.getElementById('vframe'), m=document.getElementById('vmodal');
        if(!f||!m) return;
        f.src='https://www.youtube.com/embed/'+v+'?autoplay=1&rel=0';
        m.classList.add('on');
      });
    });
  }

  window.lunaVideoKapat = function(){
    var f=document.getElementById('vframe'), m=document.getElementById('vmodal');
    if(m) m.classList.remove('on');
    if(f) f.src='';
  };

  function kur(){
    doldur();
    var m=document.getElementById('vmodal');
    if(m && !m.dataset.bagli){
      m.dataset.bagli='1';
      m.addEventListener('click',function(e){ if(e.target.id==='vmodal') window.lunaVideoKapat(); });
    }
    document.addEventListener('keydown',function(e){ if(e.key==='Escape') window.lunaVideoKapat(); });
    var y=document.getElementById('yil'); if(y) y.textContent=new Date().getFullYear();
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',kur);
  else kur();
})();
