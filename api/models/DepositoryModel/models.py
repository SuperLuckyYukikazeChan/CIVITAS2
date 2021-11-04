from django.db import models
from MaterialModel.models import Material_Detail

#库房
class Depository(models.Model):
    class Meta:
        verbose_name = "库房"
        verbose_name_plural = verbose_name

    name = models.CharField("名称",max_length=30)
    type_choice = (("个人", "个人"),("不动产", "不动产"),("城市", "城市"))
    type_of = models.CharField("类型",max_length=10,choices=type_choice,default="个人")
    depository_materials = models.ManyToManyField(Material_Detail,verbose_name="库房拥有物资",related_name="depository_materials",through="Depository_To_Material")

    def __str__(self):
        return self.name

#库房物资中间表
class Depository_To_Material(models.Model):
    class Meta:
        verbose_name = "库房物资中间表"
        verbose_name_plural = verbose_name

    depository = models.ForeignKey(Depository,on_delete=models.CASCADE,verbose_name="库房",related_name="depository_material")
    material = models.ForeignKey(Material_Detail,on_delete=models.CASCADE,verbose_name="物资")
    count = models.FloatField(verbose_name="数量")

    def __str__(self):
        return "库房物资中间表"