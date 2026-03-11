class SimpleReplicatedText {
  constructor() { this.items = []; }
  has(id) { return this.items.some((i) => sameId(i.id, id)); }
  applyInsert(op) {
    if (this.has(op.id)) return;
    const item = { id: op.id, ch: op.ch, deleted: false, leftId: op.leftId };
    if (!op.leftId) { this.items.unshift(item); return; }
    const leftIndex = this.items.findIndex((i) => sameId(i.id, op.leftId));
    if (leftIndex === -1) { this.items.push(item); return; }
    let idx = leftIndex + 1;
    while (idx < this.items.length) {
      const cur = this.items[idx];
      if (!cur.leftId || !sameId(cur.leftId, op.leftId)) break;
      if (compareId(cur.id, op.id) > 0) break;
      idx += 1;
    }
    this.items.splice(idx, 0, item);
  }
  applyDelete(op) { const it = this.items.find((i) => sameId(i.id, op.targetId)); if (it) it.deleted = true; }
  toText() { return this.items.filter((i) => !i.deleted).map((i) => i.ch).join(''); }
  visibleWithIds() { return this.items.filter((i) => !i.deleted).map((i) => ({ id: i.id, ch: i.ch })); }
}
function sameId(a,b){return a&&b&&a.lamport===b.lamport&&a.clientId===b.clientId&&a.seq===b.seq}
function compareId(a,b){if(a.lamport!==b.lamport)return a.lamport-b.lamport;if(a.clientId!==b.clientId)return a.clientId<b.clientId?-1:1;return a.seq-b.seq}

const ws = new WebSocket(`ws://${location.host}`);
const editor = document.getElementById('editor');
const nameInput = document.getElementById('name');
const cursorsEl = document.getElementById('cursors');

const crdt = new SimpleReplicatedText();
let clientId = '';
let seq = 0;
let lamport = 0;
let applyingRemote = false;

function idAtVisibleIndex(idx) {
  const vis = crdt.visibleWithIds();
  return idx <= 0 ? null : (vis[idx - 1]?.id ?? null);
}
function renderCursors(cursors) {
  cursorsEl.innerHTML = '';
  Object.entries(cursors).forEach(([cid, c]) => {
    if (!c) return;
    const span = document.createElement('span');
    span.className = 'pill';
    span.textContent = `${c.name || cid}: ${c.pos}`;
    cursorsEl.appendChild(span);
  });
}

ws.onmessage = (ev) => {
  const msg = JSON.parse(ev.data);
  if (msg.type === 'init') {
    clientId = msg.clientId;
    seq = 0;
    for (const ch of msg.text) {
      seq += 1;
      crdt.applyInsert({ id: { lamport: seq, clientId: 'bootstrap', seq }, leftId: idAtVisibleIndex(1e9), ch });
    }
    editor.value = crdt.toText();
    prev = editor.value;
    renderCursors(msg.cursors || {});
    return;
  }
  if (msg.type === 'insert') { applyingRemote = true; crdt.applyInsert(msg.op); editor.value = crdt.toText(); applyingRemote = false; return; }
  if (msg.type === 'delete') { applyingRemote = true; crdt.applyDelete(msg.op); editor.value = crdt.toText(); applyingRemote = false; return; }
  if (msg.type === 'cursor') renderCursors(msg.cursors || {});
};

let prev = '';
editor.addEventListener('input', () => {
  if (applyingRemote) return;
  const cur = editor.value;
  let i = 0;
  while (i < prev.length && i < cur.length && prev[i] === cur[i]) i++;
  if (cur.length > prev.length) {
    const inserted = cur.slice(i, i + (cur.length - prev.length));
    for (const ch of inserted) {
      seq += 1; lamport += 1;
      const op = { type:'insert', id:{lamport,clientId,seq}, leftId:idAtVisibleIndex(i), ch };
      crdt.applyInsert(op); ws.send(JSON.stringify(op)); i += 1;
    }
  } else if (cur.length < prev.length) {
    const target = crdt.visibleWithIds()[i];
    if (target) { const op = { type:'delete', targetId: target.id }; crdt.applyDelete(op); ws.send(JSON.stringify(op)); }
  }
  prev = crdt.toText(); if (editor.value !== prev) editor.value = prev;
});

editor.addEventListener('keyup', () => {
  ws.send(JSON.stringify({ type:'cursor', clientId, name:nameInput.value || clientId, pos:editor.selectionStart }));
});
