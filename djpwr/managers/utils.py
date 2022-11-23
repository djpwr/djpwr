from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.manager import BaseManager
from django.http import Http404


def get_model(label):
    """
    Get a Model class by label ('app_label.ModelName').

    :param label: Django model string: 'app_label.ModelClass'
    :return: Model class
    """
    app_label, model_name = label.split('.')

    return django_apps.get_model(app_label=app_label, model_name=model_name)


def get_manager(label, manager_name=None):
    """
    Get a model's Manager class by label ('app_label.ModelName').

    :param label: Django model string: 'app_label.ModelName'
    :param manager_name: Return get_manager instance other than Model._default_manager
    :return: Manager instance
    """
    model_class = get_model(label)

    if manager_name:
        return getattr(model_class, manager_name)

    return model_class._default_manager


def from_queryset(qs_class):
    return BaseManager.from_queryset(qs_class)


def object_or_404(manager_method, *args, **kwargs):
    try:
        return manager_method(*args, **kwargs)
    except ObjectDoesNotExist:
        raise Http404()
