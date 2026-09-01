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
  { id:"SAL0X164pbA", baslik:"Müzik Klibi",               kat:"Klip",        etiket:["isler","klip"] },
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
   ------------------------------------------------------------
   data-video="etiket"        → o etiketteki işleri basar
   data-limit="8"             → en fazla 8 iş
   data-duzen="vitrin"        → düz ızgara yerine kavisli katalog
   Fare bir işin üzerine geldiğinde video sessiz olarak oynar,
   tıklayınca sesli tam ekran açılır.
   ============================================================ */
(function(){
  var mq = window.matchMedia || function(){ return { matches:false }; };
  var FARE  = mq.call(window,'(hover:hover) and (pointer:fine)').matches;
  var AZALT = mq.call(window,'(prefers-reduced-motion: reduce)').matches;

  function kacir(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;'); }

  function kart(v){
    var b = kacir(v.baslik), k = kacir(v.kat);
    return '<article class="is" data-vid="'+v.id+'" tabindex="0" role="button" '+
      'aria-label="'+b+' — videoyu aç">'+
      '<img loading="lazy" src="https://i.ytimg.com/vi/'+v.id+'/hqdefault.jpg" alt="'+b+'">'+
      '<span class="kat">'+k+'</span>'+
      '<span class="oynat"><span></span></span>'+
      '<h3>'+b+'</h3></article>';
  }

  /* ---------- fare üzerindeyken sessiz önizleme ---------- */
  function onizle(k){
    if(!FARE || AZALT) return;
    var id = k.dataset.vid;
    if(!id || k.querySelector('.is-onizle')) return;
    clearTimeout(k._zam);
    k._zam = setTimeout(function(){
      if(k.querySelector('.is-onizle')) return;
      var f = document.createElement('iframe');
      f.className = 'is-onizle';
      f.title = 'Sessiz önizleme';
      f.setAttribute('allow','autoplay; encrypted-media');
      f.setAttribute('frameborder','0');
      f.setAttribute('tabindex','-1');
      f.src = 'https://www.youtube-nocookie.com/embed/'+id+
        '?autoplay=1&mute=1&controls=0&loop=1&playlist='+id+
        '&modestbranding=1&rel=0&playsinline=1&disablekb=1&iv_load_policy=3';
      k.appendChild(f);
      k.classList.add('oynuyor');
    }, 240);
  }
  function durdur(k){
    clearTimeout(k._zam);
    var f = k.querySelector('.is-onizle');
    if(f) f.parentNode.removeChild(f);
    k.classList.remove('oynuyor');
  }

  /* ---------- kavisli katalog ---------- */
  function vitrin(kap){
    var istek = 0;
    function ciz(){
      istek = 0;
      var r = kap.getBoundingClientRect();
      if(!r.width) return;
      var orta = r.left + r.width/2, yari = r.width/2;
      Array.prototype.forEach.call(kap.children, function(k){
        var kr = k.getBoundingClientRect();
        var d = (kr.left + kr.width/2 - orta) / yari;
        d = Math.max(-1.5, Math.min(1.5, d));
        var a = Math.abs(d);
        k.style.transform = 'translateZ(' + (-a*150).toFixed(1) + 'px) rotateY(' +
          (-d*24).toFixed(2) + 'deg) scale(' + (1 - a*0.07).toFixed(3) + ')';
        k.style.opacity = (1 - a*0.45).toFixed(3);
        k.style.zIndex  = String(100 - Math.round(a*60));
      });
    }
    function iste(){ if(!istek) istek = requestAnimationFrame(ciz); }
    kap.addEventListener('scroll', iste, { passive:true });
    window.addEventListener('resize', iste);
    if(document.fonts && document.fonts.ready) document.fonts.ready.then(iste);
    setTimeout(iste, 60); setTimeout(iste, 400);

    /* fareyle sürükleme */
    var bas = null, kaydi = false;
    kap.addEventListener('pointerdown', function(e){
      if(e.pointerType === 'touch') return;
      bas = { x:e.clientX, s:kap.scrollLeft }; kaydi = false;
      kap.classList.add('suruk');
    });
    kap.addEventListener('pointermove', function(e){
      if(!bas) return;
      var fark = e.clientX - bas.x;
      if(Math.abs(fark) > 6) kaydi = true;
      kap.scrollLeft = bas.s - fark;
    });
    ['pointerup','pointercancel','pointerleave'].forEach(function(t){
      kap.addEventListener(t, function(){ bas = null; kap.classList.remove('suruk'); });
    });
    kap.addEventListener('click', function(e){
      if(kaydi){ e.stopPropagation(); e.preventDefault(); kaydi = false; }
    }, true);
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
      if(kap.getAttribute('data-duzen') === 'vitrin' && sec.length > 2){
        kap.classList.add('vitrin');
        vitrin(kap);
      }
    });
    bagla();
  }

  function ac(id){
    if(!id) return;
    var f = document.getElementById('vframe'), m = document.getElementById('vmodal');
    if(!f || !m) return;
    f.src = 'https://www.youtube.com/embed/'+id+'?autoplay=1&rel=0';
    m.classList.add('on');
    document.body.style.overflow = 'hidden';
  }

  function bagla(){
    document.querySelectorAll('.is').forEach(function(k){
      if(k.dataset.bagli) return;
      k.dataset.bagli='1';
      k.addEventListener('click', function(){ ac(k.dataset.vid); });
      k.addEventListener('keydown', function(e){
        if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); ac(k.dataset.vid); }
      });
      k.addEventListener('mouseenter', function(){ onizle(k); });
      k.addEventListener('mouseleave', function(){ durdur(k); });
      k.addEventListener('focus', function(){ onizle(k); });
      k.addEventListener('blur',  function(){ durdur(k); });
    });
  }

  window.lunaVideoKapat = function(){
    var f=document.getElementById('vframe'), m=document.getElementById('vmodal');
    if(m) m.classList.remove('on');
    if(f) f.src='';
    document.body.style.overflow = '';
  };
  /* sayfalardaki kapat düğmesi bu adı çağırıyor */
  window.vkapat = window.lunaVideoKapat;

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
