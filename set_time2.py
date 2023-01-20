import calendar
from datetime import datetime
import json
import socket
import time
import win32api
import requests
import win32serviceutil
import servicemanager
import win32event
import win32service


class SMWinservice(win32serviceutil.ServiceFramework):
    """Base class to create winservice in Python"""
    _svc_name_ = 'setTimeFromPython'
    _svc_display_name_ = 'Set time from Python Service'
    _svc_description_ = 'Setting time in Windows from Python script'

    @classmethod
    def parse_command_line(cls):
        """ClassMethod to parse the command line"""
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):
        """Constructor of the winservice"""
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        """Called when the service is asked to stop"""
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        """Called when the service is asked to start"""
        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def start(self):
        """
        Override to add logic before the start
        eg. running condition
        """
        pass

    def stop(self):
        """
        Override to add logic before the stop
        eg. invalidating running condition
        """
        pass

    def main(self):
        """Main class to be ovverridden to add logic"""
        pass


class PythonCornerExample(SMWinservice):

    def start(self):
        self.isrunning = True

    def stop(self):
        self.isrunning = False

    def main(self):
        while self.isrunning:
            self.set_time()
            time.sleep(3600)

    def get_data_from_api(self) -> requests.Response:
        """Получаем ответ от api сервиса времени"""
        return requests.get("http://worldtimeapi.org/api/ip")

    def prepare_params(self, response_text: str) -> dict:
        """Подготавливаем параметры даты/времени"""
        if not response_text:
            return {}

        data_: dict = json.loads(response_text)
        dt: datetime = datetime.fromtimestamp(data_.get('unixtime'))
        cur_year, cur_month, cur_day, cur_hour = self.calc_year_moth_day_hour(int(data_.get('abbreviation', 0)), dt)

        return {'cur_year': cur_year, 'cur_month': cur_month, 'cur_day': cur_day,
                'day_of_week': data_.get('day_of_week') - 1, 'cur_hour': cur_hour,
                'cur_minute': dt.minute, 'cur_second': dt.second}

    def calc_year_moth_day_hour(self, abbreviation: int, dt: datetime) -> tuple[int, int, int, int]:
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

    def set_date_time(self, params: dict) -> None:
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

    def set_time(self):
        row_data_: requests.Response = self.get_data_from_api()
        if row_data_.status_code != 200:
            return

        params: dict = self.prepare_params(row_data_.text)
        if params:
            self.set_date_time(params)


if __name__ == '__main__':
    PythonCornerExample.parse_command_line()
