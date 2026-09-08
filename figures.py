"""Generate compact figures from fresh results or checked-in manuscript values."""
from __future__ import annotations

from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt

from paper_results import STATIC, CONCENTRATIONS, TRANSIENT_MW


def _static_values(static_json=None):
    if static_json is None:
        return STATIC
    p = Path(static_json)
    if not p.exists():
        return STATIC
    d = json.loads(p.read_text())
    return {case: {k: float(d[case][k]) for k in ("dcb", "cohesive", "continued")}
            for case in ("case118", "case39")}


def _transient_values(transient_json=None):
    if transient_json is None:
        return CONCENTRATIONS.copy(), {k: v.copy() for k, v in TRANSIENT_MW.items()}
    p = Path(transient_json)
    if not p.exists():
        return CONCENTRATIONS.copy(), {k: v.copy() for k, v in TRANSIENT_MW.items()}
    d = json.loads(p.read_text())
    c = np.asarray([r[0] for r in d["rows"]], float)
    rows = np.asarray(d["rows_MW"], float)
    vals = {
        "certified": rows[:, 0],
        "simulated": rows[:, 1],
        "static_exact": rows[:, 2],
        "static_dcb": rows[:, 3],
    }
    return c, vals


def make_figures(outdir="figures/generated", static_json="results/generated/static_results.json",
                 transient_json="results/generated/transient_results.json", reference_only=False):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    if reference_only:
        static_json = None
        transient_json = None

    st = _static_values(static_json)
    systems = ["case118", "case39"]
    labels = ["MATPOWER case118", "MATPOWER case39"]
    metrics = [("dcb", "DCB screen"), ("cohesive", "strict cohesion"),
               ("continued", "continued branch")]
    x = np.arange(len(systems), dtype=float)
    width = 0.24

    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    for j, (key, lab) in enumerate(metrics):
        ax.bar(x + (j-1)*width, [st[s][key] for s in systems], width=width, label=lab)
    ax.set_xticks(x, labels)
    ax.set_ylabel("loading multiplier")
    ax.set_title("Static loading thresholds")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(outdir / "static_thresholds.png", dpi=220)
    fig.savefig(outdir / "static_thresholds.pdf")
    plt.close(fig)

    c, tv = _transient_values(transient_json)
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    ax.plot(c, tv["certified"], "o-", label="energy-certified")
    ax.plot(c, tv["simulated"], "s-", label="finite-horizon cohesive simulation")
    ax.plot(c, tv["static_exact"], "^-", label="exact static strict cohesion")
    ax.plot(c, tv["static_dcb"], "x--", label="DCB static screen")
    ax.set_xlabel("balancing concentration")
    ax.set_ylabel("threshold [MW]")
    ax.set_title("case39 balanced-step thresholds at $\\alpha=4$")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(outdir / "transient_thresholds.png", dpi=220)
    fig.savefig(outdir / "transient_thresholds.pdf")
    plt.close(fig)

    return outdir


if __name__ == "__main__":
    make_figures()
