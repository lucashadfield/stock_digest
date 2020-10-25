import matplotlib.pyplot as plt
import pandas as pd


class Widget:
    POS_COLOUR = '#b3e2cd'
    NEG_COLOUR = '#fbb4ae'
    BASE_COLOUR = '#606060'

    def __init__(self, portfolio_df: pd.DataFrame):
        self.portfolio_df = portfolio_df

    @staticmethod
    def _symbol_fix(symbol):
        return symbol.split('.AX')[0]

    @staticmethod
    def _dollars(val: float) -> str:
        return f'{"-" if val < 0 else ""}${abs(val):,.0f}'

    def _colour(self, val):
        return self.POS_COLOUR if val >= 0 else self.NEG_COLOUR

    def plot(self, ax: plt.axes, *args, **kwargs) -> plt.axes:
        raise NotImplementedError
