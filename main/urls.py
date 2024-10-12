from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.fixtureview, name='fixture'),
    path('standings/', views.standing, name='standings'),
    path('stats/', views.stats, name='stats'),
    path('clubs/', views.clubs, name='clubs'),  
    path('clubs/<slug:slug>/', views.club_squad, name='club_squad'),  
  #  path('update/', views.updatefixture, name='update'),
    path('update2/', views.fetch_premier_league_stats, name='update2'),
    path('update3/', views.fetch_league_standing, name='update3'),
    
    path('test/', views.squadcreate, name='test'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
