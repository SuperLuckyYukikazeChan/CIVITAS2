from django.db import models
from django.conf import settings
from django.db.models import Q

class Friend_Manger(models.Manager):
    #是否为好友
    def is_friend(self, person1, person2):
        is_friend = self.filter(
            (Q(from_person = person1) | Q(to_person = person2)) & 
            (Q(from_person = person2) | Q(to_person = person1))
        )
        if is_friend.exists():
            return True
        else:
            return False

class Friend(models.Model):
    from_person = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name='发起者',related_name='friend_from_person')
    to_person = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name='接收者',related_name='friend_to_person')
    relationship_value = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    objects = Friend_Manger()

    def __str__(self):
        return str(self.relationship_value)

class Social_behavior(models.Model):
    from_person = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name='发起者',related_name='social_behavior_from_person')
    to_person = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name='接收者',related_name='social_behavior_to_person')
    relationship_value_change = models.IntegerField()
    type_choice = (
        ("公开赞扬", "公开赞扬"),
        ("公开谴责", "公开谴责"),
        ("私下表扬", "私下表扬"),
        ("私下批评", "私下批评"),
        ("赠送礼物", "赠送礼物"),
    )
    type_of_behavior = models.CharField(
        max_length=20,
        choices=type_choice,
        default="公开赞扬",
    )
    date = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=100)
    def __str__(self):
        return self.from_person.username + self.type_of_behavior + "了" + self.to_person.username