# Generated by Django 5.2.1 on 2025-05-16 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myBoss', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(db_index=True, default='', max_length=255, unique=True, verbose_name='用户名'),
        ),
    ]
