from django.db import models

class Calendar(models.Model):
    class Meta:
        verbose_name = "日历"
        verbose_name_plural = verbose_name
    
    total_day = models.IntegerField("总计日期")
    year = models.IntegerField("年份")
    season_choice = (("1", "春"),("2", "夏"),("3", "秋"),("4", "冬"))
    season = models.CharField("季节",max_length=20,choices=season_choice,default="1")
    day = models.IntegerField("当前日期")

    def get_date(self):
        return {
            "total_day":self.total_day,
            "year":self.year,
            "season":self.season,
            "day":self.day,
        }

    def __str__(self):
        return "日历" + str(self.id)