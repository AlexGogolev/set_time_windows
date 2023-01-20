from datetime import datetime
import requests
import json
import time
import win32api
import calendar


def get_data_from_api() -> requests.Response:
    """Получаем ответ от api сервиса времени"""
    return requests.get("http://worldtimeapi.org/api/ip")


def prepare_params(response_text: str) -> dict:
    """Подготавливаем параметры даты/времени"""
    if not response_text:
        return {}

    data_: dict = json.loads(response_text)

    dt: datetime = datetime.fromtimestamp(data_.get('unixtime'))
    cur_year, cur_month, cur_day, cur_hour = calc_year_moth_day_hour(int(data_.get('abbreviation', 0)), dt)

    return {'cur_year': cur_year, 'cur_month': cur_month, 'cur_day': cur_day,
            'day_of_week': data_.get('day_of_week') - 1, 'cur_hour': cur_hour,
            'cur_minute': dt.minute, 'cur_second': dt.second}


def calc_year_moth_day_hour(abbreviation: int, dt: datetime) -> tuple[int, int, int, int]:
    """Вычисление года, месяца, дня"""
    dt_hour = dt.hour
    cur_year = dt.year
    cur_month = dt.month
    cur_day = dt.day
    need_dec_day = True
    if dt_hour == 0:
        dt_hour = 24
    elif dt_hour == 1:
        dt_hour = 25
    elif dt_hour == 2:
        dt_hour = 26
    elif dt_hour == 3:
        dt_hour = 27
    elif dt_hour == 4:
        dt_hour = 28
    else:
        need_dec_day = False
    cur_year = cur_year - 1 if need_dec_day and dt.month == 1 and dt.day == 1 else cur_year
    cur_month = cur_month - 1 if need_dec_day and cur_day == 1 else cur_month
    cur_month = 12 if cur_month == 0 else cur_month
    if need_dec_day and dt.day != 1:
        cur_day -= 1
    elif need_dec_day and dt.day == 1:
        # тогда нужно установить день равный поледнему числу предыдущего месяца
        cur_day = calendar.monthrange(cur_year, cur_month)[1]
    cur_hour = dt_hour - abbreviation  # тут вычисляется текущий час: ТекЧас - 5
    return cur_year, cur_month, cur_day, cur_hour


def set_date_time(params: dict) -> None:
    """Установка даты и времени в windows по переданным параметрам"""
    try:
        win32api.SetSystemTime(params.get('cur_year'),
                               params.get('cur_month'),
                               params.get('day_of_week'),
                               params.get('cur_day'),
                               params.get('cur_hour'),
                               params.get('cur_minute'),
                               params.get('cur_second'), 0)
    except:
        pass


def set_time():
    row_data_: requests.Response = get_data_from_api()
    if row_data_.status_code != 200:
        return

    params: dict = prepare_params(row_data_.text)
    # data_ = json.loads(row_data_.text)
    # # cur_time_str = data_.get('datetime')  # 2022-12-11 23:24:19
    # abbreviation = int(data_.get('abbreviation'))
    # now = datetime.now()
    # cur_year = now.year
    # cur_month = now.month
    # cur_day = now.day
    # day_of_week = datetime.today().weekday()
    #
    # dt = datetime.fromtimestamp(data_.get('unixtime'))
    # # last_day_of_month = calendar.monthrange(dt.year, dt.month)[1]  # тут получаем последний день текущего месяца - если сегодня этот день,
    # # # то ...
    # dt_hour = dt.hour
    # need_dec_day = True
    # if dt_hour == 0:
    #     dt_hour = 24
    # elif dt_hour == 1:
    #     dt_hour = 25
    # elif dt_hour == 2:
    #     dt_hour = 26
    # elif dt_hour == 3:
    #     dt_hour = 27
    # elif dt_hour == 4:
    #     dt_hour = 28
    # else:
    #     need_dec_day = False
    #
    # cur_year = cur_year - 1 if need_dec_day and dt.month == 1 and dt.day == 1 else cur_year
    # cur_month = cur_month - 1 if need_dec_day and cur_day == 1 else cur_month
    # cur_month = 12 if cur_month == 0 else cur_month
    # if need_dec_day and dt.day != 1:
    #     cur_day -= 1
    # elif need_dec_day and dt.day == 1:
    #     # тогда нужно установить день равный поледнему числу предыдущего месяца
    #     cur_day = calendar.monthrange(cur_year, cur_month)[1]
    #
    # # elif dt_hour == 5:
    # #     dt_hour = 29
    #
    # cur_hour = dt_hour - abbreviation  # -5 часов
    # # print(f'cur_hour: {cur_hour}')
    #
    #
    # # tt = datetime.utcnow().time()
    #
    # # print(f'cur_hour" {cur_hour}')
    if params:
        set_date_time(params)
    time.sleep(3600)


if __name__ == '__main__':
    set_time()
