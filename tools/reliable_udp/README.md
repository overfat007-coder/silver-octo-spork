# Reliable UDP (Educational mini-TCP)

Учебный транспортный протокол поверх UDP с гарантией доставки больших файлов.

## Реализовано
- Клиентская и серверная библиотеки:
  - `tools.reliable_udp.client.ReliableUDPClient`
  - `tools.reliable_udp.server.ReliableUDPServer`
- Надежность:
  - нумерация сегментов `seq`
  - cumulative `ACK`
  - тайм-ауты и повторные отправки
  - буферизация на приемнике и упорядоченная сборка
- Простой аналог TCP Reno:
  - `cwnd`
  - `slow start`
  - `ssthresh`
  - реакция на тайм-аут (сброс окна)
  - fast retransmit по duplicate ACK
- Симуляция потерь через `drop_rate` на отправке (`UnreliableSocket`).

## CLI демо
### Сервер
```bash
python -m tools.reliable_udp.main server --host 127.0.0.1 --port 9200 --output-dir ./received --drop-rate 0.1
```

### Клиент
```bash
python -m tools.reliable_udp.main client --host 127.0.0.1 --port 9200 --file ./big.bin --drop-rate 0.1
```
