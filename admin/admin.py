from django.contrib import admin

from .changelist import PowerChangelist
from .nasty_stuff import inject_request_into_form


class PowerModelAdmin(admin.ModelAdmin):
    """
    Improved Admin class:
    - pass request objects to forms that need them using set_request
    - uses PowerChangeList, which uses prefetch_related
    - call get_extra_urls
    """

    def _create_formsets(self, request, obj, change):
        formsets, inline_instances = super()._create_formsets(request, obj, change)

        # Add current request to ModelInline instances
        for inline in inline_instances:
            if hasattr(inline, 'set_request'):
                inline.set_request(request)

        # Add current request to ModelInline Formset Forms
        for formset in formsets:
            for form in formset.forms:
                if hasattr(form, 'set_request'):
                    form.set_request(request)

        return formsets, inline_instances

    def get_changelist(self, request, **kwargs):
        return PowerChangelist

    def get_urls(self):
        urlpatterns = self.get_extra_urls() + super().get_urls()

        return urlpatterns

    def get_extra_urls(self):
        return []

    def get_form(self, request, obj=None, change=False, **kwargs):
        form_class = super().get_form(request, obj, change, **kwargs)

        return inject_request_into_form(form_class, request)

    @property
    def model_info(self):
        return self.model._meta.app_label, self.model._meta.model_name
