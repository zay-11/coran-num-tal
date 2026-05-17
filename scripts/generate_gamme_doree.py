#!/usr/bin/env python3
"""
GAMME DOREE — Generateur de frequences audio basees sur phi
Produit des fichiers WAV de meditation accordes aux nombres sacres du projet.
"""

from __future__ import annotations
import math, struct, wave
from pathlib import Path

PHI = (1 + math.sqrt(5)) / 2
INV_PHI = 1 / PHI

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "exports/audio/gamme_doree"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SAMPLE_RATE = 44100
BITS = 16
DURATION = 60  # seconds per track

# Sacred numbers from the project
SACRED = [7, 8, 19, 34, 55, 56, 61, 76, 89, 99, 123, 319, 489, 618, 786]

# Base frequencies derived from sacred numbers
# 56 Hz = Al-Waqi'a resonance, 7.83 Hz = Schumann (sub-audio, use harmonics)
BASE_FREQS = {
    "schumann_7hz": 7.83,
    "rizq_56hz": 56.0,
    "waqia_152hz": 152.0,
    "basmala_786hz": 786.0,
    "mercy_618hz": 618.0,
    "code_19hz": 19.0,
    "fattah_489hz": 489.0,
    "razzaq_319hz": 319.0,
}


def generate_sine_wave(freq, duration, sample_rate=SAMPLE_RATE, amplitude=0.3):
    """Generate a pure sine wave."""
    n_samples = int(sample_rate * duration)
    samples = []
    for i in range(n_samples):
        t = i / sample_rate
        # Fade in/out (2 seconds each)
        env = 1.0
        fade = int(2 * sample_rate)
        if i < fade:
            env = i / fade
        elif i > n_samples - fade:
            env = (n_samples - i) / fade
        val = amplitude * env * math.sin(2 * math.pi * freq * t)
        samples.append(int(val * (2 ** (BITS - 1) - 1)))
    return samples


def generate_phi_harmonics(base_freq, duration, sample_rate=SAMPLE_RATE, amplitude=0.2):
    """Generate a chord with phi-based harmonics."""
    n_samples = int(sample_rate * duration)
    samples = [0.0] * n_samples

    # Fundamental + phi harmonics
    harmonics = [base_freq]
    for i in range(1, 8):
        harmonics.append(base_freq * (PHI ** i))
        harmonics.append(base_freq * (INV_PHI ** i))

    for h in harmonics:
        if h > sample_rate / 2:  # Nyquist
            continue
        amp = amplitude / (harmonics.index(h) + 1) ** 0.7
        for i in range(n_samples):
            t = i / sample_rate
            samples[i] += amp * math.sin(2 * math.pi * h * t)

    # Normalize
    max_val = max(abs(s) for s in samples)
    if max_val > 0:
        samples = [s / max_val * 0.85 for s in samples]

    # Fade
    fade = int(3 * sample_rate)
    for i in range(n_samples):
        if i < fade:
            samples[i] *= i / fade
        elif i > n_samples - fade:
            samples[i] *= (n_samples - i) / fade

    return [int(s * (2 ** (BITS - 1) - 1)) for s in samples]


