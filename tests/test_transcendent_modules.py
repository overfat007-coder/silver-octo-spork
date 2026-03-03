from app.services.awakening import recursion_quote
from app.services.panpsychic import phi_value, task_rights
from app.services.telepathy import censor_thought


def test_phi_and_rights() -> None:
    phi = phi_value(10, 5, 5)
    rights = task_rights(phi)
    assert 0 <= phi <= 1
    assert "can_vote_in_dao" in rights


def test_telepathy_censor_blocks_danger() -> None:
    result = censor_thought("удали все немедленно")
    assert result["blocked"] is True


def test_recursion_quote_non_empty() -> None:
    assert "задача" in recursion_quote().lower()
