# 🔄 Fluxo CI/CD - Diagrama Visual

## 📊 Visão Geral

```
┌─────────────────────────────────────────────────────────────────┐
│                    DESENVOLVEDOR                                 │
└────────────┬────────────────────────────────────────────────────┘
             │
             │ git push
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    GITHUB REPOSITORY                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ feature/*    │  │     dev      │  │  prod/main   │          │
│  │ (CI apenas)  │  │ (auto deploy)│  │  (aprovação) │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└────────────┬────────────────────────────────────────────────────┘
             │
             │ trigger
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    GITHUB ACTIONS                                │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  1. CI - Tests & Quality                                 │   │
│  │     ✓ Backend tests                                      │   │
│  │     ✓ Frontend build                                     │   │
│  │     ✓ Security scan                                      │   │
│  │     ✓ Docker build                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          │                                       │
│                          ▼                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  2. Build & Push Images                                  │   │
│  │     ✓ Build backend image                                │   │
│  │     ✓ Build frontend image                               │   │
│  │     ✓ Push to GHCR                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          │                                       │
│                          ▼                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  3. Deploy (DEV = auto / PROD = manual approval)        │   │
│  │     ✓ Create backup                                      │   │
│  │     ✓ Pull new images                                    │   │
│  │     ✓ Deploy with zero downtime                          │   │
│  │     ✓ Run migrations                                     │   │
│  │     ✓ Health check                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          │                                       │
│                    ┌─────┴─────┐                                │
│                    │           │                                 │
│                 SUCCESS     FAILURE                              │
│                    │           │                                 │
│                    ▼           ▼                                 │
│            ┌──────────┐  ┌──────────┐                           │
│            │   DONE   │  │ ROLLBACK │                           │
│            └──────────┘  └──────────┘                           │
└─────────────────────────────────────────────────────────────────┘
             │                     │
             │                     │
             ▼                     ▼
┌─────────────────────┐  ┌─────────────────────┐
│   SERVIDOR DEV      │  │   SERVIDOR PROD     │
│                     │  │                     │
│  ┌──────────────┐   │  │  ┌──────────────┐  │
│  │   Backend    │   │  │  │   Backend    │  │
│  │   Frontend   │   │  │  │   Frontend   │  │
│  │   Database   │   │  │  │   Database   │  │
│  │   Redis      │   │  │  │   Redis      │  │
│  └──────────────┘   │  │  └──────────────┘  │
│                     │  │                     │
│  ┌──────────────┐   │  │  ┌──────────────┐  │
│  │   .backup/   │   │  │  │   .backup/   │  │
│  │   - images   │   │  │  │   - images   │  │
│  │   - db dumps │   │  │  │   - db dumps │  │
│  └──────────────┘   │  │  └──────────────┘  │
└─────────────────────┘  └─────────────────────┘
```

---

## 🔀 Fluxo de Branches

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                   │
│  feature/login                                                    │
│      │                                                            │
│      │ PR + merge                                                │
│      ▼                                                            │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  dev (development)                                       │    │
│  │  ✓ CI automático                                         │    │
│  │  ✓ Deploy automático para DEV                           │    │
│  │  ✓ Testes de integração                                 │    │
│  └─────────────────────────────────────────────────────────┘    │
│      │                                                            │
│      │ PR + merge (após validação)                               │
│      ▼                                                            │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  prod/main (production)                                  │    │
│  │  ✓ CI completo + security scan                          │    │
│  │  ✓ Requer aprovação manual                              │    │
│  │  ✓ Deploy para PROD                                     │    │
│  │  ✓ Smoke tests                                          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛡️ Sistema de Fallback

```
┌─────────────────────────────────────────────────────────────────┐
│                    DEPLOY PROCESS                                │
└─────────────────────────────────────────────────────────────────┘

ANTES DO DEPLOY:
┌─────────────────────────────────────────────────────────────────┐
│  1. Backup Database                                              │
│     docker-compose exec db pg_dump > .backup/db_TIMESTAMP.sql   │
│                                                                   │
│  2. Save Current Images                                          │
│     docker inspect > .backup/last_images.txt                     │
│                                                                   │
│  3. Save Timestamp                                               │
│     date > .backup/last_deploy.txt                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
DURANTE O DEPLOY:
┌─────────────────────────────────────────────────────────────────┐
│  1. Pull new images                                              │
│  2. Deploy with zero downtime                                    │
│  3. Run migrations                                               │
│  4. Health check (30 tentativas, 2s cada)                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                 SUCCESS             FAILURE
                    │                   │
                    ▼                   ▼
         ┌──────────────────┐  ┌──────────────────┐
         │   DEPLOY OK      │  │  AUTO ROLLBACK   │
         │   ✓ Limpar old   │  │  1. Stop current │
         │   ✓ Notificar    │  │  2. Restore imgs │
         └──────────────────┘  │  3. Restore DB   │
                               │  4. Start old    │
                               │  5. Verify       │
                               └──────────────────┘
```

---

## 🔄 Processo de Rollback

