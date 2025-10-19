import numpy as np
import matplotlib.pyplot as plt
import time
import csv

# ---- Load CSV manually (no pandas) ----
data = []
with open("fault_data.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        try:
            val = float(row[-1])  # last column if multiple
            data.append(val)
        except:
            continue

data = np.array(data)

# ---- Parameters ----
SAMPLE_RATE = 1000   # Hz
WINDOW_SIZE = 256    # samples for FFT
REFRESH_DELAY = 0.05 # seconds between updates

# ---- FFT feature extraction ----
def analyze_signal(window):
    n = len(window)
    fft_vals = np.fft.fft(window)
    freq = np.fft.fftfreq(n, d=1/SAMPLE_RATE)
    mag = np.abs(fft_vals[:n//2])
    freq = freq[:n//2]

    # fundamental (50Hz)
    f_idx = np.argmin(np.abs(freq - 50))
    fund = mag[f_idx]

    # harmonics above 100Hz
    harmonics = mag[freq > 100]
    harmonic_ratio = np.sum(harmonics) / np.sum(mag)

    # peak ratio
    peak = np.max(window) / (np.sqrt(np.mean(window**2)) + 1e-6)

    # thresholds
    alarm = "YES" if (fund < 0.4 or harmonic_ratio > 0.25 or peak > 1.5) else "NO"

    return fund, harmonic_ratio, peak, alarm

# ---- Live Plot ----
plt.ion()
fig, ax = plt.subplots(figsize=(8, 4))
line, = ax.plot([], [], lw=1.5)
ax.set_ylim(-1, 1)
ax.set_xlim(0, WINDOW_SIZE)
ax.set_title("Real-time Fault Simulation")
ax.set_xlabel("Samples")
ax.set_ylabel("Amplitude")
text_box = ax.text(0.02, 0.9, "", transform=ax.transAxes, fontsize=12, color="red")

# ---- Simulation loop ----
for i in range(WINDOW_SIZE, len(data)):
    window = data[i-WINDOW_SIZE:i]
    fund, h, p, alarm = analyze_signal(window)

    line.set_xdata(np.arange(WINDOW_SIZE))
    line.set_ydata(window)
    text_box.set_text(f"Alarm: {alarm}")
    ax.set_title(f"FFT Simulation | Fund={fund:.2f}, Harm={h:.2f}, Peak={p:.2f}")

    plt.pause(REFRESH_DELAY)

plt.ioff()
plt.show()
