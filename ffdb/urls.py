from django.urls import path
from . import views

urlpatterns = [
    # ex. /ffdb/
    path('', views.index, name='index'),
    
    # ex. /ffdb/1/
    path('<int:foodItems_id>/', views.detail, name='detail'),
    
    # ex. /ffdb/1/location/
    path('<int:foodItems_id>/location/', views.location, name='location'),
]
    #// ex: /ffdb/1/notes
#//    path('<int:foodItems_id>/notes/', views.notes, name='notes'),