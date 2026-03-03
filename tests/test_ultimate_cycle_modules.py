from app.services.ultimate_cycle import akasha_possible, return_to_source, toe_equation


def test_akasha_possible_has_infinite_pages_marker() -> None:
    result = akasha_possible(page=2, size=3)
    assert result["total_pages"] == "∞"
    assert len(result["items"]) == 3


def test_toe_equation_contains_action_term() -> None:
    assert "S_tasks" in toe_equation()


def test_return_to_source_contains_codex_script_lines() -> None:
    result = return_to_source()
    joined = "\n".join(result["script"])
    assert "В начале было ТЗ" in joined
    assert "И сказала Codex" not in joined
    assert "# Конец." in joined
