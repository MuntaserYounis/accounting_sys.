from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register',views.register),
    path('login',views.login),
    path('logout',views.logout),
    path('main',views.main),
    path('add_car',views.add_car),
    path('adding_car',views.adding_car),
    path('<int:id>/view',views.view),
    path('<int:id>/edit',views.edit),
    path('confirm',views.confirm),
    path('rent_car/<int:id>',views.rent),
    path('rent_thecar',views.rent_thecar),
    path('deliver/<int:id>',views.deliver),

]
