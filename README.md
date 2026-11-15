# Hybrid MSIG & Stochastic CIPP Real Options Framework

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://paper1pipeiicipp-zymat3ebvyjqerfu6xfxdj.streamlit.app/)

An interactive stochastic engineering and financial decision-support tool for sub-arctic municipal sewer rehabilitation. This application implements the analytical and Monte Carlo framework from the manuscript:

> **Hybridizing Prescriptive Watertightness Commissioning (MSIG Vol. 1 & 3) and Stochastic Trenchless Rehabilitation to Mitigate Infiltration/Inflow in Sub-Arctic Sewer Networks**  
> *EUR ING Tc. Hazwan Bin Hosdi*

---

## Overview

Municipal wastewater networks in sub-arctic regions (such as Norway, tracked via Statistics Norway's **SSB KOSTRA** database) face severe structural deficits driven by aging mid-century assets, shallow granite bedrock excavation constraints, low annual pipeline renewal rates ($0.66\%$), and high extraneous **Infiltration and Inflow (I/I)** from freeze-thaw cycles and spring snowmelt surges. Furthermore, traditional Closed-Circuit Television (CCTV) inspections suffer from up to $47.5\%$ inter-operator reproducibility variance.

This repository provides a reproducible simulation engine that bridges two complementary lifecycle controls:
1. **Front-End Prescriptive Governance (SPAN MSIG Vol. 1 & Vol. 3):** Models the impact of enforcing mandatory low-pressure air and hydrostatic watertightness testing prior to statutory asset handover to eliminate initial construction defects.
2. **Back-End Stochastic Control & Real Options (Itô Diffusion):** Models continuous-time I/I escalation via Geometric Brownian Motion (GBM) and computes the closed-form **Dixit-Pindyck optimal stopping boundary ($Q^*$)** for trenchless **Cured-In-Place Pipe (CIPP)** structural relining over open-cut bedrock excavation.

---

## Key Features

* **Exact Itô Diffusion Monte Carlo Engine:** Simulates up to $2,500$ log-normal trajectories of extraneous water ingress ($Q_{I/I,t}$) governed by freeze-thaw joint drift ($\mu_{ft}$) and spring snowmelt surge volatility ($\sigma_{\text{snow}}$).
* **Analytical Dixit-Pindyck Real Options Solver:** Computes the characteristic root ($\beta_1$), option deferral wedge ($\frac{\beta_1}{\beta_1 - 1}$), static Marshallian NPV threshold ($Q_{\text{npv}}$), and optimal CIPP intervention trigger ($Q^*$).
* **CCTV Inspection Subjectivity Module:** Incorporates observation noise ($\sigma_{\text{CCTV}}$) to demonstrate how visual condition-rating variance triggers premature capital interventions compared to continuous flow diffusion.
* **Bedrock CapEx Comparison:** Evaluates direct capital savings of trenchless CIPP relining ($K_{\text{CIPP}}$) versus open-cut excavation in shallow granite bedrock ($K_{\text{open-cut}}$).
* **Publication-Ready Outputs:** Generates first-passage stopping time distributions ($\tau^*$), cumulative intervention probability curves, and downloadable CSV summary tables aligned with Manuscript Section 4.1.

---

## Mathematical Formulation

### 1. Sub-Arctic I/I Stochastic Process
Extraneous inflow $Q_{I/I,t}$ evolves according to the continuous-time Itô stochastic differential equation:

$$dQ_{I/I,t} = \mu_{ft} Q_{I/I,t} \, dt + \sigma_{\text{snow}} Q_{I/I,t} \, dW_t$$

Using exact log-normal discretization over step $\Delta t$:

$$Q_{I/I,t+\Delta t} = Q_{I/I,t} \exp\left[ \left(\mu_{ft} - \frac{1}{2}\sigma_{\text{snow}}^2\right)\Delta t + \sigma_{\text{snow}} \sqrt{\Delta t}\, Z_t \right], \quad Z_t \sim \mathcal{N}(0, 1)$$

### 2. Optimal CIPP Relining Trigger ($Q^*$)
Minimizing expected discounted operating penalties and irreversible rehabilitation CapEx ($K_{\text{CIPP}}$) over an infinite horizon yields the smooth-pasting free boundary:

$$Q^* = \left(\frac{\beta_1}{\beta_1 - 1}\right) \frac{(r - \mu_{ft}) K_{\text{CIPP}}}{c \, \eta}$$

where:

$$\beta_1 = \frac{1}{2} - \frac{\mu_{ft}}{\sigma_{\text{snow}}^2} + \sqrt{\left(\frac{\mu_{ft}}{\sigma_{\text{snow}}^2} - \frac{1}{2}\right)^2 + \frac{2r}{\sigma_{\text{snow}}^2}}$$

---

## Local Installation & Usage

### Prerequisites
* Python 3.9 or higher

### Setup
1. Clone this repository:
   ```bash
   git clone [https://github.com/](https://github.com/)<your-username>/<your-repo-name>.git
   cd <your-repo-name>
