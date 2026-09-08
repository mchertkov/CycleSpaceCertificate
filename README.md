# CycleSpaceCertificate

Numerical companion repository for the manuscript

> **When Gigawatts of Computational Load Disappear: Cycle-Space Certificates for Grid Synchronization and Transient Stability**  
> Michael (Misha) Chertkov

The repository implements the static and transient calculations reported in the paper for simplified lossless, fixed-voltage reductions of MATPOWER case39 and case118.

The main computational pipeline is

```text
MATPOWER benchmark
        |
        v
lossless fixed-voltage reduction
        |
        +--> Dörfler--Chertkov--Bullo (DCB) screen
        |
        +--> cycle-space convex strict-cohesion oracle
        |
        +--> warm-started locally stable branch continuation
        |
        v
instantaneously balanced case39 injection step
        |
        +--> exact static strict-cohesion threshold
        +--> DCB static threshold
        +--> direct-energy certificate (2L signed boundary faces)
        +--> finite-horizon RK4 cohesion diagnostic
```

## Important model scope

The transient experiment is an **instantaneously balanced injection step**

\[
p_{\rm eff}=p+\Delta P(e_\delta-\gamma),\qquad \mathbf 1^\top\gamma=1,
\]

not a raw load rejection followed by primary-frequency/governor dynamics. The model intentionally omits voltage dynamics, reactive-power limits, protection, converter controls, load dynamics, governor delays, and stochastic forcing. Its purpose is to isolate the synchronization/cycle-space and direct-energy geometry developed in the paper.

## Repository layout

```text
CycleSpaceCertificate/
├── README.md
├── CITATION.cff
├── requirements.txt
├── environment.yml
├── matpower_loader.py
├── grids.py
├── syncnet.py
├── transient.py
├── paper_results.py
├── exp1_theory.py
├── exp2_transient.py
├── figures.py
├── verify_results.py
├── run_all.py
├── notebooks/
│   └── CycleSpaceCertificates.ipynb
├── data/
│   └── README.md
├── results/
│   ├── reference/          # values printed in the manuscript
│   └── generated/          # fresh local run (git-ignored)
├── figures/
│   ├── reference/          # figures made from manuscript values
│   └── generated/          # figures from a fresh local run
└── tests/
    └── test_sanity.py
```

## Installation

Python 3.10 or later is recommended.

### `venv` / `pip`

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Conda

```bash
conda env create -f environment.yml
conda activate cyclespacecertificate
```

## MATPOWER data

The repository does not duplicate third-party MATPOWER case files. On first use, `matpower_loader.py` downloads the standard MATPOWER 8.1 `case39.m` and `case118.m` files into `data/`.

For offline use, place those two files manually in `data/`. See [`data/README.md`](data/README.md).

## Reproducing the paper

### One command

```bash
python run_all.py
```

This performs the static checks, the case39 transient experiment, figure generation, and a regression comparison with the manuscript values.

The transient certificate is the expensive component because each threshold bisection solves all `2L = 92` signed cohesive boundary-face problems of the case39 reduction.

For a faster static-only check:

```bash
python run_all.py --skip-transient
```

For the optional time-step/horizon refinement checks:

```bash
python run_all.py --refinement-checks
```

### Notebook

From the repository root:

```bash
jupyter notebook notebooks/CycleSpaceCertificates.ipynb
```

The notebook walks through the same calculation with explanatory Markdown.

## Manuscript reference values

Checked-in regression targets live in [`results/reference/`](results/reference/). Fresh simulation output is written to `results/generated/`; the two are deliberately kept separate.

### Static loading multipliers

| system | DCB screen | strict-cohesion supremum | continued locally stable branch |
|---|---:|---:|---:|
| MATPOWER case118 | 4.363697 | 5.068736 | 5.268367 |
| MATPOWER case39 | 5.544474 | 5.544472 | 5.544472 |

The case118 continuation number is a warm-started **numerical branch limit**, not a certified saddle-node/fold.

### case39 balanced-step thresholds at `alpha = 4`

| balancing concentration | 0 | 0.25 | 0.50 | 0.75 | 1.00 |
|---|---:|---:|---:|---:|---:|
| energy-certified [MW] | 2035 | 1751 | 1442 | 1186 | 991 |
| finite-horizon cohesive simulation [MW] | 2724 | 2724 | 2585 | 2442 | 2313 |
| exact static strict cohesion [MW] | 2724 | 2724 | 2724 | 2724 | 2724 |
| DCB static screen [MW] | 2724 | 2724 | 2724 | 2724 | 2724 |

The disturbance is at MATPOWER bus 20; the fully concentrated balancing allocation is at MATPOWER bus 38. The projected load block is approximately 2724.5 MW. The reported finite-horizon diagnostic uses `T = 20 s` and `dt = 0.004 s`.

## Numerical implementation notes

- `syncnet.py` constructs an oriented incidence matrix and an integer cycle basis, solves a Phase-I LP for strict capacity-box feasibility, and then applies damped Newton to the separable convex cycle-space objective.
- `transient.py` computes the direct-method critical energy by minimizing the potential over every signed branch face of the closed cohesive polytope. Each face is initialized by a relative-interior LP and solved by equality elimination plus logarithmic-barrier Newton iterations.
- The mathematical face decomposition is exact, but the individual minima are floating-point numerical solutions rather than interval-certified values.
- `simulate_balanced_step` uses RK4 and is a finite-horizon diagnostic; it is not the theorem/certificate.
- Parallel MATPOWER branches are merged in the simplified reduction.

## Verification and tests

After a complete run:

```bash
python verify_results.py
```

For lightweight tests that do not require MATPOWER input files:

```bash
pytest -q
```

## Reference figures

The checked-in plots under `figures/reference/` are regenerated from the numerical values printed in the manuscript. After a fresh run, corresponding figures are produced under `figures/generated/`.

## Citation

Please cite the associated manuscript when using this code or data. A machine-readable software citation is provided in [`CITATION.cff`](CITATION.cff). The manuscript publication/preprint identifier can be added there once available.

## License

No software license is imposed in this prepared upload directory. Add the license you wish to use (for example, BSD-3-Clause or MIT) before making the repository broadly reusable.
