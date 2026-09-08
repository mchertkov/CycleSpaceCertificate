"""Reference values printed in the manuscript.

These constants are *reference targets* for regression checks.  Fresh simulation
outputs are written separately under ``results/generated/`` and should not be
confused with the checked-in manuscript numbers below.
"""
from __future__ import annotations

import numpy as np

STATIC = {
    "case118": {"dcb": 4.363697, "cohesive": 5.068736, "continued": 5.268367},
    "case39":  {"dcb": 5.544474, "cohesive": 5.544472, "continued": 5.544472},
}

CONCENTRATIONS = np.array([0.00, 0.25, 0.50, 0.75, 1.00], dtype=float)

TRANSIENT_MW = {
    "certified":   np.array([2035., 1751., 1442., 1186.,  991.]),
    "simulated":   np.array([2724., 2724., 2585., 2442., 2313.]),
    "static_exact":np.array([2724., 2724., 2724., 2724., 2724.]),
    "static_dcb":  np.array([2724., 2724., 2724., 2724., 2724.]),
}

MANUSCRIPT_METADATA = {
    "case39_alpha": 4.0,
    "case39_disturbance_bus": 20,
    "case39_concentrated_balancing_bus": 38,
    "case39_load_block_MW_approx": 2724.5,
    "case39_prestep_max_angle_deg_approx": 46.17,
    "case39_energy_faces": 92,
    "case39_unique_edges": 46,
    "transient_horizon_s": 20.0,
    "transient_dt_s": 0.004,
    "threshold_resolution_MW_approx": 1.0,
}
