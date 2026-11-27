# Código-fonte do site Easter Eggs GTA 6

Este branch (`source`) guarda o gerador do site. O branch `main` guarda só o site pronto, que a Cloudflare publica.

## Como atualizar o site

1. Edite `data.json` (easter eggs em `eggs`, carros em `cars`, novidades em `news`, `site.updated` com a data do dia).
2. Rode `python3 build.py` (precisa de Python 3 e Pillow; Playwright é opcional, só para gerar a imagem de compartilhamento).
3. Copie o conteúdo de `dist/` para a raiz do branch `main` (apagando o que havia antes, menos a pasta `.git`), faça commit e push no `main`.

## Formato de um easter egg (`eggs`)

- `id`: identificador em minúsculas com hífens (vira o endereço da página)
- `t`: título · `cat`: piada | misterio | gta | pop | encontro · `ok`: true se confirmado por mais de uma fonte
- `d`: descrição curta · `w`: onde fica · `how`: lista de passos · `note`: observação (opcional)
- `src`: lista de chaves de `sources` (cada fonte tem `n` nome e `u` link)
- `added`: data AAAA-MM-DD · `dif`: Fácil | Médio | Difícil · `tempo`: ex. "10 min"
- `g`: [x, y] em coordenadas do jogo (as do map.gtadb.org) para aparecer no mapa (opcional)

## Regras de conteúdo

- Texto sempre escrito com palavras próprias, com crédito e link para as fontes. Nunca copiar parágrafos.
- Sem spoilers da história. Marcar `ok: false` quando só uma fonte relatar.
- Imagens só oficiais de divulgação ou com autorização do autor.
