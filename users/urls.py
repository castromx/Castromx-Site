from .views import *
from django.urls import path

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('profile/', profile, name='profile'),
    path('add_news/', add_news, name='add_news'),
    path('', home, name='home'),
    path('add_like/<int:news_id>/', add_like, name='add_like'),
    path('add_comment/<int:news_id>/', add_comment, name='add_comment'),
    path('profile/<int:user_id>/', user_profile, name='user_profile'),
    path('notifications/', notifications, name='notifications'),
    path('edit_profile/', edit_user_profile, name='edit_user_profile'),
    path('news/<int:pk>/edit/', edit_news, name='edit_news'),
    path('news/<int:pk>/delete/', delete_news, name='delete_news'),
]