/* Luna okuma sayacı — çerezsiz, kimliksiz.
   Ne sayıyor: sayfa gerçekten OKUNDUYSA (15 sn + %25 kaydırma) bir kez.
   Ne göndermiyor: IP, kimlik, çerez. Aynı tarayıcıdan 6 saat içinde tekrar saymıyor.
   Panel bu sayıları /api/okuma üzerinden okuyor. */
(function () {
  "use strict";
  if (location.hostname !== "lunayapim.com" && location.hostname !== "www.lunayapim.com") return;
  var yol = location.pathname.replace(/\/index\.html$/, "/").replace(/\.html$/, "") || "/";
  var anahtar = "luna-okuma:" + yol, simdi = Date.now();
  try {
    var son = parseInt(localStorage.getItem(anahtar) || "0", 10);
    if (simdi - son < 6 * 3600 * 1000) return;
  } catch (e) {}
  var sure = false, kaydirma = false, gitti = false;
  setTimeout(function () { sure = true; dene(); }, 15000);
  function olc() {
    var h = document.documentElement.scrollHeight - window.innerHeight;
    if (h <= 0 || window.scrollY / h >= 0.25) { kaydirma = true; dene(); }
  }
  window.addEventListener("scroll", olc, { passive: true });
  setTimeout(olc, 1000);
  function dene() {
    if (gitti || !sure || !kaydirma) return;
    gitti = true;
    try { localStorage.setItem(anahtar, String(simdi)); } catch (e) {}
    var veri = JSON.stringify({ yol: yol, kaynak: (document.referrer || "").split("/")[2] || "" });
    try {
      if (navigator.sendBeacon) navigator.sendBeacon("/api/okuma", new Blob([veri], { type: "application/json" }));
      else fetch("/api/okuma", { method: "POST", body: veri, headers: { "Content-Type": "application/json" }, keepalive: true });
    } catch (e) {}
  }
})();
