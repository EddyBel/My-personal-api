# from datetime import date
from datetime import datetime, timedelta


def get_date_of_birth(date_of_birth: str) -> int:
    """
        This function takes as parameter a date of birth in 'YYYYY-MM-DD' format and returns the current age of the person in years. returns the current age of the person in years.

        Params:
            date_of_birth (str): date of birth
    """
    today = datetime.now().date()
    birth = datetime.strptime(
        date_of_birth, "%Y-%m-%d").date()
    age = today.year - birth.year - \
        ((today.month, today.day) < (birth.month, birth.day))
    return age


def get_date_of_expire(days: int) -> datetime:
    """This function adds the time in days to the current date. 

    Args:
        days (int): Days of adds

    Returns:
        (datetime): Update date
    """
    now = datetime.now()
    new_date = now + timedelta(days=days)
    return new_date
