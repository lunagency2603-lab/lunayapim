/* Anket oyları (12.10.2026) — çerezsiz; tekrar oyu localStorage önler.
   GET  /api/anket?id=x&n=4   → {"oy": [12, 3, 8, 1]}
   POST /api/anket {id, secim} → artırır, güncel oyları döner */
const J = (o, s = 200) => new Response(JSON.stringify(o), {
  status: s, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" } });
const idTemiz = (x) => String(x || "").toLowerCase().replace(/[^a-z0-9\-]/g, "").slice(0, 80);

async function oylar(kv, id, n) {
  const o = [];
  for (let i = 0; i < n; i++) o.push(parseInt((await kv.get(`a:${id}:${i}`)) || "0", 10));
  return o;
}

export async function onRequestGet({ request, env }) {
  const u = new URL(request.url), id = idTemiz(u.searchParams.get("id"));
  const n = Math.min(12, Math.max(2, parseInt(u.searchParams.get("n") || "4", 10)));
  if (!env.OKUMA || !id) return J({ oy: [] });
  return J({ oy: await oylar(env.OKUMA, id, n) });
}

export async function onRequestPost({ request, env }) {
  if (!env.OKUMA) return J({ hata: "KV yok" }, 500);
  let g;
  try { g = await request.json(); } catch (e) { return J({ hata: "gövde" }, 400); }
  const id = idTemiz(g.id), s = parseInt(g.secim, 10), n = Math.min(12, Math.max(2, parseInt(g.n || "4", 10)));
  if (!id || !(s >= 0 && s < n)) return J({ hata: "seçim" }, 400);
  const k = `a:${id}:${s}`;
  await env.OKUMA.put(k, String(parseInt((await env.OKUMA.get(k)) || "0", 10) + 1));
  return J({ tamam: true, oy: await oylar(env.OKUMA, id, n) });
}
