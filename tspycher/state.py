import pynecone as pc
from tspycher.libs import Helper
from datetime import date


class State(pc.State):

    @pc.var
    def my_age(self):
        return Helper.calculate_age(date(1984, 5, 31))

    @pc.var
    def ben_age(self):
        return Helper.calculate_age(date(2020, 7, 3))

    @pc.var
    def leia_age(self):
        return Helper.calculate_age(date(2022, 7, 11))