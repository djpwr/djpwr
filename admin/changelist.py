from django.contrib.admin.views.main import ChangeList


class PowerChangelist(ChangeList):
    """
    Modified ChangeList class.
    """
    list_select_related = []

    def __init__(self, request, *args, **kwargs):
        # It is sometimes very useful to have access to the request object
        self.request = request

        super().__init__(request, *args, **kwargs)

    def apply_select_related(self, qs):
        if isinstance(self.list_select_related, bool):
            # Removed True and False options for list_select_related: expanding
            # the queryset with an unknown number of related relations of unknown
            # depth is NOT a good idea.
            return qs

        if self.list_select_related:
            # Prefetch related is usually the better choice for fetching related
            # objects: it only fetches related objects for the current page.
            return qs.prefetch_related(*self.list_select_related)

        return qs
