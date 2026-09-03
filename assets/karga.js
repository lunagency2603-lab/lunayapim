/* Karga şeridi — sembol kliplerini sırayla, çapraz geçişle oynatır.
   Liste: karga-k1..k6 (sadece dosyası olan klipler; yoksa sessizce atlanır).
   "Hareketi azalt" açıksa video.js zaten oynatmaz; burada da dokunulmaz. */
(function () {
  var kutu = document.querySelector(".karga-serit");
  if (!kutu) return;
  var azalt = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (azalt) return;

  var KLIPLER = [
    ["karga-k1", "Dalda, arkadan ışık"],
    ["karga-k2", "Havalanış"],
    ["karga-k6", "Kameraya dönüş"],
    ["karga-k3", "Göz · yakın plan"],
    ["karga-k5", "Gece, çatı anteni"],
    ["karga-k4", "Şantiye üstünde süzülüş"]
  ];
  var ilk = kutu.querySelector("video");
  if (!ilk) return;
  var etiket = kutu.querySelector(".serit span:first-child");

  // ikinci katman: geçiş için
  var iki = ilk.cloneNode(false);
  iki.removeAttribute("data-luna"); iki.removeAttribute("poster");
  iki.muted = true; iki.playsInline = true; iki.preload = "auto"; iki.loop = false; iki.removeAttribute("loop");
  iki.style.cssText = "position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .6s ease";
  ilk.style.transition = "opacity .6s ease";
  kutu.style.position = "relative";
  kutu.insertBefore(iki, ilk.nextSibling);

  var sira = 0, aktif = ilk, bekleyen = iki, mevcut = [];

  function kaynak(v, ad) {
    while (v.firstChild) v.removeChild(v.firstChild);
    var w = document.createElement("source"); w.src = "assets/video/" + ad + ".webm"; w.type = "video/webm";
    var m = document.createElement("source"); m.src = "assets/video/" + ad + ".mp4";  m.type = "video/mp4";
    v.appendChild(w); v.appendChild(m); v.load();
  }
  function varMi(ad, cb) {
    var x = new XMLHttpRequest(); x.open("HEAD", "assets/video/" + ad + ".mp4", true);
    x.onload = function () { cb(x.status >= 200 && x.status < 400); };
    x.onerror = function () { cb(false); }; x.send();
  }
  function sonraki() {
    if (mevcut.length < 2) return; // tek klip: loop kalır
    sira = (sira + 1) % mevcut.length;
    var ad = mevcut[sira][0];
    kaynak(bekleyen, ad);
    bekleyen.currentTime = 0;
    bekleyen.play().then(function () {
      bekleyen.style.opacity = "1"; aktif.style.opacity = "0";
      if (etiket) etiket.textContent = "Karga · " + mevcut[sira][1];
      var t = aktif; aktif = bekleyen; bekleyen = t;
      aktif.onended = sonraki;
      setTimeout(function () { bekleyen.pause(); }, 700);
    }).catch(function () {});
  }

  var kalan = KLIPLER.length;
  KLIPLER.forEach(function (k, i) {
    varMi(k[0], function (ok) {
      if (ok) mevcut.push(k);
      if (--kalan === 0) {
        mevcut.sort(function (a, b) { return KLIPLER.indexOf(a) - KLIPLER.indexOf(b); });
        if (mevcut.length >= 2) {
          ilk.loop = false; ilk.onended = sonraki;
          if (etiket) etiket.textContent = "Karga · " + mevcut[0][1];
        }
      }
    });
  });
})();
