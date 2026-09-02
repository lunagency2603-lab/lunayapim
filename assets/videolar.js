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
     ornek          → "Örnek işler" bölümü (kendi dosyalarımız)
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
    musteri:"CM Vorarlberg · Avusturya", sure:"0:15", olcu:"1600×900",
    teslim:"Dış cephe render + kamera hareketi + marka kapanışı",
    one:2, etiket:["isler","ornek","insaat-3d","emlak"] },
  { yerel:"ornek-galzura", baslik:"Galzura Tanıtım Animasyonu", kat:"Animasyon",
    musteri:"Galzura · Avusturya", sure:"1:00", olcu:"1280×720",
    teslim:"Animasyon + seslendirme + TR/DE iki dil, yatay ve 9:16 dikey sürüm",
    one:1, etiket:["isler","ornek","urun-animasyon"] },

  /* ---------- YAYINDA ---------- */
  { teslim:"Senaryo, çekim, kurgu, renk", id:"TjUTFk9LZSs", baslik:"Kısa Film",              kat:"Kısa Film",      etiket:["isler"] },
  { teslim:"Görüntü yönetmenliği ve renk çalışması", id:"aV6_WSjJcnU", baslik:"Sinematografi",          kat:"Sinematografi",  etiket:["isler"] },
  { teslim:"Reklam filmi — çekim ve kurgu", id:"kRc1KAWI-_o", baslik:"Üretim Reklam Filmi",    kat:"Reklam",         etiket:["isler","isletme"] },
  { teslim:"Düğün günü çekimi ve klip kurgusu", id:"YGYCJZPC1cA", baslik:"Düğün Klibi",            kat:"Düğün",          etiket:["isler","dugun"] },
  { teslim:"Klip çekimi ve kurgu", id:"DuMsRUDUYc8", baslik:"Şiir Klibi",             kat:"Klip",           etiket:["isler","klip"] },
  { teslim:"Çekim, kurgu, renk", id:"CV6kVVBuxxM", baslik:"Kısa Film / Klip",       kat:"Kısa Film",      etiket:["isler","klip"] },
  { teslim:"Açılış jeneriği tasarımı", id:"itxSC873O_U", baslik:"Video Opener",           kat:"Opener",         etiket:["isler"] },
  { teslim:"Müzik klibi — çekim ve kurgu", id:"SAL0X164pbA", baslik:"Müzik Klibi",            kat:"Klip",           etiket:["isler","klip"] },

  /* ---------- İNŞAAT & MİMARİ 3D MODELLEME (kimlik bekliyor) ---------- */
  { id:"", baslik:"Villa Dış Cephe Render Animasyonu",   kat:"3D Mimari",   etiket:["kapsam","insaat-3d"] },
  { id:"", baslik:"İç Mekân Sanal Tur",                  kat:"3D Mimari",   etiket:["kapsam","insaat-3d"] },
  { id:"", baslik:"Site / Yerleşim Maket Videosu",       kat:"3D Mimari",   etiket:["kapsam","insaat-3d"] },
  { id:"", baslik:"İnşaat Aşama Simülasyonu",            kat:"3D Mimari",   etiket:["kapsam","insaat-3d"] },

  /* ---------- ÜRÜN & HİZMET ANİMASYONU (kimlik bekliyor) ---------- */
  { id:"", baslik:"3D Ürün Tanıtım Animasyonu",          kat:"Ürün 3D",     etiket:["kapsam","urun-animasyon"] },
  { id:"", baslik:"Makine Çalışma Prensibi Animasyonu",  kat:"Ürün 3D",     etiket:["kapsam","urun-animasyon"] },
  { id:"", baslik:"Üretim Hattı Fabrika Animasyonu",     kat:"Ürün 3D",     etiket:["kapsam","urun-animasyon"] },
  { id:"", baslik:"Ürün Patlatılmış Görünüm (Exploded)", kat:"Ürün 3D",     etiket:["kapsam","urun-animasyon"] },

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
    return h.replace(/luna\.css.*$/, '');
  })();

  function kacir(s){ return String(s == null ? '' : s)
    .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;'); }

  function afis(v){
    return v.yerel ? KOK + 'video/' + v.yerel + '.jpg'
                   : 'https://i.ytimg.com/vi/' + v.id + '/hqdefault.jpg';
  }

  function kart(v, i){
    var b = kacir(v.baslik), k = kacir(v.kat);
    /* künye: yalnızca gerçekten bildiğimiz alanlar — boş olan hiç yazılmıyor */
    var kunye = [];
    if(v.sure) kunye.push(kacir(v.sure));
    if(v.olcu) kunye.push(kacir(v.olcu));
    var one = v.one ? ' one one-'+v.one : '';
    return '<article class="is'+one+'" data-i="'+i+'" data-kat="'+k+'" tabindex="0" '+
      'role="button" aria-label="'+b+' — videoyu aç">'+
      '<div class="kapak">'+
        '<img loading="lazy" src="'+afis(v)+'" alt="'+b+'">'+
        '<span class="im"></span>'+
        (kunye.length ? '<span class="is-kunye">'+kunye.join(' · ')+'</span>' : '')+
      '</div>'+
      '<div class="is-alt">'+
        '<span class="kat">'+k+'</span>'+
        '<h3>'+b+'</h3>'+
        (v.musteri ? '<span class="musteri">'+kacir(v.musteri)+'</span>' : '')+
        (v.teslim ? '<span class="teslim">'+kacir(v.teslim)+'</span>' : '')+
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

  /* ---------- küre: dönen 3B katalog ----------
     Kartlar bir kürenin yüzeyine dağıtılıyor ama hep okura dönük duruyor;
     derinlik ölçek ve saydamlıkla anlatılıyor. */
  function kure(kap, kutu){
    var sahne = kap._sahne;
    if(!sahne) return;
    var ay = 0, ax = -0.12, hiz = -0.0035, sur = null, durdu = false,
        gorunur = false, raf = 0;
    var kartlar = [], nokta = [], R = 300, YASSI = 0.66, P = 950;

    function yerlestir(){
      [].slice.call(sahne.querySelectorAll('[data-kopya]')).forEach(function(c){
        c.parentNode.removeChild(c);
      });
      var asil = [].slice.call(sahne.children).filter(function(c){ return !c.hidden; });
      var n = asil.length; if(!n) return;
      var dar = window.innerWidth < 760;

      /* her iş bir kez: küre üzerinde üst üste binmesinler */
      kartlar = asil.slice();
      var say = kartlar.length;
      var gen = dar ? 150 : (say > 12 ? 168 : 190);
      /* komşu iki nokta arası yay ≈ 2·√(π/n)·R — kart genişliğinden büyük olmalı */
      var acisal = 2 * Math.sqrt(Math.PI / Math.max(4, say));
      R = Math.round(Math.max(dar ? 190 : 300, (gen * 1.95) / acisal));
      /* bakış noktası yakın: öndeki kart belirgin büyüsün */
      P = dar ? 720 : 950;
      var yazi = dar ? 38 : 46;
      var kartYuk = Math.round(gen * 0.5625) + yazi;
      var enB = R * (P / (P - R));
      var boyB = enB * YASSI;
      sahne.style.setProperty('--gen', gen + 'px');
      sahne.style.setProperty('--kyuk', kartYuk + 'px');
      sahne.style.top = Math.round(boyB + kartYuk / 2 + 16) + 'px';
      kap.style.setProperty('--yuk', Math.round(2 * boyB + kartYuk + 34) + 'px');

      /* Fibonacci küresi: noktalar yüzeye eşit dağılıyor */
      var ALTIN = Math.PI * (3 - Math.sqrt(5));
      nokta = kartlar.map(function(_, i){
        var y = 1 - (2 * (i + 0.5)) / say;
        var r = Math.sqrt(Math.max(0, 1 - y * y));
        var th = ALTIN * i;
        return { x: Math.cos(th) * r, y: y, z: Math.sin(th) * r };
      });
      [].slice.call(sahne.children).forEach(function(c){
        if(c.hidden){ c.style.transform = 'scale(0)'; c.style.opacity = '0'; }
      });
      ciz(true);
    }
    kap._yerlestir = function(){ if(kap.classList.contains('kure')) yerlestir(); };

    function ciz(tek){
      if(!tek) raf = 0;
      if(!sur && !durdu && !tek) ay += hiz;
      var cy = Math.cos(ay), sy = Math.sin(ay);
      var cx = Math.cos(ax), sx = Math.sin(ax);
      for(var i = 0; i < kartlar.length; i++){
        var p = nokta[i]; if(!p) continue;
        var x1 =  p.x * cy + p.z * sy;
        var z1 = -p.x * sy + p.z * cy;
        var y2 =  p.y * cx - z1 * sx;
        var z2 =  p.y * sx + z1 * cx;
        var o  = P / (P - z2 * R);
        var e  = kartlar[i];
        e.style.transform = 'translate3d(' + (x1 * R * o).toFixed(1) + 'px,' +
                            (y2 * R * YASSI * o).toFixed(1) + 'px,0) scale(' + o.toFixed(3) + ')';
        e.style.opacity = (0.26 + 0.74 * ((z2 + 1) / 2)).toFixed(3);
        e.style.zIndex = String(1000 + Math.round(z2 * 400));
      }
      if(!tek && gorunur && kap.classList.contains('kure'))
        raf = requestAnimationFrame(function(){ ciz(); });
    }
    function surdur(){ if(!raf && gorunur) raf = requestAnimationFrame(function(){ ciz(); }); }

    /* fare üstündeyken dönme dursun ki videoyu izleyebilesin */
    kap.addEventListener('mouseenter', function(){ durdu = true; });
    kap.addEventListener('mouseleave', function(){ durdu = false; surdur(); });

    /* sürükleyerek çevir — yatayda boylam, dikeyde enlem */
    kap.addEventListener('pointerdown', function(e){
      sur = { x:e.clientX, y:e.clientY, ay:ay, ax:ax, kaydi:false };
      kap.classList.add('suruk');
      try { kap.setPointerCapture(e.pointerId); } catch(x){}
    });
    kap.addEventListener('pointermove', function(e){
      if(!sur) return;
      var fx = e.clientX - sur.x, fy = e.clientY - sur.y;
      if(Math.abs(fx) > 5 || Math.abs(fy) > 5) sur.kaydi = true;
      ay = sur.ay + fx * 0.0075;
      ax = Math.max(-0.7, Math.min(0.7, sur.ax - fy * 0.006));
      ciz(true);
    });
    ['pointerup','pointercancel'].forEach(function(t){
      kap.addEventListener(t, function(){
        if(sur && sur.kaydi) kap._kaydi = Date.now();
        sur = null; kap.classList.remove('suruk'); surdur();
      });
    });
    kap.addEventListener('click', function(e){
      if(kap._kaydi && Date.now() - kap._kaydi < 240){ e.stopPropagation(); e.preventDefault(); }
    }, true);

    if('IntersectionObserver' in window){
      new IntersectionObserver(function(r){
        gorunur = r[0].isIntersecting; if(gorunur) surdur();
      }, { threshold:0.05 }).observe(kap);
    } else { gorunur = true; }

    window.addEventListener('resize', function(){ if(kap.classList.contains('kure')) yerlestir(); });

    function ac(kureMi){
      kap.classList.toggle('kure', kureMi);
      if(kureMi){ yerlestir(); gorunur = true; surdur(); }
      else {
        sahne.style.top = '';
        [].slice.call(sahne.querySelectorAll('[data-kopya]')).forEach(function(c){
          c.parentNode.removeChild(c); });
        [].slice.call(sahne.children).forEach(function(c){
          c.style.transform = ''; c.style.opacity = ''; c.style.zIndex = ''; });
      }
      if(kutu){
        kutu.querySelectorAll('[data-gor]').forEach(function(b){
          b.setAttribute('aria-pressed', String((b.dataset.gor === 'kure') === kureMi));
        });
      }
      try { localStorage.setItem('luna-isler-gorunum', kureMi ? 'kure' : 'izgara'); } catch(x){}
    }

    if(kutu && !kutu.querySelector('[data-gor]')){
      var g = document.createElement('span');
      g.className = 'is-gorunum';
      g.innerHTML = '<button type="button" data-gor="izgara" aria-pressed="true" title="Vitrin görünüm">Vitrin</button>'+
                    '<button type="button" data-gor="kure" aria-pressed="false" title="Küre görünüm">Küre</button>';
      var sy = kutu.querySelector('.is-sayac');
      if(sy) kutu.insertBefore(g, sy); else kutu.appendChild(g);
      g.addEventListener('click', function(e){
        var b = e.target.closest('[data-gor]'); if(!b) return;
        ac(b.dataset.gor === 'kure');
      });
    }

    var tercih = 'izgara';
    try { tercih = localStorage.getItem('luna-isler-gorunum') || 'izgara'; } catch(x){}
    if(tercih === 'spiral') tercih = 'kure';
    if(AZALT || !FARE) tercih = 'izgara';
    ac(tercih === 'kure');
  }

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
      kap.querySelectorAll('.is:not([data-kopya])').forEach(function(c){
        var gor = !k || c.getAttribute('data-kat') === k;
        c.hidden = !gor; if(gor) n++;
      });
      var s = kutu.querySelector('.is-sayac');
      if(s) s.textContent = n + ' iş';
      if(kap._yerlestir) kap._yerlestir();
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
      /* öne çıkan işler başa: one değeri büyük olan önce */
      sec = sec.slice().sort(function(a,b){ return (b.one||0) - (a.one||0); });
      if(limit > 0) sec = sec.slice(0, limit);

      if(!sec.length){
        var bolum = kap.closest('[data-video-bolum]') || kap.closest('section');
        if(bolum) bolum.style.display='none'; else kap.style.display='none';
        return;
      }
      kap.innerHTML = '<div class="sahne">' + sec.map(kart).join('') + '</div>';
      kap._sec = sec;
      kap._sahne = kap.querySelector('.sahne');

      var kutu = (kap.parentNode || document).querySelector('[data-filtre]');
      if(kutu && !kutu.dataset.kurulu){ kutu.dataset.kurulu = '1'; suzgec(kutu, kap, sec); }
      if(kap.hasAttribute('data-kure')) kure(kap, kutu);

      if(!kap.dataset.bagliKart){
        kap.dataset.bagliKart = '1';
        var bul = function(e){ var k = e.target.closest('.is');
          return (k && kap.contains(k)) ? k : null; };
        var isi = function(k){ return kap._sec[parseInt(k.getAttribute('data-i'), 10)]; };
        kap.addEventListener('click', function(e){ var k = bul(e); if(k) ac(isi(k)); });
        kap.addEventListener('keydown', function(e){ var k = bul(e);
          if(k && (e.key === 'Enter' || e.key === ' ')){ e.preventDefault(); ac(isi(k)); } });
        kap.addEventListener('mouseover', function(e){ var k = bul(e);
          if(k && k !== kap._ustunde){ if(kap._ustunde) durdur(kap._ustunde);
            kap._ustunde = k; onizle(k, isi(k)); } });
        kap.addEventListener('mouseout', function(e){ var k = bul(e);
          if(k && kap._ustunde === k && !k.contains(e.relatedTarget)){
            durdur(k); kap._ustunde = null; } });
        kap.addEventListener('focusin', function(e){ var k = bul(e); if(k) onizle(k, isi(k)); });
        kap.addEventListener('focusout', function(e){ var k = bul(e); if(k) durdur(k); });
      }
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
