

def inject_request_into_form(form_class, request):
    """
    Workaround for Admin forms that need the current request.

    Use case:

    Sometimes it is necesary to have access to the current Request object from
    within a Form instance.

    Problem:

    Django admin only offers ModelAdmin.get_form, which returns the form class. The
    actual form instance is created in _change_view. We don't want to copy paste
    the entire _change_view method.

    Solution:

    Wrap the form class returned from ModelAdmin.get_form in a decorator along
    with the request, catch the instantiation call and inject the request into
    every newly instantiated object.
    Nasty stuff...
    """
    def pretend_to_be__new__(*args, **kwargs):
        form_instance = form_class(*args, **kwargs)

        if hasattr(form_instance, 'set_request'):
            form_instance.set_request(request)

        return form_instance

    return pretend_to_be__new__
