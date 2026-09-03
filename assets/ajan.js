/* Luna Ajan — her sayfada dört iş yapan yardımcı: Sor (site bilgisi), Teklif (bant + WhatsApp),
   Plan (çalışma takvimi + .ics), Takip (TrendSaphiens konu aboneliği).
   Sunucu yok, anahtar yok; teklif ve plan tarayıcıda hesaplanır, takip /api/abone'ye gider.
   Rakam kaynağı: sitedeki fiyat tablosu (fiyatlar sayfası). Kesin teklif insan tarafından verilir. */
(function () {
  "use strict";
  if (window.__lunaAjan) return; window.__lunaAjan = 1;

  var WA = "905411602603", EPOSTA = "lunagency2603@gmail.com";
  // (anahtar, ad, bant alt, bant üst, birim, belirleyen, kapsamlar[3], plan adımları [(ad, iş günü)])
  var HIZMET = [
    ["3d", "İnşaat 3D modelleme", 45000, 250000, "proje", "Blok sayısı, daire tipi, ışık senaryosu",
     ["Tek blok, 3–4 dış cephe karesi", "Site/çok blok, 6–10 kare + iç mekân", "Kare seti + 60–90 sn animasyon"],
     [["Brifing, plan ve rölöve alımı", 1], ["Blok model ve kütle onayı", 3], ["Malzeme, çevre ve yerleşim", 3], ["Işık, kamera ve önizleme", 2], ["Final render ve iki revizyon", 3], ["Teslim: 4K kare, künye", 1]]],
    ["anim", "Proje tanıtım animasyonu", 90000, 180000, "film", "Süre, sahne sayısı, gerçek çekimle birleşim",
     ["45–60 sn, tek blok", "60–90 sn, site ölçeği", "90 sn+, gerçek çekimle birleşik"],
     [["Senaryo ve storyboard", 2], ["Model ve sahne kurulumu", 4], ["Animasyon ve kamera", 5], ["Işık, render", 4], ["Kurgu, ses, renk", 3], ["Teslim ve revizyon", 2]]],
    ["urun", "Ürün / makine animasyonu", 80000, 160000, "ürün", "Model karmaşıklığı, dil sayısı",
     ["Tek ürün, 30–45 sn", "Kesit ve çalışma prensibi, 45–60 sn", "Ürün serisi / çok dilli"],
     [["Teknik çizim ve brifing", 2], ["3D model ve kesit", 5], ["Animasyon", 4], ["Render ve kurgu", 3], ["Seslendirme, altyazı, teslim", 2]]],
    ["emlak", "Emlak video çekimi", 2500, 12000, "mülk", "Mülk büyüklüğü, drone, aylık paket",
     ["Daire, iç çekim", "Villa / müstakil, drone dahil", "Aylık portföy paketi"],
     [["Randevu ve mekân hazırlığı", 1], ["Çekim günü", 1], ["Kurgu ve renk", 2], ["Dikey ve yatay teslim", 1]]],
    ["kurumsal", "Kurumsal tanıtım filmi", 35000, 140000, "film", "Çekim günü, oyuncu, mekân sayısı",
     ["Tek mekân, 1 çekim günü", "Çok mekân, 2 çekim günü", "Senaryolu, oyunculu, 3+ gün"],
     [["Ön görüşme ve senaryo", 3], ["Çekim planı ve izinler", 2], ["Çekim günleri", 2], ["Kurgu, renk, ses", 5], ["Revizyon ve teslim", 2]]],
    ["sosyal", "Sosyal medya aylık üretim", 8000, 120000, "ay", "İçerik adedi, çekim günü, platform sayısı",
     ["Mikro işletme, ayda 1 çekim", "Küçük marka, ayda 2 çekim + tasarım", "Çok platform + video, haftalık çekim"],
     [["Marka dili ve takvim", 2], ["İlk çekim günü", 1], ["Aylık içerik üretimi", 10], ["Aylık rapor", 1]]],
    ["klip", "Klip çekimi", 45000, 180000, "klip", "Mekân sayısı, oyuncu, FPV, süre",
     ["Tek mekân, 1 gün", "2–3 mekân, FPV dahil", "Senaryolu, çok günlü"],
     [["Senaryo ve mekân keşfi", 3], ["Çekim", 2], ["Kurgu", 4], ["Renk ve VFX", 3], ["Teslim", 1]]],
    ["ai", "AI kısa film", 120000, 400000, "film", "Süre, sahne ve karakter sayısı, tutarlılık zorluğu",
     ["3–5 dk, tek karakter", "5–10 dk, 2–3 karakter", "10 dk+, çok karakter"],
     [["Senaryo ve karakter kartları", 4], ["Kare üretimi ve seçim", 6], ["Hareket ve tutarlılık", 6], ["Kurgu, ses, altyazı", 4], ["Etiket ve teslim", 1]]]
  ];
  var ILLER = ["İstanbul", "Ankara", "İzmir", "Bursa", "Antalya", "Kocaeli", "Konya", "Adana", "Gaziantep", "Mersin", "Kayseri", "Muğla", "Denizli", "Samsun", "Trabzon", "Sakarya", "Eskişehir", "Tekirdağ", "Balıkesir", "Manisa", "Aydın"];
  var KONU = [["piyasa", "Piyasalar — dolar, altın, enflasyon günü"], ["ekran", "Dizi & Film — vizyon, platform"], ["spor", "Spor Ekranı — maç hangi kanalda"], ["sanat", "Sanat — sergi, konser, sahne"], ["teknoloji", "Teknoloji — yapay zekâ, yazılım"], ["muhendislik", "Mühendislik — üretim, enerji"], ["sosyal-medya", "Sosyal Medya — platformlar, akımlar"], ["aranan", "Bugün Aranan — günün listesi"]];

  function kacir(x) { return String(x == null ? "" : x).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
  function tl(n) { return Math.round(n).toLocaleString("tr-TR") + " ₺"; }
  function el(id) { return document.getElementById(id); }
  function olc(ad, p) { try { if (window.gtag) gtag("event", ad, p || {}); } catch (e) {} }

  // sayfa bağlamı
  var yol = location.pathname;
  var BAGLAM = { hizmet: "", il: "", sekme: "sor" };
  if (/insaat-3d/.test(yol)) BAGLAM.hizmet = "3d";
  else if (/urun-animasyon/.test(yol)) BAGLAM.hizmet = "urun";
  else if (/emlak/.test(yol)) BAGLAM.hizmet = "emlak";
  else if (/isletme-tanitim|seo-icerik|yapay-zeka-seo/.test(yol)) BAGLAM.hizmet = "sosyal";
  else if (/klip/.test(yol)) BAGLAM.hizmet = "klip";
  else if (/ai-kisa-film/.test(yol)) BAGLAM.hizmet = "ai";
  else if (/dugun|drone/.test(yol)) BAGLAM.hizmet = "kurumsal";
  var mil = yol.match(/\/sehir\/([a-z0-9-]+)/);
  if (mil) { var h1 = document.querySelector("h1"); var m2 = h1 && h1.textContent.match(/([A-ZÇĞİÖŞÜ][a-zçğıöşü]+)/); BAGLAM.il = m2 ? m2[1] : mil[1]; if (!BAGLAM.hizmet) BAGLAM.hizmet = /3d/.test(yol) ? "3d" : /drone/.test(yol) ? "emlak" : /klip/.test(yol) ? "klip" : ""; }
  if (/\/trend\//.test(yol) || /\/gundem\//.test(yol) || /\/bulten\//.test(yol)) BAGLAM.sekme = "takip";
  else if (/\/hizmetler\/|\/sehir\/|fiyatlar/.test(yol)) BAGLAM.sekme = "teklif";

  function hizmetBul(k) { for (var i = 0; i < HIZMET.length; i++) if (HIZMET[i][0] === k) return HIZMET[i]; return HIZMET[0]; }

  // ---------------- TEKLİF ----------------
  function teklifHtml() {
    var sec = HIZMET.map(function (h) { return '<option value="' + h[0] + '"' + (h[0] === BAGLAM.hizmet ? " selected" : "") + '>' + kacir(h[1]) + '</option>'; }).join("");
    return '<form class="laj-form" id="laj-teklif" autocomplete="off">' +
      '<label>İş<select name="hizmet" id="laj-hizmet">' + sec + '</select></label>' +
      '<label>Kapsam<select name="kapsam" id="laj-kapsam"></select></label>' +
      '<label>İl<input name="il" list="laj-iller" placeholder="Bursa" value="' + kacir(BAGLAM.il) + '"><datalist id="laj-iller">' + ILLER.map(function (i) { return '<option value="' + i + '">'; }).join("") + '</datalist></label>' +
      '<label>Termin<select name="termin"><option>2 hafta içinde</option><option selected>1 ay içinde</option><option>Esnek</option></select></label>' +
      '<label>Not (isteğe bağlı)<textarea name="not" rows="2" maxlength="300" placeholder="Proje, mülk ya da ürün hakkında bir cümle"></textarea></label>' +
      '<button type="submit" class="laj-btn">Bandı hesapla</button>' +
      '</form><div id="laj-teklif-sonuc"></div>';
  }
  function kapsamDoldur() {
    var h = hizmetBul(el("laj-hizmet").value), s = el("laj-kapsam");
    s.innerHTML = h[6].map(function (k, i) { return '<option value="' + i + '">' + kacir(k) + '</option>'; }).join("");
  }
  function teklifHesapla(e) {
    e.preventDefault();
    var f = e.target, h = hizmetBul(f.hizmet.value), k = parseInt(f.kapsam.value, 10) || 0;
    var alt = h[2], ust = h[3], aralik = ust - alt;
    var b0 = alt + aralik * [0, 0.3, 0.6][k], b1 = alt + aralik * [0.35, 0.7, 1][k];
    var il = (f.il.value || "").trim(), yerinde = /emlak|kurumsal|klip|sosyal/.test(h[0]);
    var metin = "Merhaba, Luna Ajan'dan teklif bandı aldım.\n" +
      "İş: " + h[1] + "\nKapsam: " + h[6][k] + "\nİl: " + (il || "—") + "\nTermin: " + f.termin.value +
      (f.not.value ? "\nNot: " + f.not.value.trim() : "") +
      "\nTahmini bant: " + tl(b0) + " – " + tl(b1) + (h[4] === "ay" ? " / ay" : "") + " (+KDV)\nKesin teklif için bekliyorum.";
    var wa = "https://wa.me/" + WA + "?text=" + encodeURIComponent(metin);
    var mail = "mailto:" + EPOSTA + "?subject=" + encodeURIComponent("Teklif: " + h[1]) + "&body=" + encodeURIComponent(metin);
    el("laj-teklif-sonuc").innerHTML =
      '<div class="laj-sonuc"><span class="laj-etk">Tahmini bant · ' + kacir(h[1]) + '</span>' +
      '<b>' + tl(b0) + ' – ' + tl(b1) + (h[4] === "ay" ? ' <small>/ ay</small>' : '') + '</b><small>+ KDV · birim: ' + kacir(h[4]) + '</small>' +
      '<p>Bandı belirleyen: ' + kacir(h[5]) + '.' + (yerinde && il && il.toLowerCase() !== "bursa" ? ' Bursa dışı çekimde yol ve konaklama ayrı yazılır.' : '') +
      ' Bu rakam sitedeki fiyat tablosundan; kesin teklif bir iş günü içinde insan tarafından verilir.</p>' +
      '<div class="laj-bag"><a class="laj-btn" href="' + kacir(wa) + '" target="_blank" rel="noopener">WhatsApp\'a gönder</a>' +
      '<a href="' + kacir(mail) + '">E-posta</a><button type="button" data-kopya="' + kacir(metin) + '">Kopyala</button></div></div>';
    olc("ajan_teklif", { hizmet: h[0], kapsam: k });
    try { el("laj-teklif-sonuc").scrollIntoView({ block: "nearest", behavior: "smooth" }); } catch (x) {}
  }

  // ---------------- PLAN ----------------
  function planHtml() {
    var sec = HIZMET.map(function (h) { return '<option value="' + h[0] + '"' + (h[0] === BAGLAM.hizmet ? " selected" : "") + '>' + kacir(h[1]) + '</option>'; }).join("");
    var d = new Date(); d.setDate(d.getDate() + 3); var iso = d.toISOString().slice(0, 10);
    return '<form class="laj-form" id="laj-plan" autocomplete="off">' +
      '<label>İş<select name="hizmet">' + sec + '</select></label>' +
      '<label>Başlangıç<input type="date" name="bas" value="' + iso + '"></label>' +
      '<button type="submit" class="laj-btn">Takvimi kur</button></form><div id="laj-plan-sonuc"></div>';
  }
  function isGunuEkle(t, n) { var d = new Date(t); while (n > 0) { d.setDate(d.getDate() + 1); if (d.getDay() !== 0 && d.getDay() !== 6) n--; } return d; }
  function trTarih(d) { return d.toLocaleDateString("tr-TR", { day: "numeric", month: "long", weekday: "short" }); }
  function planKur(e) {
    e.preventDefault();
    var f = e.target, h = hizmetBul(f.hizmet.value), bas = new Date(f.bas.value || Date.now());
    if (bas.getDay() === 0 || bas.getDay() === 6) bas = isGunuEkle(bas, 1);
    var t = new Date(bas), satir = [], ics = [], toplam = 0;
    h[7].forEach(function (a, i) {
      var b0 = new Date(t), b1 = isGunuEkle(t, a[1] - 1);
      satir.push('<li><span>' + (i + 1) + '</span><b>' + kacir(a[0]) + '</b><small>' + trTarih(b0) + (a[1] > 1 ? ' → ' + trTarih(b1) : '') + ' · ' + a[1] + ' iş günü</small></li>');
      var s = b0.toISOString().slice(0, 10).replace(/-/g, ""), bit = isGunuEkle(b1, 1).toISOString().slice(0, 10).replace(/-/g, "");
      ics.push("BEGIN:VEVENT\r\nUID:luna-" + h[0] + "-" + i + "-" + s + "@lunayapim.com\r\nDTSTAMP:" + s + "T080000Z\r\nDTSTART;VALUE=DATE:" + s + "\r\nDTEND;VALUE=DATE:" + bit + "\r\nSUMMARY:" + (i + 1) + ". " + a[0] + " — " + h[1] + "\r\nDESCRIPTION:Luna Yapım çalışma planı. Kesin tarihler sözleşmeyle netleşir.\r\nEND:VEVENT");
      t = isGunuEkle(b1, 1); toplam += a[1];
    });
    var dosya = "data:text/calendar;charset=utf-8," + encodeURIComponent("BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Luna Yapim//Ajan//TR\r\n" + ics.join("\r\n") + "\r\nEND:VCALENDAR");
    el("laj-plan-sonuc").innerHTML = '<div class="laj-sonuc"><span class="laj-etk">Çalışma planı · ' + kacir(h[1]) + '</span><b>' + toplam + ' iş günü</b><small>' + trTarih(bas) + ' → ' + trTarih(isGunuEkle(bas, toplam - 1)) + '</small>' +
      '<ol class="laj-plan">' + satir.join("") + '</ol><p>Tipik akış; revizyon sayısı ve malzeme temini süreyi değiştirir. Sözleşmede kesinleşir.</p>' +
      '<div class="laj-bag"><a class="laj-btn" href="' + dosya + '" download="luna-plan-' + h[0] + '.ics">Takvime ekle (.ics)</a>' +
      '<a href="https://wa.me/' + WA + '?text=' + encodeURIComponent("Merhaba, " + h[1] + " için " + trTarih(bas) + " başlangıçlı " + toplam + " iş günlük planı Luna Ajan'dan aldım; uygunluk sorayım.") + '" target="_blank" rel="noopener">Uygunluk sor</a></div></div>';
    olc("ajan_plan", { hizmet: h[0] });
    try { el("laj-plan-sonuc").scrollIntoView({ block: "nearest", behavior: "smooth" }); } catch (x) {}
  }

  // ---------------- TAKİP ----------------
  function takipHtml() {
    var on = (document.querySelector('link[href*="luna.css"]') || {}).getAttribute ? document.querySelector('link[href*="luna.css"]').getAttribute("href").replace(/assets\/luna\.css.*$/, "") : "";
    var kat = (yol.match(/\/trend\/([a-z-]+)\//) || [])[1];
    return '<form class="laj-form" id="laj-takip" autocomplete="off">' +
      '<p class="laj-p">Seçtiğin konuların günlük sayfası çıktığında e-postana bir satır gelir; rakam yok, bağlantı var.</p>' +
      '<div class="laj-konular">' + KONU.map(function (k) { return '<label class="laj-onay"><input type="checkbox" name="konu" value="' + k[0] + '"' + (k[0] === kat || (!kat && (k[0] === "piyasa" || k[0] === "aranan")) ? " checked" : "") + '> ' + kacir(k[1]) + '</label>'; }).join("") + '</div>' +
      '<label>E-posta<input type="email" name="eposta" required placeholder="ad@ornek.com"></label>' +
      '<label class="laj-onay"><input type="checkbox" name="onay" required> Piyasa içeriğinin yatırım tavsiyesi olmadığını anladım; 18 yaşından büyüğüm.</label>' +
      '<button type="submit" class="laj-btn">Takibe al</button></form><div id="laj-takip-sonuc"></div>' +
      '<p class="laj-p"><a href="' + on + 'trend/">TrendSaphiens\'i aç →</a></p>';
  }
  function takipGonder(e) {
    e.preventDefault();
    var f = e.target, konular = [].slice.call(f.querySelectorAll('input[name=konu]:checked')).map(function (i) { return i.value; });
    var s = el("laj-takip-sonuc"); s.innerHTML = '<p class="laj-p">Kaydediliyor…</p>';
    fetch("/api/abone", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ eposta: f.eposta.value.trim(), onay: true, kaynak: "ajan:" + konular.join(","), konular: konular }) })
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (x) { s.innerHTML = '<div class="laj-sonuc"><b>' + (x.ok ? "Takipte." : "Olmadı") + '</b><p>' + kacir(x.j && (x.j.mesaj || x.j.hata) || (x.ok ? "İlk satır bir sonraki yayında gelir. İstediğin zaman çıkarsın." : "Bir şey ters gitti; sonra tekrar dene.")) + '</p></div>'; olc("ajan_takip", { konu: konular.length }); })
      .catch(function () { s.innerHTML = '<div class="laj-sonuc"><b>Ulaşılamadı</b><p>Kayıt servisi cevap vermedi; bültene TrendSaphiens sayfasından da abone olabilirsin.</p></div>'; });
  }

  // ---------------- kabuk ----------------
  function kur() {
    var kutu = el("las-kutu"), bas = kutu && kutu.querySelector(".las-bas");
    if (!kutu || !bas || el("laj-sekme")) return false;
    var dug = el("las-dug"); if (dug) { var sp = dug.querySelector("span"); if (sp) sp.textContent = "Luna Ajan"; dug.setAttribute("aria-label", "Luna Ajan: sor, teklif al, plan yap, takip et"); }
    var bb = bas.querySelector("b"); if (bb) bb.textContent = "Luna Ajan";
    var bs = bas.querySelector("span"); if (bs) bs.textContent = "Sorar · teklif çıkarır · plan yapar · takip eder";
    var sek = document.createElement("div"); sek.id = "laj-sekme"; sek.className = "laj-sekme"; sek.setAttribute("role", "tablist");
    sek.innerHTML = [["sor", "Sor"], ["teklif", "Teklif"], ["plan", "Plan"], ["takip", "Takip"]].map(function (s) { return '<button type="button" role="tab" data-sekme="' + s[0] + '" aria-selected="false">' + s[1] + '</button>'; }).join("");
    bas.parentNode.insertBefore(sek, bas.nextSibling);
    var pan = document.createElement("div"); pan.id = "laj-panel"; pan.className = "laj-panel"; pan.hidden = true;
    sek.parentNode.insertBefore(pan, sek.nextSibling);
    sek.addEventListener("click", function (e) { var b = e.target.closest("[data-sekme]"); if (b) sekmeAc(b.getAttribute("data-sekme")); });
    pan.addEventListener("submit", function (e) {
      if (e.target.id === "laj-teklif") teklifHesapla(e); else if (e.target.id === "laj-plan") planKur(e); else if (e.target.id === "laj-takip") takipGonder(e);
    });
    pan.addEventListener("change", function (e) { if (e.target.id === "laj-hizmet") kapsamDoldur(); });
    pan.addEventListener("click", function (e) {
      var k = e.target.closest("[data-kopya]"); if (!k) return;
      var t = k.getAttribute("data-kopya"), eski = k.textContent;
      (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(function () { k.textContent = "Kopyalandı"; setTimeout(function () { k.textContent = eski; }, 1600); }).catch(function () { window.prompt("Kopyala:", t); });
    });
    sekmeAc(BAGLAM.sekme);
    return true;
  }
  function sekmeAc(ad) {
    var pan = el("laj-panel"), sorAlan = [el("las-govde"), el("las-form"), document.querySelector("#las-kutu .las-not")];
    document.querySelectorAll("#laj-sekme [data-sekme]").forEach(function (b) { b.setAttribute("aria-selected", String(b.getAttribute("data-sekme") === ad)); });
    if (ad === "sor") { pan.hidden = true; sorAlan.forEach(function (x) { if (x) x.hidden = false; }); return; }
    sorAlan.forEach(function (x) { if (x) x.hidden = true; });
    pan.hidden = false;
    pan.innerHTML = ad === "teklif" ? teklifHtml() : ad === "plan" ? planHtml() : takipHtml();
    if (ad === "teklif") kapsamDoldur();
    olc("ajan_sekme", { sekme: ad });
  }
  function bekle(n) { if (kur()) return; if (n > 0) setTimeout(function () { bekle(n - 1); }, 150); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", function () { bekle(40); }); else bekle(40);
})();
