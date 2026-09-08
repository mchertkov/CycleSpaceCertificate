"""Run the complete numerical workflow used by the manuscript.

The transient certificate is the expensive step because each threshold bisection
solves all 2L signed cohesive boundary faces of the case39 reduction.
"""
from __future__ import annotations

import argparse
from exp1_theory import main as run_static
from exp2_transient import main as run_transient
from figures import make_figures
from verify_results import main as verify


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-transient", action="store_true",
                    help="run static calculations only")
    ap.add_argument("--refinement-checks", action="store_true",
                    help="also run optional dt/T transient refinement checks")
    args = ap.parse_args()

    run_static("results/generated")
    if not args.skip_transient:
        run_transient("results/generated", do_refinement_checks=args.refinement_checks)
        make_figures("figures/generated",
                     "results/generated/static_results.json",
                     "results/generated/transient_results.json")
        verify("results/generated")
    else:
        print("Skipped transient experiment. Reference figures remain in figures/reference/.")


if __name__ == "__main__":
    main()
