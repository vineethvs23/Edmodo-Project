# Generated by Django 2.1.5 on 2019-02-06 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20190205_1404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newpost',
            name='student',
        ),
    ]