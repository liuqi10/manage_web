# Generated by Django 2.1.4 on 2019-01-16 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bug_manage', '0004_saveimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='saveimage',
            name='bug_id',
            field=models.CharField(max_length=100, null=True, verbose_name='对应PxBugCount的ID'),
        ),
    ]