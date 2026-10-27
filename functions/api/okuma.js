/* Cloudflare Pages Function — okuma ve tıklama sayacı.
   Bağlamalar (Pages → Settings → Functions):
     KV namespace binding  : OKUMA
     Environment variable  : PANEL_ANAHTARI   (panelin okuma anahtarı, gizli)

   POST /api/okuma  {yol, kaynak}        → okuma: gün toplamı, sayfa, yönlendiren, şehir
   POST /api/okuma  {yol, olay}          → tıklama: tel / whatsapp / eposta / form
   GET  /api/okuma?anahtar=…&gun=30&dokum=7
        → günlük okuma+tıklama, son `dokum` günün sayfa / kaynak / şehir / tıklama dökümü (yalnız panel)

   Kişisel veri tutulmaz: IP, çerez, kimlik yok. Şehir, Cloudflare'in istek başına verdiği
   yaklaşık konumdan (request.cf.city) alınır ve yalnızca sayı olarak birikir.
*/
const GUN = () => new Date().toISOString().slice(0, 10);
const OLAYLAR = new Set(["tel", "whatsapp", "eposta", "form"]);

async function art(kv, anahtar) {
  const v = parseInt((await kv.get(anahtar)) || "0", 10) + 1;
  await kv.put(anahtar, String(v), { expirationTtl: 60 * 60 * 24 * 400 });
  return v;
}

const temiz = (s, n) => String(s || "").slice(0, n).replace(/[^\p{L}\p{N}\-\/\. ]/gu, "").trim();

export async function onRequestPost({ request, env }) {
  if (!env.OKUMA) return new Response("KV yok", { status: 500 });
  let g;
  try { g = await request.json(); } catch (e) { return new Response("", { status: 400 }); }
  const yol = String(g.yol || "/").slice(0, 160).replace(/[^\w\-\/\.]/g, "");
  const gun = GUN();
  const olay = String(g.olay || "");
  if (olay) {
    if (!OLAYLAR.has(olay)) return new Response("", { status: 400 });
    await art(env.OKUMA, `tg:${gun}`);                    // günün tıklama toplamı
    await art(env.OKUMA, `tk:${gun}:${olay}:${yol}`);     // tür + sayfa (t: ön eki tepki.js'te)
    return new Response(null, { status: 204 });
  }
  const kaynak = String(g.kaynak || "").slice(0, 80).replace(/[^\w\-\.]/g, "");
  await art(env.OKUMA, `g:${gun}`);                 // günün toplamı
  await art(env.OKUMA, `s:${gun}:${yol}`);          // sayfa bazlı
  if (kaynak) await art(env.OKUMA, `k:${gun}:${kaynak}`);  // yönlendiren
  const cf = request.cf || {};
  const ulke = temiz(cf.country, 4) || "?";
  const sehir = temiz(cf.city, 60) || "?";
  await art(env.OKUMA, `c:${gun}:${ulke}|${sehir}`);  // yaklaşık şehir
  return new Response(null, { status: 204 });
}

export async function onRequestGet({ request, env }) {
  const u = new URL(request.url);
  if (!env.PANEL_ANAHTARI || u.searchParams.get("anahtar") !== env.PANEL_ANAHTARI)
    return new Response("yetki yok", { status: 403 });
  const gunSay = Math.min(90, Math.max(1, parseInt(u.searchParams.get("gun") || "30", 10)));
  const dokum = Math.min(30, Math.max(1, parseInt(u.searchParams.get("dokum") || "7", 10)));
  const gunler = [], bugun = new Date();
  for (let i = 0; i < gunSay; i++) {
    const d = new Date(bugun); d.setUTCDate(d.getUTCDate() - i);
    const g = d.toISOString().slice(0, 10);
    const [ok, tk] = await Promise.all([env.OKUMA.get(`g:${g}`), env.OKUMA.get(`tg:${g}`)]);
    gunler.push({ gun: g, okuma: parseInt(ok || "0", 10), tiklama: parseInt(tk || "0", 10) });
  }
  // son `dokum` günün sayfa, kaynak, şehir ve tıklama dökümü
  const sayfa = {}, kaynak = {}, sehir = {}, tik = {};
  const hedefler = { s: sayfa, k: kaynak, c: sehir, tk: tik };
  for (let i = 0; i < dokum; i++) {
    const d = new Date(bugun); d.setUTCDate(d.getUTCDate() - i);
    const g = d.toISOString().slice(0, 10);
    for (const on of ["s", "k", "c", "tk"]) {
      let imlec;
      do {
        const l = await env.OKUMA.list({ prefix: `${on}:${g}:`, cursor: imlec });
        const degerler = await Promise.all(l.keys.map(k => env.OKUMA.get(k.name)));
        l.keys.forEach((k, j) => {
          const ad = k.name.slice(on.length + 1 + g.length + 1);
          hedefler[on][ad] = (hedefler[on][ad] || 0) + parseInt(degerler[j] || "0", 10);
        });
        imlec = l.list_complete ? null : l.cursor;
      } while (imlec);
    }
  }
  const sirala = (o, n) => Object.entries(o).sort((a, b) => b[1] - a[1]).slice(0, n).map(([ad, n]) => ({ ad, n }));
  const sehirler = sirala(sehir, 60).map(x => { const [ulke, ad] = x.ad.split("|"); return { ad, ulke, n: x.n }; });
  const tiklama = sirala(tik, 80).map(x => {
    const i = x.ad.indexOf(":"); return { olay: x.ad.slice(0, i), yol: x.ad.slice(i + 1), n: x.n };
  });
  return new Response(JSON.stringify({ gunler, dokum, sayfa: sirala(sayfa, 60), kaynak: sirala(kaynak, 40),
                                       sehir: sehirler, tiklama }),
    { headers: { "Content-Type": "application/json", "Cache-Control": "no-store" } });
}
