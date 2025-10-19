# ================================================================
#  Low-Voltage Line Breakage / Fault Detection  (Simulation + FFT)
#  Works on Raspberry Pi 3 or Windows
#  Author: your SIH project team
# ================================================================

import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime

# ---------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------
SAMPLE_RATE = 1000      # samples per second
WINDOW_SIZE = 1024      # FFT window length
THRESHOLD_FUND = 0.4    # minimum fundamental amplitude
THRESHOLD_HARM = 0.25   # ratio of harmonic energy / total
THRESHOLD_PEAK = 1.5    # RMS peaks trigger alarm

SHOW_PLOT = True        # turn False on Pi if headless

# ---------------------------------------------------------------
# SYNTHETIC SIGNAL GENERATOR (simulate healthy/faulty cases)
# ---------------------------------------------------------------
def generate_signal(fault=False):
    """Generate a test current waveform"""
    t = np.arange(WINDOW_SIZE) / SAMPLE_RATE
    # Base 50 Hz waveform
    current = 1.0 * np.sin(2 * np.pi * 50 * t)

    # Add normal background noise
    current += 0.05 * np.random.randn(len(t))

    if fault:
        # simulate breakage: spikes + distortion
        for k in range(0, len(t), 100):
            current[k:k+3] += np.random.uniform(2, 3)
        current += 0.4 * np.sin(2 * np.pi * 150 * t)  # harmonic
    return current


# ---------------------------------------------------------------
# FFT-BASED FEATURE EXTRACTION
# ---------------------------------------------------------------
def extract_features(signal):
    """Return fundamental, harmonic ratio, peak RMS"""
    fft_vals = np.fft.fft(signal)
    mag = np.abs(fft_vals[:WINDOW_SIZE // 2])
    freqs = np.fft.fftfreq(WINDOW_SIZE, 1 / SAMPLE_RATE)[:WINDOW_SIZE // 2]

    # Identify 50 Hz component
    idx_50 = np.argmin(np.abs(freqs - 50))
    fund = mag[idx_50]

    # Compute harmonic energy above 100 Hz
    harm_energy = np.sum(mag[freqs > 100] ** 2)
    total_energy = np.sum(mag ** 2)
    harmonic_ratio = harm_energy / total_energy if total_energy > 0 else 0

    # Peak RMS level
    rms = np.sqrt(np.mean(signal ** 2))
    peak = np.max(np.abs(signal)) / (rms + 1e-6)

    return fund, harmonic_ratio, peak


# ---------------------------------------------------------------
# ALARM DECISION LOGIC
# ---------------------------------------------------------------
def detect_fault(fund, harmonic_ratio, peak):
    """Return True if abnormal signature detected"""
    if fund < THRESHOLD_FUND:
        return True
    if harmonic_ratio > THRESHOLD_HARM:
        return True
    if peak > THRESHOLD_PEAK:
        return True
    return False


# ---------------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------------
def main():
    print("=== FFT-Based Breakage / Fault Detection ===")
    print("Press Ctrl+C to stop\n")

    if SHOW_PLOT:
        plt.ion()
        fig, ax = plt.subplots()
        line, = ax.plot([], [])
        ax.set_ylim(-4, 4)
        ax.set_xlim(0, WINDOW_SIZE)
        ax.set_title("Live Current Waveform")

    try:
        while True:
            # Alternate between healthy and faulty signals every few cycles
            fault_state = np.random.rand() > 0.7
            signal = generate_signal(fault=fault_state)

            f, h, p = extract_features(signal)
            alarm = detect_fault(f, h, p)

            # --- Display results (avoid Unicode arrows) ---
            print(f"[{datetime.now().strftime('%H:%M:%S')}]  "
                  f"Fund={f:.2f}  HarmRatio={h:.3f}  Peak={p:.2f}  "
                  f"Alarm={'YES' if alarm else 'NO'}")

            if SHOW_PLOT:
                line.set_data(range(len(signal)), signal)
                ax.figure.canvas.draw()
                ax.figure.canvas.flush_events()

            # optional delay to simulate sample update
            time.sleep(1.0)

    except KeyboardInterrupt:
        print("\nStopped by user.")
        if SHOW_PLOT:
            plt.ioff()
            plt.close()

# ---------------------------------------------------------------
if __name__ == "__main__":
    main()