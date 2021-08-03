# Generated by Django 3.2.5 on 2021-08-02 22:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('SkillModel', '0002_auto_20210802_1241'),
    ]

    operations = [
        migrations.CreateModel(
            name='building',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='auth.user')),
                ('skill_num', models.FloatField(default=0)),
                ('building', models.FloatField(default=0)),
                ('mending', models.FloatField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='cutting',
            name='skill_num',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='farming',
            name='skill_num',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='husbandry',
            name='skill_num',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='processing',
            name='skill_num',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='social',
            name='skill_num',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='skill_num',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='cutting',
            name='collection',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='cutting',
            name='exploitation',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='cutting',
            name='lumbering',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='cutting',
            name='prospecting',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='farming',
            name='cash_crops',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='farming',
            name='grain',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='farming',
            name='reclaim',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='farming',
            name='vegetables_fruit',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='husbandry',
            name='fowl',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='husbandry',
            name='hunt',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='husbandry',
            name='livestock',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='processing',
            name='food_processing',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='processing',
            name='forge',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='processing',
            name='smelt',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='processing',
            name='spin',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='processing',
            name='wood_stone_processing',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='social',
            name='communicate',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='social',
            name='eloquence',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='social',
            name='manage',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='social',
            name='write',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='fishing',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='land_transport',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='water_transport',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='userskill',
            name='building',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='SkillModel.building'),
            preserve_default=False,
        ),
    ]
