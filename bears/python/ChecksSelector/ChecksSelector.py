from coalib.settings.Setting import typed_list


def set_checks(ignore: str = '--ignore',
               ignore_check: typed_list(str) = (),
               select: str = '--select',
               select_check: typed_list(str) = ()):
    """
    :param select: Command args that execute select_checks
    :param ignore: Command args that ignore/skip ignore_check
    :param select_check: List of check IDs to run
    :param ignore_check: List of check IDs to ignore/skip
    """
    args = ()
    if select_check:
        select_list = ','.join(part.strip() for part in select_check)
        args += (select + '=' + select_list,)

    if ignore_check:
        ignore_list = ','.join(part.strip() for part in ignore_check)
        args += (ignore + '=' + ignore_list,)

    return args
