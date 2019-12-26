from datetime import date, timedelta
from typing import Optional, Tuple

from botocore.client import BaseClient

from tools.aws_tools import get_ce_client
from traceback import format_exc


def main(arg_ce_client: Optional[BaseClient] = None):
    ce = get_ce_client() if arg_ce_client is None else arg_ce_client
    result = {"daily": None, "monthly": None, "premonth": None}

    for key, date_range in {
        "daily": get_daily_range(),
        "monthly": get_current_month_range(),
        "premonth": get_pre_month_range(),
    }.items():
        try:
            result[key] = {"isSuccess": True, "data": get_cost(ce, date_range)}
        except Exception as e:
            result[key] = {
                "isSuccess": False,
                "error": {"message": str(e), "stacktrace": format_exc()},
            }
    return result


def get_current_month_range() -> Tuple[date, date]:
    today = date.today()
    end_datetime = today
    start_datetime = (
        today.replace(day=1)
        if today.day > 1
        else (today - timedelta(days=1)).replace(day=1)
    )
    return start_datetime, end_datetime


def get_pre_month_range() -> Tuple[date, date]:
    end_date, _ = get_current_month_range()
    start_date = (end_date - timedelta(days=1)).replace(day=1)
    return start_date, end_date


def get_daily_range() -> Tuple[date, date]:
    end_date = date.today()
    start_date = end_date - timedelta(days=1)
    return start_date, end_date


def create_option(date_range: Tuple[date, date]) -> dict:
    return {
        "TimePeriod": {
            "Start": date_range[0].isoformat(),
            "End": date_range[1].isoformat(),
        },
        "Granularity": "MONTHLY",
        "Metrics": ["AmortizedCost"],
    }


def execute_get_cost(option: dict, ce: BaseClient) -> dict:
    resp = ce.get_cost_and_usage(**option)
    return {
        "start": resp["ResultsByTime"][0]["TimePeriod"]["Start"],
        "end": resp["ResultsByTime"][0]["TimePeriod"]["End"],
        "billing": resp["ResultsByTime"][0]["Total"]["AmortizedCost"]["Amount"],
        "unit": resp["ResultsByTime"][0]["Total"]["AmortizedCost"]["Unit"],
    }


def get_cost(client: BaseClient, range: Tuple[date, date]):
    option = create_option(range)
    return execute_get_cost(option, client)
