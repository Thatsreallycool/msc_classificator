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

from configparser import ConfigParser
import os.path


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


def read_ini(file_path):
    """
    purpose: configuration data is read in

    :param file_path: config file path, should in the same folder as main.py
    meant for configuration of database server

    :return: dictionary with all config data ("key" = "value")
    (see config.ini.template)

    """
    if not os.path.exists(file_path):
        raise Exception("config file not found!")
    config = ConfigParser()
    config.read(file_path)

    my_config = {}
    for section in config.sections():
        my_config[section] = {}
        for key in config[section]:
            my_config[section][key] = config[section][key]
    return my_config