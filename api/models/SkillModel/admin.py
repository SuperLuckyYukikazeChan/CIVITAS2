from django.contrib import admin
from .models import User_Skill_To_Big_Skill,User_Skill_To_Small_Skill,Big_Skill,Small_Skill,User_Skill

class ChoiceFor_Big_Skill(admin.TabularInline):
    model = User_Skill_To_Big_Skill
    extra = 1

class ChoiceFor_Small_Skill(admin.TabularInline):
    model = User_Skill_To_Small_Skill
    extra = 1

class User_Skill_Admin(admin.ModelAdmin):
    inlines = [ChoiceFor_Big_Skill,ChoiceFor_Small_Skill]

admin.site.register(Big_Skill)
admin.site.register(Small_Skill)
admin.site.register(User_Skill,User_Skill_Admin)