import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def simulate_ii_diffusion(q0=50.0, mu=0.04, sigma=0.18, T=15.0, dt=0.01, simulations=500, seed=42):
    rng = np.random.default_rng(seed)
    n_steps = int(round(T / dt)) + 1
    t = np.linspace(0, T, n_steps)
    
    # Vectorized exact Geometric Brownian Motion
    z = rng.standard_normal((n_steps - 1, simulations))
    drift = (mu - 0.5 * sigma**2) * dt
    diffusion = sigma * np.sqrt(dt) * z
    
    log_returns = np.vstack([np.zeros((1, simulations)), drift + diffusion])
    q_path = q0 * np.exp(np.cumsum(log_returns, axis=0))
    
    return t, q_path

st.title("Stochastic I&I Diffusion & CIPP Intervention Model")

t, paths = simulate_ii_diffusion()
mean_path = np.mean(paths, axis=1)
q_star = np.max(mean_path) * (1.0 / 1.5)

col1, col2, col3 = st.columns(3)
col1.metric("Baseline Inflow (Q₀)", "50.00 L/s")
col2.metric("15-Yr Mean Terminal Inflow", f"{mean_path[-1]:.2f} L/s")
col3.metric("CIPP Trigger (Q*)", f"{q_star:.2f} L/s")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(t, paths[:, :30], color="steelblue", alpha=0.15, linewidth=0.8)
ax.plot(t, mean_path, color="navy", linewidth=2, label="Mean I&I Path")
ax.axhline(q_star, color="crimson", linestyle="--", linewidth=1.5, label=f"Intervention Trigger Q* ({q_star:.2f} L/s)")
ax.set_xlabel("Time (Years)")
ax.set_ylabel("Infiltration & Inflow (L/s)")
ax.legend()
st.pyplot(fig)
