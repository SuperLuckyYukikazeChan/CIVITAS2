from django.conf import settings
from django.db import models
import math
import random
from django.core.exceptions import ValidationError

#大类技能
class Big_Skill(models.Model):
    class Meta:
        verbose_name = "大类技能"
        verbose_name_plural = verbose_name

    id = models.SmallIntegerField('大类技能id',primary_key=True)
    name = models.CharField('大类技能名称',max_length=20)

    def __str__(self):
        return self.name

#小类技能
class Small_Skill(models.Model):
    class Meta:
        verbose_name = "小类技能"
        verbose_name_plural = verbose_name
        unique_together = [
            'sub','subid'
        ]

    sub = models.ForeignKey(Big_Skill,on_delete=models.CASCADE,verbose_name='所属大类')
    subid = models.SmallIntegerField('大类下的小类id')
    name = models.CharField('小类名称',max_length=20)

    def __str__(self):
        return self.name

#大类技能中间表
class User_Skill_To_Big_Skill(models.Model):
    class Meta:
        verbose_name = "用户大类技能"
        verbose_name_plural = verbose_name
        unique_together = [
            'user_skill','big_skill'
        ]

    level_choices = (
        (1,'学徒'),(2,'匠人'),(3,'匠师'),(4,'专家'),(5,'大师'),(6,'宗师'),(7,'大宗师'),
    )
    user_skill = models.ForeignKey('User_Skill',on_delete=models.CASCADE,verbose_name='用户')
    big_skill = models.ForeignKey(Big_Skill,on_delete=models.CASCADE,verbose_name='大类技能')
    skill_num = models.FloatField('技能点',default=0)
    comprehension = models.FloatField('悟性',default=0)
    level = models.SmallIntegerField('技能等级',choices=level_choices,default=1)

    def __str__(self):
        return self.user_skill.name + "的大类技能" + str(self.id)

#小类技能中间表
class User_Skill_To_Small_Skill(models.Model):
    class Meta:
        verbose_name = "用户小类技能"
        verbose_name_plural = verbose_name
        unique_together = [
            'user_skill','small_skill'
        ]

    user_skill = models.ForeignKey('User_Skill',on_delete=models.CASCADE,verbose_name='用户')
    small_skill = models.ForeignKey(Small_Skill,on_delete=models.CASCADE,verbose_name='小类技能')
    skill_num = models.FloatField('技能点',default=0)

    def __str__(self):
        return self.user_skill.name + "的小类技能" + str(self.id)

#技能管理器
class Skill_Manager(models.Manager):
    def create(self, name, *args, **kwargs):
        #创建新的技能表
        skill = super().create(name=name, *args, **kwargs)
        #获取所有的技能
        all_bs = Big_Skill.objects.all()
        all_ss = Small_Skill.objects.all()
        #添加所有的技能
        for x in all_bs:
            skill.big_skill.add(x)
        for x in all_ss:
            skill.small_skill.add(x)
        skill.save()
        return skill

