from django.urls import path
from . import admin_views as views

app_name = 'main_admin'  # This needs to match the namespace in main urls.py

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),

    # Venues
    path('venues/', views.admin_venues_list, name='admin_venues'),
    path('venues/add/', views.admin_create_venue, name='admin_add_venue'),
    path('venues/edit/<uuid:id>/', views.admin_edit_venue, name='admin_edit_venue'),
    path('venues/delete/<uuid:id>/', views.admin_delete_venue, name='admin_delete_venue'),

    # Articles
    path('articles/', views.admin_articles_list, name='admin_articles'),
    path('articles/add/', views.admin_create_article, name='admin_add_article'),
    path('articles/edit/<uuid:id>/', views.admin_edit_article, name='admin_edit_article'),
    path('articles/delete/<uuid:id>/', views.admin_delete_article, name='admin_delete_article'),

    # Events
    path('events/', views.admin_events_list, name='admin_events'),
    path('events/add/', views.admin_create_event, name='admin_add_event'),
    path('events/edit/<uuid:id>/', views.admin_edit_event, name='admin_edit_event'),
    path('events/delete/<uuid:id>/', views.admin_delete_event, name='admin_delete_event'),
]
