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
  /* 06.10.2026: TrendSaphiens kendi GA4 mülküne yazar (G-6Y0N298BY3). Önceden iki site
     aynı mülke (lunayapim.com) yazıyordu; Luna'nın ziyaretçi ve talep sayıları karışıyordu. */
  ga4: /(^|\.)trendsaphiens\.com$/.test(location.hostname) ? "G-6Y0N298BY3" : "G-CQYDCWF2DG",
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
    /* 30.09.2026 — KENDİ TRAFİĞİMİZ. Ev bağlantısının IPv6 adresi her gün değişiyor
       (28.09: …:72ac, 30.09: …:8a45), IP kuralı bu yüzden hiçbir şeyi yakalamıyordu.
       Artık cihaz işaretleniyor: bir kez lunayapim.com/?ic=1 açılınca o tarayıcıdaki
       bütün ziyaretler "internal" sayılır ve GA4'teki "Ofis ve ev" filtresi onları raporlardan
       çıkarır. Kaldırmak için ?ic=0. Tarayıcı depolaması kapalıysa sessizce geçer. */
    var ic = false;
    try {
      var q = location.search;
      if (/[?&]ic=1\b/.test(q)) localStorage.setItem("luna_ic", "1");
      if (/[?&]ic=0\b/.test(q)) localStorage.removeItem("luna_ic");
      ic = localStorage.getItem("luna_ic") === "1";
    } catch (e) { ic = false; }
    if (ic) gtag("config", o.ga4, { traffic_type: "internal" });
    else gtag("config", o.ga4);
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
    if (h.indexOf("wa.me") !== -1) {
      /* 30.09.2026 — WhatsApp mesajı hangi sayfadan geldiğini söylesin: talebin hangi
         il/hizmet sayfasından geldiği sohbetin ilk satırında görünür. Sayfa zaten hazır
         bir metin veriyorsa ona dokunulmaz. */
      try {
        var raw = a.getAttribute("href") || "";
        if (raw.indexOf("text=") === -1) {
          var bas = document.querySelector("h1");
          var ad = ((bas && bas.innerText) || document.title || "").replace(/\s+/g, " ").trim().slice(0, 90);
          var metin = "Merhaba, lunayapim.com'da \u201c" + ad + "\u201d sayfasından yazıyorum.";
          a.setAttribute("href", raw + (raw.indexOf("?") === -1 ? "?" : "&") + "text=" + encodeURIComponent(metin));
        }
      } catch (x) {}
      olay("whatsapp_tikla", { sayfa: location.pathname });
    }
    else if (h.indexOf("tel:") === 0) olay("telefon_tikla", { sayfa: location.pathname });
    else if (h.indexOf("mailto:") === 0) olay("eposta_tikla", { sayfa: location.pathname });
    else if (tf) olay("form_gonder", { kanal: tf, sayfa: location.pathname });
  }, true);
})();
