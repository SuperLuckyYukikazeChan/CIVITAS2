from django.db import models
from MaterialModel.models import MaterialDetail,Recipe
from CityModel.models import *
from CivitasModel.models import Calendar,Terrain
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

#不动产所需物资中间表
class Estate_To_Material(models.Model):
    class Meta:
        verbose_name = "不动产需求物资"
        verbose_name_plural = verbose_name

    estate = models.ForeignKey("Estate_Type",on_delete=models.CASCADE,verbose_name="不动产")
    material = models.ForeignKey(MaterialDetail,on_delete=models.CASCADE,verbose_name="物资")
    count = models.FloatField(verbose_name="数量")

    def __str__(self):
        return "不动产需求物资"

#不动产类型
class Estate_Type(models.Model):
    class Meta:
        verbose_name = "不动产类型"
        verbose_name_plural = verbose_name
    
    #名字
    name = models.CharField("不动产类型名",max_length=20)

    #土地相关
    max_lands = models.FloatField("占地面积")
    allowable_terrain = models.ManyToManyField(Terrain,verbose_name="允许建设的地形",related_name="allow_terrain")
    best_terrain = models.ManyToManyField(Terrain,verbose_name="最适地形",related_name="best_terrain",blank=True)

    #建筑材料
    need_material = models.ManyToManyField(MaterialDetail,verbose_name="建设需要材料",through=Estate_To_Material)

    #是否为原材料建筑
    is_raw_materials = models.BooleanField("是否为原材料建筑")
    list_of_raw_materials = models.ManyToManyField(MaterialDetail,verbose_name="可产原料表",related_name="list_raw_materials",blank=True)

    #是否为加工建筑
    is_machining = models.BooleanField("是否为加工建筑")
    list_of_machining = models.ManyToManyField(Recipe,verbose_name="可产加工品",related_name="list_machining",blank=True)

    number_of_work_person = models.IntegerField("单位面积工作人数",blank=True,null=True)

    #是否为住宅
    is_house = models.BooleanField("是否为住宅")
    number_of_house_person = models.IntegerField("单位面积可居住人数",blank=True,null=True)

    #是否为餐厅
    is_restaurant = models.BooleanField("是否为餐厅")

    #是否使用灌溉值机制
    is_irrigation = models.BooleanField("是否使用灌溉值机制")

    #是否使用肥力值机制
    is_fertility = models.BooleanField("是否使用肥力值机制")

    def __str__(self):
        return self.name
    
    def save(self):
        #验证工作人数
        if (self.is_raw_materials == True or self.is_machining == True) and not self.number_of_work_person:
            raise ValidationError("原料生产建筑或加工建筑需要有工作人数")
        #验证居住人数
        if self.is_house == True and not self.number_of_house_person:
            raise ValidationError("住宅需要有居住人数")
        #验证原料
        if self.is_raw_materials and not self.list_of_raw_materials.exists():
            raise ValidationError("原料生产建筑需要有可生产的原料")
        #验证加工品
        if self.is_machining and not self.list_of_machining.exists():
            raise ValidationError("加工建筑需要有加工配方")
        super().save()

