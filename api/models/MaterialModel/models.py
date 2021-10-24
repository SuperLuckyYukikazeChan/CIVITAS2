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
    level_choices = ((1, 'Q1'), (2, 'Q2'),(3, 'Q3'))
    material = models.ForeignKey('Material',on_delete=models.CASCADE,verbose_name='物资')
    productivity = models.FloatField(verbose_name='物资自身产能')
    level = models.SmallIntegerField(verbose_name='物资等级',default=1,choices=level_choices)

    class Meta:
        unique_together = [
            'material','level'
        ]

    def __str__(self):
        return self.material.name+' Q.'+str(self.level)

class Input_Recipe_Material(models.Model):
    recipe = models.ForeignKey('Recipe',on_delete=models.CASCADE,verbose_name='配方')
    material = models.ForeignKey('MaterialDetail',on_delete=models.CASCADE,verbose_name='输入物资')
    count = models.IntegerField(verbose_name='数量')

    class Meta:
        verbose_name_plural = '所需物资表'

class Output_Recipe_Material(models.Model):
    recipe = models.ForeignKey('Recipe',on_delete=models.CASCADE,verbose_name='配方')
    material = models.ForeignKey('MaterialDetail',on_delete=models.CASCADE,verbose_name='物资')
    count = models.IntegerField(verbose_name='数量')

    class Meta:
        verbose_name_plural = '产出物资表'

class Recipe(models.Model):
    input = models.ManyToManyField('MaterialDetail',related_name='input',verbose_name='输入',through=Input_Recipe_Material)
    output = models.ManyToManyField('MaterialDetail',related_name='output',verbose_name='输出',through=Output_Recipe_Material)

# class Recipe(models.Model):
#     #     DATA_SCHEMA =     {
#         "data":[
#             {
#                 "material_id":'物资id',
#                 "count":'物资id'
#             }
#         ]
#     }
    

#     raw_material_data = JSONField(verbose_name='所需物资数据')
#     '''
#     {
#         "data":[
#             {
#                 "material_id":id,
#                 "count":count
#             },
#             {
#                 "material_id":id,
#                 "count":count
#             },
#             ...
#         ]
#     }
#     '''
#     material_detail = ForeignKey('MaterialDetail',related_name='material_detail',on_delete=models.CASCADE,verbose_name='产出详情')
#     produce_count = FloatField(verbose_name='产出物资数量',default=1)

#     class Meta:
#         unique_together = [
#             'raw_material_data'
#         ]

#     def __str__(self):
#         return str(self.material_detail.material)+' Q'+str(self.material_detail.level)