from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.show_main, name='show_main'),
    path('venues/', views.show_venues, name='show_venues'),
    path('venues/<uuid:id>/', views.show_venue, name='show_venue'),
    path('articles/', views.article_list_view, name='article_list'),
    path('articles/<uuid:id>/', views.show_article, name='show_article'),
    path('ajax_article_form/', views.ajax_article_form, name='ajax_article_form'),
    path('ajax_form/venue/', views.ajax_venue_form, name='ajax_venue_form'),
    path('ajax_event_detail/<uuid:id>/', views.ajax_event_detail, name='ajax_event_detail'),
    path('ajax_delete/<str:type>/<uuid:id>/', views.ajax_delete, name='ajax_delete'),
    path('ajax_edit/<str:type>/<uuid:id>/', views.ajax_edit, name='ajax_edit'),
    path('ajax_cards/', views.ajax_cards, name='ajax_cards'),
    path('rate/', views.rate_item, name='rate_item'),
]
