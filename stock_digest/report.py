from typing import Tuple, Union

import matplotlib.pyplot as plt

from .widgets.base import Widget


class Report:
    def __init__(
        self, figsize: tuple = (10, 16), gridsize: tuple = (8, 3), dpi: int = 100
    ):
        self.figsize = figsize
        self.dpi = dpi
        self.gridsize = gridsize

        self.fig = plt.figure(figsize=figsize, dpi=dpi, constrained_layout=True)
        self.grid = self.fig.add_gridspec(*gridsize)

    def add_widget(
        self,
        widget: Widget,
        grid_pos: Tuple[Union[int, slice], Union[int, slice]],
        plot_kwargs: dict = None,
    ):
        if plot_kwargs is None:
            plot_kwargs = {}

        ax = self.fig.add_subplot(self.grid[grid_pos[0], grid_pos[1]])
        widget.plot(ax, **plot_kwargs)
