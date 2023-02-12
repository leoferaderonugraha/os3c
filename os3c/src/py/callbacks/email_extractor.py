from .callback import Params

import re


def callback(params: Params) -> None:
    pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    html = params.raw_html.decode()
    name = '.'.join(__name__.split('.')[-2:])

    emails = set()

    for match in re.finditer(pattern, html):
        email = match.group(0)
        if email not in emails:
            print(f"{name}: [+] Email found: {email}")
            emails.add(email)
