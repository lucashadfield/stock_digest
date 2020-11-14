import matplotlib.pyplot as plt
import pandas as pd


class Widget:
    POS = '#b3e2cd'
    NEG = '#fbb4ae'
    BASE = '#606060'
    LAST_FY = '#fed9a6'
    THIS_FY = '#b3cde3'

    def __init__(self, portfolio, *args, **kwargs):
        self.portfolio = portfolio

    @staticmethod
    def _symbol_fix(symbol):
        return symbol.split('.AX')[0]

    @staticmethod
    def _dollars(val: float) -> str:
        return f'{"-" if val < 0 else ""}${abs(val):,.0f}'

    def _colour(self, val):
        return self.POS if val >= 0 else self.NEG

    def plot(self, ax: plt.axes) -> plt.axes:
        raise NotImplementedError
