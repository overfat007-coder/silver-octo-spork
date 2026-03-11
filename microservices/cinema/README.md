# Cinema microservices prototype

Two interacting services:
- **Catalog Service** (`:8001`) with PostgreSQL-backed movies API (pagination + filtering).
- **Subscription Service** (`:8002`) with Redis cache for user subscription status.

Interaction:
- Catalog checks subscription status via HTTP dependency call.
- Subscription publishes status-change events to RabbitMQ (`cinema.events`).
- Catalog protects dependency calls with a Circuit Breaker.

## Run
```bash
docker compose -f microservices/cinema/docker-compose.yml up --build
```

## Key endpoints
- `GET /movies?page=1&page_size=10&genre=sci-fi&q=matrix&min_year=1990`
- `GET /protected/movies?user_id=u1`
- `GET /subscriptions/{user_id}/active`
- `POST /subscriptions/{user_id}` with `{"active": true}`
