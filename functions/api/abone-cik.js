/* Bülten aboneliği — Cloudflare Pages Function + KV.
   Bağlama: KV namespace binding  ABONE
            Environment variable  PANEL_ANAHTARI (okuma sayacıyla aynı)
   POST /api/abone        {eposta, onay:true, kaynak}  → kaydeder (çift kayıt yok)
   POST /api/abone-cik    {eposta}                     → siler
   GET  /api/abone?anahtar=… → sayı + liste (yalnız panel)                       */
const EPOSTA = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

function json(o, kod = 200) {
  return new Response(JSON.stringify(o), { status: kod,
    headers: { "Content-Type": "application/json", "Cache-Control": "no-store" } });
}

export async function onRequestPost({ request, env }) {
  if (!env.ABONE) return json({ hata: "KV yok" }, 500);
  let g; try { g = await request.json(); } catch (e) { return json({ hata: "geçersiz" }, 400); }
  const url = new URL(request.url);
  const e = String(g.eposta || "").trim().toLowerCase().slice(0, 120);
  if (!EPOSTA.test(e)) return json({ hata: "E-posta adresi geçersiz görünüyor." }, 400);
  if (url.pathname.endsWith("/abone-cik")) {
    await env.ABONE.delete("a:" + e);
    return json({ ok: true, mesaj: "Abonelik kaldırıldı." });
  }
  if (g.onay !== true) return json({ hata: "Onay kutusu işaretlenmeli." }, 400);
  const var_ = await env.ABONE.get("a:" + e);
  if (var_) return json({ ok: true, mesaj: "Bu adres zaten kayıtlı." });
  await env.ABONE.put("a:" + e, JSON.stringify({
    t: new Date().toISOString(), kaynak: String(g.kaynak || "").slice(0, 60) }));
  return json({ ok: true, mesaj: "Kaydedildi. İlk sayı bir sonraki yayında gelecek." });
}

export async function onRequestGet({ request, env }) {
  const u = new URL(request.url);
  if (!env.PANEL_ANAHTARI || u.searchParams.get("anahtar") !== env.PANEL_ANAHTARI)
    return json({ hata: "yetki yok" }, 403);
  const liste = []; let imlec;
  do {
    const l = await env.ABONE.list({ prefix: "a:", cursor: imlec });
    for (const k of l.keys) {
      const v = JSON.parse((await env.ABONE.get(k.name)) || "{}");
      liste.push({ eposta: k.name.slice(2), t: v.t, kaynak: v.kaynak });
    }
    imlec = l.list_complete ? null : l.cursor;
  } while (imlec);
  liste.sort((a, b) => (b.t || "").localeCompare(a.t || ""));
  return json({ sayi: liste.length, liste });
}
