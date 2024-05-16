from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('execute/', views.execute_query, name='execute_query'),
    path('download/', views.download_data, name='download_data'),
]
