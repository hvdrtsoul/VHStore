# Generated by Django 4.2.8 on 2023-12-26 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VHStore', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='image',
            field=models.ImageField(default='media/no-image.png', upload_to='equipment_images/'),
        ),
        migrations.AddField(
            model_name='movie',
            name='image',
            field=models.ImageField(default='media/no-image.png', upload_to='movie_images/'),
        )
    ]
