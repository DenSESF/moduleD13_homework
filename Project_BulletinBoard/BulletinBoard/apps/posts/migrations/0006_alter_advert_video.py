# Generated by Django 4.2.7 on 2023-12-02 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_alter_advert_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advert',
            name='video',
            field=models.FileField(blank=True, upload_to='<property object at 0x000001F0CD401760>/%Y%m%d%H%M%S/'),
        ),
    ]
