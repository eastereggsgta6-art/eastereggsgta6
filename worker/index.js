// Comentários do Easter Eggs GTA 6: Worker da Cloudflare com banco D1 e proteção Turnstile.
// Rotas: GET/POST /api/comments, GET /api/admin/pending, POST /api/admin/moderate. O resto é o site estático.

const MAX_NAME = 40, MAX_TEXT = 1200;

const json = (data, status = 200) =>
  new Response(JSON.stringify(data), { status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" } });

async function ensureTable(db) {
  await db.prepare(
    "CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY AUTOINCREMENT, page TEXT NOT NULL, name TEXT NOT NULL, text TEXT NOT NULL, created TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'pending', iphash TEXT)"
  ).run();
}

async function sha256(s) {
  const b = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return [...new Uint8Array(b)].map((x) => x.toString(16).padStart(2, "0")).join("");
}

function isAdmin(req, env) {
  const k = req.headers.get("x-admin-key") || "";
  return env.ADMIN_KEY && k.length >= 12 && k === env.ADMIN_KEY;
}

async function verifyTurnstile(token, ip, env) {
  if (!env.TURNSTILE_SECRET) return false;
  const fd = new FormData();
  fd.append("secret", env.TURNSTILE_SECRET);
  fd.append("response", token || "");
  if (ip) fd.append("remoteip", ip);
  const r = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", { method: "POST", body: fd });
  const j = await r.json();
  return !!j.success;
}

async function api(req, env, url) {
  const db = env.DB;
  if (!db) return json({ error: "Comentários ainda não configurados." }, 503);
  await ensureTable(db);
  const p = url.pathname;

  if (p === "/api/comments" && req.method === "GET") {
    const page = (url.searchParams.get("page") || "").slice(0, 120);
    const { results } = await db.prepare("SELECT id, name, text, created FROM comments WHERE page = ? AND status = 'approved' ORDER BY id ASC LIMIT 200").bind(page).all();
    return json({ comments: results });
  }

  if (p === "/api/comments" && req.method === "POST") {
    let b;
    try { b = await req.json(); } catch (_) { return json({ error: "Pedido inválido." }, 400); }
    const page = String(b.page || "").slice(0, 120);
    const name = String(b.name || "").trim().slice(0, MAX_NAME);
    const text = String(b.text || "").trim().slice(0, MAX_TEXT);
    if (!/^[a-z0-9-]+$/.test(page) || name.length < 2 || text.length < 3) return json({ error: "Preencha o nome e o comentário." }, 400);
    if (String(b.website || "")) return json({ ok: true }); // armadilha para robôs
    const ip = req.headers.get("cf-connecting-ip") || "";
    if (!(await verifyTurnstile(b.token, ip, env))) return json({ error: "Não conseguimos confirmar que você não é um robô. Tente de novo." }, 403);
    const iphash = (await sha256(ip + (env.ADMIN_KEY || ""))).slice(0, 24);
    const recent = await db.prepare("SELECT COUNT(*) AS n FROM comments WHERE iphash = ? AND created > ?").bind(iphash, new Date(Date.now() - 10 * 60 * 1000).toISOString()).first();
    if (recent && recent.n >= 5) return json({ error: "Muitos comentários seguidos. Espere alguns minutos." }, 429);
    await db.prepare("INSERT INTO comments (page, name, text, created, status, iphash) VALUES (?, ?, ?, ?, 'pending', ?)").bind(page, name, text, new Date().toISOString(), iphash).run();
    return json({ ok: true });
  }

  if (p === "/api/admin/pending" && req.method === "GET") {
    if (!isAdmin(req, env)) return json({ error: "Senha errada." }, 401);
    const st = url.searchParams.get("status") === "approved" ? "approved" : "pending";
    const { results } = await db.prepare("SELECT id, page, name, text, created FROM comments WHERE status = ? ORDER BY id DESC LIMIT 200").bind(st).all();
    return json({ comments: results });
  }

  if (p === "/api/admin/moderate" && req.method === "POST") {
    if (!isAdmin(req, env)) return json({ error: "Senha errada." }, 401);
    let b;
    try { b = await req.json(); } catch (_) { return json({ error: "Pedido inválido." }, 400); }
    const id = parseInt(b.id, 10);
    if (!id) return json({ error: "Comentário inválido." }, 400);
    if (b.action === "approve") await db.prepare("UPDATE comments SET status = 'approved' WHERE id = ?").bind(id).run();
    else if (b.action === "delete") await db.prepare("DELETE FROM comments WHERE id = ?").bind(id).run();
    else return json({ error: "Ação inválida." }, 400);
    return json({ ok: true });
  }

  return json({ error: "Não encontrado." }, 404);
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (url.pathname.startsWith("/api/")) {
      try { return await api(req, env, url); } catch (e) { return json({ error: "Erro no servidor." }, 500); }
    }
    return env.ASSETS.fetch(req);
  },
};
