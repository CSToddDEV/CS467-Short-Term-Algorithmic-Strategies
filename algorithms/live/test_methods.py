# 3STAT Algorithm - test_methods.py
# Fall 2021 CS 463

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
    test = t.Backtest(w.universe2, w.weight_3, True)
    n.Benchmark().benchmark_backfill()
    test.backtest()
    print(test.get_update_status())


def api_test():
    """
    Tests API
    """
    print(a.Data("TQQQ", w.weight_3).new_focus())


def test_benchmark():
    """
    Test Benchmark
    """
    test = t.Backtest(w.universe2, w.weight_3)
    n.Benchmark().benchmark_backfill()
    test.backtest()
    print(test.get_update_status())

def test_backtest():
    """
    Test Backtest
    """
    test = t.Backtest(w.universe2, w.weight_3)
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
    g.Algorithm().run()

def reset_db():
    """
    Resets DB for fresh use
    """
    prune_db()
    prune_first()
    backfill_db()

# api_test()
# backfill_db()
# test_benchmark()
# test_backtest()
# prune_db()
# prune_first()
# algo_run()
# reset_db()
