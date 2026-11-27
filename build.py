#!/usr/bin/env python3
"""Gera o site estático Easter Eggs GTA 6 a partir de data.json -> pasta dist/"""
import json, html, shutil, datetime, pathlib

ROOT = pathlib.Path(__file__).parent
D = json.load(open(ROOT / "data.json", encoding="utf-8"))
SITE, SRC, CATS, EGGS, MYS = D["site"], D["sources"], D["cats"], D["eggs"], D["mysteries"]
OUT = ROOT / "dist"
e_ = lambda s: html.escape(str(s), quote=True)
UPD = datetime.date.fromisoformat(SITE["updated"])
def is_new(e): return (UPD - datetime.date.fromisoformat(e["added"])).days <= 7
def br(d): return datetime.date.fromisoformat(d).strftime("%d/%m/%Y")
BYID = {e["id"]: e for e in EGGS}

EXTRA_CSS = """
.yt{position:relative;aspect-ratio:16/9;border-radius:14px;overflow:hidden;background:#000 center/cover no-repeat;cursor:pointer;border:1px solid var(--line)}
.yt::before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.05),rgba(0,0,0,.45))}
.yt .play{position:absolute;left:50%;top:50%;width:74px;height:52px;margin:-26px 0 0 -37px;border-radius:14px;background:#ff0033;box-shadow:0 6px 20px rgba(0,0,0,.4)}
.yt .play::after{content:"";position:absolute;left:30px;top:15px;border-style:solid;border-width:11px 0 11px 18px;border-color:transparent transparent transparent #fff}
.yt:hover .play,.yt:focus .play{transform:scale(1.08)}
.yt iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.ytc{color:var(--muted);font-size:13px;margin-top:8px}
.shot.loc img{aspect-ratio:760/440;object-fit:cover}
.shot+.shot{margin-top:10px}
.card .tags{display:flex;gap:6px;flex-wrap:wrap}
.card .tags span{font-size:11px;font-weight:700;color:var(--muted);background:var(--bg2);border:1px solid var(--line);border-radius:99px;padding:2px 8px}

.card{position:relative}
.card[hidden]{display:none}
.stretch{color:inherit;text-decoration:none}
.stretch::after{content:"";position:absolute;inset:0;border-radius:var(--r)}
.card .chk{position:relative;z-index:1}
.badge.new{background:rgba(255,61,139,.16);color:var(--pink)}
.fmsg{margin-top:12px;font-size:15px}.fmsg:empty{display:none}.fmsg.err{color:#fff;background:#3a1430;border:1px solid var(--pink);border-radius:12px;padding:12px 14px}.fdone{background:var(--card);border:1px solid var(--teal);border-radius:16px;padding:28px 22px;text-align:center;margin-top:8px}.fdone .ck{width:64px;height:64px;border-radius:50%;background:var(--teal);color:#0f0b1a;font-size:36px;line-height:64px;margin:0 auto 14px;font-weight:700}.fdone h3{font-family:"Archivo Black",sans-serif;font-size:24px;margin-bottom:8px}.fdone p{color:#d9d0ea;margin-bottom:16px}.btn[disabled]{opacity:.6;cursor:wait}
form.send{display:grid;gap:12px;max-width:640px;margin-top:18px}
form.send label{font-size:14px;font-weight:600;display:grid;gap:6px}
form.send input,form.send textarea{background:var(--bg2);border:1px solid var(--line);color:var(--text);border-radius:10px;padding:11px 13px;font:inherit;font-size:15px;outline:none}
form.send input:focus,form.send textarea:focus{border-color:var(--pink)}
form.send textarea{min-height:110px;resize:vertical}
form.send .hp{position:absolute;left:-9999px}
form.send button{justify-self:start}
.btn{background:var(--sunset);border:0;color:#1a0f12;font:inherit;font-weight:700;padding:11px 20px;border-radius:10px;cursor:pointer;text-decoration:none;display:inline-block}
.btn.ghost{background:transparent;color:var(--text);border:1px solid var(--line)}
.btn.ghost:hover{border-color:var(--teal)}
.ad-slot{margin:28px 0;min-height:90px;display:flex;justify-content:center}
.ad-slot:empty{display:none}
/* linha do tempo */
.tl{position:relative;margin-top:24px;padding-left:28px}
.tl::before{content:"";position:absolute;left:8px;top:6px;bottom:6px;width:2px;background:linear-gradient(var(--orange),var(--pink))}
.tl .g{position:relative;margin-bottom:26px}
.tl .g::before{content:"";position:absolute;left:-26px;top:6px;width:14px;height:14px;border-radius:50%;background:var(--bg);border:3px solid var(--orange)}
.tl .g h3{font-size:18px}.tl .g h3 small{color:var(--muted);font-weight:500;margin-left:8px}
.tl ul{list-style:none;margin-top:6px}
.tl li a{color:var(--text);text-decoration:none;font-size:15px;display:inline-block;padding:3px 0}
.tl li a:hover{color:var(--teal)}
/* faq */
.faq details{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 18px;margin-bottom:10px;max-width:760px}
.faq summary{cursor:pointer;font-weight:700;font-size:16px}
.faq details p{margin:10px 0 0;color:var(--muted)}
/* página do easter egg */
.crumb{font-size:13px;color:var(--muted);padding:22px 0 0}
.crumb a{color:var(--muted)}
.egg{max-width:760px;padding:18px 0 40px}
.egg h1{font-size:clamp(32px,5vw,48px);margin:12px 0 14px;max-width:none}
.egg .desc{color:var(--muted);font-size:18px}
.egg h2{font-size:13px;letter-spacing:1px;text-transform:uppercase;color:var(--orange);margin:30px 0 10px;font-family:"DM Sans",sans-serif}
.egg ol{padding-left:22px}.egg li{margin-bottom:7px}
.egg .src a{display:block;padding:10px 14px;border:1px solid var(--line);border-radius:10px;text-decoration:none;margin-bottom:8px;color:var(--text);font-size:15px}
.egg .src a:hover{border-color:var(--teal)}
.egg .src a small{color:var(--muted);display:block;font-size:12px}
.share{display:flex;gap:10px;flex-wrap:wrap}
.related{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}
.related a{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;color:var(--text);text-decoration:none;font-weight:600;font-size:15px}
.related a small{display:block;font-size:12px;font-weight:700;letter-spacing:.6px;text-transform:uppercase;margin-bottom:4px}
.related a:hover{border-color:#4a3d6e}
"""

FONTS = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,700&display=swap" rel="stylesheet">'''

def head(title, desc, path, pre, extra=""):
    url = SITE["url"].rstrip("/") + "/" + path
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e_(title)}</title>
<meta name="description" content="{e_(desc)}">
<link rel="canonical" href="{e_(url)}">
<meta property="og:type" content="website"><meta property="og:title" content="{e_(title)}">
<meta property="og:description" content="{e_(desc)}"><meta property="og:url" content="{e_(url)}">
<meta property="og:locale" content="pt_BR"><meta property="og:site_name" content="{e_(SITE["name"])}">
<meta property="og:image" content="{e_(SITE["url"].rstrip("/"))}/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{e_(SITE["url"].rstrip("/"))}/og.png">
{FONTS}
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/icon-192.png" type="image/png" sizes="192x192">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="icon" href="{pre}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{pre}apple-touch-icon.png">
<meta name="theme-color" content="#0f0b1a">
<meta name="google-adsense-account" content="{e_(SITE["adsense"])}">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={e_(SITE["adsense"])}" crossorigin="anonymous"></script>
<link rel="stylesheet" href="{pre}assets/style.css">
{extra}</head>
<body>
<header class="top"><div class="wrap">
  <a class="logo" href="{pre}index.html">EASTER EGGS <span>GTA 6</span></a>
  <nav><a href="{pre}index.html#lista">Easter eggs</a><a href="{pre}mapa.html">Mapa</a><a href="{pre}carros.html">Carros raros</a><a href="{pre}codigos.html">Códigos</a><a href="{pre}setup.html">Setup</a><a href="{pre}index.html#misterios">Mistérios</a><a href="{pre}index.html#enviar">Mandar descoberta</a></nav>
</div></header>
'''

def foot(pre):
    return f'''<footer><div class="wrap">
  <p>Site de fã, sem ligação com a Rockstar Games ou a Take-Two Interactive. Grand Theft Auto e todos os nomes relacionados pertencem aos seus donos.</p>
  <p>Siga: <a href="https://www.instagram.com/{e_(SITE["instagram"])}/" target="_blank" rel="noopener">Instagram @{e_(SITE["instagram"])}</a> · <a href="https://www.tiktok.com/@{e_(SITE["tiktok"])}" target="_blank" rel="noopener">TikTok @{e_(SITE["tiktok"])}</a> · Contato: {e_(SITE["email"])}</p>
  <p><a href="{pre}sobre.html">Sobre</a> · <a href="{pre}contato.html">Contato</a> · <a href="{pre}privacidade.html">Política de Privacidade</a></p>
  <p>Cada descoberta leva o crédito e o link de quem achou primeiro. Última atualização: {br(SITE["updated"])}.</p>
</div></footer>
<script src="{pre}assets/app.js"></script>
</body>
</html>
'''

def badges(e):
    b = '<span class="badge ok">Confirmado</span>' if e["ok"] else '<span class="badge wait">A confirmar</span>'
    if is_new(e): b = '<span class="badge new">Novo</span> ' + b
    return f'<span style="display:flex;gap:6px">{b}</span>'

CATART = {"piada": "vice", "misterio": "pantano", "gta": "keys", "pop": "praia", "encontro": "praia"}
FOTOS_ON = bool(D["site"].get("fotos"))
def foto_for(e):
    w = (e.get("w", "") + " " + e.get("t", "")).lower()
    for keys, f in [(("key lento","keys","dog island","maroon","mar aberto"),"keys"), (("grassrivers","pântano","cottonmouth"),"grassrivers"),
                    (("kalaga","lummox","tallaloko","manifest","floresta","millport"),"kalaga"), (("ambrosia","kelly county","starlet","port gellhorn","capri"),"ambrosia")]:
        if any(k in w for k in keys): return f
    if "vice" in w or "vespucci" in w or "washington" in w: return ["vice1","vice2","vice3"][sum(map(ord, e["id"])) % 3]
    if e.get("cat") == "misterio": return "grassrivers"
    return ["vice1","vice2","vice3","keys"][sum(map(ord, e["id"])) % 4]

DIFC = {"Fácil": "#3ddc84", "Médio": "#ffd23f", "Difícil": "#ff3d8b"}
def dif_html(e):
    if not e.get("dif"): return ""
    bars = {"Fácil": 1, "Médio": 2, "Difícil": 3}[e["dif"]]
    dots = "".join(f'<i style="background:{DIFC[e["dif"]] if k < bars else "#3a2f5c"}"></i>' for k in range(3))
    return f'<span class="dif" title="Dificuldade e tempo estimados"><b class="dots">{dots}</b>{e_(e["dif"])} · ⏱ {e_(e["tempo"])}</span>'

def cat_label(e): c = CATS[e["cat"]]; return f'<span class="cat" style="color:{c["c"]}">{e_(c["n"])}</span>'

def ad(slot):
    # Para ativar: cole o código do anúncio do AdSense dentro desta div (no lugar do comentário).
    return f'<div class="ad-slot" data-ad="{slot}"><!-- ANÚNCIO ({slot}): cole aqui o código do AdSense --></div>'

def comments_html(pid, path, title):
    app = SITE.get("cusdis", "")
    if not app: return ""
    return ('<h2>Comentários</h2><p class="cmt-note">Achou esse easter egg? Tem uma dica ou viu algo diferente? Conta aqui. Os comentários passam por aprovação antes de aparecer.</p>'
            '<div id="cusdis_thread" data-host="https://cusdis.com" data-app-id="' + e_(app) + '" data-page-id="' + e_(pid) + '" data-page-url="' + e_(SITE["url"] + "/" + path) + '" data-page-title="' + e_(title) + '" data-theme="dark"></div>'
            '<script defer src="https://cusdis.com/js/widget/lang/pt-br.js"></script><script defer src="https://cusdis.com/js/cusdis.es.js"></script>')

def news_html():
    N = D.get("news", [])[:5]
    if not N: return ""
    li = "".join('<li><time datetime="' + n["d"] + '">' + n["d"][8:10] + '/' + n["d"][5:7] + '</time><a href="' + n["u"] + '">' + e_(n["t"]) + '</a></li>' for n in N)
    return '<section class="news" aria-label="Novidades"><h2>🆕 Novidades no site</h2><ul>' + li + '</ul></section>'

def card(e):
    ph = f' style="--ph:url(../img/fotos/{foto_for(e)}-sm.jpg)"' if FOTOS_ON else ""
    return f'''<article class="card{' ph' if FOTOS_ON else ''}"{ph} data-id="{e["id"]}" data-cat="{e["cat"]}" data-ok="{1 if e["ok"] else 0}" data-new="{1 if is_new(e) else 0}">
  <div class="meta">{cat_label(e)}{badges(e)}</div>
  <h3><a class="stretch" href="easter-eggs/{e["id"]}.html">{e_(e["t"])}</a></h3>
  {('<span class="tags">' + ('<span>▶ vídeo</span>' if e.get("video") else '') + ('<span>📍 no mapa</span>' if e.get("map") else '') + ('<span>📷 print</span>' if e.get("img") else '') + '</span>') if (e.get("video") or e.get("map") or e.get("img")) else ''}
  <p>{e_(e["d"])}</p>
  <div class="where"><span>📍</span><span>{e_(e["w"])}</span></div>
  {dif_html(e)}
  <button class="chk" data-chk="{e["id"]}" aria-pressed="false"><span class="box"></span>Marcar como achado</button>
