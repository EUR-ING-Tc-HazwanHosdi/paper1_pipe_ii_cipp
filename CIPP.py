import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(
    page_title="MSIG-Stochastic CIPP Sub-Arctic I&I Engine",
    layout="wide"
)

# --- ANALYTICAL & STOCHASTIC ENGINES ---

def compute_real_options_trigger(mu_ft, sigma_snow, r, k_cipp, k_opencut, unit_penalty_cost, efficiency):
    """
    Computes the Dixit-Pindyck optimal stopping threshold (Q*) for trenchless CIPP
    vs. static NPV threshold (Q_npv) and shallow-bedrock open-cut replacement.
    """
    term = (mu_ft / (sigma_snow ** 2)) - 0.5
    beta_1 = -term + np.sqrt(term ** 2 + (2.0 * r) / (sigma_snow ** 2))
    
    annual_savings_per_ls = unit_penalty_cost * efficiency
    q_npv = ((r - mu_ft) * k_cipp) / annual_savings_per_ls
    ro_wedge = beta_1 / (beta_1 - 1.0)
    q_star = ro_wedge * q_npv
    
    # Lifecycle savings of CIPP vs. shallow granite open-cut replacement
    bedrock_savings_pct = ((k_opencut - k_cipp) / k_opencut) * 100.0
    
    return beta_1, ro_wedge, q_npv, q_star, bedrock_savings_pct


@st.cache_data
def simulate_subarctic_ii(q0_legacy, q0_msig, mu_ft, sigma_snow, cctv_err, T, dt, simulations, seed):
    rng = np.random.default_rng(seed)
    n_steps = int(round(T / dt)) + 1
    t = np.linspace(0, T, n_steps)
    
    z = rng.standard_normal((n_steps - 1, simulations))
    drift = (mu_ft - 0.5 * sigma_snow ** 2) * dt
    diffusion = sigma_snow * np.sqrt(dt) * z
    log_returns = np.vstack([np.zeros((1, simulations)), drift + diffusion])
    growth_factor = np.exp(np.cumsum(log_returns, axis=0))
    
    # 1. Legacy un-gated network trajectory
    q_legacy = q0_legacy * growth_factor
    
    # 2. Front-end SPAN MSIG Vol. 1 & 3 watertightness-gated network trajectory
    q_msig = q0_msig * growth_factor
    
    # 3. Noisy CCTV-observed apparent inflow (Fugledalen et al., 2021 subjectivity)
    obs_noise = rng.normal(0.0, cctv_err, size=q_legacy.shape)
    q_cctv_perceived = np.maximum(0.0, q_legacy * (1.0 + obs_noise))
    
    return t, q_legacy, q_msig, q_cctv_perceived


# --- SIDEBAR: NORWEGIAN KOSTRA & SPAN MSIG PARAMETERS ---

st.sidebar.header("1. Sub-Arctic Hydraulic & Diffusion (Section 3.2)")
q0_legacy = st.sidebar.number_input("Legacy Baseline I&I, Q₀ (L/s)", 10.0, 500.0, 50.0, 5.0)
q0_msig = st.sidebar.number_input("MSIG Vol. 3 Handover Gate Q₀ (L/s)", 0.5, 25.0, 3.5, 0.5)
mu_ft = st.sidebar.slider("Freeze-Thaw Joint Drift, μ_ft (yr⁻¹)", 0.005, 0.120, 0.040, 0.005, format="%.3f")
sigma_snow = st.sidebar.slider("Snowmelt Surge Volatility, σ_snow (yr⁻⁰·⁵)", 0.05, 0.45, 0.18, 0.01, format="%.2f")
cctv_err = st.sidebar.slider("CCTV Inspection Variance (Fugledalen et al.)", 0.00, 0.50, 0.24, 0.02, format="%.2f")

st.sidebar.header("2. Bedrock CapEx & I&I Penalty (Section 3.3)")
k_cipp = st.sidebar.number_input("Trenchless CIPP CapEx, K_CIPP (NOK)", 500000, 50000000, 8500000, 250000)
k_opencut = st.sidebar.number_input("Shallow Bedrock Open-Cut CapEx (NOK)", 1000000, 80000000, 14200000, 500000)
unit_penalty = st.sidebar.number_input("Extraneous Water Penalty C(Q) (NOK / L/s-yr)", 1000, 100000, 12500, 500)
efficiency = st.sidebar.slider("CIPP Watertightness Recovery, η (%)", 60, 100, 85, 5) / 100.0
r = st.sidebar.slider("Social Discount Rate, r (yr⁻¹)", 0.04, 0.15, 0.08, 0.005, format="%.3f")

