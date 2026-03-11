export function compareId(a, b) {
  if (a.lamport !== b.lamport) return a.lamport - b.lamport;
  if (a.clientId !== b.clientId) return a.clientId < b.clientId ? -1 : 1;
  return a.seq - b.seq;
}

export class SimpleReplicatedText {
  constructor() {
    this.items = []; // {id,ch,deleted}
  }

  has(id) {
    return this.items.some((i) => sameId(i.id, id));
  }

  applyInsert(op) {
    if (this.has(op.id)) return;
    const item = { id: op.id, ch: op.ch, deleted: false };
    if (!op.leftId) {
      this.items.unshift(item);
      return;
    }
    const leftIndex = this.items.findIndex((i) => sameId(i.id, op.leftId));
    if (leftIndex === -1) {
      this.items.push(item);
      return;
    }
    let idx = leftIndex + 1;
    while (idx < this.items.length) {
      const cur = this.items[idx];
      if (!cur.leftId || !sameId(cur.leftId, op.leftId)) break;
      if (compareId(cur.id, op.id) > 0) break;
      idx += 1;
    }
    item.leftId = op.leftId;
    this.items.splice(idx, 0, item);
  }

  applyDelete(op) {
    const it = this.items.find((i) => sameId(i.id, op.targetId));
    if (it) it.deleted = true;
  }

  toText() {
    return this.items.filter((i) => !i.deleted).map((i) => i.ch).join("");
  }

  visibleWithIds() {
    return this.items.filter((i) => !i.deleted).map((i) => ({ id: i.id, ch: i.ch }));
  }
}

function sameId(a, b) {
  return a && b && a.lamport === b.lamport && a.clientId === b.clientId && a.seq === b.seq;
}
