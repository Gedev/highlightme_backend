# Generated by Django 4.2.1 on 2024-09-26 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_bosstranslation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='highlightdetails',
            name='boss_name',
            field=models.IntegerField(default=0),
        ),
    ]
