# Generated by Django 5.0.6 on 2024-09-27 03:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_matchdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clubs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('club_name', models.CharField(max_length=50)),
                ('club_logo', models.ImageField(null=True, upload_to='images/logo')),
            ],
        ),
        migrations.CreateModel(
            name='Players',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_name', models.CharField(max_length=50)),
                ('club_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.clubs')),
            ],
        ),
        migrations.DeleteModel(
            name='Matchdetails',
        ),
    ]