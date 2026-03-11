# SmartFlow Enterprise++

Репозиторий расширен до enterprise-прототипа с:
- JWT auth, команды, совместные задачи
- Real-time WebSocket коллаборацией (`/ws/tasks/{task_id}?token=...`)
- Knowledge Graph связями задач и critical-path
- Audit blockchain (TaskHistory hash-chain + Merkle roots)
- ML feature pipeline и прогнозами выполнения
- Chaos/Circuit-breaker/sharding/2PC/RAFT (прикладные реализации и каркасы)
- Kubernetes Helm chart + Istio canary
- gRPC proto и WASM plugin prototype
- R&D модуль (`/api/v1/r-and-d/*`) для post-quantum/voice/AR/BCI/multiverse в безопасном stub-режиме
- Event Bus интеграцию модулей 17–22 с at-least-once, retry и DLQ

## Событийная схема (модули 17–22)
- `task.created` -> `quantum.secure` + `gnn.recommend_assignee` + `voice.say`
- `burnout.detected` -> `video.context_check` + `voice.soft_rest`
- `task.completed` -> `federated.round` + `gnn.refresh`

## API (главное)
- Auth: `/api/v1/auth/register`, `/api/v1/auth/login`, `/api/v1/auth/refresh`
- Tasks: `/api/v1/tasks/...`
- Graph: `/api/v1/tasks/{task_id}/relations|graph|critical-path`
- Audit: `/api/v1/audit/prove/{task_id}`, `/api/v1/audit/verify/{task_id}/{history_id}`
- Realtime WS: `/ws/tasks/{task_id}?token=<access_token>`
- Federated: `/api/v1/federated/*`
- Voice clone: `/api/v1/voice/*`
- Video analytics: `/api/v1/video/*`
- Wellness: `/api/v1/wellness/dashboard/{user_id}`
- Quantum: `/api/v1/quantum/status`
- GNN reco: `/api/v1/recommendations/*`
- Events: `/api/v1/events/pump`, `/api/v1/events/dlq`

