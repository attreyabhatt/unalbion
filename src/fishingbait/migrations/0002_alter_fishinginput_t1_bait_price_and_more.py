# Generated by Django 5.2 on 2025-06-08 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fishingbait', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fishinginput',
            name='t1_bait_price',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='fishinginput',
            name='t3_bait_price',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='fishinginput',
            name='t5_bait_price',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='fishinginput',
            name='worm_price',
            field=models.PositiveIntegerField(),
        ),
    ]
