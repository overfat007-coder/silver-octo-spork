import crypto from 'node:crypto';
import fs from 'node:fs/promises';
import path from 'node:path';

const CACHE_ROOT = process.env.CACHE_DIR || path.resolve('tools/reverse_proxy/cache');

function keyToPath(url) {
  const hash = crypto.createHash('sha256').update(url).digest('hex');
  const dir = path.join(CACHE_ROOT, hash.slice(0, 2), hash.slice(2));
  return { hash, dir };
}

export function parseCacheControl(value) {
  if (!value) return { cacheable: false, maxAge: 0 };
  const parts = value.toLowerCase().split(',').map((x) => x.trim());
  if (parts.includes('no-store')) return { cacheable: false, maxAge: 0 };

  const maxAgePart = parts.find((p) => p.startsWith('max-age='));
  if (!maxAgePart) return { cacheable: false, maxAge: 0 };
  const parsed = Number.parseInt(maxAgePart.split('=')[1], 10);
  if (!Number.isFinite(parsed) || parsed <= 0) return { cacheable: false, maxAge: 0 };
  return { cacheable: true, maxAge: parsed };
}

export async function readCache(url) {
  const { dir } = keyToPath(url);
  try {
    const metaRaw = await fs.readFile(path.join(dir, 'meta.json'), 'utf-8');
    const meta = JSON.parse(metaRaw);
    const now = Date.now();
    if (now > meta.expiresAt) return null;
    const body = await fs.readFile(path.join(dir, 'body.bin'));
    return { statusCode: meta.statusCode, headers: meta.headers, body };
  } catch {
    return null;
  }
}

export async function writeCache(url, statusCode, headers, body) {
  const cc = parseCacheControl(headers['cache-control']);
  if (!cc.cacheable) return false;

  const { dir } = keyToPath(url);
  await fs.mkdir(dir, { recursive: true });
  const meta = {
    url,
    statusCode,
    headers,
    expiresAt: Date.now() + cc.maxAge * 1000,
  };
  await fs.writeFile(path.join(dir, 'meta.json'), JSON.stringify(meta, null, 2), 'utf-8');
  await fs.writeFile(path.join(dir, 'body.bin'), body);
  return true;
}
