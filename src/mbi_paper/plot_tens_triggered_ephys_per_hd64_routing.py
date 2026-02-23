"""
Reproduces Fig. 6 (top axes)
"""

import matplotlib as mpl
mpl.use('tkagg')  # generate interactive output
import os
import pandas as pd
from pathlib import Path
from mbi_paper.lookup_tables import eid_remix_lookup, eids_ordered_xy, eid_palette, clinc_paper_matplotlib_rc
import numpy as np
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

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


for yml_path, this_routing in routing_config_info.groupby('yml_path'):
    cfg_name = Path(yml_path).stem
    if cfg_name != 'config_c':
        continue
    print(f'On config {cfg_name}')
    apply_stim_blank = False
    lfp_dict = {}
    lfp_type = "lfp"
    for file_name in this_routing['child_file_name']:
        lfp_path = (file_name + f'_tens_epoched_{lfp_type}.parquet')
        if not os.path.exists(folder_path / 'parquet_files' / lfp_path):
            continue
        print(f'\tLoading {file_name}')
        lfp_dict[file_name] = pd.read_parquet(folder_path / 'parquet_files' / lfp_path)
        this_eid_order = [cn for cn in eids_ordered_xy if cn in lfp_dict[file_name].columns]
        this_eid_palette = {lbl: eid_col for lbl, eid_col in eid_palette.items() if lbl in lfp_dict[file_name].columns}
    if not len(lfp_dict):
        print('\tNo files for this cfg')
        continue
    lfp_df = pd.concat(lfp_dict, names=['block'])
    del lfp_dict

    plot_df = lfp_df.stack().reset_index().rename(columns={0: 'value'})

    plot_df.loc[:, 't_msec'] = plot_df['t'] * 1e3
    plot_t_min, plot_t_max = -10e-3, 80e-3

    if not os.path.exists(folder_path / "figures"):
        os.makedirs(folder_path / "figures")

    pdf_path = Path(f'./figures/tens_epoched_{lfp_type}_per_amp_{cfg_name}.pdf')
    group_features = ['pw', 'amp']
    relplot_kwargs = dict(
        estimator='mean', errorbar='se', hue='channel', palette=eid_palette,
        hue_order=this_eid_order,
        col='location',
        x='t_msec', y='value',
        kind='line',
        facet_kws=dict(
            sharey=True, margin_titles=True,
            xlim=(plot_t_min * 1e3, plot_t_max * 1e3),
            legend_out=False),
    )
    dy = 10.
    y_offset = 0
    for chan in relplot_kwargs['hue_order']:
        this_mask = plot_df['channel'] == chan
        plot_df.loc[this_mask, 'value'] += y_offset
        y_offset -= dy

    downsample_more_mask = plot_df['t'].isin(np.unique(lfp_df.index.get_level_values('t'))[::5])
    plot_df = plot_df.loc[downsample_more_mask, :]
    relplot_kwargs["palette"] = {eid_remix_lookup[old_name]: c for old_name, c in relplot_kwargs["palette"].items()}
    relplot_kwargs["hue_order"] = [eid_remix_lookup[old_name] for old_name in relplot_kwargs["hue_order"]]
    plot_df['channel'] = plot_df.apply(lambda x: eid_remix_lookup[x['channel']], axis='columns')
    plot_df.sort_values(by='location', inplace=True)
    with PdfPages(pdf_path) as pdf:
        t_mask = (plot_df['t'] >= plot_t_min) & (plot_df['t'] <= plot_t_max)
        for amp, group in plot_df.loc[t_mask, :].groupby('amp', sort=False):
            if amp != 25:
                continue
            print(f'Plotting amp {amp}')
            g = sns.relplot(
                data=group,
                **relplot_kwargs
                )
            for ax in g.axes.flatten():
                ax.axvline(0, color='r')
                ax.xaxis.set_major_locator(ticker.MultipleLocator(50))
                ax.xaxis.set_minor_locator(ticker.MultipleLocator(10))
            g.set_titles(col_template="TENS on\n{col_name} fetlock")
            g.set_xlabels('')
            if 'reref' in lfp_type:
                g.set_ylabels('Reref. Spinal Potential (uV)')
            else:
                g.set_ylabels('Spinal Potential (uV)')
            g.legend.set_title('Spinal\nChannel')
            g.figure.suptitle(f'TENS amplitude: {amp} V', fontsize=1)
            desired_figsize = (5.2, 1.5)
            g.figure.set_size_inches(desired_figsize)
            sns.move_legend(
                g, 'center right', bbox_to_anchor=(1, 0.5),
                ncols=2)
            for legend_handle in g.legend.legendHandles:
                if isinstance(legend_handle, mpl.lines.Line2D):
                    legend_handle.set_lw(4 * legend_handle.get_lw())
            g.figure.align_labels()
            g.figure.draw_without_rendering()
            legend_approx_width = g.legend.legendPatch.get_width() / g.figure.get_dpi()  # inches
            new_right_margin = .85
            g.tight_layout(pad=25e-2, rect=[0, 0, new_right_margin, 1])
            pdf.savefig()
            plt.show()
        print(f"\tsaved {pdf_path}")
