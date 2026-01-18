# Amplitude Modulation Measurement Systems Visualizer

**Interactive simulation platform for analyzing AM-based transducer systems and dual-slope ADC behavior in real-time.**

---

## 📸 Demo

![Demo Screenshot Placeholder](https://via.placeholder.com/800x450. png? text=AM+Modulation+Visualization)  
*Interactive dashboard showing AM modulation, synchronous demodulation, and noise analysis*

---

## About

This application provides a hands-on visualization environment for understanding amplitude modulation in precision measurement systems. It models the complete signal chain from physical transduction (e.g., strain gauges, LVDTs) through carrier modulation and phase-sensitive demodulation.  The tool simulates realistic noise sources including white noise, 50Hz mains interference, and demonstrates dual-slope ADC integration—critical concepts in instrumentation and data acquisition systems.

**Problem it solves:** Engineers and students need to visualize how AM-based sensors respond to noise, modulation depth, and carrier frequency variations. This tool bridges theory and practice by providing real-time parameter manipulation and waveform inspection.

---

## 🛠️ Tech Stack

- **Python 3.x** - Core runtime
- **Streamlit** - Interactive web interface
- **NumPy** - Signal processing and numerical computation
- **Matplotlib** - Waveform visualization

---

## ✨ Key Features

- **Parametric AM Simulation** – Adjust carrier frequency (500-5000 Hz), signal frequency, and modulation depth in real-time
- **Multi-Source Noise Modeling** – Configurable white noise (Gaussian) and 50Hz harmonic interference with independent amplitude control
- **Synchronous Demodulation** – Phase-sensitive detection using sign-based carrier extraction
- **Dual-Slope ADC Emulation** – Visualize integration-based analog-to-digital conversion with adjustable input voltage

---

## 🚀 Installation & Usage

**Install dependencies:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install streamlit numpy matplotlib
```

**Run the application:**
```bash
streamlit run app.py
```

The app will launch in your default browser.  Use the sidebar controls to modify system parameters and observe signal transformations in real-time.

---

## 📖 Use Cases

- Academic demonstrations for measurement systems courses
- Prototyping sensor signal conditioning pipelines
- Evaluating noise rejection in bridge circuits and synchronous detectors

---

*Built for engineers who need to visualize the invisible.*