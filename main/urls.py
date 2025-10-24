from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.show_main, name='show_main'),
    path('venues/', views.show_venues, name='show_venues'),
    path('articles/', views.article_list, name='article_list'),
    path('events/', views.event_page, name='event_page'),
    path('about/', views.about_view, name='about'),
    path('venues/<uuid:id>/', views.show_venue, name='show_venue'),
    path('ajax_form/venue/', views.ajax_venue_form, name='ajax_venue_form'),
    path('ajax_delete/<str:type>/<uuid:id>/', views.ajax_delete, name='ajax_delete'),
    path('ajax_edit/<str:type>/<uuid:id>/', views.ajax_edit, name='ajax_edit'),
    path('ajax_cards/', views.ajax_cards, name='ajax_cards'),
]