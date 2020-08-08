# Generated by Django 3.0.8 on 2020-07-22 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mrds', '0002_site'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='com_type',
            field=models.CharField(blank=True, choices=[('B', 'Both'), ('', '----------'), ('N', 'Non-metallic'), ('M', 'Metallic')], default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='site',
            name='dep_id',
            field=models.CharField(blank=True, default='', max_length=255, unique=True),
        ),
    ]