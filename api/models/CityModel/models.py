from django.db import models
import random
from MaterialModel.models import Material,MaterialDetail
from CivitasModel.models import Calendar,Terrain

class Climate(models.Model):
    class Meta:
        verbose_name = "气候"
        verbose_name_plural = verbose_name
    
    #名字
    name = models.CharField("气候名",max_length=20)

    #各个季节下雨概率
    rain_chance_spring = models.FloatField("春天下雨概率")
    rain_chance_summer = models.FloatField("夏天下雨概率")
    rain_chance_autumn = models.FloatField("秋天下雨概率")
    rain_chance_winter = models.FloatField("冬天下雨概率")

    #各个季节下雨量修正
    rain_season_buff_spring = models.FloatField("春天下雨量修正")
    rain_season_buff_summer = models.FloatField("夏天下雨量修正")
    rain_season_buff_autumn = models.FloatField("秋天下雨量修正")
    rain_season_buff_winter = models.FloatField("冬天下雨量修正")

    #原始下雨天数
    raw_rain_days = models.IntegerField("原始下雨天数")

    def __str__(self):
        return self.name

class City(models.Model):
    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    #名字
    name = models.CharField("城市名",max_length=20)

    #日历
    calendar = models.ForeignKey(Calendar,on_delete=models.CASCADE,verbose_name="日历")

    #以下为天气参数
    average_temperature = models.FloatField("平均温度")
    temperature_difference = models.FloatField("温差，最低月平均温度与最高月平均温度之差")
    average_annual_precipitation = models.FloatField("平均年降水量")
    average_annual_precipitation_days = models.FloatField("平均年降水日数")
    average_annual_sunshine_hours = models.FloatField("平均年日照时数")
    #气候
    climate = models.ForeignKey(Climate,on_delete=models.CASCADE,verbose_name="气候")

    #以下为天气数据
    weather_choice = (
        ("晴", "晴"),("多云", "多云"),("阴", "阴"),("小雨", "小雨"),
        ("小雪", "小雪"),("大雨", "大雨"),("大雪", "大雪"),
    )
    weather = models.CharField("当前天气",max_length=20,choices=weather_choice,default="晴")
    temperature = models.FloatField("当前气温")
    precipitation = models.FloatField("当前降水量")
    is_rain = models.BooleanField("是否正在下雨",editable=False)

    #以下为农业相关参数
    min_irrigation_default = models.IntegerField("最小灌溉值")
    average_irrigation_default = models.IntegerField("平均灌溉值")
    max_irrigation_default = models.IntegerField("最大灌溉值")
    raw_fertility_default = models.IntegerField("默认肥力值")
    is_flooding = models.BooleanField("是否会泛滥")
    flooding = models.BooleanField("是否正在泛滥",editable=False,default=False)
    flooding_fertility_default = models.IntegerField("泛滥肥力值",blank=True,null=True)
    flooding_season_choice = (("1", "春"),("2", "夏"),("3", "秋"),("4", "冬"))
    flooding_season = models.CharField("泛滥季节",max_length=20,choices=flooding_season_choice,blank=True,null=True)

    #以下为农业相关数据
    irrigation_default = models.FloatField("当前默认灌溉值")
    fertility_default = models.FloatField("当前默认肥力值")

    #以下为特产相关
    list_of_producible_materials = models.ManyToManyField(Material,verbose_name="可产物品表",related_name="producible_materials")
    list_of_special_materials = models.ManyToManyField(Material,verbose_name="特产表",related_name="special_materials",blank=True)

    #建立时间
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    #换日天气部分
    def day_change_weather(self):
        #####################################################################################
        #基本参数运算
        #年份长度，一般不要变
        year_length = 80
        season_length = year_length / 4
        #定义气温最高/最低阈值
        max_threshold = self.average_temperature + self.temperature_difference
        min_threshold = self.average_temperature - self.temperature_difference
        #定义夏/冬均温
        average_summer = self.average_temperature + self.temperature_difference / 2
        average_winter = self.average_temperature - self.temperature_difference / 2
        average_summer_winter_difference = average_summer - average_winter
        #初始化天气参数
        average_rain_num = self.average_annual_precipitation / self.average_annual_precipitation_days

        #各个季节下雨量和概率
        rain_chance_list = [self.climate.rain_chance_spring,self.climate.rain_chance_summer,self.climate.rain_chance_autumn,self.climate.rain_chance_winter]
        rain_season_buff_list = [self.climate.rain_season_buff_spring,self.climate.rain_season_buff_summer,self.climate.rain_season_buff_autumn,self.climate.rain_season_buff_winter]
        raw_rain_days = self.climate.raw_rain_days
        #真实降水概率，根据降水日数进行修正
        for i,x in enumerate(rain_chance_list):
            rain_chance_list[i] = x * self.average_annual_precipitation_days / raw_rain_days

        #根据日照时数，进行晴/多云/阴概率修正
        #天文日照时数，取4500
        max_sunlight_hour = 4500
        #去掉下雨日数
        no_rain_sunlight_hour = max_sunlight_hour * (1 - self.average_annual_precipitation_days / 365)
        #减去日照数，即为多云，阴天小时数
        cloudy_overcast_hour = no_rain_sunlight_hour - self.average_annual_sunshine_hours
        #晴天概率
        sunny_chance = self.average_annual_sunshine_hours / no_rain_sunlight_hour
        #多云概率
        cloudy_chance = (1 - sunny_chance) * 1 / 3
        #阴天概率
        overcast_chance = (1 - sunny_chance) * 2 / 3

        #####################################################################################
        #以下获取当前日期，季节
        season = int(self.calendar.season)
        day = self.calendar.day

        #####################################################################################
        #以下为气温变化部分
        #气温变化为正负3
        temperature_change_value = random.uniform(-3,3)
        #设置目标温度，冬夏季比均温稍高/低，春秋季则线性变化
        if season == 1 :
            target_temperature = average_winter + average_summer_winter_difference * day / season_length
        elif season == 2:
            if day <= season_length / 2:
                target_temperature = average_summer * (day/(season_length/20) + 100) / 100
            else:
                target_temperature = average_summer * (120 - day/(season_length/20)) / 100
        elif season == 3:
            target_temperature = average_summer - average_summer_winter_difference * day / season_length
        elif season == 4:
            if self.temperature < 0:
                if day <= season_length / 2:
                    target_temperature = average_winter * (day/(season_length/20) + 100) / 100
                else:
                    target_temperature = average_winter * (120 - day/(season_length/20)) / 100
            else:
                if day <= season_length / 2:
                    target_temperature = average_winter * (100 - day/(season_length/20)) / 100
                else:
                    target_temperature = average_winter * (day/(season_length/20) + 80) / 100
        #低于目标温度，修正气温变化量，最高为低于15度——增加变化量3
        if self.temperature < target_temperature:
            dif = target_temperature - self.temperature
            if dif < 15:
                temperature_change_value += dif / 5
            else:
                temperature_change_value += 3
        #高于目标温度，修正气温变化量，最高为高于15度——减少变化量3
        if self.temperature > target_temperature:
            dif = self.temperature - target_temperature
            if dif < 15:
                temperature_change_value -= dif / 5
            else:
                temperature_change_value -= 3
        #第二天气温如超过气温阈值，修改气温变化量，第二天气温不超过阈值
        if self.temperature + temperature_change_value > max_threshold:
            temperature_change_value = max_threshold - self.temperature
        if self.temperature + temperature_change_value < min_threshold:
            temperature_change_value = min_threshold - self.temperature
        #修改温度
        self.temperature += temperature_change_value
    
        #####################################################################################
        #以下为降水变化部分
        #读取基础下雨概率，季节修正
        rain_chance = rain_chance_list[season - 1]
        rain_season_buff = rain_season_buff_list[season - 1]
        #根据前一天天气调整下雨概率
        #晴天
        if self.weather == "晴":
            rain_yesterday = False
            rain_num_yesterday = 0
            rain_chance *= 0.4
        #多云
        elif self.weather == "多云":
            rain_yesterday = False
            rain_num_yesterday = 0
            rain_chance *= 0.8
        #阴
        elif self.weather == "阴":
            rain_yesterday = False
            rain_num_yesterday = 0
            rain_chance *= 1
        #小雨，小雪
        elif self.weather == "小雨" or self.weather == "小雪":
            rain_yesterday = True
            rain_num_yesterday = self.rain_num
            rain_chance *= 1.4
        #大雨，大雪
        elif self.weather == "大雨" or self.weather == "大雪":
            rain_yesterday = True
            rain_num_yesterday = self.rain_num
            rain_chance *= 1.8
        #超过0.9则改为0.9
        if rain_chance > 0.9:
            rain_chance = 0.9
        #判定是否下雨
        if random.random() < rain_chance:
            self.rain = True
        else:
            self.rain = False
        #判定降水量
        if self.rain == True:
            #刚开始下雨，随机生成雨量(平均降水量的1/3-2倍)
            if rain_yesterday == False:
                rain_highorlow = random.randint(0,1)
                rain_new_buff = random.uniform(1,3)
                #小于平均
                if rain_highorlow == 0:
                    self.rain_num = average_rain_num * rain_season_buff / rain_new_buff
                #大于平均
                elif rain_highorlow == 1:
                    self.rain_num = average_rain_num * rain_season_buff * (rain_new_buff / 3 * 2)
            #前一天有下雨，根据前一天雨量增加/减少
            elif rain_yesterday == True:
                self.rain_num = rain_num_yesterday * random.uniform(0.5,1.5)
        #没下雨
        else:
            self.rain_num = 0

        #####################################################################################
        #以下为天气变化部分
        #没下雨
        if self.rain_num == 0:
            #晴天
            if self.weather == "晴":
                sunny_chance = sunny_chance * 2
                cloundy_chance = cloudy_chance
                overcast_chance = overcast_chance
                weather_random = random.uniform(0,sunny_chance + cloundy_chance + overcast_chance)
                if weather_random <= sunny_chance:
                    self.weather = "晴"
                elif weather_random <= sunny_chance + cloundy_chance:
                    self.weather = "多云"
                elif weather_random <= sunny_chance + cloundy_chance + overcast_chance:
                    self.weather = "阴"
            #多云
            elif self.weather == "多云":
                sunny_chance = sunny_chance
                cloundy_chance = cloudy_chance * 6
                overcast_chance = overcast_chance * 3
                weather_random = random.uniform(0,sunny_chance + cloundy_chance + overcast_chance)
                if weather_random <= sunny_chance:
                    self.weather = "晴"
                elif weather_random <= sunny_chance + cloundy_chance:
                    self.weather = "多云"
                elif weather_random <= sunny_chance + cloundy_chance + overcast_chance:
                    self.weather = "阴"
            #阴
            elif self.weather == "阴":
                sunny_chance = sunny_chance
                cloundy_chance = cloudy_chance * 3
                overcast_chance = overcast_chance * 6
                weather_random = random.uniform(0,sunny_chance + cloundy_chance + overcast_chance)
                if weather_random <= sunny_chance:
                    self.weather = "晴"
                elif weather_random <= sunny_chance + cloundy_chance:
                    self.weather = "多云"
                elif weather_random <= sunny_chance + cloundy_chance + overcast_chance:
                    self.weather = "阴"
            #从雨天转没雨
            else:
                sunny_chance = sunny_chance
                cloundy_chance = cloudy_chance * 6
                overcast_chance = overcast_chance * 6
                weather_random = random.uniform(0,sunny_chance + cloundy_chance + overcast_chance)
                if weather_random <= sunny_chance:
                    self.weather = "晴"
                elif weather_random <= sunny_chance + cloundy_chance:
                    self.weather = "多云"
                elif weather_random <= sunny_chance + cloundy_chance + overcast_chance:
                    self.weather = "阴"
        else:
            #小雨，小雪
            if self.rain_num <= 10:
                self.weather = "小雨"
            #大雨，大雪
            elif self.rain_num > 10:
                self.weather = "大雨"
            #验证雨雪
            if self.temperature <= 0:
                self.weather = self.weather.replace('雨','雪')
            elif self.temperature > 0:
                self.weather = self.weather.replace('雪','雨')

        #####################################################################################
        #天气影响温度
        if self.weather == "晴":
            self.temperature += 1.5
        elif self.weather == "多云":
            self.temperature += 0.5
        elif self.weather == "阴":
            self.temperature -= 0.5
        elif self.weather == "小雨":
            self.temperature -= 1
        elif self.weather == "小雪":
            self.temperature -= 2
        elif self.weather == "大雨":
            self.temperature -= 1.5
        elif self.weather == "大雪":
            self.temperature -= 3

        #####################################################################################
        #默认灌溉值变化
        if season == 1 and day == 1:
            self.irrigation_default = random.uniform(self.average_irrigation_default*0.9,self.average_irrigation_default*1.1)
        elif season == 2 and day == 1:
            self.irrigation_default = random.uniform(self.max_irrigation_default*0.9,self.max_irrigation_default*1.1)
        elif season == 3 and day == 1:
            self.irrigation_default = random.uniform(self.average_irrigation_default*0.9,self.average_irrigation_default*1.1)
        elif season == 4 and day == 1:
            self.irrigation_default = random.uniform(self.min_irrigation_default*0.9,self.min_irrigation_default*1.1)

        #####################################################################################
        #默认肥力值变化，只有会泛滥的城市才变化
        if self.is_flooding == False:
            pass
        else:
            if season == int(self.flooding_season) and day == 1:
                self.fertility_default = random.uniform(self.flooding_fertility_default*0.9,self.flooding_fertility_default*1.1)
                #不能超过100
                if self.fertility_default > 100:
                    self.fertility_default = 100
                self.flooding = True
            elif season == int(self.flooding_season) + 1 and day == 1:
                self.fertility_default = self.raw_fertility_default
                self.flooding = False
        
        #保存
        self.save()
    
    #获取城市基本信息
    def get_info(self):
        pass

    #获取城市天气
    def get_weather(self):
        pass

    #保存方法重写，加入验证
    def save(self):
        if self.precipitation == 0:
            self.is_rain = False
        else:
            self.is_rain = True
        super().save(self)

