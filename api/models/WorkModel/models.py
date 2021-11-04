from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from MaterialModel.models import Material_Detail,Recipe
from SkillModel.models import Big_Skill,Small_Skill
from MaterialModel.models import Material_Detail
from django import forms

#随机产出中间表
class Work_Main_To_Material_Detail(models.Model):
    class Meta:
        verbose_name = "随机产出中间表"
        verbose_name_plural = verbose_name

    work_main = models.ForeignKey('Work_Main',on_delete=models.CASCADE,verbose_name='工作类型')
    material_detail = models.ForeignKey(Material_Detail,on_delete=models.CASCADE,verbose_name='产出')
    chance = models.FloatField('概率',default=0)

    def __str__(self):
        return "随机产出中间表" + str(self.id)

#工作类型
class Work_Main(models.Model):
    class Meta:
        verbose_name = "工作类型"
        verbose_name_plural = verbose_name

    skill = models.ForeignKey(Big_Skill,on_delete=models.CASCADE,verbose_name="大类技能")
    skill_mini = models.ForeignKey(Small_Skill,on_delete=models.CASCADE,verbose_name="小类技能")
    type_choice = (("原料产出", "原料产出"),("加工", "加工"),("随机产出", "随机产出"),("服务", "服务"))
    type_of = models.CharField("类型",max_length=20,choices=type_choice,default="原料产出")
    production_materials = models.ForeignKey(Material_Detail,on_delete=models.CASCADE,verbose_name="产物",related_name="production_materials",blank=True,null=True)
    production_machining = models.ForeignKey(Recipe,on_delete=models.CASCADE,verbose_name="产出配方",blank=True,null=True)
    production_random_materials = models.ManyToManyField(Material_Detail,verbose_name="随机产出物资",related_name="production_random_materials",through=Work_Main_To_Material_Detail)
    
    def __str__(self):
        if self.type_of == "原料产出":
            return "产出" + self.production_materials.__str__()
        elif self.type_of == "加工":
            return "加工配方：" + self.production_machining.__str__()
        elif self.type_of == "随机产出":
            try:
                center_table = Work_Main_To_Material_Detail.objects.filter(work_main=self)
            except:
                center_table = []
            s = ""
            for x in center_table:
                s += str(x.chance) + "概率产出" + x.material_detail.__str__() + ","
            s = s.rstrip(",")
            return "随机产出:" + s
        elif self.type_of == "服务":
            return "服务"

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            print("工作类型不合法： %s" % e.message_dict)

class Work_Form(forms.ModelForm):
    class Meta:
        model = Work_Main
        fields = '__all__'
        
    def clean(self):
        type_of = self.cleaned_data.get('type_of')
        if type_of == "原料产出" and not self.cleaned_data.get('production_materials'):
            raise ValidationError("原料产出类工作需要有产出的具体原料")
        if type_of == "加工品" and not self.cleaned_data.get('production_machining'):
            raise ValidationError("加工类工作需要有产出的配方")
        if type_of == "随机产出" and not self.cleaned_data.get('production_random_materials'):
            raise ValidationError(str(self.cleaned_data))
            raise ValidationError("随机产出类工作需要有产出表")
        return self.cleaned_data