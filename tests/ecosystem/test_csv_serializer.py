from app.ecosystem.serializers.csv_serializer import CsvSerializer


def test_csv_roundtrip() -> None:
    s = CsvSerializer()
    rows = [{"id": "1", "name": "n"}]
    assert s.loads(s.dumps(rows)) == rows
