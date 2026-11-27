import json, collections
CATS = [  # (key, nome, cor, tags)
 ("esconderijo","Esconderijos","#ff3d8b",["#safehouse"]),
 ("armas","Armas (Ammu-Nation e afins)","#ff5e5e",["#guns"]),
 ("oficina","Oficinas e Pay 'n' Spray","#ff9a3c",["#modshop","#pay'n'spray","#carwash"]),
 ("posto","Postos de gasolina","#ffd23f",["#gas"]),
 ("loja","Lojas e mercados","#7cd67c",["#supermarket","#electronics","#vendor","#fence","#liquor","#pharmacy","#diamonds","retail","supermarket"]),
 ("visual","Roupas, cabelo e tatuagem","#c77dff",["#clothes","#hair","#tattoos","#shoes"]),
 ("comida","Bares e restaurantes","#ffb347",["#bar","#food","#fastfood","#drinks","restaurant","#nightclub"]),
 ("transporte","Aeroportos, marinas e estações","#5ac8fa",["#airport","#marina","#train","#bus","#metro","#metromover","#airbase","transportation"]),
 ("hotel","Hotéis e motéis","#f4a6c8",["hotel"]),
 ("lazer","Lazer e esportes","#2de2c8",["#tennis","#racetrack","#golf","leisure","events"]),
 ("publico","Polícia, hospitais e governo","#9aa7ff",["#police","#hospital","#jail","government","public"]),
 ("marco","Pontos turísticos e curiosidades","#ffffff",["#landmark","#curiosity","landmark","point-of-interest"]),
 ("natureza","Natureza","#3ddc84",["natural"]),
 ("outros","Outros lugares com nome","#a99cc4",[]),
]
SKIP_TAGS = {"#stripclub"}
TAGNAME = {"#gas":"Posto de gasolina","#supermarket":"Loja de conveniência","#guns":"Loja de armas","#modshop":"Oficina de tunagem","#pay'n'spray":"Pay 'n' Spray","#safehouse":"Esconderijo","#bar":"Bar","#food":"Restaurante","#fastfood":"Lanchonete","#clothes":"Loja de roupas","#hair":"Barbearia / salão","#tattoos":"Estúdio de tatuagem","#shoes":"Loja de sapatos","#airport":"Aeroporto / pista","#marina":"Marina","#train":"Estação de trem","#bus":"Ponto de ônibus","#metro":"Estação de metrô","#metromover":"Estação do Metromover","#police":"Delegacia","#hospital":"Hospital","#fence":"Receptador","#electronics":"Loja de eletrônicos","#landmark":"Ponto turístico","#curiosity":"Curiosidade","#tennis":"Quadra de tênis","#racetrack":"Pista de corrida","#vendor":"Vendedor","#carwash":"Lava-rápido","#nightclub":"Boate","#drinks":"Bebidas","#jail":"Prisão","#golf":"Golfe","#liquor":"Loja de bebidas","#pharmacy":"Farmácia","#diamonds":"Joalheria","#airbase":"Base aérea","#blimp":"Dirigível"}
d = json.load(open("vendor/gtadb-landmarks.json", encoding="utf-8"))
out = []; cnt = collections.Counter()
for k, v in d.items():
    if not v[1] or len(v[1]) < 2: continue
    name = v[0]; tags = v[6] if len(v) > 6 else []
    if any(t in SKIP_TAGS for t in tags): continue  # evita conteúdo adulto
    unnamed = name.startswith("?") or name.startswith('"?')
    if unnamed and not any(t.startswith("#") for t in tags): continue
    parts = name.split(", ")
    title = parts[0]
    cat = "outros"
    for key, _, _, ts in CATS:
        if any(t in ts for t in tags): cat = key; break
    if unnamed: title = TAGNAME.get(next(t for t in tags if t.startswith("#")), "Lugar sem nome")
    real = v[3] if len(v) > 3 and isinstance(v[3], str) else ""
    out.append({"id": k, "t": title, "r": ", ".join(parts[1:]), "c": cat, "x": round(v[1][0], 1), "y": round(v[1][1], 1),
                "real": real, "u": 1 if "unconfirmed" in tags else 0})
    cnt[cat] += 1
json.dump({"cats": [{"k": a, "n": b, "c": c} for a, b, c, _ in CATS], "pts": out}, open("vendor/gtadb-pts.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(len(out), cnt.most_common())
