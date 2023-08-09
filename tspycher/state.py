import reflex as rx
from tspycher.libs import Helper
from datetime import date


class State(rx.State):

    @rx.var
    def my_age(self):
        return Helper.calculate_age(date(1984, 5, 31))

    @rx.var
    def ben_age(self):
        return Helper.calculate_age(date(2020, 7, 3))

    @rx.var
    def leia_age(self):
        return Helper.calculate_age(date(2022, 7, 11))