</article>'''

def faqs():
    n, ok = len(EGGS), sum(e["ok"] for e in EGGS)
    gv = [e for e in EGGS if e.get("game") == "GTA V"]
    return [
        ("Quantos easter eggs tem em GTA 6?",
         f"Até agora a gente listou {n} easter eggs e segredos, sendo {ok} confirmados por mais de uma fonte. A comunidade continua achando coisa nova todo dia, e a lista é atualizada sempre."),
        ("Tem OVNI em GTA 6?",
         "Tem relato de abdução alienígena do lado de fora de Port Gellhorn, de madrugada, que dá um troféu escondido chamado \"The Truth Is Out There\". Os detalhes de como ativar ainda estão sendo confirmados."),
        ("Tem Pé-Grande em GTA 6?",
         "Tem. O Pé-Grande de Leonida é o Skunk Ape, do folclore da Flórida. Ele aparece na região de Grassrivers e tem até uma missão secundária, \"Search for the Skunk Ape\"."),
        ("Dá pra entrar no apartamento do Dexter em GTA 6?",
         "Não. O prédio fica em Washington Island, em Vice City, mas o apartamento é fechado. O easter egg está no terraço, com objetos que lembram o \"kit\" do personagem."),
        ("GTA 6 tem referências a GTA 5?",
         "Tem várias: " + ", ".join(e["t"].lower() if i else e["t"] for i, e in enumerate(gv)) + ". Veja a linha do tempo de referências nesta página."),
        ("Os easter eggs desta lista têm spoiler da história?",
         "Não. A gente deixa de fora tudo o que tem a ver com reviravoltas, missões principais ou o final do jogo."),
    ]

def build_index():
    cats = '<button class="chip on" data-c="all">Todos</button>' + "".join(
        f'<button class="chip" data-c="{k}">{e_(v["n"])}</button>' for k, v in CATS.items())
    sts = "".join(f'<button class="chip{" on" if k=="all" else ""}" data-s="{k}">{n}</button>' for k, n in
                  [("all", "Todos"), ("new", "Novos"), ("ok", "Confirmados"), ("wait", "A confirmar"), ("todo", "Falta achar")])
    grid = "\n".join(card(e) for e in EGGS)
    # linha do tempo
    groups = {}
    for e in EGGS:
        if e.get("game"): groups.setdefault(e["game"], []).append(e)
    years = {g["n"]: g["y"] for g in D["games"]}
    tl = "".join(f'''<div class="g"><h3>{e_(g)}<small>{years.get(g, "")}</small></h3><ul>{"".join(f'<li><a href="easter-eggs/{e["id"]}.html">→ {e_(e["t"])}</a></li>' for e in lst)}</ul></div>'''
                 for g, lst in sorted(groups.items(), key=lambda x: years.get(x[0], 9999)))
    mys = "".join(f'''<div class="mcard"><span class="qm">? Em aberto</span><h3>{e_(m["q"])}</h3><p>{e_(m["k"])}</p>
      <div class="acts">{f'<a href="easter-eggs/{m["egg"]}.html">Ver o que já se sabe</a>' if m.get("egg") else f'<a href="{e_(SRC[m["src"]]["u"])}" target="_blank" rel="noopener">Fonte do boato: {e_(SRC[m["src"]]["n"])}</a>'}<a href="#enviar">Sei a resposta</a></div></div>''' for m in MYS)
    fq = faqs()
    faq_html = "".join(f"<details><summary>{e_(q)}</summary><p>{e_(a)}</p></details>" for q, a in fq)
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in fq]}, ensure_ascii=False)
    n_ok = sum(e["ok"] for e in EGGS)
    page = head("Easter Eggs GTA 6: todos os segredos e onde achar",
                "Lista completa e atualizada de easter eggs e segredos de GTA 6 em português: onde fica, como ativar e quem descobriu. Sem spoilers da história.",
                "", "", f'<script type="application/ld+json">{ld}</script>\n')
    page += f'''
<div class="hero art{' photo' if FOTOS_ON else ''}">{'<span class="credit-hero">Imagem: Rockstar Games (divulgação)</span>' if FOTOS_ON else ''}<div class="wrap">
  <span class="kicker">Atualizado diariamente</span>
  <h1>Todos os <em>easter eggs</em> de GTA 6</h1>
  <p class="lede">Os segredos, referências e mistérios que a comunidade já encontrou em Leonida, explicados em português: onde fica, como ativar e quem descobriu. Sem spoilers da história.</p>
  <div class="stats">
    <div class="stat"><b>{len(EGGS)}</b><small>easter eggs</small></div>
    <div class="stat"><b>{n_ok}</b><small>confirmados</small></div>
    <div class="stat"><b>{sum(is_new(e) for e in EGGS)}</b><small>novos esta semana</small></div>
    <div class="stat"><b>{UPD.strftime("%d/%m")}</b><small>última atualização</small></div>
  </div>
</div></div>

<main class="wrap" id="lista">
  {ad("topo")}
  {news_html()}
  <div class="controls">
    <div class="progress">
      <span class="lbl">Seu checklist: <b id="pN">0</b> de <b id="pT">0</b> achados</span>
      <div class="bar"><i id="pBar"></i></div>
      <button class="reset" id="reset" hidden>Zerar</button>
    </div>
    <div class="search">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
      <input id="q" type="search" placeholder="Buscar: Dexter, OVNI, Red Dead, cachorro..." autocomplete="off" aria-label="Buscar easter eggs">
    </div>
    <div class="chips">{cats}</div>
    <div class="row2"><span class="count" id="count">{len(EGGS)} de {len(EGGS)} easter eggs</span><div class="toggle" style="flex-wrap:wrap">{sts}</div></div>
  </div>
  <div class="grid" id="grid">
{grid}
    <div class="empty" id="empty" hidden></div>
  </div>
</main>

<section class="block" id="guias"><div class="wrap">
  <h2>Mais guias de GTA 6</h2>
  <div class="related" style="margin-top:16px">
    <a href="carros.html"><small style="color:var(--orange)">Guia</small>Carros raros: onde achar o Infernus, o Vitello, os Emerus e mais {len(D["cars"])} carros</a>
    <a href="codigos.html"><small style="color:var(--teal)">Guia</small>Códigos e cheats: os {len(D["cheats"]["known"])} códigos descobertos e como liberar os 61</a>
    <a href="mapa.html"><small style="color:var(--pink)">Mapa</small>Mapa interativo com os easter eggs e os carros raros</a>
    <a href="trofeus.html"><small style="color:#b9e6ff">Troféus</small>Os 27 troféus visíveis explicados, com checklist e a ordem pra platina</a>
    <a href="guia-de-compra.html"><small style="color:var(--yellow)">Antes de comprar</small>Standard ou Ultimate, quanto espaço precisa e qual console roda melhor</a>
    <a href="brasil.html"><small style="color:#3ddc84">Especial</small>Referências ao Brasil no GTA 6: Anitta, Sepultura, Azymuth e mais</a>
    <a href="setup.html"><small style="color:var(--yellow)">Compras</small>Monte seu setup: console, o jogo e os acessórios pra jogar GTA 6</a>
  </div>
</div></section>

<section class="mys" id="misterios"><div class="wrap">
  <h2>Mistérios em aberto</h2>
  <p class="sub">O que a comunidade ainda não resolveu. Sabe a resposta ou tem um vídeo que mostra? Manda pra gente: quem resolver primeiro leva o crédito aqui.</p>
  <div class="mgrid">{mys}</div>
</div></section>

<section class="block" id="referencias"><div class="wrap">
  <h2>Referências a outros jogos</h2>
  <p>Tudo o que GTA 6 esconde sobre os jogos anteriores da Rockstar, em ordem de lançamento.</p>
  <div class="tl">{tl}</div>
</div></section>

<div class="wrap">{ad("meio")}</div>

<section class="block faq" id="perguntas"><div class="wrap">
  <h2>Perguntas frequentes</h2>
  {faq_html}
</div></section>

<section class="block" id="enviar"><div class="wrap">
  <h2>Achou um easter egg?</h2>
  <p>Manda o link do vídeo ou post onde ele aparece. Toda descoberta publicada aqui leva o crédito de quem achou.</p>
  <form class="send" id="form-descoberta" name="descoberta" method="POST" action="https://formsubmit.co/7330d6841b2569056867314f774fa7e5">
    <input type="hidden" name="form-name" value="descoberta">
    <p class="hp"><label>Não preencha: <input name="bot-field"></label></p>
    <label>Seu nome ou @ (pro crédito)<input name="nome" required maxlength="80" placeholder="@seuperfil"></label>
    <label>Link do vídeo ou post<input name="link" type="text" inputmode="url" required placeholder="youtube.com/... ou tiktok.com/..."></label>
    <label>O que é e onde fica<textarea name="descricao" required maxlength="1500" placeholder="Ex.: tem uma placa escondida atrás do bar em Vice Beach que..."></textarea></label>
    <label>Seu e-mail (opcional, só pra gente te responder)<input name="email" type="email" placeholder="voce@email.com"></label>
    <button class="btn" type="submit">Enviar descoberta</button>
    <div id="form-msg" class="fmsg" role="status"></div>
  </form>
  <p style="margin-top:18px">Também dá pra mandar pelo <a href="https://www.instagram.com/{e_(SITE["instagram"])}/" target="_blank" rel="noopener">Instagram @{e_(SITE["instagram"])}</a>, pelo <a href="https://www.tiktok.com/@{e_(SITE["tiktok"])}" target="_blank" rel="noopener">TikTok @{e_(SITE["tiktok"])}</a> ou pelo e-mail <strong style="color:var(--text)">{e_(SITE["email"])}</strong>.</p>
</div></section>

<section class="block" id="sobre"><div class="wrap">
  <h2>Como a lista é feita</h2>
  <p>Reunimos as descobertas publicadas por jogadores e sites especializados, reescrevemos cada uma em português e sempre colocamos o link da fonte original.</p>
  <p><span class="badge ok">Confirmado</span> quer dizer que pelo menos duas fontes independentes mostram o easter egg. <span class="badge wait">A confirmar</span> quer dizer que só uma fonte relatou até agora, ou que os detalhes ainda não batem entre elas. <span class="badge new">Novo</span> marca o que entrou na lista nos últimos 7 dias.</p>
  <p>Não incluímos nada ligado às reviravoltas ou ao final da história.</p>
</div></section>
'''
    page += foot("")
    (OUT / "index.html").write_text(page, encoding="utf-8")

def build_egg(e):
    pre = "../"
    c = CATS[e["cat"]]
    desc = f'{e["t"]} em GTA 6: {e["w"]}. Veja como encontrar, passo a passo, e quem descobriu.'
    loc = ""
    if e.get("map"):
        loc = (f'<figure class="shot loc"><img src="../img/local/{e["id"]}.jpg" alt="Localização de {e_(e["t"])} no mapa de Leonida" loading="lazy" width="760" height="440">'
               f'<figcaption>{"Região aproximada" if e.get("mapApprox") else "Local"} no mapa de Leonida · <a href="../mapa.html#{e["id"]}">abrir no mapa interativo</a> · Mapa: © Rockstar Games</figcaption></figure>')
    if e.get("img"):
        cred = e_(e.get("imgCredit", "autor"))
        if e.get("imgLink"): cred = f'<a href="{e_(e["imgLink"])}" target="_blank" rel="noopener">{cred}</a>'
        shot = f'<figure class="shot"><img src="../{e_(e["img"])}" alt="{e_(e["t"])}" loading="lazy"><figcaption>Print: {cred} · usado com permissão</figcaption></figure>' + loc
    else:
        shot = loc + '<div class="shot empty">📷 Ainda sem print deste easter egg. Tem um? <a href="../index.html#enviar">Manda pra gente</a> e leva o crédito.</div>'
    vid = ""
    if e.get("video"):
        v = e["video"]; by = v.get("by")
        vid = (f'<h2>Passo a passo em vídeo</h2>'
               f'<div class="yt" data-yt="{e_(v["id"])}" role="button" tabindex="0" aria-label="Assistir ao vídeo" style="background-image:url(https://i.ytimg.com/vi/{e_(v["id"])}/hqdefault.jpg)"><span class="play" aria-hidden="true"></span></div>'
               f'<p class="ytc">{"Vídeo com vários easter eggs, procure por este no meio. " if v.get("multi") else ""}Vídeo{" de " + e_(by) if by else ""} no YouTube · <a href="https://www.youtube.com/watch?v={e_(v["id"])}" target="_blank" rel="noopener">assistir no YouTube</a>. Os créditos são do canal que publicou.</p>')
    same = [x for x in EGGS if x["id"] != e["id"] and x["cat"] == e["cat"]]
    other = [x for x in EGGS if x["id"] != e["id"] and x["cat"] != e["cat"]]
    rel = (same + other)[:3]
    related = "".join(f'<a href="{x["id"]}.html"><small style="color:{CATS[x["cat"]]["c"]}">{e_(CATS[x["cat"]]["n"])}</small>{e_(x["t"])}</a>' for x in rel)
    ld = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": e["t"] + " (GTA 6)",
                     "description": e["d"], "inLanguage": "pt-BR", "datePublished": e["added"], "dateModified": SITE["updated"],
                     "author": {"@type": "Organization", "name": SITE["name"]}}, ensure_ascii=False)
    page = head(f'{e["t"]} – Easter egg de GTA 6: onde fica e como achar', desc, f'easter-eggs/{e["id"]}.html', pre,
                f'<script type="application/ld+json">{ld}</script>\n')
    page += f'''
<main class="wrap">
  <div class="crumb"><a href="../index.html">Início</a> › <a href="../index.html#lista">Easter eggs</a> › {e_(c["n"])}</div>
  <article class="egg">
    {(f'<figure class="eban ph" style="background-image:url(../img/fotos/{foto_for(e)}.jpg)" role="img" aria-label="Paisagem de Leonida"><figcaption>Imagem ilustrativa da região · Rockstar Games (divulgação)</figcaption></figure>') if FOTOS_ON else f'<div class="eban" style="background-image:url(../img/art/{CATART[e["cat"]]}.svg)" role="img" aria-label="Ilustração de Leonida"></div>'}
    <div class="meta" style="display:flex;gap:10px;align-items:center;flex-wrap:wrap">{cat_label(e)}{badges(e)}</div>
    <h1>{e_(e["t"])}</h1>
    {('<div class="difbig">' + dif_html(e) + '<small>Estimativa pra quem já está perto do local</small></div>') if e.get("dif") else ""}
    <p class="desc">{e_(e["d"])}</p>
    <div style="margin-top:16px"><button class="chk" data-chk="{e["id"]}" aria-pressed="false"><span class="box"></span>Marcar como achado</button></div>

    <h2>Onde fica</h2>
    {shot}
    <p>📍 {e_(e["w"])}</p>

    <h2>Como encontrar</h2>
    <ol>{"".join(f"<li>{e_(h)}</li>" for h in e["how"])}</ol>
    {f'<div class="note">{e_(e["note"])}</div>' if e.get("note") else ""}

    {vid}

    {ad("artigo")}

    <h2>Fontes e créditos</h2>
    <div class="src">{"".join(f'<a href="{e_(SRC[k]["u"])}" target="_blank" rel="noopener">{e_(SRC[k]["n"])}<small>{e_(SRC[k]["u"].split("//")[1].split("/")[0])}</small></a>' for k in e["src"])}</div>
    <p style="color:var(--muted);font-size:13px;margin-top:6px">Adicionado em {br(e["added"])}.</p>

    <h2>Compartilhar</h2>
    <div class="share">
      <a class="btn ghost" data-share="wa" data-text="{e_(e["t"])} em GTA 6:" href="#" target="_blank" rel="noopener">WhatsApp</a>
      <a class="btn ghost" data-share="x" data-text="{e_(e["t"])} em GTA 6" href="#" target="_blank" rel="noopener">X / Twitter</a>
      <button class="btn ghost" data-copy>Copiar link</button>
    </div>

    {comments_html("egg-" + e["id"], "easter-eggs/" + e["id"] + ".html", e["t"])}

    <h2>Mais easter eggs</h2>
    <div class="related">{related}</div>
    <p style="margin-top:24px"><a class="btn" href="../index.html#lista">Ver todos os easter eggs</a></p>
  </article>
