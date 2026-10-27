/* Luna okuma sayacı — çerezsiz, kimliksiz.
   Ne sayıyor: sayfa gerçekten OKUNDUYSA (15 sn + %25 kaydırma) bir kez;
   ayrıca ziyaretçi telefon / WhatsApp / e-posta bağlantısına tıklarsa ya da form gönderirse bir kez.
   Ne göndermiyor: IP, kimlik, çerez. Aynı tarayıcıdan 6 saat içinde aynı sayfayı tekrar saymıyor.
   Panel bu sayıları /api/okuma üzerinden okuyor. */
(function () {
  "use strict";
  var TS = /(^|\.)trendsaphiens\.com$/.test(location.hostname);
  if (!TS && location.hostname !== "lunayapim.com" && location.hostname !== "www.lunayapim.com") return;
  var yol = location.pathname.replace(/\/index\.html$/, "/").replace(/\.html$/, "") || "/";
  if (TS) yol = "/trend" + (yol === "/" ? "/" : yol);  // panel anahtarları trendsaphiens.com için de /trend/... kalır

  function gonder(veri) {
    var v = JSON.stringify(veri);
    try {
      if (navigator.sendBeacon) navigator.sendBeacon("/api/okuma", new Blob([v], { type: "application/json" }));
      else fetch("/api/okuma", { method: "POST", body: v, headers: { "Content-Type": "application/json" }, keepalive: true });
    } catch (e) {}
  }

  // --- tıklama: iletişim bağlantıları ve form gönderimi (sayfa başına her türden bir kez)
  var sayildi = {};
  function olay(tur) {
    if (sayildi[tur]) return;
    sayildi[tur] = true;
    gonder({ yol: yol, olay: tur });
  }
  document.addEventListener("click", function (e) {
    var a = e.target && e.target.closest ? e.target.closest("a[href]") : null;
    if (!a) return;
    var h = (a.getAttribute("href") || "").toLowerCase();
    if (h.indexOf("tel:") === 0) olay("tel");
    else if (h.indexOf("mailto:") === 0) olay("eposta");
    else if (h.indexOf("wa.me/") >= 0 || h.indexOf("api.whatsapp.com") >= 0 || h.indexOf("whatsapp://") === 0) olay("whatsapp");
  }, true);
  document.addEventListener("submit", function () { olay("form"); }, true);

  // --- okuma: 15 sn + %25 kaydırma, 6 saatte bir
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
    gonder({ yol: yol, kaynak: (document.referrer || "").split("/")[2] || "" });
  }
})();
