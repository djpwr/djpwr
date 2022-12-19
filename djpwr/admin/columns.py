from djpwr.utils.attributes import lookup_value


class AttributeColumn:
    """
    Usage:

    class BookAdmin(admin.ModelAdmin):
        list_display = ['publisher_province']

        publisher_province = AttributeColumn.build(
            'publisher.address.city.province', _("Province"),
        )

    """

    description = "Attribute"

    @classmethod
    def build(cls, attribute_lookup, description=None, **kwargs):
        def list_display_method(self, obj):
            value = cls.get_value(obj, attribute_lookup,  **kwargs)

            if value is None:
                return cls.format_empty_value(**kwargs)

            return cls.format_value(value, **kwargs)

        description = description or cls.description

        list_display_method.short_description = description
        list_display_method.admin_order_field = cls.get_order_field(
            attribute_lookup, **kwargs
        )

        return list_display_method

    @classmethod
    def get_order_field(cls, attribute_lookup, **kwargs):
        if attribute_lookup == 'self':
            return 'pk'
        else:
            return attribute_lookup.replace('.', '__')

    @classmethod
    def get_value(cls, obj, attribute_lookup, **kwargs):
        return lookup_value(obj, attribute_lookup)

    @classmethod
    def format_value(cls, value, **kwargs):
        return value

    @classmethod
    def format_empty_value(cls, **kwargs):
        return '-'


def attr_column(lookup, description=None, boolean=None):
    """
    Usage:

    class BookAdmin(admin.ModelAdmin):
        list_display = ['publisher_province']

        publisher_province = attr_column('publisher.address.city.province',_("Province"))
    """

    return AttributeColumn.build(lookup, description, boolean=boolean)
