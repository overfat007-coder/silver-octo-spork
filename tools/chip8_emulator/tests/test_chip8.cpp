#include "../src/chip8.hpp"

#include <cassert>
#include <cstdint>
#include <fstream>
#include <vector>

static std::string write_rom(const std::vector<uint8_t>& bytes) {
    const std::string p = "./chip8_test.rom";
    std::ofstream out(p, std::ios::binary);
    out.write(reinterpret_cast<const char*>(bytes.data()), static_cast<std::streamsize>(bytes.size()));
    return p;
}

int main() {
    // Program: V0=2; V1=3; V0=V0+V1; I=0x300; store V0 BCD at I..I+2
    std::vector<uint8_t> rom = {
        0x60,0x02,
        0x61,0x03,
        0x80,0x14,
        0xA3,0x00,
        0xF0,0x33,
    };

    Chip8 c;
    auto p = write_rom(rom);
    assert(c.load_rom(p));
    for (int i = 0; i < 5; ++i) c.tick();

    // Draw instruction smoke test
    std::vector<uint8_t> rom2 = {
        0x60,0x00, // V0 x
        0x61,0x00, // V1 y
        0xA0,0x50, // I fontset for 0
        0xD0,0x15, // draw 5-byte sprite
    };
    Chip8 d;
    auto p2 = write_rom(rom2);
    assert(d.load_rom(p2));
    for (int i = 0; i < 4; ++i) d.tick();
    assert(d.consume_draw_flag());
    const auto& disp = d.display();
    int lit = 0;
    for (auto v : disp) lit += v;
    assert(lit > 0);

    return 0;
}
