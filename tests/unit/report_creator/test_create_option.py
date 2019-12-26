from datetime import date

import pytest
from report_creator import create_option


class TestCreateOption(object):
    @pytest.mark.parametrize(
        "range, expected",
        [
            (
                (date(2019, 5, 1), date(2019, 6, 1)),
                {
                    "TimePeriod": {"Start": "2019-05-01", "End": "2019-06-01"},
                    "Granularity": "MONTHLY",
                    "Metrics": ["AmortizedCost"],
                },
            ),
            (
                (date(2019, 5, 1), date(2019, 5, 18)),
                {
                    "TimePeriod": {"Start": "2019-05-01", "End": "2019-05-18"},
                    "Granularity": "MONTHLY",
                    "Metrics": ["AmortizedCost"],
                },
            ),
        ],
    )
    def test_normal(self, range, expected):
        actual = create_option(range)
        assert actual == expected
