/* ============================================================
   LUNA YAPIM — TEKLİF FORMU
   ------------------------------------------------------------
   Sunucu gerektirmez. Doldurulan alanlar tek bir düzgün mesaja
   çevrilir; ziyaretçi WhatsApp'tan ya da e-postadan gönderir.
   Böylece mesai dışında gelen kişi de iz bırakabiliyor ve
   bize eksiksiz bir brief geliyor — "merhaba" mesajı değil.

   Kullanımı: sayfaya <div data-teklif-form></div> koy, bu dosyayı yükle.
   ============================================================ */

window.LUNA_FORM = {
  wa: "905411602603",
  eposta: "lunagency2603@gmail.com",
  isler: ["İnşaat / mimari 3D modelleme", "Ürün veya hizmet animasyonu",
          "Emlak tanıtım videosu", "Kurumsal tanıtım filmi", "Klip çekimi",
          "Drone / FPV çekim", "Düğün ve etkinlik", "Sosyal medya içerik üretimi",
          "Yazılım / otomasyon", "Henüz emin değilim"],
  butceler: ["Henüz belirlemedim", "25.000 ₺ altı", "25.000 – 75.000 ₺",
             "75.000 – 150.000 ₺", "150.000 ₺ üzeri", "Aylık düzenli çalışma"],
  ne_zaman: ["Bu ay", "1–3 ay içinde", "3 aydan sonra", "Sadece fiyat öğreniyorum"]
};

(function () {
  var A = window.LUNA_FORM;

  function sec(id, etiket, secenekler) {
    return '<label for="' + id + '">' + etiket + "</label><select id=\"" + id + '">' +
      secenekler.map(function (s) { return "<option>" + s + "</option>"; }).join("") + "</select>";
  }

  function iskelet() {
    return '<div class="tform">' +
      '<div class="tform-satir">' +
      '<div class="tform-alan"><label for="tf-ad">Adınız / firma</label>' +
      '<input id="tf-ad" type="text" autocomplete="organization" placeholder="Ova Yapı — Mehmet Bey"></div>' +
      '<div class="tform-alan"><label for="tf-sehir">Şehir</label>' +
      '<input id="tf-sehir" type="text" autocomplete="address-level2" placeholder="Bursa"></div>' +
      "</div>" +
      '<div class="tform-satir">' +
      '<div class="tform-alan">' + sec("tf-is", "İş ne?", A.isler) + "</div>" +
      '<div class="tform-alan">' + sec("tf-zaman", "Ne zaman?", A.ne_zaman) + "</div>" +
      "</div>" +
      '<div class="tform-alan">' + sec("tf-butce", "Bütçe aralığı (isteğe bağlı)", A.butceler) + "</div>" +
      '<div class="tform-alan"><label for="tf-not">Kısaca anlat</label>' +
      '<textarea id="tf-not" rows="4" placeholder="Nilüfer\'de 3 bloklu konut projesi. Satış ofisi için tanıtım videosu ve daire içi tur istiyoruz."></textarea></div>' +
      '<div class="tform-dug">' +
      '<button type="button" class="btn btn-dolu" data-tf="wa">WhatsApp\'tan gönder</button>' +
      '<button type="button" class="btn" data-tf="mail">E-posta ile gönder</button>' +
      '<button type="button" class="btn" data-tf="kopya">Metni kopyala</button>' +
      "</div>" +
      '<p class="tform-not">Gönder\'e bastığında bilgiler tek mesaj hâline gelir; ' +
      "kendi uygulamandan gönderirsin. Formu biz saklamıyoruz.</p>" +
      '<p class="tform-uyari" hidden>Lütfen adınızı ve kısa açıklamayı doldurun.</p></div>';
  }

  function deger(id) {
    var e = document.getElementById(id);
    return e ? String(e.value || "").trim() : "";
  }

  function mesaj() {
    var s = [];
    s.push("Merhaba Luna Yapım,");
    s.push("");
    s.push("Firma / kişi : " + (deger("tf-ad") || "—"));
    s.push("Şehir        : " + (deger("tf-sehir") || "—"));
    s.push("İş           : " + deger("tf-is"));
    s.push("Zamanlama    : " + deger("tf-zaman"));
    s.push("Bütçe        : " + deger("tf-butce"));
    s.push("");
    s.push(deger("tf-not"));
    s.push("");
    s.push("(lunayapim.com teklif formundan gönderildi)");
    return s.join("\n");
  }

  function gecerli() {
    var ok = deger("tf-ad") && deger("tf-not");
    var u = document.querySelector(".tform-uyari");
    if (u) u.hidden = !!ok;
    return !!ok;
  }

  function bagla(kap) {
    kap.addEventListener("click", function (e) {
      var d = e.target.getAttribute && e.target.getAttribute("data-tf");
      if (!d) return;
      if (!gecerli()) return;
      var m = mesaj();
      if (d === "wa") {
        window.open("https://wa.me/" + A.wa + "?text=" + encodeURIComponent(m), "_blank");
      } else if (d === "mail") {
        window.location.href = "mailto:" + A.eposta +
          "?subject=" + encodeURIComponent("Teklif talebi — " + (deger("tf-ad") || "web sitesi")) +
          "&body=" + encodeURIComponent(m);
      } else if (d === "kopya") {
        var yaz = function () { e.target.textContent = "Kopyalandı";
          setTimeout(function () { e.target.textContent = "Metni kopyala"; }, 1800); };
        if (navigator.clipboard) navigator.clipboard.writeText(m).then(yaz, yaz);
        else yaz();
      }
    });
  }

  function kur() {
    document.querySelectorAll("[data-teklif-form]").forEach(function (kap) {
      if (kap.dataset.kuruldu) return;
      kap.dataset.kuruldu = "1";
      // Form HTML'i sayfada STATİK duruyorsa ona dokunma — arama motoru ve
      // paylaşım botları JavaScript çalıştırmadan da formu görebilsin diye.
      // Yalnızca boşsa çiziyoruz (başka sayfalarda kolay kullanım için).
      if (!kap.querySelector(".tform")) kap.innerHTML = iskelet();
      bagla(kap);
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", kur);
  else kur();
})();
