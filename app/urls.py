from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),

    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('create/', views.create_post, name='create_post'),
    path('like/<int:id>/', views.like_post, name='like'),
    path('comment/<int:id>/', views.comment_post, name='comment'),

    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),
    path('edit-post/<int:id>/', views.edit_post, name='edit_post'),
]
