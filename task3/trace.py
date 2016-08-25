#!/usr/bin/python


from functools import wraps


def trace(stream):
    def decorator(func):
        trace_enabled = True

        @wraps(func)
        def internal(*args, **kwargs):
            stream.write("Enter: " + func.__name__ + str(args) + "\n")
            func(*args)
            stream.write("Exit: " + func.__name__ + "\n")
            trace_enabled = args[0].trace_enabled
        return internal if trace_enabled else func
    return decorator
