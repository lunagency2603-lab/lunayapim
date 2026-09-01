/* ============================================================
   LUNA YAPIM — VİDEO DEFTERİ
   ------------------------------------------------------------
   İKİ TÜR KAYIT VAR:

   1) YouTube işi  →  id:"..." yaz.
      Kimlik = adres çubuğundaki v= sonrası kısım.
         https://www.youtube.com/watch?v=TjUTFk9LZSs
                                        └────┬────┘
      id boş ("") bırakılırsa o iş sitede HİÇ görünmez.

   2) Kendi dosyamız  →  yerel:"dosya-adi" yaz.
      assets/video/ klasöründeki <dosya-adi>.mp4 ve <dosya-adi>.jpg
      kullanılır; varsa on-<dosya-adi>.mp4 fareyle üzerine gelince
      oynayan hafif önizleme olur.

   musteri:"..."  →  kartın altında müşteri adı yazar (isteğe bağlı)

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

  /* ---------- KENDİ DOSYALARIMIZ ---------- */
  { yerel:"ornek-cm", baslik:"Konut Projesi 3D Tanıtım Animasyonu", kat:"3D Mimari",
    musteri:"CM Vorarlberg · Avusturya", etiket:["isler","insaat-3d","emlak"] },
  { yerel:"ornek-galzura", baslik:"Galzura Tanıtım Animasyonu", kat:"Animasyon",
    musteri:"Galzura · Avusturya", etiket:["isler","urun-animasyon"] },

  /* ---------- YAYINDA ---------- */
  { id:"TjUTFk9LZSs", baslik:"Kısa Film",              kat:"Kısa Film",      etiket:["isler"] },
  { id:"aV6_WSjJcnU", baslik:"Sinematografi",          kat:"Sinematografi",  etiket:["isler"] },
  { id:"kRc1KAWI-_o", baslik:"Üretim Reklam Filmi",    kat:"Reklam",         etiket:["isler","isletme"] },
  { id:"YGYCJZPC1cA", baslik:"Düğün Klibi",            kat:"Düğün",          etiket:["isler","dugun"] },
  { id:"DuMsRUDUYc8", baslik:"Şiir Klibi",             kat:"Klip",           etiket:["isler","klip"] },
  { id:"CV6kVVBuxxM", baslik:"Kısa Film / Klip",       kat:"Kısa Film",      etiket:["isler","klip"] },
  { id:"itxSC873O_U", baslik:"Video Opener",           kat:"Opener",         etiket:["isler"] },
  { id:"SAL0X164pbA", baslik:"Müzik Klibi",            kat:"Klip",           etiket:["isler","klip"] },

  /* ---------- İNŞAAT & MİMARİ 3D MODELLEME (kimlik bekliyor) ---------- */
  { id:"", baslik:"Villa Dış Cephe Render Animasyonu",   kat:"3D Mimari",   etiket:["isler","insaat-3d"] },
  { id:"", baslik:"İç Mekân Sanal Tur",                  kat:"3D Mimari",   etiket:["isler","insaat-3d"] },
  { id:"", baslik:"Site / Yerleşim Maket Videosu",       kat:"3D Mimari",   etiket:["isler","insaat-3d"] },
  { id:"", baslik:"İnşaat Aşama Simülasyonu",            kat:"3D Mimari",   etiket:["isler","insaat-3d"] },

  /* ---------- ÜRÜN & HİZMET ANİMASYONU (kimlik bekliyor) ---------- */
  { id:"", baslik:"3D Ürün Tanıtım Animasyonu",          kat:"Ürün 3D",     etiket:["isler","urun-animasyon"] },
  { id:"", baslik:"Makine Çalışma Prensibi Animasyonu",  kat:"Ürün 3D",     etiket:["isler","urun-animasyon"] },
  { id:"", baslik:"Üretim Hattı Fabrika Animasyonu",     kat:"Ürün 3D",     etiket:["isler","urun-animasyon"] },
  { id:"", baslik:"Ürün Patlatılmış Görünüm (Exploded)", kat:"Ürün 3D",     etiket:["isler","urun-animasyon"] },

  /* ---------- KLİP ÇEKİMİ (kimlik bekliyor) ---------- */
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
   data-video="etiket"   → o etiketteki işleri basar
   data-limit="8"        → en fazla 8 iş (yoksa hepsi)
   data-filtre           → kategori düğmelerinin konacağı boş div
   Fare bir işin üzerinde durunca sessiz oynar; tıklayınca sesli açılır.
   ============================================================ */
