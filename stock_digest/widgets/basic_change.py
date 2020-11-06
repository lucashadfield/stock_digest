import matplotlib.pyplot as plt
import pandas as pd
from dateutil.relativedelta import relativedelta
from matplotlib import patches

from stock_digest import Widget


class ChangeWidget(Widget):
    @staticmethod
    def _arrow(val: float) -> str:
        return '▲' if val >= 0 else '▼'

    def plot(self, ax: plt.axes, end, start, label) -> plt.axes:
        plot_df = self.portfolio.df.reindex(pd.date_range(start=start, end=end))

        change = plot_df.abs_change[1:].sum().sum()

        rate_tmp = plot_df.holdings.iloc[0].mul(plot_df.prices).sum(1)
        rate = (rate_tmp.iloc[-1] / rate_tmp.iloc[0]) - 1

        colour = self._colour(change)

        ax.add_patch(
            patches.FancyBboxPatch(
                (0.2, 0.2), 3.6, 2.6, mutation_scale=0.5, lw=4, ec=colour, fc='white'
            )
        )

        ax.annotate(
            label,
            (0.2, 2.6),
            ha='left',
            va='center',
            size=16,
            color=self.BASE_COLOUR,
            weight='bold',
        )
        ax.annotate(
            self._arrow(change),
            (3.6, 2.55),
            ha='center',
            va='center',
            size=30,
            color=colour,
            family='DejaVu Sans',
        )

        ax.annotate(
            self._dollars(change),
            (2, 1.6),
            ha='center',
            va='center',
            size=30,
            color=self.BASE_COLOUR,
            weight='bold',
        )
        ax.annotate(
            f'{rate:+,.1%}',
            (2, 0.9),
            ha='center',
            va='center',
            size=22,
            color=self.BASE_COLOUR,
        )

        ax.set_xlim(0, 4)
        ax.set_ylim(0, 3)

        for spine in ['left', 'right', 'top', 'bottom']:
            ax.spines[spine].set_visible(False)

        ax.set_xticks([])
        ax.set_yticks([])

        return ax


class DayChangeWidget(ChangeWidget):
    def plot(self, ax: plt.axes) -> plt.axes:
        end = self.portfolio.df.index[-1]
        start = end - relativedelta(days=1)

        super().plot(ax, end, start, 'Day')


class WeekChangeWidget(ChangeWidget):
    def plot(self, ax: plt.axes) -> plt.axes:
        end = self.portfolio.df.index[-1]
        start = end - relativedelta(days=7)

        super().plot(ax, end, start, 'Week')


class MonthChangeWidget(ChangeWidget):
    def plot(self, ax: plt.axes) -> plt.axes:
        end = self.portfolio.df.index[-1]
        start = end - relativedelta(months=1)

        super().plot(ax, end, start, 'Month')
