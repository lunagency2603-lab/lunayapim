/* Hizmet sayfalarındaki tanıtım videoları.
   Kural: video, ekrana girmeden indirilmiyor. Sayfa ilk açılışta hızlı
   kalsın diye poster (afiş) karesi görünüyor, oynatma göründüğünde başlıyor.
   "Hareketi azalt" ayarı açıksa video hiç oynamıyor; afiş karesi kalıyor. */
(function () {
  var videolar = document.querySelectorAll("video[data-luna]");
  if (!videolar.length) return;

  var azalt = window.matchMedia &&
              window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (azalt) return;

  if (!("IntersectionObserver" in window)) {
    videolar.forEach(function (v) { v.play().catch(function () {}); });
    return;
  }
  var gozcu = new IntersectionObserver(function (kayitlar) {
    kayitlar.forEach(function (k) {
      var v = k.target;
      if (k.isIntersecting) {
        if (v.preload !== "auto") { v.preload = "auto"; v.load(); }
        v.play().catch(function () {});
      } else {
        v.pause();
      }
    });
  }, { threshold: 0.25 });

  Array.prototype.forEach.call(videolar, function (v) { gozcu.observe(v); });
})();
