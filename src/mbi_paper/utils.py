import numpy as np


def getThresholdCrossings(
        dataSrs, thresh=None, absVal=False,
        edgeType='rising', fs=3e4, iti=None,
        keep_max=True, itiWiggle=0.05,
        plotting=False, plot_opts=dict()):
    if absVal:
        dsToSearch = dataSrs.abs()
    else:
        dsToSearch = dataSrs
    nextDS = dsToSearch.shift(1).fillna(method='bfill')
    if edgeType == 'rising':
        crossMask = (
            (dsToSearch >= thresh) & (nextDS < thresh) |
            (dsToSearch > thresh) & (nextDS <= thresh))
    elif edgeType == 'falling':
        crossMask = (
            (dsToSearch <= thresh) & (nextDS > thresh) |
            (dsToSearch < thresh) & (nextDS >= thresh))
    elif edgeType == 'both':
        risingMask = (
            (dsToSearch >= thresh) & (nextDS < thresh) |
            (dsToSearch > thresh) & (nextDS <= thresh))
        fallingMask = (
            (dsToSearch <= thresh) & (nextDS > thresh) |
            (dsToSearch < thresh) & (nextDS >= thresh))
        crossMask = risingMask | fallingMask
    crossIdx = dataSrs.index[crossMask]
    if iti is not None:
        min_dist = int(fs * iti * (1 - itiWiggle))
        y = dsToSearch.abs().to_numpy()
        peaks = np.array([dsToSearch.index.get_loc(i) for i in crossIdx])
        if peaks.size > 1 and min_dist > 1:
            if keep_max:
                highest = peaks[np.argsort(y[peaks])][::-1]
            else:
                highest = peaks
            rem = np.ones(y.size, dtype=bool)
            rem[peaks] = False
            for peak in highest:
                if not rem[peak]:
                    sl = slice(max(0, peak - min_dist), peak + min_dist + 1)
                    rem[sl] = True
                    rem[peak] = False
            peaks = np.arange(y.size)[~rem]
            crossIdx = dsToSearch.index[peaks]
            crossMask = dsToSearch.index.isin(crossIdx)
    return crossIdx, crossMask
