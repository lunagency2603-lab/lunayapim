/* En çok okunanlar (12.10.2026) — okuma sayacının (okuma.js) son 3 günlük
   sayfa toplamlarından ilk 10. Sonuç KV'de 30 dk önbelleğe alınır.
   GET /api/populer?on=/trend/  → {"liste": [{"yol": "/trend/x", "n": 12}, ...]} */
const J = (o) => new Response(JSON.stringify(o), {
  headers: { "content-type": "application/json; charset=utf-8", "cache-control": "public, max-age=600" } });

export async function onRequestGet({ request, env }) {
  if (!env.OKUMA) return J({ liste: [] });
  const on = (new URL(request.url).searchParams.get("on") || "/trend/").replace(/[^\w\-\/]/g, "");
  const ck = "cache:populer:" + on;
  const c = await env.OKUMA.get(ck);
  if (c) { try { return J(JSON.parse(c)); } catch (e) {} }
  const top = {};
  const bugun = new Date();
  for (let i = 0; i < 3; i++) {
    const d = new Date(bugun); d.setUTCDate(d.getUTCDate() - i);
    const g = d.toISOString().slice(0, 10);
    let imlec;
    do {
      const l = await env.OKUMA.list({ prefix: `s:${g}:${on}`, cursor: imlec });
      for (const k of l.keys) {
        const yol = k.name.slice(2 + g.length + 1);
        if (yol === on || /\/(aranan|piyasa)\/\d{4}/.test(yol) || /\/(taslak|editor)/.test(yol)) continue;
        top[yol] = (top[yol] || 0) + parseInt((await env.OKUMA.get(k.name)) || "0", 10);
      }
      imlec = l.list_complete ? null : l.cursor;
    } while (imlec);
  }
  const liste = Object.entries(top).sort((a, b) => b[1] - a[1]).slice(0, 10).map(([yol, n]) => ({ yol, n }));
  const sonuc = { liste, t: new Date().toISOString() };
  await env.OKUMA.put(ck, JSON.stringify(sonuc), { expirationTtl: 1800 });
  return J(sonuc);
}
