#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

enum class OpType {
    Add,
    Move,
    Output,
    Input,
    JumpIfZero,
    JumpIfNotZero,
};

struct Op {
    OpType type;
    int argument{0};
    std::size_t jump_target{0};
};

struct Program {
    std::vector<Op> ops;
};

Program compile_program(const std::string& source) {
    Program program;
    std::vector<std::size_t> loop_stack;

    for (std::size_t i = 0; i < source.size();) {
        char c = source[i];

        if (c == '+' || c == '-') {
            int delta = 0;
            while (i < source.size() && (source[i] == '+' || source[i] == '-')) {
                delta += (source[i] == '+') ? 1 : -1;
                ++i;
            }
            if (delta != 0) {
                program.ops.push_back(Op{OpType::Add, delta, 0});
            }
            continue;
        }

        if (c == '>' || c == '<') {
            int delta = 0;
            while (i < source.size() && (source[i] == '>' || source[i] == '<')) {
                delta += (source[i] == '>') ? 1 : -1;
                ++i;
            }
            if (delta != 0) {
                program.ops.push_back(Op{OpType::Move, delta, 0});
            }
            continue;
        }

        if (c == '.') {
            program.ops.push_back(Op{OpType::Output, 0, 0});
            ++i;
            continue;
        }

        if (c == ',') {
            program.ops.push_back(Op{OpType::Input, 0, 0});
            ++i;
            continue;
        }

        if (c == '[') {
            program.ops.push_back(Op{OpType::JumpIfZero, 0, 0});
            loop_stack.push_back(program.ops.size() - 1);
            ++i;
            continue;
        }

        if (c == ']') {
            if (loop_stack.empty()) {
                throw std::runtime_error("Unmatched closing bracket ]");
            }
            std::size_t open_idx = loop_stack.back();
            loop_stack.pop_back();
            std::size_t close_idx = program.ops.size();
            program.ops.push_back(Op{OpType::JumpIfNotZero, 0, open_idx});
            program.ops[open_idx].jump_target = close_idx;
            ++i;
            continue;
        }

        ++i;  // ignore non-brainfuck symbols
    }

    if (!loop_stack.empty()) {
        throw std::runtime_error("Unmatched opening bracket [");
    }

    return program;
}

std::string op_name(OpType t) {
    switch (t) {
        case OpType::Add:
            return "ADD";
        case OpType::Move:
            return "MOVE";
        case OpType::Output:
            return "OUT";
        case OpType::Input:
            return "IN";
        case OpType::JumpIfZero:
            return "JZ";
        case OpType::JumpIfNotZero:
            return "JNZ";
    }
    return "UNKNOWN";
}

void ensure_tape_bounds(std::vector<std::uint8_t>& tape, std::size_t ptr) {
    if (ptr >= tape.size()) {
        tape.resize(ptr + 1, 0);
    }
}

void run_program(const Program& program, bool debug) {
    std::vector<std::uint8_t> tape(1, 0);
    std::size_t ptr = 0;
    std::size_t ip = 0;

    while (ip < program.ops.size()) {
        const Op& op = program.ops[ip];
        ensure_tape_bounds(tape, ptr);

        if (debug) {
            std::cerr << "[debug] ip=" << ip << " op=" << op_name(op.type)
                      << " arg=" << op.argument << " ptr=" << ptr
                      << " cell=" << static_cast<int>(tape[ptr]) << "\n";
            std::cerr << "        press ENTER for next step...";
            std::string line;
            std::getline(std::cin, line);
        }

        switch (op.type) {
            case OpType::Add: {
                int next = static_cast<int>(tape[ptr]) + op.argument;
                tape[ptr] = static_cast<std::uint8_t>(next & 0xFF);
                ++ip;
                break;
            }
            case OpType::Move: {
                long long next_ptr = static_cast<long long>(ptr) + op.argument;
                if (next_ptr < 0) {
                    throw std::runtime_error("Tape pointer moved to negative index");
                }
                ptr = static_cast<std::size_t>(next_ptr);
                ensure_tape_bounds(tape, ptr);
                ++ip;
                break;
            }
            case OpType::Output:
                std::cout << static_cast<char>(tape[ptr]);
                ++ip;
                break;
            case OpType::Input: {
                int ch = std::cin.get();
                if (ch == EOF) {
                    tape[ptr] = 0;
                } else {
                    tape[ptr] = static_cast<std::uint8_t>(ch);
                }
                ++ip;
                break;
            }
            case OpType::JumpIfZero:
                if (tape[ptr] == 0) {
                    ip = op.jump_target + 1;
                } else {
                    ++ip;
                }
                break;
            case OpType::JumpIfNotZero:
                if (tape[ptr] != 0) {
                    ip = op.jump_target + 1;
                } else {
                    ++ip;
                }
                break;
        }
    }
}

std::string read_file(const std::string& path) {
    std::ifstream in(path, std::ios::binary);
    if (!in) {
        throw std::runtime_error("Cannot open file: " + path);
    }
    return std::string((std::istreambuf_iterator<char>(in)), std::istreambuf_iterator<char>());
}

int main(int argc, char** argv) {
    try {
        if (argc < 2 || argc > 3) {
            std::cerr << "Usage: bf_interpreter <program.bf> [--debug]\n";
            return 1;
        }

        std::string file_path = argv[1];
        bool debug = (argc == 3 && std::string(argv[2]) == "--debug");
        if (argc == 3 && !debug) {
            std::cerr << "Unknown option: " << argv[2] << "\n";
            return 1;
        }

        Program program = compile_program(read_file(file_path));
        run_program(program, debug);
        return 0;
    } catch (const std::exception& ex) {
        std::cerr << "Error: " << ex.what() << "\n";
        return 2;
    }
}
