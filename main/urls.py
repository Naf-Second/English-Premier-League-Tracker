from django.urls import path
from . import views

urlpatterns = [
    path('', views.fixtureview, name='fixture'),
    path('update/', views.updategameweek, name='update'),
    path('update2/', views.fetch_premier_league_stats, name='update2'),
    path('standings/', views.standing, name='standings'),
    path('stats/', views.stats, name='stats'),
]