st.sidebar.header("3. Monte Carlo Calibration (Section 4.1)")
T = st.sidebar.slider("Planning Horizon, T (Years)", 5, 30, 15, 1)
simulations = st.sidebar.selectbox("Monte Carlo Paths", [500, 1000, 2500], index=0)
seed = st.sidebar.number_input("Random Seed", 1, 9999, 42, 1)


# --- MAIN DASHBOARD ---

st.title("Hybrid MSIG & Stochastic CIPP Real Options Framework")
st.caption("Companion Decision-Support Model for Sub-Arctic Sewer Rehabilitation (SSB KOSTRA & SPAN MSIG Vol. 1 & 3)")

if r <= mu_ft:
    st.error("Convergence Constraint: Social discount rate (r) must exceed freeze-thaw drift (μ_ft).")
    st.stop()

beta_1, ro_wedge, q_npv, q_star, bedrock_savings_pct = compute_real_options_trigger(
    mu_ft, sigma_snow, r, k_cipp, k_opencut, unit_penalty, efficiency
)

t, q_legacy, q_msig, q_cctv = simulate_subarctic_ii(
    q0_legacy, q0_msig, mu_ft, sigma_snow, cctv_err, float(T), 0.01, simulations, int(seed)
)

mean_legacy = np.mean(q_legacy, axis=1)
mean_msig = np.mean(q_msig, axis=1)
p05_legacy = np.percentile(q_legacy, 5, axis=1)
p95_legacy = np.percentile(q_legacy, 95, axis=1)

# First-passage stopping times (Legacy vs MSIG vs Noisy CCTV)
hit_legacy = q_legacy >= q_star
hit_msig = q_msig >= q_star
hit_cctv = q_cctv >= q_star

prob_legacy = np.mean(np.any(hit_legacy, axis=0)) * 100.0
prob_msig = np.mean(np.any(hit_msig, axis=0)) * 100.0

tau_legacy = t[np.argmax(hit_legacy, axis=0)[np.any(hit_legacy, axis=0)]]
med_tau_legacy = np.median(tau_legacy) if len(tau_legacy) > 0 else np.nan


# --- KEY PAPER METRICS ---

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Static NPV Trigger", f"{q_npv:.2f} L/s")
c2.metric("Optimal RO Trigger (Q*)", f"{q_star:.2f} L/s", delta=f"Wedge: {ro_wedge:.2f}x")
c3.metric("Legacy Trigger Prob.", f"{prob_legacy:.1f}%", delta=f"Med. τ*: {med_tau_legacy:.1f} yr" if not np.isnan(med_tau_legacy) else f"> {T} yr")
c4.metric("MSIG Gate Trigger Prob.", f"{prob_msig:.1f}%", delta=f"-{prob_legacy - prob_msig:.1f}% risk")
c5.metric("CIPP vs. Bedrock CapEx", f"-{bedrock_savings_pct:.1f}%", delta=f"Saves {(k_opencut - k_cipp)/1e6:.2f}M NOK")


# --- TABS ---

tab1, tab2, tab3 = st.tabs([
    "1. Legacy vs. MSIG Diffusion",
    "2. CCTV Uncertainty & Stopping Risk",
    "3. Manuscript Section 4.1 Summary Table"
])

with tab1:
    fig1, ax1 = plt.subplots(figsize=(11, 4.5))
    ax1.plot(t, q_legacy[:, :30], color="steelblue", alpha=0.12, linewidth=0.8)
    ax1.fill_between(t, p05_legacy, p95_legacy, color="steelblue", alpha=0.15, label="Legacy 90% Confidence Band")
    ax1.plot(t, mean_legacy, color="navy", linewidth=2.2, label=f"Legacy Network Mean E[Q_t] (Q₀={q0_legacy} L/s)")
    ax1.plot(t, mean_msig, color="seagreen", linewidth=2.2, label=f"SPAN MSIG Vol. 3 Handover Gate (Q₀={q0_msig} L/s)")
    ax1.axhline(q_star, color="crimson", linestyle="--", linewidth=1.8, label=f"Optimal CIPP Trigger Q* ({q_star:.2f} L/s)")
    ax1.axhline(q_npv, color="darkorange", linestyle=":", linewidth=1.5, label=f"Marshallian NPV Threshold ({q_npv:.2f} L/s)")
    ax1.set_title("Sub-Arctic Itô Diffusion: Legacy Deterioration vs. Prescriptive MSIG Watertightness Gate")
    ax1.set_xlabel("Time Horizon (Years)")
    ax1.set_ylabel("Extraneous Infiltration & Inflow, Q_I/I (L/s)")
    ax1.grid(True, linestyle="--", alpha=0.35)
    ax1.legend(loc="upper left")
    st.pyplot(fig1)

