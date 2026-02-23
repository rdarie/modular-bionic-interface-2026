"""
Reproduces Fig. 4d — Power draw vs. coil separation distance.
"""

import pandas as pd
import seaborn as sns
import matplotlib as mpl
from pathlib import Path
from matplotlib import pyplot as plt

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

sns.set(
    context='paper', style='white',
    palette='deep', font='sans-serif',
    font_scale=1, color_codes=True,
    rc={"xtick.bottom": True}
    )

data_dir = Path(__file__).resolve().parents[2] / 'data'
filepath = data_dir / 'power_consumption.csv'
data = pd.read_csv(filepath)
data.columns = ['index', 'distance', 'wpt_only', 'full']

color_full = sns.color_palette("deep")[0]   # blue
color_wpt = sns.color_palette("tab10")[1]   # orange

fig, ax_left = plt.subplots(figsize=(4, 2.5))
ax_right = ax_left.twinx()

# Full system power (left y-axis)
ax_left.plot(data['distance'], data['full'], color=color_full,
             linewidth=1.5, label='Full')
ax_left.set_ylabel('Power draw (W)\nentire worn\nsystem on',
                    color=color_full, fontsize=8)
ax_left.tick_params(axis='y', labelcolor=color_full)

# WPT only power (right y-axis)
ax_right.plot(data['distance'], data['wpt_only'], color=color_wpt,
              linewidth=1.5, label='WPT only')
ax_right.set_ylabel('Power draw (W)\nwireless power\ntransfer only',
                     color=color_wpt, fontsize=8, rotation=-90, labelpad=45)
ax_right.tick_params(axis='y', labelcolor=color_wpt)

ax_left.set_xlabel('Distance (mm)')

# Combined legend
lines_left, labels_left = ax_left.get_legend_handles_labels()
lines_right, labels_right = ax_right.get_legend_handles_labels()
ax_left.legend(lines_left + lines_right, labels_left + labels_right,
               title='Worn unit\nPower', framealpha=0.8, fontsize=7,
               title_fontsize=7, loc='center left')

ax_left.text(-0.15, 1.05, 'd', transform=ax_left.transAxes,
             fontsize=14, fontweight='bold', va='top')
sns.despine(ax=ax_left, right=False)
sns.despine(ax=ax_right, left=True, right=False)

plt.savefig(Path('./figures/power_vs_distance.png'), dpi=300, bbox_inches='tight')
plt.savefig(Path('./figures/power_vs_distance.pdf'), bbox_inches='tight')
plt.show()
