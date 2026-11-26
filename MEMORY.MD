# Memória do projeto

## Resumo atual

- O atualizador `update_apps.py` inclui Immich no workflow diário existente
  (`.github/workflows/weekly-update.yaml`, 06:00 UTC).
- Immich acompanha releases estáveis **2.x**, com servidor e ML CPU/CUDA/OpenVINO
  sincronizados. O chart atual usa pgvecto.rs, incompatível com Immich 3.
- A automação foi preparada para publicação. A instalação no TrueNAS segue pendente.

## Histórico

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
