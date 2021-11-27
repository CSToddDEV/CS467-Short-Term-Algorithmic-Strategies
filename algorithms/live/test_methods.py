# 3STAT Algorithm - test_methods.py
# Fall 2021 CS 463

from dateutil.relativedelta import relativedelta
import benchmark as n
import portfolio as p
import backtest as t
import universe as u
import weights as w
import algo as g
import datetime
import db as d
import av as a
import json
import copy


def backfill_db():
    """
    Backfills the Database
    """
    drop_db()
    t.Backtest(True)
    n.Benchmark().benchmark_backfill()
    backtest_algo()



def api_test():
    """
    Tests API
    """
    print(a.Data("TQQQ").new_focus())


def test_benchmark():
    """
    Test Benchmark
    """
    d.Database().drop_benchmarks()
    test = t.Backtest()
    n.Benchmark().benchmark_backfill()
    test.backtest()
    print(test.get_update_status())


def test_backtest():
    """
    Test Backtest
    """
    test = t.Backtest()
    test.backtest()
    print(test.get_update_status())


def prune_db():
    """
    Prunes DB
    """
    d.Database().prune_database()


def prune_first():
    """
    Removes all first of month
    """
    d.Database().prune_first_database()


def algo_run():
    """
    Algo Run
    """
    return g.Algorithm().run()


def reset_db():
    """
    Resets DB for fresh use
    """
    prune_db()
    prune_first()
    backfill_db()


def test_volatility_indicator():
    """
    Tests volatility ticker
    """
    print(a.Data("UPRO").volatility_indicator("2021-11-23"))


def test_hourly():
    """
    Test Hourly Data
    """
    test = a.Data("UPRO")
    test.hourly_data()
    print(test.get_data())


def test_csv_api():
    """
    Test CSV API
    """
    a.Data("TQQQ").pull_backfill_hourly(11, 1)


def pull_backtest_data():
    """
    Test pull_backtest_data
    """
    a.Data("TQQQ").backfill_data(11, 1)

def drop_db():
    """
    Runs Drop DB
    """
    d.Database().drop_db()

def redo_database():
    """
    Deletes and re-updates the DB
    """
    drop_db()
    backfill_db()

def test_add_db():
    """
    Test adding to DB
    """
    data_point = {
        "ticker": "Test",
        "closing_price": 100,
        "3day_sma_close": 55,
        "5day_sma_close": 56,
        "5day_sma_low": 53,
        "date": "5-11-21",
        "trading_day": False
    }

    d.Database().backtest_data_point_multiple(data_point)

def reset_portfolio():
    """
    Resets Portfolio
    """
    d.Database().drop_signals()
    p.Portfolio().reset_portfolio()

def backtest_algo():
    """
    Backtesting algo
    """
    reset_portfolio()
    today = datetime.datetime.now().replace(hour=12, minute=0, second=0)
    backtest_date = today - relativedelta(days=30)
    print("BACKTEST DATE: ", backtest_date)
    g.Algorithm(force_universe=True, today=backtest_date.strftime("%Y-%m-%d %H:%M:%S")).run()
    backtest_date = backtest_date + relativedelta(days=1)
    while backtest_date < today:
        g.Algorithm(today=backtest_date.strftime("%Y-%m-%d %H:%M:%S")).run()
        backtest_date = backtest_date + relativedelta(days=1)

# api_test()
# backfill_db()
# test_benchmark()
# test_backtest()
# prune_db()
# prune_first()
# algo_run()
# reset_db()
# test_volatility_indicator()
# test_hourly()
# test_csv_api()
# pull_backtest_data()
# redo_database()
# test_add_db()
# reset_portfolio()
backtest_algo()
