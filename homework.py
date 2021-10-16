import datetime as dt


message = 'Укажите корректный вид валюты'
DATE_FORMAT = '%d.%m.%Y'


class Record:
    def __init__(self, amount: float, comment: str,
                 date=None):
        self.amount = amount
        self.comment = comment
        if type(date) is str:
            day_time = dt.datetime.strptime(date, DATE_FORMAT)
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
        """Создание записи о денежной трате."""
        self.records.append(record)

    def get_today_stats(self):
        """Подсчет истраченных денег и калорий за текущую дату."""
        day_now = dt.date.today()
        day_amount_count = sum([i.day_amount() for i in self.records
                                if i.day_record() == day_now])
        return day_amount_count

    def get_week_stats(self):
        """Подсчет истраченных денег и калорий за последнюю неделю."""
        period = dt.timedelta(days=7)
        week_period = dt.date.today() - period
        week_amount_count = sum([i.day_amount() for i in self.records
                                 if dt.date.today() >= i.day_record()
                                 > week_period])
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
        if currency not in self.currencies.keys():
            raise ValueError(message)
        day_amount = self.get_today_stats()
        rate, valuta = [self.currencies[currency][1],
                        self.currencies[currency][0]]
        converted_rate = round((self.limit - day_amount)/rate, 2)
        duty = -converted_rate
        if self.limit > day_amount:
            answer = f'На сегодня осталось {converted_rate} {valuta}'
        elif self.limit == day_amount:
            answer = 'Денег нет, держись'
        elif self.limit < day_amount:
            answer = f'Денег нет, держись: твой долг - {duty} {valuta}'
        return answer


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        """Определение оставшейся доступной пищи на текущую дату."""
        day_amount = self.limit - self.get_today_stats()
        if day_amount > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {day_amount} кКал')
        return 'Хватит есть!'

# Привет! Не стал писать в Slack, из-за позднего времени. С общением всё
# удобно и нормально. Замечания понятны. Единственный момент: я раньше не
# встречал фразу "Вынести из кода", но понял её так как сделал в своём коде.
