import http from 'node:http';

import { readCache, writeCache } from './cache.js';

const DEFAULT_PORT = Number.parseInt(process.env.PORT || '8090', 10);
const DEFAULT_TARGET_BASE_URL = process.env.TARGET_BASE_URL || 'http://localhost:8000';

export function createProxyServer({ targetBaseUrl = DEFAULT_TARGET_BASE_URL } = {}) {
  const stats = {
    requests: 0,
    cacheHits: 0,
    cacheMisses: 0,
    backendRequests: 0,
  };

  function responseHeadersForClient(headers) {
    const cloned = { ...headers };
    delete cloned['content-encoding'];
    delete cloned['transfer-encoding'];
    return cloned;
  }

  function proxyToBackend(req, res, urlPath) {
    const target = new URL(urlPath, targetBaseUrl);
    const options = {
      protocol: target.protocol,
      hostname: target.hostname,
      port: target.port,
      path: `${target.pathname}${target.search}`,
      method: req.method,
      headers: {
        ...req.headers,
        host: target.host,
      },
    };

    stats.backendRequests += 1;

    const proxyReq = http.request(options, (backendRes) => {
      const chunks = [];
      backendRes.on('data', (chunk) => chunks.push(chunk));
      backendRes.on('end', async () => {
        const body = Buffer.concat(chunks);
        const headers = Object.fromEntries(
          Object.entries(backendRes.headers).map(([k, v]) => [k, Array.isArray(v) ? v.join(', ') : String(v ?? '')]),
        );

        if (req.method === 'GET' && backendRes.statusCode === 200) {
          await writeCache(target.toString(), backendRes.statusCode, headers, body);
        }

        res.writeHead(backendRes.statusCode || 502, responseHeadersForClient(headers));
        res.end(body);
      });
    });

    proxyReq.on('error', (err) => {
      res.writeHead(502, { 'content-type': 'application/json' });
      res.end(JSON.stringify({ error: `proxy error: ${err.message}` }));
    });

    req.pipe(proxyReq);
  }

  const server = http.createServer(async (req, res) => {
    stats.requests += 1;

    if (req.url === '/stats') {
      const payload = {
        ...stats,
        hitRate: stats.requests ? Number((stats.cacheHits / stats.requests).toFixed(4)) : 0,
      };
      res.writeHead(200, { 'content-type': 'application/json' });
      res.end(JSON.stringify(payload));
      return;
    }

    const urlPath = req.url || '/';

    if (req.method === 'GET') {
      const target = new URL(urlPath, targetBaseUrl).toString();
      const cached = await readCache(target);
      if (cached) {
        stats.cacheHits += 1;
        res.writeHead(cached.statusCode, {
          ...responseHeadersForClient(cached.headers),
          'x-proxy-cache': 'HIT',
        });
        res.end(cached.body);
        return;
      }
      stats.cacheMisses += 1;
    }

    proxyToBackend(req, res, urlPath);
  });

  return { server, stats };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const { server } = createProxyServer();
  server.listen(DEFAULT_PORT, () => {
    // eslint-disable-next-line no-console
    console.log(`reverse proxy listening on :${DEFAULT_PORT}, target=${DEFAULT_TARGET_BASE_URL}`);
  });
}
