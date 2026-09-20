/* ============================================================
   LUNA YAPIM — TASARIM STÜDYOSU
   ------------------------------------------------------------
   Ziyaretçi ürünü ve rengini seçer, hazır bir tasarım alır ya da
   kendi dosyasını açar, yazıyı ve yerleşimi ayarlar, sonucu ürünün
   üzerinde görür. "Sipariş ver" tek bir mesaj üretir; önizleme
   görseli tarayıcıda hazırlanır, kullanıcı indirip mesaja ekler.

   Sunucu yok: hiçbir dosya yüklenmiyor, hiçbir şey saklanmıyor.

   Kullanım:  <div data-studyo="baskili-tisort"></div>
              <script src="../assets/hediye-katalog.js"></script>
              <script src="../assets/hediye-studyo.js" defer></script>
   ============================================================ */
(function () {
  "use strict";
  var K = window.LUNA_HEDIYE;
  if (!K) return;

  var ns = "http://www.w3.org/2000/svg";
  function el(t, s, c) { var e = document.createElement(t); if (s) e.className = s; if (c != null) e.innerHTML = c; return e; }
  function kacir(s) { return K.kacir(s); }
  function kisitla(v, a, b) { return Math.max(a, Math.min(b, v)); }

  /* ---------- tasarım → SVG ---------- */
  function tasarimIc(id, o) {
    var t = K.tasarimlar[id];
    if (!t) return "";
    return t.ciz(o);
  }

  // Tasarımı ölçüp kendi sınırlarına oturan SVG üretir.
  // Ölçüm için geçici bir SVG DOM'a konur (getBBox yalnız render edilmiş
  // ögede çalışır); ölçülemezse 0 0 100 100 kullanılır.
  var olcuKabi = null;
  function olcuHazirla() {
    if (olcuKabi) return olcuKabi;
    olcuKabi = document.createElementNS(ns, "svg");
    olcuKabi.setAttribute("viewBox", "0 0 100 100");
    olcuKabi.setAttribute("width", "100"); olcuKabi.setAttribute("height", "100");
    olcuKabi.style.cssText = "position:absolute;left:-9999px;top:0;width:100px;height:100px;visibility:hidden";
    document.body.appendChild(olcuKabi);
    return olcuKabi;
  }

  function svgUret(id, o, tamBoy) {
    var ic = tasarimIc(id, o);
    var vb = [0, 0, 100, 100];
    try {
      var k = olcuHazirla();
      k.innerHTML = '<g id="lhs-olc">' + ic + "</g>";
      var g = k.querySelector("#lhs-olc");
      var b = g.getBBox();
      if (b && b.width > .5 && b.height > .5) {
        var p = Math.max(b.width, b.height) * 0.03;
        vb = [b.x - p, b.y - p, b.width + p * 2, b.height + p * 2];
      }
      k.innerHTML = "";
    } catch (e) { /* ölçülemedi — tam kare */ }
    var oran = vb[2] / vb[3];
    var w = tamBoy ? (oran >= 1 ? 1200 : 1200 * oran) : null;
    var boyut = tamBoy ? ' width="' + Math.round(w) + '" height="' + Math.round(w / oran) + '"' : ' width="100%" height="100%"';
    return {
      svg: '<svg xmlns="' + ns + '" viewBox="' + vb.map(function (n) { return +n.toFixed(2); }).join(" ") +
        '" preserveAspectRatio="xMidYMid meet"' + boyut + ">" + ic + "</svg>",
      oran: oran
    };
  }

  /* ---------- baskı alanı ---------- */
  function alanDik(u, varyant, alan) {
    if (varyant.alan && varyant.alan[alan.id]) return varyant.alan[alan.id];
    return alan.r;
  }

  /* ---------- tek kare kompozisyon (vitrin kartı) ---------- */
  function kompozisyon(kutu, urunId, k) {
    var u = K.urunler[urunId]; if (!u) return;
    var v = u.varyantlar.filter(function (x) { return x.id === k.varyant; })[0] || u.varyantlar[0];
    var a = u.alanlar.filter(function (x) { return x.id === k.alan; })[0] || u.alanlar[0];
    var m = K.murekkepler.filter(function (x) { return x.id === k.murekkep; })[0] || K.murekkepler[0];
    var t = K.tasarimlar[k.tasarim];
    var metin = {};
    (t.alanlar || []).forEach(function (f) { metin[f.id] = (k.metin && k.metin[f.id]) || f.varsayilan; });
    var r = alanDik(u, v, a);
    var s = svgUret(k.tasarim, { renk: m.renk, vurgu: m.vurgu, metin: metin, foto: null });
    kutu.innerHTML =
      '<img class="hs-urun" src="' + K.gorselKok + v.g + '" alt="' + kacir(u.ad + " — " + v.ad) + '" loading="lazy" decoding="async">' +
      '<div class="hs-cerceve" style="left:' + r.x + '%;top:' + r.y + '%;width:' + r.w + '%;height:' + r.h + '%">' +
      '<div class="hs-katman" style="mix-blend-mode:' + K.karisimSec(v, m) +
      ';transform:translate(-50%,-50%) scale(' + (k.olcek || .9) + ')">' + s.svg + "</div></div>";
  }

  /* ---------- stüdyo ---------- */
  function Studyo(kok, urunId) {
    var u = K.urunler[urunId];
    if (!u) { kok.innerHTML = '<p class="hs-yok">Bu ürün için stüdyo tanımlı değil.</p>'; return; }

    var ilkT = u.tasarimlar[0];
    var d = {
      varyant: u.varyantlar[0].id,
      alan: u.alanlar[0].id,
      tasarim: ilkT,
      murekkep: u.varyantlar[0].murekkep,
      metin: {},
      kendi: null, kendiAd: "", foto: null, fotoAd: "",
      x: 50, y: 50, olcek: .9, aci: 0,
      secim: {}, adet: 1, not: "", ad: "", tel: ""
    };
    u.secimler.forEach(function (s) { d.secim[s.id] = s.varsayilan || s.secenekler[0]; });
    metinVarsayilan();

    function metinVarsayilan() {
      var t = K.tasarimlar[d.tasarim];
      d.metin = {};
      (t.alanlar || []).forEach(function (f) { d.metin[f.id] = f.varsayilan; });
    }
    function varyant() { return u.varyantlar.filter(function (x) { return x.id === d.varyant; })[0]; }
    function alan() { return u.alanlar.filter(function (x) { return x.id === d.alan; })[0]; }
    function murekkep() { return K.murekkepler.filter(function (x) { return x.id === d.murekkep; })[0]; }

    /* ---- iskelet ---- */
    kok.classList.add("hs");
    kok.innerHTML =
      '<div class="hs-sol">' +
        '<div class="hs-sahne" data-sahne></div>' +
        '<div class="hs-arac">' +
          '<button type="button" class="hs-ikon" data-tas="sol" aria-label="Sola">◀</button>' +
          '<button type="button" class="hs-ikon" data-tas="yukari" aria-label="Yukarı">▲</button>' +
          '<button type="button" class="hs-ikon" data-tas="asagi" aria-label="Aşağı">▼</button>' +
          '<button type="button" class="hs-ikon" data-tas="sag" aria-label="Sağa">▶</button>' +
          '<button type="button" class="hs-ikon" data-tas="ortala">Ortala</button>' +
        '</div>' +
        '<p class="hs-not" data-not></p>' +
      '</div>' +
      '<div class="hs-sag" data-panel></div>';

    var sahne = kok.querySelector("[data-sahne]");
    var panel = kok.querySelector("[data-panel]");
    var notEl = kok.querySelector("[data-not]");

    /* ---- panel ---- */
    function grup(baslik, ic, ek) {
      return '<div class="hs-grup' + (ek ? " " + ek : "") + '"><h4>' + baslik + "</h4>" + ic + "</div>";
    }
    function cipler(ad, liste, secili, etiket) {
      return '<div class="hs-cipler">' + liste.map(function (x) {
        return '<button type="button" class="hs-cip' + (x.id === secili ? " secili" : "") +
          '" data-' + ad + '="' + x.id + '"' + (x.renk ? ' style="--nokta:' + x.renk + '"' : "") +
          '>' + (x.renk ? '<i class="hs-nokta"></i>' : "") + kacir(etiket ? etiket(x) : x.ad) + "</button>";
      }).join("") + "</div>";
    }

    function panelCiz() {
      var t = K.tasarimlar[d.tasarim];
      var h = "";

      h += grup(u.varyant_ad, cipler("varyant", u.varyantlar, d.varyant));

      if (u.alanlar.length > 1)
        h += grup("Baskı yeri", cipler("alan", u.alanlar, d.alan));

      // tasarımlar
      var tg = '<div class="hs-izgara">';
      tg += u.tasarimlar.map(function (id) {
        var td = K.tasarimlar[id];
        return '<button type="button" class="hs-tas' + (id === d.tasarim && !d.kendi ? " secili" : "") +
          '" data-tasarim="' + id + '" title="' + kacir(td.ad) + '">' +
          '<span class="hs-tas-on" data-onizleme="' + id + '"></span>' +
          '<span class="hs-tas-ad">' + kacir(td.ad) + "</span></button>";
      }).join("");
      tg += "</div>";
      tg += '<label class="hs-yukle' + (d.kendi ? " secili" : "") + '">' +
        '<input type="file" accept="image/png,image/jpeg,image/webp,image/svg+xml" data-dosya hidden>' +
        '<span class="hs-yukle-ic"><b>Kendi tasarımını aç</b>' +
        '<span>' + (d.kendi ? kacir(d.kendiAd) : "PNG, JPG ya da SVG — bilgisayarından seç") + "</span></span></label>" +
        (d.kendi ? '<button type="button" class="hs-metinbtn" data-kendi-sil>Kendi tasarımını kaldır</button>' : "");
      h += grup("Tasarım", tg);

      // metin alanları
      if (!d.kendi && t.alanlar && t.alanlar.length) {
        var mg = t.alanlar.map(function (f) {
          return '<label class="hs-alan"><span>' + kacir(f.ad) + "</span>" +
            '<input type="text" maxlength="' + (f.azami || 30) + '" data-metin="' + f.id +
            '" value="' + kacir(d.metin[f.id] || "") + '"></label>';
        }).join("");
        h += grup("Yazılar", mg);
      }

      // fotoğraf alanı olan tasarımlar
      if (!d.kendi && t.foto) {
        h += grup("Fotoğraf",
          '<label class="hs-yukle' + (d.foto ? " secili" : "") + '">' +
          '<input type="file" accept="image/png,image/jpeg,image/webp" data-foto hidden>' +
          '<span class="hs-yukle-ic"><b>Fotoğrafını aç</b><span>' +
          (d.foto ? kacir(d.fotoAd) : "Çerçevenin içine yerleşir") + "</span></span></label>");
      }

      if (!d.kendi)
        h += grup("Baskı rengi", cipler("murekkep", K.murekkepler, d.murekkep));

      h += grup("Boyut ve açı",
        '<label class="hs-kaydir"><span>Boyut <b data-ol></b></span>' +
        '<input type="range" min="25" max="130" value="' + Math.round(d.olcek * 100) + '" data-olcek></label>' +
        '<label class="hs-kaydir"><span>Açı <b data-ac></b></span>' +
        '<input type="range" min="-30" max="30" value="' + d.aci + '" data-aci></label>');

      var sg = "";
      u.secimler.forEach(function (s) {
        sg += '<label class="hs-alan"><span>' + kacir(s.ad) + "</span><select data-secim=\"" + s.id + '">' +
          s.secenekler.map(function (o) {
            return '<option' + (o === d.secim[s.id] ? " selected" : "") + ">" + kacir(o) + "</option>";
          }).join("") + "</select></label>";
      });
      sg += '<label class="hs-alan"><span>Adet</span><input type="number" min="1" max="2000" value="' + d.adet + '" data-adet></label>';
      sg += '<label class="hs-alan"><span>Adınız</span><input type="text" data-ad value="' + kacir(d.ad) + '" placeholder="Elif Yılmaz"></label>';
      sg += '<label class="hs-alan"><span>Telefon</span><input type="tel" data-tel value="' + kacir(d.tel) + '" placeholder="05.. ... .. .."></label>';
      sg += '<label class="hs-alan"><span>Not (isteğe bağlı)</span><textarea rows="2" data-notu placeholder="Kargo Bursa dışına, 27 Eylül\'e yetişmeli.">' + kacir(d.not) + "</textarea></label>";
      h += grup("Sipariş bilgileri", sg);

      h += '<div class="hs-dugmeler">' +
        '<button type="button" class="btn btn-dolu" data-siparis>Sipariş Ver</button>' +
        '<button type="button" class="btn" data-indir>Önizlemeyi indir</button>' +
        '<button type="button" class="btn" data-eposta>E-posta ile gönder</button>' +
        "</div>" +
        '<p class="hs-kucuk">Sipariş\'e bastığında seçimlerin tek bir mesaj hâline gelir ve kendi ' +
        'WhatsApp\'ından gönderirsin. Tasarım dosyan yüklenmez, bilgisayarında kalır — ' +
        'önizlemeyi indirip mesaja eklemen yeter.</p>';

      panel.innerHTML = h;
      onizlemeleriCiz();
    }

    function onizlemeleriCiz() {
      panel.querySelectorAll("[data-onizleme]").forEach(function (sp) {
        var id = sp.getAttribute("data-onizleme"), td = K.tasarimlar[id];
        var metin = {};
        (td.alanlar || []).forEach(function (f) { metin[f.id] = f.varsayilan; });
        var koyu = varyant().koyu;
        sp.innerHTML = svgUret(id, {
          renk: koyu ? "#F2F0EB" : "#14141A", vurgu: "#E8452C", metin: metin, foto: null
        }).svg;
        sp.className = "hs-tas-on" + (koyu ? " koyu" : "");
      });
    }

    /* ---- sahne ---- */
    function katmanKaynak() {
      if (d.kendi) return { tur: "img", src: d.kendi };
      var m = murekkep();
      return { tur: "svg", s: svgUret(d.tasarim, { renk: m.renk, vurgu: m.vurgu, metin: d.metin, foto: d.foto }) };
    }

    function ciz() {
      var v = varyant(), a = alan(), r = alanDik(u, v, a);
      var k = katmanKaynak();
      var ic = k.tur === "svg" ? k.s.svg
        : '<img src="' + d.kendi + '" alt="Kendi tasarımınız" class="hs-kendi">';
      sahne.innerHTML =
        '<img class="hs-urun" src="' + K.gorselKok + v.g + '" alt="' + kacir(u.ad + " — " + v.ad) + '" decoding="async">' +
        '<div class="hs-cerceve hs-secili" style="left:' + r.x + '%;top:' + r.y + '%;width:' + r.w + '%;height:' + r.h + '%">' +
        '<div class="hs-katman" data-katman style="mix-blend-mode:' +
        (d.kendi ? "normal" : K.karisimSec(v, murekkep())) + ";left:" + d.x + "%;top:" + d.y +
        "%;transform:translate(-50%,-50%) scale(" + d.olcek + ") rotate(" + d.aci + 'deg)">' + ic + "</div></div>";
      notEl.textContent = u.ad + " · " + v.ad + (u.alanlar.length > 1 ? " · " + a.ad : "") +
        (d.kendi ? " · kendi tasarımınız" : " · " + K.tasarimlar[d.tasarim].ad);
      var ol = panel.querySelector("[data-ol]"), ac = panel.querySelector("[data-ac]");
      if (ol) ol.textContent = "%" + Math.round(d.olcek * 100);
      if (ac) ac.textContent = d.aci + "°";
      surukleBagla();
    }

    /* ---- sürükleme ---- */
    function surukleBagla() {
      var kat = sahne.querySelector("[data-katman]");
      if (!kat) return;
      kat.addEventListener("pointerdown", function (e) {
        e.preventDefault();
        var cer = kat.parentNode.getBoundingClientRect();
        var bas = { x: e.clientX, y: e.clientY, dx: d.x, dy: d.y };
        kat.setPointerCapture(e.pointerId);
        function hareket(ev) {
          d.x = kisitla(bas.dx + (ev.clientX - bas.x) / cer.width * 100, 5, 95);
          d.y = kisitla(bas.dy + (ev.clientY - bas.y) / cer.height * 100, 5, 95);
          kat.style.left = d.x + "%"; kat.style.top = d.y + "%";
        }
        function birak(ev) {
          kat.removeEventListener("pointermove", hareket);
          kat.removeEventListener("pointerup", birak);
          kat.removeEventListener("pointercancel", birak);
          try { kat.releasePointerCapture(ev.pointerId); } catch (x) {}
        }
        kat.addEventListener("pointermove", hareket);
        kat.addEventListener("pointerup", birak);
        kat.addEventListener("pointercancel", birak);
      });
    }

    /* ---- önizleme görseli ---- */
    function gorselUret(bitti) {
      var v = varyant(), a = alan(), r = alanDik(u, v, a), B = 1400;
      var c = document.createElement("canvas"); c.width = c.height = B;
      var ctx = c.getContext("2d");
      ctx.fillStyle = "#F1EFEA"; ctx.fillRect(0, 0, B, B);
      var urun = new Image();
      urun.onload = function () {
        ctx.drawImage(urun, 0, 0, B, B);
        var R = { x: r.x / 100 * B, y: r.y / 100 * B, w: r.w / 100 * B, h: r.h / 100 * B };
        var kat = new Image();
        kat.onload = function () {
          var iw = kat.naturalWidth || 1000, ih = kat.naturalHeight || 1000;
          var s = Math.min(R.w / iw, R.h / ih), w = iw * s, h = ih * s;
          ctx.save();
          ctx.globalCompositeOperation = d.kendi ? "source-over" : (function () {
            var m = K.karisimSec(v, murekkep());
            return m === "normal" ? "source-over" : m;
          })();
          ctx.translate(R.x + R.w * d.x / 100, R.y + R.h * d.y / 100);
          ctx.rotate(d.aci * Math.PI / 180);
          ctx.scale(d.olcek, d.olcek);
          ctx.drawImage(kat, -w / 2, -h / 2, w, h);
          ctx.restore();
          kunye(ctx, B); bitir(c, bitti);
        };
        kat.onerror = function () { kunye(ctx, B); bitir(c, bitti); };
        var k = katmanKaynak();
        if (k.tur === "img") kat.src = d.kendi;
        else {
          var tam = svgUret(d.tasarim, { renk: murekkep().renk, vurgu: murekkep().vurgu, metin: d.metin, foto: d.foto }, true);
          kat.src = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(tam.svg);
        }
      };
      urun.onerror = function () { bitti(null); };
      urun.src = K.gorselKok + v.g;
    }

    // Kirlenmiş tuval (yerel dosyadan açıldığında olur) ya da başka bir hata
    // üretimi durdurmasın: null dönüp akış devam etsin.
    function bitir(c, bitti) {
      try { c.toBlob(function (b) { bitti(b); }, "image/jpeg", .92); }
      catch (e) { bitti(null); }
    }

    function kunye(ctx, B) {
      ctx.save();
      ctx.font = "500 20px Helvetica, Arial, sans-serif";
      ctx.fillStyle = "rgba(20,20,26,.55)";
      ctx.textAlign = "left";
      ctx.fillText("lunayapim.com · tasarım önizlemesi", 28, B - 26);
      ctx.textAlign = "right";
      ctx.fillText(kodUret(), B - 28, B - 26);
      ctx.restore();
    }

    /* ---- sipariş metni ---- */
    function kodUret() {
      var v = varyant(), a = alan();
      return ("LY-" + urunId.slice(0, 3) + "-" + v.id.slice(0, 3) + "-" +
        (d.kendi ? "OZL" : d.tasarim.slice(0, 3)) + "-" + a.id.slice(0, 3) + "-" +
        Math.round(d.olcek * 100)).toUpperCase().replace(/[^A-Z0-9-]/g, "");
    }

    function siparisMetni() {
      var v = varyant(), a = alan(), t = K.tasarimlar[d.tasarim];
      var s = ["LUNA YAPIM — TASARIM SİPARİŞİ", ""];
      s.push("Ürün: " + u.ad);
      s.push(u.varyant_ad + ": " + v.ad);
      u.secimler.forEach(function (x) { s.push(x.ad + ": " + d.secim[x.id]); });
      s.push("Adet: " + d.adet);
      s.push("Baskı yeri: " + a.ad);
      if (d.kendi) {
        s.push("Tasarım: KENDİ TASARIMIM (" + (d.kendiAd || "dosya") + ")");
        s.push("→ Bu mesaja tasarım dosyasını ve önizlemeyi eklemeyi unutmayın.");
      } else {
        s.push("Tasarım: " + t.ad);
        (t.alanlar || []).forEach(function (f) {
          if (d.metin[f.id]) s.push("  " + f.ad + ": " + d.metin[f.id]);
        });
        if (t.foto) s.push("  Fotoğraf: " + (d.foto ? (d.fotoAd || "seçildi — mesaja eklenecek") : "gönderilecek"));
        s.push("Baskı rengi: " + murekkep().ad);
      }
      s.push("Yerleşim: yatay %" + Math.round(d.x) + " · dikey %" + Math.round(d.y) +
        " · boyut %" + Math.round(d.olcek * 100) + " · açı " + d.aci + "°");
      s.push("Tasarım kodu: " + kodUret());
      if (d.not) s.push("", "Not: " + d.not);
      s.push("");
      if (d.ad) s.push("Ad: " + d.ad);
      if (d.tel) s.push("Telefon: " + d.tel);
      s.push("", "(Önizleme görselini bu mesaja ekliyorum.)");
      return s.join("\n");
    }

    function indir(b, ad) {
      if (!b) return;
      var url = URL.createObjectURL(b), a = document.createElement("a");
      a.href = url; a.download = ad; document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(url); }, 4000);
    }

    /* ---- olaylar ---- */
    panel.addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b) return;
      if (b.hasAttribute("data-varyant")) {
        d.varyant = b.getAttribute("data-varyant");
        var v = varyant(); if (v.murekkep && !d.kendi) d.murekkep = v.murekkep;
        panelCiz(); ciz(); return;
      }
      if (b.hasAttribute("data-alan")) { d.alan = b.getAttribute("data-alan"); panelCiz(); ciz(); return; }
      if (b.hasAttribute("data-tasarim")) {
        d.tasarim = b.getAttribute("data-tasarim"); d.kendi = null; d.kendiAd = "";
        metinVarsayilan(); panelCiz(); ciz(); return;
      }
      if (b.hasAttribute("data-murekkep")) { d.murekkep = b.getAttribute("data-murekkep"); panelCiz(); ciz(); return; }
      if (b.hasAttribute("data-kendi-sil")) { d.kendi = null; d.kendiAd = ""; panelCiz(); ciz(); return; }
      if (b.hasAttribute("data-indir")) {
        b.disabled = true; b.textContent = "Hazırlanıyor…";
        var zamanAsimi = setTimeout(function () {
          b.disabled = false; b.textContent = "Önizlemeyi indir";
        }, 9000);
        gorselUret(function (bl) {
          clearTimeout(zamanAsimi);
          b.disabled = false;
          b.textContent = bl ? "Önizlemeyi indir" : "Önizleme alınamadı — ekran görüntüsü alın";
          if (bl) indir(bl, "luna-" + kodUret().toLowerCase() + ".jpg");
        });
        return;
      }
      if (b.hasAttribute("data-siparis") || b.hasAttribute("data-eposta")) {
        var eposta = b.hasAttribute("data-eposta");
        var gorselVar = true;
        var ac = function () {
          var metin = siparisMetni() + (gorselVar ? "" :
            "\n(Önizleme görseli oluşmadı; ürünün ekran görüntüsünü ekliyorum.)");
          if (eposta) {
            location.href = "mailto:" + K.eposta + "?subject=" +
              encodeURIComponent("Tasarım siparişi — " + u.ad + " (" + kodUret() + ")") +
              "&body=" + encodeURIComponent(metin);
          } else {
            window.open("https://wa.me/" + K.wa + "?text=" + encodeURIComponent(metin), "_blank", "noopener");
          }
        };
        b.disabled = true;
        var eskiYazi = b.textContent; b.textContent = "Hazırlanıyor…";
        var zaman = setTimeout(function () {
          b.disabled = false; b.textContent = eskiYazi; gorselVar = false; ac();
        }, 9000);
        gorselUret(function (bl) {
          clearTimeout(zaman);
          b.disabled = false; b.textContent = eskiYazi;
          gorselVar = !!bl;
          if (bl) indir(bl, "luna-" + kodUret().toLowerCase() + ".jpg");
          ac();
        });
        return;
      }
    });

    panel.addEventListener("input", function (e) {
      var t = e.target;
      if (t.hasAttribute("data-metin")) { d.metin[t.getAttribute("data-metin")] = t.value; ciz(); return; }
      if (t.hasAttribute("data-olcek")) { d.olcek = (+t.value) / 100; ciz(); return; }
      if (t.hasAttribute("data-aci")) { d.aci = +t.value; ciz(); return; }
      if (t.hasAttribute("data-adet")) { d.adet = kisitla(parseInt(t.value || "1", 10) || 1, 1, 2000); return; }
      if (t.hasAttribute("data-ad")) { d.ad = t.value; return; }
      if (t.hasAttribute("data-tel")) { d.tel = t.value; return; }
      if (t.hasAttribute("data-notu")) { d.not = t.value; return; }
    });

    panel.addEventListener("change", function (e) {
      var t = e.target;
      if (t.hasAttribute("data-secim")) { d.secim[t.getAttribute("data-secim")] = t.value; return; }
      if (t.hasAttribute("data-dosya") || t.hasAttribute("data-foto")) {
        var f = t.files && t.files[0]; if (!f) return;
        if (f.size > 8 * 1024 * 1024) { alert("Dosya 8 MB'tan küçük olmalı."); t.value = ""; return; }
        var fr = new FileReader();
        var fotoMu = t.hasAttribute("data-foto");
        fr.onload = function () {
          if (fotoMu) { d.foto = fr.result; d.fotoAd = f.name; }
          else { d.kendi = fr.result; d.kendiAd = f.name; }
          panelCiz(); ciz();
        };
        fr.readAsDataURL(f);
      }
    });

    kok.querySelector(".hs-arac").addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b) return;
      var y = b.getAttribute("data-tas");
      if (y === "sol") d.x = kisitla(d.x - 2, 5, 95);
      if (y === "sag") d.x = kisitla(d.x + 2, 5, 95);
      if (y === "yukari") d.y = kisitla(d.y - 2, 5, 95);
      if (y === "asagi") d.y = kisitla(d.y + 2, 5, 95);
      if (y === "ortala") { d.x = 50; d.y = 50; d.aci = 0; }
      ciz();
      if (y === "ortala") panelCiz();
    });

    /* ---- vitrinden gelen kurulum ---- */
    kok.lunaKur = function (k) {
      if (k.varyant) d.varyant = k.varyant;
      if (k.alan) d.alan = k.alan;
      if (k.tasarim) { d.tasarim = k.tasarim; d.kendi = null; metinVarsayilan(); }
      if (k.murekkep) d.murekkep = k.murekkep;
      if (k.olcek) d.olcek = k.olcek;
      d.x = 50; d.y = 50; d.aci = 0;
      panelCiz(); ciz();
    };

    // adres çıpası:  #t=tasarim,varyant,alan,murekkep,olcek
    (function () {
      var h = (location.hash || "").replace(/^#/, "");
      if (h.indexOf("t=") !== 0) return;
      var p = decodeURIComponent(h.slice(2)).split(",");
      var k = {};
      if (p[0] && K.tasarimlar[p[0]]) k.tasarim = p[0];
      if (p[1] && u.varyantlar.some(function (x) { return x.id === p[1]; })) k.varyant = p[1];
      if (p[2] && u.alanlar.some(function (x) { return x.id === p[2]; })) k.alan = p[2];
      if (p[3] && K.murekkepler.some(function (x) { return x.id === p[3]; })) k.murekkep = p[3];
      if (p[4]) k.olcek = Math.max(.25, Math.min(1.3, parseFloat(p[4]) || .9));
      if (k.tasarim) { d.tasarim = k.tasarim; d.kendi = null; metinVarsayilan(); }
      if (k.varyant) d.varyant = k.varyant;
      if (k.alan) d.alan = k.alan;
      if (k.murekkep) d.murekkep = k.murekkep;
      if (k.olcek) d.olcek = k.olcek;
      setTimeout(function () { kok.scrollIntoView({ behavior: "smooth", block: "start" }); }, 260);
    })();

    panelCiz();
    ciz();
  }

  /* ---------- vitrin ---------- */
  function vitrinKur(kutu) {
    var urunId = kutu.getAttribute("data-vitrin");
    var liste = (K.vitrinler[urunId] || []).slice();
    var adet = parseInt(kutu.getAttribute("data-vitrin-adet") || "0", 10);
    if (adet > 0) liste = liste.slice(0, adet);
    var g = document.createElement("div"); g.className = "hs-vitrin";
    liste.forEach(function (k, i) {
      var kart = document.createElement("button");
      kart.type = "button"; kart.className = "hs-vkart";
      kart.setAttribute("aria-label", k.ad + " — stüdyoda aç");
      var sahne = document.createElement("span"); sahne.className = "hs-sahne hs-vsahne";
      kompozisyon(sahne, urunId, k);
      var alt = document.createElement("span"); alt.className = "hs-valt";
      alt.innerHTML = "<b>" + kacir(k.ad) + "</b><span>Bu tasarımla başla →</span>";
      kart.appendChild(sahne); kart.appendChild(alt);
      kart.addEventListener("click", function () {
        var s = document.querySelector("[data-studyo]");
        if (s && s.lunaKur) {
          s.lunaKur(k);
          s.scrollIntoView({ behavior: "smooth", block: "start" });
          return;
        }
        var hedef = kutu.getAttribute("data-vitrin-hedef");
        if (hedef) location.href = hedef + "#t=" + encodeURIComponent(
          [k.tasarim, k.varyant, k.alan, k.murekkep, k.olcek || .9].join(","));
      });
      g.appendChild(kart);
    });
    kutu.appendChild(g);
  }

  /* ---------- başlat ---------- */
  function basla() {
    document.querySelectorAll("[data-studyo]").forEach(function (k) {
      try { Studyo(k, k.getAttribute("data-studyo")); }
      catch (e) { k.innerHTML = '<p class="hs-yok">Stüdyo yüklenemedi. Sipariş için WhatsApp\'tan yazabilirsiniz.</p>'; }
    });
    document.querySelectorAll("[data-vitrin]").forEach(function (k) {
      try { vitrinKur(k); } catch (e) { k.remove(); }
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", basla);
  else basla();
})();
