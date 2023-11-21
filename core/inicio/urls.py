from django.urls import path
from core.inicio import views


app_name = 'index_app'

urlpatterns = [
   path('', views.land_page.as_view(), name="land_page"),
   path('inicio/', views.IndexView.as_view(), name="Index"),
]
