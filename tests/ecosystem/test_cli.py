from app.ecosystem.cli.ecosystem_cli import main


def test_cli_ping(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["ping"]) == 0
    out = capsys.readouterr().out
    assert "pong" in out
