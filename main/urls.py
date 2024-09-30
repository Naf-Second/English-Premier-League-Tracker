from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.fixtureview, name='fixture'),
    path('standings/', views.standing, name='standings'),
    path('stats/', views.stats, name='stats'),
    path('clubs/', views.clubs, name='clubs'),    
    path('update/', views.updategameweek, name='update'),
    path('update2/', views.fetch_premier_league_stats, name='update2'),
    path('update3/', views.squadcreate, name='update3'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
