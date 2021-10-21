from django.contrib import admin
from .models import *

class ChoiceForEstate_Material(admin.TabularInline):
    model = Estate_Material
    extra = 1

class recipelist(admin.ModelAdmin):
    list_display = ("name","max_lands","need_material_details")
    inlines = [ChoiceForEstate_Material]
    def need_material_details(self,obj):
        input_all = Estate_Material.objects.filter(pk=obj.pk)
        list_input = []
        for i in input_all:
            list_input.append(str(i.count) + "个Q" + str(i.material.level) + i.material.material.name)
        return '，'.join(list_input)

admin.site.register(Estate_Type,recipelist)
admin.site.register(Estate)