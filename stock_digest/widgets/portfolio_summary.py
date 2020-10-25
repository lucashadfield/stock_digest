import math

import matplotlib.pyplot as plt
from matplotlib import cm, patches

from stock_digest import Widget


class PortfolioSummaryWidget(Widget):
    def plot(self, ax: plt.axes) -> plt.axes:
        plt_df = (
            (self.portfolio_df.iloc[-1].holdings * self.portfolio_df.iloc[-1].prices)
            .rename('value')
            .to_frame()
        )
        plt_df['ratio'] = plt_df.value / plt_df.value.sum()
        plt_df['ratio_centre'] = plt_df.ratio.cumsum() - plt_df.ratio.div(2)
        plt_df['annot_x'] = 0.75 * (plt_df.ratio_centre * 2 * math.pi).apply(math.cos)
        plt_df['annot_y'] = 0.75 * (plt_df.ratio_centre * 2 * math.pi).apply(math.sin)

        colours = cm.get_cmap('Pastel1').colors + cm.get_cmap('Pastel2').colors
        ax.pie(plt_df.value, colors=colours)

        ax.add_patch(patches.Circle((0, 0), 0.5, color='white'))

        for ticker, details in plt_df.iterrows():
            value_str = f'${details.value:,.0f}'
            ratio_str = f'{details.ratio:.1%}'

            ax.annotate(
                r'$\bf{'
                + self._symbol_fix(ticker)
                + '}$\n'
                + value_str
                + '\n'
                + ratio_str,
                (details.annot_x, details.annot_y),
                ha='center',
                va='center',
                color=self.BASE_COLOUR,
                bbox={
                    'boxstyle': 'round,pad=0.3',
                    'fc': 'white',
                    'lw': 0,
                    'alpha': 0.5,
                },
                size=12,
            )

        ax.annotate(
            f'${plt_df.value.sum():,.0f}',
            (0, 0),
            ha='center',
            va='center',
            size=30,
            weight='bold',
            color=self.BASE_COLOUR,
        )
        ax.set_xlim(-0.8, 0.8)
        ax.set_ylim(-0.8, 0.8)

        return ax
