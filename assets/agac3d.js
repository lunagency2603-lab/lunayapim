/* Luna Yapım — AĞAÇ 3B (WebGL / three.js r128, kendi sunucumuzdan).
   Sayfanın arkasında gerçek üç boyutlu, kabuk dokulu, sisli bir ağaç; kamera kaydırdıkça
   gövde boyunca aşağı iner ve ağacın etrafında yavaşça döner. Her "dal" durağında (.dal, #agac-tepe)
   kameraya dönük büyük bir dal ve üzerinde karga (fotogerçekçi kesit). Karga duraklar arasında uçar.
   WebGL yoksa 2B çizim (agac.js) devreye girer. Kaydırma bitince çizim durur (pil). */
(function () {
  "use strict";
  var c = document.getElementById("agac");
  if (!c) return;
  var KOK = (function () { var h = document.querySelector('link[href*="luna.css"]'); return h ? h.getAttribute("href").replace(/luna\.css.*$/, "") : "assets/"; })();
  function yedek() { var s = document.createElement("script"); s.src = KOK + "agac.js?v=2"; s.defer = true; document.body.appendChild(s); }
  if (!window.THREE) { yedek(); return; }
  var T = window.THREE, renderer;
  try {
    renderer = new T.WebGLRenderer({ canvas: c, alpha: true, antialias: true, powerPreference: "high-performance" });
  } catch (e) { yedek(); return; }
  var AZALT = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var DAR = window.innerWidth < 760;
  var dpr = Math.min(DAR ? 1.5 : 2, window.devicePixelRatio || 1);
  renderer.setPixelRatio(dpr);
  renderer.outputEncoding = T.sRGBEncoding;
  renderer.toneMapping = T.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.25;
  renderer.shadowMap.enabled = !DAR;
  renderer.shadowMap.type = T.PCFSoftShadowMap;
  renderer.setClearColor(0x000000, 0);

  var scene = new T.Scene();
  scene.fog = new T.FogExp2(0x0a0a0c, DAR ? 0.06 : 0.048);
  var cam = new T.PerspectiveCamera(DAR ? 46 : 38, 1, 0.1, 120);

  // ---- ışık: arkadan amber kenar ışığı (karga klibiyle aynı dil), önden soğuk dolgu, gökten loş
  var hemi = new T.HemisphereLight(0x8d97ad, 0x14120f, 1.0); scene.add(hemi);
  var anahtar = new T.DirectionalLight(0xe8a05a, 1.6); anahtar.position.set(-6, 14, -9);
  anahtar.castShadow = !DAR; anahtar.shadow.mapSize.set(2048, 2048);
  anahtar.shadow.camera.near = 1; anahtar.shadow.camera.far = 60; anahtar.shadow.bias = -0.0008;
  anahtar.shadow.camera.left = -14; anahtar.shadow.camera.right = 14; anahtar.shadow.camera.top = 14; anahtar.shadow.camera.bottom = -14;
  scene.add(anahtar); scene.add(anahtar.target);
  var dolgu = new T.DirectionalLight(0x8f9ab5, 0.7); dolgu.position.set(8, 6, 10); scene.add(dolgu);
  var vurgu = new T.PointLight(0xe8452c, 0.0, 12); scene.add(vurgu);   // karganın yanında, çok hafif

  // ---- deterministik rastgele
  var tohum = 11;
  function r() { tohum = (tohum * 1103515245 + 12345) & 0x7fffffff; return tohum / 0x7fffffff; }

  // ---- dünya ölçüsü: ağaç 0..TEPE; belge y → dünya y
  var TEPE = 42, DOC = 1, duraklar = [];
  function dunyaY(docY) { return (TEPE - 7) - (docY / DOC) * (TEPE - 4); }

  // ---- kabuk dokusu (yüklenemezse yordamsal)
  var yukleyici = new T.TextureLoader();
  var kabuk = yukleyici.load(KOK + "agac/kabuk.jpg", function (t) { t.wrapS = t.wrapT = T.RepeatWrapping; t.anisotropy = renderer.capabilities.getMaxAnisotropy(); t.encoding = T.sRGBEncoding; t.needsUpdate = true; ihtiyac(); });
  kabuk.wrapS = kabuk.wrapT = T.RepeatWrapping;
  var kabukN = yukleyici.load(KOK + "agac/kabuk-n.jpg", function (t) { t.wrapS = t.wrapT = T.RepeatWrapping; ihtiyac(); });
  kabukN.wrapS = kabukN.wrapT = T.RepeatWrapping;
  var malzeme = new T.MeshStandardMaterial({ map: kabuk, normalMap: kabukN, normalScale: new T.Vector2(0.9, 0.9), color: 0x9a8f84, roughness: 0.96, metalness: 0.0 });

  // ---- konik boru: eğri + yarıçap fonksiyonu → geometri parçaları (tek meshe birleştirilir)
  var POS = [], NOR = [], UV = [], IDX = [], tepeNokta = [];
  function boru(noktalar, r0, r1, radyal, uvOlcek) {
    var egri = new T.CatmullRomCurve3(noktalar), n = Math.max(3, Math.round(egri.getLength() * (DAR ? 1.6 : 2.2)));
    var kare = egri.computeFrenetFrames(n, false), taban = POS.length / 3;
    for (var i = 0; i <= n; i++) {
      var t = i / n, p = egri.getPointAt(t), rad = r0 + (r1 - r0) * t;
      var N = kare.normals[i] || kare.normals[n - 1], B = kare.binormals[i] || kare.binormals[n - 1];
      for (var j = 0; j <= radyal; j++) {
        var a = (j / radyal) * Math.PI * 2, cx = Math.cos(a), sx = Math.sin(a);
        var nx = cx * N.x + sx * B.x, ny = cx * N.y + sx * B.y, nz = cx * N.z + sx * B.z;
        POS.push(p.x + nx * rad, p.y + ny * rad, p.z + nz * rad); NOR.push(nx, ny, nz);
        UV.push(j / radyal * (rad * 6 + 0.5), t * egri.getLength() * uvOlcek);
      }
    }
    for (var i2 = 0; i2 < n; i2++) for (var j2 = 0; j2 < radyal; j2++) {
      var a0 = taban + i2 * (radyal + 1) + j2, b0 = a0 + radyal + 1;
      IDX.push(a0, b0, a0 + 1, b0, b0 + 1, a0 + 1);
    }
    return egri;
  }

  // dal: başlangıç, yön, uzunluk, yarıçap, derinlik → uç noktası
  function dal(p, v, uz, rad, der, seviye) {
    v = v.clone().normalize();
    var nokta = [p.clone()], cur = p.clone(), u = v.clone(), parca = 4;
    for (var i = 0; i < parca; i++) {
      u.x += (r() - 0.5) * 0.35; u.z += (r() - 0.5) * 0.35; u.y += 0.05 + (r() - 0.5) * 0.25 - (seviye > 2 ? 0.08 : 0);  // hafif yukarı eğilim, uçlarda sarkma
      u.normalize();
      cur = cur.clone().addScaledVector(u, uz / parca); nokta.push(cur.clone());
    }
    boru(nokta, rad, rad * (der > 1 ? 0.55 : 0.15), seviye > 2 ? 4 : 6, 0.9);
    if (der > 1) {
      var adet = seviye === 1 ? 3 : 2 + (r() > 0.5 ? 1 : 0);
      for (var j = 0; j < adet; j++) {
        var w = u.clone(); w.x += (r() - 0.5) * 1.6; w.z += (r() - 0.5) * 1.6; w.y += 0.1 + (r() - 0.5) * 0.9;
        var bas = nokta[Math.min(nokta.length - 1, 2 + Math.floor(r() * 2))];
        dal(bas, w, uz * 0.62, rad * 0.55, der - 1, seviye + 1);
      }
    } else tepeNokta.push(cur.clone());
    return cur;
  }

  var govdeEgri = null, agacMesh = null;
  var kurSure = 0;
  function agacKur() {
    var t1 = performance.now();
    POS = []; NOR = []; UV = []; IDX = []; tepeNokta = []; tohum = 11;
    // gövde: hafif kıvrımlı, 0'dan tepeye
    var gp = [new T.Vector3(0, -3, 0)];
    for (var y = 2; y <= TEPE; y += 5) gp.push(new T.Vector3(Math.sin(y * 0.23) * 0.9 + (r() - 0.5) * 0.5, y, Math.cos(y * 0.19) * 0.7 + (r() - 0.5) * 0.5));
    govdeEgri = boru(gp, 1.05, 0.14, DAR ? 8 : 10, 0.7);
    // duraklara kameraya dönük büyük dallar
    for (var i = 0; i < duraklar.length; i++) {
      var d = duraklar[i], th = kameraAci(d.docY), gy = govdeNokta(d.wy);
      var yon = new T.Vector3(Math.sin(th) * 0.95 + (r() - 0.5) * 0.3, d.tepe ? 0.3 : 0.22, Math.cos(th) * 0.95 + (r() - 0.5) * 0.3);
      var uc = dal(gy, yon, d.tepe ? 3.6 : 4.6, d.tepe ? 0.16 : 0.24, 3, 1);
      d.uc = uc; d.aci = th;
    }
    // ara dallar
    var say = DAR ? 9 : 16;
    for (var k = 0; k < say; k++) {
      var wy = 4 + (TEPE - 8) * (k + 0.5) / say, a = r() * Math.PI * 2;
      dal(govdeNokta(wy), new T.Vector3(Math.sin(a), 0.35 + r() * 0.4, Math.cos(a)), 2.6 + r() * 2.2, 0.12 + r() * 0.1, DAR ? 2 : 3, 1);
    }
    // taç
    for (var m = 0; m < (DAR ? 5 : 8); m++) { var a2 = r() * Math.PI * 2; dal(govdeNokta(TEPE - 0.5), new T.Vector3(Math.sin(a2) * 0.7, 0.9 + r() * 0.5, Math.cos(a2) * 0.7), 2.4 + r() * 1.6, 0.11, 3, 1); }
    var g = new T.BufferGeometry();
    g.setAttribute("position", new T.Float32BufferAttribute(POS, 3));
    g.setAttribute("normal", new T.Float32BufferAttribute(NOR, 3));
    g.setAttribute("uv", new T.Float32BufferAttribute(UV, 2));
    g.setIndex(IDX);
    if (agacMesh) { scene.remove(agacMesh); agacMesh.geometry.dispose(); }
    agacMesh = new T.Mesh(g, malzeme); agacMesh.castShadow = !DAR; agacMesh.receiveShadow = !DAR; scene.add(agacMesh);
    // uç tomurcukları: seyrek vermilyon yapraklar (kimlik rengi, az)
    yaprakKur();
    kurSure = performance.now() - t1;
  }
  function govdeNokta(wy) { var t = Math.max(0, Math.min(1, (wy + 3) / (TEPE + 3))); return govdeEgri.getPointAt(t); }
  function kameraAci(docY) { return -0.35 + (docY / DOC) * 1.5; }

  var yaprak = null;
  function yaprakKur() {
    if (yaprak) { scene.remove(yaprak); yaprak.geometry.dispose(); }
    var n = Math.min(tepeNokta.length, DAR ? 24 : 48), geo = new T.PlaneGeometry(0.09, 0.14);
    var mat = new T.MeshStandardMaterial({ color: 0xe8452c, roughness: 0.7, side: T.DoubleSide, emissive: 0x3a0d06, emissiveIntensity: 0.35 });
    yaprak = new T.InstancedMesh(geo, mat, n); var o = new T.Object3D();
    for (var i = 0; i < n; i++) { var p = tepeNokta[Math.floor(r() * tepeNokta.length)]; o.position.copy(p); o.rotation.set(r() * 3, r() * 3, r() * 3); o.updateMatrix(); yaprak.setMatrixAt(i, o.matrix); }
    scene.add(yaprak);
  }

  // ---- toz / sis parçacıkları
  var toz = (function () {
    var n = DAR ? 220 : 520, a = new Float32Array(n * 3);
    for (var i = 0; i < n; i++) { a[i * 3] = (r() - 0.5) * 24; a[i * 3 + 1] = r() * (TEPE + 6) - 3; a[i * 3 + 2] = (r() - 0.5) * 24; }
    var g = new T.BufferGeometry(); g.setAttribute("position", new T.BufferAttribute(a, 3));
    var m = new T.PointsMaterial({ color: 0xcfc9bd, size: 0.055, transparent: true, opacity: 0.35, depthWrite: false, sizeAttenuation: true });
    var p = new T.Points(g, m); scene.add(p); return p;
  })();

  // ---- karga: fotogerçekçi kesit (sprite), kameraya bakar
  var karga = null, kargaHazir = false, kargaTex = yukleyici.load(KOK + "agac/karga.png", function (t) { t.encoding = T.sRGBEncoding; kargaHazir = true; ihtiyac(); });
  karga = new T.Sprite(new T.SpriteMaterial({ map: kargaTex, transparent: true, depthWrite: false, fog: true }));
  karga.scale.set(1.25, 1.25, 1); karga.center.set(0.5, 0.06); scene.add(karga);

  // ---- duraklar ve boyut
  function boyut() {
    var W = window.innerWidth, H = window.innerHeight;
    DOC = Math.max(document.documentElement.scrollHeight - H, 1);
    renderer.setSize(W, H, false); c.style.width = W + "px"; c.style.height = H + "px";
    cam.aspect = W / H; cam.updateProjectionMatrix();
    duraklar = [];
    var d = document.querySelectorAll("#agac-tepe, .dal");
    for (var i = 0; i < d.length; i++) {
      var rc = d[i].getBoundingClientRect(), tepe = d[i].id === "agac-tepe";
      var docY = rc.top + window.scrollY + rc.height * (tepe ? (DAR ? 0.2 : 0.45) : 0.5) - H * 0.5;
      duraklar.push({ docY: Math.max(0, docY), wy: dunyaY(Math.max(0, docY)), tepe: tepe });
    }
    agacKur(); ihtiyac();
  }

  // ---- kamera: gövde boyunca iner, etrafında döner
  var hedef = new T.Vector3(), bakis = new T.Vector3(), kamPos = new T.Vector3(), ilk = true;
  function kamera(sy, dt) {
    var wy = dunyaY(sy), th = kameraAci(sy), R = DAR ? 7.2 : 8.4;
    var g = govdeNokta(wy);
    kamPos.set(g.x + Math.sin(th) * R, wy + 0.9, g.z + Math.cos(th) * R);
    var yukari = sy < 400 ? (1 - sy / 400) * 0.9 : 0;
    bakis.set(g.x + Math.sin(th) * 1.2, wy + 0.15 + yukari, g.z + Math.cos(th) * 1.2);
    // durağa yaklaşınca bakış kargaya kayar (karga hep kadraj ortasında)
    var enYakin = null, mesafe = 1e9, H = window.innerHeight;
    for (var i = 0; i < duraklar.length; i++) { var m = Math.abs(sy - duraklar[i].docY); if (m < mesafe) { mesafe = m; enYakin = duraklar[i]; } }
    if (enYakin && enYakin.uc && mesafe < H * 0.6) {
      var w = 1 - mesafe / (H * 0.6); w = w * w * (3 - 2 * w);
      var hedefNokta = new T.Vector3(enYakin.uc.x, enYakin.uc.y + 0.35, enYakin.uc.z);
      if (enYakin.tepe && !DAR) hedefNokta.add(new T.Vector3(-Math.cos(th), 0, Math.sin(th)).multiplyScalar(1.7));  // tepede karga sağda, yazı solda
      bakis.lerp(hedefNokta, w * 0.85);
      kamPos.y += (enYakin.uc.y + 0.9 - kamPos.y) * w * 0.6;
    }
    if (ilk || AZALT) { cam.position.copy(kamPos); hedef.copy(bakis); ilk = false; }
    else { var k = 1 - Math.pow(0.001, dt); cam.position.lerp(kamPos, k); hedef.lerp(bakis, k); }
    cam.lookAt(hedef);
    // gölge kamerası ve ışıklar kamerayla birlikte insin
    anahtar.position.set(g.x - 6, wy + 14, g.z - 9); anahtar.target.position.set(g.x, wy, g.z);
    dolgu.position.set(kamPos.x + 3, wy + 5, kamPos.z + 2);
  }

  // ---- karga konumu: durak → durak uçuş
  var ucusVek = new T.Vector3(), tmp = new T.Vector3();
  function kargaYerlestir(sy, zaman) {
    if (!duraklar.length) return;
    var k0 = null, k1 = null;
    for (var j = 0; j < duraklar.length; j++) { if (duraklar[j].docY <= sy) k0 = duraklar[j]; if (duraklar[j].docY > sy && !k1) k1 = duraklar[j]; }
    var p, ucus = 0;
    if (!k0) p = duraklar[0].uc;
    else if (!k1 || AZALT) p = k0.uc;
    else {
      var u = (sy - k0.docY) / (k1.docY - k0.docY), f = u < 0.28 ? 0 : u > 0.72 ? 1 : (u - 0.28) / 0.44, e = f * f * (3 - 2 * f);
      ucus = Math.sin(e * Math.PI);
      tmp.copy(k0.uc).lerp(k1.uc, e); tmp.y += ucus * 2.2;
      // uçarken kameraya biraz yaklaş
      tmp.addScaledVector(ucusVek.subVectors(cam.position, tmp).normalize(), ucus * 1.2);
      p = tmp;
    }
    karga.position.copy(p);
    karga.position.y += ucus ? Math.sin(zaman * 11) * 0.08 * ucus : Math.sin(zaman * 1.4) * 0.012;
    karga.material.rotation = ucus ? -0.22 * ucus : 0;
    var olc = ucus ? 1.25 + 0.35 * ucus : 1.25; karga.scale.set(olc, olc, 1);
    vurgu.position.copy(p).add(new T.Vector3(0.6, 0.9, 0.6)); vurgu.intensity = 0.35 + 0.25 * ucus;
  }

  // ---- çizim döngüsü: kaydırma bitince 2,5 sn sonra durur
  var raf = 0, aktifKadar = 0, son = performance.now(), t0 = son;
  function ihtiyac() { aktifKadar = performance.now() + 2500; if (!raf) raf = requestAnimationFrame(ciz); }
  function ciz(now) {
    raf = 0;
    if (!govdeEgri) return;
    var dt = Math.min(0.1, (now - son) / 1000); son = now;
    var sy = window.scrollY, zaman = (now - t0) / 1000;
    kamera(sy, dt);
    kargaYerlestir(sy, zaman);
    if (!AZALT) { toz.rotation.y = zaman * 0.012; agacMesh && (agacMesh.rotation.z = Math.sin(zaman * 0.5) * 0.0025); }
    renderer.render(scene, cam);
    if (!AZALT && now < aktifKadar) raf = requestAnimationFrame(ciz);
  }
  window.addEventListener("scroll", ihtiyac, { passive: true });
  window.addEventListener("resize", function () { clearTimeout(window._agacZ); window._agacZ = setTimeout(boyut, 150); });
  document.addEventListener("visibilitychange", function () { if (!document.hidden) ihtiyac(); });
  function basla() { boyut(); document.body.classList.add("agacli"); }
  if (document.readyState === "complete") basla(); else window.addEventListener("load", basla);
  window.__agac3d = true; window.__agacDbg = { karga: karga, cam: cam, duraklar: function () { return duraklar; }, snap: function () { ilk = true; ihtiyac(); }, sure: function () { return kurSure; }, ucgen: function () { return agacMesh ? agacMesh.geometry.index.count / 3 : 0; } };
})();
