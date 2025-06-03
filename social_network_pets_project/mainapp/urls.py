from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomLoginForm


urlpatterns = [
    path('', views.custom_login, name='login'),  
    path('home/', views.home, name='home'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('veterinarian_dashboard/', views.veterinarian_dashboard, name='veterinarian_dashboard'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('pets/', views.pet_list, name='pet_list'),          
    path('pets/new/', views.pet_create, name='pet_create'),  
    path('add_pet/', views.add_pet, name='add_pet'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/new/', views.post_create, name='post_create'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('friendships/', views.friendship_list, name='friendship_list'),
    path('friendships/add/', views.add_friendship, name='add_friendship'),
    path('messages/', views.message_list, name='message_list'),
    path('messages/send/', views.send_message, name='send_message'),
    path('profile/', views.profile, name='profile'),
    path('admin/user/<int:user_id>/edit/', views.user_update, name='user_update'),
    path('dashboard/user/<int:user_id>/edit/', views.user_update, name='user_update'),
    path('dashboard/posts/', views.admin_post_list, name='admin_post_list'),
    path('dashboard/comments/', views.admin_comment_list, name='admin_comment_list'),
    path('dashboard/posts/<int:post_id>/delete/', views.admin_post_delete, name='admin_post_delete'),
    path('dashboard/comments/<int:comment_id>/delete/', views.admin_comment_delete, name='admin_comment_delete'),
    path('dashboard/statistics/', views.admin_statistics, name='admin_statistics'),
    path('advanced_reports/', views.advanced_reports, name='advanced_reports'),

 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)