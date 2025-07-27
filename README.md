# Schwarzschild Black Hole Orbital Simulation

This Python project simulates the orbit of a test particle around a Schwarzschild (non-rotating) black hole using relativistic corrections from General Relativity. It models the curvature of spacetime via the effective potential and visualizes orbital precession.

---

## Theory

In polar coordinates (r, φ), we define u(φ) = 1 / r. The relativistic orbital equation becomes:

**d²u/dφ² + u = (GM) / L² + 3GMu²**

This nonlinear second-order ODE accounts for:
- Orbital precession
- Photon sphere behavior
- Deviation from Newtonian orbits

---

## Code Overview

1. **Libraries**: Uses `numpy`, `scipy`, `matplotlib`, and `Pillow` (for GIF export).
2. **Physics**: Implements relativistic motion using Schwarzschild spacetime.
3. **ODE Solver**: Integrates using SciPy's `solve_ivp` (Runge-Kutta 45).
4. **Visualization**: Polar trajectory converted to Cartesian (x, y) for plotting and animation.
5. **Output**: A smooth animated GIF of the particle orbit.

---

## Demo

![Black Hole Orbit Animation](orbit.gif)

---

## Assumptions

- Particle is massless (test particle); does not curve spacetime.
- Black hole is static and non-rotating (Schwarzschild).
- No external forces; the environment is a perfect vacuum.
- Time dilation and redshift are not included—purely spatial motion.

---

## Limitations

- Simulated in 2D only.
- No frame-dragging effects (Kerr metric not used).
- No general spacetime diagram—only geometric orbits.
- Simulation may become unstable if r → 0 (falling into event horizon).

---

## Requirements

- Python 3.x
- `numpy`
- `scipy`
- `matplotlib`
- `pillow`

### Install dependencies:

```bash
pip install numpy scipy matplotlib pillow
