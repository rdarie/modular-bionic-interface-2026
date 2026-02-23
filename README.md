# Modular Bionic Interface (Darie et al. 2026)

Code to reproduce figures for "A modular, high-bandwidth, bidirectional implantable device for neural interrogation"

## Data

Download the dataset from [https://osf.io/9hxwe](https://osf.io/9hxwe) and extract to the `./data` directory.

## Setup

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -e .
```

## Reproducing Figures

Each script in `./src/mbi_paper/` generates one or more figures and saves them to `./figures/`.

| Script | Figure |
|--------|--------|
| `calculate_spectrum_benchtop.py` | Fig. 4a, 4b CLINC frequency response |
| `benchtop_ephys_figure.py` | Fig. 4c LFP replay comparison |
| `power_vs_distance.py` | Fig. 4d Power draw vs. coil separation |
| `benchtop_stim_figure.py` | Fig. 5 Benchtop stimulation waveforms |
| `plot_tens_triggered_ephys_per_hd64_routing.py` | Fig. 6 (top) TENS-triggered spinal potentials |
| `plot_tens_triggered_emg_publication.py` | Fig. 6 (bottom) TENS-triggered EMG |
| `plot_triggered_emg_publication.py` | Fig. 7 Stim-triggered EMG and spinal potentials |

Run any script from the repository root:

```bash
python src/mbi_paper/benchtop_stim_figure.py
```

## Data

Pre-processed data are organized under `data/` by recording session:

- `202311221100-Phoenix/` — In vivo electrical stimulation session
- `202401161300-Benchtop/` — LFP replay benchtop validation
- `202401221300-Benchtop/` — CLINC frequency response benchtop validation
- `202401251300-Phoenix/` — In vivo TENS session
- `202401261300-Benchtop/` — Stimulation waveform benchtop validation
- `power_consumption.csv` — Wireless power transfer measurements

## Contact

[radu_darie@alumni.brown.edu](mailto:radu_darie@alumni.brown.edu)