#技能表
class User_Skill(models.Model):
    class Meta:
        verbose_name = "技能表"
        verbose_name_plural = verbose_name
    
    name = models.CharField("名称",max_length=30)
    type_choices = (('用户','用户'),('NPC','NPC'))
    type_of = models.CharField('类型',max_length=20,choices=type_choices,default='用户')
    big_skill = models.ManyToManyField(Big_Skill,related_name='big_skill',verbose_name='大类技能',through=User_Skill_To_Big_Skill)
    small_skill = models.ManyToManyField(Small_Skill,related_name='small_skill',verbose_name='小类技能',through=User_Skill_To_Small_Skill)

    #自定义管理器
    objects = Skill_Manager()

    #增加技能
    def skill_increase(self,skill_id,skill_mini_id=None,type_buff=1,strategy_buff=1,is_education=False):
        from UserModel.models import User_Table
        #查询对应id的技能
        try:
            skill_name = Big_Skill.objects.get(pk=skill_id)
            skill = User_Skill_To_Big_Skill.objects.get_or_create(user_skill=self,big_skill=skill_name)[0]
        except:
            raise ValidationError("没有找到对应id的技能")
        #技能增长e^(-技能等级/4)
        change = math.exp(-skill.skill_num / 4)
        #进门槛降低技能增长速度
        if math.floor((skill.skill_num / 4) + 1) > skill.level and skill.skill_num < 28:
            diff = skill.skill_num - skill.level * 4
            change *= (1 - math.sqrt(diff))
        #快乐修正，20快乐---10%增长速度
        try:
            user = User_Table.objects.get(skill=self)
        except:
            raise ValidationError("该技能表没有对应的用户")
        change *= (1 + ((user.happiness - 60) / 200))
        #类型修正
        change *= type_buff
        #工作策略修正
        change *= strategy_buff
        #悟性修正，满悟性提供20%增长速度
        change *= 1 + skill.comprehension / 5
        skill.skill_num += change

        #如果提供了小类技能id，则增加小类技能
        if skill_mini_id:
            #查询对应id的技能
            try:
                skill_mini_name = Small_Skill.objects.get(subid=skill_mini_id,sub=skill_id)
                skill_mini = User_Skill_To_Small_Skill.objects.get_or_create(user_skill=self,small_skill=skill_mini_name)[0]
            except:
                raise ValidationError("没有找到对应id的小类技能")
            #基础增长3%
            change_mini = 0.03
            #当前技能每高12点，则增长速度翻一倍
            change_mini *= 1 + (skill.skill_num / 12)
            #当前小类技能越高，增长越慢，达到100%时增长速度减半
            change_mini *= 1 - (skill_mini.skill_num / 2)
            #快乐修正，20快乐-10%增长速度
            change_mini *= (1 + ((user.happiness - 60) / 200))
            #类型修正
            change_mini *= type_buff
            #工作策略修正
            change_mini *= strategy_buff
            #不超限
            change_mini = min(change_mini,1 - skill_mini.skill_num)
            skill_mini.skill_num += change_mini

        #如果为教育，则增加悟性
        if is_education:
            #增加0.1+当前技能/100
            change_comprehension = 0.1 + skill.skill_num / 100
            #不超限
            change_comprehension = min(change_comprehension,1 - skill.comprehension)
            skill.comprehension += change_comprehension

        #保存
        skill.save()
        skill_mini.save()

    #计算是否突破
    def eureka(self,skill_id):
        #查询对应id的技能
        try:
            skill_name = Big_Skill.objects.get(pk=skill_id)
            skill = User_Skill_To_Big_Skill.objects.get_or_create(user_skill=self,big_skill=skill_name)[0]
        except:
            raise ValidationError("没有找到对应id的技能")
        chance = self.eureka_chance(skill_id)
        num = random.random()
        if num < chance:
            skill.level += 1
            skill.save()
    
    #计算突破概率
    def eureka_chance(self,skill_id):
        #查询对应id的技能
        try:
            skill_name = Big_Skill.objects.get(pk=skill_id)
            skill = User_Skill_To_Big_Skill.objects.get_or_create(user_skill=self,big_skill=skill_name)[0]
        except:
            raise ValidationError("没有找到对应id的技能")
        #不在门槛内，不会突破
        if not (math.floor((skill.skill_num / 4) + 1) > skill.level and skill.level < 7):
            return 0
        #基础突破概率50%
        eureka_0 = 0.5
        #与门槛基础差值提高基础概率，最高为3倍
        diff = skill.skill_num - skill.level * 4
        eureka_really = eureka_0 * (1 + diff * 2)
        #悟性提高突破概率，最高为2倍
        eureka_really *= skill.comprehension + 1
        #实际突破概率，每高一级等级就降低一半，并且不能超过100%
        eureka_really *= 1 / (2 ** skill.level)
        eureka_really = min(1,eureka_really)
        return eureka_really

    #计算产能
    def capacity_calculation(self,skill_id,skill_mini_id=None,type_buff=1,strategy_buff=1):
        from UserModel.models import User_Table
        #查询对应id的技能
        try:
            skill_name = Big_Skill.objects.get(pk=skill_id)
            skill = User_Skill_To_Big_Skill.objects.get_or_create(user_skill=self,big_skill=skill_name)[0]
        except:
            raise ValidationError("没有找到对应id的技能")
        #如果提供了小类技能id，则查询小类技能
        if skill_mini_id:
            #查询对应id的技能
            try:
                skill_mini_name = Small_Skill.objects.get(subid=skill_mini_id,sub=skill_id)
                skill_mini = User_Skill_To_Small_Skill.objects.get_or_create(user_skill=self,small_skill=skill_mini_name)[0]
            except:
                raise ValidationError("没有找到对应id的小类技能")
        else:
            class sm:
                pass
            skill_mini = sm()
            skill_mini.skill_num = 0
        #查找用户
        try:
            user = User_Table.objects.get(skill=self)
        except:
            raise ValidationError("该技能表没有对应的用户")
        #基础产能：8+(大类技能/2)^0.85次方*(1+小类技能/2)，即小类技能最高加成为50%
        capacity = 8 + (skill.skill_num / 2) ** 0.85 * (1 + skill_mini.skill_num / 2)
        #类型修正
        capacity *= type_buff
        #快乐修正，20快乐--10%增长速度
        capacity *= (1 + ((user.happiness - 60) / 200))
        #工作策略修正
        capacity *= strategy_buff
        return capacity

    #换日技能、悟性衰减，突破
    def day_change(self):
        skill_big = User_Skill_To_Big_Skill.objects.filter(userskill=self)
        skill_mini = User_Skill_To_Small_Skill.objects.filter(userskill=self)
        for sm in skill_mini:
            #基础衰减2%+原小类的8%
            change = 0.02 + 0.08 * sm.skill_num
            #当前技能每高12点，衰减减慢一半
            change *= (1 / 2) ** (sm.skill_num / 12)
            #不能超限
            change = min(change,sm.skill_num)
            sm.skill_num -= change
            sm.save()
        for sb in skill_big:
            #突破
            self.eureka(sb.bigskill.id)
            #减少0.05+当前悟性*0.2
            change = 0.05 + sb.comprehension * 0.2
            #不能超限
            change = min(change,sb.comprehension)
            sb.comprehension -= change
            sb.save()

    def __str__(self):
        return self.name + "的技能表"

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            print("用户技能不合法： %s" % e.message_dict)