# Generated by Django 3.2.5 on 2021-10-02 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SocialContactModel', '0002_auto_20211002_1818'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='social_behavior',
            name='type',
        ),
        migrations.AddField(
            model_name='social_behavior',
            name='type_of_behavior',
            field=models.CharField(choices=[('公开赞扬', '公开赞扬'), ('公开谴责', '公开谴责'), ('私下表扬', '私下表扬'), ('私下批评', '私下批评'), ('赠送礼物', '赠送礼物')], default='公开赞扬', max_length=20),
        ),
    ]
