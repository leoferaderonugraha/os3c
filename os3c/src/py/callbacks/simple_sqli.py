from .callback import CallbackLogger, CallbackHandler, Params, Source, Method

import httpx


client = httpx.AsyncClient()


KEYWORDS = [
    'Invalid SQL Syntax',
    'You have an error in your SQL syntax',
    'ERROR: syntax error',
    'Database Error',
    'mysqli_num_rows()',
]


@CallbackHandler.register
async def simple_sqli(params: Params, logger: CallbackLogger) -> None:
    if params.request.source is not Source.FORM:
        return None

    url = params.request.url
    method = params.request.method
    req_params = params.request.params

    for param in req_params.keys():
        req_params[param] = "'"

    if method is Method.POST:
        resp = await client.post(url, data=req_params)
        is_vuln = False

        for keyword in KEYWORDS:
            if keyword in str(resp.content):
                is_vuln = True
                break

        if is_vuln:
            logger.info(f"{url} is vulnerable!")
            logger.info(f"parameters: {','.join(list(req_params.keys()))}")
            logger.info(f"method: {method}")
