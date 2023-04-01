from django.urls import path

from App_Login import views

app_name = 'App_Login'

urlpatterns = [
     path('register/', views.register, name='register'),
     path('login/', views.login_page, name='login'),
     path('profile/', views.home, name='profile'),
     path('logout/', views.logout_user, name='logout'),
]
