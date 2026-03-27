"""Procedural audio — all sound effects generated at runtime via math + pygame.mixer."""

import math
import struct
import io
import random
import pygame

SAMPLE_RATE = 22050


class Audio:
    """Generates and manages all game sound effects procedurally."""

    def __init__(self):
        self.muted = False
        self.available = True
        self.sounds: dict[str, pygame.mixer.Sound] = {}
        try:
            self._generate_all()
        except Exception:
            self.available = False

    def _generate_all(self):
        # Purchase sounds — pitch rises with rarity
        self.sounds["buy_common"] = _make_sound(_coin(440, 0.12))
        self.sounds["buy_uncommon"] = _make_sound(_coin(523, 0.14))
        self.sounds["buy_rare"] = _make_sound(_chime(659, 0.20))
        self.sounds["buy_epic"] = _make_sound(_chime(784, 0.25))
        self.sounds["buy_legendary"] = _make_sound(_fanfare())
        # Actions
        self.sounds["refresh"] = _make_sound(_whoosh())
        self.sounds["mine"] = _make_sound(_mine_hit())
        self.sounds["error"] = _make_sound(_error_buzz())
        self.sounds["use"] = _make_sound(_activate())
        self.sounds["salvage"] = _make_sound(_salvage())
        self.sounds["expand"] = _make_sound(_expand())

    def play(self, name: str):
        if self.muted or not self.available:
            return
        snd = self.sounds.get(name)
        if snd:
            snd.play()

    def play_buy(self, rarity: str):
        self.play(f"buy_{rarity}")

    def toggle_mute(self) -> bool:
        self.muted = not self.muted
        return self.muted


# ── WAV builder ─────────────────────────────────────────────────

def _make_sound(samples: list[float]) -> pygame.mixer.Sound:
    """Convert float samples [-1, 1] → pygame.mixer.Sound via in-memory WAV."""
    n = len(samples)
    raw = struct.pack(
        f"<{n}h",
        *(max(-32767, min(32767, int(s * 32767))) for s in samples),
    )
    buf = io.BytesIO()
    buf.write(b"RIFF")
    buf.write(struct.pack("<I", 36 + len(raw)))
    buf.write(b"WAVE")
    buf.write(b"fmt ")
    buf.write(struct.pack("<IHHIIHH", 16, 1, 1, SAMPLE_RATE, SAMPLE_RATE * 2, 2, 16))
    buf.write(b"data")
    buf.write(struct.pack("<I", len(raw)))
    buf.write(raw)
    buf.seek(0)
    return pygame.mixer.Sound(buf)


# ── Synthesis helpers ───────────────────────────────────────────

def _coin(freq: float, dur: float) -> list[float]:
    """Quick metallic coin clink with inharmonic overtones."""
    n = int(SAMPLE_RATE * dur)
    out: list[float] = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = max(0.0, 1.0 - t / dur) ** 2
        s = 0.40 * math.sin(2 * math.pi * freq * t)
        s += 0.20 * math.sin(2 * math.pi * freq * 2.7 * t)
        s += 0.10 * math.sin(2 * math.pi * freq * 5.3 * t)
        out.append(s * env * 0.35)
    return out


def _chime(freq: float, dur: float) -> list[float]:
    """Rich bell-like chime with harmonic series."""
    n = int(SAMPLE_RATE * dur)
    out: list[float] = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = max(0.0, 1.0 - t / dur) ** 1.5
        s = 0.30 * math.sin(2 * math.pi * freq * t)
        s += 0.20 * math.sin(2 * math.pi * freq * 2.0 * t)
        s += 0.15 * math.sin(2 * math.pi * freq * 3.0 * t)
        s += 0.10 * math.sin(2 * math.pi * freq * 4.2 * t)
        out.append(s * env * 0.35)
    return out


