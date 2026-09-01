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

  /* ---------- spiral: dönen 3B katalog ---------- */
  function spiral(kap, kutu){
    var sahne = kap._sahne;
    if(!sahne) return;
    var aci = 0, hiz = -0.10, sur = null, durdu = false, gorunur = false, raf = 0, yari = 460;

    function yerlestir(){
      /* önceki klonları temizle */
      [].slice.call(sahne.querySelectorAll('[data-kopya]')).forEach(function(c){
        c.parentNode.removeChild(c);
      });
      var asil = [].slice.call(sahne.children).filter(function(c){ return !c.hidden; });
      var n = asil.length; if(!n) return;
      var dar = window.innerWidth < 760;
      var gen = dar ? 196 : 262;

      /* 6+ iş varsa dizi bir kez daha dizilir → iki tam tur, gerçek sarmal */
      var tur = n >= 6 ? 2 : 1;
      var k = asil.slice();
      if(tur === 2){
        /* ikinci tur yarım liste kaydırılıyor: aynı açıda aynı iş iki kez durmasın */
        var kaydir = Math.floor(n / 2);
        asil.map(function(_, i){ return asil[(i + kaydir) % n]; }).forEach(function(c){
          var kl = c.cloneNode(true);
          kl.setAttribute('data-kopya', '1');
          kl.setAttribute('aria-hidden', 'true');
          kl.setAttribute('tabindex', '-1');
          kl.classList.remove('oynuyor');
          var o = kl.querySelector('.is-onizle'); if(o) o.parentNode.removeChild(o);
          sahne.appendChild(kl); k.push(kl);
        });
      }

      var say = k.length;
      var adim = 360 / n;
      var R   = Math.round(Math.max(330, (n * (gen + 34)) / (2 * Math.PI)));
      var yayilim = dar ? (tur === 2 ? 290 : 165) : (tur === 2 ? 424 : 225);
      var tirman = say > 1 ? yayilim / (say - 1) : 0;
      yari = R;
      var yazi = dar ? 52 : 62;
      sahne.style.setProperty('--gen', gen + 'px');
      sahne.style.top = Math.round(40 + yayilim / 2) + 'px';
      kap.style.setProperty('--yuk',
        Math.round(gen * 0.5625 + yazi + yayilim + 80) + 'px');
      k.forEach(function(c, i){
        c.style.transform = 'rotateY(' + (i * adim).toFixed(2) + 'deg) translateZ(' + R + 'px) ' +
                            'translateY(' + (i * tirman - yayilim / 2).toFixed(1) + 'px)';
      });
      [].slice.call(sahne.children).forEach(function(c){
        if(c.hidden) c.style.transform = 'translateZ(-4000px)';
      });
    }
    kap._yerlestir = function(){ if(kap.classList.contains('spiral')) yerlestir(); };

    function ciz(){
      raf = 0;
      if(!sur && !durdu) aci += hiz;
      sahne.style.transform = 'translateZ(' + (-yari) + 'px) rotateY(' + aci.toFixed(2) + 'deg)';
      if(gorunur && kap.classList.contains('spiral')) raf = requestAnimationFrame(ciz);
    }
    function surdur(){ if(!raf && gorunur) raf = requestAnimationFrame(ciz); }

    /* fare üstündeyken dönme dursun ki videoyu izleyebilesin */
    kap.addEventListener('mouseenter', function(){ durdu = true; });
    kap.addEventListener('mouseleave', function(){ durdu = false; surdur(); });

    /* sürükleyerek çevir */
    kap.addEventListener('pointerdown', function(e){
      sur = { x:e.clientX, a:aci, kaydi:false }; kap.classList.add('suruk');
      try { kap.setPointerCapture(e.pointerId); } catch(x){}
    });
    kap.addEventListener('pointermove', function(e){
      if(!sur) return;
      var f = e.clientX - sur.x;
      if(Math.abs(f) > 5) sur.kaydi = true;
      aci = sur.a + f * 0.30;
      sahne.style.transform = 'translateZ(' + (-yari) + 'px) rotateY(' + aci.toFixed(2) + 'deg)';
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

    window.addEventListener('resize', function(){ if(kap.classList.contains('spiral')) yerlestir(); });

    function ac(spiralMi){
      kap.classList.toggle('spiral', spiralMi);
      if(spiralMi){ yerlestir(); gorunur = true; surdur(); }
      else {
        sahne.style.transform = ''; sahne.style.top = '';
        [].slice.call(sahne.querySelectorAll('[data-kopya]')).forEach(function(c){
          c.parentNode.removeChild(c); });
        [].slice.call(sahne.children).forEach(function(c){ c.style.transform = ''; });
      }
      if(kutu){
        var d = kutu.querySelectorAll('[data-gor]');
        d.forEach(function(b){ b.setAttribute('aria-pressed', String((b.dataset.gor === 'spiral') === spiralMi)); });
      }
      try { localStorage.setItem('luna-isler-gorunum', spiralMi ? 'spiral' : 'izgara'); } catch(x){}
    }

    if(kutu && !kutu.querySelector('[data-gor]')){
      var g = document.createElement('span');
      g.className = 'is-gorunum';
      g.innerHTML = '<button type="button" data-gor="spiral" aria-pressed="true" title="Spiral görünüm">Spiral</button>'+
                    '<button type="button" data-gor="izgara" aria-pressed="false" title="Izgara görünüm">Izgara</button>';
      var say = kutu.querySelector('.is-sayac');
      if(say) kutu.insertBefore(g, say); else kutu.appendChild(g);
      g.addEventListener('click', function(e){
        var b = e.target.closest('[data-gor]'); if(!b) return;
        ac(b.dataset.gor === 'spiral');
      });
    }

    var tercih = 'spiral';
    try { tercih = localStorage.getItem('luna-isler-gorunum') || 'spiral'; } catch(x){}
    if(AZALT || !FARE) tercih = 'izgara';
    ac(tercih === 'spiral');
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
      spiral(kap, kutu);

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