#开垦难度参数
class Open_Difficulty_Parameter(models.Model):
    class Meta:
        verbose_name = "开垦难度参数"
        verbose_name_plural = verbose_name

    #定义翻倍系数
    double_parameter = models.IntegerField("基准难度翻倍参数",default=200)

    def __str__(self):
        return "开垦难度参数" + str(self.id)

#抽象的县/郊区-地形中间表
class CorS_To_Terrain(models.Model):
    class Meta:
        abstract = True

#县-地形中间表
class County_To_Terrain(models.Model):
    class Meta:
        verbose_name = "县-地形中间表"
        verbose_name_plural = verbose_name

    county = models.ForeignKey("County",on_delete=models.CASCADE,verbose_name="关联县")
    terrain = models.ForeignKey(Terrain,on_delete=models.CASCADE,verbose_name="地形")
    count = models.FloatField("%s已开垦土地数量" % terrain.name)
    open_lands_max = models.FloatField("%s土地总量" % terrain.name)

    #检查土地是否溢出
    def check_lands(self):
        if self.count <= self.open_lands_max:
            return self.open_lands_max - self.count
        else:
            return 0
    
    def __str__(self):
        return self.county.name + "的" + self.terrain.name

#郊区-地形中间表
class Suburb_To_Terrain(models.Model):
    class Meta:
        verbose_name = "郊区-地形中间表"
        verbose_name_plural = verbose_name

    county = models.ForeignKey("Suburb",on_delete=models.CASCADE,verbose_name="关联郊区")
    terrain = models.ForeignKey(Terrain,on_delete=models.CASCADE,verbose_name="地形")
    count = models.FloatField("%s已开垦土地数量" % terrain.name)
    land_parameter = models.IntegerField("%s土地参数，如为-1则代表该郊区没有该类型土地，参数均除以100后使用（方便两位小数），\
        100参数代表每开垦1个基准难度翻倍参数时开垦难度翻倍，200参数代表每开垦1/2个基准难度翻倍参数时开垦难度翻倍（翻倍更快，开垦更难），下同" % terrain.name,default=-1)

    #获取开垦难度
    def get_difficulty(self):
        return self.count / (self.county.open_difficulty_parameter.double_parameter / (self.land_parameter / 100)) * self.terrain.default_open_difficulty

    def __str__(self):
        return self.county.name + "的" + self.terrain.name
        
