"""Media service for metadata persistence."""

from app.mobile.common.store import InMemoryStore
from app.mobile.media.validate import validate


class MediaService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def upload_meta(self, media_id: str, filename: str, size: int) -> dict:
        validate(filename, size)
        record = {"media_id": media_id, "filename": filename, "size": size}
        self.store.media[media_id] = record
        return record
