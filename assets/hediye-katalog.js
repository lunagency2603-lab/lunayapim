/* ============================================================
   LUNA YAPIM — HEDİYE KATALOĞU
   ------------------------------------------------------------
   Tasarım stüdyosunun verisi: ürünler, renk varyantları, baskı
   alanları ve hazır tasarımlar. Tasarımlar SVG olarak burada
   çiziliyor — hepsi bize ait, telifli hiçbir öge yok.

   Baskı alanı (alan): ürün görselinin yüzdesi olarak
   {x, y, w, h}. Görseller 1:1 ve ürün ortalanmış varsayılıyor.
   ============================================================ */
window.LUNA_HEDIYE = (function () {

  /* ---------- yardımcılar ---------- */
  var G = "../assets/hediye/urun/";           // mockup klasörü (hizmetler/ içinden)

  function kacir(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
  // SVG içinde dış yazı tipi yüklenmiyor (görsel olarak çizildiğinde) —
  // bu yüzden yalnız sistemde bulunan aileler kullanılıyor.
  var SANS = "Helvetica Neue, Helvetica, Arial, sans-serif";
  var KALIN = "Arial Black, Arial Bold, Arial, sans-serif";
  var SERIF = "Georgia, Times New Roman, serif";

  /* ---------- hazır tasarımlar ----------
     oran : genişlik / yükseklik
     alanlar : kullanıcının dolduracağı metin kutuları
     ciz(o) : {renk, metin:{...}} → SVG içeriği (viewBox 0 0 100 100/oran)  */
  var TASARIM = {

    "kus-ay": {
      ad: "Kuş ve ay", etiket: "Çizgi", oran: 1, alanlar: [],
      ciz: function (o) {
        var c = o.renk, v = o.vurgu;
        return '<circle cx="50" cy="42" r="26" fill="none" stroke="' + v + '" stroke-width="1.2"/>' +
          '<path d="M41 62c-6-4-7-13-1-19 3-7 11-11 18-9 3 1 4 4 3 6l7 2-7 2c1 6-2 12-7 15-4 3-9 4-13 3z" fill="' + c + '"/>' +
          '<path d="M41 62c-5 1-11 5-16 11 7-3 13-6 19-8z" fill="' + c + '"/>' +
          '<path d="M47 63l-1 5M54 62l1 5" stroke="' + c + '" stroke-width="1.3" stroke-linecap="round"/>' +
          '<path d="M25 70c9-4 20-6 30-6s19 2 25 5" fill="none" stroke="' + c + '" stroke-width="1.3" stroke-linecap="round"/>' +
          '<path d="M38 66c-3 2-5 4-6 7M66 67c2 2 3 4 4 6" fill="none" stroke="' + c + '" stroke-width=".9" opacity=".7"/>' +
          '<circle cx="57" cy="39" r="1.5" fill="' + v + '"/>';
      }
    },

    "bursa-silueti": {
      ad: "Bursa silüeti", etiket: "Şehir", oran: 1.35,
      alanlar: [{ id: "alt", ad: "Alt yazı", varsayilan: "BURSA", azami: 16 }],
      ciz: function (o) {
        var c = o.renk, v = o.vurgu, t = kacir((o.metin.alt || "").toUpperCase());
        return '<path d="M4 52l14-16 9 10 12-16 11 14 8-8 13 16 12-10 13 10v6H4z" fill="none" stroke="' + c + '" stroke-width="1.4" stroke-linejoin="round"/>' +
          '<path d="M30 74V60a8 8 0 0116 0v14" fill="none" stroke="' + c + '" stroke-width="1.6"/>' +
          '<path d="M38 52a6 6 0 016 0" fill="none" stroke="' + v + '" stroke-width="1.4"/>' +
          '<rect x="54" y="58" width="3" height="16" fill="' + c + '"/>' +
          '<path d="M55.5 54l2 4h-4z" fill="' + v + '"/>' +
          '<path d="M64 74V64c0-3 2-5 4-5s4 2 4 5v10" fill="none" stroke="' + c + '" stroke-width="1.3"/>' +
          '<path d="M18 74V66" stroke="' + c + '" stroke-width="1.3"/>' +
          '<path d="M14 66c0-5 2-8 4-9 2 1 4 4 4 9z" fill="' + c + '"/>' +
          '<path d="M4 74h92" stroke="' + c + '" stroke-width="1.2"/>' +
          '<text x="50" y="89" text-anchor="middle" font-family="' + KALIN + '" font-size="12" letter-spacing="5" fill="' + c + '">' + t + '</text>';
      }
    },

    "sehir-tipografi": {
      ad: "Tipografik şehir", etiket: "Tipografi", oran: 1,
      alanlar: [{ id: "ust", ad: "Büyük yazı", varsayilan: "BURSA", azami: 10 },
                { id: "alt", ad: "Alt satır", varsayilan: "16 · YEŞİL", azami: 20 }],
      ciz: function (o) {
        var c = o.renk, v = o.vurgu;
        return '<text x="50" y="52" text-anchor="middle" font-family="' + KALIN + '" font-size="26" letter-spacing="-1" fill="' + c + '">' + kacir((o.metin.ust || "").toUpperCase()) + '</text>' +
          '<path d="M18 60h64" stroke="' + v + '" stroke-width="2"/>' +
          '<text x="50" y="74" text-anchor="middle" font-family="' + SANS + '" font-size="8" letter-spacing="4" fill="' + c + '">' + kacir((o.metin.alt || "").toUpperCase()) + '</text>' +
          '<circle cx="50" cy="25" r="2.6" fill="' + v + '"/>';
      }
    },

    "cift-tarih": {
      ad: "İki isim, bir tarih", etiket: "Çift", oran: 1.25,
      alanlar: [{ id: "isim", ad: "İsimler", varsayilan: "Elif & Can", azami: 26 },
                { id: "tarih", ad: "Tarih", varsayilan: "14.02.2027", azami: 14 }],
      ciz: function (o) {
        var c = o.renk, v = o.vurgu;
        return '<path d="M42 30c-4-5-12-4-13 3 0 6 7 11 13 16 6-5 13-10 13-16-1-7-9-8-13-3z" fill="none" stroke="' + v + '" stroke-width="1.6"/>' +
          '<text x="50" y="63" text-anchor="middle" font-family="' + SERIF + '" font-style="italic" font-size="15" fill="' + c + '">' + kacir(o.metin.isim) + '</text>' +
          '<path d="M30 70h40" stroke="' + c + '" stroke-width=".8" opacity=".6"/>' +
          '<text x="50" y="80" text-anchor="middle" font-family="' + SANS + '" font-size="7" letter-spacing="3" fill="' + c + '">' + kacir(o.metin.tarih) + '</text>';
      }
    },

    "yildiz-harita": {
      ad: "O gecenin yıldızları", etiket: "Çift", oran: 1,
      alanlar: [{ id: "alt", ad: "Tarih ya da yer", varsayilan: "BURSA · 14.02.2027", azami: 26 }],
      ciz: function (o) {
        var c = o.renk, v = o.vurgu;
        var n = [[35, 28], [45, 21], [57, 27], [64, 38], [55, 47], [44, 43], [36, 36], [61, 20], [32, 44]];
        var s = '<circle cx="50" cy="36" r="26" fill="none" stroke="' + c + '" stroke-width="1" opacity=".5"/>';
        var yol = "M" + n.slice(0, 7).map(function (p) { return p[0] + " " + p[1]; }).join("L");
        s += '<path d="' + yol + '" fill="none" stroke="' + c + '" stroke-width=".9"/>';
        n.forEach(function (p, i) {
          s += '<circle cx="' + p[0] + '" cy="' + p[1] + '" r="' + (i % 3 === 0 ? 2.1 : 1.3) + '" fill="' + (i === 1 ? v : c) + '"/>';
        });
        s += '<text x="50" y="72" text-anchor="middle" font-family="' + SANS + '" font-size="5.6" letter-spacing="2.6" fill="' + c + '">' + kacir((o.metin.alt || "").toUpperCase()) + '</text>';
        return s;
      }
    },

    "dogum-yili": {
      ad: "Doğum yılı rozeti", etiket: "Doğum günü", oran: 1,
      alanlar: [{ id: "yil", ad: "Yıl", varsayilan: "1995", azami: 6 },
                { id: "alt", ad: "Alt yazı", varsayilan: "SINIRLI ÜRETİM", azami: 22 }],
      ciz: function (o) {
        var c = o.renk, v = o.vurgu;
        return '<path d="M18 62c-6-7-6-19 0-26" fill="none" stroke="' + v + '" stroke-width="1.6"/>' +
          '<path d="M82 62c6-7 6-19 0-26" fill="none" stroke="' + v + '" stroke-width="1.6"/>' +
          '<path d="M23 58c-4-6-4-14 0-20M77 58c4-6 4-14 0-20" fill="none" stroke="' + c + '" stroke-width="1" opacity=".55"/>' +
          '<text x="50" y="55" text-anchor="middle" font-family="' + KALIN + '" font-size="21" fill="' + c + '">' + kacir(o.metin.yil) + '</text>' +
          '<text x="50" y="68" text-anchor="middle" font-family="' + SANS + '" font-size="5.6" letter-spacing="3" fill="' + c + '">' + kacir((o.metin.alt || "").toUpperCase()) + '</text>' +
          '<path d="M36 32h28" stroke="' + v + '" stroke-width="1.6"/>';
      }
    },

    "pati": {
      ad: "Pati ve isim", etiket: "Evcil hayvan", oran: 1,
      alanlar: [{ id: "isim", ad: "İsim", varsayilan: "PAŞA", azami: 14 }],
      ciz: function (o) {
        var c = o.renk, v = o.vurgu;
        return '<ellipse cx="50" cy="48" rx="13" ry="11" fill="' + c + '"/>' +
          '<ellipse cx="34" cy="34" rx="5.2" ry="7" fill="' + c + '"/>' +
          '<ellipse cx="45" cy="27" rx="5" ry="7.2" fill="' + c + '"/>' +
          '<ellipse cx="57" cy="27" rx="5" ry="7.2" fill="' + c + '"/>' +
          '<ellipse cx="67" cy="35" rx="5.2" ry="7" fill="' + c + '"/>' +
          '<circle cx="50" cy="46" r="2.6" fill="' + v + '"/>' +
          '<text x="50" y="75" text-anchor="middle" font-family="' + SANS + '" font-size="10" letter-spacing="4" fill="' + c + '">' + kacir((o.metin.isim || "").toUpperCase()) + '</text>';
      }
    },

    "dag-gunes": {
      ad: "Dağ ve güneş rozeti", etiket: "Doğa", oran: 1,
      alanlar: [{ id: "ust", ad: "Üst yazı", varsayilan: "ULUDAĞ", azami: 16 },
                { id: "alt", ad: "Alt yazı", varsayilan: "2543 M", azami: 14 }],
      ciz: function (o) {
        var c = o.renk, v = o.vurgu;
        return '<circle cx="50" cy="50" r="33" fill="none" stroke="' + c + '" stroke-width="1.6"/>' +
          '<circle cx="50" cy="50" r="28" fill="none" stroke="' + c + '" stroke-width=".7" opacity=".45"/>' +
          '<circle cx="50" cy="46" r="7" fill="none" stroke="' + v + '" stroke-width="1.4"/>' +
          '<path d="M31 60l10-12 6 7 8-11 15 16z" fill="' + c + '"/>' +
          '<path d="M30 60h40" stroke="' + c + '" stroke-width="1.2"/>' +
          '<text x="50" y="34" text-anchor="middle" font-family="' + SANS + '" font-size="5.8" letter-spacing="2.4" fill="' + c + '">' + kacir((o.metin.ust || "").toUpperCase()) + '</text>' +
          '<text x="50" y="71" text-anchor="middle" font-family="' + SANS + '" font-size="5.4" letter-spacing="2.2" fill="' + c + '">' + kacir((o.metin.alt || "").toUpperCase()) + '</text>';
      }
    },

    "monogram": {
      ad: "Monogram", etiket: "Kurumsal", oran: 1,
      alanlar: [{ id: "harf", ad: "Harfler", varsayilan: "LY", azami: 3 },
                { id: "alt", ad: "Alt yazı (isteğe bağlı)", varsayilan: "", azami: 22 }],
      ciz: function (o) {
        var c = o.renk, v = o.vurgu, alt = (o.metin.alt || "").toUpperCase();
        return '<path d="M50 20l28 28-28 28-28-28z" fill="none" stroke="' + c + '" stroke-width="1.5"/>' +
          '<path d="M50 27l21 21-21 21-21-21z" fill="none" stroke="' + v + '" stroke-width=".8"/>' +
          '<text x="50" y="56" text-anchor="middle" font-family="' + SERIF + '" font-size="21" letter-spacing="1" fill="' + c + '">' + kacir((o.metin.harf || "").toUpperCase()) + '</text>' +
          (alt ? '<text x="50" y="88" text-anchor="middle" font-family="' + SANS + '" font-size="6" letter-spacing="4" fill="' + c + '">' + kacir(alt) + '</text>' : "");
      }
    },

    "isim-serit": {
      ad: "İsim şeridi", etiket: "İsim", oran: 3,
      alanlar: [{ id: "isim", ad: "Yazı", varsayilan: "ELİF", azami: 18 }],
      ciz: function (o) {
        var c = o.renk, v = o.vurgu;
        return '<path d="M2 14h96" stroke="' + v + '" stroke-width="1.2"/>' +
          '<path d="M2 23h96" stroke="' + v + '" stroke-width="1.2"/>' +
          '<text x="50" y="21" text-anchor="middle" font-family="' + KALIN + '" font-size="11" letter-spacing="6" fill="' + c + '">' + kacir((o.metin.isim || "").toUpperCase()) + '</text>';
      }
    },

    "el-yazisi": {
      ad: "El yazısı isim", etiket: "İsim", oran: 2.4,
      alanlar: [{ id: "isim", ad: "Yazı", varsayilan: "Elif", azami: 20 },
                { id: "alt", ad: "Alt satır", varsayilan: "", azami: 20 }],
      ciz: function (o) {
        var c = o.renk, v = o.vurgu, alt = o.metin.alt || "";
        return '<text x="50" y="' + (alt ? 22 : 27) + '" text-anchor="middle" font-family="' + SERIF + '" font-style="italic" font-size="20" fill="' + c + '">' + kacir(o.metin.isim) + '</text>' +
          (alt ? '<text x="50" y="34" text-anchor="middle" font-family="' + SANS + '" font-size="6" letter-spacing="4" fill="' + c + '">' + kacir(alt.toUpperCase()) + '</text>'
               : '<path d="M36 33q14 4 28 0" fill="none" stroke="' + v + '" stroke-width="1.2" stroke-linecap="round"/>');
      }
    },

    "cicek-celengi": {
      ad: "Çiçek çelengi", etiket: "Çelenk", oran: 1,
      alanlar: [{ id: "isim", ad: "Ortadaki yazı", varsayilan: "Elif", azami: 16 },
                { id: "alt", ad: "Alt satır", varsayilan: "2027", azami: 14 }],
      ciz: function (o) {
        var c = o.renk, v = o.vurgu, s = "";
        for (var i = 0; i < 14; i++) {
          var a = (i / 14) * Math.PI * 2 + 0.35, r = 30;
          var x = 50 + Math.cos(a) * r, y = 50 + Math.sin(a) * r;
          var d = (a * 180 / Math.PI) + 90;
          s += '<g transform="translate(' + x.toFixed(1) + ' ' + y.toFixed(1) + ') rotate(' + d.toFixed(1) + ')">' +
            '<path d="M0 0c-3-3-3-7 0-9 3 2 3 6 0 9z" fill="' + (i % 4 === 0 ? v : c) + '" opacity="' + (i % 4 === 0 ? 1 : .85) + '"/>' +
            '<path d="M0 0c4-2 8-1 9 2-4 2-8 1-9-2z" fill="' + c + '" opacity=".7"/></g>';
        }
        s += '<text x="50" y="52" text-anchor="middle" font-family="' + SERIF + '" font-style="italic" font-size="15" fill="' + c + '">' + kacir(o.metin.isim) + '</text>';
        s += '<text x="50" y="64" text-anchor="middle" font-family="' + SANS + '" font-size="6" letter-spacing="4" fill="' + c + '">' + kacir((o.metin.alt || "").toUpperCase()) + '</text>';
        return s;
      }
    },

    "once-kahve": {
      ad: "Önce kahve", etiket: "Tipografi", oran: 1,
      alanlar: [{ id: "ust", ad: "Yazı", varsayilan: "ÖNCE KAHVE", azami: 18 }],
      ciz: function (o) {
        var c = o.renk, v = o.vurgu, t = (o.metin.ust || "").toUpperCase().split(" ");
        var s = '<path d="M44 26q-3-5 0-9M50 26q-3-5 0-9M56 26q-3-5 0-9" fill="none" stroke="' + v + '" stroke-width="1.4" stroke-linecap="round"/>' +
          '<path d="M34 32h32l-3 20a8 8 0 01-8 7H45a8 8 0 01-8-7z" fill="none" stroke="' + c + '" stroke-width="1.6"/>' +
          '<path d="M66 37h5a5 5 0 010 10h-4" fill="none" stroke="' + c + '" stroke-width="1.4"/>';
        s += '<text x="50" y="74" text-anchor="middle" font-family="' + KALIN + '" font-size="11" letter-spacing="2" fill="' + c + '">' + kacir(t[0] || "") + '</text>';
        if (t.length > 1) s += '<text x="50" y="86" text-anchor="middle" font-family="' + KALIN + '" font-size="11" letter-spacing="2" fill="' + c + '">' + kacir(t.slice(1).join(" ")) + '</text>';
        return s;
      }
    },

    "foto-cerceve": {
      ad: "Fotoğraf çerçevesi", etiket: "Fotoğraf", oran: 1, foto: true,
      alanlar: [{ id: "isim", ad: "Alt yazı", varsayilan: "Elif & Can", azami: 24 },
                { id: "tarih", ad: "Tarih", varsayilan: "14.02.2027", azami: 14 }],
      ciz: function (o) {
        var c = o.renk, v = o.vurgu;
        var ic = o.foto
          ? '<image href="' + o.foto + '" x="22" y="14" width="56" height="48" preserveAspectRatio="xMidYMid slice" clip-path="url(#hsfoto)"/>'
          : '<rect x="22" y="14" width="56" height="48" fill="' + c + '" opacity=".1"/>' +
            '<path d="M32 54l10-11 7 6 7-9 10 14z" fill="' + c + '" opacity=".28"/>' +
            '<circle cx="39" cy="26" r="3.4" fill="' + c + '" opacity=".28"/>' +
            '<text x="50" y="37" text-anchor="middle" font-family="' + SANS + '" font-size="4.6" letter-spacing="1.8" fill="' + c + '" opacity=".7">FOTOĞRAFINIZ</text>';
        return '<defs><clipPath id="hsfoto"><rect x="22" y="14" width="56" height="48"/></clipPath></defs>' +
          ic +
          '<rect x="22" y="14" width="56" height="48" fill="none" stroke="' + c + '" stroke-width="1.4"/>' +
          '<text x="50" y="76" text-anchor="middle" font-family="' + SERIF + '" font-style="italic" font-size="13" fill="' + c + '">' + kacir(o.metin.isim) + '</text>' +
          '<path d="M38 82h24" stroke="' + v + '" stroke-width="1"/>' +
          '<text x="50" y="91" text-anchor="middle" font-family="' + SANS + '" font-size="6" letter-spacing="3" fill="' + c + '">' + kacir(o.metin.tarih) + '</text>';
      }
    },

    "takim-rozeti": {
      ad: "Takım rozeti", etiket: "Kurumsal", oran: 1,
      alanlar: [{ id: "ust", ad: "Üst yazı", varsayilan: "LUNA", azami: 16 },
                { id: "alt", ad: "Alt yazı", varsayilan: "EKİP · 2027", azami: 20 }],
      ciz: function (o) {
        var c = o.renk, v = o.vurgu;
        return '<path d="M50 18l26 8v22c0 15-11 26-26 32-15-6-26-17-26-32V26z" fill="none" stroke="' + c + '" stroke-width="1.6"/>' +
          '<path d="M50 25l19 6v17c0 11-8 19-19 24-11-5-19-13-19-24V31z" fill="none" stroke="' + v + '" stroke-width=".8"/>' +
          '<text x="50" y="50" text-anchor="middle" font-family="' + KALIN + '" font-size="12" letter-spacing="1" fill="' + c + '">' + kacir((o.metin.ust || "").toUpperCase()) + '</text>' +
          '<path d="M39 55h22" stroke="' + v + '" stroke-width="1.2"/>' +
          '<text x="50" y="62" text-anchor="middle" font-family="' + SANS + '" font-size="4.6" letter-spacing="1.6" fill="' + c + '">' + kacir((o.metin.alt || "").toUpperCase()) + '</text>';
      }
    },

    "kalp-cizgi": {
      ad: "Tek çizgi kalp", etiket: "Çift", oran: 1.6,
      alanlar: [{ id: "tarih", ad: "Tarih ya da yazı", varsayilan: "14.02.2027", azami: 20 }],
      ciz: function (o) {
        var c = o.renk, v = o.vurgu;
        return '<path d="M20 32c0-9 8-14 15-10 5 3 8 9 12 17 4-8 7-14 12-17 7-4 15 1 15 10 0 12-16 22-27 28-11-6-27-16-27-28z" fill="none" stroke="' + c + '" stroke-width="1.7" stroke-linecap="round"/>' +
          '<circle cx="80" cy="32" r="2" fill="' + v + '"/>' +
          '<text x="50" y="76" text-anchor="middle" font-family="' + SANS + '" font-size="6.5" letter-spacing="3.6" fill="' + c + '">' + kacir((o.metin.tarih || "").toUpperCase()) + '</text>';
      }
    }
  };

  /* ---------- baskı mürekkebi seçenekleri ---------- */
  var MUREKKEP = [
    { id: "siyah", ad: "Siyah", renk: "#14141A", vurgu: "#E8452C" },
    { id: "beyaz", ad: "Beyaz", renk: "#F6F4EF", vurgu: "#E8452C" },
    { id: "kirmizi", ad: "Vermilyon", renk: "#E8452C", vurgu: "#14141A" },
    { id: "altin", ad: "Altın", renk: "#C79A3F", vurgu: "#14141A" },
    { id: "lacivert", ad: "Lacivert", renk: "#1F2E4A", vurgu: "#C79A3F" }
  ];

  var BEDEN = ["XS", "S", "M", "L", "XL", "2XL", "3XL"];
  var TEKSTIL_TASARIM = ["kus-ay", "bursa-silueti", "sehir-tipografi", "cift-tarih", "yildiz-harita",
                         "dogum-yili", "pati", "dag-gunes", "takim-rozeti", "monogram",
                         "foto-cerceve", "kalp-cizgi", "el-yazisi"];
  var PROMO_TASARIM = ["monogram", "isim-serit", "el-yazisi", "takim-rozeti", "kus-ay", "dag-gunes"];

  /* ---------- ürünler ---------- */
  var URUN = {
    "baskili-tisort": {
      ad: "Baskılı tişört", vurgu: "Tek parçadan ekip setine",
      varyant_ad: "Renk",
      varyantlar: [
        { id: "beyaz", ad: "Beyaz", g: "tisort-beyaz.jpg", koyu: false, murekkep: "siyah" },
        { id: "siyah", ad: "Siyah", g: "tisort-siyah.jpg", koyu: true, murekkep: "beyaz" },
        { id: "lacivert", ad: "Lacivert", g: "tisort-lacivert.jpg", koyu: true, murekkep: "beyaz" }
      ],
      alanlar: [
        { id: "gogus", ad: "Göğüs orta", r: { x: 33, y: 26, w: 34, h: 30 } },
        { id: "gogus-sol", ad: "Göğüs (küçük)", r: { x: 37, y: 28, w: 12, h: 10 } },
        { id: "sirt", ad: "Büyük baskı (sırt)", r: { x: 28, y: 24, w: 44, h: 36 } }
      ],
      secimler: [{ id: "beden", ad: "Beden", secenekler: BEDEN, varsayilan: "L" }],
      tasarimlar: TEKSTIL_TASARIM
    },
    "baskili-sweatshirt-hoodie": {
      ad: "Sweatshirt / hoodie", vurgu: "Kalın kumaş, geniş baskı alanı",
      varyant_ad: "Ürün ve renk",
      varyantlar: [
        { id: "hoodie-siyah", ad: "Hoodie · Siyah", g: "hoodie-siyah.jpg", koyu: true, murekkep: "beyaz" },
        { id: "hoodie-krem", ad: "Hoodie · Krem", g: "hoodie-krem.jpg", koyu: false, murekkep: "siyah" },
        { id: "sweat-gri", ad: "Sweatshirt · Gri", g: "sweatshirt-gri.jpg", koyu: false, murekkep: "siyah", alan: { gogus: { x: 34, y: 29, w: 32, h: 28 }, "gogus-sol": { x: 38, y: 31, w: 11, h: 9 }, sirt: { x: 29, y: 26, w: 42, h: 34 } } }
      ],
      alanlar: [
        { id: "gogus", ad: "Göğüs orta", r: { x: 34, y: 34, w: 32, h: 24 } },
        { id: "gogus-sol", ad: "Göğüs (küçük)", r: { x: 38, y: 36, w: 11, h: 9 } },
        { id: "sirt", ad: "Büyük baskı (sırt)", r: { x: 29, y: 31, w: 42, h: 30 } }
      ],
      secimler: [{ id: "beden", ad: "Beden", secenekler: BEDEN, varsayilan: "L" }],
      tasarimlar: TEKSTIL_TASARIM
    },
    "baskili-yelek": {
      ad: "Baskılı yelek", vurgu: "Saha, kurye ve etkinlik ekibi",
      varyant_ad: "Renk",
      varyantlar: [
        { id: "lacivert", ad: "Lacivert", g: "yelek-lacivert.jpg", koyu: true, murekkep: "beyaz" }
      ],
      alanlar: [
        { id: "gogus-sol", ad: "Göğüs (küçük)", r: { x: 36, y: 30, w: 11, h: 9 } },
        { id: "sirt", ad: "Sırt üst (büyük)", r: { x: 34, y: 27, w: 32, h: 24 } }
      ],
      secimler: [{ id: "beden", ad: "Beden", secenekler: ["S", "M", "L", "XL", "2XL", "3XL"], varsayilan: "L" }],
      tasarimlar: ["monogram", "takim-rozeti", "isim-serit", "sehir-tipografi", "dag-gunes", "el-yazisi"]
    },
    "kisiye-ozel-kupa": {
      ad: "Kişiye özel kupa", vurgu: "Her sabah eline alınan hediye",
      varyant_ad: "Kupa",
      varyantlar: [
        { id: "beyaz", ad: "Beyaz", g: "kupa-beyaz.jpg", koyu: false, murekkep: "siyah" },
        { id: "kirmizi", ad: "Kırmızı kulp", g: "kupa-kirmizi.jpg", koyu: false, murekkep: "siyah" }
      ],
      alanlar: [{ id: "govde", ad: "Gövde", r: { x: 26, y: 30, w: 34, h: 38 } }],
      secimler: [],
      tasarimlar: ["foto-cerceve", "cicek-celengi", "once-kahve", "cift-tarih", "el-yazisi",
                   "pati", "dogum-yili", "monogram", "yildiz-harita", "kalp-cizgi"]
    },
    "uv-dtf-baski": {
      ad: "UV DTF · cam bardak", vurgu: "Soğuk baskı, sert yüzey",
      varyant_ad: "Ürün",
      varyantlar: [
        { id: "cam", ad: "Cam kutu bardak", g: "cambardak.jpg", koyu: false, murekkep: "siyah" }
      ],
      alanlar: [{ id: "govde", ad: "Gövde sargısı", r: { x: 36, y: 28, w: 28, h: 42 } }],
      secimler: [],
      tasarimlar: ["cicek-celengi", "el-yazisi", "isim-serit", "cift-tarih", "yildiz-harita",
                   "dag-gunes", "monogram", "once-kahve"]
    },
    "baskili-cakmak": {
      ad: "Baskılı çakmak", vurgu: "Elden ele dolaşan logo",
      varyant_ad: "Gövde",
      varyantlar: [
        { id: "siyah", ad: "Siyah", g: "cakmak-siyah.jpg", koyu: true, murekkep: "beyaz" }
      ],
      alanlar: [{ id: "on", ad: "Ön yüz", r: { x: 38, y: 40, w: 20, h: 40 } }],
      secimler: [],
      tasarimlar: PROMO_TASARIM
    },
    "baskili-kalem": {
      ad: "Baskılı kalem", vurgu: "Her imzada görünen isim",
      varyant_ad: "Gövde",
      varyantlar: [
        { id: "siyah", ad: "Mat siyah", g: "kalem-siyah.jpg", koyu: true, murekkep: "beyaz" }
      ],
      alanlar: [{ id: "govde", ad: "Gövde boyu", r: { x: 16, y: 45.5, w: 44, h: 6.5 } }],
      secimler: [],
      tasarimlar: ["isim-serit", "monogram", "el-yazisi", "takim-rozeti"]
    },
    "kisiye-ozel-anahtarlik": {
      ad: "Kişiye özel anahtarlık", vurgu: "Cebinde taşınan hatıra",
      varyant_ad: "Gövde",
      varyantlar: [
        { id: "metal", ad: "Metal", g: "anahtarlik-metal.jpg", koyu: false, murekkep: "siyah" },
        { id: "ahsap", ad: "Ahşap", g: "anahtarlik-ahsap.jpg", koyu: false, murekkep: "siyah", alan: { on: { x: 37, y: 40, w: 26, h: 48 } } }
      ],
      alanlar: [{ id: "on", ad: "Ön yüz", r: { x: 32, y: 50, w: 32, h: 32 } }],
      secimler: [],
      tasarimlar: ["foto-cerceve", "monogram", "el-yazisi", "pati", "isim-serit", "kus-ay", "dag-gunes"]
    },
    "magnetli-kapak-acacagi": {
      ad: "Magnetli kapak açacağı", vurgu: "Buzdolabında kalıcı yer",
      varyant_ad: "Gövde",
      varyantlar: [
        { id: "celik", ad: "Çelik", g: "acacak-celik.jpg", koyu: false, murekkep: "siyah" }
      ],
      alanlar: [{ id: "on", ad: "Ön yüz", r: { x: 34, y: 16, w: 32, h: 42 } }],
      secimler: [],
      tasarimlar: ["isim-serit", "monogram", "el-yazisi", "sehir-tipografi", "takim-rozeti"]
    },
    "dtf-baski": {
      ad: "DTF baskı · tekstil", vurgu: "Kumaşa tam renkli transfer",
      varyant_ad: "Ürün ve renk",
      varyantlar: [
        { id: "tisort-beyaz", ad: "Tişört · Beyaz", g: "tisort-beyaz.jpg", koyu: false, murekkep: "siyah" },
        { id: "tisort-siyah", ad: "Tişört · Siyah", g: "tisort-siyah.jpg", koyu: true, murekkep: "beyaz" },
        { id: "hoodie-siyah", ad: "Hoodie · Siyah", g: "hoodie-siyah.jpg", koyu: true, murekkep: "beyaz", alan: { gogus: { x: 34, y: 34, w: 32, h: 24 }, "gogus-sol": { x: 38, y: 36, w: 11, h: 9 }, sirt: { x: 29, y: 31, w: 42, h: 30 } } },
        { id: "sweat-gri", ad: "Sweatshirt · Gri", g: "sweatshirt-gri.jpg", koyu: false, murekkep: "siyah", alan: { gogus: { x: 34, y: 29, w: 32, h: 28 }, "gogus-sol": { x: 38, y: 31, w: 11, h: 9 }, sirt: { x: 29, y: 26, w: 42, h: 34 } } }
      ],
      alanlar: [
        { id: "gogus", ad: "Göğüs orta", r: { x: 33, y: 26, w: 34, h: 30 } },
        { id: "gogus-sol", ad: "Göğüs (küçük)", r: { x: 37, y: 28, w: 12, h: 10 } },
        { id: "sirt", ad: "Büyük baskı (sırt)", r: { x: 28, y: 24, w: 44, h: 36 } }
      ],
      secimler: [{ id: "beden", ad: "Beden", secenekler: BEDEN, varsayilan: "L" }],
      tasarimlar: TEKSTIL_TASARIM
    }
  };

  /* ---------- vitrin: her ürün için hazır kurulumlar ---------- */
  var VITRIN = {
    "baskili-tisort": [
      { ad: "Uludağ rozeti", varyant: "siyah", tasarim: "dag-gunes", murekkep: "beyaz", alan: "gogus", olcek: .98 },
      { ad: "Çift tişörtü", varyant: "beyaz", tasarim: "cift-tarih", murekkep: "siyah", alan: "gogus", olcek: 1 },
      { ad: "Bursa silüeti", varyant: "lacivert", tasarim: "bursa-silueti", murekkep: "beyaz", alan: "gogus", olcek: 1 },
      { ad: "Doğum yılı", varyant: "siyah", tasarim: "dogum-yili", murekkep: "altin", alan: "gogus", olcek: 1 },
      { ad: "Evcil dostunuz", varyant: "beyaz", tasarim: "pati", murekkep: "siyah", alan: "gogus", olcek: .9 },
      { ad: "Ekip rozeti", varyant: "lacivert", tasarim: "takim-rozeti", murekkep: "beyaz", alan: "gogus-sol", olcek: 1 }
    ],
    "baskili-sweatshirt-hoodie": [
      { ad: "Tipografik şehir", varyant: "hoodie-siyah", tasarim: "sehir-tipografi", murekkep: "beyaz", alan: "sirt", olcek: 1 },
      { ad: "Kuş ve ay", varyant: "hoodie-krem", tasarim: "kus-ay", murekkep: "siyah", alan: "gogus", olcek: .96 },
      { ad: "Yıldız haritası", varyant: "hoodie-siyah", tasarim: "yildiz-harita", murekkep: "altin", alan: "gogus", olcek: .96 },
      { ad: "Monogram", varyant: "sweat-gri", tasarim: "monogram", murekkep: "siyah", alan: "gogus-sol", olcek: 1 },
      { ad: "Çift hoodie", varyant: "hoodie-krem", tasarim: "kalp-cizgi", murekkep: "kirmizi", alan: "gogus", olcek: 1 },
      { ad: "Takım", varyant: "hoodie-siyah", tasarim: "takim-rozeti", murekkep: "beyaz", alan: "sirt", olcek: 1 }
    ],
    "baskili-yelek": [
      { ad: "Ekip monogramı", varyant: "lacivert", tasarim: "monogram", murekkep: "beyaz", alan: "gogus-sol", olcek: 1 },
      { ad: "Görev şeridi", varyant: "lacivert", tasarim: "isim-serit", murekkep: "beyaz", alan: "sirt", olcek: 1 },
      { ad: "Takım rozeti", varyant: "lacivert", tasarim: "takim-rozeti", murekkep: "altin", alan: "sirt", olcek: 1 },
      { ad: "Kulüp", varyant: "lacivert", tasarim: "dag-gunes", murekkep: "beyaz", alan: "sirt", olcek: .94 }
    ],
    "kisiye-ozel-kupa": [
      { ad: "Fotoğraflı kupa", varyant: "beyaz", tasarim: "foto-cerceve", murekkep: "siyah", alan: "govde", olcek: 1 },
      { ad: "Çiçek çelengi", varyant: "beyaz", tasarim: "cicek-celengi", murekkep: "siyah", alan: "govde", olcek: 1 },
      { ad: "Önce kahve", varyant: "kirmizi", tasarim: "once-kahve", murekkep: "siyah", alan: "govde", olcek: 1 },
      { ad: "Çift kupası", varyant: "kirmizi", tasarim: "cift-tarih", murekkep: "siyah", alan: "govde", olcek: 1 },
      { ad: "El yazısı isim", varyant: "beyaz", tasarim: "el-yazisi", murekkep: "kirmizi", alan: "govde", olcek: 1 },
      { ad: "Pati", varyant: "beyaz", tasarim: "pati", murekkep: "siyah", alan: "govde", olcek: .96 }
    ],
    "uv-dtf-baski": [
      { ad: "Çiçek sargı", varyant: "cam", tasarim: "cicek-celengi", murekkep: "siyah", alan: "govde", olcek: 1 },
      { ad: "İsimli bardak", varyant: "cam", tasarim: "el-yazisi", murekkep: "siyah", alan: "govde", olcek: 1 },
      { ad: "Tarihli sargı", varyant: "cam", tasarim: "cift-tarih", murekkep: "siyah", alan: "govde", olcek: 1 },
      { ad: "Yıldız haritası", varyant: "cam", tasarim: "yildiz-harita", murekkep: "siyah", alan: "govde", olcek: 1 }
    ],
    "baskili-cakmak": [
      { ad: "Monogram", varyant: "siyah", tasarim: "monogram", murekkep: "beyaz", alan: "on", olcek: 1 },
      { ad: "İsim şeridi", varyant: "siyah", tasarim: "isim-serit", murekkep: "beyaz", alan: "on", olcek: 1 },
      { ad: "Kuş ve ay", varyant: "siyah", tasarim: "kus-ay", murekkep: "altin", alan: "on", olcek: 1 }
    ],
    "baskili-kalem": [
      { ad: "İsim şeridi", varyant: "siyah", tasarim: "isim-serit", murekkep: "beyaz", alan: "govde", olcek: 1 },
      { ad: "Monogram", varyant: "siyah", tasarim: "monogram", murekkep: "beyaz", alan: "govde", olcek: 1 },
      { ad: "El yazısı", varyant: "siyah", tasarim: "el-yazisi", murekkep: "altin", alan: "govde", olcek: 1 }
    ],
    "kisiye-ozel-anahtarlik": [
      { ad: "Fotoğraflı", varyant: "metal", tasarim: "foto-cerceve", murekkep: "siyah", alan: "on", olcek: 1 },
      { ad: "Monogram", varyant: "ahsap", tasarim: "monogram", murekkep: "siyah", alan: "on", olcek: 1 },
      { ad: "Pati", varyant: "metal", tasarim: "pati", murekkep: "siyah", alan: "on", olcek: 1 },
      { ad: "El yazısı", varyant: "ahsap", tasarim: "el-yazisi", murekkep: "siyah", alan: "on", olcek: 1 }
    ],
    "magnetli-kapak-acacagi": [
      { ad: "Monogram", varyant: "celik", tasarim: "monogram", murekkep: "siyah", alan: "on", olcek: 1 },
      { ad: "İsim şeridi", varyant: "celik", tasarim: "isim-serit", murekkep: "siyah", alan: "on", olcek: 1 },
      { ad: "Şehir", varyant: "celik", tasarim: "sehir-tipografi", murekkep: "siyah", alan: "on", olcek: .96 }
    ],
    "dtf-baski": [
      { ad: "Tam renkli göğüs", varyant: "tisort-siyah", tasarim: "dag-gunes", murekkep: "beyaz", alan: "gogus", olcek: .98 },
      { ad: "Açık kumaş", varyant: "tisort-beyaz", tasarim: "bursa-silueti", murekkep: "siyah", alan: "gogus", olcek: 1 },
      { ad: "Sırt baskısı", varyant: "hoodie-siyah", tasarim: "sehir-tipografi", murekkep: "beyaz", alan: "sirt", olcek: 1 },
      { ad: "Küçük logo", varyant: "sweat-gri", tasarim: "monogram", murekkep: "siyah", alan: "gogus-sol", olcek: 1 }
    ]
  };

  return {
    wa: "905411602603",
    eposta: "lunagency2603@gmail.com",
    gorselKok: G,
    tasarimlar: TASARIM,
    murekkepler: MUREKKEP,
    urunler: URUN,
    vitrinler: VITRIN,
    kacir: kacir
  };
})();
