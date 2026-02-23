"""
Reproduces Fig. 5
"""
import pandas as pd
from pathlib import Path
import matplotlib as mpl
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

sns.set(
    context='paper', style='white',
    palette='deep', font='sans-serif',
    font_scale=1, color_codes=True,
    rc={"xtick.bottom": True}
    )

# parameter sweeps
steps = np.floor(np.linspace(1, 255, 7)).astype(int)
amps = steps * 12  # uA
pws = steps * 10   # us

data_dir = Path('./data/202401261300-Benchtop')


def load_scope_csv(filepath):
    """Load Digilent WaveForms oscilloscope CSV, skipping header comments."""
    return pd.read_csv(filepath, comment='#')


# --- Panel A: Pulse width sweep (first 4 values) at 1200 uA ---
pw_indices = [0, 1, 2, 3]  # 10, 430, 850, 1280 usec
pw_data = {}
for i in pw_indices:
    fname = f'pw_sweep_{steps[i]}steps_1200ua.csv'
    df = load_scope_csv(data_dir / fname)
    pw_data[pws[i]] = df

# --- Panel B: Amplitude sweep at 200 usec ---
amp_indices = [1, 2, 3, 4, 6]  # 516, 1020, 1536, 2040, 3060 uA
amp_labels = [600, 1200, 1800, 2400, 3000]  # rounded for display
amp_data = {}
for idx, i in enumerate(amp_indices):
    fname = f'amp_sweep_{steps[i]}steps_200usec.csv'
    df = load_scope_csv(data_dir / fname)
    amp_data[amp_labels[idx]] = df

# --- Panel C: Multi-frequency stimulation ---
multi_freq_df = load_scope_csv(data_dir / 'multi_freq_120uA_200usec.csv')

# ---- Plotting ----
fig = plt.figure(figsize=(7.5, 5.5))
gs = fig.add_gridspec(2, 2, height_ratios=[1, 0.7], hspace=0.45, wspace=0.4)

# Color palettes
pw_cmap = mpl.colormaps['YlGnBu']
pw_colors = [pw_cmap(x) for x in np.linspace(0.25, 0.95, len(pw_indices))]
amp_colors = sns.color_palette("flare", n_colors=len(amp_indices))

# Panel A - Pulse width sweep
ax_a = fig.add_subplot(gs[0, 0])
for idx, pw_us in enumerate(pw_data):
    df = pw_data[pw_us]
    time_ms = df.iloc[:, 0] * 1e3
    voltage = df.iloc[:, 1]
    ax_a.plot(time_ms, voltage, color=pw_colors[idx], label=str(pw_us),
              linewidth=1.2)
ax_a.set_xlim(-1, 8)
ax_a.set_xlabel('Time (msec.)')
ax_a.set_ylabel('Voltage (V)')
ax_a.legend(title='Pulse\nWidth (usec.)', framealpha=0.8, fontsize=7,
            title_fontsize=7)
ax_a.text(-0.15, 1.05, 'a', transform=ax_a.transAxes,
          fontsize=14, fontweight='bold', va='top')
sns.despine(ax=ax_a)

# Panel B - Amplitude sweep
ax_b = fig.add_subplot(gs[0, 1])
for idx, amp_label in enumerate(amp_data):
    df = amp_data[amp_label]
    time_ms = df.iloc[:, 0] * 1e3
    voltage = df.iloc[:, 1]
    ax_b.plot(time_ms, voltage, color=amp_colors[idx], label=str(amp_label),
              linewidth=1.2)
ax_b.set_xlabel('Time (msec.)')
ax_b.set_ylabel('Voltage (V)')
ax_b.legend(title='Amplitude (uA)', framealpha=0.8, fontsize=7,
            title_fontsize=7)
ax_b.text(-0.15, 1.05, 'b', transform=ax_b.transAxes,
          fontsize=14, fontweight='bold', va='top')
sns.despine(ax=ax_b)

# Panel C - Multi-frequency stimulation
ax_c = fig.add_subplot(gs[1, :])
time_ms = multi_freq_df.iloc[:, 0] * 1e3
ch1 = multi_freq_df.iloc[:, 1]
ch2 = multi_freq_df.iloc[:, 2] + 0.17  # offset for visual separation
ch_colors = [sns.color_palette("deep")[2], sns.color_palette("deep")[0]]
ax_c.plot(time_ms, ch1, color=ch_colors[0], label='ch1', linewidth=0.5)
ax_c.plot(time_ms, ch2, color=ch_colors[1], label='ch2', linewidth=0.5)
ax_c.set_xlabel('Time (msec.)')
ax_c.set_ylabel('Voltage (V)')
ax_c.legend(
    title='Channel', framealpha=0.8, fontsize=7, title_fontsize=7,
    loc='center right', bbox_to_anchor=(1.15, 0.5))
ax_c.text(
    -0.07, 1.1, 'c', transform=ax_c.transAxes,
    fontsize=14, fontweight='bold', va='top')
sns.despine(ax=ax_c)

plt.savefig(
    Path('./figures/benchtop_stim_figure.png'), dpi=300,
            bbox_inches='tight')
plt.savefig(
    Path('./figures/benchtop_stim_figure.pdf'),
    bbox_inches='tight')
plt.show()