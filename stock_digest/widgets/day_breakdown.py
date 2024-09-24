import matplotlib.pyplot as plt

from stock_digest import Widget


class DayBreakdownWidget(Widget):
    def plot(self, ax: plt.axes) -> plt.axes:
        non_zero_tickers = self.portfolio.df.holdings.iloc[-1][self.portfolio.df.holdings.iloc[-1].gt(0)].keys()
        plot_df = (
            self.portfolio.df.daily_change.iloc[-1][non_zero_tickers]
            .sort_values(ascending=False)
            .rename('daily_change')
            .to_frame()
            .join(self.portfolio.df.prices.iloc[-1].rename('prices').to_frame())
        )

        plot_df.daily_change.plot(ax=ax, kind='bar', width=0.95, lw=0, ec=self.BASE)

        for p, symbol, prices in zip(ax.patches, plot_df.index, plot_df.prices):
            pos = p.get_height() >= 0

            p.set_facecolor(self._colour(p.get_height()))
            # ticker symbols
            ax.annotate(
                self._symbol_fix(symbol),
                (p.get_x() + p.get_width() / 2, 0),
                ha='center',
                va='top' if pos else 'bottom',
                color=self.BASE,
                size=10,
                weight='bold',
                xytext=(0, -2 if pos else 9),
                textcoords='offset pixels',
            )

            # stock prices
            ax.annotate(
                f'{prices:.2f}' if prices > 1 else f'{prices:.3f}',
                (p.get_x() + p.get_width() / 2, 0),
                ha='center',
                va='top' if pos else 'bottom',
                color=self.BASE,
                size=8,
                xytext=(0, -15 if pos else 0),
                textcoords='offset pixels',
            )

            # daily change
            ax.annotate(
                self._dollars(p.get_height()),
                (p.get_x() + p.get_width() / 2, p.get_height()),
                ha='center',
                va='bottom' if pos else 'top',
                color=self.BASE,
                weight='bold',
                size=10,
                xytext=(0, 1 if pos else -2),
                textcoords='offset pixels',
            )

        for spine in ['left', 'right', 'top', 'bottom']:
            ax.spines[spine].set_visible(False)

        ax.set_xticks([])
        ax.set_yticks([])

        ax.axhline(0, color=self.BASE, lw=0.5)
        ax.set_xlim(-0.475, len(plot_df) - 0.525)
        ylim = ax.get_ylim()
        yrange = ylim[1] - ylim[0]
        ax.set_ylim(ylim[0] - yrange / 4, ylim[1] + yrange / 4)

        return ax
