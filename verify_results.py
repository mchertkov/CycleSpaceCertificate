"""Compare a completed fresh run with the values printed in the manuscript."""
from __future__ import annotations

from pathlib import Path
import json
import numpy as np
from paper_results import STATIC, TRANSIENT_MW


def main(results_dir="results/generated"):
    d = Path(results_dir)
    static_file = d / "static_results.json"
    transient_file = d / "transient_results.json"
    if not static_file.exists() or not transient_file.exists():
        missing = [str(p) for p in (static_file, transient_file) if not p.exists()]
        raise FileNotFoundError(
            "Fresh output is missing. Run `python run_all.py` first. Missing: "
            + ", ".join(missing)
        )

    s = json.loads(static_file.read_text())
    t = json.loads(transient_file.read_text())

    print("STATIC")
    for case in ("case118", "case39"):
        print(case)
        for q in ("dcb", "cohesive", "continued"):
            got = float(s[case][q])
            exp = float(STATIC[case][q])
            print(f"  {q:10s}: got {got:.6f}, paper {exp:.6f}, diff {got-exp:+.3e}")

    got = np.asarray(t["rows_MW"], float)
    exp = np.column_stack([
        TRANSIENT_MW[k]
        for k in ["certified", "simulated", "static_exact", "static_dcb"]
    ])
    print("\nTRANSIENT [MW] -- computed minus paper")
    print(np.round(got - exp, 3))
    print("\nAt the ~1 MW bisection resolution, differences of order 1 MW are expected.")


if __name__ == "__main__":
    main()
