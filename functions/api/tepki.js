/* Emoji tepki sayacı (12.10.2026) — çerezsiz; tekrar oyu tarayıcıdaki localStorage önler.
   GET  /api/tepki?yol=/trend/x   → {"sayi": {"begen": 3, ...}}
   POST /api/tepki {yol, tepki}   → artırır */
const TEPKI = ["begen", "gul", "sasir", "uzul", "kiz", "dusun"];
const J = (o, s = 200) => new Response(JSON.stringify(o), {
  status: s, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" } });
const yolTemiz = (y) => String(y || "/").slice(0, 160).replace(/[^\w\-\/]/g, "");

export async function onRequestGet({ request, env }) {
  if (!env.OKUMA) return J({ sayi: {} });
  const yol = yolTemiz(new URL(request.url).searchParams.get("yol"));
  const sayi = {};
  for (const t of TEPKI) sayi[t] = parseInt((await env.OKUMA.get(`t:${yol}:${t}`)) || "0", 10);
  return J({ sayi });
}

export async function onRequestPost({ request, env }) {
  if (!env.OKUMA) return J({ hata: "KV yok" }, 500);
  let g;
  try { g = await request.json(); } catch (e) { return J({ hata: "gövde" }, 400); }
  const yol = yolTemiz(g.yol), t = String(g.tepki || "");
  if (!TEPKI.includes(t)) return J({ hata: "tepki" }, 400);
  const k = `t:${yol}:${t}`;
  const v = parseInt((await env.OKUMA.get(k)) || "0", 10) + 1;
  await env.OKUMA.put(k, String(v));
  return J({ tamam: true, tepki: t, sayi: v });
}
