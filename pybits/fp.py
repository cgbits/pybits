from typing import Callable, List, Optional, Any
from inspect import signature


def curry(func: Callable[..., Optional[Any]]) -> Callable[[Any], Any]:
    sig = signature(func)

    arguments = list(sig.parameters.keys())

    if len(arguments) == 1:
        return func

    def _curry(
        arg: Any,
        args: List[Any],
        count: int,
        func: Callable[..., Optional[Any]],
    ):
        args = args + [arg]

        if len(args) < count:

            def callback(arg: Any):
                return _curry(arg, args, count, func)

            return callback

        return func(*args)

    def callback(arg: Any):
        return _curry(arg, [], len(arguments), func)

    return callback
