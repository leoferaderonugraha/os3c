from .callback import CallbackHandler, CallbackLogger, Params

import re


CACHED_PHONE = set()


@CallbackHandler.register
async def phone_extractor(params: Params, logger: CallbackLogger) -> None:
    if not params.raw_html:
        return None

    pattern = re.compile(r'\b(?:\+62|62|0)(?:\d{2,3})?\d{7,8}\b')
    html = str(params.raw_html)

    for match in re.finditer(pattern, html):
        number = match.group(0)
        if number not in CACHED_PHONE:
            logger.info(f"Phone number found: {number}")
            CACHED_PHONE.add(number)
