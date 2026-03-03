"""Module 53 - Oracle task simulation."""

import hashlib


FORBIDDEN = {"как удалить систему", "кто создал создателя", "есть ли жизнь после дедлайна"}


def ask(question: str) -> dict:
    q = question.lower().strip()
    qh = hashlib.sha256(q.encode()).hexdigest()
    if any(f in q for f in FORBIDDEN):
        return {"question_hash": qh, "answer": "Тебе лучше не знать"}
    if "смысл" in q:
        return {"question_hash": qh, "answer": "42"}
    return {"question_hash": qh, "answer": "А сам как думаешь?"}


def prophecy() -> dict:
    return {"prediction": "Скоро появится задача, которая изменит архитектуру", "confidence": 0.999}
