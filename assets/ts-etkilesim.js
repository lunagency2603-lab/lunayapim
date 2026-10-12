/* TrendSaphiens etkileşim modülleri (12.10.2026)
   Kişilik testi · Bilgi testi · Anket · Emoji tepki · En çok okunanlar
   Çerez yok; tekrar oyu tarayıcıdaki localStorage önler. JS kapalıyken bütün
   sorular, seçenekler ve sonuç metinleri sayfada düz metin olarak okunur. */
(function () {
  "use strict";
  var TS = /(^|\.)trendsaphiens\.com$/.test(location.hostname);
  function yol() {
    var y = location.pathname.replace(/\/index\.html$/, "/").replace(/\.html$/, "") || "/";
    return TS ? "/trend" + (y === "/" ? "/" : y) : y;
  }
  function ls(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  function $(s, k) { return (k || document).querySelector(s); }
  function $$(s, k) { return Array.prototype.slice.call((k || document).querySelectorAll(s)); }
  function api(u, govde) {
    var o = govde ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(govde) } : {};
    return fetch(u, o).then(function (r) { if (!r.ok) throw r; return r.json(); });
  }
  document.documentElement.classList.add("ts-js");

  /* ---------- kişilik testi ---------- */
  $$("[data-test]").forEach(function (kok) {
    var sorular = $$(".ts-soru", kok), sonuc = $(".ts-test-sonuc", kok), dug = $(".ts-test-bitir", kok);
    function guncelle() {
      var cev = sorular.filter(function (s) { return $("input:checked", s); }).length;
      dug.disabled = cev < sorular.length;
      dug.textContent = cev < sorular.length ? (sorular.length - cev) + " soru kaldı" : "Sonucumu göster";
    }
    sorular.forEach(function (s, i) {
      $$("input", s).forEach(function (inp) {
        inp.addEventListener("change", function () {
          s.classList.add("cevaplandi"); guncelle();
          var sonraki = sorular[i + 1];
          if (sonraki && !$("input:checked", sonraki)) setTimeout(function () { sonraki.scrollIntoView({ behavior: "smooth", block: "center" }); }, 220);
          else if (!sonraki) setTimeout(function () { dug.scrollIntoView({ behavior: "smooth", block: "center" }); }, 220);
        });
      });
    });
    guncelle();
    dug.addEventListener("click", function () {
      var say = {};
      sorular.forEach(function (s) { var c = $("input:checked", s); if (c) say[c.value] = (say[c.value] || 0) + 1; });
      var en = null;
      Object.keys(say).forEach(function (k) { if (en === null || say[k] > say[en]) en = k; });
      var hedef = $('[data-sonuc="' + en + '"]', kok);
      $$("[data-sonuc]", kok).forEach(function (x) { x.hidden = x !== hedef; });
      sonuc.hidden = false; kok.classList.add("bitti");
      sonuc.scrollIntoView({ behavior: "smooth", block: "start" });
      if (history.replaceState) history.replaceState(null, "", "#sonuc-" + en);
    });
    var t = $(".ts-test-tekrar", kok);
    if (t) t.addEventListener("click", function () {
      $$("input", kok).forEach(function (i) { i.checked = false; });
      $$(".ts-soru", kok).forEach(function (s) { s.classList.remove("cevaplandi"); });
      sonuc.hidden = true; kok.classList.remove("bitti"); guncelle();
      sorular[0].scrollIntoView({ behavior: "smooth", block: "center" });
    });
  });

  /* ---------- bilgi testi ---------- */
  $$("[data-bilgi]").forEach(function (kok) {
    var sorular = $$(".ts-soru", kok), dogru = 0, cevap = 0, son = $(".ts-test-sonuc", kok);
    sorular.forEach(function (s) {
      var d = parseInt(s.getAttribute("data-dogru"), 10);
      $$("input", s).forEach(function (inp) {
        inp.addEventListener("change", function () {
          if (s.classList.contains("cevaplandi")) return;
          s.classList.add("cevaplandi"); cevap++;
          var secilen = parseInt(inp.value, 10);
          if (secilen === d) { dogru++; s.classList.add("dogru"); } else s.classList.add("yanlis");
          $$("label", s).forEach(function (l, j) { if (j === d) l.classList.add("dogru-sik"); if (j === secilen && j !== d) l.classList.add("yanlis-sik"); });
          $$("input", s).forEach(function (x) { x.disabled = true; });
          var a = $(".ts-aciklama", s); if (a) a.hidden = false;
          if (cevap === sorular.length) {
            var p = Math.round(100 * dogru / sorular.length), hedef = null;
            $$("[data-min]", kok).forEach(function (x) { if (p >= parseInt(x.getAttribute("data-min"), 10)) hedef = x; x.hidden = true; });
            if (hedef) hedef.hidden = false;
            $(".ts-skor", kok).textContent = dogru + " / " + sorular.length;
            son.hidden = false;
            setTimeout(function () { son.scrollIntoView({ behavior: "smooth", block: "start" }); }, 400);
          }
        });
      });
    });
  });

  /* ---------- anket ---------- */
  $$("[data-anket]").forEach(function (kok) {
    var id = kok.getAttribute("data-anket"), sec = $$(".ts-anket-sec", kok), n = sec.length, anahtar = "ts-anket:" + id;
    function goster(oy, benim) {
      var top = oy.reduce(function (a, b) { return a + b; }, 0) || 1;
      sec.forEach(function (b, i) {
        var y = Math.round(100 * (oy[i] || 0) / top);
        b.style.setProperty("--oran", y + "%");
        var o = $(".ts-anket-oran", b); if (o) o.textContent = "%" + y;
        b.disabled = true; if (String(i) === String(benim)) b.classList.add("benim");
      });
      kok.classList.add("oylandi");
      var t = $(".ts-anket-toplam", kok); if (t) t.textContent = oy.reduce(function (a, b) { return a + b; }, 0) + " oy";
    }
    var onceki = ls(anahtar);
    if (onceki !== null) api("/api/anket?id=" + id + "&n=" + n).then(function (d) { goster(d.oy, onceki); }).catch(function () {});
    sec.forEach(function (b, i) {
      b.addEventListener("click", function () {
        if (kok.classList.contains("oylandi")) return;
        ls(anahtar, String(i));
        api("/api/anket", { id: id, secim: i, n: n }).then(function (d) { goster(d.oy, i); })
          .catch(function () { var o = []; for (var j = 0; j < n; j++) o.push(j === i ? 1 : 0); goster(o, i); });
      });
    });
  });

  /* ---------- emoji tepki ---------- */
  $$("[data-tepki]").forEach(function (kok) {
    var y = yol(), anahtar = "ts-tepki:" + y, dug = $$("button[data-t]", kok);
    function yaz(sayi) { dug.forEach(function (b) { var s = $("b", b); if (s) s.textContent = sayi[b.getAttribute("data-t")] || 0; }); }
    api("/api/tepki?yol=" + encodeURIComponent(y)).then(function (d) { yaz(d.sayi || {}); }).catch(function () {});
    var onceki = ls(anahtar);
    if (onceki) { kok.classList.add("verildi"); var ob = $('button[data-t="' + onceki + '"]', kok); if (ob) ob.classList.add("benim"); }
    dug.forEach(function (b) {
      b.addEventListener("click", function () {
        if (kok.classList.contains("verildi")) return;
        var t = b.getAttribute("data-t"); ls(anahtar, t);
        kok.classList.add("verildi"); b.classList.add("benim");
        var s = $("b", b); if (s) s.textContent = (parseInt(s.textContent, 10) || 0) + 1;
        api("/api/tepki", { yol: y, tepki: t }).catch(function () {});
      });
    });
  });

  /* ---------- en çok okunanlar ---------- */
  $$("[data-populer]").forEach(function (kok) {
    var dizin = kok.getAttribute("data-dizin"), on = kok.getAttribute("data-on") || "";
    Promise.all([api("/api/populer?on=/trend/"), api(dizin)]).then(function (r) {
      var liste = (r[0].liste || []), d = r[1] || {}, html = "", n = 0;
      liste.forEach(function (x) {
        var slug = x.yol.replace(/^\/trend\//, "");
        var m = d[slug]; if (!m || n >= 6) return; n++;
        html += '<li><a href="' + on + slug + '"><span>' + (n < 10 ? "0" : "") + n + '</span><b>' + m.b + '</b><small>' + m.k + '</small></a></li>';
      });
      if (n >= 3) { $("ol", kok).innerHTML = html; kok.classList.add("canli"); }
    }).catch(function () {});
  });
})();
