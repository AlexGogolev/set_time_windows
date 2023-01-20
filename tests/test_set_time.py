from set_time1 import calc_year_moth_day_hour, prepare_params, set_date_time
from datetime import datetime
import pytest


# def test_calc_year_month_day_hour_cur_year():
#     assert calc_year_moth_day_hour(5, datetime(2022, 12, 13, 0, 15)) == (2022, 12, 12, 19)
#     assert calc_year_moth_day_hour(5, datetime(2022, 12, 13, 1, 15)) == (2022, 12, 12, 20)
#     assert calc_year_moth_day_hour(5, datetime(2022, 12, 13, 4, 15)) == (2022, 12, 12, 23)

@pytest.mark.parametrize("abbreviation, year, month, day, hour, minute, result",
                         [(5, 2022, 12, 13, 0, 15, (2022, 12, 12, 19)),
                          (5, 2022, 12, 13, 1, 15, (2022, 12, 12, 20)),
                          (5, 2022, 12, 13, 3, 15, (2022, 12, 12, 22)),
                          (5, 2022, 12, 13, 4, 15, (2022, 12, 12, 23))])
def test_calc_year_month_day_hour_cur_year(abbreviation, year, month, day, hour, minute, result):
    assert calc_year_moth_day_hour(abbreviation, datetime(year, month, day, hour, minute)) == result

# def test_calc_year_month_day_hour_next_year():
#     assert calc_year_moth_day_hour(5, datetime(2023, 1, 1, 0, 15)) == (2022, 12, 31, 19)


@pytest.mark.parametrize("abbreviation, year, month, day, hour, minute, result",
                         [(5, 2023, 1, 1, 0, 15, (2022, 12, 31, 19))])
def test_calc_year_month_day_hour_next_year(abbreviation, year, month, day, hour, minute, result):
    assert calc_year_moth_day_hour(abbreviation, datetime(year, month, day, hour, minute)) == result


