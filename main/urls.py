from django.urls import path
from . import views
from . import api_views

app_name = 'main'

urlpatterns = [
    path('', views.show_main, name='show_main'),
    path('venues/', views.show_venues, name='show_venues'),
    path('articles/', views.article_list, name='article_list'),
    path('events/', views.event_page, name='event_page'),
    path('about/', views.about_view, name='about'),
    path('articles/<uuid:id>', views.show_article, name='show_article'),
    path('venues/<uuid:id>/', views.show_venue, name='show_venue'),
    path('events/<uuid:id>', views.show_event, name='show_event'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('ajax_form/venue/', views.ajax_venue_form, name='ajax_venue_form'),
    path('ajax_event_form/', views.ajax_event_form, name='ajax_event_form'),
    path('ajax_article_form/', views.ajax_article_form, name='ajax_article_form'),
    path('ajax_event_detail/<uuid:id>/', views.ajax_event_detail, name='ajax_event_detail'),
    path('ajax_delete/<str:type>/<uuid:id>/', views.ajax_delete, name='ajax_delete'),
    path('ajax_edit/<str:type>/<uuid:id>/', views.ajax_edit, name='ajax_edit'),
    path('ajax_cards/', views.ajax_cards, name='ajax_cards'),
    path('rate/', views.rate_item, name='rate_item'),
    # API endpoints
    path('api/articles/', api_views.ArticleListCreateAPIView.as_view(), name='api_articles'),
    # Flutter endpoints
    path('flutter/create_blog/', views.create_blog_flutter, name='create_blog_flutter'),
    path('flutter/create_event/', views.create_event_flutter, name='create_event_flutter'),
    path('flutter/create_venue/', views.create_venue_flutter, name='create_venue_flutter'),
]
