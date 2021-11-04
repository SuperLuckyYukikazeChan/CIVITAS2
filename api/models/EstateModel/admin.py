from django.contrib import admin
from EstateModel.models import *

class ChoiceForEstate_Material(admin.TabularInline):
    model = Estate_To_Material
    extra = 1

class Estate_Type_Admin(admin.ModelAdmin):
    list_display = ("name","max_lands")
    inlines = [ChoiceForEstate_Material]

admin.site.register(Estate_Type,Estate_Type_Admin)
admin.site.register(Estate)