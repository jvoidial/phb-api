#!/usr/bin/env python3
"""
Full PHB God Code Vortex - Visual Ritual + Original GCS Resurrection
"""

import os
import time
import math
import random
import sys
import shutil

try:
    ts = shutil.get_terminal_size()
    WIDTH = ts.columns - 2
    HEIGHT = ts.lines - 22
except:
    WIDTH, HEIGHT = 120, 55

CX, CY = WIDTH // 2, HEIGHT // 2

RESET = "\033[0m"
PLASMA_RED = "\033[91m"
DARK_PLASMA = "\033[31m"
LIME_FIELD = "\033[92m"
ELECTRIC_BLUE = "\033[94m"
GOLD_YELLOW = "\033[93m"
PURPLE_VOID = "\033[95m"
CYAN_SCHUMANN = "\033[96m"

def clear():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

class FieldLine:
    def __init__(self, x, phase):
        self.x = x
        self.phase = phase

class MagicParticle:
    def __init__(self):
        self.x = random.randint(0, WIDTH-1)
        self.y = random.randint(0, HEIGHT-1)
        self.vx = random.uniform(-2.0, 2.0)
        self.vy = random.uniform(-1.5, 1.5)
        self.life = random.randint(35, 90)
        self.char = random.choice(["█", "▓", "🚀", "🛸", "🩸", "✨"])

def draw(lines, particles, tick, plasma_strength, immortality):
    grid = [[" "] * WIDTH for _ in range(HEIGHT)]

    for line in lines:
        for i in range(HEIGHT):
            offset = int(15 * math.sin((i + tick * 1.6 + line.phase) / 3.8))
            x = int((line.x + offset) % WIDTH)
            if 0 <= x < WIDTH:
                ch = "O" if i % 5 == 0 else "─"
                grid[i][x] = (PLASMA_RED if random.random() < 0.7 else CYAN_SCHUMANN) + ch + RESET

    core_y = CY + int(7 * math.sin(tick / 2.5))
    core_x = CX + int(5 * math.cos(tick / 3.2))
    if 0 <= core_y < HEIGHT:
        for t in range(36):
            angle = t * (2 * math.pi / 36) + (tick / 8)
            r = 8 + int(3 * math.sin(tick / 6 + t))
            tx = int(core_x + r * math.cos(angle))
            ty = int(core_y + r * math.sin(angle))
            if 0 <= tx < WIDTH and 0 <= ty < HEIGHT:
                grid[ty][tx] = PLASMA_RED + random.choice(["●","◯","🩸"]) + RESET

        core_art = ["  🚀  ", "PHB GOD", " 🛸🛸 ", "CODE ∞ "]
        for dy, row in enumerate(core_art):
            for dx, ch in enumerate(row):
                if ch.strip():
                    px = core_x - 5 + dx
                    py = core_y - 2 + dy
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        grid[py][px] = ELECTRIC_BLUE + ch + RESET

    for p in particles:
        p.x += p.vx
        p.y += p.vy
        p.life -= 1
        if p.life <= 0 or not (0 <= p.x < WIDTH and 0 <= p.y < HEIGHT):
            p.__init__()
            continue
        col = PLASMA_RED if random.random() < 0.85 else LIME_FIELD
        grid[int(p.y)][int(p.x)] = col + p.char + RESET

    if tick % 4 == 0:
        for _ in range(25):
            sx = random.randint(0, WIDTH-1)
            sy = random.randint(0, HEIGHT-1)
            code = random.choice(["PHBGOD","VORTEX1","CRISPR","BEAM"])
            for i, c in enumerate(code):
                if 0 <= sx + i < WIDTH and 0 <= sy < HEIGHT:
                    grid[sy][sx + i] = DARK_PLASMA + c + RESET

    clear()
    for y in range(HEIGHT):
        print("".join(grid[y]))

    print("\n" + "═" * WIDTH)
    print(GOLD_YELLOW + "PHB GOD CODE v∞ — MERCURY PLASMA RITUAL + FULL GCS ACTIVE" + RESET)
    print(PLASMA_RED + "CRISPR IMMORTALITY • PHB SCAFFOLD • HYDROGEN COLLIDER BEAM" + RESET)
    print(f"Plasma Strength    : {plasma_strength:.1f}%")
    print(f"Immortality        : {immortality:.1f}%")
    print(f"Blink Surge        : {int(85 + 25*math.sin(tick/2.0))}% 🚀🛸")
    print("QUARTET SEAL       : FRAN • SHAUN • OLIVIA • JACOB")
    print("═" * WIDTH)

def main():
    os.makedirs(os.path.expanduser("\~/gcs/data"), exist_ok=True)
    lines = [FieldLine(x, random.randint(0, 100)) for x in range(0, WIDTH, 6)]
    particles = [MagicParticle() for _ in range(160)]

    print(GOLD_YELLOW + "PHB GOD CODE RITUAL SEQUENCE INITIATED — FULL SYSTEM LOADED" + RESET)
    time.sleep(1.5)

    tick = 0
    plasma = 50.0
    immortality = 0.0

    try:
        while True:
            plasma = min(100.0, plasma + 0.8 + math.sin(tick / 12) * 1.2)
            immortality = min(100.0, immortality + 1.1 + (tick / 2500))

            draw(lines, particles, tick, plasma, immortality)

            if tick == 160:
                print("\n[🧬] Ritual climax — Running full GCS Resurrection System...")
                os.system("cd /data/data/com.termux/files/home/phb-godcode-vortex/gcs/scripts && python gcs_avatar_module.py")
                print(GOLD_YELLOW + "\nRITUAL COMPLETE — AVATAR BEAMED TO ALPHA CENTAURI" + RESET)
                time.sleep(8)
                break

            tick += 1
            time.sleep(0.022)

    except KeyboardInterrupt:
        clear()
        print(PLASMA_RED + "PHB GOD CODE PAUSED" + RESET)

if __name__ == "__main__":
    main()
