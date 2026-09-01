/* ============================================================
   LUNA YAPIM — SOSYAL HESAP DEFTERİ
   ------------------------------------------------------------
   TEK YAPMAN GEREKEN: aşağıya kullanıcı adını yapıştırmak.
   Boş bırakılan ("") hesap sitede HİÇ görünmez.

   Örnek:  kullanici:"lunayapim"   →  instagram.com/lunayapim

   Kullanıcı adını yazdığın an üç yerde birden görünür:
     1) alt bilgideki İletişim sütununda
     2) iletişim sayfasındaki "Bizi takip edin" şeridinde
     3) sayfanın JSON-LD şemasındaki sameAs alanında
        (Google'a "bu hesaplar bu firmaya ait" diyen alan — bunu
         yapmayan firmaların hesapları arama sonucunda firmayla
         eşleşmiyor. Biz de yapmıyorduk; artık yapıyoruz.)
   ============================================================ */

window.LUNA_SOSYAL = [
  { ag:"instagram", ad:"Instagram", kullanici:"", adres:"https://www.instagram.com/%s" },
  { ag:"youtube",   ad:"YouTube",   kullanici:"", adres:"https://www.youtube.com/@%s" },
  { ag:"linkedin",  ad:"LinkedIn",  kullanici:"", adres:"https://www.linkedin.com/company/%s" },
  { ag:"tiktok",    ad:"TikTok",    kullanici:"", adres:"https://www.tiktok.com/@%s" },
  { ag:"x",         ad:"X",         kullanici:"", adres:"https://x.com/%s" },
  { ag:"behance",   ad:"Behance",   kullanici:"", adres:"https://www.behance.net/%s" },
  { ag:"vimeo",     ad:"Vimeo",     kullanici:"", adres:"https://vimeo.com/%s" }
];

/* Yol tarifi bağlantısı — haritadaki işletme adresini yapıştır.
   Boş bırakılırsa harita satırı görünmez.
   Nereden alınır: Google Haritalar → işletme → Paylaş → Bağlantıyı kopyala */
window.LUNA_HARITA = "";

/* ============================================================
   RENDER — bu kısma dokunmana gerek yok
   ============================================================ */
(function () {
  function hesaplar() {
    return (window.LUNA_SOSYAL || [])
      .filter(function (h) { return h.kullanici && h.kullanici.trim(); })
      .map(function (h) {
        return { ag: h.ag, ad: h.ad, url: h.adres.replace("%s", h.kullanici.trim()) };
      });
  }

  function baglantilar() {
    var l = hesaplar().map(function (h) { return h.url; });
    if (window.LUNA_HARITA) l.push(window.LUNA_HARITA);
    return l;
  }

  /* 1) alt bilgi + iletişim sayfası: [data-sosyal] kapsayıcısını doldur */
  function ciz() {
    var h = hesaplar();
    document.querySelectorAll("[data-sosyal]").forEach(function (kap) {
      if (!h.length && !window.LUNA_HARITA) {
        var bolum = kap.closest("[data-sosyal-bolum]");
        if (bolum) bolum.style.display = "none"; else kap.style.display = "none";
        return;
      }
      var html = h.map(function (x) {
        return '<a href="' + x.url + '" rel="me noopener" target="_blank">' + x.ad + "</a>";
      }).join("");
      if (window.LUNA_HARITA) {
        html += '<a href="' + window.LUNA_HARITA + '" rel="noopener" target="_blank">Yol tarifi</a>';
      }
      kap.innerHTML = html;
    });
  }

  /* 2) JSON-LD şemasına sameAs (ve varsa harita bağlantısı) ekle
        Şehir sayfalarında şema @graph içinde duruyor; sadece üst seviyeye
        bakmak o sayfaları atlıyordu — artık iç içe de geziliyor. */
  function firma_mi(n) {
    if (!n || !n["@type"]) return false;
    var t = String(n["@type"]);
    return t.indexOf("Organization") !== -1 ||
           t.indexOf("LocalBusiness") !== -1 ||
           t.indexOf("ProfessionalService") !== -1;
  }

  function dugumler(v, topla) {
    if (Array.isArray(v)) { v.forEach(function (x) { dugumler(x, topla); }); return topla; }
    if (v && typeof v === "object") {
      topla.push(v);
      if (v["@graph"]) dugumler(v["@graph"], topla);
    }
    return topla;
  }

  function semaya_ekle() {
    var url = baglantilar();
    var harita = window.LUNA_HARITA || "";
    if (!url.length && !harita) return;
    document.querySelectorAll('script[type="application/ld+json"]').forEach(function (s) {
      var v;
      try { v = JSON.parse(s.textContent); } catch (e) { return; }
      var degisti = false;
      dugumler(v, []).forEach(function (n) {
        if (!firma_mi(n)) return;
        if (url.length) { n.sameAs = url; degisti = true; }
        if (harita) { n.hasMap = harita; degisti = true; }
      });
      if (degisti) s.textContent = JSON.stringify(v);
    });
  }

  function kur() { ciz(); semaya_ekle(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", kur);
  else kur();
})();
