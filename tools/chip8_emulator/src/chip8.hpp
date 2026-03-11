#pragma once

#include <array>
#include <cstdint>
#include <string>
#include <vector>

class Chip8 {
public:
    static constexpr int kDisplayWidth = 64;
    static constexpr int kDisplayHeight = 32;

    Chip8();

    bool load_rom(const std::string& path);
    void reset();
    void tick();          // execute one opcode
    void tick_timers();   // call at 60Hz

    void set_key(uint8_t key, bool pressed);

    const std::array<uint8_t, kDisplayWidth * kDisplayHeight>& display() const { return display_; }
    bool consume_draw_flag();
    bool sound_active() const { return sound_timer_ > 0; }

private:
    std::array<uint8_t, 4096> memory_{};
    std::array<uint8_t, 16> V_{};
    std::array<uint16_t, 16> stack_{};
    std::array<uint8_t, 16> keypad_{};
    std::array<uint8_t, kDisplayWidth * kDisplayHeight> display_{};

    uint16_t I_ = 0;
    uint16_t pc_ = 0x200;
    uint8_t sp_ = 0;
    uint8_t delay_timer_ = 0;
    uint8_t sound_timer_ = 0;

    bool draw_flag_ = false;
    int wait_key_reg_ = -1;

    uint16_t fetch_opcode() const;
    void clear_display();
    void load_fontset();
};
