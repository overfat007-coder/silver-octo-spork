"""JSON serializer for API payload persistence and interchange."""

import json


class JsonSerializer:
    """Serializer based on Python stdlib `json`."""

    name = "json"

    def dumps(self, value: object) -> str:
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))

    def loads(self, payload: str) -> object:
        return json.loads(payload)
