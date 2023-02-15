from .callback import CallbackHandler, CallbackLogger, Params
from urllib.parse import urlsplit

import os


@CallbackHandler.register
async def request_logger(params: Params, logger: CallbackLogger) -> None:
    url_parts = urlsplit(params.request.url)
    folder = url_parts.netloc
    file_name = folder + '/log.txt'

    if not os.path.exists(folder):
        os.makedirs(folder)

    with open(file_name, 'a') as fp:
        fp.write(f"{params.request.url} -> {params.request.method}\n")
