

def attr_filter(attr_lookup, filter_value=None, *, only_values=None):
    """
    Create a Manager filter method based on an ORM attribute lookup, either
    with or without a fixed value.

    :param attr_lookup: ORM attribute_lookup, can use dots instead of dunder
    :param filter_value: Value to use for filtering
    :param allow_only_values: Attributes allowed to return as flat list
    :return: Manager filter function

    Example:

    class BookQueryset(Queryset):
        author = attr_filter('author')
        without_publisher = attr_filter('publisher__isnull', True)

    some_author = Author.objects.get(id=1234)
    books_by_some_author = Book.objects.author(some_author)
    books_without_publisher = Book.objects.without_publisher()
    """
    if filter_value is None:
        return attr_filter_arg_value(attr_lookup, only_values=only_values)
    else:
        return attr_filter_fixed_value(
            attr_lookup, filter_value, only_values=only_values
        )


def attr_filter_arg_value(attr_lookup, *, only_values=None):
    """
    Create a Manager filter method based on an ORM attribute lookup

    :param attr_lookup: ORM attribute_lookup, can use dots instead of dunder
    :param allow_only_values: Attributes allowed to return as flat list
    :return: Manager filter function

    Example:

    class BookQueryset(Queryset):
        author = attr_filter_arg_value('author')
        publisher_city = attr_filter_arg_value('publisher__city')

    books_by_some_author = Book.objects.author('Some Author')
    books_published_in_rome = Book.objects.publisher_city('Rome')
    """
    def filter_func(self, value):
        filter_kwargs = {attr_lookup: value}

        return self.filter(**filter_kwargs)

    if only_values is None:
        return filter_func

    return allow_only_values(*only_values)(filter_func)


def attr_filter_fixed_value(attr_lookup, value, only_values=None):
    """
    Create a Manager filter method based on an ORM attribute lookup and a
    specific value

    :param attr_lookup: ORM attribute_lookup, can use dots instead of dunder
    :param value: Value to use for filtering
    :param allow_only_values: Attributes allowed to return as flat list
    :return: Manager filter function

    Example:

    class BookQueryset(Queryset):
        without_publisher = attr_filter_fixed_value('publisher__isnull', True)

    books_without_publisher = Book.objects.without_publisher()
    """

    def filter_func(self):
        filter_kwargs = {attr_lookup: value}

        return self.filter(**filter_kwargs)

    if only_values is None:
        return filter_func

    return allow_only_values(*only_values)(filter_func)


def allow_only_values(*attribute_names):
    """
    Decorator for manager methods to optionally only return a specific value

    Example:

    class BookManager(Manager):
        @allow_only_values('id')
        def author(self, author):
            return self.filter(author=author)

    book_ids_by_some_author = Book.objects.author('Some Author', only_values='id')
    """

    def func_wrapper(manager_method):
        def only_value_wrapper(*args, **kwargs):
            only_values_attribute = kwargs.pop('only_values', None)

            qs = manager_method(*args, **kwargs)

            if only_values_attribute:
                if only_values_attribute not in attribute_names:
                    raise ValueError(
                        "only_value='{}' not allowed".format(only_values_attribute)
                    )

                qs = qs.values_list(only_values_attribute, flat=True)

            return qs

        return only_value_wrapper

    return func_wrapper


# DEPRECATED: Use allow_only_values
def allow_values_only(*attribute_names):
    """
    Decorator for manager methods to optionally only return a specific value

    Example:

    class BookManager(Manager):
        @allow_values_only('id')
        def author(self, author):
            return self.filter(author=author)

    book_ids_by_some_author = Book.objects.author('Some Author', only_values='id')
    """

    def func_wrapper(manager_method):
        def value_only_wrapper(*args, **kwargs):
            only_values_attribute = kwargs.pop('only_values', None)

            qs = manager_method(*args, **kwargs)

            if only_values_attribute:
                if only_values_attribute not in attribute_names:
                    raise ValueError(
                        "only_value='{}' not allowed".format(only_values_attribute)
                    )

                qs = qs.values_list(only_values_attribute, flat=True)

            return qs

        return value_only_wrapper

    return func_wrapper