#抽象的县模型，用于被首县，郊区，郊县继承
class Abstract_County(models.Model):
    class Meta:
        abstract = True

    #名字
    name = models.CharField("县/郊区名",max_length=20)

    #三个值：繁荣，治理，产业
    prosperity_value = models.IntegerField("繁荣值")
    governance_value = models.IntegerField("治理值")
    industrial_value = models.IntegerField("产业值")

    #关联基准开垦难度参数
    open_difficulty_parameter = models.ForeignKey(Open_Difficulty_Parameter,on_delete=models.CASCADE,verbose_name="开垦难度参数")

    #属于某个城市
    belong_city = models.ForeignKey(City,on_delete=models.CASCADE,verbose_name="属于城市")

    #建立时间
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

#县城
class County(Abstract_County):
    class Meta:
        verbose_name = "县"
        verbose_name_plural = verbose_name

    #地形参数
    terrain_parameter = models.ManyToManyField(Terrain,verbose_name="地形表",through=County_To_Terrain)

    #特产表
    list_of_special_materials_county = models.ManyToManyField(MaterialDetail,verbose_name="特产表",related_name="special_materials_county",blank=True)

    #更新开垦难度
    def updata_difficulty(self):
        self.save()

#郊区
class Suburb(Abstract_County):
    class Meta:
        verbose_name = "郊区"
        verbose_name_plural = verbose_name

    #地形参数
    terrain_parameter = models.ManyToManyField(Terrain,verbose_name="地形表",through=Suburb_To_Terrain)

    #更新开垦难度
    def updata_difficulty(self):
        self.save()

#城市间道路
class City_Road(models.Model):
    class Meta:
        verbose_name = "城与城道路"
        verbose_name_plural = verbose_name

    city1 = models.ForeignKey(City,on_delete=models.CASCADE,verbose_name="城市1",related_name="city1")
    city2 = models.ForeignKey(City,on_delete=models.CASCADE,verbose_name="城市2",related_name="city2")
    distance = models.IntegerField("距离")
    terrain_choice = (("平原", "平原"),("丘陵", "丘陵"),("山地", "山地"),("淡水", "淡水"),("咸水", "咸水"))
    terrain = models.CharField("地形",max_length=20,choices=terrain_choice,default="平原")

    def __str__(self):
        return "%s到%s的%s路" % (self.city1.name,self.city2.name,self.terrain)