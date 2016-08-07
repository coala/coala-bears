from coalib.settings.FunctionMetadata import FunctionMetadata


def deprecate_settings(**depr_args):
    def _deprecate_decorator(func):
        def wrapping_function(*args, **kwargs):
            for arg, deprecated_arg in depr_args.items():
                if deprecated_arg in kwargs and arg not in kwargs:
                    print("The setting `{}` is deprecated. Please use `{}` "
                          "instead.".format(deprecated_arg, arg))
                    kwargs[arg] = kwargs[deprecated_arg]
                    del kwargs[deprecated_arg]
            return func(*args, **kwargs)
        wrapping_function.__metadata__ = FunctionMetadata.from_function(func)
        for arg, deprecated_arg in depr_args.items():
            wrapping_function.__metadata__.optional_params[
                deprecated_arg] =
                wrapping_function.__metadata__.optional_params[arg]
        return wrapping_function
    return _deprecate_decorator
