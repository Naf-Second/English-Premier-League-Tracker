# Generated by Django 5.0.6 on 2024-10-05 02:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_club_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Standing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_rank', models.IntegerField()),
                ('m_played', models.IntegerField()),
                ('m_won', models.IntegerField()),
                ('m_drawn', models.IntegerField()),
                ('m_lost', models.IntegerField()),
                ('g_forward', models.IntegerField()),
                ('g_against', models.IntegerField()),
                ('g_difference', models.CharField(max_length=5)),
                ('points', models.IntegerField()),
                ('next_match', models.CharField(max_length=100)),
                ('club_logo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='standing_logo', to='main.club')),
                ('club_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='standing_name', to='main.club')),
            ],
        ),
    ]
