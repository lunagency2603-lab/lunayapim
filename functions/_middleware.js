/* TrendSaphiens alan adı katmanı — Cloudflare Pages Functions ara katmanı.

   Aynı Pages projesi iki alan adına hizmet eder:
     lunayapim.com       → Luna Yapım sitesi (olduğu gibi)
     trendsaphiens.com   → depodaki /trend/ klasörü, KÖKTEN yayınlanır
                           (trendsaphiens.com/x  ⇐  /trend/x)

   Üretici (pusula/trend.py) hiçbir şey bilmek zorunda değil: sayfalar /trend/
   altında üretilmeye devam eder; bu katman trendsaphiens.com isteklerinde
   dosyayı /trend/ altından okur, sayfadaki bağlantıları yeni adrese çevirir,
   canonical / og:url / JSON-LD adreslerini trendsaphiens.com yapar.

   GEÇİŞ ANAHTARI (Pages → Settings → Variables and Secrets):
     TRENDSAPHIENS_CANLI = 1
   Açılınca lunayapim.com/trend/* → trendsaphiens.com/* 301 olur, lunayapim.com
   site haritasından /trend/ adresleri çıkar ve lunayapim sayfalarındaki
   /trend/ bağlantıları doğrudan trendsaphiens.com'a gider.
   Anahtar KAPALIYKEN lunayapim.com'da hiçbir şey değişmez (alan adı Cloudflare'a
   bağlanana kadar güvenli).

   Test: TS_TEST_HOST = <önizleme alanı> verilirse o alan trendsaphiens gibi davranır.
*/

const TS = "trendsaphiens.com";
const TSU = "https://" + TS;
const LY = "https://lunayapim.com";
const LY_HOSTS = new Set(["lunayapim.com", "www.lunayapim.com"]);
const TS_HOSTS = new Set([TS, "www." + TS]);
// trendsaphiens.com'da olduğu gibi (kökten) sunulan dosyalar
const KOK_DOSYA = new Set([
  "/ads.txt",
  "/favicon.ico",
  "/006754dbaedd40b08f3cb1b75e5368f1.txt", // IndexNow anahtarı
]);
const URL_ATTR = ["href", "src", "action", "poster", "data-src", "data-url"];

const canli = (env) => String(env.TRENDSAPHIENS_CANLI || "") === "1";

function tsHost(host, env) {
  if (TS_HOSTS.has(host)) return true;
  return !!env.TS_TEST_HOST && host === String(env.TS_TEST_HOST).toLowerCase();
}

// /trend/x.html → /x   ·  /trend/ekran/index.html → /ekran/   ·  /trend → /
function tsYol(p) {
  let r = p.replace(/^\/trend(?=\/|$)/, "") || "/";
  r = r.replace(/\/index(\.html)?$/, "/").replace(/\.html$/, "");
  return r || "/";
}

const trendMi = (p) => p === "/trend" || p.startsWith("/trend/");
const gecisMi = (p) => p.startsWith("/assets/") || p.startsWith("/api/") || KOK_DOSYA.has(p);

/* Bir bağlantıyı trendsaphiens.com sayfası için çevirir.
   taban: bağlantının ÖZGÜN (lunayapim.com/trend/...) sayfa adresi. */
function tsBaglanti(deger, taban, mutlak) {
  const v = deger.trim();
  if (!v || v.startsWith("#") || /^(mailto:|tel:|javascript:|data:|blob:)/i.test(v)) return null;
  let u;
  try { u = new URL(v, taban); } catch (e) { return null; }
  const host = u.hostname.toLowerCase();
  const yerel = LY_HOSTS.has(host) || TS_HOSTS.has(host) || host === new URL(taban).hostname;
  if (!yerel) return null;
  const ek = u.search + u.hash;
  if (trendMi(u.pathname)) return (mutlak ? TSU : "") + tsYol(u.pathname) + ek;
  if (gecisMi(u.pathname)) return (mutlak ? TSU : "") + u.pathname + ek;
  return LY + u.pathname + ek;
}

// Metin içindeki eski adresleri yenisine çevirir (paylaşım bağlantıları, JSON-LD…)
function metinCevir(s) {
  return s
    .replace(/https?:\/\/(www\.)?lunayapim\.com\/trend\/?/g, TSU + "/")
    .replace(/https?%3A%2F%2F(www\.)?lunayapim\.com%2Ftrend(%2F)?/gi, "https%3A%2F%2F" + TS + "%2F")
    .replace(/https?:\\\/\\\/(www\.)?lunayapim\.com\\\/trend(\\\/)?/g, "https:\\/\\/" + TS + "\\/");
}

