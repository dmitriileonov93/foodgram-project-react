# Generated by Django 2.2.19 on 2021-11-09 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_follow'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='follow',
            options={'verbose_name': 'Подписки'},
        ),
    ]
