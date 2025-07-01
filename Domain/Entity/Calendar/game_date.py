import random
from .forecast import forecast

class GameDate:
    MonthNames = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    MonthAbbreviations = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

    def __init__(self, years=0, months=0, days=0, hours=0, minutes=0):
        self.years = years
        self.months = months
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.normalize()

    @property
    def day_of_week(self):
        total_days = self.days + (self.months * 30) + (self.years * 365)
        return total_days % 7  # 0=Sunday, 1=Monday, etc.

    @property
    def forecast(self):
        # Gera um forecast aleatório baseado na data para consistência
        random.seed(self.years * 10000 + self.months * 100 + self.days)
        return random.choice([forecast.Rain, forecast.Cloudy, forecast.Sunny])

    def compare_to(self, other):
        if self.years != other.years:
            return self.years - other.years
        if self.months != other.months:
            return self.months - other.months
        if self.days != other.days:
            return self.days - other.days
        if self.hours != other.hours:
            return self.hours - other.hours
        return self.minutes - other.minutes

    def __ge__(self, other):
        return self.compare_to(other) >= 0

    def __le__(self, other):
        return self.compare_to(other) <= 0

    def __gt__(self, other):
        return self.compare_to(other) > 0

    def __lt__(self, other):
        return self.compare_to(other) < 0

    def add(self, years=0, months=0, days=0, hours=0, minutes=0):
        return GameDate(
            self.years + years,
            self.months + months,
            self.days + days,
            self.hours + hours,
            self.minutes + minutes
        )

    def add_game_date(self, game_date, years=0, months=0, days=0, hours=0, minutes=0):
        return GameDate(
            self.years + game_date.years + years,
            self.months + game_date.months + months,
            self.days + game_date.days + days,
            self.hours + game_date.hours + hours,
            self.minutes + game_date.minutes + minutes
        )

    def subtract_game_date(self, game_date, years=0, months=0, days=0, hours=0, minutes=0):
        return GameDate(
            self.years - game_date.years - years,
            self.months - game_date.months - months,
            self.days - game_date.days - days,
            self.hours - game_date.hours - hours,
            self.minutes - game_date.minutes - minutes
        )

    def normalize(self):
        # Ajusta valores negativos para zero
        self.minutes = max(0, self.minutes)
        self.hours = max(0, self.hours)
        self.days = max(0, self.days)
        self.months = max(0, self.months)
        self.years = max(0, self.years)

        if self.minutes >= 60:
            self.hours += self.minutes // 60
            self.minutes %= 60
        if self.hours >= 24:
            self.days += self.hours // 24
            self.hours %= 24
        if self.days >= 30:
            self.months += self.days // 30
            self.days %= 30
        if self.months >= 12:
            self.years += self.months // 12
            self.months %= 12

    def get_month_number(self):
        return f"{self.months + 1:02d}"

    def get_month_name(self, abreviado=False):
        if self.months < 0 or self.months > 11:
            return ""
        return self.MonthAbbreviations[self.months] if abreviado else self.MonthNames[self.months]