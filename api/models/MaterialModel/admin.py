from django.contrib import admin
from .models import *

class ChoiceFor_Material_Detail(admin.TabularInline):
    model = Material_Detail
    extra = 3

class ChoiceForRecipe_input(admin.TabularInline):
    model = Input_Recipe_Material
    extra = 1

class ChoiceForRecipe_output(admin.TabularInline):
    model = Output_Recipe_Material
    extra = 1

class recipelist(admin.ModelAdmin):
    list_display = ("id","__str__")
    inlines = [ChoiceForRecipe_input,ChoiceForRecipe_output]

class materiallist(admin.ModelAdmin):
    list_display = ('id','name')
    inlines = [ChoiceFor_Material_Detail]

admin.site.register(Material,materiallist)
admin.site.register(Recipe,recipelist)