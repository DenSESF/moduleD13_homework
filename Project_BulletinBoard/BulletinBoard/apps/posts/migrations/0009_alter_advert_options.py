# Generated by Django 4.2.7 on 2023-12-04 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_alter_advert_video'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='advert',
            options={'ordering': ('-pk',)},
        ),
    ]