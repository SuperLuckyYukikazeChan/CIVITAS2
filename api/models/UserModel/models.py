from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser,UserManager
from django.core.exceptions import ValidationError
from EstateModel.models import Estate
from CityModel.models import City
from DepositoryModel.models import Depository
import SkillModel.models as SM
from django.db.models import F

def validate_attributes(value):
    value = float(value)
    if value < 0 or value > 100:
        raise ValidationError("属性值不合法，需要在0-100之间，当前值：%s" % value)

class User_Manager(UserManager):
    def create_user(self,username,password,email,city_id):
        #创建技能表，库房
        us = SM.User_Skill.objects.create(name=username)
        ud = Depository.objects.create(name=f"{username}的库房",type_of="个人")
        #查找注册城市
        try:
            city = City.objects.get(pk=city_id)
        except:
            raise ValidationError("没有找到对应的城市")
        #创建新的用户对象
        return super().create_user(username=username,password=password,email=email,skill=us,depository=ud,location=city)

class User_Table(AbstractUser):
    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def avatar_path(self, instance, filename):
        filename = str(instance.user.id) + '.jpg'
        return "avatar/{0}".format(filename)

    #个人信息
    nick_name = models.CharField("昵称",max_length=20,blank=True,null=True)
    #avatar = models.ImageField("头像",upload_to=avatar/)
    user_sessionid = models.CharField("sessionid",max_length=32,blank=True,null=True)

    #个人属性
    stamina = models.FloatField("精力",default=100,validators=[validate_attributes])
    health = models.FloatField("健康",default=100,validators=[validate_attributes])
    happiness = models.FloatField("快乐",default=100,validators=[validate_attributes])
    starvation = models.FloatField("饥饿",default=100,validators=[validate_attributes])

    #工作相关
    had_work = models.BooleanField("是否已经工作过了",default=False)
    work_at = models.ForeignKey(Estate,on_delete=models.CASCADE,verbose_name="工作于",related_name="work_at",blank=True,null=True)

    #位置相关
    location = models.ForeignKey(City,on_delete=models.CASCADE,verbose_name="位于城市",blank=True,null=True)
    stay_at = models.ForeignKey(Estate,on_delete=models.CASCADE,verbose_name="居住于",related_name="stay_at",blank=True,null=True)

    #库房相关
    depository = models.ForeignKey(Depository,on_delete=models.CASCADE,verbose_name="拥有库房",blank=True,null=True)

    #技能相关
    skill = models.ForeignKey(SM.User_Skill,on_delete=models.CASCADE,verbose_name="技能表",blank=True,null=True)

    #自定义管理器
    objects = User_Manager()

    #四维变化
    def stamina_change(self,change):
        self.stamina = F("stamina") + change
        self.save()

    def health_change(self,change):
        self.health = F("health") + change
        self.save()

    def happiness_change(self,change):
        self.happiness = F("happiness") + change
        self.save()

    def starvation_change(self,change):
        self.starvation = F("starvation") + change
        self.save()
        
    #换日
    def day_change(self):
        #目前所有人都睡大街
        house_type = 0
        house_level = 0
        #睡大街
        if house_type == 0:
            stamina_house_bonus = 0
            happiness_house_bonus = 0
            health_house_bonus = 0
        #楼房
        if house_type == 1:
            stamina_house_bonus = 10 * house_level
            happiness_house_bonus = 0.4 * (house_level - 1)
            health_house_bonus = 0.4 * (house_level - 1)
        #宅院
        if house_type == 2:
            stamina_house_bonus = 10 * house_level
            happiness_house_bonus = 0.2 + 0.6 * (house_level - 1)
            health_house_bonus = 0.2 + 0.6 * (house_level - 1)

        #计算属性回复
        stamina_change = (30 + stamina_house_bonus) * (1 + ((self.health - 60) / 80))
        happiness_change = 3 + 0.2 * (min(60,self.starvation,self.health) - self.happiness) + 0.05 * (max(0,self.stamina + stamina_change - 100)) + happiness_house_bonus
        health_change = 3 + 0.2 * (min(60,self.starvation,self.stamina + 40) - self.health) + 0.05 * (max(0,self.stamina + stamina_change - 100)) + health_house_bonus
        starvation_change = -(0.08 * self.starvation + 2)
        really_stamina_change = stamina_change
        really_happiness_change = happiness_change
        really_health_change = health_change
        really_starvation_change = starvation_change

        #处理超界
        if self.stamina + stamina_change > 100:
            really_stamina_change = 100 - self.stamina
        elif self.stamina + stamina_change < 0:
            really_stamina_change = -self.stamina
        if self.happiness + happiness_change > 100:
            really_happiness_change = 100 - self.happiness
        elif self.happiness + happiness_change < 0:
            really_happiness_change = -self.happiness
        if self.health + health_change > 100:
            really_health_change = 100 - self.health
        elif self.health + health_change < 0:
            really_health_change = -self.health
        if self.starvation + starvation_change > 100:
            really_starvation_change = 100 - self.starvation
        elif self.starvation + starvation_change < 0:
            really_starvation_change = -self.starvation
        self.stamina += really_stamina_change
        self.happiness += really_happiness_change
        self.health += really_health_change
        self.starvation += really_starvation_change

        #工作状态恢复
        self.had_work = False

        self.save()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            print("用户表不合法： %s" % e.message_dict)

class Avatar(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        primary_key=True,
    )
    avatar = models.ImageField(
        verbose_name="头像"
    )
    def __str__(self):
        return self.name