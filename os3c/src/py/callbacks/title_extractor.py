from .callback import CallbackHandler, CallbackLogger, Params
from selectolax.parser import HTMLParser


@CallbackHandler.register
async def title_extractor(params: Params, logger: CallbackLogger) -> None:
    if not params.raw_html:
        return None

    html = HTMLParser(params.raw_html)
    title = html.tags('title')

    if not title:
        logger.error(f"{params.request.url} -> Title not found!")
        return None

    logger.info(f"{params.request.url} -> {title[0].text()}")
