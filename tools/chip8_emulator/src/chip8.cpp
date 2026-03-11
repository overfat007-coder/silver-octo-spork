#include "chip8.hpp"

#include <chrono>
#include <fstream>
#include <random>

namespace {
constexpr std::array<uint8_t, 80> kFontset = {
    0xF0,0x90,0x90,0x90,0xF0, 0x20,0x60,0x20,0x20,0x70,
    0xF0,0x10,0xF0,0x80,0xF0, 0xF0,0x10,0xF0,0x10,0xF0,
    0x90,0x90,0xF0,0x10,0x10, 0xF0,0x80,0xF0,0x10,0xF0,
    0xF0,0x80,0xF0,0x90,0xF0, 0xF0,0x10,0x20,0x40,0x40,
    0xF0,0x90,0xF0,0x90,0xF0, 0xF0,0x90,0xF0,0x10,0xF0,
    0xF0,0x90,0xF0,0x90,0x90, 0xE0,0x90,0xE0,0x90,0xE0,
    0xF0,0x80,0x80,0x80,0xF0, 0xE0,0x90,0x90,0x90,0xE0,
    0xF0,0x80,0xF0,0x80,0xF0, 0xF0,0x80,0xF0,0x80,0x80
};
}

Chip8::Chip8() { reset(); }

void Chip8::reset() {
    memory_.fill(0); V_.fill(0); stack_.fill(0); keypad_.fill(0); display_.fill(0);
    I_ = 0; pc_ = 0x200; sp_ = 0; delay_timer_ = 0; sound_timer_ = 0;
    draw_flag_ = false; wait_key_reg_ = -1;
    load_fontset();
}

void Chip8::load_fontset() {
    for (size_t i = 0; i < kFontset.size(); ++i) memory_[0x50 + i] = kFontset[i];
}

bool Chip8::load_rom(const std::string& path) {
    std::ifstream in(path, std::ios::binary);
    if (!in) return false;
    std::vector<uint8_t> rom((std::istreambuf_iterator<char>(in)), std::istreambuf_iterator<char>());
    if (rom.size() > (4096 - 0x200)) return false;
    for (size_t i = 0; i < rom.size(); ++i) memory_[0x200 + i] = rom[i];
    return true;
}

uint16_t Chip8::fetch_opcode() const {
    return static_cast<uint16_t>((memory_[pc_] << 8) | memory_[pc_ + 1]);
}

void Chip8::clear_display() {
    display_.fill(0);
    draw_flag_ = true;
}

void Chip8::set_key(uint8_t key, bool pressed) {
    if (key < keypad_.size()) keypad_[key] = pressed ? 1 : 0;
    if (pressed && wait_key_reg_ >= 0) {
        V_[wait_key_reg_] = key;
        wait_key_reg_ = -1;
    }
}

bool Chip8::consume_draw_flag() {
    bool v = draw_flag_;
    draw_flag_ = false;
    return v;
}

void Chip8::tick_timers() {
    if (delay_timer_ > 0) --delay_timer_;
    if (sound_timer_ > 0) --sound_timer_;
}

void Chip8::tick() {
    if (wait_key_reg_ >= 0) return;

    const uint16_t op = fetch_opcode();
    pc_ += 2;

    const uint8_t x = (op & 0x0F00) >> 8;
    const uint8_t y = (op & 0x00F0) >> 4;
    const uint8_t n = (op & 0x000F);
    const uint8_t kk = (op & 0x00FF);
    const uint16_t nnn = (op & 0x0FFF);

    switch (op & 0xF000) {
        case 0x0000:
            if (op == 0x00E0) clear_display();
            else if (op == 0x00EE) { --sp_; pc_ = stack_[sp_]; }
            break;
        case 0x1000: pc_ = nnn; break;
        case 0x2000: stack_[sp_++] = pc_; pc_ = nnn; break;
        case 0x3000: if (V_[x] == kk) pc_ += 2; break;
        case 0x4000: if (V_[x] != kk) pc_ += 2; break;
        case 0x5000: if (V_[x] == V_[y]) pc_ += 2; break;
        case 0x6000: V_[x] = kk; break;
        case 0x7000: V_[x] = static_cast<uint8_t>(V_[x] + kk); break;
        case 0x8000:
            switch (n) {
                case 0x0: V_[x] = V_[y]; break;
                case 0x1: V_[x] |= V_[y]; break;
                case 0x2: V_[x] &= V_[y]; break;
                case 0x3: V_[x] ^= V_[y]; break;
                case 0x4: {
                    uint16_t s = V_[x] + V_[y]; V_[0xF] = s > 255; V_[x] = s & 0xFF; break;
                }
                case 0x5: V_[0xF] = V_[x] >= V_[y]; V_[x] = static_cast<uint8_t>(V_[x] - V_[y]); break;
                case 0x6: V_[0xF] = V_[x] & 0x1; V_[x] >>= 1; break;
                case 0x7: V_[0xF] = V_[y] >= V_[x]; V_[x] = static_cast<uint8_t>(V_[y] - V_[x]); break;
                case 0xE: V_[0xF] = (V_[x] & 0x80) >> 7; V_[x] <<= 1; break;
            }
            break;
        case 0x9000: if (V_[x] != V_[y]) pc_ += 2; break;
        case 0xA000: I_ = nnn; break;
        case 0xB000: pc_ = nnn + V_[0]; break;
        case 0xC000: {
            static std::mt19937 rng(std::random_device{}());
            std::uniform_int_distribution<int> dist(0, 255);
            V_[x] = static_cast<uint8_t>(dist(rng)) & kk;
            break;
        }
        case 0xD000: {
            V_[0xF] = 0;
            for (int row = 0; row < n; ++row) {
                uint8_t sprite = memory_[I_ + row];
                for (int col = 0; col < 8; ++col) {
                    if ((sprite & (0x80 >> col)) == 0) continue;
                    int px = (V_[x] + col) % kDisplayWidth;
                    int py = (V_[y] + row) % kDisplayHeight;
                    int idx = py * kDisplayWidth + px;
                    if (display_[idx] == 1) V_[0xF] = 1;
                    display_[idx] ^= 1;
                }
            }
            draw_flag_ = true;
            break;
        }
        case 0xE000:
            if ((op & 0x00FF) == 0x9E) { if (keypad_[V_[x]]) pc_ += 2; }
            else if ((op & 0x00FF) == 0xA1) { if (!keypad_[V_[x]]) pc_ += 2; }
            break;
        case 0xF000:
            switch (op & 0x00FF) {
                case 0x07: V_[x] = delay_timer_; break;
                case 0x0A: wait_key_reg_ = x; break;
                case 0x15: delay_timer_ = V_[x]; break;
                case 0x18: sound_timer_ = V_[x]; break;
                case 0x1E: I_ += V_[x]; break;
                case 0x29: I_ = 0x50 + (V_[x] * 5); break;
                case 0x33:
                    memory_[I_] = V_[x] / 100;
                    memory_[I_ + 1] = (V_[x] / 10) % 10;
                    memory_[I_ + 2] = V_[x] % 10;
                    break;
                case 0x55: for (int i = 0; i <= x; ++i) memory_[I_ + i] = V_[i]; break;
                case 0x65: for (int i = 0; i <= x; ++i) V_[i] = memory_[I_ + i]; break;
            }
            break;
    }
}
