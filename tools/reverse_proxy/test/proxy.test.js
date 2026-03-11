import assert from 'node:assert/strict';
import http from 'node:http';
import test from 'node:test';

import { createProxyServer } from '../src/server.js';

function listen(server) {
  return new Promise((resolve) => {
    server.listen(0, '127.0.0.1', () => resolve(server.address().port));
  });
}

function getJson(url) {
  return new Promise((resolve, reject) => {
    http.get(url, (res) => {
      const chunks = [];
      res.on('data', (d) => chunks.push(d));
      res.on('end', () => resolve({ status: res.statusCode, headers: res.headers, body: Buffer.concat(chunks).toString('utf-8') }));
    }).on('error', reject);
  });
}

test('proxy caches GET responses and reports stats', async () => {
  let backendCounter = 0;
  const backend = http.createServer((req, res) => {
    if (req.url === '/item') {
      backendCounter += 1;
      res.writeHead(200, {
        'content-type': 'application/json',
        'cache-control': 'public, max-age=60',
      });
      res.end(JSON.stringify({ value: backendCounter }));
      return;
    }
    res.writeHead(404);
    res.end('not found');
  });
  const backendPort = await listen(backend);

  const { server: proxy } = createProxyServer({ targetBaseUrl: `http://127.0.0.1:${backendPort}` });
  const proxyPort = await listen(proxy);

  const first = await getJson(`http://127.0.0.1:${proxyPort}/item`);
  const second = await getJson(`http://127.0.0.1:${proxyPort}/item`);
  const stats = await getJson(`http://127.0.0.1:${proxyPort}/stats`);

  assert.equal(first.status, 200);
  assert.equal(second.status, 200);
  assert.equal(JSON.parse(first.body).value, 1);
  assert.equal(JSON.parse(second.body).value, 1);
  assert.equal(second.headers['x-proxy-cache'], 'HIT');
  assert.equal(backendCounter, 1);

  const payload = JSON.parse(stats.body);
  assert.equal(payload.cacheHits, 1);
  assert.equal(payload.cacheMisses, 1);

  await new Promise((r) => proxy.close(r));
  await new Promise((r) => backend.close(r));
});
