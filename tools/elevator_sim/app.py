"""Tkinter GUI for 10-floor elevator simulator."""

from __future__ import annotations

import queue
import threading
import time
import tkinter as tk
from tkinter import ttk

from tools.elevator_sim.engine import ElevatorConfig, ElevatorEngine, ElevatorState


class ElevatorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Elevator Simulator (10 floors)")

        self.engine = ElevatorEngine(ElevatorConfig(floors=10))
        self.snapshot_queue: queue.Queue[dict] = queue.Queue()
        self._running = True

        self.status_var = tk.StringVar(value="Инициализация")
        self.floor_var = tk.StringVar(value="1")
        self.direction_var = tk.StringVar(value="•")
        self.queue_var = tk.StringVar(value="[]")

        self._build_ui()
        self._start_sim_thread()
        self.root.after(60, self._pull_snapshots)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_ui(self) -> None:
        top = ttk.Frame(self.root, padding=12)
        top.grid(row=0, column=0, sticky="nsew")

        ttk.Label(top, text="Текущий этаж:").grid(row=0, column=0, sticky="w")
        ttk.Label(top, textvariable=self.floor_var, font=("Arial", 16, "bold")).grid(row=0, column=1, sticky="w")

        ttk.Label(top, text="Направление:").grid(row=1, column=0, sticky="w")
        ttk.Label(top, textvariable=self.direction_var, font=("Arial", 14, "bold")).grid(row=1, column=1, sticky="w")

        ttk.Label(top, text="Состояние FSM:").grid(row=2, column=0, sticky="w")
        ttk.Label(top, textvariable=self.status_var).grid(row=2, column=1, sticky="w")

        ttk.Label(top, text="Очередь вызовов:").grid(row=3, column=0, sticky="w")
        ttk.Label(top, textvariable=self.queue_var).grid(row=3, column=1, sticky="w")

        self.canvas = tk.Canvas(top, width=180, height=260, bg="#0f172a", highlightthickness=0)
        self.canvas.grid(row=0, column=2, rowspan=6, padx=12)

        self.shaft = self.canvas.create_rectangle(60, 10, 120, 250, fill="#1e293b", outline="#94a3b8")
        self.car = self.canvas.create_rectangle(62, 220, 118, 246, fill="#fbbf24", outline="#fcd34d")
        self.left_door = self.canvas.create_rectangle(64, 222, 90, 244, fill="#334155", outline="")
        self.right_door = self.canvas.create_rectangle(90, 222, 116, 244, fill="#334155", outline="")

        buttons = ttk.Frame(self.root, padding=12)
        buttons.grid(row=1, column=0, sticky="nsew")

        hall = ttk.LabelFrame(buttons, text="Внешние вызовы")
        hall.grid(row=0, column=0, padx=4, sticky="n")
        for floor in range(10, 0, -1):
            row = 10 - floor
            ttk.Label(hall, text=f"{floor:2d}").grid(row=row, column=0)
            if floor < 10:
                ttk.Button(hall, text="↑", width=2, command=lambda f=floor: self.engine.request_hall(f, 1)).grid(row=row, column=1)
            if floor > 1:
                ttk.Button(hall, text="↓", width=2, command=lambda f=floor: self.engine.request_hall(f, -1)).grid(row=row, column=2)

        inside = ttk.LabelFrame(buttons, text="Внутренние кнопки")
        inside.grid(row=0, column=1, padx=4, sticky="n")
        for floor in range(10, 0, -1):
            idx = 10 - floor
            ttk.Button(inside, text=str(floor), width=4, command=lambda f=floor: self.engine.request_inside(f)).grid(row=idx // 2, column=idx % 2)

        controls = ttk.LabelFrame(buttons, text="Управление")
        controls.grid(row=0, column=2, padx=4, sticky="n")
        ttk.Button(controls, text="Авария ON", command=lambda: self.engine.set_emergency(True)).grid(row=0, column=0, pady=2)
        ttk.Button(controls, text="Авария OFF", command=lambda: self.engine.set_emergency(False)).grid(row=1, column=0, pady=2)

    def _start_sim_thread(self) -> None:
        def loop() -> None:
            prev = time.perf_counter()
            while self._running:
                now = time.perf_counter()
                dt = now - prev
                prev = now
                self.engine.step(dt)
                self.snapshot_queue.put(
                    {
                        "floor": self.engine.current_floor,
                        "state": self.engine.state.value,
                        "direction": self.engine.direction,
                        "queue": sorted(self.engine.active_requests()),
                        "position": self.engine.position_m,
                        "door": self.engine.door_open_ratio,
                    }
                )
                time.sleep(0.03)

        threading.Thread(target=loop, daemon=True).start()

    def _pull_snapshots(self) -> None:
        last = None
        while not self.snapshot_queue.empty():
            last = self.snapshot_queue.get_nowait()
        if last:
            self.floor_var.set(str(last["floor"]))
            self.status_var.set(last["state"])
            self.direction_var.set("↑" if last["direction"] > 0 else "↓" if last["direction"] < 0 else "•")
            self.queue_var.set(str(last["queue"]))
            self._render_car(last["position"], last["door"])
        self.root.after(60, self._pull_snapshots)

    def _render_car(self, position_m: float, door_open_ratio: float) -> None:
        max_pos = self.engine.floor_to_position(10)
        y_norm = position_m / max_pos if max_pos > 0 else 0
        y_bottom = 246 - y_norm * 220
        y_top = y_bottom - 24

        self.canvas.coords(self.car, 62, y_top, 118, y_bottom)

        half_open = 14 * door_open_ratio
        self.canvas.coords(self.left_door, 64, y_top + 2, 90 - half_open, y_bottom - 2)
        self.canvas.coords(self.right_door, 90 + half_open, y_top + 2, 116, y_bottom - 2)

    def _on_close(self) -> None:
        self._running = False
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    ElevatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
