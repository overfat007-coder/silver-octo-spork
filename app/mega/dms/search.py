"""Simple fulltext-like search over document titles."""


def search_titles(index: list[dict], phrase: str)->list[dict]:
    p=phrase.lower()
    return [d for d in index if p in d.get("title","").lower()]
