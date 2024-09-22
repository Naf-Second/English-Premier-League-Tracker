# Generated by Django 5.0.6 on 2024-09-03 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='fixture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_team', models.CharField(max_length=50)),
                ('away_team', models.CharField(max_length=50)),
                ('home_score', models.CharField(max_length=10)),
                ('away_score', models.CharField(max_length=10)),
                ('date', models.CharField(max_length=50)),
                ('gameweek', models.IntegerField()),
            ],
        ),
    ]
