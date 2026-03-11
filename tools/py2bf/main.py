from __future__ import annotations

import argparse
from pathlib import Path

from tools.py2bf.compiler import PythonToBrainfuckCompiler


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile tiny Python subset to Brainfuck")
    parser.add_argument("source", help="Path to source .py file")
    parser.add_argument("--output", "-o", default="out.bf", help="Output Brainfuck file")
    args = parser.parse_args()

    source_path = Path(args.source)
    output_path = Path(args.output)

    compiler = PythonToBrainfuckCompiler()
    result = compiler.compile(source_path.read_text(encoding="utf-8"))
    output_path.write_text(result.code, encoding="utf-8")

    print(f"Compiled -> {output_path}")
    print("Variable map:")
    for name, cell in sorted(result.variable_map.items(), key=lambda kv: kv[1]):
        print(f"  {name}: cell {cell}")


if __name__ == "__main__":
    main()