#不动产
class Estate(models.Model):
    class Meta:
        verbose_name = "不动产"
        verbose_name_plural = verbose_name
    
    #名字
    name = models.CharField("不动产名",max_length=20)

    #类型
    type_of = models.ForeignKey(Estate_Type,on_delete=models.CASCADE,verbose_name="类型")

    #状态
    status_choice = (("开垦中", "开垦中"),("建设中", "建设中"),("完成", "完成"))
    status_estate = models.CharField("状态",max_length=20,choices=status_choice,default="开垦中")

    #当前占地
    now_lands = models.FloatField("当前占地",default=0)

    #位于
    location_county = models.ForeignKey(County,on_delete=models.CASCADE,verbose_name="位于县",blank=True,null=True)
    location_suburb = models.ForeignKey(Suburb,on_delete=models.CASCADE,verbose_name="位于郊区",blank=True,null=True)
    location_terrain = models.ForeignKey(Terrain,on_delete=models.CASCADE,verbose_name="位于某地形")
    is_county = models.BooleanField("是否位于县城",editable=False,default=False)
    is_suburb = models.BooleanField("是否位于郊区",editable=False,default=False)

    #产出
    production_materials = models.ForeignKey(MaterialDetail,on_delete=models.CASCADE,verbose_name="产物",editable=False,null=True)
    production_machining = models.ForeignKey(Recipe,on_delete=models.CASCADE,verbose_name="产出配方",editable=False,null=True)

    #归属权
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="使用者",related_name="estate_user")
    owner = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="拥有者",related_name="estate_owner")

    #建立时间
    created_at = models.DateTimeField("建立于",auto_now=True)

    #各种属性
    irrigation = models.FloatField("灌溉值",blank=True,null=True)
    fertility = models.FloatField("肥力值",blank=True,null=True)

    #开垦
    def open_land(self,capacity):
        #不是开垦中返回错误
        if self.status_estate != "开垦中":
            raise ValidationError("不是开垦中的不动产")
        #检查建筑位于县城还是郊区，这步没有必要
        self.check_countyorsuburb()
        #位于县城
        if self.is_county == True:
            #获取县城-地形中间表
            middle_table = County_To_Terrain.objects.filter(county=self.location_county,terrain=self.location_terrain).first()
            #获取开垦难度
            difficulty = self.location_county.terrain_parameter.get(name=self.location_terrain).default_open_difficulty
            #获取剩余土地
            left_lands = middle_table.check_lands()
        #位于郊区
        elif self.is_suburb == True:
            #获取郊区-地形中间表
            middle_table = Suburb_To_Terrain.objects.filter(county=self.location_county,terrain=self.location_terrain).first()
            #获取开垦难度
            difficulty = middle_table.get_difficulty()
            #剩余土地无限
            left_lands = float("inf")
        #计算新开土地数量
        new_lands = capacity / difficulty
        old_lands = self.now_lands
        #如果剩余土地不足，则返回错误
        if left_lands == 0:
            raise ValidationError("土地不足")
        elif left_lands < new_lands:
            new_lands = left_lands
        self.now_lands += new_lands
        #如果开垦完成了，则变更状态
        if self.now_lands >= self.type_of.max_lands:
            new_lands = self.type_of.max_lands - old_lands
            self.now_lands = self.type_of.max_lands
            self.status_estate = "建设中"
        #增加对应的地形已开垦土地数量
        middle_table.count += new_lands
        #保存
        middle_table.save()
        self.save()

    #工作
    def work_estate(self,raw_capacity):
        #不是完成返回错误
        if self.status_estate != "完成":
            raise ValidationError("不动产未完成")
        #验证是否为原料建筑/加工建筑/不是可以工作的建筑
        if self.type_of.is_raw_materials:
            is_raw_materials = True
        elif self.type_of.is_machining:
            is_raw_materials = False
        else:
            raise ValidationError("该不动产不可工作")
        #原料建筑
        if is_raw_materials == True:
            if not self.production_materials:
                raise ValidationError("未设置产物")
            #这边先return，之后要返回到目标库房
            return "产出%s%.2f" % (self.production_materials.__str__(),raw_capacity / self.production_materials.productivity)
        #加工建筑
        elif is_raw_materials == False:
            if not self.production_machining:
                raise ValidationError("未设置加工配方")
            #这边先return，之后要返回到目标库房
            return "还没做好"

    #更改原料产物
    def change_production_materials(self,id,level=1):
        #验证是否为原料建筑
        if not self.type_of.is_raw_materials:
            raise ValidationError("不是生产原料的建筑")
        #查找对应id的物资
        material = Material.objects.filter(pk=id)
        if not material.exists():
            raise ValidationError("没有对应的物资")
        #查找是否能够生产该物资
        raw_materials = self.type_of.list_of_raw_materials.filter(material=material.first(),level=level)
        if not raw_materials.exists():
            raise ValidationError("无法生产该物资，或无法生产该等级的物资")
        self.production_materials = raw_materials.first()
        self.save()

    #更改产出配方
    def change_production_machining(self,id):
        #验证是否为加工建筑
        if not self.type_of.is_machining:
            raise ValidationError("不是加工建筑")
        #查找对应id的配方
        recipe = Recipe.objects.filter(pk=id)
        if not recipe.exists():
            raise ValidationError("没有对应的配方")
        #查找是否能够使用该配方
        machining_recipe = self.type_of.list_of_machining.filter(pk=1)
        if not machining_recipe.exists():
            raise ValidationError("无法使用该配方")
        self.production_machining = machining_recipe.first()
        self.save()

    #检查位于郊区或位于县城
    def check_countyorsuburb(self,is_save=False):
        if not self.location_county and self.location_suburb:
            self.is_county = False
            self.is_suburb = True
        elif not self.location_suburb and self.location_county:
            self.is_county = True
            self.is_suburb = False
        else:
            raise ValidationError("不能既不在县城也不在郊区，或既在县城又在郊区")
        if not is_save:
            self.save()

    def __str__(self):
        return self.name

    def save(self):
        self.check_countyorsuburb(True)
        if self.type_of.is_raw_materials and not self.production_materials:
            self.production_materials = self.type_of.list_of_raw_materials.all()[0]
        super().save()