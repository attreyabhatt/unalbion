# Generated by Django 5.2 on 2025-06-06 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animal_artifacts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animalartifactitem',
            name='market_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
