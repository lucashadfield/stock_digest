import datetime
import sys
import time
import logging

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

from .data import Portfolio
from .email import Email
from .report import Report
from .widgets.basic_change import DayChangeWidget, WeekChangeWidget, MonthChangeWidget
from .widgets.day_breakdown import DayBreakdownWidget
from .widgets.portfolio_summary import PortfolioSummaryWidget


def main(
    stock_config_path: str = None,
    email_config_path: str = None,
    date: datetime.date = None,
):
    if stock_config_path is None:
        stock_config_path = '~/.config/stock_digest/stocks.yaml'

    if email_config_path is None:
        email_config_path = '~/.config/stock_digest/email.yaml'

    if date is None:
        try:
            date = parse(sys.argv[1])
        except IndexError:
            date = datetime.date.today()

    portfolio = Portfolio(stock_config_path, date, 370)

    for _ in range(72):
        # re-run every 10 mins for 12 hours if it fails
        check_dates = [
            portfolio.date,
            portfolio.date - relativedelta(days=7),
            portfolio.date - relativedelta(days=1),
        ]

        errors = portfolio.df.loc[check_dates]._error._error

        if errors.isnull().any():
            logging.warning(
                f'Nulls in data, sleeping for 600 seconds. {errors[errors.isnull()].to_dict()}'
            )
            portfolio.__call__.cache_clear()
            time.sleep(600)
        else:
            break

    report = Report()

    report.add_widget(DayChangeWidget(portfolio), (0, 0))
    report.add_widget(WeekChangeWidget(portfolio), (0, 1))
    report.add_widget(MonthChangeWidget(portfolio), (0, 2))

    report.add_widget(DayBreakdownWidget(portfolio), (slice(1, 3), slice(0, None)), {})

    report.add_widget(
        PortfolioSummaryWidget(portfolio), (slice(4, None), slice(0, None)), {}
    )

    email = Email(email_config_path)
    email.attach_fig(report.fig, str(date))
    email.send(
        f'Stocks - {date.strftime("%a, %e %b")}',
        email.config['sender'],
        email.config['recipient'],
    )