def _fanfare() -> list[float]:
    """Ascending arpeggio for legendary purchases (C5→E5→G5→C6)."""
    notes = [523.25, 659.25, 783.99, 1046.50]
    note_dur = 0.10
    tail = 0.30
    total = len(notes) * note_dur + tail
    n = int(SAMPLE_RATE * total)
    out = [0.0] * n
    for ni, freq in enumerate(notes):
        start = int(ni * note_dur * SAMPLE_RATE)
        dur = total - ni * note_dur
        for i in range(int(dur * SAMPLE_RATE)):
            idx = start + i
            if idx >= n:
                break
            t = i / SAMPLE_RATE
            env = max(0.0, 1.0 - t / dur) ** 1.5
            s = 0.25 * math.sin(2 * math.pi * freq * t)
            s += 0.12 * math.sin(2 * math.pi * freq * 2.0 * t)
            s += 0.08 * math.sin(2 * math.pi * freq * 3.0 * t)
            out[idx] += s * env * 0.30
    return out


def _whoosh() -> list[float]:
    """Swooshing noise for shop refresh."""
    dur = 0.25
    n = int(SAMPLE_RATE * dur)
    raw: list[float] = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.sin(math.pi * t / dur)
        raw.append((random.random() * 2 - 1) * env * 0.15)
    # Simple 3-tap lowpass for smoothness
    out = raw[:]
    for i in range(2, n):
        out[i] = 0.5 * raw[i] + 0.3 * raw[i - 1] + 0.2 * raw[i - 2]
    return out


def _mine_hit() -> list[float]:
    """Rocky impact thud with crumble noise."""
    dur = 0.20
    n = int(SAMPLE_RATE * dur)
    out: list[float] = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = max(0.0, 1.0 - t / dur) ** 3
        s = 0.50 * math.sin(2 * math.pi * 80 * t) * env
        noise_env = max(0.0, 1.0 - t / dur) ** 2
        s += (random.random() * 2 - 1) * 0.20 * noise_env
        out.append(s * 0.40)
    return out


def _error_buzz() -> list[float]:
    """Short descending two-tone buzz."""
    dur = 0.20
    n = int(SAMPLE_RATE * dur)
    out: list[float] = []
    for i in range(n):
        t = i / SAMPLE_RATE
        if t < 0.08:
            env, freq = 1.0, 200
        elif t < 0.12:
            env, freq = 0.0, 200
        else:
            env = max(0.0, 1.0 - (t - 0.12) / 0.08)
            freq = 160
        s = math.sin(2 * math.pi * freq * t)
        s += 0.5 * math.sin(2 * math.pi * freq * 3 * t)
        out.append(s * env * 0.20)
    return out


def _activate() -> list[float]:
    """Quick ascending sweep for item activation."""
    dur = 0.15
    n = int(SAMPLE_RATE * dur)
    out: list[float] = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = max(0.0, 1.0 - t / dur) ** 1.5
        freq = 400 + 300 * (t / dur)
        s = 0.30 * math.sin(2 * math.pi * freq * t)
        s += 0.15 * math.sin(2 * math.pi * freq * 2.0 * t)
        out.append(s * env * 0.35)
    return out


def _salvage() -> list[float]:
    """Metallic crunch followed by scattering coins."""
    dur = 0.35
    n = int(SAMPLE_RATE * dur)
    out: list[float] = []
    for i in range(n):
        t = i / SAMPLE_RATE
        s = 0.0
        # Impact
        if t < 0.10:
            env = max(0.0, 1.0 - t / 0.10) ** 2
            s += 0.30 * math.sin(2 * math.pi * 150 * t) * env
            s += (random.random() * 2 - 1) * 0.20 * env
        # Coins
        if t > 0.05:
            coin_env = max(0.0, 1.0 - (t - 0.05) / 0.30) ** 1.5
            s += 0.20 * math.sin(2 * math.pi * 880 * t) * coin_env
            s += 0.15 * math.sin(2 * math.pi * 1320 * t) * coin_env
            s += 0.10 * math.sin(2 * math.pi * 1760 * t) * coin_env
        out.append(s * 0.35)
    return out


def _expand() -> list[float]:
    """Rising major chord for inventory expansion."""
    dur = 0.30
    n = int(SAMPLE_RATE * dur)
    out: list[float] = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.sin(math.pi * t / dur)
        freq = 300 + 200 * (t / dur)
        s = 0.30 * math.sin(2 * math.pi * freq * t)
        s += 0.20 * math.sin(2 * math.pi * freq * 1.25 * t)   # major 3rd
        s += 0.15 * math.sin(2 * math.pi * freq * 1.50 * t)   # perfect 5th
        out.append(s * env * 0.30)
    return out
