/* Luna Motoru — siteyi işleten sistemin canlı künyesi.
   Sayılar assets/motor.json'dan geliyor; hepsi dosyadan SAYILDI, elle yazılmadı.
   Veri yoksa bölüm kendini gizler — boş kutu göstermiyoruz. */
(function () {
  "use strict";
  var yer = document.getElementById("luna-motor");
  if (!yer) return;

  var KOK = (function () {
    var h = document.querySelector('link[href*="luna.css"]');
    return h ? h.getAttribute("href").replace(/luna\.css.*$/, "") : "assets/";
  })();
  var AZALT = window.matchMedia &&
              window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function kacir(x) {
    return String(x == null ? "" : x).replace(/&/g, "&amp;")
      .replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function bicim(n) {
    return (typeof n === "number" && n % 1 !== 0)
      ? n.toFixed(0)
      : String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  }

  function say(e, hedef) {
    if (AZALT) { e.textContent = bicim(hedef); return; }
    var bas = null, sure = 900;
    function adim(t) {
      if (bas === null) bas = t;
      var o = Math.min(1, (t - bas) / sure);
      var y = 1 - Math.pow(1 - o, 3);          // yumuşak yavaşlama
      e.textContent = bicim(Math.round(hedef * y));
      if (o < 1) requestAnimationFrame(adim);
      else e.textContent = bicim(hedef);
    }
    requestAnimationFrame(adim);
  }

  var x = new XMLHttpRequest();
  x.open("GET", KOK + "motor.json", true);
  x.onload = function () {
    if (x.status < 200 || x.status >= 300) { yer.remove(); return; }
    var d;
    try { d = JSON.parse(x.responseText); } catch (e) { yer.remove(); return; }
    if (!d || !(d.olcum || []).length) { yer.remove(); return; }
    ciz(d);
  };
  x.onerror = function () { yer.remove(); };
  x.send();

  function ciz(d) {
    var sayaclar = d.olcum.map(function (o) {
      return '<div class="mtr-k">' +
        '<b data-hedef="' + kacir(o.d) + '">0</b>' +
        '<span class="mtr-e">' + kacir(o.e) + '</span>' +
        '<span class="mtr-a">' + kacir(o.a) + '</span>' +
        '</div>';
    }).join("");

    var boru = (d.boru || []).map(function (b, i) {
      return '<li style="--g:' + (i * 0.14) + 's">' +
        '<code>' + kacir(b.ad) + '</code>' +
        '<span>' + kacir(b["not"]) + '</span></li>';
    }).join("");

    yer.innerHTML =
      '<div class="mtr-sayac">' + sayaclar + '</div>' +
      (boru ? '<div class="mtr-boru"><span class="etk">Günlük akış</span>' +
              '<ol class="mtr-adim">' + boru + '</ol></div>' : "") +
      '<p class="mtr-not">Bu sayıların hiçbiri elle yazılmadı — depodaki ' +
      'dosyalardan sayıldı. Son güncelleme <b>' + kacir(d.guncel) + '</b>' +
      (d.saat ? ' · ' + kacir(d.saat) : '') + '.</p>';

    var kartlar = yer.querySelectorAll(".mtr-k b");
    var basladi = false;
    function calistir() {
      if (basladi) return;
      basladi = true;
      kartlar.forEach(function (e, i) {
        var h = parseFloat(e.getAttribute("data-hedef"));
        setTimeout(function () { say(e, h); }, i * 90);
      });
      yer.classList.add("mtr-on");
    }
    if (!("IntersectionObserver" in window)) { calistir(); return; }
    var g = new IntersectionObserver(function (kayit) {
      kayit.forEach(function (k) { if (k.isIntersecting) { calistir(); g.disconnect(); } });
    }, { threshold: 0.25 });
    g.observe(yer);
  }
})();
