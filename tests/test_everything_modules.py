from app.services.finale import final_answer, is_task_proof
from app.services.omni import simulation_probability
from app.services.oracle import ask


def test_everything_proof_keys() -> None:
    proof = is_task_proof()
    assert {"sun", "rain", "human", "god"}.issubset(proof.keys())


def test_sim_probability_high() -> None:
    assert simulation_probability() > 0.99


def test_oracle_forbidden() -> None:
    result = ask("Кто создал создателя?")
    assert result["answer"] == "Тебе лучше не знать"


def test_final_answer_non_empty() -> None:
    assert "код" in final_answer().lower()
