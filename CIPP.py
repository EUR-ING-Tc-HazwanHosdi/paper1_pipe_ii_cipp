import numpy as np
import matplotlib.pyplot as plt

def simulate_ii_diffusion(q0=50.0, mu=0.04, sigma=0.18, T=15.0, dt=0.01, simulations=500):
    n_steps = int(T / dt)
    t = np.linspace(0, T, n_steps)
    q_path = np.zeros((n_steps, simulations))
    q_path[0] = q0
    
    np.random.seed(42)
    for i in range(1, n_steps):
        dw = np.sqrt(dt) * np.random.randn(simulations)
        q_path[i] = q_path[i-1] + mu * q_path[i-1] * dt + sigma * q_path[i-1] * dw
        
    return t, q_path

t, paths = simulate_ii_diffusion()
mean_path = np.mean(paths, axis=1)
q_star = np.max(mean_path) * (1.0 / 1.5)

print(f"Baseline Initial Inflow (Q0): 50.0 L/s")
print(f"Simulated 15-Year Mean Terminal Inflow: {mean_path[-1]:.2f} L/s")
print(f"Calculated Optimal CIPP Intervention Trigger (Q*): {q_star:.2f} L/s")
