# Generated by Django 5.0.6 on 2024-09-27 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_club_club_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='club_logo',
            field=models.ImageField(null=True, upload_to='images/logo'),
        ),
    ]
