# Generated by Django 2.1.5 on 2019-02-05 08:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20190205_1357'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='students',
            name='newpost',
        ),
        migrations.AddField(
            model_name='newpost',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Students'),
        ),
    ]