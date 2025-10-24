from django.urls import path
from . import views  
app_name = 'main'

urlpatterns = [
    path('', views.show_main, name='show_main'),

    # --- Auth URLs ---
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

]