"""league URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""



from django.urls import path
from mission.views import Homeview
from . import views




app_name = 'mission'


urlpatterns = [


    path('', Homeview.as_view(), name='home'),
    path('highscores/', views.highscores, name='highscores'),
    path('mission/', views.missions, name='missions'),
    path('home/', views.home, name='homes'),
    #path('job', views.job, name='job'),



    #url(r'^$', mission.views.home, name='home'),


]
