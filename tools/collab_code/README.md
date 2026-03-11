# Multi-user code editor (CRDT, Simple Replicated Text)

Учебный realtime-редактор кода (textarea + WebSocket backend) с CRDT без OT.

## Что реализовано
- Node.js сервер (built-in http + native WebSocket handshake)
- CRDT на основе Simple Replicated Text (RGA-подобный):
  - вставка символов с `id = {lamport, clientId, seq}` и `leftId`
  - удаление через tombstone
  - детерминированный merge при конкурентных вставках
- Логические timestamp (Lamport) на сервере
- Ретрансляция операций вставки/удаления клиентам
- Курсоры пользователей с именами (позиции)

## Запуск
```bash
cd tools/collab_code
npm install
npm start
```
Откройте несколько вкладок `http://localhost:9400`.

## Тесты
```bash
npm test
```