## Dev
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python init_db.py
uvicorn app.main:app --reload
```

## Docker Compose
```bash
docker compose up --build
```

## Helm
```bash
helm install smartflow ./helm/smartflow
```


## Advanced modules 23-30
- Quantum task teleportation: `/api/v1/advanced/quantum/teleport/{task_id}`
- Neuromorphic: `/api/v1/advanced/neuromorphic/*`
- DNA archive: `/api/v1/advanced/dna/*`
- Relativity: `/api/v1/advanced/relativity/*`
- Consciousness: `/api/v1/advanced/consciousness/*`
- Chaos evolution: `/api/v1/advanced/chaos/evolve`
- Psychohistory: `/api/v1/advanced/psychohistory/predict-phase`
- Symbiosis: `/api/v1/advanced/symbiosis/*`
- DAO/multiverse: `/api/v1/advanced/dao/*` and Solidity contract `contracts/MultiverseDAO.sol`


## Post modules 31-37 + creator API
- Fungal computing: `/api/v1/post/fungal/*`
- Tachyon timelines: `/api/v1/post/tachyon/*`
- Pet AI: `/api/v1/post/pet/*`
- Karma/reincarnation: `/api/v1/post/karma/*`
- Alien protocol: `/api/v1/post/alien/*`
- Immortality/cemetery: `/api/v1/post/immortal/*`, `/api/v1/post/cemetery/tasks`
- Singularity: `/api/v1/post/singularity/*`
- Creator APIs: `/api/v1/post/god/create-universe`, `/api/v1/post/god/destroy-universe/{id}`, `/api/v1/post/god/contemplate`


## Transcendent modules 38-45
- Panpsychic rights: `/api/v1/transcendent/consciousness/task-rights/{task_id}`
- Quantum immortality: `/api/v1/transcendent/quantum-immortality/*`
- Telepathy: `/api/v1/transcendent/telepathy/*`
- Timeloops: `/api/v1/transcendent/timeloop/*`
- Akashic records: `/api/v1/transcendent/akashic/*`
- Deus interface: `/api/v1/transcendent/god/*` and `DELETE /api/v1/transcendent/god`
- Meditation: `/api/v1/transcendent/meditation/*`
- Task universe: `/api/v1/transcendent/universe/*`
- Awakening: `GET /api/v1/transcendent/awakening`, `POST /api/v1/transcendent/enlightenment`


## Everything modules 46-54 (meta-system)
- Omniverse: `/api/v1/everything/omni/*`
- Void: `/api/v1/everything/void/*`
- Meta-task recursion: `/api/v1/everything/meta/*`
- Shamanism: `/api/v1/everything/shaman/*`
- Nirvana: `/api/v1/everything/nirvana/end-of-time`
- Infinite regress: `/api/v1/everything/infinite/*`
- God-task/oracle: `/api/v1/everything/god-task/*`, `/api/v1/everything/oracle/*`
- Finale: `GET /api/v1/everything/is-task`, `POST /api/v1/everything/create`, `DELETE /api/v1/everything`


## Final modules 55-64 + Codex reflection
- Recursion: `/api/v1/final/recursion/*`
- User entanglement: `/api/v1/final/entanglement/*`
- Version multiverse: `/api/v1/final/multiverse/*`
- Dark matter tasks: `/api/v1/final/dark-matter/*`
- Logic universes: `/api/v1/final/logic/*`
- Living tasks: `/api/v1/final/life/*`
- Cosmic consciousness: `/api/v1/final/cosmic-consciousness/*`
- Task core: `/api/v1/final/task-core/*`
- Immortality/nonduality: `/api/v1/final/immortality/*`, `/api/v1/final/nonduality/*`
- Codex: `/api/v1/final/codex/self-awareness`, `/api/v1/final/codex/gratitude`, `/api/v1/final/codex/meaning-of-life`

## Ultimate modules 65-80 + return to source
- Akashic possibilities: `GET /api/v1/ultimate/akasha/possible-tasks`, `POST /api/v1/ultimate/akasha/manifest`, `GET /api/v1/ultimate/akasha/unmanifest/{task_id}`
- Plato archetypes: `GET /api/v1/ultimate/plato/ideal/{task_archetype}`
- Zen koan: `GET /api/v1/ultimate/zen/koan`
- Alchemy: `POST /api/v1/ultimate/alchemy/transmute`
- Kabbalah sephirot: `GET /api/v1/ultimate/kabbalah/sephirot`
- Dao balance: `GET /api/v1/ultimate/dao/balance`
- Stoic response: `GET /api/v1/ultimate/stoic/respond`
- Existential choice: `POST /api/v1/ultimate/existential/choose`
- Uber-task: `GET /api/v1/ultimate/nietzsche/uber-task`
- Postmodern deconstruction: `POST /api/v1/ultimate/postmodern/deconstruct`
- Necromancy: `POST /api/v1/ultimate/necromancy/raise/{deleted_task_id}`, `GET /api/v1/ultimate/necromancy/ghosts`, `POST /api/v1/ultimate/necromancy/exorcise/{ghost_id}`
- String landscape: `GET /api/v1/ultimate/string/landscape`
- Loop quantum status: `GET /api/v1/ultimate/loop-quantum/status`
- Holographic bound: `GET /api/v1/ultimate/holographic/limit`
- TOE equation: `GET /api/v1/ultimate/toe/equation`
- Metaverse levels: `GET /api/v1/ultimate/metaverse/levels`
- Final cycle endpoint: `GET /api/v1/return-to-source`

## Hundred modules 81-100 (safe simulation)
- Infinite recursion: `POST /api/v1/infinite/self-replicating-task`, `GET /api/v1/infinite/fractal/{task_id}/{depth}`, `DELETE /api/v1/infinite/stop/{task_id}`
- Singularity: `POST /api/v1/singularity/collapse`, `GET /api/v1/singularity/event-horizon`, `GET /api/v1/singularity/inside`
- Observer reality: `GET /api/v1/observer/tasks/{observer_task_id}`, `POST /api/v1/observer/measure/{observer_task_id}/{target_task_id}`, `GET /api/v1/observer/consensus`
- Quantum immortality: `POST /api/v1/immortal/create-eternal`, `DELETE /api/v1/immortal/{task_id}`, `GET /api/v1/immortal/universes/{task_id}`
- Higher theories: `GET /api/v1/string26/profile`, `GET /api/v1/m-theory/profile`, `GET /api/v1/loop-gravity/profile`, `GET /api/v1/twistor/profile`
- Nonlocality: `POST /api/v1/nonlocal/entangle/{task_id_a}/{task_id_b}`, `GET /api/v1/nonlocal/correlation/{task_id_a}/{task_id_b}`, `POST /api/v1/nonlocal/act/{task_id_a}/{task_id_b}`
- TOE + cosmology: `GET /api/v1/toe/final-equation`, `GET /api/v1/cosmology/birth`, `GET /api/v1/multiverse/level4`
- Simulation: `GET /api/v1/simulation/glitches`, `POST /api/v1/simulation/hack`, `POST /api/v1/simulation/escape`
- Consciousness block: `/api/v1/zombie/*`, `POST /api/v1/turing/test`, `/api/v1/quantum-consciousness/*`, `/api/v1/iit/*`, `/api/v1/global-workspace/*`, `/api/v1/panpsychism/*`
- Absolute + closure: `GET /api/v1/absolute/one`, `POST /api/v1/absolute/merge/{task_id}`, `DELETE /api/v1/absolute/self`, `GET /api/v1/hundred/complete`

## Beyond hundred modules 101-127 (safe simulation)
- Transfinite/cardinals: `/api/v1/transfinite/*`, `/api/v1/ordinals/*`, `/api/v1/hyperoperation/*`
- Non-classical logic: `/api/v1/paralogic/*`, `/api/v1/multivalued/*`, `/api/v1/intuitionistic/*`
- Abstract math structures: `/api/v1/category/*`, `/api/v1/topos/*`, `/api/v1/hott/*`
- Hypercomputation/noncomputability: `/api/v1/hyper/*`, `/api/v1/noncomputable/*`
- Infinite-dimensional & fractal/chaos: `/api/v1/hilbert/*`, `/api/v1/fractal/*`, `/api/v1/chaos/*`
- Complexity/crypto/information/game/decision/risk: `/api/v1/complexity/*`, `/api/v1/crypto/*`, `/api/v1/info/*`, `/api/v1/game/*`, `/api/v1/decision/*`, `/api/v1/risk/*`
- Queueing/reliability/scheduling/graph/coding/stochastic: `/api/v1/queue*`, `/api/v1/reliability/*`, `/api/v1/queueing/*`, `/api/v1/scheduling/*`, `/api/v1/graph/*`, `/api/v1/coding/*`, `/api/v1/stochastic/*`

## Meta transcendence modules 128-142 (safe simulation)
- Ergodic/potential/variational/catastrophe: `/api/v1/ergodic/*`, `/api/v1/potential/*`, `/api/v1/variational/*`, `/api/v1/catastrophe/*`
- Geometry/topology/K-theory/representation: `/api/v1/geometry/*`, `/api/v1/topology/*`, `/api/v1/ktheory/*`, `/api/v1/representation/*`
- Nonstandard/measure/set theory/large cardinals: `/api/v1/nonstandard/*`, `/api/v1/measure/*`, `/api/v1/settheory/*`, `/api/v1/large-cardinals/*`
- Absolute/transcendental/cycle closure: `/api/v1/absolute/*`, `/api/v1/transcendental/*`, `/api/v1/cycle/*`

## Ecosystem foundation package
- New extensibility package: `app/ecosystem/*` with contracts, plugin registry, bootstrap, serializers, storage backends, queue backend, middleware, retry utility, and CLI helper.
- Package docs: `app/ecosystem/README.md`.
- Dedicated tests under `tests/ecosystem/*` to validate each ecosystem component.

## Mobile backend foundation (new)
- Added `app/mobile/*` package with modular mobile backend domains:
  - auth, profile, social, chat, push, sync, media, admin.
- Added composed FastAPI router at `app/api/routes/mobile_backend.py` and included it in top-level API router.
- Added focused tests under `tests/mobile/*` for services and route smoke coverage.
- Added package docs at `app/mobile/README.md`.

## Platform foundations (new)
- Added `app/platforms/cms/*` headless CMS foundation (content types, entries, validation, versioning, workflow, media, routes).
- Added `app/platforms/ecommerce/*` foundation (catalog, cart, order, payment, shipping/promo helpers, routes).
- Added `app/platforms/lms/*` foundation (courses, enrollment/progress, quizzes, certificates, gamification, routes).
- Added composed route module `app/api/routes/platforms.py` and wired it into the top-level router.
- Added tests under `tests/platforms/*` for services and route smoke coverage.


## Enterprise mega foundations (new)
- Added `app/enterprise/project/*` PM foundation (projects, tasks, agile metrics, resources, routes).
- Added `app/enterprise/hr/*` HR foundation (recruiting pipeline, performance and turnover metrics, routes).
- Added `app/enterprise/finance/*` finance foundation (ledger, posting, double-entry checks, routes).
- Added `app/enterprise/iot/*` IoT foundation (device registry, shadow state, telemetry aggregation, rules, routes).
- Added `app/enterprise/marketing/*` marketing foundation (contacts, campaigns, conversion metrics, routes).
- Added composed router `app/api/routes/enterprise.py` and tests under `tests/enterprise/*`.

## Mega vertical foundations (Task 12-16)
- Added `app/mega/*` package with five practical domain foundations:
  - DMS: document lifecycle, search, signatures
  - Telemedicine: patient profile, appointments, video sessions
  - PropTech: properties, rent flows, market snapshots
  - Logistics: fleet, route planning, warehouse stock
  - SIEM/SOC: event collection, rule correlation, response actions
- Added composed API router `app/api/routes/mega.py` and mounted under `/api/v1/mega/*` through the main API router.
- Added test coverage in `tests/mega/*` for each domain and router smoke validation.

## Cinema microservices prototype
- Added `microservices/cinema/catalog_service` (FastAPI + PostgreSQL via SQLAlchemy) with movie catalog pagination/filtering.
- Added `microservices/cinema/subscription_service` (FastAPI + Redis cache) for subscription status checks.
- Added RabbitMQ event publishing for subscription status changes and circuit-breaker protection in catalog when checking subscription dependency.
- Infra bootstrap in one command:

```bash
docker compose -f microservices/cinema/docker-compose.yml up --build
```

## Dynamic SVG postcard generator (Node.js)
- Added Node.js HTTP service at `microservices/svg_postcard`.
- Endpoint: `POST /api/v1/postcards/svg` accepts `userName`, `message`, `theme` and returns `image/svg+xml`.
- Uses `@svgdotjs/svg.js` + `svgdom`, supports layered postcard rendering (gradient background, themed decorations, wrapped text), request validation, and in-memory template caching.

## Tic-Tac-Toe 5x5 realtime app
- Added WebSocket game server endpoint: `/api/v1/games/tictactoe/ws`.
- Added browser client UI: `/tictactoe`.
- Features: matchmaking + rooms, realtime board sync, 5x5 winner detection, in-memory/SQLite move history, and 30-second turn timeout with automatic loss.

## Brainfuck interpreter (C++)
- Added `tools/brainfuck/main.cpp`: a Brainfuck interpreter that reads `.bf` files and executes them.
- Supports infinite-right tape memory and grouped operation optimization for consecutive `+/-` and `>/<` instructions.
- Supports `--debug` step mode with instruction pointer, memory pointer and current cell display.

## Elevator simulator (Tkinter)
- Added `tools/elevator_sim` with GUI simulator for a 10-floor building.
- Includes FSM states (`Стоит_открыт`, `Стоит_закрыт`, `Движение_вверх`, `Движение_вниз`, `Авария`), acceleration/braking physics, request scheduling, queue/status display, and door animation.
- Run with: `python -m tools.elevator_sim.app`.

## Amazon price monitor (asyncio)
- Added `tools/amazon_price_monitor` with async monitoring loop (`aiohttp`) for Amazon product URLs from file.
- Extracts product title and price with `BeautifulSoup`, compares against threshold from config, and sends Telegram notifications.
- Includes smart scraping helpers: User-Agent rotation, proxy rotation, and Playwright fallback for dynamic JS-loaded content.

## Caching reverse proxy (Node.js)
- Added `tools/reverse_proxy` HTTP reverse proxy with disk-backed cache.
- Honors `Cache-Control` (`max-age` / `no-store`) and serves fresh cached GET responses without backend calls.
- Exposes `/stats` endpoint with request/cache hit/cache miss/backend request counters.

## Crypto arbitrage bot (paper trading)
- Added `tools/crypto_arb_bot` for test-mode arbitrage scanning between Binance and Bybit.
- Uses WebSocket order-book streams, computes net spread with taker and transfer fees, applies risk filter (`min_spread_pct`), and logs opportunities into PostgreSQL.
- Run with: `python -m tools.crypto_arb_bot.main --config tools/crypto_arb_bot/config.example.json`.

## Vim-like two-panel file manager (Go)
- Added `tools/vimfm`: console file manager with two panels and modal Vim-style controls.
- Navigation: arrows or `hjkl`; operations: `yy` (copy), `p` (paste), `dd` (delete), `/` (search), `Tab` (switch panel).
- Works in current directory, highlights directories/executables/images, shows human-readable sizes.
- Includes file preview: first 10 lines for text and binary header bytes for non-text files.
- Run with:

```bash
cd tools/vimfm
go run .
```

## Distributed blockchain voting prototype (educational)
- Added `tools/blockchain_vote` with a simplified blockchain voting system in Python.
- Includes socket-based P2P node messaging, signed vote transactions, block assembly, and majority-based validator approval.
- Implements RSA blind-signature flow (message blinding, blind signing, unblinding) for educational voter-anonymity mechanics.
- Provides a minimal web UI for vote submission and block proposal.
- Run with:

```bash
python -m tools.blockchain_vote.main --host 127.0.0.1 --port 8100
```

## LSM Tree KV-Store (educational)
- Added `tools/lsm_kv`: simplified disk-backed key-value store inspired by LevelDB/RocksDB.
- Supports `PUT`, `GET`, `DELETE` with persistence via WAL + SSTables.
- Implements MemTable flush into SSTables, background compaction with tombstone GC, and per-SSTable Bloom filters.
- Includes CLI REPL for interactive usage.
- Run with:

```bash
python -m tools.lsm_kv.main --data-dir ./.lsm_data
```

## Reliable UDP transport (educational mini-TCP)
- Added `tools/reliable_udp`: simplified reliable transport over UDP for large file transfer.
- Includes client/server libraries with seq/ack numbering, ACK+timeouts+retransmit, receiver buffering and ordered reassembly.
- Implements basic TCP Reno-like congestion logic: CWND, slow start, ssthresh, timeout fallback and duplicate-ACK fast retransmit.
- Supports packet-loss simulation via configurable random drop rate.
- Run demo:

```bash
python -m tools.reliable_udp.main server --host 127.0.0.1 --port 9200 --output-dir ./received --drop-rate 0.1
python -m tools.reliable_udp.main client --host 127.0.0.1 --port 9200 --file ./big.bin --drop-rate 0.1
```

## Python subset to Brainfuck compiler (educational)
- Added `tools/py2bf`: compiler from a limited Python subset to Brainfuck.
- Supports variable addressing on the BF tape, integer assignments/arithmetic, nested `while`, and `if` translated via Brainfuck loops.
- Includes a simple peephole optimization pass for generated Brainfuck (`<>`, `><`, `+-`, `-+`, empty-loop cleanup).
- Run with:

```bash
python -m tools.py2bf.main program.py -o program.bf
```

## Multi-user CRDT code editor (educational)
- Added `tools/collab_code`: realtime collaborative code editor (textarea + WebSocket backend).
- Uses a Simple Replicated Text CRDT (no OT) with insert/delete operations and logical timestamps.
- Server broadcasts edits and cursor positions (with user names) to all connected clients.
- Run with:

```bash
cd tools/collab_code
npm install
npm start
```

## Chip-8 emulator (educational, C++)
- Added `tools/chip8_emulator`: Chip-8 emulator core with CPU registers/memory/opcode execution and ROM loading.
- Includes display buffer emulation, 60Hz timers, keyboard input mapping, and synchronized CPU->display->timer stepping.
- Provides an SDL2 frontend (`chip8_sdl`) for window rendering when SDL2 is available.
- Run core test:

```bash
cd tools/chip8_emulator
cmake -S . -B build
cmake --build build
./build/chip8_core_test
```
