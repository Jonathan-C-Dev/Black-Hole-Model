# Schwarzschild Black Hole Orbital Simulation

This Python project simulates the orbit of a test particle around a Schwarzschild (non-rotating) black hole using relativistic corrections derived from General Relativity. The system models orbital motion under curved spacetime using the effective potential and visualizes the trajectory.

---

## Theory

In polar coordinates \((r, \phi)\), we express the radial motion using the inverse radius \(u(\phi) = \frac{1}{r}\). The relativistic orbital equation derived from the Schwarzschild metric is:

\[
\frac{d^2 u}{d\phi^2} + u = \frac{GM}{L^2} + 3GMu^2
\]

where:

- \( u = \frac{1}{r} \) is the inverse radial coordinate
- \( G \) is the gravitational constant
- \( M \) is the mass of the black hole
- \( L \) is the angular momentum per unit mass

This nonlinear second-order ODE accounts for relativistic effects like orbital precession and photon sphere instabilities.

---

## Code Logic

### 1. Import Libraries
- `numpy` and `scipy` for numerical computation and ODE solving
- `matplotlib` for plotting and animation
- `PIL` (`pillow`) for saving the animation as a GIF

### 2. Constants and Parameters
- Schwarzschild radius: \( r_s = \frac{2GM}{c^2} \)
- Adjustable constants: initial radius, angular momentum, and number of steps

### 3. Equations of Motion
The second-order ODE is rewritten as a system of first-order ODEs:
- Let \( y_0 = u(\phi) \)
- Let \( y_1 = \frac{du}{d\phi} \)

\[
\begin{cases}
\frac{dy_0}{d\phi} = y_1 \\
\frac{dy_1}{d\phi} = -y_0 + \frac{GM}{L^2} + 3GM y_0^2
\end{cases}
\]

### 4. Numerical Solver
- `solve_ivp` with method `"RK45"` integrates the ODE system over \(\phi\)

### 5. Convert to Cartesian
Convert polar coordinates to Cartesian:
\[
x = \frac{\cos(\phi)}{u}, \quad y = \frac{\sin(\phi)}{u}
\]

### 6. Animation
- Uses `FuncAnimation` to animate the orbit
- Saves as `black_hole_orbit.gif`

---

## Demo

![Orbital Simulation](black_hole_orbit.gif)

---

## Assumptions

- The particle is a **test particle**, meaning its mass is negligible and does not affect spacetime.
- The black hole is **non-rotating** (Schwarzschild metric, not Kerr).
- The system is **isolated and in vacuum**—no other gravitational sources or perturbations.
- **Only spatial motion** is visualized; time dilation and gravitational redshift are not shown.

---

## Limitations

- The simulation is limited to **two dimensions**.
- No **frame dragging** effects (no Kerr spacetime).
- Only **geometric trajectories** are simulated; **time-dependent spacetime diagrams** are not visualized.
- **Unstable or plunging orbits** (i.e. falling past event horizon) may break the simulation if \(r\) approaches zero.

---

## Dependencies

This script requires:

- Python 3.x
- numpy
- scipy
- matplotlib
- pillow (for saving GIFs)

### Install via pip:

```bash
pip install numpy scipy matplotlib pillow
