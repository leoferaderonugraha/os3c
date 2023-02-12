from .callback import Params
from selectolax.parser import HTMLParser


def callback(params: Params) -> None:
    html = HTMLParser(params.raw_html)
    title = html.tags('title')[0]
    name = '.'.join(__name__.split('.')[-2:])

    print(f"{name}: [+] {params.url} -> {title.text()}")