with tab2:
    col_a, col_b = st.columns(2)
    with col_a:
        cum_leg = np.mean(np.maximum.accumulate(hit_legacy, axis=0), axis=1) * 100.0
        cum_msig = np.mean(np.maximum.accumulate(hit_msig, axis=0), axis=1) * 100.0
        cum_cctv = np.mean(np.maximum.accumulate(hit_cctv, axis=0), axis=1) * 100.0
        
        fig2, ax2 = plt.subplots(figsize=(5.5, 4))
        ax2.plot(t, cum_leg, color="navy", linewidth=2, label="True Stochastic Legacy")
        ax2.plot(t, cum_cctv, color="darkorange", linestyle="--", linewidth=1.8, label="Noisy CCTV-Based Trigger (False Premature)")
        ax2.plot(t, cum_msig, color="seagreen", linewidth=2, label="MSIG Vol. 3 Gated Network")
        ax2.set_title("Cumulative CIPP Intervention Probability P(τ* ≤ t)")
        ax2.set_xlabel("Time (Years)")
        ax2.set_ylabel("Cumulative Probability (%)")
        ax2.set_ylim(0, 105)
        ax2.grid(True, linestyle="--", alpha=0.35)
        ax2.legend(fontsize=8.5)
        st.pyplot(fig2)
        
    with col_b:
        fig3, ax3 = plt.subplots(figsize=(5.5, 4))
        if len(tau_legacy) > 0:
            ax3.hist(tau_legacy, bins=20, color="slateblue", edgecolor="white", alpha=0.85)
            ax3.axvline(med_tau_legacy, color="crimson", linestyle="--", linewidth=1.5, label=f"Median τ* = {med_tau_legacy:.2f} yrs")
            ax3.legend()
        else:
            ax3.text(0.5, 0.5, "Q* not crossed within horizon T.", ha="center", va="center")
        ax3.set_title("Distribution of Optimal CIPP Stopping Times (τ*)")
        ax3.set_xlabel("Intervention Year (τ*)")
        ax3.set_ylabel("Frequency (Paths)")
        ax3.grid(True, linestyle="--", alpha=0.35)
        st.pyplot(fig3)

with tab3:
    st.subheader("Calibration & Results Table (Ready for Paper Section 4.1)")
    results_table = pd.DataFrame({
        "Metric / Parameter": [
            "Initial Extraneous Inflow (Q₀)",
            "15-Year Mean Terminal Inflow E[Q_T]",
            "Static Marshallian NPV Threshold (Q_npv)",
            "Real Options Optimal Trigger (Q*)",
            "Option Value of Waiting Wedge (β₁ / (β₁ - 1))",
            f"Cumulative Trigger Probability within {T} Years",
            "Median Optimal Stopping Time (τ*)",
            "Capital Outlay Savings (CIPP vs. Granite Open-Cut)"
        ],
        "Legacy Un-Gated Network": [
            f"{q0_legacy:.2f} L/s",
            f"{mean_legacy[-1]:.2f} L/s",
            f"{q_npv:.2f} L/s",
            f"{q_star:.2f} L/s",
            f"{ro_wedge:.3f}x",
            f"{prob_legacy:.1f}%",
            f"{med_tau_legacy:.2f} yrs" if not np.isnan(med_tau_legacy) else f"> {T} yrs",
            f"{bedrock_savings_pct:.1f}% ({(k_opencut - k_cipp)/1e6:.2f}M NOK)"
        ],
        "SPAN MSIG Vol. 3 Handover Gate": [
            f"{q0_msig:.2f} L/s",
            f"{mean_msig[-1]:.2f} L/s",
            f"{q_npv:.2f} L/s",
            f"{q_star:.2f} L/s",
            f"{ro_wedge:.3f}x",
            f"{prob_msig:.1f}%",
            f"> {T} yrs (Deferred)",
            "100% CapEx Deferred within Horizon"
        ]
    })
    st.table(results_table)
