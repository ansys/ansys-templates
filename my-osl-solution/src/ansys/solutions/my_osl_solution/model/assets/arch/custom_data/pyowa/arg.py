"""

Copyright © 2021 ANSYS, Inc.

"""
import functools
import inspect
import os
import warnings


class ArgumentTypeError(Exception):
    pass


class ArgumentValueError(Exception):
    pass


def check_type(**accepted_types):
    """ A decorator to check function argument types.

    Example
    -------
    >>> import arg
    >>> @arg.check_type(first=str, second=bool)
    >>> def my_method(first, second=True):
    >>>     pass

    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if _is_skipped_by_user():
                return func(*args, **kwargs)
            func_args = inspect.getcallargs(func, *args, **kwargs)
            caller = func.__name__
            if 'self' in func_args:
                class_ = func_args.get('self').__class__.__name__
                caller = '{}.{}'.format(class_, caller)
            for name, exp_types in accepted_types.items():
                if not isinstance(func_args[name], exp_types):
                    type_ = str(type(func_args[name]))
                    msg = f'{caller}({name}: {type_}) -> expect {exp_types}'
                    raise ArgumentTypeError(msg)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def check_issubclass(**accepted_types):
    """ A decorator to check function argument subclass types.

    Example
    -------
    >>> import arg
    >>> @arg.check_issubclass(first=expected_parentclass)
    >>> def my_method(first):
    >>>     pass

    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if _is_skipped_by_user():
                return func(*args, **kwargs)
            func_args = inspect.getcallargs(func, *args, **kwargs)
            caller = func.__name__
            if 'self' in func_args:
                class_ = func_args.get('self').__class__.__name__
                caller = '{}.{}'.format(class_, caller)
            for name, exp_types in accepted_types.items():
                if not issubclass(func_args[name], exp_types):
                    type_ = str(type(func_args[name]))
                    msg = f'{caller}({name}: {type_}) -> expect {exp_types}'
                    raise ArgumentTypeError(msg)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def check_isenum(**accepted_types):
    """ A decorator to check if function argument is valid enum defined
        in enum_class.

    Example
    -------
    >>> import arg
    >>> @arg.check_isenum(first=enum_class)
    >>> def my_method(first):
    >>>     pass

    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if _is_skipped_by_user():
                return func(*args, **kwargs)
            func_args = inspect.getcallargs(func, *args, **kwargs)
            caller = func.__name__
            if 'self' in func_args:
                class_ = func_args.get('self').__class__.__name__
                caller = '{}.{}'.format(class_, caller)
            for name, exp_types in accepted_types.items():
                attributes = inspect.getmembers(
                        exp_types, lambda a: not(inspect.isroutine(a)))
                attributes = [
                        a[0] for a in attributes
                        if not(a[0].startswith('__') and a[0].endswith('__'))]
                enums = [getattr(exp_types, a) for a in attributes]
                if func_args[name] not in enums:
                    type_ = str(type(func_args[name]))
                    msg = f'{caller}({name}: {type_}:{func_args[name]}) -> expect enum of {exp_types}'
                    raise ArgumentTypeError(msg)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def _is_skipped_by_user():
    return os.environ.get('DISABLE_CHECKS', '0') == '1'


def raise_error_if_value_is_less_than(value, lower_bound):
    if value < lower_bound:
        msg = f'A value equal to or greater than "{lower_bound}" is expected. Got "{value}" instead.'
        raise ArgumentValueError(msg)


def raise_error_if_value_is_greater_than(value, upper_bound):
    if value > upper_bound:
        msg = f'A value equal to or less than "{upper_bound}" is expected. Got "{value}". instead'
        raise ArgumentValueError(msg)


def raise_error_if_not_is_subclass(object_, expected_parent_class):
    if not issubclass(object_.__class__, expected_parent_class):
        msg = f'A subclass of "{expected_parent_class}" is expected. Got "{object_.__class__}" instead.'
        raise ArgumentTypeError(msg)


def raise_error_if_value_is_outside_bounds(value, bounds):
    lower_bound, upper_bound = bounds
    raise_error_if_value_is_less_than(value, lower_bound)
    raise_error_if_value_is_greater_than(value, upper_bound)


def raise_error_if_enum_is_unknown(value, EnumClass):
    allowed_enums = [attr for attr in EnumClass.__dict__
                     if not _is_dunder(attr)]
    if value not in allowed_enums:
        msg = f'A enum value of "{allowed_enums}" is expedted. Got "{value}".'
        raise ArgumentValueError(msg)


def _is_dunder(name):
    return name.startswith('__') and name.endswith('__')


def deprecated(replacement=None):
    """ A decorator to show a deprecation warning.

        Example
        -------
        >>> import arg
        >>> @arg.deprerated('new_method_name')
        >>> def old_method():
        >>>     pass

    """
    def decorator(func):
        msg = f'"{func.__name__}" is deprecated'
        if replacement is not None:
            msg += f' - use "{replacement}" instead'

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
            print(msg)
            return func(*args, **kwargs)

        return wrapper
    return decorator
