import test from 'node:test';
import assert from 'node:assert/strict';
import { SimpleReplicatedText } from '../crdt.js';

test('insert/delete merge', () => {
  const c = new SimpleReplicatedText();
  c.applyInsert({ id: { lamport: 1, clientId: 'a', seq: 1 }, leftId: null, ch: 'A' });
  c.applyInsert({ id: { lamport: 2, clientId: 'b', seq: 1 }, leftId: null, ch: 'B' });
  assert.equal(c.toText().length, 2);
  c.applyDelete({ targetId: { lamport: 1, clientId: 'a', seq: 1 } });
  assert.equal(c.toText(), 'B');
});
