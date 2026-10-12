/* Cloudflare Pages Function — editör onayı (12.10.2026).
   KV: OKUMA (mevcut bağlama; anahtarlar "onay:<slug>" önekiyle)
   GET  /api/onay                         → {"onay": {slug: {t, e}}}  (herkese açık; yalnız onaylı adresler)
   POST /api/onay {slug, islem, anahtar}  → islem: "onayla" | "geri"  (PANEL_ANAHTARI ister)
   GitHub Actions turu GET ile listeyi indirir (pusula/onay_cek.py) ve onaylı yazıları
   editör imzasıyla yayına alır. */
const J = (o, s = 200) => new Response(JSON.stringify(o), {
  status: s, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" } });

export async function onRequestGet({ env }) {
  if (!env.OKUMA) return J({ hata: "KV yok" }, 500);
  const onay = {};
  let imlec;
  do {
    const l = await env.OKUMA.list({ prefix: "onay:", cursor: imlec });
    for (const k of l.keys) {
      try { onay[k.name.slice(5)] = JSON.parse((await env.OKUMA.get(k.name)) || "{}"); } catch (e) {}
    }
    imlec = l.list_complete ? null : l.cursor;
  } while (imlec);
  return J({ onay });
}

export async function onRequestPost({ request, env }) {
  if (!env.OKUMA) return J({ hata: "KV yok" }, 500);
  let g;
  try { g = await request.json(); } catch (e) { return J({ hata: "gövde" }, 400); }
  if (!env.PANEL_ANAHTARI || g.anahtar !== env.PANEL_ANAHTARI) return J({ hata: "yetki yok" }, 403);
  const slug = String(g.slug || "").toLowerCase().replace(/[^a-z0-9\-]/g, "").slice(0, 120);
  if (!slug) return J({ hata: "slug" }, 400);
  if (g.islem === "geri") { await env.OKUMA.delete("onay:" + slug); return J({ tamam: true, slug, durum: "geri" }); }
  const kayit = { t: new Date().toISOString().slice(0, 10), e: "pusat-ceylan" };
  await env.OKUMA.put("onay:" + slug, JSON.stringify(kayit));
  return J({ tamam: true, slug, durum: "onayli", kayit });
}
