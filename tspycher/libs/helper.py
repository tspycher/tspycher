from datetime import date


class Helper(object):
    @staticmethod
    def calculate_age(birth_date):
        today = date.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))