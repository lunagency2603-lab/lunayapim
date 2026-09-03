/* Luna Yapım — AĞAÇ: sayfanın arkasında, kaydırdıkça inilen üç boyutlu ağaç ve dalındaki karga.
   Sıfır bağımlılık, tek canvas. Kural: derinlik (z) paralaks + sis; dallar sayfa boyunca,
   her "dal" durağında (.dal) büyük bir dal ve üzerinde karga. Karga duraklar arasında uçar.
   prefers-reduced-motion: salınım ve uçuş yok, sabit çizim. */
(function () {
  "use strict";
  var c = document.getElementById("agac");
  if (!c || !c.getContext) return;
  var ctx = c.getContext("2d");
  var AZALT = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var DAR = window.innerWidth < 760;
  var BONE = [239, 237, 232], VERM = [232, 69, 44];
  var dpr = Math.min(2, window.devicePixelRatio || 1);
  var W = 0, H = 0, DOC = 0, F = 900;           // F: perspektif odak uzaklığı
  var seg = [], duraklar = [], karga = null, kargaImg = new Image(), kargaHazir = false;
  var t0 = performance.now(), raf = 0, sonY = -1, kirli = true;

  var kargaBone = null;
  kargaImg.onload = function () {
    // logo turuncu; ağaçta kemik rengi siluet olsun
    kargaBone = document.createElement("canvas"); kargaBone.width = kargaImg.naturalWidth; kargaBone.height = kargaImg.naturalHeight;
    var g = kargaBone.getContext("2d"); g.drawImage(kargaImg, 0, 0);
    g.globalCompositeOperation = "source-in"; g.fillStyle = "#EFEDE8"; g.fillRect(0, 0, kargaBone.width, kargaBone.height);
    kargaHazir = true; kirli = true;
  };
  kargaImg.src = (document.body.getAttribute("data-kok") || "") + "assets/karga.png";

  // ---- deterministik rastgele
  var tohum = 7;
  function r() { tohum = (tohum * 1103515245 + 12345) & 0x7fffffff; return tohum / 0x7fffffff; }

  function boyut() {
    W = window.innerWidth; H = window.innerHeight;
    DOC = Math.max(document.documentElement.scrollHeight, H);
    c.width = Math.floor(W * dpr); c.height = Math.floor(H * dpr);
    c.style.width = W + "px"; c.style.height = H + "px";
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    kur();
  }

  // ---- ağaç kurulumu: belge koordinatında (x: -W/2..W/2 merkez, y: belge y, z: derinlik)
  function kur() {
    seg = []; duraklar = []; tohum = 7;
    var d = document.querySelectorAll(".dal, #agac-tepe");
    for (var i = 0; i < d.length; i++) {
      var rc = d[i].getBoundingClientRect();
      duraklar.push({ el: d[i], y: rc.top + window.scrollY + rc.height * (d[i].id === "agac-tepe" ? (DAR ? 0.26 : 0.58) : 0.5), tepe: d[i].id === "agac-tepe" });
    }
    var taban = DOC + 200, tepe = duraklar.length ? duraklar[0].y - H * 0.12 : H * 0.3;
    // gövde: alttan yukarı, hafif kıvrımlı
    var x = W * (DAR ? 0.8 : 0.84), z = 0, y = taban, kal = DAR ? 30 : 58, adim = 90;
    var govde = [];
    while (y > tepe) {
      var ny = y - adim, nx = x + (r() - 0.5) * 34 + Math.sin(y / 900) * 9, nz = z + (r() - 0.5) * 30;
      seg.push({ a: [x, y, z], b: [nx, ny, nz], k: kal, d: 0 });
      govde.push([nx, ny, nz]);
      x = nx; y = ny; z = nz; kal = Math.max(DAR ? 7 : 13, kal * 0.985);
    }
    // duraklara büyük dallar (sağ-sol dönüşümlü), aralara küçük dallar
    var yon = -1;
    for (var j = 0; j < duraklar.length; j++) {
      var dy = duraklar[j].y, g = enYakin(govde, dy);
      var uz = DAR ? W * 0.62 : Math.min(W * 0.36, 520);
      var tepeMi = duraklar[j].tepe;
      var kol = dal(g, [yon < 0 ? -1 : -0.35, tepeMi ? -0.5 : -0.22, (r() - 0.5) * 0.6 + (yon < 0 ? 0 : 0.8)], tepeMi ? uz * (DAR ? 0.9 : 0.62) : (yon < 0 ? uz : uz * 0.7), DAR ? 12 : 20, DAR ? 3 : 4, 1);
      duraklar[j].uc = kol;                     // karganın konacağı nokta
      duraklar[j].yon = yon;
      yon = -yon;
    }
    var say = DAR ? 4 : 12;
    for (var k = 0; k < say; k++) {
      var yy = tepe + (taban - tepe) * (0.06 + 0.9 * (k + 0.5) / say);
      var g2 = enYakin(govde, yy);
      dal(g2, [r() > 0.5 ? 1 : -1, -0.45 + r() * 0.3, (r() - 0.5) * 1.2], DAR ? W * 0.3 : 200 + r() * 200, 6, DAR ? 2 : 3, 1);
    }
    // tepe tacı
    if (duraklar.length && duraklar[0].tepe) {
      var t = govde[govde.length - 1];
      for (var m = 0; m < (DAR ? 4 : 7); m++) dal(t, [(r() - 0.5) * 2, -0.6 - r() * 0.5, (r() - 0.5) * 1.6], 120 + r() * 160, 6, 3, 1);
    }
    seg.sort(function (a, b) { return (b.a[2] + b.b[2]) - (a.a[2] + a.b[2]); });
    kirli = true;
  }
  function enYakin(govde, y) {
    var en = govde[0], f = 1e9;
    for (var i = 0; i < govde.length; i++) { var d = Math.abs(govde[i][1] - y); if (d < f) { f = d; en = govde[i]; } }
    return en;
  }
  // dal: yön vektörüyle özyinelemeli; son ucu döner (karga için)
  function dal(p, v, uz, kal, der, seviye) {
    var n = Math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]) || 1;
    var u = [v[0] / n, v[1] / n, v[2] / n];
    var parca = 3, cur = p, son = p;
    for (var i = 0; i < parca; i++) {
      // hafif kıvrım
      u = [u[0] + (r() - 0.5) * 0.22, u[1] - 0.06 + (r() - 0.5) * 0.18, u[2] + (r() - 0.5) * 0.22];
      var q = [cur[0] + u[0] * uz / parca, cur[1] + u[1] * uz / parca, cur[2] + u[2] * uz / parca];
      seg.push({ a: cur, b: q, k: kal * (1 - i / (parca + 1)), d: seviye });
      cur = q;
    }
    son = cur;
    if (der > 1) {
      var adet = 2 + (r() > 0.6 ? 1 : 0);
      for (var j = 0; j < adet; j++) {
        var w = [u[0] + (r() - 0.5) * 1.1, u[1] - 0.25 + (r() - 0.5) * 0.5, u[2] + (r() - 0.5) * 1.1];
        dal(cur, w, uz * 0.62, kal * 0.62, der - 1, seviye + 1);
      }
    }
    return son;
  }

  // ---- izdüşüm: kamera görünüm merkezinde, z derinliği paralaks verir
  function iz(p, sy) {
    var z = p[2], olc = F / (F + z + 380);
    var x = W * 0.5 + (p[0] - W * 0.5) * olc;
    var y = H * 0.5 + (p[1] - sy - H * 0.5) * olc;
    return [x, y, olc];
  }

  var RENK = [];
  function renk(g) {
    var i = Math.max(0, Math.min(24, Math.round(g * 24)));
    if (!RENK[i]) { var q = i / 24; RENK[i] = "rgb(" + Math.round(10 + 229 * q) + "," + Math.round(10 + 227 * q) + "," + Math.round(12 + 220 * q) + ")"; }
    return RENK[i];
  }
  var sonCiz = 0;
  function ciz(now) {
    raf = 0;
    // 30 kare/sn yeter; mobilde 20
    if (now - sonCiz < (DAR ? 50 : 33)) { if (!AZALT) raf = requestAnimationFrame(ciz); return; }
    sonCiz = now;
    var sy = window.scrollY, zaman = (now - t0) / 1000;
    var salin = AZALT ? 0 : Math.sin(zaman * 0.7) * 3;
    ctx.clearRect(0, 0, W, H);
    ctx.lineCap = "round";
    // uzaktan yakına sırayla çiz (sis için)
    for (var i = 0; i < seg.length; i++) {
      var s = seg[i];
      if (Math.min(s.a[1], s.b[1]) > sy + H + 300 || Math.max(s.a[1], s.b[1]) < sy - 300) continue;
      var a = iz(s.a, sy), b = iz(s.b, sy);
      var w = Math.max(0.6, s.k * a[2]);
      var sis = 0.3 + 0.7 * Math.max(0, Math.min(1, (a[2] - 0.55) / 0.5));
      var ruzgar = salin * (0.4 + s.d * 0.35);
      ctx.strokeStyle = renk(sis * (s.d ? 0.82 : 0.9));
      ctx.lineWidth = w;
      ctx.beginPath(); ctx.moveTo(a[0] + ruzgar * (s.d ? 1 : 0.2), a[1]); ctx.lineTo(b[0] + ruzgar, b[1]); ctx.stroke();
      // uç tomurcuğu: seyrek vermilyon nokta
      if (s.d >= 3 && (i % 7 === 0)) {
        ctx.fillStyle = "rgba(" + VERM.join(",") + "," + (0.55 * sis).toFixed(2) + ")";
        ctx.beginPath(); ctx.arc(b[0] + ruzgar, b[1], 1.6 * a[2], 0, 6.283); ctx.fill();
      }
    }
    // karga: en yakın durağa göre konum; duraklar arasında uçuş
    if (kargaHazir && duraklar.length) {
      var merkez = sy + H * 0.5, k0 = null, k1 = null;
      for (var j = 0; j < duraklar.length; j++) {
        if (duraklar[j].y <= merkez) k0 = duraklar[j];
        if (duraklar[j].y > merkez && !k1) k1 = duraklar[j];
      }
      var p, yon, ucus = 0;
      if (!k0) { p = duraklar[0].uc; yon = duraklar[0].yon; }
      else if (!k1 || AZALT) { p = k0.uc; yon = k0.yon; }
      else {
        var u = (merkez - k0.y) / (k1.y - k0.y);
        // dalda kalma payı: ilk %25 ve son %25 dalda otur, ortada uç
        var f = u < 0.25 ? 0 : u > 0.75 ? 1 : (u - 0.25) / 0.5;
        var e = f * f * (3 - 2 * f);
        var yay = Math.sin(e * Math.PI) * 120;
        p = [k0.uc[0] + (k1.uc[0] - k0.uc[0]) * e, k0.uc[1] + (k1.uc[1] - k0.uc[1]) * e - yay, k0.uc[2] + (k1.uc[2] - k0.uc[2]) * e - yay * 0.6];
        yon = k1.uc[0] >= k0.uc[0] ? 1 : -1; ucus = Math.sin(e * Math.PI);
      }
      var q = iz(p, sy);
      var tepede = k0 && k0.tepe && !ucus;
      var boy = (DAR ? (tepede ? 96 : 64) : (tepede ? 150 : 104)) * q[2];
      ctx.save();
      ctx.globalAlpha = 0.92;
      ctx.translate(q[0] + salin * 0.5, q[1] - boy * 0.78 + (ucus ? Math.sin(zaman * 9) * 4 * ucus : Math.sin(zaman * 1.3) * 1.2));
      ctx.scale(yon, 1);
      if (ucus) ctx.rotate(-0.18 * ucus);
      ctx.drawImage(kargaBone || kargaImg, -boy * 0.5, 0, boy, boy);
      ctx.restore();
      // dal ucunda ince vermilyon vurgu
      ctx.fillStyle = "rgba(232,69,44,.7)"; ctx.beginPath(); ctx.arc(q[0], q[1], 2.2, 0, 6.283); ctx.fill();
    }
    // kaydırma bittikten 2,5 sn sonra dur; her kaydırmada yeniden uyanır (pil ve ana iş parçacığı için)
    if (!AZALT && now < aktifKadar) raf = requestAnimationFrame(ciz);
  }
  var aktifKadar = 0;
  function uyan() { aktifKadar = performance.now() + 2500; if (!raf) raf = requestAnimationFrame(ciz); }
  window.addEventListener("scroll", uyan, { passive: true });
  function baslat() { uyan(); }
  var gorunur = true;
  document.addEventListener("visibilitychange", function () { gorunur = !document.hidden; if (gorunur) baslat(); else if (raf) { cancelAnimationFrame(raf); raf = 0; } });
  window.addEventListener("resize", function () { clearTimeout(window._agacZ); window._agacZ = setTimeout(boyut, 120); });
  function basla() { boyut(); baslat(); document.body.classList.add("agacli"); }
  function bosAnda() { if (window.requestIdleCallback) requestIdleCallback(basla, { timeout: 1200 }); else setTimeout(basla, 200); }
  if (document.readyState === "complete") bosAnda(); else window.addEventListener("load", bosAnda);
})();
