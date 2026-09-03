/* Luna Yapım — FON: fotogerçekçi sahne, 2,5 boyut.
   Aynı fotoğraftan iki katman (arka: sisli orman; ön: karga ve dalı — karga dalından hiç ayrılmaz),
   kaydırma ve fareyle farklı hızlarda kayar (paralaks), üstünde yavaş akan sis.
   Tek sahne, tek ışık, tutarlı derinlik. Kaydırma yumuşatılır; kaydırma bitince hesap durur. */
(function () {
  "use strict";
  var fon = document.getElementById("fon");
  if (!fon) return;
  var arka = fon.querySelector(".fon-arka"), on = fon.querySelector(".fon-on"), perde = fon.querySelector(".fon-perde");
  var AZALT = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var DAR = window.innerWidth < 760;
  var webp = false; try { webp = document.createElement("canvas").toDataURL("image/webp").indexOf("data:image/webp") === 0; } catch (e) {}
  var onSrc = on.getAttribute(DAR ? "data-k" : "data-b");
  if (webp) onSrc = onSrc.replace(".png", ".webp");
  arka.src = arka.getAttribute(DAR ? "data-k" : "data-b"); on.src = onSrc;

  var DOC = 1, sy = 0, syIlk = true, fare = { x: 0, y: 0 }, fareY = { x: 0, y: 0 };
  var raf = 0, aktifKadar = 0, son = performance.now(), t0 = son;
  function olc() { DOC = Math.max(document.documentElement.scrollHeight - window.innerHeight, 1); }
  function ihtiyac() { aktifKadar = performance.now() + 2200; if (!raf) raf = requestAnimationFrame(adim); }

  function adim(now) {
    raf = 0;
    var dt = Math.min(0.1, (now - son) / 1000); son = now;
    var hedef = window.scrollY;
    if (syIlk || AZALT) { sy = hedef; syIlk = false; } else sy += (hedef - sy) * (1 - Math.pow(0.0003, dt));
    if (Math.abs(hedef - sy) < 0.05) sy = hedef;
    var kf = 1 - Math.pow(0.02, dt); fareY.x += (fare.x - fareY.x) * kf; fareY.y += (fare.y - fareY.y) * kf;
    var p = Math.max(0, Math.min(1, sy / DOC));         // sayfa ilerlemesi 0..1
    var z = (now - t0) / 1000;
    // çok yavaş nefes (kamera eli) — hareket azaltmada yok
    var nefes = AZALT ? 0 : Math.sin(z * 0.35) * 3;
    // arka: yavaş kayar, hafif büyür (kamera ileri/aşağı iner hissi)
    var ax = -fareY.x * (DAR ? 0 : 14) + nefes * 0.3, ay = -p * 70 - fareY.y * (DAR ? 0 : 8), as = 1.10 + p * 0.05;
    // ön: daha hızlı kayar ve büyür → derinlik; karga dalıyla birlikte
    var ox = -fareY.x * (DAR ? 0 : 38) + nefes, oy = -p * 190 - fareY.y * (DAR ? 0 : 20), os = 1.04 + p * 0.10;
    arka.style.transform = "translate3d(" + ax.toFixed(2) + "px," + ay.toFixed(2) + "px,0) scale(" + as.toFixed(4) + ")";
    on.style.transform = "translate3d(" + ox.toFixed(2) + "px," + oy.toFixed(2) + "px,0) scale(" + os.toFixed(4) + ")";
    // aşağı indikçe sahne hafif kararır ve maviye kayar (akşam ilerler)
    if (perde) perde.style.opacity = (0.08 + p * 0.42).toFixed(3);
    if (!AZALT && now < aktifKadar) raf = requestAnimationFrame(adim);
  }

  window.addEventListener("scroll", ihtiyac, { passive: true });
  window.addEventListener("pointermove", function (e) { if (e.pointerType === "touch" || DAR) return; fare.x = e.clientX / window.innerWidth - 0.5; fare.y = e.clientY / window.innerHeight - 0.5; ihtiyac(); }, { passive: true });
  window.addEventListener("resize", function () { clearTimeout(window._fonZ); window._fonZ = setTimeout(function () { olc(); ihtiyac(); }, 150); });
  document.addEventListener("visibilitychange", function () { if (!document.hidden) ihtiyac(); });
  on.addEventListener("load", function () { fon.classList.add("fon-hazir"); ihtiyac(); });
  olc(); ihtiyac();
  if (document.readyState !== "complete") window.addEventListener("load", function () { olc(); ihtiyac(); });
  document.body.classList.add("agacli");
})();
