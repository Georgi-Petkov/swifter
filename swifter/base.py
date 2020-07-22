from os import devnull
from contextlib import contextmanager, redirect_stderr, redirect_stdout


ERRORS_TO_HANDLE = [AttributeError, ValueError, TypeError, KeyError]
try:
    from numba.core.errors import TypingError

    ERRORS_TO_HANDLE.append(TypingError)
except ImportError:
    pass
ERRORS_TO_HANDLE = tuple(ERRORS_TO_HANDLE)

SAMPLE_SIZE = 1000
N_REPEATS = 3

@contextmanager
def suppress_stdout_stderr():
    """
    A context manager that redirects stdout and stderr to devnull
    Used for avoiding repeated prints of the data during sample/test applies of Swifter
    """
    with open(devnull, "w") as fnull:
        with redirect_stderr(fnull) as err, redirect_stdout(fnull) as out:
            yield (err, out)

class _SwifterBaseObject:
    def __init__(self, base_obj):
        self._obj = base_obj
        self._nrows = self._obj.shape[0]

    @staticmethod
    def _validate_apply(expr, error_message):
        if not expr:
            raise ValueError(error_message)