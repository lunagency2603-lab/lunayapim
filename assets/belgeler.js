/* ============================================================
   LUNA YAPIM — YETKİ VE BELGE DEFTERİ
   ------------------------------------------------------------
   Drone çekimi Türkiye'de belgeye bağlı bir iş. Belgesi olmayan
   firmayla çalışan müşteri de risk alıyor — bu yüzden belgeyi
   göstermek en güçlü satış argümanlarından biri.

   TEK YAPMAN GEREKEN: aşağıdaki "no" alanlarını doldurmak.
   Boş bırakılan belge sayfada NUMARASIZ görünür: iddia yazılır,
   numara yazılmaz. Yani yanlış numara yayınlama riski yok.

   Numarayı yazdığın an üç yerde birden görünür:
     1) hizmetler/drone-fpv sayfasındaki "Yetki ve belgeler" bloğu
     2) tüm drone şehir sayfalarındaki aynı blok
     3) JSON-LD şemasındaki hasCredential alanı
        (Google'a "bu firma bu yetkiye sahip" diyen alan)

   Nereden bakılır:
     · İHA kayıt no  → iha.shgm.gov.tr → İHA Kayıt Sistemi → araç kaydı
     · Pilot lisansı → aynı sistemde pilot profili (İHA-1 / İHA-2)
     · Sigorta       → poliçe üstündeki poliçe numarası
   ============================================================ */

window.LUNA_BELGELER = {
  /* Uçuşları yapan aracın SHGM kaydı */
  iha: {
    ad: "SHGM İHA kaydı",
    aciklama: "Kullandığımız insansız hava aracı Sivil Havacılık Genel Müdürlüğü " +
              "İHA Kayıt Sistemi'ne kayıtlı.",
    no: "",                      // örn. "TR-IHA-XXXXXX"
    kurum: "Sivil Havacılık Genel Müdürlüğü"
  },
  /* Uçuşu yapan pilotun lisansı */
  pilot: {
    ad: "İHA pilot lisansı",
    aciklama: "Uçuşları SHGM'den lisanslı İHA pilotu yapıyor; taşeron pilot " +
              "kullanmıyoruz.",
    no: "",                      // örn. "IHA2-XXXXXX"
    sinif: "",                   // "İHA-1" ya da "İHA-2" — hangisiyse onu yaz
    kurum: "Sivil Havacılık Genel Müdürlüğü"
  },
  /* İsteğe bağlı — üçüncü şahıs mali sorumluluk sigortası */
  sigorta: {
    ad: "Üçüncü şahıs mali sorumluluk sigortası",
    aciklama: "Çekim sırasında oluşabilecek üçüncü şahıs zararları poliçe " +
              "kapsamında.",
    no: "",                      // poliçe numarası
    kurum: ""                    // sigorta şirketi adı
  }
};

/* ------------------------------------------------------------------ */
(function () {
  "use strict";
  var B = window.LUNA_BELGELER || {};
  var sira = ["iha", "pilot", "sigorta"];

  function kacir(x) {
    return String(x == null ? "" : x).replace(/&/g, "&amp;")
      .replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function kart(b) {
    if (!b || !b.ad) return "";
    var no = (b.no || "").trim();
    var sinif = (b.sinif || "").trim();
    var kurum = (b.kurum || "").trim();
    var alt = [];
    if (sinif) alt.push("Sınıf: " + kacir(sinif));
    if (no) alt.push("No: " + kacir(no));
    if (kurum) alt.push(kacir(kurum));
    return '<div class="blg">' +
           '<b>' + kacir(b.ad) + '</b>' +
           '<p>' + kacir(b.aciklama || "") + '</p>' +
           (alt.length ? '<span class="blg-no">' + alt.join(" · ") + '</span>'
                       : '<span class="blg-no blg-bos">Belge numarası talep üzerine ' +
                         'paylaşılıyor</span>') +
           '</div>';
  }

  function ciz() {
    var yer = document.getElementById("luna-belgeler");
    if (!yer) return;
    var ic = sira.map(function (k) {
      var b = B[k];
      // sigorta boşsa ve numarası da yoksa hiç gösterme (opsiyonel belge)
      if (k === "sigorta" && !(b && (b.no || "").trim())) return "";
      return kart(b);
    }).join("");
    if (!ic) { yer.remove(); return; }
    yer.innerHTML = ic;

    // JSON-LD: yalnızca numarası girilmiş belgeler şemaya girer
    var kimlik = sira.map(function (k) {
      var b = B[k];
      if (!b || !(b.no || "").trim()) return null;
      return {
        "@type": "EducationalOccupationalCredential",
        "name": b.ad + (b.sinif ? " (" + b.sinif + ")" : ""),
        "identifier": b.no,
        "recognizedBy": b.kurum ? { "@type": "Organization", "name": b.kurum } : undefined
      };
    }).filter(Boolean);
    if (!kimlik.length) return;
    var e = document.createElement("script");
    e.type = "application/ld+json";
    e.textContent = JSON.stringify({
      "@context": "https://schema.org", "@type": "Organization",
      "name": "Luna Yapım", "url": "https://lunayapim.com/",
      "hasCredential": kimlik
    });
    document.head.appendChild(e);
  }

  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", ciz);
  else ciz();
})();
