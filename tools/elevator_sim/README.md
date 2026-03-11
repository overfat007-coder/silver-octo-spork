# Elevator Simulator (Tkinter)

Simulation of an elevator in a 10-floor building with:
- FSM states: `Стоит_открыт`, `Стоит_закрыт`, `Движение_вверх`, `Движение_вниз`, `Авария`
- movement physics: acceleration/deceleration and travel timing
- scheduling of internal and external requests
- door animation (open/close)
- multithreaded simulation loop + UI thread rendering
- current floor, direction, and queue display

## Run
```bash
python -m tools.elevator_sim.app
```
