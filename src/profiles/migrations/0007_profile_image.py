# Generated by Django 3.0.4 on 2020-04-07 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_auto_20200403_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='photos/default-avatar.jpg', upload_to='photos'),
        ),
    ]
