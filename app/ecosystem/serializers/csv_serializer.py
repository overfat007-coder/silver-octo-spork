"""CSV serializer for tabular exports and BI pipelines."""

import csv
import io


class CsvSerializer:
    """Serialize list[dict[str, str]] to CSV and back."""

    name = "csv"

    def dumps(self, value: object) -> str:
        rows = value if isinstance(value, list) else []
        if not rows:
            return ""
        fieldnames = sorted({key for row in rows for key in row.keys()})
        out = io.StringIO()
        writer = csv.DictWriter(out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        return out.getvalue()

    def loads(self, payload: str) -> object:
        if not payload.strip():
            return []
        reader = csv.DictReader(io.StringIO(payload))
        return [dict(row) for row in reader]
