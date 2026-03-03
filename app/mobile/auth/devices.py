"""Device registry for account sessions."""


class DeviceRegistry:
    def __init__(self) -> None:
        self._devices: dict[str, set[str]] = {}

    def register(self, user_id: str, device_id: str) -> None:
        self._devices.setdefault(user_id, set()).add(device_id)

    def list_devices(self, user_id: str) -> list[str]:
        return sorted(self._devices.get(user_id, set()))
