import os.path
import time


GEP_FOLDER = os.path.expandvars('$HOME/GenomicPipeline')


def ensure(expression: bool, error_message: str, exception_type = ValueError):
    if not expression:
        raise exception_type(error_message)


def get_or_raise(document: dict, key: str):
    try:
        return document[key]
    except:
        raise KeyError(f'the TOML file does not contain the key {key}')


def get_user_friendly_time(since: int, until = None) -> str:
    if since == 0:
        return '-'
    if until is None or until <= 0:
        until = int(time.time())
    elapsed = until - since

    if elapsed < 60:  # < 60 seconds
        return f'{elapsed} seconds'
    elif elapsed < 60 * 60:  # < 1 hour
        return f'{elapsed // 60} minute(s) and {elapsed % 60} second(s)'
    else:  # >= 1 hour
        return f'{elapsed // 3600} hour(s), {elapsed % 3600 // 60} minute(s), and {elapsed % 3600 % 60} second(s)'
