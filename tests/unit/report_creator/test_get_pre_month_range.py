from datetime import date

import pytest
from freezegun import freeze_time

from report_creator import get_pre_month_range


class TestGetPreMonthRange(object):
    @pytest.mark.parametrize(
        "current_date, expected",
        [
            ("2019/06/06 02:34:23.541000+00:00", (date(2019, 5, 1), date(2019, 6, 1))),
            ("2019/03/01 02:34:23.541000+00:00", (date(2019, 1, 1), date(2019, 2, 1))),
            ("2019/03/02 02:34:23.541000+00:00", (date(2019, 2, 1), date(2019, 3, 1))),
        ],
    )
    def test_normal(self, current_date, expected):
        with freeze_time(current_date):
            actual = get_pre_month_range()
            assert actual == expected