</main>
'''
    page += foot(pre)
    (OUT / "easter-eggs" / f'{e["id"]}.html').write_text(page, encoding="utf-8")


def build_map():
    G = json.loads((ROOT / "vendor" / "gtadb-pts.json").read_text(encoding="utf-8"))
    pins = [{"id": e["id"], "t": e["t"], "w": e["w"], "c": CATS[e["cat"]]["c"], "cn": CATS[e["cat"]]["n"], "ok": e["ok"],
             "gx": e["g"][0], "gy": e["g"][1], "ap": e.get("mapApprox", False), "k": "egg", "u": "easter-eggs/" + e["id"] + ".html"} for e in EGGS if e.get("g")]
    pins += [{"id": c["id"], "t": c["t"], "w": c["w"], "c": "#ffffff", "cn": "Carro raro · " + c["tipo"], "ok": c["ok"],
              "gx": c["g"][0], "gy": c["g"][1], "ap": c.get("mapApprox", False), "k": "car", "u": "carros/" + c["id"] + ".html"} for c in D["cars"] if c.get("g")]
    allx = [{"id": e["id"], "t": e["t"]} for e in EGGS] + [{"id": c["id"], "t": "Carro: " + c["t"]} for c in D["cars"]]
    gcount = {}
    for p in G["pts"]:
        gcount[p["c"]] = gcount.get(p["c"], 0) + 1
    extra = '<link rel="stylesheet" href="assets/leaflet.css">\n<style>' + MAP_CSS + '</style>\n'
    page = head("Mapa interativo de GTA 6: easter eggs, carros raros e mais de 1.400 lugares de Leonida",
                "Mapa interativo de Leonida com os easter eggs de GTA 6, carros raros, lojas, postos, esconderijos, aeroportos e mais de 1.400 lugares.",
                "mapa.html", "", extra)
    loose = [e for e in EGGS if not e.get("g")]
    catboxes = "".join(
        '<label class="tg lc"><input type="checkbox" data-lc="' + c["k"] + '"' + ("" if c["k"] == "outros" else " checked") + '><i style="background:' + c["c"] + '"></i>' + e_(c["n"]) + ' <small>' + str(gcount.get(c["k"], 0)) + '</small></label>'
        for c in G["cats"] if gcount.get(c["k"]))
    legend = "".join('<span><i style="background:' + v["c"] + '"></i>' + e_(v["n"]) + '</span>' for v in CATS.values())
    opts = "".join('<option value="' + x["id"] + '">' + e_(x["t"]) + '</option>' for x in allx)
    loose_li = "".join('<li><a href="easter-eggs/' + e["id"] + '.html">' + e_(e["t"]) + '</a></li>' for e in loose)
    npts = len(G["pts"])
    lc_js = json.dumps({c["k"]: {"n": c["n"], "c": c["c"]} for c in G["cats"]}, ensure_ascii=False)
    html = MAP_HTML
    for k, v in {
        "%%NEGGS%%": str(len(EGGS)), "%%NPTS100%%": str(npts // 100 * 100), "%%NPTS%%": str(npts),
        "%%CATBOXES%%": catboxes, "%%LEGEND%%": legend, "%%OPTS%%": opts, "%%NLOOSE%%": str(len(loose)), "%%LOOSE%%": loose_li,
        "%%AD%%": ad("mapa"), "%%PINS%%": json.dumps(pins, ensure_ascii=False), "%%LC%%": lc_js,
        "%%NCARS%%": str(len(D["cars"])), "%%EGGIDS%%": json.dumps([e["id"] for e in EGGS]), "%%CARIDS%%": json.dumps([c["id"] for c in D["cars"]]),
    }.items():
        html = html.replace(k, v)
    page += html
    page += foot("")
    (OUT / "mapa.html").write_text(page, encoding="utf-8")
    (OUT / "assets" / "lugares.json").write_text(json.dumps(G, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    shutil.copytree(ROOT / "vendor" / "tiles", OUT / "img" / "tiles", dirs_exist_ok=True)


MAP_HTML = r"""
<main class="wrap mappage">
  <div class="crumb"><a href="index.html">Início</a> › Mapa</div>
  <h1 class="mh">Mapa interativo de Leonida</h1>
  <p class="sub">Os %%NEGGS%% easter eggs, os carros raros e mais de %%NPTS100%% lugares de Leonida, como lojas, postos, esconderijos, aeroportos e pontos turísticos. Toque num ponto para ver o que é. Alfinetes com borda tracejada estão na região certa, mas o ponto exato ainda não foi confirmado.</p>
  <div class="mprog"><div class="mptxt"><b id="pTxt">0 de %%NEGGS%%</b> easter eggs achados <span id="pCar"></span></div><div class="mpbar"><i id="pBar"></i></div></div>
  <div class="msearch"><input id="mq" type="search" placeholder="Buscar no mapa: papagaio, Ammu-Nation, Starlet Motel, aeroporto…" autocomplete="off" aria-label="Buscar no mapa"><ul id="mres" hidden></ul></div>
  <div class="maptools"><label class="tg"><input type="checkbox" id="fEgg" checked> <b>Easter eggs</b></label><label class="tg"><input type="checkbox" id="fCar" checked> <b>Carros raros</b></label><label class="tg"><input type="checkbox" id="fHide"> Esconder os que já achei</label></div>
  <details class="lcats"><summary>Lugares de Leonida (%%NPTS%%) · escolher categorias</summary><div class="lcgrid">%%CATBOXES%%</div><div class="lcbtn"><button type="button" class="btn" id="lcAll">Mostrar todos</button><button type="button" class="btn" id="lcNone">Esconder todos</button></div></details>
  <div id="map" role="application" aria-label="Mapa de Leonida"></div>
  <div class="legend">%%LEGEND%%<span><i class="sq"></i>Carro raro</span><span><i class="ap"></i>Local aproximado</span><span><i class="dot"></i>Lugar de Leonida</span></div>
  <div id="editor" hidden>
    <b>Modo de edição</b>: clique no mapa onde fica o easter egg, escolha qual é e copie o código pra mandar.
    <div class="erow"><select id="esel">%%OPTS%%</select>
    <code id="eout">Clique no mapa…</code><button class="btn" id="ecopy" type="button">Copiar</button></div>
  </div>
  <section class="loose"><h2>Ainda sem lugar no mapa (%%NLOOSE%%)</h2>
  <p>Easter eggs sem local fixo ou que ninguém localizou ainda. Sabe onde fica? <a href="index.html#enviar">Manda pra gente</a>.</p>
  <ul>%%LOOSE%%</ul></section>
  %%AD%%
  <p class="credit">Mapa e lugares de Leonida: <a href="https://map.gtadb.org" target="_blank" rel="noopener">GTA VI Map Tiles e GTA VI Landmarks Data, de map.gtadb.org</a>, sob a licença <a href="https://creativecommons.org/licenses/by/4.0/deed.pt_BR" target="_blank" rel="noopener">CC BY 4.0</a>. Fizemos alterações: traduzimos as categorias e selecionamos só os lugares com nome. A imagem do mapa é © Rockstar Games. Os easter eggs e os carros são levantamento nosso. Este é um site de fã, sem ligação com a Rockstar Games ou a Take-Two Interactive.</p>
</main>
<script src="assets/leaflet.js"></script>
<script>
(function(){
  var PINS=%%PINS%%;
  var LC=%%LC%%;
  var LP=null;
  function ll(gx,gy){return [-(16384-gy)/32,(gx+16384)/32]}
  function toG(lat,lng){return [Math.round(lng*32-16384),Math.round(16384+lat*32)]}
  var T=L.TileLayer.extend({getTileUrl:function(c){return "img/tiles/"+c.z+"/"+c.z+","+c.y+","+c.x+".jpg"}});
  var map=L.map("map",{crs:L.CRS.Simple,minZoom:1,maxZoom:6,zoomSnap:.5,attributionControl:false,preferCanvas:true,maxBounds:[ll(-12500,11500),ll(7000,-11000)],maxBoundsViscosity:.8});
  new T("",{tileSize:256,minNativeZoom:0,maxNativeZoom:5,noWrap:true,errorTileUrl:"data:image/gif;base64,R0lGODlhAQABAAAAACw="}).addTo(map);
  map.fitBounds([ll(-9000,9500),ll(4200,-8300)]);
  var esc=function(s){return String(s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})};
  var M={}, gEgg=L.layerGroup().addTo(map), gCar=L.layerGroup().addTo(map), LG={}, LM={};
  var rend=L.canvas({padding:.5});
  document.getElementById("fEgg").addEventListener("change",function(){this.checked?gEgg.addTo(map):map.removeLayer(gEgg)});
  document.getElementById("fCar").addEventListener("change",function(){this.checked?gCar.addTo(map):map.removeLayer(gCar)});
  var KEY="ovos-achados", TOTAL=%%NEGGS%%, TOTALC=%%NCARS%%, EGGIDS=%%EGGIDS%%, CARIDS=%%CARIDS%%;
  function getF(){try{return new Set(JSON.parse(localStorage.getItem(KEY)||"[]"))}catch(_){return new Set()}}
  function setF(f){try{localStorage.setItem(KEY,JSON.stringify(Array.from(f)))}catch(_){}}
  var hide=document.getElementById("fHide");
  function popHtml(p,isF){
    return '<div class="pp"><small style="color:'+(p.k==="car"?"#ffd23f":p.c)+'">'+esc(p.cn)+'</small><b>'+esc(p.t)+'</b><span>📍 '+esc(p.w)+(p.ap?' (aproximado)':'')+'</span><a href="'+p.u+'">'+(p.k==="car"?"Ver como pegar →":"Ver como encontrar →")+'</a><button type="button" class="ppf'+(isF?' on':'')+'" data-id="'+p.id+'">'+(isF?(p.k==="car"?"✓ Peguei":"✓ Achei"):(p.k==="car"?"Marcar como pego":"Marcar como achado"))+'</button></div>';
  }
  function lpHtml(p){
    var c=LC[p.c];
    return '<div class="pp"><small style="color:'+c.c+'">'+esc(c.n)+'</small><b>'+esc(p.t)+'</b>'+(p.r?'<span>📍 '+esc(p.r)+'</span>':'')+(p.real?'<span class="real">Inspirado em: '+esc(p.real)+'</span>':'')+(p.u?'<span class="unc">Local ainda não confirmado</span>':'')+'<span class="src">Fonte: map.gtadb.org (CC BY 4.0)</span></div>';
  }
  function paint(){
    var f=getF(), ne=EGGIDS.filter(function(i){return f.has(i)}).length, nc=CARIDS.filter(function(i){return f.has(i)}).length;
    document.getElementById("pTxt").textContent=ne+" de "+TOTAL;
    document.getElementById("pCar").textContent="· "+nc+" de "+TOTALC+" carros";
    document.getElementById("pBar").style.width=Math.round(ne/TOTAL*100)+"%";
    PINS.forEach(function(p){
      var m=M[p.id], isF=f.has(p.id), el=m.getElement();
      if(el) el.classList.toggle("found",isF);
      m.setPopupContent(popHtml(p,isF));
      var g=p.k==="car"?gCar:gEgg;
      if(hide.checked&&isF){g.removeLayer(m)}else if(!g.hasLayer(m)){g.addLayer(m)}
    });
  }
  PINS.forEach(function(p){
    var ic=L.divIcon({className:"pin"+(p.ap?" ap":"")+(p.k==="car"?" car":""),html:'<span style="background:'+p.c+'"></span>',iconSize:[22,22],iconAnchor:[11,11],popupAnchor:[0,-10]});
    var m=L.marker(ll(p.gx,p.gy),{icon:ic,title:p.t,keyboard:true,zIndexOffset:1000}).addTo(p.k==="car"?gCar:gEgg);
    m.bindPopup(popHtml(p,false));
    M[p.id]=m;
  });
  document.getElementById("map").addEventListener("click",function(ev){
    var b=ev.target.closest(".ppf"); if(!b) return;
    var f=getF(), id=b.getAttribute("data-id"); f.has(id)?f.delete(id):f.add(id); setF(f); paint();
    if(M[id]&&map.hasLayer(M[id])) M[id].openPopup();
  });
  hide.addEventListener("change",paint);
  window.addEventListener("storage",paint);
  paint();
  var boxes=[].slice.call(document.querySelectorAll("[data-lc]"));
  function syncLC(){boxes.forEach(function(b){var g=LG[b.getAttribute("data-lc")]; if(!g)return; b.checked?g.addTo(map):map.removeLayer(g)})}
  boxes.forEach(function(b){b.addEventListener("change",syncLC)});
  document.getElementById("lcAll").addEventListener("click",function(){boxes.forEach(function(b){b.checked=true});syncLC()});
  document.getElementById("lcNone").addEventListener("click",function(){boxes.forEach(function(b){b.checked=false});syncLC()});
  fetch("assets/lugares.json").then(function(r){return r.json()}).then(function(j){
    LP=j.pts;
    LP.forEach(function(p){
      var g=LG[p.c]||(LG[p.c]=L.layerGroup());
      var m=L.circleMarker(ll(p.x,p.y),{renderer:rend,radius:4.5,weight:1.5,color:"#0f0b1a",fillColor:LC[p.c].c,fillOpacity:.95}).addTo(g);
      m.bindPopup(function(){return lpHtml(p)}); LM[p.id]=m;
    });
    syncLC();
    gEgg.eachLayer(function(m){m.setZIndexOffset(1000)});
  }).catch(function(){});
  var q=document.getElementById("mq"), res=document.getElementById("mres");
  var norm=function(s){return String(s).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g,"")};
  function go(id){
    if(M[id]){var p=PINS.find(function(x){return x.id===id}),g=p.k==="car"?gCar:gEgg; if(!map.hasLayer(g))g.addTo(map); if(!g.hasLayer(M[id]))g.addLayer(M[id]); map.setView(M[id].getLatLng(),4); M[id].openPopup();}
    else if(LM[id]){var lp=LP.find(function(x){return x.id===id}),g2=LG[lp.c]; if(!map.hasLayer(g2)){g2.addTo(map); var bx=document.querySelector('[data-lc="'+lp.c+'"]'); if(bx)bx.checked=true;} map.setView(LM[id].getLatLng(),5); LM[id].openPopup();}
    res.hidden=true; q.blur();
  }
  q.addEventListener("input",function(){
    var v=norm(q.value.trim()); if(v.length<2){res.hidden=true;return}
    var hits=PINS.filter(function(p){return norm(p.t+" "+p.w+" "+p.cn).indexOf(v)>-1}).map(function(p){return {id:p.id,t:p.t,s:p.w,c:p.c}});
    if(LP) hits=hits.concat(LP.filter(function(p){return norm(p.t+" "+p.r+" "+LC[p.c].n).indexOf(v)>-1}).map(function(p){return {id:p.id,t:p.t,s:(p.r?p.r+" · ":"")+LC[p.c].n,c:LC[p.c].c}}));
    hits=hits.slice(0,10);
    res.innerHTML=hits.length?hits.map(function(p){return '<li><button type="button" data-id="'+p.id+'"><i style="background:'+p.c+'"></i><span>'+esc(p.t)+'<small>'+esc(p.s)+'</small></span></button></li>'}).join(""):'<li class="none">Nada no mapa com esse nome. Tente a <a href="index.html?q='+encodeURIComponent(q.value)+'#lista">busca da lista</a>.</li>';
    res.hidden=false;
  });
  res.addEventListener("click",function(ev){var b=ev.target.closest("button[data-id]"); if(b) go(b.getAttribute("data-id"))});
  q.addEventListener("keydown",function(ev){if(ev.key==="Enter"){var b=res.querySelector("button[data-id]"); if(b){ev.preventDefault();go(b.getAttribute("data-id"))}} if(ev.key==="Escape")res.hidden=true;});
  document.addEventListener("click",function(ev){if(!ev.target.closest(".msearch"))res.hidden=true});
  function fromHash(){
    var h=location.hash.slice(1);
    document.getElementById("editor").hidden=h!=="editar";
    if(M[h]) go(h);
  }
  window.addEventListener("hashchange",fromHash); fromHash();
  var tmp=null;
  map.on("click",function(ev){
    if(document.getElementById("editor").hidden) return;
    var g=toG(ev.latlng.lat,ev.latlng.lng);
    if(tmp) map.removeLayer(tmp);
    tmp=L.circleMarker(ev.latlng,{radius:9,color:"#fff",weight:3}).addTo(map);
    document.getElementById("eout").textContent=document.getElementById("esel").value+": "+g[0]+", "+g[1];
  });
  document.getElementById("esel").addEventListener("change",function(){var o=document.getElementById("eout");if(o.textContent.indexOf(":")>0)o.textContent=this.value+o.textContent.slice(o.textContent.indexOf(":"));});
  document.getElementById("ecopy").addEventListener("click",function(){var t=document.getElementById("eout").textContent,b=this;try{navigator.clipboard.writeText(t).then(function(){b.textContent="Copiado!"},function(){b.textContent="Selecione e copie"})}catch(_){b.textContent="Selecione e copie"}});
})();
</script>
"""

MAP_CSS = """
.lcats{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 14px;margin:0 0 12px}
.lcats summary{cursor:pointer;font-weight:700;font-size:14px}
.lcgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:6px 14px;margin-top:10px}
.lc i{display:inline-block;width:11px;height:11px;border-radius:50%;border:1.5px solid #0f0b1a}.lc small{color:var(--muted)}
.lcbtn{display:flex;gap:8px;margin-top:10px}.lcbtn .btn{padding:6px 12px;font-size:13px}
.legend i.dot{width:9px;height:9px;background:#a99cc4}
.pp .real{font-size:12px}.pp .unc{font-size:12px;color:var(--yellow)}.pp .src{font-size:11px;opacity:.7}

.mprog{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin:14px 0 10px}
.mptxt{font-size:14px;color:var(--muted);margin-bottom:8px}.mptxt b{color:var(--text)}
.mpbar{height:8px;background:#2a2142;border-radius:6px;overflow:hidden}.mpbar i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--pink),var(--orange),var(--yellow));transition:width .3s}
.msearch{position:relative;margin-bottom:10px}
.msearch input{width:100%;background:#0f0b1a;border:1px solid var(--line);border-radius:12px;color:var(--text);padding:12px 14px;font:inherit;font-size:15px}
.msearch ul{position:absolute;z-index:1000;left:0;right:0;top:100%;margin-top:4px;list-style:none;background:#1d1630;border:1px solid #2e2547;border-radius:12px;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,.5)}
.msearch li button{display:flex;gap:10px;align-items:center;width:100%;text-align:left;background:none;border:0;color:var(--text);padding:10px 14px;font:inherit;cursor:pointer}
.msearch li button:hover{background:#2a2142}.msearch li i{flex:0 0 12px;height:12px;border-radius:50%}
.msearch li small{display:block;color:var(--muted);font-size:12px}.msearch li.none{padding:12px 14px;color:var(--muted);font-size:14px}
.pin.found span{opacity:.35;filter:grayscale(.6)}
.pp .ppf{margin-top:8px;width:100%;background:#2a2142;border:1px solid #3a2f5c;color:#f4eefc;border-radius:8px;padding:7px;font:inherit;font-size:13px;font-weight:700;cursor:pointer}
.pp .ppf.on{background:var(--teal);color:#0f0b1a;border-color:var(--teal)}
.pin.car span{border-radius:5px;width:18px;height:18px;margin:2px}
.legend i.sq{background:#fff;border-radius:3px}
.maptools{display:flex;gap:18px;align-items:center;flex-wrap:wrap;margin:0 0 12px}
.tg{font-size:14px;color:var(--muted);display:flex;gap:6px;align-items:center;cursor:pointer}
.maptools{display:flex;gap:16px;align-items:center;flex-wrap:wrap;margin:16px 0 4px}
.seg{display:inline-flex;background:var(--bg2);border:1px solid var(--line);border-radius:99px;padding:3px}
.seg button{background:none;border:0;color:var(--muted);font:inherit;font-size:14px;font-weight:700;padding:6px 14px;border-radius:99px;cursor:pointer}
.seg button.on{background:var(--sunset);color:#1a0f12}
.tg{font-size:14px;color:var(--muted);display:flex;gap:6px;align-items:center;cursor:pointer}
.plbl{pointer-events:none}
.plbl span{display:block;transform:translate(-50%,-50%);white-space:nowrap;font-family:"DM Sans",sans-serif;font-weight:700;color:#fff;letter-spacing:.3px;
  text-shadow:0 0 3px #0f0b1a,0 0 3px #0f0b1a,0 0 6px #0f0b1a,0 1px 2px #000}
.plbl.t1 span{font-family:"Archivo Black",sans-serif;font-weight:400;font-size:15px;text-transform:uppercase;letter-spacing:1px;color:#ffe3ef}
.plbl.t2 span{font-size:13px;display:none;transform:translate(-50%,40%)}
.plbl.t3 span{font-size:11.5px;color:#d9ccf2;display:none;transform:translate(-50%,45%)}
#map.show2 .plbl.t2 span,#map.show3 .plbl.t3 span{display:block}
#map.orig .plbl span{color:#fff}

.mh{font-family:"Archivo Black",sans-serif;font-size:clamp(30px,5vw,46px);margin:10px 0 6px}
.mappage .sub{color:var(--muted);max-width:720px}
.legend{display:flex;flex-wrap:wrap;gap:14px;margin:16px 0 12px;font-size:13px;color:var(--muted)}
.legend i{display:inline-block;width:12px;height:12px;border-radius:50%;margin-right:6px;vertical-align:-1px;border:2px solid #0f0b1a}
.legend i.ap{background:transparent;border:2px dashed #fff}
#map{position:relative;z-index:0;isolation:isolate;height:min(78vh,820px);border-radius:18px;border:1px solid var(--line);background:#2f90b0}
.pin span{display:block;width:22px;height:22px;border-radius:50%;border:3px solid #0f0b1a;box-shadow:0 2px 6px rgba(0,0,0,.45)}
.pin.ap span{border:3px dashed #fff}
.pin:hover span,.pin:focus span{transform:scale(1.2)}
.leaflet-popup-content-wrapper{background:var(--bg2);color:var(--text);border-radius:12px;border:1px solid var(--line)}
.leaflet-popup-tip{background:var(--bg2)}
.leaflet-container a.leaflet-popup-close-button{color:var(--muted)}
.pp{display:flex;flex-direction:column;gap:4px;font:14px "DM Sans",sans-serif;min-width:200px}
.pp small{font-weight:700;letter-spacing:.6px;text-transform:uppercase;font-size:11px}
.pp b{font-size:16px}.pp span{color:var(--muted)}
.pp a{color:var(--teal);font-weight:700;margin-top:4px}
#editor{margin-top:14px;background:var(--card);border:1px dashed var(--pink);border-radius:12px;padding:14px 16px;font-size:14px}
.erow{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-top:10px}
.erow select{background:var(--bg2);color:var(--text);border:1px solid var(--line);border-radius:8px;padding:8px;font:inherit;max-width:100%}
.erow code{background:var(--bg);padding:8px 10px;border-radius:8px;font-size:13px;user-select:all}
.loose{margin-top:34px}.loose h2{font-size:20px;margin-bottom:6px}
.loose p{color:var(--muted);margin-bottom:10px}
.loose ul{columns:2 260px;list-style:none}.loose li{padding:3px 0}.loose li a{color:var(--text);text-decoration:none}.loose li a:hover{color:var(--teal)}
.credit{color:var(--muted);font-size:12px;margin:24px 0 10px}
"""

def build_404():
    import random
    pre = "/"
    pick = sorted([e for e in EGGS if e["ok"]], key=lambda e: e["added"], reverse=True)[:6]
    cards = "".join(f'<a href="/easter-eggs/{e["id"]}.html"><small style="color:{CATS[e["cat"]]["c"]}">{e_(CATS[e["cat"]]["n"])}</small>{e_(e["t"])}</a>' for e in pick)
    page = head("Página não encontrada – Easter Eggs GTA 6", "Essa página não existe. Veja todos os easter eggs de GTA 6.", "404.html", pre,
                '<meta name="robots" content="noindex">\n<style>.nf{padding:70px 0 60px;max-width:760px}.nf .big{font-family:"Archivo Black",sans-serif;font-size:clamp(90px,18vw,170px);line-height:.9;background:var(--sunset);-webkit-background-clip:text;background-clip:text;color:transparent}.nf h1{font-size:clamp(28px,4.5vw,42px);margin:14px 0 10px;max-width:none}.nf p{color:var(--muted);font-size:17px}.nf form{display:flex;gap:10px;margin:26px 0 34px;flex-wrap:wrap}.nf input{flex:1;min-width:220px;background:var(--bg2);border:1px solid var(--line);color:var(--text);border-radius:12px;padding:13px 15px;font:inherit;font-size:16px;outline:none}.nf input:focus{border-color:var(--pink)}.nf h2{font-size:14px;letter-spacing:1px;text-transform:uppercase;color:var(--orange);margin-bottom:12px}.nf .acts{display:flex;gap:10px;flex-wrap:wrap;margin-top:30px}</style>\n')
    page += f'''
