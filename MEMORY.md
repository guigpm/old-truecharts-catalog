# Memória do projeto

## Resumo atual

- `stable/immich-v3/1.0.0` oferece Immich 3.4.2 como instalação separada
  com PostgreSQL 16 + VectorChord, armazenamento próprio e porta 10324.
  O fluxo diário acompanha a série 3.x com imagens CPU e CUDA.

- Immich chart 15.22.4 mantém appVersion 2.7.5 e corrige as imagens de espera
  do PostgreSQL e Redis para o registro `oci.trueforge.org`.

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

### 2026-11-26 — Chart separado para Immich 3

- Criado `stable/immich-v3/1.0.0` a partir do chart 15.22.4. Preservados
  os init containers corrigidos e trocado também o domínio da imagem Alpine
  usada para aguardar a API. Os volumes de mídia agora montam sob `/data`.
- CloudNativePG mantém PostgreSQL 16 e cria `vchord` (com `vector`), `cube`
  e `earthdistance` no banco novo. Usa a imagem CNPG da TensorChord com
  VectorChord 0.4.3, digest verificado e `vchord.so` em preload.
- CPU e CUDA usam imagens 3.4.2 confirmadas. OpenVINO foi omitido porque a
  imagem de 3.4.2 não foi publicada: https://github.com/immich-app/immich/issues/33470.
- Pontos de entrada: `catalog.json`, `stable/immich-v3/app_versions.json`,
  formulário `questions.yaml` e `python3 update_apps.py --dry-run --apps immich-v3`.
- Validação: 9 testes passaram. Helm 3.14.4 executou lint e renderizou o
  chart com namespace `ix-immich-v3` e contexto SCALE simulado. Confirmados
  os manifests do Cluster CNPG, imagens, porta e caminhos de mídia.
  Em Docker descartável, a API retornou `{"res":"pong"}` com PostgreSQL
  VectorChord e Redis. A consulta real do atualizador confirmou 3.4.2.
- README principal documenta pré-requisitos, instalação separada e simulação de atualização.
- Pendente publicar o catálogo e testar no TrueNAS, incluindo o operador CNPG,
  os PVCs, os workers, ML e um upload de teste. A migração de dados da v2 deve
  ser tratada separadamente.

### 2026-11-26 — Correção do deploy do Immich

- No SCALE 24.04.2.5, PostgreSQL e Redis rodavam, mas o init do servidor
  falhava com `ImagePullBackOff` ao buscar o digest antigo de `db-wait-postgres`.
  A troca manual dos dois init containers funcionou segundo o usuário.
- Criado chart 15.22.4 a partir do 15.22.3. Os blocos `postgresClientImage`
  e `redisClientImage` em `ix_values.yaml` apontam para os digests v1.1.0
  verificados no registro novo para linux/amd64. Dependências empacotadas
  foram mantidas. O atualizador copia esses overrides nas versões seguintes.
- Regenerados `stable/immich/app_versions.json` e `catalog.json`.
  Helm 3.14.4 renderizou com Kubernetes 1.29 e os valores do chart.
  Confirmadas as duas imagens novas e a presença do recurso CNPG Cluster.
  O render local usou namespace sem prefixo ix, reservado pelo chart ao SCALE.
- Pendente publicação e validação do upgrade pelo catálogo no TrueNAS.

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
