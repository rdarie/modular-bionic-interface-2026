"""
Reproduces Fig. 6 (bottom axes)
"""

import matplotlib as mpl
mpl.use('tkagg')  # generate interactive output
import os
import pandas as pd
from pathlib import Path
from mbi_paper.lookup_tables import clinc_paper_matplotlib_rc, clinc_paper_emg_palette
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker

sns.set(
    context='paper', style='white',
    palette='deep', font='sans-serif',
    font_scale=1, color_codes=True,
    rc=clinc_paper_matplotlib_rc
    )

folder_path = Path("data/202401251300-Phoenix")
routing_config_info = pd.read_json(folder_path / 'analysis_metadata/routing_config_info.json')
routing_config_info['config_start_time'] = routing_config_info['config_start_time'].apply(
    lambda x: pd.Timestamp(x, tz='GMT'))
routing_config_info['config_end_time'] = routing_config_info['config_end_time'].apply(
    lambda x: pd.Timestamp(x, tz='GMT'))

emg_dict = {}
envelope_dict = {}
tens_info_dict = {}
for file_name in routing_config_info['child_file_name']:
    emg_path = (file_name + '_tens_epoched_emg.parquet')
    if not os.path.exists(folder_path / 'parquet_files' / emg_path):
        continue
    envelope_path = (file_name + '_tens_epoched_envelope.parquet')
    tens_info_path = (file_name + '_tens_info.parquet')
    emg_dict[file_name] = pd.read_parquet(folder_path / 'parquet_files' / emg_path)
    envelope_dict[file_name] = pd.read_parquet(folder_path / 'parquet_files' / envelope_path)
    tens_info_dict[file_name] = pd.read_parquet(folder_path / 'parquet_files' / tens_info_path)

emg_df = pd.concat(emg_dict, names=['block'])
del emg_dict
envelope_df = pd.concat(envelope_dict, names=['block'])
del envelope_dict
tens_info_df = pd.concat(tens_info_dict, names=['block'])
del tens_info_dict

plot_df = emg_df.stack().reset_index().rename(columns={0: 'value'})
plot_df.loc[:, 't_msec'] = plot_df['t'] * 1e3
plot_df['value'] *= 1e3

if not os.path.exists(folder_path / "figures"):
    os.makedirs(folder_path / "figures")

pdf_path = Path('./figures/tens_epoched_emg_per_amp.pdf')
group_features = ['pw', 'amp']

plot_t_min, plot_t_max = -10e-3, 80e-3
relplot_kwargs = dict(
    estimator='mean', errorbar='se', hue='channel',
    palette=clinc_paper_emg_palette,
    col='location', hue_order=[key for key in clinc_paper_emg_palette.keys()],
    x='t_msec', y='value',
    kind='line',  height=4, aspect=1.8,
    facet_kws=dict(
        sharey=False, margin_titles=True, legend_out=False,
        xlim=(plot_t_min * 1e3, plot_t_max * 1e3),),
)

dy = 2.5
y_offset = 0
for chan in emg_df.columns:
    this_mask = plot_df['channel'] == chan
    plot_df.loc[this_mask, 'value'] += y_offset
    y_offset -= dy

plot_df.sort_values(by='location', inplace=True)
with PdfPages(pdf_path) as pdf:
    t_mask = (plot_df['t'] >= plot_t_min) & (plot_df['t'] <= plot_t_max)
    for amp, group in plot_df.loc[t_mask, :].groupby('amp'):
        if amp != 25:
            continue
        g = sns.relplot(
            data=group,
            **relplot_kwargs
            )
        for ax in g.axes.flatten():
            ax.axvline(0, color='r')
            ax.xaxis.set_major_locator(ticker.MultipleLocator(50))
            ax.xaxis.set_minor_locator(ticker.MultipleLocator(10))
            ax.set_yticklabels([])
        g.set_titles(col_template="")
        g.set_xlabels('Time (msec.)')
        g.set_ylabels('Normalized EMG (a.u.)')
        g.legend.set_title('EMG\nChannel')
        g.figure.suptitle(f'TENS amplitude: {amp} V', fontsize=1)
        desired_figsize = (5.2, 1.5)
        g.figure.set_size_inches(desired_figsize)
        sns.move_legend(
            g, 'center right', bbox_to_anchor=(1, 0.5),
            ncols=1)
        for legend_handle in g.legend.legendHandles:
            if isinstance(legend_handle, mpl.lines.Line2D):
                legend_handle.set_lw(4 * legend_handle.get_lw())
        g.figure.align_labels()

        new_right_margin = .85  # hardcode to align to emg figure
        g.tight_layout(pad=25e-2, rect=[0, 0, new_right_margin, 1])
        pdf.savefig()
        plt.show()
