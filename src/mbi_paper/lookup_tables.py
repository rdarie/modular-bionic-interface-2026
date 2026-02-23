import pandas as pd
import numpy as np
import seaborn as sns

clinc_sample_rate = 36931.8

clinc_paper_matplotlib_rc = {
    'figure.dpi': 300, 'savefig.dpi': 300,
    'figure.titlesize': 8,
    'lines.linewidth': 0.25,
    'lines.markersize': 2.,
    'patch.linewidth': 0.25,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    "xtick.bottom": True,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.labelpad": 1,
    "axes.labelsize": 5,
    "axes.titlesize": 6,
    "axes.titlepad": 1,
    'axes.linewidth': .25,
    "xtick.labelsize": 5,
    'xtick.major.pad': 1,
    'xtick.major.size': 2,
    'xtick.major.width': 0.25,
    'xtick.minor.pad': .5,
    'xtick.minor.size': 1,
    'xtick.minor.width': 0.25,
    "ytick.labelsize": 5,
    "ytick.major.pad": 1,
    'ytick.major.size': 2,
    'ytick.major.width': 0.25,
    "legend.fontsize": 5,
    "legend.title_fontsize": 6,
    'legend.columnspacing': 0.5,
    'savefig.pad_inches': 0.,
}

clinc_paper_emg_palette = {
    'Left BF': (0.0, 0.10980392156862745, 0.4980392156862745),
    'Left GAS': (0.6941176470588235, 0.25098039215686274, 0.050980392156862744),
    'Left EDL': (0.07058823529411765, 0.44313725490196076, 0.10980392156862745),
    'Right BF': (0.6313725490196078, 0.788235294117647, 0.9568627450980393),
    'Right GAS': (1.0, 0.7058823529411765, 0.5098039215686274),
    'Right EDL': (0.5529411764705883, 0.8980392156862745, 0.6313725490196078),
}

dsi_channels = {
'PhoenixRight870-2:EMG': 'Right EDL',
'PhoenixRight870-2:EMG.1': 'Right BF',
'PhoenixRight870-2:EMG.2': 'Right GAS',
'PhoenixLeft867-2:EMG': 'Left EDL',
'PhoenixLeft867-2:EMG.1': 'Left BF',
'PhoenixLeft867-2:EMG.2': 'Left GAS',
}


HD64_topo_list = ([
    [-1, -1, 60, 55, 58, 63, -1, -1],
    [24, 54, 47, 46, 53, 52, 59, 25],
    [23, 38, 21, 20, 29, 28, 45, 26],
    [22, 31, 10,  2,  7, 19, 36, 27],
    [32, 30,  0, 13, 16,  9, 37, 35],
    [48, 41, 11,  3,  6, 18, 42, 51],
    [49, 39,  1,  4,  5,  8, 44, 50],
    [56, 40, 12, 14, 15, 17, 43, 57],
    ])
HD64_topo = pd.DataFrame(HD64_topo_list)
HD64_topo.index.name = 'y'
HD64_topo.columns.name = 'x'
HD64_topo_remix = pd.DataFrame(
    np.flipud(np.arange(1, 65).reshape(8, 8).T),
    index=HD64_topo.index, columns=HD64_topo.columns)
HD64_labels = HD64_topo.map(lambda x: f"E{x:d}" if (x >= 0) else "")
HD64_labels_remix = HD64_topo_remix.map(lambda x: f"E{x:d}" if (x >= 0) else "")
colors_list = [
    sns.cubehelix_palette(
        n_colors=8, start=st + 1.5, rot=.15, gamma=1., hue=1.0,
        light=0.8, dark=0.2, reverse=False, as_cmap=False)
    for st in np.linspace(0, 3, 10)
    ]

eids_ordered_xy = HD64_labels.unstack()
eids_ordered_xy_remix = HD64_labels_remix.unstack()
eid_remix_lookup = {eids_ordered_xy[idx]: eids_ordered_xy_remix[idx] for idx in eids_ordered_xy.index}
eid_palette = {lbl: colors_list[x][y] for (x, y), lbl in eids_ordered_xy.to_dict().items()}
eid_palette_remix = {lbl: colors_list[x][y] for (x, y), lbl in eids_ordered_xy_remix.to_dict().items()}

