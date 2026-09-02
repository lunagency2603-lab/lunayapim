/* Luna Asistan — sitenin kendi içeriğinden cevap veren yardımcı.
   Dış servis yok, API anahtarı yok, ücret yok. Ziyaretçinin sorusu
   hiçbir sunucuya gitmiyor; eşleştirme tarayıcıda yapılıyor.
   Cevabı yoksa uydurmuyor — WhatsApp'a bağlıyor. */
(function () {
  "use strict";
  if (window.__lunaAsistan) return;
  window.__lunaAsistan = 1;

  var KOK = (function () {
    var h = document.querySelector('link[href*="luna.css"]');
    return h ? h.getAttribute("href").replace(/luna\.css.*$/, "") : "assets/";
  })();

  var V = null, yukleniyor = false, acik = false, sonSorgu = "", kuyruk = [];

  /* ---------------- metin araçları ---------------- */
  var DUR = {"ve":1,"ile":1,"icin":1,"bir":1,"bu":1,"da":1,"de":1,"mi":1,"mu":1,
             "ne":1,"nasil":1,"nedir":1,"var":1,"yok":1,"olur":1,"the":1,"a":1};

  function sade(x) {
    return (x || "").toLowerCase()
      .replace(/ı/g,"i").replace(/ğ/g,"g").replace(/ü/g,"u")
      .replace(/ş/g,"s").replace(/ö/g,"o").replace(/ç/g,"c").replace(/â/g,"a")
      .normalize("NFD").replace(/[̀-ͯ]/g,"")
      .replace(/[^a-z0-9]+/g," ").trim();
  }
  function parcala(x) {
    return sade(x).split(" ").filter(function (t) { return t.length > 1 && !DUR[t]; });
  }
  function kacir(x) {
    return String(x == null ? "" : x)
      .replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
  }

  /* ---------------- veri ---------------- */
  function veriYukle(sonra) {
    if (V !== null) { sonra(); return; }
    /* Yükleme sürerken gelen ikinci istek kaybolmasın — sıraya alınıyor.
       (Kahraman kutusundan gelen soru tam da bu ana denk geliyordu.) */
    kuyruk.push(sonra);
    if (yukleniyor) return;
    yukleniyor = true;
    var x = new XMLHttpRequest();
    x.open("GET", KOK + "asistan-veri.json", true);
    x.onload = function () {
      yukleniyor = false;
      if (x.status < 200 || x.status >= 300) { V = false; bosalt(); return; }
      try { V = JSON.parse(x.responseText); } catch (e) { V = false; }
      if (V && V.soru) {
        for (var i = 0; i < V.soru.length; i++) {
          V.soru[i]._s = sade(V.soru[i].s);
          V.soru[i]._c = sade(V.soru[i].c);
        }
        for (var j = 0; j < V.sayfa.length; j++) {
          var p = V.sayfa[j];
          p._m = sade((p.b || "") + " " + (p.o || "") + " " + (p.h || ""));
          p._b = sade(p.b || "");
        }
      }
      bosalt();
    };
    x.onerror = function () { yukleniyor = false; V = false; bosalt(); };
    x.send();

    function bosalt() {
      var k = kuyruk.slice();
      kuyruk.length = 0;
      k.forEach(function (f) { try { f(); } catch (e) {} });
    }
  }

  /* ---------------- arama ---------------- */
  function sorulariAra(sorgu) {
    var t = parcala(sorgu), s = sade(sorgu), c = [];
    if (!t.length || !V || !V.soru) return c;
    for (var i = 0; i < V.soru.length; i++) {
      var q = V.soru[i], p = 0, kapsam = 0;
      for (var k = 0; k < t.length; k++) {
        var bulundu = false;
        if (q._s.indexOf(t[k]) > -1) { p += 4; bulundu = true; }
        if (q._c.indexOf(t[k]) > -1) { p += 1; bulundu = true; }
        if (bulundu) kapsam++;
      }
      if (s.length > 6 && q._s.indexOf(s) > -1) p += 12;
      // il şablonundan gelen soru: kullanıcı il adı yazmadıysa geride kalsın
      if (q.il && p > 0) {
        var ilAdi = false;
        for (var z = 0; z < t.length; z++) if (q._s.indexOf(t[z]) > -1 &&
            q._s.split(" ").indexOf(t[z]) === 0) ilAdi = true;
        if (!ilAdi) p *= 0.45;
      }
      if (p > 0) c.push({ q: q, p: p, oran: kapsam / t.length });
    }
    c.sort(function (a, b) { return b.p - a.p; });
    return c.slice(0, 4);
  }

  function sayfalariAra(sorgu) {
    var t = parcala(sorgu), c = [];
    if (!t.length || !V || !V.sayfa) return c;
    for (var i = 0; i < V.sayfa.length; i++) {
      var g = V.sayfa[i], p = 0;
      for (var k = 0; k < t.length; k++) {
        if (g._b.indexOf(t[k]) > -1) p += 3;
        else if (g._m.indexOf(t[k]) > -1) p += 1;
      }
      if (g.k === "Hizmet") p *= 1.35;          // hizmet sayfaları önce gelsin
      if (p > 0) c.push({ g: g, p: p });
    }
    c.sort(function (a, b) { return b.p - a.p; });
    return c.slice(0, 4);
  }

  /* ---------------- görünüm ---------------- */
  function el(id) { return document.getElementById(id); }

  function kur() {
    var d = document.createElement("div");
    d.id = "luna-as";
    d.innerHTML =
      '<button id="las-dug" class="las-dug" aria-expanded="false" aria-controls="las-kutu"' +
      ' aria-label="Luna Asistan\'a soru sor">' +
      '<img src="' + KOK + 'karga.png" alt="" width="26" height="26">' +
      '<span>Soru sor</span></button>' +
      '<div id="las-kutu" class="las-kutu" role="dialog" aria-modal="false"' +
      ' aria-label="Luna Asistan" hidden>' +
      '  <div class="las-bas"><div><b>Luna Asistan</b>' +
      '    <span>Sitedeki bilgiden cevaplar</span></div>' +
      '    <button class="las-kapa" aria-label="Kapat">&times;</button></div>' +
      '  <div class="las-govde" id="las-govde" aria-live="polite"></div>' +
      '  <form class="las-alt" id="las-form" autocomplete="off">' +
      '    <input id="las-giris" type="text" placeholder="Ne öğrenmek istiyorsun?"' +
      '      aria-label="Sorunuz" maxlength="140">' +
      '    <button type="submit" aria-label="Sor">→</button></form>' +
      '  <p class="las-not">Cevaplar bu sitedeki sayfalardan geliyor. ' +
      '  Bilmediğini uydurmuyor.</p>' +
      '</div>';
    document.body.appendChild(d);

    el("las-dug").addEventListener("click", function () { acik ? kapat() : ac(); });
    d.querySelector(".las-kapa").addEventListener("click", kapat);
    el("las-form").addEventListener("submit", function (e) {
      e.preventDefault(); sor(el("las-giris").value);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && acik) kapat();
    });
    d.addEventListener("click", function (e) {
      var b = e.target.closest("[data-soru]");
      if (b) { e.preventDefault(); el("las-giris").value = b.getAttribute("data-soru");
               sor(b.getAttribute("data-soru")); }
    });
  }

  function ac() {
    acik = true;
    el("las-kutu").hidden = false;
    el("las-dug").setAttribute("aria-expanded", "true");
    document.getElementById("luna-as").classList.add("las-acik");
    veriYukle(function () { if (!sonSorgu) karsila(); });
    setTimeout(function () { el("las-giris").focus(); }, 60);
  }
  function kapat() {
    acik = false;
    el("las-kutu").hidden = true;
    el("las-dug").setAttribute("aria-expanded", "false");
    document.getElementById("luna-as").classList.remove("las-acik");
  }

  var ONERI = ["Fiyatlar ne kadar?", "Ne kadar sürede teslim ediyorsunuz?",
               "Bursa dışında çalışıyor musunuz?", "Kaç revizyon hakkım var?",
               "Drone çekimi için izin gerekiyor mu?"];

  function karsila() {
    var g = el("las-govde");
    if (V === false) {
      g.innerHTML = '<div class="las-c"><p>Bilgi dosyası yüklenemedi. ' +
        'Doğrudan yazabilirsin:</p>' + baglantilar() + '</div>';
      return;
    }
    g.innerHTML = '<div class="las-c"><p>Merhaba. Sitedeki <b>' +
      (V ? V.soru.length : 0) + '</b> soru-cevap ve <b>' + (V ? V.sayfa.length : 0) +
      '</b> sayfadan cevap veriyorum. Ne sormak istersin?</p></div>' +
      '<div class="las-oner">' + ONERI.map(function (o) {
        return '<button type="button" data-soru="' + kacir(o) + '">' + kacir(o) + '</button>';
      }).join("") + '</div>';
  }

  function baglantilar() {
    var w = V && V.firma && V.firma.wa ? V.firma.wa : "";
    var t = V && V.firma && V.firma.tel ? V.firma.tel : "";
    var h = '<div class="las-bag">';
    if (w) h += '<a href="https://wa.me/' + kacir(w) + '" target="_blank" rel="noopener">WhatsApp</a>';
    if (t) h += '<a href="tel:' + kacir(t) + '">Ara</a>';
    h += '<a href="/iletisim">İletişim</a></div>';
    return h;
  }

  function olcum(sorgu, bulundu) {
    try {
      if (typeof window.gtag === "function") {
        window.gtag("event", "asistan_soru", { soru: sorgu.slice(0, 100),
                                               sonuc: bulundu ? "cevaplandi" : "cevapsiz" });
      }
    } catch (e) {}
  }

  function sor(sorgu) {
    sorgu = (sorgu || "").trim();
    if (!sorgu) return;
    sonSorgu = sorgu;
    var g = el("las-govde");
    g.innerHTML = '<div class="las-ben">' + kacir(sorgu) + '</div>' +
                  '<div class="las-c"><p>Bakıyorum…</p></div>';
    veriYukle(function () { cevapla(sorgu); });
  }

  function cevapla(sorgu) {
    var g = el("las-govde");
    var bas = '<div class="las-ben">' + kacir(sorgu) + '</div>';
    if (!V) {
      g.innerHTML = bas + '<div class="las-c"><p>Bilgi dosyasına ulaşamadım.</p>' +
        baglantilar() + '</div>';
      olcum(sorgu, false); return;
    }
    var q = sorulariAra(sorgu), s = sayfalariAra(sorgu);
    var iyi = q.length && q[0].p >= 8 && q[0].oran >= 0.5;
    var h = bas;

    if (iyi) {
      var ilk = q[0].q;
      var sy = V.sayfa[ilk.p[0]];
      h += '<div class="las-c"><b>' + kacir(ilk.s) + '</b><p>' + kacir(ilk.c) + '</p>' +
           (sy ? '<a class="las-kaynak" href="' + kacir(sy.u) + '">Kaynak: ' +
                 kacir(sy.b) + ' →</a>' : "") + '</div>';
      var digerleri = q.slice(1, 4);
      if (digerleri.length) {
        h += '<div class="las-oner"><span>Bunlar da sorulmuş:</span>' +
             digerleri.map(function (x) {
               return '<button type="button" data-soru="' + kacir(x.q.s) + '">' +
                      kacir(x.q.s) + '</button>'; }).join("") + '</div>';
      }
    } else if (s.length) {
      h += '<div class="las-c"><p>Bunun tam cevabını sitede bulamadım, ama ' +
           'aradığın büyük ihtimalle bu sayfalarda:</p><ul class="las-sayfa">' +
           s.map(function (x) {
             return '<li><a href="' + kacir(x.g.u) + '"><b>' + kacir(x.g.b) + '</b>' +
                    (x.g.o ? '<span>' + kacir(x.g.o.slice(0, 110)) + '</span>' : "") +
                    '</a></li>'; }).join("") +
           '</ul><p class="las-uyari">Emin olmak istersen doğrudan yaz — ' +
           'aynı gün dönüyoruz.</p>' + baglantilar() + '</div>';
      if (q.length) {
        h += '<div class="las-oner"><span>Yakın sorular:</span>' +
             q.slice(0, 3).map(function (x) {
               return '<button type="button" data-soru="' + kacir(x.q.s) + '">' +
                      kacir(x.q.s) + '</button>'; }).join("") + '</div>';
      }
    } else {
      h += '<div class="las-c"><p><b>Bunu tam bilemedim.</b> Uydurmak yerine ' +
           'seni doğrudan bize bağlayayım — sorunun cevabını insandan almak ' +
           'daha hızlı olacak.</p>' + baglantilar() + '</div>';
    }
    g.innerHTML = h;
    g.scrollTop = g.scrollHeight;
    olcum(sorgu, iyi || s.length > 0);
  }

  /* Dışarıdan çağrı: ana sayfadaki kahraman kutusu bunu kullanıyor. */
  window.lunaAsistanSor = function (metin) {
    if (!document.getElementById("luna-as")) kur();
    if (!acik) ac();
    var g = el("las-giris");
    if (g) g.value = metin || "";
    if (metin) sor(metin);
  };

  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", kur);
  else kur();
})();
