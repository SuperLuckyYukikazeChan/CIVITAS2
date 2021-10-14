# Generated by Django 3.2.5 on 2021-10-12 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BlogModel', '0004_alter_blog_author'),
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('MaterialModel', '0017_auto_20210813_2354'),
        ('SkillModel', '0002_auto_20210817_2005'),
        ('DietModel', '0003_alter_diet_recipe_taste_description'),
        ('SocialContactModel', '0004_social_behavior_message'),
        ('SpeechModel', '0006_speech_speechattitude_topic'),
        ('UserModel', '0003_other_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='other_user',
        ),
    ]