<main class="wrap nf">
  <div class="big">404</div>
  <h1>Esse easter egg não existe… ainda.</h1>
  <p>A página que você procurou não está aqui. Pode ter mudado de endereço, ou o link estava errado. Mas Leonida está cheia de segredos de verdade:</p>
  <form action="/" method="get" role="search">
    <input name="q" type="search" placeholder="Buscar: Pé-Grande, OVNI, Dexter, Vice City..." aria-label="Buscar easter eggs" autofocus>
    <button class="btn" type="submit">Buscar</button>
  </form>
  <h2>Os mais recentes</h2>
  <div class="related">{cards}</div>
  <div class="acts"><a class="btn" href="/#lista">Ver todos os easter eggs</a><a class="btn ghost" href="/mapa.html">Abrir o mapa</a><a class="btn ghost" href="/#misterios">Mistérios em aberto</a></div>
</main>
'''
    page += foot(pre)
    (OUT / "404.html").write_text(page, encoding="utf-8")

def build_crops():
    from PIL import Image, ImageDraw
    from PIL import ImageFont
    src = Image.open(ROOT / "vendor" / "mapa-leonida.jpg").convert("RGB")
    LBLS = json.load(open(ROOT / "labels.json", encoding="utf-8"))
    F1 = ImageFont.truetype(str(ROOT / "vendor" / "fonts" / "archivo-black-latin-400-normal.woff"), 21 * 3)
    F2 = ImageFont.truetype(str(ROOT / "vendor" / "fonts" / "dm-sans-latin-700-normal.woff"), 17 * 3)
    W, H = src.size; CW, CH = 760, 440
    (OUT / "img" / "local").mkdir(parents=True, exist_ok=True)
    items = [(e, e["id"], CATS[e["cat"]]["c"]) for e in EGGS] + [(c, "carro-" + c["id"], "#ffffff") for c in D["cars"]]
    for e, fname, colr in items:
        if not e.get("map"): continue
        px, py = e["map"][0] * W, e["map"][1] * H
        x0 = int(min(max(px - CW / 2, 0), W - CW)); y0 = int(min(max(py - CH / 2, 0), H - CH))
        # recorte com zoom 1.25x pra ficar mais legível
        z = 1.25; cw, ch = int(CW / z), int(CH / z)
        x0 = int(min(max(px - cw / 2, 0), W - cw)); y0 = int(min(max(py - ch / 2, 0), H - ch))
        im = src.crop((x0, y0, x0 + cw, y0 + ch)).resize((CW, CH), Image.LANCZOS)
        S = 3; big = Image.new("RGBA", (CW * S, CH * S), (0, 0, 0, 0)); d = ImageDraw.Draw(big)
        cx, cy = (px - x0) * z * S, (py - y0) * z * S
        col = colr
        hexes = {"#ffffff": "#ffffff", "var(--pink)": "#ff3d8b", "var(--violet)": "#8b5cf6", "var(--orange)": "#ff9a3c", "var(--teal)": "#2de2c8", "var(--yellow)": "#ffd23f"}
        rgb = tuple(int(hexes.get(col, "#ff3d8b")[i:i + 2], 16) for i in (1, 3, 5))
        if e.get("mapApprox"):
            R = 70 * S
            d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=rgb + (55,), outline=rgb + (255,), width=4 * S)
        r = 13 * S
        d.ellipse([cx - r - 4 * S, cy - r - 4 * S, cx + r + 4 * S, cy + r + 4 * S], fill=(15, 11, 26, 255))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=rgb + (255,))
        for l in []:
            lx, ly = (l["x"] * W - x0) * z * S, (l["y"] * H - y0) * z * S
            if not (40 * S < lx < (CW - 40) * S and 20 * S < ly < (CH - 20) * S): continue
            if abs(lx - cx) < 60 * S and abs(ly - cy) < 26 * S: ly = cy + 40 * S
            txt = l["n"].upper() if l["t"] == 1 else l["n"]; f = F1 if l["t"] == 1 else F2
            d.text((lx, ly), txt, font=f, anchor="mm", fill=(255, 255, 255, 255) if l["t"] != 1 else (255, 227, 239, 255), stroke_width=4 * S // 2, stroke_fill=(15, 11, 26, 255))
        big = big.resize((CW, CH), Image.LANCZOS)
        im = Image.alpha_composite(im.convert("RGBA"), big).convert("RGB")
        im.save(OUT / "img" / "local" / f'{fname}.jpg', quality=84, optimize=True, progressive=True)

ART_PAGES = {"trofeus": "keys", "guia-de-compra": "vice", "brasil": "praia", "setup": "vice", "sobre": "keys", "contato": "pantano"}

def simple_page(slug, title, desc, body, extra_css="", extra_head=""):
    page = head(title, desc, f"{slug}.html", "", extra_head + f"<style>.doc{{max-width:760px;padding:26px 20px 60px}}.doc h1{{font-family:'Archivo Black',sans-serif;font-size:clamp(32px,5vw,46px);margin:10px 0 8px;max-width:none}}.doc h2{{font-size:20px;margin:30px 0 8px}}.doc p,.doc li{{color:#d9d0ea;margin-bottom:10px}}.doc ul{{padding-left:22px}}.doc .upd{{color:var(--muted);font-size:14px}}.doc a{{color:var(--teal)}}{extra_css}</style>\n")
    page += f'<main class="wrap doc"><div class="crumb"><a href="index.html">Início</a> › {e_(title.split(" – ")[0])}</div>{('<div class="eban" style="background-image:url(img/art/' + ART_PAGES[slug] + '.svg)" role="img" aria-label="Ilustração de Leonida"></div>') if slug in ART_PAGES else ""}{body}</main>\n'
    page += foot("")
    (OUT / f"{slug}.html").write_text(page, encoding="utf-8")

def build_static_pages():
    em, ig, tt = e_(SITE["email"]), e_(SITE["instagram"]), e_(SITE["tiktok"])
    upd = br(SITE["updated"])
    simple_page("sobre", "Sobre – Easter Eggs GTA 6", "Quem faz o Easter Eggs GTA 6, como a lista de easter eggs é montada e como as descobertas são creditadas.", f"""
<h1>Sobre o site</h1>
<p>O <strong>Easter Eggs GTA 6</strong> é um site de fã, em português, que reúne os segredos, referências e mistérios escondidos em Grand Theft Auto VI. A ideia é simples: explicar cada easter egg com calma, dizer onde fica, mostrar o passo a passo e dar o crédito a quem descobriu.</p>
<h2>Como a lista é feita</h2>
<p>A gente acompanha o que jogadores, criadores de conteúdo e sites especializados estão encontrando em Leonida. Cada descoberta é checada em mais de uma fonte sempre que possível, reescrita em português com nossas palavras e publicada com o link das fontes originais.</p>
<ul>
<li><strong>Confirmado</strong>: pelo menos duas fontes independentes mostram o easter egg.</li>
<li><strong>A confirmar</strong>: só uma fonte relatou até agora, ou os detalhes ainda não batem entre as fontes.</li>
<li><strong>Novo</strong>: entrou na lista nos últimos 7 dias.</li>
</ul>
<h2>Sem spoilers</h2>
<p>Não publicamos nada ligado às reviravoltas, às missões principais ou ao final da história. Se um segredo depende de algum ponto da campanha, avisamos só o capítulo, sem contar o que acontece.</p>
<h2>Créditos e correções</h2>
<p>Toda descoberta publicada aqui leva o nome de quem achou e o link pra fonte. Os vídeos incorporados são dos canais que os publicaram, e os créditos são deles. Achou um erro, quer que um crédito seja corrigido ou prefere que algum conteúdo seu seja removido? Escreva pra <strong>{em}</strong> que a gente ajusta rápido.</p>
<h2>Aviso</h2>
<p>Este é um site independente de fãs, sem nenhuma ligação com a Rockstar Games ou a Take-Two Interactive. Grand Theft Auto, GTA, Leonida e todos os nomes, imagens e marcas relacionados pertencem aos seus respectivos donos. O mapa de Leonida usado no site é © Rockstar Games e aparece só para indicar a localização dos easter eggs.</p>
<p><a class="btn" href="contato.html" style="color:#1a0f12;text-decoration:none">Fale com a gente</a></p>
""")
    simple_page("contato", "Contato – Easter Eggs GTA 6", "Fale com o Easter Eggs GTA 6: mande uma descoberta, peça uma correção ou proponha uma parceria.", f"""
<h1>Contato</h1>
<p>Quer mandar uma descoberta, corrigir uma informação, pedir a remoção de algum conteúdo ou propor uma parceria? Use um dos canais abaixo.</p>
<ul>
<li><strong>E-mail:</strong> {em}</li>
<li><strong>Instagram:</strong> <a href="https://www.instagram.com/{ig}/" target="_blank" rel="noopener">@{ig}</a></li>
<li><strong>TikTok:</strong> <a href="https://www.tiktok.com/@{tt}" target="_blank" rel="noopener">@{tt}</a></li>
</ul>
<h2>Mande uma mensagem</h2>
<form class="send" id="form-descoberta" name="contato" method="POST" action="https://formsubmit.co/7330d6841b2569056867314f774fa7e5">
  <input type="hidden" name="form-name" value="contato">
  <p class="hp"><label>Não preencha: <input name="bot-field"></label></p>
  <label>Seu nome<input name="nome" required maxlength="80"></label>
  <label>Seu e-mail<input name="email" type="email" required placeholder="voce@email.com"></label>
  <label>Assunto<input name="assunto" maxlength="120" placeholder="Correção, crédito, parceria..."></label>
  <label>Mensagem<textarea name="mensagem" required maxlength="3000"></textarea></label>
  <button class="btn" type="submit">Enviar mensagem</button>
  <div id="form-msg" class="fmsg" role="status"></div>
</form>
<p style="margin-top:20px">Pra mandar um easter egg novo, também dá pra usar o <a href="index.html#enviar">formulário de descobertas</a> da página inicial.</p>
""")
    simple_page("privacidade", "Política de Privacidade – Easter Eggs GTA 6", "Como o Easter Eggs GTA 6 trata dados pessoais, cookies e anúncios, de acordo com a LGPD.", f"""
<h1>Política de Privacidade</h1>
<p class="upd">Última atualização: {upd}</p>
<p>Esta política explica quais dados o site <strong>eastereggsgta6.com.br</strong> ("Easter Eggs GTA 6") coleta, por que coleta e quais são os seus direitos, de acordo com a Lei Geral de Proteção de Dados (Lei nº 13.709/2018, LGPD).</p>
<h2>1. Quem é o responsável</h2>
<p>O controlador dos dados é o responsável pelo site Easter Eggs GTA 6, que pode ser contatado pelo e-mail <strong>{em}</strong>.</p>
<h2>2. Quais dados coletamos</h2>
<ul>
<li><strong>Dados que você envia</strong>: quando usa os formulários de descoberta ou de contato, recebemos o que você preencher (nome ou @, e-mail, links e a mensagem). Usamos esses dados só pra analisar a descoberta, publicar o crédito quando você pedir e responder você.</li>
<li><strong>Dados técnicos de acesso</strong>: como qualquer site, o servidor registra informações como endereço IP, tipo de navegador, páginas visitadas e horário. Usamos isso de forma agregada pra estatísticas de audiência e segurança.</li>
<li><strong>Checklist "já achei"</strong>: os easter eggs que você marca ficam salvos só no seu navegador (armazenamento local). Esses dados não são enviados pra gente.</li>
</ul>
<h2>3. Serviços de terceiros</h2>
<ul>
<li><strong>Hospedagem (Cloudflare) e formulários (FormSubmit)</strong>: o site fica hospedado na Cloudflare, Inc., e as mensagens dos formulários são entregues no nosso e-mail pelo serviço FormSubmit. As duas empresas tratam dados técnicos e as mensagens enviadas em nosso nome, fora do Brasil. Isso envolve transferência internacional de dados, feita com as garantias previstas na LGPD.</li>
<li><strong>Vídeos do YouTube</strong>: os vídeos só carregam quando você clica no player, usando o modo de privacidade reforçada (youtube-nocookie.com). A partir do clique, o Google pode coletar dados conforme a política dele.</li>
<li><strong>Fontes do Google</strong>: as fontes do site são carregadas do Google Fonts, o que envia seu endereço IP ao Google.</li>
<li><strong>Google AdSense (anúncios)</strong>: o site pode exibir anúncios do Google. O Google e seus parceiros usam cookies pra mostrar anúncios com base nas suas visitas a este e a outros sites. Você pode desativar a personalização de anúncios nas <a href="https://adssettings.google.com" target="_blank" rel="noopener">Configurações de anúncios do Google</a>. Saiba mais em <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">como o Google usa informações de sites que usam os serviços dele</a>.</li>
</ul>
<h2>4. Cookies</h2>
<p>O site em si não usa cookies próprios. Cookies podem ser definidos pelo Google (anúncios e vídeos, depois que você clica no player). Você pode bloquear ou apagar cookies nas configurações do seu navegador, e o site continua funcionando.</p>
<h2>5. Por quanto tempo guardamos</h2>
<p>Mensagens dos formulários ficam guardadas pelo tempo necessário pra responder e registrar créditos, e são apagadas quando você pedir. Dados técnicos ficam retidos pelos prazos dos serviços de hospedagem.</p>
<h2>6. Seus direitos</h2>
<p>Pela LGPD, você pode pedir a confirmação de que tratamos seus dados, o acesso, a correção, a exclusão, a portabilidade e informações sobre com quem compartilhamos, além de revogar consentimentos. É só escrever pra <strong>{em}</strong>. Você também pode reclamar à Autoridade Nacional de Proteção de Dados (ANPD).</p>
<h2>7. Público</h2>
<p>GTA 6 é um jogo para maiores de 18 anos, e este site não é direcionado a crianças.</p>
<h2>8. Mudanças nesta política</h2>
<p>Podemos atualizar esta política, por exemplo quando adicionarmos novos serviços. A data no topo mostra a versão mais recente.</p>
""")



ARROW_CSS = """
.code{display:inline-flex;gap:4px;flex-wrap:wrap}
.code b{display:inline-grid;place-items:center;width:28px;height:28px;border-radius:7px;background:var(--bg2);border:1px solid var(--line);font-size:16px;color:var(--text)}
table.t{width:100%;border-collapse:collapse;margin:8px 0 18px;font-size:15px}
table.t th{text-align:left;font-size:12px;letter-spacing:.8px;text-transform:uppercase;color:var(--muted);padding:8px 10px;border-bottom:1px solid var(--line)}
table.t td{padding:12px 10px;border-bottom:1px solid var(--line);vertical-align:top;color:#e7def5}
table.t td small{display:block;color:var(--muted);margin-top:3px}
.tw{overflow-x:auto}
.steps{counter-reset:s;list-style:none;padding:0 !important;display:grid;gap:10px;margin:10px 0 20px}
.steps li{counter-increment:s;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px 14px 54px;position:relative;color:#e7def5}
.steps li::before{content:counter(s);position:absolute;left:14px;top:12px;width:28px;height:28px;border-radius:50%;background:var(--sunset);color:#1a0f12;font-weight:800;display:grid;place-items:center}
.warn{background:rgba(255,61,139,.08);border:1px solid rgba(255,61,139,.35);color:#ffd0e2;border-radius:12px;padding:12px 16px;margin:14px 0}
.carlist{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:14px;margin:14px 0 30px}
.carcard{position:relative;background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:18px;display:flex;flex-direction:column;gap:8px}
.carcard:hover{border-color:#4a3d6e}
.carcard h3{font-size:19px;line-height:1.25;margin:0}.carcard p{color:var(--muted) !important;font-size:14px;margin:0 !important}
.carcard .kv{font-size:13px;color:var(--text)}.carcard .kv span{color:var(--muted)}
.carcard a.stretch{color:var(--text) !important;text-decoration:none}
.carpic{position:relative;background:radial-gradient(ellipse at 50% 70%,#2a2140,#171126 70%);border-radius:12px;margin:-4px -4px 4px;padding:10px 6px 2px;display:flex;justify-content:center}
.carpic .carsvg{width:100%;max-width:260px;height:auto}
.carpic.shot-yt{padding:0;overflow:hidden;aspect-ratio:16/9}
.carpic.shot-yt img{width:100%;height:100%;object-fit:cover;display:block}
.carhero.yt-h{padding:0;overflow:hidden;aspect-ratio:16/9}
.carhero.yt-h img{width:100%;height:100%;object-fit:cover;display:block}
.carhero.yt-h span{background:rgba(15,11,26,.75);padding:2px 8px;border-radius:6px;color:#d9d0ea}
.carpic .vtag{position:absolute;right:8px;top:8px;font-size:11px;font-weight:700;color:#fff;background:rgba(255,0,51,.85);border-radius:6px;padding:2px 7px}
.carhero{position:relative;background:radial-gradient(ellipse at 50% 70%,#2a2140,#171126 70%);border:1px solid var(--line);border-radius:16px;display:flex;justify-content:center;padding:18px 10px 8px;margin:6px 0 16px}
.carhero .carsvg{width:100%;max-width:440px;height:auto}
.carhero span{position:absolute;right:12px;bottom:8px;font-size:11px;color:var(--muted)}
.pill{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.6px;text-transform:uppercase;padding:3px 9px;border-radius:99px;background:rgba(255,154,60,.15);color:var(--orange)}
"""


def codes_html(code):
    label = code.replace("↑", "cima").replace("↓", "baixo").replace("←", "esquerda").replace("→", "direita")
    return '<span class="code" aria-label="' + e_(label) + '">' + "".join(f"<b>{a}</b>" for a in code.split()) + "</span>"


def src_links(keys):
    return "".join(f'<a href="{e_(SRC[k]["u"])}" target="_blank" rel="noopener">{e_(SRC[k]["n"])}<small>{e_(SRC[k]["u"].split("//")[1].split("/")[0])}</small></a>' for k in keys)


def build_codes():
    C = D["cheats"]
    cats = []
    for x in C["known"]:
        if x["cat"] not in cats:
            cats.append(x["cat"])
    tables = ""
    for cat in cats:
        rows = "".join(f'<tr><td><strong>{e_(x["n"])}</strong><small>{e_(x["e"])}</small></td><td>{codes_html(x["code"])}</td><td>{e_(x["unlock"])}</td></tr>' for x in C["known"] if x["cat"] == cat)
        tables += f'<h2>{e_(cat)}</h2><div class="tw"><table class="t"><thead><tr><th>Cheat</th><th>Código (PS5 e Xbox)</th><th>Como liberar</th></tr></thead><tbody>{rows}</tbody></table></div>'
    unk = "".join(f'<tr><td><strong>{e_(x["n"])}</strong></td><td>{e_(x["cat"])}</td><td>{e_(x["unlock"])}</td></tr>' for x in C["unknown"])
    fq = [("GTA 6 tem códigos de trapaça?", f"Tem. São 61 cheats no total, e {len(C['known'])} códigos já foram descobertos. Eles só funcionam depois que você termina a história."),
          ("Como colocar código no GTA 6?", "Abra o celular apertando ↑ no direcional. Na tela inicial do celular, segure L1 + R1 (PS5) ou LB + RB (Xbox) e digite a sequência no direcional. Antes, o cheat precisa estar liberado na aba Progresso."),
          ("Cheat do GTA 6 bloqueia troféus?", "Bloqueia. Com qualquer cheat ativo, os troféus e conquistas param de ser liberados e o jogo para de salvar. Pra voltar ao normal, saia sem salvar e carregue o último save."),
          ("Tem código de dinheiro no GTA 6?", "Tem um só: o de US$ 250.000 (↑ → ↓ ← ↑ ← ↓ →), liberado quando você termina a história.")]
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in fq]}, ensure_ascii=False)
    faq = "".join(f"<details><summary>{e_(q)}</summary><p>{e_(a)}</p></details>" for q, a in fq)
    body = f"""
<h1>Códigos e cheats de GTA 6 (PS5 e Xbox)</h1>
<p class="upd">Atualizado em {br(SITE["updated"])} · {len(C["known"])} de 61 códigos descobertos</p>
<p>GTA 6 tem 61 cheats, mas eles funcionam de um jeito diferente dos GTAs antigos: o menu de cheats só aparece <strong>depois que você termina a história</strong>, e cada cheat precisa ser liberado com um desafio. Os códigos são os mesmos no PS5 e no Xbox Series X|S.</p>
{ad("topo")}
<h2>Como usar os cheats</h2>
<ol class="steps">
<li>Termine a missão final da história. Aparece uma área nova, <strong>Cheats</strong>, na aba <strong>Progresso</strong> do menu de pausa.</li>
<li>Libere o cheat que você quer cumprindo o desafio indicado na tabela. Alguns já vêm liberados no fim da história.</li>
<li>No mundo aberto, aperte <strong>↑ no direcional</strong> pra abrir o celular.</li>
<li>Na tela inicial do celular, <strong>segure L1 + R1</strong> (PS5) ou <strong>LB + RB</strong> (Xbox) e digite a sequência no direcional.</li>
</ol>
<div class="warn"><strong>Atenção:</strong> com qualquer cheat ativo, os troféus e conquistas ficam bloqueados e o jogo para de salvar. Pra voltar ao normal, saia sem salvar e carregue o último save.</div>
<h2>Os 4 cheats liberados no fim da história</h2>
<p>US$ 250.000, Foco infinito, Força de ataque e Mudar o clima não pedem desafio nenhum: ficam prontos assim que os créditos terminam.</p>
{tables}
{ad("meio")}
<h2>Cheats com código ainda desconhecido ({len(C["unknown"])})</h2>
<p>Esses cheats existem e já se sabe como liberar cada um, mas a sequência de botões ainda não foi descoberta. Assim que aparecer, a gente atualiza.</p>
<div class="tw"><table class="t"><thead><tr><th>Cheat</th><th>Tipo</th><th>Como liberar</th></tr></thead><tbody>{unk}</tbody></table></div>
<h2>Perguntas frequentes</h2><div class="faq">{faq}</div>
<h2>Fontes</h2><div class="egg"><div class="src">{src_links(C["src"])}</div></div>
<p style="margin-top:24px"><a class="btn" href="index.html#lista" style="color:#1a0f12;text-decoration:none">Ver os easter eggs</a> <a class="btn ghost" href="carros.html" style="text-decoration:none">Carros raros</a></p>
"""
    simple_page("codigos", "Códigos de GTA 6: todos os cheats de PS5 e Xbox",
                f"Todos os códigos e cheats de GTA 6 para PS5 e Xbox: {len(C['known'])} códigos descobertos, como liberar os 61 cheats e como digitar no celular.",
                body, ARROW_CSS + ".doc{max-width:1000px}.doc .egg{padding:0;max-width:none}.faq details{max-width:none}",
                f'<script type="application/ld+json">{ld}</script>\n')


def car_card(c, pre=""):
    st = '<span class="badge ok">Confirmado</span>' if c["ok"] else '<span class="badge wait">A confirmar</span>'
    wish = '<div class="kv"><span>Lista do Randy</span></div>' if c.get("wish") else ""
    v = c.get("video") or {}
    pic = (f'<img src="https://i.ytimg.com/vi/{e_(v["id"])}/hqdefault.jpg" alt="{e_(c["t"])} em GTA 6" loading="lazy">' if v and not v.get("multi") else car_svg(c))
    return (f'<article class="carcard"><div class="carpic{" shot-yt" if v and not v.get("multi") else ""}">{pic}{"<span class=vtag>▶ vídeo</span>" if v else ""}</div><div style="display:flex;justify-content:space-between;gap:8px;align-items:center"><span class="pill">{e_(c["tipo"])}</span>{st}</div>'
            f'<h3><a class="stretch" href="{pre}carros/{c["id"]}.html">{e_(c["t"])}</a></h3><p>📍 {e_(c["w"])}</p>'
            f'<div class="kv"><span>Acesso:</span> {e_(c["access"])}</div>{wish}</article>')


def build_cars():
    cars = D["cars"]
    (OUT / "carros").mkdir(exist_ok=True)
    wish = [c for c in cars if c.get("wish")]
    other = [c for c in cars if not c.get("wish")]
    tips = "".join(f"<li>{e_(t)}</li>" for t in D["carTips"])
    body = f"""
<h1>Carros raros de GTA 6: onde encontrar</h1>
<p class="upd">Atualizado em {br(SITE["updated"])} · {len(cars)} carros</p>
<p>Os carros especiais de GTA 6 ficam sempre no mesmo lugar: em mansões, garagens, esconderijos de gangue e locais de roubo. Aqui estão os mais procurados, com o local, o horário quando importa e como levar cada um sem chamar a polícia.</p>
{ad("topo")}
<h2>Lista de desejos do Randy (Capítulo 3 em diante)</h2>
<p>O Randy, o receptador de carros, tem uma lista de superesportivos. A maioria precisa do clonador de chaves.</p>
<div class="carlist">{"".join(car_card(c) for c in wish)}</div>
<h2>Outros carros especiais</h2>
<div class="carlist">{"".join(car_card(c) for c in other)}</div>
{ad("meio")}
<h2>Dicas pra roubar, vender e registrar</h2>
<ul>{tips}</ul>
<p style="margin-top:20px"><a class="btn" href="mapa.html" style="color:#1a0f12;text-decoration:none">Ver os carros no mapa</a> <a class="btn ghost" href="codigos.html" style="text-decoration:none">Códigos e cheats</a></p>
"""
    simple_page("carros", "Carros raros de GTA 6: onde encontrar cada um",
                f"Onde encontrar os {len(cars)} carros raros mais procurados de GTA 6: Infernus, Vitello, Emerus, Thrax, Itali RSX e outros, com local, horário e como levar.",
                body, ARROW_CSS + ".doc{max-width:1000px}")
    for c in cars:
        pre = "../"
        loc = ""
        if c.get("map"):
            loc = (f'<figure class="shot loc"><img src="../img/local/carro-{c["id"]}.jpg" alt="Localização do {e_(c["t"])} no mapa" loading="lazy" width="760" height="440">'
                   f'<figcaption>{"Região aproximada" if c.get("mapApprox") else "Local"} no mapa · <a href="../mapa.html#{c["id"]}">abrir no mapa interativo</a> · Mapa: © Rockstar Games</figcaption></figure>')
        rel = [x for x in cars if x["id"] != c["id"]][:3]
        related = "".join(f'<a href="{x["id"]}.html"><small style="color:var(--orange)">{e_(x["tipo"])}</small>{e_(x["t"])}</a>' for x in rel)
        st = '<span class="badge ok">Confirmado</span>' if c["ok"] else '<span class="badge wait">A confirmar</span>'
        wishpill = '<span class="pill" style="background:rgba(45,226,200,.14);color:var(--teal)">Lista do Randy</span>' if c.get("wish") else ""
        note = f'<div class="note">{e_(c["note"])}</div>' if c.get("note") else ""
        eggbtn = f'<p style="margin-top:12px"><a class="btn" href="../easter-eggs/{c["egg"]}.html">Ver a página completa</a></p>' if c.get("egg") else ""
        steps = "".join(f"<li>{e_(h)}</li>" for h in c["how"])
        page = head(f'{c["t"]} em GTA 6: onde encontrar e como pegar',
                    f'Onde fica o {c["t"]} em GTA 6: {c["w"]}. Veja como levar o carro passo a passo.',
                    f'carros/{c["id"]}.html', pre, f"<style>{ARROW_CSS}</style>\n")
        page += f"""
<main class="wrap">
  <div class="crumb"><a href="../index.html">Início</a> › <a href="../carros.html">Carros raros</a> › {e_(c["tipo"])}</div>
  <article class="egg">
    <div class="meta" style="display:flex;gap:10px;align-items:center;flex-wrap:wrap"><span class="pill">{e_(c["tipo"])}</span>{st}{wishpill}</div>
    <h1>{e_(c["t"])}</h1>
    {carhero(c)}
    <p class="desc">📍 {e_(c["w"])}</p>
    <p style="margin-top:8px"><strong>Acesso:</strong> {e_(c["access"])}</p>
    <h2>Onde fica</h2>
    {loc}
    <h2>Como pegar</h2>
    <ol>{steps}</ol>
    {note}
    {video_block(c.get("video"))}
    {eggbtn}
    {ad("artigo")}
    <h2>Fontes</h2>
    <div class="src">{src_links(c["src"])}</div>
    <p style="color:var(--muted);font-size:13px;margin-top:6px">Adicionado em {br(c["added"])}.</p>
    <h2>Compartilhar</h2>
    <div class="share">
      <a class="btn ghost" data-share="wa" data-text="{e_(c["t"])} em GTA 6:" href="#" target="_blank" rel="noopener">WhatsApp</a>
      <a class="btn ghost" data-share="x" data-text="Onde achar o {e_(c["t"])} em GTA 6" href="#" target="_blank" rel="noopener">X / Twitter</a>
      <button class="btn ghost" data-copy>Copiar link</button>
    </div>
    <h2>Outros carros raros</h2>
    <div class="related">{related}</div>
    <p style="margin-top:24px"><a class="btn" href="../carros.html">Ver todos os carros</a></p>
  </article>
</main>
"""
        page += foot(pre)
        (OUT / "carros" / f'{c["id"]}.html').write_text(page, encoding="utf-8")


def build_og():
    n = len(EGGS)
    ncar = len(D["cars"])
    nc = len(D["cheats"]["known"])
    tpl = (ROOT / "og_template.html").read_text(encoding="utf-8")
    html_ = tpl.replace("{N}", str(n)).replace("{NCAR}", str(ncar)).replace("{NC}", str(nc))
    tmp = ROOT / "og.html"
    tmp.write_text(html_, encoding="utf-8")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1200, "height": 630})
        pg.goto(tmp.as_uri())
        pg.wait_for_timeout(1500)
        pg.screenshot(path=str(OUT / "og.png"))
        b.close()


def car_svg(c, big=False):
    col = c.get("color", "#ff3d8b")
    sh = c.get("shape", "sport")
    bodies = {
        "super": "M18 92 L40 74 L110 58 L168 56 L214 70 L262 78 L282 90 L282 104 L18 104 Z",
        "sport": "M18 94 L46 74 L104 58 L170 56 L214 72 L258 80 L282 92 L282 104 L18 104 Z",
        "classic": "M16 92 L34 78 L86 72 L108 54 L176 54 L204 74 L264 80 L284 92 L284 104 L16 104 Z",
        "muscle": "M14 90 L30 78 L92 74 L114 58 L178 58 L206 76 L270 80 L286 90 L286 104 L14 104 Z",
        "suv": "M20 96 L24 66 L64 62 L92 38 L210 38 L244 62 L278 70 L282 104 L20 104 Z",
        "tank": "M22 100 L40 78 L250 78 L276 100 Z M80 78 L96 58 L196 58 L212 78 Z M180 64 L290 52 L292 58 L184 72 Z",
    }
    glass = {
        "super": "M112 62 L166 60 L200 72 L120 74 Z",
        "sport": "M108 62 L168 60 L204 74 L112 76 Z",
        "classic": "M112 58 L172 58 L194 74 L104 74 Z",
        "muscle": "M118 62 L174 62 L196 78 L110 78 Z",
        "suv": "M98 44 L204 44 L232 64 L80 64 Z",
        "tank": "",
    }
    wheels = '<circle cx="78" cy="104" r="17" fill="#0f0b1a"/><circle cx="78" cy="104" r="8" fill="#3a3152"/><circle cx="226" cy="104" r="17" fill="#0f0b1a"/><circle cx="226" cy="104" r="8" fill="#3a3152"/>'
    if sh == "tank":
        wheels = '<rect x="30" y="96" width="246" height="22" rx="11" fill="#0f0b1a"/>' + "".join(f'<circle cx="{x}" cy="107" r="7" fill="#3a3152"/>' for x in range(50, 270, 30))
    uid = c["id"].replace("-", "")
    h = 'height="170"' if big else ""
    return (f'<svg class="carsvg" viewBox="0 0 300 130" {h} role="img" aria-label="Ilustração do {e_(c["t"])}">'
            f'<defs><linearGradient id="g{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{col}"/><stop offset="1" stop-color="{col}" stop-opacity=".55"/></linearGradient>'
            f'<radialGradient id="s{uid}" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{col}" stop-opacity=".35"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient></defs>'
            f'<ellipse cx="150" cy="116" rx="140" ry="12" fill="url(#s{uid})"/>'
            f'<path d="{bodies[sh]}" fill="url(#g{uid})" stroke="#0f0b1a" stroke-width="2" stroke-linejoin="round"/>'
            + (f'<path d="{glass[sh]}" fill="#0f0b1a" opacity=".75"/>' if glass[sh] else "")
            + f'<rect x="270" y="86" width="12" height="5" rx="2" fill="#ffd23f"/><rect x="18" y="86" width="10" height="5" rx="2" fill="#ff3d8b"/>'
            + wheels + '</svg>')


def carhero(c):
    v = c.get("video") or {}
    if v and not v.get("multi"):
        return (f'<div class="carhero yt-h"><img src="https://i.ytimg.com/vi/{e_(v["id"])}/hqdefault.jpg" alt="{e_(c["t"])} em GTA 6">'
                f'<span>Imagem: miniatura do vídeo no YouTube · créditos do canal</span></div>')
    return f'<div class="carhero">{car_svg(c, True)}<span>Ilustração</span></div>'


def video_block(v, title="Passo a passo em vídeo"):
    if not v:
        return ""
    by = v.get("by")
    pre = ""
    if v.get("multi"):
        pre = "Vídeo com vários carros: procure este no meio. "
    if v.get("pt"):
        pre += "Vídeo em português. "
    return (f'<h2>{title}</h2>'
            f'<div class="yt" data-yt="{e_(v["id"])}" role="button" tabindex="0" aria-label="Assistir ao vídeo" style="background-image:url(https://i.ytimg.com/vi/{e_(v["id"])}/hqdefault.jpg)"><span class="play" aria-hidden="true"></span></div>'
            f'<p class="ytc">{pre}Vídeo{" de " + e_(by) if by else ""} no YouTube · <a href="https://www.youtube.com/watch?v={e_(v["id"])}" target="_blank" rel="noopener">assistir no YouTube</a>. Os créditos são do canal que publicou.</p>')


def build_setup():
    items = [x for x in D.get("setup", []) if not x.get("hide")]
    groups = []
    for it in items:
        if it["g"] not in groups: groups.append(it["g"])
    body = """<h1>Monte seu setup pra jogar GTA 6</h1>
<p class="upd">Atualizado em """ + br(SITE["updated"]) + """</p>
<div class="aviso"><strong>Transparência:</strong> os botões desta página são <strong>links de afiliado do Mercado Livre</strong>. Se você comprar por eles, o site ganha uma pequena comissão, sem custo a mais pra você. É isso que ajuda a manter o site no ar. Os preços mudam todo dia, por isso não colocamos valores aqui: confira no próprio Mercado Livre.</div>"""
    for g in groups:
        body += f"<h2>{e_(g)}</h2><div class='prods'>"
        for it in [x for x in items if x["g"] == g]:
            body += f"""<div class="prod"><div class="pic">{('<img src="' + it["img"] + '" alt="' + e_(it["n"]) + '" loading="lazy" width="160" height="160">') if it.get("img") else it["ic"]}</div><div><h3>{e_(it["n"])}</h3><p>{e_(it["w"])}</p>
<a class="btn-ml" href="{e_(it["link"])}" target="_blank" rel="sponsored nofollow noopener">Ver preço no Mercado Livre →</a></div></div>"""
        body += "</div>"
    body += "<p style='margin-top:30px'>Achou um produto que deveria estar aqui? <a href='contato.html'>Manda pra gente</a>.</p>"
    css = ".aviso{background:#1d1630;border:1px solid #2e2547;border-left:4px solid var(--yellow);border-radius:12px;padding:14px 16px;margin:18px 0 6px;font-size:15px;color:#d9d0ea}.prods{display:grid;gap:12px}.prod{display:flex;gap:16px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px}.prod .pic{flex:0 0 96px;height:96px;border-radius:12px;background:#fff;display:flex;align-items:center;justify-content:center;font-size:32px;overflow:hidden}.prod .pic img{width:100%;height:100%;object-fit:contain}.prod h3{font-size:17px;margin-bottom:4px}.prod p{font-size:15px;margin-bottom:10px}.btn-ml{display:inline-block;background:#ffe600;color:#1a1a1a!important;font-weight:700;text-decoration:none;border-radius:10px;padding:9px 14px;font-size:14px}.btn-ml:hover{filter:brightness(.95)}"
    simple_page("setup", "Setup pra GTA 6: console, jogo e acessórios – Easter Eggs GTA 6", "O que você precisa pra jogar GTA 6: PS5, PS5 Pro, Xbox Series X, o jogo em mídia física, SSD, controle e headset.", body, css)


def build_brasil():
    refs = [
      ("Anitta é a Dra. Nita", "Confirmado", "Rádio The Wipe", "A cantora dá voz à Dra. Nita, uma médica fictícia que apresenta o podcast <em>Ask Dr. Nita</em> na estação de podcasts The Wipe. É humor adulto e satírico, no estilo das rádios de GTA. A personagem só aparece em áudio: não dá pra encontrar a Dra. Nita andando por Leonida. A escalação foi confirmada por Ivan Pavlovich, vice-presidente de música da Rockstar.", "gameoverdrive"),
      ("“Touch & Go”, da Anitta, é a vinheta do programa", "Confirmado", "Rádio The Wipe", "A versão em inglês de “Vai Dar Caô” abre cada episódio do <em>Ask Dr. Nita</em>.", "gameoverdrive"),
      ("Barbie Ferreira participa de um episódio", "Confirmado", "Rádio The Wipe", "A atriz, filha de mãe brasileira e com cidadania brasileira, é convidada de um dos episódios do podcast da Dra. Nita.", "gameoverdrive"),
      ("Sepultura toca na rádio de metal", "Confirmado", "The Chamber 106.6", "“Territory”, do disco <em>Chaos A.D.</em> (1993), está na playlist da estação de metal.", "gameoverdrive"),
      ("Azymuth no jazz de Leonida", "Confirmado", "Leonida Jazz Radio", "A faixa-título do disco <em>Águia Não Come Mosca</em> (1977), do trio carioca, toca na rádio de jazz.", "gameoverdrive"),
      ("Cristina Camargo logo no começo do jogo", "Confirmado", "Worldwide FM", "Uma edição de “Moral Tem Hora”, música de 1980, feita pelo produtor Ray Mang, toca na Worldwide FM. Ela aparece cedo, numa cena do Jason na academia.", "gameoverdrive"),
      ("“Brasil da Capoeira”, de Feijão & Samtheman", "A confirmar", "Worldwide FM", "Jogadores dizem ter ouvido a música na Worldwide FM, mas ainda não há confirmação oficial da lista de faixas.", "gameoverdrive"),
      ("A pistola Nipper .38 “Made in Brazil”", "Em parte", "Capa oficial", "Na arte oficial divulgada em junho, a Lucia segura uma pistola com a gravação “Made in Brazil”. Fãs apontam a Taurus, fabricante de São Leopoldo (RS), como inspiração, mas a Rockstar não comentou. No jogo a Nipper .38 existe como pistola compacta, mas ainda não se confirmou se a gravação aparece no modelo.", "canaltech2"),
      ("Legendas e menus em português do Brasil", "Confirmado", "Idioma", "O português do Brasil é um dos 13 idiomas do jogo, nas legendas, nos menus e na interface. As vozes são só em inglês, sem dublagem.", "gameoverdrive"),
    ]
    SRC = {"gameoverdrive": ("Game Overdrive", "https://gameoverdrive.com.br/gta-6-referencias-brasil/"), "canaltech2": ("Canaltech", "https://canaltech.com.br/games/nova-imagem-de-gta-6-esconde-referencia-ao-brasil/"), "canaltech": ("Canaltech", "https://canaltech.com.br/games/referencias-ao-brasil-em-gta/")}
    col = {"Confirmado": "var(--teal)", "A confirmar": "var(--yellow)", "Em parte": "var(--orange)"}
    items = ""
    for i, (t, st, onde, txt, src) in enumerate(refs, 1):
        n, u = SRC[src]
        items += f'<div class="ref"><div class="num">{i}</div><div><h3>{e_(t)}</h3><div class="tags"><span style="border-color:{col[st]};color:{col[st]}">{st}</span><span>{e_(onde)}</span></div><p>{txt}</p><p class="src">Fonte: <a href="{u}" target="_blank" rel="noopener">{n}</a></p></div></div>'
    body = f"""<h1>Referências ao Brasil no GTA 6 🇧🇷</h1>
<p class="upd">Atualizado em {br(SITE["updated"])}</p>
<p>O Brasil aparece em GTA 6 mais do que muita gente esperava: tem Anitta comandando um programa de rádio, Sepultura e Azymuth nas estações, uma pistola “Made in Brazil” na capa e o jogo inteiro legendado em português. Reunimos aqui todas as referências encontradas até agora, separando o que já foi confirmado do que ainda está em dúvida.</p>
<h2>As {len(refs)} referências encontradas até agora</h2>
<div class="refs">{items}</div>
<h2>Não é a primeira vez</h2>
<p>A Rockstar coloca o Brasil nos seus jogos há muito tempo. Todos os GTAs desde o III têm alguma referência ao país, como a clínica de depilação brasileira de San Fierro, em San Andreas, e a gangue de brasileiros que fala português pelas ruas de Liberty City, em GTA IV (<a href="{SRC['canaltech'][1]}" target="_blank" rel="noopener">Canaltech</a>). Fora da série GTA, Max Payne 3 se passa quase todo em São Paulo.</p>
<h2>Achou mais alguma?</h2>
<p>Viu uma placa, um NPC falando português ou uma música brasileira que não está aqui? <a href="index.html#enviar">Manda pra gente</a> e o crédito é seu.</p>"""
    css = ".refs{display:grid;gap:12px}.ref{display:flex;gap:16px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px}.ref .num{flex:0 0 40px;height:40px;border-radius:50%;background:linear-gradient(135deg,#009c3b,#ffdf00);color:#0f0b1a;font-weight:800;display:flex;align-items:center;justify-content:center}.ref h3{font-size:18px;margin-bottom:6px}.ref .tags{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px}.ref .tags span{border:1px solid var(--line);border-radius:20px;padding:2px 10px;font-size:12px;color:var(--muted)}.ref p{font-size:15px;margin-bottom:6px}.ref .src{font-size:13px;color:var(--muted)}"
    simple_page("brasil", "Referências ao Brasil no GTA 6: Anitta, Sepultura e mais – Easter Eggs GTA 6", "Todas as referências ao Brasil em GTA 6: Anitta como Dra. Nita, Sepultura, Azymuth e Cristina Camargo nas rádios, a pistola Made in Brazil e o jogo em português.", body, css)

TROFEUS = [
    # (nome, grau, como desbloquear em PT, dica/nota, dif 1-3)
    ("Vice Got a Price!", "Platina", "Desbloqueie todos os outros troféus. No Xbox, vale a conquista Mítica.", "É o prêmio final. Só falta ele quando todo o resto estiver feito.", 3),
    ("A Long Road", "Ouro", "Chegue a 100% de conclusão do jogo.", "O mais demorado da lista. Deixe pro fim, porque muitos outros troféus contam pro 100%.", 3),
    ("Cunning Stunts", "Prata", "Faça 250 manobras (stunts).", "Pulos de rampa e manobras com moto contam. Vá fazendo aos poucos enquanto explora.", 3),
    ("The Shootist", "Prata", "Tire medalha de ouro em todos os desafios do estande de tiro (42, segundo o AlcastHQ).", "Atenção: as medalhas liberam códigos de munição. Cheats ativos desligam troféus na sessão, então não use enquanto estiver caçando troféu.", 3),
    ("Strangers & Freaks", "Prata", "Termine 8 linhas de missões de Estranhos.", "As missões de Estranhos aparecem pelo mapa ao longo da história.", 2),
    ("Don't Touch My Deck", "Prata", "Complete 3 coleções de cartas colecionáveis.", "Vá pegando as cartas enquanto explora Leonida.", 2),
    ("You WAiNKer!", "Prata", "Use o WAiNK em 100 locais diferentes.", "Combina bem com o troféu de explorar o mapa.", 2),
    ("Maximum Withdrawal", "Prata", "Roube 5 cofres de banco e fuja em todos.", "Salve antes de cada assalto, porque precisa escapar em todos.", 3),
    ("Master of None", "Bronze", "Experimente cada tipo de atividade pelo menos uma vez (9, segundo o AlcastHQ).", "Golfe, sinuca, pesca, academia e afins. Um de cada já basta.", 1),
    ("Top Fun", "Bronze", "Vença uma corrida de drone em todos os locais da Top Fun (14, segundo o AlcastHQ).", "A loja Top Fun Drones fica em Vice Beach.", 2),
    ("Earn Cash, Not Kudos", "Bronze", "Vença 20 corridas diferentes.", "Tem que ser 20 corridas diferentes, não a mesma 20 vezes.", 2),
    ("Baited My Tackle", "Bronze", "Vença o Cal num desafio de pesca.", "Fácil e rápido quando a pesca estiver liberada.", 1),
    ("Stick Fiddler", "Bronze", "Termine um jogo de fliperama.", "Qualquer jogo de arcade serve.", 1),
    ("Positive Mental Attitude", "Bronze", "Medite em todos os pontos de meditação (18, segundo o AlcastHQ).", "Os pontos ficam espalhados pelo mapa. Vá marcando conforme encontra.", 2),
    ("One Last Thing", "Bronze", "Complete 50 desafios.", "Sai naturalmente jogando o resto.", 1),
    ("Hot Together", "Bronze", "Chegue a 4 estrelas de procurado junto com seu parceiro e despiste a polícia.", "Precisa estar com o parceiro no momento.", 2),
    ("Retail Therapy", "Bronze", "Roube 3 lojas seguidas com o parceiro sem perder o nível de procurado.", "Tenha as 3 lojas planejadas, perto umas das outras.", 2),
    ("Whip It Good", "Bronze", "Descubra 100 veículos.", "Dirigir veículos diferentes pelo mapa já conta. Os carros raros do site ajudam.", 1),
    ("Gunslinger", "Bronze", "Derrube 5 inimigos durante um único uso do Foco de Combate.", "Use o Foco num tiroteio com vários inimigos juntos.", 1),
    ("Sneakthief", "Bronze", "Roube uma joalheria sem ser detectado.", "Salve antes de tentar.", 2),
    ("A Classic Blitz Play", "Bronze", "Roube um carro-forte e fuja.", "", 1),
    ("The Goodtime State", "Bronze", "Explore Leonida inteira, revelando todas as regiões do mapa.", "Use o nosso mapa interativo pra não deixar nenhuma região pra trás.", 2),
    ("Pest Control", "Bronze", "Roube uma operação ilegal de cada gangue (9, segundo o AlcastHQ).", "", 2),
    ("Dime on the Dollar", "Bronze", "Lave US$ 250.000 em notas marcadas.", "", 2),
    ("Treat Yo Self", "Bronze", "Gaste US$ 100.000 somando todas as lojas.", "Roupas, armas e tunagem contam.", 1),
    ("Little Boxes", "Bronze", "Compre todas as garagens (8, segundo o AlcastHQ).", "", 2),
    ("On the Spot", "Bronze", "Registre 10 veículos no app da Scooter Bros.", "", 1),
]

GRAU_COR = {"Platina": "#b9e6ff", "Ouro": "#ffd23f", "Prata": "#cfd6e6", "Bronze": "#d08a52"}


def build_trofeus():
    rows = ""
    for i, (n, g, how, tip, d) in enumerate(TROFEUS):
        tid = "t" + str(i)
        dots = "".join('<i style="background:' + (DIFC[["Fácil", "Médio", "Difícil"][d - 1]] if k < d else "#3a2f5c") + '"></i>' for k in range(3))
        rows += ('<li class="tr" data-t="' + tid + '"><button type="button" class="tbox" aria-pressed="false" aria-label="Marcar ' + e_(n) + '"></button>'
                 '<div><div class="th"><b>' + e_(n) + '</b><span class="tg2" style="color:' + GRAU_COR[g] + ';border-color:' + GRAU_COR[g] + '">' + g + '</span>'
                 '<span class="dif"><b class="dots">' + dots + '</b>' + ["Fácil", "Médio", "Difícil"][d - 1] + '</span></div>'
                 '<p>' + e_(how) + '</p>' + ('<p class="tip">💡 ' + e_(tip) + '</p>' if tip else '') + '</div></li>')
    body = f"""<h1>Troféus e conquistas de GTA 6: lista e guia do 100%</h1>
<p class="upd">Atualizado em {br(SITE["updated"])}</p>
<p>GTA 6 tem <strong>55 troféus</strong>: 1 de platina, 2 de ouro, 6 de prata e 46 de bronze. No Xbox são 55 conquistas que somam 1.000 de Gamerscore, e no lugar da platina tem a nova conquista Mítica. A lista é igual no PS5 e no Xbox, e tudo se faz no modo história, sem precisar jogar online.</p>
<div class="aviso"><strong>Sem spoilers:</strong> 28 dos 55 troféus são ocultos e ligados à história. Eles saem naturalmente ao terminar as missões, então não listamos os nomes. Abaixo estão os <strong>27 troféus visíveis</strong>, com o que fazer pra conseguir cada um.</div>
<div class="tprog"><b id="tN">0</b> de {len(TROFEUS)} troféus visíveis marcados<div class="mpbar"><i id="tBar"></i></div></div>
<h2>Os 27 troféus visíveis</h2>
<ul class="trs">{rows}</ul>
<p class="tsm">Os nomes dos troféus estão em inglês, como aparecem no jogo. As explicações são nossas e foram montadas com base nas listas do AlcastHQ e do Of Zen and Computing. As quantidades marcadas com "segundo o AlcastHQ" ainda não aparecem em outras fontes.</p>
<h2>Os mais difíceis</h2>
<p>Os que mais tomam tempo são <strong>A Long Road</strong> (100% de conclusão), <strong>The Shootist</strong> (ouro em todos os desafios de tiro), <strong>Cunning Stunts</strong> (250 manobras), <strong>You WAiNKer!</strong> (100 locais de WAiNK) e <strong>Maximum Withdrawal</strong> (5 cofres de banco sem ser pego).</p>
<h2>Ordem que economiza tempo</h2>
<ol>
<li>Termine a história. Os troféus ocultos saem nesse caminho.</li>
<li>Termine as missões finais dos personagens secundários e as missões de Estranhos.</li>
<li>Explore o mapa: medite em todos os pontos e use o WAiNK nos 100 locais. Nosso <a href="mapa.html">mapa interativo</a> ajuda.</li>
<li>Corridas, drones e manobras.</li>
<li>Estande de tiro e fliperama.</li>
<li>Os assaltos: lojas, joalheria, carro-forte, cofres e operações das gangues.</li>
<li>Colecionáveis, garagens, veículos e compras.</li>
<li>Desafios que faltarem, lavagem de dinheiro e, por fim, o 100%.</li>
</ol>
<h2>Perguntas rápidas</h2>
<p><strong>Quanto tempo leva a platina?</strong> As estimativas giram em torno de 200 horas. Só a história leva de 50 a 80 horas, dependendo do ritmo.</p>
<p><strong>Códigos (cheats) desligam troféus?</strong> Sim. Com um código ativo, os troféus ficam desligados naquela sessão. Veja os <a href="codigos.html">códigos de GTA 6</a> e use só num save separado.</p>
<p><strong>Tem troféu perdível?</strong> Até agora, a comunidade não encontrou nenhum, mas isso ainda não foi confirmado. Por segurança, faça um save manual antes de missões que só acontecem uma vez.</p>
<p class="tsm">Fontes: <a href="https://alcasthq.com/?p=87554" target="_blank" rel="noopener">AlcastHQ</a>, <a href="https://www.ofzenandcomputing.com/gta-6-trophy-list-trophies-achievements/" target="_blank" rel="noopener">Of Zen and Computing</a>, <a href="https://www.gtabase.com/gta-6/achievements" target="_blank" rel="noopener">GTABase</a>.</p>"""
    css = (".trs{list-style:none;display:grid;gap:10px;padding:0}.tr{display:flex;gap:14px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px}"
           ".tr.on{border-color:var(--teal);opacity:.75}.tbox{flex:0 0 26px;height:26px;border-radius:8px;border:2px solid var(--line);background:transparent;cursor:pointer;margin-top:2px}"
           ".tr.on .tbox{background:var(--teal);border-color:var(--teal)}.tr.on .tbox::after{content:'✓';color:#0f0b1a;font-weight:800}"
           ".th{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:center;margin-bottom:4px}.th b{font-size:17px}.tg2{border:1px solid;border-radius:20px;padding:1px 9px;font-size:12px;font-weight:700}"
           ".tr p{font-size:15px;margin-bottom:4px}.tr .tip{color:var(--muted);font-size:14px}.tsm{font-size:13px;color:var(--muted)}"
           ".tprog{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin:16px 0;font-size:14px;color:var(--muted)}.tprog b{color:var(--text)}"
           ".mpbar{height:8px;background:#2a2142;border-radius:6px;overflow:hidden;margin-top:8px}.mpbar i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--pink),var(--orange),var(--yellow));transition:width .3s}"
           ".aviso{background:#1d1630;border:1px solid #2e2547;border-left:4px solid var(--yellow);border-radius:12px;padding:14px 16px;margin:18px 0 6px;font-size:15px;color:#d9d0ea}"
           ".dif{display:inline-flex;align-items:center;gap:6px;font-size:12px;color:var(--muted)}.dif .dots{display:inline-flex;gap:3px}.dif .dots i{width:6px;height:12px;border-radius:2px;display:block}")
    js = """<script>(function(){var K="trofeus-gta6",s;try{s=new Set(JSON.parse(localStorage.getItem(K)||"[]"))}catch(_){s=new Set()}
var L=[].slice.call(document.querySelectorAll(".tr"));function p(){L.forEach(function(li){var on=s.has(li.dataset.t);li.classList.toggle("on",on);li.querySelector(".tbox").setAttribute("aria-pressed",on)});
document.getElementById("tN").textContent=s.size;document.getElementById("tBar").style.width=Math.round(s.size/L.length*100)+"%"}
L.forEach(function(li){li.querySelector(".tbox").addEventListener("click",function(){var t=li.dataset.t;s.has(t)?s.delete(t):s.add(t);try{localStorage.setItem(K,JSON.stringify(Array.from(s)))}catch(_){}p()})});p()})();</script>"""
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": "Quantos troféus tem GTA 6?", "acceptedAnswer": {"@type": "Answer", "text": "GTA 6 tem 55 troféus: 1 de platina, 2 de ouro, 6 de prata e 46 de bronze. No Xbox são 55 conquistas que somam 1.000 de Gamerscore."}},
        {"@type": "Question", "name": "Quanto tempo leva a platina de GTA 6?", "acceptedAnswer": {"@type": "Answer", "text": "As estimativas giram em torno de 200 horas. Só a história leva de 50 a 80 horas."}},
        {"@type": "Question", "name": "Cheats desligam troféus em GTA 6?", "acceptedAnswer": {"@type": "Answer", "text": "Sim. Com um código ativo, os troféus ficam desligados naquela sessão."}}]}
    simple_page("trofeus", "Troféus de GTA 6: lista completa e guia da platina – Easter Eggs GTA 6",
                "Todos os 27 troféus visíveis de GTA 6 explicados em português, com checklist, os mais difíceis, a melhor ordem pra platina e se cheats desligam troféus.",
                body + js, css, '<script type="application/ld+json">' + json.dumps(faq, ensure_ascii=False) + '</script>\n')


def build_guia_compra():
    S = {x["id"]: x for x in D.get("setup", [])}
    def btn(i, txt):
        return ('<a class="btn-ml" href="' + e_(S[i]["link"]) + '" target="_blank" rel="sponsored nofollow noopener">' + txt + '</a>') if i in S else ""
    body = f"""<h1>Guia de compra de GTA 6: edições, preço, tamanho e qual console</h1>
<p class="upd">Atualizado em {br(SITE["updated"])}</p>
<p>Vai comprar GTA 6 e está em dúvida sobre edição, console ou espaço livre? Aqui está o resumo do que já foi confirmado, sem enrolação.</p>
<div class="aviso"><strong>Transparência:</strong> alguns botões desta página são links de afiliado do Mercado Livre. Se você comprar por eles, o site ganha uma pequena comissão, sem custo a mais pra você.</div>

<h2>Standard ou Ultimate?</h2>
<table class="gt"><tr><th></th><th>Standard</th><th>Ultimate</th></tr>
<tr><td>Preço nas lojas digitais do Brasil</td><td><b>R$ 449,90</b></td><td><b>R$ 549,90</b></td></tr>
<tr><td>Jogo completo</td><td>✓</td><td>✓</td></tr>
<tr><td>Conteúdo extra (veículos, armas, roupas e locais liberados ao longo da história)</td><td>—</td><td>✓</td></tr>
<tr><td>Dá pra subir de edição depois?</td><td colspan="2">Sim: o pacote de melhoria custa R$ 100, a diferença exata entre as duas</td></tr></table>
<p><strong>Resumindo:</strong> a Standard já tem o jogo inteiro. A Ultimate só acrescenta extras cosméticos e de conveniência. Se o orçamento estiver apertado, vá de Standard: dá pra pegar a melhoria depois, sem perder nada.</p>
<p class="tsm">Preços oficiais nas lojas digitais do PlayStation e do Xbox, segundo Omelete, Canaltech e TecMundo. Em promoções e no varejo o preço pode ser menor.</p>

<h2>Caixa ou digital?</h2>
<p>A versão "física" de GTA 6 <strong>não vem com disco</strong>: a caixa traz um código de download. Na prática, ela funciona igual à digital, até nos consoles sem leitor de disco, como o PS5 Slim Digital e o Xbox Series S. A vantagem da caixa é que dá pra dar de presente ou comprar no varejo quando estiver mais barata.</p>
<div class="bts">{btn("gta6-ps5", "Ver GTA 6 de PS5 no Mercado Livre →")}{btn("gta6-xbox", "Ver GTA 6 de Xbox no Mercado Livre →")}</div>

<h2>Quanto espaço precisa?</h2>
<p>A Rockstar pede <strong>até 212 GB livres</strong>, dependendo do console. No PS5, o download ficou em cerca de 210 GB. Libere espaço antes de baixar. Se o armazenamento do console estiver cheio, um HD externo ajuda a guardar outros jogos, mas o GTA 6 precisa ficar no armazenamento interno (ou num SSD interno compatível) pra rodar.</p>
<div class="bts">{btn("ssd", "Ver HD externo no Mercado Livre →")}</div>

<h2>Qual console roda melhor?</h2>
<table class="gt"><tr><th>Console</th><th>Taxa de quadros</th><th>Observação</th></tr>
<tr><td>PS5 Pro</td><td>30 fps</td><td>Imagem mais nítida, sombras com ray tracing e carregamento mais rápido</td></tr>
<tr><td>PS5</td><td>30 fps</td><td>Estável na maior parte do tempo</td></tr>
<tr><td>Xbox Series X</td><td>30 fps</td><td>Muito parecido com o PS5, com quedas leves em tiroteios pesados</td></tr>
<tr><td>Xbox Series S</td><td>30 fps</td><td>Resolução bem menor e mais quedas de desempenho</td></tr></table>
<p><strong>Não existe modo de 60 fps</strong>, nem no PS5 Pro. A Rockstar confirmou 30 fps em todos os consoles. Ela não descartou novos modos no futuro, mas também não prometeu nada.</p>
<p><strong>No Xbox One:</strong> dá pra jogar pela nuvem, com o Xbox Cloud Gaming, que usa as configurações do Series S.</p>
<p><strong>Resumindo:</strong> quem já tem PS5 ou Series X está bem servido. O Series S roda, mas é a versão mais fraca. O PS5 Pro deixa a imagem mais bonita, mas não aumenta o fps.</p>
<div class="bts">{btn("ps5", "Ver PS5 no Mercado Livre →")}{btn("xbox-x", "Ver Xbox Series X →")}{btn("xbox-s", "Ver Xbox Series S →")}</div>

<h2>Vale comprar mais alguma coisa?</h2>
<p>Um <strong>controle extra</strong> ajuda quando a bateria acaba no meio de uma missão. Um <strong>headset</strong> faz diferença nas rádios e nos diálogos. E o <strong>cartão-presente</strong> da PlayStation Store é uma boa pra quem prefere comprar digital. Separamos tudo na página <a href="setup.html">Monte seu setup</a>.</p>
<p class="tsm">Fontes: preços — <a href="https://www.omelete.com.br/games/gta-6-preco-brasil" target="_blank" rel="noopener">Omelete</a> e <a href="https://canaltech.com.br/games/e-assalto-no-jogo-e-no-bolso-preco-salgado-de-gta-6-no-brasil-espanta/" target="_blank" rel="noopener">Canaltech</a>; desempenho e tamanho — <a href="https://notebookcheck.net/Rockstar-reveals-GTA-6-console-performance-targets-and-PS5-Pro-upgrades.1447121.0.html" target="_blank" rel="noopener">Notebookcheck</a>, <a href="https://www.ggrecon.com/articles/gta-6-30fps-ps5-pro-xbox-cloud/" target="_blank" rel="noopener">GGRecon</a> e a análise da Digital Foundry resumida pelo <a href="https://gmtreks.com/gta6/page/01M7QVBT1ZQGN5PHM4ZJGM7ZHS" target="_blank" rel="noopener">GameTrek</a>.</p>"""
    css = (".gt{width:100%;border-collapse:collapse;margin:10px 0 12px;font-size:15px}.gt th,.gt td{border:1px solid var(--line);padding:9px 10px;text-align:left;vertical-align:top}"
           ".gt th{background:var(--card)}.gt td:first-child{color:#d9d0ea}.bts{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0 10px}.tsm{font-size:13px;color:var(--muted)}"
           ".btn-ml{display:inline-block;background:#ffe600;color:#1a1a1a!important;font-weight:700;text-decoration:none;border-radius:10px;padding:9px 14px;font-size:14px}"
           ".aviso{background:#1d1630;border:1px solid #2e2547;border-left:4px solid var(--yellow);border-radius:12px;padding:14px 16px;margin:18px 0 6px;font-size:15px;color:#d9d0ea}")
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": "Quanto custa GTA 6 no Brasil?", "acceptedAnswer": {"@type": "Answer", "text": "Nas lojas digitais do PS5 e do Xbox, a edição Standard custa R$ 449,90 e a Ultimate custa R$ 549,90."}},
        {"@type": "Question", "name": "Quanto espaço GTA 6 ocupa?", "acceptedAnswer": {"@type": "Answer", "text": "A Rockstar pede até 212 GB livres, dependendo do console. No PS5 o download ficou em cerca de 210 GB."}},
        {"@type": "Question", "name": "GTA 6 roda a 60 fps?", "acceptedAnswer": {"@type": "Answer", "text": "Não. GTA 6 roda a 30 fps em todos os consoles, incluindo o PS5 Pro."}},
        {"@type": "Question", "name": "A versão física de GTA 6 tem disco?", "acceptedAnswer": {"@type": "Answer", "text": "Não. A caixa traz um código de download, então funciona também em consoles sem leitor de disco."}}]}
    simple_page("guia-de-compra", "Guia de compra de GTA 6: Standard ou Ultimate, preço, tamanho e 60 fps – Easter Eggs GTA 6",
                "Standard ou Ultimate? Caixa ou digital? Quanto espaço precisa e qual console roda melhor? Tudo o que você precisa saber antes de comprar GTA 6.",
                body, css, '<script type="application/ld+json">' + json.dumps(faq, ensure_ascii=False) + '</script>\n')


def main():
    if OUT.exists(): shutil.rmtree(OUT)
    (OUT / "easter-eggs").mkdir(parents=True); (OUT / "assets").mkdir(); (OUT / "img").mkdir()
    (OUT / "img" / "LEIA-ME.txt").write_text("Coloque aqui os prints autorizados (ex.: ovo-na-torre.jpg).\n", encoding="utf-8")
    (OUT / "assets" / "style.css").write_text((ROOT / "base.css").read_text(encoding="utf-8") + EXTRA_CSS, encoding="utf-8")
    shutil.copy(ROOT / "app.js", OUT / "assets" / "app.js")
    build_index()
    build_map()
    build_404()
    build_static_pages()
    build_codes()
    build_cars()
    build_setup()
    build_brasil()
    build_trofeus()
    build_guia_compra()
    try:
        build_og()
        shutil.copy(OUT / "og.png", ROOT / "vendor" / "og.png")
    except Exception as ex:
        print("aviso: og.png não gerado (" + str(ex)[:80] + "), usando a cópia salva")
        if (ROOT / "vendor" / "og.png").exists(): shutil.copy(ROOT / "vendor" / "og.png", OUT / "og.png")
    build_crops()
    for f in ['favicon.ico','favicon.svg','apple-touch-icon.png','icon-192.png']: shutil.copy(ROOT/'vendor'/'icons'/f, OUT/f)
    shutil.copy(ROOT / 'vendor' / 'leaflet.js', OUT / 'assets' / 'leaflet.js')
    shutil.copy(ROOT / 'vendor' / 'leaflet.css', OUT / 'assets' / 'leaflet.css')
    shutil.copy(ROOT / 'vendor' / 'mapa-leonida.jpg', OUT / 'img' / 'mapa-leonida.jpg')
    shutil.copytree(ROOT / 'vendor' / 'produtos', OUT / 'img' / 'produtos')
    (OUT / 'img' / 'art').mkdir(parents=True, exist_ok=True)
    for f in (ROOT / 'art').glob('*.svg'): shutil.copy(f, OUT / 'img' / 'art' / f.name)
    if FOTOS_ON: shutil.copytree(ROOT / 'vendor' / 'fotos', OUT / 'img' / 'fotos', dirs_exist_ok=True)
    for e in EGGS: build_egg(e)
    base = SITE["url"].rstrip("/")
    urls = [base + "/", base + "/mapa.html", base + "/codigos.html", base + "/carros.html", base + "/setup.html", base + "/brasil.html", base + "/trofeus.html", base + "/guia-de-compra.html", base + "/sobre.html", base + "/contato.html", base + "/privacidade.html"] + [f'{base}/carros/{c["id"]}.html' for c in D["cars"]] + [f'{base}/easter-eggs/{e["id"]}.html' for e in EGGS]
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"  <url><loc>{u}</loc><lastmod>{SITE['updated']}</lastmod></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    (OUT / "ads.txt").write_text("google.com, " + SITE["adsense"].replace("ca-", "") + ", DIRECT, f08c47fec0942fa0\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n", encoding="utf-8")
    print("ok:", len(EGGS), "páginas de easter egg")

main()
