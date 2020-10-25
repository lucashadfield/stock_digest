import matplotlib.pyplot as plt

from stock_digest import Widget


class DayBreakdownWidget(Widget):
    def plot(self, ax: plt.axes) -> plt.axes:
        plot_df = self.portfolio_df.abs_change.iloc[-1].sort_values(ascending=False)

        plot_df.plot(ax=ax, kind='bar', width=0.95, lw=0, ec=self.BASE_COLOUR)

        for p, symbol in zip(ax.patches, plot_df.keys()):
            pos = p.get_height() >= 0

            p.set_facecolor(self._colour(p.get_height()))
            ax.annotate(
                self._symbol_fix(symbol),
                (p.get_x() + p.get_width() / 2, 0),
                ha='center',
                va='top' if pos else 'bottom',
                color=self.BASE_COLOUR,
                size=12,
                weight='bold',
                xytext=(0, -2 if pos else 2),
                textcoords='offset pixels',
            )
            ax.annotate(
                self._dollars(p.get_height()),
                (p.get_x() + p.get_width() / 2, p.get_height()),
                ha='center',
                va='bottom' if pos else 'top',
                color=self.BASE_COLOUR,
                weight='bold',
                size=12,
                xytext=(0, 2 if pos else -2),
                textcoords='offset pixels',
            )

        for spine in ['left', 'right', 'top', 'bottom']:
            ax.spines[spine].set_visible(False)

        ax.set_xticks([])
        ax.set_yticks([])

        ax.axhline(0, color=self.BASE_COLOUR, lw=0.5)
        ax.set_xlim(-0.475, len(plot_df) - 0.525)
        ylim = ax.get_ylim()
        yrange = ylim[1] - ylim[0]
        ax.set_ylim(ylim[0] - yrange / 4, ylim[1] + yrange / 4)

        return ax
