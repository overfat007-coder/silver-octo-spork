# Учебная распределенная система голосования на блокчейне

Прототип на Python:
- P2P-сеть нод через TCP сокеты;
- голос как подписанная транзакция (RSA подпись избирателя);
- сбор голосов в блок;
- консенсус по простому большинству валидаторов;
- веб-интерфейс для голосования;
- учебная RSA blind signature (ослепление сообщения перед подписью органом-эмитентом).

## Важно
Это демонстрационный код для обучения, а не production-решение.

## Запуск одной ноды
```bash
python -m tools.blockchain_vote.main --host 127.0.0.1 --port 8100
```

HTTP: `8100`, P2P: `9100` (внутренне `port + 1000`).

## Запуск с конфигом
```bash
python -m tools.blockchain_vote.main --config tools/blockchain_vote/config.example.json
```

## Пример 3 нод
```bash
python -m tools.blockchain_vote.main --host 127.0.0.1 --port 8100 --peer 127.0.0.1:9101 --peer 127.0.0.1:9102
python -m tools.blockchain_vote.main --host 127.0.0.1 --port 8101 --peer 127.0.0.1:9100 --peer 127.0.0.1:9102
python -m tools.blockchain_vote.main --host 127.0.0.1 --port 8102 --peer 127.0.0.1:9100 --peer 127.0.0.1:9101
```

Откройте `http://127.0.0.1:8100/` и отправляйте голоса, затем нажмите `Propose block`.
