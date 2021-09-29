from dataclasses import dataclass
from datetime import date


@dataclass
class User:
    username: str
    born_date: date
    born_iso: str


guido = User(
    username='guido',
    born_date=date(1956, 1, 31),
    born_iso='1956-01-31',
)

birthday_boy = User(
    username='tester',
    born_date=date.today().replace(year=1989),
    born_iso=date.today().replace(year=1989).isoformat(),
)
