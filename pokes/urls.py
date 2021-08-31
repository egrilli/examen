from django.urls import path
from . import views
urlpatterns = [
    path('', views.vacio),
    path('main', views.registro),
    path('logearse',views.logearse),
    path('pokes',views.pokes),
    path('poke/like/<int:id>', views.pokeLike),
    path('logout',views.logout)
]