function htmlMi(res) {
  return (res.headers.get("content-type") || "").includes("text/html");
}

class TsAttr {
  constructor(taban) { this.taban = taban; }
  element(el) {
    const tag = el.tagName;
    const degisen = [];
    for (const [ad, deger] of [...el.attributes]) {
      let yeni = null;
      if (URL_ATTR.includes(ad) || (tag === "meta" && ad === "content" && /^(https?:)?\/\//.test(deger))) {
        const mutlak = tag === "meta" || (tag === "link" && /canonical|alternate/.test(el.getAttribute("rel") || "")) ||
          /^https?:/i.test(deger.trim());
        yeni = tsBaglanti(deger, this.taban, mutlak);
      }
      if (yeni === null) {
        const m = metinCevir(deger);
        if (m !== deger) yeni = m;
      }
      if (yeni !== null && yeni !== deger) degisen.push([ad, yeni]);
    }
    for (const [ad, yeni] of degisen) el.setAttribute(ad, yeni);
  }
}

class MetinTampon {
  constructor(cevir) { this.cevir = cevir; this.buf = ""; }
  text(t) {
    this.buf += t.text;
    if (t.lastInTextNode) { t.replace(this.cevir(this.buf), { html: true }); this.buf = ""; }
    else t.remove();
  }
}

function tsYaz(res, taban) {
  return new HTMLRewriter()
    .on("*", new TsAttr(taban))
    .on("script", new MetinTampon(metinCevir))
    .transform(res);
}

async function tsSiteHaritasi(env, url) {
  const r = await env.ASSETS.fetch(new URL("/sitemap.xml", url));
  const xml = r.ok ? await r.text() : "";
  const bloklar = xml.match(/<url>[\s\S]*?<\/url>/g) || [];
  const secili = bloklar
    .filter((b) => /<loc>https:\/\/lunayapim\.com\/trend\//.test(b))
    .map((b) => b.replace(/<loc>https:\/\/lunayapim\.com\/trend\/([^<]*)<\/loc>/, (_, y) => `<loc>${TSU}${tsYol("/trend/" + y)}</loc>`));
  const govde = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  ${secili.join("\n  ")}\n</urlset>\n`;
  return new Response(govde, { headers: { "content-type": "application/xml; charset=utf-8", "cache-control": "public, max-age=3600" } });
}

function tsRobots() {
  const g = `User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: ${TSU}/sitemap.xml\n`;
  return new Response(g, { headers: { "content-type": "text/plain; charset=utf-8" } });
}

/* 23.09.2026 — alan adının WordPress döneminden kalan adresler.
   Search Console: 21 "soft 404" (/tag/*, /home-two/, /category/<eşlenmemiş>) ve
   51 "404" (/2022/07/..., /wp-content/...). Bunları ana sayfaya yönlendirmek
   Google'a "sahte sayfa" sinyali veriyordu. Artık 410 Gone dönüyor: "kalıcı
   olarak kaldırıldı" — Google bu adresleri 404'ten daha hızlı listeden düşürür.
   Eşlemesi olan eski kategoriler (/category/music/ → /muzik/) 301 olarak kalır. */
const ESKI_WP = /^\/(?:tag|category|author|page|product|shop|portfolio)\/|^\/(?:home-two|home-three|blog-2|blog|shop|cart|checkout|my-account|sample-page)\/?$|^\/(?:wp-|xmlrpc\.php|feed\/?$|comments\/)|^\/\d{4}\/\d{2}\//;
const eskiWpMi = (p) => ESKI_WP.test(p);
const anaSayfaMi = (konum) => {
  try { return ["/", "/trend", "/trend/"].includes(new URL(konum, TSU).pathname); } catch (e) { return false; }
};

async function hataSayfasi(env, url, kod) {
  // 22.09.2026 — önce TrendSaphiens'in kendi 404'ü; yoksa Luna Yapım'ınki.
  let s = await env.ASSETS.fetch(new URL("/trend/404.html", url));
  let taban404 = LY + "/trend/404";
  if (!s.ok) {
    s = await env.ASSETS.fetch(new URL("/404.html", url));
    taban404 = LY + "/404";
  }
  const r = new Response(s.body, { status: kod, headers: s.headers });
  return htmlMi(r) ? tsYaz(r, taban404) : r;
}

function yonlendir(konum, kod = 301) {
  return new Response(null, { status: kod, headers: { location: konum } });
}

async function trendsaphiens(ctx, url, host) {
  const { request, env, next } = ctx;
  const p = url.pathname;

  if (host === "www." + TS) return yonlendir(TSU + p + url.search);
  if (trendMi(p)) return yonlendir(TSU + tsYol(p) + url.search);
  if (gecisMi(p)) return next();
  if (p === "/robots.txt") return tsRobots();
  if (p === "/sitemap.xml") return tsSiteHaritasi(env, url);
  if (request.method !== "GET" && request.method !== "HEAD") return new Response("", { status: 405 });

  const hedef = new URL(url);
  hedef.pathname = "/trend" + p;
  const taban = LY + hedef.pathname;
  let res = await env.ASSETS.fetch(new Request(hedef.toString(), request));

  if (res.status >= 300 && res.status < 400) {
    const konum = res.headers.get("location");
    if (!konum) return res;
    const yeni = tsBaglanti(konum, hedef.toString(), false);
    // eski WP adresi ana sayfaya düşüyorsa yönlendirme değil 410 (soft 404 olmasın)
    if (eskiWpMi(p) && anaSayfaMi(yeni || konum)) return hataSayfasi(env, url, 410);
    return yonlendir(yeni || konum, res.status);
  }
  if (res.status === 404) {
    // Eskiden yalnız /404.html vardı ve trendsaphiens.com'da bulunamayan adres
    // "LUNA YAPIM" yazan bir sayfa gösteriyordu.
    return hataSayfasi(env, url, eskiWpMi(p) ? 410 : 404);
  }
  if (!htmlMi(res)) return res;
  res = new Response(res.body, res);
  res.headers.set("x-trendsaphiens", "1");
  return tsYaz(res, taban);
}

class LyAttr {
  element(el) {
    const h = el.getAttribute("href");
    if (!h) return;
    let u;
    try { u = new URL(h, this.taban); } catch (e) { return; }
    if (LY_HOSTS.has(u.hostname) && trendMi(u.pathname)) el.setAttribute("href", TSU + tsYol(u.pathname) + u.search + u.hash);
  }
}

/* 22.09.2026 — Cloudflare Pages her dalı ve her çekme isteğini ayrı bir
   <özet>.lunayapim.pages.dev adresinde yayınlıyor; üretim kopyası da
   lunayapim.pages.dev'de duruyor. Bunların hiçbirinde noindex yoktu:
   lunayapim.com'un ve trendsaphiens.com'un TAM kopyası ikinci bir alan adında
   taranabilir haldeydi. Arama motoru için bu ikiz içerik; hangi adresin asıl
   olduğunu kendisi seçiyor. Canonical etiketi lunayapim.com'u gösterse de
   öneridir, kural değildir — başlık daha kesin konuşur. */
function onizlemeMi(host) {
  return host === "lunayapim.pages.dev" || host.endsWith(".lunayapim.pages.dev");
}

function dizinDisi(res) {
  const r = new Response(res.body, res);
  r.headers.set("x-robots-tag", "noindex, nofollow");
  return r;
}

export async function onRequest(ctx) {
  const { request, env, next } = ctx;
  const url = new URL(request.url);
  const host = url.hostname.toLowerCase();

  // önizleme/pages.dev kopyaları: taranabilir ama dizine girmez
  if (onizlemeMi(host)) return dizinDisi(await asilAkis(ctx, url, host));
  return asilAkis(ctx, url, host);
}

async function asilAkis(ctx, url, host) {
  const { request, env, next } = ctx;

  if (tsHost(host, env)) return trendsaphiens(ctx, url, host);

  // www → köke 301: iki adreste aynı sayfa durmasın (trendsaphiens'te zaten var)
  if (host === "www.lunayapim.com") return yonlendir(LY + url.pathname + url.search);

  if (canli(env) && LY_HOSTS.has(host)) {
    const p = url.pathname;
    if (trendMi(p)) return yonlendir(TSU + tsYol(p) + url.search);
    if (p === "/sitemap.xml") {
      const r = await next();
      if (!r.ok) return r;
      const xml = (await r.text()).replace(/\s*<url>\s*<loc>https:\/\/lunayapim\.com\/trend\/[\s\S]*?<\/url>/g, "");
      return new Response(xml, { status: 200, headers: r.headers });
    }
    const r = await next();
    if (!htmlMi(r)) return r;
    const d = new LyAttr();
    d.taban = url.toString();
    return new HTMLRewriter().on("a[href]", d).transform(r);
  }
  return next();
}
