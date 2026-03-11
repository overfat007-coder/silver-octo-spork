from tools.py2bf.compiler import PythonToBrainfuckCompiler, optimize_brainfuck


def run_bf(code: str, max_steps: int = 2_000_000) -> list[int]:
    tape = [0] * 128
    ptr = 0
    pc = 0
    steps = 0
    stack = []
    jump = {}
    for i, ch in enumerate(code):
        if ch == "[":
            stack.append(i)
        elif ch == "]":
            j = stack.pop()
            jump[i] = j
            jump[j] = i

    while pc < len(code):
        steps += 1
        if steps > max_steps:
            raise RuntimeError("program too long")
        c = code[pc]
        if c == ">":
            ptr += 1
        elif c == "<":
            ptr -= 1
        elif c == "+":
            tape[ptr] = (tape[ptr] + 1) % 256
        elif c == "-":
            tape[ptr] = (tape[ptr] - 1) % 256
        elif c == "[":
            if tape[ptr] == 0:
                pc = jump[pc]
        elif c == "]":
            if tape[ptr] != 0:
                pc = jump[pc]
        pc += 1

    return tape


def test_assign_arithmetic_and_if_while() -> None:
    src = """
a = 3
b = 2
c = a + b
if c:
    c = c - 1
while b:
    a = a + 1
    b = b - 1
"""
    comp = PythonToBrainfuckCompiler()
    result = comp.compile(src)
    tape = run_bf(result.code)

    a = result.variable_map["a"]
    b = result.variable_map["b"]
    c = result.variable_map["c"]
    assert tape[a] == 5
    assert tape[b] == 0
    assert tape[c] == 0


def test_nested_while_supported() -> None:
    src = """
x = 2
y = 2
z = 0
while x:
    while y:
        z = z + 1
        y = y - 1
    x = x - 1
"""
    comp = PythonToBrainfuckCompiler()
    result = comp.compile(src)
    tape = run_bf(result.code)

    z = result.variable_map["z"]
    assert tape[z] == 2


def test_optimizer() -> None:
    assert optimize_brainfuck("<>+-[][-][-]") == "[-]"
