# Generated by Django 2.1.4 on 2019-01-16 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bug_manage', '0003_auto_20190104_1709'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaveImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_url', models.ImageField(upload_to='image')),
            ],
        ),
    ]
