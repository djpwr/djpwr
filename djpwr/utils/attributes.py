

def lookup_value(obj, lookup, separator='.'):
    """
    Traverse an objects attributes to find a value.

    :param obj: Object to start value traversing
    :param lookup: Lookup string that defines attribute search
    :param separator: Separator used in the lookup string
    :return: Value

    Examples:

    author_birth_date = lookup_value(book, 'author.birth_date')
    publisher_province = lookup_value(book, 'publisher.address.city.province')
    """

    if lookup == 'self':
        return obj

    value = obj

    for key in lookup.split(separator):
        value = getattr(value, key)

        if value is None:
            return None

    return value
