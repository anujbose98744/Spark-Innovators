import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert

FS = 8000  # 8 kHz sampling
T = 1.0    # 1 second window
t = np.linspace(0, T, int(FS*T), endpoint=False)

# 1?? Normal 50Hz sine (no fault)
normal_signal = np.sin(2*np.pi*50*t)

# 2?? Fault signal (simulate arcing: distorted + noisy)
fault_signal = np.sin(2*np.pi*50*t) + 0.3*np.sin(2*np.pi*150*t) + 0.05*np.random.randn(len(t))

# 3?? Envelope using Hilbert transform
envelope_normal = np.abs(hilbert(normal_signal))
envelope_fault = np.abs(hilbert(fault_signal))

plt.figure(figsize=(10,5))
plt.subplot(2,1,1)
plt.plot(t[:1000], normal_signal[:1000], label='Normal 50Hz')
plt.plot(t[:1000], fault_signal[:1000], label='Fault (noisy)', alpha=0.7)
plt.legend(); plt.title("Simulated Voltage Waveforms")

plt.subplot(2,1,2)
plt.plot(t[:1000], envelope_normal[:1000], label='Envelope Normal')
plt.plot(t[:1000], envelope_fault[:1000], label='Envelope Fault', alpha=0.7)
plt.legend(); plt.tight_layout()
plt.show()
