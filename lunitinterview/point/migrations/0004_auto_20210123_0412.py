# Generated by Django 3.1.5 on 2021-01-22 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('point', '0003_auto_20210123_0356'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contourpoint',
            options={'ordering': ['order']},
        ),
    ]