```
┌─────────────────────────────────────────────────────────────────┐
│                    ROLLBACK TRIGGERS                             │
└─────────────────────────────────────────────────────────────────┘

AUTOMÁTICO:                          MANUAL:
┌──────────────────────┐            ┌──────────────────────┐
│ ✗ Health check fail  │            │ GitHub Actions UI    │
│ ✗ Migration error    │            │ SSH + script         │
│ ✗ Container crash    │            │ Emergency procedure  │
└──────────────────────┘            └──────────────────────┘
         │                                    │
         └────────────┬───────────────────────┘
                      ▼
         ┌─────────────────────────────────────┐
         │      ROLLBACK PROCEDURE              │
         └─────────────────────────────────────┘
                      │
         ┌────────────┴────────────┐
         ▼                         ▼
┌──────────────────┐      ┌──────────────────┐
│  1. STOP         │      │  2. RESTORE      │
│  ✓ Stop current  │      │  ✓ Pull old imgs │
│  ✓ Save logs     │      │  ✓ Restore DB    │
└──────────────────┘      └──────────────────┘
         │                         │
         └────────────┬────────────┘
                      ▼
         ┌─────────────────────────────────────┐
         │  3. START                            │
         │  ✓ Start old version                │
         │  ✓ Run migrations                   │
         │  ✓ Health check                     │
         └─────────────────────────────────────┘
                      │
         ┌────────────┴────────────┐
         ▼                         ▼
    ┌─────────┐              ┌─────────┐
    │ SUCCESS │              │ FAILURE │
    │ ✓ Done  │              │ ✗ Alert │
    └─────────┘              └─────────┘
```

---

## 📊 Timeline de Deploy

```
DEV (Automático - ~5 minutos):
┌─────────────────────────────────────────────────────────────────┐
│ 0:00  │ Push to dev branch                                      │
│ 0:30  │ CI: Tests running                                       │
│ 1:30  │ Build: Docker images building                           │
│ 3:00  │ Deploy: Backup + Pull + Deploy                          │
│ 4:30  │ Verify: Health checks                                   │
│ 5:00  │ ✅ DONE                                                 │
└─────────────────────────────────────────────────────────────────┘

PROD (Com aprovação - ~10 minutos):
┌─────────────────────────────────────────────────────────────────┐
│ 0:00  │ Push to prod branch                                     │
│ 0:30  │ CI: Tests + Security scan                               │
│ 2:00  │ Build: Docker images building                           │
│ 3:30  │ ⏸️  WAITING FOR APPROVAL                                │
│ 5:00  │ ✅ Approved                                             │
│ 5:30  │ Deploy: Full backup + Pull + Deploy                     │
│ 8:00  │ Verify: Health checks + Smoke tests                     │
│ 10:00 │ ✅ DONE                                                 │
└─────────────────────────────────────────────────────────────────┘

ROLLBACK (Automático - ~3 minutos):
┌─────────────────────────────────────────────────────────────────┐
│ 0:00  │ ❌ Deploy failed                                        │
│ 0:10  │ Stop current containers                                 │
│ 0:30  │ Restore previous images                                 │
│ 1:30  │ Restore database                                        │
│ 2:00  │ Start old version                                       │
│ 2:30  │ Health check                                            │
│ 3:00  │ ✅ Rollback complete                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Pontos de Decisão

```
                    ┌─────────────┐
                    │  GIT PUSH   │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │   Branch?   │
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐       ┌─────▼─────┐     ┌─────▼─────┐
   │feature/*│       │    dev    │     │prod/main  │
   └────┬────┘       └─────┬─────┘     └─────┬─────┘
        │                  │                  │
   ┌────▼────┐       ┌─────▼─────┐     ┌─────▼─────┐
   │CI only  │       │CI + Deploy│     │CI + Wait  │
   │No deploy│       │to DEV     │     │+ Deploy   │
   └─────────┘       └─────┬─────┘     └─────┬─────┘
                           │                  │
                     ┌─────▼─────┐      ┌─────▼─────┐
                     │Health OK? │      │Approved?  │
                     └─────┬─────┘      └─────┬─────┘
                           │                  │
                    ┌──────┼──────┐    ┌──────┼──────┐
                    │      │      │    │      │      │
                   YES    NO     YES  NO     YES    NO
                    │      │      │    │      │      │
                 ┌──▼──┐ ┌▼──┐ ┌─▼──┐ │   ┌──▼──┐  │
                 │DONE │ │RB │ │DONE│ │   │WAIT │  │
                 └─────┘ └───┘ └────┘ │   └─────┘  │
                                       │            │
                                    ┌──▼──┐    ┌────▼────┐
                                    │STOP │    │CANCELED │
                                    └─────┘    └─────────┘
```

---

## 📈 Métricas de Sucesso

```
┌─────────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT METRICS                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Deploy Frequency:        Multiple times per day (DEV)          │
│                          Weekly (PROD)                           │
│                                                                   │
│  Lead Time:              5 min (DEV)                             │
│                          10 min (PROD)                           │
│                                                                   │
│  MTTR (Mean Time to      3 min (automatic rollback)             │
│  Recovery):                                                      │
│                                                                   │
│  Change Failure Rate:    < 5% (with automatic rollback)         │
│                                                                   │
│  Rollback Success:       100% (automated)                        │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

**Legenda:**
- ✓ = Sucesso
- ✗ = Falha
- ⏸️ = Aguardando
- 🔄 = Em progresso
- ❌ = Erro
- ✅ = Completo
