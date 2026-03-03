"""Generic plugin registry used by ecosystem components."""

from collections.abc import Callable


class PluginRegistry:
    """Register and resolve plugins by name."""

    def __init__(self) -> None:
        self._items: dict[str, Callable[..., object]] = {}

    def register(self, name: str, factory: Callable[..., object]) -> None:
        if name in self._items:
            raise ValueError(f"Plugin '{name}' already exists")
        self._items[name] = factory

    def create(self, name: str, **kwargs: object) -> object:
        if name not in self._items:
            raise KeyError(name)
        return self._items[name](**kwargs)

    def names(self) -> list[str]:
        return sorted(self._items.keys())
