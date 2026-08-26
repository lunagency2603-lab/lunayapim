/* ============================================================
   LUNA YAPIM — MÜŞTERİ SÖZLERİ DEFTERİ
   ------------------------------------------------------------
   Her müşteri sözü için bir satır ekle. Liste boşsa bölüm
   sitede HİÇ görünmez — uydurma yorum koymuyoruz.

   Alanlar:
     soz    → müşterinin kendi cümlesi (kısaltabilirsin, ekleme yapma)
     kim    → adı veya "Ad Soyad, Ünvan"
     firma  → firma adı (izin verdiyse)
     is     → hangi işi yaptık
     izin   → true ise adı ve firması görünür.
              false ise "Bursa'da bir inşaat firması" gibi anonim çıkar.

   Ekran görüntüsü veya yazılı onay olmadan buraya bir şey yazma;
   müşteriye gösterdiğimiz kanıt düzeyini kendimizde de tutuyoruz.
   ============================================================ */

window.LUNA_YORUMLAR = [
  // { soz:"", kim:"", firma:"", is:"", izin:true },
];

/* ============================================================
   RENDER — bu kısma dokunmana gerek yok
   ============================================================ */
(function () {
  function kacir(x) {
    return String(x == null ? "" : x).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  function kart(y) {
    var kim = y.izin
      ? kacir(y.kim || "") + (y.firma ? " · " + kacir(y.firma) : "")
      : kacir(y.kim || "İsim paylaşılmadı");
    return '<figure class="soz">' +
      "<blockquote>" + kacir(y.soz) + "</blockquote>" +
      '<figcaption>' + kim + (y.is ? ' <span class="soz-is">' + kacir(y.is) + "</span>" : "") +
      "</figcaption></figure>";
  }

  function kur() {
    var liste = (window.LUNA_YORUMLAR || []).filter(function (y) { return y && y.soz; });
    document.querySelectorAll("[data-yorumlar]").forEach(function (kap) {
      if (!liste.length) {
        var bolum = kap.closest("[data-yorum-bolum]") || kap.closest("section");
        if (bolum) bolum.style.display = "none"; else kap.style.display = "none";
        return;
      }
      var limit = parseInt(kap.getAttribute("data-limit") || "0", 10);
      var sec = limit > 0 ? liste.slice(0, limit) : liste;
      kap.innerHTML = sec.map(kart).join("");
    });

    /* Yalnızca gerçekten yazılmış sözler için Review şeması —
       puan/ortalama uydurmuyoruz, sadece metni işaretliyoruz. */
    if (liste.length) {
      var s = document.createElement("script");
      s.type = "application/ld+json";
      s.textContent = JSON.stringify(liste.map(function (y) {
        return {
          "@context": "https://schema.org", "@type": "Review",
          itemReviewed: { "@type": "Organization", name: "Luna Yapım", url: "https://lunayapim.com" },
          reviewBody: y.soz,
          author: { "@type": "Person", name: y.izin ? (y.kim || "Müşteri") : "Müşteri" }
        };
      }));
      document.head.appendChild(s);
    }
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", kur);
  else kur();
})();
