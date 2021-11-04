from django.contrib import admin
from DepositoryModel.models import Depository,Depository_To_Material

class ChoiceForDepository_Material(admin.TabularInline):
    model = Depository_To_Material
    extra = 1

class Depository_Admin(admin.ModelAdmin):
    list_display = ("name","type_of")
    inlines = [ChoiceForDepository_Material]

admin.site.register(Depository,Depository_Admin)