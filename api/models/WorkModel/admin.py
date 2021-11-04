from django.contrib import admin
from .models import *

class ChoiceFor_Work_Main(admin.TabularInline):
    model = Work_Main_To_Material_Detail
    extra = 1

class Work_Main_Admin(admin.ModelAdmin):
    form = Work_Form
    inlines = [ChoiceFor_Work_Main]

admin.site.register(Work_Main,Work_Main_Admin)