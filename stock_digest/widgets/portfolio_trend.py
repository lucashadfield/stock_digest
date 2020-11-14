import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
from matplotlib.ticker import FuncFormatter

from stock_digest import Widget


class PortfolioTrendWidget(Widget):
    def plot(self, ax: plt.axes) -> plt.axes:
        self.portfolio.df.value.sum(1).plot(
            ax=ax,
            color=self.BASE,
            lw=3,
            alpha=0.8,
            label='Portfolio Value',
            legend=True,
            zorder=-3,
        )

        fy_dates = [
            x for x in list(self.portfolio.df.index) if (x.month == 7 and x.day == 1)
        ]
        for fy, c in zip(fy_dates, [self.LAST_FY, self.THIS_FY]):
            fy_next = fy + relativedelta(years=1)

            fy_cumulative = self.portfolio.df.daily_change[
                fy : min(fy_next, self.portfolio.date)
            ].cumsum()
            fy_cumulative = (
                self.portfolio.df.value.loc[fy] + fy_cumulative - fy_cumulative.iloc[0]
            ).sum(1)

            fy_cumulative.plot(
                ax=ax,
                c=c,
                lw=4,
                label=f'FY{str(fy.year + 1)[2:]} Cumulative',
                legend=True,
                zorder=-2,
            )

        legend = True
        for fy in fy_dates:
            fy_next = fy + relativedelta(years=1)
            fy_baseline = (
                self.portfolio.df.prices.loc[fy:fy_next]
                .mul(self.portfolio.df.holdings.loc[fy])
                .sum(1)
            )
            fy_baseline.plot(
                ax=ax,
                c=self.BASE,
                alpha=0.5,
                label='FY Baseline',
                legend=legend,
                zorder=-1,
            )
            legend = False

            ax.axvline(fy, color=self.BASE, zorder=-4)
            ax.plot(
                [fy, min(fy_next, self.portfolio.date)],
                [fy_baseline.iloc[0]] * 2,
                color=self.BASE,
                zorder=-4,
            )

        ax.grid(axis='both')
        ax.set_xlim(self.portfolio.date - relativedelta(years=1), None)
        ax.set_ylim(0, None)
        ax.minorticks_off()

        ax.tick_params(
            axis='x',
            direction='in',
            pad=-20,
            length=0,
            labelsize=8,
            labelcolor=self.BASE,
        )
        for label in ax.xaxis.get_ticklabels():
            label.set_bbox(
                {
                    'boxstyle': 'square,pad=0.3',
                    'fc': 'white',
                    'lw': 0.1,
                    'alpha': 0.6,
                }
            )

        ax.tick_params(
            axis='y',
            direction='in',
            pad=-26,
            length=0,
            labelsize=8,
            labelcolor=self.BASE,
        )
        for label in ax.yaxis.get_ticklabels():
            label.set_bbox(
                {
                    'boxstyle': 'square,pad=0.3',
                    'fc': 'white',
                    'lw': 0.1,
                    'alpha': 0.6,
                }
            )

        formatter = FuncFormatter(
            lambda val, pos: f'{int(val / 1000)}k' if val > 0 else None
        )
        ax.yaxis.set_major_formatter(formatter)

        ax.legend(
            ax.get_legend_handles_labels()[1][:-1],
            ncol=4,
            bbox_to_anchor=(0.5, 1),
            loc='upper center',
            fontsize=8,
            labelcolor=self.BASE,
        )

        return ax
