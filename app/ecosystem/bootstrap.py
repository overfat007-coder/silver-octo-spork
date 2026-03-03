"""Bootstrap registry with default ecosystem implementations."""

from app.ecosystem.registry import PluginRegistry
from app.ecosystem.serializers.csv_serializer import CsvSerializer
from app.ecosystem.serializers.json_serializer import JsonSerializer
from app.ecosystem.storage.memory_kv import MemoryKV
from app.ecosystem.storage.sqlite_kv import SqliteKV


def build_default_registry() -> PluginRegistry:
    """Create plugin registry with default serializer/storage adapters."""
    registry = PluginRegistry()
    registry.register("serializer:json", JsonSerializer)
    registry.register("serializer:csv", CsvSerializer)
    registry.register("store:memory", MemoryKV)
    registry.register("store:sqlite", SqliteKV)
    return registry
