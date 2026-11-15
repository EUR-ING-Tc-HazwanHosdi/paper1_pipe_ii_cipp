import os

readme_content = """# Research Paper 1: Hybridizing Prescriptive Watertightness Commissioning (MSIG Vol. 1 & 3) and Stochastic Trenchless Rehabilitation to Mitigate Infiltration/Inflow in Sub-Arctic Sewer Networks

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://stochastic-lifecycle-energy-carbon-real-options-sizing-engine.streamlit.app/)
[![Zenodo DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24082089.svg)](https://doi.org/10.5281/zenodo.24082089)

---

## 📖 Overview
This repository contains the official core simulation scripts, empirical calibration datasets, and reproducible Google Colab notebooks for **Research Paper 1** of the independent doctoral research trilogy at the Norwegian University of Science and Technology (NTNU). 

The study develops a hybrid engineering framework combining Malaysia's centralized, prescriptive **SPAN MSIG Vol. 1 (Catchment Planning & Staged Handover Gates)** and **Vol. 3 (Sewer Networks & Watertightness Testing)** with continuous-time **Itô diffusion stochastic modeling** and **optimal stopping (*real options*)** to mitigate severe Infiltration/Inflow ($I/I$) in sub-arctic Norwegian wastewater networks.

---

## 📂 Repository Structure
```text
paper1-sub-arctic-ii-cipp/
│
├── README.md                      # Repository documentation & methodology overview
├── requirements.txt               # Python package dependencies (numpy, scipy, pandas, matplotlib)
├── notebooks/
│   └── 01_ssb_kostra_calibration.ipynb # Interactive calibration & Monte Carlo simulation notebook
└── core_models/
    └── paper1_pipe_ii_cipp.py     # Standalone continuous-time Itô diffusion & CIPP threshold solver
