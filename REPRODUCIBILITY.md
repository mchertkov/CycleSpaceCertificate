# Reproducibility map

This file maps manuscript claims to code and checked-in reference outputs.

| Manuscript quantity | Code path | Fresh output | Checked-in reference |
|---|---|---|---|
| DCB loading threshold | `syncnet.py::dcb_margin`, `exp1_theory.py::static_case` | `results/generated/static_results.json` | `results/reference/static_thresholds.*` |
| Exact strict-cohesion threshold | `syncnet.py::phase1_cycle_box`, `solve_dual`, `cohesive_threshold` | same | same |
| Continued locally stable branch | `syncnet.py::continued_stable_limit` | same | same |
| Ring winding-state count | `exp1_theory.py::ring_counts` | `results/generated/static_results.*` | formula documented in notebook |
| Balanced injection step | `transient.py::balanced_injection` | transient JSON | `results/reference/manuscript_metadata.json` |
| Critical energy `c*` | `transient.py::critical_energy` | transient JSON | thresholds in `transient_thresholds.*` |
| Energy-certified threshold | `transient.py::certified_threshold` | transient JSON | `transient_thresholds.*` |
| Finite-horizon cohesion threshold | `transient.py::simulated_threshold` | transient JSON | `transient_thresholds.*` |
| Static post-step threshold | `transient.py::static_threshold` | transient JSON | `transient_thresholds.*` |

## Core numerical settings

- case39 loading multiplier: `alpha = 4`
- disturbance/load bus: MATPOWER bus 20
- fully concentrated balancing bus: MATPOWER bus 38
- balancing concentrations: `0, 0.25, 0.5, 0.75, 1`
- synthetic damping: `0.05`
- RK4 horizon: `T = 20 s`
- RK4 step: `dt = 0.004 s`
- threshold bisection tolerance: `0.01 pu`, approximately 1 MW on a 100 MVA base
- case39 unique-edge count after merging parallel branches: `L = 46`
- signed cohesive boundary faces: `2L = 92`

## Interpretation

The static strict-cohesion result is the numerical supremum of an open winding cell. The branch-continuation endpoint is a warm-started numerical limit, not a certified fold. The face decomposition of the direct-energy barrier is exact mathematically, while each face minimum is computed in floating-point arithmetic.
