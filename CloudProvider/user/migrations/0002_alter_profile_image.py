# Generated by Django 4.2.7 on 2023-12-10 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='images/default.png', upload_to='images/'),
        ),
    ]
