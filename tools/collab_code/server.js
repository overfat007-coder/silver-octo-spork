import http from 'http';
import crypto from 'crypto';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { SimpleReplicatedText } from './crdt.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const publicDir = path.join(__dirname, 'public');

const doc = new SimpleReplicatedText();
const cursors = new Map();
const clients = new Set();
let lamport = 0;

function sendFrame(sock, data) {
  const payload = Buffer.from(data);
  const len = payload.length;
  let header;
  if (len < 126) {
    header = Buffer.from([0x81, len]);
  } else {
    header = Buffer.from([0x81, 126, (len >> 8) & 0xff, len & 0xff]);
  }
  sock.write(Buffer.concat([header, payload]));
}

function decodeFrames(buffer) {
  const messages = [];
  let off = 0;
  while (off + 2 <= buffer.length) {
    const b1 = buffer[off];
    const b2 = buffer[off + 1];
    const masked = (b2 & 0x80) !== 0;
    let len = b2 & 0x7f;
    let hdr = 2;
    if (len === 126) {
      if (off + 4 > buffer.length) break;
      len = (buffer[off + 2] << 8) | buffer[off + 3];
      hdr = 4;
    }
    const maskLen = masked ? 4 : 0;
    if (off + hdr + maskLen + len > buffer.length) break;
    let payload = buffer.slice(off + hdr + maskLen, off + hdr + maskLen + len);
    if (masked) {
      const mask = buffer.slice(off + hdr, off + hdr + 4);
      payload = Buffer.from(payload.map((v, i) => v ^ mask[i % 4]));
    }
    if ((b1 & 0x0f) === 0x1) messages.push(payload.toString('utf-8'));
    off += hdr + maskLen + len;
  }
  return { messages, rest: buffer.slice(off) };
}

function broadcast(obj) {
  const raw = JSON.stringify(obj);
  for (const c of clients) sendFrame(c, raw);
}

const server = http.createServer((req, res) => {
  const urlPath = req.url === '/' ? '/index.html' : req.url;
  const file = path.join(publicDir, urlPath);
  if (!file.startsWith(publicDir) || !fs.existsSync(file)) {
    res.statusCode = 404; res.end('not found'); return;
  }
  const ext = path.extname(file);
  const ctype = ext === '.html' ? 'text/html' : ext === '.js' ? 'application/javascript' : 'text/plain';
  res.setHeader('Content-Type', ctype);
  res.end(fs.readFileSync(file));
});

server.on('upgrade', (req, socket) => {
  const key = req.headers['sec-websocket-key'];
  if (!key) return socket.destroy();
  const accept = crypto.createHash('sha1').update(key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').digest('base64');
  socket.write([
    'HTTP/1.1 101 Switching Protocols',
    'Upgrade: websocket',
    'Connection: Upgrade',
    `Sec-WebSocket-Accept: ${accept}`,
    '\r\n',
  ].join('\r\n'));

  clients.add(socket);
  const clientId = `${Date.now()}-${Math.random().toString(16).slice(2, 8)}`;
  sendFrame(socket, JSON.stringify({ type: 'init', clientId, text: doc.toText(), cursors: Object.fromEntries(cursors) }));

  let acc = Buffer.alloc(0);
  socket.on('data', (chunk) => {
    acc = Buffer.concat([acc, chunk]);
    const { messages, rest } = decodeFrames(acc);
    acc = rest;
    for (const m of messages) {
      const msg = JSON.parse(m);
      if (msg.type === 'insert') {
        lamport = Math.max(lamport, msg.id.lamport) + 1;
        msg.id.lamport = lamport;
        doc.applyInsert(msg);
        broadcast({ type: 'insert', op: msg });
      } else if (msg.type === 'delete') {
        doc.applyDelete(msg);
        broadcast({ type: 'delete', op: msg });
      } else if (msg.type === 'cursor') {
        cursors.set(msg.clientId, { name: msg.name, pos: msg.pos });
        broadcast({ type: 'cursor', cursors: Object.fromEntries(cursors) });
      }
    }
  });
  socket.on('close', () => clients.delete(socket));
  socket.on('end', () => clients.delete(socket));
  socket.on('error', () => clients.delete(socket));
});

const port = process.env.PORT || 9400;
server.listen(port, () => console.log(`collab code editor listening on http://localhost:${port}`));
