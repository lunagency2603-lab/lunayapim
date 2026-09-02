/* Cloudflare Pages Function — okuma sayacı.
   Bağlamalar (Pages → Settings → Functions):
     KV namespace binding  : OKUMA
     Environment variable  : PANEL_ANAHTARI   (panelin okuma anahtarı, gizli)

   POST /api/okuma            {yol, kaynak}   → sayaçları artırır (herkese açık, kimlik yok)
   GET  /api/okuma?anahtar=…  &gun=30         → günlük toplam + sayfa bazlı özet (yalnız panel)
*/
const GUN = () => new Date().toISOString().slice(0, 10);

async function art(kv, anahtar) {
  const v = parseInt((await kv.get(anahtar)) || "0", 10) + 1;
  await kv.put(anahtar, String(v), { expirationTtl: 60 * 60 * 24 * 400 });
  return v;
}

export async function onRequestPost({ request, env }) {
  if (!env.OKUMA) return new Response("KV yok", { status: 500 });
  let g;
  try { g = await request.json(); } catch (e) { return new Response("", { status: 400 }); }
  const yol = String(g.yol || "/").slice(0, 160).replace(/[^\w\-\/\.]/g, "");
  const kaynak = String(g.kaynak || "").slice(0, 80).replace(/[^\w\-\.]/g, "");
  const gun = GUN();
  await art(env.OKUMA, `g:${gun}`);                 // günün toplamı
  await art(env.OKUMA, `s:${gun}:${yol}`);          // sayfa bazlı
  if (kaynak) await art(env.OKUMA, `k:${gun}:${kaynak}`);  // yönlendiren
  return new Response("", { status: 204 });
}

export async function onRequestGet({ request, env }) {
  const u = new URL(request.url);
  if (!env.PANEL_ANAHTARI || u.searchParams.get("anahtar") !== env.PANEL_ANAHTARI)
    return new Response("yetki yok", { status: 403 });
  const gunSay = Math.min(90, parseInt(u.searchParams.get("gun") || "30", 10));
  const gunler = [], bugun = new Date();
  for (let i = 0; i < gunSay; i++) {
    const d = new Date(bugun); d.setUTCDate(d.getUTCDate() - i);
    const g = d.toISOString().slice(0, 10);
    gunler.push({ gun: g, okuma: parseInt((await env.OKUMA.get(`g:${g}`)) || "0", 10) });
  }
  // son 7 günün sayfa ve kaynak dökümü
  const sayfa = {}, kaynak = {};
  for (let i = 0; i < 7; i++) {
    const d = new Date(bugun); d.setUTCDate(d.getUTCDate() - i);
    const g = d.toISOString().slice(0, 10);
    for (const on of ["s", "k"]) {
      let imlec;
      do {
        const l = await env.OKUMA.list({ prefix: `${on}:${g}:`, cursor: imlec });
        for (const k of l.keys) {
          const ad = k.name.slice(on.length + 1 + g.length + 1);
          const v = parseInt((await env.OKUMA.get(k.name)) || "0", 10);
          const hedef = on === "s" ? sayfa : kaynak;
          hedef[ad] = (hedef[ad] || 0) + v;
        }
        imlec = l.list_complete ? null : l.cursor;
      } while (imlec);
    }
  }
  const sirala = o => Object.entries(o).sort((a, b) => b[1] - a[1]).slice(0, 40).map(([ad, n]) => ({ ad, n }));
  return new Response(JSON.stringify({ gunler, sayfa: sirala(sayfa), kaynak: sirala(kaynak) }),
    { headers: { "Content-Type": "application/json", "Cache-Control": "no-store" } });
}
