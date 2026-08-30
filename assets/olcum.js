/* ============================================================
   LUNA YAPIM — ÖLÇÜM DEFTERİ
   ------------------------------------------------------------
   Sitede şu an SADECE Google Ads dönüşüm etiketi (AW-) var.
   Yani reklam dönüşümü ölçülüyor ama "kaç kişi geldi, hangi
   sayfada durdu, nereden geldi" ölçülmüyor.

   Aşağıya kimliği yapıştırdığın an ölçüm başlar. Boş bırakılan
   satır hiç yüklenmez — gereksiz istek gitmez, sayfa yavaşlamaz.

   GA4       → analytics.google.com → Yönetici → Veri akışları →
               "Ölçüm Kimliği" (G- ile başlar)
   Cloudflare→ Cloudflare → Web Analytics → siteyi ekle →
               verilen koddaki "token" değeri (çerezsiz, ücretsiz)
   ============================================================ */

window.LUNA_OLCUM = {
  ga4: "G-CQYDCWF2DG",         // örn: "G-XXXXXXXXXX"
  cloudflare: "",  // örn: "a1b2c3d4e5f6..."
};

(function () {
  var o = window.LUNA_OLCUM || {};

  if (o.ga4) {
    window.dataLayer = window.dataLayer || [];
    function gtag() { window.dataLayer.push(arguments); }
    window.gtag = window.gtag || gtag;

    /* Sayfada Google Ads etiketi varsa gtag zaten yüklenmiş oluyor.
       İkinci kez yüklemek gereksiz istek ve yavaşlama demek — bu yüzden
       önce bakıyoruz, yoksa yüklüyoruz. */
    var yuklu = !!document.querySelector(
      'script[src*="googletagmanager.com/gtag/js"]');
    if (!yuklu) {
      var s = document.createElement("script");
      s.async = true;
      s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(o.ga4);
      document.head.appendChild(s);
      gtag("js", new Date());
    }
    gtag("config", o.ga4);
  }

  if (o.cloudflare) {
    var c = document.createElement("script");
    c.defer = true;
    c.src = "https://static.cloudflareinsights.com/beacon.min.js";
    c.setAttribute("data-cf-beacon", JSON.stringify({ token: o.cloudflare }));
    document.head.appendChild(c);
  }

  /* Sayfadaki asıl dönüşümleri say: WhatsApp, telefon, form gönderimi.
     Ölçüm aracı bağlıysa oraya, değilse hiçbir yere — sessizce geçer. */
  function olay(ad, ek) {
    if (typeof window.gtag === "function") window.gtag("event", ad, ek || {});
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a,button");
    if (!a) return;
    var h = (a.getAttribute("href") || "").toLowerCase();
    var tf = a.getAttribute("data-tf");
    if (h.indexOf("wa.me") !== -1) olay("whatsapp_tikla", { sayfa: location.pathname });
    else if (h.indexOf("tel:") === 0) olay("telefon_tikla", { sayfa: location.pathname });
    else if (h.indexOf("mailto:") === 0) olay("eposta_tikla", { sayfa: location.pathname });
    else if (tf) olay("form_gonder", { kanal: tf, sayfa: location.pathname });
  }, true);
})();
