from .src.py.app import App
from .src.py.crawlers import NaiveCrawler

import argparse
import asyncio


async def main() -> None:
    description = "OS3C (Open Source Security Auditor/Checker)"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-u', '--url',
                        type=str,
                        help='Target URL')
    parser.add_argument('-i', '--ignore',
                        type=str,
                        default="",
                        help='List of ignored path (comma separated)')
    args = parser.parse_args()

    if args.url is None:
        print('URL required!')
        return None

    app = App(crawler=NaiveCrawler())

    url = args.url
    ignore_path = [path for path in args.ignore.split(',') if path]

    print(f"Will ignore: {ignore_path}\n")

    await app.check(url, ignore_path=ignore_path)
    await app.wait_for_callbacks()


asyncio.run(main())
