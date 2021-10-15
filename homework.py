import datetime as dt


class Record:
    def __init__(self, amount: float, comment: str,
                 date=None):
        self.amount = amount
        self.comment = comment
        date_format = '%d.%m.%Y'
        if type(date) is str:
            day_time = dt.datetime.strptime(date, date_format)
            self.date = day_time.date()
        elif date is None:
            self.date = dt.date.today()

    def day_record(self):
        return self.date

    def day_amount(self):
        return self.amount


class Calculator:
    def __init__(self, limit: float):
        self.limit = limit
        self.records = []

    def add_record(self, record: Record) -> None:
        """Создание записи о денежной трате"""
        self.records = self.records + [record]

    def get_today_stats(self):
        """Подсчет истраченных денег и калорий за текущую дату."""
        day_amount_count = 0
        day_now = dt.date.today()
        for i in self.records:
            if i.day_record() == day_now:
                day_amount_count = day_amount_count + i.day_amount()
        return day_amount_count

    def get_week_stats(self):
        """Подсчет истраченных денег и калорий за последнюю неделю."""
        week_amount_count = 0
        period = dt.timedelta(days=7)
        week_period = dt.date.today() - period
        for i in self.records:
            if dt.date.today() >= i.day_record() > week_period:
                week_amount_count = week_amount_count + i.day_amount()
        return week_amount_count


class CashCalculator(Calculator):
    RUB_RATE: float = 1
    USD_RATE: float = 70.97
    EURO_RATE: float = 82.35
    currencies: dict = {'rub': ('руб', RUB_RATE),
                        'usd': ('USD', USD_RATE),
                        'eur': ('Euro', EURO_RATE)}

    def get_today_cash_remained(self, currency: str):
        """Определение оставшейся суммы на текущую дату."""
        day_amount = self.get_today_stats()
        rat = self.currencies
        if self.limit > day_amount:
            return ('На сегодня осталось '
                    f'{round((self.limit - day_amount)/(rat[currency][1]), 2)}'
                    f' {rat[currency][0]}')
        elif self.limit == day_amount:
            return 'Денег нет, держись'
        else:
            return ('Денег нет, держись: твой долг - '
                    f'{round((day_amount - self.limit)/(rat[currency][1]), 2)}'
                    f' {rat[currency][0]}')


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        """Определение оставшейся доступной пищи на текущую дату."""
        day_amount = self.limit - self.get_today_stats()
        if day_amount > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {day_amount} кКал')
        else:
            return 'Хватит есть!'
