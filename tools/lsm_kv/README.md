# LSM KV Store (Educational)

Упрощенное NoSQL key-value хранилище на диске в стиле LSM Tree.

## Реализовано
- `PUT`, `GET`, `DELETE`
- Персистентность между перезапусками:
  - WAL (`wal.log`)
  - SSTables (`sst_*.sst` + `.meta`)
- MemTable в памяти
- Flush MemTable -> SSTable
- Фоновая compaction (merge + GC tombstones)
- Bloom Filter на каждый SSTable для ускорения поиска

## Запуск REPL
```bash
python -m tools.lsm_kv.main --data-dir ./.lsm_data
```

Команды:
- `PUT key value`
- `GET key`
- `DELETE key`
- `COMPACT`
- `STATS`
- `EXIT`
