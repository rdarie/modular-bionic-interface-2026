"""
Reproduces Fig. 4c
"""

import pandas as pd
from pathlib import Path
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

sns.set(
    context='paper', style='white',
    palette='deep', font='sans-serif',
    font_scale=1, color_codes=True,
    rc={
        'figure.dpi': 300, 'savefig.dpi': 300,
        'lines.linewidth': .5,
        'lines.markersize': 2.,
        'patch.linewidth': .5,
        'pdf.fonttype': 42,
        'ps.fonttype': 42,
        "xtick.bottom": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.labelpad": 1,
        "axes.labelsize": 5,
        "axes.titlesize": 6,
        "axes.titlepad": 1,
        "xtick.labelsize": 5,
        'xtick.major.pad': 1,
        'xtick.major.size': 2,
        "ytick.labelsize": 5,
        "ytick.major.pad": 1,
        'ytick.major.size': 2,
        "legend.fontsize": 5,
        "legend.title_fontsize": 6,
        }
    )

base_folder = Path('data/202401161300-Benchtop')
clinc_sample_rate = 36931.8

data_original = pd.read_csv(base_folder / 'murdoc_nform_20180725_original.csv')
data_original = data_original * 0.25  # ADC count to uV conversion for blackrock
data_original.index = data_original.index / 3e4  # seconds
data_original = data_original - data_original.mean()

data_replay = pd.read_csv(base_folder / 'murdoc_nform_20180725_replayed.csv')
data_replay = data_replay * 0.195 # ADC count to uV conversion for intan
data_replay.index = data_replay.index / clinc_sample_rate  # seconds

window_len = .5  # sec
original_t0 = 0.00233
replay_t0 = 1.7192
replay_offset = replay_t0 - original_t0
original_offset = 0

replay_mask = (data_replay.index > replay_offset) & (data_replay.index < replay_offset + window_len)
original_mask = (data_original.index > original_offset) & (data_original.index < original_offset + window_len)

plot_data_original = data_original.loc[original_mask].copy()
plot_data_original.index -= plot_data_original.index[0]

plot_data_replay = data_replay.loc[replay_mask].copy()
plot_data_replay.index -= plot_data_replay.index[0]

pdf_path = Path('./figures/lfp_replay.pdf')
png_path = Path('./figures/lfp_replay.png')
with PdfPages(pdf_path) as pdf:
    desired_figsize = (1.8, 1.1)
    fig, ax = plt.subplots(figsize=desired_figsize)
    ax.plot(plot_data_original + 100, label='Original')
    ax.plot(plot_data_replay, label='Replay')
    ax.set_ylabel('LFP (uV)')
    ax.set_xlabel('Time (sec.)')
    ax.set_xlim(plot_data_replay.index[0], plot_data_replay.index[-1])
    legend = fig.legend(loc='center right', bbox_to_anchor=(1, 0.5))
    fig.draw_without_rendering()
    legend_approx_width = legend.legendPatch.get_width() / fig.get_dpi()  # inches
    new_right_limit = 1 - legend_approx_width / desired_figsize[0]
    fig.align_labels()
    fig.tight_layout(pad=5e-1, rect=(0, 0, new_right_limit, 1))
    pdf.savefig(pad_inches=25e-3)
    fig.savefig(png_path)
    plt.show()