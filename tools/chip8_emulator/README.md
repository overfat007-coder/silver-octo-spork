# Chip-8 Emulator (C++)

Учебный эмулятор Chip-8 на C++ с ядром CPU/памяти/таймеров и SDL2-фронтендом для дисплея.

## Реализовано
- Эмуляция CPU:
  - регистры `V0..VF`, `I`, `PC`, `SP`, стек
  - память 4KB
  - исполнение основных Chip-8 опкодов (арифметика, прыжки, draw, key, timers)
- Эмуляция дисплея `64x32` (буфер пикселей)
- Таймеры `delay_timer` / `sound_timer` (тик 60Hz через `tick_timers`)
- Загрузка ROM-файла в память с адреса `0x200`
- Синхронизация:
  - CPU циклы: несколько `tick()` на итерацию
  - Timers: шаг 60Hz
  - Display: перерисовка по draw-flag
- Ввод с клавиатуры (Chip-8 keypad map)
- Флаг звука (`sound_timer > 0`) — зуммерный режим отмечен в SDL loop

## Сборка/тест ядра (без SDL)
```bash
cd tools/chip8_emulator
cmake -S . -B build
cmake --build build
./build/chip8_core_test
```

## Сборка SDL фронтенда
Требуется SDL2 dev пакет.
```bash
cd tools/chip8_emulator
cmake -S . -B build-sdl -DCHIP8_WITH_SDL=ON
cmake --build build-sdl
./build-sdl/chip8_sdl path/to/rom.ch8
```
