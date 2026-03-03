from app.ecosystem.serializers.json_serializer import JsonSerializer


def test_json_roundtrip() -> None:
    s = JsonSerializer()
    payload = s.dumps({"a": 1})
    assert s.loads(payload) == {"a": 1}
