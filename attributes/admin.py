from django.contrib import admin
from django.template.defaultfilters import truncatewords

from attributes.models import Attribute


# Register your models here.
@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_description']

    @admin.display(description="short description")
    def short_description(self, obj):
        return truncatewords(obj.description, 15)