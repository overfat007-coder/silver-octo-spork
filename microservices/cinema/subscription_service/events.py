"""RabbitMQ publisher for subscription events."""

import json
import os

RABBIT_URL = os.getenv("RABBIT_URL", "amqp://guest:guest@rabbitmq:5672/")


def publish_subscription_event(user_id: str, active: bool) -> bool:
    try:
        import pika

        params = pika.URLParameters(RABBIT_URL)
        conn = pika.BlockingConnection(params)
        ch = conn.channel()
        ch.exchange_declare(exchange="cinema.events", exchange_type="topic", durable=True)
        payload = json.dumps({"user_id": user_id, "active": active})
        ch.basic_publish(exchange="cinema.events", routing_key="subscription.status.changed", body=payload)
        conn.close()
        return True
    except Exception:
        return False
