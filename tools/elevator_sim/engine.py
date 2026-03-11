"""Elevator simulation engine with FSM, scheduling, and simple motion physics."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ElevatorState(str, Enum):
    STOIT_OTKRYT = "Стоит_открыт"
    STOIT_ZAKRYT = "Стоит_закрыт"
    DVIZHENIE_VVERH = "Движение_вверх"
    DVIZHENIE_VNIZ = "Движение_вниз"
    AVARIYA = "Авария"


@dataclass
class ElevatorConfig:
    floors: int = 10
    floor_height_m: float = 3.0
    max_speed_m_s: float = 2.0
    acceleration_m_s2: float = 1.0
    door_time_s: float = 2.0


@dataclass
class ElevatorEngine:
    config: ElevatorConfig = field(default_factory=ElevatorConfig)
    state: ElevatorState = ElevatorState.STOIT_ZAKRYT
    position_m: float = 0.0
    velocity_m_s: float = 0.0
    door_open_ratio: float = 0.0
    door_timer_s: float = 0.0
    emergency: bool = False

    requests_up: set[int] = field(default_factory=set)
    requests_down: set[int] = field(default_factory=set)
    requests_inside: set[int] = field(default_factory=set)

    def __post_init__(self) -> None:
        self.position_m = self.floor_to_position(1)

    @property
    def current_floor(self) -> int:
        floor = round(self.position_m / self.config.floor_height_m) + 1
        return max(1, min(self.config.floors, floor))

    @property
    def direction(self) -> int:
        if self.velocity_m_s > 1e-4:
            return 1
        if self.velocity_m_s < -1e-4:
            return -1
        if self.state == ElevatorState.DVIZHENIE_VVERH:
            return 1
        if self.state == ElevatorState.DVIZHENIE_VNIZ:
            return -1
        return 0

    def floor_to_position(self, floor: int) -> float:
        return (floor - 1) * self.config.floor_height_m

    def request_inside(self, floor: int) -> None:
        if 1 <= floor <= self.config.floors:
            self.requests_inside.add(floor)

    def request_hall(self, floor: int, direction: int) -> None:
        if not (1 <= floor <= self.config.floors):
            return
        if direction >= 0:
            self.requests_up.add(floor)
        else:
            self.requests_down.add(floor)

    def set_emergency(self, value: bool) -> None:
        self.emergency = value
        if value:
            self.state = ElevatorState.AVARIYA
            self.velocity_m_s = 0.0
        elif self.state == ElevatorState.AVARIYA:
            self.state = ElevatorState.STOIT_ZAKRYT

    def active_requests(self) -> set[int]:
        return self.requests_inside | self.requests_up | self.requests_down

    def next_target(self) -> int | None:
        requests = self.active_requests()
        if not requests:
            return None

        current = self.current_floor
        if self.direction >= 0:
            higher = sorted(f for f in requests if f >= current)
            if higher:
                return higher[0]
            return sorted(requests, reverse=True)[0]

        lower = sorted((f for f in requests if f <= current), reverse=True)
        if lower:
            return lower[0]
        return sorted(requests)[0]

    def _consume_floor_requests(self, floor: int) -> None:
        self.requests_inside.discard(floor)
        self.requests_up.discard(floor)
        self.requests_down.discard(floor)

    def _begin_door_open(self) -> None:
        self.state = ElevatorState.STOIT_OTKRYT
        self.velocity_m_s = 0.0
        self.door_timer_s = self.config.door_time_s

    def step(self, dt_s: float) -> None:
        if self.state == ElevatorState.AVARIYA:
            return

        # door animation
        if self.state == ElevatorState.STOIT_OTKRYT:
            self.door_open_ratio = min(1.0, self.door_open_ratio + dt_s * 2.5)
            self.door_timer_s -= dt_s
            if self.door_timer_s <= 0:
                self.state = ElevatorState.STOIT_ZAKRYT
            return

        if self.state == ElevatorState.STOIT_ZAKRYT and self.door_open_ratio > 0.0:
            self.door_open_ratio = max(0.0, self.door_open_ratio - dt_s * 2.5)

        target_floor = self.next_target()
        if target_floor is None:
            self.velocity_m_s = 0.0
            self.state = ElevatorState.STOIT_ZAKRYT
            return

        target_pos = self.floor_to_position(target_floor)
        distance = target_pos - self.position_m

        if abs(distance) < 0.02 and abs(self.velocity_m_s) < 0.05:
            self.position_m = target_pos
            self._consume_floor_requests(target_floor)
            self._begin_door_open()
            return

        direction = 1.0 if distance > 0 else -1.0
        self.state = ElevatorState.DVIZHENIE_VVERH if direction > 0 else ElevatorState.DVIZHENIE_VNIZ

        braking_distance = (self.velocity_m_s * self.velocity_m_s) / (2 * self.config.acceleration_m_s2)
        should_brake = abs(distance) <= braking_distance + 0.05

        if should_brake:
            accel = -self.config.acceleration_m_s2 * (1 if self.velocity_m_s > 0 else -1)
        else:
            accel = self.config.acceleration_m_s2 * direction

        self.velocity_m_s += accel * dt_s
        self.velocity_m_s = max(-self.config.max_speed_m_s, min(self.velocity_m_s, self.config.max_speed_m_s))

        self.position_m += self.velocity_m_s * dt_s

        min_pos = self.floor_to_position(1)
        max_pos = self.floor_to_position(self.config.floors)
        self.position_m = max(min_pos, min(self.position_m, max_pos))

        if self.position_m in {min_pos, max_pos}:
            self.velocity_m_s = 0.0
