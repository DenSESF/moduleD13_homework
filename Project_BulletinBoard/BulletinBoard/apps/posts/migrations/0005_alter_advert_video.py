# Generated by Django 4.2.7 on 2023-12-02 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_alter_advert_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advert',
            name='video',
            field=models.FileField(blank=True, upload_to='<property object at 0x0000021437CC19E0>/%Y%m%d%H%M%S/'),
        ),
    ]
