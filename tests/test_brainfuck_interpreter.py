import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "tools" / "brainfuck" / "main.cpp"
BIN = ROOT / "tools" / "brainfuck" / "bf_interpreter"
HELLO = ROOT / "tools" / "brainfuck" / "examples" / "hello.bf"


def build_interpreter() -> None:
    subprocess.run(
        ["g++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-pedantic", str(SRC), "-o", str(BIN)],
        check=True,
    )


def test_brainfuck_hello_world() -> None:
    build_interpreter()
    proc = subprocess.run([str(BIN), str(HELLO)], check=True, capture_output=True, text=True)
    assert "Hello World!" in proc.stdout


def test_brainfuck_debug_mode(tmp_path) -> None:
    build_interpreter()
    prog = tmp_path / "tiny.bf"
    prog.write_text("+++.")
    proc = subprocess.run(
        [str(BIN), str(prog), "--debug"],
        input="\n\n",
        capture_output=True,
        text=True,
        check=True,
    )
    assert "[debug]" in proc.stderr
