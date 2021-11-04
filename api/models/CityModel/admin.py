from django.contrib import admin
from .models import *

class ChoiceFor_County(admin.TabularInline):
    model = County_To_Terrain
    extra = 1

class ChoiceFor_Suburb(admin.TabularInline):
    model = Suburb_To_Terrain
    extra = 1

class County_Admin(admin.ModelAdmin):
    list_display = ("name","belong_city")
    inlines = [ChoiceFor_County]
        
class Suburb_Admin(admin.ModelAdmin):
    list_display = ("name","belong_city")
    inlines = [ChoiceFor_Suburb]

admin.site.register(Terrain)
admin.site.register(City)
admin.site.register(Climate)
admin.site.register(County,County_Admin)
admin.site.register(Suburb,Suburb_Admin)
admin.site.register(City_Road)