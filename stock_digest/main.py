import datetime
import logging
import sys
import time

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

from . import PortfolioTrendWidget
from .data import Portfolio
from .email import Email
from .report import Report
from .widgets.basic_change import (
    DayChangeWidget,
    WeekChangeWidget,
    ThisWeekChangeWidget,
    MonthChangeWidget,
    ThisMonthChangeWidget,
    YearChangeWidget,
    ThisFinancialYearChangeWidget,
)
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

    portfolio = Portfolio(stock_config_path, date, 730)

    report = Report()

    # row 0
    report.add_widget(DayChangeWidget(portfolio), (0, 0))
    report.add_widget(DayBreakdownWidget(portfolio), (0, slice(1, None)))

    # row 1
    report.add_widget(ThisWeekChangeWidget(portfolio), (1, 0))
    report.add_widget(ThisMonthChangeWidget(portfolio), (1, 1))
    report.add_widget(ThisFinancialYearChangeWidget(portfolio), (1, 2))

    # row 2
    report.add_widget(WeekChangeWidget(portfolio), (2, 0))
    report.add_widget(MonthChangeWidget(portfolio), (2, 1))
    report.add_widget(YearChangeWidget(portfolio), (2, 2))

    # row 3,4
    report.add_widget(PortfolioTrendWidget(portfolio), (slice(3, 5), slice(0, None)))

    # row 5,6,7,8
    report.add_widget(
        PortfolioSummaryWidget(portfolio), (slice(5, None), slice(0, None))
    )

    email = Email(email_config_path)
    email.attach_fig(report.fig, str(date))
    email.send(
        f'Stocks - {date.strftime("%a, %e %b")}',
        email.config['sender'],
        email.config['recipient'],
    )
