from django.db import models
from MaterialModel.models import MaterialDetail,Recipe
from CityModel.models import County,Suburb,Abstract_County

class Estate_Material(models.Model):
    class Meta:
        verbose_name = "不动产需求物资"
        verbose_name_plural = verbose_name

    estate = models.ForeignKey("Estate_Type",on_delete=models.CASCADE,verbose_name="不动产")
    material = models.ForeignKey(MaterialDetail,on_delete=models.CASCADE,verbose_name="物资")
    count = models.FloatField(verbose_name="数量")

    def __str__(self):
        return "不动产需求物资"

class Estate_Type(models.Model):
    class Meta:
        verbose_name = "不动产类型"
        verbose_name_plural = verbose_name
    
    #名字
    name = models.CharField("不动产类型名",max_length=20)

    #土地相关
    max_lands = models.FloatField("占地面积")
    allowable_terrain = models.ManyToManyField(MaterialDetail,verbose_name="允许建设的地形")
    #建筑材料
    need_material = models.ManyToManyField(MaterialDetail,verbose_name="建设需要材料",through=Estate_Material)

    #是否为原材料建筑
    is_raw_materials = models.BooleanField("是否为原材料建筑")
    list_of_raw_materials = models.ManyToManyField(MaterialDetail,verbose_name="可产原料表",related_name="list_raw_materials",blank=True)

    #是否为加工建筑
    is_machining = models.BooleanField("是否为加工建筑")
    list_of_machining = models.ManyToManyField(Recipe,verbose_name="可产加工品",related_name="list_machining",blank=True)

    number_of_work_person = models.IntegerField("单位面积工作人数",blank=True)

    #是否为住宅
    is_house = models.BooleanField("是否为住宅")
    number_of_house_person = models.IntegerField("单位面积可居住人数",blank=True)

    #是否为餐厅
    is_restaurant = models.BooleanField("是否为餐厅")

class Estate(models.Model):
    class Meta:
        verbose_name = "不动产"
        verbose_name_plural = verbose_name
    
    #名字
    name = models.CharField("不动产名",max_length=20)

    #类型
    type_of = models.ForeignKey(Estate_Type,on_delete=models.CASCADE,verbose_name="类型")

    #当前占地
    now_lands = models.FloatField("当前占地")

    #位于
    #location = models.ForeignKey(Abstract_County,on_delete=models.CASCADE,verbose_name="位于")

    #建立时间
    created_at = models.DateTimeField(auto_now=True)