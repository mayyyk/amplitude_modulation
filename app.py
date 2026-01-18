import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Measurement Systems Visualization: AM & Dual-Slope ADC")

# Sidebar for AM Parameters
st.sidebar.header("AM Modulation Parameters")
F = st.sidebar.slider("Carrier Frequency (F) [Hz]", 500, 5000, 2000)
fg = st.sidebar.slider("Signal Frequency (fg) [Hz]", 10, 200, 50)
mod_depth = st.sidebar.slider("Modulation Depth (Strain)", 0.1, 1.0, 0.5) # tensometer constant
white_noise_mean = st.sidebar.slider("White Noise Mean", -0.1, 0.1, 0.0)
white_noise_std_dev = st.sidebar.slider("White Noise Standard Devation", 0.0, 0.1, 0.01)
A_50 = st.sidebar.slider("50 HZ Noise Amplitude", 0.0, 0.2, 0.05)

# Sidebar for ADC Parameters
st.sidebar.header("Dual-Slope ADC Parameters")
vin = st.sidebar.slider("Input Voltage (Vin)", 0.5, 5.0, 2.5)
vref = -5.0 # Fixed reference
t1 = 100 # Fixed integration time units

# --- SECTION 1: AM MODULATION ---
st.header("1. AM Modulation and Synchronous Demodulation")
col1, col2 = st.columns(2)

t_am = np.arange(0, 0.1, 0.00005)
carrier = np.sin(2 * np.pi * F * t_am)
meas_signal = mod_depth * np.sin(2 * np.pi * fg * t_am)

# noise
size = len(t_am)

noise_white = np.random.normal(white_noise_mean, white_noise_std_dev, size)

noise_50hz = A_50 * np.sin(2 * np.pi * 50 * t_am)

# noise_drift = np.linspace(start_offset, end_offset, size) # thermo-electrical forces

total_noise = noise_50hz + noise_white

# AM Signal as seen in a bridge or LVDT
modulated = (meas_signal * carrier ) + total_noise
# Synchronous Demodulation: Multiplying by sign of carrier
demod_raw = modulated * np.sign(carrier)

with col1:
    fig1, ax1 = plt.subplots(3, 1)
    ax1[0].plot(t_am, meas_signal, 'r', label="Measured Signal (Physical)")
    ax1[0].set_title("Input (e.g. Strain)")
    ax1[0].legend()
    
    ax1[1].plot(t_am, total_noise, 'r', label="Noise (Physical)")
    ax1[1].set_title("Signal noise")
    ax1[1].legend()
    
    ax1[2].plot(t_am, modulated, 'b', label="Modulated Carrier (AC Supply)")
    ax1[2].set_title("Bridge Output (AM Signal)")
    ax1[2].legend()

    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots(2, 1)
    ax2[0].plot(t_am, demod_raw, 'g', label="After Phase-Sensitive Demodulator")
    ax2[0].set_title("Demodulated (Raw)")
    ax2[0].legend()
    # Simple LPF simulation (Moving average)
    lpf_signal = np.convolve(demod_raw, np.ones(20)/20, mode='same')
    ax2[1].plot(t_am, lpf_signal, 'black', linewidth=2, label="After LPF (Output)")
    ax2[1].set_title("Recovered Measurement")
    ax2[1].legend()
    st.pyplot(fig2)

# --- SECTION 2: DUAL-SLOPE ADC ---
st.header("2. Dual-Slope ADC Integration (Voltage to Time)")
st.write(f"Integrating $V_{{in}} = {vin}V$ then de-integrating with $V_{{ref}} = {vref}V$.")

# Phase 1: Charge
t_phase1 = np.arange(0, t1)
slope1 = (vin / 10) * t_phase1 # simplified RC constant
v_cap_end = slope1[-1]

# Phase 2: Discharge
# Time to discharge: v_cap_end + (vref/10)*t = 0 -> t = -v_cap_end / (vref/10)
t2 = int(abs(v_cap_end / (vref / 10)))
t_phase2 = np.arange(0, t2)
slope2 = v_cap_end + (vref / 10) * t_phase2

# Combine
t_total = np.concatenate([t_phase1, t_phase1[-1] + t_phase2])
v_total = np.concatenate([slope1, slope2])

fig3, ax3 = plt.subplots(figsize=(10, 4))
ax3.plot(t_total, v_total, color='purple', linewidth=3)
ax3.axvline(x=t1, color='gray', linestyle='--', label="T1 (Fixed Integration)")
ax3.axvline(x=t1+t2, color='orange', linestyle='--', label=f"T2 (Measured Time: {t2})")
ax3.fill_between(t_total, v_total, alpha=0.2, color='purple')
ax3.set_xlabel("Time (Clock Cycles)")
ax3.set_ylabel("Capacitor Voltage (V_cap)")
ax3.set_title("Dual-Slope Integration Process")
ax3.legend()
st.pyplot(fig3)

st.info(f"Final Calculation: $T_2$ is {t2} cycles. Notice how $T_2$ changes linearly with $V_{{in}}$.")