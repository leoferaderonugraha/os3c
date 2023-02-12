from .callback import Params
import re


def callback(params: Params) -> None:
    pattern = re.compile(r'\b(?:\+62|62|0)(?:\d{2,3})?\d{7,8}\b')
    html = params.raw_html.decode()
    name = '.'.join(__name__.split('.')[-2:])

    phone_numbers = set()

    for match in re.finditer(pattern, html):
        number = match.group(0)
        if number not in phone_numbers:
            print(f"{name}: [+] Phone number found: {number}")
            phone_numbers.add(number)
