from django.urls import path
from journeyapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('register', views.user_register),
    path('login', views.user_login),
    path('logout', views.user_logout),
    path('profilepic', views.profilepic),
    path('create_log', views.create_log),
    path('read_log', views.read_log),
    path('profile', views.profile_view),
    path('triplog_detail/<rid>', views.triplog_detail),
    path('likes_count/<Log_id>', views.like_count),
    path('show_users', views.show_users),
    path('detail_users/<rid>', views.detail_users),
    path('follow_user/<rid>', views.follow_user),
    
    path('forgot_password', views.forgot_password),
    path('otp_verification', views.otp_verification),
    path('new_password', views.new_password),
    
    
]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)