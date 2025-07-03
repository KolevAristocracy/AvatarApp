from django.contrib import admin

from attributes.models import Attribute


# Register your models here.
@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    ...