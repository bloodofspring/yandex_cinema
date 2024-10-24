from collections.abc import Callable
from typing import Any

import colorama


def handle_broad_exception(exception: Any, **custom_exceptions: tuple[type[Exception], str]) -> bool:
    for cust in custom_exceptions.values():
        exception_, message = cust
        color = cust[2] if len(cust) > 2 else colorama.Fore.LIGHTRED_EX
        if not isinstance(exception_(), exception.__class__):
            continue

        print(color + message)

        return False

    return True


def exception_handler(
        ignore_broad_exceptions: bool = False,
        default_message: str | None = None,
        **custom_exceptions: tuple[type[Exception], str]
):
    colorama.init(autoreset=True)

    def decorator(func: Callable):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as error:
                if not handle_broad_exception(exception=error, **custom_exceptions):
                    return False

                if ignore_broad_exceptions:
                    if default_message:
                        print(default_message)
                else:
                    print(colorama.Fore.LIGHTRED_EX + str(error))

                return False

        return inner

    return decorator
