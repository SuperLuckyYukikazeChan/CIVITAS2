from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Material(models.Model):
    class Meta:
        verbose_name = "物资"
        verbose_name_plural = verbose_name

    id = models.IntegerField('物资id',primary_key=True)
    name = models.CharField('物资名',max_length=20,unique=True)
    eatable = models.BooleanField('是否为食品',default=False)
    base_loss = models.FloatField('基础损耗率',default=0)

    def __str__(self):
        return self.name

class Material_Detail(models.Model):
    class Meta:
        verbose_name = "物资详情"
        verbose_name_plural = verbose_name
        unique_together = [
            'material','level'
        ]

    level_choices = ((1, 'Q1'),(2, 'Q2'),(3, 'Q3'))
    material = models.ForeignKey(Material,on_delete=models.CASCADE,verbose_name='物资')
    productivity = models.FloatField('物资自身产能')
    level = models.SmallIntegerField('物资等级',default=1,choices=level_choices)
    stamina = models.FloatField("精力",default=100,blank=True,null=True)
    health = models.FloatField("健康",default=100,blank=True,null=True)
    happiness = models.FloatField("快乐",default=100,blank=True,null=True)
    starvation = models.FloatField("饥饿",default=100,blank=True,null=True)

    def clean(self):
        if self.material.eatable and self.stamina != 0 and not self.stamina:
            raise ValidationError("食品需要精力值")
        if self.material.eatable and self.health != 0 and not self.health:
            raise ValidationError("食品需要健康值")
        if self.material.eatable and self.happiness != 0 and not self.happiness:
            raise ValidationError("食品需要快乐值")
        if self.material.eatable and self.starvation != 0 and not self.starvation:
            raise ValidationError("食品需要饥饿值")

    def __str__(self):
        return "Q" + str(self.level) + self.material.name
    
    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            print("物资不合法： %s" % e.message_dict)

class Input_Recipe_Material(models.Model):
    class Meta:
        verbose_name = "所需物资表"
        verbose_name_plural = verbose_name

    recipe = models.ForeignKey('Recipe',on_delete=models.CASCADE,verbose_name='配方')
    material = models.ForeignKey(Material_Detail,on_delete=models.CASCADE,verbose_name='输入物资')
    count = models.FloatField('数量')

class Output_Recipe_Material(models.Model):
    class Meta:
        verbose_name = "产出物资表"
        verbose_name_plural = verbose_name
    
    recipe = models.ForeignKey('Recipe',on_delete=models.CASCADE,verbose_name='配方')
    material = models.ForeignKey(Material_Detail,on_delete=models.CASCADE,verbose_name='物资')
    count = models.FloatField('数量')

class Recipe(models.Model):
    class Meta:
        verbose_name = "配方"
        verbose_name_plural = verbose_name

    input = models.ManyToManyField(Material_Detail,related_name="recipe_input",verbose_name="输入",through=Input_Recipe_Material)
    output = models.ManyToManyField(Material_Detail,related_name="recipe_output",verbose_name="输出",through=Output_Recipe_Material)

    def __str__(self):
        str_material = ""
        for x in self.input.all():
            str_material += "%s," % (x.__str__())
        str_material = str_material.rstrip(",")
        str_material += "——>"
        for x in self.output.all():
            str_material += "%s," % (x.__str__())
        str_material = str_material.rstrip(",")
        return str_material