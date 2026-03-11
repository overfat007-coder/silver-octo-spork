# Caching Reverse Proxy (Node.js)

Simple HTTP reverse proxy that forwards requests to backend and caches GET responses on disk.

## Features
- respects `Cache-Control` (`max-age`, `no-store`)
- serves fresh cache entries without backend call
- disk cache storage (URL -> hashed directory with `meta.json` + `body.bin`)
- `/stats` endpoint for cache hit/miss counters

## Run
```bash
TARGET_BASE_URL=http://localhost:8000 PORT=8090 node tools/reverse_proxy/src/server.js
```

## Stats endpoint
```bash
curl http://localhost:8090/stats
```
