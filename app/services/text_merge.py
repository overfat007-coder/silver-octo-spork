"""Pure text merge helpers used by realtime collaboration."""


def merge_text(old: str, incoming: str) -> str:
    if incoming.startswith(old) or old.startswith(incoming):
        return incoming if len(incoming) >= len(old) else old
    if incoming == old:
        return old
    return f"{old}\n----\n{incoming}"
