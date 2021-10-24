from django.contrib import admin
from .models import Material,Recipe,UserMaterial,MaterialDetail,Input_Recipe_Material,Output_Recipe_Material
# Register your models here.
class ChoiceInline(admin.TabularInline):#物资表添加
    model = MaterialDetail
    extra = 3

class ChoiceForRecipe_input(admin.TabularInline):
    model = Input_Recipe_Material
    extra = 1

class ChoiceForRecipe_output(admin.TabularInline):
    model = Output_Recipe_Material
    extra = 1

class usermateriallist(admin.ModelAdmin):
    list_display = ('user','material_detail','count')

class recipelist(admin.ModelAdmin):
    list_display = ("id","__str__")
    inlines = [ChoiceForRecipe_input,ChoiceForRecipe_output]

class materiallist(admin.ModelAdmin):
    list_display = ('material_id','name')
    inlines = [ChoiceInline]

admin.site.register(Material,materiallist)
admin.site.register(Recipe,recipelist)
admin.site.register(UserMaterial,usermateriallist)