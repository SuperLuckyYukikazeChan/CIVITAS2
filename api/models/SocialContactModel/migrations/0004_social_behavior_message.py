# Generated by Django 3.2.5 on 2021-10-02 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SocialContactModel', '0003_auto_20211002_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='social_behavior',
            name='message',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
