/* Cloudflare Pages Function — FORM KAPISI (Luna Pusula)
   Panelden üretilen formlar (lunayapim.com/form/<ad>) cevaplarını buraya gönderir;
   cevaplar KV'de birikir, Mac'teki panel anahtarla çekip siler. Mac kapalıyken de çalışır.

   Bağlamalar (Pages → Settings → Functions):
     KV namespace binding  : FORMLAR   (yoksa OKUMA namespace'i 'f:' ön ekiyle kullanılır — ek kurulum gerekmez)
     Environment variable  : PANEL_ANAHTARI  (okuma sayacıyla aynı gizli metin)

   POST /api/form   {slug, veri:{…}, jeton?, kaynak, zaman}   → cevabı saklar (herkese açık; iç formda jeton şart)
   GET  /api/form?anahtar=…&islem=liste                        → bekleyen cevaplar (yalnız panel)
   POST /api/form   {anahtar, islem:"sil", anahtarlar:[…]}     → indirilenleri siler (yalnız panel)
   POST /api/form   {anahtar, islem:"kayit", slug, ic, jeton, aktif} → form tanımını kaydeder (jeton/aktif kontrolü için)
   POST /api/form   {anahtar, islem:"durum"}                   → bekleyen sayısı + kayıtlı formlar

   Korumalar: bal küpü alanı, 24 KB sınırı, en fazla 40 alan, saatte IP başına 20 gönderim, pasif form reddi.
   Not: ziyaretçi IP'si tam saklanmıyor; yalnızca ilk iki bloğu (ör. 88.230.x.x) — teşhis için yeterli. */

