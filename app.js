/* Easter Eggs GTA 6: checklist, filtros, compartilhar e formulário */
(function () {
  var KEY = "ovos-achados";
  var found = new Set();
  try { found = new Set(JSON.parse(localStorage.getItem(KEY) || "[]")); } catch (_) {}
  function save() { try { localStorage.setItem(KEY, JSON.stringify(Array.from(found))); } catch (_) {} }
  var $ = function (s) { return document.querySelector(s); };
  var $$ = function (s) { return Array.prototype.slice.call(document.querySelectorAll(s)); };

  function paintChk(b) {
    var on = found.has(b.dataset.chk);
    b.classList.toggle("on", on);
    b.setAttribute("aria-pressed", on);
    b.innerHTML = '<span class="box">' + (on ? "✓" : "") + "</span>" + (on ? "Já achei" : "Marcar como achado");
    var c = b.closest(".card");
    if (c) c.classList.toggle("found", on);
  }
  function progress() {
    var p = $("#pN"); if (!p) return;
    var ids = $$(".card").map(function (c) { return c.dataset.id; });
    var n = ids.filter(function (i) { return found.has(i); }).length;
    p.textContent = n; $("#pT").textContent = ids.length;
    $("#pBar").style.width = (ids.length ? n / ids.length * 100 : 0) + "%";
    var r = $("#reset"); r.hidden = n === 0; r.classList.remove("warn"); r.textContent = "Zerar";
  }

  var cat = "all", status = "all", q = "";
  function norm(s) { return s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase(); }
  function filter() {
    if (!$("#grid")) return;
    var n = 0, nq = norm(q), cards = $$(".card");
    cards.forEach(function (c) {
      var ok = c.dataset.ok === "1";
      var st = status === "all" ||
        (status === "todo" ? !found.has(c.dataset.id) :
         status === "new" ? c.dataset.new === "1" :
         (status === "ok") === ok);
      var show = (cat === "all" || c.dataset.cat === cat) && st && (!nq || norm(c.textContent).indexOf(nq) > -1);
      c.hidden = !show; if (show) n++;
    });
    $("#count").textContent = n + " de " + cards.length + " easter eggs";
    var em = $("#empty"); em.hidden = n > 0;
    em.textContent = status === "todo" && !q ? "Você já achou todos! Volte amanhã pra ver os novos." : "Nada encontrado. Tenta outra palavra.";
    $$("[data-c]").forEach(function (b) { b.classList.toggle("on", b.dataset.c === cat); });
    $$("[data-s]").forEach(function (b) { b.classList.toggle("on", b.dataset.s === status); });
  }
  function paintAll() { $$("[data-chk]").forEach(paintChk); progress(); filter(); }

  document.addEventListener("click", function (ev) {
    var t = ev.target;
    var k = t.closest("[data-chk]");
    if (k) { ev.preventDefault(); var id = k.dataset.chk; found.has(id) ? found.delete(id) : found.add(id); save(); paintAll(); return; }
    if (t.id === "reset") {
      if (t.classList.contains("warn")) { found.clear(); save(); paintAll(); }
      else { t.classList.add("warn"); t.textContent = "Tem certeza? Clique de novo"; setTimeout(progress, 4000); }
      return;
    }
    var c = t.closest("[data-c]"); if (c) { cat = c.dataset.c; filter(); return; }
    var s = t.closest("[data-s]"); if (s) { status = s.dataset.s; filter(); return; }
    var cp = t.closest("[data-copy]");
    if (cp) {
      var url = location.href.split("#")[0];
      try { navigator.clipboard.writeText(url).then(function () { cp.textContent = "Link copiado!"; }, function () { cp.textContent = url; }); }
      catch (_) { cp.textContent = url; }
    }
  });
  var qi = $("#q");
  if (qi) {
    qi.addEventListener("input", function (e) { q = e.target.value; filter(); });
    try { var pq = new URLSearchParams(location.search).get("q"); if (pq) { qi.value = pq; q = pq; setTimeout(function () { var l = $("#lista"); if (l) l.scrollIntoView(); }, 50); } } catch (_) {}
  }

  $$("[data-share]").forEach(function (a) {
    var u = encodeURIComponent(location.href.split("#")[0]);
    var txt = encodeURIComponent(a.dataset.text || document.title);
    a.href = a.dataset.share === "wa" ? "https://wa.me/?text=" + txt + "%20" + u
                                      : "https://twitter.com/intent/tweet?text=" + txt + "&url=" + u;
  });

  /* Vídeo do YouTube: só carrega quando a pessoa clica (mais rápido e sem cookies antes do clique) */
  function playYt(el) {
    if (el.querySelector("iframe")) return;
    var f = document.createElement("iframe");
    f.src = "https://www.youtube-nocookie.com/embed/" + encodeURIComponent(el.dataset.yt) + "?autoplay=1&rel=0";
    f.title = "Vídeo do YouTube"; f.allow = "accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; fullscreen";
    f.allowFullscreen = true; el.innerHTML = ""; el.appendChild(f);
  }
  document.addEventListener("click", function (ev) { var y = ev.target.closest(".yt"); if (y) playYt(y); });
  document.addEventListener("keydown", function (ev) { var y = ev.target.closest && ev.target.closest(".yt"); if (y && (ev.key === "Enter" || ev.key === " ")) { ev.preventDefault(); playYt(y); } });

  /* Formulários: as mensagens chegam no e-mail via FormSubmit, com tela de confirmação */
  document.querySelectorAll("form.send").forEach(function (f) {
    var btn = f.querySelector("button[type=submit]"), label = btn.textContent;
    var msg = f.querySelector(".fmsg");
    var isContato = f.name === "contato";
    f.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var fd = new FormData(f);
      if (fd.get("bot-field")) return;
      fd.delete("bot-field"); fd.delete("form-name");
      var data = {}; fd.forEach(function (v, k) { data[k] = v; });
      if (data.link && !/^https?:\/\//i.test(data.link)) data.link = "https://" + data.link;
      data._subject = isContato ? "Contato pelo site" : "Nova descoberta enviada pelo site";
      data._template = "table";
      btn.disabled = true; btn.textContent = "Enviando…"; msg.textContent = ""; msg.className = "fmsg";
      fetch("https://formsubmit.co/ajax/7330d6841b2569056867314f774fa7e5", { method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify(data) })
        .then(function (r) { return r.json().then(function (j) { if (!r.ok || String(j.success) !== "true") throw 0; }); })
        .then(function () {
          f.reset(); f.style.display = "none";
          var done = document.createElement("div"); done.className = "fdone"; done.setAttribute("role", "status");
          done.innerHTML = '<div class="ck">✓</div><h3>' + (isContato ? "Mensagem enviada!" : "Descoberta enviada!") + '</h3><p>' +
            (isContato ? "Valeu pelo contato. A gente responde pelo e-mail assim que possível." : "Valeu! A gente vai conferir. Se for publicada, seu nome entra nos créditos.") +
            '</p><button class="btn" type="button">' + (isContato ? "Mandar outra mensagem" : "Mandar outra descoberta") + '</button>';
          f.parentNode.insertBefore(done, f.nextSibling);
          done.scrollIntoView({ behavior: "smooth", block: "center" });
          done.querySelector("button").addEventListener("click", function () { done.remove(); f.style.display = ""; });
        })
        .catch(function () { msg.textContent = "Não deu pra enviar agora. Tenta de novo em alguns minutos ou manda pelo e-mail eastereggsgta6@gmail.com."; msg.className = "fmsg err"; })
        .then(function () { btn.disabled = false; btn.textContent = label; });
    });
  });


  /* Comentários próprios (Cloudflare D1 + Turnstile) */
  document.querySelectorAll(".cmts").forEach(function (box) {
    var page = box.getAttribute("data-page"), list = box.querySelector(".cmt-list"), f = box.querySelector(".cmt-form"), msg = f.querySelector(".fmsg"), btn = f.querySelector("button[type=submit]");
    var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
    function fmt(d) { try { return new Date(d).toLocaleDateString("pt-BR", { day: "2-digit", month: "short", year: "numeric" }); } catch (_) { return ""; } }
    fetch("/api/comments?page=" + encodeURIComponent(page)).then(function (r) { return r.json(); }).then(function (j) {
      var c = j.comments || [];
      list.innerHTML = c.length ? c.map(function (x) { return '<div class="cmt"><div class="cmt-h"><b>' + esc(x.name) + '</b><time>' + fmt(x.created) + '</time></div><p>' + esc(x.text) + '</p></div>'; }).join("") : '<p class="cmt-empty">Ninguém comentou ainda. Seja o primeiro!</p>';
    }).catch(function () { list.innerHTML = '<p class="cmt-empty">Não deu pra carregar os comentários agora.</p>'; });
    f.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var fd = new FormData(f), name = (fd.get("name") || "").trim(), text = (fd.get("text") || "").trim();
      var token = fd.get("cf-turnstile-response") || "";
      if (name.length < 2 || text.length < 3) { msg.textContent = "Preencha o nome e o comentário."; msg.className = "fmsg err"; return; }
      if (!token) { msg.textContent = "Espere a verificação \"não sou um robô\" terminar e tente de novo."; msg.className = "fmsg err"; return; }
      btn.disabled = true; btn.textContent = "Enviando…"; msg.textContent = ""; msg.className = "fmsg";
      fetch("/api/comments", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ page: page, name: name, text: text, token: token, website: fd.get("website") || "" }) })
        .then(function (r) { return r.json().then(function (j) { if (!r.ok || !j.ok) throw new Error(j.error || ""); }); })
        .then(function () { f.reset(); msg.textContent = "✓ Comentário enviado! Ele aparece aqui assim que for aprovado."; msg.className = "fmsg okk"; })
        .catch(function (e) { msg.textContent = e.message || "Não deu pra enviar agora. Tente de novo."; msg.className = "fmsg err"; })
        .then(function () { btn.disabled = false; btn.textContent = "Enviar comentário"; try { window.turnstile && turnstile.reset(); } catch (_) {} });
    });
  });

  paintAll();
})();
