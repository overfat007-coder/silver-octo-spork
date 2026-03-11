# Brainfuck Interpreter (C++)

Minimal Brainfuck interpreter with:
- `.bf` file execution
- infinite-right tape memory
- command grouping optimization (`+/-` and `>/<` runs are grouped)
- debug mode (`--debug`) with step-by-step state output

## Build
```bash
g++ -std=c++17 -O2 -Wall -Wextra -pedantic tools/brainfuck/main.cpp -o tools/brainfuck/bf_interpreter
```

## Run
```bash
./tools/brainfuck/bf_interpreter tools/brainfuck/examples/hello.bf
```

## Debug mode
```bash
./tools/brainfuck/bf_interpreter tools/brainfuck/examples/hello.bf --debug
```
