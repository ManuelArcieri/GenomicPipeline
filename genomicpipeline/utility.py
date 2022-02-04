def ensure(expression: bool, error_message: str, exception_type = ValueError):
    if not expression:
        raise exception_type(error_message)
