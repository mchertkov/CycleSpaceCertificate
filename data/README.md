# MATPOWER benchmark inputs

The repository intentionally does **not** duplicate the third-party MATPOWER case files.
On first use, `matpower_loader.py` downloads the standard MATPOWER 8.1 files

- `case39.m`
- `case118.m`

from the public MATPOWER GitHub repository and places them in this directory.

For an offline run, download/copy these two files into `data/` before running the scripts.
The loader checks the local files first.

Upstream project: <https://github.com/MATPOWER/matpower>

The numerical model used here is a deliberately simplified lossless, fixed-voltage
reduction of these MATPOWER cases; it is not a full MATPOWER dynamic simulation.
