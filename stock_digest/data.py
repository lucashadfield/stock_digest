import datetime
import itertools
from functools import lru_cache
from pathlib import Path

import pandas as pd
import yaml
import yfinance as yf
from dateutil.relativedelta import relativedelta


class Portfolio:
    def __init__(self, config_path: str, date: datetime.date = None):
        config = self._load_config(Path(config_path).expanduser())
        self._validate_config(config)
        self.config = config

        self.date = datetime.date.today() if date is None else date
        self.prev_date = self.date - relativedelta(days=35)

    @staticmethod
    def _load_config(config_path: Path) -> dict:
        with config_path.open() as f:
            config = yaml.safe_load(f)

        return config

    @staticmethod
    def _validate_config(config: dict):
        for k, v in config.items():
            if v['holdings'] != sum(v['history'].values()):
                print(f'warning: {k} holdings/history mismatch')

    def build_holdings(self) -> pd.DataFrame:
        holdings = []
        for symbol, details in self.config.items():
            history = pd.Series(details['history'], name=symbol).cumsum()
            holdings.append(
                history.reindex(pd.date_range(history.index.min(), self.date, freq='D'))
                .fillna(method='ffill')
                .reindex(pd.date_range(self.prev_date, self.date, freq='D'))
                .fillna(0)
            )

        return pd.concat(holdings, 1).fillna(0)

    def _compile_tickers(self, conversion: bool = True) -> dict:
        stock = set()
        currency = set()
        for k, v in self.config.items():
            stock.add(k)
            if conversion and 'conversion' in v:
                currency.add(v['conversion'])

        return {'stock': list(stock), 'currency': list(currency)}

    def _bulk_fetch_prices(self, tickers: list) -> pd.DataFrame:
        return yf.download(
            tickers=' '.join(tickers),
            start=self.prev_date,
            end=self.date + relativedelta(days=2),
            interval='1d',
            progress=False,
        )['Adj Close']

    def _apply_offset(self, prices: pd.DataFrame) -> pd.DataFrame:
        for symbol, info in self.config.items():
            if 'us_offset' in info:
                tmp_col = prices[symbol]
                prices = prices.drop(symbol, 1)
                tmp_col.index = [
                    x + relativedelta(days=3)
                    if x.isoweekday() == 5
                    else x + relativedelta(days=1)
                    for x in tmp_col.index
                ]
                prices = prices.join(tmp_col)

        return prices

    def _apply_conversion(self, prices: pd.DataFrame) -> pd.DataFrame:
        conversions = set()
        for symbol, info in self.config.items():
            if 'conversion' in info:
                prices[symbol] *= prices[info['conversion']]
                conversions.add(info['conversion'])

        return prices.drop(conversions, 1)

    def _fill_nan(self, prices: pd.DataFrame) -> pd.DataFrame:
        prices = prices.reindex(
            pd.date_range(self.prev_date, self.date, freq='D')
        ).fillna(method='ffill')

        return prices[~prices.isnull().all(1)]

    def fetch_prices(
        self, apply_conversion: bool = True, apply_offset: bool = True
    ) -> pd.DataFrame:
        tickers = self._compile_tickers(apply_conversion)
        prices = self._bulk_fetch_prices(tickers['stock'] + tickers['currency'])

        if apply_offset:
            prices = self._apply_offset(prices)

        # append the missing info
        prices['_error'] = prices.apply(
            lambda x: list(itertools.compress(prices.columns, x.isnull())), 1
        )

        # fill the missing rows
        prices = self._fill_nan(prices)

        # apply conversions
        if apply_conversion:
            prices = self._apply_conversion(prices)

        prices['_error'] = prices['_error'].apply(lambda x: None if not len(x) else x)

        return prices

    def get(self) -> pd.DataFrame:
        holdings = self.build_holdings()
        prices = self.fetch_prices()
        _error = prices[['_error']]
        prices = prices.drop('_error', 1)
        abs_change = holdings.shift(1).mul(prices) - holdings.shift(1).mul(
            prices.shift(1)
        )

        return pd.concat(
            [holdings, prices, abs_change, _error],
            1,
            keys=('holdings', 'prices', 'abs_change', '_error'),
        )

    @lru_cache(maxsize=1)
    def __call__(self) -> pd.DataFrame:
        return self.get()
