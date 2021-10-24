from django.db import models
from django.db.models.fields import CharField, FloatField, IntegerField, SmallIntegerField
from django.db.models import JSONField
from django.db import models
from django.conf import settings
from SkillModel.admin import smalllist

class Material(models.Model):
    material_id = models.IntegerField(verbose_name='物资id',unique=True)
    name = models.CharField(max_length=20,verbose_name='物资名',unique=True)

    def __str__(self):
        return self.name

class UserMaterial(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name='用户')
    material_detail = models.ForeignKey('MaterialDetail',on_delete=models.CASCADE,verbose_name='物资详情')
    count = models.FloatField(verbose_name='拥有数量')

    class Meta:
        unique_together = [
            'user','material_detail'
        ]

    def __str__(self):
        return self.user.username

class MaterialDetail(models.Model):
    class Meta:
        verbose_name = "物资详情"
        verbose_name_plural = verbose_name
        unique_together = [
            'material','level'
        ]

    level_choices = ((1, 'Q1'), (2, 'Q2'),(3, 'Q3'))
    material = models.ForeignKey(Material,on_delete=models.CASCADE,verbose_name='物资')
    productivity = models.FloatField(verbose_name='物资自身产能')
    level = models.SmallIntegerField(verbose_name='物资等级',default=1,choices=level_choices)

    def __str__(self):
        return "Q" + str(self.level) + self.material.name

class Input_Recipe_Material(models.Model):
    class Meta:
        verbose_name = "所需物资表"
        verbose_name_plural = verbose_name

    recipe = models.ForeignKey('Recipe',on_delete=models.CASCADE,verbose_name='配方')
    material = models.ForeignKey('MaterialDetail',on_delete=models.CASCADE,verbose_name='输入物资')
    count = models.IntegerField(verbose_name='数量')

class Output_Recipe_Material(models.Model):
    class Meta:
        verbose_name = "产出物资表"
        verbose_name_plural = verbose_name
    
    recipe = models.ForeignKey('Recipe',on_delete=models.CASCADE,verbose_name='配方')
    material = models.ForeignKey('MaterialDetail',on_delete=models.CASCADE,verbose_name='物资')
    count = models.IntegerField(verbose_name='数量')

class Recipe(models.Model):
    class Meta:
        verbose_name = "配方"
        verbose_name_plural = verbose_name

    input = models.ManyToManyField(MaterialDetail,related_name="input",verbose_name="输入",through=Input_Recipe_Material)
    output = models.ManyToManyField(MaterialDetail,related_name="output",verbose_name="输出",through=Output_Recipe_Material)

    def __str__(self):
        str_material = ""
        for x in self.input.all():
            str_material += "Q%s%s," % (x.level,x.material.name)
        str_material = str_material.rstrip(",")
        str_material += "——>"
        for x in self.output.all():
            str_material += "Q%s%s," % (x.level,x.material.name)
        str_material = str_material.rstrip(",")
        return str_material