const ONEK = "f:";
const kv = env => env.FORMLAR || env.OKUMA || null;
const K = (env, k) => (env.FORMLAR ? "" : ONEK) + k;

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};
function json(o, kod = 200) {
  return new Response(JSON.stringify(o), { status: kod,
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store", ...CORS } });
}
export async function onRequestOptions() { return new Response("", { status: 204, headers: CORS }); }

const SLUG = /^[a-z0-9][a-z0-9-]{0,39}$/;
const temiz = (v, n) => String(v == null ? "" : v).replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/g, "").slice(0, n);

export async function onRequestPost({ request, env }) {
  const KV = kv(env);
  if (!KV) return json({ hata: "KV bağlı değil (FORMLAR ya da OKUMA)." }, 500);
  const ham = await request.text();
  if (ham.length > 24 * 1024) return json({ hata: "Mesaj çok uzun." }, 413);
  let g; try { g = JSON.parse(ham || "{}"); } catch (e) { return json({ hata: "geçersiz" }, 400); }

  // ---- panel işlemleri (anahtarlı)
  if (g.anahtar !== undefined) {
    if (!env.PANEL_ANAHTARI || g.anahtar !== env.PANEL_ANAHTARI) return json({ hata: "yetki yok" }, 403);
    if (g.islem === "sil") {
      let n = 0;
      for (const a of (Array.isArray(g.anahtarlar) ? g.anahtarlar : []).slice(0, 200)) {
        const k = temiz(a, 80);
        if (k.startsWith("c:")) { await KV.delete(K(env, k)); n++; }
      }
      return json({ ok: true, silinen: n });
    }
    if (g.islem === "kayit") {
      const slug = temiz(g.slug, 40);
      if (!SLUG.test(slug)) return json({ hata: "slug geçersiz" }, 400);
      await KV.put(K(env, "d:" + slug), JSON.stringify({
        ad: temiz(g.ad, 80), ic: !!g.ic, jeton: g.ic ? temiz(g.jeton, 60) : "", aktif: g.aktif !== false,
        t: new Date().toISOString() }));
      return json({ ok: true });
    }
    if (g.islem === "durum") {
      const formlar = [], bekleyen = await say(KV, env, "c:");
      let imlec;
      do {
        const l = await KV.list({ prefix: K(env, "d:"), cursor: imlec });
        for (const k of l.keys) {
          const v = JSON.parse((await KV.get(k.name)) || "{}");
          formlar.push({ slug: k.name.slice(K(env, "d:").length), ad: v.ad, ic: !!v.ic, aktif: v.aktif !== false });
        }
        imlec = l.list_complete ? null : l.cursor;
      } while (imlec);
      return json({ ok: true, bekleyen, formlar });
    }
    return json({ hata: "bilinmeyen işlem" }, 400);
  }

  // ---- ziyaretçi gönderimi
  const slug = temiz(g.slug, 40);
  if (!SLUG.test(slug)) return json({ hata: "Form tanınmadı." }, 400);
  const veri = (g.veri && typeof g.veri === "object" && !Array.isArray(g.veri)) ? g.veri : null;
  if (!veri) return json({ hata: "Boş form." }, 400);
  if (typeof veri.site_web === "string" && veri.site_web) return json({ ok: true });   // bal küpü — sessizce yut
  const alanlar = Object.keys(veri).slice(0, 40);
  const temizVeri = {};
  let dolu = 0;
  for (const a of alanlar) {
    const ad = a.toLowerCase().replace(/[^a-z0-9_]/g, "").slice(0, 28);
    if (!ad) continue;
    const v = veri[a];
    temizVeri[ad] = Array.isArray(v) ? v.slice(0, 30).map(x => temiz(x, 200)) : temiz(v, 4000);
    if (String(temizVeri[ad]).trim()) dolu++;
  }
  if (!dolu) return json({ hata: "Boş form." }, 400);

  // form tanımı: pasifse reddet, iç formsa jeton iste
  const tanim = JSON.parse((await KV.get(K(env, "d:" + slug))) || "null");
  if (tanim && tanim.aktif === false) return json({ hata: "Bu form artık kapalı." }, 410);
  if (tanim && tanim.ic && temiz(g.jeton, 60) !== tanim.jeton) return json({ hata: "Bu form ekip içi." }, 403);

  // saatlik IP sınırı
  const ip = request.headers.get("CF-Connecting-IP") || "";
  const saat = new Date().toISOString().slice(0, 13);
  const sk = K(env, "r:" + saat + ":" + ip);
  const n = parseInt((await KV.get(sk)) || "0", 10) + 1;
  await KV.put(sk, String(n), { expirationTtl: 3600 });
  if (n > 20) return json({ hata: "Çok sık gönderim. Biraz sonra tekrar deneyin." }, 429);

  const t = new Date().toISOString();
  const kimlik = "c:" + t.replace(/[-:.TZ]/g, "").slice(0, 17) + "-" + Math.random().toString(36).slice(2, 8);
  await KV.put(K(env, kimlik), JSON.stringify({
    slug, veri: temizVeri, t,
    gonderildi: temiz(g.zaman, 40),
    kaynak: temiz(g.kaynak, 200),
    ip: ip.split(".").slice(0, 2).join(".") + (ip.includes(".") ? ".x.x" : ""),
    ua: temiz(request.headers.get("User-Agent"), 120),
  }), { expirationTtl: 60 * 60 * 24 * 90 });   // panel 90 gün içinde çekmezse düşer
  return json({ ok: true });
}

async function say(KV, env, onek) {
  let n = 0, imlec;
  do {
    const l = await KV.list({ prefix: K(env, onek), cursor: imlec });
    n += l.keys.length;
    imlec = l.list_complete ? null : l.cursor;
  } while (imlec);
  return n;
}

export async function onRequestGet({ request, env }) {
  const KV = kv(env);
  const u = new URL(request.url);
  if (!env.PANEL_ANAHTARI || u.searchParams.get("anahtar") !== env.PANEL_ANAHTARI) return json({ hata: "yetki yok" }, 403);
  if (!KV) return json({ hata: "KV bağlı değil." }, 500);
  const liste = [];
  let imlec;
  do {
    const l = await KV.list({ prefix: K(env, "c:"), cursor: imlec });
    for (const k of l.keys) {
      const v = JSON.parse((await KV.get(k.name)) || "null");
      if (v) liste.push({ anahtar: k.name.slice(K(env, "").length), ...v });
      if (liste.length >= 300) break;
    }
    imlec = (l.list_complete || liste.length >= 300) ? null : l.cursor;
  } while (imlec);
  liste.sort((a, b) => (a.t || "").localeCompare(b.t || ""));
  return json({ ok: true, sayi: liste.length, liste, kv: env.FORMLAR ? "FORMLAR" : "OKUMA" });
}
