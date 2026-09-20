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
  var _say = 0;
  function benzersiz() { return "lh" + (++_say); }

  /* ---------- hazır tasarımlar ----------
     oran : genişlik / yükseklik
     alanlar : kullanıcının dolduracağı metin kutuları
     ciz(o) : {renk, metin:{...}} → SVG içeriği (viewBox 0 0 100 100/oran)  */
  var TASARIM = {

    /* ══════════ 2026 çizgisi — yeni tasarımlar ══════════ */

    "tipografi-kilit": {
      ad: "Tipografi kilidi", etiket: "Tipografi", oran: 1,
      alanlar: [{ id: "ust", ad: "Üst satır", varsayilan: "KURULUŞ 2026", azami: 20 },
                { id: "orta", ad: "Büyük yazı", varsayilan: "YEŞİL", azami: 9 },
                { id: "alt", ad: "Alt satır", varsayilan: "BURSA · TÜRKİYE", azami: 24 }],
      ciz: function (o) {
        var c = o.renk, v = o.vurgu;
        return '<text x="50" y="22" text-anchor="middle" font-family="' + SANS + '" font-size="6" letter-spacing="5" fill="' + c + '">' + kacir((o.metin.ust || "").toUpperCase()) + '</text>' +
          '<path d="M12 28h76" stroke="' + c + '" stroke-width=".9"/>' +
          '<text x="50" y="62" text-anchor="middle" font-family="' + KALIN + '" font-size="34" letter-spacing="-2" fill="' + c + '">' + kacir((o.metin.orta || "").toUpperCase()) + '</text>' +
          '<path d="M12 70h76" stroke="' + v + '" stroke-width="2.4"/>' +
          '<text x="50" y="82" text-anchor="middle" font-family="' + SANS + '" font-size="6" letter-spacing="5" fill="' + c + '">' + kacir((o.metin.alt || "").toUpperCase()) + '</text>';
      }
    },

    "varsity": {
      ad: "Kolej rozeti", etiket: "Retro", oran: 1,
      alanlar: [{ id: "ust", ad: "Kavisli yazı", varsayilan: "LUNA", azami: 14 },
                { id: "orta", ad: "Sayı ya da harf", varsayilan: "16", azami: 3 },
                { id: "alt", ad: "Alt satır", varsayilan: "BURSA", azami: 18 }],
      ciz: function (o) {
        var c = o.renk, v = o.vurgu, id = benzersiz();
        return '<defs><path id="' + id + '" d="M14 58a36 36 0 0 1 72 0" fill="none"/></defs>' +
          '<text font-family="' + KALIN + '" font-size="11" letter-spacing="2.4" fill="' + c + '">' +
          '<textPath href="#' + id + '" xlink:href="#' + id + '" startOffset="50%" text-anchor="middle">' +
          kacir((o.metin.ust || "").toUpperCase()) + '</textPath></text>' +
          '<text x="50" y="66" text-anchor="middle" font-family="' + KALIN + '" font-size="34" fill="' + c + '" stroke="' + v + '" stroke-width="1.2" paint-order="stroke">' + kacir((o.metin.orta || "").toUpperCase()) + '</text>' +
          '<path d="M24 74h52" stroke="' + v + '" stroke-width="2"/>' +
          '<text x="50" y="85" text-anchor="middle" font-family="' + SANS + '" font-size="6.4" letter-spacing="4" fill="' + c + '">' + kacir((o.metin.alt || "").toUpperCase()) + '</text>';
      }
    },

    "geometrik-kedi": {
      ad: "Geometrik kedi", etiket: "Hayvan", oran: 1,
      alanlar: [{ id: "isim", ad: "İsim (isteğe bağlı)", varsayilan: "", azami: 16 }],
      ciz: function (o) {
        var c = o.renk, v = o.vurgu, ad = (o.metin.isim || "").toUpperCase();
        return '<path d="M28 34l4-16 14 10z" fill="' + c + '"/>' +
          '<path d="M72 34l-4-16-14 10z" fill="' + c + '"/>' +
          '<path d="M50 20l22 14-6 30-16 12-16-12-6-30z" fill="none" stroke="' + c + '" stroke-width="1.8" stroke-linejoin="round"/>' +
          '<path d="M38 42l8 5-8 5z" fill="' + c + '"/>' +
          '<path d="M62 42l-8 5 8 5z" fill="' + c + '"/>' +
          '<path d="M46 58h8l-4 5z" fill="' + v + '"/>' +
          '<path d="M50 63v5M50 68l-7 4M50 68l7 4" stroke="' + c + '" stroke-width="1.2" stroke-linecap="round"/>' +
          (ad ? '<text x="50" y="88" text-anchor="middle" font-family="' + SANS + '" font-size="6.4" letter-spacing="4" fill="' + c + '">' + kacir(ad) + '</text>' : "");
      }
    },

    "goksel-faz": {
      ad: "Ay evreleri", etiket: "Göksel", oran: 2.1,
      alanlar: [{ id: "alt", ad: "Alt yazı", varsayilan: "AYNI GÖKYÜZÜ", azami: 24 }],
      ciz: function (o) {
        var c = o.renk, v = o.vurgu, s = "", x0 = 14, ad = 18, r = 6;
        for (var i = 0; i < 5; i++) {
          var x = x0 + i * ad, y = 20;
          s += '<circle cx="' + x + '" cy="' + y + '" r="' + r + '" fill="none" stroke="' + c + '" stroke-width="1"/>';
          if (i === 1) s += '<path d="M' + x + ' ' + (y - r) + 'a' + r + ' ' + r + ' 0 0 1 0 ' + (2 * r) + 'a4 ' + r + ' 0 0 0 0 -' + (2 * r) + 'z" fill="' + c + '"/>';
          if (i === 2) s += '<path d="M' + x + ' ' + (y - r) + 'a' + r + ' ' + r + ' 0 0 1 0 ' + (2 * r) + 'z" fill="' + c + '"/>';
          if (i === 3) s += '<path d="M' + x + ' ' + (y - r) + 'a' + r + ' ' + r + ' 0 0 1 0 ' + (2 * r) + 'a8 ' + r + ' 0 0 1 0 -' + (2 * r) + 'z" fill="' + c + '"/>';
          if (i === 4) s += '<circle cx="' + x + '" cy="' + y + '" r="' + r + '" fill="' + c + '"/>';
        }
        s += '<path d="M8 32h84" stroke="' + v + '" stroke-width="1"/>';
        s += '<text x="50" y="42" text-anchor="middle" font-family="' + SANS + '" font-size="6.2" letter-spacing="4.5" fill="' + c + '">' + kacir((o.metin.alt || "").toUpperCase()) + '</text>';
        return s;
      }
    },

    "soyut-geometri": {
      ad: "Soyut geometri", etiket: "Geometri", oran: 1, alanlar: [],
      ciz: function (o) {
        var c = o.renk, v = o.vurgu;
        return '<circle cx="42" cy="38" r="22" fill="none" stroke="' + c + '" stroke-width="1.6"/>' +
          '<path d="M64 38a22 22 0 0 1-22 22V38z" fill="' + v + '"/>' +
          '<rect x="58" y="14" width="14" height="14" transform="rotate(45 65 21)" fill="none" stroke="' + c + '" stroke-width="1.4"/>' +
          '<path d="M22 70h56M30 76h48M38 82h32" stroke="' + c + '" stroke-width="1.6" stroke-linecap="round"/>' +
          '<circle cx="76" cy="58" r="3" fill="' + v + '"/>';
      }
    },

    "el-cizimi": {
      ad: "El çizimi", etiket: "Çizim", oran: 1,
      alanlar: [{ id: "alt", ad: "El yazısı", varsayilan: "uzun yol", azami: 20 }],
      ciz: function (o) {
        var c = o.renk, v = o.vurgu;
        return '<circle cx="62" cy="30" r="9" fill="none" stroke="' + v + '" stroke-width="1.6"/>' +
          '<path d="M18 62c5-9 9-14 13-19 3-4 6-2 9 2 3 5 6 11 9 8 4-4 7-12 11-8 4 3 9 12 22 17" fill="none" stroke="' + c + '" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>' +
          '<path d="M14 66c8 2 20 3 36 3s28-1 36-3" fill="none" stroke="' + c + '" stroke-width="1.5" stroke-linecap="round"/>' +
          '<path d="M26 72c6 1 12 2 18 1" fill="none" stroke="' + c + '" stroke-width="1" opacity=".6" stroke-linecap="round"/>' +
          '<text x="50" y="86" text-anchor="middle" font-family="' + SERIF + '" font-style="italic" font-size="13" fill="' + c + '">' + kacir(o.metin.alt) + '</text>';
      }
    },

    "retro-dalga": {
      ad: "Retro dalga", etiket: "Retro", oran: 1,
      alanlar: [{ id: "ust", ad: "Kavisli yazı", varsayilan: "GÜNEŞ", azami: 16 },
                { id: "alt", ad: "Alt satır", varsayilan: "1995", azami: 14 }],
      ciz: function (o) {
        var c = o.renk, v = o.vurgu, id = benzersiz(), s = "";
        s += '<defs><path id="' + id + '" d="M16 54a34 34 0 0 1 68 0" fill="none"/></defs>';
        s += '<circle cx="50" cy="56" r="17" fill="' + v + '"/>';
        for (var i = 0; i < 5; i++)
          s += '<path d="M33 ' + (50 + i * 4.6) + 'h34" stroke="' + c + '" stroke-width="' + (2.6 - i * .35) + '"/>';
        s += '<text font-family="' + KALIN + '" font-size="10" letter-spacing="3" fill="' + c + '">' +
          '<textPath href="#' + id + '" xlink:href="#' + id + '" startOffset="50%" text-anchor="middle">' +
          kacir((o.metin.ust || "").toUpperCase()) + '</textPath></text>';
        s += '<path d="M22 78q7-5 14 0t14 0 14 0 14 0" fill="none" stroke="' + c + '" stroke-width="1.6"/>';
        s += '<text x="50" y="90" text-anchor="middle" font-family="' + SANS + '" font-size="6.4" letter-spacing="5" fill="' + c + '">' + kacir((o.metin.alt || "").toUpperCase()) + '</text>';
        return s;
      }
    },

    "sozluk": {
      ad: "Sözlük maddesi", etiket: "Tipografi", oran: 1.7,
      alanlar: [{ id: "kelime", ad: "Kelime", varsayilan: "elif", azami: 16 },
                { id: "tur", ad: "Tür", varsayilan: "isim", azami: 14 },
                { id: "tanim", ad: "Tanım", varsayilan: "gün ağarırken gelen huzur.", azami: 42 }],
      ciz: function (o) {
        var c = o.renk, v = o.vurgu;
        return '<text x="8" y="22" font-family="' + SERIF + '" font-size="19" fill="' + c + '">' + kacir(o.metin.kelime) + '</text>' +
          '<text x="8" y="32" font-family="' + SERIF + '" font-style="italic" font-size="7" fill="' + c + '" opacity=".75">' + kacir(o.metin.tur) + '</text>' +
          '<path d="M8 37h84" stroke="' + v + '" stroke-width="1.2"/>' +
          '<text x="8" y="48" font-family="' + SANS + '" font-size="7" fill="' + c + '"><tspan font-family="' + KALIN + '">1.</tspan> ' + kacir(o.metin.tanim) + '</text>';
      }
    },

    "koordinat": {
      ad: "Koordinat", etiket: "Yer", oran: 1.5,
      alanlar: [{ id: "yer", ad: "Yer", varsayilan: "BURSA", azami: 18 },
                { id: "kod", ad: "Koordinat", varsayilan: "40.1885° K · 29.0610° D", azami: 30 }],
      ciz: function (o) {
        var c = o.renk, v = o.vurgu;
        return '<circle cx="50" cy="26" r="11" fill="none" stroke="' + c + '" stroke-width="1.3"/>' +
          '<circle cx="50" cy="26" r="3" fill="' + v + '"/>' +
          '<path d="M50 9v8M50 35v8M33 26h8M59 26h8" stroke="' + c + '" stroke-width="1.3" stroke-linecap="round"/>' +
          '<text x="50" y="54" text-anchor="middle" font-family="' + KALIN + '" font-size="15" letter-spacing="3" fill="' + c + '">' + kacir((o.metin.yer || "").toUpperCase()) + '</text>' +
          '<text x="50" y="63" text-anchor="middle" font-family="' + SANS + '" font-size="5.4" letter-spacing="1.8" fill="' + c + '" opacity=".85">' + kacir(o.metin.kod) + '</text>';
      }
    },

    "cerceve-rozet": {
      ad: "Çerçeve rozeti", etiket: "Minimal", oran: 1.35,
      alanlar: [{ id: "ust", ad: "Üst yazı", varsayilan: "EST. 2026", azami: 16 },
                { id: "orta", ad: "Orta yazı", varsayilan: "LUNA", azami: 16 },
                { id: "alt", ad: "Alt yazı", varsayilan: "BURSA", azami: 18 }],
      ciz: function (o) {
        var c = o.renk, v = o.vurgu;
        return '<rect x="8" y="12" width="84" height="50" fill="none" stroke="' + c + '" stroke-width="1.6"/>' +
          '<rect x="12" y="16" width="76" height="42" fill="none" stroke="' + c + '" stroke-width=".7" opacity=".55"/>' +
          '<text x="50" y="28" text-anchor="middle" font-family="' + SANS + '" font-size="5.4" letter-spacing="4" fill="' + c + '">' + kacir((o.metin.ust || "").toUpperCase()) + '</text>' +
          '<text x="50" y="44" text-anchor="middle" font-family="' + SERIF + '" font-size="17" letter-spacing="2" fill="' + c + '">' + kacir((o.metin.orta || "").toUpperCase()) + '</text>' +
          '<path d="M44 50h12" stroke="' + v + '" stroke-width="1.4"/>' +
          '<text x="50" y="56" text-anchor="middle" font-family="' + SANS + '" font-size="4.8" letter-spacing="3.4" fill="' + c + '">' + kacir((o.metin.alt || "").toUpperCase()) + '</text>';
      }
    },

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
    { id: "siyah", ad: "Siyah", renk: "#14141A", vurgu: "#E8452C", acik: false },
    { id: "beyaz", ad: "Beyaz", renk: "#F6F4EF", vurgu: "#E8452C", acik: true },
    { id: "kirmizi", ad: "Vermilyon", renk: "#E8452C", vurgu: "#14141A", acik: false },
    { id: "altin", ad: "Altın", renk: "#C79A3F", vurgu: "#14141A", acik: true },
    { id: "lacivert", ad: "Lacivert", renk: "#1F2E4A", vurgu: "#C79A3F", acik: false },
    { id: "krem", ad: "Krem", renk: "#EDE7DA", vurgu: "#E8452C", acik: true }
  ];

  // Baskı kumaşın gölgesini alsın: açık üründe multiply, koyuda screen.
  // Mürekkep yönüyle uyuşmuyorsa karışım uygulanmaz (yoksa baskı kaybolur).
  function karisimSec(varyant, murekkep) {
    var k = varyant.karisim;
    if (k === "screen") return murekkep.acik ? "screen" : "normal";
    if (k === "multiply") return murekkep.acik ? "normal" : "multiply";
    return "normal";
  }

  var BEDEN = ["XS", "S", "M", "L", "XL", "2XL", "3XL"];

  var T_ALAN = [
    { id: "gogus", ad: "Göğüs orta", r: { x: 33, y: 32, w: 34, h: 30 } },
    { id: "gogus-sol", ad: "Göğüs (küçük)", r: { x: 37, y: 34, w: 12, h: 10 } },
    { id: "sirt", ad: "Büyük baskı (sırt)", r: { x: 29, y: 30, w: 42, h: 36 } }
  ];
  var SWEAT_ALAN = { gogus: { x: 34, y: 24, w: 32, h: 27 },
                     "gogus-sol": { x: 38, y: 26, w: 11, h: 9 },
                     sirt: { x: 30, y: 22, w: 40, h: 33 } };
  var HOODIE_ALAN = { gogus: { x: 34, y: 32, w: 32, h: 24 },
                      "gogus-sol": { x: 38, y: 34, w: 11, h: 9 },
                      sirt: { x: 30, y: 30, w: 40, h: 28 } };

  var TEKSTIL_TASARIM = ["tipografi-kilit", "varsity", "retro-dalga", "geometrik-kedi",
    "goksel-faz", "soyut-geometri", "el-cizimi", "kus-ay", "bursa-silueti", "sehir-tipografi",
    "dag-gunes", "koordinat", "cift-tarih", "yildiz-harita", "dogum-yili", "pati",
    "takim-rozeti", "monogram", "foto-cerceve", "kalp-cizgi"];

  var TISORT_VARYANT = [
    { id: "beyaz", ad: "Optik beyaz", g: "tisort-beyaz.jpg", koyu: false, murekkep: "siyah", karisim: "multiply" },
    { id: "krem", ad: "Ekru krem", g: "tisort-krem.jpg", koyu: false, murekkep: "siyah", karisim: "multiply" },
    { id: "siyah", ad: "Yıkamalı siyah", g: "tisort-siyah.jpg", koyu: true, murekkep: "beyaz", karisim: "screen" },
    { id: "lacivert", ad: "Lacivert", g: "tisort-lacivert.jpg", koyu: true, murekkep: "beyaz", karisim: "screen" },
    { id: "bordo", ad: "Bordo", g: "tisort-bordo.jpg", koyu: true, murekkep: "krem", karisim: "screen" }
  ];

  /* ---------- ürünler ---------- */
  var URUN = {
    "baskili-tisort": {
      ad: "Oversize baskılı tişört", vurgu: "Ağır kumaş, düşük omuz",
      varyant_ad: "Renk", varyantlar: TISORT_VARYANT, alanlar: T_ALAN,
      secimler: [{ id: "beden", ad: "Beden", secenekler: BEDEN, varsayilan: "L" }],
      tasarimlar: TEKSTIL_TASARIM
    },
    "dtf-baski": {
      ad: "DTF baskı · tekstil", vurgu: "Kumaşa tam renkli transfer",
      varyant_ad: "Ürün ve renk",
      varyantlar: [
        { id: "tisort-beyaz", ad: "Tişört · Beyaz", g: "tisort-beyaz.jpg", koyu: false, murekkep: "siyah", karisim: "multiply" },
        { id: "tisort-siyah", ad: "Tişört · Siyah", g: "tisort-siyah.jpg", koyu: true, murekkep: "beyaz", karisim: "screen" },
        { id: "tisort-bordo", ad: "Tişört · Bordo", g: "tisort-bordo.jpg", koyu: true, murekkep: "krem", karisim: "screen" },
        { id: "hoodie-siyah", ad: "Hoodie · Siyah", g: "hoodie-siyah.jpg", koyu: true, murekkep: "beyaz", karisim: "screen", alan: HOODIE_ALAN },
        { id: "sweat-gri", ad: "Sweatshirt · Gri", g: "sweatshirt-gri.jpg", koyu: false, murekkep: "siyah", karisim: "multiply", alan: SWEAT_ALAN }
      ],
      alanlar: T_ALAN,
      secimler: [{ id: "beden", ad: "Beden", secenekler: BEDEN, varsayilan: "L" }],
      tasarimlar: TEKSTIL_TASARIM
    },
    "baskili-sweatshirt-hoodie": {
      ad: "Oversize sweatshirt / hoodie", vurgu: "Kalın kumaş, geniş baskı alanı",
      varyant_ad: "Ürün ve renk",
      varyantlar: [
        { id: "hoodie-siyah", ad: "Hoodie · Siyah", g: "hoodie-siyah.jpg", koyu: true, murekkep: "beyaz", karisim: "screen" },
        { id: "hoodie-krem", ad: "Hoodie · Krem", g: "hoodie-krem.jpg", koyu: false, murekkep: "siyah", karisim: "multiply",
          alan: { gogus: { x: 34, y: 33, w: 32, h: 23 }, "gogus-sol": { x: 38, y: 35, w: 11, h: 9 }, sirt: { x: 30, y: 31, w: 40, h: 27 } } },
        { id: "sweat-gri", ad: "Sweatshirt · Gri", g: "sweatshirt-gri.jpg", koyu: false, murekkep: "siyah", karisim: "multiply", alan: SWEAT_ALAN }
      ],
      alanlar: [
        { id: "gogus", ad: "Göğüs orta", r: HOODIE_ALAN.gogus },
        { id: "gogus-sol", ad: "Göğüs (küçük)", r: HOODIE_ALAN["gogus-sol"] },
        { id: "sirt", ad: "Büyük baskı (sırt)", r: HOODIE_ALAN.sirt }
      ],
      secimler: [{ id: "beden", ad: "Beden", secenekler: BEDEN, varsayilan: "L" }],
      tasarimlar: TEKSTIL_TASARIM
    },
    "baskili-yelek": {
      ad: "Baskılı yelek", vurgu: "Saha, kurye ve etkinlik ekibi",
      varyant_ad: "Model",
      varyantlar: [
        { id: "lacivert", ad: "Softshell · Lacivert", g: "yelek-lacivert.jpg", koyu: true, murekkep: "beyaz", karisim: "screen" },
        { id: "siyah", ad: "Şişme · Siyah", g: "yelek-siyah.jpg", koyu: true, murekkep: "beyaz", karisim: "screen",
          alan: { "gogus-sol": { x: 33, y: 31, w: 12, h: 10 }, "gogus-sag": { x: 55, y: 31, w: 12, h: 10 } } }
      ],
      alanlar: [
        { id: "gogus-sol", ad: "Göğüs sol", r: { x: 34, y: 33, w: 12, h: 10 } },
        { id: "gogus-sag", ad: "Göğüs sağ", r: { x: 54, y: 33, w: 12, h: 10 } }
      ],
      secimler: [{ id: "beden", ad: "Beden", secenekler: ["S", "M", "L", "XL", "2XL", "3XL"], varsayilan: "L" }],
      tasarimlar: ["monogram", "takim-rozeti", "isim-serit", "cerceve-rozet", "el-yazisi",
                   "kus-ay", "dag-gunes", "geometrik-kedi", "koordinat"]
    },
    "kisiye-ozel-kupa": {
      ad: "Kişiye özel kupa", vurgu: "Her sabah eline alınan hediye",
      varyant_ad: "Kupa",
      varyantlar: [
        { id: "beyaz", ad: "Beyaz", g: "kupa-beyaz.jpg", koyu: false, murekkep: "siyah", karisim: "multiply" },
        { id: "kirmizi", ad: "Kırmızı kulp", g: "kupa-kirmizi.jpg", koyu: false, murekkep: "siyah", karisim: "multiply",
          alan: { govde: { x: 31, y: 37, w: 26, h: 29 } } },
        { id: "siyah", ad: "Mat siyah", g: "kupa-siyah.jpg", koyu: true, murekkep: "beyaz", karisim: "screen",
          alan: { govde: { x: 30, y: 30, w: 28, h: 34 } } }
      ],
      alanlar: [{ id: "govde", ad: "Gövde", r: { x: 38, y: 38, w: 20, h: 27 } }],
      secimler: [],
      tasarimlar: ["foto-cerceve", "cicek-celengi", "once-kahve", "cift-tarih", "el-yazisi",
                   "sozluk", "koordinat", "pati", "dogum-yili", "monogram", "yildiz-harita",
                   "kalp-cizgi", "goksel-faz", "cerceve-rozet"]
    },
    "uv-dtf-baski": {
      ad: "UV DTF · sert yüzey", vurgu: "Soğuk baskı: cam, metal, ahşap",
      varyant_ad: "Ürün",
      varyantlar: [
        { id: "cam", ad: "Cam kutu bardak", g: "cambardak.jpg", koyu: false, murekkep: "siyah", karisim: "multiply" },
        { id: "termos", ad: "Termos", g: "termos-siyah.jpg", koyu: true, murekkep: "beyaz", karisim: "screen",
          alan: { govde: { x: 40, y: 36, w: 22, h: 30 } } }
      ],
      alanlar: [{ id: "govde", ad: "Gövde sargısı", r: { x: 37, y: 34, w: 26, h: 34 } }],
      secimler: [],
      tasarimlar: ["cicek-celengi", "el-yazisi", "isim-serit", "cift-tarih", "yildiz-harita",
                   "goksel-faz", "koordinat", "monogram", "once-kahve", "cerceve-rozet"]
    },
    "baskili-cakmak": {
      ad: "Baskılı çakmak", vurgu: "Elden ele dolaşan logo",
      varyant_ad: "Gövde",
      varyantlar: [
        { id: "siyah", ad: "Siyah", g: "cakmak-siyah.jpg", koyu: true, murekkep: "beyaz", karisim: "screen" },
        { id: "krem", ad: "Krem", g: "cakmak-krem.jpg", koyu: false, murekkep: "siyah", karisim: "multiply",
          alan: { on: { x: 38, y: 42, w: 13, h: 34 } } }
      ],
      alanlar: [{ id: "on", ad: "Ön yüz", r: { x: 43, y: 45, w: 13, h: 34 } }],
      secimler: [],
      tasarimlar: ["monogram", "isim-serit", "el-yazisi", "kus-ay", "cerceve-rozet", "koordinat"]
    },
    "baskili-kalem": {
      ad: "Baskılı kalem", vurgu: "Her imzada görünen isim",
      varyant_ad: "Gövde",
      varyantlar: [
        { id: "siyah", ad: "Mat siyah", g: "kalem-siyah.jpg", koyu: true, murekkep: "beyaz", karisim: "screen" },
        { id: "gumus", ad: "Gümüş", g: "kalem-gumus.jpg", koyu: false, murekkep: "siyah", karisim: "multiply",
          alan: { govde: { x: 24, y: 52, w: 38, h: 7 } } }
      ],
      alanlar: [{ id: "govde", ad: "Gövde boyu", r: { x: 28, y: 53, w: 34, h: 7 } }],
      secimler: [],
      tasarimlar: ["isim-serit", "el-yazisi", "monogram", "cerceve-rozet"]
    },
    "kisiye-ozel-anahtarlik": {
      ad: "Kişiye özel anahtarlık", vurgu: "Cebinde taşınan hatıra",
      varyant_ad: "Gövde",
      varyantlar: [
        { id: "metal", ad: "Metal", g: "anahtarlik-metal.jpg", koyu: false, murekkep: "siyah", karisim: "multiply" },
        { id: "ahsap", ad: "Ahşap", g: "anahtarlik-ahsap.jpg", koyu: false, murekkep: "siyah", karisim: "multiply",
          alan: { on: { x: 41, y: 28, w: 20, h: 34 } } }
      ],
      alanlar: [{ id: "on", ad: "Ön yüz", r: { x: 42, y: 48, w: 24, h: 24 } }],
      secimler: [],
      tasarimlar: ["foto-cerceve", "monogram", "el-yazisi", "pati", "geometrik-kedi",
                   "isim-serit", "kus-ay", "koordinat", "cerceve-rozet"]
    },
    "magnetli-kapak-acacagi": {
      ad: "Magnetli kapak açacağı", vurgu: "Buzdolabında kalıcı yer",
      varyant_ad: "Gövde",
      varyantlar: [
        { id: "celik", ad: "Çelik", g: "acacak-celik.jpg", koyu: false, murekkep: "siyah", karisim: "multiply" },
        { id: "siyah", ad: "Mat siyah", g: "acacak-siyah.jpg", koyu: true, murekkep: "beyaz", karisim: "screen",
          alan: { on: { x: 37, y: 18, w: 26, h: 34 } } }
      ],
      alanlar: [{ id: "on", ad: "Ön yüz", r: { x: 43, y: 20, w: 18, h: 26 } }],
      secimler: [],
      tasarimlar: ["monogram", "isim-serit", "el-yazisi", "sehir-tipografi", "takim-rozeti",
                   "cerceve-rozet", "koordinat"]
    }
  };

  /* ---------- vitrin: her ürün için hazır kurulumlar ---------- */
  var VITRIN = {
    "baskili-tisort": [
      { ad: "Tipografi kilidi", varyant: "siyah", tasarim: "tipografi-kilit", murekkep: "beyaz", alan: "gogus", olcek: 1 },
      { ad: "Kolej rozeti", varyant: "krem", tasarim: "varsity", murekkep: "siyah", alan: "gogus", olcek: .96 },
      { ad: "Retro dalga", varyant: "bordo", tasarim: "retro-dalga", murekkep: "krem", alan: "gogus", olcek: .96 },
      { ad: "Geometrik kedi", varyant: "beyaz", tasarim: "geometrik-kedi", murekkep: "siyah", alan: "gogus", olcek: .94 },
      { ad: "Ay evreleri", varyant: "lacivert", tasarim: "goksel-faz", murekkep: "beyaz", alan: "gogus", olcek: 1 },
      { ad: "Soyut geometri", varyant: "krem", tasarim: "soyut-geometri", murekkep: "siyah", alan: "gogus", olcek: .92 },
      { ad: "El çizimi", varyant: "beyaz", tasarim: "el-cizimi", murekkep: "siyah", alan: "gogus", olcek: .94 },
      { ad: "Koordinat", varyant: "siyah", tasarim: "koordinat", murekkep: "altin", alan: "gogus", olcek: .9 },
      { ad: "Çift tişörtü", varyant: "beyaz", tasarim: "cift-tarih", murekkep: "siyah", alan: "gogus", olcek: .92 }
    ],
    "baskili-sweatshirt-hoodie": [
      { ad: "Sırt tipografisi", varyant: "hoodie-siyah", tasarim: "tipografi-kilit", murekkep: "beyaz", alan: "sirt", olcek: 1 },
      { ad: "Kolej", varyant: "hoodie-krem", tasarim: "varsity", murekkep: "siyah", alan: "gogus", olcek: .96 },
      { ad: "Kuş ve ay", varyant: "sweat-gri", tasarim: "kus-ay", murekkep: "siyah", alan: "gogus", olcek: .94 },
      { ad: "Ay evreleri", varyant: "hoodie-siyah", tasarim: "goksel-faz", murekkep: "altin", alan: "gogus", olcek: 1 },
      { ad: "Küçük monogram", varyant: "hoodie-krem", tasarim: "monogram", murekkep: "siyah", alan: "gogus-sol", olcek: 1 },
      { ad: "Takım", varyant: "sweat-gri", tasarim: "takim-rozeti", murekkep: "siyah", alan: "sirt", olcek: .85 }
    ],
    "baskili-yelek": [
      { ad: "Ekip monogramı", varyant: "lacivert", tasarim: "monogram", murekkep: "beyaz", alan: "gogus-sol", olcek: 1 },
      { ad: "Takım rozeti", varyant: "siyah", tasarim: "takim-rozeti", murekkep: "beyaz", alan: "gogus-sol", olcek: 1 },
      { ad: "İsim şeridi", varyant: "lacivert", tasarim: "isim-serit", murekkep: "beyaz", alan: "gogus-sag", olcek: 1 },
      { ad: "Çerçeve", varyant: "siyah", tasarim: "cerceve-rozet", murekkep: "altin", alan: "gogus-sol", olcek: 1 }
    ],
    "kisiye-ozel-kupa": [
      { ad: "Fotoğraflı kupa", varyant: "beyaz", tasarim: "foto-cerceve", murekkep: "siyah", alan: "govde", olcek: 1 },
      { ad: "Sözlük maddesi", varyant: "beyaz", tasarim: "sozluk", murekkep: "siyah", alan: "govde", olcek: 1 },
      { ad: "Önce kahve", varyant: "kirmizi", tasarim: "once-kahve", murekkep: "siyah", alan: "govde", olcek: .95 },
      { ad: "Ay evreleri", varyant: "siyah", tasarim: "goksel-faz", murekkep: "beyaz", alan: "govde", olcek: 1 },
      { ad: "Çiçek çelengi", varyant: "beyaz", tasarim: "cicek-celengi", murekkep: "siyah", alan: "govde", olcek: .95 },
      { ad: "Koordinat", varyant: "kirmizi", tasarim: "koordinat", murekkep: "siyah", alan: "govde", olcek: .95 }
    ],
    "uv-dtf-baski": [
      { ad: "Çiçek sargı", varyant: "cam", tasarim: "cicek-celengi", murekkep: "siyah", alan: "govde", olcek: 1 },
      { ad: "İsimli bardak", varyant: "cam", tasarim: "el-yazisi", murekkep: "siyah", alan: "govde", olcek: .95 },
      { ad: "Ay evreleri", varyant: "termos", tasarim: "goksel-faz", murekkep: "beyaz", alan: "govde", olcek: 1 },
      { ad: "Koordinat", varyant: "termos", tasarim: "koordinat", murekkep: "beyaz", alan: "govde", olcek: .95 }
    ],
    "baskili-cakmak": [
      { ad: "Monogram", varyant: "siyah", tasarim: "monogram", murekkep: "beyaz", alan: "on", olcek: 1 },
      { ad: "İsim şeridi", varyant: "krem", tasarim: "isim-serit", murekkep: "siyah", alan: "on", olcek: 1 },
      { ad: "Kuş ve ay", varyant: "siyah", tasarim: "kus-ay", murekkep: "altin", alan: "on", olcek: .95 }
    ],
    "baskili-kalem": [
      { ad: "İsim şeridi", varyant: "siyah", tasarim: "isim-serit", murekkep: "beyaz", alan: "govde", olcek: 1 },
      { ad: "El yazısı", varyant: "gumus", tasarim: "el-yazisi", murekkep: "siyah", alan: "govde", olcek: 1 },
      { ad: "Monogram", varyant: "siyah", tasarim: "monogram", murekkep: "beyaz", alan: "govde", olcek: 1 }
    ],
    "kisiye-ozel-anahtarlik": [
      { ad: "Fotoğraflı", varyant: "metal", tasarim: "foto-cerceve", murekkep: "siyah", alan: "on", olcek: 1 },
      { ad: "Geometrik kedi", varyant: "ahsap", tasarim: "geometrik-kedi", murekkep: "siyah", alan: "on", olcek: .95 },
      { ad: "Pati", varyant: "metal", tasarim: "pati", murekkep: "siyah", alan: "on", olcek: .9 },
      { ad: "El yazısı", varyant: "ahsap", tasarim: "el-yazisi", murekkep: "siyah", alan: "on", olcek: .95 }
    ],
    "magnetli-kapak-acacagi": [
      { ad: "Monogram", varyant: "celik", tasarim: "monogram", murekkep: "siyah", alan: "on", olcek: .95 },
      { ad: "İsim şeridi", varyant: "siyah", tasarim: "isim-serit", murekkep: "beyaz", alan: "on", olcek: 1 },
      { ad: "Şehir", varyant: "siyah", tasarim: "sehir-tipografi", murekkep: "beyaz", alan: "on", olcek: .9 }
    ],
    "dtf-baski": [
      { ad: "Tipografi kilidi", varyant: "tisort-siyah", tasarim: "tipografi-kilit", murekkep: "beyaz", alan: "gogus", olcek: 1 },
      { ad: "Açık kumaşta", varyant: "tisort-beyaz", tasarim: "geometrik-kedi", murekkep: "siyah", alan: "gogus", olcek: .94 },
      { ad: "Sırt baskısı", varyant: "hoodie-siyah", tasarim: "retro-dalga", murekkep: "beyaz", alan: "sirt", olcek: 1 },
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
    kacir: kacir,
    karisimSec: karisimSec
  };
})();
