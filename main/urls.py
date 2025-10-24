from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('venues/<uuid:id>/', views.show_venue, name='show_venue'),
    path('rate/', views.rate_item, name='rate_item'),
]
