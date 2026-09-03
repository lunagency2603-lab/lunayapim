/* Karga dizisi — sembol kliplerini sırayla, çapraz geçişle oynatır.
   Hedef: [data-karga] taşıyan her kutu (kahraman, şerit). İçindeki ilk <video> kullanılır.
   Liste: karga-k1..k6; dosyası olmayan klip sessizce atlanır.
   Olay: kutu üzerinde "karga:degisti" (detail: sira, toplam, ad, etiket)
         ve "karga:ilerleme" (detail: oran 0-1). Kahraman sayacı bunları dinler.
   "Hareketi azalt" açıksa dokunulmaz (video.js de oynatmaz). */
(function () {
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
  var KOK = (function () {
    var h = document.querySelector('link[href*="luna.css"]');
    return h ? h.getAttribute("href").replace(/luna\.css.*$/, "") : "assets/";
  })();

  function varMi(ad, cb) {
    var x = new XMLHttpRequest(); x.open("HEAD", KOK + "video/" + ad + ".mp4", true);
    x.onload = function () { cb(x.status >= 200 && x.status < 400); };
    x.onerror = function () { cb(false); }; x.send();
  }

  function kur(kutu, mevcut) {
    var ilk = kutu.querySelector("video");
    if (!ilk || mevcut.length < 1) return;
    var basla = parseInt(kutu.getAttribute("data-karga") || "0", 10) % mevcut.length;
    var etiket = kutu.querySelector("[data-karga-etiket]");

    var iki = ilk.cloneNode(false);
    iki.removeAttribute("data-luna"); iki.removeAttribute("poster"); iki.removeAttribute("autoplay");
    iki.removeAttribute("loop"); iki.loop = false;
    iki.muted = true; iki.playsInline = true; iki.preload = "auto";
    iki.style.cssText = "position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .7s ease";
    ilk.style.transition = "opacity .7s ease";
    if (getComputedStyle(kutu).position === "static") kutu.style.position = "relative";
    kutu.insertBefore(iki, ilk.nextSibling);

    var sira = basla, aktif = ilk, bekleyen = iki;

    function kaynak(v, ad) {
      while (v.firstChild) v.removeChild(v.firstChild);
      var w = document.createElement("source"); w.src = KOK + "video/" + ad + ".webm"; w.type = "video/webm";
      var m = document.createElement("source"); m.src = KOK + "video/" + ad + ".mp4";  m.type = "video/mp4";
      v.appendChild(w); v.appendChild(m); v.load();
    }
    function duyur() {
      if (etiket) etiket.textContent = "Karga · " + mevcut[sira][1];
      kutu.dispatchEvent(new CustomEvent("karga:degisti", { detail: { sira: sira, toplam: mevcut.length, ad: mevcut[sira][0], etiket: mevcut[sira][1] } }));
    }
    function ilerleme() {
      var v = aktif; if (!v.duration) return;
      kutu.dispatchEvent(new CustomEvent("karga:ilerleme", { detail: { oran: v.currentTime / v.duration } }));
    }
    function sonraki() {
      if (mevcut.length < 2) return;
      sira = (sira + 1) % mevcut.length;
      kaynak(bekleyen, mevcut[sira][0]);
      bekleyen.currentTime = 0;
      bekleyen.play().then(function () {
        bekleyen.style.opacity = "1"; aktif.style.opacity = "0";
        var t = aktif; aktif = bekleyen; bekleyen = t;
        aktif.onended = sonraki; aktif.ontimeupdate = ilerleme;
        duyur();
        setTimeout(function () { bekleyen.pause(); }, 800);
      }).catch(function () {});
    }

    // ilk klip: kutunun kendi kaynağı yerine dizinin başlangıcı
    if (mevcut[basla][0] !== "karga-k1" || !/karga-k1/.test(ilk.currentSrc || (ilk.querySelector("source") || {}).src || "")) {
      kaynak(ilk, mevcut[basla][0]);
    }
    ilk.loop = mevcut.length < 2; ilk.onended = sonraki; ilk.ontimeupdate = ilerleme;
    ilk.play().catch(function () {});
    duyur();
  }

  var kutular = document.querySelectorAll("[data-karga]");
  if (!kutular.length) return;
  var mevcut = [], kalan = KLIPLER.length;
  KLIPLER.forEach(function (k) {
    varMi(k[0], function (ok) {
      if (ok) mevcut.push(k);
      if (--kalan === 0) {
        mevcut.sort(function (a, b) { return KLIPLER.indexOf(a) - KLIPLER.indexOf(b); });
        Array.prototype.forEach.call(kutular, function (kutu) { kur(kutu, mevcut); });
      }
    });
  });
})();
