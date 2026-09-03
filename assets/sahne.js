/* Sahne — sitenin hareket katmanı. Bağımlılık yok, kütüphane yok.
   1) .gor: görünürken açılma        2) .fener: imleci izleyen ışık
   3) kahraman bölüm sayacı (karga.js olaylarını dinler)
   4) .film-serit: sürükleyerek kaydırma
   5) #tel-kafes: tel kafes 3D bina (canvas, kendi matematiği)
   6) .oncesonra: öncesi/sonrası kaydırıcı   7) .st-sayac: stüdyo bölüm sayacı */
(function () {
  "use strict";
  var AZALT = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* 1 */
  var gor = document.querySelectorAll(".gor");
  if (gor.length) {
    if (AZALT || !("IntersectionObserver" in window)) {
      Array.prototype.forEach.call(gor, function (e) { e.classList.add("gorundu"); });
    } else {
      var go = new IntersectionObserver(function (ks) {
        ks.forEach(function (k) { if (k.isIntersecting) { k.target.classList.add("gorundu"); go.unobserve(k.target); } });
      }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
      Array.prototype.forEach.call(gor, function (e) { go.observe(e); });
    }
  }

  /* 2 */
  Array.prototype.forEach.call(document.querySelectorAll(".fener"), function (b) {
    b.addEventListener("pointermove", function (e) {
      var r = b.getBoundingClientRect();
      b.style.setProperty("--fx", ((e.clientX - r.left) / r.width * 100).toFixed(1) + "%");
      b.style.setProperty("--fy", ((e.clientY - r.top) / r.height * 100).toFixed(1) + "%");
    }, { passive: true });
  });

  /* 3 */
  var hero = document.querySelector(".hero[data-karga]");
  if (hero) {
    var no = hero.querySelector(".hero-bolum b"), ad = hero.querySelector(".hero-bolum span"),
        bar = hero.querySelector(".hero-ilerleme i");
    hero.addEventListener("karga:degisti", function (e) {
      var d = e.detail, n = d.sira + 1;
      if (no) no.innerHTML = "<i>" + (n < 10 ? "0" + n : n) + "</i>/" + (d.toplam < 10 ? "0" + d.toplam : d.toplam);
      if (ad) ad.textContent = d.etiket;
      if (bar) bar.style.width = "0";
    });
    hero.addEventListener("karga:ilerleme", function (e) {
      if (bar) bar.style.width = (e.detail.oran * 100).toFixed(1) + "%";
    });
  }

  /* 4 */
  Array.prototype.forEach.call(document.querySelectorAll(".film-serit"), function (s) {
    var bas = 0, kay = 0, tut = false, hareket = false;
    s.addEventListener("pointerdown", function (e) { tut = true; hareket = false; bas = e.clientX; kay = s.scrollLeft; s.classList.add("tutuyor"); });
    window.addEventListener("pointermove", function (e) {
      if (!tut) return; var dx = e.clientX - bas; if (Math.abs(dx) > 4) hareket = true; s.scrollLeft = kay - dx;
    }, { passive: true });
    window.addEventListener("pointerup", function () { tut = false; s.classList.remove("tutuyor"); });
    s.addEventListener("click", function (e) { if (hareket) { e.preventDefault(); hareket = false; } }, true);
  });

  /* 5 — tel kafes bina: 3D noktalar, döndür, yansıt, çiz. Kütüphane yok. */
  var tk = document.getElementById("tel-kafes");
  if (tk && tk.getContext) {
    var ctx = tk.getContext("2d"), W, H, DPR = Math.min(2, window.devicePixelRatio || 1);
    function boyut() {
      var r = tk.getBoundingClientRect(); W = r.width; H = r.height;
      tk.width = W * DPR; tk.height = H * DPR; ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    }
    boyut(); window.addEventListener("resize", boyut);

    // bina: zemin kat, üst kat (geri çekilmiş), teras, merdiven kütlesi, pencere çizgileri
    var K = [], C = [];
    function kutu(x, y, z, w, h, d) {
      var i = K.length;
      K.push([x, y, z], [x + w, y, z], [x + w, y, z + d], [x, y, z + d],
             [x, y + h, z], [x + w, y + h, z], [x + w, y + h, z + d], [x, y + h, z + d]);
      [[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]].forEach(function (c) { C.push([i + c[0], i + c[1]]); });
      return i;
    }
    kutu(-1.4, 0, -0.9, 2.8, 0.9, 1.8);      // zemin kat
    kutu(-1.1, 0.9, -0.6, 2.0, 0.85, 1.4);   // üst kat
    kutu(0.9, 0, -0.9, 0.5, 1.75, 0.6);      // merdiven kulesi
    kutu(-1.4, 0.9, 0.9, 1.6, 0.06, 0.5);    // teras saçağı
    // pencere çizgileri (zemin kat ön yüz)
    for (var px = -1.1; px < 1.2; px += 0.5) { var a = K.length; K.push([px, 0.2, -0.9], [px, 0.7, -0.9]); C.push([a, a + 1]); }
    // zemin ızgarası
    for (var g = -3; g <= 3; g++) { var b1 = K.length; K.push([g, 0, -3], [g, 0, 3], [-3, 0, g], [3, 0, g]); C.push([b1, b1 + 1], [b1 + 2, b1 + 3]); }

    var aci = 0.6, egim = -0.5, t0 = null, fare = null;
    tk.addEventListener("pointermove", function (e) { var r = tk.getBoundingClientRect(); fare = (e.clientX - r.left) / r.width - 0.5; });
    tk.addEventListener("pointerleave", function () { fare = null; });

    function ciz(ts) {
      if (t0 === null) t0 = ts;
      var t = (ts - t0) / 1000;
      var hedef = fare === null ? 0.6 + t * 0.18 : 0.6 + fare * 2.2;
      aci += (hedef - aci) * (fare === null ? 1 : 0.08);
      ctx.clearRect(0, 0, W, H);
      var ca = Math.cos(aci), sa = Math.sin(aci), ce = Math.cos(egim), se = Math.sin(egim);
      var olc = Math.min(W, H) * 0.3, cx = W / 2, cy = H * 0.68;
      var P = K.map(function (p) {
        var x = p[0] * ca - p[2] * sa, z = p[0] * sa + p[2] * ca, y = p[1];
        var y2 = y * ce - z * se, z2 = y * se + z * ce;
        var per = 1 / (1 + z2 * 0.12);
        return [cx + x * olc * per, cy - y2 * olc * per, z2];
      });
      C.forEach(function (c, i) {
        var a = P[c[0]], b = P[c[1]];
        var zemin = i >= C.length - 14;
        var derin = (a[2] + b[2]) / 2;
        var alfa = zemin ? 0.16 : Math.max(0.25, Math.min(0.95, 0.75 - derin * 0.12));
        ctx.strokeStyle = zemin ? "rgba(239,237,232," + alfa + ")" : "rgba(239,237,232," + alfa + ")";
        ctx.lineWidth = zemin ? 0.6 : 1.1;
        ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke();
      });
      // tarama çizgisi: render "ilerliyor"
      var sy = (t * 0.22 % 1);
      var yy = H * 0.12 + sy * H * 0.76;
      var gr = ctx.createLinearGradient(0, yy - 40, 0, yy + 2);
      gr.addColorStop(0, "rgba(232,69,44,0)"); gr.addColorStop(1, "rgba(232,69,44,.35)");
      ctx.fillStyle = gr; ctx.fillRect(0, yy - 40, W, 42);
      ctx.fillStyle = "rgba(232,69,44,.9)"; ctx.fillRect(0, yy, W, 1);
      // köşe noktaları
      ctx.fillStyle = "#E8452C";
      P.slice(0, 32).forEach(function (p) { ctx.fillRect(p[0] - 1, p[1] - 1, 2, 2); });
      if (!AZALT) requestAnimationFrame(ciz);
    }
    if (AZALT) ciz(0); else requestAnimationFrame(ciz);
  }

  /* 6 */
  Array.prototype.forEach.call(document.querySelectorAll(".oncesonra"), function (k) {
    var g = k.querySelector("input"), vids = k.querySelectorAll("video");
    if (g) g.addEventListener("input", function () { k.style.setProperty("--k", g.value + "%"); });
    // iki video senkron
    if (vids.length === 2) {
      vids[0].addEventListener("play", function () { vids[1].currentTime = vids[0].currentTime; vids[1].play().catch(function () {}); });
      vids[0].addEventListener("pause", function () { vids[1].pause(); });
      setInterval(function () { if (Math.abs(vids[0].currentTime - vids[1].currentTime) > 0.12) vids[1].currentTime = vids[0].currentTime; }, 1000);
    }
  });

  /* 6b — bağlantı kopyala (paylaşım çubuğu) */
  Array.prototype.forEach.call(document.querySelectorAll("[data-kopyala]"), function (b) {
    b.addEventListener("click", function () {
      var u = b.getAttribute("data-kopyala"), eski = b.textContent;
      function tamam() { b.textContent = "Kopyalandı"; setTimeout(function () { b.textContent = eski; }, 1600); }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(u).then(tamam, tamam);
      else { var t = document.createElement("textarea"); t.value = u; document.body.appendChild(t); t.select(); try { document.execCommand("copy"); } catch (e) {} document.body.removeChild(t); tamam(); }
    });
  });

  /* 7 */
  var sayac = document.querySelector(".st-sayac b"), bolumler = document.querySelectorAll(".st-bolum");
  if (sayac && bolumler.length && "IntersectionObserver" in window) {
    var so = new IntersectionObserver(function (ks) {
      ks.forEach(function (k) { if (k.isIntersecting) sayac.textContent = k.target.getAttribute("data-bolum") || ""; });
    }, { threshold: 0.5 });
    Array.prototype.forEach.call(bolumler, function (b) { so.observe(b); });
  }
})();
