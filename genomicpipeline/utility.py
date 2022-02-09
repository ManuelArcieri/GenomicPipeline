def ensure(expression: bool, error_message: str, exception_type = ValueError):
    if not expression:
        raise exception_type(error_message)


def get_or_raise(document: dict, key: str):
    try:
        return document[key]
    except:
        raise KeyError(f'the TOML file does not contain the key {key}')
