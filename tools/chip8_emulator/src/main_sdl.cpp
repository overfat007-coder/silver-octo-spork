#include "chip8.hpp"

#include <SDL2/SDL.h>
#include <chrono>
#include <iostream>

namespace {
int map_key(SDL_Keycode key) {
    switch (key) {
        case SDLK_x: return 0x0; case SDLK_1: return 0x1; case SDLK_2: return 0x2; case SDLK_3: return 0x3;
        case SDLK_q: return 0x4; case SDLK_w: return 0x5; case SDLK_e: return 0x6; case SDLK_a: return 0x7;
        case SDLK_s: return 0x8; case SDLK_d: return 0x9; case SDLK_z: return 0xA; case SDLK_c: return 0xB;
        case SDLK_4: return 0xC; case SDLK_r: return 0xD; case SDLK_f: return 0xE; case SDLK_v: return 0xF;
        default: return -1;
    }
}
}

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "Usage: chip8_sdl <rom_file>\n";
        return 1;
    }

    if (SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO | SDL_INIT_TIMER) != 0) {
        std::cerr << "SDL init failed\n";
        return 1;
    }

    Chip8 chip;
    if (!chip.load_rom(argv[1])) {
        std::cerr << "Failed to load ROM\n";
        return 1;
    }

    const int scale = 12;
    SDL_Window* win = SDL_CreateWindow("Chip-8", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
                                       Chip8::kDisplayWidth * scale, Chip8::kDisplayHeight * scale, SDL_WINDOW_SHOWN);
    SDL_Renderer* ren = SDL_CreateRenderer(win, -1, SDL_RENDERER_ACCELERATED);

    bool running = true;
    auto last_timer = std::chrono::steady_clock::now();

    while (running) {
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_QUIT) running = false;
            if (e.type == SDL_KEYDOWN || e.type == SDL_KEYUP) {
                int k = map_key(e.key.keysym.sym);
                if (k >= 0) chip.set_key(static_cast<uint8_t>(k), e.type == SDL_KEYDOWN);
            }
        }

        for (int i = 0; i < 10; ++i) chip.tick(); // CPU cycles per frame slice

        auto now = std::chrono::steady_clock::now();
        if (std::chrono::duration_cast<std::chrono::milliseconds>(now - last_timer).count() >= 16) {
            chip.tick_timers();
            last_timer = now;
        }

        if (chip.consume_draw_flag()) {
            SDL_SetRenderDrawColor(ren, 0, 0, 0, 255);
            SDL_RenderClear(ren);
            SDL_SetRenderDrawColor(ren, 255, 255, 255, 255);
            const auto& pix = chip.display();
            for (int y = 0; y < Chip8::kDisplayHeight; ++y) {
                for (int x = 0; x < Chip8::kDisplayWidth; ++x) {
                    if (pix[y * Chip8::kDisplayWidth + x]) {
                        SDL_Rect r{x * scale, y * scale, scale, scale};
                        SDL_RenderFillRect(ren, &r);
                    }
                }
            }
            SDL_RenderPresent(ren);
        }

        // simple buzzer indication
        if (chip.sound_active()) {
            // no heavy audio synth here; keep place for buzzer flag
        }

        SDL_Delay(1);
    }

    SDL_DestroyRenderer(ren);
    SDL_DestroyWindow(win);
    SDL_Quit();
    return 0;
}
