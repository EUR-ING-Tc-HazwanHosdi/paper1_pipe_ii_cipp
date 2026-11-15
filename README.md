# Hybridizing Prescriptive Watertightness Commissioning (MSIG Vol. 1 & 3) and Stochastic Trenchless Rehabilitation to Mitigate Infiltration/Inflow in Sub-Arctic Sewer Networks

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Complete](https://img.shields.io/badge/Status-Research%20Paper%20Ready-success.svg)]()

This repository contains the official codebase, data pipelines, and simulation engine for **Research Paper 1**. The project establishes a novel cross-climatic engineering framework that bridges Malaysia's centralized prescriptive commissioning standards (**SPAN MSIG Vol. 1 & Vol. 3**) with continuous-time **Itô diffusion stochastic modeling** and **real options theory** to optimize trenchless sewer rehabilitation in sub-arctic regions like Norway.

---

## 📂 Repository Structure

```text
├── data/
│   ├── raw/                 # SSB KOSTRA StatBank tables & Norsk Vann guidelines metadata
│   └── processed/           # Calibrated time-series baseline matrices
├── notebooks/
│   └── 01_ssb_kostra_calibration.ipynb  # Empirical data exploration & calibration
├── src/
│   └── paper1_pipe_ii_cipp.py           # Core Itô diffusion & optimal stopping engine
├── outputs/                 # Generated Monte Carlo plots and convergence data
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## 🔬 Methodology Overview

1. **Front-End Quality Governance:** Implements SPAN MSIG Vol. 1 multi-stage handover gates and Vol. 3 stringent air/water pressure testing criteria to achieve a zero-$I/I$ baseline on new assets.
2. **Stochastic Deterioration Modeling:** Models legacy joint failure and spring snowmelt surges using continuous-time Itô diffusion:
   $$\mathrm{d}Q_{I/I}(t) = \mu_{ft} Q_{I/I}(t)\mathrm{dt} + \sigma_{snow} Q_{I/I}(t)\mathrm{d}W_t$$
3. **Optimal Stopping (*Real Options*):** Computes the critical economic and structural threshold ($Q^*$ dictating the precise timing for trenchless Cured-In-Place Pipe (CIPP) relining over disruptive open-cut trenching in shallow bedrock.

---

## 🚀 Getting Started

### Prerequisites
Ensure you have Python 3.9 or higher installed. Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

### Running the Simulation Engine
Execute the core script to simulate Monte Carlo Itô diffusion paths and calculate the optimal CIPP trigger threshold:

```bash
python src/paper1_pipe_ii_cipp.py
```

---

## 📊 Key Parameters & Calibration
* **Renewal Rate Baseline:** Calibrated to Statistics Norway (SSB KOSTRA) municipal averages (**0.66%**)