(function(){
  var mq = window.matchMedia ? window.matchMedia.bind(window) : function(){ return { matches:false }; };
  var FARE  = mq('(hover:hover) and (pointer:fine)').matches;
  var AZALT = mq('(prefers-reduced-motion: reduce)').matches;

  /* sayfa derinliğine göre assets yolu ("assets/" ya da "../assets/") */
  var KOK = (function(){
    var l = document.querySelector('link[rel="stylesheet"][href*="luna.css"]');
    var h = l ? l.getAttribute('href') : 'assets/luna.css';
    return h.replace(/luna\.css$/, '');
  })();

  function kacir(s){ return String(s == null ? '' : s)
    .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;'); }

  function afis(v){
    return v.yerel ? KOK + 'video/' + v.yerel + '.jpg'
                   : 'https://i.ytimg.com/vi/' + v.id + '/hqdefault.jpg';
  }

  function kart(v, i){
    var b = kacir(v.baslik), k = kacir(v.kat);
    return '<article class="is" data-i="'+i+'" data-kat="'+k+'" tabindex="0" role="button" '+
      'aria-label="'+b+' — videoyu aç">'+
      '<div class="kapak">'+
        '<img loading="lazy" src="'+afis(v)+'" alt="'+b+'">'+
        '<span class="im"></span>'+
      '</div>'+
      '<div class="is-alt"><span class="kat">'+k+'</span><h3>'+b+'</h3>'+
        (v.musteri ? '<span class="musteri">'+kacir(v.musteri)+'</span>' : '')+
      '</div></article>';
  }

  /* ---------- fare üzerindeyken sessiz önizleme ---------- */
  function onizle(k, v){
    if(!FARE || AZALT) return;
    if(k.querySelector('.is-onizle')) return;
    clearTimeout(k._zam);
    k._zam = setTimeout(function(){
      if(k.querySelector('.is-onizle')) return;
      var e;
      if(v.yerel){
        e = document.createElement('video');
        e.className = 'is-onizle';
        e.muted = true; e.defaultMuted = true; e.loop = true;
        e.playsInline = true; e.autoplay = true; e.preload = 'auto';
        e.setAttribute('muted',''); e.setAttribute('playsinline','');
        e.innerHTML =
          '<source src="'+KOK+'video/on-'+v.yerel+'.webm" type="video/webm">'+
          '<source src="'+KOK+'video/on-'+v.yerel+'.mp4" type="video/mp4">'+
          '<source src="'+KOK+'video/'+v.yerel+'.mp4" type="video/mp4">';
        e.addEventListener('playing', function(){ k.classList.add('oynuyor'); });
        e.addEventListener('canplay', function(){ e.play().catch(function(){}); });
        k.querySelector('.kapak').appendChild(e);
        e.load();
        e.play().catch(function(){});
        return;
      }
      e = document.createElement('iframe');
      e.className = 'is-onizle yt';
      e.title = 'Sessiz önizleme';
      e.setAttribute('allow','autoplay; encrypted-media');
      e.setAttribute('frameborder','0');
      e.setAttribute('tabindex','-1');
      e.src = 'https://www.youtube-nocookie.com/embed/'+v.id+
        '?autoplay=1&mute=1&controls=0&loop=1&playlist='+v.id+
        '&modestbranding=1&rel=0&playsinline=1&disablekb=1&iv_load_policy=3';
      e.addEventListener('load', function(){ k.classList.add('oynuyor'); });
      k.querySelector('.kapak').appendChild(e);
      k.classList.add('oynuyor');
    }, 200);
  }
  function durdur(k){
    clearTimeout(k._zam);
    var e = k.querySelector('.is-onizle');
    if(e){ if(e.pause) e.pause(); e.parentNode.removeChild(e); }
    k.classList.remove('oynuyor');
  }

  /* ---------- büyük oynatıcı ---------- */
  function ac(v){
    var m = document.getElementById('vmodal');
    if(!m) return;
    var f = document.getElementById('vframe');
    var y = document.getElementById('vlokal');
    if(!y){
      y = document.createElement('video');
      y.id = 'vlokal'; y.controls = true; y.playsInline = true;
      m.appendChild(y);
    }
    if(v.yerel){
      if(f){ f.src = ''; f.style.display = 'none'; }
      y.style.display = 'block';
      y.innerHTML = '<source src="'+KOK+'video/'+v.yerel+'.webm" type="video/webm">'+
                    '<source src="'+KOK+'video/'+v.yerel+'.mp4" type="video/mp4">';
      y.load(); y.play().catch(function(){});
    } else {
      y.pause(); y.innerHTML = ''; y.removeAttribute('src'); y.load(); y.style.display = 'none';
      if(f){ f.style.display = 'block';
        f.src = 'https://www.youtube.com/embed/'+v.id+'?autoplay=1&rel=0'; }
    }
    m.classList.add('on');
    document.body.style.overflow = 'hidden';
  }

  window.lunaVideoKapat = function(){
    var f = document.getElementById('vframe'), m = document.getElementById('vmodal'),
        y = document.getElementById('vlokal');
    if(m) m.classList.remove('on');
    if(f) f.src = '';
    if(y){ y.pause(); y.innerHTML = ''; y.removeAttribute('src'); y.load(); }
    document.body.style.overflow = '';
  };
  window.vkapat = window.lunaVideoKapat;   /* sayfalardaki kapat düğmesi bunu çağırıyor */

  /* ---------- kategori süzgeci ---------- */
  function suzgec(kutu, kap, sec){
    var katlar = [];
    sec.forEach(function(v){ if(katlar.indexOf(v.kat) === -1) katlar.push(v.kat); });
    if(katlar.length < 3){ kutu.style.display = 'none'; return; }
    var h = '<button type="button" aria-pressed="true" data-k="">Tümü</button>';
    katlar.forEach(function(k){
      h += '<button type="button" aria-pressed="false" data-k="'+kacir(k)+'">'+kacir(k)+'</button>';
    });
    h += '<span class="is-sayac">'+sec.length+' iş</span>';
    kutu.innerHTML = h;
    kutu.addEventListener('click', function(e){
      var d = e.target.closest('button'); if(!d) return;
      var k = d.getAttribute('data-k');
      kutu.querySelectorAll('button').forEach(function(b){
        b.setAttribute('aria-pressed', String(b === d));
      });
      var n = 0;
      kap.querySelectorAll('.is').forEach(function(c){
        var gor = !k || c.getAttribute('data-kat') === k;
        c.hidden = !gor; if(gor) n++;
      });
      var s = kutu.querySelector('.is-sayac');
      if(s) s.textContent = n + ' iş';
    });
  }

  function doldur(){
    var liste = window.LUNA_VIDEOLAR || [];
    document.querySelectorAll('[data-video]').forEach(function(kap){
      var etiket = kap.getAttribute('data-video');
      var limit  = parseInt(kap.getAttribute('data-limit')||'0',10);
      var sec = liste.filter(function(v){
        return (v.id || v.yerel) && v.etiket && v.etiket.indexOf(etiket) !== -1;
      });
      if(limit > 0) sec = sec.slice(0, limit);

      if(!sec.length){
        var bolum = kap.closest('[data-video-bolum]') || kap.closest('section');
        if(bolum) bolum.style.display='none'; else kap.style.display='none';
        return;
      }
      kap.innerHTML = sec.map(kart).join('');
      kap._sec = sec;

      var kutu = (kap.parentNode || document).querySelector('[data-filtre]');
      if(kutu && !kutu.dataset.kurulu){ kutu.dataset.kurulu = '1'; suzgec(kutu, kap, sec); }

      kap.querySelectorAll('.is').forEach(function(k){
        var v = sec[parseInt(k.getAttribute('data-i'), 10)];
        k.addEventListener('click', function(){ ac(v); });
        k.addEventListener('keydown', function(e){
          if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); ac(v); }
        });
        k.addEventListener('mouseenter', function(){ onizle(k, v); });
        k.addEventListener('mouseleave', function(){ durdur(k); });
        k.addEventListener('focus', function(){ onizle(k, v); });
        k.addEventListener('blur',  function(){ durdur(k); });
      });
    });
  }

  function kur(){
    doldur();
    var m = document.getElementById('vmodal');
    if(m && !m.dataset.bagli){
      m.dataset.bagli = '1';
      m.addEventListener('click', function(e){ if(e.target.id === 'vmodal') window.lunaVideoKapat(); });
    }
    document.addEventListener('keydown', function(e){ if(e.key === 'Escape') window.lunaVideoKapat(); });
    var y = document.getElementById('yil'); if(y) y.textContent = new Date().getFullYear();
  }

  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', kur);
  else kur();
})();
