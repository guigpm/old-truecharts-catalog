# Memória do projeto

## Resumo atual

- AdGuard Home, Cloudflared, Jellyfin e Navidrome foram adicionados ao fluxo
  diário. Plex e qBittorrent já tinham automação no catálogo e agora exigem
  confirmação do registro de imagens, assim como os quatro novos.

- O atualizador `update_apps.py` inclui Immich no workflow diário existente
  (`.github/workflows/weekly-update.yaml`, 06:00 UTC).
- Immich acompanha releases estáveis **2.x**, com servidor e ML CPU/CUDA/OpenVINO
  sincronizados. O chart atual usa pgvecto.rs, incompatível com Immich 3.
- A automação foi preparada para publicação. A instalação no TrueNAS segue pendente.

## Onde registrar informações

- Consulte este arquivo primeiro para localizar pontos de entrada e verificações anteriores.
- Mantenha neste arquivo os detalhes por aplicativo, atalhos de busca, decisões e
  aprendizados que reduzam trabalho repetido. Atualize o resumo e preserve o histórico.
- Edite `AI_UPDATE_GUIDE.md` apenas quando mudarem as instruções gerais de automação.

## Histórico

### 2026-11-26 — README dos apps acompanhados

- A tabela em `README.md` lista AdGuard Home, Cloudflared, Jellyfin e Navidrome
  com os registries usados em `update_apps.py`. Também documenta a confirmação das
  imagens e os limites de versão de AdGuard Home e Jellyfin.
- Conferidos os repositórios e filtros com o atualizador e verificado o diff.

### 2026-11-26 — Serviços Running da captura do TrueNAS

- `update_apps.py` segue as releases estáveis e mantém os repositórios de imagem
  dos charts de AdGuard Home, Cloudflared, Jellyfin e Navidrome. A instância
  `cloudflared-tun` aparece como TrueCharts e o chart correspondente é
  `stable/cloudflared`. A captura não confirma a origem exata da instância.
- AdGuard Home acompanha 0.x. Jellyfin acompanha 10.x devido às mudanças no banco
  ao migrar para 12.0: https://github.com/jellyfin/jellyfin/releases/tag/v12.0.
- Plex e qBittorrent consultam tags numéricas do GHCR, mantendo as imagens
  `home-operations`. Commits 947192b96 e 1bc1f8980 mostram atualizações reais
  dos respectivos charts. Falhas de consulta do manifesto agora bloqueiam
  esses dois charts e os quatro novos. O bloco principal `image` é editado
  pelo nome, mantendo imagens auxiliares.
- Kasm ficou pendente. O chart roda `kasmweb/workspaces` com `/opt` persistente
  e a troca de tag não foi validada como migração de uma instalação existente.
  Referência: https://docs.kasm.com/docs/latest/how-to/upgrade/single-server-upgrade.
- `cloudflareddns-github`, MinIO, NTP e a instância do qBittorrent aparecem
  como TrueNAS na captura. O fluxo desse catálogo não atualiza essas instalações.
  Para avaliar automação nelas, faltam os charts ou imagens efetivamente em uso
  e acesso ao ambiente. A revisão de qBittorrent cobre `stable/qbittorrent`.
- Validação: 9 testes e `git -c core.whitespace=cr-at-eol diff --check` passaram.
  Em dry-run com rede, foram confirmadas as imagens candidatas a AdGuard Home
  0.107.80, Cloudflared 2026.11.2, Jellyfin 10.11.11 e Navidrome 0.64.2.
  Plex 1.43.5.11079 e qBittorrent 5.3.1 já estavam em dia no catálogo e seus
  manifestos atuais foram confirmados diretamente no GHCR.
- Alteração local no fluxo existente. Pendente publicação e validação no NAS.

### 2026-11-26 — Nome do arquivo de memória

- Padronizada a extensão para `.md` e atualizado o link em `AGENTS.md`.
- Verificados o nome do arquivo e o destino do link.

### 2026-11-26 — Organização da documentação

- Retirada do guia a seção específica do Immich. Na lista `APPS` de
  `update_apps.py`, cada item de `additional_images` recebe `key` (bloco de
  primeiro nível em `ix_values.yaml`), `image_repo` e `tag_format`. Para o
  Immich, procure por `image`, `mlImage`, `mlCudaImage` e `mlOpenvinoImage`.
- Alteração documental verificada com `git -c core.whitespace=cr-at-eol diff --check`.

### 2026-11-26 — Automação do Immich

- `MEMORY.MD` não existia na árvore de trabalho; criado conforme `AGENTS.md`.
- Consultados `AI_UPDATE_GUIDE.md`, atualizador, workflow e chart
  `stable/immich/15.22.2` (appVersion 2.4.1).
- Adicionado Immich a `APPS`, com releases de `immich-app/immich` e imagens oficiais
  `ghcr.io/immich-app/immich-server` e `immich-machine-learning`.
- Adicionados `additional_images` e edição explícita dos blocos YAML. As quatro
  imagens precisam estar disponíveis; consulta inconclusiva também impede a
  atualização multi-imagem. Digests são resolvidos individualmente, mantendo o
  fallback existente para tag quando indisponíveis. Validação dos blocos ocorre
  antes de copiar o chart, evitando versão parcial por configuração inválida.
- Adicionado filtro opcional `version_major`, com paginação de releases e exclusão
  de drafts/prereleases. Immich fica em 2.x devido à remoção do pgvecto.rs em v3:
  https://immich.app/blog/v3-migration.
- Pontos de entrada: `python3 update_apps.py` (workflow diário) e
  `python3 update_apps.py --dry-run --apps immich` (simulação específica).
- Documentados comportamento e limite no `README.md` e `AI_UPDATE_GUIDE.md`.
- Verificações: 8 testes passaram com `python3 -m unittest discover -s tests -v`:
  sincronização das imagens, preservação do chart original e dependências,
  imagens ausentes/consulta inconclusiva, dry-run, bloco inválido, comportamento
  de imagem única, paginação e filtro estável por major.
- Simulação real: sandbox inicialmente bloqueou DNS; repetição com permissão de
  rede passou, identificando **2.4.1 -> 2.7.5** e confirmando as quatro imagens.
- `git -c core.whitespace=cr-at-eol diff --check` passou; CRLF preexistente
  preservado nos arquivos editados. Helm não está instalado; não houve teste de
  execução no TrueNAS. Nenhum chart ou índice foi gerado no repositório.
- Pendências: publicar as alterações para ativar no workflow remoto; validar
  instalação no TrueNAS. Para Immich 3, migrar banco para extensão suportada e
  validar o chart antes de alterar `version_major`.
- `AGENTS.md` já estava não rastreado antes da tarefa e foi preservado.
