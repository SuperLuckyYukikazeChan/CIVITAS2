# Generated by Django 3.2.5 on 2021-08-03 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('SkillModel', '0011_auto_20210803_0931'),
    ]

    operations = [
        migrations.CreateModel(
            name='construct',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='auth.user')),
                ('skill_num', models.FloatField(default=0)),
                ('building', models.FloatField(default=0)),
                ('mending', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='cutting',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='auth.user')),
                ('skill_num', models.FloatField(default=0)),
                ('collection', models.FloatField(default=0)),
                ('lumbering', models.FloatField(default=0)),
                ('exploitation', models.FloatField(default=0)),
                ('prospecting', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='farming',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='auth.user')),
                ('skill_num', models.FloatField(default=0)),
                ('grain', models.FloatField(default=0)),
                ('vegetables_fruit', models.FloatField(default=0)),
                ('cash_crops', models.FloatField(default=0)),
                ('reclaim', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='husbandry',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='auth.user')),
                ('skill_num', models.FloatField(default=0)),
                ('hunt', models.FloatField(default=0)),
                ('fowl', models.FloatField(default=0)),
                ('livestock', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='processing',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='auth.user')),
                ('skill_num', models.FloatField(default=0)),
                ('smelt', models.FloatField(default=0)),
                ('forge', models.FloatField(default=0)),
                ('spin', models.FloatField(default=0)),
                ('food_processing', models.FloatField(default=0)),
                ('wood_stone_processing', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='social',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='auth.user')),
                ('skill_num', models.FloatField(default=0)),
                ('eloquence', models.FloatField(default=0)),
                ('communicate', models.FloatField(default=0)),
                ('write', models.FloatField(default=0)),
                ('manage', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='vehicle',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='auth.user')),
                ('skill_num', models.FloatField(default=0)),
                ('land_transport', models.FloatField(default=0)),
                ('water_transport', models.FloatField(default=0)),
                ('fishing', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UserSkill',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='auth.user')),
                ('construct', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='SkillModel.construct', to_field='user_id')),
                ('cutting', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='SkillModel.cutting', to_field='user_id')),
                ('farming', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='SkillModel.farming', to_field='user_id')),
                ('husbandry', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='SkillModel.husbandry', to_field='user_id')),
                ('processing', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='SkillModel.processing', to_field='user_id')),
                ('social', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='SkillModel.social', to_field='user_id')),
                ('vehicle', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='SkillModel.vehicle', to_field='user_id')),
            ],
        ),
    ]
