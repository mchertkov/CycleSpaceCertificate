# Results

`reference/` contains the numerical values reported in the manuscript and is checked
into the repository for traceability.

`generated/` is populated by a fresh local run of

```bash
python run_all.py
```

Fresh output is deliberately kept separate from manuscript reference values. Use
`python verify_results.py` to compare a completed run with the manuscript numbers.
