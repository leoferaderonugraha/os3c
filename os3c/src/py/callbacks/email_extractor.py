from .callback import CallbackHandler, CallbackLogger, Params

import re


CACHED_EMAILS = set()


@CallbackHandler.register
async def email_extractor(params: Params, logger: CallbackLogger) -> None:
    if not params.raw_html:
        return None

    pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    html = str(params.raw_html)

    for match in re.finditer(pattern, html):
        email = match.group(0)
        if email not in CACHED_EMAILS:
            logger.info(f"Email found: {email}")
            CACHED_EMAILS.add(email)
