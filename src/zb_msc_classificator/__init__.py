# TODO: write timing decorator
# TODO: parameter space:
#   - weighted distribution (linear, log, binary, exp, ratio)
#   - confidence of keywords (external input = prior = expert, confidence
#   intervall) (instead of binary keyword_state_vector)
#       + bootstrap for confidence interval (small bins to find range of
#       occurences - needs to be representative! (there should be a test for
#       that)
#   - confidence of stopwords (smaller weight, confidence interval) ->
#   absorbed into keyword_state_vector prior

# TODO: analysis class

# TODO: testfiles import from ES / matrix?

import time
import datetime
import functools

from importlib.metadata import version


__version__ = version('zb_msc_classificator').split(".dev")[0]


def executing(value):
    def apply(func):
        return func(value)
    return apply


timing_device = {}


def my_timing(func):

    """Decorator function."""
    @functools.wraps(func)
    def call_func(*args, **kwargs):
        """Takes a arbitrary number of positional and keyword arguments."""
        # Call original function and return its result.
        timing_device["timestamp"] = str(datetime.datetime.now())
        starting_time = time.time()
        my_func = func(*args, **kwargs)
        timing_device["execution_time"] = time.time() - starting_time
        return my_func
    # Return function defined in this scope.
    return call_func
