import datetime

import matplotlib.pyplot as plt
import pandas as pd
from dateutil.relativedelta import relativedelta
from matplotlib import patches

from stock_digest import Widget


class ChangeWidget(Widget):
    def __init__(self, portfolio, start: datetime.date, end: datetime.date, label: str):
        self.start = start
        self.end = end
        self.label = label

        super().__init__(portfolio)

    @staticmethod
    def _arrow(val: float) -> str:
        return '▲' if val >= 0 else '▼'

    def plot(self, ax) -> plt.axes:
        plot_df = self.portfolio.df.reindex(
            pd.date_range(start=self.start, end=self.end)
        )

        change = plot_df.daily_change[1:].sum().sum()

        rate_tmp = plot_df.holdings.iloc[0].mul(plot_df.prices).sum(1)
        rate = (rate_tmp.iloc[-1] / rate_tmp.iloc[0]) - 1

        colour = self._colour(change)

        ax.add_patch(
            patches.FancyBboxPatch(
                (0.2, 0.2), 3.6, 2.6, mutation_scale=0.5, lw=4, ec=colour, fc='white'
            )
        )

        ax.annotate(
            self.label,
            (0.2, 2.6),
            ha='left',
            va='center',
            size=16,
            color=self.BASE,
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
            color=self.BASE,
            weight='bold',
        )
        ax.annotate(
            f'{rate:+,.1%}',
            (2, 0.9),
            ha='center',
            va='center',
            size=22,
            color=self.BASE,
        )

        ax.set_xlim(0, 4)
        ax.set_ylim(0, 3)

        for spine in ['left', 'right', 'top', 'bottom']:
            ax.spines[spine].set_visible(False)

        ax.set_xticks([])
        ax.set_yticks([])

        return ax


class DayChangeWidget(ChangeWidget):
    def __init__(self, portfolio):
        end = portfolio.date
        start = end - relativedelta(days=1)

        super().__init__(portfolio, start, end, 'Today')


class WeekChangeWidget(ChangeWidget):
    def __init__(self, portfolio):
        end = portfolio.date
        start = end - relativedelta(days=7)

        super().__init__(portfolio, start, end, '1 Week')


class ThisWeekChangeWidget(ChangeWidget):
    def __init__(self, portfolio):
        end = portfolio.date
        start = end - relativedelta(days=end.isoweekday())

        super().__init__(portfolio, start, end, 'This Week')


class MonthChangeWidget(ChangeWidget):
    def __init__(self, portfolio):
        end = portfolio.date
        start = end - relativedelta(months=1)

        super().__init__(portfolio, start, end, '1 Month')


class ThisMonthChangeWidget(ChangeWidget):
    def __init__(self, portfolio):
        end = portfolio.date
        start = end - relativedelta(days=end.day)

        super().__init__(portfolio, start, end, 'This Month')


class YearChangeWidget(ChangeWidget):
    def __init__(self, portfolio):
        end = portfolio.date
        start = end - relativedelta(years=1)

        super().__init__(portfolio, start, end, '1 Year')


class ThisFinancialYearChangeWidget(ChangeWidget):
    def __init__(self, portfolio):
        end = portfolio.date
        start = datetime.date(end.year if end.month >= 7 else end.year - 1, 6, 30)

        super().__init__(portfolio, start, end, 'This Year')