def save_wav(filename, samples, sample_rate=SAMPLE_RATE, bits=BITS):
    path = OUT_DIR / filename
    with wave.open(str(path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(bits // 8)
        wf.setframerate(sample_rate)
        wf.writeframes(struct.pack(f"<{len(samples)}h", *samples))
    return path


def generate_golden_scale():
    """Generate a musical scale using phi ratios (7 notes x phi spacing)."""
    base = 56.0  # Al-Waqi'a
    notes = []
    for i in range(19):  # 19 notes in the scale (Code 19)
        freq = base * (PHI ** (i / 7))  # 7-tone equal phi temperament
        notes.append(freq)
    return notes


def build():
    print("Generation de la Gamme Doree audio...")
    files = []

    # 1. Pure sacred frequencies
    print("  1/6: Frequences sacrees pures...")
    for name, freq in BASE_FREQS.items():
        if freq < 20:
            # Sub-audio: generate harmonic series
            samples = generate_phi_harmonics(freq * 8, 45, amplitude=0.25)
        else:
            samples = generate_sine_wave(freq, 45, amplitude=0.2)
        path = save_wav(f"{name}.wav", samples)
        files.append(path)
        print(f"    {path.name} ({freq} Hz)")

    # 2. Phi chord (all sacred freqs layered with phi ratios)
    print("  2/6: Accord phi complet...")
    n_samples = int(SAMPLE_RATE * 90)
    mixed = [0.0] * n_samples
    sacred_freqs = [7.83 * 8, 19, 34, 55, 56, 61, 76, 89, 99, 123, 152, 319, 489, 618, 786]
    for freq in sacred_freqs:
        if freq > SAMPLE_RATE / 4:
            continue
        amp = 0.06
        for i in range(n_samples):
            t = i / SAMPLE_RATE
            mixed[i] += amp * math.sin(2 * math.pi * freq * t)
            # Add phi harmonic
            mixed[i] += amp * 0.4 * math.sin(2 * math.pi * freq * PHI * t)
    max_val = max(abs(s) for s in mixed)
    if max_val > 0:
        mixed = [s / max_val * 0.8 for s in mixed]
    fade = int(5 * SAMPLE_RATE)
    for i in range(n_samples):
        if i < fade:
            mixed[i] *= i / fade
        elif i > n_samples - fade:
            mixed[i] *= (n_samples - i) / fade
    mixed_int = [int(s * (2 ** (BITS - 1) - 1)) for s in mixed]
    path = save_wav("accord_phi_sacre_90s.wav", mixed_int)
    files.append(path)
    print(f"    {path.name}")

    # 3. Fibonacci sequence tones
    print("  3/6: Sequence Fibonacci...")
    fib = [1, 1]
    while len(fib) < 15:
        fib.append(fib[-1] + fib[-2])
    n_samples_fib = int(SAMPLE_RATE * 60)
    fib_samples = [0.0] * n_samples_fib
    seg = n_samples_fib // len(fib)
    for j, f in enumerate(fib):
        freq = f * 10 if f * 10 < SAMPLE_RATE / 2 else f
        if freq > SAMPLE_RATE / 2:
            freq = freq % (SAMPLE_RATE // 2)
        amp = 0.15
        start = j * seg
        end = (j + 1) * seg
        for i in range(start, min(end, n_samples_fib)):
            t = i / SAMPLE_RATE
            fib_samples[i] += amp * math.sin(2 * math.pi * freq * t)
    fade = int(2 * SAMPLE_RATE)
    for i in range(n_samples_fib):
        if i < fade:
            fib_samples[i] *= i / fade
        elif i > n_samples_fib - fade:
            fib_samples[i] *= (n_samples_fib - i) / fade
    max_val = max(abs(s) for s in fib_samples)
    fib_samples = [s / max_val * 0.8 for s in fib_samples] if max_val > 0 else fib_samples
    fib_int = [int(s * (2 ** (BITS - 1) - 1)) for s in fib_samples]
    path = save_wav("sequence_fibonacci.wav", fib_int)
    files.append(path)
    print(f"    {path.name}")

    # 4. Golden scale melody
    print("  4/6: Gamme doree...")
    scale = generate_golden_scale()
    n_scale = int(SAMPLE_RATE * 90)
    scale_samples = [0.0] * n_scale
    note_len = n_scale // (len(scale) * 2)
    for j, freq in enumerate(scale):
        if freq > SAMPLE_RATE / 2:
            freq = freq % (SAMPLE_RATE // 2)
        amp = 0.15
        start = j * note_len * 2
        end = start + note_len
        for i in range(start, min(end, n_scale)):
            t = i / SAMPLE_RATE
            env = 1.0 if i > start + 100 else (i - start) / 100
            scale_samples[i] += amp * env * math.sin(2 * math.pi * freq * t)
    fade = int(3 * SAMPLE_RATE)
    for i in range(n_scale):
        if i < fade:
            scale_samples[i] *= i / fade
        elif i > n_scale - fade:
            scale_samples[i] *= (n_scale - i) / fade
    max_val = max(abs(s) for s in scale_samples)
    scale_samples = [s / max_val * 0.8 for s in scale_samples] if max_val > 0 else scale_samples
    scale_int = [int(s * (2 ** (BITS - 1) - 1)) for s in scale_samples]
    path = save_wav("gamme_doree_19_notes.wav", scale_int)
    files.append(path)
    print(f"    {path.name}")

    # 5. Meditation drone (56 Hz Waqi'a + phi harmonics)
    print("  5/6: Bourdon de meditation Waqi'a...")
    drone = generate_phi_harmonics(56.0, 180, amplitude=0.18)
    path = save_wav("meditation_waqia_3min.wav", drone)
    files.append(path)
    print(f"    {path.name}")

    # 6. Rizq activation sequence (7-19-8 beats)
    print("  6/6: Sequence d'activation Rizq...")
    n_act = int(SAMPLE_RATE * 120)
    act = [0.0] * n_act
    # 7 beats at 56 Hz, 19 beats at 152 Hz, 8 beats at 19 Hz
    pattern = [(56, 7), (152, 19), (19, 8), (56, 7), (152, 19), (19, 8), (618, 3)]
    beat_len = n_act // sum(p[1] for p in pattern)
    pos = 0
    for freq, count in pattern:
        for _ in range(count):
            for i in range(pos, min(pos + beat_len, n_act)):
                t = i / SAMPLE_RATE
                env = (i - pos) / beat_len if (i - pos) < beat_len * 0.1 else 1.0
                if i > pos + beat_len * 0.9:
                    env = (pos + beat_len - i) / (beat_len * 0.1)
                act[i] += 0.2 * env * math.sin(2 * math.pi * freq * t)
            pos += beat_len
    max_val = max(abs(s) for s in act)
    act = [s / max_val * 0.75 for s in act] if max_val > 0 else act
    act_int = [int(s * (2 ** (BITS - 1) - 1)) for s in act]
    path = save_wav("activation_rizq_7_19_8.wav", act_int)
    files.append(path)
    print(f"    {path.name}")

    # Generate index
    import json
    index = {
        "project": "Gamme Doree — Frequences Phi",
        "sample_rate": SAMPLE_RATE,
        "bits": BITS,
        "phi": PHI,
        "files": [str(f.name) for f in files],
    }
    (OUT_DIR / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")

    total_size = sum(f.stat().st_size for f in files)
    print(f"\nTotal: {len(files)} fichiers audio generes ({total_size / 1024 / 1024:.1f} MB)")
    print(f"Dossier: {OUT_DIR}")
    return OUT_DIR


if __name__ == "__main__":
    build()
