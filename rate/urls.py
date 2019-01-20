from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:slug>/all/', views.all, name='all'),
    path('<slug:slug>/first/', views.first, name='first'),
    path('<slug:slug>/<uuid:uuid>/upvote/', views.upvote, name='upvote'),
    path('<slug:slug>/<uuid:uuid>/downvote/', views.downvote, name='downvote'),
    path('<slug:slug>/<uuid:uuid>/next/', views.next, name='next'),
    path('<slug:slug>/<uuid:uuid>/show/', views.show, name='show'),
]
