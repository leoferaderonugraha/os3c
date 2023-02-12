from .src.py.app import App
from .src.py.crawlers import NaiveCrawler
from .src.py.callbacks import (
    email_extractor,
    phone_extractor,
    title_extractor
)

import argparse
import asyncio


async def main() -> None:
    parser = argparse.ArgumentParser(description="OS3C")
    parser.add_argument('-u', '--url',
                        type=str,
                        help='Target URL')
    parser.add_argument('-i', '--ignore',
                        type=str,
                        help='List of ignored path (comma separated)')
    args = parser.parse_args()

    if args.url is None:
        print('URL required!')
        return None

    callbacks = [email_extractor, title_extractor, phone_extractor]

    app = App(crawler=NaiveCrawler, callbacks=callbacks)

    url = args.url
    ignore_path = ['#']

    if args.ignore is not None:
        ignore_path.extend(args.ignore.split(','))

    await app.check(url,
                    ignore_path=ignore_path)
    await app.wait_for_callbacks()


asyncio.run(main())
