# Generated by Django 3.2.4 on 2021-06-25 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='time',
            field=models.PositiveIntegerField(default=2),
        ),
    ]