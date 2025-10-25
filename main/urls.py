from django.urls import path
<<<<<<< HEAD
from . import views  # <-- Keep only this import style
=======
from . import views
>>>>>>> origin/main

app_name = 'main'

urlpatterns = [
<<<<<<< HEAD
    # --- Main & List Pages ---
    path('', views.show_main, name='show_main'),
    path('articles/', views.article_list_view, name='article_list'),

    # --- Detail Pages ---
    path('articles/<uuid:id>', views.show_article, name='show_article'),

    # --- AJAX Form Handling ---
    path('ajax_article_form/', views.ajax_article_form, name='ajax_article_form'), # <-- KEEP THIS LINE

    # --- AJAX Detail/CRUD ---
    path('ajax_event_detail/<uuid:id>/', views.ajax_event_detail, name='ajax_event_detail'),
    path('ajax_delete/<str:type>/<uuid:id>/', views.ajax_delete, name='ajax_delete'),
    path('ajax_edit/<str:type>/<uuid:id>/', views.ajax_edit, name='ajax_edit'),
    path('ajax_cards/', views.ajax_cards, name='ajax_cards'), # For main.html filtering?
    path('rate/', views.rate_item, name='rate_item'),
=======
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
>>>>>>> origin/main
]